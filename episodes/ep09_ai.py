"""EP09 만약 AI가 세상을 지배한다면? (잠실, 롯데월드타워 = AI 본부)

실제로 계산하는 것:
- AI 도입률: 로지스틱 확산 → 거리의 사람이 하나둘 로봇(청록)으로 바뀜, 하늘의 드론 수 증가
- 데이터센터: 공원 자리에 솟아오르고, 전력 수요(IEA 415 → 945 TWh 비율)만큼 도시 창문 불빛이 줄어듦
- 청록 확산: 타워에서 가까운 건물부터 차례로 'AI 건물'이 됨
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import (CAR_COLORS, crowd, light_keys, people_colors, pose_of, set_cam, sky_at, traffic)

DUR = 56.0
META = {"id": "ep09", "title": "만약 AI가 세상을 지배한다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "A", "mode": "lydian", "bpm": 72, "seed": 99, "twist_at": 40.0}}
NP, NC, ND, NDC = 620, 120, 70, 8

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY", label="만약", title="AI가 세상을 지배한다면?", title_size=76,
         note="ChatGPT 주간 사용자 9억 명 이상 (OpenAI, 2026)",
         sub="어느 날부터 도시의 모든 결정을\nAI가 내리기 시작한다면?"),
    Beat(4.5, 10.0, badge="+1개월", title="전기 먹는 {cyan}데이터센터{/}", big="415 TWh", big_size=104,
         note="2024년 데이터센터 전력, 세계의 약 1.5% (IEA)",
         sub="AI를 돌리는 데이터센터가\n도시 곳곳에 들어섭니다."),
    Beat(10.0, 16.0, badge="+1년", title="일자리 {orange}40%{/}가 AI와 겹친다", note="IMF(2024): '노출'이지 '사라짐'은 아님",
         sub="사무실 일의 상당 부분을\nAI가 함께 하거나 대신합니다."),
    Beat(16.0, 22.0, badge="+3년", title="로봇 {cyan}500만 대{/}", note="전 세계 공장에서 일하는 산업용 로봇 (IFR, 2025)",
         sub="공장과 물류창고부터\n로봇이 먼저 자리를 차지합니다."),
    Beat(22.0, 28.0, badge="+5년", title="해마다 {yellow}5배{/}", note="최첨단 AI 학습 연산량 증가 속도 (Epoch AI)",
         sub="AI를 학습시키는 계산량이\n해마다 약 5배씩 늘고 있습니다."),
    Beat(28.0, 34.0, badge="+6년", title="2030년, AI가 쓰는 전기", big="945 TWh", big_size=104,
         note="데이터센터 전력 전망 (IEA)",
         sub="6년 만에 두 배가 넘는 전기를\n데이터센터가 쓰게 됩니다."),
    Beat(34.0, 40.0, badge="+10년", title="인터넷의 주인은?", big="봇 53%", big_size=104, big_color="cyan",
         note="2025년 웹 트래픽 중 봇의 비율 (Thales)",
         sub="이미 인터넷 트래픽의 절반 이상은\n사람이 아닙니다."),
    Beat(40.0, 48.0, badge="반전", title="AI는 이미 당신을 고르고 있다", big="70%", big_size=112, big_color="cyan",
         note="유튜브 시청 시간 중 추천으로 본 비율 (2018)",
         sub="당신이 지금 이 영상을 보는 것도\nAI 추천 덕분일 가능성이 큽니다."),
    Beat(48.0, 53.0, badge="반전", title="그리고 이 영상도…",
         sub="3D 화면·음악·자막·시뮬레이션까지\n전부 AI가 만들었습니다."),
    Beat(53.0, 56.0, badge="지금", title="AI는 이미\n세상을 {cyan}지배{/}하고 있을까요?", title_size=76),
]
GRADE = {"exposure": 0.95, "bloom": 0.3, "bloom_thr": 1.0, "vignette": 0.32}
SKY = [(0.0, "DAY"), (15.4, "DAY"), (16.4, "DUSK"), (21.6, "DUSK"), (22.6, "NIGHT"), (33.4, "NIGHT"), (34.4, "DAY"),
       (39.4, "DAY"), (40.6, "NIGHT"), (56.0, "NIGHT")]
CLOCK = [(0.0, 0.0), (4.5, 0.0), (5.0, 30.0), (10.0, 35.0), (10.5, 365.0), (16.0, 380.0), (16.5, 1096.0),
         (22.0, 1110.0), (22.5, 1826.0), (28.0, 1840.0), (28.5, 2192.0), (34.0, 2200.0), (34.5, 3652.0), (56.0, 3660.0)]


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def simulate(build_dir):
    from engine.jamsil import geometry
    g = geometry()
    rs = np.random.default_rng(909)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    days = np.array([keyed(t, CLOCK, ease=lambda u: u) for t in ts])
    years = days / 365.25
    adopt = 1 / (1 + np.exp(-(years - 4.0) * 1.1))          # AI 도입률 (로지스틱)
    adopt = (adopt - adopt[0]) / (1 - adopt[0]) * 0.62
    pp, py, ph = crowd(rs, nf, NP, (130, -95), 210)
    shirt, pants = people_colors(rs, NP)
    rank = rs.random(NP)
    robot = (rank[None, :] < adopt[:, None]).astype(np.float32)
    cp, cy = traffic(rs, nf, NC, (0, 0), 800)
    # 데이터센터: 타워 주변 큰 녹지에서 솟아오름
    gv, gfs = g["gv"], g["gfs"]
    cands = []
    i0 = 0
    for n in gfs:
        p = gv[i0:i0 + n, :2]
        i0 += n
        a = 0.5 * abs(np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1]))
        c = p.mean(0)
        d = np.hypot(*c)
        if 150 < d < 1300 and a > 2500:
            cands.append((a, c))
    cands.sort(key=lambda x: -x[0])
    dc = np.array([c for _, c in cands[:NDC]], np.float32)
    dc_t = np.sort(rs.uniform(4.8, 9.2, len(dc)))
    dc_size = np.stack([rs.uniform(38, 60, len(dc)), rs.uniform(30, 48, len(dc)), rs.uniform(18, 30, len(dc))], 1)
    # 드론: 높이 30~90m, 직선 비행 (도입률에 따라 대수 증가)
    d0 = rs.uniform(-260, 260, (ND, 2)) + np.array([110, -85])
    dv = rs.normal(0, 1, (ND, 2))
    dv = dv / np.linalg.norm(dv, axis=1, keepdims=True) * rs.uniform(8, 16, ND)[:, None]
    dz = rs.uniform(14, 55, ND)
    drn = np.zeros((nf, ND, 3), np.float32)
    for i, t in enumerate(ts):
        p = d0 + dv * t
        p = (p - np.array([110, -85]) + 260) % 520 - 260 + np.array([110, -85])
        drn[i, :, :2] = p
        drn[i, :, 2] = dz + 2 * np.sin(t * 2 + np.arange(ND))
    drank = rs.random(ND)
    drone_on = (drank[None, :] < np.clip(adopt[:, None] * 1.6, 0, 1)).astype(np.float32)
    # 청록 확산: 타워에서 가까운 건물부터
    cent = g["b_cent"]
    bd = np.hypot(cent[:, 0], cent[:, 1]) + rs.uniform(0, 200, len(cent))
    order_d = np.sort(bd)
    return dict(days=days, adopt=adopt.astype(np.float32), pp=pp, py=py, ph=ph, shirt=shirt, pants=pants,
                robot=robot, cp=cp, cy=cy, ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)],
                dc=dc, dc_t=dc_t.astype(np.float32), dc_size=dc_size.astype(np.float32), drn=drn,
                drone_on=drone_on, bd=bd.astype(np.float32), bd_sorted=order_d.astype(np.float32))


def sky(t):
    return sky_at(t, SKY)


def hud(t, sim):
    f = fi(t)
    d = float(sim["days"][f])
    right = "D-DAY" if d < 1 else (f"D+{int(d)}" if d < 300 else f"{d / 365.25:.0f}년 후")
    a = float(sim["adopt"][f])
    left = "SIMULATION" if t < 48.0 else "MADE BY AI"
    return {"left": left, "right": right, "right2": f"이 구역 로봇 비율 {int(round(100 * a))}% (가정)"}


CAM = [(0.0, (130.0, -95.0, 3.0), 322, 24, 48.0, 30), (4.4, (130.0, -95.0, 3.0), 330, 26, 52.0, 30),
       (4.9, (60.0, -60.0, 30.0), 300, 30, 520.0, 30), (9.6, (60.0, -60.0, 30.0), 315, 32, 560.0, 30),
       (10.2, (130.0, -95.0, 2.0), 310, 30, 40.0, 30), (15.8, (130.0, -95.0, 2.0), 325, 32, 44.0, 30),
       (16.4, (100.0, -80.0, 25.0), 300, 18, 120.0, 30), (21.8, (100.0, -80.0, 25.0), 315, 20, 130.0, 30),
       (22.4, (14.0, -6.0, 200.0), 230, 12, 950.0, 32), (27.8, (14.0, -6.0, 200.0), 250, 14, 900.0, 32),
       (28.4, (-200.0, 50.0, 10.0), 210, 50, 1100.0, 28), (33.8, (-200.0, 50.0, 10.0), 230, 54, 1200.0, 28),
       (34.4, (130.0, -95.0, 3.0), 300, 24, 70.0, 30), (39.8, (130.0, -95.0, 3.0), 315, 26, 78.0, 30),
       (40.4, (14.0, -6.0, 150.0), 240, 10, 760.0, 32), (47.8, (14.0, -6.0, 150.0), 255, 12, 720.0, 32),
       (48.4, (130.0, -95.0, 3.0), 320, 28, 60.0, 30), (52.8, (130.0, -95.0, 3.0), 330, 30, 70.0, 30),
       (53.4, (-200.0, 0.0, 20.0), 260, 40, 1500.0, 28), (56.0, (-200.0, 0.0, 20.0), 275, 44, 1650.0, 28)]


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    humans = J.people(NP, "humans")
    rposes = K.person_poses(ctx, K.mat_simple("m_robot", (0.78, 0.8, 0.84), 0.3, metal=0.7,
                                                emit=(0.3, 0.95, 1.0), estr=0.8),
                            K.mat_simple("m_robot2", (0.3, 0.32, 0.36), 0.4, metal=0.6),
                            K.mat_simple("m_robot3", (0.8, 0.82, 0.86), 0.3, metal=0.6),
                            K.mat_emit("m_visor", (0.3, 0.95, 1.0), 5.0), height=1.8)
    robots = K.instancer_multi(ctx, "robots", rposes, NP)
    co = J.cars(NC)
    # 데이터센터: 청록 줄무늬 상자
    dm, nt, out = K.new_mat("m_dc")
    tco = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    K.ln(nt, tco.outputs["Object"], sp.inputs[0])
    stripe = K.math_node(nt, "LESS_THAN", K.math_node(nt, "FRACT", K.math_node(nt, "MULTIPLY", sp.outputs["Z"], 9.0)), 0.12)
    b = K.principled(nt, (0.08, 0.09, 0.11), 0.4, metal=0.5, emit=(0.25, 0.9, 1.0),
                     estr=K.math_node(nt, "MULTIPLY", stripe, ctx.ctl_node(nt, "dc_glow", 4.0)))
    K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    dm.cycles.emission_sampling = "NONE"
    dco = K.instancer(ctx, "datacenters", K.proto_box(ctx, dm, "p_dc"), len(sim["dc"]), vector_scale=True)
    # 드론
    dmat = K.mat_simple("m_drone", (0.12, 0.12, 0.14), 0.4)
    led = K.mat_emit("m_led", (0.3, 1.0, 1.0), 10.0)
    parts = [(K.bm_cube(1.4, 0.18, 0.12), 0), (K.bm_cube(0.18, 1.4, 0.12), 0), (K.bm_sphere(0.16, (0, 0, -0.1), 8, 6), 1)]
    for sx in (-0.7, 0.7):
        for sy in (-0.7, 0.7):
            parts.append((K.bm_cone(0.32, 0.32, 0.03, (sx if abs(sx) else 0, sy, 0.08), 12), 0))
    dro = K.instancer(ctx, "drones", K.proto(ctx, "p_drone", K.join_bms(parts), [dmat, led]), len(sim["drn"][0]))
    nb = J.nb
    cyan = np.tile((0.3, 0.9, 1.0), (nb, 1)).astype(np.float32)
    J.set_buildings(gcol=cyan, glow=np.zeros(nb), dark=np.zeros(nb))
    tower = int(g["tower"][0])
    lk = light_keys(SKY)
    dc, dcs, dct = sim["dc"], sim["dc_size"], sim["dc_t"]
    bd = sim["bd"]

    def upd(t, f):
        set_cam(J, t, CAM)
        night = J.light(t, lk)
        a = float(sim["adopt"][f])
        power = 1.0 - 0.55 * ramp(t, 28.0, 31.0) * (1 - ramp(t, 39.5, 40.5) * 0.5)
        ctx.set_ctl("lights", (0.12 + 0.55 * night) * power)
        ctx.set_ctl("carlights", 0.3 + 0.7 * night)
        # 청록 확산: 도입률이 높을수록 타워에서 먼 건물까지
        reach = np.interp(a, [0, 0.62], [0, 1600])
        glow = np.where(bd < reach, 0.08 + 0.12 * night, 0.0).astype(np.float32)
        glow[tower] = min(1.0, 0.25 + a) * (0.2 + 0.3 * night)
        J.set_buildings(glow=glow)
        h = np.clip((t - dct) / 1.6, 0, 1)
        K.set_points(dco, np.c_[dc, np.zeros(len(dc))], scale=(h > 0).astype(np.float32),
                     size=np.c_[dcs[:, 0], dcs[:, 1], np.maximum(dcs[:, 2] * h, 0.1)], rot=np.zeros((len(dc), 3)),
                     col=np.ones((len(dc), 3)))
        ctx.set_ctl("dc_glow", 2.5 + 3.5 * night)
        rb = sim["robot"][f]
        pose = pose_of(sim["ph"][f])
        rot = np.c_[np.zeros((NP, 2)), sim["py"][f]]
        P = np.c_[sim["pp"][f], np.zeros(NP)]
        K.set_points(humans, P, scale=1 - rb, rot=rot, col=sim["shirt"], colors={"col2": sim["pants"]}, pose=pose)
        K.set_points(robots, P, scale=rb, rot=rot, col=np.ones((NP, 3)), pose=pose)
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])
        nd = sim["drn"].shape[1]
        K.set_points(dro, sim["drn"][f], scale=sim["drone_on"][f] * 2.6,
                     rot=np.c_[np.zeros((nd, 2)), np.full(nd, t * 0.3)], col=np.ones((nd, 3)))

    ctx.on_frame(upd)
