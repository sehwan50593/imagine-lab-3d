"""잠실 편 공통: 군중·차·조명·하늘·카메라 (EP03 법 / EP07 집 / EP09 AI / EP10 고디바 모찌)."""
import math

import numpy as np

from .common import FPS, keyed
from .jamsil import PathWalkers, geometry

# 자주 쓰는 촬영 지점 (타워 = 원점, m)
LAKE = (130.0, -95.0, 3.0)        # 석촌호수 북서쪽 산책로
TOWER = (14.0, -6.0, 0.0)
MALL = (-41.0, 20.0, 0.0)         # 롯데월드몰
OLYMPIC_RD = (-300.0, 160.0, 0.0)  # 올림픽로 근처 아파트 단지

DAY = dict(elev=42, az=-30, energy=3.4, col=(1.0, 0.95, 0.86), amb=0.45, amb_col=(0.50, 0.60, 0.80))
MORNING = dict(elev=16, az=-80, energy=2.8, col=(1.0, 0.80, 0.60), amb=0.32, amb_col=(0.45, 0.50, 0.72))
DUSK = dict(elev=5, az=100, energy=1.8, col=(1.0, 0.50, 0.26), amb=0.18, amb_col=(0.32, 0.27, 0.48))
NIGHT = dict(elev=50, az=160, energy=0.35, col=(0.55, 0.65, 1.0), amb=0.06, amb_col=(0.10, 0.13, 0.28))
SKIES = {"DAY": ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0), "MORNING": ((0.20, 0.30, 0.55), (0.75, 0.62, 0.52), 0.0),
         "DUSK": ((0.05, 0.06, 0.18), (0.55, 0.28, 0.18), 0.25), "NIGHT": ((0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0)}
PRESETS = {"DAY": DAY, "MORNING": MORNING, "DUSK": DUSK, "NIGHT": NIGHT}


def sky_at(t, keys):
    """keys=[(t, 'DAY'|...)] → (위색, 아래색, 별 밝기) 보간."""
    ks = [(a, (*SKIES[b][0], *SKIES[b][1], SKIES[b][2])) for a, b in keys]
    v = keyed(t, ks)
    return v[0:3], v[3:6], v[6]


def light_keys(keys):
    return [(a, PRESETS[b]) for a, b in keys]


def lines_of(g, kind="walk"):
    p, o = (g["wl_p"], g["wl_o"]) if kind == "walk" else (g["cl_p"], g["cl_o"])
    return [p[a:b] for a, b in zip(o[:-1], o[1:])]


def crowd(rs, nf, n, near, near_r, speed=(1.1, 1.6), offset=0.7, t_speed=None):
    """보행로 위를 걷는 사람들 → 위치·방향·걷기 위상(자세)."""
    g = geometry()
    pw = PathWalkers(rs, lines_of(g, "walk"), n, rs.uniform(*speed, n), offset=offset, near=near, near_r=near_r)
    pp = np.zeros((nf, n, 2), np.float32)
    py = np.zeros((nf, n), np.float32)
    ph = np.zeros((nf, n), np.float32)
    phase = rs.random(n)
    for i in range(nf):
        mul = 1.0 if t_speed is None else t_speed(i / FPS)
        pp[i], py[i] = pw.step(1 / FPS, mul)
        phase = (phase + pw.speed * mul / FPS / 1.4) % 1.0
        ph[i] = phase
    return pp, py, ph


def traffic(rs, nf, n, near, near_r, speed=(9, 14), stop=None):
    g = geometry()
    cw = PathWalkers(rs, lines_of(g, "car"), n, rs.uniform(*speed, n), offset=3.2, near=near, near_r=near_r)
    cp = np.zeros((nf, n, 2), np.float32)
    cy = np.zeros((nf, n), np.float32)
    for i in range(nf):
        mul = 1.0 if stop is None else stop(i / FPS)
        cp[i], cy[i] = cw.step(1 / FPS, mul)
    return cp, cy


def pose_of(phase, moving=None):
    p = 1 + np.floor(phase * 4) % 4
    if moving is not None:
        p = np.where(moving, p, 0)
    return p.astype(np.float32)


def people_colors(rs, n):
    shirts = np.array([(0.85, 0.85, 0.85), (0.12, 0.12, 0.14), (0.2, 0.35, 0.7), (0.75, 0.2, 0.2), (0.85, 0.7, 0.3),
                       (0.3, 0.55, 0.35), (0.6, 0.45, 0.7), (0.9, 0.55, 0.65)], np.float32)
    pants = np.array([(0.08, 0.09, 0.12), (0.18, 0.22, 0.35), (0.35, 0.32, 0.28), (0.1, 0.1, 0.1)], np.float32)
    return shirts[rs.integers(0, len(shirts), n)], pants[rs.integers(0, len(pants), n)]


CAR_COLORS = np.array([(0.85, 0.85, 0.87), (0.06, 0.06, 0.07), (0.45, 0.47, 0.5), (0.55, 0.08, 0.08),
                       (0.12, 0.2, 0.45)], np.float32)


def cam_keys_eval(t, keys):
    """keys=[(t, (x,y,z), az, el, dist, lens)]"""
    ks = [(k[0], (*k[1], k[2], k[3], k[4], k[5])) for k in keys]
    v = keyed(t, ks)
    return v[:3], v[3], v[4], v[5], v[6]


def set_cam(J, t, keys, drift=0.8):
    tgt, az, el, dist, lens = cam_keys_eval(t, keys)
    J.cam.set(tgt, az + t * drift, el, dist, lens, shift=0.04)
