"""EP19 만약에 사람이 잠을 안 자도 된다면? (시험편: 블록 캐릭터·생활 장면·내레이션, 10-30 오너 기준 채널 방식)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷, 약 2~3초):
침실 → 밤새 북적이는 거리 → 회사 야간 근무 → 24시간 지하철 → 붐비는 편의점 → 새벽반 학원 → 길에 쌓인 침대
→ 사흘 뒤 깜빡깜빡·같은 질문·싸움 → 반전: 뇌는 자는 동안 기억을 정리하고 노폐물을 씻어 냄 → 다시 불을 끄고 잠.
근거(설명란): 수면 중 노폐물 배출(Xie 외 2013, Science) · 수면과 기억 굳히기(Diekelmann & Born 2010)
· 수면 부족과 감정 조절(Yoo 외 2007).
내레이션: tools/tts.py (edge-tts 무료 음성) → assets/voice/ep19_nosleep/timeline.json·narration.m4a
"""
import json
import math
from pathlib import Path

import numpy as np

from engine.common import FPS, ramp

STYLE = "pixe"
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.3, 0.32, 1.6)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"bed": (0, 0), "street": (300, 0), "office": (600, 0), "subway": (900, 0), "store": (1200, 0),
       "class": (1500, 0), "brain": (1800, 0), "apt": (2100, 0)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 사람이 잠을 안 자도 된다면 어떻게 될까요?", gap=0.7, shot=("bed", (1.2, 0.3, 1.35), -95, 14, 4.6, 28, 0.88, 4)),
    dict(say="어느 날 밤, 아무도 졸리지 않게 됐습니다", shot=("bed", (1.35, -0.05, 1.33), -90, 4, 1.5, 32, 0.9, 0)),
    dict(say="새벽 세 시, 침대에 누울 이유가 없어졌죠", shot=("bed", (0.2, 0.5, 1.0), -105, 12, 4.6, 26, 0.92, 6)),
    dict(say="동네는 밤새 대낮처럼 북적이고", shot=("street", (1.0, 4.6, 1.5), -140, 8, 8.5, 24, 0.88, 6)),
    dict(say="하루가 여덟 시간이나 늘어나자", shot=("office", (0.0, 0.6, 1.0), -90, 20, 9.0, 24, 0.9, 0)),
    dict(say="회사는 바로 야간 근무를 만들었습니다", shot=("office", (1.1, -0.1, 1.2), -58, 6, 2.3, 30, 0.9, 6)),
    dict(say="지하철은 24시간 달리고", shot=("subway", (2.0, 0.0, 1.2), 180, 4, 8.0, 24, 0.9, 0)),
    dict(say="편의점은 밤에 더 바빠졌어요", shot=("store", (-1.0, -1.0, 1.1), -108, 13, 4.8, 26, 0.9, 4)),
    dict(say="학원엔 새벽반이 생겼고", shot=("class", (0.6, 0.2, 0.9), 160, 16, 3.6, 24, 0.9, -5)),
    dict(say="필요 없어진 침대가 길에 쌓였습니다", shot=("street", (9.4, 4.0, 0.9), -100, 16, 5.6, 28, 0.9, 6)),
    dict(say="그런데 사흘쯤 지나자", shot=("office", (1.1, -0.1, 1.3), -90, 3, 1.7, 34, 0.85, 0)),
    dict(say="사람들이 이상해지기 시작합니다", shot=("street", (-8.0, 4.6, 1.4), -40, 7, 8.0, 24, 0.9, -6)),
    dict(say="방금 들은 말을 까먹고", shot=("office", (0.75, -0.15, 1.25), -70, 12, 3.0, 30, 0.9, 4)),
    dict(say="같은 질문을 세 번씩 하고", shot=("store", (-2.4, -1.0, 1.55), -120, 3, 2.6, 28, 0.9, 4)),
    dict(say="별일 아닌 걸로 싸웁니다", gap=0.7, shot=("street", (-5.95, 4.5, 1.3), -76, 5, 4.8, 28, 0.88, 0)),
    dict(say="사실 우리 뇌는 자는 동안", shot=("brain", (0.0, 0.0, 2.0), -70, 14, 9.5, 30, 0.9, 16)),
    dict(say="하루의 기억을 정리하고", shot=("brain", (0.0, 0.0, 2.2), -30, 26, 7.2, 30, 0.92, 14)),
    dict(say="쌓인 찌꺼기를 씻어 내거든요", shot=("brain", (0.0, 0.0, 2.0), 20, 8, 6.6, 30, 0.92, 14)),
    dict(say="졸리지 않아도, 뇌는 잠이 필요했던 거예요", gap=0.5, shot=("bed", (1.35, -0.05, 1.3), -80, 6, 2.2, 30, 0.88, -4)),
    dict(say="결국 사람들은 하나둘 불을 끄고 누웠습니다", gap=0.5, shot=("apt", (0.0, 0.0, 17.0), -90, 10, 56.0, 30, 0.9, 0)),
    dict(say="오늘 밤, 당신은 몇 시간 잘 건가요?", shot=("bed", (1.35, 0.85, 0.7), -90, 62, 3.3, 30, 1.25, 0)),
]
TITLE = [("만약에", "white"), ("사람이", "white"), ("잠을 안 자도 된다면", "white"), ("어떻게 될까요?", "yellow")]

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep19_nosleep" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep19", "title": "만약에 사람이 잠을 안 자도 된다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "F", "mode": "major", "bpm": 92, "seed": 191, "twist_at": STARTS[15]}}
BEATS = []
GRADE = {"exposure": 0.96, "bloom": 0.14, "bloom_thr": 1.3, "vignette": 0.18}


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
    if LINES[line_at(t)]["shot"][0] == "brain":
        return (0.004, 0.006, 0.02), (0.012, 0.01, 0.03), 0.5
    return (0.003, 0.005, 0.016), (0.012, 0.016, 0.035), 1.0


