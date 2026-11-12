"""EP56 만약에 세상의 모든 개미가 한곳에 모인다면? (STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

컷 흐름: 훅(사람 1명당 250만 마리 카운터) → 바로(20경 마리·일렬 1,000억 km·한 변 460m 정육면체·관측대에서 봄·이름 붙은 종 1만 5,700+·열대에 삶)
→ 1주 뒤(숲 바닥 굴이 비고 씨앗 길이 끊김·흙 구멍·과자 개그) → 1년 뒤(한 군체 6,000km·다른 군체와 다툼)
→ 반전·지금(무게는 사람의 20%·야생 새·짐승보다 무거움·사람은 개미의 5배) → 20경은 최소·자료 부족 → 돌려보냄 → 질문 → 댓글 → 다음 편.
특수효과 구현: 개미 점 = 상자 인스턴스(정육면체는 큰 상자 1개 + 표면을 기는 점 300개), 훅 카운터·큰 글자 = 도트 발광 상자(srows·wdig),
일렬 = 우주 판 점선 + 오가는 점, 저울 = 기울어지는 보 + 접시, 지도 = 칸 상자. 개미는 사람 쪽으로 오지 않고 지후·연구원은 늘 안전한 자리.
효과음: 묶음 '찰싹', 컷 '휙', 훅 끝 숫자 번쩍·14번 줄 반전 '쿵'.
화면 속 크기(정육면체 40m 모형, 종 칸 1칸=약 157종, 지도 칸)는 모양을 보이려는 그림 크기이며 실제 비율이 아니다.

근거(설명란): ※ '전 세계 개미를 한곳에 순간이동시켰다'는 가정의 상상 시나리오. 개미 크기(몸길이 5mm·부피 5mm³)는 가정값, 바이오매스는 건조 탄소 기준.
· 지구의 개미는 최소 약 20경(2×10¹⁶) 마리, 465개 현장 연구 합산 추정(중앙아프리카·아시아는 자료 거의 없음) · Schultheiss 외, PNAS 119 (2022), doi:10.1073/pnas.2201550119 [줄 1·17·18]
· 사람 1명당 개미 약 250만 마리 = 2×10¹⁶ ÷ 80억 = 2.5×10⁶ (계산값, 세계 인구 80억 근사. 82억 명이면 약 244만) [줄 0]
· 일렬로 세우면 2×10¹⁶ × 0.005m = 10¹⁴m = 10¹¹km(1,000억 km) ÷ 1.496×10⁸km(지구–태양) ≈ 668, 약 670배 (계산값, 5mm 가정) [줄 3]
· 한곳에 모으면 2×10¹⁶ × 5mm³ = 10⁸m³, 세제곱근 ≈ 464m → 한 변 약 460m 정육면체 (계산값, 5mm³ 가정. 3mm³면 391m, 10mm³면 585m) [줄 4]
· 이름 붙은 개미 종·아종 1만 5,700+, 아직 이름 없는 것도 비슷한 수로 추정 · Schultheiss 외, PNAS (2022) [줄 6]
· 이름 붙은 종의 거의 3분의 2가 열대림·사바나 두 생태계에 삶 · Schultheiss 외, PNAS (2022) 보도(Phys.org) [줄 7]
· 개미가 씨앗을 옮기는 식물 최소 약 1만 1,000종(속씨식물의 약 4.5%) · Lengyel 외, Perspectives in Plant Ecology, Evolution and Systematics 12:43 (2010) [줄 9]
· 개미는 굴을 파 흙의 구멍(공극)을 늘리는 생태계 공학자(수치 없음) · Folgarait, Biodiversity and Conservation 7:1221 (1998) [줄 10]
· 유럽 지중해·대서양 연안의 아르헨티나개미는 약 6,000km에 걸친 한 초군체(조사 33곳 6,004km) · Giraud·Pedersen·Keller, PNAS 99:6075 (2002) [줄 12]
· 같은 유럽의 서로 다른 두 초군체는 서로 공격성을 보임 · Giraud 외, PNAS (2002) [줄 13]
· 개미 전체 바이오매스는 건조 탄소 약 1,200만 t = 사람의 약 20%, 야생 조류·포유류를 합친 것보다 큼 (12 ÷ 0.2 = 사람 약 6,000만 t, 계산값) · Schultheiss 외, PNAS (2022) [줄 14·15]
· 사람 바이오매스는 개미의 5배 = 1 ÷ 0.2 (계산값) [줄 16]
· 연출용(사실 개수에 안 셈): 2번 한 마리 인사, 5번 관측대에서 보기, 8·11번 숲 바닥·과자, 19번 돌려보내기, 20번 해질녘 숲
[확인중] 1. F1·F5·F6·F11 PNAS 원문 직접 열람 실패(403·reCAPTCHA) → Phys.org·Mongabay·뷔르츠부르크대 보도 경유.
[확인중] 2. F3·F4 개미 몸길이 5mm·부피 5mm³는 가정값(출처 없음, 종마다 편차). 화면에 '가정' 표기.
[확인중] 3. F2 세계 인구 80억은 근사값(UN 2022 80억, 현재 약 82억).
[확인중] 4. F8 Folgarait 1998 원문 대조 안 함(요약만 확인). 수치 없이 '흙 구멍을 늘린다'만 씀.
[확인중] 5. F9·F10 Giraud 2002 원문 대조 안 함(초록·2차 요약). '서로 다른 초군체끼리 공격'은 유럽 두 초군체 비교에 한정.
[확인중] 6. 개미가 한곳에 모였을 때 숲 변화(1주·1년 뒤) 문헌 없음 → 8~11번은 '씨앗 옮기는 길이 끊김'까지의 연출뿐, 결과 단정 안 함.
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"plain": (0, 0), "space": (300, 0), "panel": (600, 0), "forest": (900, 0), "scale": (1200, 0)}
DECK = 0.5           # 관측대 윗면 높이: 지후는 늘 관측대(높은 지대) 위
NAMES = ("hook", "gather", "wave", "beeline", "cube", "watch", "species", "tropic", "quiet", "seeds", "soil", "snack", "colony", "clash",
         "twist", "wild", "five", "plus", "gap", "back", "calm", "ask", "comment", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}

# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
# ease="out": 처음에 빨리 움직이고 천천히 멈춤(훅)
PANEL = ("panel", (0.0, 5.5, 2.9), -90, 2, 15.0, 26, 0.93, 0, 0.06)
LINES = [
    dict(d=3.0, sub="사람 1명당\n개미 250만 마리", ease="out", shot=("plain", (0.05, 0.0, 1.95), -90, 2, 4.4, 28, 0.78, 3, 0.10)),
    dict(d=3.0, sub="개미는 지구에\n약 20경 마리", shot=("plain", (0.0, 70.0, 2.4), -90, 0.3, 80.0, 28, 0.97, 0, 0.10)),
    dict(d=2.6, sub="지후는 한 마리에게\n인사해요", shot=("plain", (0.0, 1.3, 1.7), 5, 3, 4.6, 28, 0.9, -4, 0.06)),
    dict(d=3.0, sub="일렬로 세우면\n1,000억 km", shot=("space", (0.0, 0.0, 0.0), -90, 2, 15.0, 26, 0.93, 0, 0.04)),
    dict(d=3.0, sub="한곳에 모으면\n한 변 460m", shot=("plain", (0.0, 100.0, 3.0), -90, 0.5, 140.0, 26, 0.9, 0, 0.10)),
    dict(d=2.6, sub="관측대에서\n검은 덩어리를 봐요", shot=("plain", (0.0, 30.0, 2.4), -90, 0.3, 36.0, 28, 0.97, 0, 0.10)),
    dict(d=3.0, sub="이름 붙은 종만\n1만 5,700+", shot=PANEL),
    dict(d=3.0, sub="종의 거의 3분의 2는\n열대에 살아요", shot=("panel", (0.0, 5.5, 2.9), -90, 2, 16.0, 26, 0.92, 0, 0.06)),
    dict(d=2.6, sub="1주 뒤,\n숲 바닥이 조용해요", shot=("forest", (-3.2, 1.8, 0.9), -35, 8, 5.8, 28, 0.88, 6, 0.05)),
    dict(d=3.0, sub="씨앗을 옮기는 식물\n1.1만 종", shot=("forest", (0.0, 1.5, 0.45), -90, 6, 8.3, 28, 0.92, 0, 0.10)),
    dict(d=3.0, sub="굴을 파\n흙 구멍을 늘려요", shot=("forest", (0.0, 1.6, 1.7), -90, 3, 9.5, 28, 0.92, 0, 0.06)),
    dict(d=2.6, sub="피크닉 과자가\n그대로예요", shot=("forest", (0.35, 1.7, 1.15), -75, 4, 8.0, 28, 0.9, 5, 0.0)),
    dict(d=3.0, sub="한 군체가\n6,000km에 걸쳐요", shot=("panel", (0.0, 5.5, 2.9), -90, 2, 16.0, 26, 0.93, 0, 0.06)),
    dict(d=2.8, sub="다른 군체와는\n다퉈요", shot=("panel", (-1.2, 5.5, 2.9), -90, 2, 9.5, 26, 0.9, 0, 0.06)),
    dict(d=3.2, sub="20경 마리 무게는\n사람의 20%", shot=("scale", (0.0, 0.6, 1.7), -90, 2, 9.5, 28, 0.9, 0, 0.0)),
    dict(d=3.0, sub="야생 새·짐승 전부보다\n무거워요", shot=("scale", (0.0, 0.6, 2.2), -90, 2, 14.5, 26, 0.92, 0, 0.08)),
    dict(d=2.6, sub="사람이 개미보다\n5배 무거워요", shot=("scale", (0.0, 0.6, 2.2), -90, 2, 14.5, 26, 0.92, 0, 0.08)),
    dict(d=3.0, sub="20경은\n'최소'라는 뜻이에요", shot=PANEL),
    dict(d=2.6, sub="중앙아프리카·아시아\n자료 부족", shot=("panel", (0.0, 5.5, 2.9), -90, 2, 16.0, 26, 0.92, 0, 0.06)),
    dict(d=2.6, sub="개미를\n숲으로 돌려보내요", shot=("plain", (0.0, 70.0, 2.4), -90, 0.3, 80.0, 26, 0.98, 0, 0.10)),
    dict(d=3.0, sub="작은 개미가\n숲을 움직여요", shot=("forest", (0.0, 0.2, 1.3), -90, 3, 3.6, 28, 0.88, 4, 0.10)),
    dict(d=3.0, sub="개미 20경 마리,\n어디에 모을까요?", shot=("plain", (0.15, 0.0, 1.95), -90, 3, 4.8, 28, 0.9, 0, 0.10)),
    dict(d=2.4, sub="댓글로 알려 주세요.", shot=("plain", (0.0, 0.8, 1.9), -90, 3, 3.3, 30, 0.92, 0, 0.10)),
    dict(d=3.2, sub="구독하면 다음 '만약에'를\n놓치지 않아요.", shot=("plain", (0.0, 5.0, 2.2), -90, 3, 9.0, 26, 0.9, 0, 0.08)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="가정", label="사람 1명당 개미는", big="250만 마리", label_color="blue", big_color="yellow"),
    dict(at="gather", badge="바로", title="지구의 개미", big="약 20경 마리", big_color="yellow"),
    dict(at="beeline", badge="바로", title="일렬로 세우면(5mm 가정)", big="1,000억 km", big_color="cyan"),
    dict(at="cube", badge="바로", title="한곳에 모으면(5mm³ 가정)", big="한 변 460m", big_color="orange"),
    dict(at="species", badge="바로", title="이름 붙은 개미", big="1만 5,700종+", big_color="yellow"),
    dict(at="tropic", badge="바로", title="종의 약 2/3가 사는 곳", big="열대림·사바나", big_color="green"),
    dict(at="quiet", badge="1주 뒤", title="숲 바닥 개미 굴", big="텅 빈 굴", big_color="cyan"),
    dict(at="seeds", badge="1주 뒤", title="개미가 씨앗을 옮기는 식물", big="약 1.1만 종", big_color="green"),
    dict(at="soil", badge="1주 뒤", title="굴을 파는 생태계 공학자", big="흙 구멍 늘림", big_color="white"),
    dict(at="snack", badge="1주 뒤", title="피크닉 과자는", big="그대로", big_color="white"),
    dict(at="colony", badge="1년 뒤", title="아르헨티나개미 한 군체", big="6,000km", big_color="orange"),
    dict(at="clash", badge="1년 뒤", title="다른 군체끼리는", big="서로 공격성", big_color="orange"),
    dict(at="twist", badge="지금", title="20경 마리의 무게는", big="사람의 약 20%", big_color="red", note="건조 탄소 기준", note_color="cyan"),
    dict(at="wild", badge="지금", title="야생 새·짐승 전부보다", big="더 무거워요", big_color="red", note="건조 탄소 기준", note_color="cyan"),
    dict(at="five", badge="지금", title="사람 바이오매스는", big="개미의 5배", big_color="white"),
    dict(at="plus", badge="지금", title="20경은 최소 추정", big="20경 +", big_color="cyan"),
    dict(at="gap", title="중앙아프리카·아시아", big="자료 부족", big_color="cyan"),
    dict(at="back", title="모인 개미를\n{cyan}숲으로 돌려보내요{/}", title_size=64),
    dict(at="calm", title="작은 개미가\n{cyan}숲을 움직여요{/}", title_size=64),
    dict(at="ask", title="개미 20경 마리를\n{cyan}어디에 모을까요?{/}", title_size=64),
    dict(at="teaser", badge="다음 편", title="다음 '만약에'는\n{cyan}무엇일까요?{/}", title_size=70),
]
TWIST = LN["twist"]  # '20경 마리 무게는 사람의 20%' 줄 — 음악이 바뀌는 곳
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
META = {"id": "ep56", "title": "만약에 세상의 모든 개미가 한곳에 모인다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"style": "pop", "key": "G", "mode": "major", "bpm": 112, "seed": 561, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, [[LINES[0]["d"] - 0.6, "thud", 0.6], [STARTS[TWIST] + 0.1, "thud", 0.75]])}}
GRADE = {"exposure": 1.0, "bloom": 0.12, "bloom_thr": 1.4, "vignette": 0.14}


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


def earth_rot(sp):
    return _rmat(math.radians(-23.4), 0.0, 0.0) @ _rmat(0.0, 0.0, sp)


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




def earth_items(F, BL, cam, center, R, sp, set_="space"):
    """지구: 파란 구(조명 받음) + 앞쪽 반구에 보이는 땅·극지 조각(자전 sp). center = 세트 좌표."""
    ox, oy = OFF[set_]
    cw = np.array((center[0] + ox, center[1] + oy, center[2]), float)
    BL.orbw(cw, 2 * R, OCEAN)
    view = cam["loc"] - cw
    view = view / np.linalg.norm(view)
    Rm = earth_rot(sp)
    patch = 0.125 * R
    for k in LAND_IDX:
        n = Rm @ EARTH_PTS[k]
        if n @ view < 0.04:
            continue
        F.cw(cw + n * (R + 0.012), (0.05, patch, patch), LAND_COL[k], rot_n(n))

def arrow_w(G, x0, x1, z, col, y=-0.1, th=0.10):
    """세트에 서 있는 가로 화살표 (x0에서 x1로, 머리는 x1 쪽)."""
    L, s = abs(x1 - x0), (1.0 if x1 > x0 else -1.0)
    hl = 0.34
    G.b(((x0 + x1) / 2 - s * hl / 2, y, z), (max(L - hl, 0.02), 0.04, th), col)
    for q, h in enumerate((0.34, 0.22, 0.10)):
        G.b((x1 - s * (hl * (q + 0.5) / 3.0), y, z), (hl / 3.0 * 0.95, 0.04, h), col)


def hud_arrow(G, cam, nx, ny, dirn, length_h, col):
    """화면에 붙는 가로 화살표 (dirn=+1 오른쪽, −1 왼쪽, length_h = 화면 높이 비율)."""
    th = 0.012
    hl = 0.03
    sprite(G, cam, nx - dirn * hl / 2 / 0.28125, ny, max(length_h - hl, 0.01), th, col, 1.8, 0.012)
    for q, h in enumerate((0.032, 0.022, 0.012)):
        sprite(G, cam, nx + dirn * (length_h / 2 - hl * (q + 0.5) / 3.0) / 0.28125, ny, hl / 3.0 * 0.95, h, col, 1.8, 0.012)



# ───────────────────────── 색 · 숫자 ─────────────────────────
ANT = (0.045, 0.04, 0.04)                     # 개미 점(검정)
ANT_HI = (0.22, 0.15, 0.10)                   # 정육면체 표면을 기는 점(조금 밝게)
CUBE_C = (0.05, 0.045, 0.04)
HUM_C = (0.80, 0.80, 0.84)                    # 사람 막대·아이콘(채도 낮음)
OCEAN = (0.08, 0.26, 0.68)
SUN_C = (3.0, 1.9, 0.5)
CYAN_G = (0.6, 2.4, 2.6)
YEL_G = (3.0, 2.4, 0.6)
SEED_C = (0.78, 0.62, 0.30)
SOIL_C = (0.42, 0.28, 0.16)
JH_SH, JH_PA = (0.58, 0.32, 0.80), (0.15, 0.18, 0.30)      # 지후: 보라 후드 · 짧은 머리 · 남색 바지
CO_SH, CO_PA = (0.93, 0.93, 0.91), (0.22, 0.24, 0.30)      # 연구원: 흰 가운 (extra='coat')
EX_SH = [(0.62, 0.40, 0.38), (0.66, 0.60, 0.42), (0.42, 0.55, 0.45)]
DIG.update({"T": ["###", ".#.", ".#.", ".#.", ".#."], "N": ["###", "#.#", "#.#", "#.#", "#.#"], "c": ["###", "#..", "#..", "#..", "###"]})


def wdig(G, rows, cx, y, cz, cell, col, k=1.0):
    """세트에 서 있는 도트 글자 (−y쪽을 보는 면, 가운데 맞춤): 칸 하나 = 발광 상자."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        G.b((cx + ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, y, cz + (h / 2.0 - r - 0.5) * cell * k),
            (((c1 - c + 1) - 0.06) * cell * k, 0.03, cell * 0.94 * k), col)


