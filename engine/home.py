"""반려동물 편 공통 (EP12 고양이 / EP13 강아지): 주인이 출근한 뒤 혼자 남은 하루.

무대: 잠실 아파트(롯데월드타워 서쪽 약 1km, 83m) 꼭대기 층 한 집 — 지붕을 걷어낸 모습으로 내려다봄.
sim 단계(bpy 없음):
- 하루 행동: 반-마르코프 모형. 상태마다 지속 시간(로그정규)을 뽑고, 다음 행동은 시간대 활동성
  (새벽·해질녘 정점), 배고픔(마지막 식사 뒤 경과), 화장실 압력, 분리 문제 여부에 따라 고름
- 아파트 한 동 100가구 + 주인공 후보 여럿 → 장면에 맞는 하루를 산 주인공을 고름
- 주인공 동선: 집 안 길(문·통로 연결망)로 걸어 다님 (영상 시간 기준 속도)
Blender 단계: 집(바닥·낮게 자른 벽·가구), 고양이/강아지 자세 모형, 주인, 창문 상태 표시판
"""
import math

import numpy as np

from .common import FPS, keyed

BLD = 206                       # 잠실 아파트 동 (오픈스트리트맵 건물 번호, 높이 83m)
UW, UD = 12.0, 11.4             # 집 크기: x(동의 긴 축) × y(짧은 축), +y = 창문(롯데월드타워 쪽)
FZ = 0.12                       # 옥상 위 바닥 두께
DAY0 = 8 * 60 + 10              # 08:10 출근 (통계청 통근 실험통계 평균 출근 시각)
BACK = 18 * 60 + 55             # 18:55 귀가 (가정)
T_END = 21 * 60
SLEEP, REST, GROOM, EAT, DRINK, TOILET, WALK, WINDOW, PLAY, DOOR, DISTRESS, GREET = range(12)
NS = 12
CALM = (SLEEP, REST, GROOM, WINDOW)

# ───────────────────────── 집 구조 (집 기준 좌표, m) ─────────────────────────
WALLS = [  # (x0, y0, x1, y1, 높이)
    (-6.0, 5.7, 6.0, 5.7, 0.45),                                   # 창문 쪽 (낮게)
    (-6.0, -5.7, 4.3, -5.7, 1.1), (5.3, -5.7, 6.0, -5.7, 1.1),     # 현관문 4.3~5.3
    (-6.0, -5.7, -6.0, 5.7, 1.1), (6.0, -5.7, 6.0, 5.7, 1.1),
    (1.2, -5.7, 1.2, -3.2, 1.1), (1.2, -1.6, 1.2, 5.7, 1.1),       # 거실 | 방 쪽 (통로 -3.2~-1.6)
    (1.2, 0.4, 2.0, 0.4, 1.1), (3.0, 0.4, 6.0, 0.4, 1.1),          # 안방 문 2.0~3.0
    (1.2, -3.4, 2.0, -3.4, 1.1), (2.9, -3.4, 4.0, -3.4, 1.1), (5.6, -3.4, 6.0, -3.4, 1.1),
    (3.6, -5.7, 3.6, -3.4, 1.1),                                   # 욕실 | 현관
]
FLOORS = [(-6.0, -1.4, 1.2, 5.7, (0.50, 0.36, 0.24)), (-6.0, -5.7, 1.2, -1.4, (0.78, 0.76, 0.72)),
          (1.2, 0.4, 6.0, 5.7, (0.58, 0.44, 0.30)), (1.2, -3.4, 6.0, 0.4, (0.50, 0.36, 0.24)),
          (1.2, -5.7, 3.6, -3.4, (0.82, 0.84, 0.86)), (3.6, -5.7, 6.0, -3.4, (0.55, 0.55, 0.56))]
NODES = {"L1": (-2.4, 3.6), "L2": (-2.6, -3.9), "L3": (-0.3, -0.6), "O": (1.2, -2.4), "H": (2.6, -2.2),
         "BD": (2.5, 0.4), "BR": (3.4, 2.6), "BAD": (2.45, -3.4), "BA": (2.45, -4.4), "ED": (4.8, -3.4),
         "E": (4.8, -4.6)}
EDGES = [("L1", "L3"), ("L2", "L3"), ("L1", "L2"), ("L3", "O"), ("O", "H"), ("H", "BD"), ("BD", "BR"),
         ("H", "BAD"), ("BAD", "BA"), ("H", "ED"), ("ED", "E")]
SPOTS = {  # 이름: (x, y, z, 바라보는 방향°, 가까운 길목)
    "door": (4.8, -4.95, 0.0, -90, "E"), "sofa": (-5.35, 2.9, 0.42, 0, "L1"), "sofa2": (-5.35, 1.8, 0.42, 35, "L1"),
    "bed": (4.5, 3.9, 0.61, 200, "BR"), "tower": (-5.3, 5.05, 1.7, -30, "L1"), "tower_mid": (-5.3, 5.05, 1.2, 10, "L1"),
    "window": (-1.8, 5.25, 0.0, 90, "L1"), "window2": (3.0, 5.25, 0.0, 90, "BR"), "rug": (-3.0, 1.2, 0.015, 120, "L1"),
    "food": (-1.3, -4.3, 0.0, -90, "L2"), "water": (-0.85, -4.3, 0.0, -90, "L2"), "litter": (2.4, -5.05, 0.1, 90, "BA"),
    "hall": (2.8, -1.8, 0.0, 0, "H"), "cushion": (-1.2, 4.55, 0.1, 200, "L1"), "near_owner": (-1.45, 0.45, 0.0, 20, "L3"),
    "shoes": (4.05, -4.2, 0.0, 180, "E"),
}
PLAY_LOOP = [(-1.0, 0.2), (-0.6, 4.2), (-4.3, 4.6), (-4.6, 0.2), (-1.8, -0.6)]
OWNER_OUT = [(2.8, -2.0), (4.8, -3.4), (4.8, -5.1), (4.8, -6.2)]
OWNER_IN = [(4.8, -6.2), (4.8, -4.4), (4.8, -3.4), (2.6, -2.3), (1.2, -2.4), (-0.4, -0.2), (-1.9, 1.0)]