# ───────────────────────── 세트 ─────────────────────────
def _bedroom(v):
    from engine import voxel as X
    v.floor(-2.5, 2.5, -2.0, 2.0, (0.66, 0.46, 0.3), 0.25, "wood")
    v.wall((-2.5, 2.0), (2.5, 2.0), 0, 2.6, (0.86, 0.84, 0.78), 0.25, face=-1)
    v.wall((-2.5, -2.0), (-2.5, 2.0), 0, 2.6, (0.80, 0.84, 0.86), 0.25, face=-1)
    v.wall((2.5, -2.0), (2.5, 2.0), 0, 2.6, (0.80, 0.84, 0.86), 0.25, face=1)
    X.bed(v, 0.6, 2.1, -0.2, 2.0)
    v.box(0.15, 0.55, 1.45, 1.9, 0, 0.55, X.WOOD)                         # 협탁 + 디지털 시계
    v.box(0.22, 0.48, 1.6, 1.68, 0.55, 0.66, (0.08, 0.08, 0.08))
    v.box(0.24, 0.46, 1.59, 1.6, 0.57, 0.64, (1.0, 0.25, 0.15), jit=0, glow=True)
    v.box(0.3, 0.42, 1.75, 1.85, 0.55, 0.85, (0.95, 0.88, 0.7))             # 스탠드
    v.window(-1.7, -0.3, 1.99, 1.0, 2.1, lights=16)
    X.table(v, -2.15, 0.25, 0.6, 1.3, 0.75)
    X.monitor(v, -2.3, 0.25, 0.75, 0)
    X.chair(v, -1.6, 0.25, 180)
    v.box(-1.4, 0.3, -0.6, 0.6, 0, 0.015, (0.86, 0.6, 0.62), jit=0.03)    # 러그
    v.box(-2.45, -1.6, -1.95, -1.2, 0, 1.9, (0.9, 0.88, 0.84))           # 옷장
    v.box(-2.45, -1.6, -1.21, -1.19, 0.05, 1.85, (0.6, 0.6, 0.6))
    v.box(1.8, 2.4, -1.9, -1.4, 0, 0.5, (0.35, 0.6, 0.45))                # 화분
    v.box(1.75, 2.45, -1.95, -1.35, 0.5, 1.1, (0.25, 0.55, 0.25), jit=0.1)
    v.light(0.0, -0.2, 2.45, 160, (1.0, 0.88, 0.72), 0.6, "bed_ceil")
    v.light(0.36, 1.8, 1.0, 35, (1.0, 0.75, 0.45), 0.15, "bed_lamp")
    v.light(-1.0, 1.4, 1.6, 22, (0.55, 0.65, 1.0), 0.6, "bed_moon")
    v.light(-1.9, 0.25, 1.1, 8, (0.6, 0.8, 1.0), 0.3, "bed_mon")


