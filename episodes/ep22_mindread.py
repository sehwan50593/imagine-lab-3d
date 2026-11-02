"""EP22 만약에 속마음이 머리 위에 보인다면? (19·20편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
거리 말풍선 훅 → 내 눈에 보이기 시작(파란 후드 '나') → 면접관 머리 위 쿨쿨(면접자 시점) → 소개팅 둘 다 하트
→ 회의 중 웃는 부장님 머리 위 화남 표시 → 선물 받고 "고마워" 하는 친구 머리 위 물음표 → 중고거래 서로 돈 표시
→ 사람들이 모자를 쓰기 시작·모자 가게 줄 → 반전: 사람의 생각은 하루 약 6,200번 바뀐다(말풍선이 쉴 새 없이 바뀜)
→ 늘 무뚝뚝한 아빠 머리 위엔 늘 내 얼굴(안 바뀌는 말풍선) → 지금 당신 머리 위엔?
근거(설명란): Tseng & Poppenk 2020, Nature Communications — 하루 약 6,200번(연구진 추정, fMRI 뇌 상태 전환 기준).
특수효과: 말풍선 = 머리 꼭대기 위 흰 판(검은 테두리·꼬리 블록) + 작은 블록으로 그린 픽셀 그림(7x6 하트 등 14종)을
instancer_multi 점 하나씩으로 띄우고 카메라 쪽으로 돌림(빌보드). 줄마다 그림이 바뀌고 톡 튀어나오는 크기(easeOutBack).
모자도 점 인스턴스: 위에서 떨어져 얹히면 말풍선을 덮고, 반전 줄에서 위로 날아가며 말풍선이 쉴 새 없이 바뀜.
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
OFF = {"street": (0, 0), "interview": (300, 0), "cafe": (600, 0), "office": (900, 0),
       "home_am": (1200, 0), "home_pm": (1500, 0)}
NAMES = ("hook", "world", "int_a", "int_b", "date_a", "date_b", "meet_a", "meet_b", "gift_a", "gift_b",
         "deal_a", "deal_b", "hat_a", "hat_b", "tw_a", "tw_b", "tw_c", "dad_a", "dad_b", "dad_c", "end")
IX = {n: k for k, n in enumerate(NAMES)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 속마음이 머리 위에 보인다면 어떻게 될까요?", gap=0.7,
         shot=("street", (0.0, 3.85, 2.0), -88, 6, 8.0, 26, 0.93, 3)),
    dict(say="어느 날부터, 속마음이 머리 위에 떠요", shot=("street", (-0.02, 3.85, 1.9), -90, 5, 4.2, 28, 0.9, 0)),
    dict(say="면접관이 환하게 웃으며 끄덕여요", shot=("interview", (0.0, 1.15, 1.3), -90, 8, 5.0, 26, 0.92, 2)),
    dict(say="그런데 머리 위엔 쿨쿨이 떠 있었죠", shot=("interview", (0.0, 1.15, 1.5), -90, 6, 4.9, 26, 0.95, -2)),
    dict(say="소개팅에선 서로 “반가워요!”", shot=("cafe", (-1.0, 0.6, 1.2), -90, 6, 4.8, 28, 0.93, 2)),
    dict(say="머리 위엔 하트가 두근두근", shot=("cafe", (-1.0, 0.6, 1.5), -90, 5, 4.6, 28, 0.95, -2)),
    dict(say="회의 중, 부장님이 활짝 웃는데", shot=("office", (-3.1, 0.3, 1.6), -12, 6, 4.2, 28, 0.92, 2)),
    dict(say="머리 위엔 화남 표시가 부글부글", shot=("office", (-3.1, 0.3, 1.8), -8, 5, 3.5, 28, 0.92, 0)),
    dict(say="친구에게 선물을 줬더니 “고마워!”", shot=("home_am", (0.4, 1.05, 1.45), -90, 6, 3.8, 28, 0.92, 2)),
    dict(say="그런데 머리 위엔 물음표만 둥둥", shot=("home_am", (0.4, 1.05, 1.75), -90, 5, 3.4, 28, 0.92, 0)),
    dict(say="중고거래는 서로 머리 위에 돈만 떠서", shot=("street", (-9.6, 3.85, 1.7), -80, 6, 5.6, 28, 0.92, 3)),
    dict(say="흥정이 영영 끝나지 않았어요", shot=("street", (-9.6, 3.85, 1.8), -92, 5, 5.2, 28, 0.92, 0)),
    dict(say="사람들은 모자로 머리 위를 가렸고", shot=("street", (1.9, 3.85, 2.3), -75, 7, 7.2, 28, 0.93, 4)),
    dict(say="모자 가게엔 줄이 길게 늘어섰죠", gap=0.7, shot=("street", (1.6, 5.0, 2.1), -78, 8, 7.6, 28, 0.92, 4)),
    dict(say="그런데 연구에 따르면, 생각은", shot=("street", (0.8, 3.85, 1.9), -90, 5, 3.4, 28, 0.92, 0)),
    dict(say="하루에 약 6,200번 바뀐대요", shot=("street", (0.4, 3.85, 2.0), -88, 7, 7.4, 28, 0.95, -4)),
    dict(say="말풍선은 쉴 새 없이 바뀌었죠", shot=("street", (1.3, 3.85, 1.9), -105, 4, 5.2, 28, 0.92, 6)),
    dict(say="늘 무뚝뚝했던 우리 아빠", gap=0.7, shot=("home_pm", (0.9, 1.0, 1.35), -80, 5, 3.2, 28, 0.93, 3)),
    dict(say="그런데 아빠 머리 위엔 늘 내 얼굴", shot=("home_pm", (0.4, 1.0, 1.45), -90, 6, 4.4, 28, 0.95, 0)),
    dict(say="말은 안 해도, 속은 늘 나였어요", gap=0.7, shot=("home_pm", (0.9, 1.0, 1.6), -88, 4, 3.2, 28, 0.88, 0)),
    dict(say="지금 당신 머리 위엔 뭐가 떠 있을까요?", shot=("home_pm", (0.4, 1.0, 1.55), -90, 10, 4.4, 28, 1.12, 0)),
]
assert len(LINES) == len(NAMES)
TITLE = [("만약에", "white"), ("속마음이", "white"), ("머리 위에 보인다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = IX["tw_a"]            # '그런데 연구에 따르면' 줄
NIGHT_FROM = IX["dad_a"]      # 아빠 이야기(저녁 식탁)부터 밤
INT_X = (-0.75, 0.0, 0.75)    # 면접관 셋의 자리(x)

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep22_mindread" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep22", "title": "만약에 속마음이 머리 위에 보인다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "F", "mode": "lydian", "bpm": 96, "seed": 221, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

HAT_T0 = STARTS[IX["hat_a"]]       # 모자가 떨어지기 시작
HAT_OFF = STARTS[TWIST]            # 모자가 벗겨져 날아감

ME_SH, ME_PA = (0.22, 0.46, 0.90), (0.15, 0.18, 0.30)        # 주인공 '나': 파란 후드
DAD_SH, DAD_PA = (0.50, 0.42, 0.34), (0.20, 0.20, 0.22)      # 아빠: 갈색 카디건


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


def sky(t):
    if line_at(t) >= NIGHT_FROM:
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


# ───────────────────────── 말풍선·모자·카메라 (블렌더 없이 계산) ─────────────────────────
ICON_NAMES = ["heart", "anger", "question", "zzz1", "zzz2", "zzz3", "coin", "food", "note", "excl", "face",
              "dots1", "dots2", "dots3"]
ICON_IX = {n: k for k, n in enumerate(ICON_NAMES)}
FLICK = ["food", "heart", "zzz3", "coin", "note", "question", "anger", "excl"]    # 쉴 새 없이 바뀌는 생각들
ICON_FX = {"heart": "beat", "anger": "shake", "face": "calm"}
BUBW = {"hook": 0.23, "int_b": 0.24, "date_b": 0.30, "deal_a": 0.28, "deal_b": 0.28, "hat_a": 0.2, "tw_b": 0.2,
        "tw_c": 0.24}   # 말풍선이 화면 가로에서 차지할 비율(기본 0.36)
BUB_W = 0.66                                                      # 말풍선 판 가로(m)


def pop(tau, dur=0.30, over=3.0):
    """톡 튀어나오는 크기: 0 → 살짝 커졌다(1.25배쯤) → 1 (easeOutBack). tau<0이면 0."""
    if tau <= 0:
        return 0.0
    if tau >= dur:
        return 1.0
    x = tau / dur - 1.0
    return 1.0 + (over + 1.0) * x ** 3 + over * x ** 2


def icon_at(name, tau):
    """단계가 있는 그림은 떠 있은 시간(tau)에 따라: ZZZ는 Z가 하나씩 늘고, ···은 점이 하나씩 늘어남."""
    if name == "zzz":
        return "zzz%d" % (1 + min(2, int(tau / 0.4)))
    if name == "dots":
        return "dots%d" % (1 + min(2, int((tau % 1.8) / 0.45)))
    return name


def bub_eval(spec, t, a, L, post=False, off=None):
    """말풍선 한 개의 지금 모습 → (그림 이름, 크기) 또는 None.
    spec: i=그림 이름('flick'이면 FLICK을 slot초마다 갈아 끼움) · on=이 줄 안에서 뜨는 때(0~1, 음수면 이미 떠 있음)
    · slot·ph·mul·k0=바뀌는 순서. post(반전 이후 줄)이면 모자가 벗겨진 뒤(off)에야 톡 뜬다."""
    t0 = a + spec["on"] * L
    if post and off is not None:
        t0 = max(t0, off + 0.1)
    tau = t - t0
    if tau <= 0:
        return None
    name = spec["i"]
    if name == "flick":
        q = tau / spec["slot"] + spec.get("ph", 0.0)
        k = int(q)
        return FLICK[(k * spec.get("mul", 1) + spec.get("k0", 0)) % len(FLICK)], 0.6 + 0.4 * pop((q - k) * spec["slot"], 0.16)
    return icon_at(name, tau), pop(tau)


def motion(spec, t):
    """(앞으로 숙임 rad, 위아래 m, 좌우 돌림 rad). spec=(종류, 크기, 횟수/초, 위상)."""
    if not spec:
        return 0.0, 0.0, 0.0
    kind, amp, hz, ph = spec
    s = math.sin(2 * math.pi * hz * t + ph)
    if kind == "nod":
        return amp * s, 0.0, 0.0
    if kind == "droop":                       # 꾸벅꾸벅: 서서히 숙였다가 퍼뜩 들기
        return 0.02 + amp * max(0.0, s) ** 2, 0.0, 0.0
    if kind == "bob":
        return 0.0, amp * abs(s), 0.0
    return 0.0, 0.0, amp * s


def hat_pose(h, t):
    """모자 (높이 보정 m, 크기, 돌림 rad) 또는 None: 위에서 뚝 떨어져 얹히고, 반전에서 위로 휙 날아감."""
    land, off = h[3], h[4]
    if t < land - 0.5:
        return None
    if t < land:
        x = (land - t) / 0.5
        return 2.4 * x * x, 1.0, 0.0
    if t < off:
        return 0.0, 1.0, 0.0
    x = (t - off) / 0.45
    if x >= 1.0:
        return None
    return 5.5 * x, 1.0 - x * x, 10.0 * x


def hat_cover(h, t):
    """모자에 말풍선이 눌려 사라지는 정도의 반대 (1=보임, 0=가려짐). 모자가 얹히기 직전 쏙 들어감."""
    if h is None or t < h[3] - 0.12 or t >= h[4]:
        return 1.0
    return 1.0 - ramp(t, h[3] - 0.12, h[3])


def cam_pose(shot, u):
    """줄 진행도 u에서 카메라: (목표점, 방위각, 고도각, 거리, 렌즈, 위치) — 월드 좌표."""
    st, tg, az, el, dist, lens, push, daz = shot
    o = OFF[st]
    tgt = (tg[0] + o[0], tg[1] + o[1], tg[2])
    a, e, d = az + daz * u, math.radians(el), dist * (1 + (push - 1) * u)
    loc = (tgt[0] + math.cos(e) * math.cos(math.radians(a)) * d,
           tgt[1] + math.cos(e) * math.sin(math.radians(a)) * d, tgt[2] + math.sin(e) * d)
    return tgt, a, el, d, lens, loc


def _bubs():
    """줄마다 말풍선 크기 배율 — 화면 가로의 일정 비율로 보이게 (거리 비례)."""
    out = []
    for k, ln in enumerate(LINES):
        _, _, _, _, dist, lens, _, _ = ln["shot"]
        out.append(min(3.0, max(0.6, BUBW.get(NAMES[k], 0.36) * 13.5 / lens * dist / BUB_W)))
    return out


BUBS = _bubs()

# ───────────────────────── 말풍선 그림(픽셀 블록) ─────────────────────────
PAL_ORDER = "RPBVYKOyGNSHU"
PAL = {"R": (0.95, 0.16, 0.22), "P": (1.0, 0.72, 0.78), "B": (0.20, 0.45, 0.95), "V": (0.58, 0.38, 0.95),
       "Y": (1.0, 0.80, 0.12), "K": (0.10, 0.10, 0.16), "O": (1.0, 0.55, 0.10), "y": (1.0, 0.95, 0.65),
       "G": (0.28, 0.78, 0.32), "N": (0.50, 0.28, 0.13), "S": (0.95, 0.76, 0.60), "H": (0.11, 0.075, 0.055),
       "U": ME_SH}


def _zzz(n):
    """9x9 칸에 Z(3x3)를 왼쪽 아래부터 위 오른쪽으로 n개."""
    g = [["."] * 9 for _ in range(9)]
    for k in range(n):
        for r, row in enumerate(("VVV", ".V.", "VVV")):
            for c, ch in enumerate(row):
                g[6 - 3 * k + r][3 * k + c] = ch
    return ["".join(r) for r in g]


ICONS = {
    "heart": [".RR.RR.", "RPRRRRR", "RRRRRRR", ".RRRRR.", "..RRR..", "...R..."],
    "anger": ["..R.R..", "..R.R..", "RRR.RRR", ".......", "RRR.RRR", "..R.R..", "..R.R.."],
    "question": [".BBB.", "BB.BB", "...BB", "..BB.", "..B..", ".....", "..B.."],
    "zzz1": _zzz(1), "zzz2": _zzz(2), "zzz3": _zzz(3),
    "coin": ["..YKY..", ".YKKKY.", "YYKYYYY", "YYKKKYY", "YYYYKYY", ".YKKKY.", "..YKY.."],
    "food": ["..OOO..", ".OyOyO.", "OOOOOOO", "GGGGGGG", "YYYYYYY", "NNNNNNN", ".OOOOO."],
    "note": ["..GGGGG", "..G...G", "..G...G", "..G...G", "GGG.GGG", "GGG.GGG"],
    "excl": ["OOO", "OOO", ".O.", ".O.", ".O.", "...", ".O."],
    "face": [".HHHHH.", "HHHHHHH", "HSSSSSH", "HSKSKSH", ".PSSSP.", ".SRRRS.", "..UUU..", ".UUUUU."],
    "dots1": ["KK......", "KK......"], "dots2": ["KK.KK...", "KK.KK..."], "dots3": ["KK.KK.KK", "KK.KK.KK"],
}


def _bub_parts(K, name):
    """말풍선 하나 = [(bmesh, 재질번호)] — 0 흰 판 · 1 검은 테두리 · 2~ 그림 색. 원점 = 꼬리 끝, 앞 = +x(카메라 쪽)."""
    P = []

    def box(x0, x1, y0, y1, z0, z1, mi):
        P.append((K.bm_cube(x1 - x0, y1 - y0, z1 - z0, ((x0 + x1) / 2, (y0 + y1) / 2, z0), bottom=True), mi))
    # 판(모서리 한 칸씩 깎음) + 계단 꼬리 — 테두리는 같은 모양을 조금 키워 뒤에 깐다
    shape = [(-0.27, 0.27, 0.12, 0.18), (-0.33, 0.33, 0.18, 0.66), (-0.27, 0.27, 0.66, 0.72),
             (-0.06, 0.06, 0.06, 0.12), (-0.03, 0.03, 0.0, 0.06)]
    b = 0.035
    for y0, y1, z0, z1 in shape:
        box(-0.075, -0.01, y0 - b, y1 + b, z0 - b, z1 + b, 1)
    for y0, y1, z0, z1 in shape:
        box(-0.04, 0.0, y0, y1, z0, z1, 0)
    g = ICONS[name]
    gh, gw = len(g), len(g[0])
    cell = min(0.54 / gw, 0.48 / gh)        # 그림은 판 안쪽(0.54 x 0.48)에 꽉 차게, 가운데 정렬
    for r, row in enumerate(g):
        c0 = 0
        while c0 < gw:
            ch = row[c0]
            if ch == ".":
                c0 += 1
                continue
            c1 = c0
            while c1 + 1 < gw and row[c1 + 1] == ch:
                c1 += 1
            y0 = (c0 - gw / 2) * cell
            z0 = 0.42 + (gh / 2 - r - 1) * cell
            box(0.0, 0.045, y0, y0 + (c1 - c0 + 1) * cell, z0, z0 + cell, 2 + PAL_ORDER.index(ch))
            c0 = c1 + 1
    return P


def _hat_parts(K, style):
    """모자 원형 [(bmesh, 재질번호)] — 0 모자색('col') · 1 띠색('col2'). 원점 = 머리 위 바닥 가운데, 앞 = +x."""
    def box(cx, cy, z0, sx, sy, sz):
        return K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True)
    if style == 0:        # 중절모
        return [(box(0, 0, 0, 0.72, 0.72, 0.04), 0), (box(0, 0, 0.04, 0.56, 0.56, 0.46), 0),
                (box(0, 0, 0.04, 0.575, 0.575, 0.08), 1)]
    if style == 1:        # 벙거지
        return [(box(0, 0, 0, 0.86, 0.86, 0.035), 0), (box(0, 0, 0.035, 0.56, 0.56, 0.28), 0),
                (box(0, 0, 0.035, 0.575, 0.575, 0.07), 1)]
    return [(box(0, 0, 0, 0.56, 0.56, 0.26), 0), (box(0.36, 0, 0, 0.34, 0.46, 0.035), 0),   # 야구 모자
            (box(0, 0, 0.26, 0.07, 0.07, 0.05), 1)]


HAT_COLS = [((0.12, 0.12, 0.15), (0.85, 0.20, 0.25)), ((0.85, 0.25, 0.25), (0.12, 0.12, 0.15)),
            ((0.95, 0.80, 0.25), (0.15, 0.15, 0.18)), ((0.30, 0.62, 0.38), (0.95, 0.95, 0.90)),
            ((0.95, 0.95, 0.92), (0.20, 0.20, 0.25)), ((0.55, 0.36, 0.22), (0.95, 0.80, 0.30)),
            ((0.85, 0.50, 0.80), (0.95, 0.95, 0.90))]


# ───────────────────────── 세트 ─────────────────────────
def _street(v):
    from engine import voxel as X
    rs = v.rs
    v.floor(-20, 20, -3, 3, (0.32, 0.32, 0.34), 0.5)
    for x in np.arange(-19, 20, 3.0):
        v.box(x, x + 1.4, -0.06, 0.06, 0.0, 0.012, (0.95, 0.95, 0.9), jit=0)
    for y0, y1 in ((3, 6), (-6, -3)):
        v.box(-20, 20, y0, y1, 0, 0.12, (0.62, 0.62, 0.62), jit=0)
        v.floor(-20, 20, y0, y1, (0.74, 0.7, 0.64), 0.5, "check", z=0.121)
    signs = [(0.95, 0.3, 0.3), (0.3, 0.8, 1.0), (1.0, 0.8, 0.2), (0.4, 1.0, 0.5), (1.0, 0.5, 0.85), (1.0, 0.6, 0.2)]
    k = 0
    for x0, x1 in ((-20, -15), (-15, -9.5), (-9.5, -4.0), (-4.0, 1.0), (6.0, 11.0), (11.0, 16.0), (16.0, 20.0)):
        X.storefront(v, x0, x1, 6.0, 5.0, float(rs.uniform(9, 15)), signs[k % 6], face=-1, lit=0.35)
        k += 1
    X.storefront(v, 1.0, 6.0, 6.0, 5.0, 11.0, (0.95, 0.35, 0.35), face=-1, lit=0.35)       # 모자 가게
    v.box(1.5, 3.7, 5.93, 5.96, 3.55, 4.85, (0.98, 0.95, 0.9), jit=0, glow=True)         # 간판 판 + 검은 모자 그림
    px = 0.26
    for r, row in enumerate(("..KKK..", "..KKK..", "..RRR..", "..KKK..", "KKKKKKK")):
        for c, ch in enumerate(row):
            if ch != ".":
                x0 = 2.6 + (c - 3.5) * px
                z0 = 4.78 - (r + 1) * px
                v.box(x0, x0 + px, 5.90, 5.93, z0, z0 + px,
                      (0.10, 0.10, 0.14) if ch == "K" else (0.9, 0.2, 0.25), jit=0)
    for x in (-14, -6.5, 6.5, 14):
        X.street_lamp(v, x, 3.4, energy=1.0)
    # 중고거래 접이식 탁자 + 팔려는 모니터 (인도 위)
    v.o[2] += 0.12
    X.table(v, -9.6, 3.85, 0.7, 0.6, 0.75, (0.72, 0.55, 0.38))
    X.monitor(v, -9.6, 3.85, 0.75, -90, w=0.5)
    v.o[2] -= 0.12


def _interview(v):
    from engine import voxel as X
    v.floor(-3.5, 3.5, -3, 3, (0.62, 0.64, 0.68), 0.5, "check")
    v.wall((-3.5, 3), (3.5, 3), 0, 3, (0.90, 0.88, 0.82), 0.5, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, 3, (0.82, 0.84, 0.86), 0.5, face=-1)
    v.wall((3.5, -3), (3.5, 3), 0, 3, (0.82, 0.84, 0.86), 0.5, face=1)
    for x0 in (-3.2, 1.9):
        v.window(x0, x0 + 1.3, 2.99, 0.9, 2.5, night=False)
    X.table(v, 0.0, 0.2, 3.0, 1.3, 0.74, (0.52, 0.38, 0.27))
    for x in INT_X:
        X.chair(v, x, 1.15, -90, (0.2, 0.22, 0.26))
        v.box(x - 0.2, x + 0.2, 0.45, 0.7, 0.74, 0.755, (0.96, 0.96, 0.96))                # 서류
        v.box(x - 0.12, x + 0.12, 0.33, 0.38, 0.74, 0.80, (0.12, 0.14, 0.20))              # 이름표
        v.box(x + 0.26, x + 0.34, 0.55, 0.63, 0.74, 0.84, (0.95, 0.95, 0.95))              # 컵
    v.box(-1.6, -1.1, 2.55, 3.0, 0, 0.5, (0.35, 0.6, 0.45))                                # 화분
    v.box(-1.65, -1.05, 2.5, 3.0, 0.5, 1.5, (0.25, 0.55, 0.25), jit=0.1)
    v.box(1.1, 1.6, 2.55, 3.0, 0, 0.5, (0.35, 0.6, 0.45))
    v.box(1.05, 1.65, 2.5, 3.0, 0.5, 1.5, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.0, 0.0, 2.0):
        v.box(x - 0.6, x + 0.6, 0.0, 0.6, 2.95, 3.0, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.3, 2.6, 110, (0.95, 0.97, 1.0), 0.6)
    v.light(0.0, -1.6, 1.7, 45, (1.0, 0.97, 0.92), 0.6)                                    # 얼굴 앞 보조등


def _cafe(v):
    from engine import voxel as X
    v.floor(-3.5, 3.5, -3, 3, (0.55, 0.38, 0.25), 0.25, "wood")
    v.wall((-3.5, 3), (3.5, 3), 0, 2.9, (0.88, 0.80, 0.68), 0.25, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, 2.9, (0.72, 0.44, 0.34), 0.25, face=-1, kind="brick")
    v.wall((3.5, -3), (3.5, 3), 0, 2.9, (0.88, 0.80, 0.68), 0.25, face=1)
    v.window(-2.4, 0.2, -3.49, 0.9, 2.3, night=False, face=1, axis="x")
    v.box(0.9, 3.3, 2.0, 2.6, 0, 1.0, (0.45, 0.3, 0.2))                                    # 계산대
    v.box(0.85, 3.35, 1.95, 2.65, 1.0, 1.05, (0.92, 0.9, 0.86))
    v.box(2.4, 2.9, 2.2, 2.55, 1.05, 1.5, (0.75, 0.75, 0.78))                              # 커피 머신
    v.box(1.2, 3.2, 2.97, 2.99, 1.7, 2.5, (0.16, 0.16, 0.17))                              # 메뉴판
    for k in range(4):
        v.box(1.35, 1.35 + 0.6 + 0.25 * (k % 2), 2.96, 2.97, 2.3 - k * 0.17, 2.34 - k * 0.17,
              (0.95, 0.9, 0.75), jit=0, glow=True)
    for (cx, cy) in ((-1.0, 0.6), (1.0, -0.6), (-1.4, -1.7)):
        X.table(v, cx, cy, 0.8, 0.8, 0.74, (0.62, 0.45, 0.3))
        X.chair(v, cx - 0.6, cy, 0)
        X.chair(v, cx + 0.6, cy, 180)
    for dy in (-0.14, 0.14):                                                                # 소개팅 탁자: 커피 두 잔 + 꽃
        v.box(-1.0 - 0.05, -1.0 + 0.05, 0.6 + dy - 0.05, 0.6 + dy + 0.05, 0.74, 0.85, (0.97, 0.97, 0.95))
    v.box(-1.02, -0.98, 0.58, 0.62, 0.74, 0.86, (0.3, 0.6, 0.3), jit=0)
    v.box(-1.05, -0.95, 0.55, 0.65, 0.86, 0.94, (0.95, 0.35, 0.45), jit=0)
    for (x, y) in ((1.15, -0.6), (0.85, -0.55), (-1.4, -1.6)):
        v.box(x - 0.05, x + 0.05, y - 0.05, y + 0.05, 0.74, 0.85, (0.97, 0.97, 0.95))
    v.box(-3.3, -2.8, 2.3, 2.8, 0, 0.5, (0.35, 0.6, 0.45))                                  # 화분
    v.box(-3.35, -2.75, 2.25, 2.85, 0.5, 1.4, (0.25, 0.55, 0.25), jit=0.1)
    for (x, y) in ((1.0, -0.6), (2.1, 2.3)):                                                # 펜던트 등 (소개팅 탁자 위는 비움)
        v.box(x - 0.03, x + 0.03, y - 0.03, y + 0.03, 2.2, 2.9, (0.2, 0.2, 0.2), jit=0)
        v.box(x - 0.15, x + 0.15, y - 0.15, y + 0.15, 2.05, 2.2, (1.0, 0.82, 0.55), jit=0, glow=True)
        v.light(x, y, 1.95, 60, (1.0, 0.82, 0.55), 0.3)
    v.light(-1.0, 0.0, 2.1, 80, (1.0, 0.85, 0.65), 0.4)                                     # 소개팅 탁자 위 빛
    v.light(-1.0, -1.8, 1.6, 40, (1.0, 0.92, 0.82), 0.6)                                    # 얼굴 앞 보조등


def _office(v):
    from engine import voxel as X
    v.floor(-4, 4, -3, 3, (0.55, 0.57, 0.6), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, 3, (0.85, 0.86, 0.88), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, 3, (0.82, 0.84, 0.86), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, 3, (0.82, 0.84, 0.86), 0.5, face=1)
    for x0 in (-3.4, -0.6, 2.2):
        v.window(x0, x0 + 2.2, 2.99, 0.9, 2.6, night=False)
    v.box(-3.99, -3.96, -0.9, 1.5, 1.0, 2.3, (0.08, 0.08, 0.09))                           # 발표 화면
    v.box(-3.96, -3.95, -0.8, 1.4, 1.08, 2.22, (0.6, 0.8, 1.0), jit=0, glow=True)
    for k, (y0, h, c) in enumerate(((-0.65, 0.33, (0.95, 0.5, 0.3)), (-0.3, 0.5, (0.95, 0.5, 0.3)),
                                    (0.05, 0.68, (0.3, 0.8, 0.5)), (0.4, 0.88, (0.3, 0.8, 0.5)))):   # 화면 속 오르는 막대
        v.box(-3.95, -3.94, y0, y0 + 0.25, 1.12, 1.12 + h, c, jit=0, glow=True)
    X.table(v, 0.3, 0.2, 3.9, 1.3, 0.74, (0.92, 0.92, 0.9))
    for x in (-1.0, 0.3, 1.6):
        X.chair(v, x, 1.15, -90, (0.2, 0.22, 0.26))
        v.box(x - 0.25, x + 0.15, 0.55, 0.75, 0.74, 0.76, (0.96, 0.96, 0.96))
    for x in (-0.55, 0.75, 2.05):
        X.chair(v, x, -0.75, 90, (0.2, 0.22, 0.26))
        v.box(x - 0.15, x + 0.25, -0.35, -0.15, 0.74, 0.76, (0.96, 0.96, 0.96))
    for x in (-2.0, 1.0):
        v.box(x - 0.08, x + 0.08, -0.05, 0.05, 0.74, 0.86, (0.95, 0.95, 0.95))
    v.box(3.3, 3.8, 2.3, 2.8, 0, 0.5, (0.35, 0.6, 0.45))
    v.box(3.25, 3.85, 2.25, 2.85, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.5, 0.5, 3.0):
        v.box(x - 0.6, x + 0.6, -0.1, 0.5, 2.95, 3.0, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.2, 2.6, 110, (0.95, 0.97, 1.0), 0.6)
    v.light(-1.5, -1.5, 1.8, 60, (1.0, 0.97, 0.92), 0.6)                                    # 부장님 얼굴 앞 보조등


def _home(v, night):
    """식탁 있는 집: 뒤쪽 의자 둘(x=-0.1, 0.9)에 앉거나 그 사이(x=0.4)에 선다. 낮=선물, 밤=저녁 식사."""
    from engine import voxel as X
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    v.wall((-3, 2.5), (3, 2.5), 0, 2.7, (0.93, 0.90, 0.82), 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=1)
    v.box(-2.95, -1.2, 1.9, 2.48, 0, 0.88, (0.95, 0.95, 0.93))                              # 싱크대
    v.box(-2.97, -1.2, 1.86, 2.48, 0.88, 0.93, (0.55, 0.57, 0.6))
    v.box(-2.95, -1.4, 2.1, 2.48, 1.55, 2.25, (0.95, 0.95, 0.93))                           # 찬장
    v.box(-1.15, -0.45, 1.75, 2.48, 0, 2.0, (0.82, 0.84, 0.87))                             # 냉장고
    v.window(1.9, 2.8, 2.49, 1.0, 2.2, night=night, lights=12)
    X.table(v, 0.5, 0.3, 2.2, 1.0, 0.74, (0.85, 0.72, 0.52))
    X.chair(v, -0.1, 1.0, -90)
    X.chair(v, 0.9, 1.0, -90)
    v.box(-0.4, 1.7, 2.1, 2.48, 0, 0.85, (0.55, 0.38, 0.25))                                # 서랍장 + 꽃병 + 액자
    v.box(0.34, 0.46, 2.25, 2.37, 0.85, 1.0, (0.35, 0.55, 0.85))
    for x, z, c in ((0.36, 1.25, (0.95, 0.35, 0.4)), (0.42, 1.2, (0.98, 0.85, 0.3)), (0.38, 1.15, (0.95, 0.55, 0.7))):
        v.box(x - 0.04, x + 0.04, 2.3, 2.38, 1.0, z, c, jit=0.05)
    v.box(1.22, 1.42, 2.4, 2.45, 0.85, 1.15, (0.9, 0.55, 0.3))
    v.box(1.5, 1.7, 2.4, 2.45, 0.85, 1.05, (0.35, 0.65, 0.55))
    for x in (-0.1, 0.9):                                                                   # 밥그릇·국그릇·수저
        v.box(x - 0.2, x - 0.06, 0.55, 0.69, 0.74, 0.8, (0.97, 0.97, 0.95), jit=0)
        v.box(x - 0.18, x - 0.08, 0.57, 0.67, 0.8, 0.84, (0.98, 0.98, 0.96), jit=0)
        v.box(x + 0.06, x + 0.2, 0.55, 0.69, 0.74, 0.8, (0.97, 0.97, 0.95), jit=0)
        v.box(x + 0.08, x + 0.18, 0.57, 0.67, 0.8, 0.82, (0.75, 0.4, 0.2), jit=0)
        v.box(x - 0.01, x + 0.01, 0.45, 0.65, 0.745, 0.755, (0.7, 0.7, 0.72), jit=0)
    for x, y, c in ((0.25, 0.25, (0.85, 0.2, 0.2)), (0.55, 0.25, (0.3, 0.65, 0.3)), (0.4, 0.45, (0.95, 0.8, 0.3))):
        v.box(x - 0.08, x + 0.08, y - 0.08, y + 0.08, 0.74, 0.8, c)                          # 반찬
    v.box(0.3, 0.5, 0.0, 0.2, 0.74, 0.84, (0.3, 0.3, 0.33))                                  # 찌개 냄비
    if not night:
        v.box(0.22, 0.58, 0.4, 0.74, 0.74, 0.96, (0.88, 0.2, 0.25))                          # 선물 상자 + 리본
        v.box(0.38, 0.42, 0.4, 0.74, 0.96, 0.99, (1.0, 0.85, 0.3), jit=0)
        v.box(0.22, 0.58, 0.55, 0.59, 0.96, 0.99, (1.0, 0.85, 0.3), jit=0)
        v.box(0.33, 0.47, 0.5, 0.64, 0.99, 1.07, (1.0, 0.85, 0.3), jit=0)
        v.light(2.3, 1.6, 1.7, 120, (0.85, 0.92, 1.0), 0.8, "ep22_am_win")
        v.light(0.4, -1.5, 1.6, 45, (1.0, 0.95, 0.9), 0.6, "ep22_am_fill")
    else:
        v.box(1.4, 1.6, 2.46, 2.5, 1.85, 2.05, (1.0, 0.85, 0.6), jit=0, glow=True)           # 벽등
        v.light(0.4, 0.3, 1.9, 110, (1.0, 0.78, 0.5), 0.3, "ep22_pm_key")
        v.light(0.4, -1.6, 1.5, 40, (1.0, 0.82, 0.62), 0.6, "ep22_pm_fill")
        v.light(2.3, 1.9, 1.6, 15, (0.55, 0.65, 1.0), 0.6, "ep22_pm_moon")


# ───────────────────────── 캐릭터 배치 ─────────────────────────
HIDE = {IX["world"]: [(-3.4, 3.4, (0,))],
        IX["deal_a"]: [(-13.5, -5.8, (0,)), (-12.5, -6.8, (1, 2))],
        IX["deal_b"]: [(-13.5, -5.8, (0,)), (-12.5, -6.8, (1, 2))],
        IX["hat_a"]: [(-1.6, 4.6, (1, 2))],
        IX["hat_b"]: [(-4.5, 6.0, (0, 1, 2))],
        IX["tw_a"]: [(-1.6, 3.2, (0,))],
        IX["tw_b"]: [(0.0, 1.7, (0,))], IX["tw_c"]: [(0.0, 1.7, (0,))]}


def cast():
    """[dict(set, x, y, yaw, pose, hair, shirt, pants, scale, z, over={줄: 덮어쓰기}, only=보이는 줄 집합 or None,
    bub={줄: 말풍선(i=그림, on=뜨는 때)}, act={줄: 움직임}, hat=(모자 종류, 색, 띠색, 얹히는 때, 벗겨지는 때))]"""
    from engine import voxel as X
    rs = np.random.default_rng(22)
    S, Pn = X.SHIRTS, X.PANTS
    I = IX
    C = []

    def add(st, x, y, yaw, pose, hair=0, shirt=None, pants=None, scale=1.0, z=0.0, over=None, only=None,
            bub=None, act=None, hat=None):
        C.append(dict(set=st, x=x, y=y, yaw=yaw, pose=pose, hair=hair,
                      shirt=shirt or S[1 + int(rs.integers(len(S) - 1))], pants=pants or Pn[int(rs.integers(len(Pn)))],
                      scale=scale, z=z, over=over or {}, only=only, bub=bub or {}, act=act or {}, hat=hat))

    def at(st, x, y, yaw, pose, z=0.0):
        return dict(set=st, x=x, y=y, yaw=yaw, pose=pose, z=z)
    # ── 나 (파란 후드): 거리 → 소개팅 → 중고거래 → 모자 줄 → 반전 → 아빠와 저녁
    add("street", 0.0, 3.85, -90, "stand", 0, ME_SH, ME_PA, z=0.12,
        only={I[n] for n in ("world", "date_a", "date_b", "deal_a", "deal_b", "hat_b", "tw_a", "tw_b", "tw_c",
                             "dad_b", "end")},
        over={I["world"]: at("street", -0.5, 3.85, -90, "confused", 0.12),
              I["date_a"]: at("cafe", -1.5, 0.6, -35, "sit"), I["date_b"]: at("cafe", -1.5, 0.6, -35, "sit"),
              I["deal_a"]: at("street", -9.05, 3.85, 225, "stand", 0.12),
              I["deal_b"]: at("street", -9.05, 3.85, 225, "talk", 0.12),
              I["hat_b"]: at("street", 1.3, 5.0, -50, "stand", 0.12),
              I["tw_a"]: at("street", 0.8, 3.85, -90, "stand", 0.12), I["tw_b"]: at("street", 0.8, 3.85, -90, "stand", 0.12),
              I["tw_c"]: at("street", 0.8, 3.85, -90, "stand", 0.12),
              I["dad_b"]: at("home_pm", -0.1, 1.0, -90, "sit"), I["end"]: at("home_pm", -0.1, 1.0, -80, "sit")},
        bub={I["world"]: dict(i="excl", on=0.62), I["date_b"]: dict(i="heart", on=0.40),
             I["deal_a"]: dict(i="coin", on=0.62), I["deal_b"]: dict(i="coin", on=-1.0),
             I["tw_a"]: dict(i="flick", on=0.0, slot=0.30, ph=0.0, mul=3, k0=0),
             I["tw_b"]: dict(i="flick", on=-1.0, slot=0.27, ph=0.4, mul=3, k0=0),
             I["tw_c"]: dict(i="flick", on=-1.0, slot=0.27, ph=0.4, mul=3, k0=0),
             I["end"]: dict(i="dots", on=0.35)},
        hat=(2, (0.95, 0.80, 0.20), (0.15, 0.15, 0.18), HAT_T0 + 0.7, HAT_OFF + 0.25))
    # ── 거리: 먹을 생각 하며 멈춰 선 행인
    add("street", 0.45, 3.85, -90, "stand", 1, (0.95, 0.60, 0.25), (0.20, 0.20, 0.22), z=0.12, only={I["world"]},
        bub={I["world"]: dict(i="food", on=0.35)})
    # ── 면접장 (면접자 시점): 끄덕끄덕 웃는 면접관 셋 → 졸음
    for x, hair, sh, ic, on, ph in ((INT_X[0], 0, (0.28, 0.30, 0.38), "zzz", 0.56, 0.0),
                                    (INT_X[1], 1, (0.62, 0.40, 0.70), "zzz", 0.40, 1.3),
                                    (INT_X[2], 0, (0.36, 0.36, 0.40), "food", 0.68, 2.6)):
        add("interview", x, 1.15, -90, "sit", hair, sh, (0.12, 0.12, 0.15), only={I["int_a"], I["int_b"]},
            bub={I["int_b"]: dict(i=ic, on=on)},
            act={I["int_a"]: ("nod", 0.07, 1.25, ph), I["int_b"]: ("droop", 0.11, 0.42, ph)})
    # ── 소개팅 상대
    add("cafe", -0.5, 0.6, 215, "sit", 1, (0.97, 0.93, 0.93), (0.45, 0.50, 0.60), only={I["date_a"], I["date_b"]},
        bub={I["date_b"]: dict(i="heart", on=0.48)})
    # ── 회의: 부장님
    add("office", -3.1, 0.3, 0, "talk", 0, (0.20, 0.22, 0.30), (0.12, 0.12, 0.14), only={I["meet_a"], I["meet_b"]},
        bub={I["meet_b"]: dict(i="anger", on=0.38)}, act={I["meet_a"]: ("nod", 0.03, 1.1, 0.0)})
    # ── 선물 받은 친구
    add("home_am", 0.4, 1.05, -90, "talk", 1, (0.95, 0.80, 0.35), (0.20, 0.20, 0.22), only={I["gift_a"], I["gift_b"]},
        bub={I["gift_b"]: dict(i="question", on=0.50)})
    # ── 중고거래 판매자
    add("street", -10.15, 3.85, -35, "talk", 0, (0.85, 0.45, 0.20), (0.35, 0.28, 0.20), z=0.12,
        only={I["deal_a"], I["deal_b"]}, over={I["deal_b"]: dict(pose="angry")},
        bub={I["deal_a"]: dict(i="coin", on=0.70), I["deal_b"]: dict(i="coin", on=-1.0)})
    # ── 모자 가게 줄 (모자는 12번 줄에서 떨어져 얹힘)
    for k, x in enumerate((3.1, 2.5, 1.9, 0.7, 0.1)):
        col, band = HAT_COLS[(k * 2 + 1) % len(HAT_COLS)]
        add("street", x, 5.0, -50, "phone" if k in (1, 3) else "stand", int(rs.random() < 0.5), z=0.12,
            only={I["hat_a"], I["hat_b"]}, hat=(k % 3, col, band, HAT_T0 + 0.35 + 0.15 * k, HAT_OFF + 0.1))
    # ── 아빠
    add("home_pm", 0.9, 1.0, -90, "sit", 0, DAD_SH, DAD_PA, only={I[n] for n in ("dad_a", "dad_b", "dad_c", "end")},
        bub={I["dad_b"]: dict(i="face", on=0.62), I["dad_c"]: dict(i="face", on=-1.0), I["end"]: dict(i="face", on=-1.0)},
        act={I[n]: ("nod", 0.022, 1.6, 0.0) for n in ("dad_a", "dad_b", "dad_c", "end")})
    return C


def crowd(seed=221):
    """인도 걷는 사람들: 앞줄(0)은 같은 속도·같은 방향이라 서로 안 겹침. 말풍선은 앞줄(와이드 컷은 둘째 줄까지), 모자는 모든 줄."""
    from engine import voxel as X
    rs = np.random.default_rng(seed)
    W, k = [], 0
    for lane, (y, d, spd, n) in enumerate(((3.85, 1.0, 1.05, 23), (4.7, -1.0, 1.2, 14), (5.5, 1.0, 0.95, 12))):
        sp = 28.0 / n
        for j in range(n):
            col, band = HAT_COLS[int(rs.integers(len(HAT_COLS)))]
            W.append(dict(k=k, lane=lane, y=y, d=d, spd=spd, x0=-14.0 + sp * (j + 0.5) + float(rs.uniform(-0.12, 0.12)) * sp,
                          ph0=float(rs.random()), hair=int(rs.random() < 0.45),
                          sh=X.SHIRTS[1 + int(rs.integers(len(X.SHIRTS) - 1))], pa=X.PANTS[int(rs.integers(len(X.PANTS)))],
                          icon=FLICK[(k * 3) % len(FLICK)], on=float(rs.uniform(0.08, 0.72)),
                          ph=float(rs.random()), mul=(1, 3, 5, 7)[int(rs.integers(4))],
                          hat=(int(rs.integers(3)), col, band, HAT_T0 + 0.25 + 0.95 * float(rs.random()),
                               HAT_OFF + 0.05 + 0.55 * float(rs.random()))))
            k += 1
    return W


_W = {}


def _world():
    if not _W:
        _W.update(C=cast(), walk=crowd())
    return _W


def walker_spec(w, i):
    """앞줄 행인의 말풍선: 훅에선 하나씩 톡, 평소엔 그대로, 반전 줄에선 쉴 새 없이 바뀜."""
    n = NAMES[i]
    if n == "hook":
        return dict(i=w["icon"], on=w["on"]) if w["lane"] < 2 else None
    if n in ("tw_b", "tw_c"):
        return dict(i="flick", on=-1.0, slot=0.27, ph=w["ph"], mul=w["mul"], k0=w["k"]) if w["lane"] < 2 else None
    if w["lane"] != 0:
        return None
    if n == "tw_a":
        return dict(i="flick", on=0.0, slot=0.27, ph=w["ph"], mul=w["mul"], k0=w["k"])
    if n in ("world", "deal_a", "deal_b", "hat_a", "hat_b"):
        return dict(i=w["icon"], on=-1.0)
    return None


def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·말풍선·모자 점 배열과 카메라."""
    from engine import voxel as X
    W = _world()
    i = line_at(t)
    a, b = shot_span(i)
    L = max(b - a, 1e-3)
    u = (t - a) / L
    tgt, az, el, dist, lens, loc = cam_pose(LINES[i]["shot"], u)
    post = i >= TWIST
    actors = []
    for c in W["C"]:
        d = dict(c)
        d.update(c["over"].get(i, {}))
        d.update(show=c["only"] is None or i in c["only"], spec=c["bub"].get(i))
        d["pitch"], d["dz"], d["dyaw"] = motion(c["act"].get(i), t)
        actors.append(d)
    for w in W["walk"]:
        x = (w["x0"] + w["d"] * w["spd"] * t + 14.0) % 28.0 - 14.0
        hide = any(x0 < x < x1 and w["lane"] in lanes for x0, x1, lanes in HIDE.get(i, ()))
        stride = (w["ph0"] + w["spd"] * t / 0.7) % 1.0
        actors.append(dict(set="street", x=x, y=w["y"], z=0.12, yaw=0.0 if w["d"] > 0 else 180.0,
                           pose="walk_a" if stride < 0.5 else "walk_b", hair=w["hair"], shirt=w["sh"], pants=w["pa"],
                           scale=1.0, show=not hide, spec=walker_spec(w, i), hat=w["hat"], pitch=0.0, dz=0.0, dyaw=0.0))
    O = {k: [] for k in ("P", "R", "CO", "C2", "SC", "PO", "BP", "BR", "BS", "BPO", "HP", "HR", "HS", "HPO", "HC", "HC2")}
    for k, d in enumerate(actors):
        ox, oy = OFF[d["set"]]
        sc = d["scale"] if d["show"] else 0.0
        yaw = math.radians(d["yaw"])
        hz = 1.05 if d["pose"].startswith("sit") else 1.36
        O["P"].append((d["x"] + ox, d["y"] + oy, d["z"] + d["dz"]))
        O["R"].append((0.0, d["pitch"], yaw + d["dyaw"]))
        O["CO"].append(d["shirt"])
        O["C2"].append(d["pants"])
        O["SC"].append(sc)
        O["PO"].append(d["hair"] * X.NPOSE + X.POSES[d["pose"]])
        hat = d.get("hat")
        hp = hat_pose(hat, t) if (hat and sc > 0) else None
        if hp:
            O["HP"].append((d["x"] + ox, d["y"] + oy, d["z"] + (hz + 0.42) * sc + hp[0]))
            O["HR"].append((0.0, 0.0, yaw + hp[2]))
            O["HS"].append(sc * hp[1])
            O["HPO"].append(hat[0])
            O["HC"].append(hat[1])
            O["HC2"].append(hat[2])
        else:
            O["HP"].append((0.0, 0.0, 0.0))
            O["HR"].append((0.0, 0.0, 0.0))
            O["HS"].append(0.0)
            O["HPO"].append(0)
            O["HC"].append((1.0, 1.0, 1.0))
            O["HC2"].append((1.0, 1.0, 1.0))
        ev = None
        cover = hat_cover(hat, t)
        if sc > 0 and d["spec"] is not None and cover > 0:
            ev = bub_eval(d["spec"], t, a, L, post, hat[4] if hat else None)
        if ev:
            name, s = ev
            bx, by = d["x"] + ox, d["y"] + oy
            bz = d["z"] + d["dz"] + (hz + 0.57) * sc + 0.02 * math.sin(2 * math.pi * 0.8 * t + 1.7 * k)
            roll = 0.035 * math.sin(2 * math.pi * 0.9 * t + k)
            fx = ICON_FX.get(name)
            if fx == "beat":
                s *= 1 + 0.09 * max(0.0, math.sin(2 * math.pi * 1.7 * t + k)) ** 2
            elif fx == "shake":
                roll += 0.12 * math.sin(2 * math.pi * 12 * t)
            elif fx == "calm":
                s *= 1 + 0.04 * math.sin(2 * math.pi * 0.9 * t)
            O["BP"].append((bx, by, bz))
            O["BR"].append((roll, 0.0, math.atan2(loc[1] - by, loc[0] - bx)))     # 앞(+x)이 카메라를 봄
            O["BS"].append(BUBS[i] * s * cover)
            O["BPO"].append(ICON_IX[name])
        else:
            O["BP"].append((0.0, 0.0, 0.0))
            O["BR"].append((0.0, 0.0, 0.0))
            O["BS"].append(0.0)
            O["BPO"].append(0)
    return dict(O, i=i, u=u, tgt=tgt, az=az, el=el, dist=dist, lens=lens, loc=loc, actors=actors)


