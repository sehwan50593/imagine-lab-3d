"""EP32 만약에 월요일이 사라진다면? (19편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
침실 벽 달력에서 '월' 칸(요일 칸+날짜 칸 한 열)이 펑 터지며 사라지고 옆 칸이 당겨짐, 그 아래 침대에서 만세 하는 민지(훅)
→ 달력 클로즈업(일|화가 맞닿음) → 일요일 밤 침대 위 폴짝 만세, 창밖 야경 → 머리 위 월요병 구름이 펑, 환한 얼굴
→ 화요일 아침 알람(삐삐!)에 눈 뜨는 민지 → 만원 지하철 → 다들 울상(처진 눈썹·입꼬리) → 회의실, 부장님 "회의는 화요일부터"(화면에 요일 칸)
→ 교실, 시간표는 화수목금 → 반전: 달력 '화' 위에 먹구름·번개·비 → 하늘에 해·달·화수목금토성 일곱이 차례로 팝(밑에 요일 칸)
→ 달 클로즈업(옆에 '월' 칸) → 창가 달 → 퇴근길(머리 위 토·일 칸) → 카페 모임 웃음·하트 → 민지 미소 → 건배 단체컷
→ 카페 벽 달력에서 구름이 요일 칸을 옮겨 다니는 질문.
근거(설명란): 요일 이름 일·월·화·수·목·금·토는 해, 달과 오행성(화성·수성·목성·금성·토성)에서 온 칠요(七曜) 전통이다.
월요일(月曜日)은 '달의 날'. 달력 배치는 2026년 2월(1일이 일요일, 28일)과 같고, 그 밖의 장면은 지어낸 이야기입니다.
특수효과: 달력 칸 = 칸마다 하나의 원형(판+한글 도트 글자/5x7 도트 숫자, Noto Sans KR(OFL)을 16x16으로 줄인 비트맵 GLYPH)을
instancer_multi 점 하나로 두고, '월' 열은 부풀었다 터지며 반짝이를 뿌린 뒤(scale 0) 옆 열이 easeOutBack으로 당겨 오고 판은 폭이 줄어듦.
말풍선(펑!·삐삐!·?·하트) = 흰 판+도트 글자 원형을 카메라 쪽으로 돌려 세움(ep27 방식). 해·달·행성 = 발광 도트 원판 원형(줄마다 같은 색은 상자 하나).
먹구름·번개·비·알람시계·이불·컵·창밖 만세 그림자 = 일반/발광 상자 인스턴스를 프레임마다 계산. 울상 = 눈썹을 기울이고 입꼬리를 내린 새 자세 원형.
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
OFF = {"bed": (0, 0), "bedm": (300, 0), "metro": (600, 0), "meet": (900, 0), "cls": (1200, 0), "sky": (1500, 0),
       "street": (1800, 0), "cafe": (2100, 0)}
NAMES = ("hook", "vanish", "cheer", "relief", "alarm", "metro", "faces", "boss", "class", "cloud", "planets", "moon",
         "window", "commute", "cafe", "smile", "group", "ask")
IX = {n: k for k, n in enumerate(NAMES)}

X_BED, BED_TOP = -0.55, 0.45          # 침대 가운데 x · 요 윗면 높이 (침실 두 곳 모두, 머리판은 뒷벽 y=2.5 쪽)
CAFE_CX = 0.3                          # 카페 벽 달력·모임 가운데 x

# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 따라갈 사람 (이름, (dx,dy,dz))])
# cuts: 한 줄 안의 짧은 연속 컷 [(끝 u, shot), ...]   shift: 렌즈 세로 이동(센서 높이 비율, +면 화면 속 물체가 아래로)
LINES = [
    dict(say="만약에 월요일이 사라진다면 어떻게 될까요?", gap=0.95,
         shot=("bed", (X_BED, 2.46, 2.98), -90, 7, 5.6, 28, 0.93, 3)),
    dict(say="달력에서 월요일이 통째로 사라졌어요", gap=0.55,
         shot=("bed", (X_BED, 2.46, 2.78), -92, 3, 3.6, 30, 0.88, 5)),
    dict(say="일요일 밤, 직장인들은 환호했죠", gap=0.6,
         shot=("bed", (0.05, 1.8, 1.6), -120, 6, 4.6, 26, 0.9, 10)),
    dict(say="드디어 월요병이 사라진 거예요", gap=0.6,
         shot=("bed", (X_BED, 1.55, 1.95), -78, 6, 2.7, 30, 0.9, 4)),
    dict(say="그런데 화요일 아침, 알람이 울렸어요", gap=0.5,
         shot=("bedm", (X_BED, 1.5, 1.2), -95, 12, 4.0, 28, 0.92, 4),
         cuts=[(0.4, ("bedm", (X_BED + 1.1, 2.2, 0.66), -72, 14, 1.6, 30, 0.9, 6)),
               (1.0, ("bedm", (X_BED, 1.5, 1.2), -95, 12, 4.0, 28, 0.92, 4))]),
    dict(say="출근길 지하철은 여전히 만원이고", gap=0.5,
         shot=("metro", (0.5, 0.0, 1.45), 181, 2, 7.0, 20, 0.95, 2)),
    dict(say="다들 똑같이 울상을 짓고 있었어요", gap=0.55,
         shot=("metro", (4.41, 0.31, 1.5), 180, 0, 2.1, 30, 0.92, 4),
         cuts=[(0.45, ("metro", (4.41, 0.31, 1.5), 180, 0, 2.1, 30, 0.92, 4)),
               (1.0, ("metro", (2.4, 1.2, 1.35), -47, 3, 2.35, 24, 0.9, 6))]),
    dict(say="부장님이 말했죠, 회의는 화요일부터", gap=0.5,
         shot=("meet", (0.75, 2.2, 1.3), -80, 15, 7.0, 22, 0.93, 4),
         cuts=[(0.55, ("meet", (0.75, 2.2, 1.3), -80, 15, 7.0, 22, 0.93, 4)),
               (1.0, ("meet", (-0.65, 1.15, 1.3), -90, 14, 2.8, 30, 0.9, 5))]),
    dict(say="학교도 한 주를 화요일에 시작했어요", gap=0.5,
         shot=("cls", (0.0, 2.0, 1.75), -90, 5, 4.6, 24, 0.92, 3)),
    dict(say="화요일이 새로운 월요일이 되었어요", gap=0.8,
         shot=("bedm", (X_BED, 2.46, 2.98), -90, 7, 5.0, 28, 0.9, -3)),
    dict(say="요일은 해와 달, 다섯 별에서 왔어요", gap=0.6,
         shot=("sky", (0.0, 0.0, 0.6), -90, 0, 10.5, 24, 0.94, 6)),
    dict(say="월요일은 달의 날이라는 뜻이에요", gap=0.5,
         shot=("sky", (20.0, 0.0, 0.0), -90, 0, 11, 28, 0.9, 10)),
    dict(say="달의 날이 사라져도 밤엔 달이 떠요", gap=0.7,
         shot=("bed", (1.75, 2.4, 1.9), -118, 6, 5.0, 26, 0.92, 5)),
    dict(say="기다린 건 월요일이 아니라 주말이었죠", gap=0.45,
         shot=("street", (0.0, 0.0, 0.0), -90, 5, 4.8, 28, 0.92, 4, ("mj", (0.3, 0.0, 1.2)))),
    dict(say="주말엔 친구와 가족을 만나니까요", gap=0.5,
         shot=("cafe", (CAFE_CX, 1.5, 1.6), -90, 15, 5.2, 26, 0.92, 4)),
    dict(say="월요일은 없어도 월요병은 남았지만", gap=0.55,
         shot=("cafe", (CAFE_CX - 0.4, 1.9, 1.35), -75, 14, 2.8, 30, 0.9, 4)),
    dict(say="같이 웃을 사람이 있으면 괜찮아요", gap=0.7,
         shot=("cafe", (CAFE_CX, 1.5, 1.35), -100, 18, 4.6, 26, 0.92, -5)),
    dict(say="월요일이 없다면 제일 싫은 요일은?",
         shot=("cafe", (CAFE_CX, 2.9, 2.25), -90, 8, 5.8, 28, 1.08, 0)),
]
assert len(LINES) == len(NAMES)
for _ln in LINES[1:]:
    assert len(_ln["say"]) <= 20, (_ln["say"], len(_ln["say"]))
TITLE = [("만약에", "white"), ("월요일이", "white"), ("사라진다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = IX["cloud"]          # '화요일이 새로운 월요일이 되었어요' 줄 (뒤이어 10~12번 줄이 사실)

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep32_nomonday" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 54.0, "lines": [[0.3 + 2.8 * i, 2.8 * i + 2.9, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep32", "title": "만약에 월요일이 사라진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "Bb", "mode": "major", "bpm": 108, "seed": 321, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

MJ_SH, MJ_PA = (0.76, 0.64, 0.95), (0.15, 0.18, 0.30)        # 주인공 민지: 연보라 셔츠·긴 머리·남색 바지
BOSS_SH, BOSS_PA = (0.55, 0.57, 0.62), (0.22, 0.23, 0.27)    # 부장님: 회색 셔츠(+빨간 넥타이)
ST1_SH, ST1_PA = (0.95, 0.80, 0.35), (0.18, 0.20, 0.34)      # 학생 친구 하나: 노랑
ST2_SH, ST2_PA = (0.45, 0.75, 0.85), (0.18, 0.20, 0.34)      # 학생 친구 둘: 하늘색
EX_SH = [(0.85, 0.30, 0.28), (0.35, 0.65, 0.40), (0.92, 0.92, 0.90), (0.30, 0.30, 0.34), (0.95, 0.55, 0.25),
         (0.25, 0.45, 0.80), (0.80, 0.55, 0.65), (0.95, 0.80, 0.35), (0.45, 0.75, 0.85)]   # 엑스트라 (연보라·회색 셔츠 피함)


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
NIGHT_LINES = (IX["hook"], IX["vanish"], IX["cheer"], IX["relief"], IX["planets"], IX["moon"], IX["window"])
DUSK_LINES = tuple(range(IX["commute"], IX["ask"] + 1))
LAMPS = []                 # 거리 가로등 점광원 이름 (세트를 만들 때 채움)


def sky(t):
    i = line_at(t)
    if i in NIGHT_LINES:
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0
    if i in DUSK_LINES:
        return (0.20, 0.17, 0.42), (0.98, 0.58, 0.38), 0.0
    if i == IX["cloud"]:
        return (0.20, 0.24, 0.32), (0.42, 0.48, 0.56), 0.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


DAY = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lamp=0.0, lt={})


def env(i, tl, du):
    """줄별 햇빛·주변광 + 가로등 세기 + 움직이는 조명 {이름: 세기}."""
    if i in (IX["hook"], IX["vanish"], IX["cheer"], IX["relief"], IX["window"]):          # 일요일 밤 침실 (불은 켜 둠)
        return dict(DAY, sun=0.0, amb=0.15, amb_col=(0.52, 0.54, 0.76))
    if i == IX["alarm"]:
        return dict(DAY, sun=2.6, amb=0.38)
    if i == IX["cloud"]:                                   # 먹구름이 몰려오며 방이 어두워지고 번개가 번쩍
        k = ramp(tl, 0.2, 1.4)
        fl = 1.0 if (int(tl * 7.0) % 6 == 0 and tl > 1.1) else 0.0
        return dict(DAY, sun=2.6 - 1.7 * k, amb=0.38 - 0.14 * k, amb_col=(0.62 - 0.12 * k, 0.68 - 0.10 * k, 0.82 - 0.02 * k),
                    lt={"ep32_bm_flash": 260.0 * fl})
    if i in (IX["planets"], IX["moon"]):
        return dict(DAY, sun=0.0, amb=0.2, amb_col=(0.45, 0.50, 0.78))
    if i == IX["commute"]:                                 # 퇴근길 노을 + 가로등
        return dict(DAY, sun=2.4, sun_col=(1.0, 0.62, 0.38), sun_rot=(76, 0, 38), amb=0.26, amb_col=(0.70, 0.58, 0.74), lamp=120.0)
    if i >= IX["cafe"]:                                    # 따뜻한 저녁 카페
        return dict(DAY, sun=2.0, sun_col=(1.0, 0.76, 0.52), sun_rot=(66, 0, 35), amb=0.30, amb_col=(0.68, 0.62, 0.74))
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


def cam_pose(shot, u, S):
    """컷 진행도 u에서 카메라: dict(set, tgt, az, el, dist, lens, loc, shift) — 월드 좌표. CamRig.set과 같은 규칙."""
    st_, tg, az, el, dist, lens, push, daz = shot[:8]
    if len(shot) > 8 and shot[8][0] in S:                       # 사람을 따라가는 컷
        d, off = S[shot[8][0]], shot[8][1]
        tg = (d["x"] + off[0], d["y"] + off[1], d["zs"] + off[2])
    o = OFF[st_]
    tgt = (tg[0] + o[0], tg[1] + o[1], tg[2])
    a, e, dd = az + daz * u, math.radians(el), dist * (1 + (push - 1) * u)
    loc = (tgt[0] + math.cos(e) * math.cos(math.radians(a)) * dd, tgt[1] + math.cos(e) * math.sin(math.radians(a)) * dd,
           tgt[2] + math.sin(e) * dd)
    return dict(set=st_, tgt=tgt, az=a, el=el, dist=dd, lens=lens, loc=loc, shift=0.0)


def cam_axes(az, el):
    """카메라의 오른쪽·위쪽 단위벡터."""
    a, e = math.radians(az), math.radians(el)
    return (-math.sin(a), math.cos(a), 0.0), (-math.cos(a) * math.sin(e), -math.sin(a) * math.sin(e), math.cos(e))


# ───────────────────────── 도트 글자 (한글 16x16 · 숫자 5x7) ─────────────────────────
# 도트 글자 16x16: 한 줄(가로 16칸)을 16진 4자리로, 맨 윗줄부터 16줄 이어 붙임(왼쪽 칸 = 가장 높은 비트).
# 만든 법(새 낱말이 필요하면 같은 방식으로): assets/fonts/NotoSansKR-VF.ttf(OFL)를 굵기 620으로 크게 그려 글자 경계 상자를
# 16칸 격자 가운데에 꽉 차게(0.94) 줄이고, 칸 평균이 0.40 이상이면 켬. 숫자·기호는 손으로 그림.
GLYPH = {
    "일": "000c1f0c3f8c31cc70cc31cc3f8c0f0c00000ffc000c0ffc0ffc0c000ffc0ffc",
    "월": "000c1f8c18cc18cc1f8c020c7fec063c067c060c0ffc000c0ffc0c000ffe0ffc",
    "화": "041806187fd87fd80e181f983198319e3f981f1806187fd87fd8001800180018",
    "수": "0180018001c003c007e03e7c381c00007ffe7ffe018001800180018001800180",
    "목": "1ff81ff8181818181ff81ff801807ffe7ffe00001ff83ff80018001800180008",
    "금": "1ff83ffc001c001c001800187ffe7ffe000000003ffc381c381c381c3ffc1ff8",
    "토": "00003ffc3ffc380038003ff83ff838003ffc3ffc018001800180ffff7ffe0000",
    "펑": "000c3fcc3fcc198c19bc19bc198c3fec3fcc000c07f80f3c0c0c0e0c07f800e0",
    "삐": "0004000c2dac2dac2dac3dec3dec2dac2dac2dac3dec3dec000c000c000c0004",
    "카": "001000183f983f98019803987f1e7f1e06180e181c1878187018001800180010",
    "페": "000400363fb63fb61b361b361bf61bf61b361b363fb67fb60036003600360004",
}
_PLAIN = {      # 기호는 손으로 (높이 16줄)
    "!": ["..."] + ["###"] * 8 + ["..."] * 2 + ["###"] * 3 + ["..."] * 2,
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
    ":": ["0", "0", "1", "0", "1", "0", "0"],
}


def _glyph_rows(c):
    """글자 하나 → 16줄 문자열('#'=칸 켬), 비어 있는 좌우 열은 잘라 냄."""
    if c in _PLAIN:
        return list(_PLAIN[c])
    hx = GLYPH[c]
    rows = [format(int(hx[k * 4:k * 4 + 4], 16), "016b") for k in range(16)]
    on = [x for x in range(16) if any(r[x] == "1" for r in rows)]
    return [r[min(on):max(on) + 1].replace("1", "#").replace("0", ".") for r in rows]


def _text_grid(txt, ch="#"):
    """글 → 16줄 문자열(켜진 칸 = ch). 글자 사이 한 칸, 띄어쓰기 다섯 칸."""
    parts = []
    for c in txt:
        parts.append(["....."] * 16 if c == " " else _glyph_rows(c))
        parts.append(["."] * 16)
    rows = ["".join(p[r] for p in parts[:-1]) for r in range(16)]
    return [r.replace("#", ch) for r in rows]


def _digit_rows(txt):
    """숫자 글 → 7줄 문자열('#'=칸 켬). 글자 사이 한 칸."""
    rows = ["" for _ in range(7)]
    for k, c in enumerate(txt):
        for r in range(7):
            rows[r] += ("." if k else "") + FONT57[c][r].replace("1", "#").replace("0", ".")
    return rows


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


# ───────────────────────── 달력 칸 · 요일 칸 (원형 하나 = 칸 하나) ─────────────────────────
WD = "일월화수목금토"
CW, HP, DP = 0.205, 0.25, 0.20                 # 칸 가로 피치 · 요일 줄 세로 피치 · 날짜 줄 세로 피치
TW, TH, TDH = CW - 0.014, HP - 0.014, DP - 0.014     # 칸 판 크기 (틈 1.4cm)
TLY = 0.03                                      # 판 두께
BAND, CAL_MARGIN = 0.14, 0.05                   # 달력 윗띠 높이 · 아래 여백
DATES = [[1 + 7 * r + c for c in range(7)] for r in range(4)]     # 2026년 2월: 1일 = 일요일, 28일
TILE_MATS = [(0.99, 0.93, 0.62), (0.98, 0.97, 0.93), (0.13, 0.15, 0.24), (0.88, 0.18, 0.20), (0.16, 0.34, 0.90),
             (1.0, 0.55, 0.55)]      # 0 요일 판 · 1 날짜 판 · 2 검정 글씨 · 3 빨강 글씨 · 4 파랑 글씨 · 5 강조 판
TILE_ORDER = [("wd", c) for c in WD] + [("wdh", "화")] + [("dt", n) for n in range(1, 29)]
TILE_IX = {k: n for n, k in enumerate(TILE_ORDER)}


def _tile_parts(K, kind, key):
    """칸 하나 = [(bmesh, 재질번호)]. 원점 = 판 뒷면 가운데, 앞(보는 쪽) = -y, 위 = +z."""
    P = []

    def box(x0, x1, y0, y1, z0, z1, mi):
        P.append((K.bm_cube(x1 - x0, y1 - y0, z1 - z0, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)), mi))
    if kind in ("wd", "wdh"):
        w, h, plate, cell, rows = TW, TH, 5 if kind == "wdh" else 0, 0.0104, _glyph_rows(key)
        tcol = 3 if key == "일" and kind == "wd" else 4 if key == "토" else 2
    else:
        w, h, plate, cell, rows = TW, TDH, 1, 0.0142, _digit_rows(str(key))
        tcol = 3 if (key - 1) % 7 == 0 else 4 if (key - 1) % 7 == 6 else 2
    box(-w / 2, w / 2, -TLY, 0.0, -h / 2, h / 2, plate)
    gh, gw = len(rows), len(rows[0])
    for r, c0, c1 in _runs(rows):
        z1 = (gh / 2.0 - r) * cell
        box((c0 - gw / 2.0) * cell, (c1 + 1 - gw / 2.0) * cell, -TLY - 0.022, -TLY + 0.004, z1 - cell, z1, tcol)
    return P


# ───────────────────────── 말풍선 (도트 글자·그림) ─────────────────────────
C0 = 0.04                                      # 말풍선 한 칸(m). 실제 크기는 줄마다 화면 비율로 키움
PAL_ORDER = "RPKOYB"
PAL = {"R": (0.93, 0.15, 0.20), "P": (1.0, 0.72, 0.78), "K": (0.10, 0.10, 0.16), "O": (1.0, 0.55, 0.10),
       "Y": (1.0, 0.80, 0.12), "B": (0.18, 0.40, 0.95)}
ICONS = {      # 이름: (그림 줄들(글자 = 색), 그림 한 점이 차지하는 칸 수)
    "heart": ([".RR.RR.", "RPRRRRR", "RRRRRRR", ".RRRRR.", "..RRR..", "...R..."], 3),
    "q": ([".BBBBB.", "BB...BB", ".....BB", "....BB.", "...BB..", "...BB..", ".......", "...BB..", "...BB.."], 3),
    "bang": (_text_grid("펑!", "R"), 1),
    "alarm": (_text_grid("삐삐!", "R"), 1),
}
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
    for r, c0, c1 in _runs(g):                                     # 그림: 같은 색이 이어진 칸은 상자 하나로
        y0 = (c0 - gw / 2) * mult
        z0 = T + 3 + (gh - 1 - r) * mult
        box(0.0, 0.6, y0, y0 + (c1 - c0 + 1) * mult, z0, z0 + mult, 2 + PAL_ORDER.index(g[r][c0]))
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
    """말풍선 하나의 지금 크기 배율(0이면 안 보임). life가 있으면 끝에서 쏙 줄어듦."""
    tau = tl - sp["t0"]
    if tau <= 0:
        return 0.0
    life = sp.get("life")
    s = pop(tau)
    if life is not None:
        if tau >= life:
            return 0.0
        if tau > life - 0.16:
            s *= (life - tau) / 0.16
    return s


def burst_out(tau):
    """달력 칸이 터지는 크기: 살짝 부풀었다가(0.10초) 확 줄어 사라짐(0.07초). tau<0이면 그대로 1."""
    if tau <= 0:
        return 1.0
    if tau < 0.10:
        return 1.0 + 0.45 * (tau / 0.10) ** 2
    if tau < 0.17:
        return 1.45 * (1.0 - (tau - 0.10) / 0.07)
    return 0.0


# ───────────────────────── 해 · 달 · 행성 (발광 도트 원판) ─────────────────────────
BODY_COLS = {
    "sun_a": (1.0, 0.82, 0.25), "sun_b": (1.0, 0.60, 0.14), "sun_c": (1.0, 0.95, 0.60),
    "moon_a": (0.97, 0.96, 0.86), "moon_b": (0.80, 0.80, 0.74), "moon_c": (0.68, 0.70, 0.68),
    "mars_a": (0.90, 0.36, 0.22), "mars_b": (0.66, 0.22, 0.15), "mars_c": (0.98, 0.92, 0.88),
    "merc_a": (0.66, 0.63, 0.60), "merc_b": (0.42, 0.40, 0.40),
    "jup_a": (0.92, 0.76, 0.56), "jup_b": (0.74, 0.50, 0.34), "jup_c": (0.98, 0.92, 0.84), "jup_d": (0.80, 0.30, 0.22),
    "ven_a": (0.99, 0.90, 0.60), "ven_b": (0.93, 0.76, 0.46),
    "sat_a": (0.93, 0.83, 0.58), "sat_b": (0.80, 0.68, 0.45), "sat_r1": (0.90, 0.80, 0.62), "sat_r2": (0.62, 0.52, 0.40),
    "ray": (1.0, 0.86, 0.30),
}
BODY_KEYS = list(BODY_COLS)
BODY_R = {"sun": 9, "moon": 6, "mars": 4, "mercury": 3, "jupiter": 7, "venus": 5, "saturn": 5, "moonbig": 16}
BODY_ORDER = list(BODY_R)
BODY_CELL = 0.1


def _craters(ix, iz, spots, key_in, key_out):
    for cx, cz, r in spots:
        if (ix - cx) ** 2 + (iz - cz) ** 2 <= r * r:
            return key_in
    return key_out


def _body_color(name, ix, iz):
    R = BODY_R[name]
    if name == "sun":
        d = math.hypot(ix, iz)
        return "sun_c" if d < 0.38 * R else "sun_a" if d < 0.78 * R else "sun_b"
    if name == "moon":
        return _craters(ix, iz, ((-2, 2, 1), (2, -1, 1), (1, 3, 0.6), (-2, -3, 0.9)), "moon_b", "moon_a")
    if name == "moonbig":
        c = _craters(ix, iz, ((-6, 6, 3.2), (5, -3, 2.6), (-4, -8, 2.2), (8, 6, 1.8), (-9, 0, 1.6), (1, 10, 1.4), (10, -8, 1.3)),
                     "moon_c", None)
        if c:
            return c
        return _craters(ix, iz, ((-6, 6, 4.4), (5, -3, 3.6), (-4, -8, 3.2), (8, 6, 2.6)), "moon_b", "moon_a")
    if name == "mars":
        if iz >= R - 1:
            return "mars_c"
        return _craters(ix, iz, ((-1, 1, 1.2), (2, -1, 1.0)), "mars_b", "mars_a")
    if name == "mercury":
        return _craters(ix, iz, ((-1, 1, 0.9), (1, -1, 0.8)), "merc_b", "merc_a")
    if name == "jupiter":
        if 1 <= ix <= 3 and -3 <= iz <= -2:
            return "jup_d"
        return ("jup_a", "jup_a", "jup_b", "jup_b", "jup_c", "jup_a", "jup_b")[iz % 7]
    if name == "venus":
        return "ven_a" if (iz + (ix // 2)) % 3 else "ven_b"
    if name == "saturn":
        return "sat_a" if iz % 3 else "sat_b"
    return "sun_a"


def _body_boxes(name):
    """[(x0칸, x1칸, 가운데 z칸, 가운데 y칸, 두께 칸, 색 이름)] — 칸 가운데가 정수 좌표, 앞 = -y."""
    R = BODY_R[name]
    out = []
    lim = (R + 0.35) ** 2
    for iz in range(R, -R - 1, -1):
        ix = -R
        while ix <= R:
            if ix * ix + iz * iz > lim:
                ix += 1
                continue
            key = _body_color(name, ix, iz)
            j = ix
            while j + 1 <= R and (j + 1) ** 2 + iz * iz <= lim and _body_color(name, j + 1, iz) == key:
                j += 1
            out.append((ix, j, iz, 0.0, 2.0 if name != "moonbig" else 3.0, key))
            ix = j + 1
    if name == "sun":                                   # 광선 8개: 원판 둘레에 작은 상자
        for k in range(8):
            a = math.pi / 4 * k
            for rr in (R + 1.4, R + 2.4):
                cx, cz = round(rr * math.cos(a)), round(rr * math.sin(a))
                out.append((cx, cx, cz, 0.0, 2.0, "ray"))
    if name == "saturn":                                # 고리: 납작한 타원, 앞쪽 절반만 원판 앞을 가림
        rx, rz = 1.95 * R, 0.42 * R
        for iz in range(-4, 5):
            for ix in range(-int(rx) - 1, int(rx) + 2):
                d = (ix / rx) ** 2 + (iz / rz) ** 2
                if not 0.58 <= d <= 1.0:
                    continue
                if iz > 0 and ix * ix + iz * iz <= lim:        # 원판 뒤로 지나는 부분은 가려짐
                    continue
                out.append((ix, ix, iz, -2.5 if iz <= 0 else 1.5, 1.0, "sat_r1" if d < 0.8 else "sat_r2"))
    return out


def _body_parts(K, name):
    P = []
    for x0, x1, iz, yc, th, key in _body_boxes(name):
        c = BODY_CELL
        P.append((K.bm_cube((x1 - x0 + 1) * c, th * c, c, ((x0 + x1) / 2.0 * c, yc * c, iz * c)), BODY_KEYS.index(key)))
    return P


# ───────────────────────── 캐릭터 자세 (표준 자세 위에 팔·고개·눈썹·입만 바꾼 원형) ─────────────────────────
SITS = ("sit", "sit_phone", "sit_conf")
# base = 바탕 자세, arms = ((오른팔 앞뒤, 옆), (왼팔 앞뒤, 옆)) 어깨 회전각(음수 = 앞으로 듦, 옆 = 몸 밖으로 벌림),
# mouth = open/smile/frown, brow = sad(처진 눈썹), tie = 빨간 넥타이, sleep = 눈 감음, head = 고개 숙임(+)/젖힘(−),
# hroll = 고개 기울임, lie = 눈 뜨고 누움
KINDS = {
    "cheer": dict(base="stand", arms=((-2.9, 0.0), (-2.9, 0.0)), mouth="open"),
    "sit_cheer": dict(base="sit", arms=((-2.9, 0.0), (-2.9, 0.0)), mouth="open"),
    "smile": dict(base="stand", mouth="smile"),
    "sit_smile": dict(base="sit", mouth="smile"),
    "sit_laugh": dict(base="sit", mouth="open"),
    "sit_toast": dict(base="sit", arms=((-2.0, 0.0), (-0.6, 0.0)), mouth="smile"),
    "w_a": dict(base="walk_a", mouth="smile"),
    "w_b": dict(base="walk_b", mouth="smile"),
    "f_stand": dict(base="stand", mouth="frown", brow="sad"),
    "f_phone": dict(base="phone", mouth="frown", brow="sad"),
    "f_up": dict(base="stand", arms=((-2.9, 0.0), (0.0, 0.0)), mouth="frown", brow="sad"),
    "f_sit": dict(base="sit", mouth="frown", brow="sad"),
    "f_sitphone": dict(base="sit_phone", mouth="frown", brow="sad"),
    "f_sitconf": dict(base="sit_conf", mouth="frown", brow="sad"),
    "sit_sleepy": dict(base="sit", sleep=True, mouth="frown", head=0.22, hroll=0.14),
    "lieopen": dict(base="stand", lie=True),
    "lie_f": dict(base="stand", lie=True, mouth="frown", brow="sad"),
    "boss_point": dict(base="stand", arms=((0.0, -1.5), (0.0, 0.0)), mouth="open", tie=True),
    "boss_talk": dict(base="talk", tie=True),
    "boss_sad": dict(base="stand", mouth="frown", brow="sad", tie=True),
}
ARMS = {"stand": (0.0, 0.0), "sit": (-0.6, -0.6), "sit_phone": (-1.05, -0.6), "sit_conf": (-2.75, -0.6),
        "phone": (-1.05, 0.0), "angry": (-2.5, -2.5), "confused": (-2.75, 0.05), "talk": (-0.9, 0.05),
        "walk_a": (0.35, -0.35), "walk_b": (-0.35, 0.35), "lie": (0.0, 0.0)}
for _k, _sp in KINDS.items():
    ARMS[_k] = tuple(a[0] for a in _sp["arms"]) if _sp.get("arms") else ARMS[_sp["base"]]


def base_of(pose):
    return KINDS[pose]["base"] if pose in KINDS else pose


def hip_of(pose):
    return 0.47 if base_of(pose) in SITS else 0.78


def _rot_x(bm, ang, pivot):
    """x축(앞) 둘레 회전. 왼쪽(+y) 팔은 양수 = 바깥."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        y, z = p.co.y - pivot[1], p.co.z - pivot[2]
        p.co.y, p.co.z = pivot[1] + c * y - s * z, pivot[2] + s * y + c * z
    return bm