def _street(v):
    from engine import voxel as X
    rs = v.rs
    v.floor(-20, 20, -3, 3, (0.2, 0.2, 0.22), 0.5)
    for x in np.arange(-19, 20, 3.0):
        v.box(x, x + 1.4, -0.06, 0.06, 0.0, 0.012, (0.9, 0.9, 0.85), jit=0)
    for y0, y1 in ((3, 6), (-6, -3)):
        v.box(-20, 20, y0, y1, 0, 0.12, (0.6, 0.6, 0.6), jit=0)
        v.floor(-20, 20, y0, y1, (0.66, 0.64, 0.6), 0.5, "check", z=0.121)
    signs = [(0.95, 0.3, 0.3), (0.3, 0.8, 1.0), (1.0, 0.8, 0.2), (0.4, 1.0, 0.5), (1.0, 0.5, 0.85), (1.0, 0.6, 0.2)]
    x = -20.0
    k = 0
    while x < 20:
        w = float(rs.uniform(4.5, 7.0))
        X.storefront(v, x, min(20, x + w), 6.0, 5.0, float(rs.uniform(9, 15)), signs[k % 6], face=-1, lit=0.75)
        X.storefront(v, x, min(20, x + w), -6.0, 5.0, float(rs.uniform(9, 15)), signs[(k + 3) % 6], face=1, lit=0.75)
        x += w
        k += 1
    for x in (-16, -8, 0, 8, 16):
        X.street_lamp(v, x, 3.4)
        X.street_lamp(v, x + 4, -3.4)
    for x in (-12, -4, 4, 12):
        X.tree(v, x, 3.55)
    # 버려진 침대 더미 (x 8~12)
    for i, (dx, dy, z, c) in enumerate(((8.2, 3.3, 0.12, (0.35, 0.5, 0.82)), (8.4, 3.35, 0.4, (0.95, 0.95, 0.93)),
                                       (8.1, 3.3, 0.68, (0.85, 0.45, 0.45)), (8.35, 3.32, 0.96, (0.95, 0.95, 0.93)),
                                       (10.3, 3.3, 0.12, (0.5, 0.7, 0.5)), (10.2, 3.35, 0.4, (0.95, 0.95, 0.93)))):
        v.box(dx, dx + 1.5, dy, dy + 2.0, z, z + 0.26, c, jit=0.03)
    v.box(11.9, 12.0, 3.2, 5.2, 0.12, 1.7, (0.95, 0.95, 0.93))               # 세워 둔 매트리스
    v.box(11.6, 11.9, 3.2, 5.2, 0.12, 1.65, (0.95, 0.95, 0.93))


def _office(v):
    from engine import voxel as X
    v.floor(-5, 5, -4, 4, (0.55, 0.57, 0.6), 0.5, "check")
    v.wall((-5, 4), (5, 4), 0, 3, (0.85, 0.86, 0.88), 0.5, face=-1)
    v.wall((-5, -4), (-5, 4), 0, 3, (0.82, 0.84, 0.86), 0.5, face=-1)
    v.wall((5, -4), (5, 4), 0, 3, (0.82, 0.84, 0.86), 0.5, face=1)
    for x0 in (-4.6, -1.4, 1.8):
        v.window(x0, x0 + 2.8, 3.99, 0.9, 2.6, lights=30)
    v.box(4.98, 5.0, -1.5, -1.0, 2.1, 2.6, (0.95, 0.95, 0.95), jit=0)        # 벽시계
    v.box(4.96, 4.98, -1.32, -1.18, 2.35, 2.55, (0.05, 0.05, 0.05), jit=0)
    for ry, face in ((-0.8, -90), (1.6, -90)):
        for x in (-3.3, -1.1, 1.1, 3.3):
            X.table(v, x, ry, 1.5, 0.75, 0.74, (0.85, 0.82, 0.76))
            X.monitor(v, x, ry - 0.15, 0.74, 90)        # 화면이 +y(앉은 사람) 쪽
            X.chair(v, x, ry + 0.72, -90, (0.2, 0.22, 0.26))
            v.box(x + 0.35, x + 0.6, ry - 0.1, ry + 0.15, 0.74, 0.76, (0.95, 0.95, 0.95))   # 서류
    for x in (-3.0, 0.0, 3.0):
        for y in (-1.5, 1.5):
            v.box(x - 0.6, x + 0.6, y - 0.3, y + 0.3, 2.95, 3.0, (0.95, 0.97, 1.0), jit=0, glow=True)
            v.light(x, y, 2.6, 120, (0.95, 0.97, 1.0), 0.6)


