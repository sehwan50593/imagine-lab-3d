"""EP05 만약 남한과 북한이 전쟁을 한다면? (가상 시나리오) — 10-28 장면형 개편

공격 → 방어 → 동맹 → 북진 → 변수 → 결과를 장면마다 8초씩, 한 단계에 한 가지 원리만 보여준다.
실제로 계산하는 것:
- NOAA ETOPO1 한반도 지형 + Natural Earth 군사분계선 + 도시 인구로 만든 야경
- 장사정포 진지(48곳)마다 사격 일정 → 포탄 궤적(꼬리)·착탄·화재. 살아남은 진지 수만큼만 쏜다
- 탄도미사일은 패트리엇·천궁 포대에서 요격탄이 떠서 공중에서 만남(요격률 가정 80%)
- K9 대포병 사격·전투기 폭격이 진지를 하나씩 지움 → 서울로 오는 포탄이 줄어듦
- 항공모함 전단 이동, 전투기 비행, 전선(북진), 국경을 넘는 중국군 입자
숫자: 2022 국방백서(한국군 50만·북한군 128만), 주한미군 약 2.85만, 미 의회조사국 R44994(2017).
"""
import json
import math

import numpy as np

from engine.common import ASSETS, FPS, Beat, frames_of, keyed, ramp

DUR = 56.0
META = {"id": "ep05", "title": "만약 남한과 북한이 전쟁을 한다면?", "duration": DUR,
        "music": {"key": "C", "mode": "major", "bpm": 64, "seed": 25, "twist_at": 44.0}}
STYLE = "bench"
S = 1.6
EXAG = 0.00032
LAT0, LON0 = 38.0, 127.5
BOX = (33.0, 43.2, 124.0, 131.0)  # 위도, 경도 범위
NART, NK9, NBAT, NTK, NFR = 48, 24, 6, 30, 110
TRAIL = 6
NPT, NFL, NFIRE, NJET, NSHIP, NCH = 1500, 320, 700, 26, 6, 170
RED, BLUE = (1.0, 0.32, 0.12), (0.35, 0.72, 1.0)

