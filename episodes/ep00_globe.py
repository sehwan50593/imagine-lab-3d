"""지구본 점검용 (배포 안 함)."""
import numpy as np

from engine.common import ASSETS, Beat

META = {"id": "ep00g", "title": "지구본 테스트", "duration": 2.0, "music": {}}
BEATS = [Beat(0, 2.0, badge="TEST")]
GRADE = {}


def simulate(build_dir):
    from engine.tex import elev_png
    if not (build_dir / "elev.png").exists():
        elev_png(build_dir / "elev.png")
    return {"x": np.zeros(1)}


def build(ctx):
    from engine import bkit as K
    K.world_space(ctx, ambient=(0.3, 0.35, 0.5), ambient_strength=0.25)
    sun = K.sun(ctx, 3.0, rot=(60, 0, 120))
    g, at = K.globe(ctx, 4.0, tex=ASSETS / "geo" / "land_mask.png", elev=ctx.build_dir / "elev.png",
                    ice=ASSETS / "geo" / "ice_mask.png", borders=ASSETS / "geo" / "borders_rank.png")
    at.hide_render = True
    mk = K.mat_emit("m_mk", (1, 0.2, 0.2), 30)
    for lat, lon in ((37.5, 127.0), (51.5, 0.0), (40.7, -74.0), (-33.9, 151.2)):
        p = K.latlon_to_xyz(lat, lon, 4.03)
        K.mesh_obj("mk", K.bm_sphere(0.06, tuple(p)), mk)
    cam = K.CamRig(ctx, 50, fstop=0)
    seoul = K.latlon_to_xyz(30.0, 127.0, 1.0)

    def upd(t, f):
        az = float(np.degrees(np.arctan2(seoul[1], seoul[0])))
        cam.set((0, 0, 0), az + (f % 3) * 70, 25, 16)
    ctx.on_frame(upd)
