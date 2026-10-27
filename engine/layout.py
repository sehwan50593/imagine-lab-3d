"""도시 배치·에이전트 이동 (순수 numpy, 시뮬레이션 단계에서 실행 → sim.npz 로 Blender에 전달)."""
import math

import numpy as np


def river_y(x, river):
    k, b0, wdt, amp = river
    return k * x + b0 + amp * np.sin(0.35 * x)


def city_layout(rs, R, spacing=3.2, road_w=0.62, river=None, margin=0.9, hmin=0.5, hmax=4.5,
                center_boost=1.6, keep=None):
    """도로 격자 사이 블록에 건물 → array (N, 5): x, y, w, d, h."""
    out = []
    n = int(R / spacing) + 2
    inner = spacing - road_w - 0.5
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            cx, cy = (i + 0.5) * spacing, (j + 0.5) * spacing
            k = int(rs.choice([1, 2, 2, 3, 4]))
            if k == 1:
                subs = [(0, 0, inner, inner)]
            elif k == 2:
                subs = [(-inner / 4, 0, inner / 2 - 0.08, inner), (inner / 4, 0, inner / 2 - 0.08, inner)]
            elif k == 3:
                q = inner / 2 - 0.08
                subs = [(-inner / 4, -inner / 4, q, q), (inner / 4, -inner / 4, q, q), (0, inner / 4, inner - 0.08, q)]
            else:
                q = inner / 2 - 0.08
                subs = [(sx * inner / 4, sy * inner / 4, q, q) for sx in (-1, 1) for sy in (-1, 1)]
            for ox, oy, w, d in subs:
                x, y = cx + ox, cy + oy
                if math.hypot(x, y) + max(w, d) * 0.7 > R - margin:
                    continue
                if river is not None and abs(y - river_y(x, river)) < river[2] / 2 + 0.6 + max(w, d) / 2:
                    continue
                if keep is not None and not keep(x, y):
                    continue
                cen = 1.0 - min(1.0, math.hypot(x, y) / R)
                h = rs.uniform(hmin, hmax) * (0.55 + center_boost * cen * cen)
                out.append((x, y, w * rs.uniform(0.82, 1.0), d * rs.uniform(0.82, 1.0), h))
    return np.array(out, np.float32).reshape(-1, 5)


def road_nodes(R, spacing=3.2, margin=0.7):
    """도로 교차점 격자 → (nodes(N,2), 이웃 리스트)."""
    n = int(R / spacing) + 1
    pts, idx = [], {}
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i * spacing, j * spacing
            if math.hypot(x, y) < R - margin:
                idx[(i, j)] = len(pts)
                pts.append((x, y))
    nb = [[] for _ in pts]
    for (i, j), a in idx.items():
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            b = idx.get((i + di, j + dj))
            if b is not None:
                nb[a].append(b)
    return np.array(pts, np.float32), nb


class RoadWalkers:
    """도로망 위를 교차로에서 무작위로 꺾으며 움직이는 에이전트(사람·차)."""

    def __init__(self, rs, R, n, speed, spacing=3.2, lane=0.0, sidewalk=None):
        self.nodes, self.nb = road_nodes(R, spacing)
        self.rs = rs
        self.n = n
        self.speed = np.asarray(speed, np.float32) * np.ones(n, np.float32)
        self.a = rs.integers(0, len(self.nodes), n)
        self.b = np.array([rs.choice(self.nb[i]) if self.nb[i] else i for i in self.a])
        self.u = rs.random(n).astype(np.float32)
        self.lane = lane
        self.side = sidewalk  # 인도 오프셋 (사람)
        self.sign = rs.choice([-1.0, 1.0], n).astype(np.float32)

    def step(self, dt):
        pa, pb = self.nodes[self.a], self.nodes[self.b]
        seg = np.linalg.norm(pb - pa, axis=1) + 1e-6
        self.u += self.speed * dt / seg
        for i in np.where(self.u >= 1.0)[0]:
            self.u[i] -= 1.0
            prev = self.a[i]
            self.a[i] = self.b[i]
            opts = [k for k in self.nb[self.a[i]] if k != prev] or self.nb[self.a[i]] or [prev]
            self.b[i] = self.rs.choice(opts)
        pa, pb = self.nodes[self.a], self.nodes[self.b]
        d = pb - pa
        dn = d / (np.linalg.norm(d, axis=1, keepdims=True) + 1e-6)
        perp = np.stack([-dn[:, 1], dn[:, 0]], 1)
        off = self.lane if self.side is None else self.side * self.sign
        pos = pa + d * self.u[:, None] + perp * (off if np.isscalar(off) else off[:, None])
        yaw = np.arctan2(dn[:, 1], dn[:, 0])
        return pos.astype(np.float32), yaw.astype(np.float32)


