"""EP31 만약에 사람이 10센티로 줄어든다면? (19편식: 블록 캐릭터·생활 장면·내레이션)

핵심은 스케일: 사람은 scale 0.045~0.060(키 약 8.5~11cm)으로 작게, 가구·소품은 실제 크기(밥알 9mm·빗방울 5.5mm·성냥갑 14.5cm)로 만들고
카메라를 0.2~0.9m까지 바짝 붙여 거대하게 보이게 한다. 줄마다 방위각·거리가 계속 움직인다 (TWIST는 스토리보드대로 4번 줄).
장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
식탁 위 거대한 밥공기·숟가락 옆에서 올려다보는 작은 아이(훅) → 아침 침대, 베개가 산처럼 → 침대 가장자리 낭떠러지(아래로 보임)
→ 뛰어내려 사뿐 착지 → 툭툭 털며 일어남(작을수록 낙하에 강함, TWIST) → 체중계 65kg이 13g으로(블록 숫자)
→ 두 손으로 든 밥알이 주먹만 함 → 냉장고 문은 절벽·손잡이는 하늘 → 창밖(바깥에서 안을 봄)에서 비가 쏟아짐 → 빗방울 하나가 창에 퍼짐
→ 거대한 고양이가 다가옴 → 고양이 눈 클로즈업(눈이 내 얼굴보다 큼) → 흩어진 가족이 불러도 목소리가 안 닿음 → 손을 잡고 모임
→ 성냥갑 집(저녁) → 밤, 추워서 덜덜 → 고양이가 곁에서 몸을 말아 감쌈 → 고양이 털 속에서 잠든 가족 → 질문.
근거(설명란, 모두 계산값/근사): ① 몸집이 작을수록 낙하에 강하다 — J.B.S. Haldane, "On Being the Right Size"(1926).
② 키 170cm → 10cm는 1/17배, 몸무게는 부피에 비례해 1/17³≈1/4,900배: 65kg → 약 13g.
③ 큰 빗방울 지름 약 4mm × 17 ≈ 7cm ≈ 테니스공(약 6.7cm) 크기.
④ 고양이 눈 가로 약 2cm > 10cm 사람의 얼굴 너비(약 1cm).
⑤ 밥알 길이 약 6~9mm × 17 ≈ 10~15cm, 주먹 크기(내레이션에 숫자는 쓰지 않음).
특수효과: 사람은 블록 캐릭터 인스턴스의 scale만 줄이고(팔·고개·입·눈만 바꾼 새 자세 18종) 세트 소품은 실제 크기 상자.
고양이는 이 파일 안에서 상자로 만든 원형 12종(서기·걷기 2·웅크림·엎드림 눈 뜸/감음·몸 말기 6단계: 몸통을 호로 구부린 상자 사슬).
점프·낙하는 공기저항(종단속도) 곡선, 빗방울·밥알은 구·타원체 인스턴스, 창에 부딪혀 퍼지는 물은 도트 모양 상자 파편,
체중계 숫자·물음표·Z·느낌표·하트는 점 글자·그림(발광 상자). 가족이 손을 잡는 자세는 어깨 각도를 계산해 손끝이 맞닿게 함.
"""
import json
import math
from pathlib import Path

import numpy as np

from engine.common import ramp, clamp, lerp

STYLE = "pixe"
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.3, 0.32, 1.6)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게; 좌표가 커지면 작은 사람의 얼굴 디테일이 흔들려 ±300m 안에 둠)
OFF = {"bed": (0, 0), "dine": (300, 0), "sill": (-300, 0), "night": (0, 300)}

TZ = 0.7408        # 식탁 나무결 윗면 높이
BED_Z = 0.5005     # 침대 시트 높이
RUG_Z = 0.012      # 러그 높이
SC_Z = 0.0408      # 체중계 윗면
SILL_Z = 0.9508    # 창턱 윗면
MB = (0.0, 0.30)   # 성냥갑 트레이 가운데 (거실 러그 위)
MB_Z = RUG_Z + 0.0041   # 트레이 바닥 윗면
FR_Y = 1.78        # 냉장고 문 앞면
S_KID, S_DAD, S_MOM = 0.045, 0.060, 0.057   # 키 약 8.5 · 11.3 · 10.7cm

NAMES = ("hook", "wake", "cliff", "jump", "land", "kg", "rice", "fridge", "rain", "drop", "cat", "eye", "call", "gather",
         "box", "cold", "curl", "sleep", "ask")
