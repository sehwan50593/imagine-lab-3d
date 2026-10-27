"""자막·배지·제목·HUD 그리기 (PIL). 이전 영상(남자가_한명이라면_3D) 레이아웃 기준, 1080x1920."""
import re
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .common import COLORS, FONT, H, W, clamp, smooth

BADGE_Y = 184
TITLE_Y = 372
LABEL_Y = 346
BIG_Y = 474
SUB_CY = 1590
SUB_W = 980


@lru_cache(maxsize=64)
def font(size, weight=700):
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


TAG = re.compile(r"\{(\w+)\}(.*?)\{/\}", re.S)


def segments(text, default="white"):
    out, pos = [], 0
    for m in TAG.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], default))
        out.append((m.group(2), m.group(1)))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], default))
    return out


def col(name, a=255):
    c = COLORS.get(name, COLORS["white"]) if isinstance(name, str) else name
    return (*c[:3], a)


def text_block(lines, pad=18):
    """lines=[(text, size, weight, default_color, stroke)] → (RGBA 이미지, 각 줄 높이 정보)."""
    rendered = []
    for text, size, weight, dcol, stroke in lines:
        f = font(size, weight)
        segs = segments(text, dcol)
        width = sum(f.getlength(s) for s, _ in segs)
        if width > 1000:  # 화면 폭을 넘으면 글자 크기를 줄임
            size = max(24, int(size * 1000 / width))
            f = font(size, weight)
            width = sum(f.getlength(s) for s, _ in segs)
        asc, desc = f.getmetrics()
        rendered.append((segs, f, width, asc + desc, stroke))
    bw = int(max(r[2] for r in rendered)) + pad * 2 + 16
    gap = 6
    bh = int(sum(r[3] for r in rendered) + gap * (len(rendered) - 1)) + pad * 2
    base = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(base), ImageDraw.Draw(shadow)
    y = pad
    for segs, f, width, lh, stroke in rendered:
        x = (bw - width) / 2
        for s, c in segs:
            ds.text((x, y + 5), s, font=f, fill=(0, 0, 0, 170), stroke_width=stroke + 2,
                    stroke_fill=(0, 0, 0, 170))
            d.text((x, y), s, font=f, fill=col(c), stroke_width=stroke, stroke_fill=(8, 10, 24, 230))
            x += f.getlength(s)
        y += lh + gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    return Image.alpha_composite(shadow, base)


@lru_cache(maxsize=32)
def badge_img(text):
    f = font(34, 700)
    tw = f.getlength(text)
    h, padx = 60, 30
    w = int(tw + padx * 2)
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w + 3, h + 3), radius=h // 2, fill=(10, 14, 34, 150),
                        outline=(255, 255, 255, 235), width=3)
    asc, desc = f.getmetrics()
    d.text((4 + (w - tw) / 2, 4 + (h - asc - desc) / 2 - 1), text, font=f, fill=(255, 255, 255, 255))
    return im


@lru_cache(maxsize=64)
def sub_img(text):
    f = font(44, 600)
    lines = text.split("\n")
    asc, desc = f.getmetrics()
    lh = asc + desc + 12
    h = lh * len(lines) + 44 - 12
    im = Image.new("RGBA", (SUB_W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, SUB_W - 1, h - 1), radius=22, fill=(6, 8, 18, 168))
    y = 22
    for ln in lines:
        segs = segments(ln, "white")
        fl = f
        width = sum(fl.getlength(s) for s, _ in segs)
        if width > SUB_W - 56:  # 상자보다 길면 그 줄만 작게
            fl = font(max(26, int(44 * (SUB_W - 56) / width)), 600)
            width = sum(fl.getlength(s) for s, _ in segs)
        x = (SUB_W - width) / 2
        dy = (f.getmetrics()[0] - fl.getmetrics()[0]) * 0.8
        for s, c in segs:
            d.text((x, y + dy), s, font=fl, fill=col(c))
            x += fl.getlength(s)
        y += lh
    return im


def title_img(beat, big_text):
    lines = []
    if beat.label:
        lines.append((beat.label, 62, 800, beat.label_color, 5))
    if beat.title:
        for ln in beat.title.split("\n"):
            lines.append((ln, beat.title_size, 850, "white", 6))
    if big_text:
        lines.append((big_text, beat.big_size, 900, beat.big_color, 7))
    if beat.note:
        lines.append((beat.note, 44, 700, beat.note_color, 4))
    if not lines:
        return None
    return text_block(lines)