def _subway(v):
    v.floor(-8, 8, -1.45, 1.45, (0.6, 0.6, 0.62), 0.4, "check")
    for y, f in ((-1.45, 1), (1.45, -1)):
        v.wall((-8, y), (8, y), 0, 0.85, (0.78, 0.8, 0.84), 0.4, face=f)
        v.wall((-8, y), (8, y), 1.95, 2.3, (0.78, 0.8, 0.84), 0.4, face=f)
        for x0 in np.arange(-7.6, 7.6, 2.0):
            v.window(x0, x0 + 1.6, y, 0.85, 1.95, lights=6, face=f)
        s = 1 if y < 0 else -1
        v.box(-7.8, 7.8, min(y, y + 0.5 * s), max(y, y + 0.5 * s), 0, 0.45, (0.25, 0.42, 0.75), jit=0.03)
        v.box(-7.8, 7.8, min(y, y + 0.1 * s), max(y, y + 0.1 * s), 0.45, 0.85, (0.25, 0.42, 0.75), jit=0.03)
        v.box(-8, 8, min(y + 0.7 * s, y + 0.74 * s), max(y + 0.7 * s, y + 0.74 * s), 1.85, 1.89, (0.85, 0.85, 0.9))
    for x in (-8, 8):
        v.wall((x, -1.45), (x, 1.45), 0, 2.3, (0.7, 0.72, 0.76), 0.4, face=1 if x < 0 else -1)
    v.tiles((-8, -1.45, 2.3), (0.4, 0, 0), (0, 0.29, 0), 40, 10, lambda i, j: (0.88, 0.88, 0.9))
    for y in (-0.55, 0.55):
        v.box(-7.8, 7.8, y - 0.08, y + 0.08, 2.27, 2.29, (0.95, 0.97, 1.0), jit=0, glow=True)
    for x in np.arange(-6.1, 7, 2.5):
        v.box(x - 0.03, x + 0.03, 0.22, 0.28, 0, 2.3, (0.95, 0.8, 0.2), jit=0)
    for x in (-5, 0, 5):
        v.light(x, 0, 2.1, 110, (0.95, 0.97, 1.0), 0.8)


def _store(v):
    from engine import voxel as X
    v.floor(-4, 4, -3, 3, (0.9, 0.9, 0.88), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, 2.8, (0.95, 0.95, 0.94), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, 2.8, (0.95, 0.95, 0.94), 0.5, face=-1)
    for x0 in np.arange(-3.4, 3.6, 1.1):                                   # 음료 냉장고
        v.box(x0, x0 + 1.0, 2.6, 2.98, 0, 2.1, (0.7, 0.72, 0.75))
        v.box(x0 + 0.05, x0 + 0.95, 2.59, 2.6, 0.1, 2.0, (0.85, 0.95, 1.0), jit=0, glow=True)
        for r in range(4):
            for c in range(5):
                col = [(0.95, 0.3, 0.25), (0.3, 0.6, 0.95), (0.95, 0.8, 0.2), (0.4, 0.85, 0.45)][(r + c) % 4]
                xx = x0 + 0.1 + c * 0.17
                v.box(xx, xx + 0.1, 2.56, 2.585, 0.2 + r * 0.45, 0.45 + r * 0.45, col, jit=0, glow=True)
    for x in (-0.9, 0.9, 2.7):
        X.shelf(v, x - 0.35, x + 0.35, -0.6, 1.9, 1.5)
    v.box(-3.0, -2.6, -2.2, 0.2, 0, 1.0, (0.3, 0.55, 0.35))                 # 계산대
    v.box(-3.05, -2.55, -2.25, 0.25, 1.0, 1.05, (0.9, 0.9, 0.9))
    v.box(-2.95, -2.7, -1.4, -1.0, 1.05, 1.3, (0.15, 0.15, 0.17))
    v.box(-2.68, -2.66, -1.38, -1.02, 1.1, 1.28, (0.4, 0.9, 0.6), jit=0, glow=True)
    v.box(-3.99, -3.97, -1.0, 1.2, 1.7, 2.4, (0.2, 0.55, 0.3), jit=0, glow=True)   # 벽 간판
    for x in (-2.5, 0.0, 2.5):
        for y in (-1.5, 1.0):
            v.box(x - 0.7, x + 0.7, y - 0.15, y + 0.15, 2.75, 2.8, (1.0, 1.0, 1.0), jit=0, glow=True)
            v.light(x, y, 2.5, 110, (1.0, 1.0, 0.98), 0.6)


