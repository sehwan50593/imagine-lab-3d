"""EP24 만약에 하루가 12시간이라면? (20편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
식탁 창밖 해가 휙 지나고 벽시계 바늘이 빙글(훅) → 해가 뜨자마자 지는 거리 → 출근길 일출 → 점심 뒤 노을
→ 퇴근길에 또 일출 → 오후 3시인데 한밤중인 사무실 → 하품·졸음 Z·커피 컵 탑(시차증) → 밤 11시 대낮(커튼)
→ 달력 장이 날아감 → 반전: 지구의 하루는 길어지는 중(느리게 도는 지구본·창밖 공룡·달)
→ 짧은 하루엔 '나중에'가 사라짐(엄마에게 전화·만남) → 질문.
근거(설명란): 사람 생체시계 평균 약 24.2시간(Czeisler 외 1999, Science), 7천만 년 전 하루 약 23.5시간
(de Winter 외 2020, Paleoceanography and Paleoclimatology), 지금도 100년에 약 1.8밀리초씩 길어짐
(Stephenson 외 2016, Proceedings of the Royal Society A). 1년 730일 = 365.24일 x 24시간 / 12시간.
특수효과(시계 = 하루의 한 바퀴): 줄마다 시계 시각(TOD)을 정하면 sky()·창밖 유리색·해/달 블록·방 조명·벽시계 바늘이
모두 그 시각에서 나옴. 해는 07:00에 뜨고 13:00에 지고(낮 6시간) 밤 6시간 뒤 19:00에 다시 뜸(12시간 주기).
창밖 = 유리 띠·해·달·별·스카이라인을 상자 인스턴스로 매 프레임 새로 배치. 거리의 해·달은 카메라 화면 좌표로 배치.
"""
import json
import math
from pathlib import Path

import numpy as np

from engine.common import ramp

STYLE = "pixe"
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.3, 0.32, 1.6)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"home": (0, 0), "office": (300, 0), "street": (600, 0)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 하루가 열두 시간이라면 어떻게 될까요?", gap=0.7, shot=("home", (0.05, 1.05, 1.65), -90, 3, 3.5, 24, 0.93, 0)),
    dict(say="해가 뜨자마자, 금방 져 버려요", shot=("street", (1.2, 4.6, 1.75), 0, -8, 4.2, 24, 0.92, 0)),
    dict(say="출근길에 해가 뜨고", gap=0.7, shot=("street", (0.2, 4.6, 1.72), 0, -6, 5.6, 26, 0.9, 0)),
    dict(say="점심 먹고 나오니 벌써 노을이에요", shot=("street", (1.0, 4.6, 1.72), 0, -7, 4.2, 26, 0.93, 0)),
    dict(say="퇴근길엔 해가 또 떠요", gap=0.6, shot=("street", (0.8, 4.6, 1.72), 0, -5, 3.4, 28, 0.93, 0)),
    dict(say="눈 깜짝하면 하루가 끝나도", shot=("office", (0.0, 1.3, 1.9), -90, 3, 7.4, 24, 0.95, 0)),
    dict(say="회사는 여전히 시계대로 돌아가요", shot=("office", (0.0, 1.3, 1.75), -90, 3, 5.0, 26, 0.93, 0)),
    dict(say="몸속 시계는 아직 스물네 시간이라", shot=("office", (0.0, 1.75, 1.75), -90, 3, 4.2, 26, 0.92, 0)),
    dict(say="다들 하루 종일 시차증에 시달려요", gap=0.6, shot=("office", (0.05, 1.3, 1.45), -82, 4, 4.4, 24, 0.92, 4)),
    dict(say="밤 열한 시, 해가 쨍쨍해도 자야 하죠", shot=("home", (0.12, 1.6, 1.72), -90, 2, 3.6, 26, 0.93, 0)),
    dict(say="한 해가 730일이라 달력도 두꺼워졌어요", gap=0.5, shot=("home", (-0.1, 1.05, 1.2), -88, 5, 3.2, 26, 0.92, 0)),
    dict(say="그런데 사실, 지구의 하루는", shot=("home", (-0.2, 0.95, 1.15), -90, 4, 2.7, 28, 0.94, 0)),
    dict(say="지금도 조금씩 길어지고 있어요", shot=("home", (-0.1, 1.0, 1.45), -86, 4, 3.8, 24, 0.94, 3)),
    dict(say="7천만 년 전엔 스물세 시간 반이었죠", shot=("home", (0.0, 1.6, 1.6), -90, 3, 3.8, 24, 0.94, 0)),
    dict(say="달이 바닷물을 끌어당기면서", shot=("street", (1.0, 4.6, 1.72), 0, -9, 4.4, 24, 0.94, 0)),
    dict(say="지구의 자전이 느려지고 있거든요", gap=0.7, shot=("street", (1.0, 4.6, 1.72), 0, -7, 3.2, 28, 0.93, 0)),
    dict(say="하루가 이렇게 짧아지자,", gap=0.5, shot=("home", (0.0, 1.05, 1.45), -90, 3, 3.6, 26, 0.95, 0)),
    dict(say="사람들은 ‘나중에’를 미루지 않았어요", shot=("home", (0.0, 1.7, 1.7), -90, 3, 3.6, 26, 0.95, 0)),
    dict(say="보고 싶은 사람을 바로 만났죠", gap=0.7, shot=("home", (0.2, 1.05, 1.45), -90, 3, 3.8, 26, 0.95, 0)),
    dict(say="오늘 하루, 꼭 하고 싶은 게 뭔가요?", shot=("home", (0.2, 1.05, 1.45), -90, 3, 3.8, 26, 0.88, 0)),
]
TITLE = [("만약에", "white"), ("하루가", "white"), ("12시간이라면", "white"), ("어떻게 될까요?", "yellow")]
# 줄 번호 (아래 장면 효과·캐릭터 배치가 이 번호를 씀)
L_WHIRL, L_OFFICE, L_BODY, L_JET, L_BED, L_CAL = 5, 6, 7, 8, 9, 10
TWIST = 11          # '그런데 사실' 줄
L_GLOBE = (11, 12)  # 도는 지구본
L_DINO = 13         # 창밖 공룡
L_PHONE, L_MEET = 17, 18
assert all(k in LINES[i]["say"] for i, k in ((TWIST, "그런데 사실"), (L_JET, "시차증"), (L_BED, "열한 시"), (L_CAL, "730일"),
                                              (L_DINO, "7천만"), (L_MEET, "만났"), (L_PHONE, "나중에")))   # 줄 번호가 대본과 맞는지