def push_out_of_rects(p, rects, pad=0.15):
    """점들을 건물 사각형(x, y, w, d) 밖으로 밀어냄."""
    if len(rects) == 0:
        return p
    x, y = p[:, 0:1], p[:, 1:2]
    rx, ry = rects[None, :, 0], rects[None, :, 1]
    hw, hd = rects[None, :, 2] / 2 + pad, rects[None, :, 3] / 2 + pad
    dx, dy = x - rx, y - ry
    inside = (np.abs(dx) < hw) & (np.abs(dy) < hd)
    if not inside.any():
        return p
    px = hw - np.abs(dx)
    py = hd - np.abs(dy)
    mx = np.where(inside & (px < py), np.sign(dx) * px, 0).sum(1)
    my = np.where(inside & (py <= px), np.sign(dy) * py, 0).sum(1)
    q = p.copy()
    q[:, 0] += mx
    q[:, 1] += my
    return q


class Wanderers:
    """자유롭게 돌아다니는 동물 (고양이·쥐). 목표 쫓기/피하기 지원."""

    def __init__(self, rs, n, R, speed, rects, start=None):
        self.rs, self.n, self.R = rs, n, R
        self.rects = rects
        self.p = start.copy() if start is not None else rs.uniform(-R * 0.7, R * 0.7, (n, 2)).astype(np.float32)
        self.p = push_out_of_rects(self.p, rects)
        ang = rs.uniform(0, 2 * np.pi, n)
        self.v = np.stack([np.cos(ang), np.sin(ang)], 1).astype(np.float32) * speed
        self.speed = speed
        self.yaw = ang.astype(np.float32)
        self.rest = rs.random(n) < 0.3

    def step(self, dt, seek=None, flee=None, flee_r=1.6, seek_r=3.0, speed_mul=1.0):
        rs = self.rs
        jitter = rs.normal(0, 1.2, (self.n, 2)).astype(np.float32)
        self.v += jitter * self.speed * dt * 2.0
        if seek is not None and len(seek):
            d = seek[None, :, :] - self.p[:, None, :]
            dist = np.linalg.norm(d, axis=2)
            j = dist.argmin(1)
            near = dist[np.arange(self.n), j] < seek_r
            dv = d[np.arange(self.n), j]
            dv /= np.linalg.norm(dv, axis=1, keepdims=True) + 1e-6
            self.v[near] += dv[near] * self.speed * dt * 6.0
        if flee is not None and len(flee):
            d = self.p[:, None, :] - flee[None, :, :]
            dist = np.linalg.norm(d, axis=2)
            j = dist.argmin(1)
            near = dist[np.arange(self.n), j] < flee_r
            dv = d[np.arange(self.n), j]
            dv /= np.linalg.norm(dv, axis=1, keepdims=True) + 1e-6
            self.v[near] += dv[near] * self.speed * dt * 8.0
        # 섬 가장자리 밖으로 못 나가게
        r = np.linalg.norm(self.p, axis=1)
        out = r > self.R * 0.88
        self.v[out] -= self.p[out] / r[out, None] * self.speed * dt * 6.0
        sp = np.linalg.norm(self.v, axis=1, keepdims=True) + 1e-6
        self.v = self.v / sp * np.clip(sp, 0, self.speed * 1.6)
        # 가끔 쉬기
        flip = rs.random(self.n) < dt * 0.35
        self.rest = np.where(flip, ~self.rest, self.rest)
        mv = np.where(self.rest[:, None], 0.0, 1.0) * speed_mul
        self.p = self.p + self.v * dt * mv
        self.p = push_out_of_rects(self.p, self.rects)
        moving = np.linalg.norm(self.v, axis=1) > 1e-3
        target = np.arctan2(self.v[:, 1], self.v[:, 0])
        dyaw = (target - self.yaw + np.pi) % (2 * np.pi) - np.pi
        self.yaw = np.where(moving & ~self.rest, self.yaw + dyaw * min(1.0, dt * 6), self.yaw)
        return self.p.copy(), self.yaw.copy()
