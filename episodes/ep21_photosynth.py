"""EP21 만약에 사람이 광합성을 한다면? (20편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
공원 광장에 두 팔 든 초록 사람들(훅) → 아침 욕실 거울 속 내 피부가 초록으로 → 텅 빈 식당 → 공원 잔디에 누운 사람들
→ 창가로 몰린 회사 책상 → 햇볕 드는 지하철 자리 쟁탈전 → 비 오는 날 시든 사무실·예민 → 해 질 녘 퇴근길 → 일찍 잠든 밤
→ 반전: 햇볕으로 얻는 에너지는 하루 약 35kcal(에너지 막대 2%) → 교실만 한 피부 → 엽록체를 훔친 바다민달팽이
→ 결국 다시 밥 → 같이 먹는 밥 → 질문.
근거(설명란): 햇볕 받는 몸 1㎡ × 하루 일사량 약 4kWh/㎡ × 효율 약 1% = 0.04kWh ≈ 34kcal ≈ 하루 2,000kcal의 1.7%.
  2,000 / 34 ≈ 58㎡ (교실 하나). 식물 광합성 이론 최대 C3 4.6%·C4 6%(Zhu·Long·Ort 2008, Current Opinion in Biotechnology).
  광합성하는 동물: 바다민달팽이 Elysia chlorotica(Rumpho 외 2008, PNAS).
특수효과: 피부색을 인스턴스 속성(col3)으로 바꿔 초록으로 변신(비 오면 누렇게 시듦) · 빛줄기·알갱이·빗줄기는 발광 상자 인스턴스
  · 거울은 반사 재질 상자 · 두 팔 든 원형은 voxel._person의 팔 블록만 다시 돌린 것.
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
OFF = {"bath": (0, 0), "park": (300, 0), "diner": (600, 0), "office": (900, 0), "subway": (1200, 0),
       "bed": (1500, 0), "class": (1800, 0), "aqua": (2100, 0)}
TX = 7.0            # 반전 컷(에너지 막대)은 공원 잔디 오른쪽 자리에서 — 앞 장면 카메라에 막대가 비치지 않게
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 사람이 광합성을 한다면 어떻게 될까요?", gap=0.7, shot=("park", (0.0, -0.6, 0.6), -90, 3, 6.0, 28, 0.9, 4)),
    dict(say="어느 아침, 거울 속 내 피부가 초록색!", shot=("bath", (-0.1, 1.72, 1.55), -111, 3, 3.25, 34, 0.8, -3)),
    dict(say="점심시간, 식당은 텅 비었어요", shot=("diner", (-0.3, 0.6, 1.1), -80, 6, 6.2, 18, 0.92, 5)),
    dict(say="다들 공원 잔디에 누워 햇볕을 쬐거든요", shot=("park", (0.0, 2.55, 0.3), -90, 40, 6.3, 30, 0.9, 4)),
    dict(say="회사는 책상을 전부 창가로 옮겼죠", shot=("office", (0.0, -1.7, 1.15), -90, 4, 4.4, 18, 0.92, 0)),
    dict(say="지하철에선 햇볕 드는 자리 쟁탈전!", shot=("subway", (0.0, 0.9, 1.1), -88, 5, 4.4, 22, 0.92, 2)),
    dict(say="비 오는 날엔, 다들 시들시들해져요", shot=("office", (0.0, -1.7, 1.15), -90, 3, 4.4, 18, 0.9, 0)),
    dict(say="배고프니까 서로 괜히 예민해지고요", shot=("office", (0.0, -1.4, 1.2), -92, 4, 4.0, 24, 0.9, 0)),
    dict(say="해가 지면 기운이 쭉 빠져서", shot=("park", (0.0, -1.3, 1.1), -90, 5, 3.8, 28, 1.3, 0)),
    dict(say="저녁이면 온 동네가 곯아떨어졌어요", gap=0.7, shot=("bed", (0.0, 2.05, 0.8), -90, 30, 2.5, 28, 0.92, 0)),
    dict(say="그런데 사실, 햇볕으로 얻는 에너지는", shot=("park", (TX - 0.6, 2.4, 0.6), -88, 22, 7.0, 28, 0.9, 3)),
    dict(say="하루에 겨우 35킬로칼로리쯤이에요", shot=("park", (TX - 1.4, 2.4, 0.7), -75, 20, 4.2, 30, 0.9, 0)),
    dict(say="하루 필요 열량의 2%도 안 돼요", shot=("park", (TX - 1.85, 2.3, 0.15), -70, 8, 2.6, 30, 0.88, 0)),
    dict(say="다 채우려면 교실만 한 피부가 필요해요", shot=("class", (0.0, 3.2, 0.7), -90, 22, 9.5, 18, 0.9, 0)),
    dict(say="그래도 진짜 광합성하는 동물이 있어요", shot=("aqua", (0.0, 0.0, 0.12), -90, 10, 2.4, 24, 0.9, 6)),
    dict(say="해조류의 엽록체를 훔친 바다 민달팽이!", gap=0.6, shot=("aqua", (0.0, -0.15, 0.05), -90, 22, 0.9, 30, 0.9, 0)),
    dict(say="결국 사람들은 다시 밥을 먹기 시작했어요", shot=("diner", (0.0, 0.2, 1.1), -80, 6, 6.4, 26, 0.92, 4)),
    dict(say="햇볕보다 따뜻한 건 같이 먹는 밥이었죠", gap=0.7, shot=("diner", (0.4, -0.3, 1.05), -90, 5, 3.3, 30, 0.92, 0)),
    dict(say="오늘 점심은 뭐 먹을 건가요?", shot=("diner", (0.3, -0.2, 1.1), -90, 5, 3.6, 28, 1.6, 0)),
]
TITLE = [("만약에", "white"), ("사람이", "white"), ("광합성을 한다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = 10          # '그런데 사실' 줄

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep21_photosynth" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 0.3 + 2.6 * len(LINES) + 1.6, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep21", "title": "만약에 사람이 광합성을 한다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "F", "mode": "lydian", "bpm": 96, "seed": 211, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.12, "bloom_thr": 1.5, "vignette": 0.16}

SKIN = (0.93, 0.74, 0.58)
GREEN = (0.34, 0.72, 0.26)
WILT = (0.66, 0.64, 0.26)          # 비 오는 날 시든 누런 초록
TIRED = (0.30, 0.58, 0.27)         # 해 질 녘 기운 빠진 짙은 초록
MOOD = {6: (GREEN, WILT, 0.25, 0.85), 7: (WILT, WILT), 8: (GREEN, TIRED, 0.2, 0.9), 9: (TIRED, TIRED)}   # 줄별 모두의 피부색 (처음, 끝, 변하기 시작 u, 끝 u)

# 줄별 하늘·햇빛: (해 세기, 해 색, 해 각도, 환경광 세기, 환경광 색, 하늘 위, 하늘 아래, 별)
LIGHT = {
    "day": (3.0, (1.0, 0.92, 0.8), (50, 0, 35), 0.42, (0.62, 0.68, 0.82), (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0),
    "rain": (0.7, (0.85, 0.9, 1.0), (50, 0, 35), 0.50, (0.55, 0.60, 0.70), (0.30, 0.33, 0.38), (0.58, 0.60, 0.64), 0.0),
    "dusk": (2.4, (1.0, 0.55, 0.28), (80, 0, 25), 0.28, (0.55, 0.45, 0.65), (0.22, 0.20, 0.46), (0.98, 0.60, 0.38), 0.0),
    "night": (0.0, (1.0, 1.0, 1.0), (50, 0, 35), 0.12, (0.35, 0.42, 0.65), (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0),
}
WEATHER = {6: "rain", 7: "rain", 8: "dusk", 9: "night"}

# 해가 비치는 방향(K.sun 기본 각도 50,0,35) → 빛줄기 방향
SUN_DIR = np.array([-0.4388, 0.6268, -0.6428])
SUN_YAW = math.atan2(SUN_DIR[1], SUN_DIR[0])
SUN_PITCH = -math.asin(SUN_DIR[2])
NFX = 160
U = np.random.default_rng(211).random((NFX, 8))


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


def weather(i):
    return LIGHT[WEATHER.get(i, "day")]


def sky(t):
    w = weather(line_at(t))
    return w[5], w[6], w[7]


def skin(tone, i, u):
    """이 줄 진행도 u에서의 피부색. tone={줄: (처음, 끝[, 시작 u, 끝 u])}, 없으면 모두의 기분(MOOD), 없으면 초록."""
    c0, c1, s0, s1 = (*tone.get(i, MOOD.get(i, (GREEN, GREEN))), 0.3, 0.7)[:4]
    w = ramp(u, s0, s1)
    return tuple(p + (q - p) * w for p, q in zip(c0, c1))


# ───────────────────────── 세트 ─────────────────────────
def _shell(v, x0, x1, y0, y1, h, fcol, wcol, fkind="check", tile=0.5, lcol=None, rcol=None, lkind="plain"):
    """바닥 + 뒷벽(+y) + 왼벽 + 오른벽. 앞(-y)은 카메라 쪽이라 터 둠."""
    v.floor(x0, x1, y0, y1, fcol, tile, fkind)
    v.wall((x0, y1), (x1, y1), 0, h, wcol, tile, face=-1)
    v.wall((x0, y0), (x0, y1), 0, h, lcol or wcol, tile, face=-1, kind=lkind)
    v.wall((x1, y0), (x1, y1), 0, h, rcol or wcol, tile, face=1)


def _gauge(v, gx, gy, fill, col):
    """에너지 막대(배터리): 높이 1.6m, fill=채운 비율. 앞(-y)에서 보임."""
    H = 1.6
    v.box(gx - 0.28, gx + 0.28, gy - 0.12, gy + 0.12, 0, H + 0.2, (0.22, 0.24, 0.28))
    v.box(gx - 0.1, gx + 0.1, gy - 0.06, gy + 0.06, H + 0.2, H + 0.3, (0.22, 0.24, 0.28))
    v.box(gx - 0.21, gx + 0.21, gy - 0.125, gy - 0.12, 0.1, H + 0.1, (0.05, 0.06, 0.08), jit=0)
    for k in range(1, 10):
        z = 0.12 + (H - 0.04) * k / 10
        v.box(gx + 0.21, gx + 0.27, gy - 0.13, gy - 0.12, z - 0.007, z + 0.007, (0.9, 0.9, 0.9), jit=0)
    v.box(gx - 0.19, gx + 0.19, gy - 0.13, gy - 0.125, 0.12, 0.12 + (H - 0.04) * fill, col, jit=0, glow=True)
    v.box(gx - 0.05, gx + 0.05, gy - 0.075, gy - 0.06, H + 0.22, H + 0.28, col, jit=0, glow=True)           # 상태 등


def _meal(v, cx, cy):
    """상 하나: 밥 둘 + 뚝배기 찌개 + 반찬 둘."""
    for dx in (-0.42, 0.42):
        v.box(cx + dx - 0.07, cx + dx + 0.07, cy - 0.17, cy - 0.03, 0.74, 0.8, (0.97, 0.97, 0.95), jit=0.01)
        v.box(cx + dx - 0.055, cx + dx + 0.055, cy - 0.155, cy - 0.045, 0.8, 0.83, (0.99, 0.98, 0.93), jit=0.01)
    v.box(cx - 0.12, cx + 0.12, cy - 0.1, cy + 0.14, 0.74, 0.84, (0.22, 0.2, 0.2))
    v.box(cx - 0.1, cx + 0.1, cy - 0.08, cy + 0.12, 0.84, 0.86, (0.85, 0.25, 0.12), jit=0.06)
    for dx, c in ((-0.2, (0.3, 0.6, 0.25)), (0.2, (0.95, 0.55, 0.2))):
        v.box(cx + dx - 0.05, cx + dx + 0.05, cy + 0.12, cy + 0.22, 0.74, 0.78, (0.96, 0.96, 0.94))
        v.box(cx + dx - 0.04, cx + dx + 0.04, cy + 0.13, cy + 0.21, 0.78, 0.8, c, jit=0.08)


def _bath(v):
    _shell(v, -2.0, 2.0, -1.75, 1.75, 2.6, (0.78, 0.86, 0.90), (0.90, 0.94, 0.96), "check", 0.25, rcol=(0.84, 0.90, 0.93))
    v.box(-1.3, 0.5, 1.15, 1.74, 0, 0.86, (0.95, 0.95, 0.93))                        # 세면대 장
    v.box(-1.35, 0.55, 1.1, 1.74, 0.86, 0.9, (0.9, 0.92, 0.95))
    v.box(-0.8, 0.0, 1.25, 1.65, 0.9, 0.93, (0.72, 0.82, 0.9), jit=0.02)             # 대야
    v.box(-0.42, -0.38, 1.58, 1.62, 0.93, 1.1, (0.82, 0.84, 0.87), jit=0)            # 수도꼭지
    v.box(-0.42, -0.38, 1.46, 1.62, 1.08, 1.12, (0.82, 0.84, 0.87), jit=0)
    v.box(0.2, 0.32, 1.45, 1.57, 0.9, 1.0, (0.95, 0.6, 0.7))                          # 컵 + 칫솔
    v.box(0.23, 0.245, 1.5, 1.52, 1.0, 1.2, (0.3, 0.6, 0.9), jit=0)
    v.box(0.27, 0.285, 1.5, 1.52, 1.0, 1.18, (0.95, 0.85, 0.3), jit=0)
    v.box(-1.38, 0.58, 1.72, 1.75, 1.07, 2.13, (0.93, 0.9, 0.84))                     # 거울 틀 (거울 자체는 build에서)
    v.box(-1.0, 0.2, 1.68, 1.74, 2.2, 2.26, (1.0, 0.97, 0.9), jit=0, glow=True)       # 거울 위 조명
    v.box(1.35, 2.0, -1.5, 1.05, 0, 0.55, (0.96, 0.97, 0.98))                       # 욕조
    v.box(1.4, 1.95, -1.45, 1.0, 0.5, 0.53, (0.5, 0.78, 0.92), jit=0.03)
    v.box(-0.6, 0.8, 0.2, 0.8, 0.0, 0.02, (0.9, 0.72, 0.55))                          # 발매트
    v.box(-1.96, -1.9, 0.9, 1.6, 1.3, 1.34, (0.7, 0.7, 0.72), jit=0)                 # 수건걸이 + 수건
    v.box(-1.9, -1.84, 1.0, 1.5, 0.7, 1.3, (0.95, 0.8, 0.5))
    v.window(-0.6, 0.6, -1.99, 1.35, 2.25, night=False, face=1, axis="x")
    v.light(-0.5, 1.45, 2.2, 120, (1.0, 0.96, 0.88), 0.5)
    v.light(-0.6, 1.45, 1.2, 35, (1.0, 0.95, 0.85), 0.3)
    v.light(-0.1, 1.5, 1.7, 1.0, (0.5, 1.0, 0.4), 0.2, "ep21_flash")                # 변신 순간 초록 번쩍 (upd에서 세기 조절)


MATS = [(-0.8, (0.95, 0.5, 0.55)), (0.0, (0.98, 0.85, 0.35)), (0.8, (0.45, 0.68, 0.92))]
BG_LIE = [(-4.2, 6.0, (0.95, 0.6, 0.3)), (-2.4, 8.2, (0.5, 0.75, 0.95)), (3.2, 6.8, (0.95, 0.5, 0.6)),
          (5.4, 9.2, (0.98, 0.88, 0.4)), (-6.8, 4.6, (0.6, 0.85, 0.6)), (7.8, 5.2, (0.9, 0.9, 0.95))]


def _park(v):
    from engine import voxel as X
    rs = v.rs
    v.floor(-16, 16, -9, 1, (0.80, 0.76, 0.68), 0.5, "check")                        # 돌바닥 광장
    v.floor(-16, 16, 1, 13, (0.40, 0.58, 0.24), 0.5)                                 # 잔디
    for x, c in MATS:                                                                 # 돗자리 (주인공 셋) + 반전 컷 자리
        v.box(x - 0.37, x + 0.37, 1.15, 3.25, 0, 0.03, c, jit=0.03)
        v.box(x + TX - 0.37, x + TX + 0.37, 1.15, 3.25, 0, 0.03, c, jit=0.03)
    for x, yc, c in BG_LIE:                                                           # 먼 돗자리
        v.box(x - 0.38, x + 0.38, yc - 1.05, yc + 1.05, 0, 0.03, c, jit=0.03)
    for x, y, h in ((-7.0, 7.5, 4.2), (-3.2, 10.0, 3.6), (4.8, 9.5, 4.0), (9.5, 6.5, 3.4), (-11.0, 6.0, 3.8),
                    (12.5, 10.5, 4.4), (-14.0, 11.0, 4.0)):
        X.tree(v, x, y, h)
    v.box(-16, 16, 12, 13, 0, 0.9, (0.2, 0.45, 0.2), jit=0.08)                       # 울타리 덤불
    for x in range(-36, 38, 6):                                                       # 먼 건물
        w = float(rs.uniform(4.0, 6.0))
        v.box(x, x + w, 17, 22, 0, float(rs.uniform(7, 18)), (0.62, 0.68, 0.76), jit=0.04)
    for x in (-9.0, 12.0):
        X.street_lamp(v, x, 0.5, h=3.4, energy=1.0)
    v.box(-4.6, -3.2, 0.2, 0.6, 0.42, 0.47, (0.55, 0.38, 0.25))                       # 벤치
    v.box(-4.6, -3.2, 0.55, 0.6, 0.47, 0.85, (0.55, 0.38, 0.25))
    for x in (-4.5, -3.3):
        v.box(x - 0.03, x + 0.03, 0.25, 0.55, 0, 0.42, (0.3, 0.3, 0.32), jit=0)
    _gauge(v, TX - 1.85, 2.5, 0.02, (1.0, 0.3, 0.1))                                      # 에너지 막대: 2%


def _diner(v):
    from engine import voxel as X
    _shell(v, -3.5, 3.5, -3, 3, 2.9, (0.82, 0.72, 0.58), (0.93, 0.88, 0.78), "check", 0.5,
           lcol=(0.72, 0.44, 0.34), lkind="brick")
    v.window(1.4, 3.0, 2.99, 0.9, 2.3, night=False)
    v.box(-3.0, -0.6, 2.97, 2.99, 1.7, 2.5, (0.16, 0.16, 0.17))                       # 메뉴판
    for k in range(4):
        v.box(-2.85, -2.85 + 0.6 + 0.25 * (k % 2), 2.96, 2.97, 2.3 - k * 0.17, 2.34 - k * 0.17,
              (0.95, 0.9, 0.75), jit=0, glow=True)
    v.box(-3.2, -0.5, 1.9, 2.5, 0, 1.0, (0.45, 0.3, 0.2))                              # 카운터
    v.box(-3.25, -0.45, 1.85, 2.55, 1.0, 1.05, (0.92, 0.9, 0.86))
    v.box(-2.4, -1.8, 2.05, 2.4, 1.05, 1.35, (0.35, 0.35, 0.38))                       # 찌개 솥
    v.box(-2.35, -1.85, 2.1, 2.35, 1.33, 1.36, (0.8, 0.2, 0.1), jit=0.05)
    tables = ((-1.8, -0.9, 1.5), (0.4, -0.9, 1.6), (2.2, -0.9, 1.5), (-1.0, 0.95, 1.5), (1.4, 0.95, 1.5))
    for cx, cy, sx in tables:
        X.table(v, cx, cy, sx, 0.8, 0.74, (0.7, 0.52, 0.34))
        for dx in (-0.35, 0.35):
            X.chair(v, cx + dx, cy + 0.62, -90)
        _meal(v, cx, cy)
    for cx, cy, _ in tables[:3]:
        v.box(cx - 0.03, cx + 0.03, cy - 0.03, cy + 0.03, 2.2, 2.9, (0.2, 0.2, 0.2), jit=0)   # 펜던트 등
        v.box(cx - 0.15, cx + 0.15, cy - 0.15, cy + 0.15, 2.05, 2.2, (1.0, 0.82, 0.55), jit=0, glow=True)
        v.light(cx, cy, 1.95, 70, (1.0, 0.82, 0.55), 0.3)
    v.box(-3.3, -2.8, -2.8, -2.3, 0, 0.5, (0.35, 0.6, 0.45))                           # 화분
    v.box(-3.35, -2.75, -2.85, -2.25, 0.5, 1.4, (0.25, 0.55, 0.25), jit=0.1)


def _office(v):
    from engine import voxel as X
    _shell(v, -4.5, 4.5, -3, 3, 3.0, (0.55, 0.57, 0.6), (0.85, 0.86, 0.88), "check", 0.5, lcol=(0.82, 0.84, 0.86))
    v.box(-4.5, 4.5, -3.05, -2.95, 2.9, 3.0, (0.9, 0.9, 0.92))                        # 창틀 윗보 (앞은 터 둔 창)
    for k in range(5):                                                                 # 말아 올린 블라인드
        v.box(-4.5, 4.5, -3.0, -2.97, 2.45 + 0.08 * k, 2.49 + 0.08 * k, (0.9, 0.92, 0.95))
    for x in (-4.5, 4.5):
        v.box(x - 0.04, x + 0.04, -3.05, -2.95, 0, 3.0, (0.9, 0.9, 0.92))
    for cx in (-1.35, -0.45, 0.45, 1.35):
        X.table(v, cx, -2.3, 0.86, 0.7, 0.74, (0.92, 0.92, 0.9))                        # 창가 책상 (다닥다닥)
        X.chair(v, cx, -1.55, -90, (0.2, 0.22, 0.26))
        v.box(cx - 0.2, cx + 0.2, -2.35, -2.0, 0.74, 0.76, (0.55, 0.57, 0.6))            # 노트북
        v.box(cx - 0.2, cx + 0.2, -2.4, -2.37, 0.76, 1.0, (0.1, 0.1, 0.12))
        v.box(cx + 0.28, cx + 0.37, -2.25, -2.15, 0.74, 0.84, (0.97, 0.97, 0.95))        # 머그컵
    X.table(v, 0.0, 1.9, 2.0, 0.9, 0.74, (0.4, 0.28, 0.2))                              # 혼자 남은 부장 책상
    X.chair(v, 0.0, 2.5, -90, (0.2, 0.22, 0.26))
    v.box(-3.0, -0.5, 2.97, 2.99, 1.2, 2.4, (0.95, 0.95, 0.97))                        # 화이트보드
    for k, c in enumerate(((0.9, 0.3, 0.3), (0.3, 0.45, 0.85), (0.3, 0.7, 0.4))):
        v.box(-2.8, -1.4 - 0.3 * k, 2.96, 2.97, 2.05 - 0.2 * k, 2.1 - 0.2 * k, c, jit=0)
    v.box(3.3, 3.8, 2.3, 2.8, 0, 0.5, (0.35, 0.6, 0.45))                                # 화분
    v.box(3.25, 3.85, 2.25, 2.85, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.5, 0.5, 3.0):
        v.light(x, 0.2, 2.6, 110, (0.95, 0.97, 1.0), 0.6)
    for x in (-1.6, 1.6):
        v.light(x, -1.6, 2.7, 120, (0.95, 0.97, 1.0), 0.6)                                # 창가 얼굴 비추는 불


def _subway(v):
    _shell(v, -4.5, 4.5, -1.5, 1.5, 2.25, (0.50, 0.52, 0.57), (0.86, 0.88, 0.90), "check", 0.5, lcol=(0.8, 0.82, 0.85))
    for x0, x1 in ((-4.1, -2.5), (-1.6, 1.6), (2.5, 4.1)):
        v.window(x0, x1, 1.49, 0.85, 1.85, night=False)
    v.box(-4.4, 4.4, 0.95, 1.45, 0.38, 0.46, (0.95, 0.62, 0.2))                         # 긴 의자
    v.box(-4.4, 4.4, 1.38, 1.46, 0.46, 0.85, (0.88, 0.55, 0.18))
    v.box(-4.4, 4.4, 1.0, 1.45, 0, 0.38, (0.3, 0.3, 0.34))
    for x in (-2.4, 2.4):                                                              # 기둥
        v.box(x - 0.025, x + 0.025, 0.35, 0.4, 0, 2.25, (0.82, 0.84, 0.88), jit=0.02)
    v.box(-4.2, 4.2, 0.55, 0.6, 2.05, 2.1, (0.8, 0.82, 0.86), jit=0.02)                 # 손잡이 봉
    for x in np.arange(-3.6, 3.7, 0.9):
        v.box(x - 0.09, x + 0.09, 0.555, 0.585, 1.78, 2.05, (0.95, 0.9, 0.4), jit=0.05)
    for x, c in ((-3.3, (0.3, 0.6, 0.9)), (-0.8, (0.9, 0.4, 0.4)), (0.8, (0.4, 0.75, 0.5)), (3.3, (0.95, 0.75, 0.3))):
        v.box(x - 0.4, x + 0.4, 1.47, 1.49, 1.95, 2.18, c, jit=0)                       # 광고 포스터
    v.box(-4.0, 4.0, -0.1, 0.1, 2.2, 2.25, (1.0, 1.0, 0.95), jit=0, glow=True)
    for x in (-2.6, 0.0, 2.6):
        v.light(x, 0.3, 2.0, 90, (1.0, 0.98, 0.92), 0.5)


def _bed(v):
    from engine import voxel as X
    _shell(v, -3, 3, -2.5, 2.5, 2.6, (0.55, 0.4, 0.28), (0.42, 0.46, 0.6), "wood", 0.5)
    v.box(-0.8, 0.8, 0.3, 2.45, 0, 0.34, X.WOOD)                                       # 침대
    v.box(-0.76, 0.76, 0.34, 2.41, 0.34, 0.52, X.WHITE, jit=0.02)
    v.box(-0.8, 0.8, 2.39, 2.45, 0, 1.0, X.DARKWOOD)
    v.box(-0.4, 0.4, 2.0, 2.35, 0.52, 0.64, (0.97, 0.97, 0.97), jit=0.01)               # 베개
    v.box(-0.76, 0.76, 0.34, 1.7, 0.52, 0.98, (0.35, 0.5, 0.82))                        # 이불 (가슴까지)
    v.box(-1.4, -0.9, 2.0, 2.4, 0, 0.5, X.WOOD)                                          # 협탁 + 스탠드 + 알람시계
    v.box(-1.25, -1.05, 2.1, 2.3, 0.5, 0.7, (1.0, 0.8, 0.5), glow=True)
    v.box(-1.3, -1.0, 2.0, 2.09, 0.5, 0.58, (0.1, 0.1, 0.12))
    v.box(-1.28, -1.02, 1.99, 2.0, 0.52, 0.56, (1.0, 0.2, 0.15), jit=0, glow=True)
    v.window(-0.7, 0.7, 2.49, 1.35, 2.25, night=True, lights=14)                         # 머리맡 창 + 달
    v.box(0.15, 0.45, 2.45, 2.48, 1.7, 2.0, (1.0, 0.98, 0.8), jit=0, glow=True)
    v.box(-2.9, -2.4, -2.3, -1.6, 0, 0.5, (0.35, 0.6, 0.45))                            # 화분
    v.box(-2.95, -2.35, -2.35, -1.55, 0.5, 1.2, (0.25, 0.55, 0.25), jit=0.1)
    v.light(-1.15, 2.2, 0.85, 70, (1.0, 0.78, 0.5), 0.2)
    v.light(0.0, 1.9, 1.9, 40, (0.55, 0.65, 1.0), 0.6)
    v.light(0.0, 0.8, 2.2, 45, (0.6, 0.7, 1.0), 0.8)


def _class(v):
    from engine import voxel as X
    v.floor(-3, 3, -2, 8, GREEN, 0.5)                                                   # 바닥 전부 = 초록 피부 (6×10 = 60㎡)
    v.box(-0.06, 0.06, -2, 8, 0.0, 0.015, (0.2, 0.5, 0.15), jit=0)                       # 잎맥
    for y in np.arange(-1.5, 8.0, 1.0):
        v.box(0.06, 2.4, y - 0.04, y + 0.04, 0.0, 0.012, (0.2, 0.5, 0.15), jit=0)
        v.box(-2.4, -0.06, y - 0.04, y + 0.04, 0.0, 0.012, (0.2, 0.5, 0.15), jit=0)
    v.wall((-3, 8), (3, 8), 0, 3.0, (0.92, 0.92, 0.88), 0.5, face=-1)
    v.wall((-3, -2), (-3, 8), 0, 3.0, (0.88, 0.9, 0.86), 0.5, face=-1)
    v.wall((3, -2), (3, 8), 0, 3.0, (0.88, 0.9, 0.86), 0.5, face=1)
    for y0 in (0.2, 3.4):
        v.window(y0, y0 + 2.4, -2.99, 0.9, 2.4, night=False, face=1, axis="x")
    v.box(-2.0, 1.5, 7.96, 7.99, 0.9, 2.2, (0.10, 0.28, 0.20))                          # 칠판
    v.box(-2.1, 1.6, 7.95, 7.98, 0.8, 0.9, (0.6, 0.45, 0.3))
    for x0, x1, z0, z1 in ((-1.8, -1.4, 1.3, 1.7), (-0.8, 1.2, 1.0, 2.0)):             # 분필 그림: 작은 네모 → 큰 네모
        for a0, a1, b0, b1 in ((x0, x1, z0, z0 + 0.03), (x0, x1, z1 - 0.03, z1), (x0, x0 + 0.03, z0, z1), (x1 - 0.03, x1, z0, z1)):
            v.box(a0, a1, 7.93, 7.95, b0, b1, (0.92, 0.95, 0.92), jit=0)
    v.box(-1.3, -0.9, 7.93, 7.95, 1.48, 1.52, (0.92, 0.95, 0.92), jit=0)
    for k in range(6):                                                                   # 한쪽에 밀어 둔 책걸상
        y = -0.8 + 1.2 * k
        X.table(v, 2.6, y, 0.5, 0.6, 0.72, (0.7, 0.55, 0.35))
        X.chair(v, 2.1, y, 0)
    for y in (0.0, 3.5, 7.0):
        v.light(0.0, y, 2.8, 130, (0.95, 0.97, 1.0), 0.6)
    _gauge(v, -1.9, 1.8, 1.0, (0.4, 1.0, 0.3))                                           # 에너지 막대: 가득


def _aqua(v):
    rs = v.rs
    v.floor(-1.2, 1.2, -3.5, 0.8, (0.86, 0.78, 0.60), 0.1)                             # 모래 (카메라 쪽으로 길게)
    bands = [(0.02, 0.12, 0.28), (0.03, 0.18, 0.38), (0.05, 0.26, 0.48), (0.07, 0.34, 0.56), (0.10, 0.42, 0.62)]
    for k, c in enumerate(bands):                                                        # 물빛 뒷판·옆판 (위로 갈수록 밝게)
        z0 = k * 0.3
        v.box(-1.2, 1.2, 0.8, 0.85, z0, z0 + 0.3, c, jit=0, glow=True)
        v.box(-1.25, -1.2, -0.8, 0.8, z0, z0 + 0.3, c, jit=0, glow=True)
        v.box(1.2, 1.25, -0.8, 0.8, z0, z0 + 0.3, c, jit=0, glow=True)
    for x, y, n in ((-0.95, 0.5, 5), (-0.55, 0.6, 4), (0.7, 0.55, 5), (1.0, 0.3, 4), (0.2, 0.65, 3), (-1.0, -0.1, 4)):
        for j in range(n):                                                               # 해초
            xx, yy = x + float(rs.uniform(-0.12, 0.12)), y + float(rs.uniform(-0.1, 0.1))
            h = float(rs.uniform(0.5, 1.0))
            c = ((0.18, 0.45, 0.18), (0.25, 0.55, 0.2), (0.3, 0.5, 0.15))[j % 3]
            v.box(xx - 0.015, xx + 0.015, yy - 0.012, yy + 0.012, 0.0, h, c)
            for z in np.arange(0.2, h, 0.17):
                s = 1 if int(z * 10) % 2 else -1
                v.box(min(xx, xx + s * 0.08), max(xx, xx + s * 0.08), yy - 0.01, yy + 0.01, float(z), float(z) + 0.04,
                      (c[0] * 1.2, min(1.0, c[1] * 1.2), c[2] * 1.2))
    for x0, x1, y0, y1, h in ((-0.6, -0.25, 0.15, 0.4, 0.14), (0.35, 0.75, -0.1, 0.2, 0.2), (0.8, 1.0, -0.5, -0.3, 0.1)):
        v.box(x0, x1, y0, y1, 0, h, (0.45, 0.43, 0.42), jit=0.06)                        # 바위
    # 바다민달팽이 (머리가 -y, 카메라 쪽): 잎처럼 납작하고 옆 주름, 눈에 도둑 마스크
    g = (0.36, 0.72, 0.24)
    v.box(-0.07, 0.07, -0.2, 0.3, 0.0, 0.025, (0.3, 0.62, 0.22))
    v.box(-0.1, 0.1, -0.15, 0.3, 0.025, 0.06, g)
    for s in (-1, 1):
        v.box(min(0.1 * s, 0.17 * s), max(0.1 * s, 0.17 * s), -0.12, 0.28, 0.04, 0.075, (0.42, 0.78, 0.28))
        for k in range(6):
            y = -0.1 + 0.07 * k
            v.box(min(0.15 * s, 0.19 * s), max(0.15 * s, 0.19 * s), y, y + 0.045, 0.045, 0.085, (0.5, 0.82, 0.32), jit=0.06)
    v.box(-0.015, 0.015, -0.12, 0.28, 0.06, 0.07, (0.22, 0.5, 0.16))                    # 등줄기
    for k in range(8):
        y = -0.1 + 0.05 * k
        v.box(-0.09, 0.09, y, y + 0.012, 0.06, 0.066, (0.24, 0.52, 0.18), jit=0.03)
    for k in range(9):                                                                    # 붉은 점
        x, y = float(rs.uniform(-0.15, 0.13)), float(rs.uniform(-0.1, 0.26))
        v.box(x, x + 0.02, y, y + 0.02, 0.075, 0.082, (0.95, 0.45, 0.2), jit=0.05)
    v.box(-0.06, 0.06, -0.27, -0.15, 0.0, 0.055, (0.38, 0.74, 0.25))                    # 머리
    for s in (-1, 1):
        v.box(min(0.035 * s, 0.05 * s), max(0.035 * s, 0.05 * s), -0.2, -0.185, 0.055, 0.11, (0.3, 0.65, 0.2))   # 더듬이
    v.box(-0.075, 0.075, -0.283, -0.268, 0.038, 0.07, (0.03, 0.03, 0.04), jit=0)         # 도둑 마스크
    for s in (-1, 1):
        v.box(min(0.03 * s, 0.05 * s), max(0.03 * s, 0.05 * s), -0.288, -0.283, 0.047, 0.063, (1.0, 1.0, 1.0), jit=0)
    v.light(0.0, -0.4, 0.9, 25, (0.6, 0.85, 1.0), 0.3)
    v.light(0.0, 0.3, 0.7, 15, (0.5, 1.0, 0.8), 0.2)


# ───────────────────────── 캐릭터 배치 ─────────────────────────
A_SH, A_PA = (0.95, 0.55, 0.25), (0.15, 0.18, 0.30)         # 주인공: 주황 셔츠, 짧은 머리
B_SH, B_PA = (0.25, 0.45, 0.80), (0.20, 0.20, 0.22)         # 친구: 파란 셔츠, 긴 머리


def P(st, x, y, yaw, pose, z=0.0, **kw):
    return dict(set=st, x=x, y=y, yaw=yaw, pose=pose, z=z, **kw)


def cast():
    """[dict(set, x, y, yaw, pose, z, hair, shirt, pants, scale, over={줄: 그 줄의 자리·자세}, tone={줄: 피부색 변화})]
    over에 든 줄에서만 보임. move=(vx, vy)가 있으면 그 줄 동안 걸어감."""
    from engine import voxel as X
    rs = np.random.default_rng(21)
    S, Pn = [c for c in X.SHIRTS if c not in (A_SH, B_SH, X.SHIRTS[3])], X.PANTS     # 조연은 주인공 색·초록 셔츠 빼고
    C = []

    def add(plan, hair=0, shirt=None, pants=None, tone=None):
        C.append(dict(plan[min(plan)], hair=hair, shirt=shirt or S[int(rs.integers(len(S)))],
                      pants=pants or Pn[int(rs.integers(len(Pn)))], scale=1.0, over=plan, tone=tone or {}))

    def same(lines, p):
        return {k: p for k in lines}
    LIE = dict(z=-0.03)
    # 주인공 A (주황 셔츠)
    lieA, lieA2 = P("park", 0.0, 1.35, -90, "lie", **LIE), P("park", TX, 1.35, -90, "lie", **LIE)
    add({0: P("park", 0.0, -1.2, -90, "up"), 1: P("bath", 0.1, 0.95, 90, "confused"), 3: lieA,
         4: P("office", 0.45, -1.55, -90, "sit"), 5: P("subway", 0.0, 1.12, -90, "sit"),
         6: P("office", 0.45, -1.55, -90, "sit"), 7: P("office", 0.45, -1.55, -115, "sit"),
         8: P("park", -0.45, 1.2, -90, "walk_a", move=(0.0, -0.55)), 9: P("bed", 0.0, 0.45, -90, "lie", 0.49),
         10: lieA2, 11: lieA2, 12: lieA2, 13: P("class", 0.0, 3.2, -90, "up"),
         **same((16, 17, 18), P("diner", 0.75, -0.28, -90, "sit"))},
        0, A_SH, A_PA, tone={1: (SKIN, GREEN, 0.3, 0.7)})
    # 친구 B (파란 셔츠, 긴 머리)
    lieB, lieB2 = P("park", -0.8, 1.35, -90, "lie", **LIE), P("park", TX - 0.8, 1.35, -90, "lie", **LIE)
    add({0: P("park", -0.85, -0.55, -90, "up"), 3: lieB, 4: P("office", -0.45, -1.55, -90, "sit"),
         5: P("subway", -0.7, 0.45, -60, "angry"), 6: P("office", -0.45, -1.55, -90, "sit"),
         7: P("office", -0.5, -0.9, -55, "angry"), 8: P("park", 0.45, 1.5, -90, "walk_a", move=(0.0, -0.55)),
         10: lieB2, 11: lieB2, 12: lieB2, **same((16, 17, 18), P("diner", 0.05, -0.28, -90, "sit"))},
        1, B_SH, B_PA)
    # 공원: 두 팔 든 훅 + 누운 사람들(셋째 · 먼 잔디)
    for x, y, h in ((0.85, -0.55, 0), (-1.5, 0.2, 1), (1.5, 0.2, 0)):
        add({0: P("park", x, y, -90, "up")}, h)
    add({3: P("park", 0.8, 1.35, -90, "lie", **LIE), **same((10, 11, 12), P("park", TX + 0.8, 1.35, -90, "lie", **LIE))}, 0)
    for k, (x, yc, _) in enumerate(BG_LIE):
        add(same((0, 3, 10, 11, 12), P("park", x, yc - 0.95, -90, "lie", **LIE)), k % 2)
    # 식당 주인
    add({2: P("diner", -1.3, 2.75, -90, "confused"), 16: P("diner", -1.3, 2.75, -90, "talk"),
         17: P("diner", -1.3, 2.75, -90, "talk"), 18: P("diner", -1.3, 2.75, -90, "stand")},
        1, (0.92, 0.92, 0.90), (0.3, 0.3, 0.34))
    # 식당 손님들
    for x, y in ((-2.15, -0.28), (-1.45, -0.28), (1.85, -0.28), (2.55, -0.28), (-1.35, 1.57), (-0.65, 1.57),
                 (1.05, 1.57), (1.75, 1.57)):
        add(same((16, 17, 18), P("diner", x, y, -90, "sit")), int(rs.random() < 0.5))
    # 회사: 나머지 직원 둘 + 부장
    for x in (-1.35, 1.35):
        add(same((4, 6, 7), P("office", x, -1.55, -90, "sit")), int(rs.random() < 0.5))
    add({4: P("office", 0.0, 2.3, -90, "talk")}, 0, (0.2, 0.22, 0.3), (0.12, 0.12, 0.15))
    # 지하철: 앉은 사람 둘 + 자리다툼 한 명
    add({5: P("subway", -1.25, 1.12, -90, "sit")}, 0)
    add({5: P("subway", 1.25, 1.12, -90, "sit")}, 1)
    add({5: P("subway", 0.7, 0.45, -120, "angry")}, 1)
    return C


def pose_id(hair, pose):
    from engine import voxel as X
    return 2 * X.NPOSE + hair if pose == "up" else hair * X.NPOSE + X.POSES[pose]


def _arms_up(lh):
    """두 팔을 번쩍 든 원형: STAND 자세 블록에서 팔(맨 끝 4덩이)만 어깨 축으로 다시 돌림."""
    from engine import voxel as X
    parts = X._person(X.STAND, lh)
    for bm, _ in parts[-4:]:
        X._rot_y(bm, -3.0, (0, 0, 0.78 + 0.54))
    return parts


# ───────────────────────── 특수효과 (발광 상자 인스턴스) ─────────────────────────
def _fx_sun(t, u, n, c, r, z):
    """해 방향으로 날아와 몸에 닿으며 사라지는 빛줄기."""
    k = U[:n]
    ph = (k[:, 0] + t * (0.55 + 0.35 * k[:, 1])) % 1.0
    tgt = np.stack([c[0] + (k[:, 2] * 2 - 1) * r[0], c[1] + (k[:, 3] * 2 - 1) * r[1], z[0] + k[:, 4] * (z[1] - z[0])], 1)
    pos = tgt - SUN_DIR * (2.4 * (1 - ph))[:, None]
    f = np.sin(np.pi * ph) ** 0.6
    size = np.stack([0.55 * f, np.full(n, 0.014), np.full(n, 0.014)], 1)
    return pos, size, np.tile((0.0, SUN_PITCH, SUN_YAW), (n, 1)), np.tile((0.55, 0.5, 0.28), (n, 1))


def _fx_rise(t, u, n, c, r, z, col, size, spd, gate=None):
    """위로 떠오르며 깜빡이는 알갱이 (변신 번쩍·잎 반짝·물방울·잠꼬대)."""
    k = U[:n]
    ph = (k[:, 0] + t * spd * (0.6 + 0.8 * k[:, 1])) % 1.0
    pos = np.stack([c[0] + (k[:, 2] * 2 - 1) * r[0] + 0.04 * np.sin(6.28 * (0.6 * t + k[:, 5])),
                    c[1] + (k[:, 3] * 2 - 1) * r[1], z[0] + ph * (z[1] - z[0])], 1)
    s = size * (0.45 + 0.55 * k[:, 4]) * np.sin(np.pi * ph) * (ramp(u, *gate) if gate else 1.0)
    return pos, np.stack([s, s, s], 1), np.zeros((n, 3)), np.tile(col, (n, 1))


def _fx_rain(t, u, n, x, y, z):
    """창밖(카메라 쪽)에서 떨어지는 빗줄기."""
    k = U[:n]
    ph = (k[:, 0] - t * (1.8 + 0.8 * k[:, 1])) % 1.0
    zz = z[0] + ph * (z[1] - z[0])
    pos = np.stack([x[0] + k[:, 2] * (x[1] - x[0]) + 0.12 * (zz - z[0]), y[0] + k[:, 3] * (y[1] - y[0]), zz], 1)
    size = np.stack([np.full(n, 0.012), np.full(n, 0.012), 0.5 + 0.4 * k[:, 4]], 1)
    return pos, size, np.tile((0.0, 0.12, 0.0), (n, 1)), np.tile((0.2, 0.25, 0.34), (n, 1))


def _fx_steal(t, u, n, srcs, dst):
    """해초에서 달팽이 등으로 옮겨 가는(훔치는) 초록 엽록체 알갱이."""
    k = U[:n]
    s = (k[:, 0] + t * 0.55) % 1.0
    src = np.array(srcs)[(k[:, 6] * len(srcs)).astype(int)]
    a = src + np.stack([(k[:, 2] * 2 - 1) * 0.1, (k[:, 3] * 2 - 1) * 0.05, k[:, 4] * 0.3], 1)
    b = np.array(dst) + np.stack([(k[:, 5] * 2 - 1) * 0.07, (k[:, 7] * 2 - 1) * 0.15, np.zeros(n)], 1)
    pos = a + (b - a) * s[:, None] + np.array([0.0, 0.0, 0.18]) * np.sin(np.pi * s)[:, None]
    q = 0.03 * np.sin(np.pi * s) ** 0.5
    return pos, np.stack([q, q, q], 1), np.zeros((n, 3)), np.tile((0.45, 1.0, 0.3), (n, 1))


SUN_LIE = ("sun", "park", dict(n=40, c=(0.0, 2.3), r=(1.4, 0.9), z=(0.15, 0.55)))
SUN_LIE2 = ("sun", "park", dict(n=40, c=(TX, 2.3), r=(1.4, 0.9), z=(0.15, 0.55)))
FX = {
    0: ("sun", "park", dict(n=44, c=(0.0, -0.6), r=(1.9, 0.8), z=(0.2, 2.0))),
    1: ("rise", "bath", dict(n=30, c=(0.1, 1.05), r=(0.5, 0.3), z=(1.0, 2.1), col=(0.55, 1.0, 0.4), size=0.05, spd=0.4,
                              gate=(0.28, 0.5))),
    3: SUN_LIE, 10: SUN_LIE2, 11: SUN_LIE2, 12: SUN_LIE2,
    4: ("sun", "office", dict(n=36, c=(0.0, -1.6), r=(1.6, 0.3), z=(0.6, 1.8))),
    5: ("sun", "subway", dict(n=30, c=(0.0, 1.0), r=(0.7, 0.2), z=(0.6, 1.6))),
    6: ("rain", "office", dict(n=110, x=(-3.0, 3.0), y=(-4.6, -3.2), z=(0.0, 3.6))),
    7: ("rain", "office", dict(n=110, x=(-3.0, 3.0), y=(-4.2, -3.2), z=(0.0, 3.6))),
    9: ("rise", "bed", dict(n=5, c=(0.0, 2.0), r=(0.25, 0.15), z=(0.9, 1.8), col=(0.9, 0.92, 1.0), size=0.08, spd=0.18)),
    13: ("rise", "class", dict(n=70, c=(0.0, 3.0), r=(2.6, 5.0), z=(0.05, 1.4), col=(0.6, 1.0, 0.4), size=0.07, spd=0.3)),
    14: ("rise", "aqua", dict(n=14, c=(0.0, 0.0), r=(0.9, 0.4), z=(0.0, 1.3), col=(0.6, 0.9, 1.0), size=0.045, spd=0.25)),
    15: ("steal", "aqua", dict(n=14, srcs=[(-0.7, 0.45, 0.2), (0.75, 0.4, 0.2)], dst=(0.0, 0.05, 0.085))),
}
FXFN = {"sun": _fx_sun, "rise": _fx_rise, "rain": _fx_rain, "steal": _fx_steal}


def fx_state(i, t, u):
    """줄 i의 효과 알갱이 → (위치, 크기, 회전, 색) 각 NFX개 (안 쓰는 칸은 크기 0)."""
    pos, size, rot, col = (np.zeros((NFX, 3), np.float32) for _ in range(4))
    spec = FX.get(i)
    if spec:
        kind, st, kw = spec
        p, s, r, c = FXFN[kind](t, u, **kw)
        n = len(p)
        pos[:n] = np.asarray(p) + (*OFF[st], 0.0)
        size[:n], rot[:n], col[:n] = s, r, c
    return pos, size, rot, col


def build(ctx):
    from engine import bkit as K
    from engine import home as H
    from engine import voxel as X
    v = X.Vox(21)
    for name, fn in (("bath", _bath), ("park", _park), ("diner", _diner), ("office", _office), ("subway", _subway),
                     ("bed", _bed), ("class", _class), ("aqua", _aqua)):
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep21_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)
    flash = lights["ep21_flash"]

    # 사람: voxel._person 블록 그대로, 재질 목록만 바꿔 피부색을 인스턴스 속성 col3으로 (→ 초록·누렁 변신)
    mats = [K.mat_inst("ep21_m_shirt", 0.8), K.mat_inst2("ep21_m_pants", rough=0.85),
            K.mat_inst2("ep21_m_skin", attr="col3", rough=0.7), K.mat_simple("ep21_m_hair", X.HAIR, 0.8),
            K.mat_simple("ep21_m_white", (0.96, 0.96, 0.96), 0.4), K.mat_simple("ep21_m_black", (0.015, 0.015, 0.02), 0.4),
            K.mat_simple("ep21_m_mouth", (0.42, 0.10, 0.10), 0.6), K.mat_emit("ep21_m_screen", (0.6, 0.85, 1.0), 3.0)]
    protos = [K.proto(ctx, f"ep21_p_{lh}_{p:02d}", K.join_bms(X._person(p, bool(lh))), mats)
              for lh in (0, 1) for p in range(X.NPOSE)]
    protos += [K.proto(ctx, f"ep21_p_up_{lh}", K.join_bms(_arms_up(bool(lh))), mats) for lh in (0, 1)]
    C = cast()
    people = K.instancer_multi(ctx, "ep21_people", protos, len(C))
    K.add_attr(people, "col3", "FLOAT_COLOR")

    # 빛줄기·빗줄기·알갱이: 'col' 색으로 빛나는 상자 (vector_scale로 길이·굵기 따로)
    fx = K.instancer(ctx, "ep21_fx", K.proto(ctx, "ep21_p_fx", K.bm_cube(1, 1, 1), [H.mat_glow_inst("ep21_m_fx", 4.0)]),
                     NFX, vector_scale=True)
    # 욕실 거울: 거울 재질 상자 하나 (사람이 비쳐야 해서 진짜 반사)
    mir = K.instancer(ctx, "ep21_mirror", K.proto(ctx, "ep21_p_mirror", K.bm_cube(1, 1, 1, (0.5, 0, 0)),
                                                  [K.mat_simple("ep21_m_mirror", (0.93, 0.96, 1.0), 0.0, 1.0)]),
                      1, vector_scale=True)
    K.set_points(mir, [(-0.4 + OFF["bath"][0], 1.72 + OFF["bath"][1], 1.6)], scale=[1.0], size=[(0.02, 1.8, 0.9)],
                 rot=[(0.0, 0.0, math.radians(-90))])

    def upd(t, f):
        i = line_at(t)
        a, b = shot_span(i)
        u = (t - a) / max(b - a, 1e-3)
        st, tg, az, el, dist, lens, push, daz = LINES[i]["shot"]
        o = OFF[st]
        cam.set((tg[0] + o[0], tg[1] + o[1], tg[2]), az + daz * u, el, dist * (1 + (push - 1) * u), lens)
        w = weather(i)
        sun.data.energy = w[0]
        sun.data.color = w[1]
        sun.rotation_euler = [math.radians(r) for r in w[2]]
        ctx.set_ctl("ambient", w[3])
        ctx.set_rgb("ambient_col", w[4])
        flash.data.energy = 130.0 * math.sin(math.pi * ramp(u, 0.3, 0.7)) ** 2 if i == 1 else 0.0
        # 캐릭터
        Q, R, CO, C2, C3, SC, PO = [], [], [], [], [], [], []
        for k, c in enumerate(C):
            d = {**c, "move": None, **c["over"].get(i, {})}
            x, y, z, pose = d["x"], d["y"], d["z"], d["pose"]
            if d["move"]:
                x += d["move"][0] * (t - a)
                y += d["move"][1] * (t - a)
                pose = "walk_a" if ((t - a) / 0.6) % 1.0 < 0.5 else "walk_b"
            elif pose != "lie":
                z += 0.012 * math.sin(2 * math.pi * 1.3 * t + 1.9 * k)
            ox, oy = OFF[d["set"]]
            Q.append((x + ox, y + oy, z))
            R.append((0, 0, math.radians(d["yaw"])))
            CO.append(d["shirt"])
            C2.append(d["pants"])
            C3.append(skin(d["tone"], i, u))
            SC.append(d["scale"] if i in c["over"] else 0.0)
            PO.append(pose_id(d["hair"], pose))
        K.set_points(people, Q, scale=SC, rot=R, col=np.array(CO, np.float32),
                     colors={"col2": np.array(C2, np.float32), "col3": np.array(C3, np.float32)}, pose=PO)
        FP, FS, FR, FC = fx_state(i, t, u)
        K.set_points(fx, FP, scale=(FS[:, 0] > 1e-4).astype(np.float32), size=FS, rot=FR, col=FC)

    ctx.on_frame(upd)
