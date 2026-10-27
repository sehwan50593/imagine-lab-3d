"""EP05 만약 남한과 북한이 전쟁을 한다면? (가상 시나리오, 남측 선제공격으로 시작)

실제로 계산하는 것:
- NOAA ETOPO1 한반도 지형 + Natural Earth 군사분계선(남북 공유 경계) + 도시 인구로 만든 야경
- 미사일·포탄: 발사 시각·탄도(포물선)·착탄 → 섬광·화재 누적 (발사 수는 시간대별 확률)
- 전력망: 착탄이 쌓일수록 도시 불빛이 꺼짐 / 피란 흐름: 수도권에서 남쪽 도시로 이동하는 입자
숫자는 모두 공개 자료(2022 국방백서, RAND 2020, 미 의회조사국 2017, TrendForce 2026, PRIO, 국립생태원).
"""
import json
import math

import numpy as np

from engine.common import ASSETS, FPS, Beat, clamp, frames_of, keyed, ramp

DUR = 56.0
META = {"id": "ep05", "title": "만약 남한과 북한이 전쟁을 한다면?", "duration": DUR,
        "music": {"key": "C", "mode": "major", "bpm": 64, "seed": 25, "twist_at": 44.0}}
S = 1.6
EXAG = 0.00032
LAT0, LON0 = 38.0, 127.5
BOX = (33.0, 43.2, 124.0, 131.0)  # 위도, 경도 범위
NSHELL, NIMP, NFIRE, NREF, NLIFE = 220, 260, 420, 420, 320

BEATS = [
    Beat(0.0, 4.5, badge="가상 시나리오", title="남북 전쟁이 일어난다면?", note="한국군 50만 · 북한군 128만 (2022 국방백서)",
         sub="남측의 선제공격(북침)으로\n전쟁이 시작된다면?"),
    Beat(4.5, 10.0, badge="D-DAY 04:00", title="{blue}선제 타격{/}",
         sub="미사일이 휴전선 북쪽의\n장사정포 진지를 먼저 노립니다."),
    Beat(10.0, 16.0, badge="04:05", title="{red}장사정포{/} 반격", note="야포 8,800문 · 방사포 5,500문 (2022 국방백서)",
         sub="살아남은 포가 휴전선 너머\n서울을 향해 일제히 불을 뿜습니다."),
    Beat(16.0, 22.0, badge="05:00", title="서울까지 약 50km", big="사상자 최대 20.6만", big_size=96, big_color="red",
         note="장사정포 1시간 사격 시나리오 (RAND, 2020)",
         sub="수도권 2,608만 명, 인구의 절반 이상이\n포의 사거리 안에 삽니다."),
    Beat(22.0, 28.0, badge="D+3", title="첫 며칠 사망 {red}3만~30만{/}", note="재래식 무기만 썼을 때 추정 (미 의회조사국, 2017)",
         sub="불이 꺼진 도시에서 사람들은\n남쪽으로 피란길에 오릅니다."),
    Beat(28.0, 34.0, badge="D+7", title="세계가 멈춘다", big="D램 64%", big_size=104, big_color="orange",
         note="삼성·SK하이닉스 세계 점유율 (TrendForce, 2026)",
         sub="스마트폰과 서버에 들어가는 메모리의\n절반 이상을 만드는 곳이 멈춥니다."),
    Beat(34.0, 39.5, badge="1950년의 기억", title="한국전쟁 사망자", big="약 300만 명", big_size=104,
         note="추정 범위 150만~450만 (PRIO)",
         sub="70여 년 전, 같은 땅에서\n이미 일어났던 일입니다."),
    Beat(39.5, 44.0, badge="결과", title="시뮬레이션 결과: {red}승자 없음{/}",
         sub="어느 쪽이 이겨도\n피해는 한반도 전체에 남습니다."),
    Beat(44.0, 52.0, badge="반전", title="전쟁이 멈춘 땅의 {green}기적{/}",
         note="DMZ 일원 약 6,900종 · 국내 멸종위기종의 38% 이상",
         sub="70년 넘게 사람이 들어가지 못한 DMZ는\n야생동물의 마지막 피난처가 됐습니다."),
    Beat(52.0, 56.0, badge="정전 73년째", title="이 시뮬레이션은\n{green}영원히 돌리지 않기를{/}", title_size=72),
]
GRADE = {"exposure": 1.05, "bloom": 0.34, "bloom_thr": 0.85, "bloom_radius": 1.2, "vignette": 0.34}


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def to_xy(lat, lon):
    return np.array([(lon - LON0) * math.cos(math.radians(LAT0)) * S, (lat - LAT0) * S], np.float32)