def sp_of(t):
    return 0.35 * t


# ───────────────────────── 세트 ─────────────────────────
def _plain(v):
    """평원 + 관측대 + 먼 언덕. 정육면체·개미 점은 소품(움직이므로)."""
    v.floor(-90, 90, -60, 180, (0.34, 0.54, 0.26), 4.0)
    v.box(-3.4, 3.4, -2.6, 2.0, 0.0, DECK, (0.52, 0.38, 0.25))                         # 관측대(높은 지대)
    for x in np.arange(-3.3, 3.4, 1.1):                                                # 난간
        v.box(x - 0.05, x + 0.05, 1.9, 2.0, DECK, 1.3, (0.56, 0.42, 0.28))
    v.box(-3.4, 3.4, 1.92, 1.98, 1.25, 1.32, (0.60, 0.45, 0.30), jit=0.02)
    for k, (x, y, h) in enumerate(((-9.0, 7.0, 4.5), (10.0, 9.0, 5.0), (-14.0, 22.0, 6.0), (15.0, 26.0, 5.5))):   # 가까운 나무
        X.tree(v, x, y, h)
    for k in range(8):                                                                 # 먼 언덕 (y를 조금씩 비껴 놓음)
        x0 = -100 + 28 * k
        v.box(x0, x0 + 36, 150 + 7 * (k % 3), 175 + 6 * (k % 2), 0, 7 + 4 * (k % 4), (0.20, 0.38, 0.22 + 0.02 * (k % 3)), jit=0.05)


