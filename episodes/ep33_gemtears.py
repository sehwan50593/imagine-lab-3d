"""EP33 만약에 눈물이 보석이 된다면? (19편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷, 한 줄 안에서 컷이 둘로 나뉘는 곳은 영화관 한 줄):
밤 방 창가 책상에서 하은의 눈물이 톡 떨어져 하늘색 보석으로 굳고 반짝(훅, 얼굴은 제목 아래) → 같은 책상 옆모습으로 보석이 또 굳음
→ 영화관(뒤에서 큰 깨진 하트 화면+실루엣 → 앞에서 우는 얼굴, 발치마다 보석이 소복) → 시장 양파 가게(주인 어깨 너머로 눈물 줄)
→ 보석 가게 보석 산 → 가격표 숫자가 뚝뚝 하락(블록 숫자) → 공원 벤치에서 폰(▶) 보며 우는 사람들 → 서로 어깨를 감싸고 토닥이는 어른들
→ 보석 가게 주인이 분홍 보석을 들고 '?' → 반전: 슬픈 친구는 파란 보석, 웃다 우는 친구는 분홍 보석 → 눈물 한 방울 클로즈업(물방울이 책상에 톡, 물결, 보석은 안 생김)
→ 울고 난 뒤 편안한 얼굴(가벼운 반짝이 두둥실) → 저녁 식탁, 늘 웃기만 하는 엄마(발치에 보석 없음) → 하은이 케이크를 들고 옴
→ 엄마 눈에서 분홍 보석이 톡 → 분홍·파랑 보석 비교 클로즈업(분홍이 더 반짝) → 목걸이 만들기(고리가 이어지고 분홍 보석이 달림)
→ 목걸이를 건 하은, 책상 위 파란·분홍 보석, 시청자에게 질문.
근거(설명란): 눈물은 대부분 물이고 소량의 염분·단백질·지질 등이 섞여 있다(안과·생리학에서 흔히 쓰는 설명. 정확한 %는 자막·내레이션에
쓰지 않고 '대부분은 물'로만 적음). 울고 난 뒤 기분이 나아졌다고 느끼는 사람이 많지만 사람·상황마다 다르다고 알려져 있어,
이 편은 '울고 나면 마음이 가벼워지죠' 정도의 일상 경험 표현만 쓴다. 눈물이 보석이 된다는 설정과 색 구분, 그 밖의 장면은
모두 지어낸 이야기입니다.
특수효과: 보석 = 45도 돌린 네모(마름모) 여러 장을 엇갈려 세운 원형 하나(발광, 앞면에 밝은 결, 색은 인스턴스 'col': 슬픔=파랑·기쁨=분홍)를
instancer_multi 점 하나로 두고, 눈물 방울(발광 물방울 원형) → 바닥에 톡 → 보석이 easeOutBack으로 튀어나오며 돌고 + 튀는 물방울 + 퍼지는 빛 고리
+ 8방향 반짝이(발광 십자 원형, 카메라 쪽으로 돌려 세움). 보석 산·발치 보석 = 같은 원형을 층층이 쌓은 배치(위층이 차례로 솟음),
가격표 = 5x7 도트 숫자(숫자·'원'·화살표 원형)가 몇 번 뚝뚝 줄어듦, 간판·화면 = Noto Sans KR(OFL)을 16x16으로 줄인 비트맵(GLYPH, ep32와 같은 방식)과
도트 그림. 보석 근처에 파랑/분홍 점광원 둘이 따라다니며 얼굴을 물들임. 울상 = 처진 눈썹·내려간 입꼬리·볼 눈물 자국(발광 상자),
어깨동무 토닥이 = 팔을 옆으로 벌린 자세 둘을 번갈아. 목걸이 = 금빛 상자 사슬이 양쪽에서 차례로 이어짐.
"""
import json
import math
from pathlib import Path

import numpy as np

from engine import voxel as X
from engine.common import clamp, ramp

STYLE = "pixe"
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.3, 0.32, 1.6)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"room": (0, 0), "cinema": (300, 0), "market": (600, 0), "jewel": (900, 0), "park": (1200, 0), "home": (1500, 0)}
NAMES = ("hook", "rule", "cinema", "onion", "jewel", "price", "videos", "adults", "strange", "colors", "water", "lighter",
         "momsmile", "cake", "momgem", "bright", "necklace", "ask")
IX = {n: k for k, n in enumerate(NAMES)}

# 하은 방 (밤, 창가 책상): 책상 가운데 x, 하은 앉는 자리
RX, HA_Y = 0.6, 1.52
DESK_Z = 0.74
# 가운데 위치 (x, y)에 눈물이 떨어지는 책상 위 자리
LAND_Y = 1.19

# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동])
# cuts: 한 줄 안의 짧은 연속 컷 [(끝 u, shot), ...]   shift: 렌즈 세로 이동(센서 높이 비율, +면 화면 속 물체가 아래로)
LINES = [
    dict(say="만약에 눈물이 보석이 된다면 어떻게 될까요?", gap=0.95,
         shot=("room", (RX, 1.30, 1.27), -90, 6, 2.45, 30, 0.9, 4, 0.10)),
    dict(say="슬퍼서 울면, 눈물이 보석으로 굳어요", gap=0.5,
         shot=("room", (0.72, 1.12, 1.02), -58, 6, 2.6, 30, 0.92, -8, 0.0)),
    dict(say="슬픈 영화관은 매일 만석이었고", gap=0.5,
         shot=("cinema", (0.0, 0.5, 0.7), -118, 18, 5.0, 20, 0.92, 6),
         cuts=[(0.4, ("cinema", (0.0, 1.0, 2.2), 84, 6, 5.0, 22, 0.95, 5)),
               (1.0, ("cinema", (0.0, 0.5, 0.7), -118, 18, 5.0, 20, 0.92, 6))]),
    dict(say="양파 가게 앞엔 줄이 길게 늘어섰죠", gap=0.5,
         shot=("market", (0.0, -2.8, 1.0), 92, 16, 6.6, 20, 0.95, -5)),
    dict(say="보석 가게엔 보석 산이 생겼지만", gap=0.5,
         shot=("jewel", (-0.4, -0.3, 0.95), -92, 8, 4.4, 22, 0.94, 4)),
    dict(say="너무 흔해져서 값이 뚝 떨어졌어요", gap=0.5,
         shot=("jewel", (0.3, 0.1, 1.25), -98, 5, 3.4, 26, 0.93, 4)),
    dict(say="사람들은 일부러 슬픈 영상을 찾아봤고", gap=0.5,
         shot=("park", (0.0, 2.0, 0.85), -90, 6, 4.4, 17, 0.95, 4)),
    dict(say="참아 왔던 어른들도 마음껏 울었어요", gap=0.5,
         shot=("park", (0.0, 0.3, 1.0), -90, 6, 4.6, 18, 0.95, -4)),
    dict(say="그런데 이상한 일이 생겼어요", gap=0.7,
         shot=("jewel", (-1.0, 0.9, 1.3), -92, 6, 3.0, 26, 0.92, 4)),
    dict(say="슬프면 파란 보석, 기쁘면 분홍 보석", gap=0.6,
         shot=("park", (1.3, 2.0, 0.85), -90, 6, 3.8, 26, 0.94, 3)),
    dict(say="원래 눈물의 대부분은 물이에요", gap=0.5,
         shot=("room", (0.66, 1.15, 0.98), -85, 8, 1.6, 32, 0.92, 3)),
    dict(say="그래도 울고 나면 마음이 가벼워지죠", gap=0.55,
         shot=("room", (RX, 1.35, 1.3), -90, 4, 2.2, 28, 1.1, -3)),
    dict(say="하지만 엄마는 하은 앞에선 늘 웃었죠", gap=0.5,
         shot=("home", (0.0, 1.4, 1.2), -90, 6, 3.6, 24, 0.92, 4)),
    dict(say="하은이 첫 월급으로 케이크를 샀어요", gap=0.5,
         shot=("home", (0.2, 1.2, 1.15), -90, 6, 3.8, 22, 0.94, 3)),
    dict(say="엄마 눈에서 분홍 보석이 톡 떨어졌죠", gap=0.5,
         shot=("home", (-0.35, 1.25, 1.0), -90, 6, 2.3, 28, 0.92, 3)),
    dict(say="가장 반짝이는 건 기쁨의 눈물이었죠", gap=0.5,
         shot=("home", (-0.35, 1.15, 0.95), -88, 8, 1.7, 26, 0.92, 5)),
    dict(say="하은은 그 보석으로 목걸이를 만들었죠", gap=0.6,
         shot=("room", (0.6, 0.62, 0.8), -90, 32, 1.6, 28, 0.94, 4)),
    dict(say="마지막으로 운 날 어떤 눈물이었나요?",
         shot=("room", (RX, 1.3, 1.2), -90, 5, 2.2, 28, 1.3, 0)),
]
assert len(LINES) == len(NAMES)
for _ln in LINES[1:]:
    assert len(_ln["say"]) <= 20, (_ln["say"], len(_ln["say"]))
TITLE = [("만약에", "white"), ("눈물이", "white"), ("보석이 된다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = IX["colors"]          # '슬프면 파란 보석, 기쁘면 분홍 보석' 줄 (뒤이어 물 한 줄이 사실)

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep33_gemtears" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 54.0, "lines": [[0.3 + 2.9 * i, 2.9 * i + 2.9, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep33", "title": "만약에 눈물이 보석이 된다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "Ab", "mode": "major", "bpm": 78, "seed": 331, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.16, "bloom_thr": 1.3, "vignette": 0.16}

HA_SH, HA_PA = (0.50, 0.78, 0.96), (0.15, 0.18, 0.30)        # 주인공 하은: 하늘색 셔츠·긴 머리·남색 바지
MO_SH, MO_PA = (0.96, 0.62, 0.74), (0.35, 0.28, 0.20)        # 엄마: 분홍 셔츠·긴 머리
OW_SH, OW_PA = (0.28, 0.66, 0.34), (0.35, 0.28, 0.20)        # 양파 가게 주인: 초록
JW_SH, JW_PA = (0.24, 0.20, 0.34), (0.15, 0.15, 0.18)        # 보석 가게 주인: 짙은 보라 조끼
EX_SH = [(0.85, 0.30, 0.28), (0.35, 0.65, 0.40), (0.92, 0.92, 0.90), (0.30, 0.30, 0.34), (0.95, 0.55, 0.25),
         (0.25, 0.45, 0.80), (0.80, 0.55, 0.65), (0.95, 0.80, 0.35), (0.55, 0.38, 0.70)]   # 엑스트라 (하늘색·분홍·초록 피함)
SUIT = [(0.22, 0.24, 0.30), (0.30, 0.32, 0.38), (0.18, 0.22, 0.34), (0.38, 0.30, 0.28)]    # 어른들 양복·셔츠

GEM_B = (0.015, 0.14, 1.0)        # 슬픔: 파랑 (선형 발광 색)
GEM_P = (1.0, 0.07, 0.34)         # 기쁨: 분홍
TEAR_C = (0.30, 0.62, 0.95)       # 눈물 방울 (연한 하늘색 발광)


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


# ───────────────────────── 하늘 · 빛 ─────────────────────────
NIGHT_LINES = (IX["hook"], IX["rule"], IX["water"], IX["lighter"], IX["necklace"], IX["ask"])    # 밤 방
DUSK_LINES = (IX["momsmile"], IX["cake"], IX["momgem"], IX["bright"])                              # 저녁 식탁


def sky(t):
    i = line_at(t)
    if i in NIGHT_LINES:
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0
    if i in DUSK_LINES:
        return (0.20, 0.17, 0.42), (0.98, 0.58, 0.38), 0.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


DAY = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})


def env(i, tl, du):
    """줄별 햇빛·주변광 + 움직이는 조명 {이름: 세기}."""
    if i in NIGHT_LINES:                                       # 밤 방 (불은 켜 둠)
        return dict(DAY, sun=0.0, amb=0.15, amb_col=(0.52, 0.54, 0.76))
    if i == IX["cinema"]:                                      # 어두운 극장: 화면 빛만
        return dict(DAY, sun=0.0, amb=0.21, amb_col=(0.50, 0.55, 0.80))
    if i in DUSK_LINES:                                        # 따뜻한 저녁 식탁
        return dict(DAY, sun=1.8, sun_col=(1.0, 0.72, 0.50), sun_rot=(70, 0, 38), amb=0.26, amb_col=(0.70, 0.62, 0.76))
    return DAY


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def cut_at(i, u):
    """줄 i의 지금 컷: (shot, 그 컷 안 진행도)."""
    cuts = LINES[i].get("cuts")
    if not cuts:
        return LINES[i]["shot"], u
    u0 = 0.0
    for ue, sh in cuts:
        if u <= ue or (ue, sh) == cuts[-1]:
            return sh, clamp((u - u0) / max(ue - u0, 1e-3))
        u0 = ue


def cam_pose(shot, u):
    """컷 진행도 u에서 카메라: dict(set, tgt, az, el, dist, lens, loc, shift) — 월드 좌표. CamRig.set과 같은 규칙."""
    st_, tg, az, el, dist, lens, push, daz = shot[:8]
    shift = shot[8] if len(shot) > 8 else 0.0
    o = OFF[st_]
    tgt = (tg[0] + o[0], tg[1] + o[1], tg[2])
    a, e, dd = az + daz * u, math.radians(el), dist * (1 + (push - 1) * u)
    loc = (tgt[0] + math.cos(e) * math.cos(math.radians(a)) * dd, tgt[1] + math.cos(e) * math.sin(math.radians(a)) * dd,
           tgt[2] + math.sin(e) * dd)
    return dict(set=st_, tgt=tgt, az=a, el=el, dist=dd, lens=lens, loc=loc, shift=shift)


def cam_axes(az, el):
    """카메라의 오른쪽·위쪽 단위벡터."""
    a, e = math.radians(az), math.radians(el)
    return (-math.sin(a), math.cos(a), 0.0), (-math.cos(a) * math.sin(e), -math.sin(a) * math.sin(e), math.cos(e))


