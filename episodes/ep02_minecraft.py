"""EP02 만약 이 세상이 마인크래프트 세상이라면?

실제로 계산하는 것 (minecraft.wiki 규칙):
- 복셀화: 매끈한 섬을 1m 블록 격자로 바꾸는 파동 (높이맵 → 기둥별 블록)
- 하루 20분(현실 1일 = 72일) 낮밤 순환
- 중력: 모래만 떨어지고, 밑동을 캔 나무의 잎은 공중에 남음
- 무한 물: 원천 2개 사이에 새 원천이 생기는 물 흐름 세포 자동자
- 반전: 영상 자체가 픽셀(네모 블록) 2,073,600개임을 보여주는 모자이크
"""
from engine.cuts import snap
import math

import numpy as np

from engine.common import FPS, Beat, clamp, frames_of, keyed, ramp

DUR = 56.0
META = {"id": "ep02", "title": "만약 이 세상이 마인크래프트 세상이라면?", "duration": DUR,
        "music": {"key": "C", "mode": "major", "bpm": 74, "seed": 2, "twist_at": 44.0}}
N = 46          # 섬 지름(블록)
B = 0.5         # 블록 한 칸 크기(화면 단위)
R_ISL = 21.5
WAVE_T0, WAVE_V = 4.3, 8.0
NPPL = 10

BEATS = [
    Beat(0.0, 4.2, badge="D-DAY", label="만약", title="세상이 {green}마인크래프트{/}가 된다면?", title_size=74,
         note="3억 5천만 장 넘게 팔린 게임 (기네스, 2025)",
         sub="어느 날 아침, 세상 모든 것이\n1m짜리 블록으로 바뀐다면?"),
    Beat(4.2, 9.0, badge="D-DAY", title="모든 것이 {yellow}1m 블록{/}", note="블록 1개 = 1m × 1m × 1m",
         sub="땅도, 나무도, 집도\n네모난 블록으로 쪼개집니다."),
    Beat(9.0, 14.0, badge="+1일", title="하루가 {orange}20분{/}", note="현실의 하루 = 마크 세상 72일",
         sub="해와 달이 20분마다 한 바퀴.\n하루에 해가 72번 뜹니다."),
    Beat(14.0, 20.0, badge="+3일", title="나무가 {green}공중에 뜬다{/}", note="중력을 받는 블록은 모래·자갈 등 일부뿐",
         sub="나무 밑동을 다 캐도\n나뭇잎은 그대로 떠 있습니다."),
    Beat(20.0, 26.0, badge="+1주", title="물 {cyan}2칸{/} = 무한한 물",
         sub="물 원천 두 개 사이에 새 원천이 생겨\n물을 퍼내도 끝없이 채워집니다."),
    Beat(26.0, 32.0, badge="+1개월", title="하늘에 {cyan}천장{/}이 생긴다", note="땅속 −64층부터 하늘 320층까지, 384층",
         sub="320층보다 높은 곳에는\n블록을 놓을 수 없습니다."),
    Beat(32.0, 38.0, badge="+1년", title="세상의 넓이", big="지구 × 7", big_size=110,
         note="자바판 월드 6,000만 × 6,000만 블록 (계산 7.06배)",
         sub="마크 세상은 지구 표면보다\n약 7배 넓습니다."),
    Beat(38.0, 44.0, badge="+1년", title="세상 끝까지 걸으면?", big="약 80일", big_size=110,
         note="걷기 초속 4.317m, 한 번도 쉬지 않을 때 (계산)",
         sub="세상 끝 '월드 보더'까지\n쉬지 않고 걸어도 80일이 걸립니다."),
    Beat(44.0, 52.0, badge="반전", title="지금 이 화면도 {green}블록{/}이다", big="207만 개", big_size=110,
         note="1080 × 1920 = 2,073,600 픽셀",
         sub="당신이 보고 있는 이 영상도\n네모난 점(픽셀) 207만 개로 되어 있습니다."),
    Beat(52.0, 56.0, badge="지금", title="마크 세상이 되면\n당신은 {green}제일 먼저{/} 뭘 할 건가요?", title_size=70),
]
GRADE = {"exposure": 0.88, "bloom": 0.2, "bloom_thr": 1.3, "vignette": 0.28}