def hm(m):
    m = int(round(m)) % (24 * 60)
    return f"{m // 60:02d}:{m % 60:02d}"


# ───────────────────────── 하루 행동 시뮬레이션 ─────────────────────────
def activity(h, P):
    """시간대 활동성: 새벽·해질녘 정점 (고양이) / 낮 (강아지)."""
    a = P["base_act"]
    for c, amp, w in P["peaks"]:
        a += amp * math.exp(-((h - c) / w) ** 2)
    return a


def day_events(rs, P, sr):
    """한 마리의 하루(08:10~21:00): [(시작분, 끝분, 상태)], 분 = 자정 기준."""
    ev = []
    t = float(DAY0)
    s = P["first"]
    since_eat = rs.uniform(10, P["meal_gap"])
    since_toi = rs.uniform(60, P["toilet_gap"] * 0.8)
    while t < T_END:
        home = t >= BACK
        dur = P["dur"][s] * rs.lognormal(0, 0.45)
        if t < BACK <= t + dur:
            dur = BACK - t
        ev.append((t, t + dur, s))
        since_eat = 0.0 if s == EAT else since_eat + dur
        since_toi = 0.0 if s == TOILET else since_toi + dur
        t += dur
        if abs(t - BACK) < 1e-6:
            g = P["greet"] * rs.lognormal(0, 0.2)
            ev.append((t, t + g, GREET))
            t += g
            s = REST
            continue
        A = activity(t / 60.0, P)
        w = np.zeros(NS)
        w[SLEEP] = P["w_sleep"] * max(0.15, P["sleep_pivot"] - A) * (0.6 if home else 1.0)
        w[REST] = P["w_rest"]
        w[GROOM] = P["w_groom"]
        w[EAT] = 0.03 + (since_eat / P["meal_gap"]) ** 3
        w[DRINK] = P["w_drink"]
        w[TOILET] = 0.01 + 2.0 * (since_toi / P["toilet_gap"]) ** 4
        w[WALK] = P["w_walk"] * A
        w[WINDOW] = P["w_window"] * A
        w[PLAY] = P["w_play"] * A * A * (1.6 if home else 1.0)
        if not home:
            el = t - DAY0
            w[DOOR] = P["w_door"] + P["w_door0"] * math.exp(-el / P["door_tau"])
            if sr:
                w[DISTRESS] = P["w_dis"] + P["w_dis0"] * math.exp(-el / 45.0)
        w[s] *= 0.25                                  # 같은 행동 반복은 덜
        s = int(rs.choice(NS, p=w / w.sum()))
    return ev


def state_at(ev, m):
    if m < ev[0][0]:
        return ev[0][2]
    for a, b, s in ev:
        if a <= m < b:
            return s
    return ev[-1][2]


def first_start(ev, state, lo, hi):
    for a, b, s in ev:
        if s == state and lo <= a <= hi:
            return a, b
    return None


def stats_upto(ev, m):
    sl = sum(max(0.0, min(b, m) - a) for a, b, s in ev if s == SLEEP and a < m)
    meals = sum(1 for a, b, s in ev if s == EAT and a < m)
    toi = sum(1 for a, b, s in ev if s == TOILET and a < m)
    return sl, meals, toi


def population(rs, P, n, sr_frac):
    sr = rs.random(n) < sr_frac
    return [day_events(rs, P, bool(k)) for k in sr], sr


def budget(evs, lo=DAY0, hi=BACK):
    """혼자 있던 시간의 상태별 비율 (검증용)."""
    tot = np.zeros(NS)
    for ev in evs:
        for a, b, s in ev:
            tot[s] += max(0.0, min(b, hi) - max(a, lo))
    return tot / tot.sum()


# ───────────────────────── 집 안 동선 ─────────────────────────
def _graph():
    adj = {k: [] for k in NODES}
    for a, b in EDGES:
        d = math.dist(NODES[a], NODES[b])
        adj[a].append((b, d))
        adj[b].append((a, d))
    return adj


ADJ = _graph()


def route(p, spot_xy, spot_node):
    """현재 위치 → 길목들(최단 경로) → 목표 지점. 출발 길목은 (거기까지 거리 + 남은 길)이 가장 짧은 곳."""
    dist, prev, todo = {spot_node: 0.0}, {}, {spot_node}
    while todo:
        u = min(todo, key=lambda k: dist[k])
        todo.remove(u)
        for v, d in ADJ[u]:
            if dist[u] + d < dist.get(v, 1e9):
                dist[v] = dist[u] + d
                prev[v] = u
                todo.add(v)
    start = min(NODES, key=lambda k: math.dist(NODES[k], p) + dist[k])
    path, k = [start], start
    while k != spot_node:
        k = prev[k]
        path.append(k)
    pts = [tuple(p)] + [NODES[k] for k in path] + [tuple(spot_xy)]
    out = [pts[0]]
    for q in pts[1:]:
        if math.dist(out[-1], q) > 0.05:
            out.append(q)
    return np.array(out, np.float32)


def clock_curve(keys, nf):
    """영상 초 → 시계(분) 표, keys=[(초, 분)] 선형 보간."""
    ts = np.arange(nf) / FPS
    return np.array([keyed(t, keys, ease=lambda u: u) for t in ts], np.float32)


