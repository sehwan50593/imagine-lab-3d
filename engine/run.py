"""파이프라인 명령 모음 (일반 파이썬).

python -m engine.run sim ep01_cats
python -m engine.run post ep01_cats --frames 0-599 --out build/ep01_cats/chunk_0.mp4
python -m engine.run preview ep01_cats --frames 0-1679:60 --out build/ep01_cats/preview
python -m engine.run music ep01_cats
python -m engine.run assemble ep01_cats --chunks a.mp4 b.mp4 --out final.mp4
python -m engine.run plan --episodes all --chunks 3 --mode full
python -m engine.run blender ep01_cats --frames 0-30:10 --blender <path> --device GPU   (로컬 확인용)
"""
import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

from .common import BUILD, FPS, ROOT, frames_of


def episodes_all():
    return sorted(p.stem for p in (ROOT / "episodes").glob("ep[0-9][0-9]_*.py") if not p.stem.startswith("ep00"))


def load_ep(name):
    return importlib.import_module("episodes." + name)


def bdir(name):
    d = BUILD / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_sim(name):
    return dict(np.load(bdir(name) / "sim.npz", allow_pickle=False))


def cmd_sim(a):
    ep = load_ep(a.ep)
    sim = ep.simulate(bdir(a.ep))
    np.savez(bdir(a.ep) / "sim.npz", **{k: np.asarray(v) for k, v in sim.items()})
    print("sim ok", a.ep, {k: np.asarray(v).shape for k, v in sim.items()})


def _parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            r, st = part.split(":")
            x, y = r.split("-")
            out += list(range(int(x), int(y) + 1, int(st)))
        elif "-" in part:
            x, y = part.split("-")
            out += list(range(int(x), int(y) + 1))
        elif part:
            out.append(int(part))
    return sorted(set(out))


def cmd_post(a, preview=False):
    from . import post
    ep = load_ep(a.ep)
    frames = _parse(a.frames)
    in_dir = Path(a.inp) if a.inp else bdir(a.ep) / "frames"
    post.run(ep, load_sim(a.ep), frames, in_dir, Path(a.out), preview=preview)
    print("post ok", a.out)


def cmd_music(a):
    from . import music
    ep = load_ep(a.ep)
    out = music.make(ep.META, ep.META["duration"], bdir(a.ep))
    print("music ok", out)


def cmd_assemble(a):
    d = bdir(a.ep)
    lst = d / "chunks.txt"
    lst.write_text("".join(f"file '{Path(c).resolve().as_posix()}'\n" for c in a.chunks), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    str(d / "video.mp4")], check=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    music = d / "music.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "video.mp4"), "-i", str(music), "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart",
                    str(a.out)], check=True)
    print("assemble ok", a.out)


def cmd_plan(a):
    eps = episodes_all() if a.episodes == "all" else [e.strip() for e in a.episodes.split(",")]
    jobs = []
    for e in eps:
        meta = load_ep(e).META
        n = frames_of(meta["duration"])
        rd = {"pct": 67, "samples": 10, "bounces": 2, "chunks": a.chunks}
        rd.update(meta.get("render", {}))
        if a.mode == "preview":
            jobs.append({"ep": e, "part": 0, "frames": f"0-{n - 1}:{a.step}", "pct": 40, "samples": 6, "bounces": 2})
            continue
        k = max(1, int(rd["chunks"]))
        size = (n + k - 1) // k
        for i in range(k):
            s, t = i * size, min(n, (i + 1) * size) - 1
            if s <= t:
                jobs.append({"ep": e, "part": i, "frames": f"{s}-{t}", "pct": rd["pct"], "samples": rd["samples"],
                             "bounces": rd["bounces"]})
    if a.gh:
        print("matrix=" + json.dumps({"include": jobs}))
        print("eps=" + json.dumps(eps))
    else:
        print(json.dumps({"include": jobs}))


def cmd_blender(a):
    exe = a.blender
    out = Path(a.out) if a.out else bdir(a.ep) / "frames"
    cmd = [exe, "-b", "--factory-startup", "--python-exit-code", "1", "-P", str(ROOT / "engine" / "blender_main.py"),
           "--", "--ep", a.ep, "--frames", a.frames, "--out", str(out), "--pct", str(a.pct),
           "--samples", str(a.samples), "--device", a.device]
    if a.save_blend:
        cmd += ["--save-blend", a.save_blend]
    r = subprocess.run(cmd)
    sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("sim")
    p.add_argument("ep")
    for name in ("post", "preview"):
        p = sp.add_parser(name)
        p.add_argument("ep")
        p.add_argument("--frames", required=True)
        p.add_argument("--inp", default="")
        p.add_argument("--out", required=True)
    p = sp.add_parser("music")
    p.add_argument("ep")
    p = sp.add_parser("assemble")
    p.add_argument("ep")
    p.add_argument("--chunks", nargs="+", required=True)
    p.add_argument("--out", required=True)
    p = sp.add_parser("plan")
    p.add_argument("--episodes", default="all")
    p.add_argument("--chunks", type=int, default=3)
    p.add_argument("--mode", default="full")
    p.add_argument("--step", type=int, default=60)
    p.add_argument("--gh", action="store_true")
    p = sp.add_parser("blender")
    p.add_argument("ep")
    p.add_argument("--frames", default="0")
    p.add_argument("--blender", required=True)
    p.add_argument("--out", default="")
    p.add_argument("--pct", type=int, default=33)
    p.add_argument("--samples", type=int, default=8)
    p.add_argument("--device", default="GPU")
    p.add_argument("--save-blend", default="")
    a = ap.parse_args()
    if a.cmd == "sim":
        cmd_sim(a)
    elif a.cmd == "post":
        cmd_post(a)
    elif a.cmd == "preview":
        cmd_post(a, preview=True)
    elif a.cmd == "music":
        cmd_music(a)
    elif a.cmd == "assemble":
        cmd_assemble(a)
    elif a.cmd == "plan":
        cmd_plan(a)
    elif a.cmd == "blender":
        cmd_blender(a)


if __name__ == "__main__":
    main()