LN = {n: k for k, n in enumerate(NAMES)}
# say: 내레이션 = 자막 / shot: (세트, 목표점(또는 함수), 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 사람이 10센티로 줄어든다면 어떻게 될까요?", gap=0.7, shot=("dine", (0.11, 0.58, 0.86), -96, -5, 0.52, 24, 0.9, 3)),
    dict(say="아침에 눈을 뜨니 10센티가 됐어요", gap=0.5, shot=("bed", (0.0, 1.88, 0.54), -40, 20, 0.46, 26, 0.9, 5)),
    dict(say="침대 가장자리는 낭떠러지 같았죠", gap=0.45, shot=("bed", (0.40, 1.15, 0.38), 20, 36, 0.8, 26, 0.9, -6)),
    dict(say="그런데 뛰어내려도 멀쩡해요", gap=0.5, shot=("bed", (0.7, 1.15, 0.3), -75, 8, 0.7, 26, 0.95, 8)),
    dict(say="몸이 작을수록 낙하에 강하거든요", gap=0.7, shot=("bed", (1.0, 1.15, 0.11), 10, 6, 0.42, 26, 0.9, 6)),
    dict(say="몸무게도 65킬로에서 13그램으로", gap=0.8, shot=("bed", (1.30, 0.62, 0.075), -90, 28, 0.46, 26, 0.9, 4)),
    dict(say="밥알 하나가 내 주먹만 해요", gap=0.6, shot=("dine", (0.0, 0.04, 0.808), -86, 8, 0.2, 26, 0.92, 3)),
    dict(say="냉장고는 절벽, 손잡이는 하늘", gap=0.5, shot=("dine", (2.5, 1.546, 0.385), -90, -20, 0.9, 24, 0.92, 0)),
    dict(say="그때 창밖에서 비가 쏟아졌어요", gap=0.45, shot=("sill", (0.0, 2.36, 1.0), 90, 6, 0.38, 26, 0.9, 6)),
    dict(say="빗방울 하나가 테니스공만 해요", gap=0.7, shot=("sill", (0.0, 2.40, 1.0), 85, 4, 0.34, 26, 0.95, -5)),
    dict(say="그리고 거대한 고양이가 다가왔어요", gap=0.5, shot=("dine", (0.97, -0.55, 0.14), -100, 4, 0.7, 24, 0.9, 6)),
    dict(say="고양이 눈이 내 얼굴보다 커요", gap=0.8, shot=("dine", (1.03, -0.805, 0.07), -100, 3, 0.5, 28, 0.5, 5)),
    dict(say="서로 불러도 목소리가 너무 작았죠", gap=0.5, shot=("night", (0.0, 0.35, 0.06), -90, 12, 0.95, 24, 0.96, 0)),
    dict(say="그래도 끝내 손을 잡고 모였어요", gap=0.5, shot=("night", (0.0, -0.12, 0.07), -90, 10, 0.7, 26, 0.9, -2)),
    dict(say="오늘 밤 집은 성냥갑 하나면 충분해요", gap=0.5, shot=("night", (0.0, 0.31, 0.075), -90, 30, 0.5, 26, 0.9, 6)),
    dict(say="밤이 되자 추워서 덜덜 떨렸는데", gap=0.5, shot=("night", (0.0, 0.31, 0.075), -80, 24, 0.46, 26, 0.9, 5)),
    dict(say="고양이가 슬며시 곁에 몸을 말았어요", gap=0.6, shot=("night", (0.0, 0.3, 0.06), -60, 35, 0.75, 24, 0.9, 12)),
    dict(say="무서운 고양이가 따뜻한 이불이 됐죠", gap=0.9, shot=("night", (0.0, 0.3, 0.06), -100, 42, 0.62, 26, 0.85, -8)),
    dict(say="10센티면 제일 먼저 뭘 할래요?", gap=0.5, shot=("night", (0.02, 0.3, 0.08), -90, 14, 0.5, 26, 1.3, 0)),
]
assert len(LINES) == len(NAMES)
TITLE = [("만약에", "white"), ("사람이 10센티로", "white"), ("줄어든다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = LN["land"]          # '몸이 작을수록 낙하에 강하거든요' 줄 (사실 한 줄)

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep31_tiny10cm" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.8 * i, 2.8 * i + 2.8, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep31", "title": "만약에 사람이 10cm로 줄어든다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "D", "mode": "lydian", "bpm": 100, "seed": 311, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

KID_SH, KID_PA = (0.95, 0.80, 0.35), (0.20, 0.20, 0.22)      # 아이: 노랑 · 짧은 머리
DAD_SH, DAD_PA = (0.25, 0.45, 0.80), (0.15, 0.18, 0.30)      # 아빠: 파랑 · 짧은 머리
MOM_SH, MOM_PA = (0.92, 0.55, 0.60), (0.35, 0.28, 0.20)      # 엄마: 분홍 · 긴 머리


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


def captions():
    """[(시작, 끝, 글)] — 첫 줄은 가운데 제목으로 보여 주므로 아래 자막에서 뺌."""
    return [(s, e, txt) for k, (s, e, txt) in enumerate(TIMELINE["lines"]) if k > 0]


def title_span():
    s, e, _ = TIMELINE["lines"][0]
    return s, e


def simulate(build_dir):
    return {"dur": np.float32(DUR)}


BED_LINES = (LN["wake"], LN["cliff"], LN["jump"], LN["land"], LN["kg"])
DINE_DAY = (LN["hook"], LN["rice"], LN["fridge"])
DINE_RAIN = (LN["cat"], LN["eye"])
SILL = (LN["rain"], LN["drop"])
EVENING = (LN["call"], LN["gather"], LN["box"])


def sky(t):
    i = line_at(t)
    if i >= LN["cold"]:
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0
    if i in EVENING:
        return (0.20, 0.17, 0.42), (0.98, 0.58, 0.38), 0.0
    if i in SILL or i in DINE_RAIN:
        return (0.20, 0.24, 0.32), (0.42, 0.48, 0.56), 0.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


def env(i, tl, du):
    """줄별 햇빛·주변광 + 움직이는 조명 {이름: 세기}."""
    day = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if i in DINE_DAY:
        return dict(day, lt={"ep31_d_pend": 55.0, "ep31_d_win": 130.0, "ep31_d_fill": 45.0, "ep31_d_fridge": 60.0,
                             "ep31_d_floor": 0.0})
    if i in BED_LINES:
        return dict(day, lt={"ep31_b_win": 150.0, "ep31_b_fill": 70.0, "ep31_b_low": 40.0})
    if i in SILL:                                          # 비 오는 낮: 바깥은 회청색, 방 안은 따뜻한 스탠드
        return dict(day, sun=0.0, amb=0.34, amb_col=(0.52, 0.60, 0.78),
                    lt={"ep31_s_ext": 120.0, "ep31_s_lamp": 50.0, "ep31_s_room": 45.0})
    if i in DINE_RAIN:                                     # 비 오는 오후 부엌: 펜던트 + 바닥 보조광
        return dict(day, sun=0.0, amb=0.28, amb_col=(0.55, 0.62, 0.80),
                    lt={"ep31_d_pend": 95.0, "ep31_d_win": 28.0, "ep31_d_fill": 35.0, "ep31_d_fridge": 20.0,
                        "ep31_d_floor": 75.0})
    night = dict(day, sun=0.0, amb=0.14, amb_col=(0.50, 0.42, 0.55))
    if i in EVENING:                                       # 저녁: 따뜻한 스탠드
        return dict(night, lt={"ep31_n_lamp": 150.0, "ep31_n_top": 85.0, "ep31_n_moon": 14.0, "ep31_n_fill": 40.0,
                               "ep31_n_cool": 0.0})
    if i == LN["cold"]:                                    # 불이 꺼지고 달빛 + 차가운 보조광만 (얼굴은 읽히게)
        k = ramp(tl, 0.15, 0.75)
        return dict(night, amb=0.14 - 0.04 * k, amb_col=(0.50 - 0.20 * k, 0.42 - 0.04 * k, 0.55 + 0.07 * k),
                    lt={"ep31_n_lamp": 150.0 * (1 - k), "ep31_n_top": 85.0 * (1 - k), "ep31_n_moon": 14.0 + 31.0 * k,
                        "ep31_n_fill": 40.0 * (1 - k), "ep31_n_cool": 34.0 * k})
    if i == LN["curl"]:                                    # 고양이가 눕는 만큼 다시 따뜻해짐
        k = ramp(tl, 0.6, min(du, 2.6))
        return dict(night, amb=0.10 + 0.02 * k, amb_col=(0.30 + 0.12 * k, 0.38, 0.62 - 0.07 * k),
                    lt={"ep31_n_lamp": 100.0 * k, "ep31_n_top": 0.0, "ep31_n_moon": 38.0, "ep31_n_fill": 10.0 + 30.0 * k,
                        "ep31_n_cool": 34.0 - 22.0 * k})
    return dict(night, amb=0.12, amb_col=(0.42, 0.38, 0.55),
                lt={"ep31_n_lamp": 125.0, "ep31_n_top": 0.0, "ep31_n_moon": 26.0, "ep31_n_fill": 40.0, "ep31_n_cool": 12.0})


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def cam_pose(i, tl, du, u):
    """줄 진행도 u에서 카메라. CamRig.set과 같은 규칙: 위치 = 목표 + 거리 × (cos el·cos az, cos el·sin az, sin el)."""
    ln = LINES[i]
    st, tg, az, el, dist, lens, push, daz = ln["shot"]
    if callable(tg):
        tg = tg(tl, du, u)
    o = OFF[st]
    tgt = (tg[0] + o[0], tg[1] + o[1], tg[2])
    a, e, d = az + daz * u, math.radians(el), dist * (1 + (push - 1) * u)
    loc = (tgt[0] + math.cos(e) * math.cos(math.radians(a)) * d, tgt[1] + math.cos(e) * math.sin(math.radians(a)) * d,
           tgt[2] + math.sin(e) * d)
    return dict(tgt=tgt, az=a, el=el, dist=d, lens=lens, loc=loc, roll=ln.get("roll", 0.0), shift=ln.get("shift", 0.0))


def cam_axes(az, el):
    """카메라의 오른쪽·위쪽 단위벡터."""
    a, e = math.radians(az), math.radians(el)
    return (-math.sin(a), math.cos(a), 0.0), (-math.cos(a) * math.sin(e), -math.sin(a) * math.sin(e), math.cos(e))


# ───────────────────────── 5x7 점 글자 · 그림 ─────────────────────────
FONT = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    "k": ["10000", "10000", "10010", "10100", "11000", "10100", "10010"],
    "g": ["00000", "01111", "10001", "10001", "01111", "00001", "01110"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
}
HEART = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]


def text_cells(txt):
    """5x7 글자 한 줄 → ([(열, 아래에서 몇째 줄)], 전체 폭(칸)). 글자 사이 한 칸."""
    cells, x = [], 0
    for ch in txt:
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    cells.append((x + c, 6 - r))
        x += 6
    return cells, x - 1


def pix_items(cells, width, ctr, cell, right, up, col, depth=None, rz=0.0):
    """점 칸들 → 발광 상자 목록. ctr = 글 가운데 아래(세트 좌표), right·up = 글이 놓인 면의 방향 단위벡터. depth가 없으면 정육면체."""
    out = []
    dz = cell if depth is None else depth
    for c, r in cells:
        k, h = (c - (width - 1) / 2.0) * cell, (r + 0.5) * cell
        p = (ctr[0] + right[0] * k + up[0] * h, ctr[1] + right[1] * k + up[1] * h, ctr[2] + right[2] * k + up[2] * h)
        out.append((p, (cell, dz, cell) if depth is not None else (cell, cell, cell), (0.0, 0.0, rz), col))
    return out


def heart_items(ctr, cell, right, up, rz=0.0, col=(1.0, 0.35, 0.5)):
    cells = [(c, len(HEART) - 1 - r) for r, row in enumerate(HEART) for c, ch in enumerate(row) if ch == "#"]
    return pix_items(cells, len(HEART[0]), ctr, cell, right, up, col, rz=rz)


def billboard(ctr, cam_loc):
    """글·그림을 카메라 쪽으로 돌려 세우는 (오른쪽, 위, 회전) — ctr은 세트 좌표, cam_loc은 같은 세트 좌표."""
    ang = math.atan2(cam_loc[1] - ctr[1], cam_loc[0] - ctr[0])
    return (-math.sin(ang), math.cos(ang), 0.0), (0.0, 0.0, 1.0), ang


# ───────────────────────── 캐릭터 자세 (표준 자세 위에 팔·고개·입만 바꾼 원형) ─────────────────────────
SITS = ("sit", "sit_phone", "sit_conf")
# base = 바탕 자세, arms = ((오른팔 앞뒤, 옆), (왼팔 앞뒤, 옆)) 어깨 회전각(음수 = 앞으로 듦, 옆 = 몸 밖으로 벌림),
# legs = 같은 형식, head = 고개 숙임(+)/젖힘(−), hroll = 고개 기울임, mouth, sleep = 눈 감음, lie = 눈 뜨고 누움
KINDS = {
    "lieopen": dict(base="stand", lie=True),
    "lookup": dict(base="stand", head=-0.55, mouth="open"),
    "peek": dict(base="stand", head=0.5, arms=((0.2, 0.0), (0.2, 0.0))),
    "star": dict(base="stand", arms=((0.0, -2.5), (0.0, 2.5)), legs=((0.0, -0.3), (0.0, 0.3)), mouth="open"),
    "holdgrain": dict(base="stand", head=0.3, arms=((-1.35, 0.27), (-1.35, -0.27)), mouth="open"),   # 두 손으로 밥알을 감싸 듦
    "dustR": dict(base="stand", arms=((-0.85, 0.0), (0.05, 0.0)), mouth="smile"),
    "dustL": dict(base="stand", arms=((0.05, 0.0), (-0.85, 0.0)), mouth="smile"),
    "cheer": dict(base="stand", arms=((-2.9, 0.0), (-2.9, 0.0)), mouth="open"),
    "waveR": dict(base="stand", arms=((-2.8, 0.0), (0.05, 0.0)), mouth="open"),
    "waveL": dict(base="stand", arms=((0.05, 0.0), (-2.8, 0.0)), mouth="open"),
    "holdL": dict(base="stand", arms=((0.0, 0.0), (0.0, 1.222)), mouth="smile"),
    "holdR": dict(base="stand", arms=((0.0, -1.222), (0.0, 0.0)), mouth="smile"),
    "holdK": dict(base="stand", arms=((0.0, -1.90), (0.0, 1.90)), mouth="smile"),
    "sit_smile": dict(base="sit", mouth="smile"),
    "sit_hug": dict(base="sit", arms=((-1.25, 0.8), (-1.0, -0.8)), mouth="frown"),
    "sleep_d": dict(base="sit", sleep=True, hroll=-0.30, head=0.12, mouth="smile"),
    "sleep_k": dict(base="sit", sleep=True, hroll=0.12, head=0.32, mouth="smile"),
    "sleep_m": dict(base="sit", sleep=True, hroll=0.30, head=0.12, mouth="smile"),
}
KIND_ORDER = list(KINDS)


def pose_index(name, hair):
    """인스턴스 'pose' 번호: 표준 22개(머리종류*11+자세) 뒤에 새 자세들(머리종류*새자세수+번호)."""
    from engine import voxel as X
    if name in KINDS:
        return 2 * X.NPOSE + hair * len(KINDS) + KIND_ORDER.index(name)
    return hair * X.NPOSE + X.POSES[name]


def _rot_x(bm, ang, pivot):
    """x축(앞) 둘레 회전. 왼쪽(+y) 팔은 양수 = 바깥."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        y, z = p.co.y - pivot[1], p.co.z - pivot[2]
        p.co.y, p.co.z = pivot[1] + c * y - s * z, pivot[2] + s * y + c * z
    return bm


def _rot_z(bm, ang, pivot):
    """pivot=(x, y)를 지나는 세로축 둘레 회전."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        x, y = p.co.x - pivot[0], p.co.y - pivot[1]
        p.co.x, p.co.y = pivot[0] + c * x - s * y, pivot[1] + s * x + c * y
    return bm


def _zmean(bm):
    return sum(v.co.z for v in bm.verts) / len(bm.verts)


def _variant(kind, lh):
    """voxel._person으로 만든 바탕 자세에서 팔·다리·고개·입·눈만 바꾼 [(bmesh, 재질)]."""
    from engine import bkit as K
    from engine import voxel as X
    sp = KINDS[kind]
    sit = sp["base"] in SITS
    P = X._person(X.POSES[sp["base"]], lh)
    hip = 0.47 if sit else 0.78
    hz = hip + 0.58
    nl = 6 if sit else 4
    legs, torso, head, arms = P[:nl], P[nl], list(P[nl + 1:-4]), P[-4:]

    def cube(cx, cy, z0, sx, sy, sz):
        return K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True)

    def swap(drop_fn, new):
        nonlocal head
        drop = {id(bm) for bm, mi in head if drop_fn(bm, mi)}      # 먼저 고르고 나서 free (free 뒤엔 bm을 읽을 수 없음)
        keep = []
        for bm, mi in head:
            if id(bm) in drop:
                bm.free()
            else:
                keep.append((bm, mi))
        head = keep + new
    mouth = {"open": [(cube(0.232, 0, hz + 0.04, 0.02, 0.13, 0.07), 6)],
             "smile": [(cube(0.232, 0, hz + 0.04, 0.02, 0.11, 0.028), 6), (cube(0.232, -0.075, hz + 0.055, 0.02, 0.03, 0.04), 6),
                       (cube(0.232, 0.075, hz + 0.055, 0.02, 0.03, 0.04), 6)],
             "frown": [(cube(0.232, 0, hz + 0.055, 0.02, 0.13, 0.03), 6), (cube(0.232, -0.08, hz + 0.03, 0.02, 0.03, 0.045), 6),
                       (cube(0.232, 0.08, hz + 0.03, 0.02, 0.03, 0.045), 6)]}
    if sp.get("mouth"):
        swap(lambda bm, mi: mi == 6, mouth[sp["mouth"]])
    if sp.get("sleep"):                                            # 눈 감음: 흰자·눈동자를 빼고 가는 선
        swap(lambda bm, mi: mi == 4 or (mi == 5 and _zmean(bm) > hz), [(cube(0.232, sy, hz + 0.17, 0.02, 0.11, 0.025), 5)
                                                                        for sy in (-0.1, 0.1)])

    def arm(sy, pitch, roll):
        sleeve, hand = cube(0, sy, hip + 0.12, 0.18, 0.16, 0.46), cube(0, sy, hip - 0.02, 0.17, 0.15, 0.14)
        for bm in (sleeve, hand):
            if roll:
                _rot_x(bm, roll, (0, sy, hip + 0.54))
            if pitch:
                X._rot_y(bm, pitch, (0, 0, hip + 0.54))
        return [(sleeve, 0), (hand, 2)]
    if sp.get("arms"):
        for bm, _ in arms:
            bm.free()
        (pr, rr), (pl, rl) = sp["arms"]
        arms = arm(-0.34, pr, rr) + arm(0.34, pl, rl)
    if sp.get("legs"):
        for k, (pitch, roll) in enumerate(sp["legs"]):
            for bm, _ in legs[2 * k:2 * k + 2]:
                if roll:
                    _rot_x(bm, roll, (0, -0.11 if k == 0 else 0.11, hip))
                if pitch:
                    X._rot_y(bm, pitch, (0, 0, hip))
    for bm, _ in head:                                             # 고개: 목(어깨 위)을 축으로 숙이거나 젖히고 기울임
        if sp.get("hroll"):
            _rot_x(bm, sp["hroll"], (0, 0, hz))
        if sp.get("head"):
            X._rot_y(bm, sp["head"], (0, 0, hz))
    out = list(legs) + [torso] + head + list(arms)
    if sp.get("lie"):                                              # 선 모습을 뒤로 눕힘: 발끝이 원점, 머리는 -x, 얼굴은 위 (눈은 뜬 채)
        for bm, _ in out:
            X._rot_y(bm, -math.pi / 2, (0, 0, 0))
            X._shift(bm, dz=0.24)
    return out


# ───────────────────────── 세트 (실제 크기 가구: 카메라가 0.2~0.9m까지 붙어 거대하게 보임) ─────────────────────────
def _walls(v, x0, x1, y0, y1, h, back, side, front=None, tile=0.25):
    """네 벽이 막힌 방 (카메라가 어느 쪽을 봐도 빈 곳이 없게)."""
    v.wall((x0, y1), (x1, y1), 0, h, back, tile, face=-1)
    v.wall((x0, y0), (x0, y1), 0, h, side, tile, face=-1)
    v.wall((x1, y0), (x1, y1), 0, h, side, tile, face=1)
    v.wall((x0, y0), (x1, y0), 0, h, front or back, tile, face=1)