def animate(rs, ev, clock, P, owner_xy, owner_on):
    """주인공의 프레임별 위치·높이·방향·자세. 상태는 시계(clock)를 따라가고, 걷는 속도는 영상 시간 기준."""
    nf = len(clock)
    st = np.array([state_at(ev, m) for m in clock], np.int8)
    # 너무 짧은 장면(0.6초 미만)은 앞 행동에 합침 → 깜빡임 방지
    segs = []
    f = 0
    while f < nf:
        g = f
        while g < nf and st[g] == st[f]:
            g += 1
        if segs and g - f < int(0.6 * FPS) and st[f] not in (GREET,):
            segs[-1][1] = g
        else:
            segs.append([f, g, int(st[f])])
        f = g
    pos = np.zeros((nf, 2), np.float32)
    z = np.zeros(nf, np.float32)
    yaw = np.zeros(nf, np.float32)
    pose = np.zeros(nf, np.float32)
    shown = np.zeros(nf, np.int8)
    cur = np.array(SPOTS[P["start_spot"]][:2], np.float32)
    cur_z = SPOTS[P["start_spot"]][2]
    cur_yaw = math.radians(SPOTS[P["start_spot"]][3])
    last_spot = P["start_spot"]
    prev_f0 = 0
    for f0, f1, s in segs:
        # 미리 출발: 앞 행동 끝부분에 걸어가서 이 행동이 시작될 때 도착
        if f0 > 0:
            if s == PLAY:
                est = math.dist(cur, PLAY_LOOP[0]) + 1.0
            else:
                opts0 = (P.get("spots_home", {}).get(s) if clock[f0] >= BACK else None) or P["spots"].get(s, [("door", 1)])
                est = math.dist(cur, SPOTS[opts0[0][0]][:2]) * 1.3 + 0.5
            keep = max(int(0.5 * FPS), int(0.6 * (f0 - prev_f0)))   # 앞 행동은 60% 이상 보여 줌
            pre = int(min(est / P["walk_speed"] * FPS, 1.0 * FPS, max(0, f0 - prev_f0 - keep)))
            prev_f0 = f0
            arrive = f0 + 0.15 * (f1 - f0)     # 이 행동 시간의 15% 안에는 도착 (멀면 빨리감기처럼 서두름)
            if pre:
                f0 -= pre
                cur, cur_z = pos[f0 - 1].copy(), float(z[f0 - 1])
        if s == PLAY:
            loop = np.array(PLAY_LOOP + PLAY_LOOP[:1], np.float32)
            path = np.vstack([route(cur, loop[0], "L3"), loop[1:], loop[1:], loop[1:]])
            tz, tyaw, spd, still = 0.0, None, P["run_speed"], P["pose"][REST]
        else:
            if s == GREET:
                name = "door"
            else:
                opts = (P.get("spots_home", {}).get(s) if clock[f0] >= BACK else None) or P["spots"][s]
                names = [k for k, _ in opts if k != last_spot] or [opts[0][0]]
                wts = np.array([w for k, w in opts if k in names], float)
                name = names[int(rs.choice(len(names), p=wts / wts.sum()))]
            sx, sy, tz, tyd, node = SPOTS[name]
            path = route(cur, (sx, sy), node)
            tyaw, spd, still = math.radians(tyd), P["walk_speed"], P["pose"][s]
            last_spot = name
        seg = np.diff(path, axis=0)
        L = np.r_[0, np.cumsum(np.hypot(seg[:, 0], seg[:, 1]))]
        if s != PLAY and f0 > 0:
            spd = max(spd, min(9.0, L[-1] / max(0.25, (arrive - f0) / FPS)))
        for f in range(f0, f1):
            d = (f - f0) / FPS * spd
            if d < L[-1] and len(path) > 1:
                k = int(np.clip(np.searchsorted(L, d) - 1, 0, len(seg) - 1))
                u = (d - L[k]) / max(L[k + 1] - L[k], 1e-6)
                p = path[k] + seg[k] * u
                cur_yaw = math.atan2(seg[k][1], seg[k][0])
                # 높은 곳(소파·침대·캣타워)은 마지막/처음 0.6m에서 뛰어오르기/내리기
                zz = 0.0
                if tz > 0 and L[-1] - d < 0.6:
                    zz = tz * (1 - (L[-1] - d) / 0.6)
                if cur_z > 0 and d < 0.6:
                    zz = max(zz, cur_z * (1 - d / 0.6))
                pos[f], z[f], yaw[f] = p, zz, cur_yaw
                pose[f] = P["pose"]["run"] if s == PLAY else (3 + int(d / P["stride"]) % 2)
                if s == PLAY:
                    pose[f] = P["pose"]["run"] if int(d / 0.35) % 3 else P["pose"]["run2"]
            else:
                pos[f] = path[-1]
                z[f] = tz
                if tyaw is not None:
                    cur_yaw = tyaw
                yaw[f] = cur_yaw
                pose[f] = still
            shown[f] = s
        cur, cur_z = pos[f1 - 1].copy(), float(z[f1 - 1])
    # 마중: 주인이 들어오면 주인 쪽을 보고 기지개/깡충
    for f in range(nf):
        if shown[f] == GREET and z[f] == 0 and owner_on[f] > 0.5:
            d = owner_xy[f] - pos[f]
            yaw[f] = math.atan2(d[1], d[0])
            if np.hypot(*d) < 1.6:
                pose[f] = P["pose"]["greet"]
                if P.get("hop"):
                    z[f] = 0.12 * abs(math.sin(f / FPS * 9.0))
    return pos, z, yaw, pose, shown


def owner_track(nf, t_leave, t_back):
    """주인: t_leave에 현관으로 나가고, t_back에 들어와 거실에 섬 (영상 초)."""
    xy = np.zeros((nf, 2), np.float32)
    yaw = np.zeros(nf, np.float32)
    pose = np.zeros(nf, np.float32)
    on = np.zeros(nf, np.float32)
    for name, path, t0 in (("out", np.array(OWNER_OUT, np.float32), t_leave),
                           ("in", np.array(OWNER_IN, np.float32), t_back)):
        seg = np.diff(path, axis=0)
        L = np.r_[0, np.cumsum(np.hypot(seg[:, 0], seg[:, 1]))]
        for f in range(nf):
            t = f / FPS
            if name == "out" and t >= t_back:
                continue
            if name == "in" and t < t_back:
                continue
            d = max(0.0, (t - t0) * (1.25 if name == "out" else 2.6))   # 귀가 장면은 빨리감기
            if d < L[-1]:
                k = int(np.clip(np.searchsorted(L, d) - 1, 0, len(seg) - 1))
                xy[f] = path[k] + seg[k] * (d - L[k]) / max(L[k + 1] - L[k], 1e-6)
                yaw[f] = math.atan2(seg[k][1], seg[k][0])
                pose[f] = 0 if t < t0 else 1 + int(d / 0.45) % 4
                on[f] = 1.0 if (name == "in" or xy[f][1] > -5.75) else 0.0
            else:
                xy[f] = path[-1]
                yaw[f] = math.atan2(seg[-1][1], seg[-1][0]) if name == "out" else math.radians(-60)
                on[f] = 0.0 if name == "out" else 1.0
    return xy, yaw, pose, on


