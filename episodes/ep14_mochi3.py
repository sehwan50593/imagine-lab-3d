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
# 줄(앞→뒤, 지그재그), 가게 앞, 나가는 방향
ROWS = [[((-116.0, -20.0), (-116.0, 40.0)), ((-110.0, 40.0), (-110.0, -20.0)), ((-122.0, -20.0), (-122.0, 40.0))],
        [((-60.0, -61.0), (8.0, -61.0)), ((8.0, -67.0), (-60.0, -67.0)), ((-60.0, -73.0), (8.0, -73.0))],
        [((-176.0, -130.0), (-176.0, -70.0)), ((-170.0, -70.0), (-170.0, -130.0)), ((-182.0, -130.0), (-182.0, -70.0))]]
HEAD = [(-116.0, -24.0), (-64.0, -61.0), (-176.0, -134.0)]
EXIT = [(-1.0, -0.3), (-0.6, -1.0), (0.4, -1.0)]
ENTRIES = [(-260.0, 40.0), (-240.0, -60.0), (-100.0, -180.0), (40.0, -120.0)]
MALL = (-41.0, 20.0)
POPULAR = np.log([123.0, 7.14, 25.0])          # 네이버 월간 검색(만 건): 한정선·고디바 모찌, 노티드는 가정
HERD, WAIT_W = 0.6, 0.02
MU = [214 / 60.0, None, 72 / 60.0]             # 분당 입장(서비스) — 노티드는 가정
STOCK_K, CAP_G = 300, 150
TOL = ([15, 30, 45, 60, 90], [0.27, 0.51, 0.16, 0.04, 0.02])
POOL = 700
SPACING = 0.7
CLOCK = [(0.0, 270.0), (4.5, 330.0), (9.4, 400.0), (10.0, 630.0), (16.0, 750.0), (22.0, 840.0), (28.0, 930.0),
         (34.0, 1020.0), (40.0, 1140.0), (45.0, 1200.0), (56.0, 1200.0)]


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


BEATS = [
    Beat(0.0, 4.5, badge="04:30", label="만약", title="모찌 가게가 {yellow}세 곳{/}뿐이라면\n사람들은 어디로 몰릴까?",
         title_size=70, note="한정선 4,000~6,500원 · 고디바 7,500~9,000원 · 노티드 5,500원 (2026년 10월)",
         sub="잠실에 모찌 가게가\n딱 세 곳만 있다고 해 봅시다."),
    Beat(4.5, 10.0, badge="06:00", title="고디바는 {yellow}새벽부터{/}", big="150명", big_size=110, big_color="yellow",
         note="전날 밤 9시 첫 대기 · 새벽 6시 150명 넘게 줄 100m 이상 (헤럴드경제, 2026.10)",
         sub="하루 150개 한정이라\n해 뜨기 전에 줄이 끝납니다."),
    Beat(10.0, 16.0, badge="10:30", title="한정선 문 열자 {pink}폭발{/}", big="검색 17배", big_size=100, big_color="pink",
         note="네이버 월간 검색: 한정선 123만 · 고디바 모찌 7만 1,400 (블랙키위, 9~10월, 편의점 상품 포함)",
         sub="문 연 지 10분 만에\n앞에 141팀이 기다립니다."),
    Beat(16.0, 22.0, badge="12:30", title="줄이 {orange}줄을 부른다{/}",
         note="모르는 손님은 긴 줄을 '맛있다'는 신호로 읽는다 (Kremer & Debo 2016)",
         sub="'인기 메뉴'라고만 적어도\n주문이 13~20% 늘었습니다 (Cai 외 2009)."),
    Beat(22.0, 28.0, badge="14:00", title="오후 2시, {cyan}노티드{/} 합류",
         note="롯데월드몰점 한정 '도넛 찹쌀떡' 5,500원, 매일 14시 판매 (2026.10.20 출시)",
         sub="새 줄이 생기자\n짧은 줄로 갈아타는 사람이 생깁니다."),
    Beat(28.0, 34.0, badge="15:30", title="그래도 {cyan}30분{/}이 한계",
         note="맛집 대기 한계: 30분 이하 78% · 1시간 이상 6% (요리연구소 혼신 설문 402명, 2026)",
         sub="예상 대기가 길면\n줄만 보고 그냥 돌아섭니다."),
    Beat(34.0, 40.0, badge="17:00", title="돌아선 사람",
         big=lambda t, sim: f"{int(sim['balk_n'][fi(t)]):,}명", big_size=110, big_color="red",
         note="줄이 10명→15명이면 구매율 30%→27% (Lu 외 2013, 마트 델리 줄)",
         sub="고디바 허탕까지 합치면\n빈손으로 간 사람이 꽤 많습니다."),
    Beat(40.0, 46.0, badge="20:00", title="가장 많이 몰린 곳은?", big=big_result, big_size=104, big_color="pink",
         note="하루 판매 시뮬레이션 결과 (노티드 수량·속도는 가정)",
         sub="검색량 17배의 힘.\n줄이 길어도 사람들은 결국 여기로 왔습니다."),
    Beat(46.0, 51.5, badge="반전", title="세 가게는 사실 {yellow}한 건물{/}", big="롯데월드몰", big_size=100,
         note="고디바 지하1층 · 한정선 같은 층(SNS) · 노티드 5층 (뉴시스, 2026.10.22)",
         sub="그래서 실제로는 고르지 않습니다.\n'고디바 → 한정선 → 노티드', 셋 다 갑니다."),
    Beat(51.5, 56.0, badge="지금", title="당신이라면\n어디에 {yellow}먼저{/} 줄 서실 건가요?", title_size=72),
]
GRADE = {"exposure": 0.95, "bloom": 0.28, "bloom_thr": 1.05, "vignette": 0.3}
SKY = [(0.0, "NIGHT"), (5.0, "NIGHT"), (7.2, "MORNING"), (9.6, "DAY"), (35.5, "DAY"), (37.5, "DUSK"),
       (39.5, "NIGHT"), (56.0, "NIGHT")]