def _center(bm):
    n = len(bm.verts)
    return (sum(v.co.x for v in bm.verts) / n, sum(v.co.y for v in bm.verts) / n, sum(v.co.z for v in bm.verts) / n)


def _variant(name, lh):
    """voxel._person으로 만든 바탕 자세에서 팔·고개·눈썹·입·눈만 바꾼 [(bmesh, 재질)]. 재질 8 = 넥타이(빨강)."""
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
    out = list(legs) + [torso] + head + list(arms)
    if sp.get("tie"):                                              # 빨간 넥타이 (몸통 앞)
        out += [(cube(0.16, 0, hip + 0.14, 0.03, 0.07, 0.34), 8), (cube(0.16, 0, hip + 0.44, 0.04, 0.10, 0.07), 8)]
    if sp.get("lie"):                                              # 선 모습을 뒤로 눕힘: 발끝이 원점, 머리는 -x, 얼굴은 위 (눈은 뜬 채)
        for bm, _ in out:
            X._rot_y(bm, -math.pi / 2, (0, 0, 0))
            X._shift(bm, dz=0.24)
    return out


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
    """머리 꼭대기 한가운데(세트 좌표) — 말풍선 꼬리·구름이 닿는 곳."""
    return rel(d, 0.0, 0.0, hip_of(d["pose"]) + 1.04)


