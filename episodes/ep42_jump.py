"""EP42 만약 전 세계 80억 명이 같은 순간 점프한다면? (잠실 석촌호수, 1인칭 눈높이, 일차형)

10-27 기준 영상(남자가 한 명뿐이라면)과 같은 형식: 가정 → 시간순 칩(D-DAY·+1초·+1시간·+1일·+1주) → 아래 자막 한 줄.
실제로 계산하는 것:
- 점프: 모든 사람이 같은 순간 40cm(가정, 일반인 25~50cm) 뜸, 체공은 보이게 0.9초로 늘림(실제 약 0.57초). 점프 동안은 서 있음
- 지구가 밀린 거리: 점프 속도 √(2×9.8×0.4)=2.8m/s, 운동량 보존 4.96×10¹¹kg×2.8÷5.97×10²⁴kg=2.3×10⁻¹³m/s → 체공 0.57초 동안 약 1.3×10⁻¹³m = 원자 지름(약 1.1×10⁻¹⁰m)의 약 1/800
- 에너지: 1인 62kg×9.8×0.4=243J ×80억=1.94×10¹²J = TNT 약 470톤, 히로시마(약 15kt)의 약 1/32
- 합산 질량: 62kg×80억≈4.96×10¹¹kg(약 5억 톤, 상한), 지구 5.97×10²⁴kg은 약 12조 배
- 서울(605.2㎢)에 세우면 8×10⁹÷6.052×10⁸㎡=약 13명/㎡, 서 있는 군중은 5명/㎡ 넘으면 위험
숫자: UN 세계 인구 전망 2022(80억 명 2022-11-15 추정) · Walpole 외 2012(성인 평균 62kg) · NIST CODATA · OSTI/Britannica(히로시마) ·
NASA NSSDC(지구 질량) · xkcd What If #8(자전·공전 영향 없음, 굉음) · G. Keith Still 군중 밀도 지침. 점프 40cm·한곳에 모임은 가정.
"""
import numpy as np

from engine.common import FPS, Beat, frames_of
from engine.jamsil_ep import CAR_COLORS, crowd, eye_from, light_keys, people_colors, pose_of, set_cam, sky_at, traffic

DUR = 56.0
META = {"id": "ep42", "title": "만약 전 세계 80억 명이 같은 순간 점프한다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "C", "mode": "major", "bpm": 76, "seed": 421, "twist_at": 34.0}}
NP, NC = 800, 120
LAKE = (130.0, -95.0)
T_JUMP, AIR, JH = 2.4, 0.9, 0.40        # 점프 시작(초)·체공(초)·높이(m)
T_LAND = T_JUMP + AIR
STAND = (1.2, 7.0)                      # 이 구간은 서서 있음(점프 준비·착지 뒤)

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY 정오", label="전 세계", big="80억 명", label_color="blue", big_color="white",
         sub="오늘 정오, 80억 명이 같은 순간\n40cm씩 점프한다면?"),
    Beat(4.5, 10.0, badge="+1초", title="지구가 밀린 거리", big="원자의 1/800", big_size=100, big_color="yellow",
         note="계산값 약 1.3×10⁻¹³m · 40cm 점프는 가정",
         sub="사람들은 뛰었지만\n지구는 거의 움직이지 않았습니다."),
    Beat(10.0, 16.0, badge="+1초", title="점프 에너지는 {orange}TNT 470톤{/}", note="62kg × 9.8 × 0.4m × 80억 명 (계산)",
         sub="히로시마 폭탄의 약 30분의 1.\n지진계에 잡힐 만큼도 아닙니다."),
    Beat(16.0, 22.0, badge="+1시간", title="남은 건 {cyan}발자국{/}과 큰 소리", note="굉음: xkcd What If #8 설명 (연출)",
         sub="땅에는 발자국이 가득 찍히고\n굉음이 한동안 이어집니다."),
    Beat(22.0, 28.0, badge="+1일", title="자전도 공전도 {green}그대로{/}", note="xkcd What If #8",
         sub="지구는 평소처럼 돌고\n궤도도 달라지지 않습니다."),
    Beat(28.0, 34.0, badge="+1주", title="80억 명을 다 합쳐도", big="약 5억 톤", big_size=104, big_color="orange",
         note="성인 평균 62kg × 80억 명 (상한 계산)",
         sub="지구는 인류 전체보다\n약 12조 배 무겁습니다."),
    Beat(34.0, 40.0, badge="반전", title="진짜 문제는 {red}모이는 것{/}",
         sub="점프보다 어려운 건\n80억 명이 한자리에 서는 일입니다."),
    Beat(40.0, 46.0, badge="반전", title="서울에 다 세우면", big="1㎡에 13명", big_size=104, big_color="red",
         note="서울 605㎢ 기준 계산 · 5명 넘으면 위험 (군중 밀도 지침)",
         sub="5명만 넘어도 위험한 밀도라\n동시 점프는 상상 속에서만 됩니다."),
    Beat(46.0, 52.5, badge="지금", title="지구를 움직이려면\n{cyan}몇 명이 더{/} 필요할까요?", title_size=70),
    Beat(52.5, 56.0, badge="다음 편", title="오늘 저녁 7시\n{cyan}퀵샌드에 빠진다면?{/}", title_size=70),
]
GRADE = {"exposure": 0.98, "bloom": 0.25, "bloom_thr": 1.0, "vignette": 0.32}
SKY = [(0.0, "DAY"), (21.6, "DAY"), (22.6, "DUSK"), (27.6, "DUSK"), (28.6, "MORNING"), (33.6, "MORNING"), (34.6, "DAY"),
       (45.6, "DAY"), (46.6, "DUSK"), (56.0, "DUSK")]
