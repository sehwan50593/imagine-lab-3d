"""EP27 만약에 엄마의 잔소리가 하루 사라진다면? (19편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
문가에서 입만 크게 벌린 엄마, 말풍선은 빈 '…'·이불 속에서 눈만 내민 아이(훅) → 평소 아침 잔소리 말풍선이 연달아 팝
→ 오늘은 말없이 커튼만 걷고 나가는 엄마 → 벌떡 두 팔 번쩍 "자유다!" → 짝짝이 양말로 식탁 앞을 휙, 입술 꾹 문 엄마
→ 국자가 파르르 → 학교 복도 하이파이브 → 불 켠 채 게임·과자 → 던져 둔 가방을 말없이 줍는 엄마(한숨 '…')
→ 설거지하며 말을 삼키는 엄마(말풍선이 부풀다 쏙) → 조용해진 방에서 문 쪽을 힐끔
→ 반전: 오늘 들은 잔소리 0번(큰 말풍선 속 블록 숫자 0) → 밤, 허전해서 천장만 봄 → 살금살금 들어와 이불을 덮어 주는 엄마
→ "엄마… 나 숙제 안 했어" → 엄마 폭풍 잔소리(말풍선이 줄줄이)에 피식 → 소파에서 어깨를 감싼 두 사람 → 노을 속 질문.
근거(설명란): 상상 이야기이며 통계·연구 인용 없음(화면의 '0번'도 이야기 속 숫자일 뿐).
특수효과: 말풍선 = 흰 판(검은 테두리·계단 꼬리) + 한글 도트 글자(Noto Sans KR(OFL)을 16x16 칸으로 줄인 비트맵, GLYPH
16진 4자리×16줄)를 가로 한 줄씩 상자로 이어 만든 원형. instancer_multi 점 하나씩으로 띄우고 카메라 쪽으로 돌림(빌보드).
톡 튀어나오고(easeOutBack) 잔소리 폭주 컷은 0.25~0.5초 간격으로 줄줄이 팝, '삼킨 말'은 부풀다 쏙 들어감.
이불·커튼·문·가방·국자·과자·김·반짝이 = 상자 인스턴스(fx 일반 / glow 발광). 짝짝이 양말 = 걷는 자세 원형에 붙인 상자.
새 자세(두 팔 번쩍·하이파이브·국자·숙인 자세·눈 뜨고 누움·웃는 입 등) = 바탕 자세의 몸에서 팔·입만 바꾼 원형(ep25·ep23 방식).
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
OFF = {"room": (0, 0), "home": (300, 0), "school": (600, 0), "room_eve": (900, 0), "home_dusk": (1200, 0),
       "room_night": (1500, 0)}
NAMES = ("hook", "morning", "silent", "free", "socks", "lips", "school", "game", "bag", "swallow", "quiet", "zero",
         "empty", "sneak", "tuck", "confess", "storm", "smile", "hug", "ask")
LN = {n: k for k, n in enumerate(NAMES)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 엄마의 잔소리가 하루 사라진다면 어떻게 될까요?", gap=0.6, shot=("room", (0.5, 2.0, 1.9), -90, 32, 3.8, 28, 0.95, 3)),
    dict(say="평소 아침이면, 이런 말이 쏟아졌죠", shot=("room", (0.9, 2.0, 1.75), -78, 12, 4.0, 28, 0.9, 4)),
    dict(say="그런데 오늘은 한마디도 없어요", shot=("room", (1.45, 1.85, 1.25), -93, 14, 5.2, 26, 0.95, -3)),
    dict(say="어라? 오늘은 자유다!", shot=("room", (-0.1, 1.3, 1.3), -75, 7, 4.6, 28, 0.95, 4)),
    dict(say="양말은 짝짝이, 아침은 건너뛰고", shot=("home", (0.0, 0.3, 0.55), -90, 4, 4.6, 28, 0.95, 0)),
    dict(say="엄마는 입술을 꾹 깨물었어요", shot=("home", (-0.75, 0.65, 1.2), -90, 4, 3.0, 28, 0.9, 0)),
    dict(say="학교에서도 하루 종일 신났죠", shot=("school", (0.0, 0.5, 1.0), -90, 6, 5.4, 24, 0.93, 3)),
    dict(say="집에 오자마자 게임부터!", shot=("room_eve", (0.0, 1.0, 0.95), -78, 10, 4.6, 28, 0.93, 3)),
    dict(say="가방은 던져 두고, 숙제는 내일", shot=("room_eve", (0.7, 0.8, 0.85), -80, 16, 4.8, 28, 0.93, 2)),
    dict(say="엄마는 저녁 내내 말을 삼켰어요", gap=0.5, shot=("home_dusk", (-2.1, 1.0, 1.3), -58, 8, 3.7, 28, 0.92, 3)),
    dict(say="그런데 이상하게, 자꾸 조용해져요", gap=0.5, shot=("room_eve", (-0.1, 0.9, 0.95), -84, 7, 4.0, 28, 0.9, 0)),
    dict(say="오늘 들은 잔소리, 0번", gap=0.9, shot=("room_eve", (-0.1, 0.9, 1.45), -90, 4, 3.8, 28, 0.9, 0)),
    dict(say="이상하게 마음이 허전했어요", gap=0.5, shot=("room_night", (-0.1, 1.55, 0.6), -90, 52, 3.8, 28, 0.9, 3)),
    dict(say="그때 엄마가 살금살금 들어와", shot=("room_night", (0.5, 2.0, 1.25), -90, 10, 4.4, 28, 0.95, 0)),
    dict(say="말없이 이불을 덮어 주고 나갔어요", gap=0.6, shot=("room_night", (0.3, 1.7, 0.95), -110, 22, 3.8, 28, 0.93, 4)),
    dict(say="“엄마… 나 숙제 안 했어”", gap=0.4, shot=("room_night", (0.4, 1.7, 1.3), -90, 16, 4.6, 28, 0.94, 2)),
    dict(say="“뭐? 지금이 몇 시인데!”", shot=("room_night", (0.5, 2.0, 1.9), -86, 10, 4.4, 28, 0.92, 3)),
    dict(say="아이는 피식, 안심이 됐어요", shot=("room_night", (0.3, 1.4, 1.3), -98, 6, 2.9, 28, 0.92, 3)),
    dict(say="잔소리는 사랑의 다른 말이었나 봐요", gap=0.9, shot=("home_dusk", (1.2, 2.0, 1.15), -90, 5, 3.5, 28, 0.92, 0)),
    dict(say="마지막으로 잔소리 들은 건 언제예요?", shot=("home_dusk", (1.2, 2.0, 1.3), -84, 14, 4.6, 28, 1.15, -3)),
]
assert len(LINES) == len(NAMES)
TITLE = [("만약에", "white"), ("엄마의 잔소리가", "white"), ("하루 사라진다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = LN["zero"]          # '오늘 들은 잔소리, 0번' 줄

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep27_nonagging" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep27", "title": "만약에 엄마의 잔소리가 하루 사라진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "F", "mode": "major", "bpm": 84, "seed": 271, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

KID_SH, KID_PA = (0.95, 0.80, 0.35), (0.20, 0.20, 0.22)         # 아이: 노란 셔츠·짙은 회색 바지·짧은 머리
MOM_SH, MOM_PA = (0.92, 0.55, 0.60), (0.35, 0.28, 0.20)         # 엄마: 분홍 셔츠·긴 머리
FRI_SH, FRI_PA = (0.25, 0.45, 0.80), (0.15, 0.18, 0.30)         # 친구: 파란 셔츠
KID_S = 0.9                                                      # 중학생 키


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


NIGHT = range(LN["empty"], LN["smile"] + 1)       # 밤 방(허전함 → 이불 → 고백 → 폭풍 → 피식)
DUSK = (LN["swallow"], LN["hug"], LN["ask"])      # 저녁 부엌 · 해질녘 거실


def sky(t):
    i = line_at(t)
    if i in NIGHT:
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0
    if i in DUSK:
        return (0.20, 0.17, 0.42), (0.98, 0.58, 0.38), 0.0
    if i in (LN["quiet"], LN["zero"]):
        return (0.07, 0.08, 0.24), (0.50, 0.30, 0.36), 0.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


def env(i, tl, du):
    """줄별 햇빛·주변광 + 움직이는 조명 {이름: 세기}. 아침 방은 커튼이 열릴 때 환해지고, 게임 줄은 점점 어두워짐."""
    day = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if i in (LN["hook"], LN["morning"]):                # 커튼 닫힌 아침: 어둑
        return dict(day, sun=1.5, amb=0.3, amb_col=(0.55, 0.62, 0.8), lt={"ep27_am_win": 12.0})
    if i == LN["silent"]:
        k = ramp(tl, 0.95, 1.5)
        return dict(day, sun=1.5 + 1.5 * k, amb=0.3 + 0.12 * k, amb_col=(0.55 + 0.07 * k, 0.62 + 0.06 * k, 0.8 + 0.02 * k),
                    lt={"ep27_am_win": 12.0 + 118.0 * k})
    if i in (LN["game"], LN["bag"]):                    # 늦은 오후
        return dict(day, sun=1.8, sun_col=(1.0, 0.78, 0.55), sun_rot=(68, 0, 32), amb=0.3, amb_col=(0.7, 0.66, 0.7),
                    lt={"ep27_ev_ceil": 110.0, "ep27_ev_phone": 0.0})
    if i in (LN["quiet"], LN["zero"]):                  # 점점 조용하고 어두워짐 + 게임 불빛
        k = ramp(tl, 0.0, du) if i == LN["quiet"] else 1.0
        return dict(day, sun=1.8 * (1 - k), amb=0.3 - 0.17 * k, amb_col=(0.5 - 0.15 * k, 0.5 - 0.08 * k, 0.7 - 0.05 * k),
                    sun_col=(1.0, 0.78, 0.55), sun_rot=(68, 0, 32),
                    lt={"ep27_ev_ceil": 110.0 - 70.0 * k, "ep27_ev_phone": 16.0 * k})
    if i in DUSK:
        return dict(day, sun=2.6, sun_col=(1.0, 0.66, 0.42), sun_rot=(78, 0, 30), amb=0.2, amb_col=(0.55, 0.45, 0.66))
    if i in NIGHT:
        hall = 0.0
        if i == LN["sneak"]:
            hall = 90.0 * ramp(tl, 0.15, 0.7)
        elif i > LN["sneak"]:
            hall = 90.0
        return dict(day, sun=0.0, amb=0.1, amb_col=(0.3, 0.38, 0.62), lt={"ep27_night_hall": hall})
    return day                                           # 낮(집 아침·학교)


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def cam_pose(shot, u):
    """줄 진행도 u에서 카메라: (목표점, 방위각, 고도각, 거리, 렌즈, 위치) — 월드 좌표. CamRig.set과 같은 규칙."""
    st, tg, az, el, dist, lens, push, daz = shot
    o = OFF[st]
    tgt = (tg[0] + o[0], tg[1] + o[1], tg[2])
    a, e, d = az + daz * u, math.radians(el), dist * (1 + (push - 1) * u)
    loc = (tgt[0] + math.cos(e) * math.cos(math.radians(a)) * d,
           tgt[1] + math.cos(e) * math.sin(math.radians(a)) * d, tgt[2] + math.sin(e) * d)
    return tgt, a, el, d, lens, loc


def cam_axes(az, el):
    """카메라의 오른쪽·위쪽 단위벡터."""
    a, e = math.radians(az), math.radians(el)
    return (-math.sin(a), math.cos(a), 0.0), (-math.cos(a) * math.sin(e), -math.sin(a) * math.sin(e), math.cos(e))


# ───────────────────────── 말풍선: 도트 글자·그림 ─────────────────────────
C0 = 0.04                                      # 말풍선 한 칸(m). 실제 크기는 줄마다 화면 비율로 키움(bub_scale)
PAL_ORDER = "RPKOY"
PAL = {"R": (0.93, 0.15, 0.20), "P": (1.0, 0.72, 0.78), "K": (0.10, 0.10, 0.16), "O": (1.0, 0.55, 0.10),
       "Y": (1.0, 0.80, 0.12)}
# 도트 글자 16x16: 한 줄(가로 16칸)을 16진 4자리로, 맨 윗줄부터 16줄 이어 붙임(왼쪽 칸 = 가장 높은 비트).
# 만든 법(새 낱말이 필요하면 같은 방식으로): assets/fonts/NotoSansKR-VF.ttf(OFL)를 굵기 620으로 크게 그려 글자 경계 상자를
# 16칸 격자 가운데에 꽉 차게(0.94) 줄이고, 칸 평균이 0.40 이상이면 켬. '!'는 _glyph_rows에서 직접 그림.
GLYPH = {
    "일": "000c1f0c3f8c31cc70cc31cc3f8c0f0c00000ffc000c0ffc0ffc0c000ffc0ffc",
    "어": "000c040c1f0c1f8c318c318c30fc31fc318c318c1f8c0f0c000c000c000c000c",
    "나": "001000386038603860386038603e603e603860387ff87f380038003800380010",
    "늦": "18001800180018001ffc1ff800007ffe7ffe00003ff803c003c00ff03c3c0000",
    "었": "00081e1c3f1c739c61fc61fc739c3f1c0c1c04300e300e300e783bfc31ce0000",
    "양": "00180e183f1e719e61986198739e3f180c1800000ff01c3818181c380ff003c0",
    "말": "00107f187f98639c639e63987f983f1800001ff800381ff81ff818001ff81ff8",
    "씻": "000c198c198c198c1dcc1dcc3fec776c222c000c00cc00e001e007381e1e0800",
    "숙": "0180018003c007e01e783c3c00007ffe7ffe01801ff81ff80018001800180008",
    "제": "000400363fb63fb60c360e760ef60e760e361b363bf631b60036003600260004",
    "몇": "00083f9c7ffc71fc719c71fc7ffc3f9c001c01c01ffc01c001c007701e3c0000",
    "시": "0004000c070c070c070c070c070c070c0f8c1dcc38ec306c000c000c000c0004",
    "니": "000c000c300c300c300c300c300c300c300c304c3fec3f8c000c000c000c000c",
    "게": "000400663f663f660366036607e607e60e661c66386630660066006600660004",
    "임": "000c0f0c1f8c31cc30cc30cc39cc1f8c040c00000ffc0c0c0c0c0c0c0ffc0ffc",
    "자": "001800187fd83f980e180e180e1e0e1e1f181b9839d870d80018001800180018",
    "라": "001000387f380338033803387f3e7f3e603860387ff87fb80038003800380010",
    "빨": "00086b586f787ffe7ffe6f787ff87bd800081ff81ff81ff81ff818001ffc1ff8",
    "리": "000c000c3f8c018c018c018c3f8c3f8c300c300c3fec3fec000c000c000c000c",
    "불": "18181ff81ff818181ff81ff87ffe7ffe01801ff81ff81ff81ff818001ffc1ff8",
    "꺼": "0004000c3fcc3fcc0ccc0ccc0cfc0cfc1ccc19cc398c338c030c000c000c0004",
}


def _glyph_rows(c):
    """글자 하나 → 16줄 문자열('#'=칸 켬), 비어 있는 좌우 열은 잘라 냄."""
    if c == "!":
        return ["..."] + ["###"] * 8 + ["..."] * 2 + ["###"] * 3 + ["..."] * 2
    hx = GLYPH[c]
    rows = [format(int(hx[k * 4:k * 4 + 4], 16), "016b") for k in range(16)]
    on = [x for x in range(16) if any(r[x] == "1" for r in rows)]
    return [r[min(on):max(on) + 1].replace("1", "#").replace("0", ".") for r in rows]


def _text_grid(txt, ch):
    """글 → 16줄 문자열(켜진 칸 = ch). 글자 사이 한 칸, 띄어쓰기 다섯 칸."""
    parts = []
    for c in txt:
        parts.append(["....."] * 16 if c == " " else _glyph_rows(c))
        parts.append(["."] * 16)
    rows = ["".join(p[r] for p in parts[:-1]) for r in range(16)]
    return [r.replace("#", ch) for r in rows]


ICONS = {      # 이름: (그림 줄들(글자 = 색), 그림 한 점이 차지하는 칸 수)
    "heart": ([".RR.RR.", "RPRRRRR", "RRRRRRR", ".RRRRR.", "..RRR..", "...R..."], 3),
    "anger": (["..R.R..", "..R.R..", "RRR.RRR", ".......", "RRR.RRR", "..R.R..", "..R.R.."], 3),
    "excl": (["RRR", "RRR", ".R.", ".R.", ".R.", "...", ".R."], 3),
    "dots1": (["KK......", "KK......"], 3), "dots2": (["KK.KK...", "KK.KK..."], 3), "dots3": (["KK.KK.KK", "KK.KK.KK"], 3),
    "zero": ([".RRR.", "R...R", "R...R", "R...R", "R...R", "R...R", ".RRR."], 5),     # 큰 블록 숫자 0
}
TEXTS = {"wake": "일어나!", "late": "늦었어!", "sock": "양말!", "wash": "씻어!", "hw": "숙제!", "time": "몇 시니!",
         "game": "게임!", "sleep": "자라!", "fast": "빨리!", "light": "불 꺼!"}      # 잔소리 말풍선(빨간 글씨)
for _k, _t in TEXTS.items():
    ICONS[_k] = (_text_grid(_t, "R"), 1)
BUB_NAMES = list(ICONS)
BUB_IX = {n: k for k, n in enumerate(BUB_NAMES)}


def _bub_parts(K, name):
    """말풍선 하나 = [(bmesh, 재질번호)] — 0 흰 판 · 1 검은 테두리 · 2~ 그림 색(PAL_ORDER). 원점 = 꼬리 끝, 앞 = +x(카메라 쪽).
    길이는 칸(C0) 단위로 짜고 마지막에 곱함. 판 = 그림 둘레 3칸 여백, 모서리 한 칸씩 깎고 계단 꼬리."""
    g, mult = ICONS[name]
    gh, gw = len(g), len(g[0])
    W, H, T = gw * mult + 6, gh * mult + 6, 3
    P = []

    def box(x0, x1, y0, y1, z0, z1, mi):
        P.append((K.bm_cube((x1 - x0) * C0, (y1 - y0) * C0, (z1 - z0) * C0,
                            ((x0 + x1) / 2 * C0, (y0 + y1) / 2 * C0, z0 * C0), bottom=True), mi))
    hw = W / 2
    shape = [(-hw + 2, hw - 2, T, T + 1), (-hw, hw, T + 1, T + H - 1), (-hw + 2, hw - 2, T + H - 1, T + H),
             (-2, 2, 1, T), (-1, 1, 0, 1)]
    for y0, y1, z0, z1 in shape:                                   # 테두리: 같은 모양을 한 칸 키워 뒤에 깐다
        box(-0.9, -0.15, y0 - 1, y1 + 1, z0 - 1, z1 + 1, 1)
    for y0, y1, z0, z1 in shape:
        box(-0.5, 0.0, y0, y1, z0, z1, 0)
    for r, row in enumerate(g):                                    # 그림: 같은 색이 이어진 칸은 상자 하나로
        c0 = 0
        while c0 < gw:
            ch = row[c0]
            if ch == ".":
                c0 += 1
                continue
            c1 = c0
            while c1 + 1 < gw and row[c1 + 1] == ch:
                c1 += 1
            y0 = (c0 - gw / 2) * mult
            z0 = T + 3 + (gh - 1 - r) * mult
            box(0.0, 0.6, y0, y0 + (c1 - c0 + 1) * mult, z0, z0 + mult, 2 + PAL_ORDER.index(ch))
            c0 = c1 + 1
    return P


def pop(tau, dur=0.30, over=3.0):
    """톡 튀어나오는 크기: 0 → 살짝 커졌다 → 1 (easeOutBack). tau<0이면 0."""
    if tau <= 0:
        return 0.0
    if tau >= dur:
        return 1.0
    x = tau / dur - 1.0
    return 1.0 + (over + 1.0) * x ** 3 + over * x ** 2


def bub_scale(sp, tl):
    """말풍선 하나의 지금 크기 배율(0이면 안 보임). life가 있으면 끝에서 쏙 줄어듦, swell이면 천천히 부풀었다 쏙."""
    tau = tl - sp["t0"]
    if tau <= 0:
        return 0.0
    life = sp.get("life")
    s = ramp(tau, 0.0, life - 0.16) * 1.05 if sp.get("swell") else pop(tau)
    if life is not None:
        if tau >= life:
            return 0.0
        if tau > life - 0.16:
            s *= (life - tau) / 0.16
    return s


# ───────────────────────── 세트 ─────────────────────────
BED_X, BED_TOP = -0.1, 0.45            # 침대 가운데 x · 요 윗면 높이 (아이 방, 머리판이 +y 뒷벽)
DOOR = (0.85, 1.75)                     # 아이 방 뒷벽의 문 (x 범위, 문 뒤는 복도)
SOFA_TOP = 0.43                         # 거실 소파 방석 높이
DARK = (0.2, 0.2, 0.22)


def _dusk_window(v, x0, x1, y, z0, z1, face=-1, axis="y"):
    """노을 창: 창틀은 v.window 그대로, 유리 위에 보라 → 분홍 → 주황 → 노랑 띠(발광)를 얇게 겹침."""
    v.window(x0, x1, y, z0, z1, night=False, face=face, axis=axis)
    cols = ((0.36, 0.30, 0.62), (0.80, 0.42, 0.52), (1.0, 0.62, 0.30), (1.0, 0.84, 0.42))
    h = (z1 - z0) / len(cols)
    a, b = y + 0.0205 * face, y + 0.0245 * face
    lo, hi = min(a, b), max(a, b)
    for k, c in enumerate(cols):
        zb = z1 - (k + 1) * h
        if axis == "y":
            v.box(x0, x1, lo, hi, zb, zb + h, c, jit=0, glow=True)
        else:
            v.box(lo, hi, x0, x1, zb, zb + h, c, jit=0, glow=True)


def _win(v, dusk, *a, **k):
    if dusk:
        _dusk_window(v, *a, **k)
    else:
        v.window(*a, night=False, **k)


def _room(v, mode):
    """아이 방 (mode = am 아침 · eve 늦은 오후~저녁 · night 밤). 앞(-y)이 열린 방, 침대 머리판은 뒷벽, 문은 뒷벽 오른쪽."""
    from engine import voxel as X
    night = mode == "night"
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    wb, ws = (0.88, 0.91, 0.97), (0.77, 0.85, 0.95)
    v.wall((-3, 2.5), (DOOR[0], 2.5), 0, 2.7, wb, 0.25, face=-1)
    v.wall((DOOR[1], 2.5), (3, 2.5), 0, 2.7, wb, 0.25, face=-1)
    v.wall((DOOR[0], 2.5), (DOOR[1], 2.5), 2.1, 2.7, wb, 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 2.7, ws, 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 2.7, ws, 0.25, face=1)
    # 문 뒤 복도 (불빛이 새어 들어옴)
    hw = (0.96, 0.93, 0.85)
    v.floor(DOOR[0], DOOR[1], 2.5, 4.2, (0.74, 0.62, 0.48), 0.2, "wood")
    v.wall((DOOR[0], 2.5), (DOOR[0], 4.2), 0, 2.7, hw, 0.25, face=-1)
    v.wall((DOOR[1], 2.5), (DOOR[1], 4.2), 0, 2.7, hw, 0.25, face=1)
    v.wall((DOOR[0], 4.2), (DOOR[1], 4.2), 0, 2.7, hw, 0.25, face=-1)
    fr = (0.50, 0.36, 0.24)                                                    # 문틀
    v.box(DOOR[0] - 0.06, DOOR[0] - 0.005, 2.42, 2.53, 0, 2.10, fr)
    v.box(DOOR[1] + 0.005, DOOR[1] + 0.06, 2.42, 2.53, 0, 2.10, fr)
    v.box(DOOR[0] - 0.06, DOOR[1] + 0.06, 2.42, 2.53, 2.10, 2.16, fr)
    # 창 (뒷벽 오른쪽)
    if mode == "am":
        v.window(2.0, 2.9, 2.49, 1.0, 2.2, night=False)
    elif night:
        v.window(2.0, 2.9, 2.49, 1.0, 2.2, night=True, lights=10)
        v.box(2.35, 2.6, 2.44, 2.46, 1.7, 1.95, (1.0, 0.98, 0.8), jit=0, glow=True)       # 달
    else:
        _dusk_window(v, 2.0, 2.9, 2.49, 1.0, 2.2)
    if mode != "am":                                                           # 정적 커튼 (아침엔 움직이는 소품)
        cu = (0.85, 0.45, 0.42)
        v.box(1.88, 2.14, 2.38, 2.46, 0.85, 2.35, cu)
        v.box(2.78, 2.97, 2.36, 2.44, 0.85, 2.35, cu)
    # 침대 + 베개 + 머리판 (이불은 움직이는 소품)
    bx = BED_X
    v.box(bx - 0.7, bx + 0.7, 0.5, 2.45, 0, 0.28, X.WOOD)
    v.box(bx - 0.67, bx + 0.67, 0.53, 2.42, 0.28, BED_TOP, X.WHITE, jit=0.02)
    v.box(bx - 0.72, bx + 0.72, 2.38, 2.47, 0, 1.05, X.DARKWOOD)
    v.box(bx - 0.4, bx + 0.4, 1.98, 2.35, BED_TOP, BED_TOP + 0.11, (0.97, 0.97, 0.97), jit=0.01)
    # 협탁 + 스탠드
    v.box(-1.62, -1.24, 2.05, 2.45, 0, 0.5, (0.62, 0.42, 0.25))
    v.box(-1.5, -1.36, 2.18, 2.32, 0.5, 0.58, (0.3, 0.3, 0.32), jit=0)
    v.box(-1.56, -1.3, 2.12, 2.38, 0.58, 0.84, (1.0, 0.88, 0.62), jit=0, glow=night)
    # 책상 + 의자 + 책 (왼쪽 벽), 책장, 포스터
    X.table(v, -2.5, 0.9, 0.7, 1.4, 0.74, (0.82, 0.66, 0.45))
    X.chair(v, -1.75, 0.9, 180, (0.3, 0.45, 0.7))
    v.box(-2.7, -2.3, 0.6, 1.0, 0.74, 0.78, (0.35, 0.55, 0.85))
    v.box(-2.8, -2.55, 1.15, 1.45, 0.74, 0.86, (0.95, 0.95, 0.93))
    v.box(-2.95, -2.6, -1.9, -0.5, 1.15, 1.2, X.WOOD)
    v.box(-2.95, -2.6, -1.9, -0.5, 1.65, 1.7, X.WOOD)
    cols = [(0.9, 0.3, 0.3), (0.3, 0.6, 0.9), (0.95, 0.8, 0.25), (0.35, 0.75, 0.45), (0.8, 0.5, 0.85), (0.95, 0.55, 0.2)]
    for z in (1.2, 1.7):
        y = -1.85
        while y < -0.62:
            w, h = float(v.rs.uniform(0.07, 0.13)), float(v.rs.uniform(0.2, 0.36))
            v.box(-2.93, -2.65, y, y + w, z, z + h, cols[int(v.rs.integers(len(cols)))], jit=0.06)
            y += w + 0.015
    v.box(-2.99, -2.97, 0.15, 0.95, 1.35, 2.15, (0.95, 0.75, 0.3), jit=0)          # 포스터
    v.box(-2.97, -2.96, 0.25, 0.85, 1.45, 2.05, (0.3, 0.6, 0.9), jit=0)
    v.box(-2.96, -2.95, 0.45, 0.65, 1.6, 1.9, (1.0, 0.95, 0.8), jit=0)
    # 옷장 (오른쪽 벽), 러그, 장난감 상자
    v.box(2.5, 2.97, -1.6, -0.2, 0, 2.0, (0.82, 0.86, 0.92))
    v.box(2.47, 2.5, -0.95, -0.85, 0.2, 1.9, (0.4, 0.4, 0.45), jit=0)
    v.floor(-1.8, 1.2, -1.4, 0.3, (0.82, 0.55, 0.50), 0.5, "check", z=0.012)
    v.box(2.2, 2.9, -2.35, -1.85, 0, 0.45, (0.95, 0.75, 0.3))
    v.box(2.3, 2.55, -2.3, -2.05, 0.45, 0.7, (0.9, 0.3, 0.3))
    # 조명
    if mode == "am":
        v.light(1.3, 3.3, 1.9, 90, (1.0, 0.85, 0.6), 0.5, "ep27_am_hall")
        v.light(2.45, 1.9, 1.7, 130, (0.85, 0.92, 1.0), 0.8, "ep27_am_win")
        v.light(0.3, -1.2, 1.7, 90, (1.0, 0.95, 0.88), 0.6, "ep27_am_fill")
    elif mode == "eve":
        v.light(0.0, 0.5, 2.3, 110, (1.0, 0.82, 0.58), 0.5, "ep27_ev_ceil")
        v.light(2.45, 1.9, 1.7, 60, (1.0, 0.62, 0.35), 0.8, "ep27_ev_win")
        v.light(-0.1, 0.3, 1.2, 0, (0.5, 0.8, 1.0), 0.2, "ep27_ev_phone")
        v.light(-0.3, -1.4, 1.5, 30, (1.0, 0.9, 0.8), 0.6, "ep27_ev_fill")
    else:
        v.light(-1.43, 2.25, 1.0, 20, (1.0, 0.78, 0.5), 0.3, "ep27_night_lamp")
        v.light(2.45, 1.9, 1.8, 22, (0.55, 0.65, 1.0), 0.8, "ep27_night_moon")
        v.light(1.3, 3.2, 1.9, 0, (1.0, 0.82, 0.55), 0.5, "ep27_night_hall")
        v.light(0.3, -1.2, 1.7, 45, (0.6, 0.68, 1.0), 0.8, "ep27_night_fill")


def _home(v, mode):
    """주방 겸 거실 (mode = am 아침 · dusk 저녁/노을). 뒷벽 왼쪽 싱크대, 가운데 창 앞 소파, 오른쪽 구석 냉장고, 앞쪽 식탁."""
    from engine import voxel as X
    dusk = mode == "dusk"
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    v.wall((-3, 2.5), (3, 2.5), 0, 2.7, (0.93, 0.90, 0.82), 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=1)
    # 주방: 싱크대 + 개수대 + 가스레인지·냄비 + 찬장, 그 위 창
    v.box(-2.95, -0.45, 1.9, 2.48, 0, 0.88, (0.95, 0.95, 0.93))
    v.box(-2.97, -0.43, 1.86, 2.48, 0.88, 0.93, (0.55, 0.57, 0.6))
    for x in np.arange(-2.7, -0.5, 0.75):
        v.box(x, x + 0.25, 1.88, 1.9, 0.62, 0.65, DARK, jit=0)
    v.box(-0.95, -0.47, 2.1, 2.48, 1.55, 2.25, (0.95, 0.95, 0.93))
    _win(v, dusk, -2.6, -1.0, 2.49, 1.25, 2.2)
    # 왼쪽 벽 싱크대 (ㄱ자 주방): 개수대·수도꼭지 + 그 위 창 — 엄마가 옆모습으로 서서 설거지, 고개를 돌리면 얼굴이 보임
    v.box(-2.95, -2.35, 0.2, 1.84, 0, 0.88, (0.95, 0.95, 0.93))
    v.box(-2.97, -2.33, 0.2, 1.85, 0.88, 0.93, (0.55, 0.57, 0.6))
    for y in (0.4, 1.1):
        v.box(-2.35, -2.33, y, y + 0.25, 0.62, 0.65, DARK, jit=0)
    v.box(-2.9, -2.42, 0.6, 1.3, 0.93, 0.945, (0.35, 0.37, 0.42), jit=0)            # 개수대
    v.box(-2.5, -2.44, 0.92, 0.98, 0.945, 1.12, (0.8, 0.82, 0.86), jit=0)            # 수도꼭지
    v.box(-2.49, -2.3, 0.93, 0.97, 1.06, 1.10, (0.8, 0.82, 0.86), jit=0)
    _win(v, dusk, 0.35, 1.6, -2.99, 1.25, 2.2, face=1, axis="x")
    v.box(-1.45, -0.75, 2.0, 2.4, 0.935, 0.97, (0.15, 0.15, 0.17), jit=0)          # 가스레인지
    v.box(-1.25, -0.95, 2.1, 2.3, 0.97, 1.2, (0.62, 0.64, 0.68))                    # 냄비
    # 냉장고 (오른쪽 뒤 구석)
    v.box(2.2, 2.95, 1.75, 2.48, 0, 2.0, (0.82, 0.84, 0.87))
    v.box(2.28, 2.31, 1.73, 1.75, 0.9, 1.5, DARK, jit=0)
    v.box(2.5, 2.75, 1.73, 1.75, 1.3, 1.55, (0.95, 0.75, 0.3), jit=0)
    # 소파 + 뒤 창 (노을은 여기로)
    _win(v, dusk, 0.2, 1.8, 2.49, 1.05, 2.3)
    sf = (0.82, 0.50, 0.42)
    v.box(0.0, 2.0, 1.8, 2.42, 0, 0.32, sf)
    v.box(0.1, 1.9, 1.82, 2.26, 0.32, SOFA_TOP, (0.88, 0.58, 0.48))
    v.box(0.0, 2.0, 2.26, 2.45, SOFA_TOP, 0.95, sf)
    v.box(-0.12, 0.1, 1.8, 2.43, 0.32, 0.7, (0.76, 0.45, 0.38))
    v.box(1.9, 2.12, 1.8, 2.43, 0.32, 0.7, (0.76, 0.45, 0.38))
    # 식탁 + 의자 + 밥상
    X.table(v, -0.1, -0.3, 1.8, 1.0, 0.74, (0.85, 0.72, 0.52))
    X.chair(v, -1.4, -0.3, 0)
    X.chair(v, 1.2, -0.3, 180)
    for x, c in ((-0.6, (0.97, 0.97, 0.95)), (0.0, (0.97, 0.97, 0.95)), (0.5, (0.97, 0.97, 0.95))):
        v.box(x - 0.15, x + 0.15, -0.62, -0.38, 0.74, 0.77, c, jit=0)
        v.box(x - 0.08, x + 0.08, -0.56, -0.44, 0.77, 0.8, (0.95, 0.85, 0.3) if x < 0.3 else (0.45, 0.7, 0.35), jit=0)
    v.box(0.5, 0.62, -0.2, -0.08, 0.74, 0.88, (0.95, 0.6, 0.2))
    v.box(-0.9, -0.7, -0.15, 0.05, 0.74, 0.8, (0.35, 0.55, 0.85))
    # 오른쪽 벽 창, 러그, 액자
    _win(v, dusk, -1.0, 0.8, 2.99, 0.9, 2.3, face=-1, axis="x")
    v.floor(-1.2, 1.4, -1.7, 1.1, (0.78, 0.55, 0.50), 0.5, "check", z=0.012)
    for y, c in ((-1.9, (0.9, 0.55, 0.3)), (-1.2, (0.35, 0.65, 0.55)), (-0.5, (0.95, 0.8, 0.3))):
        v.box(-2.99, -2.97, y, y + 0.5, 1.5, 2.0, (0.95, 0.95, 0.92), jit=0)
        v.box(-2.97, -2.96, y + 0.06, y + 0.44, 1.56, 1.94, c, jit=0)
    if dusk:
        v.light(-0.1, -0.3, 1.9, 90, (1.0, 0.78, 0.5), 0.3, "ep27_hd_pend")
        v.light(2.4, -0.1, 1.7, 130, (1.0, 0.62, 0.38), 0.8, "ep27_hd_win")
        v.light(1.0, 2.38, 1.9, 110, (1.0, 0.65, 0.4), 0.6, "ep27_hd_sofa")
        v.light(0.9, -1.6, 1.5, 70, (1.0, 0.8, 0.62), 0.8, "ep27_hd_fill")
        v.light(-2.3, 1.0, 1.7, 90, (1.0, 0.6, 0.35), 0.6, "ep27_hd_sink")
    else:
        v.light(-0.1, -0.3, 1.9, 50, (1.0, 0.9, 0.75), 0.3, "ep27_ha_pend")
        v.light(2.4, -0.1, 1.7, 120, (0.85, 0.92, 1.0), 0.8, "ep27_ha_win")
        v.light(-1.5, 1.2, 1.8, 40, (1.0, 0.95, 0.85), 0.6, "ep27_ha_kit")
        v.light(0.0, -1.8, 1.6, 40, (1.0, 0.95, 0.88), 0.6, "ep27_ha_fill")


def _school(v):
    """학교 복도: 뒷벽 사물함 줄, 오른쪽 벽 창, 왼쪽 벽 게시판, 뒷벽 시계."""
    v.floor(-4, 4, -3, 3, (0.86, 0.82, 0.70), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, 3.0, (0.93, 0.93, 0.88), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, 3.0, (0.88, 0.90, 0.86), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, 3.0, (0.88, 0.90, 0.86), 0.5, face=1)
    for k, x in enumerate(np.arange(-3.75, 3.7, 0.5)):                              # 사물함
        c = (0.30, 0.52, 0.80) if k % 3 else (0.95, 0.70, 0.25)
        v.box(x, x + 0.46, 2.55, 2.97, 0, 2.0, c)
        for z in (1.62, 1.69, 1.76):
            v.box(x + 0.08, x + 0.38, 2.535, 2.55, z, z + 0.035, DARK, jit=0)
        v.box(x + 0.35, x + 0.39, 2.51, 2.55, 0.95, 1.2, (0.85, 0.86, 0.9), jit=0)
    for y0 in (-2.2, -0.6, 1.0):                                                    # 창 (오른쪽 벽)
        v.window(y0, y0 + 1.2, 3.99, 1.0, 2.4, night=False, face=-1, axis="x")
    v.box(-3.99, -3.96, -1.6, 1.4, 1.0, 2.3, (0.75, 0.55, 0.35))                    # 게시판 + 알록달록 종이
    for k in range(7):
        y = -1.5 + 0.4 * k
        v.box(-3.96, -3.94, y, y + 0.28, 1.3 + 0.35 * (k % 3), 1.62 + 0.35 * (k % 3),
              [(0.95, 0.95, 0.9), (0.95, 0.8, 0.3), (0.5, 0.8, 0.95), (0.95, 0.55, 0.6)][k % 4], jit=0)
    v.box(-0.35, 0.35, 2.94, 2.96, 2.35, 3.0 - 0.05, (0.97, 0.97, 0.95), jit=0)    # 시계
    v.box(-0.02, 0.02, 2.925, 2.94, 2.6, 2.85, DARK, jit=0)
    v.box(-0.02, 0.15, 2.915, 2.925, 2.58, 2.62, DARK, jit=0)
    v.light(0.0, 0.2, 2.6, 130, (0.97, 0.98, 1.0), 0.6, "ep27_sc_l0")
    v.light(-2.4, -0.5, 2.4, 90, (0.97, 0.98, 1.0), 0.6, "ep27_sc_l1")
    v.light(2.4, -0.5, 2.4, 90, (0.97, 0.98, 1.0), 0.6, "ep27_sc_l2")


def _sets():
    return (("room", lambda w: _room(w, "am")), ("home", lambda w: _home(w, "am")), ("school", _school),
            ("room_eve", lambda w: _room(w, "eve")), ("home_dusk", lambda w: _home(w, "dusk")),
            ("room_night", lambda w: _room(w, "night")))


# ───────────────────────── 캐릭터 새 자세 ─────────────────────────
# 새 자세 = (바탕 자세, 오른팔·왼팔 각(어깨에서 앞으로 들기 rad, 음수 = 앞) 또는 None, 손질)
KINDS = {
    "cheer": ("talk", (-2.9, -2.9), ""),             # 두 팔 번쩍
    "hi5R": ("talk", (-2.0, 0.05), ""),              # 오른손 하이파이브
    "hi5L": ("talk", (0.05, -2.0), ""),              # 왼손 하이파이브
    "ladle": ("stand", (-1.25, 0.05), "frown"),      # 오른손을 가슴 높이로 (국자), 입 꾹
    "reach": ("stand", (-2.2, -2.2), ""),            # 두 팔을 앞 위로 (커튼 걷기)
    "wash": ("stand", (-0.8, -0.8), "frown"),        # 설거지, 말을 삼킨 입
    "yell": ("angry", None, "bigmouth"),             # 입을 크게 벌리고 호통
    "pick": ("stand", None, "lean 1.35 -0.1"),       # 허리를 깊이 숙여 줍기
    "tuck": ("stand", None, "lean 0.75 -0.8"),       # 허리를 숙여 이불 덮기
    "lieopen": ("stand", None, "lie"),               # 눈 뜨고 누움
    "sit_talk": ("sit", None, "open"),               # 앉아서 말함
    "sit_smile": ("sit", None, "smile"),             # 앉아서 웃음
    "sit_hug": ("sit", None, "hug smile"),           # 앉아서 왼팔로 옆 사람 어깨를 감쌈, 웃음
    "walk_a_sock": ("walk_a", None, "sock"),         # 짝짝이 양말 신고 걷기
    "walk_b_sock": ("walk_b", None, "sock"),
}
KIND_ORDER = list(KINDS)
ARMS = {"stand": (0.0, 0.0), "sit": (-0.6, -0.6), "sit_phone": (-1.05, -0.6), "sit_conf": (-2.75, -0.6),
        "phone": (-1.05, 0.0), "angry": (-2.5, -2.5), "confused": (-2.75, 0.05), "talk": (-0.9, 0.05),
        "walk_a": (0.35, -0.35), "walk_b": (-0.35, 0.35), "lie": (0.0, 0.0)}
ARMS.update({k: v[1] for k, v in KINDS.items() if v[1]})
SOCKS = ((0.90, 0.20, 0.22), (0.25, 0.55, 0.90))       # 짝짝이 양말: 빨강 · 파랑 (재질 8·9)


def pose_index(name, hair):
    """인스턴스 'pose' 번호: 표준 22개(머리종류*11+자세) 뒤에 새 자세들(머리종류*새자세수+번호)."""
    from engine import voxel as X
    if name in KINDS:
        return 2 * X.NPOSE + hair * len(KINDS) + KIND_ORDER.index(name)
    return hair * X.NPOSE + X.POSES[name]


def _rot_x(bm, ang, pivot):
    """x축(앞) 둘레 회전: 팔을 옆으로 벌림. 왼쪽(+y) 팔은 양수 = 바깥."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        y, z = p.co.y - pivot[1], p.co.z - pivot[2]
        p.co.y, p.co.z = pivot[1] + c * y - s * z, pivot[2] + s * y + c * z
    return bm