# 줄마다 벽시계가 가리키는 시각(시) — (줄 시작, 줄 끝). 해는 7시에 뜨고 13시에 짐 (낮 6시간·밤 6시간, 12시간 주기)
TOD = [
    (8.8, 20.8),    # 0 훅: 시침이 한 바퀴 = 해가 한 번 뜨고 지고 밤
    (6.8, 17.0),    # 1 해가 뜨자마자 져 버림 → 밤
    (7.5, 8.4),     # 2 출근길 일출
    (12.1, 13.5),   # 3 점심 먹고 나오니 노을
    (19.15, 20.65), # 4 퇴근길에 또 일출 (앞쪽 30%에서 해가 건물 위로 올라옴)
    (7.6, 15.0),    # 5 사무실 창 셋에서 해가 휙 → 오후 3시 한밤중으로 이어짐
    (15.0, 15.1),   # 6 오후 3시인데 창밖은 한밤중
    (15.2, 15.35),  # 7
    (16.0, 16.15),  # 8
    (23.0, 23.15),  # 9 밤 11시인데 해가 쨍쨍
    (10.0, 10.15),  # 10 달력
    (10.0, 10.1),   # 11 반전: 느긋한 하루
    (10.1, 10.25),  # 12
    (9.0, 9.15),    # 13 창밖 공룡
    (2.8, 3.3),     # 14 한밤, 달
    (3.3, 3.8),     # 15
    (12.2, 12.35),  # 16 노을 (해가 창 한가운데 아래쪽)
    (12.4, 12.55),  # 17
    (12.6, 12.75),  # 18
    (12.8, 13.05),  # 19 해가 천천히 내려가 마지막에 짐
]
assert len(TOD) == len(LINES)

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep24_12hourday" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep24", "title": "만약에 하루가 12시간이라면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "G", "mode": "lydian", "bpm": 104, "seed": 241, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.92, "bloom": 0.14, "bloom_thr": 1.4, "vignette": 0.16}

HERO_SH, HERO_PA = (0.92, 0.33, 0.30), (0.15, 0.18, 0.30)        # 주인공: 산호색 셔츠
MOM_SH, MOM_PA = (0.95, 0.64, 0.72), (0.35, 0.28, 0.20)          # 엄마: 분홍 셔츠, 긴 머리
SUN_ROT = (38, 0, 22)                                             # 햇빛은 카메라 쪽 위에서 (얼굴이 밝게)
GLOW_N, LIT_N = 220, 240                                          # 인스턴스 칸 수 (발광 / 조명 받는 것)
NIGHT_LIFT = np.array((0.02, 0.035, 0.10))                        # 밤 창 유리의 남색


def line_at(t):
    """지금 몇 번째 줄(컷)인지. 첫 줄 앞 짧은 공백은 0번."""
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s - 0.02:
            i = k
    return i


def shot_span(i):
    a = 0.0 if i == 0 else STARTS[i]
    b = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    return a, b


def prog(t):
    """(줄 번호, 그 줄 진행도 0~1)"""
    i = line_at(t)
    a, b = shot_span(i)
    return i, min(max((t - a) / max(b - a, 1e-3), 0.0), 1.0)


def captions():
    """[(시작, 끝, 글)] — 첫 줄은 가운데 제목으로 보여 주므로 아래 자막에서 뺌."""
    return [(s, e, txt) for k, (s, e, txt) in enumerate(TIMELINE["lines"]) if k > 0]


def title_span():
    s, e, _ = TIMELINE["lines"][0]
    return s, e


def simulate(build_dir):
    return {"dur": np.float32(DUR)}


# ───────────────────────── 시각 → 하늘·빛 ─────────────────────────
def clock_h(i, u):
    a, b = TOD[i]
    return a + (b - a) * u


def phase(h):
    """시계 시각 → 해의 한 바퀴 위치 s (0=해 뜸, 0.5=해 짐, 0.5~1=밤). 12시간 주기, 7시에 해가 뜸."""
    return ((h - 7.0) / 12.0) % 1.0


SKY_KEYS = [  # (s, 위쪽 색, 아래쪽 색, 별)
    (0.00, (0.17, 0.20, 0.45), (1.00, 0.58, 0.36), 0.25),
    (0.05, (0.16, 0.27, 0.58), (0.95, 0.75, 0.62), 0.0),
    (0.12, (0.16, 0.30, 0.62), (0.55, 0.67, 0.85), 0.0),
    (0.38, (0.16, 0.30, 0.62), (0.55, 0.67, 0.85), 0.0),
    (0.45, (0.20, 0.20, 0.50), (0.98, 0.68, 0.45), 0.0),
    (0.50, (0.22, 0.13, 0.40), (1.00, 0.42, 0.22), 0.15),
    (0.55, (0.05, 0.05, 0.18), (0.50, 0.20, 0.25), 0.7),
    (0.62, (0.006, 0.010, 0.040), (0.040, 0.040, 0.120), 1.0),
    (0.90, (0.004, 0.006, 0.020), (0.012, 0.016, 0.040), 1.0),
    (0.95, (0.030, 0.040, 0.120), (0.300, 0.200, 0.300), 0.7),
    (1.00, (0.17, 0.20, 0.45), (1.00, 0.58, 0.36), 0.25),
]


def sky_key(s):
    """s에서의 (위쪽 색, 아래쪽 색, 별 밝기) — 키 사이를 직선으로 이음."""
    for (s0, t0, b0, g0), (s1, t1, b1, g1) in zip(SKY_KEYS, SKY_KEYS[1:]):
        if s0 <= s <= s1:
            w = (s - s0) / (s1 - s0)
            return (tuple(p + (q - p) * w for p, q in zip(t0, t1)), tuple(p + (q - p) * w for p, q in zip(b0, b1)),
                    g0 + (g1 - g0) * w)
    return SKY_KEYS[0][1], SKY_KEYS[0][2], SKY_KEYS[0][3]


def level(s):
    """낮 밝기 0~1 (해 뜰 때 올라가고 질 때 내려감, 밤엔 0)."""
    q = s if s < 0.75 else s - 1.0
    return ramp(q, -0.03, 0.07) * (1.0 - ramp(q, 0.43, 0.53))


def twilight(s):
    """해 뜨기·지기 앞뒤의 붉은 기운 0~1."""
    d = min(abs(s), abs(s - 0.5), abs(s - 1.0))
    return max(0.0, 1.0 - d / 0.09)


def lerpc(a, b, w):
    return tuple(p + (q - p) * w for p, q in zip(a, b))


def sky(t):
    i, u = prog(t)
    return sky_key(phase(clock_h(i, u)))


# ───────────────────────── 카메라 도우미 (블렌더 없이 계산) ─────────────────────────
def cam_basis(tg, az, el, dist):
    """CamRig.set과 같은 규칙: (카메라 위치, 앞, 오른쪽, 위)."""
    a, e = math.radians(az), math.radians(el)
    t = np.array(tg, float)
    loc = t + np.array((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))) * dist
    fwd = t - loc
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, (0.0, 0.0, 1.0))
    right /= np.linalg.norm(right)
    return loc, fwd, right, np.cross(right, fwd)


def shot_cam(i, u):
    """줄 i, 진행도 u의 카메라: (위치, 앞, 오른쪽, 위, 렌즈, 목표점, 거리)."""
    st, tg, az, el, dist, lens, push, daz = LINES[i]["shot"]
    o = OFF[st]
    tgt = (tg[0] + o[0], tg[1] + o[1], tg[2])
    dn = dist * (1 + (push - 1) * u)
    loc, fwd, right, up = cam_basis(tgt, az + daz * u, el, dn)
    return loc, fwd, right, up, lens, tgt, dn