def face_pt(d):
    """얼굴 한가운데(세트 좌표)."""
    return rel(d, 0.22, 0.0, hip_of(d["pose"]) + 0.8)


def hand_pt(d, side, reach=0.0):
    """side 'R'(캐릭터 오른손)·'L' 손 끝 근처 점 (서 있거나 앉은 자세용)."""
    ang = ARMS[d["pose"]][0 if side == "R" else 1]
    dd = 0.49 + reach
    return rel(d, -dd * math.sin(ang), -0.34 if side == "R" else 0.34, hip_of(d["pose"]) + 0.54 - dd * math.cos(ang))


# ───────────────────────── 세트 ─────────────────────────
WH_BED = 3.4                          # 침실 벽 높이 (달력을 높이 걸어 아래 침대와 겹치지 않게)
DARK = (0.2, 0.2, 0.22)


def sign(v, text, xc, ztop, y, cell, col, glow=True, depth=0.04):
    """뒷벽(앞 = -y)에 도트 글자 간판: 글자 뒷면이 y, 위 끝이 ztop, 가운데 xc. 같은 줄 이음은 상자 하나."""
    rows = _text_grid(text, "#")
    x0 = xc - len(rows[0]) * cell / 2
    for r, c0, c1 in _runs(rows):
        z = ztop - (r + 1) * cell
        v.box(x0 + c0 * cell, x0 + (c1 + 1) * cell, y - depth, y, z, z + cell, col, jit=0, glow=glow)


def _bed(v, mode):
    """침실 (mode night = 일요일 밤 · morning = 화요일 아침). 앞(-y)이 열린 방, 침대 머리판은 뒷벽, 벽 달력은 침대 위(움직이는 소품), 창은 오른쪽."""
    night = mode == "night"
    bx = X_BED
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    wb, ws = (0.93, 0.90, 0.82), (0.86, 0.88, 0.80)
    v.wall((-3, 2.5), (3, 2.5), 0, WH_BED, wb, 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, WH_BED, ws, 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, WH_BED, ws, 0.25, face=1)
    # 창 (뒷벽 오른쪽) + 커튼. 밤엔 먼 건물 불빛과 픽셀 달
    v.window(1.0, 2.5, 2.49, 1.05, 2.45, night=night, lights=18 if night else 0)
    cu = (0.85, 0.45, 0.42)
    v.box(0.80, 0.98, 2.36, 2.46, 0.85, 2.7, cu)
    v.box(2.52, 2.70, 2.36, 2.46, 0.85, 2.7, cu)
    v.box(0.78, 2.72, 2.34, 2.40, 2.64, 2.72, (0.4, 0.28, 0.2))
    if night:
        cell = 0.055
        for ix in range(-4, 5):
            for iz in range(-4, 5):
                if ix * ix + iz * iz <= 17 and not (ix >= 1 and iz >= 1 and (ix - 1) ** 2 + (iz - 1) ** 2 <= 5):   # 초승달 느낌으로 한 입 베어 문 원
                    v.box(1.95 + ix * cell - cell / 2, 1.95 + ix * cell + cell / 2, 2.445, 2.465,
                          2.15 + iz * cell - cell / 2, 2.15 + iz * cell + cell / 2, (1.0, 0.97, 0.78), jit=0, glow=True)
    # 침대 + 베개 + 머리판 (이불은 움직이는 소품 / 밤엔 발치에 접어 둠)
    v.box(bx - 0.7, bx + 0.7, 0.17, 2.45, 0, 0.28, X.WOOD)
    v.box(bx - 0.67, bx + 0.67, 0.20, 2.42, 0.28, BED_TOP, X.WHITE, jit=0.02)
    v.box(bx - 0.72, bx + 0.72, 2.38, 2.47, 0, 1.05, X.DARKWOOD)
    v.box(bx - 0.4, bx + 0.4, 1.98, 2.35, BED_TOP, BED_TOP + 0.11, (0.97, 0.97, 0.97), jit=0.01)
    if night:
        v.box(bx - 0.68, bx + 0.68, 0.23, 0.85, BED_TOP, BED_TOP + 0.13, (0.45, 0.58, 0.88))
        v.box(bx - 0.69, bx + 0.69, 0.81, 0.90, BED_TOP, BED_TOP + 0.15, (0.93, 0.95, 0.99))
    # 협탁 + 스탠드 (알람시계는 움직이는 소품)
    nx = bx + 1.02
    v.box(nx - 0.2, nx + 0.2, 2.05, 2.45, 0, 0.5, (0.62, 0.42, 0.25))
    v.box(nx - 0.2, nx - 0.04, 2.15, 2.31, 0.5, 0.56, (0.3, 0.3, 0.32), jit=0)
    v.box(nx - 0.15, nx - 0.09, 2.2, 2.26, 0.56, 0.8, (0.3, 0.3, 0.32), jit=0)
    v.box(nx - 0.24, nx + 0.0, 2.12, 2.36, 0.8, 1.04, (1.0, 0.88, 0.62), jit=0, glow=night)
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
    v.box(-2.99, -2.97, 0.15, 0.95, 1.55, 2.35, (0.95, 0.75, 0.3), jit=0)          # 포스터
    v.box(-2.97, -2.96, 0.25, 0.85, 1.65, 2.25, (0.3, 0.6, 0.9), jit=0)
    v.box(-2.96, -2.95, 0.45, 0.65, 1.8, 2.1, (1.0, 0.95, 0.8), jit=0)
    # 옷장 (오른쪽 벽), 러그, 화분
    v.box(2.5, 2.97, -1.6, -0.2, 0, 2.0, (0.82, 0.86, 0.92))
    v.box(2.47, 2.5, -0.95, -0.85, 0.2, 1.9, (0.4, 0.4, 0.45), jit=0)
    v.floor(bx - 1.1, bx + 1.1, -1.4, 0.3, (0.82, 0.55, 0.50), 0.5, "check", z=0.012)
    v.box(2.2, 2.7, 1.2, 1.7, 0, 0.45, (0.35, 0.6, 0.45))
    v.box(2.15, 2.75, 1.15, 1.75, 0.45, 1.05, (0.25, 0.55, 0.25), jit=0.1)
    # 조명
    if night:
        v.light(bx, 0.6, 2.9, 120, (1.0, 0.88, 0.70), 0.5, "ep32_bn_ceil")
        v.light(bx + 0.2, -1.2, 2.0, 100, (1.0, 0.93, 0.85), 0.6, "ep32_bn_fill")
        v.light(nx - 0.12, 2.24, 1.1, 25, (1.0, 0.78, 0.5), 0.3, "ep32_bn_lamp")
        v.light(2.3, 2.0, 1.8, 26, (0.55, 0.65, 1.0), 0.8, "ep32_bn_win")
    else:
        v.light(2.3, 2.0, 1.8, 140, (0.85, 0.92, 1.0), 0.8, "ep32_bm_win")
        v.light(bx + 0.2, -1.2, 2.0, 80, (1.0, 0.95, 0.88), 0.6, "ep32_bm_fill")
        v.light(bx, 0.6, 2.9, 40, (1.0, 0.9, 0.75), 0.5, "ep32_bm_ceil")
        v.light(bx, 1.9, 2.6, 0, (0.8, 0.85, 1.0), 0.4, "ep32_bm_flash")