def _books(v, x0, x1, yf, z0, z1, rows=4, dim=1.0):
    """책장 칸마다 알록달록한 책등 (yf = 책등 앞면 y, -y쪽을 봄)."""
    cols = [(0.9, 0.3, 0.3), (0.3, 0.6, 0.9), (0.95, 0.8, 0.25), (0.35, 0.75, 0.45), (0.8, 0.5, 0.85), (0.95, 0.55, 0.2),
            (0.95, 0.95, 0.92)]
    hh = (z1 - z0) / rows
    for r in range(rows):
        zb = z0 + r * hh + 0.03
        x = x0 + 0.02
        while x < x1 - 0.1:
            w, h = float(v.rs.uniform(0.03, 0.06)), float(v.rs.uniform(0.6, 0.9)) * (hh - 0.05)
            v.box(x, x + w, yf, yf + 0.22, zb, zb + h, tuple(c * dim for c in cols[int(v.rs.integers(len(cols)))]), jit=0.06)
            x += w + 0.004


def _bed(v):
    """침실(아침): 침대 머리판은 뒷벽, 오른쪽에 러그·체중계·슬리퍼. 시트 높이 0.50m, 가장자리 x=0.55."""
    from engine import voxel as X
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.2, "wood")
    _walls(v, -3, 3, -2.5, 2.5, 2.7, (0.93, 0.90, 0.82), (0.86, 0.88, 0.80))
    v.window(1.3, 2.5, 2.49, 1.05, 2.25, night=False)
    for x0, x1 in ((1.0, 1.2), (2.6, 2.8)):                                       # 커튼
        v.box(x0, x1, 2.36, 2.44, 0.85, 2.4, (0.85, 0.45, 0.42))
    # 침대: 틀 · 매트리스 · 체크 시트 · 머리판 · 베개(13cm) · 왼쪽에 말린 이불 · 발치 이불 더미
    v.box(-0.52, 0.52, 0.24, 2.43, 0.0, 0.30, X.WOOD)
    v.box(-0.55, 0.55, 0.20, 2.45, 0.30, 0.50, (0.92, 0.92, 0.95), jit=0.02)
    v.floor(-0.55, 0.55, 0.20, 2.45, (0.80, 0.88, 0.97), 0.11, "check", z=BED_Z)
    v.box(-0.58, 0.58, 2.43, 2.49, 0.0, 1.05, X.DARKWOOD)
    v.box(-0.32, 0.32, 1.98, 2.40, BED_Z, 0.62, (0.97, 0.97, 0.98), jit=0.01)
    v.box(-0.28, 0.28, 2.02, 2.36, 0.62, 0.635, (0.95, 0.95, 0.97), jit=0.01)
    v.box(-0.54, -0.14, 0.95, 1.90, BED_Z, 0.60, (0.35, 0.50, 0.82))
    v.box(-0.50, -0.18, 1.00, 1.85, 0.60, 0.625, (0.42, 0.57, 0.88))
    v.box(-0.54, 0.54, 0.22, 0.70, BED_Z, 0.58, (0.35, 0.50, 0.82))
    # 협탁 + 알람시계(빨간 화면)
    v.box(0.64, 1.08, 1.98, 2.43, 0.0, 0.50, X.WOOD)
    v.box(0.62, 1.10, 1.96, 2.45, 0.50, 0.53, (0.55, 0.38, 0.22))
    v.box(0.74, 0.96, 2.18, 2.32, 0.53, 0.64, (0.20, 0.20, 0.23))
    v.box(0.765, 0.935, 2.1735, 2.1795, 0.555, 0.615, (1.0, 0.35, 0.25), jit=0, glow=True)
    # 러그 · 슬리퍼 · 체중계(앞에 숫자 화면) · 곰인형과 블록
    v.floor(0.62, 2.1, 0.15, 1.9, (0.80, 0.50, 0.42), 0.12, "check", z=RUG_Z)
    v.box(0.78, 0.89, 0.24, 0.49, RUG_Z, 0.075, (0.90, 0.55, 0.62))
    v.box(0.95, 1.06, 0.17, 0.42, RUG_Z, 0.075, (0.90, 0.55, 0.62))
    v.box(1.15, 1.45, 0.55, 0.85, RUG_Z, SC_Z, (0.90, 0.90, 0.93))
    v.floor(1.16, 1.44, 0.56, 0.84, (0.86, 0.88, 0.92), 0.04, "check", z=SC_Z + 0.0008)
    v.box(1.20, 1.40, 0.50, 0.56, RUG_Z, 0.085, (0.22, 0.24, 0.28))
    v.box(1.215, 1.385, 0.4975, 0.4995, 0.05, 0.082, (0.02, 0.04, 0.03), jit=0)
    br = (0.62, 0.42, 0.26)
    v.box(1.70, 1.82, 1.44, 1.56, RUG_Z, 0.08, br)
    v.box(1.71, 1.81, 1.455, 1.545, 0.08, 0.15, br)
    for sy in (1.46, 1.54):
        v.box(1.72, 1.78, sy - 0.015, sy + 0.015, 0.15, 0.175, br)
    v.box(1.92, 2.02, 0.95, 1.05, RUG_Z, 0.07, (0.9, 0.3, 0.3))
    v.box(1.98, 2.08, 1.01, 1.11, RUG_Z, 0.064, (0.3, 0.6, 0.9))
    v.box(1.95, 2.05, 0.98, 1.08, 0.07, 0.12, (0.95, 0.8, 0.25))
    # 왼쪽 벽 책장
    v.box(-2.95, -2.55, -1.2, 1.0, 0, 1.9, X.WOOD)
    _books(v, -1.2, 1.0, -2.55, 0.1, 1.85)
    v.light(1.9, 2.3, 1.7, 150, (0.85, 0.92, 1.0), 0.8, "ep31_b_win")
    v.light(0.3, -1.0, 1.9, 70, (1.0, 0.95, 0.88), 0.7, "ep31_b_fill")
    v.light(0.9, 0.9, 1.1, 40, (1.0, 0.92, 0.8), 0.5, "ep31_b_low")


def _bowl(v, cx, cy, z0, col, rim):
    """밥공기: 굽 · 몸통 · 파란 띠 · 테두리 · 밥(세 층). 폭 12cm, 밥 윗면까지 약 10cm."""
    rice = (0.97, 0.96, 0.92)
    v.box(cx - 0.025, cx + 0.025, cy - 0.025, cy + 0.025, z0, z0 + 0.012, col)
    v.box(cx - 0.043, cx + 0.043, cy - 0.043, cy + 0.043, z0 + 0.012, z0 + 0.034, col)
    v.box(cx - 0.058, cx + 0.058, cy - 0.058, cy + 0.058, z0 + 0.034, z0 + 0.070, col)
    v.box(cx - 0.0585, cx + 0.0585, cy - 0.0585, cy + 0.0585, z0 + 0.040, z0 + 0.048, rim, jit=0.02)
    v.box(cx - 0.061, cx + 0.061, cy - 0.061, cy + 0.061, z0 + 0.066, z0 + 0.072, col)
    v.box(cx - 0.052, cx + 0.052, cy - 0.052, cy + 0.052, z0 + 0.070, z0 + 0.083, rice, jit=0.02)
    v.box(cx - 0.040, cx + 0.040, cy - 0.040, cy + 0.040, z0 + 0.083, z0 + 0.094, rice, jit=0.02)
    v.box(cx - 0.026, cx + 0.026, cy - 0.026, cy + 0.026, z0 + 0.094, z0 + 0.102, rice, jit=0.02)


BOWL = (0.0, 0.32)


def _dine(v):
    """부엌 겸 식당: 식탁(나무결 8.5cm 칸)에 밥공기·젓가락·반찬, 왼쪽 주방, 오른쪽 뒤 냉장고(손잡이 높이 1.2m)."""
    from engine import voxel as X
    v.floor(-3, 3, -2.5, 2.5, (0.80, 0.78, 0.72), 0.30, "check")
    _walls(v, -3, 3, -2.5, 2.5, 2.7, (0.93, 0.90, 0.82), (0.86, 0.88, 0.80))
    v.box(-2.95, -0.45, 1.95, 2.46, 0, 0.88, (0.95, 0.95, 0.93))                      # 주방 카운터 + 창
    v.box(-2.97, -0.43, 1.92, 2.46, 0.88, 0.92, (0.55, 0.57, 0.60))
    v.window(-2.4, -1.0, 2.49, 1.25, 2.3, night=False)
    # 냉장고
    v.box(1.95, 2.8, FR_Y, 2.46, 0, 1.85, (0.83, 0.85, 0.88))
    v.box(1.95, 2.8, FR_Y - 0.0045, FR_Y - 0.0005, 1.29, 1.31, (0.25, 0.27, 0.30), jit=0)
    hc = (0.30, 0.32, 0.36)
    for z0, z1 in ((1.40, 1.72), (0.82, 1.22)):
        v.box(2.65, 2.69, FR_Y - 0.043, FR_Y - 0.02, z0, z1, hc)
        for zz in (z0, z1 - 0.03):
            v.box(2.65, 2.69, FR_Y - 0.0205, FR_Y - 0.0005, zz, zz + 0.03, hc)
    for x0, x1, z0, z1, c in ((2.05, 2.17, 0.95, 1.07, (0.95, 0.3, 0.3)), (2.25, 2.37, 0.55, 0.67, (0.3, 0.6, 0.9)),
                              (2.10, 2.22, 0.30, 0.42, (0.95, 0.8, 0.25)), (2.30, 2.50, 0.88, 1.12, (0.97, 0.97, 0.94)),
                              (2.05, 2.25, 1.50, 1.60, (0.4, 0.75, 0.45))):
        v.box(x0, x1, FR_Y - 0.0045, FR_Y - 0.0005, z0, z1, c, jit=0.02)
    v.box(2.34, 2.46, FR_Y - 0.0065, FR_Y - 0.0045, 0.92, 1.06, (0.55, 0.78, 0.95), jit=0)
    # 식탁 + 의자 + 펜던트
    X.table(v, -0.2, 0.2, 1.7, 0.95, 0.74, (0.85, 0.72, 0.52))
    v.floor(-1.05, 0.65, -0.275, 0.675, (0.83, 0.67, 0.47), 0.085, "wood", z=TZ)
    for cx, cy, fd in ((-0.6, -0.80, 90), (0.15, -0.80, 90), (-1.45, 0.2, 0)):
        X.chair(v, cx, cy, fd)
    v.box(-0.22, -0.18, 0.18, 0.22, 1.9, 2.7, (0.2, 0.2, 0.2), jit=0)
    v.box(-0.42, 0.02, -0.02, 0.42, 1.78, 1.90, (1.0, 0.85, 0.6), jit=0, glow=True)
    # 식탁 위: 밥공기 · 젓가락 · 반찬 접시 · 머그컵
    _bowl(v, BOWL[0], BOWL[1], TZ, (0.96, 0.96, 0.94), (0.30, 0.45, 0.75))
    for cx in (0.335, 0.349):
        v.box(cx, cx + 0.0035, 0.04, 0.27, TZ, TZ + 0.0035, (0.45, 0.30, 0.18), jit=0.03)
    v.box(0.335, 0.425, 0.47, 0.56, TZ, TZ + 0.012, (0.96, 0.96, 0.94))
    v.box(0.348, 0.412, 0.485, 0.545, TZ + 0.012, TZ + 0.024, (0.85, 0.18, 0.12), jit=0.08)
    v.box(-0.42, -0.35, 0.24, 0.31, TZ, TZ + 0.09, (0.35, 0.55, 0.85))
    # 바닥 소품: 러그 · 고양이 밥그릇 · 장난감
    v.floor(0.3, 1.8, -1.6, -0.2, (0.78, 0.55, 0.50), 0.12, "check", z=0.012)
    v.box(1.52, 1.64, -1.50, -1.38, 0.012, 0.05, (0.85, 0.25, 0.22))
    v.box(1.54, 1.62, -1.48, -1.40, 0.05, 0.056, (0.55, 0.38, 0.22), jit=0.05)
    v.box(0.55, 0.65, -1.45, -1.35, 0.012, 0.10, (0.3, 0.6, 0.9))
    v.light(-0.2, 0.2, 1.9, 55, (1.0, 0.9, 0.75), 0.3, "ep31_d_pend")
    v.light(-1.7, 2.2, 1.8, 130, (0.85, 0.92, 1.0), 0.8, "ep31_d_win")
    v.light(0.3, -1.8, 1.6, 45, (1.0, 0.95, 0.88), 0.7, "ep31_d_fill")
    v.light(2.3, 0.9, 1.4, 60, (1.0, 0.95, 0.88), 0.6, "ep31_d_fridge")
    v.light(1.2, -1.4, 0.8, 0, (1.0, 0.88, 0.7), 0.6, "ep31_d_floor")