GRASS, DIRT, STONE, SAND, LOG, LEAF, PLANK, COBBLE, GLASS, ROOF, WATER = range(11)
TOP = {GRASS: (0.32, 0.62, 0.20), DIRT: (0.45, 0.30, 0.18), STONE: (0.48, 0.48, 0.50), SAND: (0.86, 0.80, 0.55),
       LOG: (0.55, 0.42, 0.25), LEAF: (0.18, 0.48, 0.14), PLANK: (0.70, 0.54, 0.32), COBBLE: (0.42, 0.42, 0.44),
       GLASS: (0.70, 0.85, 0.95), ROOF: (0.40, 0.18, 0.12), WATER: (0.12, 0.32, 0.75)}
SIDE = dict(TOP)
SIDE[GRASS] = (0.45, 0.30, 0.18)
SIDE[LOG] = (0.36, 0.25, 0.14)


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def value_noise(rs, n, octaves=4):
    out = np.zeros((n, n))
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        k = 2 ** (o + 2)
        g = rs.random((k + 1, k + 1))
        xs = np.linspace(0, k, n)
        i0 = np.floor(xs).astype(int).clip(0, k - 1)
        f = xs - i0
        f = f * f * (3 - 2 * f)
        a = g[i0][:, i0] * (1 - f)[None, :] + g[i0][:, i0 + 1] * f[None, :]
        b = g[i0 + 1][:, i0] * (1 - f)[None, :] + g[i0 + 1][:, i0 + 1] * f[None, :]
        out += amp * (a * (1 - f)[:, None] + b * f[:, None])
        tot += amp
        amp *= 0.5
    return out / tot