def _rot_z(bm, ang, pivot):
    """pivot=(x, y)를 지나는 세로축 둘레 회전 (옆으로 뻗은 팔을 뒤로 돌릴 때)."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        x, y = p.co.x - pivot[0], p.co.y - pivot[1]
        p.co.x, p.co.y = pivot[0] + c * x - s * y, pivot[1] + s * x + c * y
    return bm


def _variant(kind, lh):
    """voxel._person으로 만든 바탕 자세에서 팔(맨 뒤 4조각)·입·몸만 바꾼 [(bmesh, 재질)]. 재질 8·9 = 양말."""
    from engine import bkit as K
    from engine import voxel as X
    base, arms, how = KINDS[kind]
    P = X._person(X.POSES[base], lh)
    hip = 0.47 if base == "sit" else 0.78
    hz = hip + 0.58
    tok = how.split()

    def cube(cx, cy, z0, sx, sy, sz):
        return K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True)

    def arm(sy, ang, roll=0.0, turn=0.0):
        sleeve, hand = cube(0, sy, hip + 0.12, 0.18, 0.16, 0.46), cube(0, sy, hip - 0.02, 0.17, 0.15, 0.14)
        for bm in (sleeve, hand):
            if roll:
                _rot_x(bm, roll, (0, sy, hip + 0.54))
            if turn:
                _rot_z(bm, turn, (0, sy))
            X._rot_y(bm, ang, (0, 0, hip + 0.54))
        return [(sleeve, 0), (hand, 2)]

    def swap(drop, new):
        nonlocal P
        for bm, mi in P:
            if mi == drop:
                bm.free()
        P = [(bm, mi) for bm, mi in P if mi != drop] + new
    if arms:                                           # 팔만 새 각도로
        for bm, _ in P[-4:]:
            bm.free()
        P = P[:-4] + arm(-0.34, arms[0]) + arm(0.34, arms[1])
    if "hug" in tok:                                   # 오른팔은 무릎 위, 왼팔은 옆으로 뻗어 뒤로 감음 (입 부품보다 먼저)
        for bm, _ in P[-4:]:
            bm.free()
        P = P[:-4] + arm(-0.34, -0.6) + arm(0.34, 0.0, roll=1.45, turn=0.2)
    mouth = {"bigmouth": lambda: [(cube(0.232, 0, hz + 0.01, 0.02, 0.17, 0.12), 6)],
             "open": lambda: [(cube(0.232, 0, hz + 0.04, 0.02, 0.13, 0.07), 6)],
             "smile": lambda: [(cube(0.232, 0, hz + 0.04, 0.02, 0.11, 0.028), 6),       # 아랫선 + 양 끝이 올라간 입꼬리
                               (cube(0.232, -0.075, hz + 0.055, 0.02, 0.03, 0.04), 6),
                               (cube(0.232, 0.075, hz + 0.055, 0.02, 0.03, 0.04), 6)],
             "frown": lambda: [(cube(0.232, 0, hz + 0.055, 0.02, 0.13, 0.03), 6),       # 꾹 다문 입 + 내려간 입꼬리
                               (cube(0.232, -0.08, hz + 0.03, 0.02, 0.03, 0.045), 6),
                               (cube(0.232, 0.08, hz + 0.03, 0.02, 0.03, 0.045), 6)]}
    for k in tok:
        if k in mouth:
            swap(6, mouth[k]())
    if "lean" in tok:                                # 허리에서 몸·팔을 숙이고 고개는 들어 앞을 봄
        lean, aw = float(tok[1]), float(tok[2])
        body, arms_ = P[4:-4], P[-4:]
        for bm, _ in arms_:
            X._rot_y(bm, aw - lean, (0, 0, hip + 0.54))
        for bm, _ in body[1:]:
            X._rot_y(bm, -lean * 0.6, (0, 0, hz))
        for bm, _ in body + arms_:
            X._rot_y(bm, lean, (0, 0, hip))
    elif "lie" in tok:                                 # 선 모습을 뒤로 눕힘: 발끝이 원점, 머리는 -x, 얼굴은 위
        for bm, _ in P:
            X._rot_y(bm, -math.pi / 2, (0, 0, 0))
            X._shift(bm, dz=0.24)
    elif "sock" in tok:
        swing = 0.42 if base == "walk_a" else -0.42
        for (sy, sg), mi in (((-0.11, 1), 8), ((0.11, -1), 9)):
            P.append((X._rot_y(cube(0, sy, 0.09, 0.235, 0.215, 0.26), sg * swing, (0, 0, hip)), mi))
    return P


def _lean_head(lean):
    """숙인 자세의 머리 꼭대기 (앞, 높이): 고개를 lean*0.6 젖힌 뒤 허리(0.78)에서 lean만큼 숙임."""
    hb, cl, sl = -lean * 0.6, math.cos(lean), math.sin(lean)
    dx, dz = math.sin(hb) * 0.5, 0.58 + math.cos(hb) * 0.5
    return cl * dx + sl * dz, 0.78 - sl * dx + cl * dz


HEAD_TOP = {"pick": _lean_head(1.35), "tuck": _lean_head(0.75)}      # 선/앉은 자세가 아닌 것들의 머리 꼭대기 (앞, 높이)


def rel(d, fwd, lat, up):
    """캐릭터 기준 (앞, 왼쪽, 위) → 세트 좌표. 크기 반영."""
    a = math.radians(d["yaw"])
    s = d["scale"]
    return (d["x"] + s * (fwd * math.cos(a) - lat * math.sin(a)), d["y"] + s * (fwd * math.sin(a) + lat * math.cos(a)),
            d["z"] + s * up)


def head_pt(d):
    """머리 꼭대기 한가운데(세트 좌표) — 말풍선 꼬리가 닿는 곳."""
    fw, hh = HEAD_TOP.get(d["pose"], (0.0, 1.55 if d["pose"].startswith("sit") else 1.86))
    return rel(d, fw, 0.0, hh)


def hand_pt(d, side, reach=0.0):
    """side 'R'(캐릭터 오른손)·'L' 손 끝 근처 점 (서 있거나 앉은 자세용). reach = 팔 방향으로 더 나간 거리."""
    ang = ARMS[d["pose"]][0 if side == "R" else 1]
    dd = 0.49 + reach
    hip = 0.47 if d["pose"].startswith("sit") else 0.78
    return rel(d, -dd * math.sin(ang), -0.34 if side == "R" else 0.34, hip + 0.54 - dd * math.cos(ang))


# ───────────────────────── 캐릭터 배치·움직임 ─────────────────────────
def at(st, x, y, yaw, pose, z=0.0, **kw):
    return dict(set=st, x=x, y=y, yaw=yaw, pose=pose, z=z, **kw)


def mover(keys, st, step=0.3, walk=("walk_a", "walk_b"), end="stand", face=None, z=0.0, bob=0.02):
    """keys = [(줄 안 시각, x, y), ...]를 직선으로 이으며 걷는 함수(over용). 걷는 동안엔 step초마다 발걸음 자세를 바꾸고,
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
            return at(st, x, y, head, walk[int(tl / step) % 2], z + bob * abs(math.sin(math.pi * tl / step)))
        return at(st, x, y, head if face is None else face, end, z)
    return fn


