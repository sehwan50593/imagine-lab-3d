"""EP54 만약에 지구가 천왕성처럼 옆으로 누워 돈다면? (기준 영상 형식 STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

컷 흐름: 훅(한강공원 시계 00:00인데 낮은 해가 하늘을 가로지름·마지막 0.6초 번쩍) → 천왕성 97.77°(지구 구체가 눕는 눈금) → 개그(지구본 눕히면 깃발 쏟아짐)
→ 23.44° 대 97.77° 두 구체 → 천왕성 궤도 4자리(극 42년 낮·42년 밤) → 가정 표지(자전 24시간·1년 그대로) → 극권 7.8° 파란 띠 → 극권 안 86.5%
→ 서울이 극권 안으로 → [1달 뒤] 서울 한낮 해 정수리·그림자 한 점 → [3개월 뒤] 백야 75일 → [9개월 뒤] 해 안 뜨는 75일·낮 12시 잠옷
→ [1년 뒤] 적도 낮 12시간·하지 한낮 7.8°·위도별 해 높이 곡선 → 반전(극이 적도의 1.5배, 지금은 0.41배) → 막대판 뒤집기 → 충돌 가설 → 모형 연구 → 질문 → 다음 편.
특수효과(블렌더 없이 상자·구로): 구체 기울기 = 땅 조각·극관 점을 축 회전행렬로 돌림(축 막대는 발광 상자), 극권 띠·적도 띠 = 구면 위 발광 조각(위도별 점),
하늘의 해 = 카메라 앞 250m 발광 구(화면 좌표), 시계·숫자 = 도트 글자(발광 상자), 막대판 뒤집기 = 두 면을 가진 판을 세로축으로 180° 돌림, 번쩍 = postfx.
효과음: 묶음 '찰싹', 컷 '휙', 훅 번쩍 '쿵', 반전 '땡', 충돌 '쿵', 알람 '삐'. 55편이 같은 날 19:00 슬롯이라 23번 줄은 주제를 예고하지 않음(슬롯 바뀌면 문구만 교체).

근거(설명란): ※ 상상 시나리오: 지구 자전축만 97.77°로 눕고 자전 24시간·공전 365일·태양 거리·대기·바다는 지금 그대로, 춘분에 기울기가 바뀐다는 가정.
  낮 길이·백야 일수·일사량은 전부 계산값(대기 굴절·지평선 높이·구름·반사율 무시). 기울기가 바뀔 때의 바다·기후·생태 결과는 다루지 않음(문헌 없음).
· 줄 1 · 천왕성 자전축(황도면 대비 적도) 기울기 97.77°(적도 경사 82.23°), 자전 17.24시간(역방향). 97.77°는 해 적위가 ±82.23°까지 간다는 뜻(sin97.77° = sin82.23°) · NASA NSSDC Uranus Fact Sheet
· 줄 3 · 지구 자전축 기울기 23.44° · NASA NSSDC Earth Fact Sheet
· 줄 4 · 천왕성 공전 84.01년(30,685.4일). 극에 해가 계속 떠 있는 기간은 공전의 절반 = 84.01 ÷ 2 ≈ 42년(계산값). NASA Science는 "태양계에서 가장 극단적인 계절"·"반쪽은 21년짜리 어두운 겨울"로 표현
  · NASA NSSDC Uranus Fact Sheet, NASA Science Uranus Facts, Hubble 보도(42년)
· 줄 6 · 극권(해가 안 지는 위도) = 90° − 82.23° = 7.77°(지금 66.56°). 해가 머리 위까지 가는 위도(회귀선)는 ±82.23°(지금 ±23.44°) (계산값)
· 줄 7 · 극권 안 면적 비율 = 1 − sin7.77° = 1 − 0.135 = 86.5%(지금 1 − sin66.56° = 8.3%). 매일 해가 뜨고 지는 땅은 13.5% (계산값, 구면 면적 ∝ sin위도)
· 줄 9·10 · 서울(37.5°N) 한낮 해 최고 고도: 지금 90 − 37.5 + 23.44 = 75.9° → 새 지구 90°(해 적위가 37.5°가 되는 날 정수리). 적위 = asin(sin82.23° · sinλ), λ≈38° 부근(춘분 후 약 38일) (계산값)
· 줄 0·11·12 · 서울 해가 안 지는 날 약 75일, 안 뜨는 날 약 75일: 해 적위 > 90 − 37.5 = 52.5°인 날수. 케플러 방정식(이심률 0.0167)으로 1년 365.25일을 나눠 74.7일 (계산값, 굴절·지평선 높이 무시)
· 줄 14·15 · 적도는 어느 적위에서도 낮 12시간. 하지(적위 82.23°) 적도 한낮 해 고도 = 90 − 82.23 = 7.8° (계산값, 굴절 무시)
· 줄 17·18 · 1년 평균 햇빛(태양 상수 S 비율): 새 지구 극 0.315S·적도 0.208S → 극이 적도의 1.5배, 지금 지구 극 0.127S·적도 0.305S → 0.41배.
  Q = S/π·(h₀ sinφ sinδ + cosφ cosδ sin h₀)를 1년(황경 3,600칸) 평균. 대기·구름·반사율·이심률 무시, 극·적도 비교 전용 (계산값, 본문에서 '기온'이 아니라 '받는 햇빛'으로만 표기)
· 줄 20 · 천왕성 기울기는 "아주 오래전 지구 크기 천체와의 충돌의 결과일 수 있다"(가설, 확정 아님) · NASA Science Uranus Facts
· 줄 21 · 지구형 행성이 기울기 최대 90°에서도 거주 가능할 수 있다는 1차원 에너지 균형 모형 결과(대륙 배치에 따라 다름, 90°에선 극 지역이 오래 얼 수 있음, 모형 연구이며 지구에 대한 예언 아님) · Williams & Kasting, Icarus 129:254 (1997)
· 연출용 한 줄(사실 개수에 안 셈): 2번(지구본 눕히기), 5번 '자전 24시간·공전 1년 그대로(가정)', 13번(낮 12시 잠옷).
[확인중] 5건(스토리보드 그대로, 제작 전 확인 필요):
  1. [확인중] 줄 4 '극 42년': NASA Science 페이지에는 '21년 어두운 겨울'만 있어 42년은 공전 84.01년의 절반(계산)+Hubble 보도(2차)로 표기.
  2. [확인중] 줄 9·11·12 서울 고도·일수는 직접 계산(오차 수 일). 춘분에 기울기가 바뀌는 시점은 가정. 대기 굴절·지평선 높이 무시.
  3. [확인중] 줄 17·18 일사 비(1.5배·0.41배)는 외부 문헌과 대조하지 않은 직접 계산(대기·바다 열 이동 무시).
  4. [확인중] 줄 21 Williams & Kasting 원문 직접 열람 못 함(초록·2차 요약으로 확인). 카드는 '모형 연구'로만.
  5. [확인중] 기울기가 바뀔 때의 바다·기후·생태 결과는 본문에서 다루지 않음(문헌 없음 → 단정 금지).
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
TITLE_FAST = True
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"park": (0, 0), "space": (300, 0), "panel": (600, 0), "village": (900, 0)}
NAMES = ("hook", "uranus", "globe", "compare", "orbit", "assume", "circle", "share", "seoul", "zenith", "shadow", "white", "dark", "pajama",
         "equator", "lowsun", "seasons", "twist", "now", "flip", "impact", "model", "ask", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}


def _sp(dist, tgt=(0.0, 0.0, 0.0), push=0.92, daz=0, shift=0.04):
    """우주 단면 세트 정면 샷."""
    return ("space", tgt, -90, 2, dist, 26, push, daz, shift)


# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
# ease="out": 처음에 빨리 움직이고 천천히 멈춤(훅)
LINES = [
    dict(d=3.0, sub="서울에 해가\n75일 안 져요", ease="out", shot=("park", (-0.15, 0.0, 1.55), -90, 2, 4.0, 28, 0.80, 3, 0.10)),
    dict(d=3.0, sub="천왕성은 97.77°\n누워 돌아요", shot=_sp(4.2, (0.0, 0.0, 0.05))),
    dict(d=2.6, sub="지후가 지구본을\n눕혀 봐요", shot=("panel", (0.15, 3.7, 1.1), -90, 2, 5.6, 26, 0.92, 2, 0.08)),
    dict(d=3.0, sub="지금 지구는\n23.4° 기울었어요", shot=_sp(4.6, (0.0, 0.0, 0.15))),
    dict(d=3.2, sub="천왕성 극은\n42년 낮, 42년 밤", shot=_sp(5.6)),
    dict(d=2.6, sub="자전 24시간,\n1년은 그대로", shot=_sp(5.2, (0.0, 0.0, 0.1))),
    dict(d=3.0, sub="해 안 지는 곳이\n위도 7.8°부터", shot=_sp(4.0, daz=3)),
    dict(d=3.0, sub="지표 86.5%가\n극권 안이에요", shot=_sp(4.0, daz=-3)),
    dict(d=2.6, sub="서울이 극권\n안으로 들어가요", shot=("panel", (0.35, 5.0, 1.9), -90, 2, 8.0, 26, 0.92, 0, 0.06)),
    dict(d=3.0, sub="서울 한낮 해가\n정수리까지", shot=("park", (0.0, 0.0, 1.7), -90, 3, 3.8, 26, 0.92, 0, 0.05)),
    dict(d=2.6, sub="그림자가\n발밑 한 점이 돼요", shot=("park", (0.0, 0.0, 0.7), -90, 4, 5.4, 26, 0.92, 3, 0.04)),
    dict(d=3.0, sub="하지 전후\n서울은 75일 백야", shot=("park", (-0.15, 0.0, 1.55), -92, 2, 4.0, 26, 0.92, -3, 0.10)),
    dict(d=2.6, sub="9개월 뒤엔\n75일 해가 안 떠요", shot=("park", (0.0, 0.0, 1.4), -90, 2, 4.0, 26, 0.90, 0, 0.08)),
    dict(d=2.6, sub="낮 12시에\n잠옷을 입어요", shot=("park", (0.15, 0.3, 1.2), -80, 3, 4.0, 28, 0.90, 3, 0.08)),
    dict(d=3.0, sub="적도는 낮이\n늘 12시간이에요", shot=("village", (0.15, 0.0, 1.1), -90, 2, 5.4, 26, 0.92, 0, 0.06)),
    dict(d=3.0, sub="적도 하지엔\n한낮 고도 7.8°", shot=("village", (0.0, 0.0, 0.7), -90, 3, 5.4, 26, 0.92, 0, 0.04)),
    dict(d=2.6, sub="위도마다\n계절 모양이 달라요", shot=("panel", (0.0, 5.0, 2.0), -90, 2, 6.5, 26, 0.92, 0, 0.06)),
    dict(d=3.0, sub="일 년 평균\n극이 적도의 1.5배", shot=("panel", (0.0, 5.0, 1.7), -90, 2, 6.5, 26, 0.90, 0, 0.06)),
    dict(d=3.0, sub="지금 지구는\n극이 적도의 0.4배", shot=("panel", (0.0, 5.0, 1.7), -90, 2, 8.0, 26, 0.90, 0, 0.06)),
    dict(d=2.6, sub="햇빛 막대가\n거꾸로 뒤집혀요", shot=("panel", (0.0, 5.0, 1.5), -90, 2, 8.0, 26, 0.92, 2, 0.06)),
    dict(d=3.0, sub="천왕성은\n충돌로 누웠을 수도", shot=_sp(5.0)),
    dict(d=3.0, sub="90°여도 살 만하단\n모형 연구", shot=("park", (0.2, 0.0, 1.3), -85, 3, 4.4, 26, 0.92, 3, 0.08)),
    dict(d=3.0, sub="누운 지구, 어디에서 살래요?\n댓글로 알려 주세요", shot=("park", (-0.2, 0.0, 1.4), -90, 2, 4.2, 26, 0.92, 0, 0.10)),
    dict(d=3.0, sub="오늘 저녁 7시 · 새 '만약에'\n구독하면 놓치지 않아요", shot=_sp(9.0, shift=0.06)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="서울", title="자전축이 눕는다면", title_size=70, big="백야 75일", big_color="orange"),
    dict(at="uranus", badge="바로", title="천왕성 자전축", big="97.77°", big_color="yellow"),
    dict(at="globe", badge="바로", title="지구본을 눕혀 보면", title_size=70),
    dict(at="compare", badge="바로", title="지금 지구는", big="23.44°", big_color="white"),
    dict(at="orbit", badge="바로", title="천왕성의 극", big="낮 42년", big_color="cyan", note="밤도 42년 · 계산", note_color="cyan"),
    dict(at="assume", badge="가정", title="자전 24시간 그대로", title_size=68, note="자전축만 눕는다는 가정", note_color="orange"),
    dict(at="circle", badge="바로", title="해 안 지는 위도", big="7.8°", big_color="orange", note="지금은 66.6° · 계산", note_color="orange"),
    dict(at="share", badge="바로", title="극권 안 지표 면적", title_size=68, big="86.5%", big_color="red", note="지금은 8.3% · 계산", note_color="orange"),
    dict(at="seoul", badge="바로", title="서울이 극권 안으로", title_size=68),
    dict(at="zenith", badge="1달 뒤", title="서울 한낮 해 높이", title_size=68, big="90°", big_color="yellow", note="지금 75.9° · 계산", note_color="orange"),
    dict(at="shadow", badge="1달 뒤", title="그림자가 한 점으로", title_size=68),
    dict(at="white", badge="3개월 뒤", title="서울 해 안 지는 날", title_size=68, big="약 75일", big_color="orange", note="계산 · 굴절 무시", note_color="orange"),
    dict(at="dark", badge="9개월 뒤", title="안 뜨는 날도 약 75일", title_size=62),
    dict(at="pajama", badge="9개월 뒤", title="한낮 12시, 한밤", title_size=70),
    dict(at="equator", badge="1년 뒤", title="적도 낮의 길이", big="12시간", big_color="cyan", note="1년 내내 · 계산", note_color="cyan"),
    dict(at="lowsun", badge="1년 뒤", title="적도 하지 한낮 해", title_size=68, big="고도 7.8°", big_color="orange", note="90 − 82.23 · 계산", note_color="orange"),
    dict(at="seasons", badge="1년 뒤", title="위도마다 계절이 달라요", title_size=62),
    dict(at="twist", badge="지금", title="1년 평균 햇빛 극÷적도", title_size=60, big="1.5배", big_color="red",
         note="계산 · 가정 · 대기·구름 무시", note_color="orange"),
    dict(at="flip", title="햇빛 막대 뒤집힘", title_size=70, note="계산 · 가정 시나리오", note_color="orange"),
    dict(at="impact", title="천왕성이 누운 이유", title_size=68, big="충돌 가설", big_color="cyan", note="NASA · 확정 아님", note_color="cyan"),
    dict(at="model", title="기울기 90°의 지구", title_size=70, big="거주 가능?", big_color="green", note="1차원 모형 · 극은 얼 수 있음", note_color="green"),
    dict(at="ask", title="누운 지구, 어디서\n{cyan}살래요?{/}", title_size=64),
    dict(at="teaser", badge="다음 편", title="다음 '만약에'는\n{cyan}무엇일까요?{/}", title_size=70),
]
TWIST = LN["twist"]  # '1년 평균 극이 적도의 1.5배' 줄 — 음악이 바뀌는 곳
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
_FLASH_AT = LINES[0]["d"] - 0.6                         # 훅 마지막 0.6초: 해가 지후 뒤에서 번쩍
META = {"id": "ep54", "title": "만약에 지구가 천왕성처럼 옆으로 누워 돈다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"style": "retro", "key": "C", "mode": "major", "bpm": 104, "seed": 541, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, [[_FLASH_AT, "thud", 0.7], [STARTS[TWIST] + 0.3, "ding", 1.0],
                                                      [STARTS[LN["impact"]] + 0.42 * LINES[LN["impact"]]["d"], "thud", 0.7],
                                                      [STARTS[LN["pajama"]] + 0.1, "buzz", 1.0, 1.8]])}}
GRADE = {"exposure": 0.95, "bloom": 0.14, "bloom_thr": 1.4, "vignette": 0.16}


def line_at(t):
    """지금 몇 번째 줄(컷)인지."""
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s - 0.02:
            i = k
    return i


def shot_span(i):
    a = 0.0 if i == 0 else STARTS[i]
    b = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    return a, b


def simulate(build_dir):
    return {"dur": np.float32(DUR)}


# ───────────────────────── 상자 · 구 목록 ─────────────────────────
def _rmat(rx, ry, rz):
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    return (np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]) @ np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @
            np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]))


class Items:
    """상자 인스턴스 모음 (좌표는 세트 기준, off = 그 세트의 자리 OFF). 상자 원점 = 뒷면 가운데, +x로 뻗음(size로 늘림).
    b()는 회전 없는 상자를 가운데 기준으로 빨리, c()는 회전 상자를 가운데 기준으로, 구는 orb()(원점 = 가운데, size = 지름).
    cw()·orbw()는 월드 좌표(카메라 기준 물체용)."""

    def __init__(self, cap, off=(0.0, 0.0)):
        self.cap, self.off, self.P, self.S, self.R, self.C = cap, (float(off[0]), float(off[1])), [], [], [], []

    def _add(self, origin, size, col, rot):
        self.P.append((float(origin[0]), float(origin[1]), float(origin[2])))
        self.S.append((float(size[0]), float(size[1]), float(size[2])))
        self.R.append((float(rot[0]), float(rot[1]), float(rot[2])))
        self.C.append((float(col[0]), float(col[1]), float(col[2])))

    def o(self, origin, size, col, rot=(0.0, 0.0, 0.0)):
        self._add((origin[0] + self.off[0], origin[1] + self.off[1], origin[2]), size, col, rot)

    def b(self, center, size, col):
        self.o((center[0] - size[0] / 2, center[1], center[2]), size, col)

    def c(self, center, size, col, rot=(0.0, 0.0, 0.0)):
        org = np.asarray(center, float) - _rmat(*rot) @ np.array((size[0] / 2, 0.0, 0.0))
        self.o(org, size, col, rot)

    def orb(self, center, d, col):
        self.o(center, (d, d, d), col)

    def cw(self, center, size, col, rot=(0.0, 0.0, 0.0)):
        self._add(np.asarray(center, float) - _rmat(*rot) @ np.array((size[0] / 2, 0.0, 0.0)), size, col, rot)

    def orbw(self, center, d, col):
        self._add(center, (d, d, d), col, (0.0, 0.0, 0.0))

    def __len__(self):
        return len(self.P)

    def arrays(self):
        n = len(self.P)
        assert n <= self.cap, f"인스턴스 칸 부족: {n} > {self.cap}"
        pad = self.cap - n
        z3 = [(0.0, 0.0, 0.0)] * pad
        return (np.array(self.P + z3, np.float32), np.array([1.0] * n + [0.0] * pad, np.float32),
                np.array(self.S + z3, np.float32), np.array(self.R + z3, np.float32), np.array(self.C + z3, np.float32))


def euler_of(R):
    """회전행렬(열 = 상자의 x·y·z 축이 가리키는 방향) → _rmat과 맞는 오일러 (rx, ry, rz)."""
    ry = -math.asin(max(-1.0, min(1.0, float(R[2, 0]))))
    return (math.atan2(float(R[2, 1]), float(R[2, 2])), ry, math.atan2(float(R[1, 0]), float(R[0, 0])))


def rot_cam(cam):
    """카메라 화면과 나란한 납작한 판의 오일러 회전: 상자 x = 앞(두께), y = 화면 가로, z = 화면 세로."""
    return euler_of(np.stack([cam["fwd"], -cam["right"], cam["up"]], 1))


def rot_to(d):
    """상자의 +x 축이 방향 d(단위벡터)를 향하게 하는 오일러 회전."""
    return (0.0, -math.asin(max(-1.0, min(1.0, float(d[2])))), math.atan2(float(d[1]), float(d[0])))


def rot_n(n):
    """상자의 +x(두께) 축이 면의 바깥쪽 법선 n을 향하고 y·z가 면 위를 가리키게 하는 오일러 회전 (지구 땅 조각용)."""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    t1 = np.cross((0.0, 0.0, 1.0), n)
    if np.linalg.norm(t1) < 1e-4:
        t1 = np.array((0.0, 1.0, 0.0))
    t1 = t1 / np.linalg.norm(t1)
    return euler_of(np.stack([n, t1, np.cross(n, t1)], 1))


def screen_dir(cam, nx, ny, base=False):
    """화면 좌표 (nx 오른쪽 +, ny 위 +, 둘 다 -1~1)가 가리키는 방향 단위벡터. base=True면 흔들림을 뺀 카메라 기준."""
    f = cam["lens"]
    fw, rt, up = (cam["fwd0"], cam["right0"], cam["up0"]) if base else (cam["fwd"], cam["right"], cam["up"])
    d = fw + nx * (6.75 / f) * rt + (ny + 2.0 * cam["shift"]) * (12.0 / f) * up
    return d / np.linalg.norm(d)


def sprite(G, cam, nx, ny, w, h, col, dist=2.0, thick=0.02):
    """화면 좌표에 정면을 보는 납작한 상자를 카메라에서 dist m 앞에 둠. w·h = 화면 높이에 대한 비율."""
    s = dist * 24.0 / cam["lens"]
    G.cw(cam["loc"] + screen_dir(cam, nx, ny) * dist, (thick, w * s, h * s), col, rot_cam(cam))


def sprite_orb(OR, cam, nx, ny, dfrac, col, dist=2.0):
    """화면 좌표에 구를 둠 (dfrac = 화면 높이에 대한 지름 비율)."""
    OR.orbw(cam["loc"] + screen_dir(cam, nx, ny) * dist, dfrac * dist * 24.0 / cam["lens"], col)


def pop(tau, dur=0.30, over=3.0):
    """톡 튀어나오는 크기: 0 → 살짝 커졌다 → 1 (easeOutBack). tau<0이면 0."""
    if tau <= 0:
        return 0.0
    if tau >= dur:
        return 1.0
    x = tau / dur - 1.0
    return 1.0 + (over + 1.0) * x ** 3 + over * x ** 2


def vanish(tau, t0, dur=0.17):
    """퐁: t0에서 살짝 부풀었다가 쏙 사라짐. 1 → 1.3 → 0. t0 전엔 1, 사라진 뒤 0."""
    d = tau - t0
    if d <= 0.0:
        return 1.0
    if d >= dur:
        return 0.0
    if d < 0.3 * dur:
        return 1.0 + 0.3 * smooth(d / (0.3 * dur))
    return 1.3 * (1.0 - smooth((d - 0.3 * dur) / (0.7 * dur)))


def _h(n):
    """결정적 의사난수 0~1."""
    return (math.sin(n * 12.9898 + 4.1414) * 43758.5453) % 1.0


# ───────────────────────── 도트 글자 (3x5) ─────────────────────────
DIG = {"0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"], "2": ["###", "..#", "###", "#..", "###"],
       "3": ["###", "..#", "###", "..#", "###"], "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
       "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", ".#.", ".#.", ".#."], "8": ["###", "#.#", "###", "#.#", "###"],
       "9": ["###", "#.#", "###", "..#", "###"], ".": ["...", "...", "...", "...", ".#."], ":": ["...", ".#.", "...", ".#.", "..."],
       "!": [".#.", ".#.", ".#.", "...", ".#."], "?": ["###", "..#", ".##", "...", ".#."], "x": ["...", "#.#", ".#.", "#.#", "..."],
       ",": ["...", "...", "...", ".#.", "#.."], "k": ["#..", "#.#", "##.", "#.#", "#.#"], "m": [".....", "####.", "#.#.#", "#.#.#", "#.#.#"],
       "-": ["...", "...", "###", "...", "..."], "+": ["...", ".#.", "###", ".#.", "..."], "/": ["..#", "..#", ".#.", "#..", "#.."],
       "%": ["#.#", "..#", ".#.", "#..", "#.#"], " ": ["..", "..", "..", "..", ".."]}


def num_rows(txt, gap=1):
    """숫자·단위(3x5) → 5줄 문자열 목록."""
    parts = [DIG[c] for c in txt]
    out = [""] * 5
    for n, p in enumerate(parts):
        for r in range(5):
            out[r] += p[r] + ("." * gap if n + 1 < len(parts) else "")
    return out


def _runs(rows):
    """그림 → [(줄, 시작 칸, 끝 칸)] 같은 줄에서 이어진 '#' 칸을 하나로."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] != "#":
                c += 1
                continue
            c1 = c
            while c1 + 1 < len(row) and row[c1 + 1] == "#":
                c1 += 1
            out.append((r, c, c1))
            c = c1 + 1
    return out


