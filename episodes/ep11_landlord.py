"""EP11 만약 전쟁이 끝난 후 건물주들은 어떻게 될까? (서울 압구정동)

실제로 계산하는 것:
- 피난과 빈방: 주민(에이전트)이 떠나고 돌아오는 비율 → 건물마다 불 꺼진 창(빈방)
- 불길 번짐: 맞닿은 건물로 옮겨붙는 확률 모형 → 1952년 서울 주택 피해율 28.8%에 이르면 멈춤
  (전소·전파 63% / 반소·반파 37%, 1952 서울특별시 시세일람 비율)
- 돈의 가치: 1950~52 서울 도매물가(+56%·+531%·+117%)를 달마다 복리로 → 현금 1억의 실질 가치
- 세금 물결·재건: 청구서가 서쪽에서 동쪽으로 지나가고, 부서진 건물이 차례로 다시 올라감
- 반전: 2026→1963 되감기(지은 해 역순으로 사라짐) → 배밭 → 다시 자라는 도시, 땅값 배율(1963→79 875배)
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, light_keys, people_colors, pose_of, set_cam, sky_at, traffic

AREA = "apgujeong"
DUR = 56.0
META = {"id": "ep11", "title": "만약 전쟁이 끝난 후 건물주들은 어떻게 될까?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "Eb", "mode": "major", "bpm": 70, "seed": 11, "twist_at": 43.0}}
FOCUS = (1200.0, 1400.0)
ROAD = (1300.0, 1488.0, 2.0)     # 압구정로 (갤러리아 서쪽) — 길 방향(서북서↔동남동)을 따라 바라봄
NW, NC = 900, 170                # 그중 압구정로 주변
NW_ROAD, NC_ROAD = 360, 60
DAMAGE = 55082 / 191260          # 1952 서울 주택 피해율 (28.8%)
FULL = 34742 / 55082             # 피해 중 전소·전파 비율
INFL = (1.56, 6.31, 2.17)        # 1950·51·52 서울 도매물가 상승 배수
LAND_X = 875                     # 1963→1979 압구정동 땅값 배율


def lin(t, keys):
    return keyed(t, keys, ease=lambda u: u)


def sstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


WAR_M = [(4.5, 0.0), (10.0, 3.0), (12.6, 37.0)]
PEACE_Y = [(12.6, 0.0), (16.0, 0.08), (16.4, 0.5), (21.5, 1.0), (21.9, 2.0), (27.0, 3.0), (27.4, 3.2), (32.0, 4.0),
           (32.4, 6.0), (37.5, 7.0), (37.9, 8.0), (43.0, 10.0)]
YEAR = [(43.0, 2026.0), (45.0, 1963.0), (46.0, 1963.0), (47.8, 1979.0), (50.6, 2026.0)]
POP = [(0.0, 0.85), (4.5, 0.85), (10.0, 0.25), (12.6, 0.08), (16.0, 0.15), (21.5, 0.45), (25.0, 1.0), (37.5, 0.9),
       (43.0, 0.92), (44.4, 0.04), (46.0, 0.04), (50.6, 0.85), (56.0, 0.85)]
OCC = [(0.0, 0.95), (4.5, 0.95), (10.0, 0.35), (12.6, 0.2), (16.0, 0.3), (21.5, 0.6), (24.0, 1.0), (56.0, 1.0)]
CARS = [(0.0, 0.9), (4.5, 0.9), (9.0, 0.2), (10.2, 0.0), (13.0, 0.0), (16.0, 0.1), (27.0, 0.6), (37.5, 0.8),
        (43.0, 0.8), (43.8, 0.0), (47.5, 0.0), (50.6, 0.9), (56.0, 0.9)]


def year_at(t):
    return 2026.0 if (t < 43.0 or t >= 50.6) else lin(t, YEAR)


def farm_at(t):
    return float(sstep((1990.0 - year_at(t)) / 20.0)) if 43.0 <= t < 51.0 else 0.0


def price_level(m):
    p = 1.0
    for k, f in enumerate(INFL):
        p *= f ** (np.clip(m - 12 * k, 0, 12) / 12)
    return float(p)


def land_mult(t):
    y = year_at(t)
    if t < 45.0 or y <= 1963.0:
        return 1
    return int(round(LAND_X ** min(1.0, (y - 1963.0) / 16.0))) if t < 51.5 else LAND_X


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


BEATS = [
    Beat(0.0, 4.5, badge="오늘", label="만약", title="전쟁이 끝난 후\n{yellow}건물주{/}들은 어떻게 될까?", title_size=74,
         note="무대: 압구정동 · 아파트 3.3㎡당 평균 1억 4,068만 원 (부동산R114, 2025.12)",
         sub="대한민국에서 아파트값이 가장 비싼 동네,\n압구정에서 시뮬레이션합니다."),
    Beat(4.5, 10.0, badge="전쟁 발발", title="세입자가 떠난다", big="월세 -45%", big_color="red", big_size=104,
         note="개전 3개월, 키이우 월세 ㎡당 11달러 → 6달러 (Address.ua, 2022)",
         sub="전쟁이 나면 사람들이 떠나고\n월세부터 무너집니다."),
    Beat(10.0, 16.0, badge="종전", title="건물 {red}10채 중 3채{/}가 부서졌다",
         note="한국전쟁: 서울 주택 191,260호 중 55,082호 피해 (28.8%, 1952)",
         sub="무너진 건물은\n월세도, 건물값도 0이 됩니다."),
    Beat(16.0, 21.5, badge="종전 1년", title="현금이 {red}녹는다{/}",
         big=lambda t, sim: cash_text(t), big_size=96, big_color="red",
         note="1950~52년 서울 도매물가 약 21배 · 1953년 화폐개혁 100원 → 1환",
         sub="통장 속 돈의 가치는 21분의 1이 됐지만\n건물은 건물로 남았습니다."),
    Beat(21.5, 27.0, badge="종전 3년", title="빈집 {green}0.2%{/}",
         note="1950년 서독 공실률 (DIW) · 1946년 가구 1,370만 vs 집 820만",
         sub="살아남은 건물엔\n빈방이 하나도 없습니다."),
    Beat(27.0, 32.0, badge="종전 4년", title="그런데 월세는 {cyan}동결{/}",
         note="전후 서독 주택강제관리: 해지 금지 · 임대료 고정 · 세입자 배정",
         sub="집주인은 월세를 올릴 수도,\n세입자를 고를 수도 없었습니다."),
    Beat(32.0, 37.5, badge="종전 7년", title="재산의 {red}절반{/}을 내라", big="50%", big_color="red", big_size=112,
         note="서독 부담조정법(1952): 재산의 50%를 30년간 분납 · 일본(1946): 재산세 최고 90%",
         sub="전쟁 피해를 나누자며 나라가\n가진 사람에게 청구서를 보냅니다."),
    Beat(37.5, 43.0, badge="종전 10년", title="서울이 {cyan}강을 건넌다{/}", big="268 → 613㎢", big_size=92,
         note="1963년 서울 행정구역 확장 (면적 약 2.3배)",
         sub="무너진 동네를 다시 세운 도시는\n한강 남쪽으로 넓어집니다."),
    Beat(43.0, 51.5, badge="반전", title="그때 압구정은 {green}배밭{/}이었다",
         big=lambda t, sim: f"땅값 ×{land_mult(t):,}", big_color="yellow", big_size=104,
         note="1963→1979년 압구정동 땅값 875배 · 같은 기간 신당동 25배 (손정목)",
         sub="지난 전쟁 뒤 땅값이 폭등한 곳은\n오래된 도심이 아니라 강 건너 배밭이었습니다."),
    Beat(51.5, 56.0, badge="지금", title="전쟁이 끝난 날,\n당신은 {yellow}현금 · 건물 · 땅{/}\n무엇을 고를 건가요?",
         title_size=66),
]
GRADE = {"exposure": 0.95, "bloom": 0.3, "bloom_thr": 1.0, "vignette": 0.32}
FLASH = [(43.0, 0.3, (1.0, 0.97, 0.9))]
SKY = [(0.0, "DAY"), (5.0, "DAY"), (7.0, "DUSK"), (9.2, "NIGHT"), (12.4, "NIGHT"), (13.4, "MORNING"), (14.8, "DAY"),
       (21.6, "DAY"), (23.2, "DUSK"), (25.0, "NIGHT"), (31.8, "NIGHT"), (32.8, "MORNING"), (34.4, "DAY"),
       (51.0, "DAY"), (52.6, "DUSK"), (56.0, "DUSK")]


def cash_text(t):
    m = 36.0 * float(np.clip((t - 16.4) / 3.0, 0, 1))
    v = 1e8 / price_level(m)
    s = "1억 원" if v >= 0.9999e8 else f"{int(round(v / 1e4)):,}만 원"
    return f"1억 → {s}"


def spread_fire(rs, cent, area):
    """맞닿은 건물(틈 14m 이내)로 옮겨붙는 불 + 계속 떨어지는 새 불씨 → 피해율 28.8%에서 멈춤."""
    nb = len(cent)
    r = np.sqrt(area / np.pi)
    nbrs = []
    for s in range(0, nb, 600):
        d = np.hypot(cent[s:s + 600, None, 0] - cent[None, :, 0], cent[s:s + 600, None, 1] - cent[None, :, 1])
        gap = d - r[s:s + 600, None] - r[None, :]
        for i, row in enumerate(gap):
            j = np.where(row < 14.0)[0]
            nbrs.append(j[j != s + i])
    target = int(round(DAMAGE * nb))
    ign = np.full(nb, -1, int)
    burning, step = [], 0
    while (ign >= 0).sum() < target:
        if step % 3 == 0 or not burning:
            free = np.where(ign < 0)[0]
            k = rs.choice(free, min(6, len(free)), replace=False)
            ign[k] = step
            burning.extend(k.tolist())
        new = []
        for b in burning:
            for j in nbrs[b]:
                if ign[j] < 0 and rs.random() < 0.16:
                    ign[j] = step + 1
                    new.append(j)
        burning = [b for b in burning if step - ign[b] < 3] + new
        step += 1
    extra = (ign >= 0).sum() - target   # 마지막 단계에서 넘친 만큼 되돌림
    if extra > 0:
        last = np.where(ign == ign.max())[0]
        ign[rs.choice(last, min(extra, len(last)), replace=False)] = -1
    return ign


def simulate(build_dir):
    from engine import jamsil
    jamsil.use_area(AREA)
    CX, CY, RAD = jamsil.CX, jamsil.CY, jamsil.RAD
    g = jamsil.geometry()
    rs = np.random.default_rng(1111)
    nf = frames_of(DUR)
    cent, area, kind = g["b_cent"], g["b_area"], g["b_kind"]
    nb = len(cent)
    # ── 불길 번짐 → 피해 ──
    ign = spread_fire(rs, cent, area)
    dmg = ign >= 0
    t_ign = np.where(dmg, 10.0 + 2.3 * ign / max(1, ign.max()) + rs.uniform(0, 0.08, nb), 1e9).astype(np.float32)
    full = dmg & (rs.random(nb) < FULL)
    h_after = np.where(full, rs.uniform(0.08, 0.28, nb), np.where(dmg, rs.uniform(0.55, 0.85, nb), 1.0))
    t_reb = np.where(dmg, 37.9 + 3.6 * rs.random(nb), 1e9).astype(np.float32)
    # 지은 해(반전 되감기·성장 순서): 아파트 1976~88, 나머지 1978~2020
    year_b = np.where(kind == 1, rs.uniform(1976, 1988, nb), 1978 + 42 * rs.beta(2.0, 2.0, nb)).astype(np.float32)
    u_occ = rs.random(nb).astype(np.float32)
    # ── 사람·차: 동네 전체 + 압구정로(카메라 앞) 주변을 더 촘촘히 ──
    na, nc_a = NW - NW_ROAD, NC - NC_ROAD
    a, b = crowd(rs, nf, na, FOCUS, 520), crowd(rs, nf, NW_ROAD, ROAD[:2], 230)
    pp, py, ph = (np.concatenate([x, y], 1) for x, y in zip(a, b))
    shirt, pants = people_colors(rs, NW)
    a, b = traffic(rs, nf, nc_a, FOCUS, 1000), traffic(rs, nf, NC_ROAD, ROAD[:2], 320)
    cp, cy = (np.concatenate([x, y], 1) for x, y in zip(a, b))
    # ── 1963년 배밭: 9m 간격 과수원(120×80m 필지의 45%), 물 위·가장자리 제외 ──
    xs = np.arange(CX - RAD, CX + RAD, 9.0)
    ys = np.arange(CY - RAD, CY + RAD, 9.0)
    gx, gy = np.meshgrid(xs, ys)
    pts = np.c_[gx.ravel(), gy.ravel()] + rs.normal(0, 0.7, (gx.size, 2))
    keep = np.hypot(pts[:, 0] - CX, pts[:, 1] - CY) < RAD - 25
    pid = (np.floor(pts[:, 0] / 120).astype(np.int64) * 7919 + np.floor(pts[:, 1] / 80).astype(np.int64) * 104729)
    keep &= (np.abs(pid) % 100) < 45
    pts = pts[keep]
    s = 0
    wet = np.zeros(len(pts), bool)
    for n in g["wfs"]:
        q = g["wv"][g["wf"][s:s + n], :2]
        s += n
        x, y = pts[:, 0:1], pts[:, 1:2]
        xi, yi = q[None, :, 0], q[None, :, 1]
        xj, yj = np.roll(xi, 1, 1), np.roll(yi, 1, 1)
        cross = ((yi > y) != (yj > y)) & (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi)
        wet |= cross.sum(1) % 2 == 1
    orch = pts[~wet].astype(np.float32)
    orch_clear = rs.uniform(1968, 1978, len(orch)).astype(np.float32)
    orch_s = rs.uniform(4.5, 5.6, len(orch)).astype(np.float32)
    return dict(t_ign=t_ign, h_after=h_after.astype(np.float32), t_reb=t_reb, year_b=year_b, u_occ=u_occ,
                dmg=dmg.astype(np.float32), pp=pp, py=py, ph=ph, shirt=shirt, pants=pants,
                rank=rs.random(NW).astype(np.float32), cp=cp, cy=cy,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)], crank=rs.random(NC).astype(np.float32),
                orch=orch, orch_clear=orch_clear, orch_s=orch_s)


def bstate(t, s):
    """건물별 (높이 비율, 그을림, 불길, 빈방) — 렌더와 HUD가 같이 씀."""
    ti, tr = s["t_ign"], s["t_reb"]
    fall = sstep((t - ti - 0.35) / 0.5)
    hs = 1 - (1 - s["h_after"]) * fall
    reb = sstep((t - tr) / 1.2)
    hs = hs + (1 - hs) * reb
    burn = np.clip((t - ti) / 0.5, 0, 1) * (1 - reb)
    flame = np.clip(1 - np.abs(t - ti - 0.45) / 0.5, 0, 1) if t < 14.0 else np.zeros_like(ti)
    if t >= 43.0:   # 되감기·배밭·성장: 지은 해보다 이른 해엔 땅속에
        vis = sstep((year_at(t) - s["year_b"]) / 5.0)
        hs = -0.02 + 1.02 * vis
        burn = np.zeros_like(hs)
    dark = np.clip((s["u_occ"] - lin(t, OCC)) * 8, 0, 1)
    return hs.astype(np.float32), burn.astype(np.float32), flame.astype(np.float32), dark.astype(np.float32)


GOLD, ORANGE, CYAN, RED = (1.0, 0.72, 0.28), (1.0, 0.42, 0.1), (0.45, 0.85, 1.0), (1.0, 0.2, 0.15)


def glow_at(t, s, cent, flame, hs):
    nb = len(cent)
    glow = np.zeros(nb, np.float32)
    col = np.tile(np.array(GOLD, np.float32), (nb, 1))
    alive = s["dmg"] < 0.5
    if 27.2 <= t < 32.2:   # 월세 동결: 살아남은 건물이 차갑게
        glow[alive] = 0.32 * ramp(t, 27.3, 28.3) * (1 - ramp(t, 31.6, 32.2)) * (0.85 + 0.15 * math.sin(t * 3))
        col[:] = CYAN
    elif 32.2 <= t < 37.6:  # 세금 물결: 서→동으로 지나가면 금빛이 절반으로, 지나는 순간 빨갛게
        xw = -900 + (t - 33.0) / 3.0 * 3200
        passed = cent[:, 0] < xw
        near = np.abs(cent[:, 0] - xw) < 60
        glow[alive] = np.where(passed[alive], 0.27, 0.55) * ramp(t, 32.3, 33.0) * (1 - ramp(t, 37.0, 37.6))
        glow[alive & near] = 1.2
        col[near] = RED
    elif 43.0 <= t < 51.5:  # 다시 올라오는 건물은 잠깐 금빛
        rising = (hs > 0.02) & (hs < 0.98) & (t >= 46.0)
        glow[rising] = 0.9
    elif t >= 51.5:
        glow[:] = 0.22 * ramp(t, 51.6, 53.0)
    on = flame > 0.01
    glow[on] = 1.8 * flame[on] * (0.8 + 0.2 * math.sin(t * 23))
    col[on] = ORANGE
    return glow, col


def sky(t):
    return sky_at(t, SKY)


def fmt_clock(t):
    if t < 4.5:
        return "2026년 · 오늘"
    if t < 12.6:
        m = lin(t, WAR_M)
        d = int(m * 30.4)
        return f"전쟁 D+{d}" if d < 365 else f"전쟁 {int(m // 12)}년 {int(m % 12)}개월"
    if t < 43.0:
        y = lin(t, PEACE_Y)
        return "종전 D+%d" % int(y * 365) if y < 0.4 else f"종전 {int(round(y))}년"
    return f"{int(year_at(t))}년"


def hud(t, sim):
    if t < 4.5:
        r2 = "아파트 3.3㎡당 1억 4,068만 원"
    elif t < 10.0:
        r2 = f"월세 지수 {int(round(lin(t, [(4.5, 100.0), (9.5, 55.0)])))} (개전 전 = 100)"
    elif t < 16.0:
        n = int((sim["t_ign"] <= t).sum())
        r2 = f"피해 건물 {n:,}동 / {len(sim['t_ign']):,}동 ({100 * n / len(sim['t_ign']):.1f}%)"
    elif t < 21.5:
        m = 36.0 * float(np.clip((t - 16.4) / 3.0, 0, 1))
        r2 = f"물가 ×{price_level(m):.1f} (1950~52년 서울)"
    elif t < 27.0:
        r2 = "남은 집에 사람이 몰림"
    elif t < 32.0:
        r2 = "월세: 동결 · 세입자: 나라가 배정"
    elif t < 37.5:
        r2 = "청구서: 재산의 50%, 30년 분납"
    elif t < 43.0:
        d = sim["dmg"] > 0.5
        k = int(((sim["t_reb"] + 1.2 <= t) & d).sum())
        r2 = f"다시 지은 건물 {k:,}동 / {int(d.sum()):,}동"
    elif t < 51.5:
        r2 = "압구정 ×875 · 신당동 ×25 (1963→79)" if t >= 47.8 else "1963년 압구정 = 배밭"
    else:
        r2 = "2026년 압구정"
    return {"left": "SIMULATION", "right": fmt_clock(t), "right2": r2}


def labels(t, anchors, sim):
    out = []

    def tag(key, text, color, a0, a1, size=26):
        a = anchors.get(key)
        if a and a[3] and a0 <= t < a1 and 470 < a[1] < 1430 and 60 < a[0] < 1020:
            out.append({"x": a[0], "y": a[1], "text": text, "color": color, "size": size,
                        "alpha": ramp(t, a0, a0 + 0.4) * (1 - ramp(t, a1 - 0.3, a1))})
    tag("river", "한강", "cyan", 0.6, 4.4)
    tag("apt", "압구정 현대아파트", "white", 0.9, 4.4)
    tag("rodeo", "압구정로데오", "yellow", 1.2, 4.4)
    tag("river", "한강", "cyan", 38.5, 42.8)
    tag("orchard", "배밭 (1963년)", "green", 45.0, 46.6)
    tag("river", "한강", "cyan", 45.0, 51.2)
    return out


CAM = [(0.0, ROAD, 163, 32, 115.0, 30), (4.4, ROAD, 170, 33, 105.0, 30),
       (9.8, ROAD, 178, 44, 260.0, 30), (10.2, (1050.0, 1450.0, 20.0), 285, 42, 900.0, 30),
       (15.8, (1150.0, 1350.0, 10.0), 292, 36, 420.0, 30), (16.2, (1100.0, 1540.0, 2.0), 343, 34, 110.0, 30),
       (21.3, (1100.0, 1540.0, 2.0), 350, 34, 100.0, 30), (21.7, (1250.0, 1430.0, 4.0), 300, 36, 170.0, 30),
       (26.8, (1250.0, 1430.0, 4.0), 310, 36, 150.0, 30), (27.2, (1100.0, 1400.0, 10.0), 235, 40, 420.0, 30),
       (31.8, (1100.0, 1400.0, 10.0), 245, 42, 380.0, 30), (32.2, (1000.0, 1250.0, 10.0), 285, 50, 760.0, 30),
       (37.3, (1000.0, 1250.0, 10.0), 292, 50, 700.0, 30), (37.7, (1100.0, 1450.0, 10.0), 250, 34, 380.0, 30),
       (42.8, (950.0, 1500.0, 10.0), 265, 36, 1000.0, 30), (43.2, (900.0, 1450.0, 0.0), 280, 38, 1150.0, 30),
       (51.3, (900.0, 1450.0, 0.0), 290, 40, 1080.0, 30), (51.7, ROAD, 340, 36, 150.0, 30),
       (56.0, ROAD, 348, 40, 185.0, 30)]


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry, use_area
    use_area(AREA)
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    po = J.people(NW, "walkers")
    co = J.cars(NC)
    nb = J.nb
    cent, bh, area = g["b_cent"], g["b_h"], g["b_area"]
    flames = K.instancer(ctx, "flames", K.proto(ctx, "p_flame", K.bm_ico(1.0, sub=1),
                                                 [K.mat_emit("m_flame", ORANGE, 7.0, ctx, "fire")]), nb)
    fsize = np.sqrt(area) * 0.22
    orch = sim["orch"]
    no = len(orch)
    ob_or = K.instancer(ctx, "orchard", K.proto_tree(ctx, K.mat_inst("m_pear", 0.8),
                                                     K.mat_simple("m_pear_trunk", (0.25, 0.17, 0.1), 0.9), "round"), no)
    rs = np.random.default_rng(5)
    or_col = np.c_[rs.uniform(0.9, 0.98, no), rs.uniform(0.86, 0.94, no), rs.uniform(0.86, 0.95, no)].astype(np.float32)
    or_rot = np.c_[np.zeros((no, 2)), rs.uniform(0, 6.28, no)].astype(np.float32)
    or_pos = np.c_[orch, np.zeros(no)].astype(np.float32)
    lk = [(k, dict(v, energy=max(v["energy"], 0.7), amb=max(v["amb"], 0.11))) for k, v in light_keys(SKY)]
    tree_pos = np.c_[J.tree_xy, np.zeros(len(J.tree_xy))]
    last = {"tree": None, "orch": None}
    zeros_nb = np.zeros((nb, 3), np.float32)

    def upd(t, f):
        set_cam(J, t, CAM, drift=0.0)
        night = J.light(t, lk)
        ctx.set_ctl("lights", 0.12 + 0.75 * night)
        ctx.set_ctl("carlights", 0.2 + 0.8 * night)
        ctx.set_ctl("fire", 0.85 + 0.15 * math.sin(t * 17))
        ctx.set_ctl("farm", farm_at(t))
        hs, burn, flame, dark = bstate(t, sim)
        glow, gcol = glow_at(t, sim, cent, flame, hs)
        J.set_buildings(hscale=hs, glow=glow, gcol=gcol, dark=dark, burn=burn)
        K.set_points(flames, np.c_[cent, bh * np.maximum(hs, 0) + 1.5], scale=fsize * flame,
                     rot=zeros_nb, col=np.ones((nb, 3)))
        vis = np.clip((lin(t, POP) - sim["rank"]) / 0.03, 0, 1)
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(NW)], scale=vis, rot=np.c_[np.zeros((NW, 2)), sim["py"][f]],
                     col=sim["shirt"], colors={"col2": sim["pants"]}, pose=pose_of(sim["ph"][f]))
        cvis = np.clip((lin(t, CARS) - sim["crank"]) / 0.03, 0, 1) * 10.0
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=cvis, rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]],
                     col=sim["ccol"])
        y = year_at(t)
        tv = round(float(np.clip((y - 1980.0) / 6.0, 0, 1)), 3)   # 가로수는 1980년대부터
        if tv != last["tree"]:
            K.set_points(J.to, tree_pos, scale=J.tree_s0 * tv)
            last["tree"] = tv
        ov = sstep((sim["orch_clear"] - y) / 3.0) if 43.0 <= t < 51.5 else np.zeros(no, np.float32)
        key = round(float(ov.sum()), 1)
        if key != last["orch"]:
            K.set_points(ob_or, or_pos, scale=sim["orch_s"] * ov, rot=or_rot, col=or_col)
            last["orch"] = key

    ctx.on_frame(upd)
    ctx.anchor("river", lambda t: (520.0, 2230.0, 2.0))
    ctx.anchor("apt", lambda t: (620.0, 1820.0, 48.0))
    ctx.anchor("rodeo", lambda t: (1330.0, 1300.0, 28.0))
    ctx.anchor("orchard", lambda t: (880.0, 1420.0, 6.0))