def dmz_line():
    kor = json.load(open(ASSETS / "geo" / "korea_outline.json"))
    k = max((p[0] for p in kor["KOR"]), key=len)
    n = np.array(max((p[0] for p in kor["PRK"]), key=len))
    pts = []
    for x, y in k:
        if y > 37.5 and np.min(np.hypot(n[:, 0] - x, n[:, 1] - y)) < 0.01:
            pts.append((x, y))
    pts = np.array(sorted(set(pts)))
    order = np.argsort(pts[:, 0])
    return pts[order]


def arc_pos(p0, p1, u, h):
    p = p0 + (p1 - p0) * u[:, None]
    z = h * 4 * u * (1 - u)
    return np.c_[p, z]


def simulate(build_dir):
    import cv2
    from engine.common import imwrite
    from engine.tex import eastasia
    rs = np.random.default_rng(55)
    full, lat_top, lon_left, cell = eastasia()
    r0, r1 = int((lat_top - BOX[1]) / cell), int((lat_top - BOX[0]) / cell)
    c0, c1 = int((BOX[2] - lon_left) / cell), int((BOX[3] - lon_left) / cell)
    e = cv2.GaussianBlur(full, (0, 0), 0.8)[r0:r1 + 1, c0:c1 + 1]
    lats = lat_top - np.arange(r0, r1 + 1) * cell
    lons = lon_left + np.arange(c0, c1 + 1) * cell
    LON, LAT = np.meshgrid(lons, lats)
    X = (LON - LON0) * math.cos(math.radians(LAT0)) * S
    Y = (LAT - LAT0) * S
    Z = np.maximum(e, -300.0) * EXAG

    def hz(xy):
        """지형 높이(가장 가까운 격자) — 선·입자를 땅 위에 얹기."""
        xy = np.asarray(xy, np.float32)
        lat = LAT0 + xy[..., 1] / S
        lon = LON0 + xy[..., 0] / (S * math.cos(math.radians(LAT0)))
        r = np.clip(np.round((lats[0] - lat) / cell), 0, len(lats) - 1).astype(int)
        c = np.clip(np.round((lon - lons[0]) / cell), 0, len(lons) - 1).astype(int)
        return np.maximum(Z[r, c], 0.0)

    # 야경 텍스처 (R=남, G=북, B=주변국)
    cities = json.load(open(ASSETS / "geo" / "cities.json", encoding="utf-8"))
    T = 1024
    lt = np.zeros((T, T, 3), np.float32)
    x0, x1, y0, y1 = float(X.min()), float(X.max()), float(Y.min()), float(Y.max())
    for c in cities:
        if not (BOX[0] <= c["lat"] <= BOX[1] and BOX[2] <= c["lon"] <= BOX[3]):
            continue
        xy = to_xy(c["lat"], c["lon"])
        u = int((xy[0] - x0) / (x1 - x0) * (T - 1))
        v = int((y1 - xy[1]) / (y1 - y0) * (T - 1))
        ch = 0 if c["cc"] == "KOR" else (1 if c["cc"] == "PRK" else 2)
        w = (max(c["pop"], 2e4) / 1e6) ** 0.55
        if ch == 1:
            w *= 1.0 if c["name"].lower().startswith("pyongyang") else 0.18
        lt[v, u, ch] += w
    lt = cv2.GaussianBlur(lt, (0, 0), 2.2) * 14 + cv2.GaussianBlur(lt, (0, 0), 9.0) * 10
    imwrite(build_dir / "lights.png", (np.clip(lt[..., ::-1], 0, 1) * 255).astype(np.uint8))

    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    dmz = dmz_line()
    dmz_xy = np.array([to_xy(la, lo) for lo, la in dmz])
    seoul = to_xy(37.5665, 126.978)
    # 발사 사건: (발사 시각, 출발, 도착, 높이, 색 0=청 1=적)
    events = []
    for _ in range(46):  # 선제 타격: 남→북 (진지)
        t0 = rs.uniform(4.8, 9.6)
        st = to_xy(rs.uniform(36.9, 37.3), rs.uniform(126.9, 127.6))
        en = to_xy(rs.uniform(38.15, 38.6), rs.uniform(126.3, 127.6))
        events.append((t0, st, en, rs.uniform(0.8, 1.2), 0, 1.3))
    for _ in range(330):  # 장사정포: 휴전선 북쪽 → 수도권
        t0 = 10.0 + rs.gamma(2.0, 2.2)
        if t0 > 22.0:
            continue
        st = to_xy(rs.uniform(38.0, 38.45), rs.uniform(126.3, 127.5))
        en = seoul + rs.normal(0, 0.28, 2) * np.array([1.4, 1.0])
        events.append((t0, st, en, rs.uniform(0.35, 0.6), 1, 1.0))
    events.sort(key=lambda e: e[0])
    events = [(t0, st, en, h, c, d, float(hz(st)), float(hz(en))) for t0, st, en, h, c, d in events]
    sh_p = np.zeros((nf, NSHELL, 3), np.float32)
    sh_s = np.zeros((nf, NSHELL), np.float32)
    sh_c = np.zeros((nf, NSHELL), np.float32)
    im_p = np.zeros((nf, NIMP, 3), np.float32)
    im_s = np.zeros((nf, NIMP), np.float32)
    fires = []
    for i, t in enumerate(ts):
        k = 0
        m = 0
        for t0, st, en, h, colr, dur, z0, z1 in events:
            u = (t - t0) / dur
            if 0 <= u < 1 and k < NSHELL:
                p = arc_pos(st, en, np.array([u]), h)[0]
                p[2] += z0 + (z1 - z0) * u
                sh_p[i, k] = p
                sh_s[i, k] = 1.0
                sh_c[i, k] = colr
                k += 1
            if 1 <= u < 1 + 0.7 / dur and m < NIMP:
                v = (u - 1) * dur / 0.7
                im_p[i, m] = (*en, z1 + 0.02)
                im_s[i, m] = (0.4 + 1.6 * v) * (1 - v) * (1.4 if colr == 0 else 1.0)
                m += 1
    for e_ in events:
        fires.append((e_[0] + e_[5], e_[2], e_[7]))
    fires = fires[:NFIRE]
    fr_p = np.zeros((NFIRE, 3), np.float32)
    fr_t = np.full(NFIRE, 1e9, np.float32)
    for j, (tt, en, zz) in enumerate(fires):
        fr_p[j] = (*(en + rs.normal(0, 0.03, 2)), zz + 0.012)
        fr_t[j] = tt
    fire_s = np.clip((ts[:, None] - fr_t[None]) / 0.4, 0, 1) * (1 - ramp_arr(ts, 40.0, 46.0)[:, None] * 0.85)
    # 도시 전력: 착탄 누적 비율에 따라 감소
    hit = np.array([sum(1 for e_ in events if e_[4] == 1 and e_[0] + e_[5] <= t) for t in ts], np.float32)
    hit /= max(hit.max(), 1)
    south_power = 1.0 - 0.62 * hit
    strike = np.array([sum(1 for e_ in events if e_[4] == 0 and e_[0] + e_[5] <= t) for t in ts], np.float32)
    north_power = 1.0 - 0.7 * strike / max(strike.max(), 1)
    # 피란 입자: 수도권 → 대전·대구·부산·광주
    dests = [to_xy(36.35, 127.38), to_xy(35.87, 128.6), to_xy(35.18, 129.08), to_xy(35.16, 126.85)]
    ref_start = seoul + rs.normal(0, 0.25, (NREF, 2))
    ref_dest = np.array(dests)[rs.integers(0, len(dests), NREF)] + rs.normal(0, 0.15, (NREF, 2))
    ref_t0 = rs.uniform(22.5, 33.0, NREF)
    ref_speed = rs.uniform(0.08, 0.14, NREF)
    ref_p = np.zeros((nf, NREF, 3), np.float32)
    ref_s = np.zeros((nf, NREF), np.float32)
    for i, t in enumerate(ts):
        u = np.clip((t - ref_t0) * ref_speed, 0, 1)
        p = ref_start + (ref_dest - ref_start) * u[:, None]
        ref_p[i, :, :2] = p
        ref_p[i, :, 2] = hz(p) + 0.025
        ref_s[i] = np.where((t > ref_t0) & (u < 1), 1.0, 0.0) * (1 - ramp_arr(np.array([t]), 38.0, 40.0)[0])
    # DMZ 생명(반딧불처럼): 군사분계선 양옆 2km
    li = rs.integers(0, len(dmz_xy) - 1, NLIFE)
    uu = rs.random(NLIFE)
    base = dmz_xy[li] + (dmz_xy[li + 1] - dmz_xy[li]) * uu[:, None]
    base = base + rs.normal(0, 0.035, (NLIFE, 2))
    life_t0 = rs.uniform(44.5, 50.0, NLIFE)
    life_z = hz(base)
    life_ph = rs.uniform(0, 6.28, NLIFE)
    life_p = np.zeros((nf, NLIFE, 3), np.float32)
    life_s = np.zeros((nf, NLIFE), np.float32)
    for i, t in enumerate(ts):
        life_p[i, :, :2] = base + 0.02 * np.stack([np.sin(t * 0.9 + life_ph), np.cos(t * 0.7 + life_ph)], 1)
        life_p[i, :, 2] = life_z + 0.03 + 0.03 * (0.5 + 0.5 * np.sin(t * 1.3 + life_ph))
        life_s[i] = np.clip((t - life_t0) / 0.8, 0, 1) * (0.6 + 0.4 * np.sin(t * 3 + life_ph * 2))
    dmz_z = hz(dmz_xy) + 0.045
    return dict(dmz_z=dmz_z.astype(np.float32), X=X.astype(np.float32), Y=Y.astype(np.float32), Z=Z.astype(np.float32), dmz=dmz_xy.astype(np.float32),
                sh_p=sh_p, sh_s=sh_s, sh_c=sh_c, im_p=im_p, im_s=im_s, fr_p=fr_p, fire_s=fire_s.astype(np.float32),
                south=south_power.astype(np.float32), north=north_power.astype(np.float32), ref_p=ref_p, ref_s=ref_s,
                life_p=life_p, life_s=life_s, bbox=np.array([x0, x1, y0, y1], np.float32))