def _space(v):
    for k in range(260):                                      # 별 (흰·노랑·파랑 발광 점)
        d = v.rs.normal(size=3)
        d = d / np.linalg.norm(d)
        r = float(v.rs.uniform(70, 100))
        s = float(v.rs.uniform(0.25, 0.6))
        c = ((0.95, 0.95, 1.0), (1.0, 0.9, 0.6), (0.6, 0.75, 1.0))[k % 3]
        x, y, z = d * r
        v.box(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z - s / 2, z + s / 2, c, jit=0, glow=True)
    v.light(2.5, -5.0, 3.5, 220, (1.0, 0.97, 0.92), 0.6, "ep56_sp0")


def _panel(v):
    v.floor(-9, 9, -4, 6, (0.14, 0.18, 0.28), 0.5, "check")
    v.wall((-9, 6), (9, 6), 0, 10, (0.16, 0.22, 0.34), 0.5, face=-1)
    for k in range(-7, 8):
        v.box(k - 0.015, k + 0.015, 5.93, 5.97, 0.0, 10.0, (0.10, 0.34, 0.46), jit=0, glow=True)
    v.light(0.0, -1.0, 4.5, 200, (0.9, 0.95, 1.0), 0.8, "ep56_pn0")
    v.light(0.0, -3.0, 2.5, 120, (1.0, 0.95, 0.9), 0.6, "ep56_pn1")