def _classroom(v):
    from engine import voxel as X
    v.floor(-4, 4, -3.5, 3.5, (0.62, 0.45, 0.3), 0.25, "wood")
    v.wall((-4, -3.5), (-4, 3.5), 0, 3, (0.9, 0.88, 0.8), 0.5, face=-1)
    v.wall((-4, 3.5), (4, 3.5), 0, 3, (0.9, 0.88, 0.8), 0.5, face=-1)
    v.wall((-4, -3.5), (4, -3.5), 0, 3, (0.9, 0.88, 0.8), 0.5, face=1)
    v.box(-3.99, -3.93, -2.4, 2.4, 0.9, 2.3, (0.16, 0.36, 0.26), jit=0.02)   # 칠판 + 글씨
    for k in range(5):
        y0 = -2.1 + k * 0.4
        v.box(-3.93, -3.92, y0, y0 + float(v.rs.uniform(0.6, 1.8)), 1.95 - k * 0.22, 2.0 - k * 0.22, (0.95, 0.95, 0.9), jit=0)
    v.box(-3.99, -3.97, -0.25, 0.25, 2.45, 2.85, (0.95, 0.95, 0.95), jit=0)   # 시계
    for x0 in (-2.8, 0.2):
        v.window(x0, x0 + 2.4, 3.49, 1.0, 2.5, lights=18)
    for dx in (-1.6, 0.0, 1.6):
        for dy in (-1.8, 0.0, 1.8):
            X.table(v, dx, dy, 0.55, 0.9, 0.68, (0.85, 0.75, 0.55))
            X.chair(v, dx + 0.55, dy, 180, (0.45, 0.45, 0.5), h=0.4)
    for x in (-2.0, 1.5):
        for y in (-1.5, 1.5):
            v.box(x - 0.6, x + 0.6, y - 0.15, y + 0.15, 2.95, 3.0, (1.0, 1.0, 1.0), jit=0, glow=True)
            v.light(x, y, 2.6, 120, (1.0, 0.98, 0.94), 0.6)


def _apartment(v):
    from engine import voxel as X
    v.floor(-40, 40, -40, 12, (0.18, 0.24, 0.16), 2.0)
    v.box(-40, 40, -12, -6, 0, 0.05, (0.25, 0.25, 0.27), jit=0)
    for bx in (-27.0, 0.0, 27.0):
        v.box(bx - 10, bx + 10, 0, 9, 0, 38.5, (0.82, 0.8, 0.76), jit=0.02)
        v.box(bx - 10.3, bx + 10.3, -0.3, 9.3, 38.5, 39.0, (0.6, 0.6, 0.6))
    for x in (-18, -9, 9, 18):
        X.tree(v, x, -3, 4.5)
    for x in (-30, -10, 10, 30):
        X.street_lamp(v, x, -6.5, 5.0, 900)


def window_slots():
    """가운데 동 앞면 창문: 12층 × 6집 (+ 양옆 동)."""
    out = []
    for bx in (-27.0, 0.0, 27.0):
        for fl in range(12):
            for u in range(6):
                out.append((bx - 8.33 + u * 3.33, -0.05, 1.6 + fl * 3.1))
    return np.array(out, np.float32)


