"""EP08 만약 태양이 1초 동안 꺼진다면?

실제로 계산하는 것:
- 2026-10-27 행성 위치 (JPL 근사 궤도 요소) — 반지름은 평균 거리, 각도는 실제 황경
- 태양 표면이 1초 꺼진 '어둠의 껍질'이 빛의 속도로 퍼져 각 행성에 도착하는 시각
- 반전: 태양 중심에서 나오는 광자의 무작위 걸음(random walk)
"""
from engine.cuts import snap
import math

import numpy as np

from engine.astro import AU_LIGHT_S, ELEMENTS, helio, jd
from engine.common import FPS, Beat, clamp, frames_of, keyed, logkeyed, ramp, smooth

DUR = 56.0
META = {"id": "ep08", "title": "만약 태양이 1초 동안 꺼진다면?", "duration": DUR,
        "music": {"key": "D", "mode": "lydian", "bpm": 66, "seed": 8, "twist_at": 43.0}}
PLANETS = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
KOR = {"mercury": "수성", "venus": "금성", "earth": "지구", "mars": "화성", "jupiter": "목성", "saturn": "토성",
       "uranus": "천왕성", "neptune": "해왕성"}
RADIUS = {"mercury": 0.045, "venus": 0.07, "earth": 0.075, "mars": 0.055, "jupiter": 0.2, "saturn": 0.17,
          "uranus": 0.11, "neptune": 0.105}
COLOR = {"mercury": (0.55, 0.52, 0.5), "venus": (0.9, 0.78, 0.55), "mars": (0.85, 0.4, 0.22),
         "jupiter": (0.85, 0.72, 0.55), "saturn": (0.9, 0.82, 0.6), "uranus": (0.6, 0.85, 0.9),
         "neptune": (0.35, 0.5, 0.95), "earth": (0.3, 0.5, 0.9)}
SUN_R = 0.42
VOYAGER_AU = 173.3  # 2026-11 무렵 지구에서 1광일 ≈ 173 AU


def rvis(au):
    """로그 눈금 거리 (화면 단위)."""
    return SUN_R + 2.3 * np.log10(1 + np.asarray(au) / 0.11)


# 영상 시간 → 시뮬레이션 시간(초)
TIMELINE = [(0.0, 0.0), (1.0, 0.0), (2.6, 1.0), (4.0, 6.0), (8.0, 193.0), (11.5, 361.0), (14.5, 470.0),
            (16.2, 498.7), (17.8, 500.3), (21.5, 512.0), (26.5, 700.0), (29.0, 760.0), (31.5, 2597.0),
            (33.5, 4777.0), (35.3, 9563.0), (37.3, 15060.0), (40.5, 86400.0), (56.0, 90000.0)]


def T_at(t):
    if t <= 1.0:
        return 0.0
    return logkeyed(t, [(a, max(b, 1e-3)) for a, b in TIMELINE[1:]])


def fmt_T(T):
    T = max(0.0, T)
    h, rem = divmod(T, 3600)
    m, s = divmod(rem, 60)
    if T < 3600:
        return f"T+ {int(m):02d}분 {s:04.1f}초" if T < 60 else f"T+ {int(m):02d}분 {int(s):02d}초"
    return f"T+ {int(h)}시간 {int(m):02d}분"


