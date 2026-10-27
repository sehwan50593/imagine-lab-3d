"""EP01 만약 세상에 인간이 사라지고 고양이만 남는다면?

떠 있는 도시 섬 하나에서 실제로 돌아가는 시뮬레이션:
- 사람·차: 도로망 위를 걷다 D-DAY에 사라짐
- 고양이·쥐: 포식자-피식자 모델(섬 단위 개체 수) + 쫓기/도망 이동
- 식생: 도로·건물 녹지화, 거리 나무 성장 / 건물: 와이블 분포 수명으로 붕괴
"""
from engine.cuts import snap
import math

import numpy as np

from engine.common import FPS, Beat, clamp, fmt_int, frames_of, keyed, logkeyed, ramp, smooth
from engine.layout import RoadWalkers, Wanderers, city_layout, push_out_of_rects, river_y

DUR = 56.0
META = {"id": "ep01", "title": "만약 세상에 인간이 사라지고 고양이만 남는다면?", "duration": DUR,
        "music": {"key": "F", "mode": "major", "bpm": 70, "seed": 11, "twist_at": 44.5}}
R = 10.5
SPACING = 2.8
ROAD_W = 0.58
RIVER = (0.22, -2.6, 1.3, 0.55)
NC, NR, NP, NCAR, NT, NS = 40, 180, 70, 24, 260, 70

# 영상 시간(초) → 시뮬레이션 시간(일)
TIMELINE = [(0.0, 0.2917), (4.5, 0.75), (5.3, 1.0), (9.5, 1.6), (10.3, 2.0), (14.5, 4.0), (15.5, 30.0),
            (20.5, 60.0), (21.5, 365.25), (26.5, 600.0), (27.5, 3652.5), (32.5, 6000.0), (33.5, 36525.0),
            (38.5, 200000.0), (39.5, 3652500.0), (44.5, 3700000.0), (56.0, 3760000.0)]


def days_at(t):
    return logkeyed(t, TIMELINE)


def human_count(t, sim=None):
    u = smooth((t - 1.0) / 1.5)
    return fmt_int(8.2e9 * (1 - u)) + "명"


BEATS = [
    Beat(0.0, 2.5, badge="D-DAY", label="인간", big=human_count, big_color="white",
         sub="어느 날 아침, 지구에서\n인간 82억 명이 한순간에 사라진다면?"),
    Beat(2.5, 4.5, badge="D-DAY", label="남은 건", label_color="orange", big="고양이 2억~6억 마리",
         sub="어느 날 아침, 지구에서\n인간 82억 명이 한순간에 사라진다면?"),
    Beat(4.5, 9.5, badge="D+1", title="주인 없는 {orange}반려묘{/}", note="반려묘만 2.2억~3.7억 마리",
         sub="닫힌 집 안의 반려묘들은\n밖으로 나와야만 살아남습니다."),
    Beat(9.5, 14.5, badge="D+2", title="도시의 불이 꺼진다",
         sub="연료를 넣고 지킬 사람이 없으면 발전소는\n몇 시간~며칠 안에 하나둘 멈춥니다."),
    Beat(14.5, 20.5, badge="1개월 후", title="{red}쥐{/} 대폭발", note="암컷 1마리가 1년에 새끼 약 50마리",
         sub="남겨진 음식물 쓰레기를 먹고\n쥐가 폭발적으로 늘어납니다."),
    Beat(20.5, 26.5, badge="1년 후", title="고양이 = 도시의 {orange}사냥꾼{/}",
         note="미국 고양이만 한 해 새 13억~40억 마리 사냥",
         sub="사료가 끊긴 고양이는\n쥐와 새를 사냥하며 버팁니다."),
    Beat(26.5, 32.5, badge="10년 후", title="도로가 {green}숲{/}이 된다",
         sub="아스팔트 틈마다 풀과 나무가 자라\n도시를 덮어 갑니다."),
    Beat(32.5, 38.5, badge="100년 후", title="건물이 무너진다",
         sub="관리받지 못한 건물은 하나둘 무너지고\n고양이는 숲의 포식자가 됩니다."),
    Beat(38.5, 44.5, badge="1만 년 후", title="고양이의 {orange}원래 모습{/}", note="약 1만 년 전, 쥐를 따라 사람 곁에 온 동물",
         sub="품종은 서로 섞여 사라지고, 조상인\n들고양이처럼 줄무늬 고양이가 많아집니다."),
    Beat(44.5, 48.3, badge="반전", title="'{yellow}야옹{/}'이 사라진다",
         sub="다 자란 고양이는 서로에게\n거의 '야옹' 하지 않습니다."),
    Beat(48.3, 52.0, badge="반전", title="'{yellow}야옹{/}'이 사라진다",
         sub="'야옹'은 고양이가\n사람에게 말을 걸던 소리였으니까요."),
    Beat(52.0, 56.0, badge="1만 년 후", title="당신의 고양이는\n오늘 몇 번 {yellow}'야옹'{/}했나요?", title_size=70),
]
GRADE = {"exposure": 0.95, "bloom": 0.24, "bloom_thr": 1.0, "vignette": 0.3}

