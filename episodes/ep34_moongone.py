"""EP34 만약에 달이 사라진다면? (정보형 v2: 블록 캐릭터·내레이션·정보 카드·경과 배지)

컷 흐름 (한 줄 = 한 컷):
0 훅: 밤 해변 난간에서 민지가 올려다본 보름달이 0.35초에 '퐁' 번쩍 사라짐(카메라는 빠른 push) → 1 어두워진 밤하늘·가로등과 별, 민지가 손전등을 켬
→ 2 하늘 비교 컷(큰 해 상자 vs 작고 흐린 달) → 3 달 없는 밤길, 더듬거리다 전봇대에 쿵(개그 1) → 4 밤 풀밭, 달빛 아래 쇠똥구리가 똥공을 직선으로 굴림
→ 5 달이 사라지자 공 둘레를 빙글빙글(개그 2) → 6 달빛 바닷속 산호 위로 분홍 알이 한꺼번에 떠오름 → 7 달이 사라지고 알이 제각각·적게
→ 8 새벽 항구, 선장이 눈금 기둥을 가리키며 갸웃 → 9 달·해 조수 힘 화살표 비교(2.2배) → 10 기둥 옆 물높이 오르내림 폭이 평균의 46%로 줄어듦(만조선·간조선)
→ 11 갯벌 물이 차올라 드러난 갯벌이 줄고 조개 캐던 사람들이 어리둥절 → 12 1년 뒤 밤 산책(등을 든 사람들, 별이 또렷)
→ 13 서재 책상 지구본이 흔들리기 시작 → 14 달 상자가 닻줄로 축을 잡아 기울기 일정 → 15 달이 사라지자 마구 기울며 눈·꽃·단풍 아이콘이 바뀜
→ 16 반전: 해변 달이 아주 천천히 작아짐 → 17 지구본과 달 상자 사이 거리 막대가 조금 늘어남 → 18 산호 화석 줄무늬를 손가락으로 하나씩 셈
→ 19 벽시계 눈금이 22칸에서 24칸으로 → 20 민지가 달을 보며 미소 → 21 두 손 모아 소원 → 22 달 앞을 큰 고양이 실루엣이 지나감(다음 편).

근거(설명란):
2~3줄 · 보름달 빛은 햇빛의 약 1/400,000 (겉보기 등급 -12.74 대 -26.74, 14등급 차 = 10^(14/2.5) = 10^5.6 ≈ 398,000배, 계산) · NASA 달·태양 팩트시트
4~5줄 · 쇠똥구리는 달빛 편광으로 방향을 잡는다 · Dacke 외, Nature 424:33 (2003)
6~7줄 · 산호 수십 종이 보름달 며칠 뒤 같은 밤에 일제히 산란한다 · Harrison 외, Science 223:1186 (1984)
9줄 · 달의 조수 힘은 태양의 약 2.2배 (질량/거리^3로 계산, 2.18) · NASA 팩트시트 값으로 계산
10줄 · 달이 없으면 조수 크기는 평균의 약 46% (이론값, 계산값: 평균 조차는 달 힘에 비례하므로 태양÷달 = 1÷2.18 = 0.46),
       가장 큰 사리 때 기준으론 약 31% (계산값: 태양만 남으면 1÷(1+2.18) = 0.31) · 조석 이론, 계산
11줄 · 인천 앞바다는 사리 때 조수 차이가 9m 가까이(최대 대조차 8.9m) — '최대 9m'로 못 박지 않음 · 한국해양학회지 1980 '인천 조차 변동'
14~15줄 · 달은 지구 자전축 기울기(약 23.4°)의 흔들림을 잡아 주고, 없으면 크게 요동칠 수 있다 · Laskar 외, Nature 361:615 (1993).
       단, 일부 연구(Lissauer 외 2012)는 달이 없어도 기울기 변동이 제한될 수 있다고 본다.
16~17줄 · 달은 해마다 약 3.8cm 멀어진다 → 100년이면 약 3.8m (계산값: 3.8cm x 100년 = 380cm) · NASA JPL 달 레이저 반사경, NSSDC 팩트시트
18~19줄 · 약 4억 년 전 산호 화석의 1년은 약 400일 → 하루 약 22시간 (계산값: 365.25 x 24 ÷ 400 ≈ 21.9) · Wells, Nature 197:948 (1963)
(밀물·썰물 폭·갯벌 면적·지구본 기울기 흔들림·쇠똥구리 궤적 등 그림의 크기는 모두 이해를 돕는 상상 연출이며 실제 수치가 아님)

특수효과:
달 = 카메라에서 140m 밖(무한히 먼 달처럼 위치만 따라감)에 둔 발광 구 하나 + 카메라를 향한 크레이터 상자 넷. 방향은 줄마다 LINES의 moon=(화면 x, 화면 y, 각반지름)으로 정함.
달빛 길 = 달 방향 수직면을 따라 바다 위에 멀수록 길고 넓게 놓은 가는 발광 판 14장(서로 겹치지 않고 높이만 0.0015m씩 달리함). 푸른 점광원(moon)·달빛(해 조명)·길은 달과 같은 프레임에 켜지고 꺼짐.
'퐁' 사라짐 = 사라지기 0.07초 전 16% 부풀었다가 0 → 같은 순간 postfx로 화면 전체 번쩍(훅은 세게, 풀밭·바닷속·지구본은 약하게, 약 0.15초). 달 구·발광 상자는 visible_shadow=False로 달빛을 가리지 않게.
카메라는 줄마다 shot으로 push·방위각 변화, 훅은 ease='out'(처음에 빠르게), 풀밭 4번 줄은 track으로 쇠똥구리를 따라감.
하늘 비교·조수 힘 컷 = 카메라 화면 좌표(sprite)에 정면을 보는 발광 상자·구·화살표(길이 1 : 2.2)를 놓음. 사람 = ep33 방식의 원형(표준 자세 위에 팔·고개·입만 바꾼 자세 + 민지 후드·선장 모자).
조위 기둥 = 눈금 기둥(검정·흰 띠)에 만조선(빨강)·간조선(파랑) 발광 판, 물은 매 프레임 상자(윗면 높이가 사인파, 10번 줄에 진폭이 평균의 46%로 줄고 새 폭을 노란 판으로 표시).
갯벌 = 바다 쪽으로 낮아지는 계단 여섯 칸 + 물 상자가 차올라 드러난 칸이 줄어듦. 쇠똥구리 = 상자 11개 + 발광 눈 둘(다리 여섯은 걸음에 맞춰 흔들림), 공은 구, 궤적선 = 발광 점선(직선 → 5번 줄엔 원).
산호 알 = 분홍 발광 구 약 110개(산호 위에서 같은 때에 한꺼번에 / 달이 사라지면 제각각 흩어지고 3분의 2는 사라짐). 지구본 = 속이 빈 블록 구(바다·땅·극지 색)가 기울기·자전으로 돌고 축 막대가 따라 기움,
눈·꽃·단풍 아이콘 = 5x5 도트. 벽시계 눈금 = 상자 24개(n=22→24로 간격이 좁아지며 새 눈금이 생김). 고양이 = 검정 상자 열한 개(+ 초록 눈 하나)(난간 위를 걸으며 달 앞을 지남).
(자막 20자 제한: 20번 줄은 '밤', 22번 줄은 ' · ' 앞뒤 띄어쓰기를 빼서 각각 19자로 줄임)

"""
import json
import math
from pathlib import Path

import numpy as np

from engine import voxel as X
from engine.common import clamp, ramp

STYLE = "pixe"
TITLE_FAST = True
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.15, 0.3, 1.6)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게). 해변 세트 안에 마을(0)·새벽 항구(BAYX)·갯벌(FLX)이 x로 나란히 붙어 있음
OFF = {"beach": (0, 0), "meadow": (300, 0), "reef": (600, 0), "study": (900, 0)}
BAYX, FLX = 60.0, 120.0
NAMES = ("hook", "dark", "ratio", "gag1", "beetle", "dizzy", "coral", "scatter", "captain", "force", "gauge", "flat",
         "adapt", "far", "anchor", "wobble", "twist", "bar", "fossil", "clock", "smile", "wish", "cat")
IX = {n: k for k, n in enumerate(NAMES)}