def _k_free(tl, du, u):
    """침대 위에서 두 팔 번쩍 폴짝폴짝 (매트리스라 통통)."""
    return at("room", BED_X, 1.3, -90, "cheer", BED_TOP + 0.30 * abs(math.sin(math.pi * tl / 0.7)))


def _k_quiet(tl, du, u):
    """게임하다 조용해진 방: 문 쪽을 한번 힐끔 돌아봤다 돌아옴."""
    g = ramp(tl, 0.9, 1.15) * (1 - ramp(tl, 1.7, 1.95))
    return at("room_eve", BED_X, 0.75, -90 + 60 * g, "sit_phone", 0.05)


def _m_flap(tl, du, u):
    return dict(pose="yell" if int(tl / 0.13) % 2 == 0 else "angry")


_M_CURTAIN = mover([(0.0, 1.15, 2.3), (0.8, 2.3, 2.2), (1.55, 2.3, 2.2), (2.7, 1.3, 2.3)], "room", end="reach", face=90)
_M_ENTER = mover([(0.15, 1.3, 2.35), (1.15, 1.1, 0.45)], "room_eve", face=-90)
_M_SNEAK = mover([(0.0, 1.3, 3.2), (0.5, 1.3, 3.2), (1.1, 1.3, 2.45), (2.0, 1.05, 1.6)], "room_night", step=0.45, face=180)
_M_OUT = mover([(1.35, 1.05, 1.6), (1.9, 1.3, 2.3), (2.8, 1.3, 3.5)], "room_night")