# ───────────────────────── 위치 변환 ─────────────────────────
def bframe(g, b=BLD):
    """아파트 동의 중심·축·크기. +y 축은 롯데월드타워(원점) 쪽."""
    r = g["bv"][(g["bvid"] == b) & (g["bvz"] == 0)][:, :2].astype(np.float64)
    m = r.mean(0)
    _, _, vt = np.linalg.svd(r - m)
    p = (r - m) @ vt.T
    c = m + vt.T @ ((p.max(0) + p.min(0)) / 2)
    ax = vt[0]
    ny = np.array([-ax[1], ax[0]])
    if np.dot(ny, -c) < 0:
        ny = -ny
    nx = np.array([ny[1], -ny[0]])
    return dict(c=c, nx=nx, ny=ny, L=float(np.ptp(p[:, 0])), D=float(np.ptp(p[:, 1])), h=float(g["b_h"][b]),
                ang=math.atan2(nx[1], nx[0]))


def to_world(fr, x, y, z=0.0):
    x, y = np.asarray(x, np.float64), np.asarray(y, np.float64)
    wx = fr["c"][0] + fr["nx"][0] * x + fr["ny"][0] * y
    wy = fr["c"][1] + fr["nx"][1] * x + fr["ny"][1] * y
    return wx, wy, np.asarray(z, np.float64) + fr["h"] + FZ


