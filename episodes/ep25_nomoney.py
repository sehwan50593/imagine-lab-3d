"""EP25 만약에 세상에서 돈이 사라진다면? (19편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
빈 지갑에서 돈이 날아가 사라짐(훅) → 폰 잔고 0 → 빈 지갑 줄 → 라면 하나=계란 두 개(손에서 손으로)
→ 미용실 머리 값은 빵 → 월급날 쌀 한 포대 → 서로 원하는 게 달라 헛바퀴 → "저는 빵 필요 없는데요"
→ 모두가 받아 주는 물건 라면(반짝) → 라면으로 계산 → 라면 지갑 → 쌓이는 라면 저금통 탑
→ 반전: 미국의 한 교도소에서 라면이 돈처럼 쓰였다는 연구 발표(Gibson-Light 2016)
→ 미용실·월급이 라면으로 돌아감 → 믿음 릴레이 → "당신 지갑 속 돈은 진짜 무엇일까요?"
근거(설명란): Gibson-Light, 미국사회학회(ASA) 2016 연례학회 발표 — 미국의 한 남성 주립 교도소에서 수감자·직원 약 60명을
면담한 결과 라면이 서비스·물건 값을 치르는 비공식 화폐로 쓰였음(한 교도소 사례). 물물교환의 한계는 Jevons 1875,
비슷한 사례로 전쟁포로수용소의 담배 화폐는 Radford 1945(Economica).
특수효과: 지폐·라면·계란·빵·쌀 포대·지갑·폰 = 블록 소품 인스턴스(goods). 지폐는 지갑 위로 떠올라 작아지며 사라지고,
교환 장면에선 물건이 두 사람의 손 사이를 포물선으로 넘어가며, 라면은 저금통 안에 하나씩 떨어져 탑으로 쌓인다.
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
OFF = {"home": (0, 0), "mart": (300, 0), "salon": (600, 0), "office": (900, 0), "cell": (1200, 0),
       "stage": (1500, 0), "home_pm": (1800, 0)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 세상에서 돈이 사라진다면 어떻게 될까요?", gap=0.7, shot=("home", (-0.2, 0.2, 1.84), -90, 3, 3.3, 28, 0.92, 3)),
    dict(say="눈을 뜨니 통장도 지갑도 텅 비었어요", shot=("home", (-0.25, 0.1, 1.55), -90, 3, 2.8, 30, 0.92, 2)),
    dict(say="편의점 앞엔 빈 지갑 줄이 길게 섰죠", shot=("mart", (0.0, -0.2, 1.5), -90, 5, 5.4, 22, 0.94, 0)),
    dict(say="라면 하나는 계란 두 개로 샀어요", shot=("mart", (0.0, 1.0, 1.35), -90, 4, 4.8, 30, 0.96, 0)),
    dict(say="미용실은 머리를 깎아 주고 빵을 받았죠", shot=("salon", (-0.12, 1.3, 1.42), -90, 4, 4.3, 26, 0.94, 2)),
    dict(say="월급날, 회사는 쌀 한 포대를 줬어요", shot=("office", (0.0, 0.9, 1.4), -90, 4, 4.8, 30, 0.96, 0)),
    dict(say="그런데 서로 원하는 게 달랐어요", shot=("mart", (0.0, 0.5, 1.4), -90, 6, 5.4, 22, 0.94, 3)),
    dict(say="“저는 빵 필요 없는데요”", gap=0.7, shot=("mart", (0.0, 1.0, 1.4), -90, 4, 4.8, 30, 0.96, 0)),
    dict(say="그러다 모두가 받아 주는 물건이 생겼어요", shot=("mart", (0.0, 0.7, 1.6), -90, 5, 4.8, 24, 0.94, 0)),
    dict(say="바로 라면! 라면이 돈이 된 거예요", shot=("mart", (0.0, 1.0, 1.35), -90, 4, 4.8, 30, 0.96, 0)),
    dict(say="사람들은 라면 지갑을 들고 다니고", shot=("home", (-0.2, 0.2, 1.84), -90, 3, 3.3, 28, 0.9, -3)),
    dict(say="집집마다 라면 저금통이 쌓여 갔죠", gap=0.7, shot=("home", (1.55, 0.8, 1.25), -90, 4, 3.8, 26, 0.92, 0)),
    dict(say="그런데 사실, 미국의 한 교도소에서는", shot=("cell", (0.0, 0.5, 1.3), -90, 4, 5.0, 24, 0.97, 0)),
    dict(say="라면이 돈처럼 쓰였대요", shot=("cell", (0.0, 0.3, 1.3), -90, 4, 4.8, 24, 0.97, 0)),
    dict(say="2016년 학회에서 발표된 연구예요", gap=0.7, shot=("stage", (0.6, 0.5, 1.5), -90, 3, 4.4, 28, 0.94, 0)),
    dict(say="돈이 사라져도 사람들은", shot=("salon", (0.0, 0.8, 1.35), -90, 4, 4.8, 30, 0.96, 0)),
    dict(say="다시 돈을 만들어 냈어요", shot=("office", (0.0, 0.9, 1.4), -90, 4, 4.8, 30, 0.96, 0)),
    dict(say="돈은 결국 ‘믿음’이었던 거죠", gap=0.9, shot=("home_pm", (0.0, 0.0, 1.35), -90, 4, 5.0, 26, 0.96, 0)),
    dict(say="당신 지갑 속 돈은 진짜 무엇일까요?", shot=("home_pm", (-0.2, 0.2, 1.6), -90, 3, 3.3, 28, 1.2, 0)),
]
TITLE = [("만약에", "white"), ("세상에서", "white"), ("돈이 사라진다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = 12          # '그런데 사실' 줄
NIGHT_FROM = 17     # 밤 집(믿음 릴레이)부터 밤
NG = 140            # 소품(goods) 인스턴스 최대 수

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep25_nomoney" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": round(0.3 + 2.6 * len(LINES) + 1.6, 2), "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep25", "title": "만약에 세상에서 돈이 사라진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "E", "mode": "major", "bpm": 100, "seed": 251, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

MINSU_SH, MINSU_PA = (0.20, 0.72, 0.62), (0.15, 0.18, 0.30)      # 주인공 민수: 민트 후드
HANA_SH, HANA_PA = (0.96, 0.45, 0.60), (0.30, 0.30, 0.45)        # 미용사 하나: 분홍, 긴 머리
CLERK_SH, CLERK_PA = (0.98, 0.70, 0.10), (0.20, 0.20, 0.22)      # 편의점 점원: 노란 조끼
INMATE = (0.96, 0.52, 0.10)                                       # 수감복
EXTRA = [(0.25, 0.45, 0.80), (0.85, 0.30, 0.28), (0.92, 0.92, 0.90), (0.55, 0.38, 0.70), (0.30, 0.30, 0.34),
         (0.45, 0.75, 0.85)]


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


# ───────────────────────── 자세·손 위치 ─────────────────────────
# 어깨 회전각 (오른팔, 왼팔): 음수 = 앞으로 듦. 표준 자세는 engine/voxel.py와 같은 값.
ARMS = {"stand": (0.0, 0.0), "sit": (-0.6, -0.6), "sit_phone": (-1.05, -0.6), "sit_conf": (-2.75, -0.6),
        "phone": (-1.05, 0.0), "angry": (-2.5, -2.5), "confused": (-2.75, 0.05), "talk": (-0.9, 0.05),
        "walk_a": (0.35, -0.35), "walk_b": (-0.35, 0.35), "lie": (0.0, 0.0)}
# 새 자세 = (바탕 자세, 팔 각도) — 바탕 자세의 몸·얼굴에 팔만 갈아 끼운 캐릭터 원형을 이 편에서 만든다
CUSTOM = {
    "show": ("talk", (-2.0, 0.05)),       # 오른손을 얼굴 높이로 들어 보임 (지갑·지폐)
    "showL": ("talk", (0.05, -2.0)),      # 왼손
    "hold2": ("stand", (-1.3, -1.3)),     # 두 팔로 가슴 앞에 안음 (쌀 포대·빵)
    "hold2t": ("talk", (-1.3, -1.3)),
    "giveR": ("stand", (-1.45, 0.05)),    # 오른손을 가슴 높이로 내밀어 건넴
    "giveRt": ("talk", (-1.45, 0.05)),
    "giveL": ("stand", (0.05, -1.45)),
    "giveLt": ("talk", (0.05, -1.45)),
    "snipL": ("talk", (0.05, -1.88)),     # 왼손을 머리 높이로 (가위질)
    "cheer": ("talk", (-2.9, -2.9)),      # 두 팔 번쩍
}
for _k, (_b, _a) in CUSTOM.items():
    ARMS[_k] = _a
SITS = ("sit", "sit_phone", "sit_conf")


def pose_index(name, hair):
    """인스턴스 'pose' 번호: 표준 22개(머리종류*11+자세) 뒤에 새 자세들(머리종류*새자세수+번호)."""
    from engine import voxel as X
    if name in CUSTOM:
        return 2 * X.NPOSE + hair * len(CUSTOM) + list(CUSTOM).index(name)
    return hair * X.NPOSE + X.POSES[name]


def _hip(pose):
    return 0.47 if pose in SITS else 0.78


def _loc(d, fwd, lat, up=0.0):
    """캐릭터 기준 (앞, 왼쪽, 위) → 세트 좌표. 크기 반영."""
    a = math.radians(d["yaw"])
    s = d["scale"]
    return (d["x"] + s * (fwd * math.cos(a) - lat * math.sin(a)), d["y"] + s * (fwd * math.sin(a) + lat * math.cos(a)),
            d["z"] + s * up)


def hand_pt(d, side, reach=0.0):
    """side 'R'(캐릭터 오른손)·'L' 손 끝 근처 점. reach = 팔 방향으로 더 나간 거리."""
    ang = ARMS[d["pose"]][0 if side == "R" else 1]
    dd = 0.49 + reach
    return _loc(d, -dd * math.sin(ang), -0.34 if side == "R" else 0.34, _hip(d["pose"]) + 0.54 - dd * math.cos(ang))


def face_pt(d, fwd=0.0, up=0.23):
    """머리 가운데(up=0.23) 근처 점. 앉은 자세는 머리가 낮음."""
    hz = 1.05 if d["pose"] in SITS else 1.36
    return _loc(d, fwd, 0.0, hz + up)


def carry_pt(d, fwd=0.52, up=0.36):
    """두 팔로 안은 물건의 가운데."""
    return _loc(d, fwd, 0.0, _hip(d["pose"]) + up)


def wallet_pt(d, side="R"):
    """한 손을 얼굴 높이로 든 자세에서 지갑 가운데 (손보다 앞·바깥쪽)."""
    ang = ARMS[d["pose"]][0 if side == "R" else 1]
    return _loc(d, -0.49 * math.sin(ang) + 0.12, -0.46 if side == "R" else 0.46,
                _hip(d["pose"]) + 0.54 - 0.49 * math.cos(ang) + 0.03)


# ───────────────────────── 5×7 점 글자 ─────────────────────────
FONT = {
    "0": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
}


def glyph_cells(ch):
    """[(열, 아래에서 몇째 줄)] — 글자 한 칸 한 칸."""
    return [(c, 6 - r) for r, row in enumerate(FONT[ch]) for c, bit in enumerate(row) if bit == "1"]


def _pix(v, rows, pal, x0, z0, y, cell, depth=0.04):
    """문자 그림(rows)을 y 벽 앞(-y 쪽)에 발광 점으로 찍음. 맨 윗줄이 가장 위."""
    n = len(rows)
    for r, row in enumerate(rows):
        z = z0 + (n - 1 - r) * cell
        for c, ch in enumerate(row):
            if ch in pal:
                v.box(x0 + c * cell, x0 + (c + 1) * cell, y - depth, y, z, z + cell, pal[ch], jit=0, glow=True)


def _text_pix(v, text, xc, z0, y, cell, col, gap=1.4):
    """5×7 숫자 글을 가운데 xc에 발광 점으로 찍음."""
    w = 5 * cell
    total = len(text) * w + (len(text) - 1) * gap * cell
    x = xc - total / 2
    for ch in text:
        for c, r in glyph_cells(ch):
            v.box(x + c * cell, x + (c + 1) * cell, y - 0.04, y, z0 + r * cell, z0 + (r + 1) * cell, col, jit=0, glow=True)
        x += w + gap * cell


# ───────────────────────── 세트 ─────────────────────────
def _shelf_wall(v, x0, x1, y0, y1, h, rows=5):
    """벽에 붙은 진열대: 칸마다 알록달록한 상품 상자 (앞 = -y)."""
    cols = [(0.9, 0.25, 0.2), (0.95, 0.75, 0.2), (0.25, 0.55, 0.9), (0.3, 0.75, 0.35), (0.95, 0.55, 0.75),
            (0.95, 0.95, 0.92), (0.6, 0.35, 0.2)]
    v.box(x0, x1, y1 - 0.05, y1, 0, h, (0.62, 0.64, 0.68))
    v.box(x0 - 0.03, x0, y0, y1, 0, h, (0.55, 0.57, 0.6))
    v.box(x1, x1 + 0.03, y0, y1, 0, h, (0.55, 0.57, 0.6))
    step = (h - 0.12) / rows
    for r in range(rows):
        z = 0.12 + r * step
        v.box(x0, x1, y0, y1 - 0.05, z, z + 0.03, (0.8, 0.8, 0.82))
        x = x0 + 0.05
        while x < x1 - 0.2:
            w = float(v.rs.uniform(0.14, 0.24))
            hh = float(v.rs.uniform(0.14, step - 0.07))
            c = cols[int(v.rs.integers(len(cols)))]
            v.box(x, x + w, y0 + 0.1, y1 - 0.1, z + 0.03, z + 0.03 + hh, c, jit=0.08)
            x += w + 0.02


def _bed(v, x0, x1, y0, y1, blanket):
    """머리판이 +y 벽쪽인 침대. 상자마다 면이 어긋나게(같은 평면에 겹치면 그림자로 까맣게 나옴)."""
    v.box(x0, x1, y0, y1, 0, 0.32, (0.62, 0.42, 0.25))
    v.box(x0 + 0.03, x1 - 0.03, y0 + 0.03, y1 - 0.03, 0.32, 0.52, (0.92, 0.92, 0.90), jit=0.02)
    v.box(x0 + 0.05, x1 - 0.05, y0 + 0.05, y0 + 0.62 * (y1 - y0), 0.52, 0.6, blanket)
    v.box(x0 + 0.15, x1 - 0.15, y1 - 0.42, y1 - 0.08, 0.52, 0.64, (0.97, 0.97, 0.97), jit=0.01)
    v.box(x0 - 0.02, x1 + 0.02, y1 - 0.06, y1 + 0.02, 0, 1.0, (0.38, 0.25, 0.15))


def _home(v, night):
    from engine import voxel as X
    tag = "ep25_pm_" if night else "ep25_am_"
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    v.wall((-3, 2.5), (3, 2.5), 0, 2.7, (0.93, 0.90, 0.82), 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=1)
    v.floor(-0.9, 1.0, -1.6, 0.4, (0.80, 0.52, 0.48), 0.5, "check", z=0.012)                  # 러그
    _bed(v, -2.85, -1.45, 0.4, 2.45, (0.45, 0.62, 0.90))
    v.box(-1.35, -0.95, 1.95, 2.4, 0, 0.5, (0.62, 0.42, 0.25))                                  # 협탁 + 스탠드
    v.box(-1.2, -1.1, 2.1, 2.2, 0.5, 0.62, (0.3, 0.3, 0.32), jit=0)
    v.box(-1.27, -1.03, 2.03, 2.27, 0.62, 0.85, (1.0, 0.88, 0.62), jit=0, glow=night)
    v.window(0.0, 1.8, 2.49, 0.9, 2.2, night=night, lights=12)
    v.box(-0.45, -0.03, 2.4, 2.47, 0.6, 2.45, (0.85, 0.55, 0.45))                                   # 커튼
    v.box(1.83, 2.2, 2.4, 2.47, 0.6, 2.45, (0.85, 0.55, 0.45))
    for x0, c in ((-2.4, (0.95, 0.75, 0.3)), (-1.7, (0.4, 0.65, 0.9))):                         # 벽 액자
        v.box(x0, x0 + 0.5, 2.46, 2.49, 1.5, 2.1, (0.95, 0.95, 0.92))
        v.box(x0 + 0.06, x0 + 0.44, 2.45, 2.46, 1.56, 2.04, c, jit=0)
    # 책상 + 라면 저금통(틀만 있는 투명 항아리)
    X.table(v, 1.9, 1.2, 1.7, 0.9, 0.74, (0.82, 0.66, 0.45))
    for dx in (-1, 1):
        for dy in (-1, 1):
            v.box(1.9 + dx * 0.25 - 0.015, 1.9 + dx * 0.25 + 0.015, 1.2 + dy * 0.2 - 0.015, 1.2 + dy * 0.2 + 0.015, 0.77, 1.72,
                  (0.72, 0.88, 1.0), jit=0)
    v.box(1.62, 2.18, 0.98, 1.42, 0.74, 0.77, (0.35, 0.4, 0.5))
    v.box(1.62, 2.18, 0.98, 1.42, 1.72, 1.77, (0.85, 0.2, 0.2))
    v.box(1.78, 2.02, 1.15, 1.25, 1.77, 1.785, (0.1, 0.1, 0.1), jit=0)
    v.box(2.45, 2.95, -1.8, -0.8, 0, 2.1, (0.78, 0.84, 0.9))                                     # 옷장
    v.box(2.3, 2.6, -2.35, -2.05, 0, 0.45, (0.35, 0.6, 0.45))                                    # 화분
    v.box(2.25, 2.65, -2.4, -2.0, 0.45, 1.05, (0.25, 0.55, 0.25), jit=0.1)
    if night:
        v.box(1.16, 1.24, 0.56, 0.64, 1.9, 2.7, (0.2, 0.2, 0.2), jit=0)                         # 펜던트 등
        v.box(0.95, 1.45, 0.35, 0.85, 1.82, 1.9, (1.0, 0.85, 0.6), jit=0, glow=True)
        v.light(1.2, 0.6, 1.7, 150, (1.0, 0.78, 0.5), 0.3, tag + "pend")
        v.light(0.9, 2.0, 1.8, 18, (0.55, 0.65, 1.0), 0.6, tag + "moon")
        v.light(-1.15, 2.15, 1.0, 20, (1.0, 0.8, 0.55), 0.3, tag + "lamp")
        v.light(0.0, -0.5, 1.8, 60, (1.0, 0.85, 0.65), 0.6, tag + "fill")
    else:
        v.light(1.2, 0.6, 2.2, 70, (1.0, 0.9, 0.75), 0.3, tag + "pend")
        v.light(0.9, 2.0, 1.6, 120, (0.85, 0.92, 1.0), 0.8, tag + "win")


def _mart(v):
    v.floor(-3.5, 3.5, -3, 3, (0.90, 0.90, 0.88), 0.5, "check")
    v.wall((-3.5, 3), (3.5, 3), 0, 3.0, (0.96, 0.93, 0.85), 0.5, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, 3.0, (0.84, 0.90, 0.88), 0.5, face=-1)
    v.wall((3.5, -3), (3.5, 3), 0, 3.0, (0.84, 0.90, 0.88), 0.5, face=1)
    for x0, x1 in ((-3.3, -1.2), (1.2, 3.3)):                                                     # 뒷벽 진열대 둘
        _shelf_wall(v, x0, x1, 2.5, 2.98, 2.3, rows=5)
    v.box(-0.9, 0.9, 2.95, 2.97, 2.2, 2.55, (0.25, 0.8, 0.5), jit=0, glow=True)                 # 가운데 초록 간판
    v.box(-0.9, 0.9, 2.94, 2.96, 2.57, 2.62, (0.95, 0.95, 0.92), jit=0, glow=True)
    v.box(-0.2, 0.2, 2.94, 2.97, 1.55, 1.95, (0.95, 0.95, 0.92))                                # 벽시계
    v.box(-0.015, 0.015, 2.92, 2.94, 1.72, 1.9, (0.1, 0.1, 0.1), jit=0)
    v.box(-0.015, 0.1, 2.90, 2.92, 1.74, 1.76, (0.1, 0.1, 0.1), jit=0)
    # 계산대: 벽에서 앞으로 길게 (y 0.65~2.35, 폭 0.7), 위에 계산기·바구니
    v.box(-0.30, 0.30, 0.7, 2.3, 0, 1.0, (0.55, 0.40, 0.28))
    v.box(-0.35, 0.35, 0.65, 2.35, 1.0, 1.05, (0.93, 0.92, 0.88))
    v.box(-0.14, 0.14, 1.75, 2.0, 1.05, 1.12, (0.2, 0.2, 0.22))
    v.box(-0.12, 0.12, 1.73, 1.75, 1.1, 1.3, (0.4, 0.9, 0.6), jit=0, glow=True)
    v.box(-0.30, -0.05, 2.05, 2.3, 1.05, 1.2, (0.95, 0.8, 0.3))
    # 왼쪽 벽 음료 냉장고, 오른쪽 벽 냉동고
    v.box(-3.49, -3.45, -1.8, 2.2, 0.15, 2.3, (0.72, 0.88, 1.0), jit=0, glow=True)
    for z in (0.35, 0.85, 1.35, 1.85):
        y = -1.7
        while y < 2.1:
            c = [(0.9, 0.3, 0.25), (0.3, 0.7, 0.95), (0.95, 0.8, 0.25), (0.35, 0.8, 0.45)][int(v.rs.integers(4))]
            v.box(-3.44, -3.2, y, y + 0.12, z, z + 0.3, c, jit=0.06)
            y += 0.17
    v.box(3.0, 3.45, -1.5, 0.5, 0, 0.95, (0.92, 0.94, 0.97))
    v.box(3.02, 3.43, -1.45, 0.45, 0.95, 0.97, (0.7, 0.9, 1.0), jit=0, glow=True)
    for x in (-2.0, 0.0, 2.0):
        v.box(x - 0.6, x + 0.6, -0.2, 0.5, 2.95, 3.0, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.4, 2.6, 110, (1.0, 0.97, 0.92), 0.6, f"ep25_mart_l{int(x)}")


def _chair_barber(v, cx, cy):
    """앞(-y)을 보는 이발 의자 (앉는 면 높이 0.55)."""
    v.box(cx - 0.25, cx + 0.25, cy - 0.25, cy + 0.25, 0, 0.07, (0.25, 0.25, 0.28))
    v.box(cx - 0.06, cx + 0.06, cy - 0.06, cy + 0.06, 0.07, 0.45, (0.7, 0.72, 0.75))
    v.box(cx - 0.30, cx + 0.30, cy - 0.30, cy + 0.30, 0.45, 0.55, (0.75, 0.15, 0.2))
    v.box(cx - 0.28, cx + 0.28, cy + 0.32, cy + 0.42, 0.55, 1.2, (0.75, 0.15, 0.2))
    for sx in (-0.38, 0.32):
        v.box(cx + sx, cx + sx + 0.06, cy - 0.2, cy + 0.3, 0.55, 0.72, (0.25, 0.25, 0.28))
    v.box(cx - 0.2, cx + 0.2, cy - 0.55, cy - 0.3, 0.12, 0.19, (0.25, 0.25, 0.28))


def _salon(v):
    from engine import voxel as X
    v.floor(-3, 3, -2.5, 2.5, (0.93, 0.88, 0.86), 0.5, "check")
    v.wall((-3, 2.5), (3, 2.5), 0, 3.0, (0.97, 0.86, 0.88), 0.5, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 3.0, (0.92, 0.80, 0.84), 0.5, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 3.0, (0.92, 0.80, 0.84), 0.5, face=1)
    for x0, x1 in ((-2.8, -1.3), (1.3, 2.8)):                                                     # 뒷벽 미용 용품 선반
        _shelf_wall(v, x0, x1, 2.1, 2.48, 2.1, rows=4)
    v.box(-0.6, 0.6, 2.46, 2.49, 2.15, 2.45, (1.0, 0.55, 0.7), jit=0, glow=True)               # 분홍 간판 띠
    for x0 in (-2.995, 2.955):                                                                    # 옆벽 거울 (발광 하늘색 판)
        v.box(x0, x0 + 0.04, -0.5, 1.6, 0.9, 2.2, (0.72, 0.88, 1.0), jit=0, glow=True)
    _chair_barber(v, 0.0, 1.1)                                                                    # 손님 의자
    _chair_barber(v, 2.2, 1.3)                                                                    # 다른 자리
    X.table(v, 0.8, 1.9, 0.6, 0.6, 0.7, (0.92, 0.9, 0.86))                                       # 뒤쪽 탁자 + 빵 바구니
    v.box(0.62, 0.98, 1.72, 2.08, 0.7, 0.82, (0.72, 0.5, 0.3))
    v.box(-2.6, -1.4, 0.0, 0.7, 0, 0.8, (0.95, 0.95, 0.95))                                      # 접수대
    for x in (-1.5, 0.0, 1.5):
        v.box(x - 0.6, x + 0.6, -0.2, 0.5, 2.95, 3.0, (1.0, 0.97, 0.97), jit=0, glow=True)
        v.light(x, 0.9, 2.6, 110, (1.0, 0.95, 0.93), 0.6, f"ep25_salon_l{int(x)}")


def _office(v):
    from engine import voxel as X
    v.floor(-3.5, 3.5, -3, 3, (0.58, 0.60, 0.63), 0.5, "check")
    v.wall((-3.5, 3), (3.5, 3), 0, 3.0, (0.86, 0.87, 0.89), 0.5, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, 3.0, (0.82, 0.84, 0.86), 0.5, face=-1)
    v.wall((3.5, -3), (3.5, 3), 0, 3.0, (0.82, 0.84, 0.86), 0.5, face=1)
    for x0 in (-3.2, 1.4):
        v.window(x0, x0 + 1.8, 2.99, 0.9, 2.5, night=False)
    # 달력: 빨간 동그라미 친 날 = 월급날
    v.box(-0.7, 0.7, 2.95, 2.98, 1.95, 2.9, (0.97, 0.97, 0.95))
    for r in range(5):
        for c in range(7):
            red = (r, c) == (3, 4)
            v.box(-0.62 + c * 0.18, -0.62 + c * 0.18 + 0.14, 2.93, 2.95, 2.0 + r * 0.17, 2.0 + r * 0.17 + 0.13,
                  (0.9, 0.2, 0.18) if red else (0.78, 0.8, 0.84), jit=0)
    # 쌀 포대 더미 (사장님 뒤쪽)
    for k, (x, z) in enumerate(((-1.7, 0.0), (-1.3, 0.0), (-0.9, 0.0), (-1.5, 0.46), (-1.1, 0.46), (-1.3, 0.92))):
        v.box(x - 0.17, x + 0.17, 2.3, 2.58, z, z + 0.46, (0.93, 0.89, 0.78))
        v.box(x - 0.1, x + 0.1, 2.29, 2.3, z + 0.12, z + 0.34, (0.8, 0.18, 0.14), jit=0)
    X.table(v, 2.3, 2.0, 1.5, 0.7, 0.74, (0.92, 0.92, 0.9))
    X.monitor(v, 2.3, 2.25, 0.74, -90)
    X.chair(v, 2.3, 1.45, -90, (0.2, 0.22, 0.26))
    v.box(-3.3, -2.8, -2.5, -2.0, 0, 0.5, (0.35, 0.6, 0.45))
    v.box(-3.35, -2.75, -2.55, -1.95, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.0, 0.5, 2.7):
        v.box(x - 0.6, x + 0.6, -0.1, 0.5, 2.95, 3.0, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.2, 2.6, 110, (0.95, 0.97, 1.0), 0.6, f"ep25_office_l{int(x)}")


def _cell(v):
    from engine import voxel as X
    v.floor(-3, 3, -2.5, 2.4, (0.50, 0.52, 0.55), 0.5, "check")
    v.wall((-3, -2.5), (-3, 2.4), 0, 3.0, (0.52, 0.54, 0.58), 0.5, face=-1)
    v.wall((3, -2.5), (3, 2.4), 0, 3.0, (0.52, 0.54, 0.58), 0.5, face=1)
    # 뒤쪽 = 쇠창살 문 + 그 뒤 밝은 복도
    x = -2.9
    while x < 3.0:
        v.box(x - 0.025, x + 0.025, 2.28, 2.33, 0, 2.9, (0.22, 0.23, 0.27), jit=0)
        x += 0.2
    for z in (0.0, 1.0, 2.0, 2.85):
        v.box(-2.99, 2.99, 2.26, 2.35, z, z + 0.06, (0.2, 0.21, 0.25), jit=0)
    v.floor(-3, 3, 2.4, 5.0, (0.72, 0.72, 0.68), 0.5, "check")
    v.wall((-3, 5.0), (3, 5.0), 0, 3.0, (0.82, 0.84, 0.8), 0.5, face=-1)
    v.box(-2.5, 2.5, 3.2, 3.8, 2.9, 2.95, (1.0, 0.96, 0.82), jit=0, glow=True)
    v.light(0.0, 3.4, 2.6, 190, (1.0, 0.95, 0.85), 0.6, "ep25_cell_hall")
    # 이층 침대 (왼쪽 벽)
    for dx in (-2.9, -2.1):
        for dy in (0.4, 2.1):
            v.box(dx, dx + 0.06, dy, dy + 0.06, 0, 1.75, (0.35, 0.37, 0.42), jit=0)
    v.box(-2.88, -2.06, 0.42, 2.14, 0.42, 0.5, (0.55, 0.6, 0.7))
    v.box(-2.88, -2.06, 0.42, 2.14, 1.3, 1.38, (0.55, 0.6, 0.7))
    v.box(-2.84, -2.1, 0.5, 1.2, 0.5, 0.58, (0.85, 0.85, 0.82))
    # 작은 쇠 탁자 (라면 더미 올릴 자리)
    X.table(v, 1.9, 1.0, 0.8, 0.5, 0.78, (0.62, 0.64, 0.68))
    v.box(-3.0, 3.0, 2.5, 5.0, 3.0, 3.15, (0.30, 0.31, 0.35))                                    # 지붕 (해 가리기)
    v.box(-3.2, 3.2, -2.7, 2.5, 3.0, 3.15, (0.30, 0.31, 0.35))
    v.light(0.0, 0.6, 2.7, 130, (0.85, 0.92, 1.0), 0.5, "ep25_cell_lamp")
    v.box(-0.4, 0.4, 0.2, 1.0, 2.9, 2.95, (0.85, 0.92, 1.0), jit=0, glow=True)


def _stage(v):
    v.floor(-4, 4, -2.5, 2.5, (0.45, 0.32, 0.24), 0.5, "wood")
    v.wall((-4, 2.5), (4, 2.5), 0, 3.6, (0.08, 0.10, 0.18), 0.5, face=-1)
    v.wall((-4, -2.5), (-4, 2.5), 0, 3.6, (0.10, 0.12, 0.20), 0.5, face=-1)
    v.wall((4, -2.5), (4, 2.5), 0, 3.6, (0.10, 0.12, 0.20), 0.5, face=1)
    v.box(-2.6, 2.6, 2.44, 2.49, 0.55, 3.35, (0.05, 0.05, 0.07))                                 # 큰 화면 틀 + 남색 발광판
    v.box(-2.5, 2.5, 2.40, 2.44, 0.65, 3.25, (0.10, 0.20, 0.45), jit=0, glow=True)
    pal = {"W": (0.95, 0.95, 0.95), "Y": (1.0, 0.82, 0.25), "E": (1.0, 1.0, 0.92), "R": (0.9, 0.2, 0.15)}
    _pix(v, ["....W..W....", "...W..W..W..", "..YYYYYYYY..", ".YYYEEYYYYY.", ".YYYEEYYYYY.", "RRRRRRRRRRRR",
             ".RRRRRRRRRR.", "..RRRRRRRR..", "...RRRRRR..."], pal, -0.9, 0.95, 2.40, 0.12)       # 라면 그릇 그림
    _text_pix(v, "2016", 0.9, 2.45, 2.40, 0.075, (1.0, 0.9, 0.3))
    v.box(0.6, 1.2, 0.35, 0.7, 0, 1.05, (0.38, 0.27, 0.18))                                       # 연단
    v.box(0.55, 1.25, 0.3, 0.75, 1.05, 1.1, (0.3, 0.21, 0.14))
    v.box(0.82, 0.98, 0.33, 0.35, 0.5, 0.9, (0.45, 0.65, 1.0), jit=0, glow=True)
    v.box(0.895, 0.905, 0.5, 0.52, 1.1, 1.38, (0.1, 0.1, 0.1), jit=0)                            # 마이크
    v.box(-4.1, 4.1, -2.6, 2.6, 3.6, 3.75, (0.1, 0.11, 0.16))                                     # 지붕
    for x, c in ((-1.5, (1.0, 0.9, 0.8)), (0.9, (1.0, 0.95, 0.9)), (2.6, (0.9, 0.9, 1.0))):
        v.light(x, -0.3, 3.2, 150, c, 0.6, f"ep25_stage_l{int(x * 10)}")
    v.light(0.9, -0.8, 1.8, 90, (1.0, 0.95, 0.9), 0.6, "ep25_stage_face")
    v.box(-3.6, 3.6, -1.0, -0.8, 0, 0.45, (0.55, 0.12, 0.15))                                     # 무대 앞 붉은 턱


# ───────────────────────── 캐릭터 배치 ─────────────────────────
def cast():
    """[dict(name, set, x, y, yaw, pose, hair, shirt, pants, scale, z, over={줄: 덮어쓰기}, only=보이는 줄 집합)]
    처음 값 = 보이는 첫 줄의 자리, over = 줄마다 자리·자세."""
    C = []

    def add(name, hair, shirt, pants, at, scale=1.0):
        lines = sorted(at)
        first = at[lines[0]]
        over = {}
        for i in lines:
            a = at[i]
            over[i] = dict(set=a[0], x=a[1], y=a[2], yaw=a[3], pose=a[4], z=a[5] if len(a) > 5 else 0.0)
        C.append(dict(name=name, set=first[0], x=first[1], y=first[2], yaw=first[3], pose=first[4], hair=hair, shirt=shirt,
                      pants=pants, scale=scale, z=over[lines[0]]["z"], over=over, only=set(lines)))

    add("minsu", 0, MINSU_SH, MINSU_PA, {
        0: ("home", 0.0, 0.2, -90, "show"), 1: ("home", 0.0, 0.2, -90, "show"),
        2: ("mart", 0.0, -0.2, -90, "show"), 3: ("mart", -0.62, 1.1, -75, "giveL"),
        5: ("office", 0.62, 0.9, -105, "hold2"), 6: ("mart", 0.55, 0.1, -105, "hold2"),
        8: ("mart", 0.0, 0.6, -90, "cheer"), 9: ("mart", -0.62, 1.1, -75, "giveL"),
        10: ("home", 0.0, 0.2, -90, "show"), 11: ("home", 1.2, 0.5, -90, "giveL"),
        16: ("office", 0.62, 0.9, -105, "hold2"), 17: ("home_pm", -0.8, 0.0, -80, "giveL"),
        18: ("home_pm", 0.0, 0.2, -90, "show")})
    add("hana", 1, HANA_SH, HANA_PA, {
        4: ("salon", -0.62, 1.62, -90, "snipL"), 6: ("mart", -0.55, 0.1, -75, "hold2"),
        7: ("mart", -0.62, 1.1, -75, "hold2"), 8: ("mart", -0.75, 1.0, -80, "cheer"),
        15: ("salon", 0.62, 0.8, -105, "giveRt"), 17: ("home_pm", 0.0, 0.0, -90, "hold2")})
    add("clerk", 0, CLERK_SH, CLERK_PA, {
        3: ("mart", 0.62, 1.1, -105, "giveRt"), 6: ("mart", 0.0, 2.6, -90, "talk"),
        7: ("mart", 0.62, 1.1, -105, "talk"), 8: ("mart", 0.75, 1.0, -100, "cheer"),
        9: ("mart", 0.62, 1.1, -105, "giveRt"), 17: ("home_pm", 0.8, 0.0, -100, "giveR")})
    add("guest", 0, (0.45, 0.55, 0.85), (0.2, 0.2, 0.22), {
        4: ("salon", 0.0, 1.1, -90, "sit", 0.19), 15: ("salon", -0.62, 0.8, -75, "giveL")})
    add("boss", 0, (0.30, 0.30, 0.34), (0.15, 0.15, 0.18), {
        5: ("office", -0.62, 0.9, -75, "hold2t"), 16: ("office", -0.62, 0.9, -75, "hold2t")}, scale=1.04)
    add("prof", 1, (0.25, 0.28, 0.42), (0.15, 0.15, 0.2), {14: ("stage", 0.9, 0.8, -90, "talk")})
    add("inmate_a", 0, INMATE, INMATE, {12: ("cell", -0.8, 0.3, -80, "stand"), 13: ("cell", -0.8, 0.3, -80, "giveL")})
    add("inmate_b", 0, INMATE, INMATE, {12: ("cell", 0.0, 0.3, -90, "talk"), 13: ("cell", 0.0, 0.3, -90, "hold2t")})
    add("inmate_c", 1, INMATE, INMATE, {12: ("cell", 0.8, 0.3, -100, "stand"), 13: ("cell", 0.8, 0.3, -100, "giveR")})
    add("q1", 1, EXTRA[0], MINSU_PA, {2: ("mart", -0.9, -0.2, -90, "show"), 6: ("mart", -1.3, 0.7, -80, "hold2")})
    add("q3", 0, EXTRA[1], (0.20, 0.20, 0.22), {2: ("mart", 0.9, -0.2, -90, "showL"), 6: ("mart", 1.3, 0.7, -100, "hold2")})
    add("q4", 0, EXTRA[3], (0.35, 0.28, 0.20), {2: ("mart", -1.75, 0.5, -80, "confused")})
    add("q5", 1, EXTRA[4], (0.12, 0.12, 0.13), {2: ("mart", 1.75, 0.5, -100, "confused")})
    return C


CAST = {c["name"]: c for c in cast()}


def place(name, i):
    """이름·줄 번호 → 그 줄의 자리·자세 (세트 좌표)."""
    c = CAST[name]
    d = dict(c)
    d.update(c["over"][i])
    return d


# ───────────────────────── 소품 (goods) 움직임 ─────────────────────────
(RAMEN_F, RAMEN_F2, RAMEN_U, RAMEN_U2, EGG, EGGBOX, BREAD, BAGUETTE, RICE, WALLET, BILL, PHONE, SCI_A, SCI_B, CLIP,
 RBOX, SPARK, QMARK) = range(18)
rad = math.radians


def lerp3(a, b, s):
    return tuple(a[k] + (b[k] - a[k]) * s for k in range(3))


def arc(a, b, s, h):
    """a→b를 s(0~1)만큼, 가운데가 h만큼 솟는 포물선."""
    p = lerp3(a, b, s)
    return (p[0], p[1], p[2] + 4 * h * s * (1 - s))


def back(x):
    """0→1, 살짝 넘쳤다가 자리잡는 곡선."""
    x = min(max(x, 0.0), 1.0)
    return 1 + 2.70158 * (x - 1) ** 3 + 1.70158 * (x - 1) ** 2


def pop(u, a, b):
    """u가 a~b 사이에 0→1로 '퐁' 나타남."""
    return back((u - a) / (b - a))


def chain(pts, s, h=0.1):
    """점들을 차례로 이어서 지남(s 0~1), 구간마다 포물선."""
    n = len(pts) - 1
    k = min(int(s * n), n - 1)
    return arc(pts[k], pts[k + 1], s * n - k, h)


def bills(src, n, t, yaw, life=2.0, rise=0.45, spread=0.13, ph=0.0):
    """지갑 위로 떠올라 팔랑이며 작아져 사라지는 지폐 n장 (각자 시간차)."""
    out = []
    a = rad(yaw)
    for k in range(n):
        p = (k / n + t / life + ph) % 1.0
        w = spread * math.sin(2 * math.pi * (p * 1.3 + k * 0.31))
        x = src[0] + math.cos(a) * 0.04 - math.sin(a) * w
        y = src[1] + math.sin(a) * 0.04 + math.cos(a) * w
        z = src[2] + 0.1 + rise * (1 - (1 - p) ** 2)
        s = ramp(p, 0.0, 0.1) * (1 - ramp(p, 0.45, 0.92))
        rot = (math.pi / 2 + 0.5 * math.sin(6.283 * (p * 1.7 + k * 0.23)), 0.4 * math.sin(6.283 * (p * 1.1 + k * 0.41)),
               a + math.pi / 2 + 0.6 * math.sin(6.283 * (p + k * 0.13)))
        out.append((BILL, (x, y, z), rot, s))
    return out


def sparks(c, t, u, a, b, n=10, r0=0.34, axis_yaw=-90.0):
    """c 둘러싼 반짝이 n개 (화면 쪽으로 펼쳐진 원), u가 a~b에서 나타나 계속 반짝."""
    out = []
    ay = rad(axis_yaw)
    for k in range(n):
        th = 2 * math.pi * k / n + t * 1.6
        r = r0 + 0.06 * math.sin(t * 5 + k)
        p = (c[0] - math.sin(ay) * r * math.cos(th), c[1] + math.cos(ay) * r * math.cos(th), c[2] + r * math.sin(th))
        out.append((SPARK, p, (0.0, 0.0, 0.0), pop(u, a, b) * (0.45 + 0.55 * abs(math.sin(t * 6 + k * 1.3)))))
    return out


def ramen_slot(base, k, jit=1):
    """쌓인 라면 k번째(0부터) 자리 — 한 장 두께 0.045, 조금씩 어긋나게."""
    return (base[0] + 0.007 * ((k * 5) % 3 - 1) * jit, base[1] + 0.007 * ((k * 7) % 3 - 1) * jit, base[2] + 0.0225 + 0.045 * k)


def props(i, u, t):
    """i번째 줄, 진행도 u(0~1), 시각 t의 소품 [(종류, (x,y,z) 세트 좌표, (rx,ry,rz) 라디안, 크기)]."""
    out = []
    A = out.append

    def facing(d):
        return (0.0, 0.0, rad(d["yaw"]))

    CAM = (0.0, 0.0, rad(-90))            # 카메라 쪽(-y)을 보게 세워 둔 물건

    if i == 0:                             # 훅: 빈 지갑에서 지폐가 떠올라 사라짐
        d = place("minsu", 0)
        w = wallet_pt(d)
        A((WALLET, w, facing(d), 1.0))
        out += bills(w, 12, t, d["yaw"])
    elif i == 1:                           # 폰 잔고 0이 퐁 하고 나타남
        d = place("minsu", 1)
        A((PHONE, wallet_pt(d), facing(d), 1.3 * pop(u, 0.0, 0.22)))
    elif i == 2:                           # 세 사람의 빈 지갑에서 지폐가 사라짐
        for k, (n, side) in enumerate((("q1", "R"), ("minsu", "R"), ("q3", "L"))):
            d = place(n, 2)
            w = wallet_pt(d, side)
            A((WALLET, w, facing(d), 1.0))
            out += bills(w, 5, t, d["yaw"], spread=0.09, ph=k * 0.37)
    elif i == 3:                           # 계란 두 개: 민수 손 → 점원 손, 라면: 계산대 → 민수 손
        m, c = place("minsu", 3), place("clerk", 3)
        hm, hc = hand_pt(m, "L", 0.07), hand_pt(c, "R", 0.07)
        for k, (a, b) in enumerate(((0.06, 0.34), (0.14, 0.42))):
            s = ramp(u, a, b)
            o = (0.0, 0.035 * (k - 0.5), 0.0)
            p0 = tuple(hm[j] + o[j] for j in range(3))
            p1 = tuple(hc[j] + o[j] for j in range(3))
            A((EGG, arc(p0, p1, s, 0.14), (0.0, 0.0, 0.4 * s), 1.0))
        A((RAMEN_U, arc((0.0, 1.35, 1.2), hm, ramp(u, 0.52, 0.86), 0.12), CAM, 1.0))
        A((EGGBOX, (0.0, 1.9, 1.05), CAM, 1.0))
    elif i == 4:                           # 가위질 + 떨어지는 머리카락, 빵 바구니에 빵이 퐁퐁
        h = place("hana", 4)
        hp = hand_pt(h, "L", 0.05)
        sc = (hp[0] + 0.07, hp[1] + 0.02, hp[2] + 0.02)
        A((SCI_A if int(t * 4.5) % 2 == 0 else SCI_B, sc, (0.0, 0.0, 0.0), 1.0))
        for k in range(6):
            p = (k / 6 + t / 1.1) % 1.0
            A((CLIP, (sc[0] + 0.05 * math.sin(k * 2.1) - 0.05 * p, sc[1] + 0.04 * math.cos(k * 1.7), 1.45 - 0.85 * p * p),
               (p * 5, k, p * 3), 1.0))
        base = (0.8, 1.9, 0.84)
        for k, (dx, dy, a) in enumerate(((-0.09, 0.0, None), (0.09, 0.04, None), (0.0, -0.08, 0.10), (-0.02, 0.1, 0.26))):
            s = 1.0 if a is None else pop(u, a, a + 0.14)
            A((BAGUETTE if k == 3 else BREAD, (base[0] + dx, base[1] + dy, base[2] + 0.05 * (k // 2)),
               (0.0, 0.0, rad(-90 + 25 * k)), s))
    elif i in (5, 16):                     # 쌀 포대(5) / 라면 상자(16)가 사장님 품에서 민수 품으로
        b, m = place("boss", i), place("minsu", i)
        s = ramp(u, 0.12, 0.5)
        p = arc(carry_pt(b), carry_pt(m), s, 0.1)
        bob = 0.03 * math.sin(2 * math.pi * 2.0 * u) * ramp(u, 0.5, 0.6) * (1 - ramp(u, 0.85, 1.0))
        if i == 5:
            A((RICE, (p[0], p[1], p[2] + bob), CAM, 1.0))
        else:
            A((RBOX, (p[0], p[1], p[2] + bob), CAM, 1.0))
    elif i == 6:                           # 다들 서로 다른 물건을 안고 있음
        def w(k):
            return 0.012 * math.sin(2 * math.pi * (t * 1.6 + k * 0.37))
        h, m, q1, q3 = (place(n, 6) for n in ("hana", "minsu", "q1", "q3"))
        c = carry_pt(h)
        A((BREAD, (c[0], c[1], c[2] - 0.08 + w(0)), (0.0, 0.0, rad(h["yaw"] + 90)), 1.0))
        A((BREAD, (c[0], c[1], c[2] + 0.04 + w(1)), (0.0, 0.0, rad(h["yaw"] + 80)), 1.0))
        A((BAGUETTE, (c[0], c[1], c[2] + 0.15 + w(2)), (0.0, 0.0, rad(h["yaw"] + 90)), 1.0))
        c = carry_pt(m)
        A((RICE, (c[0], c[1], c[2] + w(3)), CAM, 1.0))
        c = carry_pt(q1)
        A((EGGBOX, (c[0], c[1], c[2] - 0.06 + w(4)), (0.0, 0.0, rad(q1["yaw"])), 1.3))
        A((EGGBOX, (c[0], c[1], c[2] + 0.04 + w(5)), (0.0, 0.0, rad(q1["yaw"])), 1.3))
        c = carry_pt(q3)
        fx, fy = math.cos(rad(q3["yaw"])), math.sin(rad(q3["yaw"]))
        for k in range(3):        # 폭 방향으로 조금씩 어긋나게 (옆면이 같은 평면에 겹치지 않게)
            A((BAGUETTE, (c[0] + fx * 0.02 * (k - 1), c[1] + fy * 0.02 * (k - 1), c[2] - 0.06 + 0.06 * k + w(6 + k)),
               (0.0, 0.0, rad(q3["yaw"] + 90)), 1.0))
    elif i == 7:                           # 점원 앞에서 빵이 하나 툭 떨어짐
        h = place("hana", 7)
        c = carry_pt(h)
        s = ramp(u, 0.42, 0.62)
        A((BREAD, (c[0], c[1], c[2] - 0.08), (0.0, 0.0, rad(h["yaw"] + 90)), 1.0))
        A((BREAD, (c[0], c[1], c[2] + 0.04), (0.0, 0.0, rad(h["yaw"] + 80)), 1.0))
        A((BAGUETTE, (c[0], c[1], c[2] + 0.15), (0.0, 0.0, rad(h["yaw"] + 90)), 1.0))
        A((BAGUETTE, (c[0] + 0.06 * s, c[1] - 0.12 * s, c[2] + 0.15 - (c[2] + 0.09) * s * s), (0.0, 0.0, rad(h["yaw"] + 70 + 40 * s)), 1.0))
    elif i == 8:                           # 모두가 받아 주는 물건 = 라면이 머리 위에서 반짝
        m = place("minsu", 8)
        top = _loc(m, 0.0, 0.0, 2.15)
        A((RAMEN_U, top, facing(m), 1.5 * pop(u, 0.0, 0.25)))
        out += sparks(top, t, u, 0.1, 0.3, axis_yaw=m["yaw"])
    elif i == 9:                           # 라면 값 치르기: 민수 손 → 점원 손 → 계산대 라면 더미
        m, c = place("minsu", 9), place("clerk", 9)
        hm, hc = hand_pt(m, "L", 0.07), hand_pt(c, "R", 0.07)
        base = (0.0, 1.15, 1.05)
        for k in range(3):
            A((RAMEN_F if k % 2 == 0 else RAMEN_F2, ramen_slot(base, k), (0.0, 0.0, rad(-90 + 6 * (k % 3 - 1))), 1.0))
        for j in range(3):
            a = 0.05 + 0.17 * j
            s1, s2 = ramp(u, a, a + 0.10), ramp(u, a + 0.12, a + 0.24)
            vis = 1.0 if j == 0 else pop(u, a - 0.05, a)
            k = 3 + j
            p = arc(hc, ramen_slot(base, k), s2, 0.10) if s2 > 0 else arc(hm, hc, s1, 0.06)
            A((RAMEN_F if k % 2 == 0 else RAMEN_F2, p, (0.0, 0.0, rad(-90 + 6 * (k % 3 - 1) * s2)), vis))
    elif i == 10:                          # 라면 지갑: 지갑에서 라면이 부채꼴로 삐죽
        d = place("minsu", 10)
        w = wallet_pt(d)
        A((WALLET, w, facing(d), 1.0))
        a = rad(d["yaw"])
        for k, roll in enumerate((-0.55, -0.27, 0.0, 0.27, 0.55)):
            fwd, lat, up = 0.03 + 0.012 * k, -0.07 * math.sin(roll), 0.07 * math.cos(roll) + 0.04
            p = (w[0] + math.cos(a) * fwd - math.sin(a) * lat, w[1] + math.sin(a) * fwd + math.cos(a) * lat, w[2] + up)
            A((RAMEN_U if k % 2 == 0 else RAMEN_U2, p, (roll, 0.0, a), pop(u, 0.04 + 0.05 * k, 0.16 + 0.05 * k)))
    elif i == 11:                          # 라면 저금통: 하나씩 떨어져 탑이 쌓임
        m = place("minsu", 11)
        hm = hand_pt(m, "L", 0.07)
        base = (1.9, 1.2, 0.77)
        above = (1.9, 1.2, 1.95)
        for k in range(4):
            A((RAMEN_F if k % 2 == 0 else RAMEN_F2, ramen_slot(base, k, 0.5), (0.0, 0.0, rad(-90 + 7 * (k % 3 - 1))), 1.0))
        for j in range(10):
            a = 0.05 + 0.085 * j
            s = ramp(u, a, a + 0.14)
            k = 4 + j
            if s < 0.55:
                p = arc(hm, above, s / 0.55, 0.15)
            else:
                f = (s - 0.55) / 0.45
                p = lerp3(above, ramen_slot(base, k, 0.5), f * f)
            A((RAMEN_F if k % 2 == 0 else RAMEN_F2, p, (0.0, 0.0, rad(-90 + 7 * (k % 3 - 1) * s)),
               1.0 if j == 0 else pop(u, a - 0.03, a)))
    elif i in (12, 13):                    # 교도소: 탁자 위 라면 더미 + 손에서 손으로 도는 라면
        for k in range(5):
            A((RAMEN_F if k % 2 == 0 else RAMEN_F2, ramen_slot((1.9, 1.0, 0.78), k, 0.5), (0.0, 0.0, rad(-90 + 8 * (k % 3 - 1))), 1.0))
        if i == 13:
            a_, b_, c_ = (place(n, 13) for n in ("inmate_a", "inmate_b", "inmate_c"))
            pts = [hand_pt(a_, "L", 0.07), hand_pt(b_, "R", 0.07), hand_pt(b_, "L", 0.07), hand_pt(c_, "R", 0.07)]
            s = ramp(u, 0.08, 0.88)
            A((RAMEN_U, chain(pts, s, 0.10), CAM, 1.0))
            for k in range(1, 4):
                sk = max(s - 0.045 * k, 0.0)
                if 0.0 < sk < 1.0:
                    A((SPARK, chain(pts, sk, 0.10), (0.0, 0.0, 0.0), 0.8 - 0.2 * k))
    elif i == 15:                          # 미용실: 이번엔 손님이 라면으로 값을 냄
        g, h = place("guest", 15), place("hana", 15)
        hg, hh = hand_pt(g, "L", 0.07), hand_pt(h, "R", 0.07)
        s = ramp(u, 0.10, 0.45)
        p = arc(hg, hh, s, 0.08)
        A((RAMEN_U, p, CAM, 1.0))
        out += sparks(hh, t, u, 0.25, 0.4, n=6, r0=0.22, axis_yaw=-90.0)
        for k in range(2):
            A((RAMEN_F if k == 0 else RAMEN_F2, (0.8 + 0.03 * k, 1.9 - 0.02 * k, 0.84 + 0.0225 + 0.045 * k), (0.0, 0.0, rad(-90 + 12 * k)), 1.0))
    elif i == 17:                          # 믿음 릴레이: 라면 한 봉지가 민수 → 하나 → 점원
        a_, b_, c_ = (place(n, 17) for n in ("minsu", "hana", "clerk"))
        pts = [hand_pt(a_, "L", 0.07), hand_pt(b_, "R", 0.07), hand_pt(b_, "L", 0.07), hand_pt(c_, "R", 0.07)]
        s = ramp(u, 0.10, 0.90)
        A((RAMEN_U, chain(pts, s, 0.10), CAM, 1.0))
        for k in range(1, 4):
            sk = max(s - 0.045 * k, 0.0)
            if 0.0 < sk < 1.0:
                A((SPARK, chain(pts, sk, 0.10), (0.0, 0.0, 0.0), 0.8 - 0.2 * k))
    elif i == 18:                          # 지폐 한 장 + 반짝이 + 물음표
        d = place("minsu", 18)
        w = wallet_pt(d)
        A((BILL, (w[0], w[1], w[2] + 0.02), (math.pi / 2, 0.0, rad(d["yaw"]) + math.pi / 2), 2.2))
        out += sparks((w[0], w[1], w[2] + 0.02), t, u, 0.1, 0.3, n=8, r0=0.25, axis_yaw=d["yaw"])
        A((QMARK, (w[0], w[1], w[2] + 0.62 + 0.03 * math.sin(t * 3)), facing(d), pop(u, 0.05, 0.3)))
    return out


# ───────────────────────── Blender 원형(프로토) ─────────────────────────
def _B(cx, cy, cz, sx, sy, sz):
    """가운데가 (cx,cy,cz)인 상자."""
    from engine import bkit as K
    return K.bm_cube(sx, sy, sz, (cx, cy, cz))


def _rotz(bm, ang):
    c, s = math.cos(ang), math.sin(ang)
    for v in bm.verts:
        x, y = v.co.x, v.co.y
        v.co.x, v.co.y = c * x - s * y, s * x + c * y
    return bm


def _ramen_parts(base, upright):
    """라면 봉지 = 납작(길이 x·폭 y·두께 z, 원점 = 바닥 가운데) 또는 세움(두께 x·폭 y·길이 z, 원점 = 뒷면 가운데, 띠가 위)."""
    def T(cx, cy, cz, sx, sy, sz):
        return _B(cz, cy, -cx, sz, sy, sx) if upright else _B(cx, cy, cz, sx, sy, sz)
    edge = tuple(c * 0.7 for c in base)
    WH, YE = (0.97, 0.95, 0.88), (1.0, 0.82, 0.18)
    return [(T(0, 0, 0.0225, 0.30, 0.21, 0.045), base), (T(0, 0, 0.0225, 0.304, 0.214, 0.010), WH),
            (T(0, 0, 0.047, 0.17, 0.12, 0.004), WH), (T(0.0, 0, 0.0505, 0.09, 0.05, 0.004), (0.55, 0.30, 0.15)),
            (T(0.0, 0, 0.0535, 0.07, 0.03, 0.004), YE), (T(-0.115, 0, 0.047, 0.05, 0.21, 0.004), YE),
            (T(0.147, 0, 0.0225, 0.012, 0.218, 0.05), edge), (T(-0.147, 0, 0.0225, 0.012, 0.218, 0.05), edge)]


def _goods_parts():
    """소품 종류 순서(RAMEN_F ... QMARK)대로 [(이름, [(상자, 색[, 발광])])]."""
    WH, BR, TAN = (0.97, 0.95, 0.88), (0.42, 0.26, 0.14), (0.85, 0.72, 0.55)
    wallet = [(_B(-0.01, 0, 0, 0.02, 0.34, 0.22), BR), (_B(0.004, 0, 0, 0.008, 0.30, 0.18), TAN),
              (_B(0.010, 0, 0, 0.004, 0.008, 0.18), (0.3, 0.18, 0.1))]
    for z in (-0.04, 0.0, 0.04):
        wallet.append((_B(0.010, -0.08, z, 0.004, 0.12, 0.012), (0.6, 0.45, 0.3)))
    wallet.append((_B(0.010, 0.085, -0.06, 0.004, 0.12, 0.06), (0.6, 0.45, 0.3)))
    g, g2 = (0.40, 0.74, 0.46), (0.30, 0.62, 0.36)
    bill = [(_B(0, 0, 0, 0.16, 0.075, 0.004), g, 0.4), (_B(0, 0, 0.0025, 0.14, 0.055, 0.002), g2, 0.4),
            (_B(0, 0, 0.0035, 0.036, 0.036, 0.002), (0.88, 0.96, 0.82), 0.4)]
    phone = [(_B(0, 0, 0, 0.026, 0.21, 0.38), (0.07, 0.08, 0.10)), (_B(0.0145, 0, 0, 0.003, 0.19, 0.35), (0.92, 0.96, 1.0), 1.6),
             (_B(0.0165, 0, 0.143, 0.002, 0.186, 0.058), (0.15, 0.38, 0.9), 1.6),
             (_B(0.0165, 0, -0.14, 0.002, 0.15, 0.012), (0.7, 0.72, 0.78), 1.6), (_B(0.0165, 0, -0.165, 0.002, 0.15, 0.012), (0.7, 0.72, 0.78), 1.6)]
    for c, r in glyph_cells("0"):                                                    # 큰 빨간 0
        phone.append((_B(0.017, (c - 2) * 0.022, (r - 3) * 0.022 + 0.01, 0.002, 0.022, 0.022), (0.9, 0.12, 0.12), 2.0))
    qm = [(_B(0, (c - 2) * 0.07, (r - 3) * 0.07, 0.03, 0.07, 0.07), (1.0, 0.9, 0.4), 2.5) for c, r in glyph_cells("?")]
    steel = (0.8, 0.82, 0.86)
    sci_a = [(_rotz(_B(0.07, 0, 0, 0.14, 0.012, 0.008), 0.25), steel), (_rotz(_B(0.07, 0, 0.002, 0.14, 0.012, 0.008), -0.25), steel),
             (_rotz(_B(-0.045, 0, 0, 0.07, 0.014, 0.014), 0.5), (0.85, 0.15, 0.2)),
             (_rotz(_B(-0.045, 0, 0.002, 0.07, 0.014, 0.014), -0.5), (0.85, 0.15, 0.2))]
    sci_b = [(_B(0.07, 0, 0, 0.14, 0.012, 0.008), steel), (_B(-0.045, 0, 0, 0.07, 0.03, 0.014), (0.85, 0.15, 0.2))]
    eggbox = [(_B(0, 0, 0.02, 0.12, 0.34, 0.04), (0.78, 0.68, 0.5))]
    for ix in (-0.03, 0.03):
        for iy in (-0.1, 0.0, 0.1):
            eggbox.append((_B(ix, iy, 0.08, 0.05, 0.07, 0.08), (0.96, 0.92, 0.82)))
    bread = [(_B(0, 0, 0.04, 0.26, 0.13, 0.08), (0.78, 0.52, 0.24)), (_B(0, 0, 0.095, 0.22, 0.11, 0.05), (0.62, 0.38, 0.15)),
             (_B(-0.05, 0, 0.122, 0.012, 0.09, 0.004), (0.92, 0.75, 0.48)), (_B(0.05, 0, 0.122, 0.012, 0.09, 0.004), (0.92, 0.75, 0.48))]
    bag = [(_B(0, 0, 0.04, 0.55, 0.07, 0.07), (0.82, 0.58, 0.26))] + [
        (_B(x, 0, 0.077, 0.02, 0.05, 0.004), (0.94, 0.8, 0.55)) for x in (-0.15, 0.0, 0.15)]
    rice = [(_B(0, 0, 0, 0.26, 0.46, 0.28), (0.93, 0.89, 0.78))]                                   # 가슴 앞에 가로로 안는 쌀 포대
    for sy in (-1, 1):
        rice += [(_B(0, sy * 0.25, 0, 0.12, 0.08, 0.14), (0.85, 0.80, 0.68)), (_B(0, sy * 0.215, 0, 0.14, 0.02, 0.16), (0.8, 0.15, 0.12))]
    rice += [(_B(0.132, 0, 0, 0.004, 0.26, 0.17), (0.78, 0.18, 0.14)), (_B(0.134, 0, 0, 0.003, 0.2, 0.11), WH),
             (_B(0.136, 0, 0, 0.002, 0.1, 0.05), (0.9, 0.7, 0.15))]
    rbox = [(_B(0, 0, 0, 0.32, 0.44, 0.24), (0.72, 0.55, 0.35)), (_B(0, 0, 0.122, 0.32, 0.03, 0.004), (0.85, 0.75, 0.5)),
            (_B(0.162, 0, 0, 0.004, 0.30, 0.15), (0.88, 0.2, 0.12)), (_B(0.164, 0, 0, 0.003, 0.22, 0.10), WH),
            (_B(0.166, 0, 0, 0.002, 0.10, 0.05), (0.55, 0.30, 0.15))]
    return [("ramen_f", _ramen_parts((0.88, 0.20, 0.12), False)), ("ramen_f2", _ramen_parts((0.96, 0.58, 0.12), False)),
            ("ramen_u", _ramen_parts((0.88, 0.20, 0.12), True)), ("ramen_u2", _ramen_parts((0.96, 0.58, 0.12), True)),
            ("egg", [(_B(0, 0, 0.045, 0.06, 0.06, 0.09), (0.96, 0.92, 0.82))]), ("eggbox", eggbox), ("bread", bread),
            ("baguette", bag), ("rice", rice), ("wallet", wallet), ("bill", bill), ("phone", phone), ("sci_a", sci_a),
            ("sci_b", sci_b), ("clip", [(_B(0.025, 0, 0, 0.05, 0.012, 0.012), (0.11, 0.075, 0.055))]), ("rbox", rbox),
            ("spark", [(_B(0, 0, 0, 0.05, 0.05, 0.05), (1.0, 0.92, 0.5), 3.0)]), ("qmark", qm)]


def _goods_protos(ctx):
    from engine import bkit as K
    cache = {}

    def mat(col, gl):
        key = (tuple(round(c, 3) for c in col), gl)
        if key not in cache:
            n = f"ep25_m_{len(cache):02d}"
            col = tuple(col)
            if gl >= 1.0:
                cache[key] = K.mat_emit(n, col, gl)
            elif gl > 0:
                cache[key] = K.mat_simple(n, col, 0.7, 0.0, col, gl)
            else:
                cache[key] = K.mat_simple(n, col, 0.7)
        return cache[key]

    protos = []
    for name, parts in _goods_parts():
        mats, idx, out = [], {}, []
        for bm, col, *g in parts:
            gl = g[0] if g else 0.0
            key = (tuple(round(c, 3) for c in col), gl)
            if key not in idx:
                idx[key] = len(mats)
                mats.append(mat(col, gl))
            out.append((bm, idx[key]))
        protos.append(K.proto(ctx, "ep25_p_" + name, K.join_bms(out), mats))
    return protos


def _custom_protos(ctx, mats):
    """새 자세(CUSTOM) 캐릭터 원형: 바탕 자세의 몸에서 팔 4조각만 빼고 새 각도로 다시 붙임."""
    from engine import bkit as K
    from engine import voxel as X
    out = []
    for lh in (False, True):
        for name, (base, arms) in CUSTOM.items():
            P = X._person(X.POSES[base], lh)
            for bm, _ in P[-4:]:
                bm.free()
            P = P[:-4]
            hip = _hip(base)
            for sy, ang in ((-0.34, arms[0]), (0.34, arms[1])):
                sleeve = K.bm_cube(0.18, 0.16, 0.46, (0, sy, hip + 0.12), bottom=True)
                hand = K.bm_cube(0.17, 0.15, 0.14, (0, sy, hip - 0.02), bottom=True)
                piv = (0, 0, hip + 0.54)
                P += [(X._rot_y(sleeve, ang, piv), 0), (X._rot_y(hand, ang, piv), 2)]
            out.append(K.proto(ctx, f"ep25_p_vox_{int(lh)}_{name}", K.join_bms(P), mats))
    return out


def build(ctx):
    from engine import bkit as K
    from engine import voxel as X
    v = X.Vox(25)
    for name, fn in (("home", lambda w: _home(w, False)), ("mart", _mart), ("salon", _salon), ("office", _office),
                     ("cell", _cell), ("stage", _stage), ("home_pm", lambda w: _home(w, True))):
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep25_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    mats = X.people_mats()
    protos = X.people_protos(ctx, mats) + _custom_protos(ctx, mats)
    C = cast()
    people = K.instancer_multi(ctx, "ep25_people", protos, len(C))
    goods = K.instancer_multi(ctx, "ep25_goods", _goods_protos(ctx), NG)

    def upd(t, f):
        i = line_at(t)
        a, b = shot_span(i)
        u = (t - a) / max(b - a, 1e-3)
        st, tg, az, el, dist, lens, push, daz = LINES[i]["shot"]
        o = OFF[st]
        cam.set((tg[0] + o[0], tg[1] + o[1], tg[2]), az + daz * u, el, dist * (1 + (push - 1) * u), lens)
        night = i >= NIGHT_FROM
        sun.data.energy = 0.0 if night else 3.0
        ctx.set_ctl("ambient", 0.12 if night else 0.42)
        ctx.set_rgb("ambient_col", (0.35, 0.42, 0.65) if night else (0.62, 0.68, 0.82))
        # 캐릭터
        P, R, CO, C2, SC, PO = [], [], [], [], [], []
        for c in C:
            d = dict(c)
            d.update(c["over"].get(i, {}))
            show = c["only"] is None or i in c["only"]
            ox, oy = OFF[d["set"]]
            P.append((d["x"] + ox, d["y"] + oy, d["z"]))
            R.append((0, 0, math.radians(d["yaw"])))
            CO.append(d["shirt"])
            C2.append(d["pants"])
            SC.append(d["scale"] if show else 0.0)
            PO.append(pose_index(d["pose"], d["hair"]))
        K.set_points(people, P, scale=SC, rot=R, col=np.array(CO, np.float32), colors={"col2": np.array(C2, np.float32)},
                     pose=PO)
        # 소품
        G = props(i, u, t)[:NG]
        K.set_points(goods, [(g[1][0] + o[0], g[1][1] + o[1], g[1][2]) for g in G], scale=[g[3] for g in G],
                     rot=[g[2] for g in G], pose=[g[0] for g in G])

    ctx.on_frame(upd)