def face_pt(d, fwd, up):
    """캐릭터 얼굴 앞 점(세트 기준): 앞(+x→yaw)으로 fwd, 머리 아래면(hz)에서 위로 up. 크기 반영."""
    s = d["scale"]
    hz = 1.05 if d["pose"].startswith("sit") else 1.36
    a = math.radians(d["yaw"])
    return d["x"] + math.cos(a) * fwd * s, d["y"] + math.sin(a) * fwd * s, d["z"] + (hz + up) * s


# ───────────────────────── 세트 ─────────────────────────
WIN = {
    "home": dict(set="home", x0=-1.05, x1=-0.15, z0=0.95, z1=1.85, y=2.5),
    "oc": dict(set="office", x0=-0.9, x1=0.9, z0=0.95, z1=2.85, y=3.2),
    "ol": dict(set="office", x0=-3.5, x1=-1.7, z0=0.95, z1=2.85, y=3.2),
    "or": dict(set="office", x0=1.7, x1=3.5, z0=0.95, z1=2.85, y=3.2),
}
CLK = {"home": dict(set="home", x=0.88, z=1.45, r=0.28, y=2.5),
       "office": dict(set="office", x=0.0, z=3.65, r=0.38, y=3.2)}


def _window_frame(v, w, mull=False):
    """창틀(흰 상자)·창턱. 유리는 인스턴스로 따로 그려서 색이 바뀜."""
    x0, x1, z0, z1, y = w["x0"], w["x1"], w["z0"], w["z1"], w["y"]
    t, d, fr = 0.07, 0.10, (0.95, 0.95, 0.93)
    v.box(x0 - t, x1 + t, y - d, y, z0 - t, z0, fr, jit=0.01)
    v.box(x0 - t, x1 + t, y - d, y, z1, z1 + t, fr, jit=0.01)
    v.box(x0 - t, x0, y - d, y, z0, z1, fr, jit=0.01)
    v.box(x1, x1 + t, y - d, y, z0, z1, fr, jit=0.01)
    if mull:
        xm = (x0 + x1) / 2
        v.box(xm - t / 2, xm + t / 2, y - d * 0.7, y, z0, z1, fr, jit=0.01)
    v.box(x0 - t - 0.06, x1 + t + 0.06, y - d - 0.08, y, z0 - t - 0.04, z0 - t, fr, jit=0.01)


def _clock_face(v, ck):
    """벽시계 판·테두리·눈금 (바늘은 인스턴스)."""
    cx, z, r, y = ck["x"], ck["z"], ck["r"], ck["y"]
    v.box(cx - r - 0.04, cx + r + 0.04, y - 0.06, y, z - r - 0.04, z + r + 0.04, (0.18, 0.18, 0.2), jit=0)
    v.box(cx - r, cx + r, y - 0.075, y - 0.06, z - r, z + r, (0.97, 0.96, 0.93), jit=0)
    for k in range(12):
        ph = math.radians(30 * k)
        px, pz = cx + 0.82 * r * math.sin(ph), z + 0.82 * r * math.cos(ph)
        s = (0.16 if k % 3 == 0 else 0.10) * r
        v.box(px - s / 2, px + s / 2, y - 0.087, y - 0.075, pz - s / 2, pz + s / 2, (0.12, 0.12, 0.14), jit=0)
    v.box(cx - 0.02, cx + 0.02, y - 0.125, y - 0.075, z - 0.02, z + 0.02, (0.12, 0.12, 0.14), jit=0)


def _home(v):
    from engine import voxel as X
    H = 4.6
    v.floor(-3.2, 3.2, -2.6, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    v.wall((-3.2, 2.5), (3.2, 2.5), 0, H, (0.20, 0.36, 0.44), 0.25, face=-1)
    v.wall((-3.2, -2.6), (-3.2, 2.5), 0, H, (0.24, 0.40, 0.48), 0.25, face=-1)
    v.wall((3.2, -2.6), (3.2, 2.5), 0, H, (0.24, 0.40, 0.48), 0.25, face=1)
    v.box(-0.9, 1.8, -0.4, 1.7, 0, 0.015, (0.45, 0.58, 0.68), jit=0.02)                   # 러그
    _window_frame(v, WIN["home"])
    _clock_face(v, CLK["home"])
    X.table(v, 0.45, 0.25, 2.3, 0.9, 0.74, (0.85, 0.72, 0.52))
    X.chair(v, 0.0, 1.05, -90)
    X.chair(v, 0.7, 1.05, -90)
    for x in (0.0, 0.7):                                                                  # 접시·컵
        v.box(x - 0.14, x + 0.14, 0.43, 0.67, 0.74, 0.765, (0.97, 0.97, 0.95), jit=0)
        v.box(x + 0.25, x + 0.35, 0.42, 0.52, 0.74, 0.86, (0.95, 0.6, 0.2) if x == 0.0 else (0.35, 0.55, 0.85))
    v.box(-0.07, 0.07, 0.49, 0.61, 0.765, 0.80, (0.95, 0.85, 0.3), jit=0)                 # 계란 노른자
    v.box(0.45, 1.3, 2.0, 2.48, 0, 0.8, (0.92, 0.92, 0.9))                                # 서랍장 + 화분
    v.box(0.95, 1.2, 2.1, 2.35, 0.8, 0.9, (0.35, 0.6, 0.45))
    v.box(0.9, 1.25, 2.05, 2.4, 0.9, 1.1, (0.25, 0.55, 0.25), jit=0.1)
    v.light(0.45, 0.25, 2.4, 60, (1.0, 0.9, 0.75), 0.4, "ep24_h_pend")
    v.light(-0.62, 2.0, 1.45, 80, (0.85, 0.92, 1.0), 1.0, "ep24_h_win")


def _office(v):
    from engine import voxel as X
    H = 5.2
    v.floor(-4.5, 4.5, -3.2, 3.2, (0.55, 0.57, 0.6), 0.5, "check")
    v.wall((-4.5, 3.2), (4.5, 3.2), 0, H, (0.80, 0.84, 0.88), 0.5, face=-1)
    v.wall((-4.5, -3.2), (-4.5, 3.2), 0, H, (0.78, 0.82, 0.86), 0.5, face=-1)
    v.wall((4.5, -3.2), (4.5, 3.2), 0, H, (0.78, 0.82, 0.86), 0.5, face=1)
    for k in ("oc", "ol", "or"):
        _window_frame(v, WIN[k], mull=True)
    _clock_face(v, CLK["office"])
    for cx in (-1.6, 0.0, 1.6):                                                           # 책상 줄 + 노트북 + 의자
        X.table(v, cx, 0.6, 1.4, 0.8, 0.74, (0.92, 0.92, 0.9))
        v.box(cx - 0.17, cx + 0.17, 0.5, 0.78, 0.74, 0.76, (0.55, 0.57, 0.6), jit=0.02)
        v.box(cx - 0.17, cx + 0.17, 0.46, 0.475, 0.76, 0.98, (0.4, 0.42, 0.46), jit=0.02)
        X.chair(v, cx, 1.3, -90, (0.2, 0.22, 0.26))
        if cx:
            v.box(cx + 0.35, cx + 0.45, 0.45, 0.55, 0.74, 0.8, (0.95, 0.95, 0.95))
    v.box(-4.3, -3.8, 2.4, 2.9, 0, 0.5, (0.35, 0.6, 0.45))                                # 화분
    v.box(-4.35, -3.75, 2.35, 2.95, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.4, 0.0, 2.4):
        v.box(x - 0.6, x + 0.6, 0.7, 1.3, 4.95, 5.0, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 1.0, 3.8, 170, (0.95, 0.97, 1.0), 0.6, {-2.4: "ep24_o_l", 0.0: "ep24_o_c", 2.4: "ep24_o_r"}[x])


TOWER_COLS = [(0.42, 0.45, 0.55), (0.55, 0.42, 0.38), (0.38, 0.5, 0.45), (0.5, 0.5, 0.42), (0.45, 0.4, 0.55)]


def _lamp(v, x, y, name=None, h=4.2):
    v.box(x - 0.06, x + 0.06, y - 0.06, y + 0.06, 0, h, (0.25, 0.26, 0.28))
    v.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, h, h + 0.12, (0.25, 0.26, 0.28))
    v.box(x - 0.16, x + 0.16, y - 0.16, y + 0.16, h - 0.05, h, (1.0, 0.85, 0.55), jit=0, glow=True)
    if name:
        v.light(x, y, h - 0.3, 200.0, (1.0, 0.8, 0.55), 0.3, name)


