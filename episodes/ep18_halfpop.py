"""EP18 만약 한국 인구가 절반이 된다면? (잠실 석촌호수)

실제로 계산하는 것:
- 인구: 지금 5,100만 → 절반 2,600만. 거리의 사람이 비율만큼 줄고, 65세 이상(회색 옷) 비율이 47.7%까지 늘어남
- 빈집: 불 켜진 창문이 인구 비율만큼 줄어듦, 차도 줄어듦
- 합계출산율 0.72가 이어지면 한 세대(약 30년)마다 다음 세대는 0.72 ÷ 2.1 ≈ 1/3
숫자: 통계청 장래인구추계(2023, 2072년 3,622만·고령 47.7%) · 2024 합계출산율 0.75 · 2024 출생아 23.8만 명(9년 만에 증가).
"""
import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, eye_from, light_keys, people_colors, pose_of, set_cam, sky_at, traffic

DUR = 56.0
META = {"id": "ep18", "title": "만약 한국 인구가 절반이 된다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "C", "mode": "minor", "bpm": 68, "seed": 181, "twist_at": 46.0}}
NP, NC = 700, 140
LAKE = (130.0, -95.0)
# (영상 초, 인구 비율, 65세 이상 비율)
POP = [(0.0, 1.0, 0.19), (4.5, 1.0, 0.19), (5.0, 0.95, 0.30), (16.0, 0.90, 0.38), (16.5, 0.82, 0.42),
       (28.0, 0.75, 0.46), (28.5, 0.70, 0.477), (40.0, 0.62, 0.48), (40.5, 0.5, 0.48), (46.0, 0.5, 0.48),
       (46.5, 1.0, 0.19), (56.0, 1.0, 0.19)]

BEATS = [
    Beat(0.0, 4.5, badge="2024", label="대한민국", big="5,100만", label_color="blue", big_color="white",
         sub="지금 북적이는 석촌호수.\n이 사람들이 절반으로 줄어든다면?"),
    Beat(4.5, 10.0, badge="출산율", title="여성 1명당 아이 {red}0.72명{/}", note="2023년 합계출산율, 세계 최저 (통계청)",
         sub="인구가 유지되려면 2.1명이 필요합니다.\n한국은 그 3분의 1입니다."),
    Beat(10.0, 16.0, badge="2040년", title="학교가 {orange}비어 간다{/}",
         sub="아이가 줄면 가장 먼저 동네 학교가\n문을 닫고 놀이터가 조용해집니다."),
    Beat(16.0, 22.0, badge="2050년", title="거리의 {gray}회색{/}이 늘어난다", note="회색 옷 = 65세 이상 (시뮬레이션 표시)",
         sub="일할 사람은 줄고\n돌봄이 필요한 사람은 늘어납니다."),
    Beat(22.0, 28.0, badge="2060년", title="불 꺼진 {gray}빈집{/}",
         sub="아파트 창문의 불이 하나둘 꺼집니다.\n빈집이 동네마다 생깁니다."),
    Beat(28.0, 34.0, badge="2072년", title="인구 {orange}3,622만{/}", big="2명 중 1명", big_size=100, big_color="gray",
         note="2072년 고령 인구 비율 47.7% (통계청 장래인구추계, 2023)",
         sub="국민 두 명 중 한 명이\n65세 이상이 됩니다."),
    Beat(34.0, 40.0, badge="한 세대마다", title="다음 세대는 {red}3분의 1{/}", note="0.72 ÷ 2.1 ≈ 0.34 (단순 계산)",
         sub="출산율이 그대로면 아이 세대는\n부모 세대의 3분의 1로 줄어듭니다."),
    Beat(40.0, 46.0, badge="절반", title="한산한 잠실", big="2,600만", big_size=110, big_color="orange",
         sub="지하철은 텅 비고 집값보다\n빈집 관리가 더 큰 문제가 됩니다."),
    Beat(46.0, 52.5, badge="반전", title="그런데 작년, {green}9년 만에{/}", big="출생아 ↑", big_size=104, big_color="green",
         note="2024년 출생아 23.8만 명, 전년보다 3.6% 증가 (통계청)",
         sub="2015년 이후 줄기만 하던 출생아가\n처음으로 다시 늘었습니다."),
    Beat(52.5, 56.0, badge="지금", title="절반이 되는 미래,\n{cyan}바꿀 수 있을까요?{/}", title_size=76),
]
GRADE = {"exposure": 0.98, "bloom": 0.25, "bloom_thr": 1.0, "vignette": 0.32}
SKY = [(0.0, "DAY"), (21.6, "DAY"), (22.6, "DUSK"), (27.6, "DUSK"), (28.6, "DAY"), (39.6, "DAY"), (40.6, "DUSK"),
       (45.6, "DUSK"), (46.6, "MORNING"), (56.0, "MORNING")]
CAM = [(0.0, (130.0, -95.0, 3.0), 322, 24, 48.0, 30), (4.4, (130.0, -95.0, 3.0), 330, 26, 52.0, 30),
       (4.9, (60.0, -60.0, 30.0), 300, 30, 520.0, 30), (9.6, (60.0, -60.0, 30.0), 315, 32, 560.0, 30),
       (10.2, (130.0, -95.0, 2.0), 310, 30, 40.0, 30), (15.8, (130.0, -95.0, 2.0), 325, 32, 44.0, 30),
       (16.4, (100.0, -80.0, 2.0), 300, 18, 70.0, 30), (21.8, (100.0, -80.0, 2.0), 312, 20, 78.0, 30),
       (22.4, (-200.0, 50.0, 10.0), 210, 50, 1100.0, 28), (27.8, (-200.0, 50.0, 10.0), 230, 54, 1200.0, 28),
       (28.4, (130.0, -95.0, 3.0), 300, 24, 70.0, 30), (33.8, (130.0, -95.0, 3.0), 315, 26, 78.0, 30),
       (34.4, (60.0, -60.0, 30.0), 300, 30, 520.0, 30), (39.8, (60.0, -60.0, 30.0), 315, 32, 560.0, 30),
       (40.4, (130.0, -95.0, 3.0), 322, 24, 48.0, 30), (45.8, (130.0, -95.0, 3.0), 330, 26, 52.0, 30),
       (46.4, (115.0, -85.0, 2.0), 312, 22, 36.0, 30), (52.4, (115.0, -85.0, 2.0), 322, 24, 40.0, 30),
       (53.0, (-200.0, 0.0, 20.0), 260, 40, 1500.0, 28), (56.0, (-200.0, 0.0, 20.0), 275, 44, 1650.0, 28)]
EYE = eye_from(CAM[0], 15.0, 75.0)   # 09편과 같은 호수 쪽 관찰 위치
GREY = np.array((0.72, 0.72, 0.74), np.float32)


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def pop_at(t):
    return keyed(t, [(a, (b, c)) for a, b, c in POP], ease=lambda u: u)


def simulate(build_dir):
    rs = np.random.default_rng(1818)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    pv = np.array([pop_at(t) for t in ts], np.float32)
    pp, py, ph = crowd(rs, nf, NP, LAKE, 220)
    shirt, pants = people_colors(rs, NP)
    rank = rs.random(NP)
    vis = (rank[None, :] < pv[:, 0:1]).astype(np.float32)
    # 남은 사람 중 고령 비율이 맞도록 회색 표시 (남는 사람 안에서 순서대로)
    arank = rs.random(NP)
    old = (arank[None, :] < pv[:, 1:2]).astype(np.float32)
    # 고령자는 천천히 걷는 것처럼 보이게 자세 위상을 늦춤
    ph = np.where(old > 0.5, (ph * 0.6) % 1.0, ph).astype(np.float32)
    cp, cy = traffic(rs, nf, NC, LAKE, 420)
    crank = rs.random(NC)
    cvis = (crank[None, :] < pv[:, 0:1]).astype(np.float32)
    return dict(pp=pp, py=py, ph=ph, shirt=shirt, pants=pants, vis=vis, old=old, pv=pv, cp=cp, cy=cy, cvis=cvis,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)])