BEATS = [
    Beat(0.0, 4.0, badge="T+0초", label="만약", big="태양이 1초 꺼진다면?", big_size=88,
         sub="가정: 태양 표면이 딱 1초 동안\n빛을 멈춘다면?"),
    Beat(4.0, 8.0, badge="T+1초", title="다시 켜졌다. 그런데…", note="두께 30만 km짜리 '어둠'이 날아간다",
         sub="꺼졌던 1초는 사라지지 않고\n빛의 속도로 우주에 퍼져 나갑니다."),
    Beat(8.0, 12.0, badge="3분 13초", title="{gray}수성{/} → {yellow}금성{/}", note="금성은 6분 1초 뒤",
         sub="태양에서 가까운 행성부터\n차례로 1초 동안 깜깜해집니다."),
    Beat(12.0, 16.2, badge="8분 19초", title="그동안 지구는?", note="아무것도 모른다",
         sub="빛보다 빠른 소식은 없으니까요.\n8분 19초 동안 지구는 평소와 같습니다."),
    Beat(16.2, 21.5, badge="8분 19초", title="낮이 1초 동안 {blue}밤{/}이 된다",
         sub="지구의 낮 쪽 전체가\n딱 1초 동안 어두워집니다."),
    Beat(21.5, 26.5, badge="8분 20초", title="태양광 발전 {yellow}2,391GW{/} 1초 정지",
         note="기온 변화는 약 0.00002℃ (계산)",
         sub="전 세계 태양광 발전이 잠깐 멈추지만\n지구는 거의 아무 변화도 없습니다."),
    Beat(26.5, 31.5, badge="12분 40초", title="{orange}화성{/} → {orange}목성{/}", note="목성은 43분 17초 뒤",
         sub="멀리 있을수록\n더 늦게 어둠을 맞습니다."),
    Beat(31.5, 37.3, badge="4시간 11분", title="태양계 끝 {blue}해왕성{/}", note="토성 1시간 19분 · 천왕성 2시간 39분",
         sub="1초의 어둠은 4시간 넘게 날아가\n해왕성에 닿습니다."),
    Beat(37.3, 43.0, badge="약 1일", title="{cyan}보이저 1호{/}", note="2026년 11월, 지구에서 '빛으로 하루' 거리",
         sub="인류가 가장 멀리 보낸 탐사선은\n하루 뒤에야 그 1초를 만납니다."),
    Beat(43.0, 48.5, badge="반전", title="진짜 태양 빛은 {orange}17만 년{/} 늦다",
         sub="태양 중심에서 만든 에너지가 표면까지\n나오는 데 약 17만 년이 걸립니다(NASA)."),
    Beat(48.5, 52.5, badge="반전", title="진짜 태양 빛은 {orange}17만 년{/} 늦다", note="1초 멈춤을 아는 건 중성미자 검출기뿐",
         sub="그래서 태양 중심이 1초 멈춰도\n햇빛은 수만 년 동안 그대로입니다."),
    Beat(52.5, 56.0, badge="지금", title="오늘 당신을 비춘 햇빛은\n약 {orange}17만 년 전{/}에 출발했습니다", title_size=66),
]
GRADE = {"exposure": 1.0, "bloom": 0.28, "bloom_thr": 1.2, "bloom_radius": 1.2, "vignette": 0.3, "stars": 3200,
         "star_gain": 1.25}