def _sill(v):
    """창가(바깥에서 안쪽을 봄): 창턱 높이 0.95m, 방 안쪽에 스탠드·화분·책장. 유리 자리(y=2.53) 앞이 비 오는 바깥."""
    v.floor(-2.5, 2.5, -0.9, 2.5, (0.62, 0.45, 0.30), 0.2, "wood")
    v.wall((-2.5, -0.9), (-2.5, 2.5), 0, 2.7, (0.90, 0.84, 0.74), 0.25, face=-1)
    v.wall((2.5, -0.9), (2.5, 2.5), 0, 2.7, (0.90, 0.84, 0.74), 0.25, face=1)
    v.wall((-2.5, -0.9), (2.5, -0.9), 0, 2.7, (0.92, 0.86, 0.76), 0.25, face=1)
    wb = (0.93, 0.90, 0.82)
    v.wall((-2.5, 2.5), (-0.85, 2.5), 0, 2.7, wb, 0.25, face=-1)
    v.wall((0.85, 2.5), (2.5, 2.5), 0, 2.7, wb, 0.25, face=-1)
    v.wall((-0.85, 2.5), (0.85, 2.5), 0, 0.90, wb, 0.25, face=-1)
    v.wall((-0.85, 2.5), (0.85, 2.5), 2.25, 2.7, wb, 0.25, face=-1)
    wh = (0.95, 0.95, 0.93)
    v.box(-0.95, 0.95, 2.30, 2.58, 0.90, 0.95, wh)                                     # 창턱 판
    v.floor(-0.95, 0.95, 2.30, 2.58, (0.90, 0.88, 0.82), 0.07, "wood", z=SILL_Z)
    v.box(-0.92, -0.85, 2.42, 2.53, 0.95, 2.28, wh)                                    # 창틀
    v.box(0.85, 0.92, 2.42, 2.53, 0.95, 2.28, wh)
    v.box(-0.925, 0.925, 2.415, 2.535, 2.25, 2.31, wh)
    # 창턱 위: 스탠드(왼쪽)와 화분(오른쪽)
    v.box(-0.20, -0.10, 2.40, 2.50, SILL_Z, SILL_Z + 0.02, (0.2, 0.2, 0.22))
    v.box(-0.16, -0.14, 2.44, 2.46, SILL_Z + 0.02, SILL_Z + 0.30, (0.2, 0.2, 0.22), jit=0)
    v.box(-0.23, -0.07, 2.36, 2.52, SILL_Z + 0.30, SILL_Z + 0.40, (1.0, 0.82, 0.52), jit=0, glow=True)
    v.box(0.09, 0.21, 2.40, 2.52, SILL_Z, SILL_Z + 0.10, (0.78, 0.45, 0.30))
    for x, y, h in ((0.12, 2.44, 0.28), (0.16, 2.48, 0.22), (0.19, 2.44, 0.30), (0.14, 2.50, 0.18)):
        v.box(x - 0.012, x + 0.012, y - 0.012, y + 0.012, SILL_Z + 0.10, SILL_Z + 0.10 + h, (0.28, 0.58, 0.28), jit=0.08)
    # 방 안쪽: 책장 + 러그
    v.box(-0.8, 0.8, -0.88, -0.55, 0, 2.0, (0.62, 0.42, 0.25))
    _books(v, -0.8, 0.8, -0.56, 0.1, 1.95, dim=0.55)
    v.floor(-1.5, 1.5, 0.0, 2.0, (0.80, 0.50, 0.42), 0.12, "check", z=0.012)
    v.light(0.0, 3.4, 1.5, 120, (0.75, 0.85, 1.0), 0.8, "ep31_s_ext")
    v.light(-0.15, 2.4, SILL_Z + 0.33, 50, (1.0, 0.8, 0.5), 0.3, "ep31_s_lamp")
    v.light(0.0, 0.3, 2.2, 45, (1.0, 0.9, 0.75), 0.6, "ep31_s_room")


def _matchbox(v, cx, cy):
    """성냥갑 트레이(집) 14.5×10×3cm + 뒤에 누운 겉갑(빨간 상표) + 앞에 흩어진 성냥개비. 트레이 안쪽 바닥 = MB_Z."""
    z0 = RUG_Z
    c = (0.84, 0.72, 0.50)
    hx, hy, zt = 0.0725, 0.05, z0 + 0.030
    v.box(cx - hx, cx + hx, cy - hy, cy + hy, z0, z0 + 0.004, c, jit=0.02)
    v.box(cx - hx, cx + hx, cy - hy, cy - hy + 0.004, z0 + 0.004, zt, c, jit=0.02)
    v.box(cx - hx, cx + hx, cy + hy - 0.004, cy + hy, z0 + 0.004, zt, c, jit=0.02)
    v.box(cx - hx, cx - hx + 0.004, cy - hy + 0.004, cy + hy - 0.004, z0 + 0.004, zt, c, jit=0.02)
    v.box(cx + hx - 0.004, cx + hx, cy - hy + 0.004, cy + hy - 0.004, z0 + 0.004, zt, c, jit=0.02)
    v.box(cx - hx, cx + hx, cy + 0.058, cy + 0.092, z0, z0 + 0.034, (0.80, 0.22, 0.18))            # 겉갑
    v.box(cx - 0.05, cx + 0.05, cy + 0.0605, cy + 0.0895, z0 + 0.034, z0 + 0.0352, (0.97, 0.93, 0.82), jit=0)
    v.box(cx - 0.012, cx + 0.012, cy + 0.068, cy + 0.082, z0 + 0.0352, z0 + 0.0364, (0.95, 0.25, 0.15), jit=0)
    v.box(cx - 0.065, cx + 0.065, cy + 0.0565, cy + 0.0575, z0 + 0.008, z0 + 0.026, (0.28, 0.16, 0.12), jit=0)   # 마찰면
    for k in range(5):                                                                              # 성냥개비
        y = cy - 0.16 + 0.015 * k
        x = cx - 0.46 + 0.012 * (k % 2)
        v.box(x, x + 0.12, y, y + 0.0035, z0, z0 + 0.0035, (0.86, 0.72, 0.48), jit=0.03)
        v.box(x - 0.006, x, y - 0.0005, y + 0.0040, z0, z0 + 0.0045, (0.85, 0.15, 0.10), jit=0.03)


def _night(v):
    """거실(저녁~밤): 러그 위 성냥갑, 뒤쪽 소파, 왼쪽 스탠드·책장, 오른쪽 밤 창."""
    v.floor(-3, 3, -2.5, 2.5, (0.58, 0.42, 0.28), 0.2, "wood")
    _walls(v, -3, 3, -2.5, 2.5, 2.7, (0.82, 0.76, 0.66), (0.78, 0.72, 0.64))
    v.floor(-1.7, 1.5, -1.0, 1.4, (0.62, 0.38, 0.34), 0.12, "check", z=RUG_Z)
    sf, cu = (0.34, 0.42, 0.52), (0.40, 0.48, 0.58)
    v.box(-1.9, 1.9, 1.75, 2.42, 0, 0.40, sf)
    v.box(-1.85, -0.05, 1.77, 2.2, 0.40, 0.50, cu)
    v.box(0.05, 1.85, 1.77, 2.2, 0.40, 0.50, cu)
    v.box(-1.9, 1.9, 2.2, 2.42, 0.50, 0.95, sf)
    v.box(-1.96, -1.84, 1.75, 2.40, 0.40, 0.62, sf)
    v.box(1.84, 1.96, 1.75, 2.40, 0.40, 0.62, sf)
    v.box(-1.3, -0.8, 2.05, 2.2, 0.5, 0.85, (0.95, 0.75, 0.3))
    v.box(0.7, 1.2, 2.05, 2.2, 0.5, 0.85, (0.85, 0.40, 0.35))
    v.box(-2.35, -2.31, 1.58, 1.62, 0, 1.45, (0.2, 0.2, 0.2), jit=0)                   # 스탠드
    v.box(-2.50, -2.16, 1.43, 1.77, 1.45, 1.78, (1.0, 0.82, 0.52), jit=0, glow=True)
    v.box(-2.95, -2.55, -1.5, 0.8, 0, 1.9, (0.62, 0.42, 0.25))                         # 책장
    _books(v, -1.5, 0.8, -2.55, 0.1, 1.85)
    v.window(-0.6, 0.9, 2.99, 0.9, 2.25, night=True, lights=14, face=-1, axis="x")
    v.box(2.86, 2.94, -0.95, -0.66, 0.8, 2.35, (0.55, 0.30, 0.32))
    v.box(2.86, 2.94, 0.96, 1.25, 0.8, 2.35, (0.55, 0.30, 0.32))
    _matchbox(v, MB[0], MB[1])
    v.light(-2.33, 1.6, 1.6, 150, (1.0, 0.78, 0.5), 0.3, "ep31_n_lamp")
    v.light(0.0, 0.3, 2.1, 85, (1.0, 0.88, 0.7), 0.5, "ep31_n_top")
    v.light(2.6, 0.1, 1.7, 14, (0.55, 0.65, 1.0), 0.9, "ep31_n_moon")
    v.light(0.0, -0.5, 0.45, 40, (1.0, 0.85, 0.65), 0.4, "ep31_n_fill")
    v.light(0.1, -0.6, 0.55, 0, (0.6, 0.7, 1.0), 0.5, "ep31_n_cool")


def _sets():
    return (("bed", _bed), ("dine", _dine), ("sill", _sill), ("night", _night))


# ───────────────────────── 고양이 (이 파일 안에서 상자로 만든 주황 줄무늬) ─────────────────────────
# 재질 번호: 0 털 · 1 줄무늬 · 2 크림(주둥이·발·배) · 3 분홍(코·속귀) · 4 홍채(살짝 빛남) · 5 검정 · 6 흰색(하이라이트·수염)
CAT_COLS = [(0.93, 0.52, 0.16), (0.62, 0.28, 0.07), (0.98, 0.93, 0.82), (0.96, 0.62, 0.66), (0.86, 0.88, 0.16),
            (0.015, 0.015, 0.02), (0.97, 0.97, 0.97)]
# 원점 = 엉덩이 바닥, 앞 = +x. 서기/걷기/웅크림은 곧은 몸, lie는 엎드림, rb는 몸을 오른쪽으로 말아 가는 단계(호 반지름 RING_R)
CAT_ORDER = ["stand", "walk_a", "walk_b", "crouch", "lie0o", "lie0c", "rb0", "rb1", "rb2", "rb3", "rb4", "rb5"]
CAT_IX = {n: k for k, n in enumerate(CAT_ORDER)}
RING_R = 0.21          # 말았을 때 몸 가운데선 반지름 (안쪽 반지름 = RING_R - 0.07 > 성냥갑 반대각선/2)
SPINE = 0.40           # 몸통 길이
BENDS = [0.18, 0.38, 0.58, 0.78, 0.92, 1.0]
CAT_EYES = {"stand": 1, "walk_a": 1, "walk_b": 1, "crouch": 1, "lie0o": 1, "lie0c": 0,
            "rb0": 1, "rb1": 1, "rb2": 1, "rb3": 0, "rb4": 0, "rb5": 0}


def _cat_head(K, eyes):
    """머리 (머리 기준 좌표: 뒤쪽 면 x=0, 앞 x=0.11, 바닥 z=0). 눈은 홍채(십자 모양 칸)+세로 동공+하이라이트, 감으면 가는 선."""
    P = []

    def b(cx, cy, z0, sx, sy, sz, mi):
        P.append((K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True), mi))
    b(0.055, 0, 0.0, 0.11, 0.13, 0.11, 0)
    for sy in (-0.043, 0.043):                                       # 귀 + 속귀 (머리 옆면과 같은 평면이 되지 않게 안쪽으로)
        b(0.03, sy, 0.107, 0.03, 0.04, 0.045, 0)
        b(0.0455, sy, 0.114, 0.004, 0.026, 0.03, 3)
    for y in (-0.03, 0.0, 0.03):                                      # 이마 줄무늬
        b(0.05, y, 0.108, 0.06, 0.012, 0.005, 1)
    b(0.1175, 0, 0.003, 0.014, 0.065, 0.037, 2)                       # 주둥이 · 코 · 입
    b(0.1275, 0, 0.034, 0.006, 0.02, 0.012, 3)
    b(0.1255, 0, 0.012, 0.002, 0.03, 0.004, 5)
    for dz in (0.012, 0.020, 0.028):                                   # 수염
        for sg in (-1, 1):
            b(0.1255, sg * 0.075, dz, 0.003, 0.09, 0.003, 6)
    ze = 0.063
    for sy in (-0.036, 0.036):
        if eyes:
            for dy, w, h in ((0.0, 0.032, 0.042), (-0.0185, 0.005, 0.032), (0.0185, 0.005, 0.032)):   # 테두리: 십자를 겹치지 않는 3조각으로
                b(0.1104, sy + dy, ze - h / 2, 0.0016, w, h, 5)
            for dy, w, h in ((0.0, 0.026, 0.036), (-0.0155, 0.005, 0.026), (0.0155, 0.005, 0.026)):   # 홍채
                b(0.1126, sy + dy, ze - h / 2, 0.0028, w, h, 4)
            b(0.1147, sy, ze - 0.016, 0.0016, 0.010, 0.032, 5)         # 동공
            b(0.1161, sy + 0.007, ze + 0.006, 0.0014, 0.008, 0.008, 6)  # 하이라이트
        else:
            b(0.1105, sy, ze - 0.002, 0.002, 0.036, 0.005, 5)
    return P