# ───────────────────────── 도트 글자 (한글 16x16 · 숫자 5x7) ─────────────────────────
# 도트 글자 16x16: 한 줄(가로 16칸)을 16진 4자리로, 맨 윗줄부터 16줄 이어 붙임(왼쪽 칸 = 가장 높은 비트).
# 만든 법(새 낱말이 필요하면 같은 방식으로): assets/fonts/NotoSansKR-VF.ttf(OFL)를 굵기 620으로 크게 그려 글자 경계 상자를
# 16칸 격자 가운데에 꽉 차게(0.94) 줄이고, 칸 평균이 0.40 이상이면 켬. 숫자·기호는 손으로 그림.
GLYPH = {
    "눈": "10001800180018001ff81ffc00007ffe7ffe018001803980380038003ffc1ff8",
    "물": "1ff81ff8181818181ff800007ffe7ffe01803ff81ff81ff83ff838003ffc1ff8",
    "보": "0000300c300c381c3ffc3ffc300c300c3ffc3ffc018001800180ffff7ffe0000",
    "석": "0004060c060c063c077c0f0c1f8c39ec304c00040ffc0ffc000c000c000c0004",
    "양": "00180e183f1e719e61986198739e3f180c1800000ff01c3818181c380ff003c0",
    "파": "001800187fd83f981b181b181b1e1b1e1b181b187fd87fd80018001800180018",
    "원": "000c0f8c1fcc38cc18cc1f8c060c7fec7fec077c077c1e0c18001c001ffe0ffc",
}
FONT57 = {
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
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
}


def _glyph_rows(c):
    """글자 하나 → 16줄 문자열('#'=칸 켬), 비어 있는 좌우 열은 잘라 냄."""
    hx = GLYPH[c]
    rows = [format(int(hx[k * 4:k * 4 + 4], 16), "016b") for k in range(16)]
    on = [x for x in range(16) if any(r[x] == "1" for r in rows)]
    return [r[min(on):max(on) + 1].replace("1", "#").replace("0", ".") for r in rows]


def _text_grid(txt, ch="#", mirror=False):
    """글 → 16줄 문자열(켜진 칸 = ch). 글자 사이 한 칸, 띄어쓰기 다섯 칸. mirror=True면 좌우를 뒤집음(뒷면에서 읽히게)."""
    parts = []
    for c in txt:
        parts.append(["....."] * 16 if c == " " else _glyph_rows(c))
        parts.append(["."] * 16)
    rows = ["".join(p[r] for p in parts[:-1]) for r in range(16)]
    if mirror:
        rows = [r[::-1] for r in rows]
    return [r.replace("#", ch) for r in rows]


def _digit_rows(c):
    """숫자 한 글자 → 7줄 문자열('#'=칸 켬)."""
    return [r.replace("1", "#").replace("0", ".") for r in FONT57[c]]


def _runs(rows):
    """그림 → [(줄, 시작 칸, 끝 칸)] 같은 글자가 가로로 이어진 칸을 하나로."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] == ".":
                c += 1
                continue
            c1 = c
            while c1 + 1 < len(row) and row[c1 + 1] == row[c]:
                c1 += 1
            out.append((r, c, c1))
            c = c1 + 1
    return out


def pop(tau, dur=0.30, over=3.0):
    """톡 튀어나오는 크기: 0 → 살짝 커졌다 → 1 (easeOutBack). tau<0이면 0."""
    if tau <= 0:
        return 0.0
    if tau >= dur:
        return 1.0
    x = tau / dur - 1.0
    return 1.0 + (over + 1.0) * x ** 3 + over * x ** 2


# ───────────────────────── 캐릭터 자세 (표준 자세 위에 팔·고개·눈썹·입·눈만 바꾼 원형) ─────────────────────────
SITS = ("sit", "sit_phone", "sit_conf")
# base = 바탕 자세, arms = ((오른팔 앞뒤, 옆), (왼팔 앞뒤, 옆)) 어깨 회전각(앞뒤: 음수 = 앞으로 듦, 옆: 오른팔은 +가 몸 쪽·왼팔은 +가 바깥),
# mouth = open/smile/frown, brow = sad(처진 눈썹), sleep = 눈 감음, head = 고개 숙임(+)/젖힘(−), hroll = 고개 기울임
# (phone 바탕은 팔·고개를 바꾸지 않음: 폰 상자가 팔 조각 뒤에 붙어 있음)
KINDS = {
    "cry_sit": dict(base="sit", mouth="frown", brow="sad", head=0.10),
    "cry_sit_h": dict(base="sit", mouth="frown", brow="sad", head=0.24),
    "cry_sit_f": dict(base="sit", arms=((-2.1, 0.5), (-0.6, 0.0)), mouth="frown", brow="sad", head=0.12),
    "cry_sit_g": dict(base="sit", arms=((-0.6, 0.0), (-2.1, -0.5)), mouth="frown", brow="sad", head=0.12),
    "cry_stand": dict(base="stand", mouth="frown", brow="sad", head=0.10),
    "cry_face": dict(base="stand", arms=((-2.1, 0.5), (0.0, 0.0)), mouth="frown", brow="sad", head=0.10),
    "cry_onion": dict(base="stand", arms=((-1.9, 0.0), (0.0, 0.0)), mouth="frown", brow="sad", head=0.08),
    "cry_phone": dict(base="phone", mouth="frown", brow="sad"),
    "cry_sitphone": dict(base="sit_phone", mouth="frown", brow="sad"),
    "show_sit": dict(base="sit", arms=((-1.25, 0.0), (-0.6, 0.0)), mouth="frown", brow="sad", head=0.10),
    "hugA": dict(base="stand", arms=((0.0, 0.0), (0.0, 1.30)), mouth="frown", brow="sad", head=0.14, hroll=-0.12),
    "hugA2": dict(base="stand", arms=((0.0, 0.0), (0.0, 1.10)), mouth="frown", brow="sad", head=0.14, hroll=-0.12),
    "hugB": dict(base="stand", arms=((0.0, -1.30), (0.0, 0.0)), mouth="frown", brow="sad", head=0.14, hroll=0.12),
    "hugB2": dict(base="stand", arms=((0.0, -1.10), (0.0, 0.0)), mouth="frown", brow="sad", head=0.14, hroll=0.12),
    "smile": dict(base="stand", mouth="smile"),
    "sit_smile": dict(base="sit", mouth="smile"),
    "hold_smile": dict(base="stand", arms=((-1.3, 0.0), (-1.3, 0.0)), mouth="smile"),
    "hw_a": dict(base="walk_a", arms=((-1.3, 0.0), (-1.3, 0.0)), mouth="smile"),
    "hw_b": dict(base="walk_b", arms=((-1.3, 0.0), (-1.3, 0.0)), mouth="smile"),
    "sit_relax": dict(base="sit", sleep=True, mouth="smile", hroll=0.10),
    "sit_joy": dict(base="sit", arms=((-1.85, 0.70), (-1.85, -0.78)), mouth="smile", head=0.06),
    "sit_wow": dict(base="sit", mouth="open", hroll=0.06),
    "sit_laugh": dict(base="sit", mouth="open", sleep=True, hroll=0.10),
    "wonder": dict(base="stand", arms=((-1.5, 0.0), (0.0, 0.0)), mouth="open"),
    "owner_sad": dict(base="stand", mouth="frown", brow="sad", head=0.12),
}
ARMS = {"stand": (0.0, 0.0), "sit": (-0.6, -0.6), "sit_phone": (-1.05, -0.6), "sit_conf": (-2.75, -0.6),
        "phone": (-1.05, 0.0), "angry": (-2.5, -2.5), "confused": (-2.75, 0.05), "talk": (-0.9, 0.05),
        "walk_a": (0.35, -0.35), "walk_b": (-0.35, 0.35), "lie": (0.0, 0.0)}
ROLLS = {}
for _k, _sp in KINDS.items():
    ARMS[_k] = tuple(a[0] for a in _sp["arms"]) if _sp.get("arms") else ARMS[_sp["base"]]
    ROLLS[_k] = tuple(a[1] for a in _sp["arms"]) if _sp.get("arms") else (0.0, 0.0)


def base_of(pose):
    return KINDS[pose]["base"] if pose in KINDS else pose


def hip_of(pose):
    return 0.47 if base_of(pose) in SITS else 0.78


def _rot_x(bm, ang, pivot):
    """x축(앞) 둘레 회전 (y·z만 움직임)."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        y, z = p.co.y - pivot[1], p.co.z - pivot[2]
        p.co.y, p.co.z = pivot[1] + c * y - s * z, pivot[2] + s * y + c * z
    return bm


def _center(bm):
    n = len(bm.verts)
    return (sum(v.co.x for v in bm.verts) / n, sum(v.co.y for v in bm.verts) / n, sum(v.co.z for v in bm.verts) / n)


def _variant(name, lh):
    """voxel._person으로 만든 바탕 자세에서 팔·고개·눈썹·입·눈만 바꾼 [(bmesh, 재질)]."""
    from engine import bkit as K
    sp = KINDS[name]
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
        swap(lambda bm, mi: mi == 4 or (mi == 5 and _center(bm)[2] > hz), [(cube(0.232, sy, hz + 0.17, 0.02, 0.11, 0.025), 5)
                                                                            for sy in (-0.1, 0.1)])
    if sp.get("brow") == "sad":                                    # 처진 눈썹: 안쪽 끝이 올라가게 기울임
        for bm, mi in head:
            if mi == 3:
                cx, cy, cz = _center(bm)
                if abs(cx - 0.236) < 0.012 and 0.05 < abs(cy) < 0.15 and abs(cz - (hz + 0.285)) < 0.02:
                    _rot_x(bm, -0.42 if cy > 0 else 0.42, (0, cy, cz))

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
    for bm, _ in head:                                             # 고개: 목(어깨 위)을 축으로 숙이거나 젖히고 기울임
        if sp.get("hroll"):
            _rot_x(bm, sp["hroll"], (0, 0, hz))
        if sp.get("head"):
            X._rot_y(bm, sp["head"], (0, 0, hz))
    return list(legs) + [torso] + head + list(arms)


def _person_parts(pose, hair):
    """표준 자세면 voxel 원형, 새 자세면 _variant."""
    if pose in KINDS:
        return _variant(pose, bool(hair))
    return X._person(X.POSES[pose], bool(hair))


# ───────────────────────── 위치 도우미 ─────────────────────────
def rel(d, fwd, lat, up):
    """캐릭터 기준 (앞, 왼쪽, 위) → 세트 좌표. 크기 반영."""
    a = math.radians(d["yaw"])
    s = d["scale"]
    return (d["x"] + s * (fwd * math.cos(a) - lat * math.sin(a)), d["y"] + s * (fwd * math.sin(a) + lat * math.cos(a)),
            d["z"] + s * up)


def head_pt(d):
    """머리 꼭대기 한가운데(세트 좌표)."""
    return rel(d, 0.0, 0.0, hip_of(d["pose"]) + 1.04)


def face_pt(d):
    """얼굴 한가운데(세트 좌표)."""
    return rel(d, 0.22, 0.0, hip_of(d["pose"]) + 0.8)


def eye_pt(d, side):
    """side +1(캐릭터 왼쪽 눈)·−1 눈 아래쪽 끝(세트 좌표) — 눈물이 시작되는 곳."""
    return rel(d, 0.24, 0.1 * side, hip_of(d["pose"]) + 0.58 + 0.12)


def chin_pt(d, side):
    """턱 끝 앞쪽 (눈물이 뚝 떨어지는 곳)."""
    return rel(d, 0.26, 0.1 * side, hip_of(d["pose"]) + 0.56)


def hand_pt(d, side, reach=0.0):
    """side 'R'(캐릭터 오른손)·'L' 손 끝 근처 점 (옆으로 벌리는 롤 반영)."""
    ang = ARMS[d["pose"]][0 if side == "R" else 1]
    roll = ROLLS.get(d["pose"], (0.0, 0.0))[0 if side == "R" else 1]
    dd = 0.49 + reach
    sy = -0.34 if side == "R" else 0.34
    lat = sy + dd * math.sin(roll)              # 롤은 어깨에서 팔을 +y 쪽으로 기울임 (오른팔은 몸 쪽, 왼팔은 바깥)
    r = dd * math.cos(roll)
    return rel(d, -r * math.sin(ang), lat, hip_of(d["pose"]) + 0.54 - r * math.cos(ang))


# ───────────────────────── 세트 ─────────────────────────
DARK = (0.2, 0.2, 0.22)
WOODC = (0.62, 0.42, 0.25)


def _bed(v, x0, x1, y0, y1, blanket):
    """머리판이 +y 벽쪽인 침대. 상자마다 면이 어긋나게(같은 평면에 겹치면 그림자로 까맣게 나옴)."""
    v.box(x0, x1, y0, y1, 0, 0.32, WOODC)
    v.box(x0 + 0.03, x1 - 0.03, y0 + 0.03, y1 - 0.03, 0.32, 0.52, (0.92, 0.92, 0.90), jit=0.02)
    v.box(x0 + 0.05, x1 - 0.05, y0 + 0.05, y0 + 0.62 * (y1 - y0), 0.52, 0.6, blanket)
    v.box(x0 + 0.15, x1 - 0.15, y1 - 0.42, y1 - 0.08, 0.52, 0.64, (0.97, 0.97, 0.97), jit=0.01)
    v.box(x0 - 0.02, x1 + 0.02, y1 - 0.06, y1 + 0.02, 0, 1.0, (0.38, 0.25, 0.15))


def _book_shelf(v, x0, x1, y0, y1, h, rows):
    """벽(+x 쪽 벽이면 x1이 벽)에 붙은 책장: 칸마다 알록달록한 책 (앞 = 방 안쪽)."""
    cols = [(0.9, 0.3, 0.3), (0.3, 0.6, 0.9), (0.95, 0.8, 0.25), (0.35, 0.75, 0.45), (0.8, 0.5, 0.85), (0.95, 0.55, 0.2)]
    v.box(x0, x1, y0, y1, 0, 0.06, WOODC)
    step = (h - 0.06) / rows
    for r in range(rows + 1):
        v.box(x0, x1, y0, y1, 0.06 + r * step - (0.03 if r == rows else 0.0), 0.09 + r * step - (0.03 if r == rows else 0.0), WOODC)
    for r in range(rows):
        z = 0.09 + r * step
        y = y0 + 0.03
        while y < y1 - 0.12:
            w, hh = float(v.rs.uniform(0.05, 0.1)), float(v.rs.uniform(0.18, step - 0.06))
            v.box(x0 + 0.04, x1 - 0.04, y, y + w, z, z + hh, cols[int(v.rs.integers(len(cols)))], jit=0.06)
            y += w + 0.012


