"""잠실 시점 점검 (배포 안 함)."""
import numpy as np

from engine.common import FPS, Beat, frames_of
from engine.jamsil import PathWalkers, geometry

DUR = 2.0
META = {"id": "ep00j", "title": "잠실 테스트", "duration": DUR, "music": {}}
BEATS = [Beat(0, 2.0, badge="잠실", title="잠실 3인칭 시점")]
GRADE = {"exposure": 0.95, "bloom": 0.22, "bloom_thr": 1.2}
NP, NC = 600, 160


def sky(t):
    return (0.18, 0.32, 0.62), (0.55, 0.65, 0.8), 0.0


def simulate(build_dir):
    g = geometry()
    rs = np.random.default_rng(1)
    nf = frames_of(DUR)
    lines = [g["wl_p"][a:b] for a, b in zip(g["wl_o"][:-1], g["wl_o"][1:])]
    clines = [g["cl_p"][a:b] for a, b in zip(g["cl_o"][:-1], g["cl_o"][1:])]
    pw = PathWalkers(rs, lines, NP, rs.uniform(1.1, 1.6, NP), offset=0.6, near=(130, -95), near_r=220)
    cw = PathWalkers(rs, clines, NC, rs.uniform(9, 14, NC), offset=3.5, near=(-120, -200), near_r=900)
    pp = np.zeros((nf, NP, 2), np.float32)
    py = np.zeros((nf, NP), np.float32)
    cp = np.zeros((nf, NC, 2), np.float32)
    cy = np.zeros((nf, NC), np.float32)
    for i in range(nf):
        pp[i], py[i] = pw.step(1 / FPS)
        cp[i], cy[i] = cw.step(1 / FPS)
    return dict(pp=pp, py=py, cp=cp, cy=cy, shirt=rs.uniform(0.1, 0.95, (NP, 3)).astype(np.float32),
                pants=rs.uniform(0.05, 0.35, (NP, 3)).astype(np.float32),
                ccol=np.array([(0.8, 0.8, 0.82), (0.08, 0.08, 0.1), (0.6, 0.1, 0.1), (0.2, 0.3, 0.6)],
                              np.float32)[rs.integers(0, 4, NC)])


def build(ctx):
    import math
    from engine.jamsil import Jamsil
    sim = ctx.sim
    J = Jamsil(ctx, geometry())
    J.sun.rotation_euler = (math.radians(50), 0, math.radians(-30))
    J.sun.data.energy = 3.2
    ctx.set_ctl("lights", 0.15)
    po = J.people(NP)
    co = J.cars(NC)

    def upd(t, f):
        tg = (130, -95, 3)
        J.cam.set(tg, 322, (26, 16, 40)[f % 3], (42, 26, 120)[f % 3], 30, shift=0.05)
        ph = (t * 1.8 + np.arange(NP) * 0.37) % 1.0
        pose = 1 + np.floor(ph * 4) % 4
        ctx.K = None
        from engine import bkit as K
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(NP)], scale=np.ones(NP), rot=np.c_[np.zeros((NP, 2)), sim["py"][f]],
                     col=sim["shirt"], colors={"col2": sim["pants"]}, pose=pose)
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])
    ctx.on_frame(upd)