def simulate(build_dir):
    rs = np.random.default_rng(22)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    c = (N - 1) / 2
    yy, xx = np.mgrid[0:N, 0:N]
    rr = np.hypot(xx - c, yy - c)
    inside = rr <= R_ISL
    hn = value_noise(rs, N)
    h = 3 + (hn - 0.35) * 14
    h -= np.clip((rr - 14) / 7, 0, 1) ** 2 * 4
    # 호수(분지): 중심 남서쪽
    lx, ly = c - 6, c + 5
    lake = np.hypot(xx - lx, yy - ly) < 5.2
    h = np.where(lake, 1.0, h)
    h = np.round(np.clip(h, 1, 11)).astype(int)
    h[~inside] = -99
    # 언덕 위 집 3채 자리 평탄화
    houses = [(c + 5, c - 5), (c + 9, c + 3), (c - 2, c - 9)]
    for hx, hy in houses:
        hx, hy = int(hx), int(hy)
        base = int(np.median(h[hy - 3:hy + 4, hx - 3:hx + 4]))
        h[hy - 3:hy + 4, hx - 3:hx + 4] = np.where(inside[hy - 3:hy + 4, hx - 3:hx + 4], base, -99)
    blocks = []  # (x, y, z, kind, group)  group: 0=땅 1=나무줄기 2=잎 3=집 4=모래낙하
    for j in range(N):
        for i in range(N):
            if h[j, i] < 0:
                continue
            top = h[j, i]
            beach = (not lake[j, i]) and np.any(lake[max(0, j - 2):j + 3, max(0, i - 2):i + 3])
            for z in range(-3, top + 1):
                if z == top:
                    k = SAND if (beach or lake[j, i]) else GRASS
                elif z >= top - 2:
                    k = SAND if (beach or lake[j, i]) else DIRT
                else:
                    k = STONE
                blocks.append((i, j, z, k, 0))
    # 나무
    trees = []
    tries = 0
    while len(trees) < 12 and tries < 500:
        tries += 1
        i, j = rs.integers(4, N - 4, 2)
        if h[j, i] < 2 or lake[j, i] or any(abs(i - a) < 4 and abs(j - b) < 4 for a, b in trees) or \
                any(abs(i - hx) < 5 and abs(j - hy) < 5 for hx, hy in houses):
            continue
        trees.append((int(i), int(j)))
    hero_tree = min(trees, key=lambda p: (p[0] - (c + 3)) ** 2 + (p[1] - (c - 1)) ** 2)
    for ti, (i, j) in enumerate(trees):
        top = h[j, i]
        hero = (i, j) == hero_tree
        for z in range(top + 1, top + 5):
            blocks.append((i, j, z, LOG, 1 if hero else 5))
        for dz in range(3, 6):
            rad = 2 if dz < 5 else 1
            for dx in range(-rad, rad + 1):
                for dy in range(-rad, rad + 1):
                    if abs(dx) == rad and abs(dy) == rad and rs.random() < 0.6:
                        continue
                    if dx == 0 and dy == 0 and dz < 5:
                        continue
                    blocks.append((i + dx, j + dy, top + dz + 1, LEAF, 2 if hero else 6))
    # 집
    for hx, hy in houses:
        hx, hy = int(hx), int(hy)
        base = h[hy, hx]
        for z in range(base + 1, base + 4):
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if abs(dx) == 2 or abs(dy) == 2:
                        win = (z == base + 2 and (dx == 0 or dy == 0))
                        door = (z <= base + 2 and dx == 0 and dy == -2)
                        if door:
                            continue
                        blocks.append((hx + dx, hy + dy, z, GLASS if win else (COBBLE if z == base + 1 else PLANK), 3))
        for lvl in range(3):
            r = 3 - lvl
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if abs(dx) == r or abs(dy) == r or lvl == 2:
                        blocks.append((hx + dx, hy + dy, base + 4 + lvl, ROOF, 3))
    # 떠 있는 모래 기둥 (중력 시연) — 호수 동쪽 절벽 위
    sx, sy = hero_tree[0] + 4, hero_tree[1]
    sbase = max(h[sy, sx], 1)
    sand_ids = []
    for z in range(sbase + 4, sbase + 8):
        sand_ids.append(len(blocks))
        blocks.append((sx, sy, z, SAND, 4))
    support_id = len(blocks)
    blocks.append((sx, sy, sbase + 3, DIRT, 7))  # 이 받침을 캐면 모래가 떨어짐
    bl = np.array(blocks, np.float32)
    nb = len(bl)
    pos = np.stack([(bl[:, 0] - c) * B, (bl[:, 1] - c) * B, bl[:, 2] * B], 1)
    kind = bl[:, 3].astype(int)
    group = bl[:, 4].astype(int)
    top_c = np.array([TOP[k] for k in kind], np.float32)
    side_c = np.array([SIDE[k] for k in kind], np.float32)
    jitter = rs.uniform(0.92, 1.06, (nb, 1)).astype(np.float32)
    top_c *= jitter
    side_c *= jitter
    dist = np.hypot(pos[:, 0], pos[:, 1]) / B
    appear = WAVE_T0 + dist / WAVE_V + rs.uniform(0, 0.15, nb) + np.clip(bl[:, 2], 0, 20) * 0.01
    scale = np.zeros((nf, nb), np.float32)
    zoff = np.zeros((nf, nb), np.float32)
    for i, t in enumerate(ts):
        u = np.clip((t - appear) / 0.35, 0, 1)
        scale[i] = np.where(u > 0, np.minimum(1.0, u * 1.15) - np.maximum(0, u - 0.87) * 1.15 * 0, 0)
    # 나무 밑동 캐기: 줄기 블록이 아래부터 차례로 사라짐 (14.6~16.2초)
    trunk = np.where(group == 1)[0]
    trunk = trunk[np.argsort(pos[trunk, 2])]
    for k, idx in enumerate(trunk):
        tk = 14.6 + 0.4 * k
        scale[:, idx] *= np.clip((tk - ts) / 0.12, 0, 1)
    # 모래 받침 캐기 → 모래 낙하(중력 가속도)
    t_cut = 17.2
    scale[:, support_id] *= np.clip((t_cut - ts) / 0.12, 0, 1)
    g = 9.8 * 1.2  # 블록/초² (보기 좋게)
    fall_len = 1.0  # 받침 1칸 높이만큼 떨어짐
    for k, idx in enumerate(sand_ids):
        tt = np.maximum(ts - t_cut, 0)
        d = np.minimum(0.5 * g * tt * tt, fall_len)
        zoff[:, idx] = -d * B
    # 물 세포 자동자 (호수 분지, 높이 1층 위)
    W = np.zeros((N, N))
    src = np.zeros((N, N), bool)
    basin = lake.copy()
    s1, s2 = (int(lx - 2), int(ly)), (int(lx + 2), int(ly))
    water_frames = np.zeros((nf, N, N), np.float32)
    tick_dt = 0.12
    nxt = 20.3
    for i, t in enumerate(ts):
        if t >= 20.3 and not src[s1[1], s1[0]]:
            src[s1[1], s1[0]] = src[s2[1], s2[0]] = True
        while t >= nxt and t < 26.5:
            nxt += tick_dt
            L = np.where(src, 8.0, W)
            new = L.copy()
            for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                sh = np.roll(np.roll(L, dj, 0), di, 1)
                new = np.maximum(new, np.where(basin, sh - 1, 0))
            # 원천 2개 이상과 붙은 칸 → 새 원천 (무한 물 규칙)
            cnt = sum(np.roll(np.roll(src, dj, 0), di, 1).astype(int) for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            src = src | (basin & (cnt >= 2))
            W = np.where(basin, np.clip(new, 0, 8), 0)
        water_frames[i] = np.where(src, 8.0, W) / 8.0 if t >= 20.3 else 0.0
    # 사람 (2블록 높이 상자 인간), 섬 위를 걸어다님
    ppl = rs.uniform(-R_ISL * 0.55, R_ISL * 0.55, (NPPL, 2)) * B
    ang = rs.uniform(0, 6.28, NPPL)
    ppl_p = np.zeros((nf, NPPL, 3), np.float32)
    ppl_yaw = np.zeros((nf, NPPL), np.float32)
    hh = h.astype(float)

    def ground(p):
        ii = np.clip(np.round(p[:, 0] / B + c).astype(int), 0, N - 1)
        jj = np.clip(np.round(p[:, 1] / B + c).astype(int), 0, N - 1)
        z = hh[jj, ii]
        return np.where(z < 0, 0, z + 0.5) * B, lake[jj, ii]

    walker = 0  # 38~44초: 한 명이 세상 끝을 향해 걸어감
    for i, t in enumerate(ts):
        ang += rs.normal(0, 0.6, NPPL) / FPS
        step = np.stack([np.cos(ang), np.sin(ang)], 1) * 0.55 * B / FPS
        if t >= 38.0:
            ang[walker] = math.radians(40)
            step[walker] = np.array([math.cos(ang[walker]), math.sin(ang[walker])]) * 1.4 * B / FPS
        newp = ppl + step
        z, wet = ground(newp)
        rad = np.hypot(newp[:, 0], newp[:, 1]) / B
        bad = ((rad > R_ISL - 2) | wet) & (np.arange(NPPL) != walker if t >= 38 else True)
        ang = np.where(bad, ang + math.pi * 0.7, ang)
        ppl = np.where(bad[:, None], ppl, newp)
        z, _ = ground(ppl)
        ppl_p[i, :, :2] = ppl
        ppl_p[i, :, 2] = z
        ppl_yaw[i] = ang
    import cv2
    hs = np.where(hh < 0, -4, hh)
    up = cv2.resize(hs, (N * 3, N * 3), interpolation=cv2.INTER_CUBIC)
    xs = (np.arange(N * 3) / 3.0 - c) * B
    XX, YY = np.meshgrid(xs, xs)
    ZZ = np.where(np.hypot(XX, YY) / B < R_ISL + 0.5, up * B + 0.5 * B, -1.5)
    tr_xy = np.array([((i - c) * B, (j - c) * B, (h[j, i] + 0.5) * B) for i, j in trees], np.float32)
    ho_xy = np.array([((int(x) - c) * B, (int(y) - c) * B, (h[int(y), int(x)] + 0.5) * B) for x, y in houses], np.float32)
    hero_c = np.array([(hero_tree[0] + 2 - c) * B, (hero_tree[1] - c) * B, (h[hero_tree[1], hero_tree[0]] + 3) * B],
                      np.float32)
    return dict(hero=hero_c, sm_X=XX.astype(np.float32), sm_Y=YY.astype(np.float32), sm_Z=ZZ.astype(np.float32), tr_xy=tr_xy, ho_xy=ho_xy, pos=pos.astype(np.float32), kind=kind.astype(np.float32), top_c=top_c, side_c=side_c, scale=scale,
                zoff=zoff, water=water_frames, lake=lake.astype(np.float32), h=h.astype(np.float32),
                ppl_p=ppl_p, ppl_yaw=ppl_yaw, smooth_h=hh.astype(np.float32))


def postfx(img, t):
    """반전: 화면이 점점 큰 픽셀 블록으로."""
    if t < 44.3 or t > 52.4:
        return img
    import cv2
    u = ramp(t, 44.3, 46.5) * (1 - ramp(t, 50.8, 52.4))
    b = int(round(1 + 47 * u))
    if b <= 1:
        return img
    h, w = img.shape[:2]
    sm = cv2.resize(img, (max(1, w // b), max(1, h // b)), interpolation=cv2.INTER_AREA)
    return cv2.resize(sm, (w, h), interpolation=cv2.INTER_NEAREST)


CLOCK = [(0.0, 0.0), (9.0, 0.0), (9.6, 1.0), (14.0, 1.3), (14.6, 3.0), (20.0, 3.3), (20.6, 7.0), (26.0, 7.3),
         (26.6, 30.0), (32.0, 33.0), (32.6, 365.0), (56.0, 370.0)]


def labels(t, anchors, sim):
    out = []
    a = anchors.get("gap")
    if a and a[3] and 16.0 < t < 20.0:
        out.append({"x": a[0], "y": a[1], "text": "밑동 없음 → 그래도 떠 있음", "color": "yellow", "size": 26,
                    "alpha": ramp(t, 16.0, 16.5)})
    a = anchors.get("sand")
    if a and a[3] and 17.0 < t < 20.0:
        out.append({"x": a[0], "y": a[1], "text": "모래만 떨어짐", "color": "orange", "size": 26,
                    "alpha": ramp(t, 17.2, 17.7)})
    return out


def hud(t, sim):
    d = keyed(t, CLOCK)
    mc_days = d * 72
    right = "경과 0일" if d < 0.5 else (f"경과 {d:.0f}일" if d < 300 else "경과 1년")
    return {"left": "SIMULATION", "right": right, "right2": f"마크 시간 {int(mc_days):,}일째"}


def build(ctx):
    import bpy
    from engine import bkit as K
    sim = ctx.sim
    K.world_space(ctx, ambient=(0.45, 0.55, 0.8), ambient_strength=0.38)
    sun = K.sun(ctx, 3.2, color=(1.0, 0.95, 0.85), angle=2.0)
    # 블록 재질: 윗면 col / 옆면 col2, 16×16 픽셀 무늬
    bm_, nt, out = K.new_mat("m_block")
    tco = nt.nodes.new("ShaderNodeTexCoord")
    vm = nt.nodes.new("ShaderNodeVectorMath")
    vm.operation = "MULTIPLY"
    K.ln(nt, tco.outputs["Object"], vm.inputs[0])
    vm.inputs[1].default_value = (16, 16, 16)
    fl = nt.nodes.new("ShaderNodeVectorMath")
    fl.operation = "FLOOR"
    K.ln(nt, vm.outputs[0], fl.inputs[0])
    wn = nt.nodes.new("ShaderNodeTexWhiteNoise")
    wn.noise_dimensions = "3D"
    K.ln(nt, fl.outputs[0], wn.inputs["Vector"])
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    nsep = nt.nodes.new("ShaderNodeSeparateXYZ")
    K.ln(nt, geo.outputs["Normal"], nsep.inputs[0])
    osep = nt.nodes.new("ShaderNodeSeparateXYZ")
    K.ln(nt, tco.outputs["Object"], osep.inputs[0])
    is_top = K.math_node(nt, "GREATER_THAN", nsep.outputs["Z"], 0.5)
    strip = K.math_node(nt, "GREATER_THAN", osep.outputs["Z"], 0.78)  # 잔디 블록 옆 윗줄
    use_top = K.math_node(nt, "MAXIMUM", is_top, strip)
    colr = K.mix_rgb(nt, use_top, K.inst_attr(nt, "col2"), K.inst_attr(nt, "col"))
    shade = K.math_node(nt, "MULTIPLY_ADD", wn.outputs["Value"], 0.22, 0.86)
    colr = K.mix_rgb(nt, 1.0, colr, shade, "MULTIPLY")
    b = K.principled(nt, colr, 0.9)
    K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    pb = K.proto(ctx, "p_block", K.bm_cube(1, 1, 1, (0, 0, -0.5), bottom=True), [bm_])
    pos = sim["pos"]
    nb = len(pos)
    blk = K.instancer(ctx, "blocks", pb, nb)
    K.add_attr(blk, "col2", "FLOAT_COLOR")
    # 물 블록 (호수 격자)
    lake = sim["lake"]
    lj, li = np.where(lake > 0.5)
    c = (N - 1) / 2
    wpos = np.stack([(li - c) * B, (lj - c) * B, np.full(len(li), 1.5 * B)], 1).astype(np.float32)
    wm = K.mat_water("m_mcwater", color=(0.10, 0.28, 0.72), rough=0.15, emit=0.4)
    wbox = K.proto(ctx, "p_water", K.bm_cube(1, 1, 1, (0, 0, 0), bottom=True), [wm])
    wat = K.instancer(ctx, "water", wbox, len(wpos), vector_scale=True)
    # 매끈한 원래 세상 (파동이 지나가면 사라짐)
    XX, YY, ZZ = sim["sm_X"], sim["sm_Y"], sim["sm_Z"]
    sm, nt, out = K.new_mat("m_smooth")
    g2 = nt.nodes.new("ShaderNodeNewGeometry")
    s2 = nt.nodes.new("ShaderNodeSeparateXYZ")
    K.ln(nt, g2.outputs["Position"], s2.inputs[0])
    ramp_ = nt.nodes.new("ShaderNodeValToRGB")
    K.ln(nt, K.math_node(nt, "DIVIDE", s2.outputs["Z"], 6.0, clamp=True), ramp_.inputs[0])
    e = ramp_.color_ramp.elements
    e[0].position, e[0].color = 0.02, (0.78, 0.72, 0.5, 1)
    e[1].position, e[1].color = 1.0, (0.5, 0.5, 0.48, 1)
    for pos_, c_ in ((0.12, (0.26, 0.52, 0.18)), (0.7, (0.20, 0.42, 0.14))):
        el = e.new(pos_)
        el.color = (*c_, 1)
    bs = K.principled(nt, ramp_.outputs["Color"], 0.8)
    rdist = K.math_node(nt, "SQRT", K.math_node(nt, "ADD", K.math_node(nt, "POWER", s2.outputs["X"], 2.0),
                                                K.math_node(nt, "POWER", s2.outputs["Y"], 2.0)))
    gone = K.math_node(nt, "LESS_THAN", rdist, ctx.ctl_node(nt, "wave_r", -1.0))
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    K.ln(nt, gone, mx.inputs[0])
    K.ln(nt, bs.outputs["BSDF"], mx.inputs[1])
    K.ln(nt, tr.outputs[0], mx.inputs[2])
    K.ln(nt, mx.outputs[0], out.inputs["Surface"])
    smooth = K.grid_mesh("smooth", XX, YY, ZZ, sm, skirt_z=-1.6)
    smooth.data.polygons.foreach_set("use_smooth", [True] * len(smooth.data.polygons))
    K.island(ctx, (R_ISL + 0.6) * B, thick=0.05, depth=5.0, top_mat=K.mat_simple("m_none", (0.1, 0.1, 0.1)))
    bpy.data.objects["island_top"].hide_render = True
    bpy.data.objects["island_side"].location.z = -3.4 * B
    # 매끈한 세상의 나무·집 (파동이 닿으면 사라짐)
    leaf = K.mat_inst("m_sleaf", 0.8)
    trunk = K.mat_simple("m_strunk", (0.3, 0.2, 0.1), 0.9)
    s_tree = K.instancer(ctx, "s_trees", K.proto_tree(ctx, leaf, trunk, "round"), len(sim["tr_xy"]))
    hparts = [(K.bm_cube(2.2, 2.2, 1.5, (0, 0, 0), True), 0), (K.bm_cone(1.7, 0.0, 1.0, (0, 0, 1.5), 4), 1)]
    s_house = K.instancer(ctx, "s_houses", K.proto(ctx, "p_shouse", K.join_bms(hparts),
                                                   [K.mat_simple("m_swall", (0.85, 0.8, 0.7), 0.7),
                                                    K.mat_simple("m_sroof", (0.55, 0.2, 0.15), 0.6)]), len(sim["ho_xy"]))
    trx, hox = sim["tr_xy"], sim["ho_xy"]
    # 사람(상자 인간): 다리·몸·머리
    pm = K.mat_inst("m_mcppl", 0.7)
    parts = [(K.bm_cube(0.22, 0.12, 0.44, (0, 0, 0), True), 0), (K.bm_cube(0.26, 0.16, 0.38, (0, 0, 0.44), True), 0),
             (K.bm_cube(0.24, 0.24, 0.24, (0, 0, 0.82), True), 1)]
    pp = K.proto(ctx, "p_mcppl", K.join_bms(parts), [pm, K.mat_simple("m_mcskin", (0.85, 0.65, 0.5), 0.7)])
    ppl = K.instancer(ctx, "mcppl", pp, NPPL)
    pcol = np.array([(0.2, 0.5, 0.9), (0.9, 0.3, 0.3), (0.3, 0.7, 0.3), (0.9, 0.7, 0.2), (0.6, 0.3, 0.8)] * 2,
                    np.float32)
    # 네모난 해와 달
    sq_sun = K.mesh_obj("mc_sun", K.bm_cube(1.4, 1.4, 0.05), K.mat_emit("m_sq_sun", (1.0, 0.92, 0.55), 12.0))
    sq_moon = K.mesh_obj("mc_moon", K.bm_cube(1.1, 1.1, 0.05), K.mat_emit("m_sq_moon", (0.85, 0.9, 1.0), 4.0))
    # 건축 한계(320층) 격자 천장, 월드 보더 벽
    gm, nt, out = K.new_mat("m_ceiling")
    tco2 = nt.nodes.new("ShaderNodeTexCoord")
    sp2 = nt.nodes.new("ShaderNodeSeparateXYZ")
    K.ln(nt, tco2.outputs["Object"], sp2.inputs[0])
    gx = K.math_node(nt, "LESS_THAN", K.math_node(nt, "FRACT", K.math_node(nt, "MULTIPLY", sp2.outputs["X"], 2.0)), 0.06)
    gy = K.math_node(nt, "LESS_THAN", K.math_node(nt, "FRACT", K.math_node(nt, "MULTIPLY", sp2.outputs["Y"], 2.0)), 0.06)
    line = K.math_node(nt, "MAXIMUM", gx, gy)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (0.4, 0.85, 1.0, 1)
    K.ln(nt, K.math_node(nt, "MULTIPLY", line, ctx.ctl_node(nt, "ceiling", 0.0)), em.inputs["Strength"])
    trc = nt.nodes.new("ShaderNodeBsdfTransparent")
    addc = nt.nodes.new("ShaderNodeAddShader")
    K.ln(nt, trc.outputs[0], addc.inputs[0])
    K.ln(nt, em.outputs[0], addc.inputs[1])
    K.ln(nt, addc.outputs[0], out.inputs["Surface"])
    gm.cycles.emission_sampling = "NONE"
    bmc = K.bmesh.new()
    K.bmesh.ops.create_grid(bmc, x_segments=1, y_segments=1, size=14.0)
    ceil = K.mesh_obj("ceiling", bmc, gm)
    ceil.location.z = 9.0
    wall_m = K.mat_emit("m_border", (0.3, 0.6, 1.0), 1.5, ctx, "border")
    wall = K.mesh_obj("border", K.bm_cube(60.0, 0.3, 40.0, (0, 0, -15.0), True), wall_m)
    wall.location = (0, 70.0, 0)
    wall.rotation_euler = (0, 0, math.radians(-50))
    cam = K.CamRig(ctx, 30, fstop=0)
    top_c, side_c, scale_all, zoff = sim["top_c"], sim["side_c"], sim["scale"], sim["zoff"]
    rot0 = np.zeros((nb, 3), np.float32)
    CAM = [(0.0, (0, 0, 0.8), -60, 34, 29.0, 28), (4.2, (0, 0, 0.8), -50, 36, 27.0, 28),
           (9.0, (0, 0, 0.5), -20, 40, 30.0, 28), (14.0, "hero", 115, 9, 12.0, 30),
           (19.8, "hero", 100, 11, 12.5, 30), (20.4, (-3.0, 2.5, 0.6), 45, 42, 15.0, 30),
           (25.8, (-3.0, 2.5, 0.6), 70, 46, 15.5, 30), (26.4, (0, 0, 3.0), 90, 24, 34.0, 26),
           (31.8, (0, 0, 3.0), 110, 26, 36.0, 26), (32.4, (0, 0, 0), 130, 50, 70.0, 26),
           (38.0, (4.0, 3.0, 0), 150, 32, 30.0, 28), (44.0, (6.0, 6.0, 0), 160, 30, 34.0, 28),
           (52.0, (0, 0, 0.5), 200, 36, 31.0, 28), (56.0, (0, 0, 0.5), 220, 38, 33.0, 28)]

    hero = tuple(float(x) for x in sim["hero"])
    CAM = [(k[0], hero if k[1] == "hero" else k[1], *k[2:]) for k in CAM]

    def upd(t, f):
        v = keyed(t, snap([(k[0], (*k[1], *k[2:])) for k in CAM]))
        cam.set(v[:3], v[3] + t * 1.5, v[4], v[5], v[6], shift=0.05)
        wave_r = (t - WAVE_T0) * WAVE_V * B
        ctx.set_ctl("wave_r", wave_r if t > WAVE_T0 else -1.0)
        smooth.hide_render = t > WAVE_T0 + (R_ISL + 3) / WAVE_V
        dtr = np.hypot(trx[:, 0], trx[:, 1])
        K.set_points(s_tree, trx, scale=np.where(dtr > wave_r, 2.6, 0.0) if t > WAVE_T0 else np.full(len(trx), 2.6),
                     rot=np.zeros((len(trx), 3)), col=np.tile((0.2, 0.5, 0.15), (len(trx), 1)))
        dho = np.hypot(hox[:, 0], hox[:, 1])
        K.set_points(s_house, hox, scale=np.where(dho > wave_r, 1.0, 0.0) if t > WAVE_T0 else np.ones(len(hox)),
                     rot=np.zeros((len(hox), 3)), col=np.ones((len(hox), 3)))
        p = pos.copy()
        p[:, 2] += zoff[f]
        K.set_points(blk, p, scale=scale_all[f] * B, rot=rot0, col=top_c, colors={"col2": side_c})
        wl = sim["water"][f][lake > 0.5]
        K.set_points(wat, wpos, scale=(wl > 0.01).astype(np.float32), size=np.c_[np.full(len(wl), B), np.full(len(wl), B),
                                                                                 np.maximum(wl, 0.05) * B * 0.9],
                     rot=np.zeros((len(wpos), 3)), col=np.ones((len(wpos), 3)))
        K.set_points(ppl, sim["ppl_p"][f], scale=np.full(NPPL, B) * (t > WAVE_T0 + 1.5),
                     rot=np.c_[np.zeros((NPPL, 2)), sim["ppl_yaw"][f]], col=pcol)
        # 낮밤: 9~14초 동안 해가 빠르게 여러 바퀴, 그 밖엔 낮
        if 9.0 <= t < 14.0:
            ang = (t - 9.0) / 5.0 * 2 * math.pi * 2.0 + math.pi * 0.25
        else:
            ang = math.radians(55)
        sx, sz = math.cos(ang), math.sin(ang)
        sq_sun.location = (sx * 16, -3.0, sz * 16)
        sq_moon.location = (-sx * 16, -3.0, -sz * 16)
        sq_sun.rotation_euler = (0, -ang + math.pi / 2, 0)
        sq_moon.rotation_euler = (0, -ang + math.pi / 2, 0)
        day = clamp(sz * 3 + 0.3)
        src = K.Vector((sx, -0.25, max(sz, -0.2)))
        sun.rotation_euler = (-src).to_track_quat("-Z", "Y").to_euler()
        sun.data.energy = 0.25 + 3.0 * day
        sun.data.color = (1.0, 0.85 + 0.1 * day, 0.7 + 0.2 * day) if day > 0.1 else (0.6, 0.7, 1.0)
        ctx.set_ctl("ambient", 0.08 + 0.3 * day)
        ctx.set_ctl("ceiling", 2.5 * ramp(t, 26.4, 27.4) * (1 - ramp(t, 31.6, 32.4)))
        ctx.set_ctl("border", 1.6 * ramp(t, 38.3, 39.5) * (1 - ramp(t, 43.6, 44.4)))

    ctx.on_frame(upd)
    hz_ = sim["hero"]
    ctx.anchor("gap", lambda t: (float(hz_[0]) - 2 * B, float(hz_[1]), float(hz_[2]) - 0.6 * B))
    ctx.anchor("sand", lambda t: (float(hz_[0]) + 2 * B, float(hz_[1]), float(hz_[2]) + 2.6 * B))