def _metro(v):
    """지하철 객차: 길이 14(x) · 폭 3(y) · 높이 2.4. 양쪽 긴 의자, 문 3쌍, 창, 손잡이, 천장등. 카메라는 통로(|y|<1)에 둠."""
    L, W, H = 7.0, 1.5, 2.4
    wall_c, end_c = (0.90, 0.90, 0.87), (0.84, 0.86, 0.88)
    v.floor(-L, L, -W, W, (0.66, 0.67, 0.70), 0.5, "check")
    v.wall((-L, W), (L, W), 0, H, wall_c, 0.5, face=-1)
    v.wall((-L, -W), (L, -W), 0, H, wall_c, 0.5, face=1)
    v.wall((-L, -W), (-L, W), 0, H, end_c, 0.5, face=-1)
    v.wall((L, -W), (L, W), 0, H, end_c, 0.5, face=1)
    v.floor(-L, L, -W, W, (0.82, 0.82, 0.80), 0.5, z=H)

    def S(sgn, o0, o1):          # sgn쪽 벽에서 안쪽으로 o0~o1 떨어진 y 구간
        a, b = sgn * (W - o0), sgn * (W - o1)
        return min(a, b), max(a, b)
    seat, base, dark = (0.22, 0.52, 0.60), (0.30, 0.31, 0.35), (0.35, 0.37, 0.41)
    ads = [(0.95, 0.35, 0.35), (0.98, 0.85, 0.30), (0.35, 0.65, 0.95), (0.96, 0.96, 0.92)]
    for sgn in (1, -1):
        for k, (x0, x1) in enumerate(((-6.6, -5.2), (-3.3, -1.0), (1.0, 3.3), (5.2, 6.6))):
            v.window(x0, x1, sgn * (W - 0.01), 0.95, 1.95, night=False, face=-sgn)
            y0, y1 = S(sgn, 0.02, 0.05)
            v.box(x0 + 0.1, x1 - 0.1, y0, y1, 2.08, 2.32, ads[(k + (sgn > 0)) % 4], jit=0.02)          # 창 위 광고
        for xd in (-4.2, 0.0, 4.2):                                                                      # 문
            y0, y1 = S(sgn, 0.03, 0.06)
            v.box(xd - 0.68, xd + 0.68, y0, y1, 0.0, 2.05, (0.60, 0.62, 0.66), jit=0.02)
            yp0, yp1 = S(sgn, 0.06, 0.075)
            for a, b in ((xd - 0.62, xd - 0.03), (xd + 0.03, xd + 0.62)):
                v.box(a, b, yp0, yp1, 0.8, 1.85, (0.62, 0.78, 0.95), jit=0, glow=True)
            yf0, yf1 = S(sgn, 0.02, 0.07)
            for a, b, z0, z1 in ((xd - 0.74, xd - 0.68, 0.0, 2.05), (xd + 0.68, xd + 0.74, 0.0, 2.05),
                                 (xd - 0.74, xd + 0.74, 2.05, 2.12)):
                v.box(a, b, yf0, yf1, z0, z1, dark, jit=0.02)
            ys0, ys1 = S(sgn, 0.03, 0.05)
            v.box(xd - 0.5, xd + 0.5, ys0, ys1, 2.18, 2.26, (1.0, 0.55, 0.35), jit=0, glow=True)        # 문 위 표시등
        for x0, x1 in ((-6.9, -5.0), (-3.4, -1.0), (1.0, 3.4), (5.0, 6.9)):                             # 긴 의자
            c0, c1 = S(sgn, 0.04, 0.5)
            v.box(x0, x1, c0, c1, 0.38, 0.45, seat)
            b0, b1 = S(sgn, 0.1, 0.46)
            v.box(x0 + 0.05, x1 - 0.05, b0, b1, 0.0, 0.38, base)
            r0, r1 = S(sgn, 0.04, 0.12)
            v.box(x0, x1, r0, r1, 0.46, 0.92, seat)
        for x in (-3.4, -1.0, 1.0, 3.4):                                                                 # 기둥
            p0, p1 = S(sgn, 0.515, 0.565)
            v.box(x - 0.025, x + 0.025, p0, p1, 0.0, 2.39, (0.82, 0.84, 0.88), jit=0.01)
        yr = sgn * 0.65
        v.box(-6.8, 6.8, yr - 0.02, yr + 0.02, 2.08, 2.12, (0.8, 0.82, 0.86), jit=0)                    # 선반 봉
        for x in np.arange(-6.3, 6.4, 0.6):                                                              # 손잡이
            v.box(x - 0.01, x + 0.01, yr - 0.01, yr + 0.01, 1.74, 2.08, (0.9, 0.9, 0.88), jit=0)
            for a, b, c, d_, th in ((-0.06, 0.06, 1.62, 1.66, 0.012), (-0.06, 0.06, 1.74, 1.78, 0.012),
                                    (-0.06, -0.04, 1.66, 1.74, 0.008), (0.04, 0.06, 1.66, 1.74, 0.008)):
                v.box(x + a, x + b, yr - th, yr + th, c, d_, (0.96, 0.82, 0.25), jit=0)
    for xe, face in ((-L, 1), (L, -1)):                                                                   # 객차 끝 문
        xa, xb = (xe + 0.01, xe + 0.05) if face > 0 else (xe - 0.05, xe - 0.01)
        v.box(xa, xb, -0.55, 0.55, 0.0, 2.05, (0.60, 0.62, 0.66), jit=0.02)
        xa2, xb2 = (xe + 0.05, xe + 0.065) if face > 0 else (xe - 0.065, xe - 0.05)
        v.box(xa2, xb2, -0.4, 0.4, 1.0, 1.85, (0.85, 0.92, 1.0), jit=0, glow=True)
    for yy in (-0.45, 0.45):                                                                              # 천장 등
        v.box(-6.8, 6.8, yy - 0.12, yy + 0.12, 2.37, 2.395, (1.0, 1.0, 1.0), jit=0, glow=True)
    for k, x in enumerate((-6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0)):
        v.light(x, 0.0, 2.1, 90, (1.0, 0.98, 0.95), 0.5, f"ep32_metro_l{k}")


def _meet(v):
    """회의실 (x -4~4, y -3~3, 앞 -y가 열림): 뒷벽 가운데 발표 화면(요일 칸은 움직이는 소품), 가운데 긴 탁자, 오른쪽 벽 창."""
    WH = 3.2
    v.floor(-4, 4, -3, 3, (0.55, 0.57, 0.60), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, WH, (0.85, 0.86, 0.88), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, WH, (0.82, 0.84, 0.86), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, WH, (0.82, 0.84, 0.86), 0.5, face=1)
    for y0, y1 in ((-2.3, -0.9), (0.4, 1.8)):
        v.window(y0, y1, 3.99, 1.0, 2.5, night=False, face=-1, axis="x")
    v.box(-1.9, 1.9, 2.93, 2.99, 0.85, 2.85, (0.08, 0.08, 0.09))                     # 발표 화면 틀
    v.box(-1.8, 1.8, 2.91, 2.93, 0.95, 2.75, (0.86, 0.93, 1.0), jit=0, glow=True)   # 화면 면
    v.box(-1.65, 1.65, 2.89, 2.91, 2.4, 2.66, (0.25, 0.42, 0.85), jit=0, glow=True)  # 슬라이드 제목 띠
    for k, (c, hh) in enumerate(((0.95, 0.55), (0.55, 0.40), (0.30, 0.25))):         # 슬라이드 막대그래프
        v.box(-1.5 + 0.35 * k, -1.2 + 0.35 * k, 2.89, 2.91, 1.0, 1.0 + hh, (0.95, 0.5, 0.3) if k == 0 else (0.3, 0.8, 0.5), jit=0, glow=True)
    X.table(v, 0.0, 0.2, 5.2, 1.3, 0.74, (0.92, 0.92, 0.90))
    cc = (0.2, 0.22, 0.26)
    for x in (-1.9, -0.65, 0.6, 1.85):
        X.chair(v, x, 1.15, -90, cc)
        X.chair(v, x, -0.75, 90, cc)
        v.box(x - 0.25, x + 0.15, 0.45, 0.65, 0.74, 0.76, (0.96, 0.96, 0.96))        # 서류
        v.box(x - 0.15, x + 0.25, -0.05, 0.15, 0.74, 0.76, (0.96, 0.96, 0.96))
    for x in (-1.3, 1.2):
        v.box(x - 0.08, x + 0.08, 0.15, 0.3, 0.74, 0.86, (0.95, 0.95, 0.95))        # 종이컵
    v.box(3.2, 3.7, 2.2, 2.7, 0, 0.5, (0.35, 0.6, 0.45))                              # 화분
    v.box(3.15, 3.75, 2.15, 2.75, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    v.box(-3.8, -3.2, 2.2, 2.7, 0, 1.2, (0.78, 0.8, 0.84))                            # 서류장
    for x in (-2.5, 0.5, 3.0):
        v.box(x - 0.6, x + 0.6, -0.1, 0.5, 3.15, 3.2, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.2, 2.8, 110, (0.95, 0.97, 1.0), 0.6, f"ep32_meet_l{int(x * 10)}")
    v.light(0.0, -2.0, 2.0, 70, (1.0, 0.97, 0.92), 0.6, "ep32_meet_fill")


def _cls(v):
    """교실 (x -4~4, y -3~3, 앞 -y가 열림): 뒷벽에 창 둘과 시간표(요일 칸은 움직이는 소품), 책상·의자는 카메라 쪽을 봄."""
    WH = 3.1
    v.floor(-4, 4, -3, 3, (0.80, 0.68, 0.50), 0.5, "wood")
    wc = (0.93, 0.93, 0.88)
    v.wall((-4, 3), (4, 3), 0, WH, wc, 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, WH, (0.88, 0.90, 0.86), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, WH, (0.88, 0.90, 0.86), 0.5, face=1)
    for x0, x1 in ((-3.7, -1.9), (1.9, 3.7)):
        v.window(x0, x1, 2.99, 1.0, 2.6, night=False)
    # 시간표 (뒷벽 가운데): 판 + 칸마다 파스텔 색
    v.box(-0.85, 0.85, 2.94, 2.97, 1.05, 2.8, (0.97, 0.96, 0.9))
    pas = [(0.98, 0.78, 0.78), (0.78, 0.9, 0.98), (0.98, 0.92, 0.7), (0.8, 0.95, 0.8), (0.9, 0.82, 0.98)]
    for c in range(4):
        for r in range(5):
            x = (c - 1.5) * 0.33
            z = 2.18 - 0.2 * r
            v.box(x - 0.15, x + 0.15, 2.915, 2.94, z - 0.085, z + 0.085, pas[(c + 2 * r) % 5], jit=0.02)
    v.box(-0.28, 0.28, 2.94, 2.97, 2.84, 3.0 - 0.0, (0.97, 0.97, 0.95), jit=0)         # 벽시계
    v.box(-0.02, 0.02, 2.925, 2.94, 2.88, 2.97, DARK, jit=0)
    v.box(-0.02, 0.1, 2.915, 2.925, 2.9, 2.93, DARK, jit=0)
    for x, y in ((-1.7, 0.35), (-0.6, 0.35), (0.6, 0.35), (1.7, 0.35), (-1.15, 1.45), (0.0, 1.45), (1.15, 1.45)):
        X.table(v, x, y, 0.8, 0.55, 0.72, (0.80, 0.68, 0.50))                          # 책상 (학생 앞)
        X.chair(v, x, y + 0.55, -90, (0.3, 0.45, 0.7))
    v.box(3.3, 3.8, -2.4, -1.9, 0, 0.5, (0.35, 0.6, 0.45))                             # 화분
    v.box(3.25, 3.85, -2.45, -1.85, 0.5, 1.2, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.4, 0.0, 2.4):
        v.box(x - 0.6, x + 0.6, 0.0, 0.5, 3.05, 3.1, (1.0, 1.0, 0.98), jit=0, glow=True)
        v.light(x, 0.8, 2.7, 110, (1.0, 0.98, 0.94), 0.6, f"ep32_cls_l{int(x * 10)}")
    v.light(0.0, -2.0, 2.0, 70, (1.0, 0.97, 0.92), 0.6, "ep32_cls_fill")


def _sky(v):
    """하늘 (바닥 없음): 해·달·행성은 발광 원판 인스턴스. 요일 칸 판이 보이도록 앞에서 비추는 조명만 둠."""
    v.light(0.0, -5.0, 0.6, 520, (0.92, 0.95, 1.0), 1.0, "ep32_sky_l0")
    v.light(-3.5, -5.0, 3.2, 420, (0.92, 0.95, 1.0), 1.0, "ep32_sky_l1")
    v.light(3.5, -5.0, -2.0, 420, (0.92, 0.95, 1.0), 1.0, "ep32_sky_l2")
    v.light(20.0, -5.0, 0.8, 420, (0.92, 0.95, 1.0), 1.0, "ep32_sky_l3")


def _lamp(v, x, y, name, h=4.2):
    """가로등 (낮엔 꺼짐, 노을엔 켬 — 점광원 세기는 프레임마다 name으로 바꿈)."""
    v.box(x - 0.06, x + 0.06, y - 0.06, y + 0.06, 0, h, (0.25, 0.26, 0.28))
    v.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, h, h + 0.12, (0.25, 0.26, 0.28))
    v.box(x - 0.16, x + 0.16, y - 0.16, y + 0.16, h - 0.05, h, (1.0, 0.85, 0.55), jit=0, glow=True)
    v.light(x, y, h - 0.3, 1.0, (1.0, 0.8, 0.55), 0.3, name)
    if name not in LAMPS:
        LAMPS.append(name)