def _street(v):
    from engine import voxel as X
    rs = v.rs
    XA, XB = -46.0, 20.0
    v.floor(XA, XB, -3, 3, (0.32, 0.32, 0.34), 0.5)
    for x in np.arange(XA + 1, XB, 3.0):
        v.box(x, x + 1.4, -0.06, 0.06, 0.0, 0.012, (0.95, 0.95, 0.9), jit=0)
    for y0, y1 in ((3, 6), (-6, -3)):
        v.box(XA, XB, y0, y1, 0, 0.12, (0.62, 0.62, 0.62), jit=0)
        v.floor(XA, XB, y0, y1, (0.74, 0.7, 0.64), 0.5, "check", z=0.121)
    signs = [(0.95, 0.3, 0.3), (0.3, 0.8, 1.0), (1.0, 0.8, 0.2), (0.4, 1.0, 0.5), (1.0, 0.5, 0.85), (1.0, 0.6, 0.2)]
    for face, y in ((-1, 6.0), (1, -6.0)):                                                # 길가 가게 (먼 쪽일수록 낮게)
        x, k = XA, face
        while x < XB:
            w = float(rs.uniform(4.5, 7.0))
            hmax = 9.0 + 4.0 * ramp(x, -10.0, 10.0) if x > -10 else 7.0 + 2.0 * (x > -30)
            top = hmax + 2.0 if face < 0 else min(hmax + 2.0, 11.0)       # 햇빛 쪽(남쪽) 건물은 낮게: 인도에 그림자가 안 드리우게
            X.storefront(v, x, min(XB, x + w), y, 5.0, float(rs.uniform(7.0, top)), signs[k % 6], face=face, lit=0.35)
            x += w
            k += 1
    yy, k = -34.0, 0                                                                      # 길 끝을 막는 낮은 빌딩 줄
    while yy < 34:
        w = float(rs.uniform(4.0, 7.0))
        h = float(rs.uniform(6.0, 7.5) if -9 < yy < 11 else rs.uniform(8.0, 14.0))   # 해·달이 지나는 가운데는 낮게
        v.box(XA - 9, XA, yy, yy + w, 0, h, TOWER_COLS[k % len(TOWER_COLS)], jit=0.03)
        nx = max(1, int(w / 1.5))
        for r in range(int((h - 2.5) / 2.2)):
            for c in range(nx):
                on = rs.random() < 0.4
                py = yy + (c + 0.5) * w / nx
                v.box(XA, XA + 0.03, py - 0.4, py + 0.4, 2.0 + r * 2.2, 3.1 + r * 2.2,
                      (0.75, 0.58, 0.32) if on else (0.05, 0.06, 0.09), jit=0, glow=on)
        yy += w
        k += 1
    for n, x in enumerate((10, 2)):                                                       # 가로등은 카메라 뒤·옆에만 (화면 안의 기둥이
        _lamp(v, x, 3.4, f"ep24_s_l{n}")                                                  # 주인공 머리 뒤·해 앞에 겹쳐 서 보이지 않게)


# ───────────────────────── 캐릭터 배치 ─────────────────────────
def cast():
    """[dict(set, x, y, yaw, pose, hair, shirt, pants, scale, z, over={줄: 덮어쓰기}, only=보이는 줄 집합 or None,
    walk={줄: 걷는 속도 m/s(앞 방향)})]"""
    from engine import voxel as X
    rs = np.random.default_rng(24)
    S, Pn = X.SHIRTS, X.PANTS
    C = []

    def add(st, x, y, yaw, pose, hair=0, shirt=None, pants=None, scale=1.0, z=0.0, over=None, only=None, walk=None):
        C.append(dict(set=st, x=x, y=y, yaw=yaw, pose=pose, hair=hair,
                      shirt=shirt or S[int(rs.integers(len(S)))], pants=pants or Pn[int(rs.integers(len(Pn)))],
                      scale=scale, z=z, over=over or {}, only=only, walk=walk or {}))
    sw = dict(set="street", y=4.6, yaw=0, z=0.12)
    hero_over = {
        0: dict(pose="sit_conf"),
        1: dict(sw, x=1.2, pose="confused"),
        2: dict(sw, x=0.2, pose="walk_a"),
        3: dict(sw, x=1.0, pose="stand"),
        4: dict(sw, x=0.8, pose="talk"),
        L_WHIRL: dict(set="office", x=0.0, y=1.3, pose="sit"),
        L_OFFICE: dict(set="office", x=0.0, y=1.3, pose="sit"),
        L_BODY: dict(set="office", x=0.0, y=1.78, pose="talk"),
        L_JET: dict(set="office", x=0.0, y=1.3, pose="sit_conf"),
        L_BED: dict(x=0.3, y=1.75, pose="talk"),
        L_CAL: dict(pose="sit_conf"),
        L_DINO: dict(x=0.3, y=1.75, pose="confused"),
        14: dict(sw, x=1.0, pose="stand"),
        15: dict(sw, x=1.0, pose="confused"),
        L_PHONE: dict(x=0.0, y=1.75, pose="phone"),
    }
    # 주인공: 산호색 셔츠 짧은 머리 (줄마다 자리·자세)
    add("home", 0.0, 1.05, -90, "sit", 0, HERO_SH, HERO_PA, over=hero_over, walk={2: 0.9})
    # 엄마: 마지막 두 줄
    add("home", 0.7, 1.05, -90, "sit", 1, MOM_SH, MOM_PA, only={L_MEET, L_MEET + 1})
    # 사무실 동료
    off = {L_WHIRL, L_OFFICE, L_BODY, L_JET}
    add("office", -1.6, 1.3, -90, "sit", 1, (0.35, 0.65, 0.40), (0.2, 0.2, 0.22), only=off)
    add("office", 1.6, 1.3, -90, "sit", 0, (0.3, 0.3, 0.34), (0.15, 0.15, 0.18), only=off,
        over={L_JET: dict(pose="sit_conf")})
    return C