def _cat_place(X, parts, ox, oy, oz, yaw):
    for bm, _ in parts:
        if yaw:
            _rot_z(bm, yaw, (0.0, 0.0))
        X._shift(bm, ox, oy, oz)
    return parts


def _cat_upright(K, X, name):
    """서기·걷기·웅크림: 곧은 몸통 + 다리 4 + 목·머리 + 위로 말린 꼬리."""
    P = []
    low = name == "crouch"
    z = 0.045 if low else 0.11            # 몸통 바닥
    phase = {"walk_a": 1, "walk_b": -1}.get(name, 0)

    def b(cx, cy, z0, sx, sy, sz, mi):
        P.append((K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True), mi))
    b(0.20, 0, z, 0.40, 0.15, 0.14, 0)
    b(0.20, 0, z - 0.005, 0.30, 0.09, 0.02, 2)
    b(0.396, 0, z + 0.01, 0.014, 0.08, 0.10, 2)
    for k in range(5):
        b(0.045 + 0.075 * k, 0, z + 0.003, 0.028, 0.158, 0.14, 1)
    if low:                                                           # 웅크림: 앞발은 앞으로 쭉, 뒷다리는 접어 엉덩이 옆
        for sy in (-0.05, 0.05):
            b(0.40, sy, 0.0, 0.15, 0.05, 0.045, 0)
            b(0.49, sy, 0.0, 0.05, 0.056, 0.035, 2)
            b(0.07, sy * 1.2, 0.0, 0.12, 0.07, 0.10, 0)
    else:
        sw = 0.45 * phase
        for lx, ly, sg in ((0.355, -0.048, 1), (0.355, 0.048, -1), (0.07, -0.052, -1), (0.07, 0.052, 1)):
            front = lx > 0.2
            leg = K.bm_cube(0.055 if front else 0.085, 0.05 if front else 0.06, (0.12 if front else 0.13) - 0.035, (lx, ly, 0.035),
                            bottom=True)
            paw = K.bm_cube(0.065, 0.056, 0.037, (lx + 0.003, ly, 0.0), bottom=True)
            for bm in (leg, paw):
                if sw:
                    X._rot_y(bm, sg * sw, (lx, 0, 0.12))
            P += [(leg, 0), (paw, 2)]
    b(0.385, 0, z + 0.08, 0.09, 0.10, 0.15, 0)                        # 목
    hz = z + 0.145
    P += _cat_place(X, _cat_head(K, True), 0.415, 0.0, hz - 0.0, 0.0)
    for k in range(9):                                                # 꼬리: 뒤로 뻗다 위로
        w = 0.048 - 0.002 * k
        zz = (0.06 if low else 0.17) + (0.014 if low else 0.038) * k
        b(-0.03 - 0.028 * k, 0, zz - 0.025, 0.05, w, 0.05, 1 if (k % 2 or k == 8) else 0)
    return P


def _cat_lie(K, X, bend, eyes):
    """엎드린 고양이: 몸통 16칸을 호로 이은 상자 사슬(오른쪽으로 bend만큼 휨) + 엉덩이 + 머리(턱 괴고) + 꼬리(같은 호의 뒤쪽)."""
    P = []
    kap = -bend / RING_R
    n = 16
    ds = SPINE / n

    def pos(s):
        if abs(kap) < 1e-6:
            return s, 0.0, 0.0
        return math.sin(kap * s) / kap, (1 - math.cos(kap * s)) / kap, kap * s

    for k in range(n):
        px, py, h = pos((k + 0.5) * ds)
        bm = K.bm_cube(ds * 1.18, 0.152 - 0.002 * k, 0.125 + 0.0012 * (k % 5), (px, py, 0.0), bottom=True)   # 겹치는 이웃 칸(몸을 말 때 안쪽에서 최대 4칸)과 윗면 높이를 달리
        P.append((_rot_z(bm, h, (px, py)), 1 if k % 3 == 2 else 0))
    px, py, h = pos(0.06)                                             # 엉덩이 불룩
    for sg in (-1, 1):
        bm = K.bm_cube(0.09, 0.07, 0.135, (px - sg * 0.07 * math.sin(h), py + sg * 0.07 * math.cos(h), 0.0), bottom=True)
        P.append((_rot_z(bm, h, (px - sg * 0.07 * math.sin(h), py + sg * 0.07 * math.cos(h))), 0))
    ex, ey, eh = pos(SPINE)                                           # 머리: 몸 끝에서 안쪽으로 더 돌려 턱을 괴고
    hh = eh - 0.7 * bend
    head = _cat_head(K, eyes)
    for sy in (-0.045, 0.045):                                        # 턱 밑 앞발
        head.append((K.bm_cube(0.075, 0.05, 0.036, (0.135, sy, 0.0), bottom=True), 2))
    P += _cat_place(X, head, ex - 0.005 * math.cos(eh), ey - 0.005 * math.sin(eh), 0.0, hh)
    for k in range(10):                                               # 꼬리: 같은 호를 뒤로 이어 바닥에 깔림
        px, py, h = pos(-(k + 0.5) * 0.032)
        w = 0.05 - 0.0015 * k
        bm = K.bm_cube(0.036, w, w, (px, py, 0.0), bottom=True)
        P.append((_rot_z(bm, h, (px, py)), 1 if (k % 2 or k == 9) else 0))
    return P


def _cat_parts(name):
    from engine import bkit as K
    from engine import voxel as X
    if name in ("stand", "walk_a", "walk_b", "crouch"):
        return _cat_upright(K, X, name)
    if name in ("lie0o", "lie0c"):
        return _cat_lie(K, X, 0.0, name == "lie0o")
    k = int(name[2])
    return _cat_lie(K, X, BENDS[k], bool(CAT_EYES[name]))


def ring_origin(c, psi_deg):
    """몸을 말았을 때 고리 가운데가 c가 되도록 하는 고양이 원점(엉덩이)과 방향. 고리 가운데는 몸의 오른쪽 RING_R."""
    p = math.radians(psi_deg)
    return c[0] - RING_R * math.sin(p), c[1] + RING_R * math.cos(p)


# ───────────────────────── 캐릭터 위치·손·얼굴 점 ─────────────────────────
def at(st, x, y, yaw, pose, z=0.0, **kw):
    return dict(set=st, x=x, y=y, yaw=yaw, pose=pose, z=z, **kw)


def rel(d, fwd, lat, up):
    """캐릭터 기준 (앞, 왼쪽, 위) → 세트 좌표. 크기 반영."""
    a = math.radians(d["yaw"])
    s = d["scale"]
    return (d["x"] + s * (fwd * math.cos(a) - lat * math.sin(a)), d["y"] + s * (fwd * math.sin(a) + lat * math.cos(a)),
            d["z"] + s * up)


def _base(pose):
    return KINDS[pose]["base"] if pose in KINDS else pose


def face_pt(d):
    """얼굴 가운데 점(세트 좌표). 누운 자세는 머리가 몸 뒤(-x)쪽에 있음."""
    s = d["scale"]
    a = math.radians(d["yaw"])
    if d["pose"] in ("lie", "lieopen"):
        return (d["x"] - math.cos(a) * 1.59 * s, d["y"] - math.sin(a) * 1.59 * s, d["z"] + 0.24 * s)
    hz = 1.28 if _base(d["pose"]) in SITS else 1.59
    return (d["x"], d["y"], d["z"] + hz * s)


def mouth_pt(d):
    """입 앞 점(세트 좌표)."""
    hz = 1.05 if _base(d["pose"]) in SITS else 1.36
    return rel(d, 0.26, 0.0, hz + 0.045)


def walk_pose(tl, step=0.26):
    return "walk_a" if int(tl / step) % 2 == 0 else "walk_b"


def mover(keys, st, step=0.26, end="stand", face=None, z=0.0, bob=0.003):
    """keys = [(줄 안 시각, x, y), ...]를 직선으로 이으며 걷는 함수(over용). 걷는 동안엔 step초마다 발걸음 자세를 바꾸고
    멈추면 end 자세로 face 방향(없으면 마지막으로 가던 방향)을 본다."""
    segs = [(a, b) for a, b in zip(keys, keys[1:]) if abs(b[1] - a[1]) + abs(b[2] - a[2]) > 1e-6]

    def fn(tl, du, u):
        head = math.degrees(math.atan2(segs[0][1][2] - segs[0][0][2], segs[0][1][1] - segs[0][0][1]))
        for a, b in segs:
            if a[0] < tl:
                head = math.degrees(math.atan2(b[2] - a[2], b[1] - a[1]))
        x, y, moving = keys[-1][1], keys[-1][2], False
        if tl <= keys[0][0]:
            x, y = keys[0][1], keys[0][2]
        elif tl < keys[-1][0]:
            for a, b in zip(keys, keys[1:]):
                if a[0] <= tl < b[0]:
                    k = (tl - a[0]) / (b[0] - a[0])
                    x, y = a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k
                    moving = abs(b[1] - a[1]) + abs(b[2] - a[2]) > 1e-6
        if moving:
            return at(st, x, y, head, walk_pose(tl, step), z + bob * abs(math.sin(math.pi * tl / step)))
        return at(st, x, y, head if face is None else face, end, z)
    return fn


# ───────────────────────── 점프·낙하 (공기저항: 종단속도에 가까워짐) ─────────────────────────
EDGE_X = 0.50                      # 침대 가장자리(0.55) 앞에서 아이가 서는 곳
VT, TAU0, VX = 0.62, 0.28, 0.50    # 종단속도 m/s · 시간상수 s · 가로 속도 m/s


def drop(tau):
    return VT * (tau - TAU0 * (1 - math.exp(-tau / TAU0)))


def _solve_land():
    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if drop(mid) < BED_Z - RUG_Z else (lo, mid)
    return hi


TAU_L = _solve_land()              # 침대에서 러그까지 떨어지는 시간 (약 1.07초)
LAND_X = EDGE_X + VX * TAU_L
T_JUMP = 0.35                      # 3번 줄에서 뛰어내리는 때


def _k_hook(tl, du, u):
    return at("dine", 0.15, 0.58, -115, "lookup", TZ)


def _k_wake(tl, du, u):
    if tl < 0.6:
        return at("bed", 0.0, 1.82, -90, "lie", BED_Z)
    if tl < 1.2:
        return at("bed", 0.0, 1.82, -90, "lieopen", BED_Z)
    return at("bed", 0.0, 1.88, -55, "sit_conf", BED_Z)


def _k_cliff(tl, du, u):
    if tl < 0.9:
        k = tl / 0.9
        return at("bed", lerp(-0.04, EDGE_X, k), 1.15, 0, walk_pose(tl), BED_Z + 0.002 * abs(math.sin(math.pi * tl / 0.26)))
    return at("bed", EDGE_X, 1.15, 0, "peek" if tl < 1.9 else "confused", BED_Z)


def _k_jump(tl, du, u):
    if tl < T_JUMP:
        return at("bed", EDGE_X, 1.15, 0, "peek", BED_Z)
    tau = tl - T_JUMP
    hop = 0.03 * math.sin(math.pi * tau / 0.3) if tau < 0.3 else 0.0
    if tau < TAU_L:
        return at("bed", EDGE_X + VX * tau, 1.15, 0, "star", max(BED_Z + hop - drop(tau), RUG_Z))
    k = tau - TAU_L
    return at("bed", LAND_X, 1.15, 0, "stand", RUG_Z + (0.007 * abs(math.sin(math.pi * k / 0.16)) if k < 0.16 else 0.0))


def _t_jump(tl, du, u):
    """3번 줄 카메라 목표점: 떨어지는 아이를 따라감."""
    d = _k_jump(tl, du, u)
    return (0.55 * d["x"] + 0.45 * 0.80, 1.15, d["z"] + 0.05)


