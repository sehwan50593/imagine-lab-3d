"""목표점을 가리지 않는 관찰 위치 찾기: python tools/find_eye.py <area> tx ty tz [dist...]"""
import math
import sys

import numpy as np

sys.path.insert(0, ".")
from engine.jamsil import geometry, use_area  # noqa: E402

use_area(sys.argv[1])
g = geometry()
bv, bf, bfs, bid = g["bv"], g["bf"], g["bfs"], g["bfid"]
st = np.r_[0, np.cumsum(bfs)[:-1]]
# 건물 윗면(가로 면)만 다각형으로
polys = []
for s0, n, b in zip(st, bfs, bid):
    p = bv[bf[s0:s0 + n]]
    if n >= 3 and np.ptp(p[:, 2]) < 0.1 and p[0, 2] > 1:
        polys.append((p[:, :2], float(p[0, 2])))


def inside(poly, x, y):
    xs, ys = poly[:, 0], poly[:, 1]
    xj, yj = np.roll(xs, 1), np.roll(ys, 1)
    c = ((ys > y) != (yj > y)) & (x < (xj - xs) * (y - ys) / (yj - ys + 1e-12) + xs)
    return bool(c.sum() % 2)


paths = [(p, h, p.min(0), p.max(0)) for p, h in polys]


def blocked(a, b):
    for u in np.linspace(0.0, 0.97, 120):
        q = a + (b - a) * u
        for pa, h, lo, hi in paths:
            if h > q[2] and lo[0] <= q[0] <= hi[0] and lo[1] <= q[1] <= hi[1] and inside(pa, q[0], q[1]):
                return True
    return False


T = np.array([float(v) for v in sys.argv[2:5]])
dists = [float(v) for v in sys.argv[5:]] or [90, 120]
for d in dists:
    for el in (12, 16, 20, 25):
        ok = []
        for az in range(0, 360, 15):
            a, e = math.radians(az), math.radians(el)
            E = T + np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)]) * d
            if not blocked(E, T):
                ok.append(az)
        print(f"dist {d} el {el}: clear az {ok}")
