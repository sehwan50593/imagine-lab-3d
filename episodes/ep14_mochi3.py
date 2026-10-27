"""EP14 모찌 가게가 한정선·고디바·노티드 세 곳뿐이라면, 사람들은 어디로 몰릴까? (잠실)

실제로 계산하는 것 (1분 단위 대기열 시뮬레이션):
- 고디바: 전날 밤부터 줄, 새벽 6시 반 등록 마감, 하루 150개 한정 → 151번째부터 허탕
- 한정선: 10:30 개장, 시간당 약 214팀 입장(대기 214팀 ≈ 1시간, MTN 2026-10-02)
- 노티드: 13시부터 줄, 14시 판매 시작, 시간당 약 72명·하루 300개 (가정)
- 손님 선택: 인기(네이버 검색량) + 줄이 길수록 끌림(Kremer & Debo 2016) − 예상 대기 시간,
  각자 기다릴 수 있는 한계(설문: 15분 27%·30분 51%·45분 16%·1시간 4%·그 이상 2%)를 넘으면 포기
  (한정선은 캐치테이블로 원격 대기라 한계 2배로 둠)
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, light_keys, people_colors, pose_of, sky_at, traffic

DUR = 56.0
META = {"id": "ep14", "title": "모찌 가게가 세 곳뿐이라면 사람들은 어디로 몰릴까?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "D", "mode": "major", "bpm": 84, "seed": 14, "twist_at": 46.0}}
NAMES = ["한정선", "고디바", "노티드"]
COLS = [(1.0, 0.45, 0.65), (1.0, 0.72, 0.28), (0.45, 0.80, 1.0)]
COLN = ["pink", "yellow", "cyan"]
# 세 가게를 롯데월드몰 남쪽 광장에 앞뒤로 (한 화면에 다 보이게, 10-28 오너: 고정 시점)
# 가게는 왼쪽(서쪽), 줄은 오른쪽으로 가로로 늘어서서 길이가 한눈에 보임 — 뒤 한정선 · 가운데 노티드 · 앞 고디바
HEAD_X, TAIL_X = -38.0, -8.0
BAND_Y = [[-58.0 - 2.5 * i for i in range(6)], [-78.0, -80.5, -83.0], [-91.0 - 2.5 * i for i in range(6)]]


def _zig(ys):
    return [((HEAD_X, y), (TAIL_X, y)) if i % 2 == 0 else ((TAIL_X, y), (HEAD_X, y)) for i, y in enumerate(ys)]


ROWS = [_zig(BAND_Y[0]), _zig(BAND_Y[2]), _zig(BAND_Y[1])]     # 0 한정선(뒤), 1 고디바(앞), 2 노티드(가운데)
HEAD = [(HEAD_X - 3.0, ROWS[j][0][0][1]) for j in range(3)]
EXIT = [(-1.0, 0.15), (-1.0, -0.15), (-1.0, 0.0)]
ENTRIES = [(-260.0, 40.0), (-240.0, -60.0), (-100.0, -180.0), (40.0, -120.0)]
MALL = (-41.0, 20.0)
POPULAR = np.log([123.0, 7.14, 25.0])          # 네이버 월간 검색(만 건): 한정선·고디바 모찌, 노티드는 가정
HERD, WAIT_W = 0.6, 0.02
MU = [214 / 60.0, None, 72 / 60.0]             # 분당 입장(서비스) — 노티드는 가정
STOCK_K, CAP_G = 300, 150
TOL = ([15, 30, 45, 60, 90], [0.27, 0.51, 0.16, 0.04, 0.02])
POOL = 700
SPACING = 0.7
RATE = 0.25   # 장면 안에서는 영상 1초 = 15초 (사람 움직임이 자연스럽게), 장면 사이에서만 시간이 건너뜀
SCENES = [(0.0, 4.5, 270.0), (4.5, 10.0, 365.0), (10.0, 16.0, 640.0), (16.0, 22.0, 750.0), (22.0, 28.0, 842.0),
          (28.0, 34.0, 930.0), (34.0, 40.0, 1020.0), (40.0, 46.0, 1192.0), (46.0, 56.0, 1200.0)]
CLOCK = []
for _t0, _t1, _m in SCENES:
    CLOCK += [(_t0 + 0.005, _m), (_t1 - 0.005, _m + (RATE * (_t1 - _t0) if _m < 1200 else 0.0))]
CLOCK[0] = (0.0, CLOCK[0][1])
FLASH = [(t0, 0.22, (0.0, 0.0, 0.0)) for t0, _, _ in SCENES[1:]]   # 장면 전환 = 눈 깜빡임
WALK = 1.4    # m/s


def clock_at(t):
    return keyed(t, CLOCK, ease=lambda u: u)


def lam(m):
    """분당 도착 (주말 롯데월드몰 가정)."""
    for a, b, v in ((270, 390, 1.4), (390, 600, 0.0), (600, 720, 6.0), (720, 840, 7.0), (840, 1020, 8.0),
                    (1020, 1140, 6.0), (1140, 1200, 3.0)):
        if a <= m < b:
            return v
    return 0.0


def slots(j, n=POOL):
    pts = []
    for a, b in ROWS[j]:
        a, b = np.array(a), np.array(b)
        k = int(np.hypot(*(b - a)) / SPACING)
        pts += [a + (b - a) * (i / k) for i in range(k)]
    return np.array(pts, np.float32)


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def simulate(build_dir):
    from engine.jamsil import geometry, use_area
    use_area("jamsil")
    geometry()
    rs = np.random.default_rng(1414)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    clock = np.array([clock_at(t) for t in ts], np.float32)
    arr = [[], [], []]     # 줄에 선 시각(분)
    srv = [[], [], []]     # 차례가 끝난 시각 (구매 또는 허탕으로 떠남)
    got = [[], [], []]     # 샀는지
    balk = []              # (시각, 가게)
    # ── 고디바 새벽 줄: 전날 21시부터 60명, 04:30~06:30 분당 1.4명, 06:30 마감 → 앞 150명만 ──
    g_arr = sorted(list(rs.uniform(-180, 270, 60)) + list(270 + np.cumsum(rs.exponential(1 / 1.4, 400))))
    g_arr = [a for a in g_arr if a < 390]
    for k, a in enumerate(g_arr):
        arr[1].append(a)
        srv[1].append(390.0 + 0.04 * k)
        got[1].append(k < CAP_G)
    # ── 낮: 한 명씩 도착 → 선택 ──
    m, last = 600.0, [600.0, 0.0, 780.0]
    q_srv = [[], [], []]
    sold_k = 0
    while m < 1200:
        rate = lam(m)
        if rate <= 0:
            m += 1.0
            continue
        m += rs.exponential(1 / rate)
        if m >= 1200:
            break
        tol = rs.choice(TOL[0], p=TOL[1])
        util, feas = [], []
        for j in (0, 2):
            opened = (m >= 600) if j == 0 else (m >= 780)
            if not opened or (j == 2 and sold_k >= STOCK_K):
                continue
            q = sum(1 for s in q_srv[j] if s > m)
            start = 630.0 if j == 0 else 840.0
            wait = q / MU[j] + max(0.0, start - m)
            if wait <= tol * (2.0 if j == 0 else 1.0):   # 한정선은 캐치테이블 원격 줄서기
                util.append(POPULAR[j] + HERD * math.log1p(q) - WAIT_W * wait + rs.gumbel())
                feas.append(j)
        if not feas:
            balk.append((m, 0 if m < 780 else int(rs.integers(0, 2)) * 2))
            continue
        j = feas[int(np.argmax(util))]
        start = 630.0 if j == 0 else 840.0
        s = max(m, start, last[j]) + rs.exponential(1 / MU[j])
        if j == 2:
            sold_k += 1
        last[j] = s
        arr[j].append(m)
        srv[j].append(s)
        got[j].append(True)
        q_srv[j].append(s)
    out = {}
    for j in range(3):
        a, s = np.array(arr[j], np.float32), np.array(srv[j], np.float32)
        out[f"arr{j}"], out[f"srv{j}"], out[f"got{j}"] = a, s, np.array(got[j], np.float32)
        out[f"ta{j}"] = np.interp(a, clock, ts).astype(np.float32)          # 영상 시각
        out[f"ts{j}"] = np.interp(s, clock, ts).astype(np.float32)
        out[f"ent{j}"] = rs.integers(0, len(ENTRIES), len(a)).astype(np.int8)
        sh, pa = people_colors(rs, len(a))
        out[f"shirt{j}"], out[f"pants{j}"] = sh, pa
        out[f"q{j}"] = np.array([((a <= c) & (s > c)).sum() for c in clock], np.float32)
        out[f"done{j}"] = np.array([((s <= c) & (out[f"got{j}"] > 0)).sum() for c in clock], np.float32)
    bt = np.array([b[0] for b in balk], np.float32)
    out["balk_t"] = np.interp(bt, clock, ts).astype(np.float32)
    out["balk_shop"] = np.array([b[1] for b in balk], np.int8)
    out["balk_n"] = np.array([(bt <= c).sum() for c in clock], np.float32) + \
        np.array([((out["srv1"] <= c) & (out["got1"] < 1)).sum() for c in clock], np.float32)
    out["clock"] = clock
    pp, py, ph = crowd(rs, nf, 260, (-20.0, 0.0), 330)
    out.update(pp=pp, py=py, ph=ph)
    out["shirt"], out["pants"] = people_colors(rs, 260)
    cp, cy = traffic(rs, nf, 90, (0.0, 0.0), 700)
    out.update(cp=cp, cy=cy, ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), 90)])
    tot = [int(out[f"done{j}"][-1]) for j in range(3)]
    print("판매:", dict(zip(NAMES, tot)), "포기·허탕:", int(out["balk_n"][-1]), "최대 줄:",
          [int(out[f"q{j}"].max()) for j in range(3)])
    return out


def winner(sim):
    tot = [int(sim[f"done{j}"][-1]) for j in range(3)]
    j = int(np.argmax(tot))
    return j, tot


def big_result(t, sim):
    j, tot = winner(sim)
    n = int(tot[j] * min(1.0, max(0.0, (t - 40.3) / 2.5)))
    return f"{NAMES[j]} {n:,}명"


STYLE = "bench"   # 1인칭 벤치 시점 + 아래 자막 위주 + 오른쪽 일수 카운터 (10-27 오너)
BEATS = [
    Beat(0.0, 4.5, badge="가정", title="모찌 가게가 {yellow}세 곳{/}뿐이라면?",
         sub="오늘 새벽, 잠실에 모찌 가게가 딱 세 곳.\n사람들은 어디로 몰릴까요?"),
    Beat(4.5, 10.0, title="고디바 {yellow}새벽 줄{/}", big="150명", big_color="yellow",
         sub="해 뜨기도 전에 고디바 앞에 150명.\n하루 150개 한정이라 줄은 여기서 끝납니다."),
    Beat(10.0, 16.0, title="{pink}한정선{/} 문 열다", big="141팀", big_color="pink",
         sub="오전 10시 반, 한정선이 문을 열자\n10분 만에 141팀이 줄을 섭니다."),
    Beat(16.0, 22.0, title="줄이 {orange}줄을 부른다{/}",
         sub="긴 줄을 보면 '맛집인가 보다' 하고\n지나가던 사람까지 따라 섭니다."),
    Beat(22.0, 28.0, title="{cyan}노티드{/} 판매 시작",
         sub="오후 2시, 노티드가 팔기 시작하자\n짧은 줄로 갈아타는 사람이 생깁니다."),
    Beat(28.0, 34.0, title="기다림은 {cyan}30분{/}까지",
         sub="대부분은 30분 넘게 기다리지 않습니다.\n줄만 보고 돌아서는 사람이 늘어납니다."),
    Beat(34.0, 40.0, title="빈손으로 간 사람",
         big=lambda t, sim: f"{int(sim['balk_n'][fi(t)]):,}명", big_color="red",
         sub="줄이 길어 포기하거나 다 팔려서\n그냥 돌아간 사람이 이만큼입니다."),
    Beat(40.0, 46.0, title="가장 많이 몰린 곳", big=big_result, big_color="pink",
         sub="밤이 되어 세어 보니, 검색이 17배 많은\n한정선으로 가장 많은 사람이 몰렸습니다."),
    Beat(46.0, 51.5, badge="반전", title="사실은 {yellow}한 건물{/}",
         sub="세 가게는 모두 롯데월드몰 안에 있어서\n실제로는 셋 다 들르는 사람이 많습니다."),
    Beat(51.5, 56.0, title="",
         sub="당신이라면\n어디에 먼저 줄 서실 건가요?"),
]
GRADE = {"exposure": 0.95, "bloom": 0.28, "bloom_thr": 1.05, "vignette": 0.3}
SKY = [(0.0, "NIGHT"), (4.49, "NIGHT"), (4.51, "MORNING"), (9.99, "MORNING"), (10.01, "DAY"), (33.99, "DAY"),
       (34.01, "DUSK"), (39.99, "DUSK"), (40.01, "NIGHT"), (56.0, "NIGHT")]   # 하늘도 장면 전환 때만 바뀜
# 고정 시점: 광장 앞 육교 높이에서 세 가게를 한 화면에 (참고 영상처럼 장소는 그대로, 시간만 흐름)
EYE = (-25.0, -142.0, 20.0)
T_TOWER, T_SCENE = (14.0, -6.0, 260.0), (-25.0, -80.0, 0.0)
SHOTS = [  # (t0, t1, 시작 시선, 끝 시선, 시작 렌즈, 끝 렌즈)
    (0.0, 4.5, T_TOWER, T_SCENE, 18.0, 22.0),
    (4.5, 46.0, T_SCENE, (-25.0, -79.0, 0.0), 22.0, 23.0),
    (46.0, 51.5, T_SCENE, (0.0, -20.0, 60.0), 23.0, 18.0),
    (51.5, 56.0, (0.0, -20.0, 60.0), T_TOWER, 18.0, 17.0)]


def cam_at(t):
    for t0, t1, a, b, l0, l1 in SHOTS:
        if t < t1 or t1 == SHOTS[-1][1]:
            u = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
            u = u * u * (3 - 2 * u)
            return tuple(x + (y - x) * u for x, y in zip(a, b)), l0 + (l1 - l0) * u


def banner_pos(j, t):
    """가게 표시 기둥: 반전 때 롯데월드몰로 모임 (한정선·고디바 지하1층 = 바닥, 노티드 5층)."""
    hx, hy = HEAD[j]
    u = ramp(t, 46.3, 48.3)
    tz = (0.0, 0.0, 22.0)[j]
    tx, ty = MALL[0] + (j - 1) * 9.0, MALL[1] - 22.0
    return hx + (tx - hx) * u, hy + (ty - hy) * u, tz * u


def sky(t):
    return sky_at(t, SKY)


def counter(t, sim):
    c = float(sim["clock"][fi(t)])
    return "1일차", f"{int(c // 60):02d}:{int(c % 60):02d}"


def labels(t, anchors, sim):
    """줄마다 한가운데 위에 '가게 이름 · 대기 n명' (어느 줄이 어느 가게인지 한눈에)."""
    out = []
    if t >= 46.3:
        return out
    f = fi(t)
    for j in range(3):
        a = anchors.get(f"q{j}")
        if not (a and a[3]):
            continue
        q = int(sim[f"q{j}"][f])
        if j == 1 and t >= 9.4:
            txt = "고디바 · 완판"
        elif j == 2 and t < 22.0:
            txt = "노티드 · 14시 판매"
        else:
            txt = f"{NAMES[j]} · 대기 {q}명"
        out.append({"x": min(960.0, max(130.0, a[0])), "y": a[1], "text": txt, "color": COLN[j], "size": 40,
                    "alpha": 1.0 if t < 45.8 else max(0.0, (46.3 - t) * 2)})
    return out


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry, use_area
    use_area("jamsil")
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    nb = J.nb
    J.set_buildings(gcol=np.tile((1.0, 0.72, 0.28), (nb, 1)).astype(np.float32), glow=np.zeros(nb),
                    dark=np.zeros(nb))
    tr = J.tree_xy
    # 카메라와 세 줄 사이(시야 부채꼴) 나무 치움
    rel = tr - np.array(EYE[:2])
    near = (rel[:, 1] > -5) & (rel[:, 1] < 90) & (np.abs(rel[:, 0]) < 12 + rel[:, 1] * 0.45)
    K.set_points(J.to, np.c_[tr, np.zeros(len(tr))], scale=np.where(near, 0.0, J.tree_s0))
    walkers = J.people(260, "walkers")
    co = J.cars(90)
    qp = [J.people(POOL, f"q{j}") for j in range(3)]
    boxm = K.mat_inst("m_mbox", 0.35, emit_attr=None)
    box = K.proto(ctx, "p_mbox", K.bm_cube(0.32, 0.22, 0.12, (0, 0, 0)), [boxm])
    bx = [K.instancer(ctx, f"box{j}", box, POOL) for j in range(3)]
    ban_m = []
    for j in range(3):
        m = K.mat_simple(f"m_ban{j}", COLS[j], 0.4, emit=COLS[j], estr=1.0)
        ban_m.append(K.proto(ctx, f"p_ban{j}", K.bm_cube(2.4, 2.4, 9.0, (0, 0, 0), bottom=True), [m]))
    bans = [K.instancer(ctx, f"ban{j}", ban_m[j], 1) for j in range(3)]
    sl = [slots(j) for j in range(3)]
    lk = [(k, dict(v, energy=max(v["energy"], 0.7), amb=max(v["amb"], 0.11))) for k, v in light_keys(SKY)]
    ent = np.array(ENTRIES, np.float32)

    def slot_pos(j, r):
        r = np.clip(r, 0, len(sl[j]) - 1.001)
        i = np.floor(r).astype(int)
        u = (r - i)[:, None]
        return sl[j][i] * (1 - u) + sl[j][np.minimum(i + 1, len(sl[j]) - 1)] * u

    clk = sim["clock"]

    def jump(tv):
        g = fi(tv)
        return clk[min(len(clk) - 1, g + 2)] - clk[max(0, g - 2)] > 1.0

    def upd(t, f):
        tgt, lens = cam_at(t)
        J.cam.look(EYE, tgt, lens)
        night = J.light(t, lk)
        ctx.set_ctl("lights", 0.12 + 0.6 * night)
        ctx.set_ctl("carlights", 0.2 + 0.8 * night)
        for j in range(3):
            ta, tsv, got = sim[f"ta{j}"], sim[f"ts{j}"], sim[f"got{j}"]
            n = len(ta)
            pos = np.zeros((POOL, 2), np.float32)
            yaw = np.zeros(POOL, np.float32)
            sc = np.zeros(POOL, np.float32)
            walk = np.zeros(POOL, bool)
            bsc = np.zeros(POOL, np.float32)
            # 지금 보일 사람: 줄 뒤로 걸어 들어오는 중(3.5초) / 줄 / 떠나는 중(6초)
            idx = np.where((ta - 3.5 <= t) & (tsv + 6.0 > t))[0]
            if len(idx):
                c = float(sim["clock"][f])
                ahead_done = np.searchsorted(np.sort(sim[f"srv{j}"]), c)
                qn = float(sim[f"q{j}"][f])
                for k in idx:
                    p = k % POOL
                    if t < ta[k]:              # 걸어오는 중: 장면 안에서 온 사람만 (시간이 건너뛸 때 온 사람은 이미 줄에)
                        if jump(ta[k]):
                            continue
                        r = qn + (ta[k] - t) * WALK / SPACING
                        if r >= len(sl[j]) - 1:
                            continue
                        q = slot_pos(j, np.array([r]))[0]
                        d = slot_pos(j, np.array([max(0.0, r - 1.0)]))[0] - q
                        pos[p], yaw[p], sc[p], walk[p] = q, math.atan2(d[1], d[0]), 1.0, True
                    elif t < tsv[k]:           # 줄
                        r = k - ahead_done
                        if r < len(sl[j]):
                            q = slot_pos(j, np.array([float(r)]))[0]
                            nxt = slot_pos(j, np.array([max(0.0, r - 1.0)]))[0]
                            d = nxt - q
                            pos[p], sc[p] = q, 1.0
                            yaw[p] = math.atan2(d[1], d[0]) if np.hypot(*d) > 1e-3 else math.atan2(*EXIT[j][::-1])
                    else:                      # 떠남 (장면 안에서 끝난 사람만 걸어서 나감)
                        if jump(tsv[k]):
                            continue
                        u = t - tsv[k]
                        e = np.array(EXIT[j], np.float32)
                        e /= np.linalg.norm(e)
                        q = np.array(HEAD[j], np.float32) + e * u * WALK + np.array([0.0, 0.25 * (k % 7) - 0.75])
                        pos[p], yaw[p], sc[p], walk[p] = q, math.atan2(e[1], e[0]), min(1.0, (6.0 - u) * 2), True
                        bsc[p] = sc[p] * got[k] * (j != 1)   # 고디바는 새벽엔 번호표만
            K.set_points(qp[j], np.c_[pos, np.zeros(POOL)], scale=sc, rot=np.c_[np.zeros((POOL, 2)), yaw],
                         col=sim[f"shirt{j}"][np.arange(POOL) % max(1, n)] if n else np.ones((POOL, 3)),
                         colors={"col2": sim[f"pants{j}"][np.arange(POOL) % max(1, n)] if n else np.ones((POOL, 3))},
                         pose=np.where(walk, 1 + (np.floor(t * 2.6 + np.arange(POOL) * 0.37) % 4), 0).astype(np.float32))
            fwd = np.stack([np.cos(yaw), np.sin(yaw)], 1)
            side = np.stack([-np.sin(yaw), np.cos(yaw)], 1)
            K.set_points(bx[j], np.c_[pos + fwd * 0.18 + side * 0.28, np.full(POOL, 0.85)], scale=bsc,
                         rot=np.c_[np.zeros((POOL, 2)), yaw], col=np.tile(COLS[j], (POOL, 1)))
            x, y, z = banner_pos(j, t)
            on = 1.0
            K.set_points(bans[j], [(x, y, z)], scale=[on * (0.6 if (j == 1 and 9.4 <= t < 46.0) else 1.0)],
                         rot=[(0, 0, 0)], col=[COLS[j]])
        K.set_points(walkers, np.c_[sim["pp"][f], np.zeros(260)],
                     scale=(np.hypot(sim["pp"][f][:, 0] - EYE[0], sim["pp"][f][:, 1] - EYE[1]) > 12.0).astype(np.float32),
                     rot=np.c_[np.zeros((260, 2)), sim["py"][f]], col=sim["shirt"], colors={"col2": sim["pants"]},
                     pose=pose_of(sim["ph"][f]))
        cpf = sim["cp"][f]
        in_zone = (cpf[:, 0] > -60) & (cpf[:, 0] < 5) & (cpf[:, 1] > -112) & (cpf[:, 1] < -50)   # 줄 선 광장엔 차 없음
        K.set_points(co, np.c_[cpf, np.zeros(90)], scale=np.where(in_zone, 0.0, 10.0),
                     rot=np.c_[np.zeros((90, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)
    for j in range(3):
        ctx.anchor(f"shop{j}", (lambda jj: (lambda t: (*banner_pos(jj, t)[:2], banner_pos(jj, t)[2] + 11.0)))(j))
    ctx.anchor("mall", lambda t: (MALL[0], MALL[1], 70.0))
    for j in range(3):
        ys = [r[0][1] for r in ROWS[j]]
        ctx.anchor(f"q{j}", (lambda x, y: (lambda t: (x, y, 4.5)))((HEAD_X + TAIL_X) / 2, sum(ys) / len(ys)))