# 카메라: (t, 목표, 방위, 고도, 거리, 렌즈)
CAM_KEYS = [
    (0.0, (0.0, 0.0, 0.0), -20, 22, 4.2, 30),
    (3.5, (0.4, 0.4, 0.0), -10, 30, 6.0, 30),
    (8.0, (0.8, 0.8, 0.0), 10, 40, 7.5, 30),
    (12.0, "earth", 120, 20, 1.7, 34),
    (15.8, "earth", 140, 10, 0.64, 40),
    (21.5, "earth", 152, 10, 0.62, 40),
    (25.0, "earth", 165, 26, 2.4, 34),
    (27.5, (0.5, 0.5, 0.0), 120, 50, 11.0, 28),
    (31.5, (0.0, 0.0, 0.0), 130, 56, 15.5, 26),
    (37.0, (0.0, 0.0, 0.0), 150, 60, 17.5, 26),
    (40.5, (0.0, 0.0, 0.0), 170, 64, 22.0, 26),
    (43.0, (0.0, 0.0, 0.0), 185, 20, 2.6, 32),
    (48.5, (0.0, 0.0, 0.0), 200, 16, 1.9, 34),
    (52.5, (0.0, 0.0, 0.0), 215, 25, 3.2, 32),
    (56.0, (0.0, 0.0, 0.0), 230, 40, 9.0, 28),
]


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def simulate(build_dir):
    from engine.tex import planet_textures
    planet_textures(build_dir)
    rs = np.random.default_rng(8)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    T = np.array([T_at(t) for t in ts])
    when = jd(2026, 10, 27)
    pos = {}
    arrive = {}
    for p in PLANETS:
        v = helio(p, when)
        ang = math.atan2(v[1], v[0])
        a = ELEMENTS[p][0][0]
        r = float(rvis(a))
        pos[p] = np.array([r * math.cos(ang), r * math.sin(ang), 0.0], np.float32)
        arrive[p] = a * AU_LIGHT_S
    vang = math.radians(255.0)
    vr = float(rvis(VOYAGER_AU))
    voyager = np.array([vr * math.cos(vang), vr * math.sin(vang), 0.9], np.float32)
    # 행성별 밝기: 어둠의 껍질이 지나가는 1초 + 화면에서 보이도록 최소 0.45초 유지
    lit = np.ones((nf, len(PLANETS)), np.float32)
    for k, p in enumerate(PLANETS):
        a0 = arrive[p]
        inside = (T >= a0) & (T < a0 + 1.0)
        idx = np.where(T >= a0)[0]
        if len(idx):
            f0 = idx[0]
            inside[f0:f0 + int(0.45 * FPS)] = True
        lit[:, k] = np.where(inside, 0.0, 1.0)
        # 부드럽게
        lit[:, k] = np.convolve(np.pad(lit[:, k], 2, mode="edge"), np.ones(5) / 5, mode="valid")
    sun_on = np.where((ts >= 1.0) & (ts < 2.6), 0.0, 1.0).astype(np.float32)
    sun_on = np.convolve(np.pad(sun_on, 3, mode="edge"), np.ones(7) / 7, mode="valid")
    # 어둠의 껍질 (화면 반지름): 앞쪽 = c·T, 뒤쪽 = c·(T-1)
    front = rvis(np.maximum(T, 0) / AU_LIGHT_S)
    back = rvis(np.maximum(T - 1.0, 0) / AU_LIGHT_S)
    show = (T > 0).astype(np.float32)
    # 빛 입자: 태양에서 계속 나가는 광자 (꺼진 1초 동안 나간 것은 없음)
    NPH = 2000
    ph_ang = rs.uniform(0, 2 * np.pi, NPH)
    ph_u = rs.random(NPH)          # 화면 반지름 위치 (0..1)
    ph_z = rs.normal(0, 0.05, NPH)
    rmax = float(rvis(VOYAGER_AU)) * 1.08
    ph = np.zeros((nf, NPH, 3), np.float32)
    ph_s = np.zeros((nf, NPH), np.float32)
    for i in range(nf):
        u = (ph_u + ts[i] * 0.045) % 1.0
        r = SUN_R + 0.02 + u * (rmax - SUN_R)
        ph[i, :, 0] = r * np.cos(ph_ang)
        ph[i, :, 1] = r * np.sin(ph_ang)
        ph[i, :, 2] = ph_z * (r / rmax)
        dark = (r <= front[i] + 0.03) & (r >= back[i] - 0.03) & (show[i] > 0)
        ph_s[i] = np.where(dark, 0.0, 1.0) * (0.55 + 0.45 * (1 - u))
    # 반전: 광자 무작위 걸음 (태양 내부)
    NW = 1400
    walk = np.zeros((NW, 3), np.float32)
    p = np.zeros(3)
    step = 0.0105
    for k in range(NW):
        d = rs.normal(size=3)
        d /= np.linalg.norm(d)
        q = p + d * step
        if np.linalg.norm(q) < SUN_R * 0.98:
            p = q
        walk[k] = p
    walk_n = np.clip((ts - 43.4) / 8.0, 0, 1) * NW
    return dict(T=T, lit=lit, sun_on=sun_on, front=front, back=back, show=show, ph=ph, ph_s=ph_s,
                walk=walk, walk_n=walk_n, voyager=voyager, **{f"pos_{p}": pos[p] for p in PLANETS},
                arrive=np.array([arrive[p] for p in PLANETS]))