def srows(G, cam, rows, nx, ny, cell, col, dist=1.8, k=1.0):
    """도트 그림을 화면 좌표 (nx, ny) 가운데에 그림 (cell = 한 칸의 화면 높이 비율, k = 크기 배율). 카메라 앞 납작한 발광 상자들."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        px = ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k
        py = (h / 2.0 - r - 0.5) * cell * k
        sprite(G, cam, nx + px / 0.28125, ny + py / 0.5, ((c1 - c + 1) - 0.06) * cell * k, cell * 0.94 * k, col, dist, 0.012)


def frows(G, rows, center, cell, col, k=1.0, thick=0.03, psi=0.0):
    """바닥·판 위에 눕힌 도트 그림 (세트 좌표, 가운데 맞춤): 가로 = +x(psi만큼 돌림), 줄은 아래로 갈수록 −y. 위에서 내려다보는 판용."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    cp, sp = math.cos(psi), math.sin(psi)
    for r, c, c1 in _runs(rows):
        dx, dy = ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, (h / 2.0 - r - 0.5) * cell * k
        G.c((center[0] + dx * cp - dy * sp, center[1] + dx * sp + dy * cp, center[2]),
            (((c1 - c + 1) - 0.06) * cell * k, cell * 0.94 * k, thick), col, (0.0, 0.0, psi))



# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def _basis(loc, tgt):
    fwd = tgt - loc
    fwd = fwd / np.linalg.norm(fwd)
    right = np.cross(fwd, (0.0, 0.0, 1.0))
    right = right / np.linalg.norm(right)
    return fwd, right, np.cross(right, fwd)


def cam_pose(i, tau, u):
    """줄 i, 줄 시작 후 τ초(진행도 u)의 카메라: dict(set, tgt, az, el, dist, lens, loc, shift, fwd, right, up) — 월드 좌표. CamRig.set과 같은 규칙."""
    shot = LINES[i]["shot"]
    st_, tg, az, el, dist, lens, push, daz = shot[:8]
    shift = shot[8] if len(shot) > 8 else 0.0
    ul = 1.0 - (1.0 - u) ** 2 if LINES[i].get("ease") == "out" else u
    o = OFF[st_]
    tgt = np.array((tg[0] + o[0], tg[1] + o[1], tg[2]), float)
    a, e, dd = az + daz * ul, el + (shot[9] if len(shot) > 9 else 0.0) * ul, dist * (1 + (push - 1) * ul)
    ea = math.radians(e)
    loc = tgt + np.array((math.cos(ea) * math.cos(math.radians(a)), math.cos(ea) * math.sin(math.radians(a)), math.sin(ea))) * dd
    fwd, right, up = _basis(loc, tgt)
    return dict(set=st_, tgt=tgt, az=a, el=e, dist=dd, lens=lens, loc=loc, shift=shift, fwd=fwd, right=right, up=up, fwd0=fwd, right0=right, up0=up)


def project(cam, p):
    """월드 점 → (화면 x 0~1 왼쪽부터, y 0~1 위부터, 깊이). CamRig(센서 세로 24mm) + 렌즈 세로 이동(shift)과 같은 규칙."""
    d = np.asarray(p, float) - cam["loc"]
    z = float(d @ cam["fwd"])
    k = cam["lens"] / 24.0
    return 0.5 + (float(d @ cam["right"]) / z) * k / (1080.0 / 1920.0), 0.5 - (float(d @ cam["up"]) / z) * k + cam["shift"], z


def cam_of(t):
    i = line_at(t)
    a, b = shot_span(i)
    tau = max(t - a, 0.0)
    return cam_pose(i, tau, min(tau / max(b - a, 1e-3), 1.0))


# ───────────────────────── 캐릭터 자세 (표준 자세 위에 팔·고개·입만 바꾼 원형 + 후드·가운·헬멧) ─────────────────────────
# base = 바탕 자세, arms = ((오른팔 앞뒤, 옆), (왼팔 앞뒤, 옆)) 어깨 회전각(앞뒤 음수 = 앞으로 듦, 양수 = 뒤로 젖힘, 옆: 오른팔 +가 몸 쪽·왼팔 +가 바깥),
# mouth = open/smile/frown, head = 고개 숙임(+)/젖힘(−)
KINDS = {
    "smile": dict(base="stand", mouth="smile"),
    "aw_up": dict(base="stand", head=-0.50, mouth="open"),                                       # 입을 벌리고 하늘을 올려다봄
    "shield": dict(base="stand", arms=((-2.55, 0.45), (-2.55, -0.45)), head=0.12, mouth="open"),  # 두 팔로 얼굴을 가림
    "gape": dict(base="stand", arms=((-0.25, -0.30), (-0.25, 0.30)), mouth="open", head=-0.25),  # 멍하니 입을 벌림
    "shock": dict(base="stand", arms=((-2.9, 0.20), (-2.9, -0.20)), mouth="open", head=-0.15),   # 두 손을 번쩍
    "film": dict(base="stand", arms=((-2.4, 0.0), (0.0, 0.0)), head=-0.30),                      # 폰을 들고 하늘을 찍음
    "point_up": dict(base="stand", arms=((-2.2, 0.0), (0.0, 0.0)), head=-0.40, mouth="open"),   # 하늘을 가리킴
    "look_up": dict(base="stand", head=-0.45),
    "look_up_h": dict(base="stand", head=-0.45, mouth="smile"),
    "carry": dict(base="stand", arms=((-1.30, 0.14), (-1.30, -0.14)), mouth="smile"),            # 유리판을 두 손으로 듦
    "carry_o": dict(base="stand", arms=((-1.30, 0.14), (-1.30, -0.14)), mouth="open"),
    "work": dict(base="stand", arms=((-2.7, 0.12), (-2.7, -0.12)), head=-0.30),                  # 사다리 위에서 위로 팔을 뻗음
    "point": dict(base="stand", arms=((-1.5, 0.0), (0.0, 0.0)), mouth="smile"),
    "think": dict(base="stand", arms=((-2.7, 0.0), (0.0, 0.0)), head=0.1),
    "peer": dict(base="stand", arms=((-1.2, 0.1), (-1.2, -0.1)), head=0.35),                     # 망원경을 들여다봄
    "walk_a_s": dict(base="walk_a", mouth="smile"),
    "walk_b_s": dict(base="walk_b", mouth="smile"),
}
ARMS = {"stand": (0.0, 0.0), "sit": (-0.6, -0.6), "phone": (-1.05, 0.0), "angry": (-2.5, -2.5), "confused": (-2.75, 0.05),
        "talk": (-0.9, 0.05), "walk_a": (0.35, -0.35), "walk_b": (-0.35, 0.35), "sit_phone": (-1.05, -0.6), "sit_conf": (-2.75, -0.6),
        "lie": (0.0, 0.0)}
ROLLS = {}
for _k, _sp in KINDS.items():
    ARMS[_k] = tuple(a[0] for a in _sp["arms"]) if _sp.get("arms") else ARMS[_sp["base"]]
    ROLLS[_k] = tuple(a[1] for a in _sp["arms"]) if _sp.get("arms") else (0.0, 0.0)


def base_of(pose):
    return KINDS[pose]["base"] if pose in KINDS else pose


def hip_of(pose):
    return 0.47 if base_of(pose) in ("sit", "sit_phone", "sit_conf") else 0.78


def _rot_x(bm, ang, pivot):
    """x축(앞) 둘레 회전 (y·z만 움직임)."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        y, z = p.co.y - pivot[1], p.co.z - pivot[2]
        p.co.y, p.co.z = pivot[1] + c * y - s * z, pivot[2] + s * y + c * z
    return bm


def _rot_head(bm, ang, pivot):
    """y축(옆) 둘레 회전인데 목(피벗) 위 꼭짓점만 돌림 — 긴 머리 아래쪽은 몸 뒤로 그대로 늘어짐."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        if p.co.z >= pivot[2] - 1e-6:
            x, z = p.co.x - pivot[0], p.co.z - pivot[2]
            p.co.x, p.co.z = pivot[0] + c * x + s * z, pivot[2] - s * x + c * z
    return bm


def _variant(name, lh):
    """voxel._person으로 만든 바탕 자세에서 팔·고개·입만 바꾼 [(bmesh, 재질)]."""
    from engine import bkit as K
    sp = KINDS[name]
    sit = sp["base"] in ("sit", "sit_phone", "sit_conf")
    P = X._person(X.POSES[sp["base"]], lh)
    hip = 0.47 if sit else 0.78
    hz = hip + 0.58
    nl = 6 if sit else 4
    legs, torso, head, arms = P[:nl], P[nl], list(P[nl + 1:-4]), P[-4:]

    def cube(cx, cy, z0, sx, sy, sz):
        return K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True)
    mouth = {"open": [(cube(0.232, 0, hz + 0.04, 0.02, 0.13, 0.07), 6)],
             "smile": [(cube(0.232, 0, hz + 0.04, 0.02, 0.11, 0.028), 6), (cube(0.232, -0.075, hz + 0.055, 0.02, 0.03, 0.04), 6),
                       (cube(0.232, 0.075, hz + 0.055, 0.02, 0.03, 0.04), 6)],
             "frown": [(cube(0.232, 0, hz + 0.065, 0.02, 0.11, 0.028), 6), (cube(0.232, -0.075, hz + 0.045, 0.02, 0.03, 0.04), 6),
                       (cube(0.232, 0.075, hz + 0.045, 0.02, 0.03, 0.04), 6)]}
    if sp.get("mouth"):
        drop = {id(bm) for bm, mi in head if mi == 6}      # 먼저 고르고 나서 free (free 뒤엔 bm을 읽을 수 없음)
        keep = []
        for bm, mi in head:
            if id(bm) in drop:
                bm.free()
            else:
                keep.append((bm, mi))
        head = keep + mouth[sp["mouth"]]

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
    if sp.get("head"):                                             # 고개: 목(어깨 위)을 축으로 숙이거나 젖힘
        for bm, _ in head:
            _rot_head(bm, sp["head"], (0, 0, hz))
    return list(legs) + [torso] + head + list(arms)