def sky(t):
    return sky_at(t, SKY)


def hud(t, sim):
    p, a = sim["pv"][fi(t)]
    right = f"{int(round(5100 * p)):,}만"
    return {"left": "SIMULATION", "right": right, "right2": f"65세 이상 {int(round(100 * a))}%"}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("old")
    if a and a[3] and 16.8 < t < 21.6:
        out.append({"x": a[0], "y": a[1], "text": "65세 이상", "color": "gray", "size": 28, "lift": 8,
                    "alpha": ramp(t, 17.0, 17.6)})
    return out


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    po = J.people(NP, "people")
    co = J.cars(NC)
    nb = J.nb
    wrank = np.random.default_rng(18).random(nb)
    J.set_buildings(gcol=np.tile((1.0, 0.85, 0.55), (nb, 1)).astype(np.float32), glow=np.zeros(nb), dark=np.zeros(nb))
    lk = light_keys(SKY)
    lk = [(k_, dict(v_, energy=max(v_["energy"], 0.7), amb=max(v_["amb"], 0.11))) for k_, v_ in lk]

    def upd(t, f):
        set_cam(J, t, CAM, eye=EYE)
        night = J.light(t, lk)
        p = float(sim["pv"][f][0])
        ctx.set_ctl("lights", (0.12 + 0.5 * night) * (0.4 + 0.6 * p))
        ctx.set_ctl("carlights", 0.3 + 0.7 * night)
        lit = (wrank < p).astype(np.float32)
        J.set_buildings(glow=(0.14 * (0.3 + night) * lit).astype(np.float32), dark=(1 - lit) * 0.6)
        o = sim["old"][f][:, None]
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(NP)], scale=sim["vis"][f],
                     rot=np.c_[np.zeros((NP, 2)), sim["py"][f]], col=sim["shirt"] * (1 - o) + GREY * o,
                     colors={"col2": sim["pants"]}, pose=pose_of(sim["ph"][f]))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=10.0 * sim["cvis"][f],
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)

    def old_anchor(t):
        f = fi(t)
        m = (sim["old"][f] > 0.5) & (sim["vis"][f] > 0.5)
        if not m.any():
            return None
        eye = np.array(EYE[:2])
        P = sim["pp"][f]
        d = np.hypot(*(P - eye).T)
        d = np.where(m & (d > 25), d, 1e9)
        i = int(np.argmin(d))
        return float(P[i, 0]), float(P[i, 1]), 2.3
    ctx.anchor("old", old_anchor)