def _room(v):
    """하은의 방 (밤): 앞(-y)이 열린 방. 뒷벽 창(밤 도시 불빛) 앞에 책상, 책상 건너편에 하은이 앉음. 침대(왼쪽)·책장(오른쪽)."""
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    wb, ws = (0.90, 0.87, 0.86), (0.80, 0.85, 0.92)
    v.wall((-3, 2.5), (3, 2.5), 0, 2.8, wb, 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 2.8, ws, 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 2.8, ws, 0.25, face=1)
    v.window(-0.55, 1.75, 2.49, 1.0, 2.4, night=True, lights=26)
    cu = (0.90, 0.64, 0.70)
    v.box(-0.92, -0.64, 2.34, 2.45, 0.8, 2.64, cu)                          # 커튼
    v.box(1.83, 2.11, 2.34, 2.45, 0.8, 2.64, cu)
    v.box(-0.97, 2.16, 2.36, 2.40, 2.64, 2.70, (0.4, 0.28, 0.2))            # 커튼 봉
    v.box(-0.64, 1.84, 2.18, 2.48, 0.96, 1.012, (0.95, 0.95, 0.93))         # 창턱
    v.box(1.40, 1.70, 2.24, 2.44, 1.012, 1.10, (0.35, 0.6, 0.45))           # 창턱 화분
    v.box(1.36, 1.74, 2.2, 2.48, 1.10, 1.45, (0.25, 0.55, 0.25), jit=0.1)
    _bed(v, -2.85, -1.45, 0.4, 2.45, (0.45, 0.62, 0.90))
    v.floor(-0.8, 2.0, -1.3, 0.2, (0.82, 0.55, 0.58), 0.5, "check", z=0.012)  # 러그
    _book_shelf(v, 2.62, 2.97, 0.0, 1.9, 1.9, 4)
    v.box(-2.99, -2.97, -1.6, -0.4, 1.4, 2.2, (0.95, 0.75, 0.3), jit=0)       # 포스터
    v.box(-2.97, -2.96, -1.5, -0.5, 1.5, 2.1, (0.3, 0.6, 0.9), jit=0)
    v.box(-2.96, -2.95, -1.2, -0.8, 1.65, 1.95, (1.0, 0.95, 0.8), jit=0)
    # 책상 + 의자 + 책상 위 소품 (스탠드·휴지·공책·컵)
    X.table(v, RX, 0.8, 1.9, 1.0, DESK_Z, (0.84, 0.68, 0.46))
    X.chair(v, RX, HA_Y, -90, (0.35, 0.45, 0.70))
    v.box(-0.14, 0.02, 0.93, 1.09, DESK_Z, DESK_Z + 0.03, (0.3, 0.3, 0.32), jit=0)
    v.box(-0.07, -0.05, 0.99, 1.03, DESK_Z + 0.03, DESK_Z + 0.36, (0.3, 0.3, 0.32), jit=0)
    v.box(-0.19, 0.07, 0.9, 1.12, DESK_Z + 0.36, DESK_Z + 0.46, (1.0, 0.85, 0.6), jit=0, glow=True)
    v.box(1.06, 1.32, 0.52, 0.68, DESK_Z, DESK_Z + 0.1, (0.95, 0.96, 0.98))                  # 휴지 상자
    v.box(1.13, 1.23, 0.57, 0.62, DESK_Z + 0.1, DESK_Z + 0.19, (0.99, 0.99, 0.99), jit=0.01)
    v.box(0.05, 0.40, 0.42, 0.68, DESK_Z, DESK_Z + 0.025, (0.35, 0.55, 0.85))                 # 공책
    v.box(1.36, 1.5, 0.88, 1.02, DESK_Z, DESK_Z + 0.11, (0.97, 0.97, 0.95))                   # 컵
    v.light(RX, 0.2, 2.7, 120, (1.0, 0.88, 0.70), 0.5, "ep33_rm_ceil")
    v.light(RX + 0.2, -1.2, 2.0, 105, (1.0, 0.93, 0.85), 0.6, "ep33_rm_fill")
    v.light(-0.06, 1.0, 1.15, 25, (1.0, 0.78, 0.5), 0.3, "ep33_rm_lamp")
    v.light(1.0, 2.0, 1.8, 26, (0.55, 0.65, 1.0), 0.8, "ep33_rm_win")


# ── 영화관: 앞(-y) 벽이 큰 화면, 객석은 화면을 향해(-y) 계단식 세 줄. 카메라는 뒤(+y)나 화면 쪽 앞에서 찍음
CIN_Y = (0.0, 1.6, 3.2)              # 줄 y (줄 사이 1.6m, 계단 한 칸의 앞뒤 폭 ±0.8)
CIN_Z = (0.0, 0.3, 0.6)              # 줄 바닥 높이
CIN_X = (-2.25, -1.35, -0.45, 0.45, 1.35, 2.25)
HEART = ["..RRR...RRR..", ".RRRRR.RRRRR.", "RRRRRR.RRRRRR", "RRRRR.RRRRRRR", "RRRRRR.RRRRRR", ".RRRRR.RRRRR.",
         "..RRRR.RRRR..", "...RRR.RRR...", "....RR.RR....", ".....R.R.....", "......R......"]


def _pix(v, rows, pal, x0, z0, y, cell, depth=0.04):
    """문자 그림(rows)을 y 벽 앞(-y 쪽)에 발광 점으로 찍음. 맨 윗줄이 가장 위. 같은 색이 가로로 이어진 칸은 상자 하나."""
    n = len(rows)
    for r, c0, c1 in _runs(rows):
        ch = rows[r][c0]
        if ch in pal:
            z = z0 + (n - 1 - r) * cell
            v.box(x0 + c0 * cell, x0 + (c1 + 1) * cell, y - depth, y, z, z + cell, pal[ch], jit=0, glow=True)
    return None


def _seat(v, cx, y, z0):
    red = (0.66, 0.13, 0.20)
    v.box(cx - 0.21, cx + 0.21, y - 0.32, y + 0.2, z0 + 0.28, z0 + 0.36, red)
    v.box(cx - 0.21, cx + 0.21, y + 0.21, y + 0.29, z0 + 0.36, z0 + 1.0, red)
    v.box(cx - 0.06, cx + 0.06, y - 0.05, y + 0.15, z0, z0 + 0.28, (0.2, 0.2, 0.24))


def _cinema(v):
    v.floor(-4.5, 4.5, -6, 7, (0.30, 0.09, 0.14), 0.5, "check")
    wall = (0.16, 0.10, 0.20)
    v.wall((-4.5, -6), (-4.5, 7), 0, 4.6, wall, 0.5, face=-1)
    v.wall((4.5, -6), (4.5, 7), 0, 4.6, wall, 0.5, face=1)
    v.wall((-4.5, 7), (4.5, 7), 0, 4.6, wall, 0.5, face=-1)
    v.wall((-4.5, -6), (4.5, -6), 0, 4.6, (0.10, 0.08, 0.14), 0.5, face=1)
    v.floor(-4.6, 4.6, -6.1, 7.1, (0.07, 0.05, 0.09), 1.0, z=4.6)                  # 천장
    for k in (1, 2):                                                               # 계단식 바닥
        v.box(-4.48, 4.48, CIN_Y[k] - 0.8, CIN_Y[k] + 0.8, 0, CIN_Z[k], (0.34, 0.10, 0.16))
    for yk, zk in zip(CIN_Y, CIN_Z):
        for cx in CIN_X:
            _seat(v, cx, yk, zk)
    for yy in np.arange(-5.0, 6.6, 1.5):                                           # 옆벽 기둥(어두운 붉은 판)
        v.box(-4.49, -4.4, yy, yy + 0.7, 0.3, 3.4, (0.30, 0.09, 0.14))
        v.box(4.4, 4.49, yy, yy + 0.7, 0.3, 3.4, (0.30, 0.09, 0.14))
        v.box(-4.47, -4.42, yy + 0.2, yy + 0.5, 2.3, 2.36, (1.0, 0.82, 0.5), jit=0, glow=True)   # 벽등
        v.box(4.42, 4.47, yy + 0.2, yy + 0.5, 2.3, 2.36, (1.0, 0.82, 0.5), jit=0, glow=True)
    # 화면: 틀 + 남색 발광판 + 깨진 하트
    v.box(-3.4, 3.4, -5.99, -5.95, 0.75, 4.2, (0.04, 0.04, 0.06))
    v.box(-3.3, 3.3, -5.95, -5.93, 0.85, 4.1, (0.06, 0.10, 0.24), jit=0, glow=True)
    _pix(v, HEART, {"R": (1.0, 0.18, 0.32)}, -1.69, 1.0, -5.895, 0.26, depth=0.03)      # 관객 쪽(+y)에서 보이게 판 앞에 얹음
    # 뒷벽: 영사창 + 비상구등
    v.box(-0.4, 0.4, 6.95, 6.98, 3.5, 4.0, (0.9, 0.95, 1.0), jit=0, glow=True)
    v.box(-0.5, 0.5, 6.98, 6.995, 3.4, 4.1, (0.05, 0.05, 0.07), jit=0)
    v.box(4.41, 4.45, 5.2, 5.8, 3.4, 3.7, (0.25, 1.0, 0.5), jit=0, glow=True)
    # 조명: 화면 빛(차가운 흰색)이 객석 얼굴에 닿게 + 약한 따뜻한 위쪽 빛
    for k, (x, z) in enumerate(((-2.2, 2.6), (0.0, 2.9), (2.2, 2.6))):
        v.light(x, -3.5, z, 250, (0.80, 0.89, 1.0), 0.8, "ep33_cin_s%d" % k)
    v.light(0.0, 1.0, 3.9, 90, (1.0, 0.86, 0.70), 0.8, "ep33_cin_top")
    v.light(0.0, 4.6, 3.6, 70, (0.9, 0.9, 1.0), 0.8, "ep33_cin_back")


# ── 시장: 포장길 + 양파 가게(가운데 뒤, 손님 줄은 앞(-y)쪽으로) + 옆 가게 + 뒤 건물. 카메라는 주인 어깨 너머(+y)에서 -y를 봄
ONION_COLS = [(0.84, 0.62, 0.30), (0.78, 0.55, 0.26), (0.66, 0.27, 0.40), (0.88, 0.70, 0.36)]


def _vtext(v, chars, xc, ztop, y, cell, col, front=True, depth=0.03):
    """세로로 쌓은 도트 글자 간판 한 면: 앞(-y)에서 읽히면 front, 뒤(+y)에서 읽히면 mirror. 위 끝 ztop, 가운데 xc."""
    z = ztop
    for ch in chars:
        rows = _glyph_rows(ch) if front else [r[::-1] for r in _glyph_rows(ch)]
        w = len(rows[0])
        x0 = xc - w * cell / 2
        for r, c0, c1 in _runs(rows):
            zz = z - (r + 1) * cell
            if front:
                v.box(x0 + c0 * cell, x0 + (c1 + 1) * cell, y - depth, y, zz, zz + cell, col, jit=0, glow=True)
            else:
                v.box(x0 + c0 * cell, x0 + (c1 + 1) * cell, y, y + depth, zz, zz + cell, col, jit=0, glow=True)
        z -= 17 * cell


def _market(v):
    from engine import voxel as X_
    rs = v.rs
    v.floor(-10, 10, -10, 6, (0.68, 0.64, 0.58), 0.5, "check")
    # 양파 가게: 계산대 + 상자 셋 + 세로 간판
    v.box(-1.65, 1.65, 0.0, 0.9, 0, 0.95, (0.55, 0.38, 0.22))
    v.box(-1.7, 1.7, -0.05, 0.95, 0.95, 1.0, (0.88, 0.72, 0.50))
    for cx in (-1.0, 0.0, 1.0):
        v.box(cx - 0.38, cx + 0.38, 0.1, 0.8, 1.0, 1.16, (0.62, 0.42, 0.25))
        for i in range(5):
            for j in range(4):
                c = ONION_COLS[int(rs.integers(len(ONION_COLS)))]
                x, y = cx - 0.26 + 0.13 * i, 0.2 + 0.15 * j
                v.box(x - 0.055, x + 0.055, y - 0.055, y + 0.055, 1.16, 1.26, c, jit=0.05)
                v.box(x - 0.014, x + 0.014, y - 0.014, y + 0.014, 1.26, 1.3, (0.65, 0.8, 0.45), jit=0.05)
    for x in (-1.32, 1.32):                                                       # 손님 줄 위 현수막 (기둥 둘 + 판, 앞뒤 모두 글자)
        v.box(x - 0.04, x + 0.04, -0.74, -0.66, 0, 2.9, (0.5, 0.4, 0.3), jit=0)
    v.box(-1.3, 1.3, -0.72, -0.68, 2.3, 2.85, (0.97, 0.95, 0.88))
    for mirror, y0, y1 in ((False, -0.75, -0.72), (True, -0.68, -0.65)):
        rows = _text_grid("양파", "#", mirror=mirror)
        x0 = -len(rows[0]) * 0.028 / 2
        for r, c0, c1 in _runs(rows):
            z = 2.78 - (r + 1) * 0.028
            v.box(x0 + c0 * 0.028, x0 + (c1 + 1) * 0.028, y0, y1, z, z + 0.028, (0.15, 0.55, 0.25), jit=0, glow=True)
    # 옆 가게 둘 (과일 상자) + 뒤 건물
    for sx, cols in ((-5.2, [(0.9, 0.25, 0.2), (0.95, 0.6, 0.2), (0.4, 0.75, 0.3)]), (5.2, [(0.95, 0.8, 0.25), (0.9, 0.4, 0.5), (0.4, 0.7, 0.9)])):
        v.box(sx - 1.3, sx + 1.3, 0.0, 0.8, 0, 0.9, (0.58, 0.42, 0.28))
        for k in range(5):
            c = cols[k % 3]
            v.box(sx - 1.15 + 0.5 * k, sx - 0.7 + 0.5 * k, 0.1, 0.7, 0.9, 1.1, c, jit=0.06)
        for k in range(8):
            c = (0.95, 0.5, 0.3) if k % 2 == 0 else (0.97, 0.96, 0.92)
            v.box(sx - 1.4 + 0.35 * k, sx - 1.4 + 0.35 * (k + 1), -0.5, 1.2, 2.3, 2.36, c, jit=0.02, bottom=True)
        for x in (sx - 1.35, sx + 1.35):
            for y in (-0.45, 1.15):
                v.box(x - 0.04, x + 0.04, y - 0.04, y + 0.04, 0, 2.3, (0.5, 0.4, 0.3), jit=0)
    signs = [(0.95, 0.3, 0.3), (0.3, 0.8, 1.0), (1.0, 0.8, 0.2), (0.4, 1.0, 0.5), (1.0, 0.5, 0.85)]
    k = 0
    for x0, x1 in ((-16, -9), (-9, -2), (-2, 5), (5, 11), (11, 17)):
        X_.storefront(v, x0, x1, -10.0, 5.0, float(rs.uniform(9, 14)), signs[k % 5], face=1, lit=0.35)
        k += 1
    for x in (-8, 8):
        X_.tree(v, x, 3.0)