def _person_parts(pose, hair, extra=""):
    """표준 자세면 voxel 원형, 새 자세면 _variant. extra: 'hood'(지후 후드) · 'coat'(연구원 흰 가운) · 'cap'(공사 헬멧)."""
    from engine import bkit as K
    P = _variant(pose, bool(hair)) if pose in KINDS else X._person(X.POSES[pose], bool(hair))
    hip = hip_of(pose)
    hz = hip + 0.58
    if extra == "hood":                                            # 목 뒤 후드 (셔츠 색) + 흰 끈 둘
        P.append((K.bm_cube(0.14, 0.40, 0.22, (-0.20, 0, hz - 0.13), bottom=True), 0))
        for sy in (-0.07, 0.07):
            P.append((K.bm_cube(0.014, 0.026, 0.17, (0.158, sy, hip + 0.30), bottom=True), 4))
    elif extra == "coat":                                          # 허리 아래로 내려오는 가운 자락(셔츠 색) + 목 뒤 깃
        P.append((K.bm_cube(0.34, 0.54, 0.36, (0, 0, hip - 0.30), bottom=True), 0))
        P.append((K.bm_cube(0.12, 0.40, 0.14, (-0.10, 0, hip + 0.52), bottom=True), 0))
    elif extra == "cap":                                           # 안전모: 둥근 윗판 + 앞챙 (흰색)
        P.append((K.bm_cube(0.56, 0.56, 0.20, (-0.01, 0, hz + 0.40), bottom=True), 4))
        P.append((K.bm_cube(0.12, 0.42, 0.03, (0.28, 0, hz + 0.40), bottom=True), 4))
    return P


# ───────────────────────── 위치 도우미 ─────────────────────────
def rel(d, fwd, lat, up):
    """캐릭터 기준 (앞, 왼쪽, 위) → 세트 좌표. 크기 반영."""
    a = math.radians(d["yaw"])
    s = d["scale"]
    return (d["x"] + s * (fwd * math.cos(a) - lat * math.sin(a)), d["y"] + s * (fwd * math.sin(a) + lat * math.cos(a)),
            d["z"] + s * up)


def head_pt(d, up=1.04):
    """머리 꼭대기 한가운데(세트 좌표)."""
    return rel(d, 0.0, 0.0, hip_of(d["pose"]) + up)


def hand_pt(d, side, reach=0.0):
    """side 'R'(캐릭터 오른손)·'L' 손 끝 근처 점 (옆으로 벌리는 롤 반영)."""
    ang = ARMS[d["pose"]][0 if side == "R" else 1]
    roll = ROLLS.get(d["pose"], (0.0, 0.0))[0 if side == "R" else 1]
    dd = 0.49 + reach
    sy = -0.34 if side == "R" else 0.34
    lat = sy + dd * math.sin(roll)
    r = dd * math.cos(roll)
    return rel(d, -r * math.sin(ang), lat, hip_of(d["pose"]) + 0.54 - r * math.cos(ang))


def st(set_, x, y, yaw, pose, z=0.0, **kw):
    """한 줄 안에서의 자리·자세. 선택 값: v 속도(m/s, 줄 시작부터) · stop 멈추는 τ(초) · pair 걷기 두 자세 · cad 걸음 주기 ·
    then (τ, 바뀐 자세) · alt (자세A, 자세B, 주기, 위상) 번갈아 · seq [(τ, 자세)...] 자세 순서 · sway (각도, 주기, 위상) 몸이 좌우로 돌아봄 ·
    keys [(τ, (x, y, z, yaw))...] 부드럽게 이어지는 경로(있으면 x, y, z, yaw가 이걸로 정해짐) · ease 경로 보간(기본 부드럽게) ·
    fn 함수(τ, t) → dict(x=, y=, z=, yaw=, pose=) 덮어쓰기."""
    return dict(set=set_, x=x, y=y, z=z, yaw=yaw, pose=pose, **kw)


def _poses_of(s):
    out = {s["pose"]}
    for k in ("pair", "alt"):
        if k in s:
            out |= set(s[k][:2])
    if "then" in s:
        out.add(s["then"][1])
    for _, p in s.get("seq", []):
        out.add(p)
    out |= set(s.get("also", ()))
    return out

def state_of(c, i, u, tau, dur, t):
    """캐릭터 c의 줄 i, 진행도 u(τ초)에서의 자리·자세(세트 좌표) 또는 None(안 보임)."""
    a = c["at"].get(i)
    if a is None:
        return None
    if isinstance(a, list):                           # 한 줄 안에서 컷마다 자리가 바뀜
        us, a = [(us_, aa) for us_, aa in a if u >= us_ - 1e-6][-1]
        tau = tau - us * dur
    d = dict(a)
    if "keys" in a:
        d["x"], d["y"], d["z"], d["yaw"] = keyed(tau, a["keys"], a.get("ease", smooth))
        moving = tau < a["keys"][-1][0]
    else:
        vx, vy = a.get("v", (0.0, 0.0))
        tt = min(max(tau, 0.0), a.get("stop", 1e9))
        d["x"], d["y"] = a["x"] + vx * tt, a["y"] + vy * tt
        moving = (vx != 0.0 or vy != 0.0) and tau < a.get("stop", 1e9)
    if "then" in a and tau >= a["then"][0]:
        d["pose"] = a["then"][1]
    for t0, p in a.get("seq", []):
        if tau >= t0:
            d["pose"] = p
    al = a.get("alt")
    if al:
        d["pose"] = al[int((t + al[3]) / al[2]) % 2]
    if "sway" in a:
        amp, per, ph = a["sway"]
        d["yaw"] = a["yaw"] + amp * math.sin(2 * math.pi * (t / per + ph))
    if moving and "pair" in a:
        cad = a.get("cad", 0.28)
        d["pose"] = a["pair"][int(t / cad) % 2]
        d["z"] += 0.03 * abs(math.sin(math.pi * t / cad))
    if "fn" in a:
        d.update(a["fn"](tau, t))
    d["scale"] = c["scale"]
    return d


# ── 지구 (파란 구 + 땅 조각)
def _fib(n):
    ga = math.pi * (3.0 - math.sqrt(5.0))
    return np.array([(math.sqrt(1 - z * z) * math.cos(ga * k), math.sqrt(1 - z * z) * math.sin(ga * k), z)
                     for k, z in ((k, 1 - 2 * (k + 0.5) / n) for k in range(n))])


EARTH_PTS = _fib(1100)


def _is_land(p):
    return math.sin(3.1 * p[0] + 1.0) * math.sin(2.7 * p[1] + 2.0) + 0.7 * math.sin(3.9 * p[2] + 0.5) > 0.12


LAND = [bool(_is_land(p)) for p in EARTH_PTS]
LAND_IDX = [k for k, p in enumerate(EARTH_PTS) if LAND[k] or abs(p[2]) > 0.88]


def _land_col(k):
    z = abs(EARTH_PTS[k][2])
    if z > 0.88:
        return (0.93, 0.96, 1.0)
    h = _h(k + 2000)
    return (0.74, 0.63, 0.38) if h > 0.82 else (0.22 + 0.10 * h, 0.55 + 0.12 * _h(k + 3000), 0.22 + 0.06 * h)


LAND_COL = {k: _land_col(k) for k in LAND_IDX}


def sp_of(t):
    return 0.35 * t