def _m_bag(tl, du, u):
    """문에서 들어와 던져 둔 가방 앞에서 허리를 숙여 줍고, 가방을 든 채 한숨."""
    if tl < 1.15:
        return _M_ENTER(tl, du, u)
    return at("room_eve", 1.1, 0.45, -90, "pick" if tl < 1.9 else "stand")


def _m_wash(tl, du, u):
    """설거지하다 방 쪽을 흘끔흘끔."""
    g = ramp(tl, 0.8, 1.05) * (1 - ramp(tl, 1.35, 1.6)) + ramp(tl, 1.75, 1.95) * (1 - ramp(tl, 2.2, 2.4))
    return at("home_dusk", -1.9, 0.95, 180 + 75 * g, "wash")


def _m_tuck(tl, du, u):
    """침대 곁에서 허리를 숙여 이불을 덮어 주고, 말없이 문으로 나감."""
    if tl < 1.35:
        return at("room_night", 1.05, 1.6, 180, "tuck")
    return _M_OUT(tl, du, u)


def _m_storm(tl, du, u):
    return at("room_night", 1.15, 2.3, -130, "yell" if int(tl / 0.13) % 2 == 0 else "angry")


_CAST = []


def cast():
    """[dict(tag, set, x, y, z, yaw, pose, hair, shirt, pants, scale, over={줄: dict 또는 함수(tl, du, u)}, only=보이는 줄 집합)]"""
    if _CAST:
        return _CAST
    from engine import voxel as X
    L = LN
    C = _CAST

    def add(tag, st, x, y, yaw, pose, hair, shirt, pants, scale=1.0, z=0.0, over=None, only=None):
        C.append(dict(tag=tag, set=st, x=x, y=y, yaw=yaw, pose=pose, hair=hair, shirt=shirt, pants=pants, scale=scale,
                      z=z, over=over or {}, only=only))
    n = len(LINES)
    sofa_kid = SOFA_TOP - 0.36 * KID_S
    # ── 아이 (노란 셔츠): 침대에서 눈만 내밀고 → 앉아 멍 → 두 팔 번쩍 → 양말 짝짝이로 식탁 앞을 휙 → 학교 → 게임 → 밤 → 소파
    add("kid", "room", BED_X, 0.77, -90, "lieopen", 0, KID_SH, KID_PA, KID_S, BED_TOP, only=set(range(n)) - {L["lips"], L["swallow"]},
        over={L["silent"]: at("room", 0.5, 1.25, 0, "sit_conf", 0.05), L["free"]: _k_free,
              L["socks"]: mover([(0.0, -2.0, -1.2), (2.7, 2.1, -1.2)], "home", step=0.17, walk=("walk_a_sock", "walk_b_sock")),
              L["school"]: mover([(0.0, -1.75, 0.3), (0.9, -0.5, 0.3)], "school", step=0.28, end="hi5R", face=0),
              L["game"]: at("room_eve", BED_X, 0.75, -90, "sit_phone", 0.05),
              L["bag"]: at("room_eve", BED_X, 0.75, -90, "sit_phone", 0.05), L["quiet"]: _k_quiet,
              L["zero"]: at("room_eve", BED_X, 0.75, -90, "sit", 0.05),
              L["empty"]: at("room_night", BED_X, 0.77, -90, "lieopen", BED_TOP),
              L["sneak"]: at("room_night", BED_X, 0.77, -90, "lieopen", BED_TOP),
              L["tuck"]: at("room_night", BED_X, 0.77, -90, "lie", BED_TOP),
              L["confess"]: at("room_night", BED_X, 0.75, -90, "sit_talk", 0.05),
              L["storm"]: at("room_night", BED_X, 0.75, -90, "sit", 0.05),
              L["smile"]: at("room_night", BED_X, 0.75, -90, "sit_smile", 0.05),
              L["hug"]: at("home_dusk", 1.45, 2.0, -90, "sit_smile", sofa_kid),
              L["ask"]: at("home_dusk", 1.45, 2.0, -90, "sit_smile", sofa_kid)})
    # ── 엄마 (분홍 셔츠·긴 머리): 문가 호통(말풍선은 빈 …) → 커튼만 걷고 → 입술 꾹 → 가방 줍고 → 설거지 → 살금살금 → 폭풍 → 소파
    add("mom", "room", 1.15, 2.3, -90, "yell", 1, MOM_SH, MOM_PA, 1.0, 0.0,
        only={L[k] for k in ("hook", "morning", "silent", "socks", "lips", "bag", "swallow", "sneak", "tuck", "confess",
                             "storm", "smile", "hug", "ask")},
        over={L["morning"]: _m_flap, L["silent"]: _M_CURTAIN,
              L["socks"]: at("home", -0.55, 0.65, -90, "ladle"), L["lips"]: at("home", -0.55, 0.65, -90, "ladle"),
              L["bag"]: _m_bag, L["swallow"]: _m_wash, L["sneak"]: _M_SNEAK, L["tuck"]: _m_tuck,
              L["confess"]: at("room_night", 1.15, 2.3, -130, "stand"), L["storm"]: _m_storm, L["smile"]: _m_storm,
              L["hug"]: at("home_dusk", 0.9, 2.0, -90, "sit_hug", SOFA_TOP - 0.36),
              L["ask"]: at("home_dusk", 0.9, 2.0, -90, "sit_hug", SOFA_TOP - 0.36)})
    # ── 학교 복도: 친구와 엑스트라 (아이는 위에서 걸어와 하이파이브)
    sc = {L["school"]}
    add("friend", "school", 0.5, 0.3, 180, "stand", 0, FRI_SH, FRI_PA, KID_S, only=sc,
        over={L["school"]: mover([(0.0, 1.75, 0.3), (0.9, 0.5, 0.3)], "school", step=0.28, end="hi5L", face=180)})
    rs = np.random.default_rng(27)
    ex = [("walk", [(0.0, 3.6, -1.5), (6.0, -3.6, -1.5)], 1), ("walk", [(0.0, -3.6, -2.2), (7.0, 3.6, -2.2)], 0),
          ("walk", [(0.0, 3.6, 1.3), (8.0, -3.6, 1.3)], 0), ("walk", [(0.0, -3.8, 1.9), (9.0, 3.8, 1.9)], 1),
          ("talk", (-2.7, 2.1, -80), 1), ("stand", (-2.0, 2.1, -105), 0), ("phone", (2.2, 2.1, -95), 0),
          ("talk", (3.1, 0.4, 180), 1), ("stand", (3.1, -0.3, 180), 0), ("stand", (-3.3, -0.2, -20), 1)]
    for k, (kind, p, hair) in enumerate(ex):
        sh, pa = X.SHIRTS[int(rs.integers(len(X.SHIRTS)))], X.PANTS[int(rs.integers(len(X.PANTS)))]
        if kind == "walk":
            add("ex%d" % k, "school", p[0][1], p[0][2], 0, "stand", hair, sh, pa, 0.95, only=sc,
                over={L["school"]: mover(p, "school", step=0.35)})
        else:
            add("ex%d" % k, "school", p[0], p[1], p[2], kind, hair, sh, pa, 0.95, only=sc)
    return C


