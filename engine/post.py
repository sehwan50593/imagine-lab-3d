"""Blender가 렌더한 선형 EXR → 블룸·톤매핑·업스케일 → 자막 합성 → H.264 조각 인코딩."""
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("OPENCV_IO_ENABLE_OPENEXR", "1")
import cv2  # noqa: E402
import numpy as np  # noqa: E402

from .common import FPS, H, W, imread, imwrite  # noqa: E402
from .overlay import Overlay  # noqa: E402


def load_lin(path):
    """Blender EXR(선형, 프리멀티플라이드 RGBA) → float32 HxWx4."""
    import OpenEXR
    with OpenEXR.File(str(path)) as f:
        ch = f.channels()
        if "RGBA" in ch:
            im = ch["RGBA"].pixels
        elif "RGB" in ch:
            rgb = ch["RGB"].pixels
            im = np.concatenate([rgb, np.ones(rgb.shape[:2] + (1,), rgb.dtype)], 2)
        else:
            im = np.stack([ch[k].pixels for k in ("R", "G", "B", "A") if k in ch], -1)
    im = np.asarray(im, np.float32)
    if im.shape[2] == 3:
        im = np.concatenate([im, np.ones(im.shape[:2] + (1,), np.float32)], 2)
    return np.ascontiguousarray(im)


def bloom(lin, thr=0.9, strength=0.32, radius=1.0):
    lum = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    k = np.clip(lum - thr, 0, None) / np.maximum(lum, 1e-4)
    bright = np.minimum(lin * k[..., None], 40.0)
    h, w = lin.shape[:2]
    acc = np.zeros_like(lin)
    cur = bright
    weights = (0.55, 0.75, 0.95, 1.0, 0.9)
    for i, wgt in enumerate(weights):
        nw, nh = max(2, w >> (i + 2)), max(2, h >> (i + 2))
        cur = cv2.resize(cur, (nw, nh), interpolation=cv2.INTER_AREA)
        bl = cv2.GaussianBlur(cur, (0, 0), 1.6 * radius)
        acc += cv2.resize(bl, (w, h), interpolation=cv2.INTER_LINEAR) * wgt
    return lin + acc * strength


def aces(x):
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)


def srgb(x):
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.maximum(x, 1e-8), 1 / 2.4) - 0.055)


_VIG = {}


def vignette(h, w, amount):
    key = (h, w, amount)
    if key not in _VIG:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        nx, ny = (xx / w - 0.5) * 2, (yy / h - 0.5) * 2 * (h / w) * 0.62
        r2 = nx * nx + ny * ny
        _VIG[key] = (1 - amount * np.clip(r2 - 0.25, 0, None) ** 1.1)[..., None].astype(np.float32)
    return _VIG[key]


class Sky:
    """카메라 회전을 따라 움직이는 별 + 남색 그라데이션 (선형 값)."""

    def __init__(self, grade):
        g = grade or {}
        rs = np.random.default_rng(g.get("star_seed", 5))
        n = g.get("stars", 2600)
        d = rs.normal(size=(n, 3))
        self.dirs = (d / np.linalg.norm(d, axis=1, keepdims=True)).astype(np.float32)
        mag = rs.random(n) ** 6
        self.bright = (0.05 + 2.6 * mag).astype(np.float32) * g.get("star_gain", 1.0)
        tint = rs.random(n)
        self.col = np.stack([0.85 + 0.15 * tint, 0.9 + 0.05 * tint, 1.0 - 0.12 * tint], 1).astype(np.float32)
        top = np.array(g.get("sky_top", (0.0045, 0.0065, 0.022)), np.float32)
        bot = np.array(g.get("sky_bottom", (0.0018, 0.0025, 0.009)), np.float32)
        yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        self.grad = np.broadcast_to(top * (1 - yy) + bot * yy, (H, W, 3)).copy()
        glow = np.array(g.get("sky_glow", (0.004, 0.006, 0.016)), np.float32)
        yy2, xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
        r2 = ((xx2 - W / 2) / W) ** 2 + ((yy2 - H * 0.52) / H * 0.9) ** 2
        self.grad += glow * np.exp(-r2 * 7.0)[..., None]

    def render(self, cam):
        img = self.grad.copy()
        if cam is None:
            return img
        m = np.array(cam[:16], np.float32).reshape(4, 4)
        lens, sh = cam[16], cam[17]
        rot = m[:3, :3]
        dc = self.dirs @ rot  # 월드 → 카메라 (회전행렬 전치)
        z = -dc[:, 2]
        vis = z > 1e-3
        f = lens / sh * H
        x = W / 2 + dc[vis, 0] / z[vis] * f
        y = H / 2 - dc[vis, 1] / z[vis] * f
        b = self.bright[vis, None] * self.col[vis]
        ok = (x >= 1) & (x < W - 2) & (y >= 1) & (y < H - 2)
        x, y, b = x[ok], y[ok], b[ok]
        x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
        fx, fy = (x - x0)[:, None], (y - y0)[:, None]
        layer = np.zeros((H, W, 3), np.float32)
        for dx, dy, wgt in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
            np.add.at(layer, (y0 + dy, x0 + dx), b * wgt)
        layer = cv2.GaussianBlur(layer, (0, 0), 0.75) * 2.2
        return img + layer


