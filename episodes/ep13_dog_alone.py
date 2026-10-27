"""EP13 주인이 나가면 강아지는 뭐 하고 지낼까? (잠실 아파트 꼭대기 층)

실제로 계산하는 것 (engine/home.py):
- 강아지 하루 행동: 반-마르코프 모형 — 처음엔 현관 쪽을 보고 낑낑(Scaglia 외 2013: 90분 중 살피기 8.6분·낑낑 6.4분),
  대부분은 쉬기(같은 연구: 54.3분), 분리 문제 강아지(5%, Salonen 외 2020)는 현관에서 우는 불안 행동
- 아파트 한 동 100마리(분리 문제 5마리) + 주인공 후보 → 장면마다 그 행동을 실제로 한 주인공의 하루를 따라감
- 주인공 동선: 집 안 길찾기, 걷기 속도는 영상 시간 기준 / 마중은 깡충깡충
"""
from engine.common import Beat, FPS, frames_of, ramp
from engine.home import (DOOR, DRINK, EAT, GREET, GROOM, PLAY, REST, SLEEP, TOILET, WALK, WINDOW, DISTRESS,
                         first_start, hm, state_at)

KIND = "dog"
DUR = 56.0
SEED = 1313
N_SR, N_CAND = 5, 500                   # 100마리 중 분리 문제 5마리 (Salonen 외 2020: 5%)
T_LEAVE = 0.3
SR_SHOW = (28.6, 34.0)                  # 아파트 한 동 장면에서 분리 문제 집 표시
FUR = (0.95, 0.93, 0.88)                # 흰 말티즈 느낌
META = {"id": "ep13", "title": "주인이 나가면 강아지는 뭐 하고 지낼까?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "G", "mode": "major", "bpm": 76, "seed": 13, "twist_at": 40.0}}
P = dict(first=DOOR, start_spot="hall", base_act=0.55, peaks=[(8.2, 0.5, 0.5)],
         dur={SLEEP: 55, REST: 18, GROOM: 2, EAT: 3.0, DRINK: 1.0, TOILET: 1.5, WALK: 1.5, WINDOW: 5, PLAY: 3.0,
              DOOR: 6.0, DISTRESS: 3.0, GREET: 4.0},
         w_sleep=2.4, sleep_pivot=1.6, w_rest=2.6, w_groom=0.2, w_drink=0.3, w_walk=0.7, w_window=0.4, w_play=0.25,
         w_door=0.25, w_door0=4.0, door_tau=25.0, w_dis=0.8, w_dis0=4.0, meal_gap=300.0, toilet_gap=300.0, greet=4.0,
         spots={SLEEP: [("cushion", .45), ("sofa", .25), ("bed", .3)],
                REST: [("cushion", .3), ("rug", .25), ("door", .25), ("hall", .2)],
                GROOM: [("cushion", 1)], EAT: [("food", 1)], DRINK: [("water", 1)], TOILET: [("litter", 1)],
                WALK: [("hall", .3), ("rug", .3), ("window2", .2), ("shoes", .2)], WINDOW: [("window", 1)],
                DOOR: [("door", .5), ("shoes", .5)], DISTRESS: [("door", 1)], GREET: [("door", 1)]},
         spots_home={REST: [("near_owner", 1)], GROOM: [("near_owner", 1)], SLEEP: [("near_owner", 1)],
                     WALK: [("near_owner", 1)], WINDOW: [("near_owner", 1)]},
         pose={SLEEP: 0, REST: 1, GROOM: 1, EAT: 3, DRINK: 3, TOILET: 2, WALK: 2, WINDOW: 2, PLAY: 1, DOOR: 1,
               DISTRESS: 2, GREET: 7, "run": 5, "run2": 6, "greet": 7},
         walk_speed=4.0, run_speed=6.5, stride=0.28, hop=True)


def m(h, mi):
    return h * 60 + mi


def select(ev):
    sc, info = 0.0, {"sniff": (m(12, 30), m(12, 35))}
    sc += 3 * (state_at(ev, m(8, 15)) == DOOR) + 3 * (state_at(ev, m(8, 24)) == DOOR) +         1 * (state_at(ev, m(8, 33)) in (DOOR, REST))
    sc += 2 * (state_at(ev, m(9, 30)) in (REST, SLEEP)) + 2 * (state_at(ev, m(10, 30)) == SLEEP)
    sc += 2 * (state_at(ev, m(14, 45)) == SLEEP) + 1 * (state_at(ev, m(15, 30)) == SLEEP)
    e = first_start(ev, DOOR, m(12, 0), m(13, 10))
    if e:
        sc += 3 + min(1.0, (e[1] - e[0]) / 5.0)
        info["sniff"] = e
    return sc, info


def clock_keys(i):
    s0, s1 = i["sniff"]
    return [(0.0, m(8, 6)), (4.5, m(8, 12)), (10.0, m(8, 40)), (16.0, m(11, 30)), (17.6, s0 - 0.3), (20.6, s1 + 0.3),
            (22.0, m(13, 30)), (28.0, m(16, 0)), (34.0, m(18, 40)), (35.2, m(18, 54)), (39.5, m(19, 1)),
            (40.0, m(19, 2)), (46.0, m(19, 20)), (51.5, m(19, 50)), (56.0, m(21, 0))]


BEATS = [
    Beat(0.0, 4.5, badge="08:10", label="만약", title="주인이 나가면\n{orange}강아지{/}는 뭐 하고 지낼까?", title_size=74,
         note="반려동물이 혼자 있는 시간: 하루 평균 5시간 54분 (KB경영연구소, 2025)",
         sub="평균 출근 시각 8시 10분 (통계청).\n문이 닫히고, 강아지 혼자 남았습니다."),
    Beat(4.5, 10.0, badge="08:15", title="처음엔 현관 앞 {orange}낑낑{/}",
         note="혼자 남은 개 90분 관찰: 주변 살피기 8.6분 · 낑낑거림 6.4분 (Scaglia 외 2013)",
         sub="문 쪽을 보고, 귀를 세우고,\n작게 낑낑거립니다."),
    Beat(10.0, 16.0, badge="09:30", title="그리고 {blue}대부분 쉰다{/}", big="60%", big_size=112,
         note="문제 없는 개 30마리 90분 촬영: 가만히 쉬기 54.3분 (Scaglia 외 2013)",
         sub="생각보다 차분합니다.\n혼자 있는 시간의 절반 넘게 쉽니다."),
    Beat(16.0, 22.0, badge="12:30", title="냄새로 {yellow}시간{/}을 잰다?",
         note="주인 냄새가 옅어지는 정도로 시간을 짐작한다는 가설 (Horowitz) — 아직 검증 안 됨",
         sub="현관의 주인 신발 냄새를 맡으며\n'얼마나 지났는지' 안다는 가설이 있습니다."),
    Beat(22.0, 28.0, badge="14:30", title="낮잠, 또 낮잠", big="하루 약 11시간", big_size=96,
         note="측정 연구 범위 8~13.5시간, 평균 11시간 조금 안 됨 (Sleep Foundation 정리)",
         sub="혼자인 낮 시간은\n대부분 잠으로 채웁니다."),
    Beat(28.0, 34.0, badge="17:00", label="아파트 한 동, 강아지 100마리라면", title="{red}5마리{/}는 분리 불안",
         note="핀란드 반려견 13,700마리: 분리 관련 행동 5% · 소음 민감 32% (Salonen 외 2020)",
         sub="이 강아지들은 주인이 나가고 몇 분 안에\n울거나 물건을 망가뜨리기 시작합니다."),
    Beat(34.0, 40.0, badge="18:55", title="주인이 오면 꼬리 {orange}3배{/}",
         note="다시 만났을 때 꼬리 흔들기: 30분 뒤 0.09 → 2시간 뒤 0.27 (Rehn & Keeling 2011)",
         sub="30분 떨어졌을 때보다\n2시간 뒤에 훨씬 격하게 반깁니다."),
    Beat(40.0, 46.0, badge="반전", title="2시간 = 4시간?", big="0.27 vs 0.26", big_size=100, big_color="yellow",
         note="꼬리 흔들기 비율: 2시간 0.27 · 4시간 0.26 (Rehn & Keeling 2011, 개 12마리)",
         sub="2시간을 넘기면 반기는 정도는\n거의 차이가 없었습니다."),
    Beat(46.0, 51.5, badge="그럼 11시간은?", title="{orange}80.1%{/}가 혼자 두고 나간다",
         note="반려동물을 혼자 두고 외출하는 가구 (KB경영연구소, 2025)",
         sub="개가 시간을 어떻게 느끼는지는\n아직 아무도 모릅니다."),
    Beat(51.5, 56.0, badge="지금", title="오늘 당신의 강아지는\n{orange}몇 시간{/} 기다렸을까요?", title_size=72),
]
GRADE = {"exposure": 0.95, "bloom": 0.28, "bloom_thr": 1.0, "vignette": 0.3}
SKY = [(0.0, "MORNING"), (4.6, "MORNING"), (8.0, "DAY"), (26.0, "DAY"), (27.6, "DUSK"), (28.4, "DUSK"),
       (29.2, "NIGHT"), (56.0, "NIGHT")]
EYE = (-5.4, 5.3, 4.0)   # 거실 창가 구석, 낮은 벽(1.1m) 너머까지 보이는 높이
CAM = [(0.0, ("unit", 0.0, 0.0, 0.0), -110, 58, 95.0, 30), (1.2, ("unit", 0.0, 0.0, 0.0), -105, 56, 70.0, 30),
       (4.4, ("unit", 1.5, -2.0, 0.3), -100, 52, 17.0, 30),
       (4.8, ("hero",), -105, 58, 12.0, 30), (9.8, ("hero",), -95, 58, 11.0, 30),
       (10.2, ("hero",), -80, 56, 12.5, 30), (15.8, ("hero",), -65, 56, 12.0, 30),
       (16.2, ("hero",), -115, 58, 10.5, 30), (21.8, ("hero",), -105, 58, 10.0, 30),
       (22.2, ("hero",), -70, 60, 11.5, 30), (27.8, ("hero",), -80, 60, 11.0, 30),
       (28.2, ("bld",), -96, 8, 130.0, 30), (33.8, ("bld",), -88, 9, 122.0, 30),
       (34.2, ("unit", 3.0, -3.5, 0.0), -100, 56, 13.0, 30), (39.8, ("unit", 2.0, -2.5, 0.0), -95, 56, 13.0, 30),
       (40.2, ("unit", -1.7, 0.7, 0.3), -115, 52, 10.5, 30), (45.8, ("unit", -1.7, 0.7, 0.3), -100, 52, 10.0, 30),
       (46.2, ("unit", -1.7, 0.7, 0.3), -90, 50, 12.0, 30), (51.3, ("unit", -1.7, 0.7, 0.3), -85, 50, 12.0, 30),
       (51.7, ("unit", 0.0, 0.0, 0.0), -95, 45, 26.0, 30), (56.0, ("unit", 0.0, 0.0, 0.0), -90, 32, 140.0, 30)]


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def simulate(build_dir):
    import sys
    from engine.home import simulate_home
    return simulate_home(sys.modules[__name__])


def build(ctx):
    import sys
    from engine.home import build_home_scene
    build_home_scene(ctx, sys.modules[__name__])


def sky(t):
    from engine.jamsil_ep import sky_at
    return sky_at(t, SKY)


def hud(t, sim):
    f = fi(t)
    c = float(sim["clock"][f])
    if t < 4.5:
        r2 = "주인 출근 · 강아지 혼자"
    elif t < 28.0:
        s = int(sim["sleep_min"][f])
        r2 = f"오늘 잔 시간 {s // 60}시간 {s % 60}분 · 밥 {int(sim['meals'][f])}번 · 쉬 {int(sim['toilets'][f])}번"
    elif t < 34.0:
        fs = sim["fac_state"][f]
        r2 = (f"분리 문제 {int(sim['fac_sr'].sum())}마리 · 자는 중 {int((fs == SLEEP).sum())}"
              f" · 깨어 있음 {int((fs != SLEEP).sum())}")
    else:
        r2 = "주인 귀가 18:55"
    return {"left": "SIMULATION", "right": hm(c), "right2": r2}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("hero")
    if a and a[3] and 4.8 < t < 27.8 and 520 < a[1] < 1450:
        out.append({"x": a[0], "y": a[1], "text": "강아지", "color": "orange", "size": 24, "lift": 40})
        f = fi(t)
        if 5.0 < t < 9.8 and int(sim["shown"][f]) == DOOR and int(t * 1.6) % 2 == 0:
            out.append({"x": a[0] + 70, "y": a[1] - 40, "text": "낑낑", "color": "yellow", "size": 30,
                        "alpha": ramp(t % 1.25, 0.0, 0.15)})
    return out