# ───────────────────────── 소품 (일반 상자 fx · 발광 상자 glow) ─────────────────────────
# 상자 = (중심, 크기, 회전(라디안), 색) — 세트 좌표
DOOR_COL, QUILT, HEM = (0.62, 0.45, 0.30), (0.35, 0.50, 0.82), (0.93, 0.95, 0.99)


def _xf(p, rz, off):
    """p에서 방향 rz(라디안)로 돌려 놓은 물건의 몸 기준 (앞, 왼쪽, 위) 오프셋 → 세트 좌표."""
    c, s = math.cos(rz), math.sin(rz)
    return p[0] + off[0] * c - off[1] * s, p[1] + off[0] * s + off[1] * c, p[2] + off[2]


def quilt(edge, shake=0.0, ph=0.0, top=0.89):
    """아이 몸 위 이불: 침대 폭 전체를 덮는 납작한 층 + 몸을 덮는 두둑한 언덕(edge = 머리 쪽 끝 y) + 하얀 접힌 단."""
    sx, sz = shake * math.sin(ph * 9.0), shake * math.cos(ph * 11.0)
    by = max(edge - 0.3, 0.8)
    return [((BED_X + sx, (0.56 + by) / 2, BED_TOP + 0.10), (1.30, by - 0.56, 0.20), (0, 0, 0), QUILT),
            ((BED_X + sx, (0.62 + edge) / 2, (0.64 + top) / 2 + sz), (0.80, edge - 0.62, top - 0.64), (0, 0, 0), QUILT),
            ((BED_X + sx, edge - 0.05, top + sz), (0.82, 0.10, 0.03), (0, 0, 0), HEM)]