MOUND_X = -3.2                                                                          # 개미 굴 둔덕 가운데 x


def _forest(v):
    v.floor(-24, 24, -14, 34, (0.20, 0.40, 0.17), 2.0)
    for x, y, h in ((-9, 9, 5), (8, 11, 4.5), (-14, 16, 6), (13, 18, 5.5), (-5, 22, 5), (5, 26, 6.5), (-16, 28, 5.5), (16, 30, 5), (0, 32, 6)):
        X.tree(v, x, y, h)
    m = MOUND_X
    v.box(m - 1.6, m + 1.6, 2.5, 5.5, 0.0, 0.55, (0.46, 0.32, 0.20))                    # 개미 굴 둔덕 + 구멍
    v.box(m - 1.1, m + 1.1, 3.0, 5.0, 0.55, 1.05, (0.44, 0.30, 0.19))
    v.box(m - 0.6, m + 0.6, 3.5, 4.5, 1.05, 1.45, (0.42, 0.29, 0.18))
    v.box(m - 0.35, m + 0.35, 2.46, 2.5, 0.12, 0.5, (0.05, 0.04, 0.03), jit=0)


def _scale(v):
    v.floor(-9, 9, -6, 8, (0.80, 0.82, 0.86), 1.0)
    v.wall((-9, 8), (9, 8), 0, 10, (0.50, 0.66, 0.84), 1.0, face=-1)
    v.light(0.0, -1.0, 5.5, 330, (1.0, 0.97, 0.92), 0.8, "ep56_sc0")
    v.light(0.0, -4.0, 3.0, 150, (1.0, 0.95, 0.9), 0.6, "ep56_sc1")


def _sets():
    return (("plain", _plain), ("space", _space), ("panel", _panel), ("forest", _forest), ("scale", _scale))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 2600, 900, 40, 40


def ant(F, x, y, z, yaw_deg, s=0.28, wig=0.0, col=ANT):
    """주인공급 개미 한 마리(상자 11개). yaw_deg 방향을 봄, wig = 더듬이 흔들림 -1~1."""
    a = math.radians(yaw_deg)
    c, sn = math.cos(a), math.sin(a)

    def at(fx, fy=0.0, fz=0.0):
        return (x + s * (fx * c - fy * sn), y + s * (fx * sn + fy * c), z + s * fz)
    F.c(at(-0.62, 0, 0.05), (s * 0.62, s * 0.5, s * 0.45), col, (0.0, 0.0, a))
    F.c(at(0.0, 0, 0.0), (s * 0.4, s * 0.34, s * 0.34), col, (0.0, 0.0, a))
    F.c(at(0.46, 0, 0.05), (s * 0.36, s * 0.4, s * 0.38), col, (0.0, 0.0, a))
    for fx in (-0.1, 0.05, 0.2):
        F.c(at(fx, 0, -0.14), (s * 0.05, s * 0.9, s * 0.05), col, (0.0, 0.0, a))
    for side in (-1, 1):
        F.c(at(0.88, side * 0.22, 0.2), (s * 0.5, s * 0.05, s * 0.05), col, (0.0, 0.0, a + side * (0.55 + 0.45 * wig)))


def figure(F, x, y, z, s=1.0, col=HUM_C):
    """사람 아이콘(몸통 + 머리, 상자 2개)."""
    F.b((x, y, z + 0.32 * s), (0.34 * s, 0.22 * s, 0.64 * s), col)
    F.b((x, y, z + 0.78 * s), (0.26 * s, 0.24 * s, 0.26 * s), (0.88, 0.76, 0.66))


def animal(F, x, y, z, kind, s=1.0):
    """야생 새(kind 0)·짐승(kind 1) 아이콘(채도 낮음)."""
    if kind == 0:
        F.b((x, y, z + 0.15 * s), (0.34 * s, 0.2 * s, 0.2 * s), (0.62, 0.56, 0.40))
        F.b((x + 0.2 * s, y, z + 0.26 * s), (0.14 * s, 0.14 * s, 0.14 * s), (0.62, 0.56, 0.40))
    else:
        F.b((x, y, z + 0.28 * s), (0.62 * s, 0.26 * s, 0.28 * s), (0.50, 0.42, 0.34))
        F.b((x + 0.38 * s, y, z + 0.38 * s), (0.22 * s, 0.2 * s, 0.2 * s), (0.50, 0.42, 0.34))
        F.b((x, y, z + 0.07 * s), (0.5 * s, 0.2 * s, 0.14 * s), (0.30, 0.26, 0.22))


# ── 평원: 큰 정육면체 · 개미 점
CUBE_Y0, CUBE_S = 80.0, 40.0


def cube_props(F, G, t, k=1.0, label=True):
    s = CUBE_S * k
    if s < 0.05:
        return
    F.b((0.0, CUBE_Y0 + s / 2, s / 2), (s, s, s), CUBE_C)
    if k < 0.98:
        return
    for q in range(300):                                                   # 표면을 기는 점
        x = -19.0 + 38.0 * _h(q + 5)
        z = (38.0 * _h(q + 405) + t * (1.2 + 2.0 * _h(q + 805))) % 38.0 + 1.0
        F.b((x + 0.6 * math.sin(1.7 * t + q), CUBE_Y0 - 0.12, z), (0.7, 0.2, 0.7), ANT_HI)
    if label:
        for z in (0.0, 10.0, 20.0, 30.0, 40.0):
            G.b((-24.0, CUBE_Y0 - 0.3, z), (1.6 if z in (0.0, 40.0) else 1.0, 0.2, 0.35), CYAN_G)
        G.b((-24.0, CUBE_Y0 - 0.3, 20.0), (0.35, 0.2, 40.0), CYAN_G)