def ramp_arr(ts, a, b):
    x = np.clip((np.asarray(ts) - a) / (b - a), 0, 1)
    return x * x * (3 - 2 * x)


CLOCK = [(0.0, 0.0), (4.5, 0.0), (9.6, 4.0), (10.3, 5.0), (15.6, 50.0), (16.4, 60.0), (21.4, 78.0),
         (22.5, 60 * 24 * 3), (27.5, 60 * 24 * 3 + 180), (28.5, 60 * 24 * 7), (56.0, 60 * 24 * 7)]


def hud(t, sim):
    if t >= 34.0:
        right = "1953.7.27 정전협정 → 73년째" if t >= 44.0 else ("1950~1953" if t < 39.5 else "시뮬레이션 종료")
        return {"left": "SIMULATION", "right": right, "right2": "가상 시나리오"}
    m = keyed(t, CLOCK)
    d, rem = divmod(int(m), 60 * 24)
    h, mi = divmod(rem, 60)
    h += 4
    d += h // 24
    h %= 24
    return {"left": "SIMULATION", "right": f"D+{d}  {h:02d}:{mi:02d}", "right2": "가상 시나리오"}


def labels(t, anchors, sim):
    out = []
    for key, nm, col, t0, t1 in (("seoul", "서울", "white", 1.0, 34.0), ("pyongyang", "평양", "white", 1.0, 34.0),
                                 ("busan", "부산", "white", 1.0, 34.0), ("dmz", "휴전선", "red", 1.0, 44.0),
                                 ("dmz2", "DMZ", "green", 45.0, 56.0), ("fab", "반도체 공장", "orange", 28.3, 34.0)):
        a = anchors.get(key)
        if a and a[3] and t0 <= t < t1:
            out.append({"x": a[0], "y": a[1], "text": nm, "color": col, "size": 26, "lift": 8,
                        "alpha": min(ramp(t, t0, t0 + 0.6), 1 - ramp(t, t1 - 0.5, t1))})
    return out


