"""Blender 안에서 실행: 에피소드 장면을 만들고 지정 프레임을 EXR로 렌더.

blender -b --factory-startup --python-exit-code 1 -P engine/blender_main.py -- \
    --ep ep01_cats --frames 0-599 --out build/ep01_cats/frames --pct 67 --samples 24 --device CPU
"""
import argparse
import importlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import bpy  # noqa: E402
import numpy as np  # noqa: E402

from engine import bkit  # noqa: E402
from engine.common import BUILD, FPS  # noqa: E402


def parse_frames(spec):
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" in part:  # a-b:step
            rng_, step = part.split(":")
            a, b = rng_.split("-")
            out += list(range(int(a), int(b) + 1, int(step)))
        elif "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(set(out))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    ap.add_argument("--frames", default="0")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pct", type=int, default=67)
    ap.add_argument("--samples", type=int, default=24)
    ap.add_argument("--device", default="CPU")
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--save-blend", default="")
    a = ap.parse_args(argv)

    ep = importlib.import_module("episodes." + a.ep)
    build_dir = BUILD / a.ep
    sim = dict(np.load(build_dir / "sim.npz", allow_pickle=False))
    bkit.reset()
    ctx = bkit.Ctx(sim, a, build_dir)
    t0 = time.time()
    ep.build(ctx)
    bkit.configure(ctx.scene, a.pct, a.samples, a.device)
    if a.threads:
        ctx.scene.render.threads_mode = "FIXED"
        ctx.scene.render.threads = a.threads
    print(f"[build] {time.time() - t0:.1f}s", flush=True)
    if a.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=a.save_blend)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    anchors_path = out / "anchors.json"
    anchors = json.load(open(anchors_path)) if anchors_path.exists() else {}
    frames = parse_frames(a.frames)
    for i, f in enumerate(frames):
        t = f / FPS
        tf = time.time()
        ctx.scene.frame_set(f)
        for fn in ctx.updaters:
            fn(t, f)
        bpy.context.view_layer.update()
        an = ctx.anchors(t)
        cam = ctx.scene.camera
        mw = [v for row in cam.matrix_world for v in row]
        an["_cam"] = [round(v, 6) for v in mw] + [cam.data.lens, cam.data.sensor_height]
        anchors[str(f)] = an
        ctx.scene.render.filepath = str(out / f"{f:05d}.exr")
        bpy.ops.render.render(write_still=True)
        print(f"[frame] {f} ({i + 1}/{len(frames)}) {time.time() - tf:.2f}s", flush=True)
        if i % 20 == 0 or i == len(frames) - 1:
            json.dump(anchors, open(anchors_path, "w"))
    json.dump(anchors, open(anchors_path, "w"))


try:
    main()
except Exception:
    import traceback
    traceback.print_exc()
    sys.exit(1)