def pile(extra=0.0):
    """앉은 아이 뒤쪽(침대 머리 쪽)에 뭉쳐 둔 이불."""
    return [((BED_X, 1.55, BED_TOP + 0.11), (1.25, 0.85, 0.22), (0, 0, 0), QUILT),
            ((BED_X - 0.1, 1.95, BED_TOP + 0.25 + extra), (0.8, 0.5, 0.18), (0, 0, 0.25), (0.42, 0.58, 0.88))]


def curtain(k):
    """아침 창 커튼 (k 0 = 닫힘 · 1 = 활짝 걷음)."""
    w = 0.55 - 0.35 * k
    return [((1.9 + w / 2, 2.43, 1.6), (w, 0.06, 1.5), (0, 0, 0), (0.85, 0.45, 0.42)),
            ((2.95 - w / 2, 2.40, 1.6), (w, 0.06, 1.5), (0, 0, 0), (0.80, 0.42, 0.40))]


def door(phi):
    """문짝: 경첩(문 오른쪽)에서 복도 쪽(+y)으로 phi 라디안 열림 (0 = 닫힘). 열린 문짝이 방에서 보는 엄마를 가리지 않게."""
    w, t, h = DOOR[1] - DOOR[0] - 0.02, 0.05, 2.08
    hx, hy = DOOR[1] - 0.01, 2.44
    dx, dy = -math.cos(phi), math.sin(phi)
    rz = math.atan2(dy, dx)
    k = (hx + dx * (w - 0.1) + dy * 0.05, hy + dy * (w - 0.1) - dx * 0.05, 1.0)
    return [((hx + dx * w / 2, hy + dy * w / 2, h / 2), (w, t, h), (0, 0, rz), DOOR_COL),
            (k, (0.07, 0.07, 0.07), (0, 0, rz), (0.95, 0.8, 0.3))]