def _jewel(v):
    """보석 가게: 뒷벽 선반+'눈물보석' 간판, 긴 계산대(위에 보석 더미 둘 + 가격표), 계산대 앞 바닥에 보석 산 자리."""
    v.floor(-4, 4, -3, 3.2, (0.90, 0.90, 0.88), 0.5, "check")
    v.wall((-4, 3.2), (4, 3.2), 0, 3.0, (0.32, 0.28, 0.48), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3.2), 0, 3.0, (0.38, 0.34, 0.55), 0.5, face=-1)
    v.wall((4, -3), (4, 3.2), 0, 3.0, (0.38, 0.34, 0.55), 0.5, face=1)
    # 뒷벽 선반 셋 + 발광 쟁반(파랑 계열) + 간판
    blues = [(0.10, 0.35, 1.0), (0.20, 0.50, 1.0), (0.05, 0.25, 0.85)]
    for z in (0.95, 1.45, 1.95):
        v.box(-3.6, 3.6, 2.8, 3.15, z, z + 0.04, (0.62, 0.42, 0.25))
        for k, x in enumerate(np.arange(-3.3, 3.4, 0.85)):
            v.box(x - 0.27, x + 0.27, 2.86, 3.1, z + 0.04, z + 0.075, blues[(k + int(z * 3)) % 3], jit=0, glow=True)
    rows = _text_grid("눈물보석", "#")
    x0 = -len(rows[0]) * 0.04 / 2
    for r, c0, c1 in _runs(rows):
        z = 2.95 - (r + 1) * 0.04
        v.box(x0 + c0 * 0.04, x0 + (c1 + 1) * 0.04, 3.12, 3.16, z, z + 0.04, (0.90, 0.45, 0.05), jit=0, glow=True)
    # 계산대
    v.box(-3.0, 1.0, -0.1, 0.75, 0, 0.95, (0.30, 0.22, 0.18))
    v.box(-3.05, 1.05, -0.15, 0.8, 0.95, 1.0, (0.96, 0.94, 0.88))
    # 가격표 (계산대 오른쪽 끝): 받침 + 카드 + 빨간 윗띠. 숫자는 움직이는 소품
    v.box(0.18, 0.32, 0.0, 0.24, 1.0, 1.04, (0.25, 0.25, 0.3), jit=0)
    v.box(-0.3, 0.8, 0.1, 0.13, 1.04, 1.44, (0.99, 0.97, 0.92))
    v.box(-0.29, 0.79, 0.09, 0.125, 1.34, 1.46, (0.88, 0.2, 0.22))
    # 오른쪽 바닥: 보석 산 받침
    v.box(-1.8, 1.0, -2.3, -0.2, 0, 0.08, (0.38, 0.24, 0.42))
    for x in (-2.8, 0.2, 2.8):
        v.box(x - 0.6, x + 0.6, -0.1, 0.5, 2.95, 3.0, (1.0, 0.98, 0.95), jit=0, glow=True)
        v.light(x, 0.4, 2.7, 105, (1.0, 0.97, 0.92), 0.6, "ep33_jw_l%d" % int(x * 10))
    v.light(0.0, -1.8, 2.0, 95, (1.0, 0.97, 0.94), 0.6, "ep33_jw_fill")


def _bench(v, cx, cy):
    """벤치: 앉는 널 + 등받이(+y 쪽) + 다리. 앉은 사람은 -y를 봄."""
    wd = (0.62, 0.42, 0.25)
    v.box(cx - 0.8, cx + 0.8, cy - 0.22, cy + 0.2, 0.42, 0.47, wd)
    v.box(cx - 0.8, cx + 0.8, cy + 0.22, cy + 0.27, 0.47, 0.9, wd)
    for dx in (-0.7, 0.7):
        v.box(cx + dx - 0.04, cx + dx + 0.04, cy - 0.2, cy + 0.26, 0, 0.42, (0.3, 0.3, 0.32), jit=0)


def _park(v):
    from engine import voxel as X_
    rs = v.rs
    v.floor(-12, 12, -4, 9, (0.40, 0.64, 0.32), 0.5, "check")
    v.floor(-12, 12, -1.4, 0.5, (0.82, 0.74, 0.60), 0.5, "check", z=0.01)         # 길
    _bench(v, -1.3, 2.0)
    _bench(v, 1.3, 2.0)
    for x, y in ((-5.5, 5.0), (-2.0, 6.2), (1.5, 5.4), (5.0, 6.0), (8.5, 5.0), (-8.5, 6.0), (-4.5, 3.8)):
        X_.tree(v, x, y, float(rs.uniform(3.0, 3.8)))
    for x in (-3.4, 3.4):
        X_.street_lamp(v, x, 3.0, h=3.4, energy=1.0)
    for x in (-6.0, -0.2, 3.8, 7.0):                                              # 덤불
        v.box(x - 0.7, x + 0.7, 3.6, 4.3, 0, 0.7, (0.25, 0.55, 0.28), jit=0.08)
    signs = [(0.95, 0.3, 0.3), (0.3, 0.8, 1.0), (1.0, 0.8, 0.2), (0.4, 1.0, 0.5)]
    for k, (x0, x1) in enumerate(((-18, -8), (-8, 2), (2, 12), (12, 22))):
        X_.storefront(v, x0, x1, 11.0, 5.0, float(rs.uniform(9, 14)), signs[k % 4], face=-1, lit=0.35)


def _home(v):
    """저녁 거실 식탁: 뒷벽 노을 창(왼쪽), 가운데 식탁(흰 식탁보) + 의자, 위 펜던트등. 앞(-y)이 열림."""
    v.floor(-3.2, 3.2, -2.5, 2.5, (0.72, 0.54, 0.36), 0.25, "wood")
    v.wall((-3.2, 2.5), (3.2, 2.5), 0, 2.8, (0.96, 0.89, 0.80), 0.25, face=-1)
    v.wall((-3.2, -2.5), (-3.2, 2.5), 0, 2.8, (0.90, 0.82, 0.74), 0.25, face=-1)
    v.wall((3.2, -2.5), (3.2, 2.5), 0, 2.8, (0.90, 0.82, 0.74), 0.25, face=1)
    # 노을 창: 위 보라 · 가운데 분홍 · 아래 주황 띠 (발광) + 흰 창틀
    for z0, z1, c in ((1.0, 1.45, (0.90, 0.20, 0.03)), (1.45, 1.9, (0.85, 0.12, 0.22)), (1.9, 2.35, (0.30, 0.10, 0.75))):
        v.box(-1.4, 0.6, 2.47, 2.49, z0, z1, c, jit=0, glow=True)
    fr = (0.97, 0.96, 0.93)
    for x0, x1, z0, z1 in ((-1.46, 0.66, 0.94, 1.0), (-1.46, 0.66, 2.35, 2.41), (-1.46, -1.4, 1.0, 2.35), (0.6, 0.66, 1.0, 2.35),
                           (-0.43, -0.37, 1.0, 2.35)):
        v.box(x0, x1, 2.43, 2.49, z0, z1, fr)
    v.box(-1.7, -1.46, 2.34, 2.46, 0.9, 2.5, (0.92, 0.55, 0.50))                 # 커튼
    v.box(0.66, 0.9, 2.34, 2.46, 0.9, 2.5, (0.92, 0.55, 0.50))
    # 식탁 + 식탁보 + 의자
    X.table(v, 0.0, 0.8, 1.8, 1.0, 0.74, (0.82, 0.66, 0.45))
    v.box(-0.95, 0.95, 0.27, 1.33, 0.74, 0.765, (0.98, 0.97, 0.95), jit=0.01)
    X.chair(v, -0.5, 1.52, -90, (0.55, 0.38, 0.25))
    X.chair(v, 0.5, 1.52, -90, (0.55, 0.38, 0.25))
    X.chair(v, 1.25, 0.8, 180, (0.55, 0.38, 0.25))
    X.chair(v, -1.25, 0.8, 0, (0.55, 0.38, 0.25))
    # 펜던트등 + 벽 액자 + 선반
    v.box(-0.03, 0.03, 0.77, 0.83, 1.95, 2.8, (0.2, 0.2, 0.2), jit=0)
    v.box(-0.3, 0.3, 0.5, 1.1, 1.85, 1.95, (1.0, 0.85, 0.6), jit=0, glow=True)
    for x0, c in ((1.2, (0.95, 0.75, 0.3)), (1.9, (0.4, 0.65, 0.9)), (2.6, (0.9, 0.5, 0.6))):
        v.box(x0, x0 + 0.5, 2.46, 2.49, 1.5, 2.1, (0.97, 0.96, 0.93))
        v.box(x0 + 0.06, x0 + 0.44, 2.45, 2.46, 1.56, 2.04, c, jit=0)
    v.box(2.35, 3.0, 2.0, 2.45, 0, 0.9, (0.9, 0.9, 0.92))                         # 주방 수납장
    v.box(2.3, 3.05, 1.95, 2.49, 0.9, 0.95, (0.5, 0.52, 0.56))
    v.box(-3.15, -2.65, 0.4, 1.9, 0, 0.45, (0.55, 0.45, 0.6))                     # 왼쪽 소파
    v.box(-3.15, -2.9, 0.4, 1.9, 0.45, 1.0, (0.62, 0.52, 0.68))
    v.floor(-1.6, 1.6, -0.9, 0.2, (0.85, 0.58, 0.55), 0.5, "check", z=0.012)       # 러그
    v.box(-2.8, -2.4, -1.9, -1.5, 0, 0.45, (0.35, 0.6, 0.45))                    # 화분
    v.box(-2.85, -2.35, -1.95, -1.45, 0.45, 1.2, (0.25, 0.55, 0.25), jit=0.1)
    v.light(0.0, 0.8, 1.8, 135, (1.0, 0.82, 0.58), 0.3, "ep33_hm_pend")
    v.light(-0.6, 1.9, 1.5, 120, (1.0, 0.78, 0.65), 0.8, "ep33_hm_win")
    v.light(0.3, -1.4, 1.9, 95, (1.0, 0.92, 0.82), 0.6, "ep33_hm_fill")


def _sets():
    return (("room", _room), ("cinema", _cinema), ("market", _market), ("jewel", _jewel), ("park", _park), ("home", _home))


# ───────────────────────── 캐릭터 배치 · 움직임 ─────────────────────────
def st(set_, x, y, yaw, pose, z=0.0, **kw):
    """한 줄 안에서의 자리·자세. 선택 값: v 속도(m/s, 줄 시작부터) · stop 멈추는 τ(초) · pair 걷기 두 자세 · cad 걸음 주기 ·
    turn (τ0, τ1, 끝 yaw) · then (τ, 바뀐 자세) · alt (자세A, 자세B, 주기, 위상) 번갈아."""
    return dict(set=set_, x=x, y=y, z=z, yaw=yaw, pose=pose, **kw)


# 영화관 관객 자세 (골고루 우는 모습)
CIN_KINDS = ("cry_sit", "cry_sit_f", "cry_sit_h", "cry_sit_g", "cry_sit", "cry_sit_h")
# 시장 줄: (x, y) 앞사람부터
QUEUE = [(0.1, -0.55), (-0.7, -1.4), (0.7, -2.25), (-0.8, -3.1), (0.75, -3.95), (-0.85, -4.8), (0.8, -5.65)]