def tag_img(text, color="white", size=30, bg=(8, 12, 30, 190)):
    f = font(size, 700)
    tw = f.getlength(text)
    asc, desc = f.getmetrics()
    w, h = int(tw + 28), asc + desc + 14
    im = Image.new("RGBA", (w + 4, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 2, w + 1, h + 1), radius=h // 2, fill=bg, outline=col(color, 200), width=2)
    cx = (w + 4) / 2
    d.polygon([(cx - 8, h + 1), (cx + 8, h + 1), (cx, h + 13)], fill=bg)
    d.text((2 + 14, 2 + 7 - 1), text, font=f, fill=col(color))
    return im


def paste(dst, im, x, y, alpha=1.0, scale=1.0):
    """dst: float32 HxWx3 (0..1). im: PIL RGBA. (x, y)=붙일 위치의 중심."""
    if im is None or alpha <= 0.003:
        return
    if abs(scale - 1.0) > 1e-3:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    a = np.asarray(im, dtype=np.float32) / 255.0
    x0, y0 = int(round(x - im.width / 2)), int(round(y - im.height / 2))
    x1, y1 = x0 + im.width, y0 + im.height
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x0c, y0c, x1c, y1c = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if x1c <= x0c or y1c <= y0c:
        return
    src = a[sy0:sy0 + (y1c - y0c), sx0:sx0 + (x1c - x0c)]
    al = src[..., 3:4] * alpha
    reg = dst[y0c:y1c, x0c:x1c]
    reg *= (1 - al)
    reg += src[..., :3] * al


def block_alpha(t, t0, t1, fin=0.32, fout=0.28):
    a_in = smooth((t - t0) / fin) if fin > 0 else 1.0
    a_out = smooth((t1 - t) / fout) if fout > 0 else 1.0
    return clamp(min(a_in, a_out))


class Overlay:
    """프레임마다 배지·제목·자막·HUD를 합성."""

    def __init__(self, ep, sim):
        self.ep, self.sim = ep, sim
        self.cache = {}

    def _same(self, a, b, attr):
        return a is not None and b is not None and getattr(a, attr) == getattr(b, attr)

    def draw(self, img, t, anchors):
        ep = self.ep
        beats = ep.BEATS
        # 장면 전환 번쩍임
        for tc, dur, c in getattr(ep, "FLASH", []):
            a = max(0.0, 1.0 - abs(t - tc) / dur)
            if a > 0:
                img *= (1 - a)
                img += np.array(c, np.float32) * a
        # 3D 위치에 붙는 라벨 (말풍선·도시 이름 등)
        if hasattr(ep, "labels"):
            for lb in ep.labels(t, anchors, self.sim):
                im = tag_img(lb["text"], lb.get("color", "white"), lb.get("size", 30))
                paste(img, im, lb["x"], lb["y"] - im.height / 2 - lb.get("lift", 6),
                      alpha=lb.get("alpha", 1.0), scale=lb.get("scale", 1.0))
        # HUD: 시뮬레이션 실행 표시 + 경과 시간
        hud = ep.hud(t, self.sim) if hasattr(ep, "hud") else {}
        self._hud(img, t, hud)
        for i, b in enumerate(beats):
            if not (b.t0 - 0.01 <= t < b.t1 + 0.01):
                continue
            prev = beats[i - 1] if i > 0 else None
            nxt = beats[i + 1] if i + 1 < len(beats) else None
            # 배지: 이전/다음과 같으면 페이드 없이 유지
            fin = 0 if (self._same(prev, b, "badge") and prev.t1 >= b.t0 - 0.05) or b.t0 <= 0 else 0.25
            fout = 0 if self._same(nxt, b, "badge") and nxt.t0 <= b.t1 + 0.05 else 0.22
            if b.badge:
                paste(img, badge_img(b.badge), W / 2, BADGE_Y, block_alpha(t, b.t0, b.t1, fin, fout))
            big = b.big(t, self.sim) if callable(b.big) else b.big
            same_title = lambda o: o is not None and o.title == b.title and o.label == b.label and \
                (o.big == b.big or (callable(o.big) and o.big is b.big)) and o.note == b.note
            fin = 0 if (same_title(prev) and prev.t1 >= b.t0 - 0.05) or b.t0 <= 0 else 0.34
            fout = 0 if same_title(nxt) and nxt.t0 <= b.t1 + 0.05 else 0.26
            key = ("title", b.label, big, b.title, b.note, b.big_size, b.title_size)
            im = self.cache.get(key)
            if im is None:
                im = title_img(b, big)
                if not callable(b.big):
                    self.cache[key] = im
            if im is not None:
                a = block_alpha(t, b.t0, b.t1, fin, fout)
                pop = 1.0 if fin == 0 else 0.94 + 0.06 * smooth((t - b.t0) / 0.32)
                top = 300 if b.label else 318
                paste(img, im, W / 2, top + im.height / 2 - 18, a, pop)
            if b.sub:
                fin = 0 if (self._same(prev, b, "sub") and prev.t1 >= b.t0 - 0.05) or b.t0 <= 0 else 0.25
                fout = 0 if self._same(nxt, b, "sub") and nxt.t0 <= b.t1 + 0.05 else 0.22
                paste(img, sub_img(b.sub), W / 2, SUB_CY, block_alpha(t, b.t0, b.t1, fin, fout))
            break

    def _hud(self, img, t, hud):
        key = ("hud", hud.get("left", "SIM"), hud.get("right", ""), hud.get("right2", ""))
        im = self.cache.get(key)
        if im is None:
            im = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            f = font(26, 700)
            d.text((86, 20), hud.get("left", "SIMULATION"), font=f, fill=(255, 255, 255, 200))
            r = hud.get("right", "")
            if r:
                d.text((W - 60 - f.getlength(r), 20), r, font=f, fill=(255, 255, 255, 210))
            r2 = hud.get("right2", "")
            if r2:
                f2 = font(24, 600)
                d.text((W - 60 - f2.getlength(r2), 58), r2, font=f2, fill=(200, 225, 255, 190))
            if len(self.cache) > 400:
                self.cache.clear()
            self.cache[key] = im
        paste(img, im, W / 2, 115, 1.0)
        # 깜빡이는 실행 표시 점
        on = 0.55 + 0.45 * (0.5 + 0.5 * np.cos(t * 2 * np.pi * 0.9))
        dot = self.cache.get("dot")
        if dot is None:
            dot = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
            dd = ImageDraw.Draw(dot)
            dd.ellipse((8, 8, 32, 32), fill=(255, 70, 70, 120))
            dot = dot.filter(ImageFilter.GaussianBlur(4))
            dd = ImageDraw.Draw(dot)
            dd.ellipse((13, 13, 27, 27), fill=(255, 80, 80, 255))
            self.cache["dot"] = dot
        paste(img, dot, 66, 95 + 2, on)