def facade_slots(fr, n=100):
    """-y 쪽(타워 반대편) 벽의 창문 자리: 층 1~25 × 4집."""
    xs = np.array([-18.0, -6.0, 6.0, 18.0])
    fl = np.arange(int(fr["h"] / 3.1) - 1, 0, -1)[: n // len(xs)]
    gx, gf = np.meshgrid(xs, fl)
    y = -fr["D"] / 2 - 0.25
    wx, wy, _ = to_world(fr, gx.ravel(), np.full(gx.size, y))
    zz = gf.ravel() * 3.1 + 1.6
    return np.c_[wx, wy, zz].astype(np.float32)


# ───────────────────────── Blender ─────────────────────────
def _box_list(kind):
    F = []
    WOOD, WHITE, DARK = (0.45, 0.30, 0.18), (0.86, 0.86, 0.84), (0.08, 0.08, 0.09)
    SOFA, RUG = (0.30, 0.38, 0.52), (0.80, 0.74, 0.62)

    def box(cx, cy, sx, sy, sz, z0, col):
        F.append((cx, cy, sx, sy, sz, z0 + FZ, col))

    def table(cx, cy, sx, sy, h, col):
        box(cx, cy, sx, sy, 0.05, h - 0.05, col)
        for dx in (-1, 1):
            for dy in (-1, 1):
                box(cx + dx * (sx / 2 - 0.06), cy + dy * (sy / 2 - 0.06), 0.05, 0.05, h - 0.05, 0, col)
    for x0, y0, x1, y1, col in FLOORS:
        F.append(((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, FZ, 0.0, col))
    for x0, y0, x1, y1, h in WALLS:   # 낮게 자른 벽 + 어두운 단면(윗면)
        if x0 == x1:
            box(x0, (y0 + y1) / 2, 0.12, abs(y1 - y0) + 0.12, h, 0, (0.92, 0.91, 0.88))
            box(x0, (y0 + y1) / 2, 0.13, abs(y1 - y0) + 0.13, 0.02, h, (0.22, 0.21, 0.2))
        else:
            box((x0 + x1) / 2, y0, abs(x1 - x0) + 0.12, 0.12, h, 0, (0.92, 0.91, 0.88))
            box((x0 + x1) / 2, y0, abs(x1 - x0) + 0.13, 0.13, 0.02, h, (0.22, 0.21, 0.2))
    box(-2.4, 5.7, 7.0, 0.16, 0.04, 0.45, (0.97, 0.97, 0.97))      # 창틀
    box(3.6, 5.7, 4.6, 0.16, 0.04, 0.45, (0.97, 0.97, 0.97))
    box(-3.75, -5.35, 4.5, 0.65, 0.9, 0, WHITE)                    # 조리대
    box(-3.75, -5.35, 4.5, 0.68, 0.04, 0.9, (0.25, 0.25, 0.27))
    box(-0.95, -5.3, 0.9, 0.75, 1.85, 0, (0.70, 0.72, 0.75))       # 냉장고
    table(-3.0, -2.6, 1.6, 0.9, 0.74, WOOD)                         # 식탁·의자
    for dx in (-0.45, 0.45):
        for dy in (-0.75, 0.75):
            box(-3.0 + dx, -2.6 + dy, 0.42, 0.42, 0.45, 0, WOOD)
    box(-5.45, 2.4, 0.95, 2.3, 0.42, 0, SOFA)                       # 소파
    box(-5.85, 2.4, 0.22, 2.3, 0.85, 0, SOFA)
    box(-5.45, 1.17, 0.95, 0.2, 0.62, 0, SOFA)
    box(-5.45, 3.63, 0.95, 0.2, 0.62, 0, SOFA)
    box(-3.6, 2.4, 2.4, 3.2, 0.015, 0, RUG)                         # 러그·탁자·TV
    table(-3.7, 2.4, 0.6, 1.1, 0.38, WOOD)
    box(0.9, 2.4, 0.45, 1.8, 0.45, 0, DARK)
    box(1.02, 2.4, 0.06, 1.6, 0.9, 0.5, (0.02, 0.02, 0.025))
    box(0.6, 5.2, 0.4, 0.4, 0.4, 0, (0.55, 0.32, 0.22))             # 화분
    box(0.6, 5.2, 0.62, 0.62, 0.55, 0.4, (0.20, 0.45, 0.18))
    box(0.6, 5.2, 0.4, 0.4, 0.35, 0.95, (0.24, 0.52, 0.22))
    box(4.9, 3.3, 2.1, 1.6, 0.35, 0, WOOD)                          # 침대
    box(4.9, 3.3, 2.0, 1.5, 0.2, 0.35, (0.93, 0.93, 0.92))
    box(4.55, 3.3, 1.35, 1.56, 0.06, 0.55, (0.45, 0.58, 0.78))
    box(5.7, 3.3, 0.35, 1.2, 0.12, 0.55, (0.97, 0.97, 0.97))
    box(4.5, 0.78, 3.0, 0.6, 1.8, 0, (0.78, 0.74, 0.68))            # 옷장
    table(1.75, 4.9, 0.6, 1.2, 0.74, WOOD)                          # 책상
    box(3.1, -5.25, 0.45, 0.6, 0.45, 0, (0.96, 0.96, 0.97))         # 변기
    box(3.85, -4.6, 0.45, 1.8, 1.0, 0, (0.66, 0.60, 0.52))          # 신발장
    box(-1.3, -4.3, 0.2, 0.2, 0.06, 0, (0.85, 0.35, 0.3))           # 밥그릇·물그릇
    box(-1.3, -4.3, 0.15, 0.15, 0.02, 0.06, (0.55, 0.36, 0.2))
    box(-0.85, -4.3, 0.2, 0.2, 0.06, 0, (0.3, 0.55, 0.85))
    box(-0.85, -4.3, 0.15, 0.15, 0.02, 0.055, (0.55, 0.75, 0.95))
    if kind == "cat":
        box(-5.3, 5.05, 0.6, 0.6, 0.06, 0, (0.78, 0.70, 0.56))      # 캣타워
        box(-5.3, 5.05, 0.12, 0.12, 1.65, 0, (0.72, 0.62, 0.45))
        for zz in (0.6, 1.15, 1.65):
            box(-5.3, 5.05, 0.55, 0.55, 0.05, zz, (0.78, 0.70, 0.56))
        box(2.4, -5.05, 0.55, 0.45, 0.14, 0, (0.40, 0.55, 0.65))     # 화장실(모래)
        box(2.4, -5.05, 0.48, 0.38, 0.02, 0.1, (0.86, 0.80, 0.66))
        box(-2.6, 0.9, 0.08, 0.08, 0.08, 0.015, (0.95, 0.3, 0.5))    # 장난감
    else:
        box(-1.2, 4.55, 0.9, 0.7, 0.12, 0, (0.72, 0.28, 0.22))       # 강아지 방석
        box(-1.2, 4.55, 0.7, 0.5, 0.04, 0.1, (0.92, 0.82, 0.70))
        box(2.4, -5.05, 0.6, 0.45, 0.01, 0, (0.92, 0.94, 0.96))      # 배변 패드
        box(-2.6, 0.9, 0.1, 0.1, 0.1, 0.015, (0.95, 0.75, 0.2))      # 공
        box(4.1, -4.55, 0.3, 0.12, 0.08, 0, (0.15, 0.15, 0.18))      # 주인 신발
        box(4.1, -4.25, 0.3, 0.12, 0.08, 0, (0.15, 0.15, 0.18))
    return F


def _mesh_from_boxes(K, name, items, mat):
    import bpy
    V, Fc, C = [], [], []
    quads = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    for cx, cy, sx, sy, sz, z0, col in items:
        base = len(V)
        for dz in (0.0, sz):
            for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                V.append((cx + dx * sx / 2, cy + dy * sy / 2, z0 + dz))
        for q in quads:
            Fc.append([base + i for i in q])
            C.append((*col, 1.0))
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], Fc)
    me.attributes.new("fcol", "FLOAT_COLOR", "FACE").data.foreach_set("color", np.asarray(C, np.float32).ravel())
    me.materials.append(mat)
    return K.link(bpy.data.objects.new(name, me))


def build_home(ctx, fr, kind):
    """집 한 채를 아파트 동 옥상(꼭대기 층 자리)에 놓음."""
    from . import bkit as K
    m, nt, out = K.new_mat("m_home")
    a = nt.nodes.new("ShaderNodeAttribute")
    a.attribute_name = "fcol"
    b = K.principled(nt, a.outputs["Color"], 0.7)
    K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    ob = _mesh_from_boxes(K, "home", _box_list(kind), m)
    ob.location = (fr["c"][0], fr["c"][1], fr["h"])
    ob.rotation_euler = (0, 0, fr["ang"])
    return ob


def _rot_y(bm, ang, pivot=(0, 0, 0)):
    c, s = math.cos(ang), math.sin(ang)
    for v in bm.verts:
        x, zz = v.co.x - pivot[0], v.co.z - pivot[2]
        v.co.x, v.co.z = pivot[0] + c * x + s * zz, pivot[2] - s * x + c * zz
    return bm


