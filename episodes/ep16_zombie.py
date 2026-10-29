"""EP16 만약 잠실에 좀비가 나타난다면? (잠실역 사거리)

실제로 계산하는 것:
- 감염 확산: SIR 모형. 감염자(초록) 반경 안의 사람은 매 초 일정 확률로 감염, 감염자는 가장 가까운 사람 쪽으로 걸음
- 도망: 감염자 근처 사람은 반대 방향으로 뜀, 일부는 건물 안으로 숨음(사라짐)
- 차: 교차로로 몰려 정체 후 멈춤, 도시 불빛은 날이 갈수록 꺼짐
숫자: Alemi 외(코넬대, 2015) 좀비 확산 시뮬레이션 · Ophiocordyceps(좀비 개미 곰팡이).
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, eye_from, light_keys, people_colors, pose_of, set_cam, sky_at, traffic

DUR = 56.0
META = {"id": "ep16", "title": "만약 잠실에 좀비가 나타난다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "D", "mode": "lydian", "bpm": 84, "seed": 161, "twist_at": 46.0}}
C = np.array([-214.4, 61.7])
NP, NC = 700, 140

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY 18:00", label="잠실역", big="좀비 1명", label_color="green", big_color="green",
         sub="퇴근길 잠실역 사거리에\n좀비 한 명이 나타난다면?"),
    Beat(4.5, 10.0, badge="+10분", title="1명이 순식간에 {green}10명{/}",
         sub="물린 사람이 또 다른 사람을 뭅니다.\n사람이 많을수록 더 빨리 번집니다."),
    Beat(10.0, 16.0, badge="+1시간", title="사거리가 {red}멈췄다{/}",
         sub="도망치는 차들이 교차로에 뒤엉키고\n버려진 차가 길을 막습니다."),
    Beat(16.0, 22.0, badge="+1일", title="잠실 인구 {green}절반{/}", big=lambda t, s: f"{int(s['inf_pct'][fi(t)])}%",
         big_size=110, big_color="green",
         sub="사람이 빽빽한 도시는\n좀비에게 가장 좋은 사냥터입니다."),
    Beat(22.0, 28.0, badge="+3일", title="살아남은 사람은 {cyan}위로{/}",
         note="좀비 확산 시뮬레이션: 대도시는 며칠, 외딴 산골은 몇 주를 버팀 (코넬대, 2015)",
         sub="문을 막고 높은 층으로 숨은 사람들만\n불을 끄고 버팁니다."),
    Beat(28.0, 34.0, badge="+1주", title="도시의 불이 {gray}꺼진다{/}",
         sub="발전소를 지킬 사람이 없어\n불빛이 하나둘 사라집니다."),
    Beat(34.0, 40.0, badge="+1달", title="정답은 {cyan}사람 없는 곳{/}",
         sub="연구진의 결론도 같았습니다.\n도시를 빨리 벗어나 산으로 가라."),
    Beat(40.0, 46.0, badge="+1달", title="고요한 잠실",
         sub="움직이는 건 좀비뿐.\n좀비도 먹을 것이 없어 흩어집니다."),
    Beat(46.0, 52.5, badge="반전", title="좀비는 {green}실제로{/} 있다", big="좀비 개미", big_size=104, big_color="green",
         note="동충하초 곰팡이 Ophiocordyceps — 개미 몸을 조종함",
         sub="곰팡이에 감염된 개미는 조종당해\n높은 곳에 올라가 포자를 퍼뜨립니다."),
    Beat(52.5, 56.0, badge="지금", title="당신은 잠실에서\n{cyan}어디로{/} 도망치겠습니까?", title_size=74),
]
GRADE = {"exposure": 0.95, "bloom": 0.35, "bloom_thr": 1.0, "vignette": 0.36}
SKY = [(0.0, "DUSK"), (15.4, "DUSK"), (16.4, "DAY"), (21.6, "DAY"), (22.6, "NIGHT"), (33.6, "NIGHT"), (34.4, "MORNING"),
       (45.6, "MORNING"), (46.6, "NIGHT"), (56.0, "NIGHT")]
CLOCK = [(0.0, 0.0), (4.5, 0.0), (5.0, 10.0), (10.0, 12.0), (10.5, 60.0), (16.0, 65.0), (16.5, 1440.0), (22.0, 1460.0),
         (22.5, 4320.0), (28.0, 4400.0), (28.5, 10080.0), (34.0, 10100.0), (34.5, 43200.0), (56.0, 43300.0)]
CAM = [(0.0, (-214.0, 62.0, 3.0), 250, 50, 130.0, 30), (4.4, (-214.0, 62.0, 3.0), 260, 48, 115.0, 30),
       (4.9, (-214.0, 62.0, 2.0), 255, 46, 70.0, 30), (9.8, (-214.0, 62.0, 2.0), 268, 48, 80.0, 30),
       (10.4, (-190.0, 85.0, 2.0), 230, 34, 52.0, 30), (15.8, (-190.0, 85.0, 2.0), 245, 36, 58.0, 30),
       (16.4, (-214.0, 62.0, 6.0), 200, 50, 210.0, 30), (21.8, (-214.0, 62.0, 6.0), 215, 52, 240.0, 30),
       (22.4, (-240.0, 40.0, 30.0), 300, 34, 90.0, 30), (27.8, (-240.0, 40.0, 30.0), 315, 36, 100.0, 30),
       (28.4, (14.0, -6.0, 180.0), 235, 14, 1000.0, 32), (33.8, (14.0, -6.0, 180.0), 250, 16, 940.0, 32),
       (34.4, (-215.0, 50.0, 3.0), 240, 52, 160.0, 30), (39.8, (-215.0, 50.0, 3.0), 255, 54, 175.0, 30),
       (40.4, (-214.0, 62.0, 3.0), 260, 46, 115.0, 30), (45.8, (-214.0, 62.0, 3.0), 270, 48, 130.0, 30),
       (46.4, (-170.0, 110.0, 2.0), 230, 34, 42.0, 30), (52.4, (-170.0, 110.0, 2.0), 245, 36, 46.0, 30),
       (53.0, (-214.0, 62.0, 3.0), 280, 44, 100.0, 30), (56.0, (-214.0, 62.0, 3.0), 295, 46, 110.0, 30)]
EYE = eye_from((0.0, CAM[0][1], 195.0, 0.0, 100.0), 16.0)   # 03편과 같은 관찰 위치 (건물에 안 가림)
GREEN = np.array((0.35, 0.75, 0.25), np.float32)


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def simulate(build_dir):
    rs = np.random.default_rng(1616)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    mins = np.array([keyed(t, CLOCK, ease=lambda u: u) for t in ts], np.float32)
    pp, py, ph = crowd(rs, nf, NP, tuple(C), 230)
    shirt, pants = people_colors(rs, NP)
    # ── 감염: 장면 안은 실제 걸음으로 퍼지고, 장면 사이(시간 건너뜀)는 목표 비율까지 채움 ──
    target = np.interp(mins, [0, 10, 60, 1440, 4320, 10080, 43200], [0.0015, 0.018, 0.12, 0.5, 0.72, 0.85, 0.9])
    inf_t = np.full(NP, np.inf)
    d0 = np.hypot(pp[0, :, 0] - C[0], pp[0, :, 1] - C[1])
    inf_t[int(np.argmin(d0))] = 0.0
    off = np.zeros((NP, 2), np.float32)   # 쫓기/도망 오프셋
    out_p = np.zeros_like(pp)
    hide = np.zeros((nf, NP), np.float32)
    hrank = rs.random(NP)
    for i in range(nf):
        t = ts[i]
        p = pp[i] + off
        inf = inf_t <= t
        if inf.any() and (~inf).any():
            zi, hi_ = np.where(inf)[0], np.where(~inf)[0]
            d = np.hypot(p[hi_, None, 0] - p[None, zi, 0], p[hi_, None, 1] - p[None, zi, 1])
            dmin = d.min(1)
            near = zi[d.argmin(1)]
            # 물림: 2m 안이면 초당 60%
            bit = (dmin < 2.0) & (rs.random(len(hi_)) < 0.6 / FPS)
            inf_t[hi_[bit]] = t
            # 도망: 12m 안 좀비 반대쪽으로
            v = p[hi_] - p[near]
            nv = np.hypot(v[:, 0], v[:, 1])[:, None] + 1e-6
            flee = (dmin < 12.0)[:, None]
            off[hi_] += np.where(flee, v / nv * 2.6 / FPS, 0)
            # 쫓기: 좀비는 가장 가까운 사람 쪽으로 천천히
            dz = np.hypot(p[zi, None, 0] - p[None, hi_, 0], p[zi, None, 1] - p[None, hi_, 1])
            tg = hi_[dz.argmin(1)]
            w = p[tg] - p[zi]
            nw = np.hypot(w[:, 0], w[:, 1])[:, None] + 1e-6
            off[zi] += np.where(dz.min(1)[:, None] < 25.0, w / nw * 1.6 / FPS, 0)
        # 시간 건너뜀 보정: 목표 비율보다 적으면 가까운 순서로 채움
        frac = float((inf_t <= t).mean())
        if frac < target[i] - 0.01:
            cand = np.where(inf_t > t)[0]
            dz = np.hypot(p[cand, 0] - C[0], p[cand, 1] - C[1])
            k = int((target[i] - frac) * NP)
            inf_t[cand[np.argsort(dz)[:k]]] = t
        off *= 0.995
        out_p[i] = pp[i] + off
        # 숨기: 사람(감염 안 된)의 일부는 1일 뒤부터 건물 안으로
        hide[i] = ((hrank < np.interp(mins[i], [0, 1440, 4320, 43200], [0, 0.4, 0.8, 1.0])) & (inf_t > t))
    infected = (inf_t[None, :] <= ts[:, None]).astype(np.float32)
    vis = 1.0 - hide
    inf_pct = 100 * infected.mean(1)
    cp, cy = traffic(rs, nf, NC, tuple(C), 520, speed=(10, 15),
                     stop=lambda t: 1.0 if t < 10.4 else (1.6 if t < 12.0 else 0.0))
    crash = rs.normal(0, 0.6, NC)
    near_c = np.hypot(cp[:, :, 0] - C[0], cp[:, :, 1] - C[1]) < 70
    cy = np.where((ts >= 12.0)[:, None] & near_c, cy + crash[None, :], cy)
    return dict(pp=out_p.astype(np.float32), py=py.astype(np.float32), ph=ph, shirt=shirt, pants=pants,
                infected=infected, vis=vis.astype(np.float32), inf_pct=inf_pct.astype(np.float32), mins=mins,
                cp=cp, cy=cy.astype(np.float32), ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)])


def sky(t):
    return sky_at(t, SKY)


def hud(t, sim):
    m = float(sim["mins"][fi(t)])
    right = f"+{int(m)}분" if m < 60 else (f"+{int(m // 60)}시간" if m < 1440 else f"D+{int(m // 1440)}")
    if t < 0.5:
        right = "D-DAY 18:00"
    r2 = "반전" if t >= 46 else f"감염 {int(round(sim['inf_pct'][fi(t)]))}%"
    return {"left": "SIMULATION", "right": right, "right2": r2}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("zero")
    if a and a[3] and t < 4.4:
        out.append({"x": a[0], "y": a[1], "text": "첫 좀비", "color": "green", "size": 30, "lift": 10,
                    "alpha": ramp(t, 0.6, 1.1)})
    return out


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    po = J.people(NP, "people")
    co = J.cars(NC)
    nb = J.nb
    rs = np.random.default_rng(16)
    off_t = rs.uniform(28.5, 33.0, nb)   # 건물 불이 꺼지는 시각
    J.set_buildings(gcol=np.tile((1.0, 0.85, 0.55), (nb, 1)).astype(np.float32), glow=np.zeros(nb), dark=np.zeros(nb))
    lk = light_keys(SKY)
    lk = [(k_, dict(v_, energy=max(v_["energy"], 0.7), amb=max(v_["amb"], 0.11))) for k_, v_ in lk]
    zero = int(np.argmax(sim["infected"][0]))

    def upd(t, f):
        set_cam(J, t, CAM, eye=EYE)
        night = J.light(t, lk)
        on = 1.0 - np.clip((t - off_t) / 0.8, 0, 1)
        ctx.set_ctl("lights", (0.12 + 0.5 * night) * (1.0 - 0.95 * ramp(t, 28.6, 32.5)))
        ctx.set_ctl("carlights", (0.3 + 0.7 * night) * (1.0 if t < 22.4 else 0.2))
        J.set_buildings(glow=(0.08 * night * on).astype(np.float32))
        z = sim["infected"][f][:, None]
        col = sim["shirt"] * (1 - z) + GREEN * z
        moving = np.ones(NP, bool)
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(NP)], scale=sim["vis"][f],
                     rot=np.c_[np.zeros((NP, 2)), sim["py"][f]], col=col,
                     colors={"col2": sim["pants"] * (1 - z) + 0.5 * GREEN * z}, pose=pose_of(sim["ph"][f], moving))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)
    ctx.anchor("zero", lambda t: (float(sim["pp"][fi(t)][zero][0]), float(sim["pp"][fi(t)][zero][1]), 2.4))