LINES[LN["jump"]]["shot"] = ("bed", _t_jump, -20, 10, 0.55, 26, 0.9, 6)


def _t_cliff(tl, du, u):
    """2번 줄 카메라 목표점: 침대 가장자리 쪽으로 걸어가는 아이를 천천히 따라감."""
    return (lerp(0.28, 0.46, ramp(tl, 0.0, 1.2)), 1.15, 0.38)


LINES[LN["cliff"]]["shot"] = ("bed", _t_cliff, 20, 36, 0.8, 26, 0.9, -6)


def _k_land(tl, du, u):
    if tl < 0.2:
        return at("bed", LAND_X, 1.15, 10, "stand", RUG_Z)
    if tl < 1.5:
        return at("bed", LAND_X, 1.15, 10, "dustR" if int((tl - 0.2) / 0.2) % 2 == 0 else "dustL", RUG_Z)
    return at("bed", LAND_X, 1.15, lerp(10, 150, ramp(tl, 1.5, 2.0)), "lookup", RUG_Z)


SC_XY = (1.30, 0.72)


def scale_text(tl):
    """체중계 화면: 65kg → (숫자가 굴러 내려가) → 13g."""
    if tl < 0.5:
        return "65kg"
    k = ramp(tl, 0.5, 1.15)
    if tl < 1.2:
        return "%dkg" % int(round(lerp(65, 13, k)))
    return "13g"


def _k_kg(tl, du, u):
    if tl < 0.5:
        return at("bed", SC_XY[0], SC_XY[1], -90, "stand", SC_Z)
    if tl < 1.25:
        return at("bed", SC_XY[0], SC_XY[1], -90, "confused", SC_Z)
    p = ((tl - 1.25) % 0.5) / 0.5
    z = SC_Z + 0.014 * 4 * p * (1 - p)
    return at("bed", SC_XY[0], SC_XY[1], -90, "cheer" if z > SC_Z + 0.002 else "stand", z)


def _k_rice(tl, du, u):
    return at("dine", 0.0, 0.05, -80, "holdgrain", TZ + 0.0015 * abs(math.sin(2.2 * tl)))


def _k_fridge(tl, du, u):
    if tl < 0.7:
        return at("dine", 2.50, 1.08, 90, "lookup", 0.0)
    p = ((tl - 0.7) % 0.55) / 0.55
    z = 0.05 * 4 * p * (1 - p)
    return at("dine", 2.50, 1.08, 90, "cheer" if z > 0.004 else "lookup", z)


KID_SILL = (-0.01, 2.36)


def _k_rain(tl, du, u):
    return at("sill", KID_SILL[0], KID_SILL[1], 90, "confused" if tl < 1.2 else "lookup", SILL_Z)


T_DROP = 1.15              # 9번 줄: 큰 빗방울이 창에 부딪히는 때
DROP_AT = (0.065, 2.535, 1.07)


def _k_drop(tl, du, u):
    if tl < T_DROP:
        return at("sill", KID_SILL[0], KID_SILL[1], 90, "stand", SILL_Z)
    k = tl - T_DROP
    if k < 0.45:                                                   # 깜짝: 팔을 번쩍 들고 뒤로 폴짝
        z = SILL_Z + 0.02 * 4 * (k / 0.45) * (1 - k / 0.45)
        return at("sill", KID_SILL[0], KID_SILL[1] - 0.03 * ramp(k, 0.0, 0.45), 90, "cheer", z)
    return at("sill", KID_SILL[0], KID_SILL[1] - 0.03, 90, "confused", SILL_Z)


CAT_P0, CAT_P1 = (1.10, 1.50), (1.02, 0.25)      # 10번 줄: 고양이가 걸어오는 길 (바깥쪽 식탁 오른쪽 길)


def _k_cat(tl, du, u):
    c = cat_state(LN["cat"], tl, du)
    face = math.degrees(math.atan2(c["y"] + 0.52, c["x"] - 0.86))
    return at("dine", 0.86, -0.52, face, "stand" if tl < 1.0 else "confused", 0.0)


CAT_EYE = dict(head=(1.0, -0.80), psi=-100.0)


def _k_eye(tl, du, u):
    h = CAT_EYE["head"]
    p = math.radians(CAT_EYE["psi"])
    f, l = 0.09, 0.085
    x = h[0] + f * math.cos(p) - l * math.sin(p)
    y = h[1] + f * math.sin(p) + l * math.cos(p)
    return at("dine", x, y, CAT_EYE["psi"], "confused", 0.0)


# 밤 거실: 가족 (아빠 파랑·엄마 분홍·아이 노랑)
FORM_Y = -0.15
KX = 0.0
DX = KX - 0.087                    # 손잡은 줄에서 아빠(왼쪽)·엄마(오른쪽) 자리 (손이 맞닿는 간격)
MX = KX + 0.0848
TRAY = {"d": (MB[0] - 0.047, MB[1] + 0.025), "k": (MB[0], MB[1] + 0.025), "m": (MB[0] + 0.047, MB[1] + 0.025)}


def _wave(tl, ph, a="waveR", b="cheer", per=0.3):
    return a if int((tl + ph) / per) % 2 == 0 else b


def _k_call(tl, du, u):
    return at("night", 0.0, -0.25, 90, _wave(tl, 0.0), RUG_Z)


def _d_call(tl, du, u):
    return at("night", -0.20, 0.80, -90, _wave(tl, 0.15, "waveL", "cheer"), RUG_Z)


def _m_call(tl, du, u):
    return at("night", 0.17, 0.30, -90, _wave(tl, 0.07, "waveR", "cheer"), RUG_Z)


def _k_gather(tl, du, u):
    if tl < 0.35:
        return at("night", KX, FORM_Y - 0.10 * (1 - tl / 0.35), 90 - 180 * ramp(tl, 0.0, 0.35), "cheer", RUG_Z)
    return at("night", KX, FORM_Y, -90, "holdK" if tl > 1.45 else "stand", RUG_Z)


def _d_gather(tl, du, u):
    if tl < 1.35:
        return mover([(0.0, -0.20, 0.80), (1.35, DX, FORM_Y)], "night", step=0.16, face=-90, z=RUG_Z)(tl, du, u)
    return at("night", DX, FORM_Y, -90, "holdL", RUG_Z)


def _m_gather(tl, du, u):
    if tl < 1.35:
        return mover([(0.0, 0.17, 0.30), (1.35, MX, FORM_Y)], "night", step=0.16, face=-90, z=RUG_Z)(tl, du, u)
    return at("night", MX, FORM_Y, -90, "holdR", RUG_Z)


def _sit(tag, pose, jit=0.0, tl=0.0):
    x, y = TRAY[tag]
    if jit:
        x += jit * math.sin(2 * math.pi * 13 * tl + (0.0 if tag == "d" else 1.7 if tag == "k" else 3.1))
    return at("night", x, y, -90, pose, MB_Z)


def _k_box(tl, du, u):
    return _sit("k", "sit_smile")


def _k_cold(tl, du, u):
    return _sit("k", "sit_hug", 0.0012, tl)


def _k_curl(tl, du, u):
    return _sit("k", "sit_conf" if tl < 1.1 else "sit_smile")


def _k_ask(tl, du, u):
    x, y = TRAY["k"]
    return at("night", x, y + 0.01, -90, "waveR" if int(tl / 0.35) % 2 == 0 else "cheer", MB_Z)


# ───────────────────────── 고양이 움직임 ─────────────────────────
def cat_state(i, tl, du):
    """줄 i에서 고양이 {set, x, y, z, yaw, pose, scale} 또는 None."""
    if i == LN["cat"]:                                   # 먼 곳에서 카메라 쪽으로 성큼성큼, 끝에서 멈춤
        k = clamp(tl / 2.1)
        x, y = lerp(CAT_P0[0], CAT_P1[0], k), lerp(CAT_P0[1], CAT_P1[1], k)
        walking = k < 1.0
        return dict(set="dine", x=x, y=y, z=0.0, yaw=math.degrees(math.atan2(CAT_P1[1] - CAT_P0[1], CAT_P1[0] - CAT_P0[0])),
                    pose=walk_pose(tl, 0.24) if walking else "stand", scale=1.0)
    if i == LN["eye"]:                                   # 엎드려 턱을 괴고 눈을 깜빡
        psi = CAT_EYE["psi"]
        p = math.radians(psi)
        h = CAT_EYE["head"]
        ox, oy = h[0] - 0.455 * math.cos(p), h[1] - 0.455 * math.sin(p)
        blink = 0.95 <= tl < 1.10 or 2.0 <= tl < 2.15
        return dict(set="dine", x=ox, y=oy, z=0.0, yaw=psi, pose="lie0c" if blink else "lie0o", scale=1.0)
    if i in (LN["curl"], LN["sleep"], LN["ask"]):        # 성냥갑 곁으로 와서 눕고 몸을 말아 감쌈
        psi = 90.0
        ox, oy = ring_origin(MB, psi)
        if i == LN["curl"]:
            if tl < 0.7:
                return dict(set="night", x=ox, y=lerp(oy - 0.60, oy, ramp(tl, 0.0, 0.7)), z=RUG_Z, yaw=psi,
                            pose=walk_pose(tl, 0.2), scale=1.0)
            seq = [(0.7, "stand"), (0.85, "crouch"), (1.05, "lie0o"), (1.2, "rb0"), (1.37, "rb1"), (1.54, "rb2"),
                   (1.71, "rb3"), (1.88, "rb4"), (2.05, "rb5")]
            pose = "stand"
            for t0, nm in seq:
                if tl >= t0:
                    pose = nm
            return dict(set="night", x=ox, y=oy, z=RUG_Z, yaw=psi, pose=pose, scale=1.0)
        return dict(set="night", x=ox, y=oy, z=RUG_Z, yaw=psi, pose="rb5", scale=1.0 + 0.012 * math.sin(2 * math.pi * 0.45 * tl))
    return None


_CAST = []


def cast():
    """[dict(tag, set, x, y, z, yaw, pose, hair, shirt, pants, scale, over={줄: dict 또는 함수(tl, du, u)}, only=보이는 줄 집합 또는 None)]"""
    if _CAST:
        return _CAST
    L = LN

    def add(tag, hair, shirt, pants, scale, over, only=None):
        _CAST.append(dict(tag=tag, set="bed", x=0.0, y=0.0, yaw=0.0, pose="stand", hair=hair, shirt=shirt, pants=pants,
                          scale=scale, z=0.0, over=over, only=only))
    fam = {L[k] for k in ("call", "gather", "box", "cold", "curl", "sleep", "ask")}
    add("kid", 0, KID_SH, KID_PA, S_KID, {
        L["hook"]: _k_hook, L["wake"]: _k_wake, L["cliff"]: _k_cliff, L["jump"]: _k_jump, L["land"]: _k_land,
        L["kg"]: _k_kg, L["rice"]: _k_rice, L["fridge"]: _k_fridge, L["rain"]: _k_rain, L["drop"]: _k_drop,
        L["cat"]: _k_cat, L["eye"]: _k_eye, L["call"]: _k_call, L["gather"]: _k_gather, L["box"]: _k_box,
        L["cold"]: _k_cold, L["curl"]: _k_curl, L["sleep"]: lambda tl, du, u: _sit("k", "sleep_k"), L["ask"]: _k_ask})
    add("dad", 0, DAD_SH, DAD_PA, S_DAD, {
        L["call"]: _d_call, L["gather"]: _d_gather, L["box"]: lambda tl, du, u: _sit("d", "sit_smile"),
        L["cold"]: lambda tl, du, u: _sit("d", "sit_hug", 0.0012, tl),
        L["curl"]: lambda tl, du, u: _sit("d", "sit_conf" if tl < 0.9 else "sit_smile"),
        L["sleep"]: lambda tl, du, u: _sit("d", "sleep_d"), L["ask"]: lambda tl, du, u: _sit("d", "sleep_d")}, only=fam)
    add("mom", 1, MOM_SH, MOM_PA, S_MOM, {
        L["call"]: _m_call, L["gather"]: _m_gather, L["box"]: lambda tl, du, u: _sit("m", "sit_smile"),
        L["cold"]: lambda tl, du, u: _sit("m", "sit_hug", 0.0012, tl),
        L["curl"]: lambda tl, du, u: _sit("m", "sit_conf" if tl < 0.9 else "sit_smile"),
        L["sleep"]: lambda tl, du, u: _sit("m", "sleep_m"), L["ask"]: lambda tl, du, u: _sit("m", "sleep_m")}, only=fam)
    return _CAST


