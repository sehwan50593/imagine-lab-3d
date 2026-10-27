"""EP12 주인이 나가면 고양이는 뭐 하고 지낼까? (잠실 아파트 꼭대기 층)

실제로 계산하는 것 (engine/home.py):
- 고양이 하루 행동: 반-마르코프 모형 — 상태별 지속 시간, 새벽·해질녘 활동 정점(Smit 외 2024),
  배고픔(자유 급식, 하루 여러 번 조금씩), 화장실 압력(하루 약 2.5회), 분리 문제 고양이(13.5%)의 불안 행동
- 아파트 한 동 100마리(분리 문제 13마리) + 주인공 후보 → 장면마다 그 행동을 실제로 한 주인공의 하루를 따라감
- 주인공 동선: 집 안 길찾기, 걷기·우다다 속도는 영상 시간 기준
"""
from engine.common import Beat, FPS, frames_of
from engine.home import (DOOR, DRINK, EAT, GREET, GROOM, PLAY, REST, SLEEP, TOILET, WALK, WINDOW, DISTRESS,
                         first_start, hm, state_at)

KIND = "cat"
DUR = 56.0
SEED = 1212
N_SR, N_CAND = 13, 500                  # 100마리 중 분리 문제 13마리 (13.45%, de Souza Machado 외 2020)
T_LEAVE = 0.3
SR_SHOW = (34.6, 40.0)                # 아파트 한 동 장면에서 분리 문제 집 표시
FUR = (0.88, 0.46, 0.14)                # 치즈 태비
META = {"id": "ep12", "title": "주인이 나가면 고양이는 뭐 하고 지낼까?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "F", "mode": "major", "bpm": 72, "seed": 12, "twist_at": 46.0}}
P = dict(first=WALK, start_spot="hall", base_act=0.45, peaks=[(7.0, 0.8, 1.2), (17.5, 1.0, 1.4)],
         dur={SLEEP: 48, REST: 16, GROOM: 4, EAT: 3.0, DRINK: 1.0, TOILET: 3.0, WALK: 2.0, WINDOW: 9, PLAY: 3.0,
              DOOR: 3.0, DISTRESS: 4.0, GREET: 5.0},
         w_sleep=2.6, sleep_pivot=1.7, w_rest=2.2, w_groom=0.8, w_drink=0.35, w_walk=1.2, w_window=0.9, w_play=0.45,
         w_door=0.05, w_door0=0.0, door_tau=30.0, w_dis=0.6, w_dis0=2.0, meal_gap=70.0, toilet_gap=520.0, greet=5.0,
         spots={SLEEP: [("sofa", .3), ("bed", .35), ("tower", .15), ("window", .2)],
                REST: [("rug", .3), ("window", .25), ("sofa2", .2), ("tower_mid", .15), ("hall", .1)],
                GROOM: [("rug", .4), ("sofa2", .3), ("bed", .3)], EAT: [("food", 1)], DRINK: [("water", 1)],
                TOILET: [("litter", 1)], WALK: [("hall", .3), ("rug", .3), ("window2", .2), ("door", .2)],
                WINDOW: [("window", .5), ("tower", .3), ("window2", .2)], DOOR: [("door", 1)],
                DISTRESS: [("door", 1)], GREET: [("door", 1)]},
         spots_home={REST: [("near_owner", 1)], GROOM: [("near_owner", 1)], SLEEP: [("near_owner", 1)],
                     WALK: [("near_owner", 1)], WINDOW: [("near_owner", 1)]},
         pose={SLEEP: 0, REST: 1, GROOM: 2, EAT: 1, DRINK: 1, TOILET: 2, WALK: 2, WINDOW: 2, PLAY: 1, DOOR: 2,
               DISTRESS: 2, GREET: 7, "run": 5, "run2": 6, "greet": 7},
         walk_speed=4.0, run_speed=6.5, stride=0.25)


def m(h, mi):
    return h * 60 + mi


def select(ev):
    sc, info = 0.0, {"eat": (m(12, 50), m(12, 53)), "toilet": (m(15, 0), m(15, 2)), "play": (m(17, 5), m(17, 8))}
    sc += 2 * (state_at(ev, m(8, 55)) == SLEEP) + 2 * (state_at(ev, m(9, 25)) == SLEEP)
    sc += 1 * (state_at(ev, m(10, 50)) in (REST, WINDOW, GROOM)) + 1 * (state_at(ev, m(11, 30)) in (REST, WINDOW))
    for key, s, lo, hi in (("eat", EAT, m(12, 20), m(13, 20)), ("toilet", TOILET, m(14, 20), m(15, 35)),
                           ("play", PLAY, m(16, 25), m(17, 45))):
        e = first_start(ev, s, lo, hi)
        if e:
            sc += 3 + min(1.0, (e[1] - e[0]) / 4.0)   # 길게 한 행동일수록 화면에 잘 보임
            info[key] = e
    return sc, info


def clock_keys(i):
    (e0, e1), (o0, o1), (p0, p1) = i["eat"], i["toilet"], i["play"]
    return [(0.0, m(8, 6)), (4.5, m(8, 12)), (10.0, m(9, 40)), (16.0, m(12, 0)), (17.6, e0 - 0.2), (20.6, e1 + 0.3),
            (22.0, m(14, 0)), (23.4, o0 - 0.5), (26.4, o1 + 0.3), (28.0, m(16, 0)), (29.2, p0 - 0.2), (32.8, p1 + 0.5),
            (34.0, m(18, 0)), (40.0, m(18, 50)), (41.0, m(18, 54)), (45.5, m(19, 2)), (46.0, m(19, 5)),
            (51.5, m(19, 40)), (56.0, m(21, 0))]


BEATS = [
    Beat(0.0, 4.5, badge="08:10", label="만약", title="주인이 나가면\n{orange}고양이{/}는 뭐 하고 지낼까?", title_size=74,
         note="반려동물이 혼자 있는 시간: 하루 평균 5시간 54분 (KB경영연구소, 2025)",
         sub="평균 출근 시각 8시 10분 (통계청).\n문이 닫히고, 고양이 혼자 남았습니다."),
    Beat(4.5, 10.0, badge="08:30", title="일단 {blue}잔다{/}", big="하루 13.2시간", big_size=100,
         note="고양이 하루 수면 약 13.2시간 (뇌파 측정, Ursin 1968)",
         sub="하루의 절반 넘게 잡니다.\n혼자 둔 시간이 길수록 더 오래 누워 쉽니다."),
    Beat(10.0, 16.0, badge="10:00", title="깨어 있어도 {cyan}가만히{/}", big="74%", big_size=110,
         note="누움 37% · 앉음 37% · 활발히 움직임 3% (가속도계, Smit 외 2024)",
         sub="실제로 뛰어다니는 시간은\n하루 45분이 안 됩니다."),
    Beat(16.0, 22.0, badge="12:40", title="밥은 {yellow}조금씩 자주{/}", big="하루 12~20번", big_size=100,
         note="자유 급식 고양이, 한 번에 5~7g (Kane 외 1981)",
         sub="한 번에 사료 한 숟가락 정도씩,\n하루에도 여러 번 나눠 먹습니다."),
    Beat(22.0, 28.0, badge="14:50", title="화장실 하루 {orange}2.5번{/}",
         note="센서 측정 하루 평균 2.5회 · 보호자가 직접 본 횟수 0.6회 (JVIM, 2017)",
         sub="주인이 보는 건\n4번 중 1번뿐입니다."),
    Beat(28.0, 34.0, badge="17:00", title="해 질 녘 {green}우다다{/}",
         note="활동 정점: 새벽 6~8시 · 저녁 4~7시 (겨울, 가속도계 Smit 외 2024)",
         sub="사냥꾼의 시간이 오면\n집 안을 전력으로 달립니다."),
    Beat(34.0, 40.0, badge="18:20", label="아파트 한 동, 고양이 100마리라면", title="{red}13마리{/}는 혼자가 힘들다",
         note="분리 관련 문제 13.5% — 브라질 고양이 223마리 중 30마리 (de Souza Machado 외 2020)",
         sub="물건 망가뜨리기·지나친 울음·엉뚱한 곳 소변.\n장난감이 없는 집에서 더 많았습니다."),
    Beat(40.0, 46.0, badge="18:55", title="주인이 오면 {pink}가르랑{/}",
         note="4시간 혼자였던 고양이가 30분 때보다 더 가르랑·기지개 (Eriksson 외 2017)",
         sub="무심해 보여도\n오래 떨어질수록 더 반깁니다."),
    Beat(46.0, 51.5, badge="반전", title="고양이 애착 {pink}64.3%{/}", big="사람 아기 65%", big_size=96,
         note="주인과 '안정 애착'을 보인 새끼 고양이 비율 (Vitale 외 2019, Current Biology)",
         sub="고양이는 사람 아기와 거의 같은 비율로\n주인에게 애착을 보입니다."),
    Beat(51.5, 56.0, badge="지금", title="오늘 당신의 고양이는\n{orange}몇 시간{/} 기다렸을까요?", title_size=72),
]
GRADE = {"exposure": 0.95, "bloom": 0.28, "bloom_thr": 1.0, "vignette": 0.3}
SKY = [(0.0, "MORNING"), (4.6, "MORNING"), (8.0, "DAY"), (31.6, "DAY"), (33.3, "DUSK"), (33.9, "DUSK"),
       (34.6, "NIGHT"), (56.0, "NIGHT")]
CAM = [(0.0, ("unit", 0.0, 0.0, 0.0), -110, 58, 95.0, 30), (1.2, ("unit", 0.0, 0.0, 0.0), -105, 56, 70.0, 30),
       (4.4, ("unit", 1.5, -2.0, 0.3), -100, 52, 17.0, 30),
       (4.8, ("hero",), -105, 58, 13.0, 30), (9.8, ("hero",), -90, 58, 12.0, 30),
       (10.2, ("hero",), -80, 56, 12.5, 30), (15.8, ("hero",), -65, 56, 12.0, 30),
       (16.2, ("hero",), -115, 58, 11.0, 30), (21.8, ("hero",), -105, 58, 10.5, 30),
       (22.2, ("hero",), -70, 60, 11.0, 30), (27.8, ("hero",), -80, 60, 10.5, 30),
       (28.2, ("hero",), -100, 60, 12.5, 30), (33.8, ("hero",), -88, 60, 12.0, 30),
       (34.2, ("bld",), -96, 8, 130.0, 30), (39.8, ("bld",), -88, 9, 122.0, 30),
       (40.2, ("unit", 3.0, -3.5, 0.0), -100, 56, 13.0, 30), (45.8, ("unit", 2.0, -2.5, 0.0), -95, 56, 13.0, 30),
       (46.2, ("unit", -1.7, 0.7, 0.3), -115, 52, 10.5, 30), (51.3, ("unit", -1.7, 0.7, 0.3), -100, 52, 9.5, 30),
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
        r2 = "주인 출근 · 고양이 혼자"
    elif t < 34.0:
        s = int(sim["sleep_min"][f])
        r2 = f"오늘 잔 시간 {s // 60}시간 {s % 60}분 · 밥 {int(sim['meals'][f])}번 · 화장실 {int(sim['toilets'][f])}번"
    elif t < 40.0:
        fs = sim["fac_state"][f]
        r2 = (f"분리 문제 {int(sim['fac_sr'].sum())}마리 · 자는 중 {int((fs == SLEEP).sum())}"
              f" · 깨어 있음 {int((fs != SLEEP).sum())}")
    else:
        r2 = "주인 귀가 18:55"
    return {"left": "SIMULATION", "right": hm(c), "right2": r2}


def labels(t, anchors, sim):
    out = []
    a = anchors.get("hero")
    if a and a[3] and 4.8 < t < 33.8 and 520 < a[1] < 1450:
        out.append({"x": a[0], "y": a[1], "text": "고양이", "color": "orange", "size": 24, "lift": 40})
    a = anchors.get("tower")
    if a and a[3] and (0.4 < t < 4.4 or 34.4 < t < 39.6) and 470 < a[1] < 1430:
        out.append({"x": a[0], "y": a[1], "text": "롯데월드타워", "color": "white", "size": 24})
    return out
