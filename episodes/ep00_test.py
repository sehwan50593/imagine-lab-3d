"""엔진 점검용 장면 (배포 안 함)."""
import numpy as np

from engine.common import ASSETS, Beat

META = {"id": "ep00", "title": "테스트", "duration": 2.0, "music": {"key": "F", "seed": 3}}
BEATS = [Beat(0, 2.0, badge="D-DAY", label="고양이", big="6억 마리", sub="엔진 점검용 {orange}테스트{/} 장면입니다.\n두 번째 줄")]
GRADE = {}


def simulate(build_dir):
    from engine.tex import elev_png
    elev_png(build_dir / "elev.png")
    rs = np.random.default_rng(1)
    return {"cat_xy": rs.uniform(-6, 6, (40, 2))}


def hud(t, sim):
    return {"left": "SIMULATION", "right": f"경과 {t:.1f}초"}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("cat0")
    if a and a[3]:
        out.append({"x": a[0], "y": a[1], "text": "야옹", "color": "yellow"})
    return out


def build(ctx):
    from engine import bkit as K
    K.world_space(ctx)
    K.sun(ctx, 3.0, rot=(48, 0, 40))
    gm = K.mat_ground(ctx, river=(0.25, -3.0, 1.4, 0.6))
    K.island(ctx, 10, top_mat=gm)
    lay = K.city_layout(10, river=(0.25, -3.0, 1.4, 0.6), seed=4)
    bm = K.mat_building(ctx)
    pb = K.proto_box(ctx, bm)
    bi = K.instancer(ctx, "blds", pb, len(lay), vector_scale=True)
    K.add_attr(bi, "lit")
    K.add_attr(bi, "seed")
    arr = np.array(lay, np.float32)
    rs = np.random.default_rng(2)
    cols = np.array([(0.55, 0.55, 0.58), (0.62, 0.58, 0.52), (0.45, 0.48, 0.55), (0.7, 0.68, 0.64)])[rs.integers(0, 4, len(arr))]
    K.set_points(bi, np.c_[arr[:, 0], arr[:, 1], np.zeros(len(arr))], scale=np.ones(len(arr)),
                 size=arr[:, 2:5], rot=np.zeros((len(arr), 3)), col=cols, lit=rs.uniform(0.2, 0.9, len(arr)),
                 seed=rs.uniform(0, 100, len(arr)))
    fur = K.mat_inst("m_fur", 0.7)
    eye = K.mat_emit("m_eye", (0.9, 1.0, 0.4), 3.0)
    pc = K.proto_cat(ctx, fur, eye)
    ci = K.instancer(ctx, "cats", pc, 40)
    xy = ctx.sim["cat_xy"]
    K.set_points(ci, np.c_[xy, np.zeros(40)], scale=np.full(40, 2.0), rot=np.c_[np.zeros((40, 2)), rs.uniform(0, 6.28, 40)],
                 col=np.tile((0.9, 0.5, 0.15), (40, 1)))
    leaf = K.mat_inst("m_leaf", 0.8)
    trunk = K.mat_simple("m_trunk", (0.25, 0.15, 0.08), 0.9)
    pt = K.proto_tree(ctx, leaf, trunk)
    ti = K.instancer(ctx, "trees", pt, 60)
    txy = rs.uniform(-8, 8, (60, 2))
    K.set_points(ti, np.c_[txy, np.zeros(60)], scale=rs.uniform(0.8, 1.4, 60), rot=np.zeros((60, 3)),
                 col=np.tile((0.15, 0.4, 0.12), (60, 1)))
    g, at = K.globe(ctx, 2.0, tex=ASSETS / "geo" / "land_mask.png", elev=ctx.build_dir / "elev.png",
                    ice=ASSETS / "geo" / "ice_mask.png", borders=ASSETS / "geo" / "borders_rank.png")
    g.location = at.location = (0, 0, 9)
    mk = K.mat_emit("m_mk", (1, 0.2, 0.2), 20)
    seoul = K.latlon_to_xyz(37.5, 127.0, 2.02) + np.array([0, 0, 9])
    K.mesh_obj("seoul", K.bm_sphere(0.05, tuple(seoul)), mk)
    cam = K.CamRig(ctx, 30)

    def upd(t, f):
        cam.set((0, 0, 1.5), 30 + t * 10, 32, 36)
    ctx.on_frame(upd)
    ctx.anchor("cat0", lambda t: (float(xy[0, 0]), float(xy[0, 1]), 0.8))
