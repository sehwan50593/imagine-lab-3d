"""EP17 만약 인터넷이 하루 끊긴다면? (잠실역 사거리)

실제로 계산하는 것:
- 가게 불빛(카드 결제)·건물 화면이 꺼짐, 사람들은 멈춰 서서 휴대폰을 보다가(정지) 현금을 찾아 ATM 쪽으로 모임
- 차: 내비 없이 길을 헤매 교차로 주변을 빙빙 돎(속도 저하), 다음 날 다시 정상
숫자: 2018 KT 아현국사 화재 · 2021-10-25 KT 전국 장애 · 2024-07-19 CrowdStrike(윈도우 PC 약 850만 대) · 해저 케이블.
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, eye_from, light_keys, people_colors, pose_of, set_cam, sky_at, traffic

DUR = 56.0
META = {"id": "ep17", "title": "만약 인터넷이 하루 끊긴다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "G", "mode": "major", "bpm": 76, "seed": 171, "twist_at": 46.0}}
C = np.array([-214.4, 61.7])
NP, NC = 640, 150
ATM = np.array([(-260.0, 20.0), (-170.0, 110.0), (-150.0, 10.0), (-280.0, 110.0)], np.float32)

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY 09:00", label="인터넷", big="0 bps", label_color="red", big_color="red",
         sub="출근길 아침, 한국 전체의 인터넷이\n하루 동안 끊긴다면?"),
    Beat(4.5, 10.0, badge="+1분", title="모두가 {yellow}멈춰 섰다{/}",
         sub="지도도 메신저도 안 됩니다.\n사람들이 길 한가운데서 휴대폰만 봅니다."),
    Beat(10.0, 16.0, badge="+1시간", title="카드가 {red}안 긁힌다{/}", note="2018 KT 아현국사 화재: 서울 서부 카드 결제·통신 마비",
         sub="결제 단말기가 모두 인터넷으로 연결돼\n가게들이 하나둘 문을 닫습니다."),
    Beat(16.0, 22.0, badge="+3시간", title="ATM 앞 {orange}긴 줄{/}",
         sub="현금을 가진 사람만 살 수 있습니다.\n은행 앞은 줄이 끝없이 늘어섭니다."),
    Beat(22.0, 28.0, badge="+6시간", title="내비 없는 {yellow}길 잃은 차{/}", note="2021-10-25 KT 전국 장애: 약 1시간 반 만에 대혼란",
         sub="택시·배달도 길을 못 찾고\n도로는 같은 곳을 빙빙 도는 차로 막힙니다."),
    Beat(28.0, 34.0, badge="+12시간", title="공항·병원도 {red}종이{/}로", big="850만 대", big_size=104, big_color="red",
         note="2024 CrowdStrike 장애로 멈춘 윈도우 PC 수",
         sub="실제로 PC가 한꺼번에 멈춘 날,\n세계 곳곳의 비행기가 결항했습니다."),
    Beat(34.0, 40.0, badge="+18시간", title="그런데 사람들이 {cyan}말을 건다{/}",
         sub="휴대폰 대신 옆 사람에게 길을 묻고\n동네 가게는 외상 장부를 꺼냅니다."),
    Beat(40.0, 46.0, badge="+24시간", title="인터넷이 {green}돌아왔다{/}",
         sub="불이 다시 켜지고 결제가 됩니다.\n밀린 알림이 한꺼번에 울립니다."),
    Beat(46.0, 52.5, badge="반전", title="인터넷은 하늘이 아니라 {cyan}바닷속{/}", big="99%", big_size=112, big_color="cyan",
         note="나라와 나라 사이 데이터의 대부분은 해저 케이블로 오감",
         sub="위성이 아니라 바다 밑 굵은 케이블\n몇 가닥이 세계를 잇고 있습니다."),
    Beat(52.5, 56.0, badge="지금", title="당신은 인터넷 없이\n{yellow}며칠{/} 버틸 수 있나요?", title_size=74),
]
GRADE = {"exposure": 0.95, "bloom": 0.3, "bloom_thr": 1.0, "vignette": 0.32}
SKY = [(0.0, "MORNING"), (9.4, "MORNING"), (10.6, "DAY"), (27.6, "DAY"), (28.6, "DUSK"), (33.6, "DUSK"), (34.6, "NIGHT"),
       (45.6, "NIGHT"), (46.6, "NIGHT"), (56.0, "NIGHT")]
CLOCK = [(0.0, 0.0), (4.5, 0.0), (5.0, 1.0), (10.0, 2.0), (10.5, 60.0), (16.0, 62.0), (16.5, 180.0), (22.0, 182.0),
         (22.5, 360.0), (28.0, 362.0), (28.5, 720.0), (34.0, 722.0), (34.5, 1080.0), (40.0, 1082.0), (40.5, 1440.0),
         (56.0, 1442.0)]
CAM = [(0.0, (-214.0, 62.0, 3.0), 250, 50, 130.0, 30), (4.4, (-214.0, 62.0, 3.0), 260, 48, 115.0, 30),
       (4.9, (-190.0, 85.0, 2.0), 230, 34, 52.0, 30), (9.8, (-190.0, 85.0, 2.0), 245, 36, 58.0, 30),
       (10.4, (-214.0, 62.0, 3.0), 275, 50, 125.0, 30), (15.8, (-214.0, 62.0, 3.0), 285, 50, 135.0, 30),
       (16.4, (-240.0, 40.0, 2.0), 300, 34, 50.0, 30), (21.8, (-240.0, 40.0, 2.0), 315, 36, 56.0, 30),
       (22.4, (-214.0, 62.0, 6.0), 200, 50, 210.0, 30), (27.8, (-214.0, 62.0, 6.0), 215, 52, 240.0, 30),
       (28.4, (14.0, -6.0, 180.0), 235, 14, 1000.0, 32), (33.8, (14.0, -6.0, 180.0), 250, 16, 940.0, 32),
       (34.4, (-215.0, 50.0, 3.0), 240, 52, 160.0, 30), (39.8, (-215.0, 50.0, 3.0), 255, 54, 175.0, 30),
       (40.4, (-214.0, 62.0, 3.0), 260, 46, 115.0, 30), (45.8, (-214.0, 62.0, 3.0), 270, 48, 130.0, 30),
       (46.4, (14.0, -6.0, 150.0), 240, 10, 760.0, 32), (52.4, (14.0, -6.0, 150.0), 255, 12, 720.0, 32),
       (53.0, (-214.0, 62.0, 3.0), 280, 44, 100.0, 30), (56.0, (-214.0, 62.0, 3.0), 295, 46, 110.0, 30)]
EYE = eye_from((0.0, CAM[0][1], 195.0, 0.0, 100.0), 16.0)   # 03편과 같은 관찰 위치


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def offline(t):
    return 4.5 <= t < 40.5


def simulate(build_dir):
    from engine.jamsil import geometry
    g = geometry()
    rs = np.random.default_rng(1717)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    mins = np.array([keyed(t, CLOCK, ease=lambda u: u) for t in ts], np.float32)
    # 사람: 끊긴 직후엔 멈춰 섬(속도 0.1), 그 뒤 천천히
    sp = lambda t: float(np.interp(t, [0, 4.6, 5.2, 9.8, 10.4, 40.5, 41.0], [1, 1, 0.08, 0.08, 0.8, 0.8, 1.1]))
    pp, py, ph = crowd(rs, nf, NP, tuple(C), 270, t_speed=sp)
    shirt, pants = people_colors(rs, NP)
    # ATM 줄: 16~34초 사이 일부가 ATM 앞에 한 줄로 섬
    qsel = rs.random(NP) < 0.35
    qi = rs.integers(0, len(ATM), NP)
    order = np.zeros(NP)
    for a in range(len(ATM)):
        idx = np.where(qsel & (qi == a))[0]
        order[idx] = np.arange(len(idx))
    ang = rs.uniform(0, 2 * np.pi, len(ATM))
    qdir = np.c_[np.cos(ang), np.sin(ang)].astype(np.float32)
    qpos = ATM[qi] + qdir[qi] * (1.5 + order[:, None] * 0.9)
    w = np.clip((ts - 16.4) / 2.0, 0, 1) * (1 - np.clip((ts - 33.8) / 1.5, 0, 1))
    w = w * w * (3 - 2 * w)
    pp = np.where(qsel[None, :, None], pp * (1 - w[:, None, None]) + qpos[None] * w[:, None, None], pp)
    stand = ((w[:, None] > 0.98) & qsel[None, :]) | ((ts[:, None] > 4.8) & (ts[:, None] < 9.8))
    for i in range(nf):
        if w[i] > 0.5:
            py[i] = np.where(qsel, np.arctan2(-qdir[qi][:, 1], -qdir[qi][:, 0]), py[i])
    # 차: 길 잃고 느려짐
    cs = lambda t: float(np.interp(t, [0, 4.6, 6.0, 40.5, 41.5], [1, 1, 0.35, 0.35, 1.0]))
    cp, cy = traffic(rs, nf, NC, tuple(C), 520, speed=(10, 15), stop=cs)
    cent = g["b_cent"]
    dist = np.hypot(cent[:, 0] - C[0], cent[:, 1] - C[1])
    small = np.where(g["b_area"] < 5000)[0]
    shops = small[np.argsort(dist[small])][:40]
    close_t = rs.uniform(10.5, 15.0, len(shops))
    return dict(pp=pp.astype(np.float32), py=py.astype(np.float32), ph=ph, shirt=shirt, pants=pants,
                stand=stand.astype(np.float32), qw=w.astype(np.float32), cp=cp, cy=cy, mins=mins,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)], shops=shops.astype(np.int32),
                close_t=close_t.astype(np.float32))


def sky(t):
    return sky_at(t, SKY)


def hud(t, sim):
    m = float(sim["mins"][fi(t)])
    right = "D-DAY 09:00" if t < 4.5 else (f"+{int(m)}분" if m < 60 else f"+{int(m // 60)}시간")
    r2 = "반전" if t >= 46 else ("인터넷 끊김" if offline(t) else "인터넷 정상")
    return {"left": "SIMULATION", "right": right, "right2": r2}


def labels(t, anchors, sim):
    out = []
    for i in range(len(ATM)):
        a = anchors.get(f"atm{i}")
        if a and a[3] and 17.0 < t < 21.6:
            out.append({"x": a[0], "y": a[1], "text": "ATM 줄", "color": "orange", "size": 26, "lift": 8,
                        "alpha": ramp(t, 17.2, 17.8)})
            break
    return out


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    po = J.people(NP, "people")
    co = J.cars(NC)
    # 휴대폰 화면 불빛 (사람 손 높이의 작은 파란 점)
    ph_m = K.mat_emit("m_phone", (0.4, 0.7, 1.0), 6.0, ctx, "phone")
    phones = K.instancer(ctx, "phones", K.proto(ctx, "p_phone", K.bm_cube(0.12, 0.08, 0.14, (0.25, 0, 1.25), True),
                                                 [ph_m]), NP)
    atm_m = K.mat_emit("m_atm", (0.3, 1.0, 0.5), 6.0, ctx, "atm")
    atms = K.instancer(ctx, "atms", K.proto(ctx, "p_atm", K.bm_cube(1.2, 0.8, 2.2, (0, 0, 1.1), True), [atm_m]), len(ATM))
    K.set_points(atms, np.c_[ATM, np.zeros(len(ATM))], scale=np.ones(len(ATM)), rot=np.zeros((len(ATM), 3)),
                 col=np.ones((len(ATM), 3)))
    nb = J.nb
    shops = sim["shops"]
    tower = int(g["tower"][0])
    J.set_buildings(gcol=np.tile((1.0, 0.85, 0.55), (nb, 1)).astype(np.float32), glow=np.zeros(nb), dark=np.zeros(nb))
    lk = light_keys(SKY)
    lk = [(k_, dict(v_, energy=max(v_["energy"], 0.7), amb=max(v_["amb"], 0.11))) for k_, v_ in lk]

    def upd(t, f):
        set_cam(J, t, CAM, eye=EYE)
        night = J.light(t, lk)
        off = offline(t)
        ctx.set_ctl("lights", 0.12 + 0.5 * night)
        ctx.set_ctl("carlights", 0.3 + 0.7 * night)
        glow = np.full(nb, 0.05 * night, np.float32)
        shop_on = np.where(off & (t > sim["close_t"]), 0.0, 0.35)
        glow[shops] = shop_on
        if t >= 40.5:
            glow[:] = 0.12 * ramp(t, 40.5, 41.5) + 0.04
            glow[shops] = 0.4
        glow[tower] = 0.0 if off else 0.3
        J.set_buildings(glow=glow)
        # 휴대폰: 끊긴 직후 모두 켜서 들여다봄, 이후 꺼짐 / 복구 순간 다시 켜짐
        p_on = 1.0 if 4.6 < t < 10.0 or 40.5 < t < 46.0 else 0.0
        ctx.set_ctl("phone", 6.0 * p_on)
        ctx.set_ctl("atm", 5.0 if 16.0 < t < 34.0 else 1.0)
        moving = sim["stand"][f] < 0.5
        R = np.c_[np.zeros((NP, 2)), sim["py"][f]]
        P = np.c_[sim["pp"][f], np.zeros(NP)]
        K.set_points(po, P, scale=np.ones(NP), rot=R, col=sim["shirt"], colors={"col2": sim["pants"]},
                     pose=pose_of(sim["ph"][f], moving))
        K.set_points(phones, P, scale=np.full(NP, p_on), rot=R, col=np.ones((NP, 3)))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)
    for i in range(len(ATM)):
        ctx.anchor(f"atm{i}", (lambda q: (lambda t: (float(ATM[q][0]), float(ATM[q][1]), 3.0)))(i))