def actor(c, i, el):
    """줄 i, 그 줄이 시작된 뒤 el초에서 캐릭터 c의 상태. 걷는 줄은 앞으로 이동하며 걸음 자세를 번갈아."""
    d = dict(c)
    d.update(c["over"].get(i, {}))
    sp = c["walk"].get(i, 0.0)
    if sp:
        a = math.radians(d["yaw"])
        d["x"] += math.cos(a) * sp * el
        d["y"] += math.sin(a) * sp * el
        d["pose"] = "walk_a" if int(el / 0.34) % 2 == 0 else "walk_b"
    return d


def crowd(n=30, seed=241):
    rs = np.random.default_rng(seed)
    lane = rs.choice([1.3, 2.3, 3.3, 3.6, 5.8, -3.8, -4.6], n) + rs.uniform(-0.1, 0.1, n)
    d = np.where(rs.random(n) < 0.5, 1.0, -1.0)
    x0 = rs.uniform(-40, 20, n)
    spd = rs.uniform(0.9, 1.4, n)
    ph = rs.uniform(0, 1, n)
    hair = (rs.random(n) < 0.45).astype(int)
    from engine import voxel as X
    pick = [0, 2, 3, 4, 5, 6, 8]                    # 주인공 산호색·엄마 분홍과 헷갈리는 색은 뺌
    sh = np.array([X.SHIRTS[pick[k]] for k in rs.integers(len(pick), size=n)], np.float32)
    pa = np.array([X.PANTS[i] for i in rs.integers(len(X.PANTS), size=n)], np.float32)
    return dict(lane=lane, d=d, x0=x0, spd=spd, ph=ph, hair=hair, sh=sh, pa=pa)


# ───────────────────────── 효과 상자 목록 ─────────────────────────
def _rmat(rx, ry, rz):
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    return (np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]) @ np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @
            np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]))


class Items:
    """상자 인스턴스 모음. 상자 원점 = 뒷면 가운데, +x로 뻗음(size로 늘림). c()는 가운데 기준으로 넣음."""

    def __init__(self, cap):
        self.cap, self.P, self.S, self.R, self.C = cap, [], [], [], []

    def o(self, origin, size, col, rot=(0.0, 0.0, 0.0)):
        self.P.append(tuple(float(q) for q in origin))
        self.S.append(tuple(float(q) for q in size))
        self.R.append(tuple(float(q) for q in rot))
        self.C.append(tuple(float(q) for q in col))

    def c(self, center, size, col, rot=(0.0, 0.0, 0.0)):
        org = np.asarray(center, float) - _rmat(*rot) @ np.array((size[0] / 2, 0.0, 0.0))
        self.o(org, size, col, rot)

    def arrays(self):
        n = len(self.P)
        assert n <= self.cap, f"인스턴스 칸 부족: {n} > {self.cap}"
        pad = self.cap - n
        z3 = [(0.0, 0.0, 0.0)] * pad
        return (np.array(self.P + z3, np.float32), np.array([1.0] * n + [0.0] * pad, np.float32),
                np.array(self.S + [(0.0, 0.0, 0.0)] * pad, np.float32), np.array(self.R + z3, np.float32),
                np.array(self.C + z3, np.float32))


STAR_UV = [(0.12, 0.88), (0.30, 0.72), (0.45, 0.93), (0.62, 0.78), (0.80, 0.90), (0.90, 0.68), (0.22, 0.58),
           (0.72, 0.62)]
SKYBLK = [(0.00, 0.15, 0.17), (0.15, 0.28, 0.10), (0.28, 0.43, 0.24), (0.43, 0.56, 0.13), (0.56, 0.71, 0.27),
          (0.71, 0.85, 0.15), (0.85, 1.00, 0.21)]
DOTS = [(2, 0.30, 0.45), (2, 0.65, 0.70), (4, 0.25, 0.30), (4, 0.70, 0.55), (4, 0.50, 0.80), (0, 0.50, 0.50),
        (6, 0.40, 0.50), (6, 0.75, 0.70), (3, 0.50, 0.50), (5, 0.50, 0.50)]
# 옆모습 공룡: (가운데 x, 가운데 z, 가로, 세로, 색) — 발 중앙이 원점, 오른쪽을 봄
DINO = [(0.0, 0.42, 0.52, 0.28, (0.30, 0.62, 0.30)), (0.04, 0.33, 0.40, 0.10, (0.58, 0.80, 0.46)),
        (-0.30, 0.45, 0.22, 0.24, (0.30, 0.62, 0.30)), (-0.48, 0.42, 0.20, 0.16, (0.30, 0.62, 0.30)),
        (-0.64, 0.38, 0.18, 0.11, (0.28, 0.58, 0.28)), (-0.78, 0.35, 0.14, 0.07, (0.26, 0.54, 0.26)),
        (0.30, 0.60, 0.15, 0.22, (0.30, 0.62, 0.30)), (0.42, 0.76, 0.28, 0.17, (0.32, 0.66, 0.32)),
        (0.46, 0.665, 0.22, 0.05, (0.85, 0.45, 0.45)), (0.26, 0.40, 0.07, 0.04, (0.26, 0.54, 0.26)),
        (0.30, 0.355, 0.07, 0.04, (0.26, 0.54, 0.26))]