BEATS = [
    Beat(0.0, 7.0, badge="가상 시나리오", title="남북 전쟁이 일어난다면?",
         sub="한국군 50만 명, 북한군 128만 명이\n휴전선을 사이에 두고 마주 서 있습니다."),
    Beat(7.0, 15.0, badge="1단계", title="1단계 {red}장사정포{/} 공격",
         sub="휴전선 북쪽 산속 진지에서 포탄과 로켓이\n50km 떨어진 서울로 쏟아집니다."),
    Beat(15.0, 23.0, badge="2단계", title="2단계 {blue}막고, 되쏜다{/}",
         sub="미사일은 패트리엇·천궁이 공중에서 막고,\n포 진지는 K9 자주포가 찾아내 부숩니다."),
    Beat(23.0, 31.0, badge="3단계", title="3단계 {blue}미군 합류{/}",
         sub="주한미군 2만 8천여 명에 더해\n미 항공모함과 전투기가 바다를 건너옵니다."),
    Beat(31.0, 39.0, badge="4단계", title="4단계 하늘 장악 → {blue}북진{/}",
         sub="전투기가 먼저 하늘을 잡으면\n지상군이 휴전선을 넘어 북쪽으로 올라갑니다."),
    Beat(39.0, 47.0, badge="5단계", title="변수: {red}중국{/}",
         sub="1950년처럼 중국군이 국경을 넘어오면\n전쟁은 다시 길어질 수 있습니다."),
    Beat(47.0, 52.0, badge="결과", title="이겨도 {red}잃는 것{/}",
         sub="많은 분석은 한미연합군이 결국 이긴다고 보지만\n첫 며칠에만 3만~30만 명이 숨질 수 있습니다."),
    Beat(52.0, 56.0, badge="지금", title="이 시뮬레이션은\n{green}영원히 돌리지 않기를{/}", title_size=72,
         sub="1953년 정전 이후 73년,\n휴전선은 지금도 멈춰 있습니다."),
]
GRADE = {"exposure": 1.05, "bloom": 0.2, "bloom_thr": 1.0, "bloom_radius": 1.2, "vignette": 0.34}
# 장면 안에서는 천천히, 장면 사이에서만 시간이 건너뜀 (분, 새벽 4시 기준)
CLOCK = [(0.0, 0.0), (7.0, 1.0), (7.01, 2.0), (15.0, 10.0), (15.01, 12.0), (23.0, 20.0),
         (23.01, 1440 + 300.0), (31.0, 2 * 1440 + 600.0), (31.01, 7 * 1440.0), (39.0, 30 * 1440.0),
         (39.01, 32 * 1440.0), (47.0, 40 * 1440.0)]


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
    return pts[np.argsort(pts[:, 0])]


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def orbit(target, az, el, dist):
    a, e = math.radians(az), math.radians(el)
    t = np.asarray(target, np.float32)
    return t + np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)], np.float32) * dist


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
        """지형 높이(가장 가까운 격자) — 부대·불을 땅 위에 얹기."""
        xy = np.asarray(xy, np.float32)
        lat = LAT0 + xy[..., 1] / S
        lon = LON0 + xy[..., 0] / (S * math.cos(math.radians(LAT0)))
        r = np.clip(np.round((lats[0] - lat) / cell), 0, len(lats) - 1).astype(int)
        c = np.clip(np.round((lon - lons[0]) / cell), 0, len(lons) - 1).astype(int)
        return np.maximum(Z[r, c], 0.0)

    def on_ground(xy, lift=0.0):
        xy = np.asarray(xy, np.float32)
        return np.concatenate([xy, (hz(xy) + lift)[..., None]], -1).astype(np.float32)

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
    dmz_x, dmz_y = dmz_xy[:, 0], dmz_xy[:, 1]
    seoul = to_xy(37.5665, 126.978)

    def dmz_at(x):
        return np.interp(x, dmz_x, dmz_y)

    # ── 부대 배치 ──
    ax = rs.uniform(to_xy(38, 126.35)[0], to_xy(38, 127.55)[0], NART)
    art = np.c_[ax, dmz_at(ax) + rs.uniform(0.08, 0.5, NART)].astype(np.float32)   # 휴전선 북쪽 산속
    kx = rs.uniform(to_xy(38, 126.7)[0], to_xy(38, 127.4)[0], NK9)
    k9 = np.c_[kx, np.minimum(dmz_at(kx) - rs.uniform(0.1, 0.3, NK9), seoul[1] + 0.45)].astype(np.float32)
    bat = (seoul + np.array([[0.25, 0.05], [-0.2, 0.1], [0.05, 0.25], [0.3, -0.2], [-0.25, -0.15], [0.0, -0.3]])
           ).astype(np.float32)
    # ── 진지 파괴 시각: K9이 서울에서 가까운 순서로, 남은 건 전투기가 ──
    order = np.argsort(np.hypot(*(art - seoul).T))
    kill_t = np.full(NART, 1e9, np.float32)
    shots = []   # (t0, dur, p0, p1, h, kind, art, 요격 u)  kind: 0 포탄 1 미사일 2 요격탄 3 K9
    k9_times = np.r_[np.linspace(15.6, 22.6, 28), np.linspace(23.4, 30.0, 10)]
    for tk, j in zip(k9_times, order[:len(k9_times)]):
        src = k9[rs.integers(0, NK9)]
        shots.append((tk, 1.5, src, art[j], 0.32, 3, int(j), 1.0))
        kill_t[j] = tk + 1.5
    jet_targets = order[len(k9_times):]
    # ── 전투기: 항모·평택·남동쪽(일본)에서 출발 → 남은 진지 폭격, 나머지는 북쪽 깊숙이 ──
    carrier0, carrier1 = to_xy(36.85, 130.95), to_xy(37.35, 130.05)
    origins = [to_xy(36.97, 127.03), to_xy(33.6, 130.9)]
    jets = []
    for i in range(NJET):
        t0 = rs.uniform(25.5, 37.0)
        if i < len(jet_targets):
            j = int(jet_targets[i])
            tgt = art[j]
            t0 = rs.uniform(25.5, 31.5)
        else:
            j = -1
            tgt = to_xy(rs.uniform(38.8, 40.0), rs.uniform(125.4, 127.6))
        o = (carrier0 + (carrier1 - carrier0) * min(1.0, (t0 - 23) / 8)) if i % 3 == 0 else origins[i % 3 - 1]
        o = np.asarray(o, np.float32)
        dur = float(np.hypot(*(tgt - o))) / 1.6
        jets.append((t0, dur, o, np.asarray(tgt, np.float32), j))
        if j >= 0:
            kill_t[j] = t0 + dur
    # ── 북한 사격 일정: 살아 있는 진지만 쏜다 ──
    for j in range(NART):
        t = 7.2 + rs.exponential(1.2)
        while t < min(kill_t[j], 33.0):
            tgt = seoul + rs.normal(0, 0.16, 2) * np.array([1.3, 1.0])
            shots.append((t, rs.uniform(2.4, 3.2), art[j], tgt, rs.uniform(0.35, 0.55), 0, -1, 1.0))
            t += rs.exponential(4.5)
    # 탄도미사일: 더 북쪽에서 높게 → 2단계부터 80% 요격
    for i in range(16):
        t0 = rs.uniform(7.5, 27.0)
        src = to_xy(rs.uniform(38.9, 39.6), rs.uniform(125.6, 127.2))
        tgt = seoul + rs.normal(0, 0.12, 2)
        u_hit = rs.uniform(0.72, 0.82) if (t0 > 13.0 and rs.random() < 0.8) else 1.0
        shots.append((t0, 3.6, src, tgt, 1.5, 1, -1, u_hit))
        if u_hit < 1:
            meet_t = t0 + 3.6 * u_hit
            b = bat[np.argmin(np.hypot(*(bat - tgt).T))]
            shots.append((meet_t - 1.1, 1.1, b, (src, tgt, 1.5, u_hit), 0.0, 2, -1, 1.0))
    shots.sort(key=lambda s: s[0])

    def arc(p0, p1, h, u):
        u = np.asarray(u, np.float32)
        p = p0[None] + (p1 - p0)[None] * u[:, None]
        z0, z1 = hz(p0), hz(p1)
        return np.c_[p, z0 + (z1 - z0) * u + h * 4 * u * (1 - u)]

    pt_p = np.zeros((nf, NPT, 3), np.float32)
    pt_s = np.zeros((nf, NPT), np.float32)
    pt_c = np.zeros((nf, NPT, 3), np.float32)
    fl_p = np.zeros((nf, NFL, 3), np.float32)
    fl_s = np.zeros((nf, NFL), np.float32)
    fl_c = np.zeros((nf, NFL, 3), np.float32)
    flashes = []    # (t, xyz, 크기, 색)
    fires = []      # (t, xyz)
    red_hits, blue_hits = [], []
    for t0, dur, p0, p1, h, kind, j, uh in shots:
        if kind == 2:      # 요격: 미사일과 만나는 자리에서 공중 폭발
            src, tgt, mh, mu = p1
            flashes.append((t0 + dur, arc(src, tgt, mh, [mu])[0], 1.6, (0.8, 0.9, 1.0)))
            continue
        if kind == 1 and uh < 1:
            continue
        end = arc(p0, p1, h, [1.0])[0]
        flashes.append((t0 + dur, end + np.array([0, 0, 0.01]), 1.0 if kind == 0 else 1.5,
                        (1.0, 0.6, 0.3) if kind in (0, 1) else (0.7, 0.85, 1.0)))
        fires.append((t0 + dur, end))
        (red_hits if kind in (0, 1) else blue_hits).append(t0 + dur)
    for t0, dur, o, tgt, j in jets:
        if j >= 0:
            e_ = np.r_[tgt, hz(tgt)]
            flashes.append((t0 + dur, e_ + np.array([0, 0, 0.01]), 1.8, (1.0, 0.75, 0.4)))
            fires.append((t0 + dur, e_))
            blue_hits.append(t0 + dur)
    trail_u = np.arange(TRAIL, dtype=np.float32) * 0.035
    trail_s = np.linspace(1.0, 0.25, TRAIL).astype(np.float32)
    for i, t in enumerate(ts):
        k = 0
        for t0, dur, p0, p1, h, kind, j, uh in shots:
            if t < t0 or k + TRAIL > NPT:
                continue
            u = (t - t0) / dur
            if kind == 2:
                if u >= 1:
                    continue
                src, tgt, mh, mu = p1
                meet = arc(src, tgt, mh, [mu])[0]
                uu = np.clip(u - trail_u * 2, 0, 1)
                b0 = np.r_[p0, hz(p0)]
                q = b0[None] + (meet - b0)[None] * uu[:, None]
                q[:, 2] += 0.15 * np.sin(uu * math.pi)
                col = BLUE
            else:
                if u >= uh:
                    continue
                q = arc(p0, p1, h, np.clip(u - trail_u, 0, 1))
                col = RED if kind in (0, 1) else BLUE
            pt_p[i, k:k + TRAIL] = q
            pt_s[i, k:k + TRAIL] = trail_s * (1.6 if kind == 1 else 1.0)
            pt_c[i, k:k + TRAIL] = col
            k += TRAIL
        m = 0
        for tf, p, sz, c in flashes:
            v = (t - tf) / 0.6
            if 0 <= v < 1 and m < NFL:
                fl_p[i, m] = p
                fl_s[i, m] = sz * (0.4 + 1.6 * v) * (1 - v)
                fl_c[i, m] = c
                m += 1
    fires = sorted(fires, key=lambda f: f[0])[:NFIRE]
    fr_p = np.zeros((NFIRE, 3), np.float32)
    fr_t = np.full(NFIRE, 1e9, np.float32)
    for q, (tt, p) in enumerate(fires):
        fr_p[q] = p + np.r_[rs.normal(0, 0.02, 2), 0.01]
        fr_t[q] = tt
    fire_s = np.clip((ts[:, None] - fr_t[None]) / 0.4, 0, 1) * (1 - 0.8 * smooth((ts[:, None] - 50.0) / 4.0))
    # 도시 전력: 착탄이 쌓일수록 불이 꺼짐
    rh = np.searchsorted(np.sort(red_hits), ts) / max(len(red_hits), 1)
    bh = np.searchsorted(np.sort(blue_hits), ts) / max(len(blue_hits), 1)
    south = 1.0 - 0.5 * rh
    north = 1.0 - 0.75 * bh
    # ── 전투기 위치 ──
    jt_p = np.zeros((nf, NJET, 3), np.float32)
    jt_s = np.zeros((nf, NJET), np.float32)
    jt_r = np.zeros((nf, NJET, 3), np.float32)
    for q, (t0, dur, o, tgt, j) in enumerate(jets):
        d = tgt - o
        u = (ts - t0) / dur
        jt_p[:, q, :2] = o[None] + d[None] * u[:, None]
        jt_p[:, q, 2] = 0.42 + 0.05 * np.sin(u * 3)
        jt_s[:, q] = ((u >= 0) & (u < 1.6)) * np.clip(np.minimum(u * 6 + 0.2, (1.6 - u) * 4), 0, 1)
        jt_r[:, q, 2] = math.atan2(d[1], d[0])
    # ── 항모 전단 ──
    sh_off = np.array([[0, 0], [0.12, 0.15], [-0.1, -0.13], [0.22, -0.05], [-0.2, 0.12], [0.3, 0.2]], np.float32)
    ship_u = smooth((ts - 23.0) / 8.0)
    car = carrier0[None] + (carrier1 - carrier0)[None] * ship_u[:, None]
    sp_p = np.zeros((nf, NSHIP, 3), np.float32)
    sp_p[:, :, :2] = car[:, None, :] + sh_off[None]
    sp_s = np.tile(np.array([1.0, 1.0, 0.45, 0.45, 0.45, 0.45], np.float32), (nf, 1)) * \
        ((ts >= 22.5) & (ts < 47))[:, None]
    yaw_c = math.atan2(*(carrier1 - carrier0)[::-1])
    # ── 전선(북진): 휴전선에서 평양 북쪽까지 ──
    fx0 = np.linspace(dmz_x.min() + 0.02, dmz_x.max() - 0.02, NFR)
    fstart = np.c_[fx0, dmz_at(fx0)]
    a_, b_ = to_xy(39.45, 125.15), to_xy(39.2, 127.5)
    fend = a_[None] + (b_ - a_)[None] * np.linspace(0, 1, NFR)[:, None]
    fend[:, 1] += 0.06 * np.sin(np.linspace(0, 9, NFR))
    adv = smooth((ts - 31.6) / 7.0)
    fr_line = fstart[None] + (fend - fstart)[None] * adv[:, None, None]
    fl_vis = ((ts >= 31.0) & (ts < 47.0)).astype(np.float32)
    front = np.zeros((nf, NFR, 3), np.float32)
    front[:, :, :2] = fr_line
    front[:, :, 2] = hz(fr_line) + 0.03
    ti = np.linspace(2, NFR - 3, NTK).astype(int)
    tanks = np.zeros((nf, NTK, 3), np.float32)
    tanks[:, :, :2] = fr_line[:, ti] - np.array([0, 0.07])
    tanks[:, :, 2] = hz(tanks[:, :, :2])
    fcen = front[:, :, :2].mean(1)
    # ── 중국 국경을 넘는 입자 (변수) ──
    yalu = np.array([to_xy(40.1, 124.4), to_xy(40.6, 125.2), to_xy(41.15, 126.3), to_xy(41.4, 127.4),
                     to_xy(41.7, 128.2)])
    seg = rs.integers(0, len(yalu) - 1, NCH)
    w = rs.random(NCH)[:, None]
    cb = yalu[seg] + (yalu[seg + 1] - yalu[seg]) * w + np.array([0, 0.12])
    ct0 = rs.uniform(39.6, 45.5, NCH)
    cv = np.c_[rs.normal(0.05, 0.05, NCH), -rs.uniform(0.09, 0.15, NCH)]
    ch_p = np.zeros((nf, NCH, 3), np.float32)
    ch_s = np.zeros((nf, NCH), np.float32)
    for i, t in enumerate(ts):
        p = cb + cv * np.clip(t - ct0, 0, None)[:, None]
        ch_p[i, :, :2] = p
        ch_p[i, :, 2] = hz(p) + 0.03
        ch_s[i] = (t >= ct0) * (t < 47.0)
    # ── 카메라: 장면마다 한 자리, 컷은 장면 사이에서만 ──
    center = np.r_[to_xy(37.9, 127.3), 0.0]
    cam_l = np.zeros((nf, 3), np.float32)
    cam_t = np.zeros((nf, 3), np.float32)
    lens = np.zeros(nf, np.float32)
    for i, t in enumerate(ts):
        if t < 7.0:
            u = t / 7.0
            tg = center
            cl = orbit(center, -90, 60 - 4 * u, 20 - 3 * u)
            ln_ = 30
        elif t < 15.0:          # 서울 뒤 낮은 하늘에서 휴전선 쪽을 보는 눈 (포탄이 넘어오는 방향)
            u = (t - 7.0) / 8.0
            tg = np.r_[to_xy(37.95, 127.0), 0.15]
            cl = orbit(tg, -95, 16 + 2 * u, 2.6 - 0.2 * u)
            ln_ = 28
        elif t < 23.0:          # 서울 위에서 휴전선 쪽을 보는 3인칭
            u = (t - 15.0) / 8.0
            tg = np.r_[to_xy(37.85, 127.0), 0.0]
            cl = orbit(tg, -112, 32, 4.3 - 0.4 * u)
            ln_ = 28
        elif t < 31.0:          # 항모 뒤를 따라가는 시점
            c3 = np.r_[car[i], 0.0]
            cl = c3 + np.array([0.5, -0.22, 0.12])
            tg = c3 + np.array([-2.6, 0.25, 0.0])
            ln_ = 26
        elif t < 39.0:          # 전선 뒤에서 북쪽을 보는 시점
            c3 = np.r_[fcen[i], 0.0]
            cl = c3 + np.array([0.0, -1.05, 0.5])
            tg = c3 + np.array([0.0, 1.9, 0.0])
            ln_ = 26
        elif t < 47.0:
            u = (t - 39.0) / 8.0
            tg = np.r_[to_xy(40.0, 126.4), 0.0]
            cl = orbit(tg, -90, 50 - 4 * u, 9.5 - 1.0 * u)
            ln_ = 30
        elif t < 52.0:
            u = (t - 47.0) / 5.0
            tg = center
            cl = orbit(center, -90, 62, 23 - 1.5 * u)
            ln_ = 30
        else:
            u = (t - 52.0) / 4.0
            tg = np.r_[to_xy(38.15, 127.2), 0.0]
            cl = orbit(tg, -85, 46, 9.0 - 0.8 * u)
            ln_ = 30
        cam_l[i], cam_t[i], lens[i] = cl, tg, ln_
    alive = (ts[:, None] < kill_t[None]).astype(np.float32)
    clock = np.array([keyed(t, CLOCK, ease=lambda u: u) for t in ts], np.float32)
    return dict(X=X.astype(np.float32), Y=Y.astype(np.float32), Z=Z.astype(np.float32), dmz=dmz_xy.astype(np.float32),
                dmz_z=(hz(dmz_xy) + 0.045).astype(np.float32), bbox=np.array([x0, x1, y0, y1], np.float32),
                pt_p=pt_p, pt_s=pt_s, pt_c=pt_c, fl_p=fl_p, fl_s=fl_s, fl_c=fl_c, fr_p=fr_p,
                fire_s=fire_s.astype(np.float32), south=south.astype(np.float32), north=north.astype(np.float32),
                jt_p=jt_p, jt_s=jt_s, jt_r=jt_r, sp_p=sp_p, sp_s=sp_s, yaw_c=np.float32(yaw_c),
                front=front, fl_vis=fl_vis, tanks=tanks, ch_p=ch_p, ch_s=ch_s,
                units=on_ground(np.r_[art, k9, bat]), alive=alive, cam_l=cam_l, cam_t=cam_t, lens=lens, clock=clock,
                art=on_ground(art), k9=on_ground(k9), bat=on_ground(bat),
                carc=np.c_[car, np.full(nf, 0.05)].astype(np.float32), fcen=fcen.astype(np.float32))