WIDE = (-128.0, -72.0, 0.0)      # 세 줄이 다 보이는 곳 — 남쪽(석촌호수 쪽)에서 봐서 타워는 뒤 배경
CAM = [(0.0, WIDE, 262, 54, 380.0, 30), (4.3, WIDE, 270, 52, 345.0, 30),
       (4.7, (-26.0, -67.0, 3.0), 272, 26, 52.0, 30), (9.8, (-26.0, -67.0, 3.0), 282, 28, 48.0, 30),
       (10.2, (-116.0, 8.0, 2.0), 200, 34, 72.0, 30), (15.8, (-116.0, 8.0, 2.0), 212, 36, 66.0, 30),
       (16.2, (-90.0, -30.0, 2.0), 262, 44, 200.0, 30), (21.8, (-90.0, -30.0, 2.0), 272, 44, 185.0, 30),
       (22.2, (-176.0, -100.0, 2.0), 315, 32, 66.0, 30), (27.8, (-176.0, -100.0, 2.0), 325, 34, 62.0, 30),
       (28.2, WIDE, 265, 54, 370.0, 30), (33.8, WIDE, 275, 54, 350.0, 30),
       (34.2, (-116.0, 10.0, 2.0), 215, 40, 125.0, 30), (39.8, (-116.0, 10.0, 2.0), 225, 42, 135.0, 30),
       (40.2, WIDE, 260, 56, 400.0, 30), (45.8, WIDE, 270, 56, 380.0, 30),
       (46.2, (-41.0, 20.0, 25.0), 220, 24, 270.0, 30), (51.3, (-41.0, 20.0, 25.0), 232, 26, 250.0, 30),
       (51.7, WIDE, 262, 46, 340.0, 30), (56.0, WIDE, 272, 50, 400.0, 30)]


def banner_pos(j, t):
    """가게 표시 기둥: 반전 때 롯데월드몰로 모임 (한정선·고디바 지하1층 = 바닥, 노티드 5층)."""
    hx, hy = HEAD[j]
    u = ramp(t, 46.3, 48.3)
    tz = (0.0, 0.0, 22.0)[j]
    tx, ty = MALL[0] + (j - 1) * 9.0, MALL[1] - 22.0
    return hx + (tx - hx) * u, hy + (ty - hy) * u, tz * u


def sky(t):
    return sky_at(t, SKY)


def hud(t, sim):
    f = fi(t)
    c = float(sim["clock"][f])
    clock = f"{int(c // 60):02d}:{int(c % 60):02d}"
    if t < 40.0:
        r2 = " · ".join(f"{NAMES[j]} {int(sim[f'q{j}'][f])}" for j in range(3)) + " (대기)"
        if 4.5 <= t < 10.0:
            n = int((sim["arr1"] <= c).sum())
            r2 = f"고디바 줄 {int(sim['q1'][f])}명 · 남은 번호 {max(0, 150 - n)}개" if t < 9.0 else "고디바 등록 마감 · 완판"
    elif t < 46.0:
        r2 = " · ".join(f"{NAMES[j]} {int(sim[f'done{j}'][f]):,}" for j in range(3)) + " (판매)"
    else:
        r2 = "세 가게 모두 롯데월드몰"
    return {"left": "SIMULATION", "right": clock, "right2": r2}


