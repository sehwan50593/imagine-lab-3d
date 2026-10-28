"""EP09 만약 AI가 세상을 지배한다면? (잠실, 롯데월드타워 = AI 본부) — 10-28 장면형 개편

주인공 '나'가 석촌호수 산책로를 걷는 출근길을 1년 후 → 10년 후까지 장면마다 따라간다.
1인칭(나의 눈)과 3인칭(나의 뒤)을 번갈아, 장면마다 AI가 바꾸는 것 하나씩:
배달 로봇·드론 → 자율주행차 → 사무실 불 꺼짐 → 데이터센터와 도시 전력 → 로봇이 절반인 거리 → 추천 알고리즘.
장면 안에서는 실제 걷는 속도(1.3m/s), 시간은 장면 사이(깜빡임)에서만 건너뜀.
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, lines_of, people_colors, pose_of, sky_at, traffic

DUR = 56.0
META = {"id": "ep09", "title": "만약 AI가 세상을 지배한다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "A", "mode": "lydian", "bpm": 72, "seed": 99, "twist_at": 40.0}}
STYLE = "bench"
NP, NC, ND, NDC, NAC = 620, 120, 70, 8, 16
LAKE = (130.0, -95.0)
TOWER = (14.0, -6.0)

# (시작, 끝, 시점, 하늘, 로봇 비율, 표시 시각)  시점: 3rd 뒤에서 / 1st 나의 눈 / up 타워 올려봄 / high 높은 3인칭 / crane 하늘로
SCENES = [(0.0, 7.0, "3rd", "MORNING", 0.0, ("D-DAY", "08:10")),
          (7.0, 15.0, "1st", "DAY", 0.15, ("1년 후", "08:12")),
          (15.0, 23.0, "road", "DAY", 0.25, ("3년 후", "08:15")),
          (23.0, 31.0, "up", "DUSK", 0.35, ("5년 후", "17:40")),
          (31.0, 39.0, "high", "NIGHT", 0.45, ("6년 후", "21:00")),
          (39.0, 47.0, "1st", "NIGHT", 0.62, ("10년 후", "21:10")),
          (47.0, 52.0, "3rd", "NIGHT", 0.62, ("지금", "")),
          (52.0, 56.0, "crane", "NIGHT", 0.62, ("지금", ""))]

BEATS = [
    Beat(0.0, 7.0, badge="만약", title="AI가 세상을 지배한다면?", title_size=72,
         sub="어느 날부터 도시의 모든 결정을 AI가 내린다면?\n잠실에 사는 '나'의 출근길로 따라가 봅니다."),
    Beat(7.0, 15.0, badge="1년 후", title="1년 후, {cyan}배달 로봇{/}",
         sub="택배와 음식 배달은 로봇과 드론이 맡습니다.\n길에서 일하던 사람들이 하나둘 줄어듭니다."),
    Beat(15.0, 23.0, badge="3년 후", title="3년 후, 차는 {cyan}AI가 운전{/}",
         sub="도로 위 차가 모두 자율주행으로 바뀝니다.\n택시·버스 기사가 하던 일을 AI가 맡습니다."),
    Beat(23.0, 31.0, badge="5년 후", title="5년 후, {orange}사무실 불{/}이 꺼진다",
         sub="일자리의 40%가 AI와 겹친다는 분석(IMF).\n저녁이 오기 전에 사무실 불부터 꺼집니다."),
    Beat(31.0, 39.0, badge="6년 후", title="6년 후, 전기는 {cyan}AI 먼저{/}",
         sub="데이터센터가 쓰는 전기가 두 배로 늘면(IEA 전망)\n도시의 불빛이 줄어듭니다."),
    Beat(39.0, 47.0, badge="10년 후", title="10년 후, 거리의 {cyan}절반{/}이 로봇",
         sub="사람보다 로봇이 더 많이 걷는 거리.\n인터넷은 이미 그렇습니다. 트래픽의 53%가 봇."),
    Beat(47.0, 52.0, badge="반전", title="AI는 이미 당신을 고르고 있다", big="70%", big_size=112, big_color="cyan",
         sub="유튜브 시청 시간의 70%는 추천에서 나옵니다.\n이 영상을 보는 것도 AI 추천 덕분일지 모릅니다."),
    Beat(52.0, 56.0, badge="반전", title="그리고 이 영상도…",
         sub="3D 화면·음악·자막·시뮬레이션까지\n전부 AI가 만들었습니다."),
]
GRADE = {"exposure": 0.95, "bloom": 0.3, "bloom_thr": 1.0, "vignette": 0.32}


def _sky_keys():
    out = []
    for t0, t1, _, sky, _, _ in SCENES:
        out += [(t0 + 0.01, sky), (t1 - 0.01, sky)]
    return out


SKY = _sky_keys()


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def scene_of(t):
    for i, s in enumerate(SCENES):
        if s[0] <= t < s[1]:
            return i
    return len(SCENES) - 1


def simulate(build_dir):
    from engine.jamsil import geometry
    g = geometry()
    rs = np.random.default_rng(909)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    sc = np.array([scene_of(t) for t in ts])
    frac = np.array([SCENES[k][4] for k in sc], np.float32)
    pp, py, ph = crowd(rs, nf, NP, LAKE, 210)
    shirt, pants = people_colors(rs, NP)
    rank = rs.random(NP)
    robot = (rank[None, :] < frac[:, None]).astype(np.float32)
    cp, cy = traffic(rs, nf, NC, LAKE, 350)
    # ── 주인공 '나': 호수 근처 긴 산책로를 장면마다 다른 구간에서 걷는다 ──
    lines = [l_ for l_ in lines_of(g, "walk") if len(l_) >= 2 and np.min(np.hypot(*(l_ - np.array(LAKE)).T)) < 140]
    lens = [float(np.sum(np.hypot(*np.diff(l_, axis=0).T))) for l_ in lines]
    order = np.argsort(lens)[::-1]
    pro = np.zeros((nf, 2), np.float32)
    fwd = np.zeros((nf, 2), np.float32)
    walking = np.zeros(nf, bool)
    for k, (t0, t1, mode, *_rest) in enumerate(SCENES):
        l_ = lines[int(order[k % 3])]
        cum = np.r_[0, np.cumsum(np.hypot(*np.diff(l_, axis=0).T))]
        speed = 0.0 if mode == "up" else 1.3
        s0 = min(cum[-1] * (0.15 + 0.1 * (k % 4)), max(cum[-1] - speed * (t1 - t0) - 2, 0))
        heading = None
        for i in np.where(sc == k)[0]:
            s = s0 + speed * (ts[i] - t0)
            j = int(np.clip(np.searchsorted(cum, s) - 1, 0, len(l_) - 2))
            seg = l_[j + 1] - l_[j]
            d = seg / max(np.hypot(*seg), 1e-6)
            u = (s - cum[j]) / max(cum[j + 1] - cum[j], 1e-6)
            pro[i] = l_[j] + seg * u + np.array([-d[1], d[0]]) * 0.7
            heading = d if heading is None else heading * 0.93 + d * 0.07   # 굽은 길에서 고개가 확 돌지 않게
            heading = heading / np.hypot(*heading)
            fwd[i] = heading
            walking[i] = speed > 0
    pro_yaw = np.arctan2(fwd[:, 1], fwd[:, 0]).astype(np.float32)
    pro_ph = (ts * 1.3 / 1.4) % 1.0
    # 3년 후 장면: 나에게서 가장 가까운 찻길 지점 (차를 보며 걷는 장면)
    clines = [l_ for l_ in lines_of(g, "car") if len(l_) >= 2]
    mid = pro[int((15.0 + 19.0) * FPS)]
    li = int(np.argmin([np.min(np.hypot(*(l_ - mid).T)) for l_ in clines]))
    rl = clines[li]
    road = rl[np.argmin(np.hypot(*(rl - mid).T))]
    # 그 찻길을 줄지어 달리는 자율주행차 (양방향, 같은 간격·같은 속도 = AI가 한꺼번에 조절)
    rc = np.r_[0, np.cumsum(np.hypot(*np.diff(rl, axis=0).T))]
    s_road = rc[np.argmin(np.hypot(*(rl - mid).T))]
    ac_p = np.zeros((nf, NAC, 2), np.float32)
    ac_y = np.zeros((nf, NAC), np.float32)
    for q in range(NAC):
        sgn = 1.0 if q % 2 == 0 else -1.0
        s = s_road + sgn * (ts * 11.0) + (q // 2 - NAC / 4) * 16.0 * sgn
        s = (s - s_road + 150) % 300 - 150 + s_road
        s = np.clip(s, 0, rc[-1])
        j = np.clip(np.searchsorted(rc, s) - 1, 0, len(rl) - 2)
        seg = rl[j + 1] - rl[j]
        sl = np.maximum(rc[j + 1] - rc[j], 1e-6)
        d = seg / sl[:, None]
        ac_p[:, q] = rl[j] + seg * ((s - rc[j]) / sl)[:, None] + np.c_[-d[:, 1], d[:, 0]] * 1.8 * sgn
        ac_y[:, q] = np.arctan2(d[:, 1] * sgn, d[:, 0] * sgn)
    # ── 카메라 ──
    def vantage(dist, el, az=315.0):
        """타워를 가리는 건물이 없는 남동쪽 하늘 (tools/find_eye.py로 확인: 600m·고도각 12~25°)."""
        a, e = math.radians(az), math.radians(el)
        return np.array([TOWER[0] + math.cos(e) * math.cos(a) * dist, TOWER[1] + math.cos(e) * math.sin(a) * dist,
                         60 + math.sin(e) * dist], np.float32)

    cam_l = np.zeros((nf, 3), np.float32)
    cam_t = np.zeros((nf, 3), np.float32)
    lens_ = np.zeros(nf, np.float32)
    for i, t in enumerate(ts):
        k = sc[i]
        mode = SCENES[k][2]
        u = (t - SCENES[k][0]) / (SCENES[k][1] - SCENES[k][0])
        p = np.r_[pro[i], 0.0]
        f3 = np.r_[fwd[i], 0.0]
        if mode == "3rd":
            cl, tg, ln = p - f3 * 4.2 + np.array([0, 0, 2.3]), p + f3 * 7 + np.array([0, 0, 1.1]), 24
        elif mode == "1st":
            cl, tg, ln = p + f3 * 0.25 + np.array([0, 0, 1.62]), p + f3 * 12 + np.array([0, 0, 1.4]), 22
        elif mode == "up":       # 멈춰 서서 타워와 사무실을 올려다봄
            look = np.r_[TOWER, 60 + 120 * u]
            cl, tg, ln = p + np.array([0, 0, 1.62]), look, 22
        elif mode == "road":     # 나의 어깨 너머로 찻길을 봄
            to = np.r_[road - pro[i], 0.0]
            to = to / max(np.linalg.norm(to), 1e-6)
            cl, tg, ln = p - to * 4.0 + np.array([0, 0, 2.6]), np.r_[road, 1.0], 24
        elif mode == "high":     # 호수 위 높은 곳에서 타워 쪽 도시 전체
            cl = vantage(600 - 40 * u, 20)
            tg, ln = np.r_[TOWER, 70.0], 26
        else:                    # crane: 하늘로 올라가며 도시 전체
            cl = vantage(620 + 160 * u, 22 + 6 * u)
            tg, ln = np.r_[TOWER, 90.0], 26
        cam_l[i], cam_t[i], lens_[i] = cl, tg, ln
    # 1인칭일 때 카메라 바로 앞을 지나는 사람은 숨김 (얼굴을 뚫고 지나가지 않게)
    near_cam = np.hypot(pp[..., 0] - cam_l[:, None, 0], pp[..., 1] - cam_l[:, None, 1]) < 1.2
    hide = near_cam & np.isin(np.array([SCENES[k][2] for k in sc]), ["1st", "up"])[:, None]
    # ── 데이터센터: 6년 후 장면 시작에 공원 자리에서 솟아오름 ──
    gv, gfs = g["gv"], g["gfs"]
    cands = []
    i0 = 0
    for n in gfs:
        q = gv[i0:i0 + n, :2]
        i0 += n
        a = 0.5 * abs(np.sum(q[:, 0] * np.roll(q[:, 1], -1) - np.roll(q[:, 0], -1) * q[:, 1]))
        c = q.mean(0)
        if 150 < np.hypot(*c) < 1300 and a > 2500:
            cands.append((a, c))
    cands.sort(key=lambda x: -x[0])
    dc = np.array([c for _, c in cands[:NDC]], np.float32)
    dc_t = np.sort(rs.uniform(31.4, 35.0, len(dc)))
    dc_size = np.stack([rs.uniform(38, 60, len(dc)), rs.uniform(30, 48, len(dc)), rs.uniform(18, 30, len(dc))], 1)
    # ── 드론 (1년 후부터, 로봇 비율만큼) ──
    d0 = rs.uniform(-260, 260, (ND, 2)) + np.array(LAKE)
    dv = rs.normal(0, 1, (ND, 2))
    dv = dv / np.linalg.norm(dv, axis=1, keepdims=True) * rs.uniform(5, 9, ND)[:, None]
    dz = rs.uniform(14, 45, ND)
    drn = np.zeros((nf, ND, 3), np.float32)
    for i, t in enumerate(ts):
        q = d0 + dv * t
        drn[i, :, :2] = (q - np.array(LAKE) + 260) % 520 - 260 + np.array(LAKE)
        drn[i, :, 2] = dz + 2 * np.sin(t * 2 + np.arange(ND))
    drone_on = (rs.random(ND)[None, :] < np.clip(frac[:, None] * 1.6, 0, 1)).astype(np.float32)
    # ── 사무실 불: 5년 후 장면에서 건물마다 차례로 꺼짐 ──
    cent = g["b_cent"]
    off_t = 24.0 + rs.uniform(0, 6.0, len(cent))
    return dict(pp=pp, py=py, ph=ph, shirt=shirt, pants=pants, robot=robot, hide=hide.astype(np.float32),
                cp=cp, cy=cy, ac_p=ac_p, ac_y=ac_y, ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)],
                pro=pro, pro_yaw=pro_yaw, pro_ph=pro_ph.astype(np.float32), walking=walking.astype(np.float32),
                cam_l=cam_l, cam_t=cam_t, lens=lens_, scene=sc.astype(np.int32),
                dc=dc, dc_t=dc_t.astype(np.float32), dc_size=dc_size.astype(np.float32), drn=drn, drone_on=drone_on,
                off_t=off_t.astype(np.float32))


def sky(t):
    return sky_at(t, SKY)


def counter(t, sim):
    top, main = SCENES[scene_of(t)][5]
    return (top, main) if main else ("시뮬레이션", top)


def labels(t, anchors, sim):
    k = scene_of(t)
    t0, t1 = SCENES[k][0], SCENES[k][1]
    items = {1: [("robot", "배달 로봇", "cyan")], 2: [("me", "나", "white"), ("car", "자율주행차", "cyan")],
             3: [("tower", "AI 본부", "cyan")], 4: [(next((f"dc{j}" for j in range(NDC) if (anchors.get(f"dc{j}") or [0, 0, 0, 0])[3]), "dc0"), "데이터센터", "cyan")], 5: [("robot", "로봇", "cyan")],
             6: [("me", "나", "white")]}.get(k, [])
    out = []
    for key, nm, col in items:
        a = anchors.get(key)
        if a and a[3]:
            out.append({"x": min(960.0, max(130.0, a[0])), "y": a[1], "text": nm, "color": col, "size": 36, "lift": 8,
                        "alpha": min(ramp(t, t0 + 0.4, t0 + 0.9), 1 - ramp(t, t1 - 0.4, t1))})
    return out


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    from engine.jamsil_ep import light_keys
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
    me = J.people(1, "me")
    co = J.cars(NC)
    aco = J.cars(NAC, "acars")
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
    dmat = K.mat_simple("m_drone", (0.12, 0.12, 0.14), 0.4)
    led = K.mat_emit("m_led", (0.3, 1.0, 1.0), 10.0)
    parts = [(K.bm_cube(1.4, 0.18, 0.12), 0), (K.bm_cube(0.18, 1.4, 0.12), 0), (K.bm_sphere(0.16, (0, 0, -0.1), 8, 6), 1)]
    for sx in (-0.7, 0.7):
        for sy in (-0.7, 0.7):
            parts.append((K.bm_cone(0.32, 0.32, 0.03, (sx, sy, 0.08), 12), 0))
    dro = K.instancer(ctx, "drones", K.proto(ctx, "p_drone", K.join_bms(parts), [dmat, led]), ND)
    nb = J.nb
    J.set_buildings(gcol=np.tile((0.3, 0.9, 1.0), (nb, 1)).astype(np.float32), glow=np.zeros(nb), dark=np.zeros(nb))
    tower = int(g["tower"][0])
    lk = light_keys(SKY)
    dc, dcs, dct = sim["dc"], sim["dc_size"], sim["dc_t"]
    off_t = sim["off_t"]
    white = np.tile((0.9, 0.92, 0.95), (NC, 1)).astype(np.float32)

    def upd(t, f):
        k = int(sim["scene"][f])
        J.cam.look(sim["cam_l"][f], sim["cam_t"][f], float(sim["lens"][f]))
        night = J.light(t, lk)
        power = 1.0 - 0.5 * (k >= 4)
        ctx.set_ctl("lights", (0.12 + 0.55 * night) * power)
        ctx.set_ctl("carlights", 0.3 + 0.7 * night)
        dark = np.clip((t - off_t) / 0.6, 0, 1) * (k >= 3)
        glow = np.zeros(nb, np.float32)
        glow[tower] = (0.25 + 0.35 * night) * (k >= 3)
        J.set_buildings(glow=glow, dark=(0.85 * dark).astype(np.float32))
        h = np.clip((t - dct) / 1.6, 0, 1)
        K.set_points(dco, np.c_[dc, np.zeros(len(dc))], scale=(h > 0).astype(np.float32),
                     size=np.c_[dcs[:, 0], dcs[:, 1], np.maximum(dcs[:, 2] * h, 0.1)], rot=np.zeros((len(dc), 3)),
                     col=np.ones((len(dc), 3)))
        ctx.set_ctl("dc_glow", 2.5 + 3.5 * night)
        vis = 1 - sim["hide"][f]
        rb = sim["robot"][f]
        pose = pose_of(sim["ph"][f])
        rot = np.c_[np.zeros((NP, 2)), sim["py"][f]]
        P = np.c_[sim["pp"][f], np.zeros(NP)]
        K.set_points(humans, P, scale=(1 - rb) * vis, rot=rot, col=sim["shirt"], colors={"col2": sim["pants"]}, pose=pose)
        K.set_points(robots, P, scale=rb * vis, rot=rot, col=np.ones((NP, 3)), pose=pose)
        mode = SCENES[k][2]
        show_me = 1.0 if mode in ("3rd", "road") else 0.0
        mp = pose_of(np.array([sim["pro_ph"][f]]), np.array([sim["walking"][f] > 0]))
        K.set_points(me, np.r_[sim["pro"][f], 0.0][None], scale=np.array([show_me]),
                     rot=np.array([[0, 0, float(sim["pro_yaw"][f])]]), col=np.array([[1.0, 0.38, 0.08]]),
                     colors={"col2": np.array([[0.12, 0.14, 0.22]])}, pose=mp)
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=white if k >= 2 else sim["ccol"])
        K.set_points(aco, np.c_[sim["ac_p"][f], np.zeros(NAC)], scale=np.full(NAC, 10.0 if k >= 2 else 0.0),
                     rot=np.c_[np.zeros((NAC, 2)), sim["ac_y"][f]], col=white[:NAC])
        K.set_points(dro, sim["drn"][f], scale=sim["drone_on"][f] * 2.6,
                     rot=np.c_[np.zeros((ND, 2)), np.full(ND, t * 0.3)], col=np.ones((ND, 3)))

    ctx.on_frame(upd)

    def nearest(key, valid):
        """카메라 앞 15~45m 안의 것 하나에 이름표."""
        def fn(t):
            f = fi(t)
            c, tg = sim["cam_l"][f], sim["cam_t"][f]
            d = tg[:2] - c[:2]
            d = d / max(np.hypot(*d), 1e-6)
            P = sim[key][f] if sim[key].ndim == 3 else sim[key]
            rel = P - c[:2]
            ahead = rel @ d
            side = np.abs(rel[:, 0] * d[1] - rel[:, 1] * d[0])
            ok = (ahead > 12) & (ahead < 45) & (side < ahead * 0.25) & valid(f)
            if not ok.any():
                return None
            i = int(np.argmin(np.where(ok, ahead, 1e9)))
            return float(P[i, 0]), float(P[i, 1]), 2.4
        return fn

    ctx.anchor("me", lambda t: (float(sim["pro"][fi(t)][0]), float(sim["pro"][fi(t)][1]), 1.8))
    ctx.anchor("robot", nearest("pp", lambda f: sim["robot"][f] > 0))
    ctx.anchor("car", nearest("ac_p", lambda f: np.ones(NAC, bool)))
    ctx.anchor("tower", lambda t: (TOWER[0], TOWER[1], 470.0))
    for j in range(len(dc)):
        ctx.anchor(f"dc{j}", (lambda j: lambda t: (float(dc[j, 0]), float(dc[j, 1]), float(dcs[j, 2]) + 6))(j))
