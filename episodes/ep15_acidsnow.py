"""EP15 만약 눈이 염산이라면? (잠실 석촌호수) — 예전 방식(한자리 관찰자·숫자 자막)

실제로 계산하는 것:
- 눈 덮임: 땅·도로·잔디에 눈 얼룩이 시간에 따라 넓어짐, 하얀 산성 김(염화수소)이 피어오름
- 사람: 김이 오르면 뛰기 시작해 건물 안으로 사라지는 비율이 늘어남
- 금속: 차가 멈춰 서고 차체가 녹 색으로, 나무·잔디는 갈색으로, 호수는 산성 색으로
- 콘크리트(석회)는 얼룩지며 깎이고, 유리 타워는 그대로
숫자: 염산 pH 1 가정 · 위산 pH 1.5~3.5 · 산성비 기준 pH 5.6 · NOAA CAMEO Chemicals(염산 성질).
"""
import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, eye_from, people_colors, pose_of, set_cam, traffic

DUR = 56.0
META = {"id": "ep15", "title": "만약 눈이 염산이라면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "E", "mode": "major", "bpm": 72, "seed": 151, "twist_at": 46.0}}
NP, NC, NS, NF = 600, 120, 1400, 200
LAKE = (130.0, -95.0)
TOWER = (14.0, -6.0)

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY 08:00", label="첫눈", big="pH 1", label_color="cyan", big_color="cyan",
         sub="올겨울 첫눈이 물이 아니라\n진한 염산으로 내린다면?"),
    Beat(4.5, 10.0, badge="+5분", title="눈 닿는 곳마다 {yellow}하얀 김{/}",
         note="진한 염산은 습한 공기에서 염화수소 안개를 만듦 (NOAA)",
         sub="코를 찌르는 김이 피어오르고\n사람들은 건물 안으로 뜁니다."),
    Beat(10.0, 16.0, badge="+30분", title="금속이 {orange}녹기 시작{/}", note="철·알루미늄 + 염산 → 수소 거품",
         sub="차는 멈춰 서고 차체와 우산 살대가\n거품을 내며 삭아 갑니다."),
    Beat(16.0, 22.0, badge="+반나절", title="공원이 {orange}갈색{/}으로", big="잔디 · 나무", big_size=96, big_color="orange",
         sub="잎과 잔디는 산에 타 갈색이 되고\n석촌호수는 물고기가 못 사는 산성 호수가 됩니다."),
    Beat(22.0, 28.0, badge="+3일", title="{orange}콘크리트{/}가 깎인다", note="석회(탄산칼슘) + 염산 → 이산화탄소 거품",
         sub="건물 겉면은 거품을 내며 얼룩지고\n조금씩 깎여 나갑니다."),
    Beat(28.0, 34.0, badge="+3일", title="그런데 {cyan}유리{/}는 멀쩡", big="유리", big_size=104, big_color="cyan",
         note="염산은 실험실에서 유리병에 보관함",
         sub="유리로 덮인 타워만은\n거의 그대로 서 있습니다."),
    Beat(34.0, 40.0, badge="+1주", title="텅 빈 도시", big="외출 0명", big_size=100, big_color="gray",
         sub="방독면 없이는 밖에 나갈 수 없고\n눈 대신 석회를 뿌려 산을 중화합니다."),
    Beat(40.0, 46.0, badge="+1달", title="비가 와도 {yellow}끝이 아니다{/}",
         sub="녹은 산은 하수도와 한강으로 흘러\n강물까지 산성으로 만듭니다."),
    Beat(46.0, 52.5, badge="반전", title="염산은 이미 당신 안에 있다", big="pH 1.5", big_size=112, big_color="yellow",
         note="위산의 주성분 = 염산 (pH 1.5~3.5)",
         sub="위벽은 점액으로 매일\n이 염산에서 스스로를 지킵니다."),
    Beat(52.5, 56.0, badge="지금", title="진짜 산성비는\n이것보다 {cyan}4만 배{/} 약하다", title_size=74),
]
GRADE = {"exposure": 1.0, "bloom": 0.2, "bloom_thr": 1.0, "vignette": 0.3}