def _street(v):
    """퇴근길 거리 (x -24~24): 차도 y -3~3, 인도 y 3~6 / -6~-3, 양쪽 가게 건물. 노을이라 가로등이 켜짐."""
    rs = v.rs
    v.floor(-24, 24, -3, 3, (0.32, 0.32, 0.34), 0.5)
    for x in np.arange(-23.0, 24.0, 3.0):
        v.box(x, x + 1.4, -0.06, 0.06, 0.0, 0.012, (0.95, 0.95, 0.9), jit=0)
    for y0, y1 in ((3, 6), (-6, -3)):
        v.box(-24, 24, y0, y1, 0, 0.12, (0.62, 0.62, 0.62), jit=0)
        v.floor(-24, 24, y0, y1, (0.74, 0.70, 0.64), 0.5, "check", z=0.124)
    signs = [(0.95, 0.3, 0.3), (0.3, 0.8, 1.0), (1.0, 0.8, 0.2), (0.4, 1.0, 0.5), (1.0, 0.5, 0.85), (1.0, 0.6, 0.2)]
    k = 0
    for y, face in ((6.0, -1), (-6.0, 1)):
        x = -24.0
        while x < 24:
            w = float(rs.uniform(4.5, 7.0))
            X.storefront(v, x, min(24.0, x + w), y, 5.0, float(rs.uniform(9, 15)), signs[k % 6], face=face, lit=0.35)
            x += w
            k += 1
    for n, (x, y) in enumerate(((-18, 5.6), (-10, 5.6), (-2, 5.6), (6.0, 5.6), (14, 5.6), (-14, -5.6), (-6, -5.6), (2, -5.6),
                                (10, -5.6), (18, -5.6))):
        _lamp(v, x, y, f"ep32_slamp{n}")
    for x, y in ((-12, 3.55), (-5, 3.55), (4.8, 3.55), (17.5, 3.55), (-20, -3.55), (22, -3.55)):
        X.tree(v, x, y)
    v.light(0.0, 1.5, 3.0, 160, (1.0, 0.9, 0.78), 1.0, "ep32_street_fill")


def _cafe(v):
    """카페 (x -3.5~3.5, y -3~3, 앞 -y가 열림, 벽 높이 3.2): 뒷벽 가운데 벽 달력(움직이는 소품), 왼쪽 위 '카페' 간판, 오른쪽 계산대,
    가운데 긴 탁자. 벽돌 벽, 창, 펜던트 등."""
    WH = 3.4
    v.floor(-3.5, 3.5, -3, 3, (0.55, 0.38, 0.25), 0.25, "wood")
    v.wall((-3.5, 3), (3.5, 3), 0, WH, (0.88, 0.80, 0.68), 0.25, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, WH, (0.72, 0.44, 0.34), 0.25, face=-1, kind="brick")
    v.wall((3.5, -3), (3.5, 3), 0, WH, (0.88, 0.80, 0.68), 0.25, face=1)
    v.window(-2.4, 0.2, -3.49, 0.9, 2.3, night=False, face=1, axis="x")
    sign(v, "카페", -2.0, 3.1, 2.99, 0.04, (1.0, 0.86, 0.45))
    v.box(2.0, 3.4, 2.0, 2.6, 0, 1.0, (0.45, 0.3, 0.2))                                # 계산대
    v.box(1.95, 3.45, 1.95, 2.65, 1.0, 1.05, (0.92, 0.9, 0.86))
    v.box(2.5, 3.0, 2.2, 2.55, 1.05, 1.5, (0.75, 0.75, 0.78))                           # 커피 머신
    v.box(2.1, 2.3, 2.2, 2.35, 1.05, 1.15, (0.95, 0.95, 0.95))
    v.box(1.9, 3.4, 2.97, 2.99, 1.8, 2.6, (0.16, 0.16, 0.17))                           # 메뉴판
    for k in range(4):
        v.box(2.05, 2.05 + 0.6 + 0.25 * (k % 2), 2.96, 2.97, 2.4 - k * 0.17, 2.44 - k * 0.17, (0.95, 0.9, 0.75), jit=0, glow=True)
    X.table(v, CAFE_CX, 1.2, 3.0, 0.9, 0.74, (0.62, 0.45, 0.30))                       # 모임 탁자
    for x in (-0.8, 0.0, 0.8, 1.6):
        X.chair(v, x + 0.1, 1.95, -90)
    for x in (-0.4, 0.4, 1.2):
        X.chair(v, x + 0.1, 0.45, 90)
    X.chair(v, -1.45, 1.2, 0)
    X.chair(v, 2.05, 1.2, 180)
    for x, y, w in ((-2.1, -1.4, 0.8), (2.4, -1.5, 0.8)):                               # 가장자리 작은 탁자
        X.table(v, x, y, w, w, 0.74, (0.62, 0.45, 0.30))
    X.chair(v, -2.1, -0.8, -90)
    X.chair(v, -2.1, -2.0, 90)
    X.chair(v, 2.4, -0.9, -90)
    X.chair(v, 2.4, -2.1, 90)
    for x, y in ((-2.1, -1.4), (2.4, -1.5)):
        v.box(x - 0.05, x + 0.05, y - 0.05, y + 0.05, 0.74, 0.85, (0.97, 0.97, 0.95))
    for x in (-0.55, 0.15, 0.85, 1.55):                                                   # 탁자 위 컵·케이크
        v.box(x - 0.05, x + 0.05, 1.3, 1.4, 0.74, 0.84, (0.97, 0.97, 0.95))
    v.box(0.0, 0.3, 0.95, 1.2, 0.74, 0.78, (0.97, 0.97, 0.95))
    v.box(0.05, 0.25, 1.0, 1.15, 0.78, 0.9, (0.95, 0.65, 0.7))
    v.box(-3.3, -2.8, 2.3, 2.8, 0, 0.5, (0.35, 0.6, 0.45))                              # 화분
    v.box(-3.35, -2.75, 2.25, 2.85, 0.5, 1.4, (0.25, 0.55, 0.25), jit=0.1)
    for x, y in ((-1.1, 1.2), (1.8, 1.2)):
        v.box(x - 0.02, x + 0.02, y - 0.02, y + 0.02, 2.5, 3.4, (0.2, 0.2, 0.2), jit=0)   # 펜던트 등 (달력 양옆 바깥)
        v.box(x - 0.14, x + 0.14, y - 0.14, y + 0.14, 2.38, 2.5, (1.0, 0.82, 0.55), jit=0, glow=True)
    v.light(-1.1, 1.2, 2.1, 90, (1.0, 0.82, 0.55), 0.3, "ep32_cafe_p0")
    v.light(1.8, 1.2, 2.1, 90, (1.0, 0.82, 0.55), 0.3, "ep32_cafe_p1")
    v.light(0.3, -1.8, 2.2, 90, (1.0, 0.9, 0.78), 0.6, "ep32_cafe_fill")
    v.light(-2.8, 0.5, 2.0, 60, (0.85, 0.92, 1.0), 0.8, "ep32_cafe_win")
    v.light(0.3, 2.3, 2.9, 80, (1.0, 0.9, 0.78), 0.5, "ep32_cafe_wall")


def _sets():
    return (("bed", lambda w: _bed(w, "night")), ("bedm", lambda w: _bed(w, "morning")), ("metro", _metro),
            ("meet", _meet), ("cls", _cls), ("sky", _sky), ("street", _street), ("cafe", _cafe))


# ───────────────────────── 캐릭터 배치 · 움직임 ─────────────────────────
def st(set_, x, y, yaw, pose, z=0.0, **kw):
    """한 줄 안에서의 자리·자세. 선택 값: v 속도(m/s, 줄 시작부터) · stop 멈추는 τ(초) · pair 걷기 두 자세 · cad 걸음 주기 ·
    turn (τ0, τ1, 끝 yaw) · then (τ, 바뀐 자세) · alt (자세A, 자세B, 주기, 위상) 번갈아 · hop (높이 m, 주기 초, 시작 τ) 폴짝
    · road 인도/차도 높이 자동."""
    return dict(set=set_, x=x, y=y, z=z, yaw=yaw, pose=pose, **kw)


def _strap_up(xs, side):
    """손잡이(x=xs, y=±0.65)를 오른손으로 잡고 선 사람의 (x, y, yaw): side +1은 -x 쪽(카메라 쪽)을 봄."""
    return (xs + 0.13, 0.31, 180) if side > 0 else (xs - 0.13, -0.31, 0)


# 지하철 서 있는 사람: (손잡이 x, 쪽) / 앉은 사람: (x, 쪽, 자세)
STRAPS = [(-3.3, 1), (-2.1, 1), (-0.9, 1), (0.3, 1), (1.5, 1), (4.5, 1),
          (-2.7, -1), (-1.5, -1), (-0.3, -1), (0.9, -1), (2.1, -1), (3.3, -1)]
SEATS = [(-6.3, 1, "f_sitphone"), (-5.7, 1, "f_sit"), (-3.1, 1, "f_sit"), (-2.5, 1, "f_sitphone"), (-1.9, 1, "f_sit"),
         (-1.3, 1, "f_sitphone"), (1.3, 1, "f_sitphone"), (1.9, 1, "f_sit"), (2.5, 1, "f_sitphone"), (3.1, 1, "f_sit"),
         (5.4, 1, "f_sit"), (6.0, 1, "f_sitphone"), (6.6, 1, "f_sit"),
         (-6.3, -1, "f_sit"), (-5.7, -1, "f_sitphone"), (-3.1, -1, "f_sitphone"), (-2.5, -1, "f_sit"), (-1.9, -1, "f_sitphone"),
         (-1.3, -1, "f_sit"), (1.3, -1, "f_sit"), (1.9, -1, "f_sitphone"), (2.5, -1, "f_sit"), (3.1, -1, "f_sitphone"),
         (5.4, -1, "f_sitphone"), (6.0, -1, "f_sit"), (6.6, -1, "f_sit")]
STANDERS = [(-4.0, -0.9, -90, "f_stand"), (4.5, 0.9, 90, "f_stand"), (3.9, -0.8, -90, "f_phone"),
            (0.0, 0.85, 90, "f_stand"), (-0.2, -0.85, -90, "f_phone"), (5.6, 0.2, 180, "f_stand")]
MJ_STRAP = (4.5, 1)         # 민지가 잡은 손잡이 (지하철)