# 조명 키프레임: (t, 해 고도, 해 방위, 해 세기, 해 색, 주변광 세기, 주변광 색, 창문 불빛)
DAY = dict(elev=42, az=40, energy=3.2, col=(1.0, 0.93, 0.82), amb=0.42, amb_col=(0.45, 0.55, 0.78))
MORNING = dict(elev=16, az=-30, energy=2.6, col=(1.0, 0.78, 0.58), amb=0.32, amb_col=(0.42, 0.48, 0.70))
DUSK = dict(elev=4, az=150, energy=1.6, col=(1.0, 0.48, 0.25), amb=0.16, amb_col=(0.30, 0.25, 0.45))
NIGHT = dict(elev=55, az=200, energy=0.55, col=(0.55, 0.65, 1.0), amb=0.09, amb_col=(0.12, 0.15, 0.32))
BLUE = dict(elev=10, az=170, energy=1.1, col=(0.70, 0.72, 1.0), amb=0.2, amb_col=(0.30, 0.34, 0.62))
END = dict(elev=14, az=200, energy=2.2, col=(0.78, 0.80, 1.0), amb=0.28, amb_col=(0.34, 0.38, 0.68))
GOLD = dict(elev=12, az=120, energy=2.6, col=(1.0, 0.70, 0.42), amb=0.26, amb_col=(0.45, 0.42, 0.55))
LIGHT_KEYS = [(0.0, MORNING), (3.0, MORNING), (4.4, DUSK), (6.0, NIGHT), (13.9, NIGHT), (15.2, MORNING), (20.0, DAY),
              (21.0, DAY), (32.0, DAY), (33.2, GOLD), (38.0, GOLD), (39.2, DAY), (44.0, DAY), (45.5, DUSK),
              (50.0, BLUE), (52.5, END), (56.0, END)]
WINDOW_KEYS = [(0.0, 0.12), (3.0, 0.2), (4.6, 0.55), (10.4, 0.55), (12.6, 0.0), (56, 0.0)]

# 카메라: (t, 목표(x,y,z), 방위각, 고도각, 거리, 렌즈)
CAM_KEYS = [
    (0.0, (0.0, 0.0, 0.0), -70, 34, 42, 26),
    (2.4, (0.0, 0.0, 0.3), -62, 31, 38, 27),
    (4.5, (0.3, -0.3, 0.5), -50, 28, 31, 28),
    (9.3, (0.3, -0.3, 0.5), -25, 30, 30, 28),
    (10.6, (0.0, 0.0, 0.0), 0, 52, 44, 26),
    (14.2, (0.0, 0.0, 0.0), 20, 50, 42, 26),
    (15.6, (-1.4, 1.4, 0.0), 45, 64, 19, 28),
    (20.2, (-1.4, 1.4, 0.0), 72, 62, 20, 28),
    (21.6, (0.8, 0.8, 0.3), 95, 52, 27, 28),
    (26.2, (0.8, 0.8, 0.3), 115, 50, 28, 28),
    (27.6, (0.0, 0.0, 0.0), 130, 42, 42, 26),
    (32.5, (0.0, 0.0, 0.2), 160, 30, 37, 26),
    (38.5, (0.0, 0.0, 0.0), 200, 46, 44, 26),
    (44.0, (0.0, 0.0, 0.0), 228, 42, 42, 26),
    (45.6, (2.8, 2.8, 0.35), 250, 20, 7.0, 40),
    (51.6, (2.8, 2.8, 0.35), 268, 22, 7.6, 40),
    (55.8, (0.0, 0.0, -0.5), 300, 34, 50, 26),
]
HERO = (2.8, 2.8)
HOTSPOTS = [(-2.8, 2.8), (0.0, -5.6), (5.6, 2.8)]