def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """훅: 지후 뒤로 개미 점이 쏟아지고(떨어져 쌓임) 카운터가 250만으로 빠르게 오르다 마지막 0.6초 ×250만으로 번쩍."""
    tc = (dur - 0.6) / dur
    pc = min(u / tc, 1.0) ** 1.6
    for k in range(140):                                                   # 쏟아지는 점
        ph = (t * 0.9 + _h(k)) % 1.0
        F.b((-0.80 + 0.28 * (_h(k + 9) - 0.5), 1.5 + 0.25 * _h(k + 30), 6.2 - 5.55 * ph * ph), (0.09, 0.09, 0.09), ANT)
    for k in range(int(70 * pc) + 1):                                      # 쌓이는 더미
        r = 0.34 * (1.0 - 0.07 * (k // 8))
        F.b((-0.80 + r * (2 * _h(k + 50) - 1), 1.5 + 0.25 * _h(k + 70), DECK + 0.05 + 0.09 * (k // 8)), (0.1, 0.1, 0.09), ANT)
    c = tau - (dur - 0.6)
    txt = "{:,}".format(int(2500000 * pc))
    if c > 0:
        srows(G, cam, num_rows("x2,500,000"), 0.0, -0.30, 0.0066 * (1.0 + 0.12 * math.sin(c * 16)), YEL_G, 1.8)
    else:
        srows(G, cam, num_rows(txt), 0.0, -0.30, 0.0066, CYAN_G, 1.8)


def props_gather(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """개미 점 250개가 지평선 쪽에서 한곳(검은 덩어리)으로 모여 듦."""
    m = 3.0 + 22.0 * smooth(ramp(u, 0.15, 0.95))
    F.b((0.0, 100.0, m / 2), (m, m, m), CUBE_C)
    for k in range(250):
        h1, h2, h3 = _h(k + 11), _h(k + 211), _h(k + 411)
        s = smooth(ramp(u * 1.3 - 0.3 * h3, 0.0, 0.6))
        x = lerp(-85.0 + 170.0 * h1, (h2 - 0.5) * m * 0.8, s) + 0.8 * math.sin(2.0 * t + k)
        y = lerp(120.0 + 55.0 * h2, 100.0 + (h3 - 0.5) * m * 0.8, s)
        F.b((x, y, 0.4), (1.1, 1.1, 0.6), ANT)


def props_wave(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """개그 1: 난간 위 개미 한 마리가 더듬이를 흔들어 답함."""
    ant(F, 0.4, 1.95, 1.32 + 0.12, -90.0 + 12.0 * math.sin(2.0 * t), wig=math.sin(2 * math.pi * t / 0.45) if tau > 0.5 else 0.0)


def props_beeline(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """우주 판: 지구에서 해까지 개미 점선, 오가는 밝은 점, ×670, 가정 표지 5mm."""
    earth_items(F, BL, cam, (-2.4, 0.0, 0.0), 0.6, sp_of(t))
    OR.orb((2.4, 0.0, 0.0), 1.0, SUN_C)
    for k in range(40):
        G.b((-1.75 + 3.6 * k / 39.0, 0.0, 0.0), (0.1, 0.1, 0.1), (1.3, 1.3, 1.4))
    for q in range(6):
        ph = (t * 0.55 + q / 6.0) % 1.0
        x = -1.75 + 3.6 * (ph * 2 if ph < 0.5 else 2 - ph * 2)
        G.b((x, -0.05, 0.0), (0.2, 0.2, 0.2), YEL_G)
    wdig(G, num_rows("x670"), 0.0, -0.3, 1.5, 0.22, YEL_G, pop(tau - 0.3, 0.3))
    wdig(G, num_rows("5mm"), 0.0, -0.3, -1.1, 0.13, CYAN_G, pop(tau - 0.9, 0.3))
    for q in range(11):                                                    # 가정 표지 점선 테두리
        if q % 2 == 0:
            for zz in (-0.55, -1.65):
                G.b((-1.0 + 0.2 * q, -0.3, zz), (0.12, 0.03, 0.04), (3.0, 1.3, 0.4))


def props_cube(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    cube_props(F, G, t, 1.0)
    wdig(G, num_rows("460m"), 0.0, CUBE_Y0 - 0.6, 20.0, 1.5, YEL_G, pop(tau - 0.2, 0.3))


def props_watch(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    cube_props(F, G, t, 1.0, label=False)


# ── 지도 판 (세로 판 앞에 칸 상자로 그림)
MAP_Y = 5.55
WORLD = ["", "...#####.....##....#######.###########", "..#######...####..#####################", "..########...###..####################.",
         "...######.....#..##.##.################.", "....####.........#####.######.#####.....", ".....###........#######.######..###.....",
         "......###.......########.#####........##", ".......##.......########..###.......####", "......####.......######............####",
         "......#####.......####.......", ".......####.......###........", ".......###.........##..........", "........##.........#...........", "........#", ""]
WORLD = [r.ljust(40, ".") for r in WORLD]
assert all(len(r) == 40 for r in WORLD) and len(WORLD) == 16
MAP_CS = 0.165


def map_xz(c, r):
    return (c - 20 + 0.5) * MAP_CS, 1.4 + (16 - r - 0.5) * MAP_CS


def props_species(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """종 칸 100개(1칸 약 157종)가 깜박이고, 이름 없는 같은 수의 빈 칸이 점선으로."""
    cs = 0.23
    for r in range(10):
        for c in range(10):
            z = 1.85 + (r + 0.5) * cs
            xl, xr = -2.9 + (c + 0.5) * cs, 0.6 + (c + 0.5) * cs
            b = 0.55 + 0.45 * math.sin(2 * math.pi * (t * 1.4 + _h(r * 10 + c)))
            if tau > 0.02 * (r * 10 + c) * 0.6:
                G.b((xl, MAP_Y, z), (cs * 0.86, 0.05, cs * 0.86), (2.6 * b, 2.0 * b, 0.4 * b))
            for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):             # 빈 칸 = 모서리 점 4개
                G.b((xr + dx * cs * 0.4, MAP_Y, z + dz * cs * 0.4), (0.05, 0.05, 0.05), (0.5, 0.9, 1.4))
    wdig(G, num_rows("x157"), -1.75, MAP_Y - 0.03, 1.4, 0.07, CYAN_G, pop(tau - 0.4, 0.3))


def props_tropic(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """세계 지도 칸: 열대림(초록)·사바나(노랑) 띠만 왼쪽부터 켜짐."""
    reach = ramp(u, 0.1, 0.7) * 40.0
    b = 0.75 + 0.25 * math.sin(2 * math.pi * t / 0.8)
    for r, row in enumerate(WORLD):
        for c, ch in enumerate(row):
            if ch != "#":
                continue
            x, z = map_xz(c, r)
            if 6 <= r <= 10 and c <= reach:
                col = (0.3 * b, 1.7 * b, 0.55 * b) if (c * 7 + r * 3) % 3 else (2.2 * b, 1.8 * b, 0.3 * b)
                G.b((x, MAP_Y, z), (MAP_CS * 0.94, 0.05, MAP_CS * 0.94), col)
            else:
                F.b((x, MAP_Y, z), (MAP_CS * 0.94, 0.05, MAP_CS * 0.94), (0.28, 0.40, 0.52))


# ── 숲 바닥
def props_quiet(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """1주 뒤: 굴 둘레가 텅 비고 마른 잎만 조용히 흩날림."""
    for k in range(12):
        ph = (t * 0.25 + _h(k)) % 1.0
        F.b((MOUND_X - 2.4 + 5.0 * ph, 1.6 + 1.2 * _h(k + 7), 0.9 - 0.8 * ph + 0.1 * math.sin(6 * ph + k)), (0.12, 0.08, 0.02), (0.62, 0.50, 0.22))


def props_seeds(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """씨앗이 개미 길로 옮겨지다 길이 끊긴 자리에서 줄지어 멈춤(화살표가 초록에서 회색으로)."""
    for k in range(12):                                                    # 개미 길(점선), 0.3~0.65 사이가 끊김
        x = -1.1 + 0.2 * k
        if not 0.3 < x < 0.65:
            F.b((x, 1.5, 0.04), (0.1, 0.1, 0.05), ANT_HI)
    F.b((-1.5, 1.5, 0.28), (0.5, 0.5, 0.5), (0.30, 0.55, 0.26))           # 씨앗 식물(출발)
    F.b((1.5, 1.5, 0.22), (0.6, 0.6, 0.45), (0.46, 0.32, 0.20))           # 굴(도착)
    s = smooth(ramp(tau, 0.0, 1.4))
    for k in range(5):
        x = min(-1.0 + 0.25 * k + 0.9 * s, 0.25 - 0.25 * (4 - k))
        F.b((x, 1.5, 0.18), (0.18, 0.18, 0.18), SEED_C)
    stuck = ramp(tau, 1.4, 1.9)
    col = tuple(lerp(a, b, stuck) for a, b in zip((0.5, 2.0, 0.6), (0.6, 0.6, 0.6)))
    arrow_w(G, -1.2, -0.1 + 0.9 * (1.0 - stuck), 0.8, col, y=1.5, th=0.10)
    if stuck > 0.5:
        wdig(G, DIG["x"], 0.5, 1.45, 0.45, 0.1, (3.0, 0.4, 0.3), pop(tau - 1.8, 0.3))


def props_soil(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """흙 단면판: 굴 구멍이 있다가 시간이 지나 사라짐, 점선 '가정' 표지(?)."""
    F.b((0.0, 1.6, 1.7), (3.6, 0.4, 2.4), SOIL_C)
    k = 1.0 - smooth(ramp(u, 0.3, 0.85))
    yy = 1.38
    for cx, cz, w, h in ((-1.0, 1.75, 0.25, 1.7), (0.0, 1.0, 2.2, 0.25), (1.0, 1.6, 0.25, 1.3), (-0.2, 2.1, 0.25, 1.0)):
        if k > 0.02:                                                       # 굴: 얇은 쪽이 줄어들며 사라짐
            F.b((cx, yy, cz), (w * (k if w < h else 1.0) + 0.001, 0.04, h * (k if h <= w else 1.0) + 0.001), (0.07, 0.05, 0.04))
    for q in range(9):                                                     # 점선 표지
        if q % 2 == 0:
            for zz in (3.15, 3.75):
                G.b((-0.55 + 0.14 * q, 1.35, zz), (0.10, 0.03, 0.04), (3.0, 1.3, 0.4))
    wdig(G, DIG["?"], 0.0, 1.33, 3.45, 0.11, (3.0, 2.4, 0.5), pop(tau - 0.8, 0.3))


def props_snack(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """개그 2: 피크닉 매트 위 과자가 그대로 / 연구원이 '!' 표지를 듦."""
    F.b((0.35, 1.7, 0.03), (2.2, 1.7, 0.05), (0.72, 0.28, 0.26))
    for a in range(3):
        for b in range(2):
            F.b((-0.25 + 0.6 * a, 1.35 + 0.65 * b, 0.07), (0.3, 0.3, 0.04), (0.88, 0.84, 0.78))
    for k, (x, y) in enumerate(((0.1, 1.6), (0.5, 1.75), (0.9, 1.5), (0.4, 2.05))):
        F.b((x, y, 0.12), (0.3, 0.3, 0.09), (0.84, 0.66, 0.34))
    rs = S.get("rs")
    if rs:
        hx, hy, hz = hand_pt(rs, "R", 0.1)
        F.b((hx, hy, hz + 0.35), (0.7, 0.05, 0.5), (0.95, 0.92, 0.82))
        F.b((hx, hy, hz + 0.05), (0.04, 0.04, 0.35), (0.5, 0.4, 0.3))
        wdig(G, DIG["!"], hx, hy - 0.04, hz + 0.35, 0.09, (3.0, 0.5, 0.4), pop(tau - 0.5, 0.3))


def coast_z(x):
    return 2.9 + 0.35 * math.sin(0.9 * x + 0.6) + 0.25 * math.sin(2.1 * x)


def coast_base(F):
    F.b((0.0, 5.62, 2.3), (7.0, 0.06, 2.8), (0.10, 0.28, 0.55))            # 바다
    for x in np.arange(-3.4, 3.45, 0.2):                                   # 땅
        z0 = coast_z(float(x))
        F.b((float(x), 5.55, (z0 + 4.9) / 2), (0.2, 0.05, 4.9 - z0), (0.36, 0.44, 0.30))


def props_colony(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """지중해 해안 지도: 한 색 띠가 이탈리아에서 스페인 대서양 연안까지 뻗음."""
    coast_base(F)
    reach = -3.4 + 6.8 * smooth(ramp(u, 0.05, 0.8))
    for x in np.arange(-3.4, 3.45, 0.1):
        if x <= reach:
            G.b((float(x), 5.45, coast_z(float(x)) - 0.14), (0.12, 0.05, 0.16), (3.0, 1.4, 0.3))
    wdig(G, num_rows("6,000km"), 0.0, 5.42, 1.35, 0.1, YEL_G, pop(tau - 0.9, 0.3))


def props_clash(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """같은 지도: 두 번째 색 점 3개가 띠 안쪽에, 두 색이 부딪힐 때 반짝."""
    coast_base(F)
    for x in np.arange(-3.4, 3.45, 0.1):
        G.b((float(x), 5.45, coast_z(float(x)) - 0.14), (0.12, 0.05, 0.16), (3.0, 1.4, 0.3))
    for x in (-1.5, -1.0, -0.5):
        z = coast_z(x) - 0.14
        G.b((x, 5.4, z), (0.22, 0.05, 0.22), (0.4, 1.6, 3.0))
        ph = (t * 1.6 + x) % 1.0
        for q in range(6):
            a = 2 * math.pi * q / 6 + 0.5
            G.b((x + 0.5 * ph * math.cos(a), 5.38, z + 0.5 * ph * math.sin(a)), (0.07, 0.04, 0.07), (3.0, 2.8, 2.4))


# ── 저울 판
def scale_base(F, ang):
    """기둥 + 기울어지는 보 + 접시 두 개. 접시 위 윗면 높이를 (왼쪽, 오른쪽)으로 돌려줌. ang>0이면 오른쪽(+x)이 내려감."""
    Lh, zc = 2.0, 3.0
    F.b((0.0, 0.8, 0.1), (1.6, 1.0, 0.2), (0.50, 0.50, 0.55))
    F.b((0.0, 0.8, 1.5), (0.3, 0.3, 2.8), (0.55, 0.56, 0.60))
    F.c((0.0, 0.8, zc), (2 * Lh + 0.4, 0.2, 0.2), (0.35, 0.36, 0.40), (0.0, ang, 0.0))
    out = []
    for sgn in (-1, 1):
        xe, ze = sgn * Lh * math.cos(ang), zc - sgn * Lh * math.sin(ang)
        for dx in (-0.55, 0.55):
            F.b((xe + dx, 0.8, ze - 0.55), (0.03, 0.03, 1.1), (0.4, 0.4, 0.44))
        F.b((xe, 0.8, ze - 1.1), (1.5, 1.0, 0.08), (0.85, 0.80, 0.65))
        out.append((xe, ze - 1.06))
    return out


def ant_pile(F, cx, y, top, n):
    for k in range(n):
        F.b((cx + 0.4 * (2 * _h(k + 3) - 1) * (1 - 0.03 * (k // 10)), y + 0.3 * (2 * _h(k + 33) - 1), top + 0.1 + 0.2 * (k // 10)), (0.2, 0.2, 0.2), ANT)


def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """반전: 막대 둘. 사람(회색 블록) 막대 100%, 개미(검정) 막대는 1/5."""
    k = smooth(ramp(tau, 0.1, 0.9))
    hh, ah = 2.4 * k + 0.01, 0.48 * k + 0.01
    F.b((-1.3, 0.8, 0.3 + hh / 2), (0.8, 0.5, hh), HUM_C)
    F.b((1.3, 0.8, 0.3 + ah / 2), (0.8, 0.5, ah), ANT)
    for x in (-1.3, 1.3):
        F.b((x, 0.8, 0.15), (1.2, 0.8, 0.3), (0.55, 0.56, 0.60))
    wdig(G, num_rows("100%"), -1.3, 0.4, 0.3 + hh + 0.5, 0.12, (2.6, 2.6, 2.6), pop(tau - 0.9, 0.3))
    wdig(G, num_rows("20%"), 1.3, 0.4, 0.3 + ah + 0.5, 0.15, YEL_G, pop(tau - 1.1, 0.3))


def props_wild(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """야생 새·짐승 더미(오른쪽 접시) vs 개미 덩어리(왼쪽 접시): 개미 쪽이 더 내려감."""
    ang = -0.30 * smooth(ramp(u, 0.2, 0.65))
    (xl, tl), (xr, tr) = scale_base(F, ang)
    ant_pile(F, xl, 0.8, tl, 36)
    for k in range(9):
        animal(F, xr - 0.55 + 0.28 * (k % 5), 0.8 + 0.3 * (k // 5 - 0.3), tr + 0.16 * (k // 5) * 1.5, k % 2, 0.9)
    wdig(G, DIG["!"], 0.0, 0.1, 4.6, 0.22, (3.0, 0.5, 0.4), pop(tau - 1.0, 0.3))


def props_five(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """사람 쪽 접시가 크게 내려감, 개미 쪽은 작은 상자 하나."""
    ang = 0.34 * smooth(ramp(u, 0.1, 0.55))
    (xl, tl), (xr, tr) = scale_base(F, ang)
    F.b((xl, 0.8, tl + 0.15), (0.3, 0.3, 0.3), ANT)
    for k in range(5):
        figure(F, xr - 0.6 + 0.3 * k, 0.8, tr, 0.9)
    wdig(G, num_rows("x5"), xr, 0.5, tr + 1.15, 0.2, YEL_G, pop(tau - 0.9, 0.3))


def props_plus(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """2×10^16 + : 숫자 뒤에 '+', 흙 밑에서 점 하나가 올라옴."""
    wdig(G, num_rows("2x10"), -1.4, 5.42, 3.5, 0.2, YEL_G)
    wdig(G, num_rows("16"), 0.75, 5.42, 4.2, 0.1, YEL_G)
    wdig(G, DIG["+"], 1.7, 5.42, 3.5, 0.2, CYAN_G, pop(tau - 0.5, 0.3))
    F.b((0.0, 5.45, 1.0), (8.0, 0.3, 0.8), SOIL_C)
    k = smooth(ramp(tau, 0.6, 2.0))
    G.b((0.3, 5.28, 1.45 + 0.5 * k), (0.28, 0.1, 0.28), (2.4, 2.2, 2.0))


def props_gap(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """세계 지도: 중앙아프리카·아시아에 회색 빗금, 연구원이 '?' 표지(자료 부족)."""
    for r, row in enumerate(WORLD):
        for c, ch in enumerate(row):
            if ch != "#":
                continue
            x, z = map_xz(c, r)
            hatch = (6 <= r <= 10 and 17 <= c <= 23) or (3 <= r <= 7 and 26 <= c <= 33)
            if hatch and (r + c) % 2 == 0:
                F.b((x, MAP_Y, z), (MAP_CS * 0.94, 0.05, MAP_CS * 0.94), (0.70, 0.70, 0.72))
            else:
                F.b((x, MAP_Y, z), (MAP_CS * 0.94, 0.05, MAP_CS * 0.94), (0.28, 0.40, 0.52) if not hatch else (0.16, 0.20, 0.26))
    rs = S.get("rs")
    if rs:
        hx, hy, hz = hand_pt(rs, "R", 0.1)
        k = pop(tau - 0.4, 0.3)
        F.b((hx, hy, hz + 0.4 * k), (0.8 * k + 0.001, 0.05, 0.55 * k + 0.001), (0.95, 0.92, 0.82))
        wdig(G, DIG["?"], hx, hy - 0.04, hz + 0.4 * k, 0.1, (3.0, 2.4, 0.5), k)


def props_back(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """검은 덩어리가 줄어들며 점들이 흩어져 평원·숲으로 돌아감."""
    s = smooth(ramp(u, 0.1, 0.9))
    cube_props(F, G, t, max(1.0 - s, 0.0) if s < 0.97 else 0.0, label=False)
    for q in range(300):
        h1, h2, h3 = _h(q + 5), _h(q + 405), _h(q + 805)
        sx, sz = -19.0 + 38.0 * h1, 1.0 + 38.0 * h2
        ex, ey = -75.0 + 150.0 * h3, 25.0 + 120.0 * _h(q + 1205)
        p = smooth(ramp(s * 1.2 - 0.2 * h3, 0.0, 0.8))
        F.b((lerp(sx, ex, p), lerp(CUBE_Y0 - 0.12, ey, p), lerp(sz, 0.3, p) + 5.0 * 4 * p * (1 - p)), (0.7, 0.7, 0.7), ANT_HI)


def props_calm(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """해질녘 숲: 지후가 손가락에 개미 한 마리를 올려 보고 내려놓음."""
    d = S.get("jh")
    if not d:
        return
    hx, hy, hz = hand_pt(d, "R", 0.0)
    k = smooth(ramp(tau, 1.9, 2.7))
    gx, gy = hx + 0.1, hy
    ant(F, lerp(hx, gx, k), lerp(hy, gy, k), lerp(hz + 0.1, 0.12, k), -90.0 + 25.0 * math.sin(1.5 * t), s=0.2, wig=math.sin(2 * math.pi * t / 0.5))


def props_ask(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """지구본 위 핀 두 개(어디에 모을까)."""
    cw = (0.55, -0.4, 2.35)
    earth_items(F, BL, cam, cw, 0.4, sp_of(t), "plain")
    c = np.array((cw[0] + OFF["plain"][0], cw[1] + OFF["plain"][1], cw[2]), float)
    for q, (a, b, col) in enumerate(((-0.45, 0.30, (3.0, 0.5, 0.4)), (0.40, -0.25, CYAN_G))):
        n = a * cam["right"] + b * cam["up"] - math.sqrt(1.0 - a * a - b * b) * cam["fwd"]
        OR.orbw(c + n * 0.42, 0.13 * pop(tau - 0.4 - 0.3 * q, 0.3), col)


def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """개미 점 덩어리 위에서 반짝이는 물음표(주제 예고 없음)."""
    for k in range(120):
        a, b = 2 * math.pi * _h(k), math.acos(2 * _h(k + 200) - 1)
        a += 0.5 * t
        F.b((1.3 * math.sin(b) * math.cos(a), 6.0 + 1.3 * math.sin(b) * math.sin(a), 2.2 + 1.3 * math.cos(b)), (0.2, 0.2, 0.2), ANT)
    q = 0.65 + 0.35 * math.sin(2 * math.pi * t / 0.9)
    wdig(G, DIG["?"], 0.0, 4.4, 2.2, 0.4, (3.0 * q, 2.4 * q, 0.5 * q), pop(tau - 0.3, 0.3))


PROPS = {LN["hook"]: props_hook, LN["gather"]: props_gather, LN["wave"]: props_wave, LN["beeline"]: props_beeline, LN["cube"]: props_cube,
         LN["watch"]: props_watch, LN["species"]: props_species, LN["tropic"]: props_tropic, LN["quiet"]: props_quiet, LN["seeds"]: props_seeds,
         LN["soil"]: props_soil, LN["snack"]: props_snack, LN["colony"]: props_colony, LN["clash"]: props_clash, LN["twist"]: props_twist,
         LN["wild"]: props_wild, LN["five"]: props_five, LN["plus"]: props_plus, LN["gap"]: props_gap, LN["back"]: props_back,
         LN["calm"]: props_calm, LN["ask"]: props_ask, LN["teaser"]: props_teaser}


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
    P = "plain"

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    jh = {L["hook"]: st(P, 0.4, 0.0, -80, "gape", z=DECK, seq=[(1.9, "shock")]),
          L["wave"]: st(P, -0.1, 0.7, 90, "smile", z=DECK, alt=("think", "smile", 0.42, 0.0)),
          L["cube"]: st(P, -0.7, 0.0, 90, "stand", z=DECK),
          L["watch"]: st(P, -0.7, 0.0, 90, "look_up", z=DECK),
          L["quiet"]: st("forest", MOUND_X, 0.9, 90, "peer"),
          L["snack"]: st("forest", -0.3, 0.5, 40, "smile"),
          L["twist"]: st("scale", 0.0, -0.9, -90, "gape", seq=[(1.5, "shock")]),
          L["back"]: st(P, -0.7, 0.0, 90, "smile", z=DECK),
          L["calm"]: st("forest", 0.0, 0.3, -90, "peer"),
          L["ask"]: st(P, -0.25, 0.0, -90, "smile", z=DECK, alt=("smile", "point", 0.9, 0.0)),
          L["comment"]: st(P, 0.0, 0.0, -90, "smile", z=DECK, alt=("smile", "point_up", 0.8, 0.0))}
    add("jh", 0, JH_SH, JH_PA, jh, extra="hood")
    add("rs", 1, CO_SH, CO_PA, {
        L["cube"]: st(P, 0.7, 0.0, 90, "point", z=DECK),
        L["watch"]: st(P, 0.7, 0.0, 90, "point_up", z=DECK),
        L["snack"]: st("forest", 1.5, 0.6, 150, "think"),
        L["gap"]: st("panel", -2.5, 3.2, -100, "think"),
        L["back"]: st(P, 0.7, 0.0, 90, "stand", z=DECK)}, extra="coat")
    add("e1", 1, EX_SH[0], (0.20, 0.20, 0.24), {L["hook"]: st(P, -0.35, 1.1, -100, "look_up", z=DECK)})
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
SPACE_SKY = ((0.003, 0.004, 0.014), (0.010, 0.013, 0.034), 1.8)
ROOM_SKY = ((0.04, 0.05, 0.09), (0.10, 0.12, 0.18), 0.0)


def sky(t):
    s = cam_of(t)["set"]
    if s == "space":
        return SPACE_SKY
    if s == "panel":
        return ROOM_SKY
    return DUSK_SKY if line_at(t) == LN["calm"] else DAY_SKY


def env(i, st_, u=0.0):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=3.0, sun_col=(1.0, 0.95, 0.85), sun_rot=(50, 0, 30), amb=0.5, amb_col=(0.62, 0.72, 0.95), lt={})
    if st_ == "space":
        e.update(sun=4.2, sun_col=(1.0, 0.96, 0.9), sun_rot=(55, 0, 60), amb=0.10, amb_col=(0.30, 0.36, 0.62), lt={"ep56_sp0": 220.0})
    elif st_ == "panel":
        e.update(sun=0.4, sun_col=(1.0, 0.96, 0.9), amb=0.45, amb_col=(0.70, 0.76, 0.92), lt={"ep56_pn0": 200.0, "ep56_pn1": 120.0})
    elif st_ == "scale":
        e.update(sun=1.0, amb=0.6, amb_col=(0.75, 0.80, 0.92), lt={"ep56_sc0": 330.0, "ep56_sc1": 150.0})
    elif i == LN["calm"]:
        e.update(sun=2.4, sun_col=(1.0, 0.62, 0.38), sun_rot=(72, 0, 20), amb=0.34, amb_col=(0.72, 0.52, 0.62))
    return e


# 번쩍 (줄, 줄 시작 후 초, 세기, 길이 초): 훅 끝 숫자가 ×250만으로 바뀔 때, 반전 줄 시작
def _flashes():
    a, b = shot_span(LN["hook"])
    return [(LN["hook"], (b - a) - 0.6, 0.30, 0.18), (LN["twist"], 0.05, 0.22, 0.16)]


WARM = np.array((1.0, 0.95, 0.86), np.float32)


def flash_level(t):
    a = 0.0
    for i, tau0, peak, dur in _flashes():
        t0 = shot_span(i)[0] + tau0
        a = max(a, peak * clamp((t - t0 + 0.02) / 0.03) * (1.0 - clamp((t - t0 - 0.01) / dur)))
    return a


def postfx(img, t):
    """번쩍(전체 화면): 훅에서 숫자가 ×250만으로 바뀔 때, 반전 줄 시작."""
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
    v = X.Vox(56)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.45, 0.55, 0.85), ambient_strength=0.32, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 0.9, name="ep56_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep56_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep56_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep56_fx", K.proto(ctx, "ep56_p_fx", cube(), [K.mat_inst("ep56_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep56_glow", K.proto(ctx, "ep56_p_glow", cube(), [_mat_glow("ep56_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep56_orb", K.proto(ctx, "ep56_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep56_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep56_bl", K.proto(ctx, "ep56_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep56_m_bl", 0.8)]),
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