def finish(rgba, grade, sky, cam):
    g = grade or {}
    up = cv2.resize(rgba, (W, H), interpolation=cv2.INTER_CUBIC) if rgba.shape[1] != W else rgba
    a = np.clip(up[..., 3:4], 0, 1)
    x = np.maximum(up[..., :3], 0) + sky.render(cam) * (1 - a)
    x = bloom(x, g.get("bloom_thr", 0.9), g.get("bloom", 0.32), g.get("bloom_radius", 1.0))
    x = aces(x * g.get("exposure", 0.9))
    x = srgb(x)
    x = x * vignette(x.shape[0], x.shape[1], g.get("vignette", 0.35))
    return np.clip(x, 0, 1)


def ffmpeg_writer(out, fps=FPS):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-g", "60", "-bf", "2",
           "-x264-params", "keyint=60:min-keyint=60:scenecut=0", str(out)]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def load_anchors(in_dir):
    p = Path(in_dir) / "anchors.json"
    if not p.exists():
        return {}, {}
    raw = json.load(open(p, encoding="utf-8"))
    out, cams = {}, {}
    for f, items in raw.items():
        cams[int(f)] = items.pop("_cam", None)
        out[int(f)] = {k: (v[0] * W, (1 - v[1]) * H, v[2], v[3]) for k, v in items.items()}
    return out, cams


def run(ep, sim, frames, in_dir, out, preview=False):
    in_dir, out = Path(in_dir), Path(out)
    ov = Overlay(ep, sim)
    anchors, cams = load_anchors(in_dir)
    grade = getattr(ep, "GRADE", {})
    sky = Sky(grade)
    writer = None if preview else ffmpeg_writer(out)
    shots = []
    for f in frames:
        lin = load_lin(in_dir / f"{f:05d}.exr")
        img = finish(lin, grade, sky, cams.get(f)).astype(np.float32)
        ov.draw(img, f / FPS, anchors.get(f, {}))
        u8 = (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)
        if writer:
            writer.stdin.write(u8.tobytes())
        else:
            shots.append((f, u8))
    if writer:
        writer.stdin.close()
        if writer.wait() != 0:
            raise RuntimeError("ffmpeg 인코딩 실패")
    else:
        out.mkdir(parents=True, exist_ok=True)
        for f, u8 in shots:
            imwrite(out / f"{f:05d}.jpg", u8[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 92])
        contact(shots, out / "contact.jpg")


def contact(shots, path, cols=6, tw=270):
    if not shots:
        return
    th = int(tw * H / W)
    rows = (len(shots) + cols - 1) // cols
    sheet = np.zeros((rows * (th + 4), cols * (tw + 4), 3), np.uint8)
    for i, (f, u8) in enumerate(shots):
        r, c = divmod(i, cols)
        sm = cv2.resize(u8, (tw, th), interpolation=cv2.INTER_AREA)
        cv2.putText(sm, f"{f / FPS:.1f}s", (6, th - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (0, 255, 255), 1, cv2.LINE_AA)
        sheet[r * (th + 4):r * (th + 4) + th, c * (tw + 4):c * (tw + 4) + tw] = sm
    imwrite(path, sheet[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 88])


if __name__ == "__main__":
    sys.exit("engine.run 을 사용하세요")