def cam_at(t):
    ks = [(k[0], (*k[1], k[2], k[3], k[4], k[5])) for k in CAM_KEYS]
    v = keyed(t, snap(ks))
    return v[:3], v[3], v[4], v[5], v[6]


def fmt_elapsed(d):
    if d < 2:
        h = (d % 1) * 24
        return f"D+{int(d)}  {int(h):02d}:{int((h % 1) * 60):02d}"
    if d < 60:
        return f"{int(d)}일"
    if d < 730:
        return f"{int(d / 30.44)}개월"
    return f"{int(round(d / 365.25)):,}년"


def simulate(build_dir):
    rs = np.random.default_rng(101)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    days = np.array([days_at(t) for t in ts], np.float64)
    bld = city_layout(rs, R, SPACING, ROAD_W, river=RIVER, margin=0.7)
    nb = len(bld)
    rects = bld[:, :4]
    palette = np.array([(0.78, 0.74, 0.66), (0.66, 0.70, 0.76), (0.80, 0.62, 0.50), (0.60, 0.64, 0.62),
                        (0.86, 0.82, 0.74), (0.52, 0.56, 0.66), (0.74, 0.56, 0.46)], np.float32)
    bld_col = palette[rs.integers(0, len(palette), nb)] * rs.uniform(0.85, 1.05, (nb, 1))
    bld_lit = rs.uniform(0.35, 1.0, nb).astype(np.float32)
    bld_seed = rs.uniform(0, 100, nb).astype(np.float32)
    # 정전 물결: 섬 한쪽부터 꺼짐
    off_t = 10.4 + 2.2 * smooth_arr((bld[:, 0] * 0.6 + bld[:, 1] * 0.8 + R) / (2.4 * R)) + rs.normal(0, 0.12, nb)
    # 건물 수명(년): 와이블
    life = 60 + 260 * rs.weibull(2.0, nb) * (1.0 + 0.15 * bld[:, 4])
    tilt_ax = rs.uniform(0, 2 * np.pi, nb)
    tilt_mag = rs.uniform(0.12, 0.42, nb)
    years = days / 365.25
    prog = np.clip((years[:, None] - life[None, :]) / (life[None, :] * 0.25), 0, 1)
    prog = prog * prog * (3 - 2 * prog)
    final_h = rs.uniform(0.12, 0.32, nb)
    bld_h = bld[None, :, 4] * (1 - prog * (1 - final_h[None, :]))
    bld_rot = np.zeros((nf, nb, 3), np.float32)
    bld_rot[:, :, 0] = prog * tilt_mag[None] * np.cos(tilt_ax)[None]
    bld_rot[:, :, 1] = prog * tilt_mag[None] * np.sin(tilt_ax)[None]

    # 개체 수 모델 (섬 단위): 쥐 R, 고양이 C, 남은 음식 F, 식생 V
    Rr, Cc, F = 26.0, 12.0, 1.0
    pop_R, pop_C = np.zeros(nf), np.zeros(nf)
    escaped_total = 22.0
    veg = np.zeros(nf)
    prev_d = days[0]
    for i, d in enumerate(days):
        span = max(0.0, d - prev_d)
        nsub = int(min(6000, max(1, math.ceil(span / (0.25 if d < 3650 else 5.0)))))
        dt = span / nsub if nsub else 0.0
        for _ in range(nsub):
            prev_d += dt
            V = 1 - math.exp(-max(0.0, prev_d - 200) / 4000.0)
            F = math.exp(-prev_d / 150.0)          # 남은 음식물 쓰레기
            K = 45 + 380 * F + 70 * V              # 쥐 환경 수용력
            pred = 0.0006 * Rr * Cc                # 고양이의 사냥
            Rr = max(2.0, Rr + (0.075 * Rr * (1 - Rr / K) - pred) * dt)
            emerge = escaped_total * (math.exp(-max(0, prev_d - 0.4) / 0.7) / 0.7) if 0.4 < prev_d < 4 else 0.0
            Cc = max(3.0, Cc + (0.062 * pred - 0.003 * Cc + emerge) * dt)
        pop_R[i], pop_C[i] = Rr, Cc
        veg[i] = 1 - math.exp(-max(0.0, d - 200) / 4000.0)
    overgrow = np.clip(np.interp(np.log10(np.maximum(days, 1)), [np.log10(200), np.log10(3650), np.log10(36500),
                                                                    np.log10(3.65e6)], [0.0, 0.5, 0.82, 1.0]), 0, 1)
    decay = np.clip(np.interp(np.log10(np.maximum(days, 1)), [np.log10(30), np.log10(3650), np.log10(36500)],
                              [0.0, 0.45, 0.85]), 0, 1)

    # ── 에이전트 ──
    walkers = RoadWalkers(rs, R, NP, rs.uniform(0.55, 0.85, NP), SPACING, sidewalk=0.42)
    cars = RoadWalkers(rs, R, NCAR, rs.uniform(1.8, 2.6, NCAR), SPACING, lane=0.15)
    vanish = rs.uniform(1.15, 2.35, NP)
    car_stop = rs.uniform(1.6, 2.6, NCAR)
    car_speed = cars.speed.copy()
    ppl_p = np.zeros((nf, NP, 2), np.float32)
    ppl_yaw = np.zeros((nf, NP), np.float32)
    ppl_on = np.zeros((nf, NP), np.float32)
    car_p = np.zeros((nf, NCAR, 2), np.float32)
    car_yaw = np.zeros((nf, NCAR), np.float32)
    spark_p = np.zeros((nf, NP, 3), np.float32)
    spark_on = np.zeros((nf, NP), np.float32)
    car_jit = rs.normal(0, 0.25, NCAR)
    for i, t in enumerate(ts):
        if t < 3.0:
            p, y = walkers.step(1 / FPS)
            last_p, last_y = p, y
        ppl_p[i], ppl_yaw[i] = last_p, last_y
        ppl_on[i] = np.clip((vanish - t) / 0.25, 0, 1)
        k = np.clip((t - vanish) / 0.9, 0, 1)
        spark_on[i] = np.where((t >= vanish) & (t < vanish + 0.9), 1 - k, 0)
        spark_p[i, :, :2] = last_p
        spark_p[i, :, 2] = 0.3 + k * 1.8
        cars.speed = car_speed * np.clip((car_stop - t) / 0.8, 0, 1)
        cp, cy = cars.step(1 / FPS)
        stopped = t > car_stop
        car_p[i] = cp
        car_yaw[i] = cy + np.where(stopped, car_jit * smooth_arr((t - car_stop) / 0.6), 0)

    # 고양이: 처음 바깥 12마리 + 건물에서 나오는 반려묘
    door = bld[rs.integers(0, nb, NC), :2] + rs.normal(0, 0.5, (NC, 2))
    cats = Wanderers(rs, NC, R, 0.55, rects, start=door.astype(np.float32))
    hot = np.array(HOTSPOTS, np.float32)
    rat_start = hot[rs.integers(0, len(hot), NR)] + rs.normal(0, 1.2, (NR, 2)).astype(np.float32)
    ratw = Wanderers(rs, NR, R, 0.9, rects, start=rat_start)
    cat_col0 = np.array([(0.86, 0.45, 0.12), (0.04, 0.04, 0.045), (0.92, 0.91, 0.88), (0.46, 0.48, 0.52),
                         (0.93, 0.80, 0.60), (0.48, 0.34, 0.20), (0.75, 0.55, 0.35)], np.float32)
    cat_col = cat_col0[rs.integers(0, len(cat_col0), NC)]
    order = rs.permutation(NC)
    order = np.r_[0, order[order != 0]]  # 주인공 고양이(0)는 항상 있음
    rank = np.empty(NC, int)
    rank[order] = np.arange(NC)
    cat_p = np.zeros((nf, NC, 2), np.float32)
    cat_yaw = np.zeros((nf, NC), np.float32)
    cat_on = np.zeros((nf, NC), np.float32)
    rat_p = np.zeros((nf, NR, 2), np.float32)
    rat_yaw = np.zeros((nf, NR), np.float32)
    rat_on = np.zeros((nf, NR), np.float32)
    cat_vis = np.zeros(NC, np.float32)
    rat_vis = np.zeros(NR, np.float32)
    rat_rank = rs.permutation(NR)
    for i, t in enumerate(ts):
        ncat = min(NC, int(round(pop_C[i])))
        nrat = min(NR, int(round(pop_R[i])))
        rat_alive = rat_vis > 0.5
        cp, cy = cats.step(1 / FPS, seek=ratw.p[rat_alive] if rat_alive.any() else None, seek_r=2.5)
        food = math.exp(-days[i] / 150.0)
        rp, ry = ratw.step(1 / FPS, seek=hot if food > 0.15 else None, seek_r=3.2,
                           flee=cats.p[cat_vis > 0.5], flee_r=1.4, speed_mul=1.2)
        if t >= 44.0:  # 반전: 주인공 고양이는 한 자리에 앉아 있음
            cats.p[0] = np.array(HERO, np.float32)
            cats.v[0] = 0
            cats.yaw[0] = 2.6
            cp[0], cy[0] = cats.p[0], cats.yaw[0]
        cat_vis += (((rank < ncat).astype(np.float32)) - cat_vis) * 0.12
        rat_vis += (((rat_rank < nrat).astype(np.float32)) - rat_vis) * 0.15
        cat_p[i], cat_yaw[i], cat_on[i] = cp, cy, cat_vis
        rat_p[i], rat_yaw[i], rat_on[i] = rp, ry, rat_vis
    tabby = np.clip(np.interp(np.log10(np.maximum(days, 1)), [np.log10(36500), np.log10(3.65e6)], [0, 1]), 0, 1)

    # 나무: 공원 나무 + 도로를 뒤덮는 새 나무
    tree_xy = []
    tries = 0
    while len(tree_xy) < NT and tries < 20000:
        tries += 1
        p = rs.uniform(-R * 0.92, R * 0.92, 2)
        if np.hypot(*p) > R - 0.5:
            continue
        if abs(p[1] - river_y(p[0], RIVER)) < RIVER[2] / 2 + 0.1:
            continue
        q = push_out_of_rects(p[None].astype(np.float32), rects, pad=0.25)[0]
        if np.abs(q - p).sum() > 1e-4:
            continue
        if np.hypot(p[0] - HERO[0], p[1] - HERO[1]) < 3.0:
            continue
        rel = p - np.array(HERO)
        clear = False
        for az in (250 + 46 * 1.2, 268 + 52 * 1.2):
            dv = np.array([math.cos(math.radians(az)), math.sin(math.radians(az))])
            along = rel @ dv
            if 0 < along < 9 and abs(rel[0] * dv[1] - rel[1] * dv[0]) < 1.6 + along * 0.2:
                clear = True
        if clear:
            continue
        tree_xy.append(p)
    tree_xy = np.array(tree_xy, np.float32)
    nt = len(tree_xy)
    tree_birth = np.r_[np.full(50, -1.0), rs.uniform(0.02, 0.95, nt - 50)]
    tree_size = rs.uniform(0.7, 1.5, nt)
    tree_s = np.clip((overgrow[:, None] - tree_birth[None, :]) / 0.12, 0, 1) * tree_size[None]
    tree_s[:, :50] = tree_size[None, :50]
    tree_col = np.array([(0.13, 0.36, 0.10), (0.18, 0.42, 0.12), (0.10, 0.30, 0.12), (0.22, 0.40, 0.10)],
                        np.float32)[rs.integers(0, 4, nt)]
    tree_kind = (rs.random(nt) < 0.3).astype(np.float32)

    # 가로등
    lamp_xy = []
    for i in range(-3, 4):
        for j in range(-3, 4):
            for ox, oy in ((0.45, 0.45), (-0.45, -0.45)):
                p = np.array([i * SPACING + ox + SPACING / 2, j * SPACING + oy], np.float32)
                if np.hypot(*p) < R - 0.8 and abs(p[1] - river_y(p[0], RIVER)) > 1.2:
                    lamp_xy.append(p)
    lamp_xy = np.array(lamp_xy, np.float32)

    # "야옹" 말풍선 사건: 시간에 따라 줄어듦
    events = []
    for c in range(12):
        t = rs.uniform(0, 1.0)
        while t < DUR:
            d = days_at(t)
            rate = 0.55 if d < 2 else (0.32 if d < 40 else (0.06 if d < 400 else 0.0))
            if t > 43.5:
                rate = 0.0
            if rate <= 0:
                t += 0.5
                continue
            t += rs.exponential(1 / rate)
            if t < DUR and days_at(t) < 400 and t < 43.5:
                events.append((c, t))
    meow = np.array(events, np.float32).reshape(-1, 2)

    lights = np.array([keyed(t, WINDOW_KEYS) for t in ts], np.float32)
    bld_lit_f = np.repeat(bld_lit[None], nf, 0)
    bld_lit_f *= np.clip((off_t[None, :] - ts[:, None]) / 0.35 + 1.0, 0, 1)
    rust = np.clip((np.log10(np.maximum(days, 1)) - np.log10(36525 * 1.5)) / 0.5, 0, 1)
    return dict(rust=rust, days=days, bld=bld, bld_col=bld_col, bld_seed=bld_seed, bld_lit=bld_lit_f, bld_h=bld_h,
                bld_rot=bld_rot, ppl_p=ppl_p, ppl_yaw=ppl_yaw, ppl_on=ppl_on, car_p=car_p, car_yaw=car_yaw,
                spark_p=spark_p, spark_on=spark_on, cat_p=cat_p, cat_yaw=cat_yaw, cat_on=cat_on, cat_col=cat_col,
                rat_p=rat_p, rat_yaw=rat_yaw, rat_on=rat_on, tabby=tabby, tree_xy=tree_xy, tree_s=tree_s,
                tree_col=tree_col, tree_kind=tree_kind, lamp_xy=lamp_xy, meow=meow, lights=lights,
                overgrow=overgrow, decay=decay, pop_R=pop_R, pop_C=pop_C, veg=veg,
                ppl_col=rs.uniform(0.15, 0.95, (NP, 3)).astype(np.float32),
                car_col=np.array([(0.75, 0.1, 0.1), (0.1, 0.25, 0.6), (0.85, 0.85, 0.85), (0.1, 0.1, 0.12),
                                  (0.9, 0.7, 0.1)], np.float32)[rs.integers(0, 5, NCAR)])