# say: 내레이션 / cap: 화면 자막(아라비아 숫자) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동])
# ease="out"이면 카메라가 처음에 빨리 움직이고 천천히 멈춤(훅)
LINES = [
    dict(say="달이 사라지면 밀물과 썰물이 절반 아래로 줄어요", gap=0.5, ease="out",
         shot=("beach", (0.45, -0.5, 1.6), -86, 4, 3.3, 20, 0.72, 4, 0.10), moon=(0.45, 0.55, 7.0)),
    dict(say="먼저 밤하늘이 확 어두워져요", cap="밤하늘이 확 어두워져요",
         shot=("beach", (0.0, -0.5, 1.35), 82, 6, 3.4, 22, 0.9, -4, 0.10)),
    dict(say="보름달은 햇빛의 사십만 분의 일이에요", cap="보름달은 햇빛의 40만분의 1",
         shot=("beach", (0.0, 0.0, 40.0), 90, -75, 39.3, 20, 1.0, 0)),
    dict(say="그래도 밤엔 달이 제일 밝았죠", gap=0.5,
         shot=("beach", (1.6, -2.4, 0.95), -90, 3, 7.0, 24, 0.94, 2, 0.04)),
    dict(say="쇠똥구리는 달빛으로 길을 찾아요",
         shot=("meadow", (0.0, 1.0, 0.2), -90, 3, 3.4, 28, 0.92, 4), moon=(0.35, 0.50, 4.5)),
    dict(say="달이 없으면 빙글빙글 돌아요", gap=0.5,
         shot=("meadow", (0.2, 1.0, 0.25), -80, 14, 2.6, 28, 0.9, 6), moon=(0.35, 0.50, 4.5)),
    dict(say="산호는 보름달 뒤에 알을 낳아요",
         shot=("reef", (0.0, 1.5, 1.3), -90, 6, 5.2, 24, 0.92, 4), moon=(0.40, 0.45, 4.0)),
    dict(say="신호를 잃으면 알이 뿔뿔이 흩어져요", cap="신호를 잃으면 알이 흩어져요", gap=0.5,
         shot=("reef", (0.0, 1.5, 1.3), -80, 6, 5.2, 24, 0.92, -4)),
    dict(say="한 달 뒤, 바닷물이 달라졌어요", gap=0.4,
         shot=("beach", (BAYX + 2.2, 0.4, 0.95), 100, 6, 4.8, 24, 0.9, -3, 0.12)),
    dict(say="달의 힘은 태양의 두 배가 넘어서", cap="달의 힘은 태양의 약 2.2배", gap=1.05,
         shot=("beach", (0.0, 0.0, 40.0), 90, -75, 39.3, 20, 1.0, 0)),
    dict(say="달이 없으면 조수는 절반 아래로 줄어요", cap="달이 없으면 조수는 절반 이하", gap=0.7,
         shot=("beach", (BAYX + 1.5, 0.9, -1.1), 90, 14, 7.0, 26, 0.95, -3)),
    dict(say="구 미터 가까운 경기만 갯벌도 줄어들어요", cap="9m 가까운 경기만 갯벌도 줄어요", gap=0.7,
         shot=("beach", (FLX, 9.0, 0.0), -90, 32, 14.0, 24, 0.9, -3, 0.04)),
    dict(say="일 년 뒤, 사람들은 적응했어요", cap="1년 뒤, 사람들은 적응했어요", gap=0.4,
         shot=("beach", (3.0, -2.2, 1.2), -150, 6, 12.0, 22, 0.92, 4, 0.05)),
    dict(say="진짜 문제는 아주 먼 훗날이에요", cap="진짜 문제는 아주 먼 훗날", gap=0.4,
         shot=("study", (-0.45, 1.45, 1.05), -90, 8, 2.6, 26, 0.92, 4, 0.06)),
    dict(say="달은 자전축을 잡아 주는 닻이에요", cap="달은 자전축을 잡아 주는 닻",
         shot=("study", (0.0, 1.45, 1.1), -90, 6, 3.0, 26, 0.92, 3)),
    dict(say="없으면 기울기가 크게 흔들릴 수 있어요", cap="없으면 기울기가 크게 흔들릴 수도", gap=0.5,
         shot=("study", (0.0, 1.45, 1.1), -92, 6, 3.0, 26, 0.92, -3)),
    dict(say="그런데 달은 지금도 멀어지는 중이에요", cap="달은 지금도 멀어지는 중이에요",
         shot=("beach", (0.45, -0.5, 1.6), -92, 4, 3.4, 20, 0.95, 1.5, 0.10), moon=(0.16, 0.06, 7.0)),
    dict(say="백 년이면 삼 미터 팔십 센티나 멀어져요", cap="100년이면 3.8m나 멀어져요", gap=0.5,
         shot=("study", (0.05, 1.45, 1.1), -90, 6, 3.0, 26, 0.9, 3)),
    dict(say="사 억 년 전엔 일 년이 사백 일이었어요", cap="4억 년 전엔 1년이 약 400일",
         shot=("study", (0.8, 1.5, 0.98), -90, 8, 1.5, 30, 0.9, 4, 0.04)),
    dict(say="그러니 하루는 지금보다 짧았죠", cap="그러니 하루는 더 짧았죠", gap=0.5,
         shot=("study", (0.6, 2.4, 1.9), -90, 0, 3.0, 28, 0.9, 0)),
    dict(say="오늘 밤 달은 어제보다 조금 더 멀어요", cap="오늘 달은 어제보다 조금 더 멀어요", gap=0.4,
         shot=("beach", (0.3, -0.5, 1.6), -92, 4, 2.9, 20, 0.95, 4, 0.10), moon=(0.38, 0.36, 6.5)),
    dict(say="오늘 밤 달에게 무슨 소원을 빌래요?", cap="오늘 밤 달에게 무슨 소원을 빌래요?", gap=0.6,
         shot=("beach", (0.3, -0.5, 1.6), -92, 4, 2.7, 20, 0.95, -4, 0.10), moon=(0.30, 0.34, 6.5)),
    dict(say="오늘 저녁 일곱 시, 고양이가 사람만큼 커진다면?", cap="다음 편·고양이가 사람만큼 커지면?",
         shot=("beach", (0.6, -0.5, 1.7), -90, 4, 3.8, 20, 0.97, 0, 0.12), moon=(0.0, 0.0, 9.0)),
]
assert len(LINES) == len(NAMES)
TITLE = [("만약에", "white"), ("달이", "white"), ("사라진다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = 16          # '그런데 달은 지금도 멀어지는 중이에요' 줄

CLOCK = [(1, "경과", "바로"), (8, "경과", "1달 뒤"), (12, "경과", "1년 뒤"), (13, "경과", "수억 년 뒤"),
         (16, "경과", "지금"), (20, None)]
CARDS = [
    dict(lines=(2, 3), big="1/40만", small="보름달 빛 ÷ 햇빛", color="yellow", src="NASA 팩트시트 -12.74 대 -26.74"),
    dict(lines=(4, 5), big="달빛 나침반", small="쇠똥구리는 달빛 편광으로 방향을 잡아요", color="cyan", src="Nature 2003, Dacke 외"),
    dict(lines=(6, 7), big="보름달 뒤", small="산호 수십 종이 같은 밤에 알을 낳아요", color="pink", src="Science 1984, Harrison 외"),
    dict(lines=(9, 9), big="2.2 : 1", small="달 : 태양, 조수를 만드는 힘(계산)", color="yellow", src="NASA 팩트시트 값으로 계산"),
    dict(lines=(10, 10), big="평균의 약 46%", small="달이 없을 때 조수 크기(이론값, 큰 사리 때는 약 31%)", color="orange", src="계산 1÷2.18"),
    dict(lines=(11, 11), big="9m 가까이", small="인천 앞바다 사리 때 조수 차이", color="orange", src="한국해양학회지 1980"),
    dict(lines=(14, 15), big="기울기 23.4°", small="달이 지구 자전축의 흔들림을 잡아 줘요", color="cyan", src="Nature 1993, Laskar 외"),
    dict(lines=(16, 17), big="해마다 3.8cm", small="달이 멀어지는 속도 · 100년이면 약 3.8m(계산값)", color="yellow", src="NASA JPL 달 레이저 반사경"),
    dict(lines=(18, 19), big="1년 = 400일", small="약 4억 년 전 산호 화석 성장선 · 하루 약 22시간(계산)", color="yellow", src="Nature 1963, Wells"),
    dict(lines=(22, 22), big="다음 편", small="오늘 저녁 7시 · 고양이가 사람만큼 커진다면?", color="cyan", src="구독하면 놓치지 않아요"),
]
for _ln in LINES[1:]:
    assert len(_ln.get("cap", _ln["say"])) <= 20, _ln.get("cap", _ln["say"])
assert all(0 < c["lines"][0] <= c["lines"][1] < len(LINES) for c in CARDS)

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep34_moongone" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 65.0, "lines": [[0.15 + 2.8 * i, 2.8 * i + 2.8, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep34", "title": "만약에 달이 사라진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"key": "Eb", "mode": "lydian", "bpm": 76, "seed": 341, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.95, "bloom": 0.2, "bloom_thr": 1.25, "vignette": 0.16}

MJ_SH, MJ_PA = (0.45, 0.74, 0.95), (0.15, 0.18, 0.30)     # 민지: 하늘색 후드·긴 머리·남색 바지
CAP_SH, CAP_PA = (0.95, 0.55, 0.25), (0.15, 0.18, 0.30)   # 선장 아저씨: 주황 점퍼
EX_SH = [(0.85, 0.30, 0.28), (0.35, 0.65, 0.40), (0.92, 0.92, 0.90), (0.30, 0.30, 0.34), (0.95, 0.80, 0.35),
         (0.55, 0.38, 0.70), (0.80, 0.55, 0.65)]          # 엑스트라 (하늘색·주황 피함)


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
    """[(시작, 끝, 글)] — 첫 줄은 가운데 제목 카드로 보여 주므로 아래 자막에서 뺌. 자막은 cap(아라비아 숫자)."""
    return [(s, e, LINES[k].get("cap", txt)) for k, (s, e, txt) in enumerate(TIMELINE["lines"]) if k > 0]


def title_span():
    s, e, _ = TIMELINE["lines"][0]
    return s, e


def simulate(build_dir):
    return {"dur": np.float32(DUR)}


# ───────────────────────── 달 · 하늘 · 빛 ─────────────────────────
R_FAR = 140.0                                          # 달 구를 두는 거리(m): 카메라 위치 + 방향 x R_FAR (무한히 먼 달처럼 시차 없음)
MOONC = (0.62, 0.74, 1.0)                              # 달빛 색
# 달이 사라지는 순간(줄 시작 후 초). 이 줄들은 앞부분엔 달이 있고 이 순간 '퐁' 사라짐
VANISH = {IX["hook"]: 0.36, IX["dizzy"]: 0.30, IX["scatter"]: 0.30, IX["wobble"]: 0.85}
MOON_LINES = {IX["hook"], IX["beetle"], IX["dizzy"], IX["coral"], IX["scatter"], IX["anchor"], IX["wobble"],
              IX["twist"], IX["bar"], IX["smile"], IX["wish"], IX["cat"]}
_MD = {}


def moon_dir(i):
    """줄 i의 하늘 달 방향(월드 단위벡터): 줄 가운데 시점 카메라에서 LINES[i]['moon']=(nx, ny, 각반지름) 화면 자리에 보이는 방향."""
    if i not in _MD:
        nx, ny = LINES[i]["moon"][:2]
        cam = cam_pose(i, 0.5)
        f = cam["lens"]
        d = cam["fwd"] + nx * (6.75 / f) * cam["right"] + (ny + 2.0 * cam["shift"]) * (12.0 / f) * cam["up"]
        _MD[i] = d / np.linalg.norm(d)
    return _MD[i]


def moon_k(i, tau):
    """줄 i, 줄 시작 후 tau초에서 달의 크기 배율(0=없음). 사라지기 직전 살짝 부풀었다가 '퐁'."""
    if i not in MOON_LINES:
        return 0.0
    v = VANISH.get(i)
    if v is None:
        return 1.0
    if tau < v - 0.07:
        return 1.0
    if tau < v:
        return 1.0 + 0.16 * (tau - (v - 0.07)) / 0.07
    return 0.0


def flash_level(t):
    """달이 사라질 때 화면 전체 번쩍(약 0.15초). 훅은 세게, 그 밖의 줄은 약하게."""
    a = 0.0
    for i, v in VANISH.items():
        t0 = shot_span(i)[0] + v
        w = 1.0 if i == 0 else 0.4
        a = max(a, w * clamp((t - t0 + 0.02) / 0.03) * (1.0 - clamp((t - t0 - 0.01) / 0.12)))
    return a


def postfx(img, t):
    """STYLE='pixe'에선 overlay의 FLASH가 안 쓰여서 번쩍을 여기서 화면 전체에 얹음 (제목·자막은 그 위에 그려짐)."""
    a = flash_level(t)
    if a <= 0.0:
        return img
    return img + (np.array((0.95, 0.98, 1.0), np.float32) - img) * np.float32(a)


NIGHT_SKY = ((0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0)


def sky(t):
    i = line_at(t)
    if i in (IX["coral"], IX["scatter"]):                                  # 바닷속: 푸른 배경
        return (0.03, 0.12, 0.26), (0.05, 0.20, 0.36), 0.0
    if i in (IX["ratio"], IX["force"]):                                    # 하늘 비교 컷: 짙은 남색 + 별
        return (0.006, 0.010, 0.040), (0.020, 0.030, 0.090), 1.3
    if IX["captain"] <= i <= IX["flat"]:                                   # 새벽 항구·갯벌
        return (0.16, 0.20, 0.46), (0.96, 0.58, 0.45), 0.25
    if i == IX["adapt"]:                                                   # 별이 또렷
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.7
    return NIGHT_SKY


def set_of(i):
    return LINES[i]["shot"][0]


def env(i, tau):
    """줄별 달빛(해 조명)·주변광 + 움직이는 조명 {이름: 세기}."""
    m = 1.0 if moon_k(i, tau) > 0 else 0.0
    e = dict(sun=0.0, sun_col=MOONC, sun_rot=(64, 0, 178), amb=0.22, amb_col=(0.52, 0.58, 0.84), lt={})
    st = set_of(i)
    if IX["captain"] <= i <= IX["flat"]:                                   # 새벽: 낮은 주황 햇빛 + 분홍빛 하늘 주변광
        e.update(sun=2.3, sun_col=(1.0, 0.74, 0.56), sun_rot=(80, 0, 200), amb=0.40, amb_col=(0.80, 0.74, 0.88))
    elif st == "beach":
        e.update(sun=0.95 * m, amb=0.22 + 0.04 * m)
        e["lt"] = {"ep34_l%d" % k: 230.0 for k in range(4)}
    elif st == "meadow":
        e.update(sun=1.0 * m, sun_rot=(58, 0, 120), amb=0.20 + 0.04 * m)
        e["lt"] = {"ep34_mw_fill": 40.0 + 60.0 * m}
    elif st == "reef":
        e.update(sun=1.1 * m, sun_rot=(25, 0, 150), amb=0.46, amb_col=(0.28, 0.58, 0.90))
        e["lt"] = {"ep34_rf_fill": 70.0 + 40.0 * m}
    elif st == "study":
        e.update(amb=0.22, amb_col=(0.55, 0.60, 0.82))
        e["lt"] = {"ep34_st_lamp": 55.0, "ep34_st_ceil": 110.0}
    if i in (IX["ratio"], IX["force"]):
        e.update(amb=0.0)
    if "moon" in LINES[i] and st != "reef":
        D = moon_dir(i)
        e["sun_rot"] = (52, 0, math.degrees(math.atan2(D[1], D[0])) + 40.0 + 90.0)
    return e


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def cam_pose(i, u):
    """줄 i, 진행도 u의 카메라: dict(set, tgt, az, el, dist, lens, loc, shift, fwd, right, up) — 월드 좌표. CamRig.set과 같은 규칙."""
    st_, tg, az, el, dist, lens, push, daz = LINES[i]["shot"][:8]
    shift = LINES[i]["shot"][8] if len(LINES[i]["shot"]) > 8 else 0.0
    if LINES[i].get("ease") == "out":
        u = 1.0 - (1.0 - u) ** 2
    o = OFF[st_]
    tgt = np.array((tg[0] + o[0], tg[1] + o[1], tg[2]), float)
    if LINES[i].get("track"):                              # 움직이는 주인공을 따라가는 카메라: 목표점 x가 초속 track m로 감
        a_, b_ = shot_span(i)
        tgt[0] += LINES[i]["track"] * u * (b_ - a_)
    a, e, dd = az + daz * u, math.radians(el), dist * (1 + (push - 1) * u)
    loc = tgt + np.array((math.cos(e) * math.cos(math.radians(a)), math.cos(e) * math.sin(math.radians(a)), math.sin(e))) * dd
    fwd = tgt - loc
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, (0.0, 0.0, 1.0))
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return dict(set=st_, tgt=tgt, az=a, el=el, dist=dd, lens=lens, loc=loc, shift=shift, fwd=fwd, right=right, up=up)


def project(cam, p):
    """월드 점 → (화면 x 0~1 왼쪽부터, y 0~1 위부터, 깊이). CamRig(센서 세로 24mm) + 렌즈 세로 이동(shift)과 같은 규칙."""
    d = np.asarray(p, float) - cam["loc"]
    z = float(d @ cam["fwd"])
    k = cam["lens"] / 24.0
    return 0.5 + (float(d @ cam["right"]) / z) * k / (1080.0 / 1920.0), 0.5 - (float(d @ cam["up"]) / z) * k + cam["shift"], z


# ───────────────────────── 상자 · 구 목록 ─────────────────────────
def _rmat(rx, ry, rz):
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    return (np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]) @ np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @
            np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]))