def cat_poses(ctx, fur, dark):
    """0 웅크려 잠 · 1 식빵 · 2 앉음 · 3·4 걷기 · 5·6 달리기 · 7 기지개 (앞 = +x, m)."""
    from . import bkit as K
    S, C = K.bm_sphere, K.bm_cone

    def head(x, z, y=0.0, r=0.105):
        return [(S(r, (x, y, z), 12, 8, scale=(1.0, 1.0, 0.92)), 0),
                (C(0.045, 0.0, 0.09, (x - 0.005, y + 0.052, z + 0.06), 4), 0),
                (C(0.045, 0.0, 0.09, (x - 0.005, y - 0.052, z + 0.06), 4), 0),
                (S(0.02, (x + 0.095, y + 0.037, z + 0.02), 6, 4), 1),
                (S(0.02, (x + 0.095, y - 0.037, z + 0.02), 6, 4), 1)]

    def tail(pts, r0=0.032):
        return [(S(r0 - 0.002 * i, p, 6, 4), 0) for i, p in enumerate(pts)]

    def legs(xs, z0=0.0, h=0.13):
        return [(C(0.033, 0.028, h, (x, y, z0), 6), 0) for x, y in xs]
    P = []
    # 0 웅크려 잠
    P.append([(S(0.2, (0, 0, 0.1), 14, 8, scale=(1.15, 1.0, 0.5)), 0)] + head(0.12, 0.12, 0.13, 0.095) +
             tail([(-0.18 + 0.06 * i, -0.17 + 0.012 * i * i, 0.05) for i in range(6)]))
    # 1 식빵
    P.append([(S(0.16, (0, 0, 0.13), 14, 8, scale=(1.5, 0.95, 0.82)), 0)] + head(0.25, 0.24) +
             tail([(-0.2 + 0.06 * i, 0.13, 0.04) for i in range(6)]))
    # 2 앉음
    P.append([(S(0.15, (-0.04, 0, 0.19), 14, 8, scale=(0.95, 0.85, 1.35)), 0)] + head(0.06, 0.42) +
             legs([(0.06, 0.045), (0.06, -0.045)], 0.0, 0.2) +
             tail([(-0.17 + 0.045 * i, 0.03 * i, 0.03) for i in range(6)]))
    # 3·4 걷기
    for k in (0, 1):
        o = 0.035 if k else -0.035
        P.append([(S(0.16, (0, 0, 0.17), 14, 8, scale=(1.55, 0.85, 0.8)), 0)] + head(0.27, 0.29) +
                 legs([(0.12 + o, 0.07), (0.12 - o, -0.07), (-0.12 - o, 0.07), (-0.12 + o, -0.07)], 0.0, 0.15) +
                 tail([(-0.25 - 0.06 * u, 0, 0.19 + 0.2 * u * u) for u in np.linspace(0, 1, 6)]))
    # 5·6 달리기
    for k in (0, 1):
        f, b = (0.27, -0.27) if k else (0.08, -0.08)
        P.append([(S(0.15, (0, 0, 0.19), 14, 8, scale=(1.85, 0.8, 0.72)), 0)] + head(0.3, 0.27) +
                 legs([(f, 0.05), (f - 0.03, -0.05), (b, 0.05), (b + 0.03, -0.05)], 0.02, 0.15) +
                 tail([(-0.3 - 0.07 * i, 0, 0.21 + 0.01 * i) for i in range(6)]))
    # 7 기지개 (앞은 낮게, 엉덩이는 높게)
    body = _rot_y(S(0.16, (0, 0, 0.16), 14, 8, scale=(1.6, 0.85, 0.75)), math.radians(-18), (0, 0, 0.16))
    P.append([(body, 0)] + head(0.29, 0.14) + legs([(0.3, 0.06), (0.3, -0.06)], 0.0, 0.05) +
             legs([(-0.14, 0.07), (-0.14, -0.07)], 0.0, 0.2) +
             tail([(-0.27 - 0.03 * i, 0, 0.28 + 0.05 * i) for i in range(6)]))
    return [K.proto(ctx, f"p_cat_{i}", K.join_bms(parts), [fur, dark], smooth=True) for i, parts in enumerate(P)]


def dog_poses(ctx, fur, dark):
    """작은 흰 강아지(말티즈 느낌): 0 웅크려 잠 · 1 엎드림 · 2 앉음 · 3·4 걷기 · 5·6 달리기 · 7 반김(꼬리 위)."""
    from . import bkit as K
    S, C = K.bm_sphere, K.bm_cone

    def head(x, z, y=0.0):
        return [(S(0.12, (x, y, z), 12, 8), 0),
                (S(0.055, (x + 0.1, y, z - 0.03), 8, 6, scale=(1.25, 1.0, 0.9)), 0),
                (S(0.022, (x + 0.165, y, z - 0.015), 6, 4), 1),
                (S(0.017, (x + 0.08, y + 0.05, z + 0.03), 6, 4), 1),
                (S(0.017, (x + 0.08, y - 0.05, z + 0.03), 6, 4), 1),
                (S(0.06, (x - 0.02, y + 0.11, z - 0.04), 8, 6, scale=(0.6, 0.45, 1.3)), 0),
                (S(0.06, (x - 0.02, y - 0.11, z - 0.04), 8, 6, scale=(0.6, 0.45, 1.3)), 0)]

    def legs(xs, h=0.16, z0=0.0):
        return [(C(0.045, 0.04, h, (x, y, z0), 6), 0) for x, y in xs]
    P = []
    P.append([(S(0.22, (0, 0, 0.11), 14, 8, scale=(1.2, 1.05, 0.5)), 0)] + head(0.14, 0.14, 0.14) +
             [(S(0.06, (-0.2, -0.16, 0.08), 8, 6), 0)])
    P.append([(S(0.17, (0, 0, 0.13), 14, 8, scale=(1.5, 0.9, 0.72)), 0)] + head(0.26, 0.28) +
             [(S(0.04, (0.3, 0.06, 0.03), 6, 4), 0), (S(0.04, (0.3, -0.06, 0.03), 6, 4), 0),
              (S(0.06, (-0.26, 0, 0.12), 8, 6), 0)])
    P.append([(S(0.16, (-0.05, 0, 0.22), 14, 8, scale=(1.0, 0.9, 1.3)), 0)] + head(0.08, 0.48) +
             legs([(0.08, 0.05), (0.08, -0.05)], 0.24) + [(S(0.06, (-0.22, 0, 0.08), 8, 6), 0)])
    for k in (0, 1):
        o = 0.04 if k else -0.04
        P.append([(S(0.17, (0, 0, 0.25), 14, 8, scale=(1.45, 0.9, 0.85)), 0)] + head(0.27, 0.4) +
                 legs([(0.13 + o, 0.08), (0.13 - o, -0.08), (-0.13 - o, 0.08), (-0.13 + o, -0.08)]) +
                 [(S(0.065, (-0.27, 0, 0.38), 8, 6), 0)])
    for k in (0, 1):
        f, b = (0.26, -0.26) if k else (0.08, -0.08)
        P.append([(S(0.16, (0, 0, 0.26), 14, 8, scale=(1.7, 0.85, 0.78)), 0)] + head(0.3, 0.37) +
                 legs([(f, 0.06), (f - 0.03, -0.06), (b, 0.06), (b + 0.03, -0.06)], 0.15, 0.04) +
                 [(S(0.06, (-0.3, 0, 0.36), 8, 6), 0)])
    P.append([(S(0.17, (0, 0, 0.25), 14, 8, scale=(1.45, 0.9, 0.85)), 0)] + head(0.28, 0.44) +
             legs([(0.13, 0.08), (0.13, -0.08), (-0.13, 0.08), (-0.13, -0.08)]) +
             [(S(0.07, (-0.26, 0, 0.46), 8, 6), 0), (S(0.05, (-0.29, 0, 0.53), 8, 6), 0)])
    return [K.proto(ctx, f"p_dog_{i}", K.join_bms(parts), [fur, dark], smooth=True) for i, parts in enumerate(P)]