def smooth_arr(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def hud(t, sim):
    f = fi(t)
    d = float(sim["days"][f])
    C = int(round(sim["pop_C"][f]))
    Rn = int(round(sim["pop_R"][f]))
    right2 = f"이 섬의 고양이 {C} · 쥐 {Rn}" if t > 2.4 else "이 섬의 사람 70 · 고양이 12"
    return {"left": "SIMULATION", "right": "경과 " + fmt_elapsed(d), "right2": right2}


def labels(t, anchors, sim):
    out = []
    for c, t0 in sim["meow"]:
        if t0 <= t < t0 + 1.1:
            a = anchors.get(f"cat{int(c)}")
            if a and a[3] and sim["cat_on"][fi(t)][int(c)] > 0.6:
                u = (t - t0) / 1.1
                out.append({"x": a[0], "y": a[1], "text": "야옹", "color": "yellow", "size": 28,
                            "alpha": min(1, (1 - u) * 4, u * 8), "scale": 0.85 + 0.15 * min(1, u * 6)})
    return out


def build(ctx):
    from engine import bkit as K
    sim = ctx.sim
    K.world_space(ctx, ambient=(0.45, 0.55, 0.78), ambient_strength=0.4)
    sun = K.sun(ctx, 3.0)
    ground = K.mat_ground(ctx, spacing=SPACING, road_w=ROAD_W, river=RIVER, park=0.3)
    K.island(ctx, R, top_mat=ground)
    # 건물
    bld = sim["bld"]
    nb = len(bld)
    pb = K.proto_box(ctx, K.mat_building(ctx, wstr=3.4))
    bo = K.instancer(ctx, "blds", pb, nb, vector_scale=True)
    K.add_attr(bo, "lit")
    K.add_attr(bo, "seed")
    # 사람·불꽃·차
    pp = K.proto_person(ctx, K.mat_inst("m_shirt", 0.7), K.mat_simple("m_skin", (0.85, 0.66, 0.52), 0.6))
    po = K.instancer(ctx, "people", pp, NP)
    sp = K.proto(ctx, "p_spark", K.bm_ico(0.07, sub=1), [K.mat_emit("m_spark", (0.75, 0.9, 1.0), 9.0)])
    so = K.instancer(ctx, "sparks", sp, NP)
    pc = K.proto_car(ctx, K.mat_inst("m_car", 0.35, coat=0.6, ctx=ctx, decay_to=(0.22, 0.12, 0.07)),
                     K.mat_simple("m_glass", (0.05, 0.07, 0.1), 0.1),
                     K.mat_emit("m_head", (1.0, 0.95, 0.8), 6.0, ctx, "carlights"),
                     K.mat_emit("m_tail", (1.0, 0.1, 0.05), 6.0, ctx, "carlights"))
    co = K.instancer(ctx, "cars", pc, NCAR)
    # 고양이(줄무늬 섞기)·쥐
    fur_m, nt, out = K.new_mat("m_fur")
    base = K.inst_attr(nt, "col")
    tco = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    K.ln(nt, tco.outputs["Object"], sep.inputs[0])
    stripe = K.math_node(nt, "GREATER_THAN", K.math_node(nt, "SINE", K.math_node(nt, "MULTIPLY", sep.outputs["X"], 70.0)), 0.25)
    tabby_c = K.mix_rgb(nt, stripe, (0.50, 0.40, 0.28), (0.16, 0.12, 0.08))
    furc = K.mix_rgb(nt, ctx.ctl_node(nt, "tabby", 0.0), base, tabby_c)
    b = K.principled(nt, furc, 0.75)
    b.inputs["Sheen Weight"].default_value = 0.4
    K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    eye = K.mat_emit("m_eye", (0.75, 1.0, 0.35), 4.0, ctx, "eyes")
    pcat = K.proto_cat(ctx, fur_m, eye)
    cato = K.instancer(ctx, "cats", pcat, NC)
    prat = K.proto_rat(ctx, K.mat_simple("m_rat", (0.42, 0.37, 0.33), 0.75))
    rato = K.instancer(ctx, "rats", prat, NR)
    # 나무
    leaf = K.mat_inst("m_leaf", 0.85)
    trunk = K.mat_simple("m_trunk", (0.22, 0.14, 0.08), 0.9)
    tr_round = K.instancer(ctx, "trees_r", K.proto_tree(ctx, leaf, trunk, "round"), len(sim["tree_xy"]))
    tr_pine = K.instancer(ctx, "trees_p", K.proto_tree(ctx, leaf, trunk, "pine"), len(sim["tree_xy"]))
    # 음식물 쓰레기 더미 (남은 음식 F에 따라 줄어듦)
    bag = K.proto(ctx, "p_bag", K.bm_ico(0.16, sub=1, scale=(1, 1, 0.8)),
                  [K.mat_simple("m_bag", (0.09, 0.12, 0.10), 0.25)])
    rsb = np.random.default_rng(5)
    bag_xy = np.concatenate([np.array(h) + rsb.normal(0, 0.35, (14, 2)) for h in HOTSPOTS]).astype(np.float32)
    bago = K.instancer(ctx, "bags", bag, len(bag_xy))
    bag_s = rsb.uniform(0.8, 1.6, len(bag_xy))
    # 가로등
    lamp = K.proto_lamp(ctx, K.mat_simple("m_pole", (0.15, 0.15, 0.17), 0.5),
                        K.mat_emit("m_bulb", (1.0, 0.8, 0.5), 9.0, ctx, "lamps"))
    lo = K.instancer(ctx, "lamps", lamp, len(sim["lamp_xy"]))
    lxy = sim["lamp_xy"]
    txy = sim["tree_xy"]
    kind = sim["tree_kind"]
    rot_t = np.c_[np.zeros((len(txy), 2)), (np.arange(len(txy)) * 2.4) % 6.28]
    cam = K.CamRig(ctx, 32, fstop=9.0)
    import bpy
    sd = bpy.data.lights.new("spot", "AREA")
    sd.size = 2.5
    sd.color = (1.0, 0.85, 0.7)
    sd.energy = 0.0
    spot = K.link(bpy.data.objects.new("spot", sd))
    spot.location = (HERO[0] + 0.6, HERO[1] - 0.4, 3.2)
    zeros = lambda n: np.zeros((n, 3), np.float32)  # noqa: E731

    def upd(t, f):
        tgt, az, el, dist, lens = cam_at(t)
        close = clamp((32 - dist) / 20)
        cam.set(tgt, az + t * 1.2, el, dist, lens, shift=0.07 * (1 - close))
        spot.data.energy = 90.0 * ramp(t, 44.6, 46.0)
        cam.ob.data.dof.aperture_fstop = 9.0 - 4.5 * close
        # 조명
        lk = [(k, (v["elev"], v["az"], v["energy"], *v["col"], v["amb"], *v["amb_col"])) for k, v in LIGHT_KEYS]
        L = keyed(t, lk)
        sun.rotation_euler = (math.radians(90 - L[0]), 0, math.radians(L[1]))
        sun.data.energy = L[2]
        sun.data.color = L[3:6]
        ctx.set_ctl("ambient", L[6])
        ctx.set_rgb("ambient_col", L[7:10])
        night = clamp((0.3 - L[6]) / 0.2)
        ctx.set_ctl("lights", float(sim["lights"][f]))
        ctx.set_ctl("lamps", float(clamp((12.0 - t) / 1.2)) * (0.3 + 0.7 * night))
        ctx.set_ctl("carlights", float(clamp((2.6 - t) / 0.6)))
        ctx.set_ctl("eyes", 0.3 + 3.5 * night)
        ctx.set_ctl("overgrow", float(sim["overgrow"][f]))
        ctx.set_ctl("decay", float(sim["decay"][f]))
        ctx.set_ctl("tabby", float(sim["tabby"][f]))
        # 건물
        K.set_points(bo, np.c_[bld[:, :2], np.zeros(nb)], scale=np.ones(nb),
                     size=np.c_[bld[:, 2:4], sim["bld_h"][f]], rot=sim["bld_rot"][f], col=sim["bld_col"],
                     lit=sim["bld_lit"][f], seed=sim["bld_seed"])
        K.set_points(po, np.c_[sim["ppl_p"][f], np.zeros(NP)], scale=sim["ppl_on"][f] * 1.05,
                     rot=np.c_[np.zeros((NP, 2)), sim["ppl_yaw"][f]], col=sim["ppl_col"])
        K.set_points(so, sim["spark_p"][f], scale=sim["spark_on"][f] * 1.4, rot=zeros(NP), col=np.ones((NP, 3)))
        gone = 1.0 - float(sim["rust"][f])
        food = math.exp(-float(sim["days"][f]) / 150.0)
        K.set_points(bago, np.c_[bag_xy, np.full(len(bag_xy), 0.05)], scale=bag_s * min(1.0, food * 1.6),
                     rot=np.zeros((len(bag_xy), 3)), col=np.ones((len(bag_xy), 3)))
        K.set_points(lo, np.c_[lxy, np.zeros(len(lxy))], scale=np.full(len(lxy), 1.4 * gone),
                     rot=np.zeros((len(lxy), 3)), col=np.ones((len(lxy), 3)))
        K.set_points(co, np.c_[sim["car_p"][f], np.zeros(NCAR)], scale=np.full(NCAR, 1.3 * gone),
                     rot=np.c_[np.zeros((NCAR, 2)), sim["car_yaw"][f]], col=sim["car_col"])
        K.set_points(cato, np.c_[sim["cat_p"][f], np.zeros(NC)], scale=sim["cat_on"][f] * 1.85,
                     rot=np.c_[np.zeros((NC, 2)), sim["cat_yaw"][f]], col=sim["cat_col"])
        K.set_points(rato, np.c_[sim["rat_p"][f], np.zeros(NR)], scale=sim["rat_on"][f] * 1.7,
                     rot=np.c_[np.zeros((NR, 2)), sim["rat_yaw"][f]], col=np.ones((NR, 3)))
        ts_ = sim["tree_s"][f]
        K.set_points(tr_round, np.c_[txy, np.zeros(len(txy))], scale=ts_ * (kind < 0.5), rot=rot_t,
                     col=sim["tree_col"])
        K.set_points(tr_pine, np.c_[txy, np.zeros(len(txy))], scale=ts_ * (kind >= 0.5), rot=rot_t,
                     col=sim["tree_col"])

    ctx.on_frame(upd)
    for c in range(12):
        ctx.anchor(f"cat{c}", (lambda c: lambda t: (float(sim["cat_p"][fi(t)][c][0]),
                                                    float(sim["cat_p"][fi(t)][c][1]), 0.75))(c))