class Items:
    """상자 인스턴스 모음. 상자 원점 = 뒷면 가운데, +x로 뻗음(size로 늘림). c()는 가운데 기준으로 넣음. 구는 kind='orb'(원점 = 가운데, size = 지름)."""

    def __init__(self, cap):
        self.cap, self.P, self.S, self.R, self.C = cap, [], [], [], []

    def o(self, origin, size, col, rot=(0.0, 0.0, 0.0)):
        self.P.append(tuple(float(q) for q in origin))
        self.S.append(tuple(float(q) for q in size))
        self.R.append(tuple(float(q) for q in rot))
        self.C.append(tuple(float(q) for q in col))

    def c(self, center, size, col, rot=(0.0, 0.0, 0.0)):
        org = np.asarray(center, float) - _rmat(*rot) @ np.array((size[0] / 2, 0.0, 0.0))
        self.o(org, size, col, rot)

    def orb(self, center, d, col):
        self.o(center, (d, d, d), col)

    def __len__(self):
        return len(self.P)

    def arrays(self):
        n = len(self.P)
        assert n <= self.cap, f"인스턴스 칸 부족: {n} > {self.cap}"
        pad = self.cap - n
        z3 = [(0.0, 0.0, 0.0)] * pad
        return (np.array(self.P + z3, np.float32), np.array([1.0] * n + [0.0] * pad, np.float32),
                np.array(self.S + z3, np.float32), np.array(self.R + z3, np.float32), np.array(self.C + z3, np.float32))


def rot_cam(cam):
    """카메라 화면과 나란한 납작한 판의 오일러 회전: 상자 x = 앞(두께), y = 화면 가로, z = 화면 세로."""
    R = np.stack([cam["fwd"], -cam["right"], cam["up"]], 1)
    ry = -math.asin(max(-1.0, min(1.0, float(R[2, 0]))))
    return (math.atan2(float(R[2, 1]), float(R[2, 2])), ry, math.atan2(float(R[1, 0]), float(R[0, 0])))


def rot_to(d):
    """상자의 +x 축이 방향 d(단위벡터)를 향하게 하는 오일러 회전."""
    return (0.0, -math.asin(max(-1.0, min(1.0, float(d[2])))), math.atan2(float(d[1]), float(d[0])))


def sprite(G, cam, nx, ny, w, h, col, dist=100.0, thick=0.5, dx=0.0):
    """화면 좌표 (nx 오른쪽 +, ny 위 +, 둘 다 -1~1)에 정면을 보는 납작한 상자를 카메라에서 dist m 밖에 둠. w·h = 화면 높이에 대한 비율."""
    f = cam["lens"]
    d = cam["fwd"] + nx * (6.75 / f) * cam["right"] + (ny + 2.0 * cam["shift"]) * (12.0 / f) * cam["up"]
    d = d / np.linalg.norm(d)
    s = dist * 24.0 / f
    G.c(cam["loc"] + d * dist + cam["right"] * dx, (thick, w * s, h * s), col, rot_cam(cam))


def sprite_orb(OR, cam, nx, ny, dfrac, col, dist=100.0):
    """화면 좌표에 구를 둠 (dfrac = 화면 높이에 대한 지름 비율)."""
    f = cam["lens"]
    d = cam["fwd"] + nx * (6.75 / f) * cam["right"] + (ny + 2.0 * cam["shift"]) * (12.0 / f) * cam["up"]
    d = d / np.linalg.norm(d)
    OR.orb(cam["loc"] + d * dist, dfrac * dist * 24.0 / f, col)


def pop(tau, dur=0.30, over=3.0):
    """톡 튀어나오는 크기: 0 → 살짝 커졌다 → 1 (easeOutBack). tau<0이면 0."""
    if tau <= 0:
        return 0.0
    if tau >= dur:
        return 1.0
    x = tau / dur - 1.0
    return 1.0 + (over + 1.0) * x ** 3 + over * x ** 2


