"""EP20 만약에 거짓말을 하면 코가 길어진다면? (19편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
기자회견 긴 코(훅) → 아침 식탁 "숙제 다 했어요" → 회의실 "부장님 말씀이 다 맞아요" → 코로 꽉 찬 회의실
→ 소개팅 "저도 방금 왔어요"(빈 컵 넷) → 옷 가게 "잘 어울리세요" → 기자회견 코가 화면 밖으로
→ 마스크 쓴 거리·코 덮개 가게 줄 → 솔직한 말에 싸움 → 반전: 사람은 하루 평균 한두 번 거짓말(작은 코가 퐁퐁)
→ 밤 식탁 "엄마는 하나도 안 힘들어" → 어떤 거짓말은 사랑.
근거(설명란): 일기 연구에서 대학생은 하루 약 2번, 일반 성인은 약 1번 거짓말, 대부분 심각하지 않다고 여김
(DePaulo 외 1996, Journal of Personality and Social Psychology).
특수효과: 코·마스크 = 얼굴 앞 상자 인스턴스(vector_scale) — 코는 그 줄에서 길이가 자람.
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
OFF = {"news": (0, 0), "home_am": (300, 0), "office": (600, 0), "cafe": (900, 0), "shop": (1200, 0),
       "street": (1500, 0), "home_pm": (1800, 0)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 거짓말을 하면 코가 길어진다면 어떻게 될까요?", gap=0.7, shot=("news", (-0.3, 1.2, 2.0), -55, 4, 4.2, 28, 0.92, 3)),
    dict(say="어느 날부터, 거짓말을 하면 코가 자랍니다", shot=("home_am", (0.0, 0.9, 1.0), -90, 14, 5.6, 26, 0.9, 4)),
    dict(say="“숙제 다 했어요!” 아이의 코가 쭉", shot=("home_am", (0.0, 0.95, 1.0), -50, 6, 2.7, 30, 0.9, 0)),
    dict(say="엄마는 한눈에 알아챘죠", shot=("home_am", (0.5, 1.25, 1.25), -75, 8, 3.3, 28, 0.92, -4)),
    dict(say="회사에선 “부장님 말씀이 다 맞아요!”", shot=("office", (-1.6, 0.7, 1.15), -80, 8, 3.1, 28, 0.9, 0)),
    dict(say="회의실이 코로 꽉 찼어요", shot=("office", (0.3, 0.2, 0.9), -75, 38, 6.0, 26, 0.9, 6)),
    dict(say="소개팅에선 “저도 방금 왔어요”", shot=("cafe", (-1.0, 0.65, 1.15), -60, 6, 3.0, 28, 0.9, 0)),
    dict(say="옷 가게에선 “정말 잘 어울리세요!”", shot=("shop", (1.15, 0.6, 1.45), -60, 6, 2.9, 28, 0.9, 0)),
    dict(say="기자회견에선 코가 화면을 뚫고 나왔죠", shot=("news", (-0.25, 1.4, 1.5), -35, 3, 3.4, 28, 0.85, 0)),
    dict(say="사람들은 마스크로 코를 가리기 시작했고", shot=("street", (0.0, 4.9, 1.45), 0, 5, 5.5, 30, 0.92, 0)),
    dict(say="코 덮개 가게엔 줄이 길게 섰어요", shot=("street", (1.2, 5.0, 1.6), -55, 10, 6.0, 28, 0.9, 4)),
    dict(say="거짓말을 못 하니, 말이 너무 솔직해졌죠", shot=("shop", (1.15, 0.6, 1.45), -60, 5, 2.8, 30, 0.92, 4)),
    dict(say="“솔직히 그 옷 진짜 별로야”", shot=("shop", (1.15, 0.6, 1.45), -120, 5, 2.8, 30, 0.92, -4)),
    dict(say="여기저기서 싸움이 터졌습니다", gap=0.7, shot=("street", (-1.5, 4.35, 1.35), -100, 7, 3.8, 30, 0.9, 6)),
    dict(say="그런데 사실, 사람은 하루 평균", shot=("street", (0.0, 4.0, 1.2), -90, 14, 10.0, 26, 0.9, 0)),
    dict(say="한두 번은 거짓말을 한대요", shot=("cafe", (0.3, 0.2, 1.1), -90, 14, 5.5, 26, 0.9, 4)),
    dict(say="대부분은 별일 아닌 작은 거짓말이죠", gap=0.7, shot=("office", (0.3, 0.5, 1.1), -100, 12, 4.8, 26, 0.9, 6)),
    dict(say="“엄마는 하나도 안 힘들어”", gap=0.9, shot=("home_pm", (0.35, 1.0, 1.25), -72, 6, 3.2, 26, 0.92, 0)),
    dict(say="어떤 거짓말은 사랑이었어요", gap=0.7, shot=("home_pm", (0.0, 0.85, 1.3), -115, 4, 1.9, 32, 0.92, 0)),
    dict(say="오늘 당신이 한 거짓말은 어떤 거였나요?", shot=("home_pm", (0.3, 0.95, 1.15), -90, 10, 4.2, 26, 1.35, 0)),
]
TITLE = [("만약에", "white"), ("거짓말을 하면", "white"), ("코가 길어진다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = 14          # '그런데 사실' 줄
NIGHT_FROM = 17     # 밤 식탁부터 밤

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep20_pinocchio" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep20", "title": "만약에 거짓말을 하면 코가 길어진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "D", "mode": "major", "bpm": 100, "seed": 201, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

SKIN = (0.93, 0.74, 0.58)
MASK = (0.96, 0.97, 0.98)


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


def nose_len(spec, u):
    """spec=(처음, 끝[, 자라기 시작 u, 끝 u]) → 이 줄 진행도 u에서의 코 길이(m)."""
    a, b, s0, s1 = (*spec, 0.35, 0.8)[:4]
    return a + (b - a) * ramp(u, s0, s1)


def face_pt(d, fwd, up):
    """캐릭터 얼굴 앞 점(세트 기준): 앞(+x→yaw)으로 fwd, 머리 아래면(hz)에서 위로 up. 크기 반영."""
    s = d["scale"]
    hz = 1.05 if d["pose"].startswith("sit") else 1.36
    a = math.radians(d["yaw"])
    return d["x"] + math.cos(a) * fwd * s, d["y"] + math.sin(a) * fwd * s, d["z"] + (hz + up) * s


# ───────────────────────── 세트 ─────────────────────────
def _home(v, night):
    from engine import voxel as X
    v.floor(-3, 3, -2.5, 2.5, (0.70, 0.52, 0.34), 0.25, "wood")
    v.wall((-3, 2.5), (3, 2.5), 0, 2.7, (0.93, 0.90, 0.82), 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 2.7, (0.86, 0.88, 0.80), 0.25, face=1)
    v.box(-2.95, 0.4, 1.9, 2.48, 0, 0.88, (0.95, 0.95, 0.93))                 # 싱크대
    v.box(-2.97, 0.42, 1.86, 2.48, 0.88, 0.93, (0.55, 0.57, 0.6))
    v.box(-2.95, 0.4, 2.1, 2.48, 1.55, 2.25, (0.95, 0.95, 0.93))              # 찬장
    for x in np.arange(-2.7, 0.3, 0.75):
        v.box(x, x + 0.25, 1.88, 1.9, 0.62, 0.65, (0.3, 0.3, 0.32), jit=0)
        v.box(x, x + 0.25, 2.08, 2.1, 1.62, 1.65, (0.3, 0.3, 0.32), jit=0)
    v.box(-1.7, -1.3, 2.2, 2.4, 0.93, 1.2, (0.75, 0.75, 0.78))                # 전기 주전자
    v.box(0.6, 1.45, 1.75, 2.48, 0, 2.0, (0.82, 0.84, 0.87))                  # 냉장고
    v.box(1.38, 1.41, 1.73, 1.75, 0.9, 1.5, (0.3, 0.3, 0.32), jit=0)
    v.box(0.75, 1.0, 1.73, 1.75, 1.3, 1.55, (0.95, 0.75, 0.3), jit=0)         # 자석 메모
    v.window(1.8, 2.8, 2.49, 1.0, 2.2, night=night, lights=12)
    X.table(v, 0.0, 0.3, 1.8, 1.0, 0.74, (0.85, 0.72, 0.52))
    X.chair(v, 0.0, 1.0, -90)
    X.chair(v, -0.7, -0.4, 90)
    X.chair(v, 0.7, -0.4, 90)
    for x, y in ((0.0, 0.6), (-0.55, 0.05), (0.55, 0.05)):                    # 접시
        v.box(x - 0.14, x + 0.14, y - 0.12, y + 0.12, 0.74, 0.77, (0.97, 0.97, 0.95), jit=0)
    v.box(-0.06, 0.06, 0.6, 0.66, 0.77, 0.8, (0.95, 0.85, 0.3), jit=0)       # 계란 노른자
    v.box(0.25, 0.36, 0.55, 0.66, 0.74, 0.88, (0.95, 0.6, 0.2) if not night else (0.95, 0.95, 0.95))  # 컵
    v.box(-0.5, -0.1, 0.62, 0.72, 0.74, 0.78, (0.35, 0.55, 0.85))            # 공책
    v.box(-0.04, 0.04, 0.26, 0.34, 1.9, 2.7, (0.2, 0.2, 0.2), jit=0)          # 펜던트 등
    v.box(-0.22, 0.22, 0.08, 0.52, 1.82, 1.9, (1.0, 0.85, 0.6), jit=0, glow=True)
    v.box(1.8, 2.4, -2.2, -1.6, 0, 0.5, (0.35, 0.6, 0.45))                    # 화분
    v.box(1.75, 2.45, -2.25, -1.55, 0.5, 1.1, (0.25, 0.55, 0.25), jit=0.1)
    if night:
        v.light(0.0, 0.3, 1.7, 120, (1.0, 0.78, 0.5), 0.3, "pm_pend")
        v.light(2.3, 1.9, 1.6, 15, (0.55, 0.65, 1.0), 0.6, "pm_moon")
    else:
        v.light(0.0, 0.3, 1.7, 40, (1.0, 0.9, 0.75), 0.3, "am_pend")
        v.light(2.3, 1.6, 1.7, 120, (0.85, 0.92, 1.0), 0.8, "am_win")


def _office(v):
    from engine import voxel as X
    v.floor(-4, 4, -3, 3, (0.55, 0.57, 0.6), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, 3, (0.85, 0.86, 0.88), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, 3, (0.82, 0.84, 0.86), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, 3, (0.82, 0.84, 0.86), 0.5, face=1)
    for x0 in (-3.4, -0.6, 2.2):
        v.window(x0, x0 + 2.2, 2.99, 0.9, 2.6, night=False)
    v.box(-3.99, -3.96, -0.9, 1.5, 1.0, 2.3, (0.08, 0.08, 0.09))              # 발표 화면
    v.box(-3.96, -3.95, -0.8, 1.4, 1.08, 2.22, (0.6, 0.8, 1.0), jit=0, glow=True)
    v.box(-3.95, -3.94, -0.5, 1.1, 1.75, 1.85, (0.95, 0.5, 0.3), jit=0, glow=True)   # 화면 속 막대그래프
    v.box(-3.95, -3.94, -0.5, 0.4, 1.5, 1.6, (0.3, 0.8, 0.5), jit=0, glow=True)
    X.table(v, 0.3, 0.2, 3.9, 1.3, 0.74, (0.92, 0.92, 0.9))
    X.chair(v, -2.15, 0.2, 0, (0.2, 0.22, 0.26))
    for x in (-1.0, 0.3, 1.6):
        X.chair(v, x, 1.15, -90, (0.2, 0.22, 0.26))
        v.box(x - 0.25, x + 0.15, 0.55, 0.75, 0.74, 0.76, (0.96, 0.96, 0.96))    # 서류
    for x in (-0.55, 0.75, 2.05):
        X.chair(v, x, -0.75, 90, (0.2, 0.22, 0.26))
        v.box(x - 0.15, x + 0.25, -0.35, -0.15, 0.74, 0.76, (0.96, 0.96, 0.96))
    for x in (-2.0, 1.0):
        v.box(x - 0.08, x + 0.08, -0.05, 0.05, 0.74, 0.86, (0.95, 0.95, 0.95))  # 종이컵
    v.box(3.3, 3.8, 2.3, 2.8, 0, 0.5, (0.35, 0.6, 0.45))                      # 화분
    v.box(3.25, 3.85, 2.25, 2.85, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.5, 0.5, 3.0):
        v.box(x - 0.6, x + 0.6, -0.1, 0.5, 2.95, 3.0, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.2, 2.6, 110, (0.95, 0.97, 1.0), 0.6)


def _cafe(v):
    from engine import voxel as X
    v.floor(-3.5, 3.5, -3, 3, (0.55, 0.38, 0.25), 0.25, "wood")
    v.wall((-3.5, 3), (3.5, 3), 0, 2.9, (0.88, 0.80, 0.68), 0.25, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, 2.9, (0.72, 0.44, 0.34), 0.25, face=-1, kind="brick")
    v.wall((3.5, -3), (3.5, 3), 0, 2.9, (0.88, 0.80, 0.68), 0.25, face=1)
    v.window(-2.4, 0.2, -3.49, 0.9, 2.3, night=False, face=1, axis="x")
    v.box(0.9, 3.3, 2.0, 2.6, 0, 1.0, (0.45, 0.3, 0.2))                        # 계산대
    v.box(0.85, 3.35, 1.95, 2.65, 1.0, 1.05, (0.92, 0.9, 0.86))
    v.box(2.4, 2.9, 2.2, 2.55, 1.05, 1.5, (0.75, 0.75, 0.78))                 # 커피 머신
    v.box(1.3, 1.5, 2.2, 2.35, 1.05, 1.15, (0.95, 0.95, 0.95))
    v.box(1.2, 3.2, 2.97, 2.99, 1.7, 2.5, (0.16, 0.16, 0.17))                 # 메뉴판
    for k in range(4):
        v.box(1.35, 1.35 + 0.6 + 0.25 * (k % 2), 2.96, 2.97, 2.3 - k * 0.17, 2.34 - k * 0.17,
              (0.95, 0.9, 0.75), jit=0, glow=True)
    for (cx, cy) in ((-1.0, 0.6), (1.0, -0.6), (-1.4, -1.7)):
        X.table(v, cx, cy, 0.8, 0.8, 0.74, (0.62, 0.45, 0.3))
        X.chair(v, cx - 0.6, cy, 0)
        X.chair(v, cx + 0.6, cy, 180)
    for k in range(4):                                                          # 오래 기다린 빈 컵 넷
        x = -1.25 + 0.17 * k
        v.box(x - 0.05, x + 0.05, 0.38, 0.48, 0.74, 0.86, (0.97, 0.97, 0.95))
    for (x, y) in ((1.15, -0.6), (0.85, -0.55), (-1.4, -1.6)):
        v.box(x - 0.05, x + 0.05, y - 0.05, y + 0.05, 0.74, 0.85, (0.97, 0.97, 0.95))
    v.box(-3.3, -2.8, 2.3, 2.8, 0, 0.5, (0.35, 0.6, 0.45))                    # 화분
    v.box(-3.35, -2.75, 2.25, 2.85, 0.5, 1.4, (0.25, 0.55, 0.25), jit=0.1)
    for (x, y) in ((-1.0, 0.6), (1.0, -0.6), (2.1, 2.3)):
        v.box(x - 0.03, x + 0.03, y - 0.03, y + 0.03, 2.2, 2.9, (0.2, 0.2, 0.2), jit=0)   # 펜던트 등
        v.box(x - 0.15, x + 0.15, y - 0.15, y + 0.15, 2.05, 2.2, (1.0, 0.82, 0.55), jit=0, glow=True)
        v.light(x, y, 1.95, 60, (1.0, 0.82, 0.55), 0.3)


def _shop(v):
    from engine import voxel as X
    rs = v.rs
    v.floor(-3.5, 3.5, -3, 3, (0.86, 0.86, 0.84), 0.5, "check")
    v.wall((-3.5, 3), (3.5, 3), 0, 2.9, (0.95, 0.94, 0.92), 0.5, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, 2.9, (0.90, 0.86, 0.82), 0.5, face=-1)
    v.wall((3.5, -3), (3.5, 3), 0, 2.9, (0.90, 0.86, 0.82), 0.5, face=1)
    cloth = [(0.85, 0.3, 0.3), (0.3, 0.45, 0.8), (0.95, 0.8, 0.35), (0.35, 0.65, 0.4), (0.95, 0.95, 0.92),
             (0.55, 0.38, 0.7), (0.2, 0.2, 0.22), (0.95, 0.6, 0.7)]
    for x0, x1 in ((-3.0, -0.4), (0.4, 3.0)):                                   # 벽 옷걸이
        v.box(x0, x1, 2.6, 2.64, 1.76, 1.8, (0.7, 0.7, 0.72), jit=0)
        x = x0 + 0.05
        while x < x1 - 0.12:
            v.box(x, x + 0.1, 2.35, 2.85, float(rs.uniform(0.75, 1.0)), 1.74, cloth[int(rs.integers(len(cloth)))])
            x += 0.15
    X.table(v, -1.6, -0.2, 1.3, 0.8, 0.8, (0.92, 0.92, 0.9))                 # 개어 둔 옷
    for k in range(6):
        x = -2.1 + (k % 3) * 0.38
        y = -0.4 + (k // 3) * 0.38
        v.box(x, x + 0.3, y, y + 0.3, 0.8, 0.86 + 0.03 * (k % 2), cloth[(k * 3) % len(cloth)])
    v.box(3.44, 3.5, 0.0, 1.3, 0.05, 2.15, (0.62, 0.42, 0.25))                # 거울
    v.box(3.43, 3.44, 0.08, 1.22, 0.12, 2.07, (0.72, 0.82, 0.9), jit=0, glow=True)
    v.box(-3.45, -2.4, 1.6, 1.64, 0.1, 2.25, (0.75, 0.3, 0.35))               # 탈의실 커튼
    for x in (-2.0, 0.5, 2.5):
        v.box(x - 0.6, x + 0.6, -0.2, 0.4, 2.85, 2.9, (1.0, 1.0, 0.98), jit=0, glow=True)
        v.light(x, 0.1, 2.5, 110, (1.0, 0.97, 0.92), 0.6)


def _news(v):
    v.floor(-4, 4, -3, 3, (0.25, 0.27, 0.33), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, 3.2, (0.15, 0.25, 0.5), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, 3.2, (0.2, 0.22, 0.28), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, 3.2, (0.2, 0.22, 0.28), 0.5, face=1)
    v.box(-3.5, 3.5, 2.96, 2.98, 2.55, 2.62, (0.45, 0.65, 1.0), jit=0, glow=True)     # 뒤판 줄 조명
    v.box(-3.5, 3.5, 2.96, 2.98, 0.55, 0.6, (0.45, 0.65, 1.0), jit=0, glow=True)
    v.box(-0.45, 0.45, 2.95, 2.97, 1.95, 2.4, (1.0, 0.85, 0.4), jit=0, glow=True)     # 로고
    v.box(-0.45, 0.45, 1.05, 1.45, 0, 1.1, (0.38, 0.27, 0.18))                 # 연단
    v.box(-0.5, 0.5, 1.0, 1.5, 1.1, 1.15, (0.3, 0.21, 0.14))
    v.box(-0.25, 0.25, 1.03, 1.05, 0.62, 0.95, (0.45, 0.65, 1.0), jit=0, glow=True)
    for x in (-0.14, 0.0, 0.14):                                                # 마이크
        v.box(x - 0.012, x + 0.012, 1.2, 1.224, 1.15, 1.36, (0.1, 0.1, 0.1), jit=0)
        v.box(x - 0.03, x + 0.03, 1.19, 1.24, 1.36, 1.44, (0.08, 0.08, 0.08), jit=0)
    for x, c in ((-2.2, (0.85, 0.25, 0.25)), (2.2, (0.25, 0.45, 0.85))):      # 깃발
        v.box(x - 0.03, x + 0.03, 2.4, 2.46, 0, 2.6, (0.75, 0.7, 0.4), jit=0)
        v.box(x + 0.03, x + 0.75, 2.42, 2.44, 1.7, 2.45, c, jit=0.06)
    v.box(2.1, 2.5, -1.45, -1.05, 1.25, 1.55, (0.15, 0.15, 0.17))             # 방송 카메라
    v.box(2.22, 2.38, -1.06, -0.98, 1.32, 1.48, (0.1, 0.1, 0.1))
    for dx, dy in ((-0.15, -0.15), (0.15, -0.15), (0.0, 0.15)):
        v.box(2.3 + dx - 0.02, 2.3 + dx + 0.02, -1.25 + dy - 0.02, -1.25 + dy + 0.02, 0, 1.25, (0.2, 0.2, 0.22), jit=0)
    for x in (-2.0, 0.0, 2.0):
        v.light(x, 0.5, 2.9, 160, (1.0, 0.97, 0.92), 0.8)
    v.light(0.0, -0.6, 1.8, 120, (1.0, 0.95, 0.9), 0.5)                         # 얼굴 조명


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
    X.storefront(v, 1.0, 6.0, 6.0, 5.0, 11.0, (1.0, 0.72, 0.6), face=-1, lit=0.35)   # 코 덮개 가게
    v.box(2.9, 4.1, 5.94, 5.97, 3.6, 4.7, (0.98, 0.95, 0.9), jit=0, glow=True)        # 간판 판 + 튀어나온 큰 코
    v.box(3.3, 3.7, 5.1, 5.94, 3.95, 4.3, SKIN)
    x = -20.0
    while x < 20:
        w = float(rs.uniform(4.5, 7.0))
        X.storefront(v, x, min(20, x + w), -6.0, 5.0, float(rs.uniform(9, 15)), signs[k % 6], face=1, lit=0.35)
        x += w
        k += 1
    for x in (-16, -8, 0, 8, 16):
        X.street_lamp(v, x, 3.4, energy=1.0)
        X.street_lamp(v, x + 4, -3.4, energy=1.0)
    for x in (-12, -4, 4.5, 12):
        X.tree(v, x, 3.55)


# ───────────────────────── 캐릭터 배치 ─────────────────────────
KID_SH, KID_PA = (0.95, 0.80, 0.35), (0.20, 0.20, 0.22)
MOM_SH, MOM_PA = (0.92, 0.55, 0.60), (0.35, 0.28, 0.20)


def cast():
    """[dict(set, x, y, yaw, pose, hair, shirt, pants, scale, z, over={줄: 덮어쓰기}, only=보이는 줄 집합 or None,
    nose={줄: (처음, 끝[, 시작u, 끝u])}, mask=마스크 쓰는 줄 집합)]"""
    from engine import voxel as X
    rs = np.random.default_rng(20)
    S, Pn = X.SHIRTS, X.PANTS
    C = []

    def add(st, x, y, yaw, pose, hair=0, shirt=None, pants=None, scale=1.0, z=0.0, over=None, only=None,
            nose=None, mask=()):
        C.append(dict(set=st, x=x, y=y, yaw=yaw, pose=pose, hair=hair,
                      shirt=shirt or S[int(rs.integers(len(S)))], pants=pants or Pn[int(rs.integers(len(Pn)))],
                      scale=scale, z=z, over=over or {}, only=only, nose=nose or {}, mask=set(mask)))

    def pop(i, n=0.15):
        """작은 거짓말: 그 줄 안에서 저마다 다른 때에 작은 코가 퐁."""
        s0 = float(rs.uniform(0.05, 0.6))
        return {i: (0.0, n, s0, s0 + 0.15)}
    # 기자회견: 대변인 + 기자들
    add("news", 0.0, 1.75, -90, "talk", 0, (0.2, 0.22, 0.3), (0.15, 0.16, 0.2),
        nose={0: (1.6, 1.6), 8: (0.0, 2.4, 0.3, 0.9)})
    for x, y in ((-1.6, -0.9), (-0.8, -0.9), (0.8, -0.9), (1.6, -0.9), (-1.2, -1.6), (1.2, -1.6)):
        add("news", x, y, 90, "phone", int(rs.random() < 0.5), only={8})   # 첫 컷(제목)에선 머리가 코를 가려 뺌
    # 아침 식탁: 아이 + 엄마
    add("home_am", 0.0, 1.0, -90, "sit", 0, KID_SH, KID_PA, scale=0.78, z=0.1, over={3: dict(pose="sit_conf")},
        nose={2: (0.0, 0.6), 3: (0.6, 0.6)})
    add("home_am", -1.6, 1.55, -90, "stand", 1, MOM_SH, MOM_PA, over={3: dict(x=1.0, y=1.55, yaw=-115, pose="angry")})
    # 회의실: 부장 + 거짓말한 직원 + 동료
    add("office", -2.15, 0.2, 0, "sit", 0, (0.3, 0.3, 0.34), (0.15, 0.15, 0.18), nose={5: (0.45, 0.45), **pop(16)})
    add("office", -1.0, 1.15, -90, "sit", 0, (0.28, 0.48, 0.85), (0.18, 0.2, 0.3), over={4: dict(yaw=-140)},
        nose={4: (0.0, 0.85), 5: (0.85, 0.85), **pop(16)})
    for x, y, yaw in ((0.3, 1.15, -90), (1.6, 1.15, -90), (-0.55, -0.75, 90), (0.75, -0.75, 90), (2.05, -0.75, 90)):
        add("office", x, y, yaw, "sit", int(rs.random() < 0.45), nose={5: (0.7, 0.7), **pop(16)})
    # 카페: 소개팅 두 사람(6번 줄만) + 손님·점원
    add("cafe", -1.6, 0.6, 0, "sit", 0, (0.35, 0.65, 0.40), (0.2, 0.2, 0.22), only={6}, nose={6: (0.0, 0.6, 0.4, 0.85)})
    add("cafe", -0.3, 0.75, 180, "stand", 1, (0.92, 0.92, 0.90), (0.45, 0.5, 0.6), only={6})
    for x, y, yaw in ((0.4, -0.6, 0), (1.6, -0.6, 180), (-2.0, -1.7, 0), (-0.8, -1.7, 180)):
        add("cafe", x, y, yaw, "sit", int(rs.random() < 0.5), nose=pop(15))
    add("cafe", 2.0, 1.75, -90, "stand", 1, (0.95, 0.55, 0.25), (0.2, 0.2, 0.22), nose=pop(15))
    # 옷 가게: 점원(7) → 친구(11·12), 손님은 같은 자리
    add("shop", 0.6, 0.6, 0, "talk", 1, (0.95, 0.55, 0.25), (0.2, 0.2, 0.22), only={7}, nose={7: (0.0, 0.55, 0.4, 0.85)})
    add("shop", 0.6, 0.6, 0, "confused", 0, (0.45, 0.75, 0.85), (0.15, 0.18, 0.3), only={11, 12},
        over={12: dict(pose="talk")})
    add("shop", 1.7, 0.6, 180, "stand", 1, (0.55, 0.38, 0.70), (0.12, 0.12, 0.13),
        over={11: dict(pose="talk"), 12: dict(pose="angry")})
    # 거리: 코 덮개 가게 줄(10) · 싸우는 두 쌍(13)
    for k, x in enumerate((3.0, 2.35, 1.7, 1.05, 0.4, -0.25, -0.9)):
        add("street", x, 5.0 + 0.06 * (k % 2), 0, "phone" if k in (2, 5) else "stand", int(rs.random() < 0.5),
            z=0.12, only={10}, mask={10})
    for x, yaw in ((-1.9, 0), (-1.1, 180), (1.2, 0), (2.0, 180)):
        add("street", x, 4.35, yaw, "angry", int(rs.random() < 0.5), z=0.12, only={13})
    # 밤 식탁: 지친 엄마 + 곁에 선 아이
    add("home_pm", 0.0, 1.0, -90, "sit_conf", 1, MOM_SH, MOM_PA, over={18: dict(pose="sit"), 19: dict(pose="sit")},
        nose={17: (0.0, 0.3, 0.5, 0.95), 18: (0.3, 0.3), 19: (0.3, 0.3)})
    add("home_pm", 0.8, 1.25, -160, "stand", 0, KID_SH, KID_PA, scale=0.78, over={18: dict(x=0.62, y=1.2, yaw=-165)})
    return C


def crowd(n=70, seed=201):
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
    lie = rs.random(n) < 0.75                        # 반전 컷에서 작은 코가 나는 사람
    lie_at = rs.uniform(0.05, 0.7, n)
    return dict(lane=lane, d=d, x0=x0, spd=spd, ph=ph, hair=hair, sh=sh, pa=pa, lie=lie, lie_at=lie_at)


def build(ctx):
    from engine import bkit as K
    from engine import voxel as X
    v = X.Vox(20)
    for name, fn in (("news", _news), ("office", _office), ("cafe", _cafe), ("shop", _shop), ("street", _street)):
        v.at(*OFF[name])
        fn(v)
    for name, night in (("home_am", False), ("home_pm", True)):
        v.at(*OFF[name])
        _home(v, night)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep20_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    protos = X.people_protos(ctx, X.people_mats())
    C = cast()
    cr = crowd()
    NCR = len(cr["lane"])
    people = K.instancer_multi(ctx, "ep20_people", protos, len(C) + NCR)
    # 코·마스크: 얼굴 앞에 붙는 상자 (원점 = 뒷면 가운데, +x로 뻗음)
    fx = K.instancer(ctx, "ep20_fx", K.proto(ctx, "ep20_p_fx", K.bm_cube(1, 1, 1, (0.5, 0, 0)),
                                             [K.mat_inst("ep20_m_fx", 0.7)]), len(C) + NCR, vector_scale=True)

    def nose_or_mask(d, ox, oy, i, u, show):
        """(점, 크기, 색) 또는 None — 마스크가 코보다 먼저."""
        if not show:
            return None
        s = d["scale"]
        if i in d["mask"]:
            x, y, z = face_pt(d, 0.10, 0.07)
            return (x + ox, y + oy, z), (0.17 * s, 0.49 * s, 0.16 * s), MASK
        if i in d["nose"]:
            L = nose_len(d["nose"][i], u)
            if L > 0.005:
                x, y, z = face_pt(d, 0.235, 0.115)
                return (x + ox, y + oy, z), (L, 0.075 * s, 0.07 * s), SKIN
        return None

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
        # 캐릭터 + 코·마스크
        P, R, CO, C2, SC, PO = [], [], [], [], [], []
        FP, FS, FC = [], [], []
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
            fxi = nose_or_mask(d, ox_, oy_, i, u, show)
            FP.append(fxi[0] if fxi else (0, 0, 0))
            FS.append((*fxi[1], math.radians(d["yaw"])) if fxi else (0, 0, 0, 0))
            FC.append(fxi[2] if fxi else SKIN)
        sx, sy = OFF["street"]
        for k in range(NCR):
            x = (cr["x0"][k] + cr["d"][k] * cr["spd"][k] * t + 14) % 28 - 14
            stride = (cr["ph"][k] + cr["spd"][k] * t / 0.7) % 1.0
            lane = cr["lane"][k]
            z = 0.12 if abs(lane) > 3 else 0.0
            yaw = 0.0 if cr["d"][k] > 0 else 180.0
            hide = (i == 10 and lane > 0 and -3.0 < x < 4.5) or (i == 13 and lane > 0 and abs(x) < 3.2 and lane < 5.2) \
                or (i == 9 and lane > 0 and x > 2.5)   # 9번 줄 카메라(인도 위 x≈5.5) 앞을 지나는 사람

            P.append((x + sx, lane + sy, z))
            R.append((0, 0, math.radians(yaw)))
            CO.append(cr["sh"][k])
            C2.append(cr["pa"][k])
            SC.append(0.0 if hide else 1.0)
            PO.append(int(cr["hair"][k]) * X.NPOSE + (X.WALK_A if stride < 0.5 else X.WALK_B))
            d = dict(x=x, y=lane, z=z, yaw=yaw, pose="walk", scale=1.0, mask={9, 10},
                     nose={14: (0.0, 0.22, cr["lie_at"][k], cr["lie_at"][k] + 0.15)} if cr["lie"][k] else {})
            fxi = nose_or_mask(d, sx, sy, i, u, not hide)
            FP.append(fxi[0] if fxi else (0, 0, 0))
            FS.append((*fxi[1], math.radians(yaw)) if fxi else (0, 0, 0, 0))
            FC.append(fxi[2] if fxi else SKIN)
        K.set_points(people, P, scale=SC, rot=R, col=np.array(CO, np.float32), colors={"col2": np.array(C2, np.float32)},
                     pose=PO)
        FS = np.array(FS, np.float32)
        K.set_points(fx, FP, scale=(FS[:, 0] > 0).astype(np.float32), size=FS[:, :3],
                     rot=np.stack([np.zeros(len(FS)), np.zeros(len(FS)), FS[:, 3]], 1), col=np.array(FC, np.float32))

    ctx.on_frame(upd)