def _mat_glow(name, strength=1.0):
    """인스턴스 'col' 색으로 빛나는 재질 (불덩이·충격파·글자·별·눈금). 색 값이 1보다 크면 더 밝게 번짐."""
    from engine import bkit as K
    m, nt, out = K.new_mat(name)
    e = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, K.inst_attr(nt, "col"), e.inputs["Color"])
    e.inputs["Strength"].default_value = strength
    K.ln(nt, e.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m



def wdig(G, rows, cx, y, cz, cell, col, k=1.0):
    """세트에 서 있는 도트 글자 (−y쪽을 보는 면, 가운데 맞춤): 칸 하나 = 발광 상자."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        G.b((cx + ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, y, cz + (h / 2.0 - r - 0.5) * cell * k),
            (((c1 - c + 1) - 0.06) * cell * k, 0.03, cell * 0.94 * k), col)



def earth_rot(sp, tilt=23.44):
    """구체의 몸 좌표(z = 자전축) → 월드: 자전 sp(라디안) 뒤 화면 안쪽으로 tilt도 기울임(y축 둘레, 위 극이 오른쪽으로)."""
    return _rmat(0.0, math.radians(tilt), 0.0) @ _rmat(0.0, 0.0, sp)


def axis_of(tilt):
    a = math.radians(tilt)
    return np.array((math.sin(a), 0.0, math.cos(a)))


# ───────────────────────── 색 · 숫자 ─────────────────────────
OCEAN = (0.08, 0.26, 0.68)
ICE = (0.50, 0.80, 0.88)
ROCK = (0.55, 0.50, 0.46)
SUN_C = (3.0, 2.2, 0.8)
BLUE_G = (0.35, 1.2, 3.0)
FILL_G = (0.08, 0.30, 0.80)
YEL_G = (3.0, 2.4, 0.6)
ORG_G = (3.0, 1.5, 0.3)
CYA_G = (0.5, 2.2, 2.8)
WHT_G = (2.2, 2.2, 2.4)
JH_SH, JH_PA = (0.58, 0.32, 0.80), (0.15, 0.18, 0.30)      # 지후: 보라 후드 · 짧은 머리 · 남색 바지
CO_SH, CO_PA = (0.93, 0.93, 0.91), (0.22, 0.24, 0.30)      # 연구원: 흰 가운 (extra='coat')
EX_SH = [(0.55, 0.45, 0.42), (0.58, 0.55, 0.40), (0.40, 0.52, 0.45), (0.42, 0.50, 0.58)]   # 엑스트라는 채도 낮게
TABLE_C = (0.45, 0.33, 0.24)
PLATE_C = (0.10, 0.14, 0.24)


def wpt(set_, p):
    """세트 좌표 → 월드 좌표."""
    return (p[0] + OFF[set_][0], p[1] + OFF[set_][1], p[2])


def to_ndc(cam, p):
    """월드 점 → 화면 좌표(nx 오른쪽 +, ny 위 +, −1~1)."""
    x, y, _ = project(cam, p)
    return (x - 0.5) * 2.0, 1.0 - 2.0 * y


def sky_orb(OR, cam, nx, ny, dfrac, col, D=250.0):
    """하늘의 해: 카메라 앞 D m 발광 구 (dfrac = 화면 높이에 대한 지름 비율)."""
    OR.orbw(cam["loc"] + screen_dir(cam, nx, ny) * D, dfrac * D * 24.0 / cam["lens"], col)


def gauge(G, cam, a, b, col, n=14, s=0.007):
    """화면 좌표 a→b 점선 지시선."""
    for q in range(n + 1):
        p = q / n
        sprite(G, cam, lerp(a[0], b[0], p), lerp(a[1], b[1], p), s, s, col, 1.8, 0.012)


def park_clock(G, txt, col=(0.6, 2.4, 2.6), k=1.0):
    wdig(G, num_rows(txt), -0.62, 0.92, 1.38, 0.036, col, k)


# ───────────────────────── 세트 ─────────────────────────
def _park(v):
    """한강변 공원: 잔디·산책로·강·낮은 도시 윤곽·다리·나무·시계 판."""
    v.floor(-40, 40, -9, 6, (0.30, 0.38, 0.26), 1.0)
    v.floor(-40, 40, -1.6, 2.6, (0.52, 0.49, 0.45), 0.5, z=0.01)
    v.floor(-90, 90, 6.0, 160, (0.06, 0.14, 0.30), 5.0, z=-0.3)                           # 한강
    v.box(-40, 40, 5.9, 6.1, -0.3, -0.02, (0.40, 0.40, 0.38))                               # 둑
    for k in range(12):                                                                   # 먼 도시 윤곽 (낮게, y를 조금씩 비껴 놓음)
        x0 = -110 + 20 * k
        v.box(x0, x0 + 14, 150 + 7 * (k % 3), 160 + 6 * (k % 4), 0, 3 + 2.2 * (k % 4), (0.07, 0.09, 0.15 + 0.02 * (k % 3)), jit=0.05)
    v.box(-90, 90, 62.0, 63.2, 3.0, 3.8, (0.12, 0.13, 0.20))                              # 다리
    for k in range(-4, 5):
        v.box(20 * k, 20 * k + 1.2, 62.1, 63.1, -0.3, 3.0, (0.14, 0.15, 0.22))
    for x, y, h in ((-3.2, 3.4, 2.6), (3.4, 4.2, 3.0), (-6.5, 4.8, 3.4), (6.8, 2.8, 2.4)):   # 나무
        v.box(x - 0.15, x + 0.15, y - 0.15, y + 0.15, 0.0, h * 0.55, (0.30, 0.22, 0.16))
        v.box(x - 0.9, x + 0.9, y - 0.9, y + 0.9, h * 0.5, h, (0.18, 0.34, 0.20))
    v.box(1.6, 3.0, 2.2, 2.6, 0.0, 0.45, (0.50, 0.40, 0.30))                               # 벤치
    v.box(1.6, 3.0, 2.5, 2.6, 0.45, 0.95, (0.50, 0.40, 0.30))
    v.box(-1.10, -0.14, 0.95, 1.05, 1.20, 1.56, (0.10, 0.11, 0.16))                        # 시계 판
    v.box(-1.02, -0.97, 0.98, 1.02, 0.0, 1.20, (0.12, 0.12, 0.16))
    v.box(-0.27, -0.22, 0.98, 1.02, 0.0, 1.20, (0.12, 0.12, 0.16))
    v.light(0.0, -1.5, 3.4, 300, (0.75, 0.85, 1.0), 0.5, "ep54_k0")
    v.light(-2.0, 1.0, 3.3, 170, (1.0, 0.8, 0.55), 0.4, "ep54_k1")


def _space(v):
    rs = v.rs
    for k in range(260):                                      # 별 (흰·노랑·파랑 발광 점)
        d = rs.normal(size=3)
        d = d / np.linalg.norm(d)
        r = float(rs.uniform(70, 100))
        s = float(rs.uniform(0.25, 0.6))
        c = ((0.95, 0.95, 1.0), (1.0, 0.9, 0.6), (0.6, 0.75, 1.0))[k % 3]
        x, y, z = d * r
        v.box(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z - s / 2, z + s / 2, c, jit=0, glow=True)
    v.box(-3.0, 3.0, -1.2, 1.2, -1.12, -0.95, (0.14, 0.20, 0.34))                          # 서 있는 유리 판
    v.box(-3.0, 3.0, -1.23, -1.2, -1.0, -0.95, (0.3, 0.8, 1.0), jit=0, glow=True)
    v.light(2.5, -5.0, 3.5, 220, (1.0, 0.97, 0.92), 0.6, "ep54_sp0")


def _panel(v):
    v.floor(-9, 9, -4, 6, (0.14, 0.18, 0.28), 0.5, "check")
    v.wall((-9, 6), (9, 6), 0, 10, (0.16, 0.22, 0.34), 0.5, face=-1)
    for k in range(-7, 8):
        v.box(k - 0.015, k + 0.015, 5.93, 5.97, 0.0, 10.0, (0.10, 0.34, 0.46), jit=0, glow=True)
    v.light(0.0, -1.0, 4.5, 200, (0.9, 0.95, 1.0), 0.8, "ep54_pn0")
    v.light(0.0, -3.0, 2.5, 120, (1.0, 0.95, 0.9), 0.6, "ep54_pn1")


def _village(v):
    """적도 바닷가 마을: 모래·바다·낮은 집·야자."""
    v.floor(-14, 14, -9, 5.0, (0.74, 0.68, 0.52), 0.5)
    v.floor(-14, 14, 5.0, 90, (0.05, 0.18, 0.34), 4.0, z=-0.3)
    v.box(-14, 14, 4.9, 5.1, -0.3, -0.02, (0.66, 0.60, 0.48))
    for x, y, w, h, c in ((-7.0, 3.2, 2.6, 2.2, (0.78, 0.60, 0.46)), (-4.6, 2.4, 2.2, 1.9, (0.50, 0.62, 0.70)),
                          (4.0, 3.0, 2.4, 2.3, (0.76, 0.68, 0.48)), (6.6, 3.8, 2.2, 2.0, (0.52, 0.66, 0.54))):
        v.box(x - w / 2, x + w / 2, y - 1.2, y + 1.2, 0, h, c)
        v.box(x - w / 2 - 0.15, x + w / 2 + 0.15, y - 1.35, y + 1.35, h, h + 0.4, (0.35, 0.24, 0.22))
    for x, y in ((-2.8, 2.6), (2.6, 2.2), (8.0, 1.5), (-9.0, 1.2)):                         # 야자
        v.box(x - 0.1, x + 0.1, y - 0.1, y + 0.1, 0.0, 2.4, (0.40, 0.30, 0.20))
        for q, (dx, dy) in enumerate(((0.5, 0), (-0.5, 0), (0, 0.5), (0, -0.5))):         # 잎마다 높이를 달리해 윗면이 겹치지 않게
            v.box(x + dx - 0.35, x + dx + 0.35, y + dy - 0.35, y + dy + 0.35, 2.4 + 0.03 * q, 2.5 + 0.03 * q, (0.20, 0.42, 0.24))
    v.light(0.0, -1.5, 4.6, 260, (1.0, 0.95, 0.85), 0.5, "ep54_v0")
    v.light(-3.0, -2.0, 3.2, 140, (1.0, 0.85, 0.6), 0.4, "ep54_v1")


def _sets():
    return (("park", _park), ("space", _space), ("panel", _panel), ("village", _village))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 1900, 700, 40, 40


def planet(F, G, BL, cam, center, Rr, tilt, sp, set_="space", rod=True, body=OCEAN, land=True):
    """파란 구(조명 받음) + 앞쪽 반구의 땅·극지 조각(자전 sp, 축 기울기 tilt도) + 축 막대. center = 세트 좌표."""
    ox, oy = OFF[set_]
    cw = np.array((center[0] + ox, center[1] + oy, center[2]), float)
    BL.orbw(cw, 2 * Rr, body)
    if land:
        view = cam["loc"] - cw
        view = view / np.linalg.norm(view)
        Rm = earth_rot(sp, tilt)
        patch = 0.125 * Rr
        for k in LAND_IDX:
            n = Rm @ EARTH_PTS[k]
            if n @ view < 0.04:
                continue
            F.cw(cw + n * (Rr + 0.012), (0.05, patch, patch), LAND_COL[k], rot_n(n))
    if rod:
        G.cw(cw, (Rr * 2.7, 0.03, 0.03), YEL_G, rot_to(axis_of(tilt)))


def _cw(set_, center):
    ox, oy = OFF[set_]
    return np.array((center[0] + ox, center[1] + oy, center[2]), float)


def lat_ring(G, cam, cw, Rr, tilt, lat, col, size=0.05, step=1, nseg=96):
    """위도 lat(도) 고리: 구면 위 발광 조각. step=2면 점선."""
    T = _rmat(0.0, math.radians(tilt), 0.0)
    view = cam["loc"] - cw
    view = view / np.linalg.norm(view)
    cl, sl = math.cos(math.radians(lat)), math.sin(math.radians(lat))
    for q in range(0, nseg, step):
        a = 2 * math.pi * q / nseg
        n = T @ np.array((cl * math.cos(a), cl * math.sin(a), sl))
        if n @ view < 0.06:
            continue
        G.cw(cw + n * (Rr + 0.03), (0.03, size, size), col, rot_n(n))


def cap_fill(G, cam, cw, Rr, tilt, lat0, col, stride=2, outside=False):
    """|위도| ≥ lat0 인 면(극권 안, outside=True면 그 바깥 띠)을 발광 조각으로 채움."""
    T = _rmat(0.0, math.radians(tilt), 0.0)
    view = cam["loc"] - cw
    view = view / np.linalg.norm(view)
    s0 = math.sin(math.radians(lat0))
    for k in range(0, len(EARTH_PTS), stride):
        p = EARTH_PTS[k]
        if (abs(p[2]) >= s0) == outside:
            continue
        n = T @ p
        if n @ view < 0.06:
            continue
        G.cw(cw + n * (Rr + 0.02), (0.03, 0.17 * Rr * math.sqrt(stride / 2.0), 0.17 * Rr * math.sqrt(stride / 2.0)), col, rot_n(n))


def tilt_labels(G, tilt, x, z, cell=0.05, k=1.0):
    wdig(G, num_rows("%.1f" % tilt), x, -0.7, z, cell, YEL_G, k)


# ── 줄별 소품
def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """한강공원: 시계가 00:00부터 빠르게 돌고, 해는 낮게 뜬 채 하늘을 한 번 가로지름. 마지막 0.6초 해가 번쩍."""
    tf = dur - 0.6
    k = clamp(tau / tf)
    boom = ramp(tau, tf, dur - 0.1)
    sky_orb(OR, cam, lerp(-0.85, 0.40, smooth(k)), 0.04, 0.15 * (1.0 + 1.2 * boom), SUN_C)
    m = 1440.0 * k
    park_clock(G, "%02d:%02d" % (int(m // 60) % 24, int(m % 60)))


def props_uranus(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """우주 단면판: 지구 구체가 23.4°에서 97.8°로 눕고 눈금 숫자가 올라감."""
    tilt = lerp(23.44, 97.77, smooth(ramp(u, 0.12, 0.7)))
    planet(F, G, BL, cam, (0.0, 0.0, 0.05), 0.6, tilt, sp_of(t), "space")
    for z in (0.80, 0.94):                                    # 똑바로 선 기준 점선(구 뒤)
        G.b((0.0, 0.9, z), (0.03, 0.03, 0.07), WHT_G)
    tilt_labels(G, tilt, -0.55, 0.74, 0.04, pop(tau - 0.15, 0.3))


FLAGS = [(60, (0.95, 0.25, 0.25)), (190, (0.95, 0.80, 0.25)), (330, (0.30, 0.70, 0.95)), (470, (0.95, 0.95, 0.95)),
         (640, (0.35, 0.80, 0.40)), (790, (0.90, 0.45, 0.15)), (930, (0.75, 0.40, 0.90))]


def _globe_tilt(tau):
    return lerp(23.44, 97.77, smooth(ramp(tau, 0.3, 1.2)))


def props_globe(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """개그 1: 지구본을 눕히자 꽂힌 작은 깃발들이 빙글 돌아 쏟아짐 (아무도 안 다침)."""
    gc, Rg = (0.6, 3.9, 1.35), 0.42
    F.b((0.6, 3.9, 0.45), (0.5, 0.5, 0.9), TABLE_C)
    F.b((0.6, 3.9, 0.92), (0.7, 0.7, 0.06), (0.30, 0.24, 0.20))
    tilt = _globe_tilt(tau)
    planet(F, G, BL, cam, gc, Rg, tilt, 0.6, "panel")
    cw = _cw("panel", gc)
    for j, (k, col) in enumerate(FLAGS):
        td = 0.55 + 0.11 * j
        if tau < td:
            n = earth_rot(0.6, tilt) @ EARTH_PTS[k]
            pos, rot, sw = cw + n * (Rg + 0.01), None, 0.0
        else:
            n0 = earth_rot(0.6, _globe_tilt(td)) @ EARTH_PTS[k]
            s = tau - td
            p0 = cw + n0 * (Rg + 0.01)
            pos = p0 + (n0 * 0.9 + np.array((0.0, 0.0, 0.6))) * s + np.array((0.0, 0.0, -4.9 * s * s))
            pos = np.array((pos[0], pos[1], max(pos[2], 0.04)))
            n, rot, sw = n0, (3.0 * s, 2.0 * s, 1.0 * s), s
        if rot is None:
            F.cw(pos + n * 0.08, (0.16, 0.02, 0.02), (0.85, 0.85, 0.85), rot_to(n))
            F.cw(pos + n * 0.13, (0.02, 0.11, 0.07), col, rot_n(n))
        else:
            F.cw(pos, (0.16, 0.02, 0.02), (0.85, 0.85, 0.85), rot)
            F.cw(pos + 0.05 * np.array((math.sin(sw * 5), 0.0, 0.0)), (0.02, 0.11, 0.07), col, rot)


def props_compare(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """구체 두 개 나란히: 왼 23.44°, 오른 97.77°."""
    planet(F, G, BL, cam, (-0.62, 0.5, 0.5), 0.45, 23.44, sp_of(t), "space")
    planet(F, G, BL, cam, (0.62, 0.5, 0.5), 0.45, 97.77, sp_of(t), "space")
    wdig(G, num_rows("23.44"), -0.62, 0.0, -0.22, 0.04, WHT_G, pop(tau - 0.3, 0.3))
    wdig(G, num_rows("97.77"), 0.62, 0.0, -0.22, 0.04, YEL_G, pop(tau - 0.7, 0.3))


def props_orbit(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """궤도 판: 해 둘레 4자리, 극이 해를 향한 자리(왼·오른)마다 노란 면, 낮 42년 표시."""
    ro = 0.8
    OR.orb((0.0, 0.0, 0.0), 0.40 * (1.0 + 0.04 * math.sin(2 * math.pi * t / 0.9)), SUN_C)
    for q in range(48):
        if tau > 0.1 + 0.025 * q:
            a = 2 * math.pi * q / 48
            G.b((ro * math.cos(a), 0.0, ro * math.sin(a)), (0.035, 0.035, 0.035), (0.5, 0.9, 1.4))
    for x, z in ((-ro, 0.0), (0.0, ro), (ro, 0.0), (0.0, -ro)):
        BL.orb((x, 0.0, z), 0.4, ICE)
        G.b((x, 0.0, z), (0.72, 0.03, 0.03), WHT_G)
    OR.orb((-ro + 0.19, 0.0, 0.0), 0.15 * pop(tau - 0.5, 0.3), YEL_G)
    OR.orb((ro - 0.19, 0.0, 0.0), 0.15 * pop(tau - 1.3, 0.3), YEL_G)
    wdig(G, num_rows("42"), -0.45, -0.2, -0.4, 0.05, YEL_G, pop(tau - 0.7, 0.3))
    wdig(G, num_rows("42"), 0.45, -0.2, -0.4, 0.05, YEL_G, pop(tau - 1.5, 0.3))


def props_assume(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """누운 지구가 24시간 시계와 함께 그대로 돌고, 연구원이 점선 '가정' 표지를 들어 올림."""
    planet(F, G, BL, cam, (0.15, 0.5, 0.3), 0.4, 97.77, sp_of(t) * 1.6, "space")
    cx, cz, rr = 0.75, 0.3, 0.16
    for q in range(12):
        a = 2 * math.pi * q / 12
        G.b((cx + rr * math.sin(a), 0.2, cz + rr * math.cos(a)), (0.03, 0.03, 0.03), WHT_G)
    a = 2 * math.pi * t / 1.2
    G.c((cx + 0.5 * rr * math.sin(a), 0.2, cz + 0.5 * rr * math.cos(a)), (rr, 0.03, 0.03), YEL_G, rot_to(np.array((math.sin(a), 0.0, math.cos(a)))))
    wdig(G, num_rows("24"), cx, 0.2, cz - 0.38, 0.035, YEL_G, pop(tau - 0.3, 0.3))
    d = S.get("rs_s")
    if d is None:
        return
    hx, hy, hz = head_pt(d)
    k = smooth(ramp(tau, 0.2, 0.9))
    cz2 = hz + 0.38 + 0.12 * k
    F.b((hx, hy - 0.05, cz2), (0.7 * k + 0.01, 0.04, 0.45 * k + 0.01), (0.95, 0.92, 0.82))
    if k > 0.9:
        for q in range(8):
            if q % 2 == 0:
                x = hx - 0.33 + 0.09 * q
                for zz in (cz2 - 0.21, cz2 + 0.21):
                    G.b((x + 0.04, hy - 0.08, zz), (0.07, 0.03, 0.03), (3.0, 1.3, 0.4))
        wdig(G, num_rows("24/365"), hx, hy - 0.08, cz2, 0.027, (3.0, 2.4, 0.5), pop(tau - 1.0, 0.3))


def props_circle(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """극권 띠: 점선 66.6° 위로 새 파란 띠가 7.8°까지 확 내려옴."""
    planet(F, G, BL, cam, (0.0, 0.0, 0.0), 0.7, 97.77, sp_of(t) * 0.5, "space")
    cw = _cw("space", (0.0, 0.0, 0.0))
    k = smooth(ramp(u, 0.15, 0.7))
    lat = lerp(66.56, 7.77, k)
    for s in (1.0, -1.0):
        lat_ring(G, cam, cw, 0.7, 97.77, s * 66.56, WHT_G, 0.03, step=2)
        lat_ring(G, cam, cw, 0.7, 97.77, s * lat, BLUE_G, 0.06)


def props_share(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """파란 띠 안이 차오르고 적도 띠 13.5%만 밝게 남음."""
    planet(F, G, BL, cam, (0.0, 0.0, 0.0), 0.7, 97.77, sp_of(t) * 0.5, "space")
    cw = _cw("space", (0.0, 0.0, 0.0))
    lat0 = lerp(90.0, 7.77, smooth(ramp(u, 0.08, 0.75)))
    cap_fill(G, cam, cw, 0.7, 97.77, lat0, FILL_G)
    if u > 0.75:
        cap_fill(G, cam, cw, 0.7, 97.77, 7.77, (2.4, 2.0, 1.0), stride=1, outside=True)
        wdig(G, num_rows("13.5%"), 0.0, -0.8, -0.8, 0.04, YEL_G, pop(tau - 0.75 * dur, 0.3))


MAP_X, MAP_Z, MAP_H, MAP_W = 0.5, 2.25, 1.25, 2.2


def _lat_z(lat):
    return MAP_Z + lat * MAP_H / 90.0


def props_seoul(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """지도판: 서울 점이 파란 극권 안으로 쏙 들어가고 지후가 '?'."""
    F.b((MAP_X, 5.5, MAP_Z), (MAP_W + 0.1, 0.06, 2 * MAP_H + 0.1), PLATE_C)
    for x, z, w, h in ((-0.45, 3.0, 0.7, 0.5), (0.15, 1.9, 0.45, 0.75), (0.85, 3.1, 0.9, 0.55), (1.15, 1.7, 0.4, 0.4), (-0.6, 1.7, 0.4, 0.3)):
        F.b((MAP_X + x, 5.46, z), (w, 0.04, h), (0.36, 0.44, 0.34))
    F.b((MAP_X, 5.452, MAP_Z), (MAP_W, 0.03, _lat_z(7.77) - _lat_z(-7.77)), (0.95, 0.80, 0.40))     # 적도 띠(13.5%)
    for z in (_lat_z(66.56), _lat_z(-66.56)):                                                        # 지금의 극권 점선
        for q in range(0, 11):
            G.b((MAP_X - MAP_W / 2 + 0.1 + q * 0.2, 5.43, z), (0.1, 0.03, 0.02), WHT_G)
    k = smooth(ramp(u, 0.1, 0.55))
    top, bot = _lat_z(90.0), _lat_z(7.77)
    hn = (top - bot) * k
    if hn > 0.01:
        G.b((MAP_X, 5.415, top - hn / 2), (MAP_W, 0.03, hn), FILL_G)
        G.b((MAP_X, 5.415, 2 * MAP_Z - top + hn / 2), (MAP_W, 0.03, hn), FILL_G)
    q = 0.6 + 0.4 * math.sin(2 * math.pi * t / 0.5)
    G.b((MAP_X + 0.3, 5.40, _lat_z(37.5)), (0.12, 0.04, 0.12), (3.0 * q, 1.6 * q, 0.3 * q))
    d = S.get("jh")
    if d is not None:
        hx, hy, hz = head_pt(d)
        wdig(G, DIG["?"], hx, hy - 0.1, hz + 0.4, 0.09, (3.0, 2.4, 0.5), pop(tau - 1.0, 0.3))


def props_zenith(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """한강 정오: 해가 점점 높이 올라 고도 지시선이 75.9°에서 90°로."""
    e = smooth(ramp(u, 0.1, 0.8))
    sx, sy = 0.12, lerp(-0.02, 0.32, e)
    sky_orb(OR, cam, sx, sy, 0.12, SUN_C)
    park_clock(G, "12:00", YEL_G)
    d = S.get("jh")
    if d is None:
        return
    h = to_ndc(cam, wpt("park", head_pt(d)))
    gauge(G, cam, (h[0], h[1] + 0.12), (sx, sy - 0.08), YEL_G)
    alt = lerp(75.9, 90.0, e)
    txt = "90" if alt > 89.95 else "%.1f" % alt
    srows(G, cam, num_rows(txt), (h[0] + sx) / 2 - 0.25, (h[1] + sy) / 2, 0.011, YEL_G, 1.8, pop(tau - 0.2, 0.3))


def props_shadow(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """정오에 지후 그림자가 발밑 한 점으로 줄어듦 (눈높이 근접)."""
    ls = lerp(1.7, 0.34, smooth(ramp(u, 0.15, 0.85)))
    F.b((0.1 - ls / 2 + 0.17, 0.0, 0.025), (ls, 0.38, 0.015), (0.06, 0.07, 0.09))
    park_clock(G, "12:00", YEL_G)


def props_white(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """밤 11시 한강: 도시 불은 꺼졌는데 해가 지평선 위를 돌고 시계 숫자만 빠르게 지나감."""
    sky_orb(OR, cam, lerp(-0.9, 0.9, u), 0.02, 0.12, (3.0, 1.4, 0.4))
    m = 1380.0 + 1440.0 * u
    park_clock(G, "%02d:%02d" % (int(m // 60) % 24, int(m % 60)))


def props_dark(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """한낮 12시인데 별이 뜬 하늘, 가로등이 켜짐."""
    park_clock(G, "12:00", YEL_G)
    for x, y in ((-1.1, 1.8), (1.0, 1.6)):                          # 켜진 가로등
        G.b((x, y, 1.42), (0.20, 0.20, 0.20), (2.8, 2.2, 1.2))
        F.b((x, y, 0.65), (0.08, 0.08, 1.30), (0.20, 0.20, 0.24))


def props_pajama(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """개그 2: 12:00 알람이 울리자 지후가 잠옷(수면 모자)으로 갈아입음, 창밖은 한밤."""
    F.b((0.6, 0.2, 0.3), (0.8, 0.5, 0.6), TABLE_C)
    sh = 0.012 * math.sin(2 * math.pi * t / 0.06) if tau < 1.8 else 0.0
    F.b((0.6 + sh, 0.2, 0.92), (0.62, 0.22, 0.40), (0.80, 0.22, 0.20))
    for sx in (-0.2, 0.2):
        BL.orb((0.6 + sx + sh, 0.2, 1.17), 0.14, (0.85, 0.80, 0.30))
    wdig(G, num_rows("12:00"), 0.6 + sh, 0.08, 0.92, 0.026, YEL_G)
    if tau < 1.8:
        for q in range(8):
            a = 2 * math.pi * q / 8 + 0.4 * t
            G.b((0.6 + 0.55 * math.cos(a), 0.1, 0.92 + 0.45 * math.sin(a)), (0.05, 0.03, 0.05), (3.0, 2.4, 0.6))
    d = S.get("jh")
    if d is not None and tau > 0.5:                                  # 수면 모자
        hx, hy, hz = head_pt(d)
        k = pop(tau - 0.5, 0.25)
        for dz, w, c in ((0.02, 0.56, (0.30, 0.38, 0.75)), (0.14, 0.40, (0.30, 0.38, 0.75)), (0.26, 0.26, (0.30, 0.38, 0.75))):
            F.b((hx - 0.03 * dz * 10, hy, hz + dz * k - 0.12), (w * k + 0.001, w * k + 0.001, 0.14 * k + 0.001), c)
        BL.orb((hx - 0.12, hy, hz + 0.40 * k - 0.12), 0.14 * k, (0.95, 0.95, 0.95))


def props_equator(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """적도 마을: 해뜨기 6시·해지기 18시가 열두 달 내내 같은 줄에 고정되는 달력 판."""
    bx = 0.5
    F.b((bx, 1.8, 1.55), (1.3, 0.06, 1.0), PLATE_C)
    wdig(G, num_rows("6:00"), bx - 0.38, 1.75, 1.8, 0.024, YEL_G)
    wdig(G, num_rows("18:00"), bx - 0.38, 1.75, 1.3, 0.024, ORG_G)
    for q in range(12):
        if tau > 0.2 + 0.1 * q:
            x = bx - 0.02 + q * 0.055
            G.b((x, 1.74, 1.8), (0.04, 0.03, 0.04), YEL_G)
            G.b((x, 1.74, 1.3), (0.04, 0.03, 0.04), ORG_G)
    if tau > 1.6:
        for z in (1.8, 1.3):
            G.b((bx + 0.3, 1.73, z), (0.66, 0.02, 0.012), WHT_G)


def props_lowsun(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """적도 하지 정오: 해가 낮게(7.8°) 걸리고 지후 그림자가 길게 늘어짐."""
    sx, sy = -0.75, -0.14
    sky_orb(OR, cam, sx, sy, 0.10, (3.0, 2.4, 1.0))
    ls = 3.4 * smooth(ramp(tau, 0.2, 1.3))
    F.b((0.1 + ls / 2, 0.0, 0.025), (ls, 0.42, 0.015), (0.40, 0.36, 0.28))
    d = S.get("jh")
    if d is None:
        return
    h = to_ndc(cam, wpt("village", head_pt(d)))
    gauge(G, cam, (h[0], h[1]), (-1.0, h[1]), WHT_G, 10)
    gauge(G, cam, (h[0], h[1]), (sx, sy), YEL_G, 10)
    srows(G, cam, num_rows("7.8"), -0.55, h[1] - 0.12, 0.011, YEL_G, 1.8, pop(tau - 0.8, 0.3))


def noon_alt(lat, day):
    """위도 lat에서 하루(day = 춘분 후 일수)의 한낮 해 높이(도), 0 미만은 0 (계산값)."""
    dec = math.degrees(math.asin(math.sin(math.radians(82.23)) * math.sin(2 * math.pi * day / 365.25)))
    return max(90.0 - abs(lat - dec), 0.0)


LAT_COLS = ((0, (0.5, 1.8, 2.8)), (20, (0.5, 2.6, 1.0)), (40, (3.0, 2.6, 0.5)), (60, (3.0, 1.4, 0.4)), (80, (3.0, 0.5, 0.5)))


def props_seasons(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """달력 판: 위도 5개가 제각각 한낮 해 높이 곡선을 그림."""
    F.b((0.0, 5.5, 2.25), (3.2, 0.06, 2.5), PLATE_C)
    G.b((0.0, 5.43, 1.25), (2.6, 0.02, 0.02), WHT_G)
    G.b((-1.3, 5.43, 2.25), (0.02, 0.02, 2.0), WHT_G)
    prog = smooth(ramp(u, 0.1, 0.85))
    for lat, col in LAT_COLS:
        for q in range(0, 66):
            day = q * 365.25 / 65.0
            if q / 65.0 > prog:
                break
            G.b((-1.3 + 2.6 * q / 65.0, 5.42, 1.25 + noon_alt(lat, day) / 90.0 * 2.0), (0.05, 0.03, 0.05), col)
        wdig(G, num_rows("%d" % lat), -1.46, 5.42, 1.25 + (90 - lat) / 90.0 * 2.0, 0.03, col)


NOW_V, NEW_V = (0.127, 0.305), (0.315, 0.208)          # (극, 적도) 1년 평균 햇빛(태양 상수 S 비율, 계산값)
POLE_C, EQ_C = (3.0, 1.5, 0.3), (0.4, 1.8, 2.8)


def bars(G, x, vals, w, scale, base, labels=True, cell=0.05):
    for dx, v, col in ((-w, vals[0], POLE_C), (w, vals[1], EQ_C)):
        h = max(v * scale, 0.01)
        G.b((x + dx, 5.0, base + h / 2), (w * 0.8, 0.3, h), col)
        if labels:
            wdig(G, num_rows("%.3f" % v), x + dx, 4.8, base + h + 0.3, cell, WHT_G)


def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """17: 반전 — 지금 지구 막대(극<적도)가 확 뒤집혀 누운 지구(극>적도). 18: 두 그래프 나란히."""
    F.b((0.0, 5.0, 0.88), (3.4, 0.6, 0.04), (0.20, 0.22, 0.30))
    base, scale = 0.9, 6.0
    if i == LN["twist"]:
        r = pop(tau - 0.4, 0.5, 2.0)
        vals = tuple(lerp(a, b, r) for a, b in zip(NOW_V, NEW_V))
        bars(G, 0.0, vals, 0.7, scale, base, cell=0.05)
        for q in range(19):
            G.b((-1.1 + 0.12 * q, 4.7, base + NEW_V[1] * scale), (0.06, 0.03, 0.02), WHT_G)
    else:
        bars(G, -0.95, NEW_V, 0.3, scale, base, cell=0.028)
        bars(G, 0.95, NOW_V, 0.3, scale, base, cell=0.028)
        wdig(G, num_rows("1.5"), -0.95, 4.8, base + 2.45, 0.06, YEL_G, pop(tau - 0.3, 0.3))
        wdig(G, num_rows("0.41"), 0.95, 4.8, base + 2.45, 0.06, CYA_G, pop(tau - 0.7, 0.3))


def props_flip(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """연구원이 두 면짜리 막대판을 홱 뒤집음(앞 = 지금 지구, 뒤 = 누운 지구)."""
    bc = np.array((600.0, 5.0, 1.95))
    psi = math.pi * smooth(ramp(tau, 0.35, 1.0))
    c, s = math.cos(psi), math.sin(psi)
    F.cw(bc, (1.9, 0.12, 2.2), PLATE_C, (0.0, 0.0, psi))
    for side, vals in ((-1.0, NOW_V), (1.0, NEW_V)):
        for lx, v, col in ((-0.45 * -side, vals[0], POLE_C), (0.45 * -side, vals[1], EQ_C)):
            h = max(v * 4.5, 0.01)
            ly, lz = 0.09 * side, -1.0 + h / 2
            G.cw(bc + np.array((c * lx - s * ly, s * lx + c * ly, lz)), (0.5, 0.06, h), col, (0.0, 0.0, psi))


def props_impact(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """충돌 가설: 작은 구가 날아와 천왕성에 부딪히자 축이 눕는 점선 가설 그림."""
    th = 97.77 * smooth(ramp(u, 0.46, 0.8)) + 3.0 * math.sin(2 * math.pi * t / 0.5) * ramp(u, 0.46, 0.5) * (1.0 - ramp(u, 0.6, 0.85))
    planet(F, G, BL, cam, (0.25, 0.0, 0.0), 0.5, th, sp_of(t), "space", body=ICE, land=False)
    th_ = tau - 0.42 * dur
    hit = np.array((-0.2, -0.1, 0.18))
    if th_ < 0.0:
        pos = hit + np.array((-1.3, 0.0, 0.8)) * (-th_ / (0.42 * dur)) ** 1.5
    else:
        pos = hit + np.array((-0.9, 0.0, 0.5)) * th_ * 0.8
    BL.orb(tuple(pos), 0.26, ROCK)
    if 0.0 <= th_ < 0.35:
        f = pop(th_, 0.12) * (1.0 - th_ / 0.35)
        OR.orb(tuple(hit), 0.7 * f, (3.0, 2.4, 1.2))
    for q in range(0, 24):                                          # 점선 틀 + 물음표 = 가설 표지
        a = q / 24.0
        for (x, z) in ((-1.05 + 2.1 * a, 0.95), (-1.05 + 2.1 * a, -0.95), (-1.05, -0.95 + 1.9 * a), (1.05, -0.95 + 1.9 * a)):
            if q % 2 == 0:
                G.b((x, 0.6, z), (0.07, 0.03, 0.03), (3.0, 1.3, 0.4))
    wdig(G, DIG["?"], 0.8, 0.5, 0.72, 0.1, (3.0, 2.4, 0.5), pop(tau - 0.3, 0.3))


def props_model(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """노을 공원: 지후가 눕힌 지구본을 다시 23.4°로 세워 놓음."""
    F.b((0.6, 0.35, 0.45), (0.4, 0.4, 0.9), TABLE_C)
    tilt = lerp(97.77, 23.44, smooth(ramp(tau, 0.2, 1.4)))
    planet(F, G, BL, cam, (0.6, 0.35, 1.3), 0.36, tilt, sp_of(t) * 0.7, "park")


def props_ask(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """지후가 카메라를 보며 눕힌 지구본의 적도·극에 두 핀을 꽂음."""
    gc, Rg = (-0.6, 0.3, 1.25), 0.4
    F.b((-0.6, 0.3, 0.4), (0.4, 0.4, 0.8), TABLE_C)
    tilt = 97.77
    planet(F, G, BL, cam, gc, Rg, tilt, sp_of(t) * 0.5, "park")
    cw = _cw("park", gc)
    ax = axis_of(tilt)
    for n, col, t0 in ((np.array((0.0, -1.0, 0.0)), CYA_G, 0.4), (ax, ORG_G, 1.0)):     # 적도 핀 · 극 핀
        k = pop(tau - t0, 0.3)
        G.cw(cw + n * (Rg + 0.1 * k), (0.2 * k + 0.001, 0.02, 0.02), WHT_G, rot_to(n))
        OR.orbw(cw + n * (Rg + 0.22 * k), 0.09 * k, col)


def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """누운 지구 구체 속에서 반짝이는 물음표."""
    planet(F, G, BL, cam, (0.0, 0.0, 0.0), 1.3, 97.77, sp_of(t) * 0.6, "space", rod=False)
    q = 0.65 + 0.35 * math.sin(2 * math.pi * t / 0.9)
    wdig(G, DIG["?"], 0.0, -1.7, 0.0, 0.4, (0.3 * q, 0.6 * q, 3.0 * q), pop(tau - 0.3, 0.3))
    for k in range(24):
        a = 2 * math.pi * _h(k + 20) + 0.4 * t
        r = 1.9 + 0.7 * _h(k + 50)
        s = 0.07 * (0.5 + 0.5 * math.sin(2 * math.pi * (t * 1.3 + _h(k))))
        G.b((r * math.cos(a), -0.4 - 0.5 * _h(k + 80), r * math.sin(a)), (s, s, s), (2.6, 2.4, 1.2))


PROPS = {LN["hook"]: props_hook, LN["uranus"]: props_uranus, LN["globe"]: props_globe, LN["compare"]: props_compare, LN["orbit"]: props_orbit,
         LN["assume"]: props_assume, LN["circle"]: props_circle, LN["share"]: props_share, LN["seoul"]: props_seoul, LN["zenith"]: props_zenith,
         LN["shadow"]: props_shadow, LN["white"]: props_white, LN["dark"]: props_dark, LN["pajama"]: props_pajama, LN["equator"]: props_equator,
         LN["lowsun"]: props_lowsun, LN["seasons"]: props_seasons, LN["twist"]: props_twist, LN["now"]: props_twist, LN["flip"]: props_flip,
         LN["impact"]: props_impact, LN["model"]: props_model, LN["ask"]: props_ask, LN["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR, BL, LT = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off), Items(N_BL, off), []
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN
    P, SP_, PN, V = "park", "space", "panel", "village"

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    jh = {L["hook"]: st(P, 0.1, 0.0, -95, "look_up", seq=[(1.7, "gape")]),
          L["globe"]: st(PN, -0.45, 3.5, -70, "think", seq=[(0.9, "point")]),
          L["seoul"]: st(PN, -0.75, 4.2, -80, "gape", seq=[(1.2, "shock")]),
          L["zenith"]: st(P, 0.0, 0.0, -90, "look_up", seq=[(1.6, "point_up")]),
          L["shadow"]: st(P, 0.0, 0.0, -90, "gape", seq=[(1.3, "point")]),
          L["white"]: st(P, 0.1, 0.0, -100, "film"),
          L["dark"]: st(P, 0.0, 0.0, -90, "look_up", seq=[(1.2, "shock")]),
          L["pajama"]: st(P, -0.3, 0.0, -80, "shock", seq=[(1.2, "smile")]),
          L["equator"]: st(V, -0.5, 0.0, -80, "point", seq=[(1.6, "smile")]),
          L["lowsun"]: st(V, 0.0, 0.0, -90, "gape"),
          L["flip"]: st(PN, -1.15, 4.3, -90, "stand", seq=[(1.1, "shock")]),
          L["model"]: st(P, -0.25, 0.0, -85, "look_up_h"),
          L["ask"]: st(P, 0.1, 0.0, -90, "smile", alt=("smile", "point", 0.9, 0.0))}
    add("jh", 0, JH_SH, JH_PA, jh, extra="hood")
    add("jh_s", 0, JH_SH, JH_PA, {L["compare"]: st(SP_, 0.0, -0.2, 90, "look_up", z=-0.95, sway=(40, 2.2, 0.0))}, scale=0.5, extra="hood")
    add("rs_s", 1, CO_SH, CO_PA, {L["assume"]: st(SP_, -0.6, -0.25, -80, "work", z=-0.95)}, scale=0.6, extra="coat")
    add("rs", 1, CO_SH, CO_PA, {L["flip"]: st(PN, 1.15, 4.3, -100, "work", seq=[(1.4, "smile")])}, extra="coat")
    add("e1", 1, EX_SH[2], (0.20, 0.20, 0.24),
        {L[n]: st(P, -1.3, 2.2, -80, "look_up_h" if n == "white" else "smile") for n in ("hook", "zenith", "white", "dark", "model", "ask")})
    add("e2", 0, EX_SH[0], (0.20, 0.20, 0.24), {L["equator"]: st(V, 1.1, 1.8, -120, "smile"), L["lowsun"]: st(V, 1.0, 1.8, -120, "look_up_h")})
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
NIGHT_SKY = ((0.012, 0.025, 0.085), (0.06, 0.10, 0.22), 1.0)
DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
HOOK_SKY = ((0.14, 0.18, 0.44), (0.95, 0.56, 0.32), 0.3)
TWI_SKY = ((0.06, 0.07, 0.22), (0.80, 0.38, 0.30), 0.5)
DUSK_SKY = ((0.14, 0.10, 0.30), (0.95, 0.50, 0.35), 0.5)
SPACE_SKY = ((0.003, 0.004, 0.014), (0.010, 0.013, 0.034), 1.8)
ROOM_SKY = ((0.04, 0.05, 0.09), (0.10, 0.12, 0.18), 0.0)
PARK_SKY = {LN["hook"]: HOOK_SKY, LN["zenith"]: DAY_SKY, LN["shadow"]: DAY_SKY, LN["white"]: TWI_SKY, LN["model"]: DUSK_SKY}


def sky(t):
    i = line_at(t)
    s = cam_of(t)["set"]
    if s == "space":
        return SPACE_SKY
    if s == "panel":
        return ROOM_SKY
    if s == "village":
        return DAY_SKY
    return PARK_SKY.get(i, NIGHT_SKY)


def env(i, st_, u=0.0):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=0.9, sun_col=(0.55, 0.65, 1.0), sun_rot=(55, 0, 35), amb=0.32, amb_col=(0.45, 0.55, 0.85), lt={})
    if st_ == "park":
        e["lt"] = {"ep54_k0": 300.0, "ep54_k1": 170.0}
        if i == LN["hook"]:
            e.update(sun=2.4, sun_col=(1.0, 0.62, 0.30), sun_rot=(80, 0, 180), amb=0.40, amb_col=(0.75, 0.60, 0.55))
        elif i in (LN["zenith"], LN["shadow"]):
            e.update(sun=3.2, sun_col=(1.0, 0.96, 0.88), sun_rot=(6, 0, 0), amb=0.55, amb_col=(0.60, 0.70, 0.90),
                     lt={"ep54_k0": 80.0, "ep54_k1": 50.0})
        elif i == LN["white"]:
            e.update(sun=1.8, sun_col=(1.0, 0.50, 0.25), sun_rot=(82, 0, 200), amb=0.32, amb_col=(0.55, 0.42, 0.60))
        elif i == LN["model"]:
            e.update(sun=2.0, sun_col=(1.0, 0.58, 0.35), sun_rot=(72, 0, 20), amb=0.34, amb_col=(0.70, 0.52, 0.66))
    elif st_ == "village":
        e["lt"] = {"ep54_v0": 260.0, "ep54_v1": 140.0}
        if i == LN["lowsun"]:
            e.update(sun=3.0, sun_col=(1.0, 0.92, 0.75), sun_rot=(82.2, 0, -90), amb=0.45, amb_col=(0.62, 0.68, 0.82))
        else:
            e.update(sun=2.8, sun_col=(1.0, 0.95, 0.85), sun_rot=(25, 0, -90), amb=0.50, amb_col=(0.62, 0.68, 0.82))
    elif st_ == "space":
        e.update(sun=4.2, sun_col=(1.0, 0.96, 0.9), sun_rot=(55, 0, 60), amb=0.10, amb_col=(0.30, 0.36, 0.62), lt={"ep54_sp0": 220.0})
    elif st_ == "panel":
        e.update(sun=0.4, sun_col=(1.0, 0.96, 0.9), amb=0.45, amb_col=(0.70, 0.76, 0.92), lt={"ep54_pn0": 200.0, "ep54_pn1": 120.0})
    return e


# 번쩍 (줄, 줄 시작 후 초, 세기, 길이 초): 훅 끝 해가 번쩍, 반전 줄 시작
def _flashes():
    return [(LN["hook"], _FLASH_AT, 0.35, 0.18), (LN["twist"], 0.3, 0.2, 0.16)]


WARM = np.array((1.0, 0.95, 0.86), np.float32)


def flash_level(t):
    a = 0.0
    for i, tau0, peak, dur in _flashes():
        t0 = shot_span(i)[0] + tau0
        a = max(a, peak * clamp((t - t0 + 0.02) / 0.03) * (1.0 - clamp((t - t0 - 0.01) / dur)))
    return a


def postfx(img, t):
    """번쩍(전체 화면): 훅 끝 해가 번쩍일 때, 반전 줄 시작."""
    a = flash_level(t)
    if a > 0.0:
        img = img + (WARM - img) * np.float32(a)
    return img


_W = {}


def _world():
    """캐릭터 목록과 원형(자세·머리·꾸밈) 번호표 — 블렌더 없이 계산."""
    if not _W:
        C = cast()
        keys = set()
        for c in C:
            for a in c["at"].values():
                for s in ([x for _, x in a] if isinstance(a, list) else [a]):
                    for p in _poses_of(s):
                        keys.add((p, c["hair"], c["extra"]))
        keys = sorted(keys)
        _W.update(C=C, keys=keys, PI={k: n for n, k in enumerate(keys)})
    return _W


def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·소품 점 배열, 카메라, 조명."""
    W = _world()
    i = line_at(t)
    a, b = shot_span(i)
    dur = max(b - a, 1e-3)
    tau = max(t - a, 0.0)             # 줄 시작 0.02초 전부터 그 줄로 치므로 음수 방지
    u = min(tau / dur, 1.0)
    cam = cam_pose(i, tau, u)
    S, P, R, CO, C2, SC, PO = {}, [], [], [], [], [], []
    for c in W["C"]:
        d = state_of(c, i, u, tau, dur, t)
        CO.append(c["shirt"])
        C2.append(c["pants"])
        if d is None or d["set"] != cam["set"]:
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
        PO.append(W["PI"][(d["pose"], c["hair"], c["extra"])])
    F, G, OR, BL, LT = props(i, tau, dur, u, S, t, cam)
    return dict(i=i, tau=tau, u=u, set=cam["set"], cam=cam, A=S, P=P, R=R, CO=CO, C2=C2, SC=SC, PO=PO, F=F, G=G, OR=OR, BL=BL, LT=LT,
                env=env(i, cam["set"], u))

# ───────────────────────── Blender 원형(프로토) ─────────────────────────
def build(ctx):
    from engine import bkit as K
    v = X.Vox(54)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.45, 0.55, 0.85), ambient_strength=0.32, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 0.9, name="ep54_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep54_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep54_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep54_fx", K.proto(ctx, "ep54_p_fx", cube(), [K.mat_inst("ep54_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep54_glow", K.proto(ctx, "ep54_p_glow", cube(), [_mat_glow("ep54_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep54_orb", K.proto(ctx, "ep54_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep54_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep54_bl", K.proto(ctx, "ep54_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep54_m_bl", 0.8)]),
                     N_BL, vector_scale=True)
    for ob in (gl, orb):                                              # 발광 상자·달이 햇빛을 가리지 않게
        try:
            ob.visible_shadow = False
        except AttributeError:
            pass

    def upd(t, f):
        S = frame_state(t)
        c = S["cam"]
        cam.set(tuple(float(q) for q in c["tgt"]), c["az"], c["el"], c["dist"], c["lens"], shift=c["shift"])
        e = S["env"]
        sun.data.energy = e["sun"]
        sun.data.color = e["sun_col"]
        sun.rotation_euler = tuple(math.radians(q) for q in e["sun_rot"])
        ctx.set_ctl("ambient", e["amb"])
        ctx.set_rgb("ambient_col", e["amb_col"])
        for name, ob in lights.items():
            ob.data.energy = e["lt"].get(name, 0.0)
        K.set_points(people, S["P"], scale=S["SC"], rot=S["R"], col=np.array(S["CO"], np.float32),
                     colors={"col2": np.array(S["C2"], np.float32)}, pose=S["PO"])
        for ob, items in ((fx, S["F"]), (gl, S["G"]), (orb, S["OR"]), (bl, S["BL"])):
            Pp, Sc, Sz, Rt, Co = items.arrays()
            K.set_points(ob, Pp, scale=Sc, size=Sz, rot=Rt, col=Co)

    ctx.on_frame(upd)