# ───────────────────────── 캐릭터 자세 (표준 자세 위에 팔·고개·입만 바꾼 원형 + 모자·후드) ─────────────────────────
SITS = ("sit", "sit_phone", "sit_conf")
# base = 바탕 자세, arms = ((오른팔 앞뒤, 옆), (왼팔 앞뒤, 옆)) 어깨 회전각(앞뒤 음수 = 앞으로 듦, 옆: 오른팔 +가 몸 쪽·왼팔 +가 바깥),
# mouth = open/smile/frown, head = 고개 숙임(+)/젖힘(−)
KINDS = {
    "look_up": dict(base="stand", head=-0.55),
    "look_up_h": dict(base="stand", head=-0.45, mouth="smile"),
    "pray_up": dict(base="stand", arms=((-1.45, 0.55), (-1.45, -0.55)), head=-0.42, mouth="smile"),
    "flash": dict(base="stand", arms=((-1.4, 0.0), (0.0, 0.0)), head=0.12),
    "grope_a": dict(base="walk_a", arms=((-1.5, 0.0), (-1.5, 0.0)), mouth="open"),
    "grope_b": dict(base="walk_b", arms=((-1.5, 0.0), (-1.5, 0.0)), mouth="open"),
    "ouch": dict(base="stand", arms=((-2.7, 0.0), (0.0, 0.0)), mouth="open", head=0.25),
    "point": dict(base="stand", arms=((-1.5, 0.0), (0.0, 0.0))),
    "dig": dict(base="stand", arms=((-0.9, 0.0), (-0.9, 0.0)), head=0.3),
    "carry_a": dict(base="walk_a", arms=((-0.9, 0.0), (0.0, 0.0)), mouth="smile"),
    "carry_b": dict(base="walk_b", arms=((-0.9, 0.0), (0.0, 0.0)), mouth="smile"),
}
ARMS = {"stand": (0.0, 0.0), "sit": (-0.6, -0.6), "phone": (-1.05, 0.0), "angry": (-2.5, -2.5), "confused": (-2.75, 0.05),
        "talk": (-0.9, 0.05), "walk_a": (0.35, -0.35), "walk_b": (-0.35, 0.35)}
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
    P = X._person(X.POSES[sp["base"]], lh)
    hip = 0.78
    hz = hip + 0.58
    legs, torso, head, arms = P[:4], P[4], list(P[5:-4]), P[-4:]

    def cube(cx, cy, z0, sx, sy, sz):
        return K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True)
    mouth = {"open": [(cube(0.232, 0, hz + 0.04, 0.02, 0.13, 0.07), 6)],
             "smile": [(cube(0.232, 0, hz + 0.04, 0.02, 0.11, 0.028), 6), (cube(0.232, -0.075, hz + 0.055, 0.02, 0.03, 0.04), 6),
                       (cube(0.232, 0.075, hz + 0.055, 0.02, 0.03, 0.04), 6)]}
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
    """표준 자세면 voxel 원형, 새 자세면 _variant. extra: 'hood'(민지 후드) · 'cap'(선장 모자)."""
    from engine import bkit as K
    P = _variant(pose, bool(hair)) if pose in KINDS else X._person(X.POSES[pose], bool(hair))
    hz = hip_of(pose) + 0.58
    if extra == "hood":                                            # 목 뒤 후드 (셔츠 색)
        P.append((K.bm_cube(0.14, 0.40, 0.22, (-0.20, 0, hz - 0.13), bottom=True), 0))
    elif extra == "cap":                                           # 선장 모자: 남색(바지 색) 윗판 + 검은 챙
        P.append((K.bm_cube(0.52, 0.52, 0.10, (0, 0, hz + 0.455), bottom=True), 1))
        P.append((K.bm_cube(0.14, 0.44, 0.03, (0.30, 0, hz + 0.455), bottom=True), 5))
    return P


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
    then (τ, 바뀐 자세) · alt (자세A, 자세B, 주기, 위상) 번갈아 · fall (τ0, τ1, 각도) 뒤로 넘어짐 · bob 위아래 흔들림."""
    return dict(set=set_, x=x, y=y, z=z, yaw=yaw, pose=pose, **kw)


MJ_AT = (0.0, -0.5)         # 해변에서 민지가 선 자리 (난간 앞)


ZT = (0.6, 0.35, 0.1, -0.15, -0.4, -0.65)       # 갯벌 계단 윗면 높이 (바다 쪽으로 갈수록 낮아짐), 한 칸 폭 4m, y = 4k ~ 4k+4
POLE = (2.8, -2.4)                                # 전봇대 자리 (해변 세트)


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    rs = np.random.default_rng(34)
    C = []
    L = IX

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))

    def extra(name, at, hair=None):
        add(name, int(rs.random() < 0.5) if hair is None else hair, EX_SH[int(rs.integers(len(EX_SH)))],
            X.PANTS[int(rs.integers(len(X.PANTS)))], at)
    # ── 민지 (하늘색 후드 · 긴 머리): 난간 앞에서 올려다봄
    mx, my = MJ_AT
    add("mj", 1, MJ_SH, MJ_PA, {
        L["hook"]: st("beach", mx, my, 90, "look_up"),
        L["dark"]: st("beach", mx, my, 90, "flash"),
        L["twist"]: st("beach", mx, my, 90, "look_up"),
        L["smile"]: st("beach", mx, my, 90, "look_up_h"),
        L["wish"]: st("beach", mx, my, 90, "pray_up"),
        L["cat"]: st("beach", mx, my, 90, "look_up_h")}, extra="hood")
    # ── 선장 아저씨 (주황 점퍼 · 모자): 항구 부두에서 눈금 기둥을 가리킴
    add("cp", 0, CAP_SH, CAP_PA, {
        L["captain"]: st("beach", BAYX + 2.9, -0.2, 142, "point", then=(1.3, "confused"))}, extra="cap")
    # ── 개그 1: 달 없는 밤길, 더듬거리며 걷다 전봇대에 쿵 (A) · 반대쪽에서 더듬거리는 사람 (B, C)
    px, py = POLE
    add("ga", 1, EX_SH[0], X.PANTS[1], {L["gag1"]: st("beach", px - 2.3, py, 0, "grope_a", v=(1.15, 0.0), stop=1.65,
                                                       pair=("grope_a", "grope_b"), cad=0.30, then=(1.7, "ouch"), fall=(1.85, 2.3, -1.45))})
    add("gb", 0, EX_SH[4], X.PANTS[0], {L["gag1"]: st("beach", px + 1.6, py - 0.9, 180, "grope_a", v=(-0.95, 0.0),
                                                       pair=("grope_a", "grope_b"), cad=0.34)})
    add("gc", 1, EX_SH[2], X.PANTS[3], {L["gag1"]: st("beach", px - 3.4, py + 0.9, 0, "grope_a", v=(0.85, 0.0),
                                                       pair=("grope_a", "grope_b"), cad=0.36)})
    # ── 일 년 뒤 밤 산책: 두 쌍이 반대로 걸으며 손에 작은 등을 듦
    for k, (x0, y0, yaw, v) in enumerate(((-0.4, -3.0, 0, 0.5), (-1.5, -3.0, 0, 0.5), (4.4, -2.0, 180, -0.5), (5.5, -2.0, 180, -0.5),
                                          (1.8, -4.2, 0, 0.4))):
        extra("st%d" % k, {L["adapt"]: st("beach", x0, y0, yaw, "carry_a", v=(v, 0.0), pair=("carry_a", "carry_b"), cad=0.44)})
    # ── 갯벌 사람들: 조개 캐다 물이 차오르는 걸 보고 어리둥절 (계단 칸 안에 서서)
    for k, (x, y, yaw) in enumerate(((-0.9, 2.6, -70), (1.0, 3.6, -100), (-1.7, 6.2, -110), (0.3, 7.0, -85), (1.8, 6.0, -65),
                                     (-2.8, 11.0, -95), (-0.6, 12.0, -80), (1.6, 11.5, -110), (3.0, 13.0, -90))):
        band = int(y // 4)
        pose = ("dig", "confused", "stand")[k % 3]
        extra("fl%d" % k, {L["flat"]: st("beach", FLX + x, y, yaw, pose, z=ZT[min(band, 5)],
                                        alt=(pose, "confused" if pose != "confused" else "stand", 1.2 + 0.2 * (k % 3), 0.3 * k))})
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
    if "then" in a and tau >= a["then"][0]:
        d["pose"] = a["then"][1]
    al = a.get("alt")
    if al:
        d["pose"] = al[int((t + al[3]) / al[2]) % 2]
    if moving and "pair" in a:
        cad = a.get("cad", 0.28)
        d["pose"] = a["pair"][int(t / cad) % 2]
        d["z"] += 0.03 * abs(math.sin(math.pi * t / cad))
    d["pitch"] = 0.0
    fl = a.get("fall")
    if fl:
        d["pitch"] = fl[2] * ramp(tau, fl[0], fl[1])
    d["scale"] = c["scale"]
    return d


# ───────────────────────── 세트 ─────────────────────────
STONE = (0.50, 0.52, 0.58)


def _lamp(v, x, y, name, h=3.8, energy=230.0):
    """가로등: 기둥 + 머리 + 따뜻한 발광판. 점광원 이름은 env()가 켜고 끔."""
    v.box(x - 0.06, x + 0.06, y - 0.06, y + 0.06, 0, h, (0.25, 0.26, 0.28))
    v.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, h, h + 0.12, (0.25, 0.26, 0.28))
    v.box(x - 0.16, x + 0.16, y - 0.16, y + 0.16, h - 0.05, h, (1.0, 0.85, 0.55), jit=0, glow=True)
    v.light(x, y, h - 0.3, energy, (1.0, 0.8, 0.55), 0.3, name)


def _beach(v):
    """밤 해변 마을: 돌바닥 산책로(y -6~0) · 난간(y 0) · 방파제 아래 바다(z -1.5) · 뒤쪽 가게 · 가로등 넷 · 전봇대."""
    rs = v.rs
    v.floor(-14, 14, -10, 0, STONE, 0.5, "check")
    for x in np.arange(-13.5, 14, 1.0):                                       # 난간 기둥 + 윗대·가운데대
        v.box(x - 0.04, x + 0.04, -0.04, 0.04, 0, 0.95, (0.78, 0.8, 0.84))
    v.box(-14, 14, -0.055, 0.055, 0.95, 1.03, (0.86, 0.88, 0.92))
    v.box(-14, 14, -0.03, 0.03, 0.50, 0.54, (0.78, 0.8, 0.84))
    v.box(-14, 14, 0.08, 0.4, -1.5, -0.01, (0.40, 0.42, 0.46))                # 방파제 벽 (바다 쪽)
    v.box(-420, 420, 0.4, 600, -1.9, -1.5, (0.035, 0.075, 0.17), jit=0)       # 바다
    signs = [(0.95, 0.3, 0.3), (0.3, 0.8, 1.0), (1.0, 0.8, 0.2), (0.4, 1.0, 0.5)]
    x, k = -14.0, 0
    while x < 14:                                                             # 산책로 뒤 가게 줄 (불 켠 창)
        w = float(rs.uniform(4.5, 6.0))
        X.storefront(v, x, min(14.0, x + w), -10.0, 5.0, float(rs.uniform(7, 10)), signs[k % 4], face=1, lit=0.5)
        x += w
        k += 1
    for n, lx in enumerate((-10.0, -4.0, 5.0, 11.0)):
        _lamp(v, lx, -1.6, "ep34_l%d" % n)
    px, py = POLE                                                             # 전봇대
    v.box(px - 0.12, px + 0.12, py - 0.12, py + 0.12, 0, 6.0, (0.40, 0.28, 0.18))
    v.box(px - 0.9, px + 0.9, py - 0.06, py + 0.06, 5.4, 5.5, (0.35, 0.25, 0.16))
    v.box(px - 0.6, px + 0.6, py - 0.05, py + 0.05, 4.9, 4.98, (0.35, 0.25, 0.16))
    for dx in (-0.8, 0.0, 0.8):
        v.box(px + dx - 0.04, px + dx + 0.04, py - 0.04, py + 0.04, 5.5, 5.62, (0.80, 0.82, 0.86))
    v.box(-14, 14, py - 0.01, py + 0.01, 5.66, 5.68, (0.08, 0.08, 0.1), jit=0)


def _bay(v):
    """새벽 항구 (해변 세트 안 x=BAYX): 부두 바닥 · 잔교 · 눈금 기둥(만조선 빨강·간조선 파랑) · 바닷속 바닥. 물은 매 프레임 상자로."""
    v.floor(-8, 8, -6, -1, (0.55, 0.50, 0.45), 0.5, "check")
    v.box(-8, 8, -1.0, -0.8, -6.0, -0.01, (0.40, 0.38, 0.36))                  # 부두 벽
    v.box(-0.8, 3.6, -0.8, 0.6, -0.4, -0.01, (0.46, 0.33, 0.21))             # 잔교 널
    v.box(-30, 30, -0.8, 24, -6.3, -6.0, (0.10, 0.14, 0.18), jit=0.02)        # 바다 바닥
    v.box(1.35, 1.65, 0.75, 1.05, -3.0, 3.4, (0.88, 0.88, 0.84))              # 눈금 기둥
    for k in range(12):
        if k % 2:
            v.box(1.34, 1.66, 0.74, 1.06, -3.0 + 0.5 * k, -2.5 + 0.5 * k, (0.10, 0.10, 0.12), jit=0)
    v.box(0.6, 2.4, 0.66, 1.14, -0.22, -0.18, (0.95, 0.15, 0.15), jit=0, glow=True)     # 만조선
    v.box(0.6, 2.4, 0.66, 1.14, -2.02, -1.98, (0.2, 0.45, 1.0), jit=0, glow=True)     # 간조선
    for x0, x1, h, c in ((-8, -2, 6.0, (0.95, 0.5, 0.4)), (-2, 5, 7.5, (0.4, 0.8, 1.0)), (5, 8, 5.5, (1.0, 0.8, 0.3))):
        X.storefront(v, x0, x1, -6.5, 5.0, h, c, face=1, lit=0.3)
    v.box(-5.2, -4.6, -4.2, -3.6, 0, 0.8, (0.55, 0.40, 0.25))                  # 부두 통 · 상자
    v.box(-4.4, -3.9, -3.6, -3.0, 0, 0.5, (0.35, 0.50, 0.65))


def _flats(v):
    """갯벌 (해변 세트 안 x=FLX): 바다 쪽으로 낮아지는 계단 여섯 칸 + 웅덩이 · 바닷가 둑."""
    mud = ((0.46, 0.39, 0.31), (0.51, 0.43, 0.34))
    for k in range(6):
        v.box(-14, 14, 4 * k, 4 * k + 4, -3.2, ZT[k], mud[k % 2], jit=0.03)
    v.box(-14, 14, -8, 0, -3.2, 0.7, (0.32, 0.45, 0.25), jit=0.05)            # 둑 (풀밭)
    for x0, x1, y0, y1, k in ((-6, -3, 2.0, 3.4, 0), (2, 5.5, 5.5, 7.0, 1), (-2, 1, 9.5, 11.0, 2), (4, 7, 12.5, 14, 3)):
        v.box(x0, x1, y0, y1, ZT[k], ZT[k] + 0.012, (0.20, 0.28, 0.34), jit=0)   # 물웅덩이
    rs = v.rs
    for _ in range(26):                                                       # 조개 껍데기
        x, y = float(rs.uniform(-12, 12)), float(rs.uniform(0.3, 15.0))
        z = ZT[int(y // 4)]
        v.box(x, x + 0.1, y, y + 0.08, z, z + 0.04, (0.92, 0.9, 0.82), jit=0.03)
    X.storefront(v, -14, -5, -9.0, 5.0, 6.0, (0.95, 0.5, 0.4), face=1, lit=0.3)


def _tuft(v, x, y, rs):
    h = float(rs.uniform(0.25, 0.6))
    for dx, dy in ((0.0, 0.0), (0.07, 0.03), (-0.06, 0.05)):
        hh = h * float(rs.uniform(0.6, 1.0))
        v.box(x + dx - 0.025, x + dx + 0.025, y + dy - 0.025, y + dy + 0.025, 0, hh, (0.16, 0.34 + 0.1 * float(rs.random()), 0.14))


def _meadow(v):
    """밤 풀밭: 어두운 풀 바닥 · 풀 포기 · 꽃 · 돌 · 먼 숲. 쇠똥구리 길(y≈1)은 비워 둠."""
    rs = v.rs
    v.floor(-9, 9, -6, 9, (0.10, 0.23, 0.10), 0.5, "check")
    for _ in range(190):
        x, y = float(rs.uniform(-8.6, 8.6)), float(rs.uniform(-5.6, 8.6))
        if abs(y - 1.0) < 1.1 and abs(x) < 4.0:
            continue
        _tuft(v, x, y, rs)
    for x, y, c in ((-3.2, 2.6, (1.0, 0.95, 0.7)), (3.6, 3.1, (1.0, 0.85, 0.4)), (-4.4, 0.2, (0.95, 0.7, 0.85)), (4.8, -0.4, (1.0, 0.95, 0.7))):
        v.box(x - 0.015, x + 0.015, y - 0.015, y + 0.015, 0, 0.55, (0.2, 0.45, 0.2))
        v.box(x - 0.07, x + 0.07, y - 0.07, y + 0.07, 0.55, 0.62, c, jit=0.02)
    for x, y, s in ((-5.5, 4.0, 0.7), (5.2, 5.5, 0.9), (2.5, 7.0, 0.8)):
        v.box(x - s, x + s, y - s * 0.8, y + s * 0.8, 0, s * 0.8, (0.40, 0.42, 0.46), jit=0.05)
    for x in np.arange(-9.0, 9.0, 3.0):                                       # 먼 숲 (낮고 어두운 덩어리, y를 조금씩 어긋나게)
        v.box(x, x + 2.6, 9.5 + 0.13 * x % 0.6, 12.0, 0, float(rs.uniform(0.9, 1.5)), (0.07, 0.17, 0.09), jit=0.04)
    v.light(0.0, -1.0, 2.4, 55, (0.6, 0.72, 1.0), 1.0, "ep34_mw_fill")


CORAL_COL = [(0.95, 0.45, 0.60), (0.95, 0.58, 0.25), (0.62, 0.42, 0.82), (0.72, 0.86, 0.36), (0.35, 0.78, 0.78), (0.95, 0.80, 0.35)]
CORALS = [(-2.0, 2.2, "branch", 0), (-0.8, 3.2, "brain", 1), (0.3, 2.3, "branch", 2), (1.4, 3.4, "branch", 5), (2.3, 2.1, "brain", 4),
          (-1.5, 4.4, "branch", 3), (0.0, 5.0, "fan", 0), (1.7, 4.8, "branch", 1), (-3.2, 3.6, "fan", 3), (3.3, 3.8, "fan", 2),
          (-0.4, 1.0, "tube", 3), (1.0, 1.2, "tube", 5), (-2.4, 0.8, "tube", 0), (2.6, 0.7, "tube", 2)]
EGG_SRC = [(x, y, 0.95 if k == "branch" else 0.5) for x, y, k, _ in CORALS if k in ("branch", "brain")]   # 알이 떠오르는 산호 위 자리


def _coral(v, x, y, kind, ci):
    c = CORAL_COL[ci]
    if kind == "branch":
        v.box(x - 0.1, x + 0.1, y - 0.1, y + 0.1, 0, 0.6, c)
        v.box(x - 0.07, x + 0.07, y - 0.07, y + 0.07, 0.6, 0.95, c)
        v.box(x + 0.1, x + 0.38, y - 0.06, y + 0.06, 0.3, 0.42, c)
        v.box(x + 0.3, x + 0.42, y - 0.05, y + 0.05, 0.42, 0.75, c)
        v.box(x - 0.36, x - 0.1, y - 0.06, y + 0.06, 0.4, 0.5, c)
        v.box(x - 0.36, x - 0.26, y - 0.05, y + 0.05, 0.5, 0.8, c)
    elif kind == "brain":
        for w, z0 in ((0.5, 0.0), (0.38, 0.17), (0.24, 0.32)):
            v.box(x - w, x + w, y - w * 0.8, y + w * 0.8, z0, z0 + 0.17, c, jit=0.05)
    elif kind == "fan":
        v.box(x - 0.45, x + 0.45, y - 0.04, y + 0.04, 0.0, 0.2, c)
        v.box(x - 0.55, x + 0.55, y - 0.035, y + 0.035, 0.2, 0.75, c, jit=0.06)
    else:
        for dx in (-0.12, 0.0, 0.12):
            v.box(x + dx - 0.04, x + dx + 0.04, y - 0.04, y + 0.04, 0, 0.3 + 0.12 * (dx != 0.0), c)


def _reef(v):
    """바닷속 산호밭: 모래 바닥 · 산호 열네 무리 · 뒤 바위벽. 알(분홍 구슬)은 매 프레임 구로."""
    rs = v.rs
    v.floor(-8, 8, -4, 8, (0.72, 0.68, 0.55), 0.5, "check")
    for x, y, kind, ci in CORALS:
        _coral(v, x, y, kind, ci)
    for x in np.arange(-8.0, 8.0, 2.0):
        v.box(x, x + 1.8, 8.0 + 0.1 * (x % 0.7), 10.0, 0, float(rs.uniform(1.0, 2.0)), (0.14, 0.26, 0.32), jit=0.05)
    v.light(0.0, -1.0, 2.6, 95, (0.55, 0.78, 1.0), 1.0, "ep34_rf_fill")


DESK_Z = 0.74
GLOBE_AT = (-0.45, 1.45, DESK_Z + 0.32)                   # 지구본 가운데
MOONBOX_AT = (0.45, 1.45, DESK_Z + 0.36)
CLK_AT = (0.75, 1.95, 0.42)                                # 벽시계: x, 벽에서 앞으로 나오는 높이 z, 반지름 (y=2.5 벽)
FOS_AT = (0.8, 1.55)                                       # 산호 화석 단면 (x, y)


def _study(v):
    """서재 책상 (밤): 뒷벽 창·벽시계 판 · 책상 위 스탠드·지구본 받침·화석 받침. 지구본·달 상자·시계 눈금은 매 프레임."""
    v.floor(-3, 3, -2.5, 2.5, (0.62, 0.45, 0.30), 0.25, "wood")
    wb = (0.34, 0.40, 0.55)
    v.wall((-3, 2.5), (3, 2.5), 0, 2.9, wb, 0.25, face=-1)
    v.wall((-3, -2.5), (-3, 2.5), 0, 2.9, (0.30, 0.36, 0.50), 0.25, face=-1)
    v.wall((3, -2.5), (3, 2.5), 0, 2.9, (0.30, 0.36, 0.50), 0.25, face=1)
    v.window(-2.7, -1.3, 2.49, 1.0, 2.3, night=True, lights=5)
    cx, cz, r = CLK_AT[0], CLK_AT[1], CLK_AT[2]
    v.box(cx - r - 0.05, cx + r + 0.05, 2.43, 2.48, cz - r - 0.05, cz + r + 0.05, (0.20, 0.20, 0.22), jit=0)   # 벽시계 테두리·판 (벽에서 0.02 띄움)
    v.box(cx - r, cx + r, 2.42, 2.43, cz - r, cz + r, (0.97, 0.96, 0.93), jit=0)
    X.table(v, 0.0, 1.45, 2.6, 0.95, DESK_Z, (0.70, 0.52, 0.34))
    v.box(-0.45 - 0.14, -0.45 + 0.14, 1.45 - 0.14, 1.45 + 0.14, DESK_Z, DESK_Z + 0.04, (0.35, 0.28, 0.2))        # 지구본 받침
    v.box(0.45 - 0.14, 0.45 + 0.14, 1.45 - 0.14, 1.45 + 0.14, DESK_Z, DESK_Z + 0.04, (0.35, 0.28, 0.2))         # 달 상자 받침
    fx, fy = FOS_AT
    v.box(fx - 0.22, fx + 0.22, fy - 0.12, fy + 0.12, DESK_Z, DESK_Z + 0.03, (0.35, 0.28, 0.2))               # 화석 받침
    v.box(fx - 0.19, fx + 0.19, fy - 0.03, fy + 0.03, DESK_Z + 0.03, DESK_Z + 0.37, (0.84, 0.78, 0.64), jit=0.02)   # 화석 단면 판
    for k in range(15):                                                                                       # 성장선(앞면에 얇게 튀어나온 줄무늬)
        z0 = DESK_Z + 0.06 + 0.02 * k
        v.box(fx - 0.17 + 0.004 * (k % 3), fx + 0.17 - 0.004 * (k % 3), fy - 0.036, fy - 0.03, z0, z0 + 0.008, (0.45, 0.36, 0.26), jit=0)
    v.box(-1.2, -1.14, 1.2, 1.26, DESK_Z, DESK_Z + 0.4, (0.3, 0.3, 0.32), jit=0)                              # 스탠드
    v.box(-1.3, -1.04, 1.1, 1.36, DESK_Z + 0.4, DESK_Z + 0.46, (1.0, 0.85, 0.6), jit=0, glow=True)
    v.box(-1.5, -1.2, 1.7, 1.9, DESK_Z, DESK_Z + 0.06, (0.9, 0.35, 0.3))                                      # 책 몇 권
    v.box(-1.45, -1.18, 1.72, 1.88, DESK_Z + 0.06, DESK_Z + 0.11, (0.3, 0.55, 0.85))
    v.light(-1.0, 1.0, 1.3, 55, (1.0, 0.8, 0.55), 0.3, "ep34_st_lamp")
    v.light(0.0, 0.5, 2.6, 110, (1.0, 0.92, 0.8), 0.6, "ep34_st_ceil")


def _beach_all(v):
    """해변 세트 = 마을(0) + 새벽 항구(BAYX) + 갯벌(FLX)이 x로 나란히."""
    ox, oy = OFF["beach"]
    _beach(v)
    v.at(ox + BAYX, oy)
    _bay(v)
    v.at(ox + FLX, oy)
    _flats(v)
    v.at(ox, oy)


def _sets():
    return (("beach", _beach_all), ("meadow", _meadow), ("reef", _reef), ("study", _study))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL · 점광원 LT) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 560, 400, 220, 8
MOON_C, MOON_CR = (2.6, 2.8, 3.2), (1.35, 1.55, 2.1)       # 달 몸·크레이터 (선형 발광 색)
SUN_C = (6.0, 4.4, 1.5)
WATER_C = (0.10, 0.32, 0.50)
MID_Z, AMP = -1.1, 0.9                                     # 항구 물높이 가운데·진폭(m): 눈금 기둥의 만조선 -0.2 · 간조선 -2.0과 같음
CRATERS = ((-0.28, 0.22, 0.20), (0.24, -0.20, 0.16), (0.14, 0.30, 0.10), (-0.10, -0.38, 0.12))


def moon_sky(G, OR, i, tau, cam):
    """하늘의 달: 발광 구 + 크레이터 상자(카메라를 향함). 사라지는 줄은 moon_k가 0이 되면 그리지 않음. 반환: 달 크기 배율."""
    k = moon_k(i, tau)
    if k <= 0.0 or "moon" not in LINES[i]:
        return 0.0
    D = moon_dir(i)
    rm = R_FAR * math.tan(math.radians(LINES[i]["moon"][2]) * k)
    c = cam["loc"] + D * R_FAR
    dim = 0.5 if set_of(i) == "reef" else 1.0
    OR.orb(c, 2 * rm, tuple(q * dim for q in MOON_C))
    rg = np.cross(D, (0.0, 0.0, 1.0))
    rg /= np.linalg.norm(rg)
    up = np.cross(rg, D)
    for dx, dz, r in CRATERS:
        depth = rm * math.sqrt(max(0.0, 1.0 - dx * dx - dz * dz)) + 0.012 * rm
        G.c(c - D * depth + rg * dx * rm + up * dz * rm, (0.02 * rm, 2 * r * rm, 2 * r * rm), tuple(q * dim for q in MOON_CR), rot_cam(cam))
    return k


def moon_road(G, cam, i, k):
    """바다 위 은빛 달빛 길: 달 방향 수직면을 따라 가는 발광 판을 멀수록 길고 넓게 (서로 겹치지 않음)."""
    D = moon_dir(i)
    az = math.atan2(D[1], D[0])
    ca, sa = math.cos(az), math.sin(az)
    if sa < 0.2 or set_of(i) != "beach":
        return
    r0 = max(4.0, (1.4 - (cam["loc"][1] - OFF["beach"][1])) / sa)
    n = 14
    for j in range(n):
        r = r0 * (110.0 / r0) ** (j / (n - 1))
        w = (0.5 + 0.09 * r) * (0.75 + 0.5 * ((j * 7) % 5) / 4.0) * k
        G.c((cam["loc"][0] + ca * r, cam["loc"][1] + sa * r, -1.5 + 0.02 + 0.0015 * j), (0.05 * r + 0.2, w, 0.02), (1.8, 2.1, 2.7), (0.0, 0.0, az))


def glyph(G, pat, x, y, z, cell, col):
    """앞(−y쪽 카메라)을 보는 도트 그림: (x, z)는 왼쪽 위 칸 가운데."""
    for r, row in enumerate(pat):
        for c_, ch in enumerate(row):
            if ch == "#":
                G.c((x + c_ * cell, y, z - r * cell), (cell * 0.92, 0.02, cell * 0.92), col)


SNOW = ["#.#.#", ".###.", "#####", ".###.", "#.#.#"]
FLOWER = [".#.#.", "#####", ".#.#.", "#####", ".#.#."]
MAPLE = ["..#..", "#.#.#", ".###.", "#####", "..#.."]
SEASONS = ((SNOW, (3.0, 3.4, 4.0)), (FLOWER, (4.0, 1.3, 2.2)), (MAPLE, (4.0, 1.4, 0.3)))


def sprite_arrow(G, cam, x0, ny, lnx, col):
    """화면 좌표 오른쪽을 가리키는 도트 화살표: x0에서 lnx(nx 단위, 1 = 화면 반폭)만큼. 1 nx = 0.28125 화면높이."""
    sprite(G, cam, x0 + lnx / 2, ny, lnx * 0.28125, 0.014, col, 100.0, 0.4)
    sprite(G, cam, x0 + lnx, ny, 0.05, 0.05, col, 99.0, 0.4)


def bay_level(i, tau):
    """새벽 항구 물높이: 8번 줄은 느리게 한 번 크게, 10번 줄은 오르내리다 폭이 평균의 46%로 줄어듦."""
    if i == IX["captain"]:
        return MID_Z + AMP * math.sin(2 * math.pi * tau / 3.4 - 0.6)
    a = AMP * (1.0 - 0.54 * ramp(tau, 0.9, 1.7))
    return MID_Z + a * math.sin(2 * math.pi * tau / 2.3 + 0.9)


def flat_level(tau):
    """갯벌 바닷물: 밀려 들어오는 높이 (조수 폭이 줄어 간조 때도 물이 더 높음 → 드러난 갯벌이 줄어듦)."""
    return -0.62 + 0.82 * ramp(tau, 0.1, 2.3)


def water_box(F, cx, cy, sx, sy, z_bot, level, col=WATER_C):
    F.c((cx, cy, (z_bot + level) / 2), (sx, sy, level - z_bot), col)


def props_beach(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    L = IX
    k = 0.0
    if i in MOON_LINES:
        k = moon_sky(G, OR, i, tau, cam)
        if k > 0.0:
            moon_road(G, cam, i, k)
    mj = S.get("mj")
    if mj is not None:
        tg = rel(mj, 0.0, 0.0, 1.55)
        if k > 0.0:                                                   # 약한 푸른 점광원 (달과 함께 켜지고 꺼짐)
            LT.append(((tg[0] - 0.9, tg[1] - 1.8, tg[2] + 1.0), "moon", 120.0))
    if i == L["dark"] and mj is not None:                             # 휴대폰 손전등 (0.25초에 켜짐)
        hp = hand_pt(mj, "R", 0.1)
        ya = math.radians(mj["yaw"])
        on = pop(tau - 0.25, 0.3, 1.0)
        F.c((hp[0], hp[1], hp[2]), (0.09, 0.05, 0.17), (0.1, 0.1, 0.12), (0.0, 0.0, ya))
        G.c((hp[0] + math.cos(ya) * 0.045, hp[1] + math.sin(ya) * 0.045, hp[2]), (0.015, 0.075, 0.15),
            (5.0 * on + 0.3, 4.8 * on + 0.3, 4.0 * on + 0.3), (0.0, 0.0, ya))
        LT.append(((hp[0] + math.cos(ya) * 0.35, hp[1] + math.sin(ya) * 0.35, hp[2] + 0.1), "warm", 30.0 * on))
    if i == L["gag1"]:                                                 # 개그 1: 쿵 — 별이 돌고 먼지가 퍼짐
        ga = S.get("ga")
        if ga is not None and tau > 1.7:
            hd = head_pt(ga)
            te = tau - 1.7
            for n in range(5):
                a = 6.0 * te + n * 2 * math.pi / 5
                G.c((hd[0] + 0.28 * math.cos(a), hd[1] + 0.28 * math.sin(a) * 0.5, hd[2] + 0.18 + 0.05 * math.sin(3 * te + n)),
                    (0.08, 0.08, 0.08), (4.0, 3.2, 0.5), (0.0, 0.0, a))
            px, py = POLE
            for n in range(7):                                         # 전봇대 앞 먼지·충격 조각
                a = n * 2 * math.pi / 7
                r = 0.15 + 0.7 * min(te / 0.5, 1.0)
                s = 0.12 * (1.0 - min(te / 0.9, 1.0))
                if s > 0.01:
                    G.c((px + 0.15 + r * math.cos(a), py - 0.3 + r * math.sin(a) * 0.5, 0.2 + 0.4 * min(te / 0.5, 1.0)),
                        (s, s, s), (1.6, 1.5, 1.3), (0.0, 0.0, a))
    if i == L["adapt"]:                                                # 산책하는 사람들이 든 작은 등
        for n in range(5):
            d = S.get("st%d" % n)
            if d is None:
                continue
            hp = hand_pt(d, "R", 0.02)
            F.c((hp[0], hp[1], hp[2] + 0.01), (0.05, 0.05, 0.03), (0.2, 0.2, 0.22))
            G.c((hp[0], hp[1], hp[2] - 0.06), (0.09, 0.09, 0.12), (3.2, 2.1, 0.8))
    if i == L["cat"]:                                                  # 달 앞을 지나는 큰 고양이 실루엣
        cat_items(F, G, tau, dur)
    if i == L["ratio"]:                                                # 하늘 비교 컷: 큰 해 상자 vs 작고 흐린 달 (1 nx = 0.28125 화면높이)
        pul = 1.0 + 0.03 * math.sin(tau * 5.0)
        a = pop(tau - 0.05, 0.35, 1.4)
        nx0, ny0 = -0.28, -0.06
        sprite(G, cam, nx0, ny0, 0.22 * a * pul, 0.22 * a * pul, SUN_C, 100.0, 0.5)
        for n in range(8):
            ang = n * math.pi / 4 + 0.15 * math.sin(tau)
            sprite(G, cam, nx0 + 0.17 * math.cos(ang) / 0.28125, ny0 + 2 * 0.17 * math.sin(ang), 0.03 * a, 0.03 * a, (5.0, 3.4, 0.9), 99.0, 0.4)
        sprite_orb(OR, cam, 0.58, -0.06, 0.07 * pop(tau - 0.45, 0.35, 1.4), (0.85, 0.95, 1.2))
    if i == L["force"]:                                                # 조수 힘 비교: 해 상자·화살표 짧게 / 달 상자·화살표 2.2배
        g = ramp(tau, 0.25, 1.35)
        sprite(G, cam, -0.72, 0.14, 0.095, 0.095, SUN_C, 100.0, 0.5)
        sprite_orb(OR, cam, -0.72, -0.20, 0.095, (0.95, 1.05, 1.3))
        for ny, ln, col in ((0.14, 0.50, (5.0, 3.0, 0.7)), (-0.20, 0.50 * 2.2, (2.2, 3.0, 5.0))):
            if ln * g > 0.02:
                sprite_arrow(G, cam, -0.50, ny, ln * g, col)
    if i in (L["captain"], L["gauge"]):                                # 새벽 항구: 물이 오르내림
        lev = bay_level(i, tau)
        bx = OFF["beach"][0] + BAYX
        water_box(F, bx, 11.6, 60.0, 24.8, -5.99, lev)
        for n in range(6):                                             # 물결 반짝임 (물 위 얇은 판, 서로 겹치지 않게)
            sx = bx - 3.0 + 1.6 * n + 0.4 * math.sin(tau * 1.5 + n)
            G.c((sx, 2.0 + 1.1 * (n % 3), lev + 0.012 + 0.001 * n), (0.7, 0.05, 0.012), (1.8, 1.3, 1.0))
        if i == L["gauge"] and tau > 1.5:                              # 줄어든 새 폭(평균의 약 46%)을 노란 표시로
            a = AMP * 0.46
            for zz in (MID_Z + a, MID_Z - a):
                G.c((bx + 1.5, 0.67, zz), (1.2, 0.04, 0.05), (3.4, 2.8, 0.4))
    if i == L["flat"]:                                                 # 갯벌: 바닷물이 차올라 드러난 갯벌이 줄어듦
        fx = OFF["beach"][0] + FLX
        lev = flat_level(tau)
        water_box(F, fx, 20.0, 60.0, 40.2, -3.15, lev, (0.12, 0.34, 0.50))
        for n in range(5):                                             # 물과 계단이 만나는 선에 거품 한 줄
            if ZT[n] >= lev > ZT[n + 1]:
                G.c((fx, 4 * (n + 1) + 0.03, lev + 0.014), (28.0, 0.06, 0.012), (1.6, 1.8, 2.0))
    return k


def cat_items(F, G, tau, dur):
    """큰 고양이 실루엣(검정): 난간 위를 오른쪽에서 왼쪽으로 걸어 달 앞을 지나감. 몸·머리·귀·꼬리·다리 네 개."""
    s = 1.5
    cx = 2.6 - 5.2 * (tau / max(dur, 1e-3))
    base = (cx, 0.0, 1.03)
    ph = tau * 7.0
    blk = (0.012, 0.012, 0.016)

    def P(dx, dy, dz):
        return (base[0] + dx * s, base[1] + dy * s, base[2] + dz * s)
    F.c(P(0.0, 0.0, 0.55), (0.95 * s, 0.34 * s, 0.38 * s), blk)
    F.c(P(-0.58, 0.0, 0.80), (0.34 * s, 0.30 * s, 0.30 * s), blk)
    for sy in (-0.1, 0.1):
        F.c(P(-0.62, sy, 1.02), (0.10 * s, 0.08 * s, 0.16 * s), blk)
    F.c(P(0.56, 0.0, 0.62), (0.28 * s, 0.08 * s, 0.08 * s), blk)
    F.c(P(0.76, 0.0, 0.80), (0.08 * s, 0.08 * s, 0.34 * s), blk, (0.0, 0.0, 0.0))
    F.c(P(0.80 + 0.05 * math.sin(ph), 0.0, 1.0), (0.10 * s, 0.08 * s, 0.14 * s), blk)
    for n, (lx, ly) in enumerate(((-0.34, -0.1), (-0.34, 0.1), (0.34, -0.1), (0.34, 0.1))):
        sw = 0.45 * math.sin(ph + (math.pi if n % 3 else 0.0))
        F.c(P(lx, ly, 0.22), (0.10 * s, 0.10 * s, 0.44 * s), blk, (0.0, sw, 0.0))
    G.c(P(-0.755, -0.155, 0.84), (0.02, 0.07 * s, 0.07 * s), (0.5, 3.0, 0.9))


def _h(n):
    """결정적 의사난수 0~1."""
    return (math.sin(n * 12.9898 + 4.1414) * 43758.5453) % 1.0


# ── 풀밭: 쇠똥구리가 똥공을 직선으로 굴려 가다(4번 줄), 달이 사라지면 공 둘레를 빙글빙글(5번 줄)
BT_X0, BT_SP, BT_Y, BT_R = -2.0, 1.25, 1.0, 0.55
BT_XE = BT_X0 + BT_SP * (STARTS[IX["dizzy"]] - STARTS[IX["beetle"]])           # 4번 줄이 끝날 때 쇠똥구리 x
LINES[IX["beetle"]]["track"] = BT_SP
LINES[IX["beetle"]]["shot"] = ("meadow", (BT_X0 + 0.3, BT_Y, 0.22), -90, 3, 2.4, 28, 1.0, 3)
_CX5 = BT_XE + BT_SP * VANISH[IX["dizzy"]] + 0.55                              # 5번 줄 공이 멈추는 자리(원의 가운데)
LINES[IX["dizzy"]]["shot"] = ("meadow", (_CX5 - 0.05, BT_Y, 0.22), -86, 5, 2.6, 28, 0.92, 4)


def beetle_state(i, tau):
    """(쇠똥구리 (x,y), 방향 rad, 공 (x,y), 궤적 점 목록, 어지러움 0/1)"""
    if i == IX["beetle"]:
        x = BT_X0 + BT_SP * tau
        return (x, BT_Y), 0.0, (x + 0.55, BT_Y), [(BT_X0 + 0.17 * k, BT_Y) for k in range(int((x - BT_X0 - 0.2) / 0.17) + 1)], 0.0
    v = VANISH[IX["dizzy"]]
    if tau < v:
        x = BT_XE + BT_SP * tau
        tr = [(BT_X0 + 0.17 * k, BT_Y) for k in range(int((x - BT_X0 - 0.2) / 0.17) + 1) if BT_X0 + 0.17 * k > x - 1.8]
        return (x, BT_Y), 0.0, (x + 0.55, BT_Y), tr, 0.0
    th = math.pi + 5.5 * (tau - v)
    pos = (_CX5 + BT_R * math.cos(th), BT_Y + BT_R * math.sin(th))
    tr = [(_CX5 + BT_R * math.cos(a), BT_Y + BT_R * math.sin(a)) for a in np.arange(math.pi, th, 0.42)]
    tr += [(BT_XE + BT_SP * v - 0.17 * k, BT_Y) for k in range(1, 7)]
    return pos, th + math.pi / 2, (_CX5, BT_Y), tr, 1.0


def bt_box(F, p, psi, lc, size, col, rz=0.0, sc=1.25):
    c, s = math.cos(psi), math.sin(psi)
    F.c((p[0] + sc * (c * lc[0] - s * lc[1]), p[1] + sc * (s * lc[0] + c * lc[1]), sc * lc[2]), tuple(q * sc for q in size), col, (0.0, 0.0, psi + rz))


def props_meadow(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    moon_sky(G, OR, i, tau, cam)
    p, psi, ball, trail, diz = beetle_state(i, tau)
    ox = OFF["meadow"][0]
    p, ball = (p[0] + ox, p[1]), (ball[0] + ox, ball[1])
    body, shell = (0.16, 0.19, 0.32), (0.42, 0.55, 0.95)
    bt_box(F, p, psi, (-0.04, 0.0, 0.17), (0.30, 0.22, 0.16), body)
    bt_box(F, p, psi, (-0.04, 0.0, 0.262), (0.22, 0.03, 0.02), shell)
    bt_box(F, p, psi, (0.17, 0.0, 0.17), (0.14, 0.18, 0.13), body)
    bt_box(F, p, psi, (0.27, 0.0, 0.15), (0.10, 0.15, 0.11), body)
    bt_box(F, p, psi, (0.345, 0.0, 0.205), (0.08, 0.03, 0.06), body)
    for sy in (-0.05, 0.05):
        c, s = math.cos(psi), math.sin(psi)
        G.c((p[0] + 1.25 * (c * 0.325 - s * sy), p[1] + 1.25 * (s * 0.325 + c * sy), 0.19 * 1.25), (0.03, 0.04, 0.04), (3.0, 3.0, 3.0), (0.0, 0.0, psi))
    ph = 14.0 * t
    for side in (-1, 1):
        for j in range(3):
            sw = 0.5 * math.sin(ph + j * 2.1 + (math.pi if side > 0 else 0.0))
            bt_box(F, p, psi, (0.03 + 0.1 * j, side * 0.15, 0.08), (0.04, 0.16, 0.03), body, rz=side * (0.5 + sw))
    BL.orb((ball[0], ball[1], 0.2), 0.40, (0.30, 0.19, 0.10))
    for n, (tx, ty) in enumerate(trail[:40]):
        G.c((tx + ox, ty, 0.014), (0.10, 0.04, 0.012), (0.7, 2.0, 3.0))
    if diz > 0.0 and tau > VANISH[IX["dizzy"]] + 0.2:                  # 어지러워서 머리 위를 도는 별
        for n in range(3):
            a = 7.0 * tau + n * 2.1
            G.c((p[0] + 0.2 * math.cos(a), p[1] + 0.2 * math.sin(a), 0.5 + 0.03 * math.sin(5 * tau + n)), (0.07, 0.07, 0.07), (4.0, 3.2, 0.5), (0.0, 0.0, a))


# ── 바닷속: 달빛 아래 산호 위로 분홍 알이 한꺼번에 떠오름(6번 줄), 달이 사라지면 제각각·적게(7번 줄)
EGG_N = 16
EGGS = []
for _si, _s in enumerate(EGG_SRC):
    for _m in range(EGG_N):
        _n = _si * EGG_N + _m
        EGGS.append(dict(src=_s, ts=0.15 + 0.7 * _h(_n), v=0.5 + 0.35 * _h(_n + 100), dx=(_h(_n + 200) - 0.5) * 0.4, dy=(_h(_n + 300) - 0.5) * 0.3,
                         ph=6.3 * _h(_n + 400), keep=(_n % 3 == 0), vel=((_h(_n + 500) - 0.5) * 0.7, (_h(_n + 600) - 0.5) * 0.5, (_h(_n + 700) - 0.35) * 0.4)))
EGG_T6 = STARTS[IX["scatter"]] - STARTS[IX["coral"]]


def egg_at(e, T):
    """알 e의 T초(6번 줄 시작부터)에서의 (x, y, z, 크기 배율)."""
    sx, sy, z0 = e["src"]
    if T < e["ts"]:
        return None
    k = pop(T - e["ts"], 0.25, 1.5)
    x = sx + e["dx"] + 0.05 * math.sin(3.0 * T + e["ph"])
    y = sy + e["dy"] + 0.04 * math.cos(2.5 * T + e["ph"])
    z = z0 + 0.1 + e["v"] * (T - e["ts"])
    tv = EGG_T6 + VANISH[IX["scatter"]]
    if T > tv:                                                          # 달이 사라진 뒤: 제각각 흩어지고 일부는 사라짐
        d = T - tv
        x += e["vel"][0] * d
        y += e["vel"][1] * d
        z += (e["vel"][2] - e["v"]) * d + 0.0
        if not e["keep"]:
            k *= 1.0 - ramp(d, 0.0, 0.5)
    return x, y, z, k


def props_reef(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    moon_sky(G, OR, i, tau, cam)
    T = tau if i == IX["coral"] else EGG_T6 + tau
    ox, oy = OFF["reef"]
    for e in EGGS:
        r = egg_at(e, T)
        if r is not None and r[3] > 0.01:
            OR.orb((r[0] + ox, r[1] + oy, r[2]), 0.075 * r[3], (2.8, 1.0, 1.8))
    if i == IX["coral"]:                                               # 산란 순간 산호 위가 분홍빛으로
        for sx, sy, z0 in EGG_SRC:
            g = ramp(tau, 0.1, 0.5)
            G.c((sx + ox, sy + oy, z0 + 0.03), (0.28, 0.28, 0.03), (1.6 * g, 0.5 * g, 0.9 * g))
    if moon_k(i, tau) > 0.0:
        LT.append(((ox, oy - 0.5, 3.2), "moon", 90.0))


# ── 서재 책상: 지구본(속이 빈 블록 구)·달 상자·축 막대·계절 아이콘·거리 막대·화석·벽시계
def globe_cells(R=0.2, cell=0.05):
    """블록 지구본: 속이 빈 구 껍질 [(x, y, z, 색)] — 바다 파랑·땅 초록·극지 흰색. z가 극축."""
    n = int(round(R / cell)) + 1
    g = np.arange(-n, n + 1) * cell
    gx, gy, gz = np.meshgrid(g, g, g, indexing="ij")
    inside = gx ** 2 + gy ** 2 + gz ** 2 <= (R + 1e-6) ** 2
    sh = np.zeros_like(inside)
    for ax in range(3):
        for dd in (-1, 1):
            sh |= ~np.roll(inside, dd, ax)
    out = []
    for x, y, z in zip(gx[inside & sh], gy[inside & sh], gz[inside & sh]):
        xn, yn, zn = x / R, y / R, z / R
        land = math.sin(3.1 * xn + 1.0) * math.sin(2.7 * yn + 2.0) + 0.7 * math.sin(3.9 * zn + 0.5) > 0.35
        c = (0.95, 0.97, 1.0) if abs(zn) > 0.82 else ((0.30, 0.70, 0.30) if land else (0.15, 0.40, 0.85))
        out.append((x, y, z, c))
    return out


GLOBE = globe_cells()
TILT0 = math.radians(23.4)


def globe_xf(i, tau):
    """(기울기 x, 기울기 y, 자전) — 13번 줄 흔들리기 시작, 14번 줄 일정, 15번 줄 달이 사라지면 마구 흔들림."""
    sp = 0.9 * tau
    if i == IX["far"]:
        w = ramp(tau, 0.4, 2.2)
        return TILT0 + 0.10 * w * math.sin(2 * math.pi * 0.9 * tau), 0.09 * w * math.sin(2 * math.pi * 0.7 * tau + 1.0), sp
    if i == IX["wobble"]:
        d = max(tau - VANISH[i], 0.0)
        w = ramp(d, 0.0, 0.5)
        return (TILT0 + w * 0.95 * math.sin(2 * math.pi * 0.85 * d + 0.8), w * 0.8 * math.sin(2 * math.pi * 1.25 * d + 1.0), sp)
    return TILT0, 0.0, sp


def rotm(tx, ty, sp):
    cx, sx, cy, sy, cz, sz = math.cos(tx), math.sin(tx), math.cos(ty), math.sin(ty), math.cos(sp), math.sin(sp)
    return (np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]) @ np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @
            np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]))


def props_study(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    L = IX
    ox, oy = OFF["study"]
    gx, gy, gz = GLOBE_AT[0] + ox, GLOBE_AT[1] + oy, GLOBE_AT[2]
    mxl = MOONBOX_AT[0] + ox + (0.06 * ramp(tau, 0.3, dur) if i == L["bar"] else 0.0)
    if i in (L["far"], L["anchor"], L["wobble"], L["bar"]):
        tx, ty, sp = globe_xf(i, tau)
        R = rotm(tx, ty, sp)
        for x, y, z, c in GLOBE:
            q = R @ np.array((x, y, z))
            F.c((gx + q[0], gy + q[1], gz + q[2]), (0.05, 0.05, 0.05), c)
        ax = R @ np.array((0.0, 0.0, 1.0))
        F.c((gx, gy, gz), (0.64, 0.016, 0.016), (0.85, 0.7, 0.3), rot_to(ax))          # 축 막대 (양쪽 극 밖으로 튀어나옴)
        F.c((gx, gy, DESK_Z + 0.02), (0.05, 0.05, 0.04), (0.4, 0.3, 0.2))              # 받침 위 짧은 기둥
    mk = moon_k(i, tau) if i in (L["anchor"], L["wobble"], L["bar"]) else 0.0
    if mk > 0.0:
        OR.orb((mxl, MOONBOX_AT[1] + oy, MOONBOX_AT[2]), 0.28 * mk, MOON_C)
        for dx, dz, r in ((-0.25, 0.2, 0.2), (0.22, -0.2, 0.16)):
            G.c((mxl + dx * 0.14, MOONBOX_AT[1] + oy - 0.138, MOONBOX_AT[2] + dz * 0.14), (0.01, 2 * r * 0.14, 2 * r * 0.14), MOON_CR)
        LT.append(((mxl, MOONBOX_AT[1] + oy - 0.6, MOONBOX_AT[2] + 0.3), "moon", 40.0))
    if i == L["anchor"] or (i == L["wobble"] and mk > 0.0):            # 달이 자전축을 잡는 닻줄 (점선)
        for n in range(8):
            G.c((gx + 0.27 + n * (mxl - gx - 0.5) / 7.0, gy - 0.12, gz), (0.03, 0.012, 0.012), (1.0, 1.8, 3.0))
    if i == L["wobble"] and tau > VANISH[i]:                           # 눈·꽃·단풍 아이콘이 마구 바뀜
        pat, col = SEASONS[int((tau - VANISH[i]) / 0.26) % 3]
        glyph(G, pat, gx - 0.09, gy - 0.5, gz + 0.5, 0.036, col)
    if i == L["bar"]:                                                  # 달 박스와 지구 사이 거리 막대가 조금 더 늘어남
        x0, x1 = gx + 0.27, mxl - 0.14
        z = gz - 0.3
        G.c(((x0 + x1) / 2, gy - 0.12, z), (x1 - x0, 0.014, 0.02), (3.4, 2.6, 0.5))
        for xx in (x0, x1):
            G.c((xx, gy - 0.12, z), (0.016, 0.016, 0.1), (3.4, 2.6, 0.5))
        for n in range(1, int((x1 - x0) / 0.1) + 1):
            G.c((x0 + 0.1 * n, gy - 0.12, z), (0.012, 0.012, 0.05), (1.6, 1.3, 0.3))
    if i == L["fossil"]:                                               # 줄무늬를 세는 손가락: 위에서 아래로 짚으며 하나씩 켬
        fx, fy = FOS_AT[0] + ox, FOS_AT[1] + oy
        kk = min(int(tau / 0.16), 14)
        for k in range(kk + 1):
            z0 = DESK_Z + 0.06 + 0.02 * (14 - k)
            G.c((fx, fy - 0.0385, z0 + 0.004), (0.30, 0.004, 0.009), (3.4, 2.6, 0.4))
        zk = DESK_Z + 0.064 + 0.02 * (14 - kk)
        tap = 0.012 * abs(math.sin(tau * 19.0))
        F.o((fx + 0.1, fy - 0.2 + tap, zk), (0.16, 0.028, 0.028), (0.93, 0.74, 0.58), (0.0, 0.0, math.pi / 2))
        F.c((fx + 0.1, fy - 0.28 + tap, zk - 0.02), (0.08, 0.1, 0.07), (0.93, 0.74, 0.58))
        F.c((fx + 0.1, fy - 0.5 + tap, zk - 0.1), (0.07, 0.34, 0.07), MJ_SH)
    if True:                                                           # 벽시계: 평소 24칸, 19번 줄에선 22칸에서 24칸으로 늘어남(새 눈금이 생기며 간격이 좁아짐)
        cx, cz, r = CLK_AT[0] + ox, CLK_AT[1], CLK_AT[2]
        yy = 2.5 + oy - 0.09
        n_e = 22.0 + 2.0 * ramp(u, 0.12, 0.85) if i == L["clock"] else 24.0
        for k in range(24):
            s = clamp(n_e - k)
            if s <= 0.01:
                continue
            th = 2 * math.pi * k / n_e
            d = np.array((math.sin(th), 0.0, math.cos(th)))
            big = 1.3 if k % 6 == 0 else 1.0
            F.c((cx + d[0] * 0.33 * r / 0.42, yy, cz + d[2] * 0.33 * r / 0.42), (0.07 * s * big, 0.012, 0.016 * s), (0.10, 0.10, 0.14), rot_to(d))
        for ang, ln, wd in ((math.radians(40 + 5 * tau), 0.19, 0.03), (math.radians(120 + 60 * tau), 0.29, 0.02)):
            d = np.array((math.sin(ang), 0.0, math.cos(ang)))
            F.c((cx + d[0] * ln / 2, yy - 0.006, cz + d[2] * ln / 2), (ln, 0.012, wd), (0.12, 0.12, 0.16), rot_to(d))


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 월드 좌표."""
    F, G, OR, BL, LT = Items(N_FX), Items(N_GL), Items(N_OR), Items(N_BL), []
    {"beach": props_beach, "meadow": props_meadow, "reef": props_reef, "study": props_study}[set_of(i)](
        i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·소품 점 배열, 카메라, 조명."""
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
        R.append((0.0, d["pitch"], math.radians(d["yaw"])))
        SC.append(d["scale"])
        PO.append(W["PI"][(d["pose"], c["hair"], c["extra"])])
    cam = cam_pose(i, u)
    F, G, OR, BL, LT = props(i, tau, dur, u, S, t, cam)
    return dict(i=i, tau=tau, u=u, set=cam["set"], cam=cam, A=S, P=P, R=R, CO=CO, C2=C2, SC=SC, PO=PO, F=F, G=G, OR=OR, BL=BL, LT=LT,
                env=env(i, tau))


# ───────────────────────── Blender 원형(프로토) ─────────────────────────
def _mat_glow(name, strength=1.0):
    """인스턴스 'col' 색으로 빛나는 재질 (달·알·눈금·궤적선·별 등). 색 값이 1보다 크면 더 밝게 번짐."""
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
    v = X.Vox(34)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.52, 0.58, 0.84), ambient_strength=0.22, ground=(0.1, 0.1, 0.14))
    sun = K.sun(ctx, 0.0, color=MOONC, name="ep34_sun")
    cam = K.CamRig(ctx, lens=24, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep34_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep34_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep34_fx", K.proto(ctx, "ep34_p_fx", cube(), [K.mat_inst("ep34_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep34_glow", K.proto(ctx, "ep34_p_glow", cube(), [_mat_glow("ep34_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep34_orb", K.proto(ctx, "ep34_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep34_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep34_bl", K.proto(ctx, "ep34_p_bl", K.bm_sphere(0.5, (0, 0, 0), 20, 10), [K.mat_inst("ep34_m_bl", 0.8)]),
                     N_BL, vector_scale=True)
    for ob in (gl, orb):                                              # 달·발광 상자가 달빛(해 조명)을 가리지 않게
        try:
            ob.visible_shadow = False
        except AttributeError:
            pass
    lm = K.point_light(ctx, (0, 0, -80), 0.0, (0.55, 0.72, 1.0), 0.4, "ep34_lt_moon")
    lw = K.point_light(ctx, (0, 0, -80), 0.0, (1.0, 0.82, 0.6), 0.3, "ep34_lt_warm")

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
        for ob, kind in ((lm, "moon"), (lw, "warm")):
            hit = [(p, w) for p, k, w in S["LT"] if k == kind]
            if hit:
                ob.location, ob.data.energy = hit[0][0], hit[0][1]
            else:
                ob.data.energy = 0.0

    ctx.on_frame(upd)