# ───────────────────────── 캐릭터 배치 ─────────────────────────
def cast():
    """[(세트, x, y, 방향°, 자세, 머리, 셔츠, 바지, 크기, 높이, {줄: 덮어쓰기}, 보이는 줄 집합 or None)]"""
    from engine import voxel as X
    rs = np.random.default_rng(19)
    S, Pn = X.SHIRTS, X.PANTS
    C = []

    def add(st, x, y, yaw, pose, hair=0, shirt=None, pants=None, scale=1.0, z=0.0, over=None, only=None):
        C.append(dict(set=st, x=x, y=y, yaw=yaw, pose=pose, hair=hair,
                      shirt=shirt or S[int(rs.integers(len(S)))], pants=pants or Pn[int(rs.integers(len(Pn)))],
                      scale=scale, z=z, over=over or {}, only=only))
    hero_shirt, hero_pants = (0.28, 0.48, 0.85), (0.18, 0.2, 0.3)
    # 주인공 '나' (침실·회사)
    add("bed", 1.35, -0.05, -90, "sit", 0, hero_shirt, hero_pants, z=0.1,
        over={2: dict(x=-0.45, y=0.35, yaw=-75, pose="phone", z=0.0),
              20: dict(x=1.35, y=-0.12, yaw=-90, pose="lie", z=0.38)})
    add("office", 1.1, -0.08, -90, "sit", 0, hero_shirt, hero_pants, over={12: dict(pose="sit_conf")})
    add("office", 0.3, -0.3, -15, "talk", 1, (0.92, 0.55, 0.6), (0.2, 0.2, 0.25), only={12})
    for x, ry in ((-3.3, -0.8), (-1.1, -0.8), (3.3, -0.8), (-3.3, 1.6), (-1.1, 1.6), (1.1, 1.6), (3.3, 1.6)):
        add("office", x, ry + 0.72, -90, "sit_phone" if rs.random() < 0.3 else "sit", int(rs.random() < 0.45))
    # 지하철
    for x in (-6.4, -5.2, -3.4, -2.2, -0.2, 1.0, 3.2, 4.4, 6.2):
        add("subway", x, -1.05, 90, "sit_phone" if rs.random() < 0.6 else "sit", int(rs.random() < 0.5))
    for x in (-5.8, -4.0, -1.6, 0.4, 2.6, 5.0):
        add("subway", x, 1.05, -90, "sit_phone" if rs.random() < 0.6 else "sit", int(rs.random() < 0.5))
    add("subway", 1.7, 0.45, 180, "stand", 0, hero_shirt, hero_pants)
    add("subway", 3.6, -0.3, 170, "phone", 1)
    # 편의점: 점원 + 줄 선 손님
    add("store", -3.45, -1.0, 0, "stand", 1, (0.3, 0.6, 0.35), (0.15, 0.15, 0.18), over={13: dict(pose="talk")})
    for i, x in enumerate((-2.15, -1.35, -0.55, 0.25, 1.05, 1.85)):
        add("store", x, -1.0 + 0.08 * (i % 2), 180, "phone" if i in (2, 4) else "stand", int(rs.random() < 0.5),
            over={13: dict(pose="confused")} if i == 0 else None)
    # 교실 새벽반: 학생 9명 + 선생님
    for dx in (-1.6, 0.0, 1.6):
        for dy in (-1.8, 0.0, 1.8):
            add("class", dx + 0.55, dy, 180, "sit", int(rs.random() < 0.5), scale=0.78)
    add("class", -3.3, 1.2, -30, "talk", 0, (0.95, 0.95, 0.92), (0.25, 0.25, 0.3))
    # 거리: 싸우는 두 사람 (14번 줄에서만 화남)
    add("street", -6.6, 4.5, -30, "stand", 0, (0.85, 0.3, 0.28), over={14: dict(pose="angry")})
    add("street", -5.3, 4.5, -150, "stand", 1, (0.95, 0.8, 0.35), over={14: dict(pose="angry")})
    return C