def cast():
    """[dict(name, hair, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    rs = np.random.default_rng(32)
    C = []
    WALK = ("walk_a", "walk_b")

    def add(name, hair, shirt, pants, at, scale=1.0):
        C.append(dict(name=name, hair=hair, shirt=shirt, pants=pants, at=at, scale=scale))

    def extra(name, at, scale=1.0, hair=None):
        add(name, int(rs.random() < 0.5) if hair is None else hair, EX_SH[int(rs.integers(len(EX_SH)))],
            X.PANTS[int(rs.integers(len(X.PANTS)))], at, scale)

    L = IX
    mx, my, myaw = _strap_up(*MJ_STRAP)
    # ── 민지 (연보라 셔츠 · 긴 머리)
    add("mj", 1, MJ_SH, MJ_PA, {
        L["hook"]: st("bed", X_BED, 1.7, -90, "sit", z=BED_TOP, then=(0.85, "sit_cheer"), hop=(0.07, 0.8, 0.85)),
        L["vanish"]: st("bed", X_BED, 1.7, -90, "sit_cheer", z=BED_TOP, hop=(0.07, 0.8, 0.0)),
        L["cheer"]: st("bed", X_BED, 1.25, -90, "cheer", z=BED_TOP, hop=(0.30, 0.72, 0.0)),
        L["relief"]: st("bed", X_BED, 1.55, -90, "sit", z=BED_TOP, then=(1.15, "sit_cheer"), hop=(0.06, 0.7, 1.15)),
        L["alarm"]: [(0.0, st("bedm", X_BED, 0.46, -90, "lie", z=BED_TOP)),
                     (0.62, st("bedm", X_BED, 1.75, -90, "sit_sleepy", z=BED_TOP, then=(1.25, "f_sit")))],
        L["metro"]: st("metro", mx, my, myaw, "f_up"),
        L["faces"]: st("metro", mx, my, myaw, "f_up"),
        L["boss"]: st("meet", -0.65, 1.15, -90, "f_sit"),
        L["cloud"]: st("bedm", X_BED, 1.75, -90, "f_sit", z=BED_TOP),
        L["window"]: st("bed", 1.75, 2.0, 90, "smile"),
        L["commute"]: st("street", -4.2, 4.3, 0, "stand", z=0.12, v=(1.25, 0.0), pair=("w_a", "w_b"), cad=0.3),
        L["cafe"]: st("cafe", 0.1, 1.95, -90, "sit_smile", alt=("sit_smile", "sit_laugh", 0.46, 0.0)),
        L["smile"]: st("cafe", 0.1, 1.95, -90, "sit_smile"),
        L["group"]: st("cafe", 0.1, 1.95, -90, "sit_toast", alt=("sit_toast", "sit_smile", 0.9, 0.0)),
        L["ask"]: st("cafe", 0.1, 1.95, -90, "sit_smile", alt=("sit_smile", "sit_laugh", 0.7, 0.0))}, 1.0)
    # ── 부장님 (회색 셔츠 · 빨간 넥타이): 화면 옆에서 요일 칸을 가리킴
    add("boss", 0, BOSS_SH, BOSS_PA, {
        L["boss"]: st("meet", 2.35, 2.35, -90, "boss_point", then=(2.2, "boss_talk"))}, 1.04)
    # ── 학생 친구 둘 (교실)
    add("st1", 0, ST1_SH, ST1_PA, {
        L["class"]: st("cls", -0.6, 0.9, -90, "f_sit", then=(1.6, "f_sitconf"))}, 0.9)
    add("st2", 1, ST2_SH, ST2_PA, {
        L["class"]: st("cls", 0.6, 0.9, -90, "f_sit", alt=("f_sit", "f_sitphone", 1.3, 0.0))}, 0.9)
    for k, (x, y, pose) in enumerate(((-1.7, 0.9, "f_sit"), (1.7, 0.9, "f_sitconf"), (-1.15, 2.0, "f_sit"), (0.0, 2.0, "f_sit"),
                                      (1.15, 2.0, "f_sitphone"))):
        extra(f"cl{k}", {L["class"]: st("cls", x, y, -90, pose)}, 0.9)
    # ── 지하철: 서 있는 사람 · 앉은 사람 · 문 앞 사람
    for k, (xs, side) in enumerate(STRAPS):
        if (xs, side) == MJ_STRAP:
            continue
        x, y, yaw = _strap_up(xs, side)
        at = {L["metro"]: st("metro", x, y, yaw, "f_up")}
        if not 0.6 < x < 4.2:                       # 6번 줄은 카메라가 지나는 자리를 비워 둠
            at[L["faces"]] = at[L["metro"]]
        extra(f"ms{k}", at)
    for k, (x, side, pose) in enumerate(SEATS):
        at = st("metro", x, 1.2 * side, -90 * side, pose)
        extra(f"mq{k}", {L["metro"]: at, L["faces"]: at})
    for k, (x, y, yaw, pose) in enumerate(STANDERS):
        at = st("metro", x, y, yaw, pose)
        extra(f"mt{k}", {L["metro"]: at} if 0.6 < x < 4.2 else {L["metro"]: at, L["faces"]: at})
    # ── 회의실: 탁자 양쪽 직원들 (민지는 건너편 자리)
    for k, (x, pose) in enumerate(((-1.9, "f_sit"), (0.6, "f_sitconf"), (1.85, "f_sit"))):
        extra(f"fr{k}", {L["boss"]: st("meet", x, 1.15, -90, pose)})
    for k, (x, pose) in enumerate(((-1.9, "f_sitphone"), (-0.65, "f_sit"), (0.6, "f_sit"), (1.85, "f_sitconf"))):
        extra(f"nr{k}", {L["boss"]: st("meet", x, -0.75, 90, pose)})
    # ── 거리: 퇴근하는 사람들 (인도 y 3~6, 위쪽/아래쪽 오가는 줄)
    for k in range(16):
        lane = [3.6, 4.2, 4.8, 5.4, 3.8, 5.0][k % 6] + float(rs.uniform(-0.1, 0.1))
        d = 1.0 if k % 2 else -1.0
        x0 = float(rs.uniform(-14, 10))
        extra(f"w{k}", {L["commute"]: st("street", x0, lane, 0 if d > 0 else 180, "stand", z=0.12, v=(d * float(rs.uniform(0.9, 1.4)), 0.0),
                                         pair=WALK, cad=0.3)})
    # ── 카페: 단체 (건너편 좌석은 카메라를 봄) + 가족 + 손님
    shirts = [(0.85, 0.30, 0.28), (0.25, 0.45, 0.80), (0.35, 0.65, 0.40), (0.95, 0.55, 0.25), (0.92, 0.55, 0.60)]
    cf = [L["cafe"], L["smile"], L["group"], L["ask"]]
    for k, (name, x, y, yaw, hair, sh, sc) in enumerate((
            ("fa", -0.7, 1.95, -90, 1, shirts[0], 1.0), ("fb", 0.9, 1.95, -90, 0, shirts[1], 1.04), ("fc", 1.7, 1.95, -90, 1, shirts[2], 1.0),
            ("mom", -1.45, 1.2, 0, 1, shirts[4], 1.0), ("kid", 0.6, 0.45, 90, 0, (0.95, 0.80, 0.35), 0.72),
            ("sis", 1.4, 0.45, 90, 1, (0.45, 0.75, 0.85), 0.78), ("dad", 2.05, 1.2, 180, 0, (0.38, 0.55, 0.45), 1.04))):
        at = {ln: st("cafe", x, y, yaw, "sit_smile", alt=("sit_smile", "sit_laugh", 0.42 + 0.09 * k, 0.11 * k)) for ln in cf}
        at[L["group"]] = st("cafe", x, y, yaw, "sit_toast", alt=("sit_toast", "sit_smile", 0.9, 0.12 * k))
        add(name, hair, sh, X.PANTS[k % len(X.PANTS)], at, sc)
    for k, (x, y, yaw, hair) in enumerate(((-2.1, -0.8, -90, 1), (-2.1, -2.0, 90, 0), (2.4, -0.9, -90, 0), (2.4, -2.1, 90, 1))):
        extra(f"cu{k}", {ln: st("cafe", x, y, yaw, "sit_smile") for ln in cf}, 1.0, hair)
    extra("bar", {ln: st("cafe", 2.7, 1.75, -90, "smile") for ln in cf})
    return C


def _poses_of(s):
    out = {s["pose"]}
    if "pair" in s:
        out |= set(s["pair"])
    if "then" in s:
        out.add(s["then"][1])
    if "alt" in s:
        out |= set(s["alt"][:2])
    return out


_W = {}


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
    hp = a.get("hop")
    if hp and tau >= hp[2]:
        d["z"] += hp[0] * abs(math.sin(math.pi * (tau - hp[2]) / hp[1]))
    d["zs"] = a["z"]                                  # 카메라가 따라갈 매끈한 높이 (걸음·폴짝 출렁임 제외)
    if a.get("road"):
        d["z"] = 0.12 if abs(d["y"]) >= 3.0 else 0.0
        d["zs"] = 0.12 * ramp(abs(d["y"]), 2.6, 3.4)
    d["scale"] = c["scale"]
    return d


# ───────────────────────── 소품 (일반 상자 F · 발광 상자 G · 달력 칸 T · 말풍선 B · 해/달/행성 O) ─────────────────────────
# 상자 = (중심, 크기, 회전(라디안), 색) — 세트 좌표.  칸 = (위치, 크기 배율, 회전, 이름 (종류, 키)).
QUILT, HEM = (0.45, 0.58, 0.88), (0.93, 0.95, 0.99)
BOARD, BAND_C = (0.97, 0.96, 0.92), (0.93, 0.40, 0.36)
SIL = (0.10, 0.09, 0.14)                                 # 창밖 사람 그림자 색
CAL = {"bed": (X_BED, 2.46, 2.62), "bedm": (X_BED, 2.46, 2.62), "cafe": (CAFE_CX, 2.96, 2.52)}
T_POP, T_SLIDE, SLIDE_DUR = 0.55, 0.95, 0.55           # 훅에서 '월' 열이 터지는 때 · 옆 열이 당겨 오기 시작하는 때 · 당겨 오는 시간(초)
CAL_H = BAND + HP + 4 * DP + CAL_MARGIN                 # 달력 판 높이
BOUNCE = [(1.0, 0.85, 0.3), (1.0, 0.55, 0.7), (1.0, 1.0, 0.9), (0.5, 0.9, 0.75), (0.55, 0.75, 1.0)]


def back_out(x, over=1.9):
    """0→1로 가며 살짝 넘쳤다 돌아오는 곡선 (easeOutBack)."""
    x = clamp(x)
    y = x - 1.0
    return 1.0 + (over + 1.0) * y ** 3 + over * y ** 2


def burst(c, tau, n=8, r=0.4, life=0.7, cols=BOUNCE, s0=0.07, seed=0):
    """c에서 사방으로 터져 나가는 발광 반짝이 (tau = 터진 뒤 초). 앞(-y)으로도 조금 튐."""
    out = []
    if tau <= 0 or tau > life:
        return out
    f = tau / life
    for k in range(n):
        a = 2 * math.pi * (k + 0.37 * seed) / n + 0.7 * (k % 3)
        rr = r * (0.45 + 0.55 * ((k * 5 + seed) % 7) / 6.0) * math.sqrt(f)
        s = s0 * (1 - f) * (1 + 0.5 * (k % 2))
        out.append(((c[0] + rr * math.cos(a), c[1] - 0.12 * f - 0.03 * (k % 3), c[2] + rr * math.sin(a) * 0.9),
                    (s, s, s), (a, f * 4, 0), cols[(k + seed) % len(cols)]))
    return out


def sparkles(c, tl, t0, n=14, r=0.9, life=0.9, cols=BOUNCE, s0=0.11):
    """c 둘러싸고 터져 나가는 발광 반짝이 (ep27과 같은 모양)."""
    out = []
    tau = tl - t0
    if tau <= 0 or tau > life:
        return out
    f = tau / life
    for k in range(n):
        a = 2 * math.pi * k / n + 0.7 * (k % 3)
        rr = r * (0.35 + 0.65 * ((k * 5) % 7) / 6.0) * math.sqrt(f)
        s = s0 * (1 - f) * (1 + 0.5 * (k % 2))
        out.append(((c[0] + rr * math.cos(a), c[1] + 0.15 * math.sin(a * 2), c[2] + rr * math.sin(a) * 0.9 + 0.15),
                    (s, s, s), (a, f * 4, 0), cols[k % len(cols)]))
    return out


def twinkles(box, t, n=8, col=(1.0, 0.98, 0.8), s0=0.05):
    """반짝이는 별 점: box = (x0, x1, y, z0, z1)."""
    out = []
    for k in range(n):
        q = ((k * 0.6180339) % 1.0, (k * 0.7548777 + 0.3) % 1.0)
        s = s0 * (0.25 + 0.75 * max(0.0, math.sin(2 * math.pi * (0.55 * t + 0.31 * k))) ** 2)
        out.append(((box[0] + (box[1] - box[0]) * q[0], box[2], box[3] + (box[4] - box[3]) * q[1]), (s, s, s), (0, 0, 0.78), col))
    return out


CLOUD = ["..##..###..", ".#########.", "###########", ".#########."]       # 먹구름 도트 (위 → 아래)
CL_LIGHT, CL_DARK, CL_EYE = (0.60, 0.62, 0.68), (0.40, 0.42, 0.50), (0.12, 0.13, 0.18)


def cloud(c, s=1.0, face=True, cell=0.09):
    """먹구름(월요병) 일반 상자 목록. c = 아래 가운데. 얼굴: 처진 눈·꾹 다문 입."""
    out = []
    n = len(CLOUD)
    for r, c0, c1 in _runs(CLOUD):
        w = (c1 - c0 + 1) * cell * s
        x = c[0] + ((c0 + c1 + 1) / 2.0 - 5.5) * cell * s
        z = c[2] + (n - 1 - r + 0.5) * cell * s
        out.append(((x, c[1], z), (w, 0.30 * s, cell * s), (0, 0, 0), CL_DARK if r == n - 1 else CL_LIGHT))
    if face:
        for ex in (-0.17, 0.17):
            out.append(((c[0] + ex * s, c[1] - 0.16 * s, c[2] + 0.22 * s), (0.055 * s, 0.03 * s, 0.075 * s), (0, 0, 0), CL_EYE))
        out.append(((c[0], c[1] - 0.16 * s, c[2] + 0.13 * s), (0.17 * s, 0.03 * s, 0.03 * s), (0, 0, 0), CL_EYE))
        for ex in (-0.095, 0.095):
            out.append(((c[0] + ex * s, c[1] - 0.16 * s, c[2] + 0.105 * s), (0.03 * s, 0.03 * s, 0.05 * s), (0, 0, 0), CL_EYE))
    return out


def rain(c, t, w=0.9, fall=0.9, n=14, s=1.0):
    """먹구름 아래로 떨어지는 빗줄기 (파란 작은 상자). c = 구름 아래 가운데."""
    out = []
    for k in range(n):
        p = (t * 1.5 + k * 0.381) % 1.0
        x = c[0] + (((k * 0.618) % 1.0) - 0.5) * w * s
        out.append(((x, c[1] - 0.2 * s, c[2] - fall * p * s), (0.03 * s, 0.03 * s, 0.11 * s), (0, 0, 0.0), (0.45, 0.65, 0.98)))
    return out


def bolt(c, s=1.0):
    """번개: c(구름 아래)에서 지그재그로 내려오는 발광 상자."""
    pts = [(0.02, 0.0), (0.14, -0.2), (-0.06, -0.38), (0.10, -0.62), (-0.02, -0.86)]
    out = []
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        out.append(((c[0] + (x0 + x1) / 2 * s, c[1] - 0.2 * s, c[2] + (z0 + z1) / 2 * s), (0.055 * s, 0.04 * s, (abs(z1 - z0) + 0.06) * s),
                    (0, 0.5 * math.atan2(x1 - x0, abs(z1 - z0)), 0), (1.0, 0.95, 0.4)))
    return out


def steam(x, y, z0, t, n=4, rise=0.4, size=0.05):
    """김: 하얀 작은 상자가 솟아 오르며 작아짐."""
    out = []
    for k in range(n):
        p = (k / n + t / 1.5) % 1.0
        s = size * (1 - 0.6 * p)
        out.append(((x + 0.04 * math.sin(6.3 * (p + k * 0.37)), y + 0.03 * math.cos(6.3 * (p + k * 0.21)), z0 + rise * p),
                    (s, s, s), (p * 3, k, p * 2), (0.97, 0.97, 0.98)))
    return out


def quilt(edge, shake=0.0, ph=0.0, top=0.89):
    """누운 민지 몸 위 이불: 침대 폭 전체를 덮는 납작한 층 + 몸을 덮는 두둑한 언덕(edge = 머리 쪽 끝 y) + 하얀 접힌 단."""
    sx, sz = shake * math.sin(ph * 9.0), shake * math.cos(ph * 11.0)
    by = max(edge - 0.3, 0.8)
    return [((X_BED + sx, (0.23 + by) / 2, BED_TOP + 0.10), (1.30, by - 0.23, 0.20), (0, 0, 0), QUILT),
            ((X_BED + sx, (0.34 + edge) / 2, (0.64 + top) / 2 + sz), (0.80, edge - 0.34, top - 0.64), (0, 0, 0), QUILT),
            ((X_BED + sx, edge - 0.05, top + sz), (0.82, 0.10, 0.03), (0, 0, 0), HEM)]


def pile():
    """앉은 민지 발치(침대 앞쪽)에 뭉쳐 둔 이불."""
    return [((X_BED, 0.65, BED_TOP + 0.11), (1.25, 0.8, 0.22), (0, 0, 0), QUILT),
            ((X_BED - 0.1, 0.55, BED_TOP + 0.25), (0.8, 0.5, 0.18), (0, 0, 0.25), (0.42, 0.58, 0.88))]


ALARM_P = (X_BED + 1.02 + 0.08, 2.2, 0.5)         # 협탁 위 알람시계 자리 (바닥 가운데)


def alarm(tl, ringing):
    """알람시계: 몸통·빨간 화면·종 둘·망치. 울리면 몸통이 바르르 떨리고 종이 흔들림. (일반 상자, 발광 상자)"""
    x, y, z = ALARM_P
    j = 0.012 if ringing else 0.0
    ox, oz = j * math.sin(2 * math.pi * 23 * tl), j * math.cos(2 * math.pi * 29 * tl)
    sw = 0.25 * math.sin(2 * math.pi * 18 * tl) if ringing else 0.0
    F = [((x + ox, y, z + 0.08 + oz), (0.17, 0.10, 0.16), (0, 0, 0), (0.95, 0.40, 0.38)),
         ((x + ox - 0.055, y, z + 0.185 + oz), (0.06, 0.06, 0.04), (0, sw, 0), (1.0, 0.85, 0.3)),
         ((x + ox + 0.055, y, z + 0.185 + oz), (0.06, 0.06, 0.04), (0, -sw, 0), (1.0, 0.85, 0.3)),
         ((x + ox, y, z + 0.215 + oz), (0.014, 0.014, 0.05), (0, 0.4 * sw, 0), (0.3, 0.3, 0.32)),
         ((x + ox - 0.06, y, z + 0.015 + oz), (0.03, 0.05, 0.03), (0, 0, 0), (0.3, 0.3, 0.32)),
         ((x + ox + 0.06, y, z + 0.015 + oz), (0.03, 0.05, 0.03), (0, 0, 0), (0.3, 0.3, 0.32))]
    G = [((x + ox, y - 0.055, z + 0.085 + oz), (0.12, 0.012, 0.06), (0, 0, 0), (1.0, 0.25, 0.2 if ringing else 0.1))]
    if ringing:                                         # 울림 표시: 시계 양옆 바깥으로 퍼지는 짧은 막대
        for k in range(3):
            p = (tl * 3.0 + k / 3.0) % 1.0
            for sgn in (-1, 1):
                G.append(((x + sgn * (0.13 + 0.12 * p), y - 0.07, z + 0.12 + 0.03 * (k - 1) * 2), (0.02, 0.02, 0.06 * (1 - p) + 0.02),
                          (0, 0, 0), (1.0, 0.9, 0.5)))
    return F, G


def calendar(setn, i, tl, hot=False, cloud_hop=None):
    """벽 달력 한 장 → (일반 상자, 발광 상자, 칸 목록). 훅(0번 줄)에선 '월' 열이 터지고 옆 열이 당겨 오며, 그 뒤엔 6열.
    hot이면 '화' 칸이 강조(분홍) 판."""
    cx, cy, cz = CAL[setn]
    hook = i == IX["hook"]
    if hook:
        k = back_out((tl - T_SLIDE) / SLIDE_DUR, 1.2) if tl > T_SLIDE else 0.0
    else:
        k = 1.0
    kb = clamp(k)
    zt = cz + CAL_H / 2
    zh = zt - BAND - HP / 2
    F, G, T = [], [], []
    wb = 7 * CW + 0.14 - CW * kb
    F.append(((cx, cy + 0.015, cz), (wb, 0.03, CAL_H), (0, 0, 0), BOARD))
    F.append(((cx, cy - 0.01, zt - BAND / 2), (wb, 0.02, BAND), (0, 0, 0), BAND_C))
    for sx in (-0.45, 0.45):
        F.append(((cx + sx, cy - 0.03, zt - 0.045), (0.05, 0.03, 0.05), (0, 0, 0), (0.25, 0.22, 0.28)))
    for c in range(7):
        x0 = cx + (c - 3) * CW
        if c == 1:
            xf = x0
        elif c == 0:
            xf = cx + (-2.5) * CW
        else:
            xf = cx + ((c - 1) - 2.5) * CW
        x = x0 + (xf - x0) * k
        for r in range(-1, 4):                         # -1 = 요일 줄
            z = zh if r < 0 else zt - BAND - HP - DP * (r + 0.5)
            s = 1.0
            if c == 1:
                tau = (tl - (T_POP + 0.07 * (r + 1))) if hook else 99.0
                s = burst_out(tau)
                if hook and tau > 0.10:
                    G += burst((x, cy - 0.06, z), tau - 0.10, 12 if r < 0 else 8, 0.5 if r < 0 else 0.32, 0.75, BOUNCE, 0.105 if r < 0 else 0.08, seed=r + 2)
            if s <= 0.001:
                continue
            if r < 0:
                kind = "wdh" if (hot and c == 2) else "wd"
                T.append(((x, cy - 0.003, z), s, (0, 0, 0), (kind, WD[c])))
            else:
                T.append(((x, cy - 0.003, z), s, (0, 0, 0), ("dt", DATES[r][c])))
    return F, G, T


def col_x(setn, col6):
    """달력이 6열이 된 뒤 col6번째 열(0~5)의 가운데 x."""
    cx = CAL[setn][0]
    return cx + (col6 - 2.5) * CW


def tile_billboard(az):
    """칸을 카메라 쪽으로 돌리는 z 회전(라디안): 칸 앞면은 -y."""
    return math.radians(az + 90.0)


def planets_layout():
    """하늘 장면 해·달·행성 자리와 이름·요일 글자 (세트 좌표)."""
    return [("sun", (-1.4, 0.0, 3.3), "일", 0.2), ("moon", (1.6, 0.0, 3.4), "월", 0.6),
            ("mars", (-1.9, 0.0, 1.2), "화", 1.0), ("mercury", (0.0, 0.0, 1.2), "수", 1.3), ("jupiter", (1.9, 0.0, 1.2), "목", 1.6),
            ("venus", (-1.1, 0.0, -0.9), "금", 1.9), ("saturn", (1.4, 0.0, -0.9), "토", 2.2)]


BODY_LABEL_DZ = {"sun": -1.55, "moon": -1.05, "mars": -1.0, "mercury": -0.9, "jupiter": -1.25, "venus": -1.0, "saturn": -1.0}


def props(i, tl, du, u, S, t, cam):
    """줄 i의 소품 → (일반 상자 F, 발광 상자 G, 칸 T, 말풍선 B, 해/달/행성 O). 모두 세트 좌표."""
    F, G, T, B, O = [], [], [], [], []
    L = IX
    mj = S.get("mj")

    def cal(setn, **kw):
        f, g, tt = calendar(setn, i, tl, **kw)
        F.extend(f)
        G.extend(g)
        T.extend(tt)
    if i == L["hook"]:
        cal("bed")
        cx, cy, cz = CAL["bed"]
        zh = cz + CAL_H / 2 - BAND - HP / 2
        B.append(dict(at=(cx + (1 - 3) * CW, cy - 0.06, zh + HP / 2), name="bang", t0=T_POP + 0.02, off=(0, 26), cpx=7.0, life=0.95))
    elif i == L["vanish"]:
        cal("bed")
        cx, cy, cz = CAL["bed"]
        zh = cz + CAL_H / 2 - BAND - HP / 2
        for n_ in range(2):                                    # 일|화가 맞닿은 자리에서 반짝
            G += sparkles((cx - 2.0 * CW, cy - 0.12, zh), tl, 0.15 + 0.9 * n_, 8, 0.32, 0.6, BOUNCE, 0.06)
    elif i == L["cheer"]:
        cal("bed")
        for k_ in range(3):
            G += sparkles((X_BED, 1.4, 1.8), tl, 0.30 + 0.72 * k_, 10, 0.8, 0.7, BOUNCE, 0.09)
        for k_, (wx, wz) in enumerate(((1.2, 1.25), (1.62, 1.55), (2.22, 1.28), (2.3, 1.68))):     # 창밖 건너편 집들: 만세 하는 직장인 그림자
            G.append(((wx, 2.425, wz), (0.17, 0.02, 0.22), (0, 0, 0), (1.0, 0.78, 0.4)))
            bob = 0.02 * math.sin(2 * math.pi * 2.6 * t + 1.9 * k_)
            F += [((wx, 2.41, wz - 0.03), (0.05, 0.02, 0.08), (0, 0, 0), SIL), ((wx, 2.41, wz + 0.04 + bob), (0.04, 0.02, 0.04), (0, 0, 0), SIL),
                  ((wx - 0.04, 2.41, wz + 0.04 + bob), (0.02, 0.02, 0.07), (0, 0, 0), SIL), ((wx + 0.04, 2.41, wz + 0.04 + bob), (0.02, 0.02, 0.07), (0, 0, 0), SIL)]
    elif i == L["relief"]:
        cal("bed")
        if mj:
            hx, hy, hz = head_pt(mj)
            if tl < 1.15:
                F += cloud((hx, hy, hz + 0.22 + 0.03 * math.sin(2 * math.pi * 1.6 * tl)), 0.72, True)
            else:
                G += burst((hx, hy - 0.05, hz + 0.4), tl - 1.15, 10, 0.55, 0.8, [(0.75, 0.78, 0.85), (1.0, 1.0, 0.95)] + BOUNCE, 0.055, seed=1)
                G += sparkles((hx, hy - 0.1, hz + 0.1), tl, 1.2, 12, 0.7, 0.9, BOUNCE, 0.09)
    elif i == L["alarm"]:
        cal("bedm")
        ring = tl > 0.05
        f, g = alarm(tl, ring)
        F += f
        G += g
        B.append(dict(at=(ALARM_P[0], ALARM_P[1] - 0.06, ALARM_P[2] + 0.3), name="alarm", t0=0.05, off=(60, 36), cpx=7.0, life=None))
        if u < 0.62:
            F += quilt(1.85, shake=0.008, ph=tl * 6.0, top=0.92)
        else:
            e = 1.85 - 0.9 * ramp(u, 0.62, 0.72)
            F += (quilt(e, top=0.92) if e > 1.0 else []) + pile()
    elif i == L["faces"]:
        for n_, nm in enumerate(("mj", "mq6", "mq7", "mq8", "mq9")):
            d = S.get(nm)
            if d:
                hx, hy, hz = head_pt(d)
                F += cloud((hx, hy, hz + 0.12 + 0.02 * math.sin(2 * math.pi * 1.3 * t + n_)), 0.42, False)
    elif i == L["boss"]:
        # 발표 화면: 요일 칸 여섯 (화 강조)
        sx = [(-2.5 + k) * CW * 1.45 for k in range(6)]
        for k_, c in enumerate("일화수목금토"):
            kind = "wdh" if c == "화" else "wd"
            bob = 0.05 * ramp(tl, 1.3, 1.6) * math.sin(2 * math.pi * 2.2 * tl) if c == "화" else 0.0
            sc_ = 1.45 + (0.35 * ramp(tl, 1.3, 1.6) if c == "화" else 0.0)
            T.append(((sx[k_], 2.905, 1.78 + bob), sc_, (0, 0, 0), (kind, c)))
        for nm in ("fr0", "fr1", "fr2", "mj"):
            d = S.get(nm)
            if d:
                hx, hy, hz = head_pt(d)
                F += cloud((hx, hy, hz + 0.12 + 0.02 * math.sin(2 * math.pi * 1.3 * t + len(nm))), 0.42, False)
    elif i == L["class"]:
        for c, ch in enumerate("화수목금"):
            T.append((((c - 1.5) * 0.33, 2.935, 2.5), 1.6 if ch != "화" else 1.6 + 0.12 * math.sin(2 * math.pi * 1.8 * tl), (0, 0, 0),
                      ("wdh" if ch == "화" else "wd", ch)))
        for nm in ("st1", "st2"):
            d = S.get(nm)
            if d:
                hx, hy, hz = head_pt(d)
                F += cloud((hx, hy, hz + 0.12 + 0.02 * math.sin(2 * math.pi * 1.3 * t + len(nm))), 0.5, False)
                F += [(rel(d, -0.32, 0, 0.82), (0.16, 0.34, 0.42), (0, 0, math.radians(d["yaw"])), (0.85, 0.30, 0.28))]    # 등 뒤 책가방
    elif i == L["cloud"]:
        cx, cy, cz = CAL["bedm"]
        cal("bedm", hot=tl > 1.0)
        tx = col_x("bedm", 1)
        zt = cz + CAL_H / 2
        k = ramp(tl, 0.15, 1.15)
        px = tx + (1.0 - k) * -2.6
        pz = zt + 0.3 + 0.05 * math.sin(2 * math.pi * 1.2 * tl) + 0.4 * (1.0 - k)
        F += cloud((px, cy - 0.25, pz), 1.15, True)
        if k > 0.95:
            F += rain((px, cy - 0.25, pz), t, 0.95, 1.3)
            if int(tl * 7.0) % 6 == 0 and tl > 1.1:
                G += bolt((px + 0.1, cy - 0.25, pz), 1.1)
        F += pile()
    elif i == L["window"]:
        cal("bed")
        G += twinkles((1.15, 2.4, 2.44, 1.9, 2.4), t, 7)
    elif i == L["commute"]:
        for n_, nm in enumerate(("mj", "w1", "w3", "w6", "w9", "w12")):
            d = S.get(nm)
            if not d:
                continue
            hx, hy, hz = head_pt(d)
            ang = tile_billboard(cam["az"])
            ca, sa = math.cos(ang), math.sin(ang)
            if nm == "mj":
                for sgn, ch in ((-1, "토"), (1, "일")):
                    p = ramp(tl, 0.1 + 0.2 * (sgn > 0), 0.5 + 0.2 * (sgn > 0))
                    T.append(((hx + sgn * 0.17 * ca, hy + sgn * 0.17 * sa, hz + 0.45 + 0.04 * math.sin(2 * math.pi * 1.4 * t + sgn)),
                              p * 1.15, (0, 0, ang), ("wd", ch)))
            else:
                p = ramp(tl, 0.3 + 0.18 * n_, 0.7 + 0.18 * n_)
                T.append(((hx, hy, hz + 0.4 + 0.04 * math.sin(2 * math.pi * 1.4 * t + n_)), p * 0.9, (0, 0, ang),
                          ("wd", "토" if n_ % 2 else "일")))
    elif i in (L["cafe"], L["smile"], L["group"], L["ask"]):
        cx, cy, cz = CAL["cafe"]
        if i == L["ask"]:
            cal("cafe", hot=False)
            zt = cz + CAL_H / 2
            stops = [1, 2, 3, 4, 5, 0, 1]
            dwell, trav = 0.22, 0.2
            tk = tl
            xs = [col_x("cafe", c) for c in stops]
            n_ = int(tk // (dwell + trav))
            n_ = min(n_, len(stops) - 1)
            ph = tk - n_ * (dwell + trav)
            x0, x1 = xs[n_], xs[min(n_ + 1, len(stops) - 1)]
            k = ramp(ph, dwell, dwell + trav) if n_ < len(stops) - 1 else 0.0
            px = x0 + (x1 - x0) * k
            pz = zt + 0.27 + 0.2 * math.sin(math.pi * k)
            F += cloud((px, cy - 0.25, pz), 0.85, True)
            if mj:
                hx, hy, hz = head_pt(mj)
                B.append(dict(at=(hx, hy, hz), name="q", t0=0.2, off=(40, 20), cpx=7.0, life=None))
        else:
            cal("cafe")
        if i == L["cafe"]:
            for n_, (nm, t0) in enumerate((("fa", 0.35), ("fb", 0.9), ("mom", 1.45), ("dad", 1.95))):
                d = S.get(nm)
                if d:
                    hx, hy, hz = head_pt(d)
                    B.append(dict(at=(hx, hy, hz), name="heart", t0=t0, off=(18, 0), cpx=6.5, life=1.2))
        if i == L["smile"] and mj:
            hx, hy, hz = head_pt(mj)
            B.append(dict(at=(hx, hy, hz), name="heart", t0=0.5, off=(30, 6), cpx=8.0, life=1.4))
            G += sparkles((hx, hy - 0.15, hz - 0.1), tl, 0.3, 10, 0.55, 0.9, BOUNCE, 0.07)
        if i == L["group"]:
            for k_, nm in enumerate(("mj", "fa", "fb", "fc", "mom", "kid", "sis", "dad")):
                d = S.get(nm)
                if d and d["pose"] == "sit_toast":
                    hx, hy, hz = hand_pt(d, "R", 0.06)
                    F += [((hx, hy, hz + 0.07), (0.075, 0.075, 0.13), (0, 0, 0), (0.97, 0.97, 0.95)),
                          ((hx, hy, hz + 0.1), (0.07, 0.07, 0.06), (0, 0, 0), (0.55, 0.32, 0.2))]
            for k_ in range(3):
                G += sparkles((CAFE_CX + 0.2, 1.25, 1.55), tl, 0.5 + 0.9 * k_, 10, 0.55, 0.6, BOUNCE, 0.06)
        for (sx_, sy_) in ((-0.55, 1.35), (0.15, 1.35), (0.85, 1.35)):
            F += steam(sx_, sy_, 0.85, t, 3, 0.3, 0.04)
    return F, G, T, B, O


def planet_items(i, tl):
    """하늘 장면(10번 줄) 해·달·행성 + 요일 칸 / 달 클로즈업(11번 줄) 큰 달 + '월' 칸 + 반짝이 → (O, T, G)."""
    O, T, G = [], [], []
    if i == IX["planets"]:
        for nm, p, ch, t0 in planets_layout():
            s = pop(tl - t0)
            if s > 0:
                O.append((p, s, (0, 0, 0), nm))
                sl = pop(tl - t0 - 0.18)
                if sl > 0:
                    T.append(((p[0], p[1] - 0.02, p[2] + BODY_LABEL_DZ[nm]), 2.3 * sl, (0, 0, 0), ("wd", ch)))
        G += twinkles((-4.0, 4.0, 0.5, -3.4, 5.4), tl, 12, (1.0, 0.98, 0.85), 0.07)
    elif i == IX["moon"]:
        O.append(((20.0, 0.0, 0.0), 1.0 + 0.02 * math.sin(2 * math.pi * 0.5 * tl), (0, 0, 0), "moonbig"))
        sl = pop(tl - 0.35)
        if sl > 0:
            T.append(((20.0 + 1.55, -0.3, -1.45 + 0.05 * math.sin(2 * math.pi * 1.1 * tl)), 3.4 * sl, (0, 0, math.radians(-6)), ("wd", "월")))
        G += twinkles((17.0, 23.0, 0.6, -4.5, 4.5), tl, 14, (1.0, 0.98, 0.85), 0.08)
    return O, T, G


# ───────────────────────── 말풍선 배치 ─────────────────────────
def bubbles(specs, tl, cam, o):
    """말풍선 목록 → [(꼬리 끝 위치(월드), 회전, 크기 배율, 그림 번호)]. 카메라 쪽을 보게 돌리고, 화면에서 한 칸이 cpx 픽셀이 되게 키움.
    at = 꼬리가 향하는 점(세트 좌표), off = 화면 픽셀 단위 이동(오른쪽·위가 +)."""
    az, el, lens, loc = cam["az"], cam["el"], cam["lens"], cam["loc"]
    right, up = cam_axes(az, el)
    out = []
    for k, sp in enumerate(specs):
        s0 = bub_scale(sp, tl)
        if s0 <= 0.0:
            continue
        a = (sp["at"][0] + o[0], sp["at"][1] + o[1], sp["at"][2])
        pxw = math.dist(a, loc) / (lens * 80.0)               # 화면 한 픽셀의 월드 크기(m): 1920px 높이 / 센서 24mm = 80px/mm
        ox, oz = sp["off"]
        p = [a[j] + right[j] * ox * pxw + up[j] * oz * pxw for j in range(3)]
        roll = 0.035 * math.sin(2 * math.pi * 0.9 * tl + k)
        s = sp["cpx"] * pxw / C0 * s0
        out.append((tuple(p), (roll, 0.0, math.atan2(loc[1] - p[1], loc[0] - p[0])), s, BUB_IX[sp["name"]]))
    return out


# ───────────────────────── 한 프레임 ─────────────────────────
N_FX, N_GL, N_TILE, N_BUB, N_BODY = 160, 150, 52, 6, 8


def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·소품·칸·말풍선·해/달/행성 점 배열, 카메라, 조명."""
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
    cam = cam_pose(shot, ul, S)
    o = OFF[cam["set"]]
    F, G, T, B, O = props(i, tau, dur, u, S, t, cam)
    O2, T2, G2 = planet_items(i, tau)
    O += O2
    T += T2
    G += G2

    def shift(items):
        return [((p[0] + o[0], p[1] + o[1], p[2]), s, r, c) for p, s, r, c in items]
    TT = [((p[0] + o[0], p[1] + o[1], p[2]), s, r, TILE_IX[key]) for p, s, r, key in T]
    OO = [((p[0] + o[0], p[1] + o[1], p[2]), s, r, BODY_ORDER.index(nm)) for p, s, r, nm in O]
    bub = bubbles(B, tau, cam, o)
    return dict(i=i, tl=tau, u=u, set=cam["set"], cam=cam, A=S, P=P, R=R, CO=CO, C2=C2, SC=SC, PO=PO, fx=shift(F), glow=shift(G),
                tiles=TT, bodies=OO, BP=[q[0] for q in bub], BR=[q[1] for q in bub], BS=[q[2] for q in bub],
                BPO=[q[3] for q in bub], env=env(i, tau, dur))