def labels(t, anchors, sim):
    out = []
    if t >= 51.5:
        return out
    for j in range(3):
        a = anchors.get(f"shop{j}")
        if a and a[3] and 480 < a[1] < 1440 and 40 < a[0] < 1040:
            sold = (j == 1 and t >= 9.4)
            txt = NAMES[j] + (" · 완판" if sold else "") + (" (14시 판매)" if j == 2 and t < 22.0 else "")
            out.append({"x": a[0], "y": a[1], "text": txt, "color": COLN[j], "size": 26})
    a = anchors.get("mall")
    if a and a[3] and 46.6 < t < 51.4 and 480 < a[1] < 1440:
        out.append({"x": a[0], "y": a[1], "text": "롯데월드몰", "color": "white", "size": 28,
                    "alpha": ramp(t, 46.6, 47.2)})
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
    walkers = J.people(260, "walkers")
    co = J.cars(90)
    qp = [J.people(POOL, f"q{j}") for j in range(3)]
    boxm = K.mat_inst("m_mbox", 0.35, emit_attr=None)
    box = K.proto(ctx, "p_mbox", K.bm_cube(0.32, 0.22, 0.12, (0, 0, 0)), [boxm])
    bx = [K.instancer(ctx, f"box{j}", box, POOL) for j in range(3)]
    ban_m = []
    for j in range(3):
        m = K.mat_simple(f"m_ban{j}", COLS[j], 0.4, emit=COLS[j], estr=2.5)
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

    def upd(t, f):
        tgt, az, el, dist, lens = (lambda v: (v[:3], v[3], v[4], v[5], v[6]))(
            keyed(t, [(k[0], (*k[1], k[2], k[3], k[4], k[5])) for k in CAM]))
        J.cam.set(tgt, az, el, dist, lens, shift=0.04)
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
            # 지금 보일 사람: 걸어오는 중(1초) / 줄 / 떠나는 중(2.5초)
            idx = np.where((ta - 1.0 <= t) & (tsv + 2.5 > t))[0]
            if len(idx):
                served = (tsv <= t)
                # 줄 안 순서 = 나보다 먼저 와서 아직 안 끝난 사람 수 (분 단위 시각으로 매끄럽게)
                c = float(sim["clock"][f])
                ahead_done = np.searchsorted(np.sort(sim[f"srv{j}"]), c)
                for k in idx:
                    p = k % POOL
                    if t < ta[k]:              # 걸어오는 중
                        u = (t - (ta[k] - 1.0))
                        e = ent[sim[f"ent{j}"][k]]
                        tail = sl[j][min(len(sl[j]) - 1, int(sim[f"q{j}"][f]))]
                        q = e + (tail - e) * u
                        d = tail - e
                        pos[p], yaw[p], sc[p], walk[p] = q, math.atan2(d[1], d[0]), min(1.0, u * 3), True
                    elif not served[k]:        # 줄
                        r = k - ahead_done
                        if r < len(sl[j]):
                            q = slot_pos(j, np.array([float(r)]))[0]
                            nxt = slot_pos(j, np.array([max(0.0, r - 1.0)]))[0]
                            d = nxt - q
                            pos[p], sc[p] = q, 1.0
                            yaw[p] = math.atan2(d[1], d[0]) if np.hypot(*d) > 1e-3 else math.atan2(*EXIT[j][::-1])
                    else:                      # 떠남
                        u = t - tsv[k]
                        e = np.array(EXIT[j], np.float32)
                        e /= np.linalg.norm(e)
                        q = np.array(HEAD[j], np.float32) + e * u * 7.0 + np.array([0.0, 0.25 * (k % 7) - 0.75])
                        pos[p], yaw[p], sc[p], walk[p] = q, math.atan2(e[1], e[0]), max(0.0, 1 - max(0.0, u - 2.0) * 2), True
                        bsc[p] = sc[p] * got[k] * (j != 1)   # 고디바는 새벽엔 번호표만
            K.set_points(qp[j], np.c_[pos, np.zeros(POOL)], scale=sc, rot=np.c_[np.zeros((POOL, 2)), yaw],
                         col=sim[f"shirt{j}"][np.arange(POOL) % max(1, n)] if n else np.ones((POOL, 3)),
                         colors={"col2": sim[f"pants{j}"][np.arange(POOL) % max(1, n)] if n else np.ones((POOL, 3))},
                         pose=np.where(walk, 1 + (np.floor(t * 4 + np.arange(POOL) * 0.37) % 4), 0).astype(np.float32))
            fwd = np.stack([np.cos(yaw), np.sin(yaw)], 1)
            side = np.stack([-np.sin(yaw), np.cos(yaw)], 1)
            K.set_points(bx[j], np.c_[pos + fwd * 0.18 + side * 0.28, np.full(POOL, 0.85)], scale=bsc,
                         rot=np.c_[np.zeros((POOL, 2)), yaw], col=np.tile(COLS[j], (POOL, 1)))
            x, y, z = banner_pos(j, t)
            on = 1.0
            K.set_points(bans[j], [(x, y, z)], scale=[on * (0.6 if (j == 1 and 9.4 <= t < 46.0) else 1.0)],
                         rot=[(0, 0, 0)], col=[COLS[j]])
        K.set_points(walkers, np.c_[sim["pp"][f], np.zeros(260)], scale=np.ones(260),
                     rot=np.c_[np.zeros((260, 2)), sim["py"][f]], col=sim["shirt"], colors={"col2": sim["pants"]},
                     pose=pose_of(sim["ph"][f]))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(90)], scale=np.full(90, 10.0),
                     rot=np.c_[np.zeros((90, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)
    for j in range(3):
        ctx.anchor(f"shop{j}", (lambda jj: (lambda t: (*banner_pos(jj, t)[:2], banner_pos(jj, t)[2] + 11.0)))(j))
    ctx.anchor("mall", lambda t: (MALL[0], MALL[1], 70.0))