def counter(t, sim):
    if t >= 52.0:
        return "정전", "73년째"
    if t >= 47.0:
        return "시뮬레이션", "결과"
    m = float(sim["clock"][fi(t)])
    d, rem = divmod(int(m) + 240, 1440)
    if d == 0:
        return "D-DAY", f"{rem // 60:02d}:{rem % 60:02d}"
    return "경과", f"D+{d}"


def labels(t, anchors, sim):
    f = fi(t)
    n_art = int(sim["alive"][f, :NART].sum())
    items = [("seoul", "서울", "white", 0.5, 31.0), ("pyongyang", "평양", "white", 0.5, 7.0),
             ("pyongyang", "평양", "white", 31.0, 47.0), ("dmz", "휴전선", "red", 0.5, 15.0),
             ("art", f"장사정포 진지 {n_art}곳", "red", 1.0, 31.0), ("k9", "K9 자주포", "blue", 15.3, 23.0),
             ("bat", "패트리엇·천궁", "blue", 15.3, 23.0), ("car", "미 항공모함 전단", "blue", 23.3, 31.0),
             ("osan", "주한미군 (평택)", "blue", 23.3, 31.0), ("front", "한미연합군 전선", "blue", 31.3, 47.0),
             ("china", "중국 국경", "red", 39.3, 47.0), ("dmz", "휴전선", "green", 52.3, 56.0)]
    out = []
    for key, nm, col, t0, t1 in items:
        a = anchors.get(key)
        if a and a[3] and t0 <= t < t1 and (key != "art" or n_art > 0):
            out.append({"x": min(960.0, max(130.0, a[0])), "y": a[1], "text": nm, "color": col, "size": 34,
                        "lift": 10, "alpha": min(ramp(t, t0, t0 + 0.5), 1 - ramp(t, t1 - 0.4, t1))})
    return out