# ───────────────────────── 소품·효과 (일반 상자 F · 발광 상자 G · 금속 상자 M · 구/타원체 B) ─────────────────────────
WHITE, STEAM = (0.97, 0.97, 0.95), (0.97, 0.97, 0.98)
RICE_C, DROP_C, SPLAT_C = (0.97, 0.96, 0.92), (0.55, 0.78, 1.0), (0.72, 0.86, 1.0)
GRAIN = 0.009           # 밥알 길이(m)
DROPD = 0.0055          # 큰 빗방울 지름(m) — 키 8.5cm 아이에겐 테니스공 크기
RW = np.random.default_rng(3103).uniform(0.0, 1.0, (200, 6))


def _euler_xyz(R):
    """회전행렬 → Blender XYZ 오일러 (R = Rz·Ry·Rx)."""
    sy = -R[2, 0]
    b = math.asin(max(-1.0, min(1.0, sy)))
    if abs(sy) < 0.99999:
        return (math.atan2(R[2, 1], R[2, 2]), b, math.atan2(R[1, 0], R[0, 0]))
    return (math.atan2(-R[1, 2], R[1, 1]), b, 0.0)


def _frame(axis):
    """긴 축(로컬 z)이 axis를 향하는 회전행렬 (열 = 로컬 x, y, z)."""
    z = np.array(axis, float)
    z /= np.linalg.norm(z)
    x = np.cross((0.0, 0.0, 1.0), z)
    x = x / np.linalg.norm(x) if np.linalg.norm(x) > 1e-6 else np.array((1.0, 0.0, 0.0))
    return np.stack([x, np.cross(z, x), z], 1)


def spoon(head, axis, col=(0.88, 0.90, 0.93)):
    """금속 숟가락: head(머리 시작점)에서 axis 방향으로 머리 5cm · 목 2cm · 손잡이 10cm + 머리 테두리."""
    R = _frame(axis)
    e = _euler_xyz(R)
    H, d = np.array(head, float), R[:, 2]
    out = [(tuple(H + d * off), sz, e, col) for off, sz in
           ((0.026, (0.034, 0.0035, 0.052)), (0.062, (0.009, 0.0035, 0.02)), (0.122, (0.013, 0.0035, 0.10)))]
    for sx in (-1, 1):
        out.append((tuple(H + d * 0.026 + R[:, 0] * sx * 0.0165 + R[:, 1] * 0.0025), (0.0025, 0.0045, 0.052), e, col))
    return out


def steam(x, y, z0, t, n=6, rise=0.13, size=0.013):
    """밥공기에서 오르는 김: 하얀 작은 상자가 솟으며 작아짐."""
    out = []
    for k in range(n):
        p = (k / n + t / 1.8) % 1.0
        s = size * (1 - 0.55 * p)
        out.append(((x + 0.014 * math.sin(6.3 * (p + k * 0.37)), y + 0.01 * math.cos(6.3 * (p + k * 0.21)), z0 + rise * p),
                    (s, s, s), (p * 3, k, p * 2), STEAM))
    return out


def puffs(c, tl, t0, n=8, r=0.045, life=0.6, size=0.012, col=(0.95, 0.93, 0.88)):
    """c 둘러싸고 퍼지며 사라지는 먼지 덩이."""
    tau = tl - t0
    if tau <= 0 or tau > life:
        return []
    f = tau / life
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + 0.4 * (k % 3)
        rr = r * (0.3 + 0.7 * math.sqrt(f))
        s = size * (1 - f) * (1 + 0.4 * (k % 2))
        out.append(((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a), c[2] + s / 2 + 0.006 * f), (s, s, s), (a, f * 3, 0), col))
    return out


def sparkles(c, tl, t0, n=12, r=0.05, life=0.9, size=0.006, cols=((1.0, 0.85, 0.3), (1.0, 0.6, 0.75), (1.0, 1.0, 0.9))):
    """c 둘러싸고 터지는 발광 반짝이."""
    tau = tl - t0
    if tau <= 0 or tau > life:
        return []
    f = tau / life
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + 0.7 * (k % 3)
        rr = r * (0.35 + 0.65 * ((k * 5) % 7) / 6.0) * math.sqrt(f)
        s = size * (1 - f) * (1 + 0.5 * (k % 2))
        out.append(((c[0] + rr * math.cos(a), c[1] + 0.3 * rr * math.sin(2 * a), c[2] + rr * math.sin(a) * 0.9 + 0.01), (s, s, s),
                    (a, f * 4, 0), cols[k % len(cols)]))
    return out


def breath(d, tl, ph=0.0, n=3, life=0.9, size=0.0075):
    """얼굴 앞에서 오르며 사라지는 하얀 입김."""
    mx, my, mz = mouth_pt(d)
    a = math.radians(d["yaw"])
    out = []
    for k in range(n):
        age = (tl + ph + k * life / n) % life
        f = age / life
        s = size * (1 - 0.6 * f) * (d["scale"] / 0.05)
        fwd = 0.004 + 0.03 * f
        out.append(((mx + math.cos(a) * fwd, my + math.sin(a) * fwd, mz - 0.003 + 0.04 * f), (s, s, s), (0.4 * k, 0.3 * k, 0.5 * k),
                    (0.96, 0.98, 1.0)))
    return out


def voice(d, target, tl, ph=0.0, n=3, size=0.006, reach=0.07):
    """부르는 목소리: 입에서 target 쪽으로 나가다 작아져 사라짐(너무 작아서 안 닿음)."""
    mx, my, mz = mouth_pt(d)
    dx, dy = target[0] - mx, target[1] - my
    ln = math.hypot(dx, dy) or 1.0
    out = []
    for k in range(n):
        f = (tl * 1.5 + ph + k / n) % 1.0
        s = size * (1 - f) * (d["scale"] / 0.05)
        out.append(((mx + dx / ln * reach * f, my + dy / ln * reach * f, mz + 0.004 * math.sin(6.3 * (f + k))), (s, s, s), (0, 0, 0),
                    (0.96, 0.96, 0.92)))
    return out


def rain_streaks(tl, n=40, y0=2.575, y1=2.64, x_half=0.17):
    """유리 바깥(y>2.54)에서 비스듬히 떨어지는 빗줄기 (발광 가는 상자)."""
    out = []
    for k in range(n):
        r = RW[k]
        sp = 2.2 + 1.4 * r[2]
        z = 1.45 - ((r[3] * 0.65 + tl * sp) % 0.65)
        out.append(((-x_half + 2 * x_half * r[0], y0 + (y1 - y0) * r[1], z + 0.0), (0.0016, 0.0016, 0.075), (0.0, 0.12, 0.0),
                    (0.42, 0.54, 0.70)))
    return out


def splat(x, z, tau, big=1.0):
    """유리(y=2.533)에 부딪혀 퍼지는 물: 납작한 물판 + 둘레로 튀는 방울 6 + 아래로 흐르는 줄."""
    if tau <= 0 or tau > 0.9:
        return []
    f = clamp(tau / 0.45)
    w = big * 0.010 * math.sqrt(ramp(tau, 0.0, 0.12))
    out = [((x, 2.533, z), (w, 0.0015, w), (0, 0, 0), SPLAT_C)]
    for dx, dz, k in ((1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 0.7), (-1, 1, 0.7), (1, -1, 0.7), (-1, -1, 0.7)):
        out.append(((x + dx * w * 1.05, 2.533, z + dz * w * 1.05), (w * k * 0.9, 0.0015, w * k * 0.9), (0, 0, 0), SPLAT_C))
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.5
        r = big * (0.010 + 0.024 * math.sqrt(f))
        s = big * 0.0045 * (1 - 0.8 * f)
        out.append(((x + r * math.cos(a), 2.533, z + r * math.sin(a)), (s, 0.002, s), (0, 0, 0), SPLAT_C))
    run = big * 0.05 * clamp((tau - 0.1) / 0.7) ** 1.3
    if run > 0.004:
        out.append(((x, 2.533, z - run / 2), (0.0025 * big, 0.0015, run), (0, 0, 0), SPLAT_C))
    return out


HITS8 = [(0.30, -0.09, 1.10), (0.62, 0.07, 1.22), (0.92, -0.05, 1.03), (1.20, 0.10, 1.14), (1.48, -0.11, 1.26),
         (1.78, 0.02, 1.07), (2.05, -0.03, 1.20), (2.32, 0.09, 1.02)]


def rain_hits(tl):
    """8번 줄: 작은 빗방울들이 날아와 창에 탁탁 부딪혀 퍼짐. -> (구 B, 물판 F)"""
    B, F = [], []
    for th, x, z in HITS8:
        p = (tl - (th - 0.22)) / 0.22
        if 0.0 <= p < 1.0:
            q = 1 - p
            B.append((0, (x + 0.05 * q, 2.533 + 0.18 * q, z + 0.10 * q * q), 0.0045, (0, 0, 0), DROP_C))
        F += splat(x, z, tl - th)
    return B, F


def drop_flight(tl):
    """9번 줄: 큰 빗방울(지름 5.5mm) 하나가 날아와 창에 부딪혀 퍼짐. -> (구 B, 물판 F)"""
    t0 = T_DROP - 0.55
    p = (tl - t0) / 0.55
    B, F = [], []
    if 0.0 <= p < 1.0:
        q = 1 - p
        B.append((0, (DROP_AT[0] + 0.07 * q, 2.533 + 0.19 * q, DROP_AT[2] + 0.10 * q * q), DROPD, (0, 0, 0), DROP_C))
    else:
        F = splat(DROP_AT[0], DROP_AT[2], tl - T_DROP, big=1.5)
    return B, F


def _mound():
    """밥 더미 위·옆에 얹는 밥알 자리 (x, y, z(식탁 기준), 방향, 기울기) — 위쪽 28 · 옆쪽 20."""
    r = np.random.default_rng(3101)
    out = []
    for k in range(48):
        if k < 28:
            out.append((r.uniform(-0.024, 0.024), r.uniform(-0.024, 0.024), 0.1035, r.uniform(0, math.pi), r.uniform(-0.3, 0.3)))
        else:
            a, q = r.uniform(0, 2 * math.pi), r.uniform(0.030, 0.045)
            out.append((q * math.cos(a), q * math.sin(a), 0.0965, r.uniform(0, math.pi), r.uniform(-0.3, 0.3)))
    return out


MOUND = _mound()


def mound_grains():
    return [(1, (BOWL[0] + x, BOWL[1] + y, TZ + z), GRAIN, (rx, 0.0, rz), RICE_C) for x, y, z, rz, rx in MOUND]


def loose_grains(pts):
    return [(1, (x, y, TZ + 0.0022), GRAIN, (0.0, 0.0, a), RICE_C) for x, y, a in pts]