def mat_glow_inst(name, strength=4.0):
    """인스턴스 'col' 색으로 빛나는 판 (창문 상태 표시)."""
    from . import bkit as K
    m, nt, out = K.new_mat(name)
    e = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, K.inst_attr(nt, "col"), e.inputs["Color"])
    e.inputs["Strength"].default_value = strength
    K.ln(nt, e.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


STATE_COL = np.array([(0.10, 0.18, 0.55), (0.30, 0.38, 0.70), (0.45, 0.75, 0.85), (1.0, 0.75, 0.25),
                      (0.35, 0.75, 1.0), (0.75, 0.55, 0.30), (0.30, 1.0, 0.45), (0.95, 0.95, 0.75),
                      (0.35, 1.0, 0.35), (1.0, 0.55, 0.15), (1.0, 0.12, 0.08), (1.0, 0.6, 0.8)], np.float32)


# ───────────────────────── 편 공통: sim·장면 ─────────────────────────
def simulate_home(E):
    """E = 편 모듈 (KIND, P, SR_FRAC, N_SR, SEED, select, clock_keys, T_LEAVE)."""
    from . import jamsil
    from .common import frames_of
    from .jamsil_ep import CAR_COLORS, crowd, people_colors, traffic
    jamsil.use_area("jamsil")
    g = jamsil.geometry()
    fr = bframe(g)
    rs = np.random.default_rng(E.SEED)
    nf = frames_of(E.DUR)
    # 아파트 한 동 100가구 (분리 문제 정확히 N_SR마리) + 주인공 후보
    fac = [day_events(rs, E.P, k < E.N_SR) for k in range(100)]
    order = rs.permutation(100)
    fac = [fac[i] for i in order]
    fac_sr = (order < E.N_SR)
    best, best_score = None, -1e9
    for _ in range(E.N_CAND):
        ev = day_events(rs, E.P, False)
        sc, info = E.select(ev)
        if sc > best_score:
            best, best_score, best_info = ev, sc, info
    clock = clock_curve(E.clock_keys(best_info), nf)
    t_back = float(np.argmax(clock >= BACK)) / FPS
    oxy, oyaw, opose, oon = owner_track(nf, E.T_LEAVE, t_back)
    pos, z, yaw, pose, shown = animate(rs, best, clock, E.P, oxy, oon)
    wx, wy, wz = to_world(fr, pos[:, 0], pos[:, 1], z)
    hero_w = np.c_[wx, wy, wz].astype(np.float32)
    k = int(FPS * 0.4)
    pad = np.pad(hero_w, ((k, k), (0, 0)), mode="edge")
    hero_s = np.stack([np.convolve(pad[:, i], np.ones(2 * k + 1) / (2 * k + 1), "valid") for i in range(3)], 1)
    fac_state = np.array([[state_at(ev, m) for ev in fac] for m in clock], np.int8)
    st = np.array([stats_upto(best, m) for m in clock], np.float32)
    # 거리(출근길) 사람·차
    street = fr["c"] - fr["ny"] * (fr["D"] / 2 + 22)
    pp, py, ph = crowd(rs, nf, 260, tuple(street), 240)
    shirt, pants = people_colors(rs, 260)
    cp, cy = traffic(rs, nf, 70, tuple(street), 520)
    print("hero score", best_score, best_info, "| budget(100) alone:",
          dict(zip(["잠", "쉼", "그루밍", "밥", "물", "화장실", "돌아", "창밖", "우다다", "현관", "불안"],
                   np.round(budget(fac)[:11], 3))))
    return dict(clock=clock, pos=pos, z=z, yaw=yaw, pose=pose, shown=shown, hero_w=hero_w, hero_s=hero_s.astype(np.float32),
                oxy=oxy, oyaw=oyaw, opose=opose, oon=oon, t_back=np.float32(t_back), fac_state=fac_state,
                fac_sr=fac_sr.astype(np.float32), sleep_min=st[:, 0], meals=st[:, 1], toilets=st[:, 2],
                pp=pp, py=py, ph=ph, shirt=shirt, pants=pants, cp=cp, cy=cy,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), 70)], street=street.astype(np.float32))