def build(ctx):
    import bpy
    from engine import bkit as K
    sim = ctx.sim
    K.world_space(ctx, ambient=(0.25, 0.3, 0.5), ambient_strength=0.08)
    K.sun(ctx, 0.5, color=(0.6, 0.7, 1.0), rot=(50, 0, -140), angle=2.0)
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
    col = K.mix_rgb(nt, 0.45, ramp_.outputs["Color"], (0.05, 0.06, 0.1), "MULTIPLY")
    b = K.principled(nt, col, 0.85, emit=(1.0, 0.72, 0.38), estr=K.math_node(nt, "MULTIPLY", glow, 4.5))
    K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    K.grid_mesh("terrain", X, Y, Z, m, skirt_z=-0.3)
    K.box_obj("sea", x0 - 0.01, x1 + 0.01, y0 - 0.01, y1 + 0.01, -0.3, 0.0, K.mat_water(color=(0.01, 0.03, 0.08)))
    K.box_obj("base", x0, x1, y0, y1, -0.55, -0.3, K.mat_earth_side())
    # 군사분계선 (마지막에 초록으로)
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

    def glow_mat(name, strength):
        mm, nt_, out_ = K.new_mat(name)
        em_ = nt_.nodes.new("ShaderNodeEmission")
        K.ln(nt_, K.inst_attr(nt_, "col"), em_.inputs["Color"])
        em_.inputs["Strength"].default_value = strength
        K.ln(nt_, em_.outputs[0], out_.inputs["Surface"])
        mm.cycles.emission_sampling = "NONE"
        return mm

    pts = K.instancer(ctx, "projectiles", K.proto(ctx, "p_pt", K.bm_ico(0.011, sub=1), [glow_mat("m_pt", 8.0)]), NPT)
    fls = K.instancer(ctx, "flashes", K.proto(ctx, "p_fl", K.bm_ico(0.035, sub=2), [glow_mat("m_fl", 5.0)]), NFL)
    fro = K.instancer(ctx, "fires", K.proto(ctx, "p_fire", K.bm_ico(0.010, sub=1),
                                             [K.mat_emit("m_fire", (1.0, 0.4, 0.12), 3.5, ctx, "fire")]), NFIRE)
    # 부대 표식: 진지(빨강)·K9·포대(파랑) — 스스로 빛나서 밤에도 보이게
    um = K.mat_inst("m_unit", 0.5, emit_attr="glow", emit_color=(1, 1, 1), emit_strength=2.5)
    uo = K.instancer(ctx, "units", K.proto_box(ctx, um, "p_unit"), NART + NK9 + NBAT, vector_scale=True)
    K.add_attr(uo, "glow")
    tank_bm = K.join_bms([(K.bm_cube(0.03, 0.02, 0.01, bottom=True), 0),
                          (K.bm_cube(0.014, 0.012, 0.007, (0, 0, 0.01), True), 0),
                          (K.bm_cube(0.024, 0.004, 0.003, (0.016, 0, 0.013), True), 0)])
    tko = K.instancer(ctx, "tanks", K.proto(ctx, "p_tank", tank_bm,
                                             [K.mat_simple("m_tank", (0.25, 0.45, 0.8), 0.5, emit=BLUE, estr=0.6)]), NTK)
    frl = K.instancer(ctx, "front", K.proto(ctx, "p_front", K.bm_ico(0.008, sub=1),
                                             [K.mat_emit("m_front", BLUE, 4.0)]), NFR)
    jet_bm = K.join_bms([(K.bm_cube(0.07, 0.012, 0.008), 0), (K.bm_cube(0.022, 0.07, 0.003, (-0.006, 0, 0)), 0),
                         (K.bm_cube(0.012, 0.03, 0.003, (-0.03, 0, 0)), 0), (K.bm_ico(0.005, (0.035, 0, 0), 1), 1)])
    jto = K.instancer(ctx, "jets", K.proto(ctx, "p_jet", jet_bm,
                                            [K.mat_simple("m_jet", (0.75, 0.78, 0.82), 0.4, emit=(0.5, 0.7, 1.0), estr=0.8),
                                             K.mat_emit("m_jetled", (0.6, 0.9, 1.0), 12.0)]), NJET)
    ship_bm = K.join_bms([(K.bm_cube(0.35, 0.08, 0.026, bottom=True), 0),
                          (K.bm_cube(0.055, 0.018, 0.035, (0.045, -0.026, 0.026), True), 0),
                          (K.bm_cube(0.26, 0.006, 0.004, (0, 0, 0.027), True), 1)])
    spo = K.instancer(ctx, "ships", K.proto(ctx, "p_ship", ship_bm, [K.mat_simple("m_ship", (0.42, 0.45, 0.5), 0.5),
                                                                     K.mat_emit("m_deck", (0.7, 0.85, 1.0), 1.2)]), NSHIP)
    cho = K.instancer(ctx, "china", K.proto(ctx, "p_ch", K.bm_ico(0.014, sub=1), [K.mat_emit("m_ch", RED, 8.0)]), NCH)
    cam = K.CamRig(ctx, 30, fstop=0)
    U = sim["units"]
    nu = len(U)
    ucol = np.r_[np.tile(RED, (NART, 1)), np.tile(BLUE, (NK9, 1)), np.tile((0.55, 0.9, 1.0), (NBAT, 1))]
    usize = np.r_[np.tile((0.045, 0.045, 0.025), (NART, 1)), np.tile((0.035, 0.035, 0.02), (NK9, 1)),
                  np.tile((0.05, 0.05, 0.04), (NBAT, 1))]
    fp = sim["fr_p"]

    def upd(t, f):
        cam.look(sim["cam_l"][f], sim["cam_t"][f], float(sim["lens"][f]))
        ctx.set_ctl("south", float(sim["south"][f]))
        ctx.set_ctl("north", float(sim["north"][f]))
        g = ramp(t, 52.0, 53.5)
        ctx.set_rgb("dmz_col", (1.0 - 0.6 * g, 0.25 + 0.75 * g, 0.2 + 0.25 * g))
        ctx.set_ctl("dmz_str", 3.0 + 2.0 * g)
        ctx.set_ctl("fire", 1.0 - 0.6 * ramp(t, 50.0, 54.0))
        K.set_points(pts, sim["pt_p"][f], scale=sim["pt_s"][f], rot=np.zeros((NPT, 3)), col=sim["pt_c"][f])
        K.set_points(fls, sim["fl_p"][f], scale=sim["fl_s"][f], rot=np.zeros((NFL, 3)), col=sim["fl_c"][f])
        K.set_points(fro, fp, scale=sim["fire_s"][f], rot=np.zeros((NFIRE, 3)), col=np.ones((NFIRE, 3)))
        vis = np.r_[sim["alive"][f], np.full(NK9 + NBAT, 1.0 if t < 47.0 else 0.0)]
        K.set_points(uo, U, scale=vis, size=usize, rot=np.zeros((nu, 3)), col=ucol, glow=np.ones(nu))
        fv = float(sim["fl_vis"][f])
        K.set_points(tko, sim["tanks"][f], scale=np.full(NTK, fv),
                     rot=np.tile((0, 0, math.pi / 2), (NTK, 1)), col=np.ones((NTK, 3)))
        K.set_points(frl, sim["front"][f], scale=np.full(NFR, fv), rot=np.zeros((NFR, 3)), col=np.ones((NFR, 3)))
        K.set_points(jto, sim["jt_p"][f], scale=sim["jt_s"][f] * 1.4, rot=sim["jt_r"][f], col=np.ones((NJET, 3)))
        K.set_points(spo, sim["sp_p"][f], scale=sim["sp_s"][f], rot=np.tile((0, 0, float(sim["yaw_c"])), (NSHIP, 1)),
                     col=np.ones((NSHIP, 3)))
        K.set_points(cho, sim["ch_p"][f], scale=sim["ch_s"][f], rot=np.zeros((NCH, 3)), col=np.ones((NCH, 3)))

    ctx.on_frame(upd)

    def fixed(lat, lon, z=0.25):
        xy = to_xy(lat, lon)
        return lambda t: (float(xy[0]), float(xy[1]), z)

    def mean_of(key, z=0.12):
        c = sim[key].mean(0)
        return lambda t: (float(c[0]), float(c[1]), float(c[2]) + z)

    def art_anchor(t):
        al = sim["alive"][fi(t), :NART] > 0
        p = sim["art"][al].mean(0) if al.any() else sim["art"].mean(0)
        return float(p[0]), float(p[1]), float(p[2]) + 0.12

    ctx.anchor("seoul", fixed(37.5665, 126.978))
    ctx.anchor("pyongyang", fixed(39.0392, 125.7625))
    ctx.anchor("dmz", fixed(38.28, 127.6))
    ctx.anchor("china", fixed(41.2, 126.6, 0.35))
    ctx.anchor("osan", fixed(36.97, 127.03, 0.15))
    ctx.anchor("k9", mean_of("k9"))
    ctx.anchor("bat", mean_of("bat", 0.18))
    ctx.anchor("art", art_anchor)
    ctx.anchor("car", lambda t: tuple(float(v) for v in sim["carc"][fi(t)] + np.array([0, 0, 0.06])))
    ctx.anchor("front", lambda t: (float(sim["fcen"][fi(t)][0]), float(sim["fcen"][fi(t)][1]) + 0.25, 0.25))