def backpack(p, rz, flat=False, col=(0.85, 0.25, 0.25)):
    """책가방 (p = 가운데, flat이면 등을 대고 누움)."""
    dk = tuple(c * 0.75 for c in col)
    if flat:
        return [(_xf(p, rz, (0, 0, 0.09)), (0.36, 0.44, 0.18), (0, 0, rz), col),
                (_xf(p, rz, (0, 0.0, 0.2)), (0.28, 0.3, 0.06), (0, 0, rz), dk),
                (_xf(p, rz, (0.19, 0, 0.1)), (0.03, 0.4, 0.1), (0, 0, rz), (0.15, 0.15, 0.17))]
    return [(_xf(p, rz, (0, 0, 0)), (0.18, 0.36, 0.44), (0, 0, rz), col),
            (_xf(p, rz, (0.1, 0, -0.06)), (0.06, 0.28, 0.2), (0, 0, rz), dk),
            (_xf(p, rz, (0, 0, 0.24)), (0.1, 0.1, 0.05), (0, 0, rz), (0.15, 0.15, 0.17))]


def worn_pack(d):
    """등에 멘 책가방 + 어깨끈 (d = 캐릭터)."""
    s = d["scale"]
    rz = math.radians(d["yaw"])
    out = [(rel(d, -0.24, 0, 1.06), (0.2 * s, 0.42 * s, 0.52 * s), (0, 0, rz), (0.85, 0.25, 0.25)),
           (rel(d, -0.36, 0, 1.0), (0.07 * s, 0.34 * s, 0.22 * s), (0, 0, rz), (0.65, 0.15, 0.18))]
    for sy in (-0.2, 0.2):
        out.append((rel(d, 0.02, sy, 1.08), (0.32 * s, 0.05 * s, 0.48 * s), (0, 0, rz), (0.15, 0.15, 0.17)))
    return out


def snack(p, rz, col=(0.9, 0.25, 0.2)):
    """과자 봉지 (서 있음)."""
    return [(_xf(p, rz, (0, 0, 0.14)), (0.05, 0.2, 0.27), (0, 0, rz), col),
            (_xf(p, rz, (0.03, 0, 0.14)), (0.02, 0.14, 0.1), (0, 0, rz), (1.0, 0.85, 0.25)),
            (_xf(p, rz, (0, 0, 0.28)), (0.06, 0.22, 0.03), (0, 0, rz), tuple(c * 0.7 for c in col))]


def ladle(d, t):
    """엄마 오른손에 쥔 국자: 긴 손잡이 + 아래쪽 국물 뜨는 부분. 파르르 떨림."""
    hx, hy, hz = hand_pt(d, "R", 0.08)
    j = 0.012
    jx, jy = j * math.sin(2 * math.pi * 19 * t), j * math.cos(2 * math.pi * 23 * t)
    return [((hx + jx, hy + jy, hz + 0.10), (0.035, 0.035, 0.46), (0.07 * math.sin(2 * math.pi * 17 * t), 0, 0), (0.78, 0.8, 0.84)),
            ((hx + jx, hy + jy, hz - 0.14), (0.13, 0.13, 0.07), (0, 0, 0), (0.78, 0.8, 0.84))]


def steam(x, y, z0, t, n=5, rise=0.55):
    """김: 하얀 작은 상자가 솟아 오르며 작아짐."""
    out = []
    for k in range(n):
        p = (k / n + t / 1.5) % 1.0
        s = 0.075 * (1 - 0.6 * p)
        out.append(((x + 0.06 * math.sin(6.3 * (p + k * 0.37)), y + 0.04 * math.cos(6.3 * (p + k * 0.21)), z0 + rise * p),
                    (s, s, s), (p * 3, k, p * 2), (0.97, 0.97, 0.98)))
    return out


def sparkles(c, tl, t0, n=14, r=0.9, life=0.9, cols=((1.0, 0.85, 0.3), (1.0, 0.6, 0.75), (1.0, 1.0, 0.9))):
    """c 둘러싸고 터져 나가는 발광 반짝이."""
    out = []
    tau = tl - t0
    if tau <= 0 or tau > life:
        return out
    f = tau / life
    for k in range(n):
        a = 2 * math.pi * k / n + 0.7 * (k % 3)
        rr = r * (0.35 + 0.65 * ((k * 5) % 7) / 6.0) * math.sqrt(f)
        s = 0.11 * (1 - f) * (1 + 0.5 * (k % 2))
        out.append(((c[0] + rr * math.cos(a), c[1] + 0.15 * math.sin(a * 2), c[2] + rr * math.sin(a) * 0.9 + 0.15),
                    (s, s, s), (a, f * 4, 0), cols[k % len(cols)]))
    return out


def motes(box, t, n=12, col=(1.0, 0.9, 0.6)):
    """빛 속에 떠다니는 먼지: box = (x0, x1, y0, y1, z0, z1)."""
    out = []
    for k in range(n):
        q = ((k * 0.6180339) % 1.0, (k * 0.3819660 + 0.2) % 1.0, (k * 0.7548777 + 0.4) % 1.0)
        x = box[0] + (box[1] - box[0]) * q[0] + 0.08 * math.sin(0.9 * t + 6.3 * q[1])
        y = box[2] + (box[3] - box[2]) * q[1] + 0.06 * math.sin(0.7 * t + 6.3 * q[2])
        z = box[4] + (box[5] - box[4]) * ((q[2] - 0.05 * t) % 1.0)
        out.append(((x, y, z), (0.03, 0.03, 0.03), (k, 0.3 * k, 0), col))
    return out


def props(i, tl, du, u, A, t):
    """줄 i의 소품 (일반 상자 F, 발광 상자 G) — 세트 좌표."""
    F, G = [], []
    kid, mom, fr = A["kid"], A["mom"], A["friend"]
    L = LN
    if i in (L["hook"], L["morning"], L["silent"], L["free"]):          # 아침 방
        if i == L["hook"]:
            F += quilt(2.095)
        elif i == L["morning"]:
            F += quilt(2.45, shake=0.03, ph=tl * 6.0, top=0.93)
        elif i == L["silent"]:
            F += pile()
        else:
            F += pile() + [((-1.55, 0.95, 0.12), (0.6, 0.85, 0.24), (0, 0, 0.4), QUILT)]
        k = 0.0 if i in (L["hook"], L["morning"]) else (ramp(tl, 0.95, 1.5) if i == L["silent"] else 1.0)
        F += curtain(k) + door(1.5)
        if i == L["silent"]:
            G += motes((1.8, 2.9, 0.4, 2.3, 0.3, 2.2), t, 12) if k > 0.5 else []
        if i == L["free"]:
            G += sparkles((BED_X, 1.3, 1.9), tl, 0.05, 16, 1.0, 1.2) + sparkles((BED_X, 1.3, 1.9), tl, 1.25, 16, 1.0, 1.2)
    elif i in (L["socks"], L["lips"]):                                    # 아침 식탁: 국솥 김 + 엄마가 쥔 국자
        F += steam(-1.05, 2.2, 1.2, t) + ladle(mom, t)
    elif i == L["school"]:
        F += worn_pack(kid) + worn_pack(fr)
        G += sparkles((0.0, 0.3, 1.45), tl, 0.95, 12, 0.55, 0.6)
    elif i in (L["game"], L["bag"], L["quiet"], L["zero"]):              # 저녁 방
        F += pile(0.02) + snack((0.3, 1.0, BED_TOP + 0.01), math.radians(-60))
        F += [((0.1, 0.55, BED_TOP + 0.02), (0.07, 0.05, 0.02), (0, 0, 0.5), (1.0, 0.82, 0.3)),
              ((-0.55, 0.6, BED_TOP + 0.02), (0.06, 0.05, 0.02), (0, 0, 1.0), (1.0, 0.82, 0.3))]
        F += door(1.5)
        if i == L["bag"]:                                                 # 던져 둔 가방 → 엄마가 줍는다
            rz = math.radians(-40)
            floor = (1.15, -0.15, 0.0)
            if tl < 1.15:
                F += backpack(floor, rz, True)
            else:
                hand = rel(mom, 0.55, 0.0, 0.25)
                side = rel(mom, 0.02, -0.4, 0.48)
                k = ramp(tl, 1.5, 1.95)
                p = tuple(hand[j] + (side[j] - hand[j]) * k for j in range(3))
                if tl < 1.45:
                    p = tuple(floor[j] + (hand[j] - floor[j]) * ramp(tl, 1.15, 1.45) for j in range(3))
                F += backpack(p, rz, tl < 1.3)
            F += [((0.85, -0.55, 0.015), (0.2, 0.13, 0.03), (0, 0, 0.7), (0.95, 0.95, 0.9)),       # 쏟아진 공책·필통
                  ((1.45, -0.35, 0.02), (0.17, 0.05, 0.04), (0, 0, 0.3), (0.3, 0.6, 0.9))]
            if tl > 2.0:                                                  # 한숨 김
                mx, my, mz = rel(mom, 0.25, 0.0, 1.45)
                for k in range(3):
                    p = ((tl - 2.0) * 0.8 + k * 0.33) % 1.0
                    F.append(((mx + 0.3 * p, my - 0.1 * p, mz + 0.12 * p), (0.07 * (1 - p), 0.07 * (1 - p), 0.07 * (1 - p)),
                              (0, 0, 0), (0.95, 0.95, 0.98)))
    elif i == L["swallow"]:                                               # 설거지: 왼쪽 벽 싱크대의 물줄기·거품
        F += [((-2.43, 0.95, 0.99), (0.03, 0.03, 0.14), (0, 0, 0), (0.6, 0.8, 1.0))]
        for k in range(6):
            p = (k / 6 + t / 1.8) % 1.0
            F.append(((-2.85 + 0.3 * ((k * 3) % 5) / 4, 0.7 + 0.1 * k, 0.96 + 0.4 * p), (0.06, 0.06, 0.06), (k, p, 0), (0.98, 0.98, 1.0)))
    elif i in (L["empty"], L["sneak"], L["tuck"], L["confess"], L["storm"], L["smile"]):     # 밤 방
        if i in (L["empty"], L["sneak"]):
            F += quilt(1.7)
        elif i == L["tuck"]:
            F += quilt(1.7 + 0.28 * ramp(tl, 0.25, 1.1))
        else:
            F += pile()
        phi = 0.0 if i == L["empty"] else (1.45 * ramp(tl, 0.1, 0.7) if i == L["sneak"] else 1.45)
        F += door(phi)
    elif i == L["ask"]:
        G += motes((0.0, 2.2, 0.5, 2.3, 0.3, 2.3), t, 14, (1.0, 0.8, 0.5))
    return F, G