def hud(t, sim):
    f = fi(t)
    return {"left": "SIMULATION", "right": fmt_T(float(sim["T"][f])), "right2": "빛의 속도 299,792 km/s"}


def labels(t, anchors, sim):
    out = []
    f = fi(t)
    T = float(sim["T"][f])
    if 3.0 < t < 41.0:
        for k, p in enumerate(PLANETS):
            a = anchors.get(p)
            if not a or not a[3]:
                continue
            if p == "earth" and 12.5 < t < 25.5:
                continue
            dark = sim["lit"][f][k] < 0.5
            out.append({"x": a[0], "y": a[1], "text": KOR[p], "color": "gray" if dark else "white", "size": 24,
                        "alpha": 0.9, "lift": 14})
    if 37.3 < t < 43.0:
        a = anchors.get("voyager")
        if a and a[3]:
            out.append({"x": a[0], "y": a[1], "text": "보이저 1호", "color": "cyan", "size": 26, "lift": 12})
    return out


def build(ctx):
    import bpy
    from engine import bkit as K
    sim = ctx.sim
    K.world_space(ctx, ambient=(0.2, 0.22, 0.3), ambient_strength=0.05)
    # 태양
    sm, nt, out = K.new_mat("m_sun")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 9.0
    noise.inputs["Detail"].default_value = 6.0
    col = K.mix_rgb(nt, noise.outputs["Fac"], (1.0, 0.55, 0.12), (1.0, 0.85, 0.45))
    em = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, col, em.inputs["Color"])
    on = ctx.ctl_node(nt, "sun_on", 1.0)
    K.ln(nt, K.math_node(nt, "MULTIPLY_ADD", on, 6.0, 0.05), em.inputs["Strength"])
    # 반전 때 반투명 (내부 보이기)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    K.ln(nt, ctx.ctl_node(nt, "sun_clear", 0.0), mx.inputs[0])
    K.ln(nt, em.outputs[0], mx.inputs[1])
    em2 = nt.nodes.new("ShaderNodeEmission")
    em2.inputs["Color"].default_value = (1.0, 0.45, 0.1, 1)
    em2.inputs["Strength"].default_value = 0.1
    add = nt.nodes.new("ShaderNodeAddShader")
    K.ln(nt, tr.outputs[0], add.inputs[0])
    K.ln(nt, em2.outputs[0], add.inputs[1])
    K.ln(nt, add.outputs[0], mx.inputs[2])
    K.ln(nt, mx.outputs[0], out.inputs["Surface"])
    sm.cycles.emission_sampling = "NONE"
    K.mesh_obj("sun", K.bm_sphere(SUN_R, seg=48, rings=24), sm, smooth=True)
    core = K.mesh_obj("core", K.bm_sphere(SUN_R * 0.22, seg=24, rings=12),
                      K.mat_emit("m_core", (1.0, 0.85, 0.6), 2.5, ctx, "core_on"), smooth=True)
    # 행성 (가짜 조명: 태양 방향 셰이더)
    planets = {}
    orb_mat = K.mat_emit("m_orb", (0.35, 0.5, 0.9), 0.4, ctx, "orbits")
    for k, p in enumerate(PLANETS):
        pm, nt, out = K.new_mat("m_" + p)
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        vm = nt.nodes.new("ShaderNodeVectorMath")
        vm.operation = "NORMALIZE"
        K.ln(nt, geo.outputs["Position"], vm.inputs[0])
        dot = nt.nodes.new("ShaderNodeVectorMath")
        dot.operation = "DOT_PRODUCT"
        K.ln(nt, geo.outputs["Normal"], dot.inputs[0])
        K.ln(nt, vm.outputs[0], dot.inputs[1])
        shade = K.math_node(nt, "MAXIMUM", K.math_node(nt, "MULTIPLY", dot.outputs["Value"], -1.0), 0.0)
        shade = K.math_node(nt, "MULTIPLY", shade, ctx.ctl_node(nt, "lit_" + p, 1.0))
        if p == "earth":
            uv = nt.nodes.new("ShaderNodeTexCoord").outputs["UV"]
            day = nt.nodes.new("ShaderNodeTexImage")
            day.image = K.load_image(ctx.build_dir / "earth_day.png")
            K.ln(nt, uv, day.inputs["Vector"])
            night = nt.nodes.new("ShaderNodeTexImage")
            night.image = K.load_image(ctx.build_dir / "earth_night.png")
            K.ln(nt, uv, night.inputs["Vector"])
            dayc = K.mix_rgb(nt, 1.0, day.outputs["Color"], shade, "MULTIPLY")
            nightf = K.math_node(nt, "POWER", K.math_node(nt, "SUBTRACT", 1.0,
                                                          K.math_node(nt, "MULTIPLY", shade, 3.0, clamp=True)), 2.0)
            nc = K.mix_rgb(nt, 1.0, night.outputs["Color"], nightf, "MULTIPLY")
            c = K.mix_rgb(nt, 1.0, dayc, nc, "ADD")
            strength = 2.4
        else:
            c = K.mix_rgb(nt, shade, (0.01, 0.01, 0.012), COLOR[p])
            strength = 1.6
        em = nt.nodes.new("ShaderNodeEmission")
        K.ln(nt, c, em.inputs["Color"])
        em.inputs["Strength"].default_value = strength
        K.ln(nt, em.outputs[0], out.inputs["Surface"])
        pm.cycles.emission_sampling = "NONE"
        bm = K.bm_sphere(RADIUS[p], seg=64 if p == "earth" else 24, rings=32 if p == "earth" else 12, uv=True)
        ob = K.mesh_obj(p, bm, pm, smooth=True)
        ob.location = tuple(sim["pos_" + p])
        if p == "earth":
            ob.rotation_euler = (math.radians(23.4), 0, 0)
        planets[p] = ob
        # 궤도선
        ring = bpy.data.curves.new("orb_" + p, "CURVE")
        ring.dimensions = "3D"
        ring.bevel_depth = 0.002
        spl = ring.splines.new("POLY")
        r = float(np.linalg.norm(sim["pos_" + p]))
        spl.points.add(127)
        for i in range(128):
            a = 2 * math.pi * i / 127
            spl.points[i].co = (r * math.cos(a), r * math.sin(a), 0, 1)
        ro = K.link(bpy.data.objects.new("orb_" + p, ring))
        ro.data.materials.append(orb_mat)
    # 토성 고리
    sat = planets["saturn"]
    bm = K.bmesh.new()
    inner, outer = [], []
    for i in range(64):
        a = 2 * math.pi * i / 64
        inner.append(bm.verts.new((math.cos(a) * RADIUS["saturn"] * 1.3, math.sin(a) * RADIUS["saturn"] * 1.3, 0)))
        outer.append(bm.verts.new((math.cos(a) * RADIUS["saturn"] * 2.2, math.sin(a) * RADIUS["saturn"] * 2.2, 0)))
    for i in range(64):
        j = (i + 1) % 64
        bm.faces.new((inner[i], inner[j], outer[j], outer[i]))
    rm = K.mesh_obj("sat_ring", bm, K.mat_emit("m_ring", (0.85, 0.75, 0.55), 0.8))
    rm.location = sat.location
    rm.rotation_euler = (math.radians(75), 0, math.radians(20))
    # 광자 입자
    pp = K.proto(ctx, "p_photon", K.bm_ico(0.0045, sub=0), [K.mat_emit("m_photon", (1.0, 0.85, 0.55), 3.0)])
    pho = K.instancer(ctx, "photons", pp, sim["ph"].shape[1])
    # 어둠 껍질 가장자리 (얇은 고리 2개)
    rings = []
    for nm, colr in (("front", (0.55, 0.75, 1.0)), ("back", (1.0, 0.7, 0.4))):
        cu = bpy.data.curves.new("ring_" + nm, "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = 0.0035
        spl = cu.splines.new("POLY")
        spl.points.add(255)
        for i in range(256):
            a = 2 * math.pi * i / 255
            spl.points[i].co = (math.cos(a), math.sin(a), 0, 1)
        ob = K.link(bpy.data.objects.new("ring_" + nm, cu))
        ob.data.materials.append(K.mat_emit("m_ring_" + nm, colr, 3.0, ctx, "ring_" + nm))
        rings.append(ob)
    # 보이저 1호 (작은 별처럼)
    vo = K.mesh_obj("voyager", K.bm_ico(0.05, tuple(sim["voyager"]), sub=1),
                    K.mat_emit("m_voy", (0.6, 0.95, 1.0), 8.0, ctx, "voy"))
    # 광자 무작위 걸음 자국
    wp = K.proto(ctx, "p_walk", K.bm_ico(0.0055, sub=0), [K.mat_emit("m_walk", (1.0, 0.95, 0.75), 6.0)])
    wo = K.instancer(ctx, "walk", wp, len(sim["walk"]))
    cam = K.CamRig(ctx, 30, fstop=0)
    earth = planets["earth"]
    walk = sim["walk"]

    def cam_at(t):
        ks = []
        for k in CAM_KEYS:
            tgt = tuple(sim["pos_earth"]) if k[1] == "earth" else k[1]
            ks.append((k[0], (*tgt, k[2], k[3], k[4], k[5])))
        return keyed(t, snap(ks))

    def upd(t, f):
        v = cam_at(t)
        cam.set(v[:3], v[3], v[4], v[5], v[6])
        ctx.set_ctl("sun_on", float(sim["sun_on"][f]))
        clear = ramp(t, 43.2, 44.6) * (1 - ramp(t, 52.8, 54.5))
        ctx.set_ctl("sun_clear", clear)
        ctx.set_ctl("core_on", 0.3 + clear)
        for k, p in enumerate(PLANETS):
            ctx.set_ctl("lit_" + p, float(sim["lit"][f][k]))
        earth.rotation_euler[2] = t * 0.08
        ctx.set_ctl("orbits", 1.0 - 0.75 * ramp(t, 12.0, 14.0) * (1 - ramp(t, 24.0, 26.0)))
        sh = float(sim["show"][f])
        fr, bk = float(sim["front"][f]), float(sim["back"][f])
        bk = min(bk, fr - 0.05)
        rings[0].scale = (fr, fr, 1)
        rings[1].scale = (max(bk, 0.01), max(bk, 0.01), 1)
        vis = sh * (1 - ramp(t, 41.5, 43.0))
        ctx.set_ctl("ring_front", 1.6 * vis)
        ctx.set_ctl("ring_back", 0.9 * vis)
        ctx.set_ctl("voy", 8.0 * (1 - ramp(t, 42.5, 43.5)) * (0.6 + 0.4 * math.sin(t * 5)))
        n = pho.data.vertices.__len__()
        phs = sim["ph_s"][f] * (1 - clear)
        K.set_points(pho, sim["ph"][f], scale=phs, rot=np.zeros((n, 3)), col=np.ones((n, 3)))
        wn = int(sim["walk_n"][f])
        ws = np.zeros(len(walk), np.float32)
        ws[:wn] = 1.0
        if wn:
            ws[max(0, wn - 6):wn] = 2.2
        K.set_points(wo, walk, scale=ws * clear, rot=np.zeros((len(walk), 3)), col=np.ones((len(walk), 3)))

    ctx.on_frame(upd)
    for p in PLANETS:
        ctx.anchor(p, (lambda p: lambda t: tuple(float(x) for x in sim["pos_" + p] + np.array([0, 0, RADIUS[p] + 0.02])))(p))
    ctx.anchor("voyager", lambda t: tuple(float(x) for x in sim["voyager"]))