def build(ctx):
    from engine import bkit as K
    from engine import voxel as X
    v = X.Vox(22)
    for name, fn in (("street", _street), ("interview", _interview), ("cafe", _cafe), ("office", _office)):
        v.at(*OFF[name])
        fn(v)
    for name, night in (("home_am", False), ("home_pm", True)):
        v.at(*OFF[name])
        _home(v, night)
    v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep22_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)
    W = _world()
    N = len(W["C"]) + len(W["walk"])
    people = K.instancer_multi(ctx, "ep22_people", X.people_protos(ctx, X.people_mats()), N)
    # 말풍선: 그림마다 원형 하나(판+꼬리+픽셀 블록), 점마다 'pose'로 그림을 고름. 재질은 전부 같은 목록.
    mats = [K.mat_simple("ep22_m_bub", (0.97, 0.97, 0.95), 0.6, emit=(1.0, 1.0, 1.0), estr=0.45),
            K.mat_simple("ep22_m_bord", (0.07, 0.08, 0.13), 0.8)]
    for n, ch in enumerate(PAL_ORDER):
        col = tuple(float(c) for c in PAL[ch])
        mats.append(K.mat_simple("ep22_m_ico_%d" % n, col, 0.5, emit=None if ch == "K" else col, estr=0.9))
    bub = K.instancer_multi(ctx, "ep22_bub", [K.proto(ctx, "ep22_p_bub_" + n, K.join_bms(_bub_parts(K, n)), mats)
                                              for n in ICON_NAMES], N)
    try:
        bub.visible_shadow = False
    except AttributeError:
        pass
    hat_mats = [K.mat_inst("ep22_m_hat", 0.6), K.mat_inst2("ep22_m_hatband", "col2", 0.7)]
    hats = K.instancer_multi(ctx, "ep22_hats", [K.proto(ctx, "ep22_p_hat%d" % s, K.join_bms(_hat_parts(K, s)), hat_mats)
                                                for s in range(3)], N)

    def upd(t, f):
        S = frame_state(t)
        cam.set(S["tgt"], S["az"], S["el"], S["dist"], S["lens"])
        night = S["i"] >= NIGHT_FROM
        sun.data.energy = 0.0 if night else 3.0
        ctx.set_ctl("ambient", 0.12 if night else 0.42)
        ctx.set_rgb("ambient_col", (0.35, 0.42, 0.65) if night else (0.62, 0.68, 0.82))
        K.set_points(people, S["P"], scale=S["SC"], rot=S["R"], col=np.array(S["CO"], np.float32),
                     colors={"col2": np.array(S["C2"], np.float32)}, pose=S["PO"])
        K.set_points(bub, S["BP"], scale=S["BS"], rot=S["BR"], pose=S["BPO"])
        K.set_points(hats, S["HP"], scale=S["HS"], rot=S["HR"], col=np.array(S["HC"], np.float32),
                     colors={"col2": np.array(S["HC2"], np.float32)}, pose=S["HPO"])

    ctx.on_frame(upd)