def crowd(n=80, seed=191):
    rs = np.random.default_rng(seed)
    lane = rs.choice([3.7, 4.9, 5.6, -3.8, -4.6, -5.4], n) + rs.uniform(-0.15, 0.15, n)
    d = np.where(rs.random(n) < 0.5, 1.0, -1.0)
    x0 = rs.uniform(-14, 14, n)
    spd = rs.uniform(0.9, 1.4, n)
    ph = rs.uniform(0, 1, n)
    hair = (rs.random(n) < 0.45).astype(int)
    from engine import voxel as X
    sh = np.array([X.SHIRTS[i] for i in rs.integers(len(X.SHIRTS), size=n)], np.float32)
    pa = np.array([X.PANTS[i] for i in rs.integers(len(X.PANTS), size=n)], np.float32)
    weird = rs.random(n) < 0.45
    return dict(lane=lane, d=d, x0=x0, spd=spd, ph=ph, hair=hair, sh=sh, pa=pa, weird=weird)


def build(ctx):
    from engine import bkit as K
    from engine import voxel as X
    from engine.home import mat_glow_inst
    v = X.Vox(19)
    for name, fn in (("bed", _bedroom), ("street", _street), ("office", _office), ("subway", _subway),
                     ("store", _store), ("class", _classroom), ("apt", _apartment)):
        v.at(*OFF[name])
        fn(v)
    # 뇌
    v.at(*OFF["brain"])
    for x, y, z, c in X.brain_voxels():
        v.box(x - 0.1, x + 0.1, y - 0.1, y + 0.1, z + 2.0 - 0.1, z + 2.0 + 0.1, c, jit=0.05)
    v.box(-0.35, 0.35, -0.3, 0.3, 0.0, 1.0, (0.85, 0.5, 0.58))
    v.light(-3.0, -3.0, 5.0, 900, (1.0, 0.85, 0.9), 1.5)
    v.light(3.5, 2.0, 3.0, 500, (0.6, 0.75, 1.0), 1.5)
    obs, lights = v.build(ctx, glow_strength=3.2)
    K.world_space(ctx, ambient=(0.35, 0.42, 0.65), ambient_strength=0.16, ground=(0.06, 0.06, 0.08))
    cam = K.CamRig(ctx, lens=28, fstop=0)

    protos = X.people_protos(ctx, X.people_mats())
    C = cast()
    cr = crowd()
    NCR = len(cr["lane"])
    people = K.instancer_multi(ctx, "vpeople", protos, len(C) + NCR)
    # 뇌: 기억(노란 블록)·청소(파란 블록)
    gm = mat_glow_inst("m_brainfx", 4.0)
    fx = K.instancer(ctx, "brainfx", K.proto(ctx, "p_fx", K.bm_cube(1, 1, 1), [gm]), 220)
    rs = np.random.default_rng(7)
    surf = np.array([(x, y, z) for x, y, z, _ in X.brain_voxels()], np.float32)
    mem_dst = surf[rs.choice(len(surf), 60, replace=False)] * 1.04
    mem_src = rs.normal(size=(60, 3)).astype(np.float32)
    mem_src = mem_src / np.linalg.norm(mem_src, axis=1, keepdims=True) * 7.0
    wash = rs.uniform(0, 2 * math.pi, (160, 2)).astype(np.float32)
    # 아파트 창문
    slots = window_slots()
    wm = K.instancer(ctx, "apt_win", K.proto(ctx, "p_win", K.bm_cube(1, 1, 1), [mat_glow_inst("m_aptwin", 3.0)]),
                     len(slots), vector_scale=True)
    wrs = np.random.default_rng(23)
    w_on = wrs.random(len(slots)) < 0.82
    w_off = wrs.uniform(0.05, 0.92, len(slots))
    ox, oy = OFF["apt"]
    slots_w = slots + np.array((ox, oy, 0), np.float32)
    wcol = np.where(wrs.random(len(slots))[:, None] < 0.8, (1.0, 0.78, 0.42), (0.75, 0.85, 1.0)).astype(np.float32)

    def upd(t, f):
        i = line_at(t)
        a, b = shot_span(i)
        u = (t - a) / max(b - a, 1e-3)
        st, tg, az, el, dist, lens, push, daz = LINES[i]["shot"]
        o = OFF[st]
        cam.set((tg[0] + o[0], tg[1] + o[1], tg[2]), az + daz * u, el, dist * (1 + (push - 1) * u), lens)
        # 침실 불: 마지막 컷만 끔
        dark = i == 20
        lights["bed_ceil"].data.energy = 0.0 if dark else 160.0
        lights["bed_lamp"].data.energy = 6.0 if dark else 35.0
        lights["bed_moon"].data.energy = 60.0 if dark else 22.0
        # 캐릭터
        P, R, CO, C2, SC, PO = [], [], [], [], [], []
        for c in C:
            d = dict(c)
            d.update(c["over"].get(i, {}))
            show = c["only"] is None or i in c["only"]
            ox_, oy_ = OFF[d["set"]]
            P.append((d["x"] + ox_, d["y"] + oy_, d["z"]))
            R.append((0, 0, math.radians(d["yaw"])))
            CO.append(d["shirt"])
            C2.append(d["pants"])
            SC.append(d["scale"] if show else 0.0)
            PO.append(d["hair"] * X.NPOSE + X.POSES[d["pose"]])
        sx, sy = OFF["street"]
        weird_now = i in (11, 14)
        for k in range(NCR):
            slow = 0.35 if (weird_now and cr["weird"][k]) else 1.0
            x = (cr["x0"][k] + cr["d"][k] * cr["spd"][k] * t * slow + 14) % 28 - 14
            stride = (cr["ph"][k] + cr["spd"][k] * t * slow / 0.7) % 1.0
            pose = X.WALK_A if stride < 0.5 else X.WALK_B
            if weird_now and cr["weird"][k]:
                pose = X.CONFUSED if k % 2 else X.STAND
            P.append((x + sx, cr["lane"][k] + sy, 0.12 if abs(cr["lane"][k]) > 3 else 0.0))
            R.append((0, 0, 0.0 if cr["d"][k] > 0 else math.pi))
            CO.append(cr["sh"][k])
            C2.append(cr["pa"][k])
            SC.append(0.0 if (i == 14 and abs(x + 5.95) < 3.0 and cr["lane"][k] < 4.7) else 1.0)
            PO.append(int(cr["hair"][k]) * X.NPOSE + pose)
        K.set_points(people, P, scale=SC, rot=R, col=np.array(CO, np.float32), colors={"col2": np.array(C2, np.float32)},
                     pose=PO)
        # 뇌 효과
        bx, by = OFF["brain"]
        pos = np.zeros((220, 3), np.float32)
        scl = np.zeros(220, np.float32)
        col = np.zeros((220, 3), np.float32)
        if i in (16, 17):   # 기억 블록이 날아와 제자리에 박힘 → 다음 컷에도 남음
            k = np.ones((60, 1), np.float32)
            if i == 16:
                k = np.clip((u * 1.3 - np.arange(60) / 60 * 0.5) / 0.6, 0, 1)[:, None]
                k = k * k * (3 - 2 * k)
            pos[:60] = mem_src * (1 - k) + mem_dst * k
            scl[:60] = 0.16
            col[:60] = (1.0, 0.85, 0.3)
        if i == 17:
            th = wash[:, 0] + u * 2.2
            ph_ = wash[:, 1]
            r = np.array((2.15, 1.75, 1.5), np.float32)
            p = np.stack([np.cos(th) * np.cos(ph_) * r[0], np.sin(ph_) * r[1] * 0.9,
                          np.sin(th) * np.cos(ph_) * r[2]], 1)
            pos[60:] = p
            scl[60:] = 0.12
            col[60:] = (0.35, 0.75, 1.0)
        pos[:, 2] += 2.0
        pos[:, 0] += bx
        pos[:, 1] += by
        K.set_points(fx, pos, scale=scl, rot=np.zeros((220, 3)), col=col)
        # 아파트 창문 꺼짐 (19번 줄 동안 차례로)
        prog = u if i == 19 else (1.0 if i > 19 else 0.0)
        on = w_on & (w_off > prog)
        K.set_points(wm, slots_w, scale=np.ones(len(slots)), size=np.tile((1.9, 0.12, 1.4), (len(slots), 1)),
                     rot=np.zeros((len(slots), 3)), col=np.where(on[:, None], wcol, (0.02, 0.025, 0.04)))

    ctx.on_frame(upd)
