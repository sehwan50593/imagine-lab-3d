"""EP10 만약 고디바 모찌가 전 세계적인 열풍이 된다면? (잠실 롯데월드몰)

실제로 계산하는 것:
- 새벽 대기열: 도착(시간대별 포아송) → 10:30 판매 시작, 하루 150개 한정 → 151번째부터 빈손 귀가
- 열풍 확산: Bass 모형(p=0.03, q=0.38, 1단위=10일) → 따라 하는 가게(금빛)가 잠실에 번지고, 유행이 식으면 폐업
- 거리 사람들: 산 사람은 금색 상자를 들고 걷고, 열풍 지수에 따라 비율이 바뀜
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import (CAR_COLORS, crowd, light_keys, people_colors, pose_of, set_cam, sky_at, traffic)

DUR = 56.0
META = {"id": "ep10", "title": "만약 고디바 모찌가 전 세계적인 열풍이 된다면?", "duration": DUR,
        "music": {"key": "Ab", "mode": "major", "bpm": 76, "seed": 10, "twist_at": 45.0}}
NQ, NW, NC = 330, 520, 120
ROWS = [((-60.0, -61.0), (8.0, -61.0)), ((8.0, -67.0), (-60.0, -67.0)), ((-60.0, -73.0), (8.0, -73.0))]
SPACING_Q = 0.72
SOLD = 150

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY 04:30", label="만약", title="{orange}고디바 모찌{/}가\n전 세계 열풍이 된다면?", title_size=72,
         note="지금은 잠실 롯데월드몰 한 곳에서만 판매",
         sub="새벽 4시 반, 잠실.\n문 열기 6시간 전부터 줄이 생깁니다."),
    Beat(4.5, 10.0, badge="D-DAY 10:30", title="하루 {yellow}150개{/} 한정", note="정가 7,500~9,000원 (2026년 10월)",
         sub="수령이 시작되는 10시 30분,\n151번째 손님부터는 빈손입니다."),
    Beat(10.0, 16.0, badge="D+7", title="리셀가 {red}3배{/}", big="8,500 → 25,000원", big_size=92,
         note="대리구매 호가 (한국경제, 2026)",
         sub="줄 서는 시간이 곧 돈이 됩니다.\n대신 줄 서 주는 사람이 등장합니다."),
    Beat(16.0, 22.0, badge="D+30", title="전 세계로 번진다", note="확산 모형: 혁신 0.03 · 모방 0.38 (Bass)",
         sub="영상 하나가 퍼지면\n세계 곳곳의 매장 앞에도 줄이 생깁니다."),
    Beat(22.0, 28.0, badge="D+60", title="{orange}카카오{/} 값이 다시 뛴다?", note="코코아 사상 최고가 톤당 약 1만 2,900달러 (2024.12)",
         sub="두바이 초콜릿 열풍 땐 피스타치오 값이\n1년 새 약 35% 올랐습니다."),
    Beat(28.0, 34.0, badge="D+90", title="{yellow}찹쌀{/}이 귀해진다", note="한국인 1인당 쌀 소비 53.9kg, 역대 최저 (2025)",
         sub="그런데 떡을 만드는 데 쓰는 쌀은\n한 해 동안 32% 늘었습니다."),
    Beat(34.0, 40.0, badge="D+120", title="골목마다 모찌 가게", note="탕후루 가게는 2023년 한 해 약 1,300곳 개업",
         sub="비슷한 가게가\n잠실 골목마다 문을 엽니다."),
    Beat(40.0, 45.0, badge="D+180", title="열풍은 생각보다 짧다", note="검색 열기 유지: 탕후루 159일 · 두쫀쿠 49일",
         sub="유행이 식으면\n가게도 하나둘 문을 닫습니다."),
    Beat(45.0, 52.0, badge="반전", title="벨기에 초콜릿의 주인은?", big="튀르키예", big_size=110, big_color="orange",
         note="2008년 튀르키예 기업 일디즈(Yildiz)가 8억 5천만 달러에 인수",
         sub="그리고 한국·일본 고디바는\n2019년부터 한국 사모펀드 MBK파트너스가 운영합니다."),
    Beat(52.0, 56.0, badge="지금", title="당신은 새벽 4시에\n{orange}줄 설 수 있나요?{/}", title_size=74),
]
GRADE = {"exposure": 0.95, "bloom": 0.26, "bloom_thr": 1.1, "vignette": 0.3}

SKY = [(0.0, "NIGHT"), (3.0, "NIGHT"), (4.6, "MORNING"), (6.0, "DAY"), (15.6, "DAY"), (17.0, "DUSK"), (18.4, "NIGHT"),
       (21.6, "NIGHT"), (22.6, "DAY"), (39.5, "DAY"), (41.0, "DUSK"), (44.6, "DUSK"), (45.6, "NIGHT"), (56.0, "NIGHT")]

# 시뮬레이션 시계: 영상 초 → 경과 일 (D-DAY 04:30 = 0.1875)
CLOCK = [(0.0, 0.1875), (4.5, 0.4375), (10.0, 0.47), (10.8, 7.0), (16.0, 8.0), (16.8, 30.0), (22.0, 32.0),
         (22.8, 60.0), (28.0, 62.0), (28.8, 90.0), (34.0, 93.0), (34.8, 120.0), (40.0, 123.0), (40.8, 180.0),
         (56.0, 184.0)]


def day_at(t):
    return keyed(t, CLOCK, ease=lambda u: u)


def bass(days, p=0.03, q=0.38, unit=10.0):
    x = np.asarray(days) / unit
    e = np.exp(-(p + q) * x)
    F = (1 - e) / (1 + (q / p) * e)
    f = (p + q) ** 2 / p * e / (1 + (q / p) * e) ** 2
    return F, f / ((p + q) ** 2 / (4 * q))  # 누적, 정점=1로 맞춘 확산 속도


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def queue_slots(n):
    pts = []
    for a, b in ROWS:
        a, b = np.array(a), np.array(b)
        L = np.hypot(*(b - a))
        k = int(L / SPACING_Q)
        for i in range(k):
            pts.append(a + (b - a) * (i / k))
    pts = np.array(pts, np.float32)[:n]
    yaw = np.zeros(len(pts), np.float32)
    for i in range(len(pts) - 1):
        d = pts[i] - pts[i + 1] if i + 1 < len(pts) else pts[i - 1] - pts[i]
        yaw[i] = math.atan2(d[1], d[0])
    yaw[-1] = yaw[-2]
    return pts, yaw


def simulate(build_dir):
    from engine.jamsil import geometry
    g = geometry()
    rs = np.random.default_rng(1010)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    days = np.array([day_at(t) for t in ts])
    F, heat = bass(days)
    # ── 대기열 ──
    slots, syaw = queue_slots(NQ)
    arrive = np.sort(rs.uniform(-1.6, 4.3, NQ))  # 영상 0초 전부터 도착 (시뮬레이션 03:00~10:00)
    q_on = np.zeros((nf, NQ), np.float32)
    q_pos = np.zeros((nf, NQ, 2), np.float32)
    q_yaw = np.zeros((nf, NQ), np.float32)
    q_box = np.zeros((nf, NQ), np.float32)
    serve_t0, serve_rate = 5.0, 34.0  # 10:30부터 초당 34명씩 (영상 속도)
    exit_dir = np.array([1.0, -0.6]) / np.hypot(1.0, 0.6)
    for i, t in enumerate(ts):
        served = int(max(0.0, (t - serve_t0) * serve_rate)) if t >= serve_t0 else 0
        served = min(served, NQ)
        for k in range(NQ):
            if t < arrive[k]:
                continue
            if k >= served:
                slot = k - served if k - served < len(slots) else len(slots) - 1
                q_pos[i, k] = slots[slot]
                q_yaw[i, k] = syaw[slot]
                q_on[i, k] = 1.0
            else:
                # 판매 끝난 사람: 상자 들고(150번까지) 혹은 빈손으로 떠남
                tk = serve_t0 + k / serve_rate
                dt_ = t - tk
                if dt_ < 6.0:
                    q_pos[i, k] = slots[0] + exit_dir * dt_ * 1.6 + np.array([0.0, -0.3 * (k % 5)])
                    q_yaw[i, k] = math.atan2(exit_dir[1], exit_dir[0])
                    q_on[i, k] = 1.0
                    q_box[i, k] = 1.0 if k < SOLD else 0.0
        if 9.4 <= t < 10.0:  # 장면 전환: 남은 줄은 해산
            q_on[i] *= max(0.0, 1 - (t - 9.4) / 0.6)
        elif 10.0 <= t < 16.0:  # D+7: 밤새 더 긴 줄 (대신 줄 서는 사람 포함)
            q_pos[i] = slots[np.minimum(np.arange(NQ), len(slots) - 1)]
            q_yaw[i] = syaw[np.minimum(np.arange(NQ), len(syaw) - 1)]
            q_on[i] = np.clip((t - 10.0) / 0.4, 0, 1) * (1 - np.clip((t - 15.6) / 0.4, 0, 1))
            q_box[i] = 0.0
        elif 16.0 <= t < 52.0:
            q_on[i] = 0.0
        else:  # 마지막: 다음 날 새벽, 다시 줄이 생김
            t2 = (t - 52.0) * 1.3 - 1.6
            for k in range(NQ):
                if arrive[k] <= t2:
                    q_pos[i, k] = slots[min(k, len(slots) - 1)]
                    q_yaw[i, k] = syaw[min(k, len(syaw) - 1)]
                    q_on[i, k] = 1.0
    # 매진 후 151번째부터는 줄에서 빠져 떠남(빈손)
    # ── 거리 군중 ──
    pp, py, ph = crowd(rs, nf, NW, (-20, -60), 330)
    shirt, pants = people_colors(rs, NW)
    box_frac = np.interp(days, [0, 7, 30, 120, 180], [0.02, 0.1, 0.35, 0.3, 0.06])
    holder = rs.random(NW)
    w_box = (holder[None, :] < box_frac[:, None]).astype(np.float32)
    # 대신 줄 서 주는 사람(빨간 조끼)은 D+7 장면 줄에 섞음
    cp, cy = traffic(rs, nf, NC, (0, 0), 900)
    # ── 따라 하는 가게(금빛): 몰 주변 저층 상가부터 확산 → 정점 뒤 폐업 ──
    cent, hts = g["b_cent"], g["b_h"]
    dist = np.hypot(cent[:, 0] + 40, cent[:, 1] - 20)
    cand = np.where((hts < 25) & (dist < 1100))[0]
    order = cand[np.argsort(dist[cand] + rs.uniform(0, 250, len(cand)))]
    nshop = len(order)
    open_at = np.linspace(0, 1, nshop) ** 1.4         # 누적 확산 F가 이 값을 넘으면 개업
    close_at = rs.uniform(0.15, 0.95, nshop)          # 열풍 지수가 이 값 아래로 내려가면 폐업 (정점 이후)
    shop_glow = np.zeros((nf, nshop), np.float32)
    peak_day = days[np.argmax(heat)]
    for i in range(nf):
        on = F[i] * 1.15 > open_at
        if days[i] > peak_day:
            on &= heat[i] > close_at * 0.55
        shop_glow[i] = on.astype(np.float32)
    shop_glow = np.clip(shop_glow * (ts[:, None] > 16.0), 0, 1)
    cocoa = 5490 * (1 + 0.9 * np.clip(F, 0, 1) * (ts > 22.0))
    q_shirt, q_pants = people_colors(rs, NQ)
    resell = rs.random(NQ) < 0.18
    q_shirt2 = np.where(resell[:, None], np.array([0.85, 0.12, 0.1], np.float32), q_shirt)
    return dict(q_shirt2=q_shirt2.astype(np.float32), resell=resell.astype(np.float32), days=days, F=F, heat=heat, q_on=q_on, q_pos=q_pos, q_yaw=q_yaw, q_box=q_box, pp=pp, py=py, ph=ph,
                shirt=shirt, pants=pants, w_box=w_box, cp=cp, cy=cy,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)], shops=order.astype(np.int32),
                shop_glow=shop_glow, cocoa=cocoa.astype(np.float32),
                q_shirt=q_shirt, q_pants=q_pants)


def sky(t):
    return sky_at(t, SKY)


def fmt_clock(d):
    if d < 1:
        h = d * 24
        return f"D-DAY {int(h):02d}:{int((h % 1) * 60):02d}"
    return f"D+{int(d)}"


def hud(t, sim):
    f = fi(t)
    d = float(sim["days"][f])
    if t < 10.0:
        waiting = int(sim["q_on"][f].sum())
        sold = min(SOLD, int(max(0, (t - 5.0) * 34)))
        r2 = f"대기 {waiting}명 · 남은 수량 {SOLD - sold}개"
    elif t < 45.0:
        r2 = f"열풍 지수 {int(100 * float(sim['heat'][f]))} · 모찌 가게 {int(sim['shop_glow'][f].sum())}곳 (가정)"
    else:
        r2 = "브랜드: 튀르키예 · 한국 운영: MBK"
    return {"left": "SIMULATION", "right": fmt_clock(d), "right2": r2}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("store")
    if a and a[3] and t < 10.0 and 500 < a[1] < 1400:
        out.append({"x": a[0], "y": a[1], "text": "고디바 매장 (지하1층)", "color": "yellow", "size": 26})
    a = anchors.get("q150")
    if a and a[3] and 4.5 < t < 9.4:
        out.append({"x": a[0], "y": a[1], "text": "여기부터 빈손", "color": "red", "size": 26,
                    "alpha": ramp(t, 5.0, 5.6)})
    return out


CAM = [(0.0, (-26.0, -67.0, 4.0), 272, 22, 46.0, 30), (4.4, (-26.0, -67.0, 4.0), 280, 24, 42.0, 30),
       (9.6, (-20.0, -66.0, 4.0), 292, 26, 44.0, 30), (10.2, (-26.0, -67.0, 2.0), 245, 34, 40.0, 30),
       (15.8, (-26.0, -67.0, 2.0), 232, 36, 46.0, 30), (16.4, (20.0, -20.0, 40.0), 230, 22, 520.0, 30),
       (21.8, (20.0, -20.0, 40.0), 250, 24, 560.0, 30), (22.4, (-60.0, -60.0, 3.0), 210, 36, 140.0, 30),
       (27.8, (-60.0, -60.0, 3.0), 225, 40, 160.0, 30), (28.4, (120.0, -90.0, 3.0), 300, 30, 60.0, 30),
       (33.8, (120.0, -90.0, 3.0), 315, 32, 70.0, 30), (34.4, (-200.0, 50.0, 10.0), 200, 52, 900.0, 28),
       (44.6, (-200.0, 50.0, 10.0), 230, 55, 1000.0, 28), (45.4, (14.0, -6.0, 220.0), 250, 10, 980.0, 32),
       (51.6, (14.0, -6.0, 220.0), 262, 12, 900.0, 32), (52.4, (-26.0, -67.0, 4.0), 268, 24, 48.0, 30),
       (56.0, (-26.0, -67.0, 4.0), 282, 26, 44.0, 30)]


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    po = J.people(NW, "walkers")
    qo = J.people(NQ, "queue")
    co = J.cars(NC)
    boxm = K.mat_simple("m_gbox", (0.85, 0.62, 0.22), 0.3, metal=0.8, emit=(1.0, 0.75, 0.3), estr=0.6)
    box = K.proto(ctx, "p_gbox", K.bm_cube(0.32, 0.22, 0.12, (0, 0, 0)), [boxm])
    wbo = K.instancer(ctx, "wboxes", box, NW)
    qbo = K.instancer(ctx, "qboxes", box, NQ)
    nb = J.nb
    shops = sim["shops"]
    tower = int(g["tower"][0])
    gold = np.tile((1.0, 0.72, 0.28), (nb, 1)).astype(np.float32)
    dark = np.zeros(nb, np.float32)
    dark[tower] = 0.75   # 타워는 유리 위주라 불 켜진 창이 적음
    J.set_buildings(gcol=gold, glow=np.zeros(nb), dark=dark)
    lk = light_keys(SKY)
    zeros3 = lambda n: np.zeros((n, 3), np.float32)  # noqa: E731

    def hand(p, yaw):
        fwd = np.stack([np.cos(yaw), np.sin(yaw)], 1)
        side = np.stack([-np.sin(yaw), np.cos(yaw)], 1)
        return np.c_[p + fwd * 0.18 + side * 0.28, np.full(len(p), 0.85)]

    def upd(t, f):
        set_cam(J, t, CAM)
        night = J.light(t, lk)
        ctx.set_ctl("lights", 0.12 + 0.4 * night)
        ctx.set_ctl("carlights", 0.2 + 0.8 * night)
        glow = np.zeros(nb, np.float32)
        glow[shops] = sim["shop_glow"][f] * (0.35 + 0.45 * night)
        glow[24] = 0.06 + 0.22 * night  # 롯데월드몰(매장)
        heat = float(sim["heat"][f])
        glow[tower] = night * min(1.0, heat * 1.3) * (1.0 if t > 16 else 0.0) * 0.35
        J.set_buildings(glow=glow)
        pose = pose_of(sim["ph"][f])
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(NW)], scale=np.ones(NW),
                     rot=np.c_[np.zeros((NW, 2)), sim["py"][f]], col=sim["shirt"], colors={"col2": sim["pants"]},
                     pose=pose)
        K.set_points(wbo, hand(sim["pp"][f], sim["py"][f]), scale=sim["w_box"][f], rot=np.c_[np.zeros((NW, 2)), sim["py"][f]],
                     col=np.ones((NW, 3)))
        qp = sim["q_pos"][f]
        moving = np.zeros(NQ, bool)
        qpose = np.where(moving, 1, 0).astype(np.float32)
        K.set_points(qo, np.c_[qp, np.zeros(NQ)], scale=sim["q_on"][f], rot=np.c_[np.zeros((NQ, 2)), sim["q_yaw"][f]],
                     col=sim["q_shirt2"] if 10.0 <= t < 16.0 else sim["q_shirt"], colors={"col2": sim["q_pants"]},
                     pose=qpose)
        K.set_points(qbo, hand(qp, sim["q_yaw"][f]), scale=sim["q_box"][f] * sim["q_on"][f],
                     rot=np.c_[np.zeros((NQ, 2)), sim["q_yaw"][f]], col=np.ones((NQ, 3)))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)
    ctx.anchor("store", lambda t: (-20.0, -57.0, 7.0))
    slots, _ = queue_slots(NQ)
    s150 = slots[min(SOLD, len(slots) - 1)]
    ctx.anchor("q150", lambda t: (float(s150[0]), float(s150[1]), 2.4))