# 흐린 눈 오는 날 빛 → 1주 뒤 해 질 녘 → 반전은 밤
GREY = dict(elev=38, az=-30, energy=1.4, col=(0.92, 0.94, 1.0), amb=0.55, amb_col=(0.62, 0.66, 0.74))
LATE = dict(elev=8, az=100, energy=0.9, col=(1.0, 0.72, 0.55), amb=0.3, amb_col=(0.42, 0.42, 0.52))
DARK = dict(elev=50, az=160, energy=0.35, col=(0.55, 0.65, 1.0), amb=0.08, amb_col=(0.10, 0.13, 0.28))
SKY_GREY = ((0.24, 0.26, 0.30), (0.50, 0.51, 0.53), 0.0)
SKY_LATE = ((0.08, 0.09, 0.14), (0.38, 0.30, 0.28), 0.0)
SKY_DARK = ((0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0)
LIGHT_KEYS = [(0.0, GREY), (33.6, GREY), (34.6, LATE), (45.6, LATE), (46.6, DARK), (56.0, DARK)]
SKY_KEYS = [(a, (*v[0], *v[1], v[2])) for a, v in
            [(0.0, SKY_GREY), (33.6, SKY_GREY), (34.6, SKY_LATE), (45.6, SKY_LATE), (46.6, SKY_DARK), (56.0, SKY_DARK)]]
RUST = np.array((0.40, 0.19, 0.07), np.float32)
BROWN = np.array((0.30, 0.20, 0.08), np.float32)

CAM = [(0.0, (130.0, -95.0, 3.0), 322, 24, 48.0, 30), (4.4, (130.0, -95.0, 3.0), 330, 26, 52.0, 30),
       (4.9, (115.0, -85.0, 2.0), 312, 22, 36.0, 30), (9.6, (115.0, -85.0, 2.0), 322, 24, 40.0, 30),
       (10.2, (100.0, -80.0, 2.0), 300, 18, 70.0, 30), (15.8, (100.0, -80.0, 2.0), 312, 20, 78.0, 30),
       (16.4, (130.0, -110.0, 2.0), 310, 30, 120.0, 30), (21.8, (130.0, -110.0, 2.0), 322, 32, 132.0, 30),
       (22.4, (60.0, -60.0, 20.0), 300, 26, 260.0, 30), (27.8, (60.0, -60.0, 20.0), 312, 28, 280.0, 30),
       (28.4, (14.0, -6.0, 200.0), 230, 12, 950.0, 32), (33.8, (14.0, -6.0, 200.0), 250, 14, 900.0, 32),
       (34.4, (130.0, -95.0, 3.0), 300, 24, 70.0, 30), (39.8, (130.0, -95.0, 3.0), 315, 26, 78.0, 30),
       (40.4, (-200.0, 50.0, 10.0), 210, 50, 1100.0, 28), (45.8, (-200.0, 50.0, 10.0), 230, 54, 1200.0, 28),
       (46.4, (14.0, -6.0, 150.0), 240, 10, 760.0, 32), (52.4, (14.0, -6.0, 150.0), 255, 12, 720.0, 32),
       (53.0, (-200.0, 0.0, 20.0), 260, 40, 1500.0, 28), (56.0, (-200.0, 0.0, 20.0), 275, 44, 1650.0, 28)]
EYE = eye_from(CAM[0], 15.0, 75.0)   # 09편과 같은 호수 쪽 관찰 위치 (건물에 안 가림)
CLOCK = [(0.0, 0.0), (4.5, 0.0), (5.0, 5.0), (10.0, 6.0), (10.5, 30.0), (16.0, 32.0), (16.5, 300.0), (22.0, 320.0),
         (22.5, 4320.0), (34.0, 4400.0), (34.5, 10080.0), (40.0, 10100.0), (40.5, 43200.0), (56.0, 43300.0)]


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def gone_at(t):
    """건물 안으로 들어간 사람 비율."""
    return float(np.interp(t, [0, 5.0, 10.0, 16, 22, 34, 36], [0, 0, 0.55, 0.75, 0.88, 0.95, 1.0]))


def run_at(t):
    return float(np.interp(t, [0, 5.0, 6.5, 12, 18], [1.0, 1.0, 2.3, 2.3, 1.0]))


def stop_at(t):
    return float(np.interp(t, [0, 10.5, 13.5], [1.0, 1.0, 0.0]))


def wilt_at(t):
    return float(np.interp(t, [0, 16.3, 20.5], [0.0, 0.0, 1.0]))


def snow_cover_at(t):
    return float(np.interp(t, [0, 3, 8, 16, 22, 34, 40, 46], [0.0, 0.08, 0.2, 0.36, 0.45, 0.55, 0.4, 0.2]))


def simulate(build_dir):
    from engine.jamsil import geometry
    g = geometry()
    rs = np.random.default_rng(1515)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    pp, py, ph = crowd(rs, nf, NP, LAKE, 220, t_speed=run_at)
    shirt, pants = people_colors(rs, NP)
    rank = rs.random(NP)
    gone = np.array([gone_at(t) for t in ts], np.float32)
    vis = (rank[None, :] >= gone[:, None]).astype(np.float32)
    cp, cy = traffic(rs, nf, NC, LAKE, 420, stop=stop_at)
    eye = np.array(EYE, np.float32)
    # ── 하얀 산성 김: 호수 주변 땅에서 피어올라 커지다 사라짐 (수명 3초) ──
    life = 3.0
    fb = rs.uniform(0, life, NF)
    spawn = np.array(LAKE, np.float32) + rs.normal(0, 45, (NF, 2)).astype(np.float32)
    fp = np.zeros((nf, NF, 3), np.float32)
    fs = np.zeros((nf, NF), np.float32)
    amt = np.interp(ts, [0, 4.5, 5.5, 16, 22, 28, 34], [0.15, 0.15, 1.0, 0.7, 0.35, 0.3, 0.0])
    frank = rs.random(NF)
    last = np.full(NF, -1)
    for i, t in enumerate(ts):
        cyc = np.floor((t + fb) / life).astype(int)
        age = ((t + fb) % life) / life
        new = cyc != last
        if new.any():
            spawn[new] = np.array(LAKE, np.float32) + rs.normal(0, 45, (int(new.sum()), 2)).astype(np.float32)
            last[new] = cyc[new]
        fp[i, :, :2] = spawn
        fp[i, :, 2] = 0.3 + 2.5 * age
        far = np.hypot(*(spawn - eye[:2]).T) > 40.0   # 카메라 바로 앞은 비움 (화면이 뿌예지지 않게)
        fs[i] = (frank < amt[i]) * far * np.sin(np.pi * age) * (0.8 + 1.6 * age)
    # ── 눈송이: 관찰 위치 앞 상자 안에서 떨어짐 ──
    base = rs.uniform([-30, -30, 0], [30, 30, 30], (NS, 3)).astype(np.float32)
    fall = rs.uniform(1.0, 1.6, NS).astype(np.float32)
    srank = rs.random(NS)
    s_amt = np.interp(ts, [0, 4.5, 16, 34, 40, 46], [0.6, 1.0, 0.8, 0.45, 0.2, 0.0])
    sp_ = np.zeros((nf, NS, 3), np.float32)
    ss_ = np.zeros((nf, NS), np.float32)
    for i, t in enumerate(ts):
        off = base[:, :2] + np.array([0.6, 0.3]) * t
        xy = eye[:2] + (off + 30) % 60 - 30
        z = eye[2] - 25 + (base[:, 2] - fall * t) % 30
        sp_[i] = np.c_[xy, z]
        d = np.linalg.norm(sp_[i] - eye, axis=1)
        ss_[i] = (srank < s_amt[i]) * (d > 3.0) * (z > 0.05)
    car_j = rs.uniform(0, 3, NC).astype(np.float32)
    tree_j = rs.uniform(0, 3, len(g["trees"])).astype(np.float32)
    etch = rs.uniform(0.6, 0.9, len(g["b_h"])).astype(np.float32)
    days = np.array([keyed(t, CLOCK, ease=lambda u: u) for t in ts], np.float32)
    return dict(pp=pp, py=py, ph=ph, shirt=shirt, pants=pants, vis=vis, cp=cp, cy=cy,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)], fp=fp, fs=fs.astype(np.float32),
                sp=sp_, ss=ss_.astype(np.float32), car_j=car_j, tree_j=tree_j, etch=etch, mins=days)