def window_items(G, w, s, mode="city", t=0.0, u=0.0):
    """창 하나의 '바깥 풍경'을 상자로: 유리 띠(하늘 위·아래 색)·해/달·별·스카이라인·불빛. 시각 s에서 매 프레임 새로."""
    ox, oy = OFF[w["set"]]
    x0, x1, z0, z1, y = w["x0"] + ox, w["x1"] + ox, w["z0"], w["z1"], w["y"] + oy
    ww, hh = x1 - x0, z1 - z0
    m = min(ww, hh)
    top, bot, stars = sky_key(s)
    L = level(s)
    night = 1.0 - L
    for k in range(6):                                                    # 유리: 아래(수평선 색)→위(하늘 색)
        f = (k + 0.5) / 6.0
        col = (np.array(bot) + (np.array(top) - np.array(bot)) * f) * 1.5 + NIGHT_LIFT * night
        G.c(((x0 + x1) / 2, y - 0.010, z0 + hh * f), (ww, 0.012, hh / 6 + 0.003), col)
    if s < 0.5:                                                           # 해: 왼쪽 아래 → 위 → 오른쪽 아래
        a = s / 0.5
        arc = math.sin(math.pi * a)
        k = ramp(arc, 0.0, 0.3)
        col = np.array((1.0, 0.50, 0.20)) * (1 - k) * 5.0 + np.array((1.0, 0.88, 0.40)) * k * 6.0
        S = 0.30 * m
        G.c((x0 + ww * (0.10 + 0.80 * a), y - 0.020, z0 + hh * (0.12 + 0.62 * arc)), (S, 0.012, S), col)
    else:                                                                 # 달 (크레이터 점 셋)
        b = (s - 0.5) / 0.5
        arc = math.sin(math.pi * b)
        M = 0.22 * m
        mx, mz = x0 + ww * (0.10 + 0.80 * b), z0 + hh * (0.20 + 0.62 * arc)
        G.c((mx, y - 0.020, mz), (M, 0.012, M), (2.6, 2.8, 3.2))
        for dx, dz, r in ((-0.22, 0.20, 0.20), (0.20, -0.18, 0.16), (0.12, 0.25, 0.10)):
            G.c((mx + dx * M, y - 0.0275, mz + dz * M), (r * M, 0.004, r * M), (1.4, 1.6, 2.1))
    if stars > 0.05:
        for k, (uu, vv) in enumerate(STAR_UV):
            tw = stars * (0.75 + 0.25 * math.sin(t * 5.0 + k * 1.7))
            q = 0.03 * m / 0.9
            G.c((x0 + ww * uu, y - 0.015, z0 + hh * vv), (q, 0.01, q), (3.0 * tw, 3.0 * tw, 3.0 * tw))
    if mode == "dino":
        _prehistoric(G, x0, x1, z0, z1, y, ww, hh, m, t, u)
        return
    sk = (np.array((0.30, 0.36, 0.50)) * L + np.array((0.012, 0.016, 0.035)) * night) * (1.0 + 0.5 * twilight(s))
    for u0, u1, hf in SKYBLK:                                             # 스카이라인
        G.c((x0 + ww * (u0 + u1) / 2, y - 0.030, z0 + hh * hf / 2), (ww * (u1 - u0), 0.02, hh * hf), sk)
    amp = ramp(night, 0.35, 0.8)
    if amp > 0.01:
        q = 0.035 * m / 0.9
        for bi, uu, vv in DOTS:                                           # 밤엔 건물 불빛
            u0, u1, hf = SKYBLK[bi]
            G.c((x0 + ww * (u0 + (u1 - u0) * uu), y - 0.045, z0 + hh * hf * vv), (q, 0.005, q),
                (2.5 * amp, 2.0 * amp, 1.0 * amp))


def _prehistoric(G, x0, x1, z0, z1, y, ww, hh, m, t, u):
    """7천만 년 전 창밖: 땅·야자수 둘·걷는 공룡."""
    G.c(((x0 + x1) / 2, y - 0.030, z0 + hh * 0.04), (ww, 0.02, hh * 0.08), (0.30, 0.62, 0.22))
    for px in (x0 + 0.10 * ww, x0 + 0.92 * ww):
        top = z0 + hh * 0.52
        G.c((px, y - 0.030, z0 + hh * 0.30), (0.05 * m / 0.9, 0.02, hh * 0.44), (0.55, 0.36, 0.18))
        G.c((px, y - 0.040, top), (0.14 * m / 0.9, 0.02, 0.05 * m / 0.9), (0.20, 0.58, 0.18))
        for sgn in (-1, 1):
            G.c((px + sgn * 0.10 * m / 0.9, y - 0.040, top - 0.03), (0.14 * m / 0.9, 0.02, 0.04 * m / 0.9),
                (0.18, 0.52, 0.16), rot=(0.0, sgn * 0.45, 0.0))
        G.c((px, y - 0.040, top + 0.05), (0.04 * m / 0.9, 0.02, 0.10 * m / 0.9), (0.22, 0.62, 0.20))
    sc = 0.75 * m / 0.9
    bx, bz = x0 + ww * (0.38 + 0.18 * u), z0 + hh * 0.06
    sw = 0.05 * math.sin(t * 9.0)
    for cx, cz, sx, sz, col in DINO:
        G.c((bx + sc * cx, y - 0.050, bz + sc * cz), (sc * sx, 0.03, sc * sz), tuple(q * 1.3 for q in col))
    for k, sg in enumerate((1, -1)):                                      # 걷는 다리 (앞뒤로 엇갈려 흔듦)
        G.c((bx + sc * (-0.02 + sw * sg), y - 0.045 - 0.01 * k, bz + sc * 0.14), (sc * 0.14, 0.03, sc * 0.28),
            tuple(q * 1.3 for q in (0.28, 0.58, 0.28)))
        G.c((bx + sc * (0.05 + sw * sg), y - 0.045 - 0.01 * k, bz + sc * 0.025), (sc * 0.22, 0.03, sc * 0.05),
            tuple(q * 1.3 for q in (0.24, 0.50, 0.24)))
    G.c((bx + sc * 0.46, y - 0.066, bz + sc * 0.80), (sc * 0.05, 0.01, sc * 0.05), (3.0, 3.0, 3.0))      # 눈
    G.c((bx + sc * 0.47, y - 0.072, bz + sc * 0.80), (sc * 0.025, 0.01, sc * 0.035), (0.02, 0.02, 0.02))


def clock_items(G, ck, h):
    """벽시계 바늘: 시침은 시각 h에 맞춰 12시간에 한 바퀴, 분침은 1시간에 한 바퀴 (뒤집지 않고 앞 보는 벽 기준)."""
    ox, oy = OFF[ck["set"]]
    cx, z, r, y = ck["x"] + ox, ck["z"], ck["r"], ck["y"] + oy
    for L, wd, dy, ang in ((0.50 * r, 0.16 * r, 0.095, 360.0 * ((h / 12.0) % 1.0)),
                           (0.76 * r, 0.10 * r, 0.110, 360.0 * (h % 1.0))):
        G.o((cx, y - dy, z), (L, 0.012, wd), (0.03, 0.03, 0.04), (0.0, math.radians(ang) - math.pi / 2, 0.0))