def _mat_glow(name, strength=3.0):
    """인스턴스 'col' 색으로 빛나는 재질 (반짝이·번개)."""
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
    v = X.Vox(32)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep32_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats() + [K.mat_simple("ep32_m_tie", (0.85, 0.15, 0.15), 0.6)]
    protos = [K.proto(ctx, "ep32_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep32_people", protos, len(W["C"]))
    # 달력 칸·요일 칸: 칸마다 원형 하나(판 + 글자), 점마다 'pose'로 칸을 고름
    tmats = [K.mat_simple("ep32_m_tile%d" % n, c, 0.6) for n, c in enumerate(TILE_MATS)]
    tiles = K.instancer_multi(ctx, "ep32_tiles", [K.proto(ctx, "ep32_tp_%02d" % n, K.join_bms(_tile_parts(K, *key)), tmats)
                                                  for n, key in enumerate(TILE_ORDER)], N_TILE)
    # 말풍선: 그림마다 원형 하나(판+꼬리+도트 글자), 재질은 전부 같은 목록
    bmats = [K.mat_simple("ep32_m_bub", (0.97, 0.97, 0.95), 0.6, emit=(1.0, 1.0, 1.0), estr=0.45),
             K.mat_simple("ep32_m_bord", (0.07, 0.08, 0.13), 0.8)]
    for n, ch in enumerate(PAL_ORDER):
        col = tuple(float(c) for c in PAL[ch])
        bmats.append(K.mat_simple("ep32_m_ico_%d" % n, col, 0.5, emit=None if ch == "K" else col, estr=0.9))
    bub = K.instancer_multi(ctx, "ep32_bub", [K.proto(ctx, "ep32_p_bub_" + n, K.join_bms(_bub_parts(K, n)), bmats)
                                              for n in BUB_NAMES], N_BUB)
    try:
        bub.visible_shadow = False
    except AttributeError:
        pass
    # 해·달·행성: 발광 도트 원판
    bm_ = [K.mat_simple("ep32_m_body_" + k, BODY_COLS[k], 0.5, emit=BODY_COLS[k], estr=1.7) for k in BODY_KEYS]
    bodies = K.instancer_multi(ctx, "ep32_bodies", [K.proto(ctx, "ep32_p_body_" + n, K.join_bms(_body_parts(K, n)), bm_)
                                                    for n in BODY_ORDER], N_BODY)
    cube = lambda: K.bm_cube(1, 1, 1)
    fx = K.instancer(ctx, "ep32_fx", K.proto(ctx, "ep32_p_fx", cube(), [K.mat_inst("ep32_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep32_glow", K.proto(ctx, "ep32_p_glow", cube(), [_mat_glow("ep32_m_glow")]), N_GL, vector_scale=True)

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
        for nm_ in LAMPS:
            lights[nm_].data.energy = e["lamp"]
        for name, en in e["lt"].items():
            lights[name].data.energy = en
        K.set_points(people, S["P"], scale=S["SC"], rot=S["R"], col=np.array(S["CO"], np.float32),
                     colors={"col2": np.array(S["C2"], np.float32)}, pose=S["PO"])
        n = len(S["BS"])
        BP, BR, BS, BPO = (np.zeros((N_BUB, 3), np.float32), np.zeros((N_BUB, 3), np.float32), np.zeros(N_BUB, np.float32),
                           np.zeros(N_BUB, np.float32))
        if n:
            BP[:n], BR[:n], BS[:n], BPO[:n] = S["BP"][:N_BUB], S["BR"][:N_BUB], S["BS"][:N_BUB], S["BPO"][:N_BUB]
        K.set_points(bub, BP, scale=BS, rot=BR, pose=BPO)
        for ob, items, cap in ((tiles, S["tiles"], N_TILE), (bodies, S["bodies"], N_BODY)):
            Pp, Ss, Rr, Kk = (np.zeros((cap, 3), np.float32), np.zeros(cap, np.float32), np.zeros((cap, 3), np.float32),
                              np.zeros(cap, np.float32))
            for k, (p, s, r, ix) in enumerate(items[:cap]):
                Pp[k], Ss[k], Rr[k], Kk[k] = p, s, r, ix
            K.set_points(ob, Pp, scale=Ss, rot=Rr, pose=Kk)
        boxes(fx, S["fx"], N_FX)
        boxes(gl, S["glow"], N_GL)

    ctx.on_frame(upd)