def cam_target(fr, sim, key, f):
    kind = key[0]
    if kind == "hero":
        return tuple(float(v) for v in sim["hero_s"][f])
    if kind == "unit":
        x, y, zz = to_world(fr, key[1], key[2], key[3])
        return float(x), float(y), float(zz)
    if kind == "bld":
        return float(fr["c"][0]), float(fr["c"][1]), fr["h"] * 0.55
    s = sim["street"]
    return float(s[0]), float(s[1]), 2.0


def build_home_scene(ctx, E):
    from . import bkit as K
    from .jamsil import Jamsil, geometry, use_area
    from .jamsil_ep import light_keys, pose_of
    use_area("jamsil")
    sim = ctx.sim
    g = geometry()
    fr = bframe(g)
    J = Jamsil(ctx, g)
    build_home(ctx, fr, E.KIND)
    fur = K.mat_inst("m_fur", 0.85)
    dark = K.mat_simple("m_pet_dark", (0.02, 0.02, 0.025), 0.3)
    protos = (cat_poses if E.KIND == "cat" else dog_poses)(ctx, fur, dark)
    pet = K.instancer_multi(ctx, "pet", protos, 1)
    owner = K.instancer_multi(ctx, "owner", K.person_poses(
        ctx, K.mat_inst("m_oshirt", 0.75), K.mat_inst2("m_opants"), K.mat_simple("m_oskin", (0.86, 0.68, 0.55), 0.6),
        K.mat_simple("m_ohair", (0.05, 0.04, 0.035), 0.6)), 1)
    po = J.people(len(sim["shirt"]), "commuters")
    co = J.cars(len(sim["ccol"]))
    slots = facade_slots(fr)
    marks = K.instancer(ctx, "facade_marks", K.proto(ctx, "p_mark", K.bm_cube(1, 1, 1), [mat_glow_inst("m_mark", 6.0)]),
                        len(slots), vector_scale=True)
    lamp = K.point_light(ctx, tuple(to_world(fr, -1.5, 0.5, 2.6)), energy=0, color=(1.0, 0.82, 0.62), radius=1.5,
                         name="home_lamp")
    lk = [(k, dict(v, energy=max(v["energy"], 0.6), amb=max(v["amb"], 0.1))) for k, v in light_keys(E.SKY)]
    ang = math.degrees(fr["ang"])
    fur_col = np.array([E.FUR], np.float32)
    nb = J.nb
    dark_b = np.zeros(nb, np.float32)
    zeros = np.zeros(nb, np.float32)
    J.set_buildings(gcol=np.ones((nb, 3), np.float32), glow=zeros, dark=dark_b)

    def upd(t, f):
        keys = [(k[0], (*cam_target(fr, sim, k[1], f), k[2] + ang, k[3], k[4], k[5])) for k in E.CAM]
        v = keyed(t, keys)
        J.cam.set(v[:3], v[3], v[4], v[5], v[6], shift=0.04)
        night = J.light(t, lk)
        ctx.set_ctl("lights", 0.15 + 0.7 * night)
        ctx.set_ctl("carlights", 0.2 + 0.8 * night)
        home = float(np.clip((t - float(sim["t_back"]) - 0.25) / 0.15, 0, 1))   # 주인이 들어오며 불을 켬
        lamp.data.energy = 900.0 * home * night
        x, y, zz = sim["hero_w"][f]
        K.set_points(pet, [(x, y, zz)], scale=[1.0], rot=[(0, 0, float(sim["yaw"][f]) + fr["ang"])], col=fur_col,
                     colors={"col2": fur_col}, pose=[float(sim["pose"][f])])
        ox, oy, oz = to_world(fr, sim["oxy"][f][0], sim["oxy"][f][1], 0.0)
        K.set_points(owner, [(float(ox), float(oy), float(oz))], scale=[float(sim["oon"][f])],
                     rot=[(0, 0, float(sim["oyaw"][f]) + fr["ang"])], col=[(0.16, 0.22, 0.38)],
                     colors={"col2": [(0.08, 0.08, 0.1)]}, pose=[float(sim["opose"][f])])
        fs = sim["fac_state"][f].astype(int)
        col = STATE_COL[fs] * np.where(fs == DISTRESS, 0.75 + 0.25 * math.sin(t * 9), 1.0)[:, None]
        if E.SR_SHOW[0] <= t < E.SR_SHOW[1]:   # 분리 문제가 있는 집은 붉게 깜빡임
            sr = sim["fac_sr"] > 0.5
            col[sr] = np.array([1.0, 0.12, 0.08], np.float32) * (0.7 + 0.3 * math.sin(t * 7))
        if E.SR_SHOW[0] - 0.6 <= t < E.SR_SHOW[1] + 0.4:   # 이 동은 창 불을 끄고 표시판만 보이게
            dark_b[BLD] = 1.0
        else:
            dark_b[BLD] = 0.0
        J.set_buildings(dark=dark_b)
        show = float(E.SR_SHOW[0] - 0.6 <= t < E.SR_SHOW[1] + 0.4)   # 아파트 한 동 장면에서만
        K.set_points(marks, slots, scale=np.full(len(slots), show), size=np.tile((3.2, 0.12, 1.9), (len(slots), 1)),
                     rot=np.tile((0, 0, fr["ang"]), (len(slots), 1)), col=col)
        n = len(sim["shirt"])
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(n)], scale=np.ones(n), rot=np.c_[np.zeros((n, 2)), sim["py"][f]],
                     col=sim["shirt"], colors={"col2": sim["pants"]}, pose=pose_of(sim["ph"][f]))
        nc = len(sim["ccol"])
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(nc)], scale=np.full(nc, 10.0),
                     rot=np.c_[np.zeros((nc, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)
    ctx.anchor("hero", lambda t: tuple(float(v) + (0.0 if i < 2 else 0.6) for i, v in
                                       enumerate(sim["hero_w"][min(len(sim["hero_w"]) - 1, int(round(t * FPS)))])))
    ctx.anchor("tower", lambda t: (14.0, -6.0, 420.0))
    ctx.anchor("facade", lambda t: (float(slots[0][0]), float(slots[0][1]), float(slots[0][2]) + 6.0))
