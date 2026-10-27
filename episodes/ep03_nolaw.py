"""EP03 만약 이 세상에서 법이 사라진다면? (잠실역 사거리)

실제로 계산하는 것:
- 경찰차·신호등이 사라진 교차로: 차들이 몰려 엉키면 그 자리에서 멈추는 정체 확산
- 일탈: 일부 사람이 '이탈자'(빨강)가 되어 빨리 움직이고, 가게 불빛이 붉게 깜빡이며 화재가 번짐
- 협력: 이탈자 비율이 줄고, 사람들이 모임 장소로 모여 규칙(파란 고리)을 만든 뒤 신호가 돌아옴
숫자: 1969 몬트리올 경찰 파업, 1977 뉴욕 정전, 델라웨어대 재난연구, Tyler(1990), 우르남무 법전.
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil import PathWalkers, geometry
from engine.jamsil_ep import (CAR_COLORS, crowd, light_keys, lines_of, people_colors, pose_of, set_cam, eye_from, sky_at,
                              traffic)

DUR = 56.0
META = {"id": "ep03", "title": "만약 이 세상에서 법이 사라진다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "E", "mode": "major", "bpm": 70, "seed": 33, "twist_at": 46.0}}
C = np.array([-214.4, 61.7])
NP, NC, NPOL, NFIRE = 640, 150, 6, 40
GROUPS = np.array([(-260.0, 20.0), (-170.0, 110.0), (-150.0, 10.0), (-280.0, 110.0), (-215.0, -30.0)], np.float32)

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY 00:00", label="법", big="전부 삭제", label_color="red",
         sub="오늘 밤 0시, 세상의 모든 법과\n경찰·법원이 한순간에 사라진다면?"),
    Beat(4.5, 10.0, badge="+1시간", title="신호등이 꺼졌다",
         sub="교통 법규가 사라진 교차로에서\n먼저 가려는 차들이 뒤엉킵니다."),
    Beat(10.0, 16.0, badge="+16시간", title="1969년 {orange}몬트리올{/}", note="경찰 파업 16시간: 체포 108명 · 피해 약 200만 달러",
         sub="실제로 경찰이 사라졌던 16시간,\n도시는 순식간에 혼란에 빠졌습니다."),
    Beat(16.0, 22.0, badge="+26시간", title="1977년 뉴욕 정전", big="상점 1,616곳", big_size=100, big_color="red",
         note="26시간 동안 화재 1,037건 · 체포 3,776명",
         sub="질서가 멈추자 약탈과 방화가\n도시 곳곳으로 번졌습니다."),
    Beat(22.0, 28.0, badge="+3일", title="그런데 대부분은 {green}가만히{/} 있었다",
         note="재난 땐 약탈보다 협력이 훨씬 흔하다 (델라웨어대 재난연구센터)",
         sub="위기 속 사람들은 대부분\n서로 돕는 쪽을 택했습니다."),
    Beat(28.0, 34.0, badge="+1개월", title="이웃이 다시 {cyan}규칙{/}을 만든다",
         sub="동네마다 모여 순번을 정하고\n지킬 약속을 정합니다."),
    Beat(34.0, 40.0, badge="+1년", title="처벌보다 {yellow}양심{/}", note="법을 지키는 이유: 처벌 공포보다 정당성·도덕 (Tyler, 1990)",
         sub="사람들이 규칙을 지키는 건\n벌이 무서워서만은 아닙니다."),
    Beat(40.0, 46.0, badge="+10년", title="약속은 다시 {yellow}법{/}이 된다",
         sub="지키기로 한 약속은 글로 적히고\n신호등도 다시 켜집니다."),
    Beat(46.0, 52.5, badge="반전", title="법이 사라진 세상의 첫 발명품", big="다시, 법", big_size=110, big_color="yellow",
         note="현존 최고(最古) 법전 우르남무 — 약 4,100년 전",
         sub="인류는 법이 없던 적이 없습니다.\n없어지면, 언제나 다시 만들었으니까요."),
    Beat(52.5, 56.0, badge="지금", title="당신이 만들\n{yellow}첫 번째 법{/}은?", title_size=78),
]
GRADE = {"exposure": 0.95, "bloom": 0.3, "bloom_thr": 1.0, "vignette": 0.32}
SKY = [(0.0, "NIGHT"), (9.4, "NIGHT"), (10.6, "DAY"), (15.4, "DAY"), (16.4, "NIGHT"), (21.6, "NIGHT"), (22.6, "MORNING"),
       (23.6, "DAY"), (39.6, "DAY"), (40.6, "DUSK"), (45.6, "DUSK"), (46.6, "NIGHT"), (56.0, "NIGHT")]
CLOCK = [(0.0, 0.0), (4.5, 0.0), (5.0, 1.0), (10.0, 1.4), (10.5, 16.0), (16.0, 16.5), (16.5, 26.0), (22.0, 27.0),
         (22.5, 72.0), (28.0, 75.0), (28.5, 720.0), (34.0, 740.0), (34.5, 8766.0), (40.0, 8800.0), (40.5, 87660.0),
         (56.0, 87700.0)]


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def simulate(build_dir):
    g = geometry()
    rs = np.random.default_rng(303)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    # ── 사람 ──
    pp, py, ph = crowd(rs, nf, NP, tuple(C), 270)
    shirt, pants = people_colors(rs, NP)
    defect_p = rs.random(NP)
    frac = np.interp(ts, [0, 9.8, 10.4, 16, 22, 24, 28, 56], [0, 0, 0.08, 0.14, 0.14, 0.05, 0.02, 0.0])
    defect = (defect_p[None, :] < frac[:, None]).astype(np.float32)
    # 이탈자는 빨리 달리는 것처럼 (위치를 앞쪽으로 당김)
    run = np.zeros_like(pp)
    for i in range(1, nf):
        d = pp[i] - pp[i - 1]
        run[i] = run[i - 1] * 0.92 + d * defect[i][:, None] * 1.6
    pp = pp + run
    # 모임: 28~46초 사이 절반이 모임 장소로 가서 멈춤
    gsel = rs.random(NP) < 0.55
    gi = rs.integers(0, len(GROUPS), NP)
    gpos = GROUPS[gi] + rs.normal(0, 3.2, (NP, 2)).astype(np.float32)
    w = np.clip((ts - 28.4) / 2.5, 0, 1) * (1 - np.clip((ts - 44.5) / 1.5, 0, 1))
    w = w * w * (3 - 2 * w)
    stand = (w[:, None] > 0.98) & gsel[None, :]
    pp = np.where(gsel[None, :, None], pp * (1 - w[:, None, None]) + gpos[None] * w[:, None, None], pp)
    for i in range(nf):
        if w[i] > 0.02:
            d = gpos - pp[i]
            yaw_g = np.arctan2(d[:, 1], d[:, 0])
            py[i] = np.where(gsel, np.where(stand[i], np.arctan2(GROUPS[gi][:, 1] - gpos[:, 1], GROUPS[gi][:, 0] - gpos[:, 0]),
                                            yaw_g), py[i])
    # ── 차: 4.5초부터 교차로로 몰리며 정체 ──
    cp, cy = traffic(rs, nf, NC, tuple(C), 520, speed=(10, 15),
                     stop=lambda t: 1.0 if t < 4.6 else (1.5 if t < 6.4 else (0.0 if t < 40.5 else 1.0)))
    jam = (ts >= 6.4) & (ts < 40.5)
    crash_yaw = rs.normal(0, 0.5, NC)
    near = np.hypot(cp[:, :, 0] - C[0], cp[:, :, 1] - C[1]) < 60
    cy = np.where(jam[:, None] & near, cy + crash_yaw[None, :], cy)
    # 경찰차: 교차로 주변 도로 위 (2초에 사라짐)
    pw = PathWalkers(rs, lines_of(g, "car"), NPOL, rs.uniform(8, 11, NPOL), offset=3.2, near=tuple(C), near_r=160)
    pol_p = np.zeros((nf, NPOL, 2), np.float32)
    pol_y = np.zeros((nf, NPOL), np.float32)
    for i in range(nf):
        pol_p[i], pol_y[i] = pw.step(1 / FPS)
    pol_on = np.clip(1 - (ts - 2.0) / 0.5, 0, 1)
    # ── 가게 약탈 깜빡임·화재 ──
    cent = g["b_cent"]
    dist = np.hypot(cent[:, 0] - C[0], cent[:, 1] - C[1])
    small = np.where(g["b_area"] < 5000)[0]
    shops = small[np.argsort(dist[small])][:34]
    loot_t = rs.uniform(10.5, 20.5, len(shops))
    fire_src = cent[shops[rs.integers(0, len(shops), NFIRE)]] + rs.normal(0, 14, (NFIRE, 2))
    fire_t = rs.uniform(16.3, 21.0, NFIRE)
    return dict(pp=pp.astype(np.float32), py=py.astype(np.float32), ph=ph, shirt=shirt, pants=pants, defect=defect,
                stand=stand.astype(np.float32), cp=cp, cy=cy.astype(np.float32),
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)], pol_p=pol_p, pol_y=pol_y,
                pol_on=pol_on.astype(np.float32), shops=shops.astype(np.int32), loot_t=loot_t.astype(np.float32),
                fire_src=fire_src.astype(np.float32), fire_t=fire_t.astype(np.float32), group_w=w.astype(np.float32))


def sky(t):
    return sky_at(t, SKY)


def hud(t, sim):
    h = keyed(t, CLOCK, ease=lambda u: u)
    if h < 48:
        right = f"D+{int(h // 24)}  {int(h % 24):02d}:00"
    elif h < 24 * 60:
        right = f"D+{int(h // 24)}"
    else:
        right = f"{h / 8766:.0f}년 후"
    f = fi(t)
    nd = int(sim["defect"][f].sum())
    r2 = f"법 0개 · 이탈자 {nd}명" if t < 40 else "법 다시 생김"
    if t < 2.0:
        r2 = "법 · 경찰 · 법원 작동 중"
    return {"left": "SIMULATION", "right": right, "right2": r2}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("police")
    if a and a[3] and t < 2.2:
        out.append({"x": a[0], "y": a[1], "text": "경찰차", "color": "blue", "size": 26, "lift": 10})
    a = anchors.get("signal")
    if a and a[3] and 4.6 < t < 10.0:
        out.append({"x": a[0], "y": a[1], "text": "신호등 꺼짐", "color": "red", "size": 26, "alpha": ramp(t, 4.8, 5.3)})
    return out


CAM = [(0.0, (-214.0, 62.0, 3.0), 250, 50, 130.0, 30), (4.4, (-214.0, 62.0, 3.0), 260, 48, 115.0, 30),
       (9.8, (-214.0, 62.0, 3.0), 275, 50, 125.0, 30), (10.4, (-190.0, 85.0, 2.0), 230, 34, 52.0, 30),
       (15.8, (-190.0, 85.0, 2.0), 245, 36, 58.0, 30), (16.4, (-214.0, 62.0, 6.0), 200, 50, 210.0, 30),
       (21.8, (-214.0, 62.0, 6.0), 215, 52, 240.0, 30), (22.4, (-240.0, 40.0, 2.0), 300, 34, 50.0, 30),
       (27.8, (-240.0, 40.0, 2.0), 315, 36, 56.0, 30), (28.4, (-215.0, 50.0, 3.0), 240, 52, 160.0, 30),
       (33.8, (-215.0, 50.0, 3.0), 255, 54, 175.0, 30), (34.4, (-170.0, 110.0, 2.0), 230, 34, 42.0, 30),
       (39.8, (-170.0, 110.0, 2.0), 245, 36, 46.0, 30), (40.4, (-214.0, 62.0, 3.0), 260, 46, 115.0, 30),
       (45.8, (-214.0, 62.0, 3.0), 270, 48, 130.0, 30), (46.4, (14.0, -6.0, 180.0), 235, 14, 1000.0, 32),
       (52.4, (14.0, -6.0, 180.0), 250, 16, 940.0, 32), (53.0, (-214.0, 62.0, 3.0), 280, 44, 100.0, 30),
       (56.0, (-214.0, 62.0, 3.0), 295, 46, 110.0, 30)]
EYE = eye_from((0.0, CAM[0][1], 195.0, 0.0, 100.0), 16.0)   # 건물에 안 가리는 방향 (tools/find_eye.py)   # 1인칭 관찰 위치 (육교·옥상 높이에 고정)


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    tr = J.tree_xy
    near_c = np.hypot(tr[:, 0] - C[0], tr[:, 1] - C[1]) < 50
    K.set_points(J.to, np.c_[tr, np.zeros(len(tr))], scale=np.where(near_c, 0.0, J.tree_s0),
                 rot=np.zeros((len(tr), 3)), col=np.tile((0.15, 0.38, 0.11), (len(tr), 1)))
    po = J.people(NP, "people")
    co = J.cars(NC)
    # 경찰차 (파랑·빨강 경광등)
    pol_m = K.mat_simple("m_pol", (0.92, 0.92, 0.95), 0.35)
    bar = K.mat_emit("m_polbar", (0.2, 0.4, 1.0), 12.0, ctx, "polbar")
    bar2 = K.mat_emit("m_polbar2", (1.0, 0.15, 0.1), 12.0, ctx, "polbar2")
    parts = [(K.bm_cube(4.6, 2.0, 1.0, (0, 0, 0.4), True), 0), (K.bm_cube(2.6, 1.8, 0.7, (-0.3, 0, 1.4), True), 0),
             (K.bm_cube(0.5, 0.7, 0.18, (-0.3, 0.4, 2.1), True), 1), (K.bm_cube(0.5, 0.7, 0.18, (-0.3, -0.4, 2.1), True), 2)]
    polo = K.instancer(ctx, "police", K.proto(ctx, "p_police", K.join_bms(parts), [pol_m, bar, bar2]), NPOL)
    # 신호등 4개
    sig_g = K.mat_emit("m_sig_g", (0.2, 1.0, 0.4), 10.0, ctx, "sig_g")
    sig_r = K.mat_emit("m_sig_r", (1.0, 0.15, 0.1), 10.0, ctx, "sig_r")
    pole = K.mat_simple("m_sigpole", (0.15, 0.15, 0.17), 0.5)
    sparts = [(K.bm_cone(0.15, 0.12, 5.5, (0, 0, 0), 8), 0), (K.bm_cube(0.5, 0.5, 1.4, (0, 0, 5.5), True), 0),
              (K.bm_sphere(0.18, (0.26, 0, 6.5), 8, 6), 1), (K.bm_sphere(0.18, (0.26, 0, 5.9), 8, 6), 2)]
    sig = K.instancer(ctx, "signals", K.proto(ctx, "p_signal", K.join_bms(sparts), [pole, sig_r, sig_g]), 4)
    sxy = C + np.array([(16, 16), (-16, 16), (-16, -16), (16, -16)], np.float32)
    K.set_points(sig, np.c_[sxy, np.zeros(4)], scale=np.ones(4),
                 rot=np.c_[np.zeros((4, 2)), np.array([3.93, 5.5, 0.79, 2.36])], col=np.ones((4, 3)))
    fire = K.instancer(ctx, "fires3", K.proto(ctx, "p_fire3", K.bm_ico(1.4, sub=1),
                                               [K.mat_emit("m_fire3", (1.0, 0.45, 0.12), 9.0, ctx, "fire3")]), NFIRE)
    ring_m = K.mat_emit("m_ring3", (0.35, 0.85, 1.0), 2.0, ctx, "rings")
    rb = K.bmesh.new()
    ins, ous = [], []
    for i_ in range(48):
        a_ = 2 * math.pi * i_ / 48
        ins.append(rb.verts.new((math.cos(a_) * 0.9, math.sin(a_) * 0.9, 0)))
        ous.append(rb.verts.new((math.cos(a_), math.sin(a_), 0)))
    for i_ in range(48):
        j_ = (i_ + 1) % 48
        rb.faces.new((ins[i_], ins[j_], ous[j_], ous[i_]))
    ringp = K.proto(ctx, "p_ring3", rb, [ring_m])
    ringo = K.instancer(ctx, "rings3", ringp, len(GROUPS))
    nb = J.nb
    shops = sim["shops"]
    tower = int(g["tower"][0])
    red = np.tile((1.0, 0.18, 0.12), (nb, 1)).astype(np.float32)
    J.set_buildings(gcol=red, glow=np.zeros(nb), dark=np.zeros(nb))
    lk = light_keys(SKY)
    lk = [(k_, dict(v_, energy=max(v_["energy"], 0.7), amb=max(v_["amb"], 0.11))) for k_, v_ in lk]

    def upd(t, f):
        set_cam(J, t, CAM, eye=EYE)
        night = J.light(t, lk)
        lawless = 4.5 <= t < 40.5
        ctx.set_ctl("lights", 0.12 + 0.5 * night)
        ctx.set_ctl("carlights", 0.3 + 0.7 * night)
        blink = 0.5 + 0.5 * math.sin(t * 18)
        ctx.set_ctl("polbar", 12.0 * blink)
        ctx.set_ctl("polbar2", 12.0 * (1 - blink))
        cyc = (t % 4.0) < 2.0
        ctx.set_ctl("sig_g", 0.0 if lawless else (10.0 if cyc else 0.0))
        ctx.set_ctl("sig_r", 0.0 if lawless else (0.0 if cyc else 10.0))
        glow = np.zeros(nb, np.float32)
        lt = t - sim["loot_t"]
        flick = (lt > 0) & (lt < 8.0) & ((np.sin(t * 9 + np.arange(len(shops)) * 1.7) > 0) | (lt < 1.0))
        glow[shops] = np.where(flick & (t < 28.0), 0.22 + 0.2 * night, 0.0)
        if t >= 40.5:
            glow[tower] = 0.25 * ramp(t, 40.5, 42.0)
        J.set_buildings(glow=glow,
                        gcol=np.where(np.arange(nb)[:, None] == tower, np.array([1.0, 0.8, 0.35]), red).astype(np.float32)
                        if t >= 40.5 else None)
        dd = sim["defect"][f]
        col = np.where(dd[:, None] > 0.5, np.array([0.9, 0.12, 0.1], np.float32), sim["shirt"])
        moving = sim["stand"][f] < 0.5
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(NP)], scale=np.ones(NP), rot=np.c_[np.zeros((NP, 2)), sim["py"][f]],
                     col=col, colors={"col2": sim["pants"]}, pose=pose_of(sim["ph"][f], moving))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])
        K.set_points(polo, np.c_[sim["pol_p"][f], np.zeros(NPOL)], scale=np.full(NPOL, float(sim["pol_on"][f])),
                     rot=np.c_[np.zeros((NPOL, 2)), sim["pol_y"][f]], col=np.ones((NPOL, 3)))
        ft = t - sim["fire_t"]
        fs = np.where((ft > 0) & (ft < 9.0) & (t < 26.0), np.clip(ft / 0.6, 0, 1) * (0.8 + 0.3 * np.sin(t * 11 + np.arange(NFIRE))), 0)
        ctx.set_ctl("fire3", 9.0)
        K.set_points(fire, np.c_[sim["fire_src"], np.full(NFIRE, 1.2)], scale=fs, rot=np.zeros((NFIRE, 3)),
                     col=np.ones((NFIRE, 3)))
        gw = float(sim["group_w"][f])
        K.set_points(ringo, np.c_[GROUPS, np.full(len(GROUPS), 0.2)], scale=np.full(len(GROUPS), 7.5 * gw),
                     rot=np.zeros((len(GROUPS), 3)), col=np.ones((len(GROUPS), 3)))
        ctx.set_ctl("rings", 1.4 * gw)

    ctx.on_frame(upd)
    ctx.anchor("police", lambda t: (float(sim["pol_p"][fi(t)][0][0]), float(sim["pol_p"][fi(t)][0][1]), 4.0))
    ctx.anchor("signal", lambda t: (float(sxy[0][0]), float(sxy[0][1]), 8.0))