def cast():
    """[dict(name, hair, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    rs = np.random.default_rng(33)
    C = []
    L = IX

    def add(name, hair, shirt, pants, at, scale=1.0):
        C.append(dict(name=name, hair=hair, shirt=shirt, pants=pants, at=at, scale=scale))

    def extra(name, at, scale=1.0, hair=None, suit=False):
        sh = SUIT[int(rs.integers(len(SUIT)))] if suit else EX_SH[int(rs.integers(len(EX_SH)))]
        add(name, int(rs.random() < 0.5) if hair is None else hair, sh, X.PANTS[int(rs.integers(len(X.PANTS)))], at, scale)

    # ── 하은 (하늘색 셔츠 · 긴 머리)
    add("ha", 1, HA_SH, HA_PA, {
        L["hook"]: st("room", RX, HA_Y, -90, "cry_sit"),
        L["rule"]: st("room", RX, HA_Y, -90, "cry_sit", alt=("cry_sit", "cry_sit_f", 1.3, 0.0)),
        L["water"]: st("room", RX, HA_Y, -90, "cry_sit"),
        L["lighter"]: st("room", RX, HA_Y, -90, "sit_relax"),
        L["momsmile"]: st("home", 0.5, 1.52, -90, "sit"),
        L["cake"]: st("home", 2.35, 1.5, 180, "hold_smile", v=(-0.95, 0.0), stop=1.5, pair=("hw_a", "hw_b"), cad=0.3,
                      turn=(1.55, 1.9, 270), then=(2.4, "smile")),
        L["momgem"]: st("home", 0.925, 1.5, -90, "smile"),
        L["bright"]: st("home", 0.925, 1.5, -90, "smile"),
        L["ask"]: st("room", RX, HA_Y, -90, "sit_smile")})
    # ── 엄마 (분홍 셔츠 · 긴 머리)
    add("mo", 1, MO_SH, MO_PA, {
        L["momsmile"]: st("home", -0.5, 1.52, -90, "sit_smile"),
        L["cake"]: [(0.0, st("home", -0.5, 1.52, -90, "sit_smile")), (0.55, st("home", -0.5, 1.52, -90, "sit_wow")),
                    (0.8, st("home", -0.5, 1.52, -90, "sit_joy"))],
        L["momgem"]: st("home", -0.5, 1.52, -90, "sit_joy"),
        L["bright"]: st("home", -0.5, 1.52, -90, "sit_joy")})
    # ── 영화관: 세 줄 × 여섯 자리 가득 (모두 울고 있음)
    for k, (yk, zk) in enumerate(zip(CIN_Y, CIN_Z)):
        for j, cx in enumerate(CIN_X):
            kind = CIN_KINDS[(j + 2 * k) % len(CIN_KINDS)]
            alt = (kind, "cry_sit_f" if kind != "cry_sit_f" else "cry_sit", 1.0 + 0.25 * ((j + k) % 3), 0.31 * j)
            extra("cin%d%d" % (k, j), {L["cinema"]: st("cinema", cx, yk, -90, kind, z=zk, alt=alt)})
    # ── 시장: 주인(초록) + 줄 선 손님
    add("ow", 0, OW_SH, OW_PA, {L["onion"]: st("market", 0.95, -0.4, 90, "hold_smile")})
    for k, (x, y) in enumerate(QUEUE):
        kind = ("cry_onion", "cry_face", "cry_onion", "cry_stand")[k % 4]
        extra("cu%d" % k, {L["onion"]: st("market", x, y, 90, kind)})
    # ── 보석 가게 주인 (보라 조끼)
    add("jw", 0, JW_SH, JW_PA, {
        L["jewel"]: st("jewel", -0.5, 1.35, -90, "owner_sad"),
        L["price"]: st("jewel", -0.3, 1.35, -90, "owner_sad"),
        L["strange"]: st("jewel", -1.3, 1.35, -90, "wonder")})
    # ── 공원 L6: 벤치 둘에 앉아 폰 보는 넷 + 뒤에 선 셋
    for k, (x, hair) in enumerate(((-1.65, 0), (-0.95, 1), (0.95, 1), (1.65, 0))):
        extra("pb%d" % k, {L["videos"]: st("park", x, 2.0, -90, "cry_sitphone")}, hair=hair)
    for k, x in enumerate((-2.7, 0.05, 2.75)):
        extra("ps%d" % k, {L["videos"]: st("park", x, 3.1, -90, "cry_phone")})
    # ── 공원 L7: 어깨동무하고 토닥이는 어른 둘씩 셋 (양복 색)
    for k, (cx, cy) in enumerate(((-1.0, 0.1), (1.0, -0.05), (0.0, 2.2))):
        for s_, (dx, kinds) in enumerate(((-0.36, ("hugA", "hugA2")), (0.36, ("hugB", "hugB2")))):
            ph = 0.17 * (s_ + k)
            extra("ad%d%d" % (k, s_), {L["adults"]: st("park", cx + dx, cy, -90, kinds[0], alt=(kinds[0], kinds[1], 0.36, ph))},
                  suit=True, hair=(k + s_) % 2)
    # ── 공원 L9: 슬픈 친구(파란 보석) · 웃다 우는 친구(분홍 보석)
    add("f1", 0, (0.55, 0.40, 0.72), (0.15, 0.18, 0.30), {L["colors"]: st("park", 0.95, 2.0, -90, "cry_sit")})
    add("f2", 1, (0.95, 0.80, 0.35), (0.20, 0.20, 0.22), {L["colors"]: st("park", 1.65, 2.0, -90, "sit_laugh")})
    return C


_W = {}


def _poses_of(s):
    out = {s["pose"]}
    for k in ("pair", "alt"):
        if k in s:
            out |= set(s[k][:2])
    if "then" in s:
        out.add(s["then"][1])
    return out


def _world():
    """캐릭터 목록과 원형(자세·머리) 번호표 — 블렌더 없이 계산."""
    if not _W:
        C = cast()
        keys = set()
        for c in C:
            for a in c["at"].values():
                for s in ([x for _, x in a] if isinstance(a, list) else [a]):
                    for p in _poses_of(s):
                        keys.add((p, c["hair"]))
        keys = sorted(keys)
        _W.update(C=C, keys=keys, PI={k: n for n, k in enumerate(keys)})
    return _W


def state_of(c, i, u, tau, dur, t):
    """캐릭터 c의 줄 i, 진행도 u(τ초)에서의 자리·자세(세트 좌표) 또는 None(안 보임)."""
    a = c["at"].get(i)
    if a is None:
        return None
    if isinstance(a, list):                           # 한 줄 안에서 컷마다 자리가 바뀜
        us, a = [(us_, aa) for us_, aa in a if u >= us_ - 1e-6][-1]
        tau = tau - us * dur
    d = dict(a)
    vx, vy = a.get("v", (0.0, 0.0))
    tt = min(max(tau, 0.0), a.get("stop", 1e9))
    d["x"], d["y"] = a["x"] + vx * tt, a["y"] + vy * tt
    moving = (vx != 0.0 or vy != 0.0) and tau < a.get("stop", 1e9)
    tr = a.get("turn")
    if tr:
        d["yaw"] = a["yaw"] + (tr[2] - a["yaw"]) * ramp(tau, tr[0], tr[1])
    if "then" in a and tau >= a["then"][0]:
        d["pose"] = a["then"][1]
    al = a.get("alt")
    if al:
        d["pose"] = al[int((t + al[3]) / al[2]) % 2]
    if moving and "pair" in a:
        cad = a.get("cad", 0.28)
        d["pose"] = a["pair"][int(t / cad) % 2]
        d["z"] += 0.03 * abs(math.sin(math.pi * t / cad))
    d["scale"] = c["scale"]
    return d


# ───────────────────────── 소품·효과 (상자 F · 발광 상자 G · 보석/반짝이/물방울 GM · 도트 숫자 DG · 점광원 LT) ─────────────────────────
# 상자 = (중심, 크기, 회전(라디안), 색) — 세트 좌표.  GM = (위치, 크기 배율, 돎(라디안), 색, 종류)  DG = (위치, 배율, 돎, 번호)
GM_GEM, GM_STAR, GM_DROP = 0, 1, 2
STREAK_C = (0.10, 0.30, 0.55)           # 볼 눈물 자국 (발광)
TEAR_P = (0.62, 0.34, 0.50)             # 기쁨의 눈물 방울 (분홍빛)
STAR_B, STAR_P, STAR_W = (0.60, 0.82, 1.0), (1.0, 0.74, 0.88), (1.0, 0.97, 0.90)
GOLD = (0.95, 0.78, 0.30)


def _h(n):
    """결정적 의사난수 0~1."""
    return (math.sin(n * 12.9898 + 4.1414) * 43758.5453) % 1.0


def gem(p, s, rz, kind):
    return (p, s, rz, GEM_P if kind == "p" else GEM_B, GM_GEM)


def drop(p, s=1.0, col=TEAR_C):
    return (p, s, 0.0, col, GM_DROP)


def star(p, s, col=STAR_W, spin=0.0):
    return (p, s, spin, col, GM_STAR)


def twinkle(c, tl, cam, n=5, r=0.2, seed=0, col=STAR_W, size=0.07, rate=1.1, t0=0.0):
    """c 둘레(카메라 쪽을 보는 평면)에서 번갈아 반짝이는 십자 별 n개."""
    if tl < t0:
        return []
    right, up = cam_axes(cam["az"], cam["el"])
    out = []
    for k in range(n):
        a = 6.283 * ((k + 0.37 * seed) / n) + 0.5 * seed
        rr = r * (0.55 + 0.45 * _h(seed * 31 + k))
        ph = (tl * rate * (0.8 + 0.5 * _h(seed * 7 + k)) + _h(seed * 13 + k * 5)) % 1.0
        s = size * math.sin(math.pi * ph) ** 2
        if s > 0.004:
            ca, sa = math.cos(a) * rr, math.sin(a) * rr
            out.append(star((c[0] + right[0] * ca + up[0] * sa, c[1] + right[1] * ca + up[1] * sa, c[2] + right[2] * ca + up[2] * sa),
                            s, col, 0.4 * k))
    return out


def burst(c, tau, cam, n=7, r=0.28, life=0.75, col=STAR_B, size=0.09):
    """c에서 사방으로 튀는 반짝이 (tau = 터진 뒤 초)."""
    if tau <= 0 or tau > life:
        return []
    right, up = cam_axes(cam["az"], cam["el"])
    f = tau / life
    out = []
    for k in range(n):
        a = 6.283 * (k + 0.4) / n + 0.3 * (k % 2)
        rr = r * math.sqrt(f) * (0.65 + 0.35 * _h(k * 3.3))
        s = size * (1 - f) ** 0.7 * (0.7 + 0.5 * (k % 2))
        ca, sa = math.cos(a) * rr, math.sin(a) * rr
        out.append(star((c[0] + right[0] * ca + up[0] * sa, c[1] + right[1] * ca + up[1] * sa, c[2] + right[2] * ca + up[2] * sa),
                        s, col, a))
    return out


def splash(c, ta, n=5, col=TEAR_C):
    """바닥에 닿은 눈물이 톡 튀는 작은 물방울 (ta = 닿은 뒤 초, 0.4초)."""
    if ta <= 0 or ta > 0.4:
        return []
    out = []
    for k in range(n):
        a = 6.283 * (k + 0.3) / n
        v, vz = 0.28 + 0.1 * (k % 2), 1.5 + 0.5 * (k % 3)
        z = vz * ta - 4.9 * ta * ta
        if z < 0:
            continue
        out.append(drop((c[0] + math.cos(a) * v * ta, c[1] + math.sin(a) * v * ta, c[2] + 0.02 + z), 0.32 * (1 - ta / 0.4) + 0.08, col))
    return out


def fall_time(src, dst):
    """눈물 방울이 src에서 dst까지 떨어지는 데 걸리는 시간(초) — 실제보다 조금 느리게."""
    return max(0.26, 1.15 * math.sqrt(2 * max(src[2] - dst[2], 0.05) / 9.8))


def ring(c, ta, col, life=0.5, r0=0.05, r1=0.30):
    """닿은 자리(c)에서 바닥을 따라 퍼지는 얇은 빛 고리 (납작한 발광 상자 넷, ta = 닿은 뒤 초)."""
    if ta <= 0 or ta > life:
        return []
    f = ta / life
    rr, th = r0 + (r1 - r0) * math.sqrt(f), 0.016 * (1 - f) + 0.003
    out = []
    for sx, sy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        out.append(((c[0] + sx * rr, c[1] + sy * rr, c[2] + 0.012), (th if sx else 2 * rr + th, th if sy else 2 * rr + th, 0.006),
                    (0, 0, 0), col))
    return out


def tear_gem(src, dst, t0, tl, cam, kind="b", size=1.0, rz0=0.0, ft=None, G=None):
    """눈물 방울이 src에서 dst로 떨어져(톡) 보석으로 굳음 → (GM 목록, 점광원 세기 0~1). G를 주면 닿는 순간 빛 고리도 거기에 더함."""
    out, glow = [], 0.0
    tau = tl - t0
    if tau < 0:
        return out, glow
    ft = ft or fall_time(src, dst)
    h = max(src[2] - dst[2], 0.05)
    tc = TEAR_P if kind == "p" else TEAR_C
    if tau < ft:
        f = tau / ft
        out.append(drop((src[0] + (dst[0] - src[0]) * f, src[1] + (dst[1] - src[1]) * f, src[2] - h * f * f), 0.75 - 0.1 * f, tc))
        return out, 0.0
    ta = tau - ft
    s = pop(ta, 0.32, 3.2)
    out.append(gem(dst, size * s, rz0 + 1.8 * (1 - min(1.0, ta / 0.32)), kind))
    if G is not None:
        G += ring(dst, ta, (0.40, 0.70, 1.0) if kind == "b" else (1.0, 0.45, 0.75), 0.5, 0.06 * size, 0.18 * size + 0.12)
    col = STAR_P if kind == "p" else STAR_B
    out += burst((dst[0], dst[1], dst[2] + 0.07 * size), ta, cam, col=col, size=0.07 * size + 0.03, r=0.2 * size + 0.1)
    out += splash(dst, ta, 5, tc)
    glow = max(0.0, 1.0 - ta / 1.0)
    return out, glow


def heap(c, R, rings, s, kind, seed, tl=99.0, grow=None):
    """보석 산: 가운데 c, 바닥 반지름 R, 층 수 rings. 위로 갈수록 반지름·개수가 줄고, grow=(첫 튀어나옴 τ, 층 간격, 처음부터 있는 층 수)면 위층이 차례로 솟음."""
    out = []
    for r in range(rings):
        f = 1.0 - r / rings
        rr = R * f
        n = 1 if r == rings - 1 else max(3, int(round(2 * math.pi * rr / (0.16 * s * 1.1))))
        if r == rings - 1:
            rr = 0.0
        sc = 1.0
        if grow and r >= grow[2]:
            sc = pop(tl - (grow[0] + grow[1] * (r - grow[2])), 0.35, 3.0)
        if sc <= 0.0:
            continue
        for k in range(n):
            a = 2 * math.pi * k / n + 0.7 * r + 0.5 * _h(seed + r * 13 + k)
            rad = rr * (0.85 + 0.2 * _h(seed + k + r * 5))
            out.append(gem((c[0] + math.cos(a) * rad, c[1] + math.sin(a) * rad * 0.9, c[2] + r * 0.075 * s),
                           s * sc * (0.85 + 0.3 * _h(seed + k * 3 + r)), 6.28 * _h(seed + k + r * 2), kind))
    return out


def slots(d, n, seed, base=0.5, spread=0.5, lat=0.9, gs=1.0):
    """캐릭터 d 발치(앞쪽)에 보석을 놓을 자리 n개 → [(위치, 크기, 돎)]. gs = 크기 배율."""
    out = []
    for k in range(n):
        f = base + spread * _h(seed + k * 3.1)
        la = (_h(seed * 7 + k * 1.7) - 0.5) * lat
        out.append((rel(d, f, la, 0.0), gs * (0.8 + 0.3 * _h(seed + k)), 6.28 * _h(seed + k * 9)))
    return out


def streaks(d, col=STREAK_C):
    """볼을 타고 내리는 눈물 자국 (발광 상자 둘)."""
    s = d["scale"]
    hz = hip_of(d["pose"]) + 0.58
    return [(rel(d, 0.238, 0.1 * side, hz + 0.095), (0.012 * s, 0.024 * s, 0.085 * s), (0.0, 0.0, math.radians(d["yaw"])), col)
            for side in (-1, 1)]


def cry_char(d, tl, seed, kind="b", t0=0.15, n_static=2, new=True, cam=None, base=0.5, spread=0.5, lat=0.9, fromchin=True, gs=1.0):
    """우는 사람 한 명: 볼 눈물 자국 + 발치 보석(처음부터 있는 n_static개 + 이 줄 안에서 눈물 → 톡 → 굳는 1개)
    → (G, GM, 점광원 세기)."""
    G = streaks(d, STREAK_C if kind == "b" else (0.5, 0.25, 0.35))
    GM = []
    sl = slots(d, n_static + 1, seed, base, spread, lat, gs)
    for p, s, rz in sl[:n_static]:
        GM.append(gem(p, s, rz, kind))
    glow = 0.0
    if new:
        p, s, rz = sl[n_static]
        side = 1 if _h(seed) > 0.5 else -1
        src = (chin_pt(d, side) if fromchin else eye_pt(d, side))
        items, glow = tear_gem(src, p, t0 + 1.7 * _h(seed * 3.7), tl, cam, kind, s, rz)
        GM += items
    return G, GM, glow


def cake(c, s=1.0, tl=0.0, flame=True):
    """2단 케이크 (분홍 크림·딸기·초): c = 바닥 가운데. → (F, G)"""
    x, y, z = c
    F = [((x, y, z + 0.05 * s), (0.36 * s, 0.36 * s, 0.10 * s), (0, 0, 0), (0.97, 0.94, 0.88)),
         ((x, y, z + 0.11 * s), (0.375 * s, 0.375 * s, 0.025 * s), (0, 0, 0), (1.0, 0.72, 0.80)),
         ((x, y, z + 0.1675 * s), (0.24 * s, 0.24 * s, 0.09 * s), (0, 0, 0), (0.97, 0.94, 0.88)),
         ((x, y, z + 0.2275 * s), (0.255 * s, 0.255 * s, 0.025 * s), (0, 0, 0), (1.0, 0.72, 0.80))]
    for dx, dy in ((-0.07, -0.05), (0.07, -0.05), (0.0, 0.06)):
        F.append(((x + dx * s, y + dy * s, z + 0.265 * s), (0.05 * s, 0.05 * s, 0.05 * s), (0, 0, 0.5), (0.90, 0.15, 0.20)))
    F.append(((x, y, z + 0.31 * s), (0.02 * s, 0.02 * s, 0.1 * s), (0, 0, 0), (0.55, 0.75, 1.0)))
    G = []
    if flame:
        fs = (1.0 + 0.15 * math.sin(tl * 23.0)) * s
        G.append(((x, y, z + 0.385 * s), (0.036 * fs, 0.036 * fs, 0.05 * fs), (0, 0, 0), (1.0, 0.55, 0.12)))
    return F, G


def chain_pts(d, n=9):
    """목걸이 사슬: 몸통 앞을 U자로 감는 점 n개 + 펜던트 자리."""
    hz = hip_of(d["pose"]) + 0.58
    pts = []
    for k in range(n):
        f = -1 + 2 * k / (n - 1)
        pts.append(rel(d, 0.165, 0.17 * f, hz - 0.02 - 0.11 * (1 - f * f)))
    return pts, rel(d, 0.18, 0.0, hz - 0.185)


PLAY = ["#..", "##.", "###", "##.", "#.."]


def play_icon(c, cam, size=0.032, col=(0.75, 0.92, 1.0)):
    """'▶' 도트 그림(발광 정육면체 일곱)을 카메라 쪽 평면에 띄움 — 영상을 보는 중이라는 표시."""
    right, up = cam_axes(cam["az"], cam["el"])
    out = []
    for r, row in enumerate(PLAY):
        for q, ch in enumerate(row):
            if ch == "#":
                dx, dz = (q - 1) * size, (2 - r) * size
                out.append(((c[0] + right[0] * dx + up[0] * dz, c[1] + right[1] * dx + up[1] * dz, c[2] + right[2] * dx + up[2] * dz),
                            (size * 0.92,) * 3, (0, 0, 0), col))
    return out


def qmark(c, cam, size=0.045, bob=0.0, col=(1.0, 0.82, 0.92)):
    """'?' 도트 글자(발광 정육면체들)를 카메라 쪽 평면에 띄움."""
    right, up = cam_axes(cam["az"], cam["el"])
    out = []
    rows = _digit_rows("?")
    for r, row in enumerate(rows):
        for q, ch in enumerate(row):
            if ch == "#":
                dx, dz = (q - 2) * size, (3 - r) * size + bob
                out.append(((c[0] + right[0] * dx + up[0] * dz, c[1] + right[1] * dx + up[1] * dz, c[2] + right[2] * dx + up[2] * dz),
                            (size * 0.92,) * 3, (0, 0, 0), col))
    return out


# ── 도트 숫자 가격표 (왼쪽 아래가 원점인 글자 원형: 숫자 0~9, 원 = 10, 아래 화살표 = 11)
PRICES = [9800, 6400, 3900, 1700, 800, 300, 90]
TAG = (0.25, 0.10, 1.13)              # 가격표 카드 앞면 가운데 x · 앞면 y · 글자 바닥 z
DCELL = 0.024
WON_W = 13 * 0.0105


def _won_rows():
    return _glyph_rows("원")


def price_items(idx, tl, t_change):
    """가격표 글자 [(위치, 배율, 돎, 번호)]: 값이 바뀐 직후 0.18초 동안 살짝 커졌다 줄어듦."""
    txt = str(PRICES[idx])
    dw, gap = 5 * DCELL, 0.03
    total = 0.15 + 0.07 + len(txt) * dw + (len(txt) - 1) * gap + 0.07 + WON_W
    x = TAG[0] - total / 2
    bump = 1.0 + 0.18 * max(0.0, 1.0 - (tl - t_change) / 0.18) if tl >= t_change else 1.0
    out = [((x, TAG[1], TAG[2]), 1.0, 0.0, 11)]
    x += 0.15 + 0.07
    for ch in txt:
        out.append(((x, TAG[1], TAG[2]), bump, 0.0, int(ch)))
        x += dw + gap
    out.append(((x + 0.04, TAG[1], TAG[2]), 1.0, 0.0, 10))
    return out


# 책상 위 보석: (x, y, 크기, 돎). 앞의 둘은 훅 전에 이미 굳은 것, 나머지 넷은 앞 줄들에서 차례로 굳는 것
DESK_GEMS = [(0.12, 1.06, 0.9, 0.3), (0.30, 1.16, 0.8, 1.1)]
LANDS = [(0.70, LAND_Y, 1.35, 0.2), (0.50, LAND_Y, 1.35, 1.0), (0.88, 1.06, 1.35, 2.1), (0.58, 1.0, 1.35, 0.6), (0.76, 0.92, 1.35, 1.7)]
HOOK_TEARS = [(0.0, 1, 0), (1.55, -1, 1), (2.95, 1, 2)]               # (시작 τ, 어느 눈(+1 왼쪽), LANDS 번호)
RULE_TEARS = [(0.25, -1, 3), (1.55, 1, 4)]                           # (시작 τ, 어느 눈, LANDS 번호)
CARRY_END = (0.925, 0.98, 1.16)                                       # 하은이 식탁 앞에서 케이크를 든 자리
TABLE_CAKE = (0.15, 0.85, 0.765)
PINK_LAND = [(-0.38, 1.18, 1.2, 0.4, 0.3), (-0.64, 1.14, 1.2, 1.5, 1.4)]   # 엄마 눈물이 떨어지는 자리 (x, y, 크기, 돎, 시작 τ)
NECK = (0.6, 0.62)
MTN = (-0.4, -1.2, 0.08)                                              # 보석 가게 보석 산 가운데                                                    # 목걸이를 펼친 책상 위 자리 (가운데 x, y)


def _lt(pos, kind, power):
    return (pos, kind, power)


def _dishes(F):
    """식탁 위 접시·밥그릇."""
    for x, y, c in ((-0.72, 0.52, (0.85, 0.5, 0.3)), (-0.3, 0.46, (0.95, 0.95, 0.9)), (0.62, 0.5, (0.45, 0.7, 0.35)),
                    (0.75, 0.95, (0.9, 0.35, 0.3))):
        F.append(((x, y, 0.765 + 0.02), (0.17, 0.17, 0.04), (0, 0, 0), (0.97, 0.97, 0.95)))
        F.append(((x, y, 0.765 + 0.055), (0.12, 0.12, 0.03), (0, 0, 0), c))


def props(i, tl, dur, u, S, t, cam):
    """i번째 줄, 줄 시작 후 tl초, 진행도 u의 소품: (상자 F, 발광 상자 G, 보석·반짝이·물방울 GM, 도트 숫자 DG, 점광원 LT) — 세트 좌표."""
    F, G, GM, DG, LT = [], [], [], [], []
    L = IX
    if i in (L["hook"], L["rule"]):                                   # 밤 방: 하은의 눈물이 책상에 톡 → 하늘색 보석
        ha = S["ha"]
        G += streaks(ha)
        for x, y, s, r in DESK_GEMS:
            GM.append(gem((x, y, DESK_Z), s, r, "b"))
        if i == L["hook"]:
            ev = [(t0, eye_pt(ha, side), (LANDS[k][0], LANDS[k][1]), LANDS[k][2], LANDS[k][3]) for t0, side, k in HOOK_TEARS]
        else:
            for x, y, s, r in LANDS[:3]:
                GM.append(gem((x, y, DESK_Z), s, r, "b"))
            ev = [(t0, eye_pt(ha, side), (LANDS[k][0], LANDS[k][1]), LANDS[k][2], LANDS[k][3]) for t0, side, k in RULE_TEARS]
        last = None
        for t0, src, land, s, r in ev:
            items, g = tear_gem(src, (land[0], land[1], DESK_Z), t0, tl, cam, "b", s, r, G=G)
            GM += items
            if tl >= t0:
                last = (land, g)
        if last:
            (lx, ly), g = last
            LT.append(_lt((lx, ly - 0.15, DESK_Z + 0.3), "b", 3.0 + 7.0 * g))
        for k, (x, y, s, r) in enumerate(DESK_GEMS + LANDS[:3]):
            GM += twinkle((x, y, DESK_Z + 0.09), tl, cam, 3, 0.17, k + 1, STAR_B, 0.09, 1.1)
    elif i == L["cinema"]:                                            # 영화관: 객석 18명이 울고 발치마다 보석이 소복
        for k in range(3):
            for j in range(6):
                d = S.get("cin%d%d" % (k, j))
                if d is None:
                    continue
                g_, gm_, _ = cry_char(d, tl, 100 + 10 * k + j, "b", 0.1, 4 if k == 0 else 3, True, cam,
                                      *((0.62, 1.0, 1.0, True, 1.5) if k == 0 else (0.62, 0.14, 0.5, True, 1.3)))
                G += g_
                GM += gm_
        for k, (x, y, z) in enumerate(((-1.4, -0.9, 0.4), (0.9, -1.1, 0.4), (0.0, -0.7, 0.4), (-0.3, 0.7, 0.9), (1.8, 0.6, 0.9))):
            GM += twinkle((x, y, z), tl, cam, 3, 0.25, 50 + k, STAR_B, 0.09, 1.0)
    elif i == L["onion"]:                                             # 시장 양파 가게: 줄 선 손님들이 양파를 들고 울고, 발치마다 보석
        ow = S["ow"]
        hp = rel(ow, 0.5, 0.0, hip_of(ow["pose"]) + 0.38)
        F.append(((hp[0], hp[1], hp[2] + 0.07), (0.15, 0.15, 0.14), (0, 0, 0.3), (0.84, 0.62, 0.30)))
        F.append(((hp[0], hp[1], hp[2] + 0.17), (0.04, 0.04, 0.07), (0, 0, 0), (0.65, 0.8, 0.45)))
        for k in range(7):
            d = S["cu%d" % k]
            g_, gm_, _ = cry_char(d, tl, 200 + k, "b", 0.1 + 0.15 * (k % 3), 2, True, cam, 0.4, 0.5, 0.9, False, 1.5)
            G += g_
            GM += gm_
            if d["pose"] == "cry_onion":
                ph = hand_pt(d, "R", 0.0)
                F.append(((ph[0], ph[1], ph[2] + 0.06), (0.11, 0.11, 0.1), (0, 0, 0.5 * k), ONION_COLS[k % 4]))
                F.append(((ph[0], ph[1], ph[2] + 0.125), (0.03, 0.03, 0.04), (0, 0, 0), (0.65, 0.8, 0.45)))
        for k, (x, y) in enumerate(((0.0, -0.9), (-0.35, -2.5), (0.3, -4.2))):
            GM += twinkle((x, y, 0.55), tl, cam, 3, 0.3, 60 + k, STAR_B, 0.09, 1.0)
    elif i in (L["jewel"], L["price"], L["strange"]):                 # 보석 가게: 계산대 위 더미 둘 + 오른쪽 보석 산 + 가격표
        grow_a = (0.5, 0.4, 2) if i == L["jewel"] else None
        grow_c = (0.3, 0.35, 2) if i == L["jewel"] else None
        GM += heap((-1.9, 0.35, 1.0), 0.38, 3, 0.8, "b", 11, tl, grow_a)
        GM += heap((-0.8, 0.35, 1.0), 0.38, 3, 0.8, "b", 21, tl, grow_a)
        GM += heap(MTN, 1.1, 6, 1.5, "b", 31, tl, grow_c)
        if i == L["price"]:
            for k, (a, r_, s) in enumerate(((0.3, 0.55, 1.0), (0.9, 0.35, 1.2), (1.5, 0.7, 0.9), (2.1, 0.45, 1.1))):
                ang = 2.0 + 1.3 * k
                GM.append(gem((MTN[0] + r_ * math.cos(ang), MTN[1] + r_ * math.sin(ang) * 0.9, MTN[2] + 0.08 + 0.66 * (1.0 - r_ / 1.1)),
                              1.2 * s * pop(tl - a, 0.35, 3.0), 1.0 * k, "b"))
            idx = min(int(tl / 0.36), len(PRICES) - 1)
            DG += price_items(idx, tl, idx * 0.36)
        elif i == L["jewel"]:
            DG += price_items(0, tl, -9.0)
        for k, c in enumerate(((-1.9, 0.35, 1.35), (-0.8, 0.35, 1.35), (MTN[0], MTN[1], 1.0), (MTN[0] + 0.9, MTN[1] + 0.2, 0.5))):
            GM += twinkle(c, tl, cam, 3, 0.35, 70 + k, STAR_B, 0.1, 1.0)
        if i == L["strange"]:
            jw = S["jw"]
            for k, (x, y, z) in enumerate(((-2.0, 0.45, 1.3), (-1.8, 0.3, 1.25), (-0.85, 0.4, 1.3))):     # 파란 더미 사이 분홍 보석
                GM.append(gem((x, y, z), 0.8, 1.7 * k, "p"))
            hp = hand_pt(jw, "R", 0.06)
            gp = (hp[0], hp[1], hp[2] + 0.1)
            GM.append(gem(gp, 1.25 * pop(tl - 0.1, 0.35, 3.0), 1.3 * tl, "p"))
            GM += twinkle((gp[0], gp[1], gp[2] + 0.1), tl, cam, 5, 0.22, 3, STAR_P, 0.09, 1.3, 0.3)
            hd = head_pt(jw)
            if tl > 0.5:
                G += qmark((hd[0], hd[1] + 0.1, hd[2] + 0.38), cam, 0.045 * pop(tl - 0.5, 0.3, 3.0), 0.03 * math.sin(tl * 4.0))
            LT.append(_lt((gp[0], gp[1] - 0.2, gp[2] + 0.15), "p", 5.0 + 2.0 * math.sin(tl * 6.0)))
    elif i == L["videos"]:                                            # 공원 벤치: 폰으로 슬픈 영상을 보며 우는 사람들
        for k, name in enumerate(("pb0", "pb1", "pb2", "pb3", "ps0", "ps1", "ps2")):
            d = S[name]
            g_, gm_, _ = cry_char(d, tl, 300 + k, "b", 0.1 + 0.2 * (k % 3), 2, True, cam,
                                  *((0.62, 0.3, 0.6, True, 1.7) if k < 4 else (0.45, 0.5, 0.8, True, 1.7)))
            G += g_
            GM += gm_
            hd = head_pt(d)
            G += play_icon((hd[0], hd[1], hd[2] + 0.22 + 0.025 * math.sin(tl * 4.0 + k)), cam)
        for k, (x, y) in enumerate(((-1.3, 1.1), (1.3, 1.1), (0.0, 2.3))):
            GM += twinkle((x, y, 0.45), tl, cam, 3, 0.3, 80 + k, STAR_B, 0.1, 1.0)
    elif i == L["adults"]:                                            # 어깨동무하고 서로 토닥이는 어른들
        for k in range(3):
            for s_ in range(2):
                d = S["ad%d%d" % (k, s_)]
                g_, gm_, _ = cry_char(d, tl, 400 + 2 * k + s_, "b", 0.1 + 0.2 * ((k + s_) % 3), 2, True, cam, 0.42, 0.4, 0.5, True, 1.7)
                G += g_
                GM += gm_
        for k, (x, y) in enumerate(((-1.0, -0.5), (1.0, -0.6), (0.0, 1.6))):
            GM += twinkle((x, y, 0.5), tl, cam, 3, 0.35, 90 + k, STAR_B, 0.1, 1.0)
    elif i == L["colors"]:                                            # 반전: 슬프면 파란 보석, 기쁘면 분홍 보석
        f1, f2 = S["f1"], S["f2"]
        G += streaks(f1)
        G += streaks(f2, (0.55, 0.28, 0.40))
        ev = ((f1, "b", 0.3, (0.8, 0.1)), (f2, "p", 1.0, (0.8, -0.1)), (f1, "b", 1.8, (1.0, -0.15)), (f2, "p", 2.5, (1.0, 0.15)))
        glow = {"b": None, "p": None}
        for k, (d, kind, t0, (fw, lt)) in enumerate(ev):
            p = rel(d, fw, lt, 0.0)
            items, g = tear_gem(chin_pt(d, 1 if k % 2 == 0 else -1), p, t0, tl, cam, kind, 1.15, 0.9 * k, G=G)
            GM += items
            if tl >= t0:
                glow[kind] = (p, g)
        for kind, v in glow.items():
            if v:
                p, g = v
                LT.append(_lt((p[0], p[1] - 0.2, p[2] + 0.3), kind, 3.5 + 7.0 * g))
        for k, d in enumerate((f1, f2)):
            c = rel(d, 0.9, 0.0, 0.1)
            GM += twinkle(c, tl, cam, 4, 0.3, 110 + k, STAR_B if k == 0 else STAR_P, 0.09, 1.2, 0.8 + 0.7 * k)
    elif i == L["water"]:                                             # 눈물 한 방울 클로즈업: 물방울이 책상에 톡, 물결
        ha = S["ha"]
        G += streaks(ha)
        for x, y, s, r in DESK_GEMS:                                  # 클로즈업이라 책상 앞쪽은 비워 둠 (물방울이 잘 보이게)
            GM.append(gem((x, y, DESK_Z), s, r, "b"))
        for k, (t0, side, land) in enumerate(((0.25, 1, (0.74, 1.04)), (1.5, -1, (0.54, 1.04)))):
            tau = tl - t0
            src = chin_pt(ha, side)
            ft = 0.42
            if tau < 0:
                continue
            if tau < ft:
                f = tau / ft
                GM.append(drop((src[0] + (land[0] - src[0]) * f, src[1] + (land[1] - src[1]) * f, src[2] - (src[2] - DESK_Z - 0.03) * f * f),
                               1.1 * (1 - 0.15 * f), TEAR_C))
            else:
                ta = tau - ft
                F.append(((land[0], land[1], DESK_Z + 0.005), (0.15 * pop(ta, 0.3, 1.5), 0.15 * pop(ta, 0.3, 1.5), 0.012), (0, 0, 0),
                          (0.55, 0.78, 0.95)))
                GM += splash((land[0], land[1], DESK_Z), ta, 6, TEAR_C)
                for q, r0 in enumerate((0.0, 0.18)):
                    tr = ta - r0
                    if 0 < tr < 1.0:
                        rr, th = 0.07 + 0.22 * tr, 0.012 * (1 - tr)
                        for sx, sy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                            G.append(((land[0] + sx * rr, land[1] + sy * rr, DESK_Z + 0.01),
                                      (th if sx else 2 * rr + th, th if sy else 2 * rr + th, 0.006), (0, 0, 0), (0.45, 0.75, 1.0)))
        for k, (x, y, s, r) in enumerate(DESK_GEMS):
            GM += twinkle((x, y, DESK_Z + 0.07), tl, cam, 2, 0.14, 120 + k, STAR_B, 0.07, 1.0)
    elif i == L["lighter"]:                                           # 울고 난 뒤 편안한 얼굴 + 가벼운 반짝이가 두둥실
        ha = S["ha"]
        for x, y, s, r in DESK_GEMS + LANDS:
            GM.append(gem((x, y, DESK_Z), s, r, "b"))
        hd = head_pt(ha)
        for k in range(9):
            ph = (tl * 0.22 + _h(k * 5.1)) % 1.0
            sx = hd[0] + 0.55 * (_h(k * 2.3) - 0.5) * 2 + 0.05 * math.sin(tl * 2 + k)
            GM.append(star((sx, hd[1] - 0.15 + 0.2 * _h(k * 4.4), hd[2] - 0.2 + 1.0 * ph), 0.13 * math.sin(math.pi * ph) ** 0.7, STAR_W, 0.5 * k + tl))
        for k, (x, y, s, r) in enumerate(DESK_GEMS + LANDS):
            GM += twinkle((x, y, DESK_Z + 0.07), tl, cam, 2, 0.14, 130 + k, STAR_B, 0.05, 0.9)
    elif i == L["momsmile"]:                                          # 저녁 식탁: 늘 웃기만 하는 엄마 (발치에 보석 없음)
        _dishes(F)
        mo = S["mo"]
        F.append(((mo["x"] + 0.0, 0.88, 0.765 + 0.07), (0.2, 0.2, 0.1), (0, 0, 0), (0.78, 0.30, 0.22)))   # 찌개 냄비
        for k in range(3):
            ph = (tl * 0.5 + k / 3.0) % 1.0
            GM.append(star((mo["x"] + 0.03 * math.sin(ph * 9 + k), 0.88, 0.95 + 0.4 * ph), 0.06 * math.sin(math.pi * ph), STAR_W, ph))
    elif i == L["cake"]:                                              # 하은이 케이크를 들고 와 식탁에 놓음
        _dishes(F)
        ha = S["ha"]
        hand = rel(ha, 0.55, 0.0, hip_of(ha["pose"]) + 0.38)
        s = ramp(tl, 1.9, 2.4)
        if tl < 1.9:
            pos = (hand[0], hand[1], hand[2])
        else:
            a_ = (CARRY_END[0], CARRY_END[1], CARRY_END[2])
            pos = (a_[0] + (TABLE_CAKE[0] - a_[0]) * s, a_[1] + (TABLE_CAKE[1] - a_[1]) * s,
                   a_[2] + (TABLE_CAKE[2] - a_[2]) * s + 0.14 * math.sin(math.pi * s))
        f_, g_ = cake(pos, 1.0, tl)
        F += f_
        G += g_
    elif i in (L["momgem"], L["bright"]):                             # 엄마 눈에서 분홍 보석이 톡 → 분홍·파랑 보석 비교(분홍이 더 반짝)
        _dishes(F)
        f_, g_ = cake(TABLE_CAKE, 1.0, tl)
        F += f_
        G += g_
        mo = S["mo"]
        if i == L["momgem"]:
            G += streaks(mo, (0.55, 0.28, 0.40))
            glow, lastp = 0.0, None
            for k, (x, y, s, r, t0) in enumerate(PINK_LAND):
                items, g = tear_gem(eye_pt(mo, 1 if k == 0 else -1), (x, y, 0.765), t0, tl, cam, "p", s, r, G=G)
                GM += items
                if tl >= t0:
                    lastp = (x, y, g)
            if lastp:
                LT.append(_lt((lastp[0], lastp[1] - 0.15, 0.765 + 0.3), "p", 4.0 + 8.0 * lastp[2]))
            for k, (x, y, s, r, t0) in enumerate(PINK_LAND):
                GM += twinkle((x, y, 0.84), tl, cam, 4, 0.2, 140 + k, STAR_P, 0.07, 1.2, t0 + 0.5)
        else:
            sp = 0.9 * tl
            for k, (x, y, s, r, t0) in enumerate(PINK_LAND):
                GM.append((((x, y, 0.765)), s * (1.15 if k == 0 else 0.9), r + sp, tuple(1.3 * c for c in GEM_P), GM_GEM))
            GM.append(((-0.14, 1.2, 0.765), 1.2, 0.3 + 0.3 * tl, tuple(0.55 * c for c in GEM_B), GM_GEM))
            GM += twinkle((-0.4, 1.18, 0.86), tl, cam, 7, 0.28, 150, STAR_P, 0.1, 1.6)
            GM += twinkle((-0.64, 1.14, 0.86), tl, cam, 5, 0.22, 151, STAR_P, 0.08, 1.4)
            GM += twinkle((-0.14, 1.2, 0.86), tl, cam, 1, 0.1, 152, STAR_B, 0.05, 0.7)
            LT.append(_lt((-0.45, 1.0, 1.05), "p", 6.0 + 2.0 * math.sin(tl * 5.0)))
            LT.append(_lt((-0.12, 1.0, 1.0), "b", 1.5))
    elif i == L["necklace"]:                                          # 목걸이 만들기: 고리가 이어지고 분홍 보석이 달림
        for x, y, s, r in DESK_GEMS + LANDS:
            if y > 0.95:
                GM.append(gem((x, y, DESK_Z), s, r, "b"))
        cx, cy = NECK
        ang0, gap, n = math.pi / 2, 0.55, 24
        for k in range(n):
            th = ang0 + gap / 2 + (2 * math.pi - gap) * (k + 0.5) / n
            order = min(k, n - 1 - k)                               # 뒤쪽(고리 열린 곳)에서 앞쪽으로 양쪽이 차례로 이어짐
            sc = pop(tl - (0.25 + 0.1 * order), 0.25, 3.0)
            if sc > 0:
                F.append(((cx + 0.30 * math.cos(th), cy + 0.2 * math.sin(th), DESK_Z + 0.02), (0.065 * sc, 0.045 * sc, 0.035 * sc),
                          (0, 0, th + math.pi / 2), GOLD))
        t0, ft = 1.75, 0.3                                          # 분홍 보석이 위에서 떨어져 고리 앞쪽에 달림
        pz = (cx, cy - 0.2, DESK_Z + 0.04)
        glow = 0.0
        if tl >= t0:
            if tl < t0 + ft:
                f = (tl - t0) / ft
                GM.append(gem((pz[0], pz[1], 1.1 - (1.1 - pz[2]) * f * f), 0.7, 0.5 + 3.0 * f, "p"))
            else:
                ta = tl - t0 - ft
                GM.append(gem(pz, 0.7 * (1.0 + 0.3 * max(0.0, 1.0 - ta / 0.25)), 0.5, "p"))
                GM += burst((pz[0], pz[1], pz[2] + 0.06), ta, cam, col=STAR_P, size=0.08, r=0.25)
                glow = max(0.0, 1.0 - ta)
        GM += twinkle((pz[0], pz[1], pz[2] + 0.1), tl, cam, 6, 0.22, 160, STAR_P, 0.07, 1.4, t0 + ft)
        if tl >= 0.3:
            LT.append(_lt((cx, cy - 0.35, DESK_Z + 0.35), "p", 3.0 + 9.0 * glow))
    elif i == L["ask"]:                                               # 목걸이를 건 하은 + 책상 위 파란·분홍 보석 + 질문
        ha = S["ha"]
        for x, y, s, r in DESK_GEMS + LANDS:
            GM.append(gem((x, y, DESK_Z), s, r, "b"))
        GM.append(gem((0.28, 0.62, DESK_Z), 1.0, 0.8, "p"))
        pts, pend = chain_pts(ha)
        for p in pts:
            F.append((p, (0.03, 0.03, 0.03), (0, 0, math.radians(ha["yaw"])), GOLD))
        GM.append(gem((pend[0], pend[1], pend[2] - 0.045), 0.62, 0.2 * tl, "p"))
        GM += twinkle((pend[0], pend[1] - 0.05, pend[2] + 0.03), tl, cam, 4, 0.12, 170, STAR_P, 0.05, 1.3)
        GM += twinkle((0.28, 0.62, DESK_Z + 0.09), tl, cam, 4, 0.16, 171, STAR_P, 0.06, 1.1)
        for k, (x, y, s, r) in enumerate(DESK_GEMS + LANDS):
            GM += twinkle((x, y, DESK_Z + 0.07), tl, cam, 2, 0.14, 180 + k, STAR_B, 0.05, 0.9)
        hd = head_pt(ha)
        for k in range(6):
            ph = (tl * 0.18 + _h(k * 5.1)) % 1.0
            GM.append(star((hd[0] + 0.7 * (_h(k * 2.3) - 0.5), hd[1] - 0.1 + 0.2 * _h(k * 4.4), hd[2] - 0.1 + 0.9 * ph),
                           0.07 * math.sin(math.pi * ph) ** 0.7, STAR_W, 0.5 * k + tl))
        LT.append(_lt((pend[0], pend[1] - 0.2, pend[2] + 0.05), "p", 2.5))
        LT.append(_lt((0.2, 0.55, DESK_Z + 0.3), "b", 2.0))
    return F, G, GM, DG, LT


# ───────────────────────── 한 프레임 ─────────────────────────
N_FX, N_GL, N_GM, N_DG = 150, 260, 420, 24


def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·소품·보석·숫자 점 배열, 카메라, 조명."""
    W = _world()
    i = line_at(t)
    a, b = shot_span(i)
    dur = max(b - a, 1e-3)
    tau = max(t - a, 0.0)             # 줄 시작 0.02초 전부터 그 줄로 치므로 음수 방지
    u = min(tau / dur, 1.0)
    S, P, R, CO, C2, SC, PO = {}, [], [], [], [], [], []
    for c in W["C"]:
        d = state_of(c, i, u, tau, dur, t)
        CO.append(c["shirt"])
        C2.append(c["pants"])
        if d is None:
            P.append((0.0, 0.0, 0.0))
            R.append((0.0, 0.0, 0.0))
            SC.append(0.0)
            PO.append(0)
            continue
        S[c["name"]] = d
        ox, oy = OFF[d["set"]]
        P.append((d["x"] + ox, d["y"] + oy, d["z"]))
        R.append((0.0, 0.0, math.radians(d["yaw"])))
        SC.append(d["scale"])
        PO.append(W["PI"][(d["pose"], c["hair"])])
    shot, ul = cut_at(i, u)
    cam = cam_pose(shot, ul)
    o = OFF[cam["set"]]
    F, G, GM, DG, LT = props(i, tau, dur, u, S, t, cam)
    face = math.radians(cam["az"] + 90.0)

    def shift(items):
        return [((p[0] + o[0], p[1] + o[1], p[2]), s, r, c) for p, s, r, c in items]
    GMs = [((p[0] + o[0], p[1] + o[1], p[2]), s, ((0.0, rz, face) if k == GM_STAR else (0.0, 0.0, rz)), c, k) for p, s, rz, c, k in GM]
    DGs = [((p[0] + o[0], p[1] + o[1], p[2]), s, (0.0, 0.0, rz), ix) for p, s, rz, ix in DG]
    LTs = [((p[0] + o[0], p[1] + o[1], p[2]), k, w) for p, k, w in LT]
    return dict(i=i, tl=tau, u=u, set=cam["set"], cam=cam, A=S, P=P, R=R, CO=CO, C2=C2, SC=SC, PO=PO, fx=shift(F), glow=shift(G),
                gems=GMs, digits=DGs, LT=LTs, env=env(i, tau, dur))