Z_PAT = [(0, 0), (1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (2, 2)]
HEART_PAT = [(1, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (1, 3),
             (2, 3), (3, 3), (2, 4)]


def glyph(G, pat, x, y, z, cell, col):
    """앞(−y쪽 카메라)을 보는 도트 글자: (x, z)는 왼쪽 위 칸 가운데."""
    for c, r in pat:
        G.c((x + c * cell, y, z - r * cell), (cell * 0.92, 0.02, cell * 0.92), col)


def zzz(G, d, t, n=3):
    """자는 듯 졸린 캐릭터 머리 위로 Z가 커지며 떠오름."""
    top = d["z"] + (1.51 if d["pose"].startswith("sit") else 1.82) * d["scale"]
    ox, oy = OFF[d["set"]]
    for k in range(n):
        f = (t * 0.55 + k / n) % 1.0
        cell = (0.035 + 0.045 * f) * d["scale"]
        a = 1.0 - ramp(f, 0.75, 1.0)
        col = (2.2 * a, 2.6 * a, 3.2 * a)
        glyph(G, Z_PAT, d["x"] + ox + 0.15 + 0.35 * f, d["y"] + oy, top + 0.15 + 0.55 * f, cell, col)


def globe_cells(R=0.2, cell=0.05):
    """블록 지구본: 속이 빈 구 껍질 [(x, y, z, 색)] — 바다 파랑·땅 초록·극지 흰색."""
    n = int(round(R / cell)) + 1
    g = np.arange(-n, n + 1) * cell
    gx, gy, gz = np.meshgrid(g, g, g, indexing="ij")
    inside = gx ** 2 + gy ** 2 + gz ** 2 <= (R + 1e-6) ** 2
    sh = np.zeros_like(inside)
    for ax in range(3):
        for dd in (-1, 1):
            sh |= ~np.roll(inside, dd, ax)
    out = []
    for x, y, z in zip(gx[inside & sh], gy[inside & sh], gz[inside & sh]):
        xn, yn, zn = x / R, y / R, z / R
        land = math.sin(3.1 * xn + 1.0) * math.sin(2.7 * yn + 2.0) + 0.7 * math.sin(3.9 * zn + 0.5) > 0.35
        c = (0.95, 0.97, 1.0) if abs(zn) > 0.82 else ((0.30, 0.70, 0.30) if land else (0.15, 0.40, 0.85))
        out.append((x, y, z, c))
    return out


GLOBE = globe_cells()
CAL_X, CAL_Y = -0.45, 0.30                                                # 식탁 위 달력·지구본 자리


def home_props(Lt, G, i, u, el, t, s, h):
    """집 줄마다 따로 나오는 소품: 커튼(L_BED)·달력 더미와 날리는 장(L_CAL)·도는 지구본(L_GLOBE)·하트(L_MEET)."""
    w = WIN["home"]
    ox, oy = OFF["home"]
    if i == L_BED:                                                        # 해가 쨍쨍해서 커튼을 침
        k = ramp(u, 0.45, 0.85)                                           # '자야 하죠'에 맞춰 닫힘
        Lc = 0.12 + 0.40 * k
        col = (0.78, 0.30, 0.35)
        Lt.o((w["x0"] + ox - 0.06, w["y"] + oy - 0.13, 1.45), (Lc, 0.05, 1.15), col)
        Lt.o((w["x1"] + ox + 0.06, w["y"] + oy - 0.13, 1.45), (Lc, 0.05, 1.15), col, (0.0, 0.0, math.pi))
    if i == L_CAL:                                                        # 달력 더미가 쑥쑥 두꺼워지고 장이 날아감
        k = ramp(u, 0.25, 0.7)                                            # '두꺼워졌어요'에 맞춰 두꺼워짐
        Hh = 0.05 + 0.5 * k
        Lt.c((CAL_X + ox, CAL_Y + oy, 0.74 + Hh / 2), (0.30, 0.20, Hh), (0.96, 0.96, 0.94))
        Lt.c((CAL_X + ox, CAL_Y + oy, 0.74 + Hh + 0.01), (0.30, 0.20, 0.02), (0.85, 0.20, 0.20))
        if u > 0.04:
            for n in range(12):
                f = (el * 1.5 + n / 12.0) % 1.0
                vx = (0.9 if n % 2 else -0.9) * (0.4 + 0.6 * ((n * 7) % 5) / 4.0)
                sz = 0.95 * (1.0 - ramp(f, 0.75, 1.0)) * ramp(f, 0.0, 0.08)
                if sz > 0.02:
                    Lt.c((CAL_X + ox + vx * f, CAL_Y + oy - 0.5 * f, 0.74 + Hh + 0.05 + 0.9 * f - 0.35 * f * f),
                         (0.26 * sz, 0.006, 0.18 * sz), (0.97, 0.97, 0.95), (6.0 * f * (1 if n % 3 else -1), 0.0,
                                                                         4.0 * f * (1 if n % 2 else -1)))
    if i in L_GLOBE:                                                      # 지구본: 앞 줄에선 빨리 돌다가 뒷 줄에서 느려짐
        psi = 6.0 * el if i == L_GLOBE[0] else 6.0 * el * (1.0 - 0.45 * u)     # 각속도 6 → 0.6 rad/s로 느려짐
        gx, gy, gz = CAL_X + ox, CAL_Y + oy, 0.74 + 0.06 + 0.2
        Lt.c((gx, gy, 0.74 + 0.015), (0.16, 0.16, 0.03), (0.55, 0.38, 0.22))
        Lt.c((gx, gy, 0.74 + 0.05), (0.03, 0.03, 0.06), (0.55, 0.38, 0.22))
        cs, sn = math.cos(psi), math.sin(psi)
        for x, y, z, c in GLOBE:
            Lt.c((gx + x * cs - y * sn, gy + x * sn + y * cs, gz + z), (0.05, 0.05, 0.05), c, (0.0, 0.0, psi))
    if i == L_MEET:                                                       # 둘 사이로 하트가 퐁퐁
        for n in range(3):
            f = ((el - 0.15 * n) * 0.7) % 1.0
            if el > 0.15 * n:
                a = 1.0 - ramp(f, 0.7, 1.0)
                cell = 0.05
                glyph(G, HEART_PAT, ox + (0.10 + 0.25 * n + 0.2 * f) - 2 * cell, oy + 0.9, 1.85 + 0.5 * f, cell,
                      (3.0 * a, 0.7 * a, 1.2 * a))


CUPS = [(0.45, 0.74), (0.55, 0.74), (0.65, 0.74), (0.50, 0.85), (0.60, 0.85), (0.55, 0.96), (-0.45, 0.74),
        (-0.55, 0.74), (-0.50, 0.85)]


def office_props(Lt, G, i, u, el, t, s, h):
    ox, oy = OFF["office"]
    if i == L_JET:                                                        # 커피 컵이 하나씩 쌓임
        for n, (cx, cz) in enumerate(CUPS):
            if u > 0.05 + 0.04 * n:
                Lt.c((cx + ox, 0.40 + oy, cz + 0.055), (0.085, 0.085, 0.11), (0.97, 0.97, 0.95))
                Lt.c((cx + ox, 0.40 + oy, cz + 0.05), (0.09, 0.09, 0.04), (0.65, 0.45, 0.28))


def sky_body(s):
    """거리 하늘의 해(s<0.5)·달: (종류, nx, ny) — 카메라 화면 좌표(오른쪽 +, 위 +). 왼쪽 아래에서 떠올라 위를 지나 오른쪽 아래로."""
    if s < 0.5:
        a = s / 0.5
        return "sun", -0.62 + 0.78 * a, -0.06 + 0.80 * math.sin(math.pi * a)
    b = (s - 0.5) / 0.5
    return "moon", -0.55 + 0.70 * b, -0.06 + 0.72 * math.sin(math.pi * b)


def street_sky(G, s, loc, fwd, right, up, lens):
    """거리의 해·달 블록: 카메라 화면 좌표로 100m 밖에 두어 먼 건물 뒤에서 떠오르고 가려짐."""
    th, tv = 6.75 / lens, 12.0 / lens

    def sprite(nx, ny, size, col, thick=0.6, dist=100.0, ox=0.0, oz=0.0):
        d = fwd + nx * th * right + ny * tv * up
        d = d / np.linalg.norm(d)
        p = loc + d * dist + right * ox + up * oz
        G.c(p, (thick, size, size), col, (0.0, 0.0, math.atan2(d[1], d[0])))
    kind, nx, ny = sky_body(s)
    if kind == "sun":
        k = ramp(math.sin(math.pi * (s / 0.5)), 0.0, 0.3)
        sprite(nx, ny, 11.0, np.array((1.0, 0.50, 0.20)) * (1 - k) * 5.0 + np.array((1.0, 0.88, 0.40)) * k * 6.0)
    else:
        M = 10.0
        sprite(nx, ny, M, (2.6, 2.8, 3.2))
        for dx, dz, r in ((-0.22, 0.20, 0.20), (0.20, -0.18, 0.16), (0.12, 0.25, 0.10)):
            sprite(nx, ny, r * M, (1.4, 1.6, 2.1), thick=0.3, dist=99.0, ox=dx * M, oz=dz * M)


def build(ctx):
    from engine import bkit as K
    from engine import voxel as X
    from engine.home import mat_glow_inst
    v = X.Vox(24)
    for name, fn in (("home", _home), ("office", _office), ("street", _street)):
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, rot=SUN_ROT, name="ep24_sun")
    fill = K.point_light(ctx, (0, 0, 0), energy=0.0, color=(0.92, 0.94, 1.0), radius=0.8, name="ep24_fill")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    protos = X.people_protos(ctx, X.people_mats())
    C = cast()
    cr = crowd()
    NCR = len(cr["lane"])
    people = K.instancer_multi(ctx, "ep24_people", protos, len(C) + NCR)
    # 효과 상자: 발광(창밖 유리·해·달·바늘·글자) / 조명 받는 것(커튼·달력·지구본·컵)
    glow = K.instancer(ctx, "ep24_glow", K.proto(ctx, "ep24_p_glow", K.bm_cube(1, 1, 1, (0.5, 0, 0)),
                                                 [mat_glow_inst("ep24_m_glow", 1.0)]), GLOW_N, vector_scale=True)
    lit = K.instancer(ctx, "ep24_lit", K.proto(ctx, "ep24_p_lit", K.bm_cube(1, 1, 1, (0.5, 0, 0)),
                                               [K.mat_inst("ep24_m_lit", 0.7)]), LIT_N, vector_scale=True)

    def upd(t, f):
        i, u = prog(t)
        a0, _ = shot_span(i)
        el = t - a0
        st, _, az, elv, _, _, _, daz = LINES[i]["shot"]
        loc, fwd, right, up, lens, tgt, dn = shot_cam(i, u)
        cam.set(tgt, az + daz * u, elv, dn, lens)
        h = clock_h(i, u)
        s = phase(h)
        L = level(s)
        tw = twilight(s)
        # 하늘 밝기에 맞춰 햇빛·달빛·주변광
        sun.data.energy = 3.0 * L + 0.9 * tw * (1 - L) + 0.4 * (1 - L)
        sun.data.color = lerpc((0.55, 0.65, 1.0), lerpc((1.0, 0.94, 0.84), (1.0, 0.60, 0.36), tw), min(1.0, L * 2.0))
        ctx.set_ctl("ambient", 0.14 + 0.30 * L)
        ctx.set_rgb("ambient_col", lerpc((0.35, 0.42, 0.65), (0.62, 0.68, 0.82), L))
        if st == "home":
            lights["ep24_h_pend"].data.energy = 40.0 + 90.0 * (1 - L)
            lights["ep24_h_win"].data.energy = 15.0 + 70.0 * L
            lights["ep24_h_win"].data.color = lerpc((0.6, 0.7, 1.0), lerpc((0.85, 0.92, 1.0), (1.0, 0.6, 0.35), tw), L)
        if st == "street":
            for n in range(2):
                lights[f"ep24_s_l{n}"].data.energy = 260.0 * (1 - L)
            fill.location = tuple(float(q) for q in loc + np.array((0.0, 0.0, 0.25)))
            fill.data.energy = 300.0 * (1 - L)
        else:
            fill.data.energy = 0.0
        # 캐릭터
        P, R, CO, C2, SC, PO = [], [], [], [], [], []
        states = []
        for c in C:
            d = actor(c, i, el)
            show = c["only"] is None or i in c["only"]
            ox_, oy_ = OFF[d["set"]]
            P.append((d["x"] + ox_, d["y"] + oy_, d["z"]))
            R.append((0, 0, math.radians(d["yaw"])))
            CO.append(d["shirt"])
            C2.append(d["pants"])
            SC.append(d["scale"] if show else 0.0)
            PO.append(d["hair"] * X.NPOSE + X.POSES[d["pose"]])
            if show:
                states.append(d)
        sx, sy = OFF["street"]
        corridor = st == "street"
        fh = np.array(fwd[:2]) / max(np.linalg.norm(fwd[:2]), 1e-6)
        for k in range(NCR):
            x = (cr["x0"][k] + cr["d"][k] * cr["spd"][k] * t + 40) % 60 - 40
            stride = (cr["ph"][k] + cr["spd"][k] * t / 0.7) % 1.0
            lane = cr["lane"][k]
            z = 0.12 if abs(lane) > 3 else 0.0
            yaw = 0.0 if cr["d"][k] > 0 else 180.0
            hide = not corridor
            if corridor:                                                   # 카메라 앞 길목과 화면 가운데 ±9° 안(주인공 뒤)의 행인은 숨김
                rr = np.array((x + sx, lane + sy)) - loc[:2]
                along, lat = float(rr @ fh), abs(float(rr[0] * fh[1] - rr[1] * fh[0]))
                hide = (-0.5 < along < 60.0 and lat < max(1.0, 0.16 * along)) or (-0.5 < along < 1.5 and lat < 1.6)
            P.append((x + sx, lane + sy, z))
            R.append((0, 0, math.radians(yaw)))
            CO.append(cr["sh"][k])
            C2.append(cr["pa"][k])
            SC.append(0.0 if hide else 1.0)
            PO.append(int(cr["hair"][k]) * X.NPOSE + (X.WALK_A if stride < 0.5 else X.WALK_B))
        K.set_points(people, P, scale=SC, rot=R, col=np.array(CO, np.float32), colors={"col2": np.array(C2, np.float32)},
                     pose=PO)
        # 효과 상자
        G, Lt = Items(GLOW_N), Items(LIT_N)
        if st == "home":
            window_items(G, WIN["home"], s, "dino" if i == L_DINO else "city", t, u)
            clock_items(G, CLK["home"], h)
            home_props(Lt, G, i, u, el, t, s, h)
            if i == L_BED:
                zzz(G, states[0], t)
        elif st == "office":
            for k in ("oc", "ol", "or"):
                window_items(G, WIN[k], s, "city", t)
            clock_items(G, CLK["office"], h)
            office_props(Lt, G, i, u, el, t, s, h)
            if i in (L_BODY, L_JET):
                zzz(G, states[0], t)
        else:
            street_sky(G, s, loc, fwd, right, up, lens)
        for ob, items in ((glow, G), (lit, Lt)):
            Pp, Sc, Sz, Rt, Co = items.arrays()
            K.set_points(ob, Pp, scale=Sc, size=Sz, rot=Rt, col=Co)

    ctx.on_frame(upd)