def build(ctx):
    import bpy
    from engine import bkit as K
    sim = ctx.sim
    K.world_space(ctx, ambient=(0.25, 0.3, 0.5), ambient_strength=0.08)
    moon = K.sun(ctx, 0.5, color=(0.6, 0.7, 1.0), rot=(50, 0, -140), angle=2.0)
    X, Y, Z = sim["X"], sim["Y"], sim["Z"]
    x0, x1, y0, y1 = [float(v) for v in sim["bbox"]]
    # 지형: 고도색(어둡게) + 야경 텍스처 발광
    m, nt, out = K.new_mat("m_kterrain")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    K.ln(nt, geo.outputs["Position"], sep.inputs[0])
    u = K.math_node(nt, "DIVIDE", K.math_node(nt, "SUBTRACT", sep.outputs["X"], x0), x1 - x0)
    v = K.math_node(nt, "DIVIDE", K.math_node(nt, "SUBTRACT", sep.outputs["Y"], y0), y1 - y0)
    uvn = nt.nodes.new("ShaderNodeCombineXYZ")
    K.ln(nt, u, uvn.inputs[0])
    K.ln(nt, v, uvn.inputs[1])
    li = nt.nodes.new("ShaderNodeTexImage")
    li.image = K.load_image(ctx.build_dir / "lights.png", True)
    li.extension = "EXTEND"
    K.ln(nt, uvn.outputs[0], li.inputs["Vector"])
    lsep = nt.nodes.new("ShaderNodeSeparateColor")
    K.ln(nt, li.outputs["Color"], lsep.inputs[0])
    glow = K.math_node(nt, "ADD", K.math_node(nt, "MULTIPLY", lsep.outputs["Red"], ctx.ctl_node(nt, "south", 1.0)),
                       K.math_node(nt, "MULTIPLY", lsep.outputs["Green"], ctx.ctl_node(nt, "north", 1.0)))
    glow = K.math_node(nt, "ADD", glow, K.math_node(nt, "MULTIPLY", lsep.outputs["Blue"], 0.55))
    meters = K.math_node(nt, "DIVIDE", sep.outputs["Z"], EXAG)
    ramp_ = nt.nodes.new("ShaderNodeValToRGB")
    K.ln(nt, K.math_node(nt, "DIVIDE", meters, 2000.0, clamp=True), ramp_.inputs[0])
    e = ramp_.color_ramp.elements
    e[0].position, e[0].color = 0.0, (0.10, 0.16, 0.10, 1)
    e[1].position, e[1].color = 1.0, (0.55, 0.55, 0.58, 1)
    mid = e.new(0.35)
    mid.color = (0.20, 0.22, 0.14, 1)
    day = ctx.ctl_node(nt, "daylight", 0.0)
    col = K.mix_rgb(nt, day, K.mix_rgb(nt, 0.55, ramp_.outputs["Color"], (0.05, 0.06, 0.1), "MULTIPLY"),
                    ramp_.outputs["Color"])
    b = K.principled(nt, col, 0.85, emit=(1.0, 0.72, 0.38), estr=K.math_node(nt, "MULTIPLY", glow, 4.5))
    K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    K.grid_mesh("terrain", X, Y, Z, m, skirt_z=-0.3)
    K.box_obj("sea", x0 - 0.01, x1 + 0.01, y0 - 0.01, y1 + 0.01, -0.3, 0.0, K.mat_water(color=(0.01, 0.03, 0.08)))
    K.box_obj("base", x0, x1, y0, y1, -0.55, -0.3, K.mat_earth_side())
    # 군사분계선
    dmz = sim["dmz"]
    cu = bpy.data.curves.new("dmz", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.012
    spl = cu.splines.new("POLY")
    spl.points.add(len(dmz) - 1)
    for i, (x, y) in enumerate(dmz):
        spl.points[i].co = (float(x), float(y), float(sim["dmz_z"][i]), 1)
    dob = K.link(bpy.data.objects.new("dmz", cu))
    dm, nt, out = K.new_mat("m_dmz")
    em = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, ctx.ctl_rgb(nt, "dmz_col", (1.0, 0.25, 0.2)), em.inputs["Color"])
    K.ln(nt, ctx.ctl_node(nt, "dmz_str", 3.0), em.inputs["Strength"])
    K.ln(nt, em.outputs[0], out.inputs["Surface"])
    dm.cycles.emission_sampling = "NONE"
    dob.data.materials.append(dm)
    # 포탄·섬광·화재·피란·생명
    shell_m, nt, out = K.new_mat("m_shell")
    em = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, K.mix_rgb(nt, K.inst_attr(nt, "kind", "Fac"), (0.45, 0.75, 1.0), (1.0, 0.45, 0.2)), em.inputs["Color"])
    em.inputs["Strength"].default_value = 14.0
    K.ln(nt, em.outputs[0], out.inputs["Surface"])
    shell_m.cycles.emission_sampling = "NONE"
    sho = K.instancer(ctx, "shells", K.proto(ctx, "p_shell", K.bm_ico(0.022, sub=1), [shell_m]), NSHELL)
    K.add_attr(sho, "kind")
    imo = K.instancer(ctx, "impacts", K.proto(ctx, "p_imp", K.bm_ico(0.05, sub=2),
                                               [K.mat_emit("m_imp", (1.0, 0.62, 0.3), 9.0)]), NIMP)
    fro = K.instancer(ctx, "fires", K.proto(ctx, "p_fire", K.bm_ico(0.018, sub=1),
                                             [K.mat_emit("m_fire", (1.0, 0.4, 0.12), 7.0, ctx, "fire")]), NFIRE)
    rfo = K.instancer(ctx, "refugees", K.proto(ctx, "p_ref", K.bm_ico(0.012, sub=0),
                                                [K.mat_emit("m_ref", (1.0, 0.95, 0.85), 5.0)]), NREF)
    lfo = K.instancer(ctx, "life", K.proto(ctx, "p_life", K.bm_ico(0.012, sub=1),
                                            [K.mat_emit("m_life", (0.45, 1.0, 0.5), 9.0)]), NLIFE)
    cam = K.CamRig(ctx, 30, fstop=0)
    seoul = tuple(float(v) for v in to_xy(37.5665, 126.978)) + (0.0,)
    dmzc = tuple(float(v) for v in to_xy(38.1, 127.1)) + (0.0,)
    center = tuple(float(v) for v in to_xy(37.6, 127.6)) + (0.0,)
    CAM = [(0.0, center, -90, 62, 23.0, 30), (4.5, dmzc, -95, 50, 15.0, 30), (10.0, dmzc, -100, 42, 11.0, 32),
           (16.0, seoul, -110, 46, 9.0, 32), (21.5, seoul, -115, 50, 10.5, 32), (22.5, center, -100, 60, 21.0, 30),
           (28.0, center, -95, 64, 24.0, 30), (34.0, center, -90, 66, 25.0, 30), (39.5, center, -85, 66, 25.0, 30),
           (44.0, dmzc, -90, 48, 12.5, 32), (51.5, dmzc, -80, 44, 11.0, 32), (56.0, center, -75, 58, 22.0, 30)]
    fp = sim["fr_p"]
    nfz = np.zeros((NFIRE, 3), np.float32)

    def upd(t, f):
        v = keyed(t, [(k[0], (*k[1], *k[2:])) for k in CAM])
        cam.set(v[:3], v[3], v[4], v[5], v[6], shift=0.05)
        ctx.set_ctl("south", float(sim["south"][f]))
        ctx.set_ctl("north", float(sim["north"][f]))
        day = ramp(t, 43.0, 47.0) * 0.7
        ctx.set_ctl("daylight", day)
        moon.data.energy = 0.5 + 2.4 * day
        moon.data.color = (0.6 + 0.4 * day, 0.7 + 0.2 * day, 1.0 - 0.2 * day)
        ctx.set_ctl("ambient", 0.08 + 0.25 * day)
        g = ramp(t, 44.0, 46.0)
        ctx.set_rgb("dmz_col", (1.0 - 0.6 * g, 0.25 + 0.75 * g, 0.2 + 0.25 * g))
        ctx.set_ctl("dmz_str", 3.0 + 2.0 * g)
        ctx.set_ctl("fire", 1.0 - 0.8 * ramp(t, 40.0, 46.0))
        K.set_points(sho, sim["sh_p"][f], scale=sim["sh_s"][f], rot=np.zeros((NSHELL, 3)), col=np.ones((NSHELL, 3)),
                     kind=sim["sh_c"][f])
        K.set_points(imo, sim["im_p"][f], scale=sim["im_s"][f], rot=np.zeros((NIMP, 3)), col=np.ones((NIMP, 3)))
        K.set_points(fro, fp, scale=sim["fire_s"][f], rot=nfz, col=np.ones((NFIRE, 3)))
        K.set_points(rfo, sim["ref_p"][f], scale=sim["ref_s"][f], rot=np.zeros((NREF, 3)), col=np.ones((NREF, 3)))
        K.set_points(lfo, sim["life_p"][f], scale=sim["life_s"][f], rot=np.zeros((NLIFE, 3)), col=np.ones((NLIFE, 3)))

    ctx.on_frame(upd)
    pos = {"seoul": (37.5665, 126.978), "pyongyang": (39.0392, 125.7625), "busan": (35.1796, 129.0756),
           "dmz": (38.25, 127.6), "dmz2": (38.3, 127.9), "fab": (37.05, 127.1)}
    for k, (la, lo) in pos.items():
        xy = to_xy(la, lo)
        ctx.anchor(k, (lambda xy: lambda t: (float(xy[0]), float(xy[1]), 0.25))(xy))