# ───────────────────────── 말풍선 배치 ─────────────────────────
N_FX, N_GL, N_B = 48, 40, 8              # 소품(일반)·소품(발광)·말풍선 인스턴스 개수 (프레임마다 같은 길이로 넘김)


def bb(who, name, t0, ox, oz, cpx=8.0, **kw):
    """말풍선 한 개: 누구 머리 위 · 그림 · 뜨는 때(줄 시작 후 초, 음수 = 이미 떠 있음) · 꼬리 끝 위치(머리 꼭대기에서 오른쪽·위로 몇 칸)
    · 한 칸이 화면에서 차지하는 픽셀 · life(초, 지나면 쏙 사라짐) · swell(천천히 부풀다 쏙) · typing(점이 하나씩 늘어남)."""
    return dict(who=who, name=name, t0=t0, off=(ox, oz), cpx=cpx, **kw)


BUB = {
    LN["hook"]: [bb("mom", "dots3", -1.0, -40, -20, 10.0)],
    LN["morning"]: [bb("mom", "wake", 0.2, -22, -14, 7.5), bb("mom", "late", 0.7, -34, 14, 7.5),
                    bb("mom", "sock", 1.2, -10, 24, 7.5), bb("mom", "wash", 1.7, -30, 42, 7.5)],
    LN["silent"]: [bb("mom", "dots3", 0.1, 0, 4, 9.0)],
    LN["socks"]: [bb("mom", "anger", 0.3, 14, 4, 8.0)],
    LN["lips"]: [bb("mom", "anger", 0.15, 16, 0, 9.0)],
    LN["bag"]: [bb("mom", "dots3", 2.0, 4, 2, 9.0, typing=True)],
    LN["swallow"]: [bb("mom", "excl", 0.3, 4, 2, 11.0, life=0.8, swell=True), bb("mom", "excl", 1.35, 4, 2, 11.0, life=0.8, swell=True)],
    LN["zero"]: [bb("kid", "zero", 0.15, 0, 4, 11.0)],
    LN["confess"]: [bb("mom", "excl", 0.8, 0, 2, 8.0)],
    LN["storm"]: [bb("mom", "hw", 0.0, -20, -10, 7.0), bb("mom", "time", 0.3, -34, 14, 7.0), bb("mom", "game", 0.6, -12, 30, 7.0),
                  bb("mom", "sleep", 0.9, -36, 46, 7.0), bb("mom", "fast", 1.2, -8, 56, 7.0), bb("mom", "light", 1.5, -30, 72, 7.0)],
    LN["smile"]: [bb("mom", n, 0.35 * k, -20 - 14 * (k % 2), -4 + 17 * k, 6.5, life=1.4)
                  for k, n in enumerate(("hw", "time", "game", "sleep", "fast", "light"))],
    LN["hug"]: [bb("mom", "heart", 0.3, 18, 0, 9.0)],
    LN["ask"]: [bb("mom", "heart", -1.0, 18, 0, 9.0)],
}


def bubbles(i, tl, t, A, cam):
    """줄 i의 말풍선 → [(꼬리 끝 위치(월드), 회전, 크기 배율, 그림 번호)]. 카메라 쪽을 보게 돌리고, 화면에서 한 칸이 일정 픽셀이 되게 키움."""
    tgt, az, el, dist, lens, loc = cam
    right, up = cam_axes(az, el)
    out = []
    for k, sp in enumerate(BUB.get(i, ())):
        d = A[sp["who"]]
        s0 = bub_scale(sp, tl)
        if s0 <= 0.0 or not d["show"]:
            continue
        hx, hy, hz = head_pt(d)
        ox, oy = OFF[d["set"]]
        a = (hx + ox, hy + oy, hz)
        cell = sp["cpx"] * math.dist(a, loc) / (lens * 80.0)         # 한 칸의 월드 크기(m): 1920px 높이 / 센서 24mm = 80px/mm
        sx, sz = sp["off"]
        p = [a[j] + right[j] * sx * cell + up[j] * sz * cell for j in range(3)]
        p[2] += 0.01 * math.sin(2 * math.pi * 0.8 * t + 1.7 * k)
        roll = 0.035 * math.sin(2 * math.pi * 0.9 * t + k)
        s = cell / C0 * s0
        name = sp["name"]
        if sp.get("typing"):
            name = "dots%d" % (1 + min(2, int(max(tl - sp["t0"], 0.0) / 0.3)))
        elif name == "anger":
            roll += 0.12 * math.sin(2 * math.pi * 12 * t)
        elif name == "heart":
            s *= 1 + 0.09 * max(0.0, math.sin(2 * math.pi * 1.7 * t + k)) ** 2
        out.append((tuple(p), (roll, 0.0, math.atan2(loc[1] - p[1], loc[0] - p[0])), s, BUB_IX[name]))
    return out


# ───────────────────────── 한 프레임 ─────────────────────────
def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·말풍선·소품 점 배열, 카메라, 조명."""
    i = line_at(t)
    a, b = shot_span(i)
    du = max(b - a, 1e-3)
    tl = max(t - a, 0.0)
    u = min(tl / du, 1.0)
    shot = LINES[i]["shot"]
    cam = cam_pose(shot, u)
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
    F, G = props(i, tl, du, u, A, t)
    o = OFF[shot[0]]

    def shift(items):
        return [((p[0] + o[0], p[1] + o[1], p[2]), s, r, c) for p, s, r, c in items]
    bub = bubbles(i, tl, t, A, cam)
    return dict(O, i=i, tl=tl, u=u, set=shot[0], cam=cam, fx=shift(F), glow=shift(G), env=env(i, tl, du),
                BP=[q[0] for q in bub], BR=[q[1] for q in bub], BS=[q[2] for q in bub], BPO=[q[3] for q in bub])


def _mat_glow(name, strength=3.0):
    """인스턴스 'col' 색으로 빛나는 재질 (반짝이·먼지)."""
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
    v = X.Vox(27)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep27_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    mats = X.people_mats()
    socks = [K.mat_simple("ep27_m_sock%d" % n, c, 0.8) for n, c in enumerate(SOCKS)]
    protos = X.people_protos(ctx, mats)
    for lh in (False, True):
        for kind in KIND_ORDER:
            protos.append(K.proto(ctx, "ep27_p_%s_%d" % (kind, int(lh)), K.join_bms(_variant(kind, lh)),
                                  mats + socks if "sock" in kind else mats))
    C = cast()
    people = K.instancer_multi(ctx, "ep27_people", protos, len(C))
    # 말풍선: 그림마다 원형 하나(판+꼬리+도트 글자), 점마다 'pose'로 그림을 고름. 재질은 전부 같은 목록.
    bmats = [K.mat_simple("ep27_m_bub", (0.97, 0.97, 0.95), 0.6, emit=(1.0, 1.0, 1.0), estr=0.45),
             K.mat_simple("ep27_m_bord", (0.07, 0.08, 0.13), 0.8)]
    for n, ch in enumerate(PAL_ORDER):
        col = tuple(float(c) for c in PAL[ch])
        bmats.append(K.mat_simple("ep27_m_ico_%d" % n, col, 0.5, emit=None if ch == "K" else col, estr=0.9))
    bub = K.instancer_multi(ctx, "ep27_bub", [K.proto(ctx, "ep27_p_bub_" + n, K.join_bms(_bub_parts(K, n)), bmats)
                                              for n in BUB_NAMES], N_B)
    try:
        bub.visible_shadow = False
    except AttributeError:
        pass
    fx = K.instancer(ctx, "ep27_fx", K.proto(ctx, "ep27_p_fx", K.bm_cube(1, 1, 1), [K.mat_inst("ep27_m_fx", 0.7)]), N_FX,
                     vector_scale=True)
    gl = K.instancer(ctx, "ep27_glow", K.proto(ctx, "ep27_p_glow", K.bm_cube(1, 1, 1), [_mat_glow("ep27_m_glow")]), N_GL,
                     vector_scale=True)

    def boxes(ob, items, cap):
        Pp, Ss, Rr, Cc = (np.zeros((cap, 3), np.float32) for _ in range(4))
        for k, (p, s, r, c) in enumerate(items[:cap]):
            Pp[k], Ss[k], Rr[k], Cc[k] = p, s, r, c
        K.set_points(ob, Pp, scale=(Ss[:, 0] > 0).astype(np.float32), size=Ss, rot=Rr, col=Cc)

    def upd(t, f):
        S = frame_state(t)
        tgt, az, el, dist, lens, _ = S["cam"]
        cam.set(tgt, az, el, dist, lens)
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
        n = len(S["BS"])
        BP, BR, BS, BPO = (np.zeros((N_B, 3), np.float32), np.zeros((N_B, 3), np.float32), np.zeros(N_B, np.float32),
                           np.zeros(N_B, np.float32))
        if n:
            BP[:n], BR[:n], BS[:n], BPO[:n] = S["BP"][:N_B], S["BR"][:N_B], S["BS"][:N_B], S["BPO"][:N_B]
        K.set_points(bub, BP, scale=BS, rot=BR, pose=BPO)
        boxes(fx, S["fx"], N_FX)
        boxes(gl, S["glow"], N_GL)

    ctx.on_frame(upd)