def props(i, tl, du, u, A, cat, cam, t):
    """줄 i의 소품 → (F 일반 상자, G 발광 상자, M 금속 상자, B 구·타원체) — 세트 좌표. 상자 = (중심, 크기, 오일러, 색), 구 = (종류, 중심, 지름, 오일러, 색)."""
    F, G, M, B = [], [], [], []
    L = LN
    kid = A["kid"]
    st = LINES[i]["shot"][0]
    o = OFF[st]
    cl = (cam["loc"][0] - o[0], cam["loc"][1] - o[1], cam["loc"][2])             # 카메라 위치(세트 좌표)

    def bb(ctr):
        return billboard(ctr, cl)
    if i == L["hook"]:                                                           # 훅: 밥 김 · 숟가락 · 밥알
        F += steam(BOWL[0], BOWL[1], TZ + 0.105, t)
        M += spoon((BOWL[0] + 0.012, BOWL[1] - 0.006, TZ + 0.090), (0.55, -0.20, 0.80))
        B += mound_grains() + loose_grains([(0.17, 0.12, 0.4), (-0.03, 0.09, 1.9), (0.06, 0.05, 1.2)])
        G += sparkles((BOWL[0] + 0.06, BOWL[1] - 0.04, TZ + 0.15), tl, 0.35, 8, 0.03, 0.8, 0.004)
    elif i == L["wake"]:
        if tl < 0.75:                                                            # 자는 동안 Z
            for k, (dx, dz, c) in enumerate(((0.0, 0.0, 0.0035), (0.012, 0.012, 0.0027))):
                f = clamp((tl - 0.1 * k) / 0.65)
                fp = face_pt(kid)
                ctr = (fp[0] + dx, fp[1], fp[2] + 0.025 + dz + 0.02 * f)
                right, up, rz = bb(ctr)
                cells, w = text_cells("Z")
                G += pix_items(cells, w, ctr, c * (1 - 0.5 * f), right, up, (0.75, 0.85, 1.0), rz=rz)
    elif i == L["jump"]:
        F += puffs((EDGE_X + 0.01, 1.15, BED_Z), tl, T_JUMP + 0.02, 5, 0.025, 0.45, 0.009)
        F += puffs((LAND_X, 1.15, RUG_Z), tl, T_JUMP + TAU_L, 9, 0.05, 0.6, 0.012)
    elif i == L["land"]:
        for k in range(5):
            F += puffs((kid["x"], kid["y"], kid["z"] + 0.045), tl, 0.25 + 0.2 * k, 4, 0.022, 0.4, 0.008)
        G += sparkles((kid["x"], kid["y"], kid["z"] + 0.06), tl, 1.6, 8, 0.045, 0.7, 0.004)
    elif i == L["kg"]:
        txt = scale_text(tl)
        cells, w = text_cells(txt)
        done = tl >= 1.2
        G += pix_items(cells, w, (SC_XY[0], 0.4964, 0.0513), 0.0042, (1.0, 0.0, 0.0), (0.0, 0.0, 1.0),
                       (1.0, 0.85, 0.25) if done else (0.35, 1.0, 0.5), depth=0.0018)
        G += sparkles((SC_XY[0], 0.49, 0.07), tl, 1.2, 12, 0.07, 0.8, 0.005)
    elif i == L["rice"]:
        gp = rel(kid, 0.4608, 0.0, 1.2166)                                         # 두 손 사이 (팔 끝)
        B.append((1, gp, GRAIN * 1.15, (0.0, 0.0, math.radians(kid["yaw"]) + math.pi / 2), RICE_C))
        B += mound_grains()
        B += loose_grains([(-0.05, 0.26, 0.5), (0.07, 0.34, 2.0), (-0.09, 0.33, 1.1), (0.10, 0.27, 0.2), (0.03, 0.40, 2.6),
                           (-0.02, 0.22, 1.5), (0.11, 0.38, 0.9)])
        F += steam(BOWL[0], BOWL[1], TZ + 0.105, t)
    elif i == L["rain"]:
        G += rain_streaks(tl)
        b, f = rain_hits(tl)
        B += b
        F += f
    elif i == L["drop"]:
        G += rain_streaks(tl, 24)
        b, f = drop_flight(tl)
        B += b
        F += f
    elif i == L["call"]:
        mom, dad = A["mom"], A["dad"]
        F += voice(mom, (kid["x"], kid["y"], 0), tl, 0.0) + voice(dad, (mom["x"], mom["y"], 0), tl, 0.33)
        F += voice(kid, (mom["x"], mom["y"], 0), tl, 0.6)
    elif i == L["gather"]:
        if tl > 1.55:
            ctr = (KX, FORM_Y, RUG_Z + S_DAD * 1.95 + 0.012)
            right, up, rz = bb(ctr)
            pul = 1 + 0.12 * ramp(tl, 1.55, 1.8) * (1 + math.sin(6.3 * (tl - 1.55)) * 0.3)
            G += heart_items(ctr, 0.0038 * ramp(tl, 1.55, 1.75) * pul, right, up, rz)
            G += sparkles((KX, FORM_Y, RUG_Z + 0.07), tl, 1.5, 12, 0.07, 0.9, 0.005)
    elif i == L["cold"]:
        for k, tag in enumerate(("dad", "kid", "mom")):
            F += breath(A[tag], tl, 0.31 * k)
    elif i == L["curl"]:
        if 0.3 < tl < 0.95:                                                      # 고양이가 오자 깜짝: 느낌표
            ctr = (MB[0], MB[1] + 0.025, MB_Z + 0.135)
            right, up, rz = bb(ctr)
            cells, w = text_cells("!")
            s = 0.0042 * ramp(tl, 0.3, 0.42) * (1 - ramp(tl, 0.85, 0.95))
            G += pix_items(cells, w, ctr, max(s, 1e-5), right, up, (1.0, 0.85, 0.25), rz=rz)
        if tl > 1.8:
            ctr = (MB[0], MB[1] + 0.025, MB_Z + 0.135)
            right, up, rz = bb(ctr)
            G += heart_items(ctr, 0.0035 * ramp(tl, 1.8, 2.0), right, up, rz)
    elif i == L["sleep"]:
        for k, (dx, dz) in enumerate(((0.0, 0.0), (0.014, 0.014))):
            f = ((tl * 0.5 + 0.5 * k) % 1.0)
            ctr = (MB[0] + 0.0 + dx, MB[1] + 0.025, MB_Z + 0.115 + dz + 0.03 * f)
            right, up, rz = bb(ctr)
            cells, w = text_cells("Z")
            G += pix_items(cells, w, ctr, 0.0035 * (1 - 0.5 * f), right, up, (0.75, 0.85, 1.0), rz=rz)
    elif i == L["ask"]:
        fp = face_pt(kid)
        ctr = (fp[0], fp[1], fp[2] + 0.05 + 0.004 * math.sin(2 * math.pi * 0.9 * tl))
        right, up, rz = bb(ctr)
        cells, w = text_cells("?")
        G += pix_items(cells, w, ctr, 0.0062 * ramp(tl, 0.0, 0.25), right, up, (1.0, 0.85, 0.25), rz=rz)
        G += sparkles((fp[0], fp[1], fp[2] + 0.02), tl, 0.3, 14, 0.06, 1.2, 0.005)
    return F, G, M, B


# ───────────────────────── 한 프레임 ─────────────────────────
def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·고양이·소품 배열, 카메라, 조명."""
    i = line_at(t)
    a, b = shot_span(i)
    du = max(b - a, 1e-3)
    tl = max(t - a, 0.0)
    u = min(tl / du, 1.0)
    cam = cam_pose(i, tl, du, u)
    A, O = {}, {k: [] for k in ("P", "R", "CO", "C2", "SC", "PO")}
    for c in cast():
        d = dict(c)
        ov = c["over"].get(i)
        if callable(ov):
            ov = ov(tl, du, u)
        d.update(ov or {})
        d["show"] = c["only"] is None or i in c["only"]
        A[c["tag"]] = d
        ox, oy = OFF[d["set"]]
        O["P"].append((d["x"] + ox, d["y"] + oy, d["z"]))
        O["R"].append((0.0, 0.0, math.radians(d["yaw"])))
        O["CO"].append(d["shirt"])
        O["C2"].append(d["pants"])
        O["SC"].append(d["scale"] if d["show"] else 0.0)
        O["PO"].append(pose_index(d["pose"], d["hair"]))
    cat = cat_state(i, tl, du)
    F, G, M, B = props(i, tl, du, u, A, cat, cam, t)
    st = LINES[i]["shot"][0]
    o = OFF[st]

    def shift(items):
        return [((p[0] + o[0], p[1] + o[1], p[2]), s, r, c) for p, s, r, c in items]
    ball = [(k, (p[0] + o[0], p[1] + o[1], p[2]), s, r, c) for k, p, s, r, c in B]
    ct = None
    if cat:
        ox, oy = OFF[cat["set"]]
        ct = dict(P=(cat["x"] + ox, cat["y"] + oy, cat["z"]), R=(0.0, 0.0, math.radians(cat["yaw"])), S=cat["scale"],
                  PO=CAT_IX[cat["pose"]])
    return dict(O, i=i, tl=tl, u=u, set=st, cam=cam, A=A, cat=ct, fx=shift(F), glow=shift(G), met=shift(M), ball=ball,
                env=env(i, tl, du))


N_FX, N_GL, N_MET, N_BALL = 120, 150, 12, 100


def _mat_glow(name, strength=3.0):
    """인스턴스 'col' 색으로 빛나는 재질 (숫자·반짝임·빗줄기)."""
    from engine import bkit as K
    m, nt, out = K.new_mat(name)
    e = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, K.inst_attr(nt, "col"), e.inputs["Color"])
    e.inputs["Strength"].default_value = strength
    K.ln(nt, e.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def build(ctx):
    from engine import bkit as K
    from engine import voxel as X
    v = X.Vox(31)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep31_sun")
    cam = K.CamRig(ctx, lens=26, fstop=0)

    mats = X.people_mats()
    protos = X.people_protos(ctx, mats)
    for lh in (False, True):
        for kind in KIND_ORDER:
            protos.append(K.proto(ctx, "ep31_p_%s_%d" % (kind, int(lh)), K.join_bms(_variant(kind, lh)), mats))
    people = K.instancer_multi(ctx, "ep31_people", protos, len(cast()))
    # 고양이: 상자로 만든 원형 12종 (서기·걷기·웅크림·엎드림·몸 말기)
    cm = [K.mat_simple("ep31_c_fur", CAT_COLS[0], 0.9), K.mat_simple("ep31_c_stripe", CAT_COLS[1], 0.9),
          K.mat_simple("ep31_c_cream", CAT_COLS[2], 0.9), K.mat_simple("ep31_c_pink", CAT_COLS[3], 0.7),
          K.mat_simple("ep31_c_iris", CAT_COLS[4], 0.35, 0.0, CAT_COLS[4], 0.45), K.mat_simple("ep31_c_black", CAT_COLS[5], 0.4),
          K.mat_simple("ep31_c_white", CAT_COLS[6], 0.5)]
    cat = K.instancer_multi(ctx, "ep31_cat", [K.proto(ctx, "ep31_cp_" + n, K.join_bms(_cat_parts(n)), cm) for n in CAT_ORDER], 1)
    cube = lambda: K.bm_cube(1, 1, 1)
    fx = K.instancer(ctx, "ep31_fx", K.proto(ctx, "ep31_p_fx", cube(), [K.mat_inst("ep31_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep31_glow", K.proto(ctx, "ep31_p_glow", cube(), [_mat_glow("ep31_m_glow")]), N_GL, vector_scale=True)
    met = K.instancer(ctx, "ep31_met", K.proto(ctx, "ep31_p_met", cube(), [K.mat_simple("ep31_m_met", (0.88, 0.90, 0.93), 0.28, 0.85)]),
                      N_MET, vector_scale=True)
    balls = K.instancer_multi(ctx, "ep31_balls", [
        K.proto(ctx, "ep31_p_drop", K.bm_sphere(0.5, (0, 0, 0), 12, 8), [K.mat_simple("ep31_m_drop", DROP_C, 0.06, 0.0, (0.35, 0.62, 0.95), 0.6, 0.6)]),
        K.proto(ctx, "ep31_p_rice", K.bm_sphere(0.5, (0, 0, 0), 10, 6, scale=(1.0, 0.45, 0.42)), [K.mat_inst("ep31_m_rice", 0.55)])],
        N_BALL)

    def boxes(ob, items, cap):
        Pp, Ss, Rr, Cc = (np.zeros((cap, 3), np.float32) for _ in range(4))
        for k, (p, s, r, c) in enumerate(items[:cap]):
            Pp[k], Ss[k], Rr[k], Cc[k] = p, s, r, c
        K.set_points(ob, Pp, scale=(Ss[:, 0] > 0).astype(np.float32), size=Ss, rot=Rr, col=Cc)

    def upd(t, f):
        S = frame_state(t)
        c = S["cam"]
        cam.set(c["tgt"], c["az"], c["el"], c["dist"], c["lens"], roll=c["roll"], shift=c["shift"])
        e = S["env"]
        sun.data.energy = e["sun"]
        sun.data.color = e["sun_col"]
        sun.rotation_euler = tuple(math.radians(q) for q in e["sun_rot"])
        ctx.set_ctl("ambient", e["amb"])
        ctx.set_rgb("ambient_col", e["amb_col"])
        for name, en in e["lt"].items():
            lights[name].data.energy = en
        K.set_points(people, S["P"], scale=S["SC"], rot=S["R"], col=np.array(S["CO"], np.float32),
                     colors={"col2": np.array(S["C2"], np.float32)}, pose=S["PO"])
        ct = S["cat"]
        if ct:
            K.set_points(cat, [ct["P"]], scale=[ct["S"]], rot=[ct["R"]], pose=[ct["PO"]])
        else:
            K.set_points(cat, [(0.0, 0.0, 0.0)], scale=[0.0], rot=[(0.0, 0.0, 0.0)], pose=[0])
        boxes(fx, S["fx"], N_FX)
        boxes(gl, S["glow"], N_GL)
        boxes(met, S["met"], N_MET)
        Pb, Rb, Cb = (np.zeros((N_BALL, 3), np.float32) for _ in range(3))
        Sb, Kb = np.zeros(N_BALL, np.float32), np.zeros(N_BALL, np.float32)
        for k, (kind, p, dia, r, c) in enumerate(S["ball"][:N_BALL]):
            Pb[k], Sb[k], Rb[k], Cb[k], Kb[k] = p, dia, r, c, kind
        K.set_points(balls, Pb, scale=Sb, rot=Rb, col=Cb, pose=Kb)

    ctx.on_frame(upd)