# 눈높이 시점: 석촌호수 산책로에서 한자리에 서서 장면마다 바라보는 곳만 바뀜
CAM = [(0.0, (130.0, -95.0, 3.0), 322, 3, 18.0, 30), (4.4, (130.0, -95.0, 3.0), 322, 3, 18.0, 30),
       (4.9, (130.0, -95.0, 1.0), 300, 3, 14.0, 30), (9.8, (130.0, -95.0, 1.0), 300, 3, 14.0, 30),
       (10.4, (130.0, -95.0, 3.0), 322, 3, 18.0, 30), (15.8, (130.0, -95.0, 3.0), 322, 3, 18.0, 30),
       (16.4, (60.0, -60.0, 8.0), 300, 3, 90.0, 30), (21.8, (60.0, -60.0, 8.0), 300, 3, 90.0, 30),
       (22.4, (14.0, -6.0, 60.0), 250, 3, 330.0, 28), (27.8, (14.0, -6.0, 60.0), 250, 3, 330.0, 28),
       (28.4, (130.0, -95.0, 3.0), 322, 3, 18.0, 30), (33.8, (130.0, -95.0, 3.0), 322, 3, 18.0, 30),
       (34.4, (130.0, -95.0, 3.0), 322, 3, 18.0, 30), (39.8, (130.0, -95.0, 3.0), 322, 3, 18.0, 30),
       (40.4, (130.0, -95.0, 3.0), 322, 3, 18.0, 30), (45.8, (130.0, -95.0, 3.0), 322, 3, 18.0, 30),
       (46.4, (115.0, -85.0, 3.0), 312, 3, 20.0, 30), (52.4, (115.0, -85.0, 3.0), 312, 3, 20.0, 30),
       (53.0, (60.0, -60.0, 8.0), 300, 3, 90.0, 30), (56.0, (60.0, -60.0, 8.0), 300, 3, 90.0, 30)]
EYE = eye_from(CAM[0], 3.0, 18.0)
CLOCK = [(0.0, "D-DAY"), (4.5, "D+0 1초"), (16.0, "D+0 1시간"), (22.0, "D+1"), (28.0, "D+7"), (34.0, "점프 전"), (46.0, "지금")]


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def jump_z(t):
    u = (t - T_JUMP) / AIR
    return JH * 4.0 * u * (1.0 - u) if 0.0 < u < 1.0 else 0.0


def standing(t):
    return 0.0 if STAND[0] < t < STAND[1] else 1.0


def shake(t):
    d = t - T_LAND
    return 0.14 * np.exp(-d * 9.0) * np.sin(d * 55.0) if d > 0 else 0.0


def simulate(build_dir):
    rs = np.random.default_rng(4242)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    pp, py, ph = crowd(rs, nf, NP, LAKE, 110, t_speed=standing)
    shirt, pants = people_colors(rs, NP)
    cp, cy = traffic(rs, nf, NC, LAKE, 420)
    z = np.array([jump_z(t) for t in ts], np.float32)
    mv = np.array([standing(t) > 0 for t in ts])
    sh = np.array([shake(t) for t in ts], np.float32)
    return dict(pp=pp, py=py, ph=ph, shirt=shirt, pants=pants, cp=cp, cy=cy, z=z, mv=mv, sh=sh,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)])


def sky(t):
    return sky_at(t, SKY)


def hud(t, sim):
    lab = [c for c in CLOCK if c[0] <= t][-1][1]
    return {"left": "SIMULATION", "right": lab, "right2": "점프 40cm · 80억 명"}


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    po = J.people(NP, "people")
    co = J.cars(NC)
    nb = J.nb
    J.set_buildings(gcol=np.tile((1.0, 0.85, 0.55), (nb, 1)).astype(np.float32), glow=np.zeros(nb), dark=np.zeros(nb))
    lk = light_keys(SKY)
    lk = [(k_, dict(v_, energy=max(v_["energy"], 0.7), amb=max(v_["amb"], 0.11))) for k_, v_ in lk]

    def upd(t, f):
        set_cam(J, t, CAM, eye=(EYE[0], EYE[1], EYE[2] + float(sim["sh"][f])))
        night = J.light(t, lk)
        ctx.set_ctl("lights", 0.12 + 0.5 * night)
        ctx.set_ctl("carlights", 0.3 + 0.7 * night)
        J.set_buildings(glow=(0.14 * (0.3 + night) * np.ones(nb)).astype(np.float32))
        pos = np.c_[sim["pp"][f], np.full(NP, sim["z"][f], np.float32)]
        K.set_points(po, pos, scale=np.ones(NP, np.float32), rot=np.c_[np.zeros((NP, 2)), sim["py"][f]],
                     col=sim["shirt"], colors={"col2": sim["pants"]}, pose=pose_of(sim["ph"][f], sim["mv"][f]))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=10.0 * np.ones(NC, np.float32),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])

    ctx.on_frame(upd)