def sky(t):
    v = keyed(t, SKY_KEYS)
    return v[0:3], v[3:6], v[6]


def hud(t, sim):
    m = float(sim["mins"][fi(t)])
    if m < 60:
        right = f"+{int(m)}분"
    elif m < 1440:
        right = f"+{int(m // 60)}시간"
    else:
        right = f"D+{int(m // 1440)}"
    out = int(round(100 * float(sim["vis"][fi(t)].mean())))
    r2 = "반전" if t >= 46 else f"밖에 있는 사람 {out}%"
    return {"left": "SIMULATION", "right": right, "right2": r2}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("tower")
    if a and a[3] and 28.6 < t < 33.6:
        out.append({"x": a[0], "y": a[1], "text": "유리 타워 · 멀쩡", "color": "cyan", "size": 30, "lift": 10,
                    "alpha": ramp(t, 28.8, 29.4)})
    a = anchors.get("lake")
    if a and a[3] and 16.6 < t < 21.6:
        out.append({"x": a[0], "y": a[1], "text": "산성 호수", "color": "yellow", "size": 30, "alpha": ramp(t, 17.0, 17.6)})
    return out


def _snowify(K, ctx, mat, ctl, color, scale=0.35):
    """기존 재질의 바탕색에 ctl 값만큼 얼룩덜룩 섞기 (엔진 재질은 그대로 두고 이 편에서만)."""
    nt = mat.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    sock = b.inputs["Base Color"]
    src = sock.links[0].from_socket if sock.is_linked else tuple(sock.default_value)[:3]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 4.0
    K.ln(nt, geo.outputs["Position"], nz.inputs["Vector"])
    cov = ctx.ctl_node(nt, ctl, 0.0)
    fac = K.math_node(nt, "MULTIPLY", K.math_node(nt, "SUBTRACT", nz.outputs["Fac"],
                                                    K.math_node(nt, "SUBTRACT", 1.0, cov)), 6.0, clamp=True)
    K.ln(nt, K.mix_rgb(nt, fac, src, color), sock)


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    import bpy
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    snow_white = (0.86, 0.88, 0.90)
    for name, scale in (("m_city_ground", 0.35), ("m_jroad", 0.5)):
        _snowify(K, ctx, bpy.data.materials[name], "snow", snow_white, scale)
    _snowify(K, ctx, bpy.data.materials["m_grass"], "wilt", tuple(BROWN), 0.08)
    _snowify(K, ctx, bpy.data.materials["m_grass"], "snow", snow_white, 0.35)
    _snowify(K, ctx, bpy.data.materials["m_jwater"], "acid", (0.16, 0.17, 0.05), 0.02)
    humans = J.people(NP, "humans")
    co = J.cars(NC)
    fm, nt, out = K.new_mat("m_fume")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    df = K.principled(nt, (0.92, 0.94, 0.9), 1.0)
    mx = nt.nodes.new("ShaderNodeMixShader")
    mx.inputs[0].default_value = 0.25
    K.ln(nt, tr.outputs[0], mx.inputs[1])
    K.ln(nt, df.outputs["BSDF"], mx.inputs[2])
    K.ln(nt, mx.outputs[0], out.inputs["Surface"])
    fum = K.instancer(ctx, "fumes", K.proto(ctx, "p_fume", K.bm_ico(1.0, (0, 0, 0), 2), [fm], smooth=True), NF)
    flake = K.mat_simple("m_flake", (0.95, 0.96, 1.0), 0.5, emit=(0.9, 0.92, 1.0), estr=0.35)
    snow = K.instancer(ctx, "flakes", K.proto(ctx, "p_flake", K.bm_ico(0.06, (0, 0, 0), 1), [flake]), NS)
    nb = J.nb
    J.set_buildings(gcol=np.tile((1.0, 0.8, 0.5), (nb, 1)).astype(np.float32), glow=np.zeros(nb), dark=np.zeros(nb),
                    burn=np.zeros(nb))
    tower = int(g["tower"][0])
    tr_xy = J.tree_xy
    tree_green = np.array([(0.13, 0.36, 0.10), (0.18, 0.42, 0.12), (0.10, 0.30, 0.12)], np.float32)[
        np.random.default_rng(9).integers(0, 3, len(tr_xy))]
    etch = sim["etch"].copy()
    etch[tower] = 0.0

    def upd(t, f):
        set_cam(J, t, CAM, eye=EYE)
        night = J.light(t, LIGHT_KEYS)
        ctx.set_ctl("lights", 0.1 + 0.5 * night)
        ctx.set_ctl("carlights", 0.4 + 0.6 * night)
        ctx.set_ctl("snow", snow_cover_at(t))
        w = wilt_at(t)
        ctx.set_ctl("wilt", 0.15 + 0.85 * w if w > 0 else 0.0)
        ctx.set_ctl("acid", 0.9 * w)
        tw = np.clip((t - 16.3 - sim["tree_j"]) / 3.0, 0, 1)[:, None]
        K.set_points(J.to, np.c_[tr_xy, np.zeros(len(tr_xy))], col=tree_green * (1 - tw) + BROWN * tw)
        J.set_buildings(burn=(etch * np.clip((t - 22.3) / 4.0, 0, 1)).astype(np.float32))
        K.set_points(humans, np.c_[sim["pp"][f], np.zeros(NP)], scale=sim["vis"][f],
                     rot=np.c_[np.zeros((NP, 2)), sim["py"][f]], col=sim["shirt"], colors={"col2": sim["pants"]},
                     pose=pose_of(sim["ph"][f]))
        rust = (np.clip((t - 10.3 - sim["car_j"]) / 4.0, 0, 1) * 0.85)[:, None]
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"] * (1 - rust) + RUST * rust)
        K.set_points(fum, sim["fp"][f], scale=sim["fs"][f], rot=np.zeros((NF, 3)), col=np.ones((NF, 3)))
        K.set_points(snow, sim["sp"][f], scale=sim["ss"][f], rot=np.zeros((NS, 3)), col=np.ones((NS, 3)))

    ctx.on_frame(upd)
    ctx.anchor("tower", lambda t: (TOWER[0], TOWER[1], 380.0))
    ctx.anchor("lake", lambda t: (LAKE[0] + 10.0, LAKE[1] - 25.0, 1.0))