# ───────────────────────── Blender 원형(프로토) ─────────────────────────
def _mat_gem(name, mul, white, strength):
    """인스턴스 'col' 색으로 빛나는 재질 (mul 곱해 어둡게, white만큼 흰색을 섞어 밝게)."""
    from engine import bkit as K
    m, nt, out = K.new_mat(name)
    c = K.inst_attr(nt, "col")
    if white > 0:
        c = K.mix_rgb(nt, white, c, (1.0, 1.0, 1.0))
    if mul != 1.0:
        c = K.mix_rgb(nt, 1.0, c, (mul, mul, mul), "MULTIPLY")
    e = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, c, e.inputs["Color"])
    e.inputs["Strength"].default_value = strength
    K.ln(nt, e.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def _mat_glow(name, strength=3.0):
    """인스턴스 'col' 색으로 빛나는 재질 (볼 눈물 자국·반짝이 상자 등)."""
    return _mat_gem(name, 1.0, 0.0, strength)


def _gem_parts(K):
    """보석 = 45도 돌린 네모(마름모) 여러 장. 가운데 큰 마름모를 앞뒤(xz)·옆(yz) 두 장 엇갈려 세우고, 작은 마름모 둘을 곁에 붙이고,
    앞뒤 면에 밝은 마름모 결을 얹음. 원점 = 바닥 가운데. 재질 0 몸 · 1 어두운 면 · 2 밝은 결."""
    pa = math.pi / 4
    P = []
    cz = 0.0676

    def dia_y(sx, sy, cx, cy, cz_, mi):                    # xz 평면 마름모 (y축 둘레로 45도)
        bm = K.bm_cube(sx, sy, sx, (cx, cy, cz_))
        P.append((X._rot_y(bm, pa, (cx, cy, cz_)), mi))

    def dia_x(sx, sy, cx, cy, cz_, mi):                    # yz 평면 마름모 (x축 둘레로 45도)
        bm = K.bm_cube(sx, sy, sy, (cx, cy, cz_))
        P.append((_rot_x(bm, pa, (cx, cy, cz_)), mi))
    dia_y(0.09, 0.034, 0.0, 0.0, cz, 0)
    dia_x(0.030, 0.085, 0.0, 0.0, cz, 1)
    dia_y(0.05, 0.026, -0.058, 0.012, 0.042, 0)
    dia_y(0.045, 0.026, 0.056, -0.010, 0.037, 0)
    dia_y(0.032, 0.005, -0.016, -0.0215, 0.082, 2)
    dia_y(0.032, 0.005, 0.016, 0.0215, 0.082, 2)
    return P


def _star_parts(K):
    """네 방향 + 대각선 반짝이 (얇은 십자 둘 + 짧은 대각선 둘). 배율 1.0 = 한 변 1m (배율 = 미터), 원점 = 가운데, 앞 = -y."""
    P = []
    for sx, sz in ((1.0, 0.09), (0.09, 1.0)):
        P.append((K.bm_cube(sx, 0.04, sz, (0, 0, 0)), 0))
    for ang in (math.pi / 4, -math.pi / 4):
        bm = K.bm_cube(0.56, 0.04, 0.07, (0, 0, 0))
        P.append((X._rot_y(bm, ang, (0, 0, 0)), 0))
    return P


def _drop_parts(K):
    """눈물 방울 = 층층이 좁아지는 네모 넷 (도트 물방울), 원점 = 가운데."""
    P = []
    for w, h, zc in ((0.052, 0.034, -0.040), (0.040, 0.030, -0.008), (0.027, 0.028, 0.021), (0.013, 0.026, 0.046)):
        P.append((K.bm_cube(w, w, h, (0, 0, zc)), 0))
    return P


DIG_ARROW = ["..#..", "..#..", "..#..", "..#..", "#.#.#", ".###.", "..#.."]


def _digit_parts(K, ix):
    """도트 글자 한 개 = 같은 줄 이음 상자들. 원점 = 왼쪽 아래 앞. 0~9 숫자 · 10 원 · 11 아래 화살표."""
    if ix < 10:
        rows, cell = _digit_rows(str(ix)), DCELL
    elif ix == 10:
        rows, cell = _won_rows(), 0.0105
    else:
        rows, cell = DIG_ARROW, DCELL
    n = len(rows)
    P = []
    for r, c0, c1 in _runs(rows):
        P.append((K.bm_cube((c1 - c0 + 1) * cell, 0.015, cell, ((c0 + c1 + 1) / 2.0 * cell, -0.0065, (n - 1 - r + 0.5) * cell)), 0))
    return P


def build(ctx):
    from engine import bkit as K
    v = X.Vox(33)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep33_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep33_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep33_people", protos, len(W["C"]))
    # 보석·반짝이·물방울: 원형 하나 = 점 하나, 색은 인스턴스 'col'
    gmat = [_mat_gem("ep33_m_gem", 1.0, 0.0, 1.9), _mat_gem("ep33_m_gemd", 0.5, 0.0, 1.9), _mat_gem("ep33_m_gemh", 1.0, 0.7, 2.4)]
    gm = K.instancer_multi(ctx, "ep33_gems", [K.proto(ctx, "ep33_p_gem", K.join_bms(_gem_parts(K)), gmat),
                                              K.proto(ctx, "ep33_p_star", K.join_bms(_star_parts(K)), [_mat_gem("ep33_m_star", 1.0, 0.0, 6.0)]),
                                              K.proto(ctx, "ep33_p_drop", K.join_bms(_drop_parts(K)), [_mat_gem("ep33_m_drop", 1.0, 0.0, 3.0)])],
                           N_GM)
    try:
        gm.visible_shadow = False
    except AttributeError:
        pass
    dmat = [K.mat_simple("ep33_m_dig", (0.78, 0.08, 0.10), 0.6, emit=(0.78, 0.08, 0.10), estr=0.6)]
    dig = K.instancer_multi(ctx, "ep33_digits", [K.proto(ctx, "ep33_p_dig%02d" % n, K.join_bms(_digit_parts(K, n)), dmat)
                                                 for n in range(12)], N_DG)
    cube = lambda: K.bm_cube(1, 1, 1)
    fx = K.instancer(ctx, "ep33_fx", K.proto(ctx, "ep33_p_fx", cube(), [K.mat_inst("ep33_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep33_glow", K.proto(ctx, "ep33_p_glow", cube(), [_mat_glow("ep33_m_glow")]), N_GL, vector_scale=True)
    glb = K.point_light(ctx, (0, 0, -80), 0.0, (0.35, 0.55, 1.0), 0.12, "ep33_gl_b")
    glp = K.point_light(ctx, (0, 0, -80), 0.0, (1.0, 0.45, 0.75), 0.12, "ep33_gl_p")

    def boxes(ob, items, cap):
        Pp, Ss, Rr, Cc = (np.zeros((cap, 3), np.float32) for _ in range(4))
        for k, (p, s, r, c) in enumerate(items[:cap]):
            Pp[k], Ss[k], Rr[k], Cc[k] = p, s, r, c
        K.set_points(ob, Pp, scale=(Ss[:, 0] > 0).astype(np.float32), size=Ss, rot=Rr, col=Cc)

    def upd(t, f):
        S = frame_state(t)
        c = S["cam"]
        cam.set(c["tgt"], c["az"], c["el"], c["dist"], c["lens"], shift=c["shift"])
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
        n = min(len(S["gems"]), N_GM)
        Pp, Ss, Rr, Cc, Kk = (np.zeros((N_GM, 3), np.float32), np.zeros(N_GM, np.float32), np.zeros((N_GM, 3), np.float32),
                              np.zeros((N_GM, 3), np.float32), np.zeros(N_GM, np.float32))
        for k, (p, s, r, col, kind) in enumerate(S["gems"][:n]):
            Pp[k], Ss[k], Rr[k], Cc[k], Kk[k] = p, s, r, col, kind
        K.set_points(gm, Pp, scale=Ss, rot=Rr, col=Cc, pose=Kk)
        nd = min(len(S["digits"]), N_DG)
        Pp, Ss, Rr, Kk = np.zeros((N_DG, 3), np.float32), np.zeros(N_DG, np.float32), np.zeros((N_DG, 3), np.float32), np.zeros(N_DG, np.float32)
        for k, (p, s, r, ix) in enumerate(S["digits"][:nd]):
            Pp[k], Ss[k], Rr[k], Kk[k] = p, s, r, ix
        K.set_points(dig, Pp, scale=Ss, rot=Rr, pose=Kk)
        boxes(fx, S["fx"], N_FX)
        boxes(gl, S["glow"], N_GL)
        for ob, kind in ((glb, "b"), (glp, "p")):
            hit = [(p, w) for p, k, w in S["LT"] if k == kind]
            if hit:
                ob.location, ob.data.energy = hit[0][0], hit[0][1]
            else:
                ob.data.energy = 0.0

    ctx.on_frame(upd)
