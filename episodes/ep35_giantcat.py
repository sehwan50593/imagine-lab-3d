"""EP35 만약에 고양이가 사람만큼 커진다면? (정보형 v2: 블록 캐릭터·생활 장면·정보 카드·내레이션)

컷 흐름 (내레이션 한 줄 = 한 컷, 0.0초부터 움직임):
소파 위 사람 크기 고양이가 쩍 하품 + 문가에서 뒷걸음질 치는 지수(훅, 빠른 push) → 침대에서 눈 떠 거실로, 소파 위 거대 고양이("!")
→ 바닥 줄자 옆에서 46cm가 170cm로 쑥 커짐 → 체중계 숫자가 4에서 200으로 → 고양이가 폴짝 올라앉자 소파 다리가 꺾여 주저앉음(개그 1)
→ 침대를 통째로 차지하고 몸을 만 채 쿨쿨(Z) → 지수는 바닥에 요를 펴고 눕는다 → 1주 뒤 마트 사료 통로가 텅 빔('품절' 깃발)
→ 사료 포대를 오물오물 먹어 치움 → 빈 포대 탑이 쌓임 → 점프: 선반을 올려다봄 → 원래 크기 고양이가 선반으로 휙
→ 거대 고양이는 뛰지만 못 닿고 쿵(개그 2, 선반 책이 떨어짐) → 1년 뒤 높은 캣타워·낮은 가구 집에서 바닥에 앉음
→ 작은 고양이들이 캣타워에서 사뿐히 뛰어내려 착지 → 쓱 걸어감 → 반전: 근력 14 대 체중 50 막대 → 일어서려다 휘청, 폭삭 주저앉음
→ 다 큰 고양이는 주로 사람에게 야옹(말풍선) → 배고파·놀아 줘·옆에 있어 줘(말풍선 셋) → 지수가 꼭 안아 줌(노을빛·하트)
→ 고양이 얼굴 클로즈업(질문) → 다음 편 예고(창밖 도시가 흔들림).
근거(설명란):
① 2~3번 줄 · 집고양이는 머리~몸통 평균 약 46cm, 몸무게 보통 4~5kg(4kg 기준). 키를 3.7배(46→170cm)로 키우면 부피·몸무게는
   3.7×3.7×3.7 = 50.65 ≈ 50배 → 4kg × 50 ≈ 200kg (모양과 밀도가 같다는 가정의 계산값) · 위키백과 'Cat', J.B.S. Haldane 「On Being the Right Size」(1926)
② 5~6번 줄 · 고양이는 하루 12~16시간(평균 13~14시간) 잔다 · 위키백과 'Cat', UF Health
③ 8~9번 줄 · 안정시 에너지 RER = 70 × 체중^0.75, 성묘 유지 ×1.2 → 4kg: 70×4^0.75 = 198 → ×1.2 ≈ 238 ≈ 약 240kcal,
   200kg: 70×200^0.75 = 3,723 → ×1.2 ≈ 4,467 ≈ 약 4,500kcal → 4,467÷238 ≈ 19배 (계산값) · AAFP 2022 급여 지침(RER 공식), PetMD 예시
④ 11~12번 줄 · 점프 높이는 몸집에 비례하지 않고 거의 무관하다: 벼룩은 약 60cm(2피트), 사람은 약 1.5m(5피트) · Haldane 1926 (Harper's 1926.3)
⑤ 14~15번 줄 · 고층에서 떨어져 병원에 온 고양이 132마리 중 약 90%가 살았다(병원에 온 고양이만 센 값이라 실제 생존율은 더 낮을 수 있음)
   · Whitney·Mehlhaff, JAVMA 191:1399 (1987)
⑥ 16~17번 줄 · 근력은 단면적(3.7×3.7 = 13.69 ≈ 14배), 몸무게는 부피(3.7³ ≈ 50배)에 비례 → 체중당 근력은 약 1/3.7 (계산값) · Haldane 1926
⑦ 18~19번 줄 · 다 자란 고양이는 고양이끼리는 거의 야옹하지 않고, 야옹은 주로 사람을 향한 소리다
   · 노르웨이 생명과학대(NMBU) Bjarne Braastad, ScienceNorway 2019-10-17
(22번 줄은 다음 편 예고이고, 나머지 장면·'나비'와 '지수'는 지어낸 이야기입니다.)
특수효과: 고양이 = 31편의 상자 원형(서기·걷기·웅크림·엎드림·몸 말기)을 가져와 이 파일 안에서 17종으로 늘림(앉기·하품 두 단계·야옹·웃는 눈·올려다봄·점프·먹기 둘).
같은 원형의 배율만 0.843(머리~몸통 46cm)·3.12(170cm = 3.7배)로 바꿔 작은/거대 고양이를 만들고, 줄자 줄에선 배율이 easeOutBack으로 쑥 커짐.
하품 = 윗머리를 뒤로 젖히고 아래턱 상자를 내려 입속(빨강)·혀·송곳니가 보이게 한 원형. 소파 = 동적 상자 9개(다리 넷이 양옆으로 벌어지며 짧아지고 몸통·방석이 내려앉음)
+ 먼지 덩이·나뭇조각. 체중계·줄자 숫자 = 7-세그먼트 발광 상자, 막대 = 눈금 하나 3cm(14칸·50칸)로 자라는 상자. 점프 = 중력 9.8 포물선(leap_path) + 몸 기울기,
쿵 = 카메라 목표점 흔들림 + 발밑 먼지 + 선반 책 낙하. 사료 포대 = 납작해지다 탑 위로 휙 날아가 쌓이는 상자. 말풍선·'품절' 깃발·막대 이름표 = Noto Sans KR(OFL)을
16x16으로 줄인 비트맵(GLYPH, 27~33편과 같은 방식)과 도트 그림. 창밖 도시 = 유리 앞에 세운 건물 상자들이 우르르 떨림(카메라 흔들림과 함께).
"""
import json
import math
from pathlib import Path

import numpy as np

from engine import voxel as X
from engine.common import clamp, lerp, ramp

STYLE = "pixe"
TITLE_FAST = True
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.15, 0.3, 1.6)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"liv": (0, 0), "bed": (300, 0), "mart": (600, 0), "year": (900, 0), "year2": (1200, 0)}
NAMES = ("hook", "wake", "ruler", "scale", "sofa", "nap", "futon", "mart", "eat", "tower", "look", "jump_s", "jump_g", "year",
         "fall_a", "fall_b", "bars", "stand", "meow", "wants", "hug", "face", "quake")
LN = {n: k for k, n in enumerate(NAMES)}

S_J = 0.92                 # 지수 키 약 1.7m (블록 사람 1.0 = 1.85m)
S_S = 0.46 / 0.5455        # 원래 크기 고양이: 머리~몸통(코끝~엉덩이) 모델 0.5455m x 0.843 = 46cm
S_G = S_S * 3.7            # 거대 고양이: 3.7배 = 약 170cm

# say: 내레이션 / cap: 아래 자막(아라비아 숫자) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 끝 목표점[, ("follow", 고양이 번호, 높이)]]])
# cuts: 한 줄 안의 짧은 연속 컷 [(끝 u, shot), ...]   shift: 렌즈 세로 이동(센서 높이 비율, +면 화면 속 물체가 아래로)
LINES = [
    dict(say="고양이가 사람만 해지면 몸무게가 이백 킬로그램이에요", cap="사람만 한 고양이는 약 200kg", gap=0.4,
         shot=("liv", (-2.3, 2.3, 1.45), -90, 3, 4.4, 28, 0.66, 3, 0.09, (-1.8, 2.3, 1.45))),
    dict(say="눈을 떠 보니 고양이가 사람만 해졌어요", cap="눈 떠 보니 고양이가 사람만 해졌어요", gap=0.4,
         shot=("bed", (0.0, 2.0, 0.95), -62, 12, 4.4, 28, 0.9, 5),
         cuts=[(0.45, ("bed", (0.0, 2.0, 0.95), -62, 12, 4.4, 28, 0.9, 5)),
               (1.0, ("liv", (-1.95, 2.5, 1.45), -90, 3, 4.6, 28, 0.9, 3, 0.07))]),
    dict(say="키가 삼 점 칠 배가 되면", cap="키가 3.7배가 되면", gap=0.4,
         shot=("liv", (1.25, 1.2, 0.6), -90, 14, 6.4, 28, 0.94, 0, 0.08)),
    dict(say="몸무게는 오십 배가 돼요", cap="몸무게는 50배가 돼요", gap=0.5,
         shot=("liv", (1.35, 1.4, 1.0), -80, 10, 6.0, 28, 0.94, 4, 0.06)),
    dict(say="소파는 한 번에 주저앉았죠", cap="소파는 한 번에 주저앉았죠", gap=0.5,
         shot=("liv", (-1.3, 1.7, 0.75), -75, 16, 5.4, 28, 0.92, 4, 0.12)),
    dict(say="고양이는 하루 열두 시간 넘게 자요", cap="고양이는 하루 12시간 넘게 자요", gap=0.4,
         shot=("bed", (0.0, 1.75, 0.5), -85, 30, 4.8, 28, 0.9, 4, 0.10)),
    dict(say="침대는 이제 고양이 차지예요", cap="침대는 이제 고양이 차지예요", gap=0.5,
         shot=("bed", (1.0, 1.4, 0.45), -78, 24, 5.4, 28, 0.9, 3, 0.06)),
    dict(say="일 주일 뒤, 마트 사료 코너가 텅 비었어요", cap="1주 뒤, 사료 코너가 텅 비었어요", gap=0.5,
         shot=("mart", (0.0, 3.2, 1.0), -90, 7, 5.8, 24, 0.9, 0)),
    dict(say="하루 필요 열량은 사천오백 킬로칼로리예요", cap="하루 필요 열량 약 4,500kcal", gap=0.4,
         shot=("liv", (0.0, 1.5, 0.75), -55, 12, 5.6, 28, 0.92, 4, 0.05)),
    dict(say="원래보다 열아홉 배를 먹어야 해요", cap="원래보다 약 19배를 먹어야 해요", gap=0.5,
         shot=("liv", (-0.1, 1.3, 0.7), -60, 8, 4.4, 28, 0.9, -3, 0.05)),
    dict(say="그런데 점프는 어떨까요?", cap="그런데 점프는 어떨까요?", gap=0.5,
         shot=("liv", (2.75, 1.2, 1.05), -150, 8, 5.5, 24, 0.92, 4, 0.04)),
    dict(say="벼룩은 육십 센티, 사람은 일 미터 반을 뛰어요", cap="벼룩 60cm, 사람 1.5m 뛰어요", gap=0.4,
         shot=("liv", (2.8, 1.4, 0.5), -150, 6, 4.3, 28, 0.92, 3, 0.04, (2.8, 1.4, 0.5), ("follow", 1, 0.3))),
    dict(say="몸집이 커도 점프 높이는 비슷해요", cap="몸집이 커도 점프 높이는 비슷해요", gap=0.5,
         shot=("liv", (2.8, 1.4, 0.95), -150, 6, 5.4, 28, 0.95, 2, 0.04)),
    dict(say="일 년 뒤, 높은 곳은 포기했어요", cap="1년 뒤, 높은 곳은 포기했어요", gap=0.5,
         shot=("year", (2.2, 1.7, 0.85), -90, 6, 4.9, 28, 0.94, 2, 0.06)),
    dict(say="떨어져 병원에 온 고양이 백서른두 마리 중", cap="떨어져 병원 온 고양이 132마리 중", gap=0.4,
         shot=("year", (2.3, 1.7, 0.8), -92, 7, 4.9, 28, 0.94, 2, 0.05)),
    dict(say="약 구십 퍼센트가 살아남았어요", cap="약 90%가 살아남았어요", gap=0.5,
         shot=("year", (1.95, 0.95, 0.3), -90, 8, 4.0, 28, 0.96, 0, 0.05)),
    dict(say="그런데 몸이 커지면 오히려 약해져요", cap="그런데 커질수록 오히려 약해져요", gap=0.4,
         shot=("year", (-1.7, 0.9, 0.85), -88, 5, 5.4, 28, 0.94, 0, 0.05)),
    dict(say="근력은 열네 배, 몸무게는 오십 배라서요", cap="근력은 14배, 몸무게는 50배라서요", gap=0.5,
         shot=("year", (0.6, 1.1, 0.7), -88, 8, 5.7, 28, 0.92, 0, 0.05)),
    dict(say="다 자란 고양이는 주로 사람에게 야옹해요", cap="다 큰 고양이는 주로 사람에게 야옹", gap=0.4,
         shot=("year", (-1.6, 1.9, 1.0), -90, 5, 5.9, 28, 0.94, 0, 0.05)),
    dict(say="배고파, 놀아 줘, 옆에 있어 줘", cap="배고파, 놀아 줘, 옆에 있어 줘", gap=0.5,
         shot=("year", (-0.8, 1.6, 1.2), -90, 4, 3.9, 28, 0.93, 0, 0.05)),
    dict(say="지수는 거대한 고양이를 꼭 안아 줬어요", cap="지수는 거대한 고양이를 꼭 안았어요", gap=0.6,
         shot=("year2", (-0.85, 1.7, 1.15), -90, 6, 4.6, 28, 0.92, 0, 0.05)),
    dict(say="당신의 고양이는 오늘 뭐라고 했나요?", cap="당신의 고양이는 오늘 뭐라고 했나요?", gap=0.5,
         shot=("year2", (-0.8, 1.55, 1.1), 180, 3, 2.1, 30, 0.95, 0)),
    dict(say="내일 낮 열두 시, 서울에 규모 칠 지진이 온다면?", cap="서울에 규모 7 지진이 온다면?",
         shot=("year", (-0.4, 2.8, 1.55), -90, 3, 4.6, 26, 0.96, 0, 0.03)),
]
assert len(LINES) == len(NAMES)
for _ln in LINES:
    assert len(_ln["cap"]) <= 20, (_ln["cap"], len(_ln["cap"]))
TITLE = [("만약에", "white"), ("고양이가", "white"), ("사람만큼 커진다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = 16                  # '그런데 몸이 커지면 오히려 약해져요' 줄 (반전 사실)
CLOCK = [(1, "경과", "바로"), (7, "경과", "1주 뒤"), (13, "경과", "1년 뒤"), (16, "경과", "지금"), (18, None)]
CARDS = [
    dict(lines=(2, 3), big="4kg → 약 200kg", small="키 3.7배 → 부피 약 50배(46→170cm, 계산값)", color="yellow", src="Haldane 1926"),
    dict(lines=(5, 6), big="12~16시간", small="고양이가 하루에 자는 시간", color="cyan", src="위키백과 · UF Health"),
    dict(lines=(8, 9), big="약 4,500kcal", small="하루 필요 열량, 원래(약 240)의 약 19배(계산값)", color="orange", src="AAFP 2022 에너지 공식"),
    dict(lines=(11, 12), big="60cm vs 1.5m", small="벼룩과 사람의 점프 · 몸집이 커도 높이는 비슷", color="yellow", src="Haldane 1926"),
    dict(lines=(14, 15), big="약 90% 생존", small="고층에서 떨어져 병원에 온 고양이 132마리 중", color="green", src="JAVMA 1987"),
    dict(lines=(16, 17), big="근력 14 : 체중 50", small="근력은 단면적, 체중은 부피에 비례(계산값)", color="red", src="Haldane 1926"),
    dict(lines=(18, 19), big="야옹은 사람용", small="다 큰 고양이끼리는 거의 안 해요", color="pink", src="NMBU · ScienceNorway 2019"),
    dict(lines=(22, 22), big="다음 편", small="내일 낮 12시 · 서울에 규모 7 지진이 온다면?", color="cyan", src="구독하면 놓치지 않아요"),
]

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep35_giantcat" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 66.0, "lines": [[0.15 + 2.8 * i, 2.8 * i + 2.9, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep35", "title": "만약에 고양이가 사람만큼 커진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"style": "funny", "key": "G", "mode": "major", "bpm": 108, "seed": 351, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

JI_SH, JI_PA = (0.95, 0.55, 0.25), (0.20, 0.20, 0.22)         # 지수: 주황 셔츠·긴 머리·짙은 회색 바지
EX_SH = [(0.25, 0.45, 0.80), (0.85, 0.30, 0.28), (0.35, 0.65, 0.40), (0.92, 0.92, 0.90), (0.55, 0.38, 0.70), (0.30, 0.30, 0.34),
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
    """[(시작, 끝, 글)] — 첫 줄은 가운데 제목으로 보여 주므로 아래 자막에서 뺌. 자막은 cap(아라비아 숫자·단위)을 씀."""
    return [(s, e, LINES[k].get("cap", txt)) for k, (s, e, txt) in enumerate(TIMELINE["lines"]) if k > 0]


def title_span():
    s, e, _ = TIMELINE["lines"][0]
    return s, e


def simulate(build_dir):
    return {"dur": np.float32(DUR)}


# ───────────────────────── 하늘 · 빛 ─────────────────────────
DUSK = (LN["hug"], LN["face"])                    # 따뜻한 저녁 거실


def sky(t):
    if line_at(t) in DUSK:
        return (0.20, 0.17, 0.42), (0.98, 0.58, 0.38), 0.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


DAY = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})


def env(i, tl, du):
    """줄별 햇빛·주변광 (조명 세기는 세트에 고정). 안아 주는 두 줄은 노을 거실(year2): 낮은 주황 해 + 보랏빛 주변광."""
    if i in DUSK:
        return dict(DAY, sun=2.4, sun_col=(1.0, 0.66, 0.42), sun_rot=(78, 0, 30), amb=0.24, amb_col=(0.58, 0.48, 0.68))
    return DAY


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def _shake_spec(i):
    """줄 i의 흔들림 [(시작 τ, 길이, 세기 m, 진동수 Hz)] — 목표점을 흔들어 쿵·우르르를 줌."""
    if i == LN["sofa"]:
        return [(T_LAND, 0.9, 0.035, 14.0)]
    if i == LN["jump_g"]:
        return [(T_THUD, 0.8, 0.045, 13.0)]
    if i == LN["stand"]:
        return [(2.5, 0.6, 0.02, 12.0)]
    if i == LN["quake"]:
        return [(0.4, 4.2, 0.010, 11.0)]
    return ()


def shake(i, tl):
    out = [0.0, 0.0, 0.0]
    for t0, dur, amp, hz in _shake_spec(i):
        if i == LN["quake"]:
            k = ramp(tl, t0, t0 + 2.0)                    # 서서히 커지는 흔들림
        else:
            k = (1 - clamp((tl - t0) / dur)) ** 2 if tl >= t0 else 0.0
        if k <= 0.0:
            continue
        w = 2 * math.pi * hz
        out[0] += amp * k * math.sin(w * tl + 1.3)
        out[1] += 0.5 * amp * k * math.sin(w * 0.83 * tl + 0.4)
        out[2] += amp * k * math.sin(w * 1.21 * tl + 2.1)
    return out


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


def cam_pose(i, tl, u):
    """컷 진행도에서 카메라: dict(set, tgt, az, el, dist, lens, loc, shift) — 월드 좌표. CamRig.set과 같은 규칙."""
    shot, ul = cut_at(i, u)
    st, tg, az, el, dist, lens, push, daz = shot[:8]
    sh = shot[8] if len(shot) > 8 else 0.0
    tg2 = shot[9] if len(shot) > 9 else tg
    o = OFF[st]
    dx, dy, dz = shake(i, tl)
    e_ = ramp(ul, 0.0, 1.0)
    tgt = (lerp(tg[0], tg2[0], e_) + o[0] + dx, lerp(tg[1], tg2[1], e_) + o[1] + dy, lerp(tg[2], tg2[2], e_) + dz)
    if len(shot) > 10:                                    # 따라가는 카메라: 고양이를 살짝 늦게 쫓아감
        a_, b_ = shot_span(i)
        c = cats(i, max(tl - 0.18, 0.0), max(b_ - a_, 1e-3))[shot[10][1]]
        if c is not None:
            tgt = (c["x"] + o[0] + dx, c["y"] + o[1] + dy, c["z"] + shot[10][2] + dz)
    a, e, dd = az + daz * ul, math.radians(el), dist * (1 + (push - 1) * ul)
    loc = (tgt[0] + math.cos(e) * math.cos(math.radians(a)) * dd, tgt[1] + math.cos(e) * math.sin(math.radians(a)) * dd,
           tgt[2] + math.sin(e) * dd)
    return dict(set=st, tgt=tgt, az=a, el=el, dist=dd, lens=lens, loc=loc, shift=sh)


def cam_axes(az, el):
    """카메라의 오른쪽·위쪽 단위벡터."""
    a, e = math.radians(az), math.radians(el)
    return (-math.sin(a), math.cos(a), 0.0), (-math.cos(a) * math.sin(e), -math.sin(a) * math.sin(e), math.cos(e))


# ───────────────────────── 캐릭터 자세 (표준 자세 위에 팔·고개·입·눈만 바꾼 원형) ─────────────────────────
SITS = ("sit", "sit_phone", "sit_conf")
# base = 바탕 자세, arms = ((오른팔 앞뒤, 옆), (왼팔 앞뒤, 옆)) 어깨 회전각(앞뒤: 음수 = 앞으로 듦, 옆: 오른팔은 +가 몸 쪽·왼팔은 +가 바깥),
# mouth = open/smile, head = 고개 숙임(+)/젖힘(−), hroll = 고개 기울임, lie = 눈 뜨고 누움
KINDS = {
    "lieopen": dict(base="stand", lie=True),
    "shock_a": dict(base="walk_a", arms=((-2.05, 0.30), (-2.05, -0.30)), mouth="open", head=-0.10),
    "shock_b": dict(base="walk_b", arms=((-2.05, 0.30), (-2.05, -0.30)), mouth="open", head=-0.10),
    "gasp": dict(base="stand", arms=((-2.2, 0.35), (-2.2, -0.35)), mouth="open", head=-0.08),
    "smile": dict(base="stand", mouth="smile"),
    "sit_smile": dict(base="sit", mouth="smile"),
    "sit_wow": dict(base="sit", mouth="open", hroll=0.06),
    "carry": dict(base="stand", arms=((-1.3, 0.0), (-1.3, 0.0)), mouth="smile"),
    "carry_a": dict(base="walk_a", arms=((-1.3, 0.0), (-1.3, 0.0)), mouth="smile"),
    "carry_b": dict(base="walk_b", arms=((-1.3, 0.0), (-1.3, 0.0)), mouth="smile"),
    "hug": dict(base="stand", arms=((-1.45, 0.50), (-1.45, -0.50)), mouth="smile", head=0.10, hroll=0.10),
}
KIND_ORDER = list(KINDS)


def pose_index(name, hair):
    """인스턴스 'pose' 번호: 표준 22개(머리종류*11+자세) 뒤에 새 자세들(머리종류*새자세수+번호)."""
    if name in KINDS:
        return 2 * X.NPOSE + hair * len(KINDS) + KIND_ORDER.index(name)
    return hair * X.NPOSE + X.POSES[name]


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


def _rot_z(bm, ang, pivot):
    """pivot=(x, y)를 지나는 세로축 둘레 회전."""
    c, s = math.cos(ang), math.sin(ang)
    for p in bm.verts:
        x, y = p.co.x - pivot[0], p.co.y - pivot[1]
        p.co.x, p.co.y = pivot[0] + c * x - s * y, pivot[1] + s * x + c * y
    return bm


def _variant(kind, lh):
    """voxel._person으로 만든 바탕 자세에서 팔·고개·입만 바꾼 [(bmesh, 재질)]."""
    from engine import bkit as K
    sp = KINDS[kind]
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
                       (cube(0.232, 0.075, hz + 0.055, 0.02, 0.03, 0.04), 6)]}
    if sp.get("mouth"):
        swap(lambda bm, mi: mi == 6, mouth[sp["mouth"]])

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
    if sp.get("lie"):                                              # 선 모습을 뒤로 눕힘: 발끝이 원점, 머리는 -x, 얼굴은 위 (눈은 뜬 채)
        for bm, _ in out:
            X._rot_y(bm, -math.pi / 2, (0, 0, 0))
            X._shift(bm, dz=0.24)
    return out


# ───────────────────────── 고양이 (이 파일 안에서 상자로 만든 주황 줄무늬, 31편 원형을 가져와 늘림) ─────────────────────────
# 재질 번호: 0 털 · 1 줄무늬 · 2 크림(주둥이·발·배) · 3 분홍(코·속귀·혀) · 4 홍채(살짝 빛남) · 5 검정 · 6 흰색(하이라이트·수염·송곳니) · 7 입속(진한 빨강)
CAT_COLS = [(0.93, 0.52, 0.16), (0.62, 0.28, 0.07), (0.98, 0.93, 0.82), (0.96, 0.62, 0.66), (0.86, 0.88, 0.16),
            (0.015, 0.015, 0.02), (0.97, 0.97, 0.97), (0.55, 0.08, 0.14)]
# 원점 = 엉덩이 바닥, 앞 = +x. (모델 크기 = 머리~몸통 0.525m → 배율 0.876이면 46cm, 3.24면 170cm)
CAT_ORDER = ["stand", "walk_a", "walk_b", "crouch", "lie0o", "lie0c", "rb5", "sit", "sit_y1", "sit_y2", "sit_meow", "sit_happy",
             "sit_up", "sit_blink", "leap", "eat_a", "eat_b"]
CAT_IX = {n: k for k, n in enumerate(CAT_ORDER)}
RING_R = 0.21          # 말았을 때 몸 가운데선 반지름
SPINE = 0.40           # 몸통 길이
BEND_FULL = 1.0        # 다 말았을 때 휨(31편 rb5)


def _cat_head(K, eyes="open", gape=0.0, blush=False):
    """머리 [(bmesh, 재질)] (머리 기준 좌표: 뒤쪽 면 x=0, 앞 x=0.11, 바닥 z=0).
    eyes = open(홍채·동공) / closed(가는 선) / happy(웃는 눈 ^^) / squeeze(꾹 감음). gape>0이면 윗머리가 젖혀지고 아래턱이 내려가 입이 벌어짐."""
    U, Rr, Lw = [], [], []             # 윗머리(젖혀짐) · 제자리 · 아래턱(내려감)

    def b(lst, cx, cy, z0, sx, sy, sz, mi):
        lst.append((K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True), mi))
    g = gape > 0
    zb = 0.040 if g else 0.0
    b(U, 0.055, 0, zb, 0.11, 0.13, 0.11 - zb, 0)                      # 머리통
    for sy in (-0.043, 0.043):                                         # 귀 + 속귀 (머리 옆면과 같은 평면이 되지 않게 안쪽으로)
        b(U, 0.03, sy, 0.107, 0.03, 0.04, 0.045, 0)
        b(U, 0.0455, sy, 0.114, 0.004, 0.026, 0.03, 3)
    for y in (-0.03, 0.0, 0.03):                                       # 이마 줄무늬
        b(U, 0.05, y, 0.108, 0.06, 0.012, 0.005, 1)
    if g:
        b(U, 0.1175, 0, zb + 0.004, 0.014, 0.036, 0.020, 2)           # 윗입술(크림)
        b(U, 0.1275, 0, zb + 0.016, 0.006, 0.02, 0.012, 3)            # 코
        for sy in (-0.020, 0.020):                                     # 윗 송곳니
            b(U, 0.1085, sy, zb - 0.014, 0.012, 0.010, 0.016, 6)
        for dz in (0.012, 0.020, 0.028):                               # 수염
            for sg in (-1, 1):
                b(U, 0.1255, sg * 0.075, zb + dz, 0.003, 0.09, 0.003, 6)
    else:
        b(U, 0.1175, 0, 0.003, 0.014, 0.065, 0.037, 2)                # 주둥이 · 코 · 입
        b(U, 0.1275, 0, 0.034, 0.006, 0.02, 0.012, 3)
        b(U, 0.1255, 0, 0.012, 0.002, 0.03, 0.004, 5)
        for dz in (0.012, 0.020, 0.028):
            for sg in (-1, 1):
                b(U, 0.1255, sg * 0.075, dz, 0.003, 0.09, 0.003, 6)
    ze = 0.075 if g else 0.063
    for sy in (-0.036, 0.036):
        if eyes == "open":
            for dy, w, h in ((0.0, 0.032, 0.042), (-0.0185, 0.005, 0.032), (0.0185, 0.005, 0.032)):   # 테두리: 십자를 겹치지 않는 3조각으로
                b(U, 0.1104, sy + dy, ze - h / 2, 0.0016, w, h, 5)
            for dy, w, h in ((0.0, 0.026, 0.036), (-0.0155, 0.005, 0.026), (0.0155, 0.005, 0.026)):   # 홍채
                b(U, 0.1126, sy + dy, ze - h / 2, 0.0028, w, h, 4)
            b(U, 0.1147, sy, ze - 0.016, 0.0016, 0.010, 0.032, 5)    # 동공
            b(U, 0.1161, sy + 0.007, ze + 0.006, 0.0014, 0.008, 0.008, 6)   # 하이라이트
        elif eyes == "happy":                                          # ^ ^ : 가운데가 높은 세 칸
            for dy, dz in ((-0.011, 0.0), (0.0, 0.007), (0.011, 0.0)):
                b(U, 0.1105, sy + dy, ze - 0.012 + dz, 0.002, 0.012, 0.007, 5)
        else:                                                          # 가는 선 (squeeze는 더 굵게)
            b(U, 0.1105, sy, ze - 0.004, 0.002, 0.036, 0.009 if eyes == "squeeze" else 0.005, 5)
    if blush:                                                          # 볼 홍조
        for sy in (-0.053, 0.053):
            b(U, 0.1108, sy, ze - 0.040, 0.002, 0.022, 0.014, 3)
    if g:
        b(Rr, 0.022, 0, 0.0, 0.012, 0.11, 0.075, 7)                   # 목구멍 벽
        for sy in (-0.0575, 0.0575):                                   # 입꼬리 쪽 뺨 판
            b(Rr, 0.032, sy, 0.0, 0.046, 0.015, 0.078, 0)
        b(Lw, 0.056, 0, 0.0, 0.10, 0.098, 0.026, 0)                   # 아래턱
        b(Lw, 0.056, 0, 0.0265, 0.094, 0.088, 0.003, 7)               # 입속 바닥
        b(Lw, 0.07, 0, 0.0295, 0.05, 0.036, 0.009, 3)                 # 혀
        b(Lw, 0.1, 0, 0.0, 0.012, 0.05, 0.020, 2)                     # 턱끝
        for sy in (-0.020, 0.020):                                     # 아래 송곳니
            b(Lw, 0.1, sy, 0.0265, 0.010, 0.010, 0.012, 6)
        for bm, _ in U:
            X._rot_y(bm, -0.55 * gape, (0.0135, 0, zb))
        for bm, _ in Lw:
            X._rot_y(bm, 0.80 * gape, (0.0135, 0, 0.026))
    return U + Rr + Lw


def _cat_place(parts, ox, oy, oz, yaw=0.0):
    for bm, _ in parts:
        if yaw:
            _rot_z(bm, yaw, (0.0, 0.0))
        X._shift(bm, ox, oy, oz)
    return parts


def _cat_upright(K, name, neck_pitch=0.0, gape=0.0):
    """서기·걷기·웅크림: 곧은 몸통 + 다리 4 + 목·머리 + 위로 말린 꼬리 (31편 원형). neck_pitch>0이면 목·머리를 앞으로 숙임(먹기)."""
    P = []
    low = name == "crouch"
    z = 0.045 if low else 0.11            # 몸통 바닥
    phase = {"walk_a": 1, "walk_b": -1}.get(name, 0)

    def b(cx, cy, z0, sx, sy, sz, mi):
        P.append((K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True), mi))
    b(0.20, 0, z, 0.40, 0.15, 0.14, 0)
    b(0.20, 0, z - 0.005, 0.30, 0.09, 0.02, 2)
    b(0.396, 0, z + 0.01, 0.014, 0.08, 0.10, 2)
    for k in range(5):
        b(0.045 + 0.075 * k, 0, z + 0.003, 0.028, 0.158, 0.14, 1)
    if low:                                                           # 웅크림: 앞발은 앞으로 쭉, 뒷다리는 접어 엉덩이 옆
        for sy in (-0.05, 0.05):
            b(0.40, sy, 0.0, 0.15, 0.05, 0.045, 0)
            b(0.49, sy, 0.0, 0.05, 0.056, 0.035, 2)
            b(0.07, sy * 1.2, 0.0, 0.12, 0.07, 0.10, 0)
    else:
        sw = 0.45 * phase
        for lx, ly, sg in ((0.355, -0.048, 1), (0.355, 0.048, -1), (0.07, -0.052, -1), (0.07, 0.052, 1)):
            front = lx > 0.2
            leg = K.bm_cube(0.055 if front else 0.085, 0.05 if front else 0.06, (0.12 if front else 0.13) - 0.035, (lx, ly, 0.035),
                            bottom=True)
            paw = K.bm_cube(0.065, 0.056, 0.037, (lx + 0.003, ly, 0.0), bottom=True)
            for bm in (leg, paw):
                if sw:
                    X._rot_y(bm, sg * sw, (lx, 0, 0.12))
            P += [(leg, 0), (paw, 2)]
    neck = K.bm_cube(0.09, 0.10, 0.15, (0.385, 0, z + 0.08), bottom=True)   # 목 + 머리
    head = _cat_place(_cat_head(K, "open", gape), 0.415, 0.0, z + 0.145)
    if neck_pitch:
        for bm in [neck] + [h[0] for h in head]:
            X._rot_y(bm, neck_pitch, (0.37, 0.0, z + 0.09))
    P += [(neck, 0)] + head
    for k in range(9):                                                # 꼬리: 뒤로 뻗다 위로
        w = 0.048 - 0.002 * k
        zz = (0.06 if low else 0.17) + (0.014 if low else 0.038) * k
        b(-0.03 - 0.028 * k, 0, zz - 0.025, 0.05, w, 0.05, 1 if (k % 2 or k == 8) else 0)
    return P


def _cat_eat(K, name):
    """먹기: 선 자세에서 목·머리만 앞으로 푹 숙임 (eat_a 깊이, eat_b 살짝 들고 입을 벌림 = 오물오물)."""
    return _cat_upright(K, "stand", 1.05, 0.0) if name == "eat_a" else _cat_upright(K, "stand", 0.78, 0.55)


def _cat_leap(K):
    """점프 공중 자세: 앞다리는 앞으로 쭉, 뒷다리는 뒤로 쭉, 꼬리는 곧게 뒤로 (몸 기울기는 인스턴스 회전으로)."""
    P = []
    z = 0.11

    def b(cx, cy, z0, sx, sy, sz, mi):
        P.append((K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True), mi))
    b(0.20, 0, z, 0.40, 0.15, 0.14, 0)
    b(0.20, 0, z - 0.005, 0.30, 0.09, 0.02, 2)
    b(0.396, 0, z + 0.01, 0.014, 0.08, 0.10, 2)
    for k in range(5):
        b(0.045 + 0.075 * k, 0, z + 0.003, 0.028, 0.158, 0.14, 1)
    for ly in (-0.048, 0.048):                                        # 앞다리: 어깨에서 앞으로
        leg = K.bm_cube(0.05, 0.05, 0.15, (0.34, ly, 0.0), bottom=True)
        paw = K.bm_cube(0.056, 0.056, 0.035, (0.34, ly, -0.035), bottom=True)
        for bm in (leg, paw):
            X._rot_y(bm, -1.35, (0.34, 0, 0.19))
        P += [(leg, 0), (paw, 2)]
    for ly in (-0.052, 0.052):                                        # 뒷다리: 엉덩이에서 뒤로
        leg = K.bm_cube(0.07, 0.056, 0.17, (0.07, ly, 0.0), bottom=True)
        paw = K.bm_cube(0.07, 0.056, 0.035, (0.07, ly, -0.035), bottom=True)
        for bm in (leg, paw):
            X._rot_y(bm, 1.25, (0.07, 0, 0.19))
        P += [(leg, 0), (paw, 2)]
    b(0.385, 0, z + 0.08, 0.09, 0.10, 0.15, 0)                        # 목
    P += _cat_place(_cat_head(K, "open"), 0.415, 0.0, z + 0.145)
    for k in range(9):                                                # 꼬리: 곧게 뒤로
        w = 0.048 - 0.002 * k
        b(-0.03 - 0.03 * k, 0, z + 0.07 + 0.004 * k, 0.05, w, 0.05, 1 if (k % 2 or k == 8) else 0)
    return P


def _cat_sit(K, eyes="open", gape=0.0, blush=False, look=0.0):
    """앉은 고양이(두 앞발 곧게, 엉덩이는 바닥, 꼬리는 옆으로 휘감음). 높이 약 0.4m(머리 꼭대기)."""
    P = []

    def b(cx, cy, z0, sx, sy, sz, mi):
        P.append((K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True), mi))
    for sy in (-0.062, 0.062):                                        # 엉덩이(허벅지) + 줄무늬
        b(-0.03, sy, 0.0, 0.21, 0.09, 0.14, 0)
        for sx in (-0.075, -0.01):
            b(sx, sy, 0.0, 0.026, 0.098, 0.147, 1)
    b(-0.085, 0, 0.0, 0.07, 0.115, 0.12, 0)
    pv = (0.02, 0.0, 0.07)                                            # 윗몸: 앞으로 살짝 기울어 선 상자
    for bm in (K.bm_cube(0.12, 0.14, 0.21, (0.02, 0, 0.07), bottom=True), ):
        P.append((X._rot_y(bm, 0.22, pv), 0))
    for z0 in (0.12, 0.17, 0.22):                                     # 윗몸 줄무늬
        bm = K.bm_cube(0.125, 0.148, 0.026, (0.02, 0, z0), bottom=True)
        P.append((X._rot_y(bm, 0.22, pv), 1))
    bm = K.bm_cube(0.012, 0.085, 0.16, (0.083, 0, 0.09), bottom=True)  # 가슴 크림
    P.append((X._rot_y(bm, 0.22, pv), 2))
    for sy in (-0.045, 0.045):                                        # 앞다리 + 발
        b(0.10, sy, 0.0, 0.05, 0.05, 0.25, 0)
        b(0.108, sy, 0.0, 0.07, 0.056, 0.034, 2)
    b(0.07, 0, 0.20, 0.08, 0.10, 0.10, 0)                             # 목
    head = _cat_head(K, eyes, gape, blush)
    hx, hz = 0.07, 0.255
    pitch = look - (0.38 if gape > 0.7 else 0.12 * gape)
    for bm, _ in head:
        X._shift(bm, hx, 0, hz)
        if pitch:
            X._rot_y(bm, pitch, (hx + 0.015, 0, hz + 0.02))
    P += head
    path = [(-0.13, -0.03), (-0.165, -0.075), (-0.165, -0.12), (-0.135, -0.15), (-0.08, -0.155), (-0.02, -0.155),
            (0.04, -0.155), (0.10, -0.15), (0.15, -0.13), (0.172, -0.10)]
    for k, (tx, ty) in enumerate(path):                               # 꼬리: 엉덩이 옆으로 돌아 앞발 쪽으로
        w = 0.046 - 0.0015 * k
        b(tx, ty, 0.0 + 0.0, 0.046, w, 0.046 + (0.012 if k == 9 else 0.0), 1 if (k % 2 or k == 9) else 0)
    return P


def _cat_lie(K, bend, eyes):
    """엎드린 고양이: 몸통 16칸을 호로 이은 상자 사슬(오른쪽으로 bend만큼 휨) + 엉덩이 + 머리(턱 괴고) + 꼬리(같은 호의 뒤쪽). (31편 원형)"""
    P = []
    kap = -bend / RING_R
    n = 16
    ds = SPINE / n

    def pos(s):
        if abs(kap) < 1e-6:
            return s, 0.0, 0.0
        return math.sin(kap * s) / kap, (1 - math.cos(kap * s)) / kap, kap * s

    for k in range(n):
        px, py, h = pos((k + 0.5) * ds)
        bm = K.bm_cube(ds * 1.18, 0.152 - 0.002 * k, 0.125 + 0.0012 * (k % 5), (px, py, 0.0), bottom=True)
        P.append((_rot_z(bm, h, (px, py)), 1 if k % 3 == 2 else 0))
    px, py, h = pos(0.06)                                             # 엉덩이 불룩
    for sg in (-1, 1):
        bm = K.bm_cube(0.09, 0.07, 0.135, (px - sg * 0.07 * math.sin(h), py + sg * 0.07 * math.cos(h), 0.0), bottom=True)
        P.append((_rot_z(bm, h, (px - sg * 0.07 * math.sin(h), py + sg * 0.07 * math.cos(h))), 0))
    ex, ey, eh = pos(SPINE)                                           # 머리: 몸 끝에서 안쪽으로 더 돌려 턱을 괴고
    hh = eh - 0.7 * bend
    head = _cat_head(K, "open" if eyes else "closed")
    for sy in (-0.045, 0.045):                                        # 턱 밑 앞발
        head.append((K.bm_cube(0.075, 0.05, 0.036, (0.135, sy, 0.0), bottom=True), 2))
    P += _cat_place(head, ex - 0.005 * math.cos(eh), ey - 0.005 * math.sin(eh), 0.0, hh)
    for k in range(10):                                               # 꼬리: 같은 호를 뒤로 이어 바닥에 깔림
        px, py, h = pos(-(k + 0.5) * 0.032)
        w = 0.05 - 0.0015 * k
        bm = K.bm_cube(0.036, w, w, (px, py, 0.0), bottom=True)
        P.append((_rot_z(bm, h, (px, py)), 1 if (k % 2 or k == 9) else 0))
    return P


def _cat_parts(name):
    from engine import bkit as K
    if name in ("stand", "walk_a", "walk_b", "crouch"):
        return _cat_upright(K, name)
    if name in ("lie0o", "lie0c"):
        return _cat_lie(K, 0.0, name == "lie0o")
    if name == "rb5":
        return _cat_lie(K, BEND_FULL, False)
    if name == "leap":
        return _cat_leap(K)
    if name == "sit":
        return _cat_sit(K)
    if name == "sit_y1":
        return _cat_sit(K, "squeeze", 0.45)
    if name == "sit_y2":
        return _cat_sit(K, "squeeze", 1.0)
    if name == "sit_meow":
        return _cat_sit(K, "open", 0.4)
    if name == "sit_happy":
        return _cat_sit(K, "happy", 0.0, True)
    if name == "sit_up":
        return _cat_sit(K, "open", 0.0, False, -0.55)
    if name == "sit_blink":
        return _cat_sit(K, "closed")
    if name in ("eat_a", "eat_b"):
        return _cat_eat(K, name)
    raise KeyError(name)


def ring_origin(c, psi_deg, s=1.0):
    """몸을 말았을 때 고리 가운데가 c가 되도록 하는 고양이 원점(엉덩이) (배율 s). 고리 가운데는 몸의 오른쪽 RING_R."""
    p = math.radians(psi_deg)
    return c[0] - s * RING_R * math.sin(p), c[1] + s * RING_R * math.cos(p)



# ───────────────────────── 도트 글자 (한글 16x16 · 숫자 5x7) · 말풍선 ─────────────────────────
# 도트 글자 16x16: 한 줄(가로 16칸)을 16진 4자리로, 맨 윗줄부터 16줄 이어 붙임(왼쪽 칸 = 가장 높은 비트).
# 만든 법(새 낱말이 필요하면 같은 방식으로): assets/fonts/NotoSansKR-VF.ttf(OFL)를 굵기 620으로 크게 그려 글자 경계 상자를
# 가로세로 비율 그대로 16칸 격자 가운데에 꽉 차게(0.94) 줄이고, 칸 평균이 0.40 이상이면 켬. 숫자·기호는 5x7 글꼴 또는 손으로 그림.
GLYPH = {
    "야": "001000181e183f18739e619e61986198619e739e3f181e180018001800180010",
    "옹": "03c01ff01838381c1c380ff001807ffe7ffe00000ff01ff8181818381ff003c0",
    "배": "0004006c336c336c336c3f6c3f7c337c336c336c3f6c3f6c006c006c006c0004",
    "고": "00003ffc3ffc000c000c000c000c030c031c031c031803000300ffff7ffe0000",
    "파": "001000187fd83f981b181b181b1e1b1e1b181b187fd87fd80018001800180010",
    "놀": "1000180018001ff81ff801807ffe7ffe00003ff81ff81ff81ff818001ffc1ff8",
    "아": "001000183e183f1863986198619e619e619873983f181e180018001800180010",
    "줘": "00041fcc3fcc070c070c1fcc38ec000c3fec3fec060c067c060c060c060c0004",
    "옆": "000c0e0c3ffc31fc71cc71cc31fc1ffc060c0ffc0ffc0730033003301ffc0ffc",
    "에": "0004006c1e6c3f6c336c336c33ec33ec336c336c3f6c1e6c006c006c006c0004",
    "있": "00081e1c3f1c719c619c619c739c3f1c0c1c00000c300e301e783bfc33cc0000",
    "어": "000c040c1f0c1b8c318c31cc30fc30fc318c318c1f8c0f0c000c000c000c000c",
    "근": "1ff83ffc001c001c001c001c001c7ffe7ffe000038003800380038003ffc1ffc",
    "력": "000c3f0c3fbc03fc3f8c3f8c307c318c3f8c000c0ffc0ffc000c000c000c000c",
    "체": "00040c7e0c7e3ffe3ffe0c7e0cfe0efe0e7e1f7e3bfe31fe007e007e002e0004",
    "중": "3ffc3ffc03c007e03e7c3c3c00007ffe7ffe01800ff01ff838181c381ff803c0",
    "품": "3ff83ffc0c700c700e703ffc00007ffe7ffe01801ff83ff8381838183ff81ff8",
    "절": "000c3fcc3fcc060c0f7c0f0c39cc30cc00000ffc07fc0ffc0ffc0c000ffe0ffc",
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
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
}


def _glyph_rows(c):
    """글자 하나 → 16줄 문자열('#'=칸 켬), 비어 있는 좌우 열은 잘라 냄. 숫자는 5x7을 두 배로(위아래 한 줄씩 비움)."""
    if c in FONT57:
        rows = ["." * 10] + ["".join(("##" if b == "1" else "..") for b in r) for r in FONT57[c] for _ in (0, 1)] + ["." * 10]
        return [r.replace("1", "#") for r in rows]
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


C0 = 0.04                                      # 말풍선 한 칸(m). 실제 크기는 말풍선마다 화면 비율로 키움(cpx)
PAL_ORDER = "RPKOYGB"
PAL = {"R": (0.93, 0.15, 0.20), "P": (1.0, 0.72, 0.78), "K": (0.10, 0.10, 0.16), "O": (1.0, 0.55, 0.10),
       "Y": (1.0, 0.80, 0.12), "G": (0.08, 0.60, 0.32), "B": (0.15, 0.40, 0.90)}
ICONS = {      # 이름: (그림 줄들(글자 = 색), 그림 한 점이 차지하는 칸 수)
    "excl": (["RRR", "RRR", ".R.", ".R.", ".R.", "...", ".R."], 3),
    "heart": ([".RR.RR.", "RPRRRRR", "RRRRRRR", ".RRRRR.", "..RRR..", "...R..."], 3),
    "dots3": (["KK.KK.KK", "KK.KK.KK"], 3),
    "meow": (_text_grid("야옹", "K"), 1),
    "hungry": (_text_grid("배고파", "K"), 1),
    "play": (_text_grid("놀아 줘", "K"), 1),
    "stay": (_text_grid("옆에 있어 줘", "K"), 1),
    "str": (_text_grid("근력 14", "G"), 1),
    "wgt": (_text_grid("체중 50", "R"), 1),
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
    s = pop(tau)
    life = sp.get("life")
    if life is not None:
        if tau >= life:
            return 0.0
        if tau > life - 0.16:
            s *= (life - tau) / 0.16
    return s


# ── 7-세그먼트 숫자 (체중계·눈금 숫자) · 5x7 점 글자(Z) ──
SEG7 = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}


def seg_digits(text, cx, cz, y, col, w=0.14, h=0.30, t=0.035, gap=0.2, depth=0.012):
    """7-세그먼트 숫자 줄 → 발광 상자 [(위치, 크기, 회전, 색)]. text의 공백은 건너뜀(오른쪽 맞춤은 호출 쪽에서 공백으로). y 평면, 앞 = -y."""
    out = []
    n = len(text)
    for k, ch in enumerate(text):
        if ch == " ":
            continue
        x0 = cx + (k - (n - 1) / 2.0) * gap
        seg = {"a": (x0, cz + h / 2 - t / 2, w, t), "d": (x0, cz - h / 2 + t / 2, w, t), "g": (x0, cz, w, t),
               "b": (x0 + w / 2 - t / 2, cz + h / 4, t, h / 2), "c": (x0 + w / 2 - t / 2, cz - h / 4, t, h / 2),
               "f": (x0 - w / 2 + t / 2, cz + h / 4, t, h / 2), "e": (x0 - w / 2 + t / 2, cz - h / 4, t, h / 2)}
        for s in SEG7[int(ch)]:
            px, pz, sx, sz = seg[s]
            out.append(((px, y, pz), (sx, depth, sz), (0.0, 0.0, 0.0), col))
    return out


def pix_runs(txt, ctr, cell, right, up, col, rz=0.0):
    """5x7 글자 → 같은 줄에 이어진 칸을 상자 하나로 묶은 발광 상자 목록 (right·up = 글이 놓인 면의 방향 단위벡터)."""
    out = []
    n = len(txt)
    for k, ch in enumerate(txt):
        for r, row in enumerate(FONT57[ch]):
            c = 0
            while c < 5:
                if row[c] != "1":
                    c += 1
                    continue
                c1 = c
                while c1 + 1 < 5 and row[c1 + 1] == "1":
                    c1 += 1
                kx = ((k * 6 + (c + c1 + 1) / 2.0) - (n * 6 - 1) / 2.0) * cell
                kz = (6 - r + 0.5) * cell
                p = (ctr[0] + right[0] * kx + up[0] * kz, ctr[1] + right[1] * kx + up[1] * kz, ctr[2] + right[2] * kx + up[2] * kz)
                out.append((p, (cell * (c1 - c + 1), cell * 0.5, cell), (0.0, 0.0, rz), col))
                c = c1 + 1
    return out


def billboard(ctr, cam_loc):
    """글·그림을 카메라 쪽으로 돌려 세우는 (오른쪽, 위, 회전) — ctr은 세트 좌표, cam_loc은 같은 세트 좌표."""
    ang = math.atan2(cam_loc[1] - ctr[1], cam_loc[0] - ctr[0])
    return (-math.sin(ang), math.cos(ang), 0.0), (0.0, 0.0, 1.0), ang - math.pi / 2


# ── 효과 도우미 ──
def puffs(c, tl, t0, n=8, r=0.045, life=0.6, size=0.012, col=(0.95, 0.93, 0.88)):
    """c 둘러싸고 퍼지며 사라지는 먼지 덩이 (세트 좌표)."""
    tau = tl - t0
    if tau <= 0 or tau > life:
        return []
    f = tau / life
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + 0.4 * (k % 3)
        rr = r * (0.3 + 0.7 * math.sqrt(f))
        s = size * (1 - f) * (1 + 0.4 * (k % 2))
        out.append(((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a), c[2] + s / 2 + 0.006 * f), (s, s, s), (a, f * 3, 0), col))
    return out


def sparkles(c, tl, t0, n=12, r=0.05, life=0.9, size=0.006, cols=((1.0, 0.85, 0.3), (1.0, 0.6, 0.75), (1.0, 1.0, 0.9))):
    """c 둘러싸고 터지는 발광 반짝이."""
    tau = tl - t0
    if tau <= 0 or tau > life:
        return []
    f = tau / life
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + 0.7 * (k % 3)
        rr = r * (0.35 + 0.65 * ((k * 5) % 7) / 6.0) * math.sqrt(f)
        s = size * (1 - f) * (1 + 0.5 * (k % 2))
        out.append(((c[0] + rr * math.cos(a), c[1] + 0.3 * rr * math.sin(2 * a), c[2] + rr * math.sin(a) * 0.9 + 0.01), (s, s, s),
                    (a, f * 4, 0), cols[k % len(cols)]))
    return out


def ballistic(p0, v0, tt, g=9.8, floor=0.0):
    """p0에서 v0로 던진 물체의 tt초 뒤 위치 (바닥 floor에 닿으면 그 자리에 멈춤)."""
    x, y = p0[0] + v0[0] * tt, p0[1] + v0[1] * tt
    z = p0[2] + v0[2] * tt - 0.5 * g * tt * tt
    if z <= floor:
        disc = v0[2] ** 2 + 2 * g * (p0[2] - floor)
        t1 = (v0[2] + math.sqrt(max(disc, 0.0))) / g
        return (p0[0] + v0[0] * t1, p0[1] + v0[1] * t1, floor), True
    return (x, y, z), False



# ───────────────────────── 세트 ─────────────────────────
WOODC = (0.62, 0.42, 0.25)
DWOOD = (0.38, 0.25, 0.15)
DARK = (0.2, 0.2, 0.22)
SISAL = (0.78, 0.66, 0.48)
WALLH = 3.0

# 거실 가구 자리 (세트 좌표)
SOFA = dict(x0=-2.4, x1=-0.1, y0=1.75, y1=2.99)          # 소파 (뒷벽, 문 오른쪽): 폭 2.3 · 깊이 1.25
SOFA_SEAT = 0.46                                          # 멀쩡한 소파 방석 높이
SHELF_Z = 1.5                                             # 높은 선반 윗면 (뒷벽 오른쪽)
SHELF_X = (1.6, 3.6)
SHELF_Y = (2.5, 2.99)
DOOR_X = (-3.5, -2.6)                                     # 뒷벽 왼쪽 문 자리 (뒤는 복도)
SOFA_CX = -1.65                                           # 소파 위 거대 고양이가 앉는 x (소파 왼쪽 치우침: 문가 지수와 가깝게)


def _room3(v, x0, x1, yf, yb, wall, side, floor_col, tile=0.25, kind="wood"):
    """앞(-y)이 열린 방: 바닥 + 뒷벽·양옆 벽(높이 3m)."""
    v.floor(x0, x1, yf, yb, floor_col, tile, kind)
    v.wall((x0, yb), (x1, yb), 0, WALLH, wall, tile, face=-1)
    v.wall((x0, yf), (x0, yb), 0, WALLH, side, tile, face=-1)
    v.wall((x1, yf), (x1, yb), 0, WALLH, side, tile, face=1)


def _cat_tower(v):
    """높은 캣타워 (1년 뒤 거실 오른쪽 뒤): 바닥판 + 사이잘 기둥 둘 + 발판 셋(0.5 · 0.95 · 1.4m) + 숨숨집."""
    pl = (0.90, 0.84, 0.74)
    v.box(2.2, 3.8, 1.4, 2.9, 0, 0.10, (0.85, 0.82, 0.76))
    v.box(2.45, 2.70, 1.85, 2.10, 0.10, 1.40, SISAL)
    v.box(3.25, 3.50, 2.35, 2.60, 0.10, 0.95, SISAL)
    v.box(2.30, 3.30, 1.55, 2.45, 0.48, 0.52, pl)
    v.box(2.75, 3.75, 1.95, 2.85, 0.93, 0.97, pl)
    v.box(2.30, 3.30, 1.55, 2.45, 1.38, 1.42, pl)
    v.box(3.0, 3.75, 1.5, 2.3, 0.10, 0.48, (0.82, 0.70, 0.55))
    v.box(3.2, 3.55, 1.49, 1.5, 0.12, 0.38, (0.12, 0.10, 0.08), jit=0)
    v.box(2.25, 2.35, 1.5, 1.7, 0.10, 0.16, (0.9, 0.5, 0.5))


def _liv(v):
    """지수네 거실(낮): 앞(-y)이 열린 방. 뒷벽 왼쪽 문(복도)·그 옆 소파(동적)와 창, 뒷벽 오른쪽 높은 선반, 오른쪽 벽 TV."""
    wb, ws = (0.93, 0.90, 0.82), (0.88, 0.89, 0.80)
    v.floor(-4, 4, -4.0, 3.0, (0.72, 0.54, 0.36), 0.25, "wood")
    v.wall((-4, 3), (DOOR_X[0], 3), 0, WALLH, wb, 0.25, face=-1)         # 뒷벽: 문 자리(x -3.5~-2.6, 높이 2.1)를 비움
    v.wall((DOOR_X[0], 3), (DOOR_X[1], 3), 2.1, WALLH, wb, 0.25, face=-1)
    v.wall((DOOR_X[1], 3), (4, 3), 0, WALLH, wb, 0.25, face=-1)
    v.wall((-4, -4), (-4, 3), 0, WALLH, ws, 0.25, face=-1)
    v.wall((4, -4), (4, 3), 0, WALLH, ws, 0.25, face=1)
    # 문 뒤 복도 (바닥·양옆 벽·밝은 끝벽·천장 불빛) · 문틀
    v.floor(DOOR_X[0], DOOR_X[1], 3.0, 3.9, (0.62, 0.46, 0.30), 0.3, "wood")
    v.wall((DOOR_X[0], 3.0), (DOOR_X[0], 3.9), 0, 2.1, (0.84, 0.80, 0.72), 0.3, face=-1)
    v.wall((DOOR_X[1], 3.0), (DOOR_X[1], 3.9), 0, 2.1, (0.84, 0.80, 0.72), 0.3, face=1)
    v.wall((DOOR_X[0], 3.9), (DOOR_X[1], 3.9), 0, 2.1, (0.95, 0.92, 0.85), 0.3, face=-1)
    v.floor(DOOR_X[0], DOOR_X[1], 3.0, 3.9, (0.90, 0.88, 0.82), 0.3, z=2.1)
    v.box(DOOR_X[0] + 0.2, DOOR_X[1] - 0.2, 3.2, 3.7, 2.06, 2.1, (1.0, 0.92, 0.75), jit=0, glow=True)
    v.box(DOOR_X[0] - 0.08, DOOR_X[0], 2.93, 2.99, 0, 2.1, DWOOD)
    v.box(DOOR_X[1], DOOR_X[1] + 0.08, 2.93, 2.99, 0, 2.1, DWOOD)
    v.box(DOOR_X[0] - 0.08, DOOR_X[1] + 0.08, 2.93, 2.99, 2.1, 2.18, DWOOD)
    # 창(소파 위) + 커튼
    v.window(-2.1, -0.4, 2.99, 1.15, 2.5, night=False, face=-1)
    cu = (0.90, 0.64, 0.70)
    v.box(-2.38, -2.15, 2.86, 2.95, 0.9, 2.7, cu)
    v.box(-0.35, -0.12, 2.86, 2.95, 0.9, 2.7, cu)
    v.box(-2.43, -0.07, 2.88, 2.92, 2.66, 2.72, DWOOD)
    # 그림 액자 · 러그 · 화분
    v.box(0.45, 1.25, 2.96, 2.99, 1.4, 2.1, (0.35, 0.25, 0.18))
    v.box(0.50, 1.20, 2.95, 2.96, 1.45, 2.05, (0.55, 0.75, 0.92), jit=0.02)
    v.box(0.50, 1.20, 2.94, 2.95, 1.45, 1.70, (0.45, 0.68, 0.40), jit=0.03)
    v.floor(-3.0, 0.5, -0.6, 1.5, (0.82, 0.55, 0.58), 0.5, "check", z=0.012)
    v.box(-3.85, -3.35, -1.3, -0.8, 0, 0.45, (0.35, 0.6, 0.45))
    v.box(-3.9, -3.3, -1.35, -0.75, 0.45, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    # 오른쪽 벽: TV 장 + TV
    v.box(3.25, 3.95, -0.3, 1.9, 0, 0.5, DWOOD)
    v.box(3.90, 3.95, 0.0, 1.6, 0.5, 1.2, (0.05, 0.05, 0.06))
    v.box(3.89, 3.90, 0.05, 1.55, 0.55, 1.15, (0.20, 0.32, 0.45), jit=0, glow=True)
    # 높은 선반: 널빤지 + 받침 둘 + 책 줄 + 화분 (왼쪽 끝 책은 쓰러지는 책으로 따로 움직임)
    sx0, sx1 = SHELF_X
    sy0, sy1 = SHELF_Y
    v.box(sx0, sx1, sy0, sy1, SHELF_Z - 0.05, SHELF_Z, (0.70, 0.52, 0.34))
    for bx in (sx0 + 0.18, sx1 - 0.18):
        v.box(bx - 0.04, bx + 0.04, sy0 + 0.05, sy1 - 0.01, SHELF_Z - 0.33, SHELF_Z - 0.05, DWOOD)
    cols = [(0.9, 0.3, 0.3), (0.3, 0.6, 0.9), (0.95, 0.8, 0.25), (0.35, 0.75, 0.45), (0.8, 0.5, 0.85), (0.95, 0.55, 0.2)]
    x = sx0 + 0.12
    k = 0
    while x < 2.38:
        w = 0.05 + 0.02 * (k % 3)
        h = 0.20 + 0.03 * ((k * 5) % 4)
        v.box(x, x + w, 2.80, 2.96, SHELF_Z, SHELF_Z + h, cols[k % len(cols)], jit=0.05)
        x += w + 0.006
        k += 1
    v.box(3.12, 3.40, 2.70, 2.95, SHELF_Z, SHELF_Z + 0.18, (0.35, 0.6, 0.45))
    v.box(3.08, 3.44, 2.66, 2.99, SHELF_Z + 0.18, SHELF_Z + 0.5, (0.25, 0.55, 0.25), jit=0.1)
    # 조명
    v.light(-1.0, 0.8, 2.7, 140, (1.0, 0.92, 0.78), 0.5, "ep35_liv_a")
    v.light(-1.25, 2.0, 2.3, 100, (0.85, 0.92, 1.0), 0.8, "ep35_liv_w")
    v.light(2.2, 0.6, 2.7, 130, (1.0, 0.95, 0.85), 0.6, "ep35_liv_b")
    v.light(0.5, -2.0, 2.2, 90, (1.0, 0.95, 0.9), 0.8, "ep35_liv_f")
    v.light((DOOR_X[0] + DOOR_X[1]) / 2, 3.4, 1.9, 40, (1.0, 0.92, 0.78), 0.3, "ep35_liv_hall")


def _bed(v):
    """침실(낮): 머리판이 뒷벽인 침대(시트 0.52 · 이불 0.60) + 오른쪽 창 + 협탁 + 옷장. 바닥 오른쪽은 지수가 요를 펴는 자리."""
    _room3(v, -3.2, 3.2, -4.0, 3.0, (0.86, 0.88, 0.95), (0.80, 0.84, 0.92), (0.70, 0.52, 0.34))
    v.box(-0.9, 0.9, 0.9, 2.94, 0, 0.32, WOODC)                                          # 침대 틀
    v.box(-0.87, 0.87, 0.93, 2.91, 0.32, 0.52, (0.92, 0.92, 0.90), jit=0.02)             # 매트리스
    v.box(-0.95, 0.95, 2.94, 2.99, 0, 1.05, DWOOD)                                        # 머리판
    v.box(-0.85, 0.85, 0.95, 2.0, 0.52, 0.60, (0.42, 0.60, 0.88))                        # 이불
    v.box(-0.72, -0.05, 2.45, 2.88, 0.52, 0.64, (0.97, 0.97, 0.97), jit=0.01)            # 베개
    v.box(0.05, 0.72, 2.45, 2.88, 0.52, 0.64, (0.97, 0.97, 0.97), jit=0.01)
    v.window(1.3, 2.7, 2.99, 1.0, 2.5, night=False, face=-1)
    cu = (0.90, 0.64, 0.70)
    v.box(1.05, 1.28, 2.86, 2.95, 0.8, 2.7, cu)
    v.box(2.72, 2.95, 2.86, 2.95, 0.8, 2.7, cu)
    v.box(-1.55, -1.05, 2.45, 2.9, 0, 0.55, WOODC)                                       # 협탁 + 스탠드
    v.box(-1.4, -1.2, 2.6, 2.75, 0.55, 0.62, DARK)
    v.box(-1.45, -1.15, 2.55, 2.8, 0.62, 0.85, (1.0, 0.88, 0.62), jit=0, glow=True)
    v.box(-3.15, -2.5, 0.8, 2.9, 0, 2.3, (0.80, 0.72, 0.62))                             # 옷장
    v.box(-2.505, -2.495, 1.78, 1.82, 0.1, 2.2, DWOOD, jit=0)
    for y in (1.7, 1.9):
        v.box(-2.52, -2.49, y - 0.02, y + 0.02, 1.0, 1.25, DWOOD, jit=0)
    v.floor(1.0, 3.0, 0.0, 2.6, (0.78, 0.62, 0.55), 0.5, "check", z=0.012)              # 요 밑 러그
    v.light(0.0, 1.5, 2.7, 130, (1.0, 0.92, 0.78), 0.5, "ep35_bed_a")
    v.light(2.0, 2.2, 2.3, 100, (0.85, 0.92, 1.0), 0.8, "ep35_bed_w")
    v.light(0.2, -1.5, 2.2, 90, (1.0, 0.95, 0.9), 0.8, "ep35_bed_f")


def _gondola(v, x0, x1, y0, y1, h, rows, gaps=(), left=True):
    """마트 진열대: 가운데 판 양쪽에 알록달록 상품. gaps = [(y 시작, y 끝)] 구간은 텅 빔(몇 개만 남김)."""
    rs = v.rs
    v.box(x0, x1, y0, y1, 0, 0.1, (0.55, 0.56, 0.58))
    c0, c1 = x0 + (x1 - x0) * 0.4, x1 - (x1 - x0) * 0.4
    v.box(c0, c1, y0 + 0.01, y1 - 0.01, 0.1, h, (0.7, 0.72, 0.75))
    cols = [(0.9, 0.25, 0.2), (0.95, 0.75, 0.2), (0.25, 0.55, 0.9), (0.3, 0.75, 0.35), (0.95, 0.55, 0.75), (0.95, 0.95, 0.92),
            (0.6, 0.35, 0.2), (0.95, 0.55, 0.15)]
    for r in range(rows):
        z = 0.12 + r * (h - 0.15) / rows
        v.box(x0, x1, y0, y1, z, z + 0.03, (0.8, 0.8, 0.82))
        y = y0 + 0.04
        while y < y1 - 0.12:
            w = float(rs.uniform(0.08, 0.16))
            hh = float(rs.uniform(0.12, (h - 0.15) / rows - 0.06))
            c = cols[int(rs.integers(len(cols)))]
            gap = any(ga - 0.02 < y and y + w < gb + 0.02 for ga, gb in gaps)
            if not gap:
                for side in ((x0 + 0.02, c0 - 0.01), (c1 + 0.01, x1 - 0.02)):
                    v.box(side[0], side[1], y, y + w, z + 0.03, z + 0.03 + hh, c, jit=0.08)
            y += w + 0.015


def _flag(v, xa, xb, y, zc, ch="R"):
    """통로 쪽으로 튀어나온 빨간 '품절' 깃발 (앞 = -y, 글자는 흰 발광 점)."""
    v.box(xa, xb, y, y + 0.03, zc - 0.16, zc + 0.16, (0.85, 0.13, 0.17), jit=0)
    rows = _text_grid("품절", "#")
    n = len(rows[0])
    cell = (xb - xa) * 0.9 / n
    z0 = zc - 8 * cell
    for r, c0, c1 in _runs(rows):
        v.box(xa + (xb - xa) * 0.05 + c0 * cell, xa + (xb - xa) * 0.05 + (c1 + 1) * cell, y - 0.012, y, z0 + (15 - r) * cell,
              z0 + (16 - r) * cell, (1.0, 0.97, 0.9), jit=0, glow=True)


def _mart(v):
    """마트 사료 통로: 양옆 진열대(가운데 구간은 텅 빈 '품절'), 끝벽 배너. 카메라는 통로 입구(-y)에서 안쪽(+y)을 봄."""
    v.floor(-3.2, 3.2, -3.4, 7.0, (0.86, 0.87, 0.85), 0.5, "check")
    wc = (0.95, 0.94, 0.92)
    v.wall((-3.2, 7.0), (3.2, 7.0), 0, 3.4, wc, 0.5, face=-1)
    v.wall((-3.2, -3.4), (-3.2, 7.0), 0, 3.4, (0.90, 0.88, 0.84), 0.5, face=-1)
    v.wall((3.2, -3.4), (3.2, 7.0), 0, 3.4, (0.90, 0.88, 0.84), 0.5, face=1)
    gaps = ((1.4, 4.7),)
    _gondola(v, -2.3, -1.45, 0.2, 6.4, 2.0, 5, gaps)
    _gondola(v, 1.45, 2.3, 0.2, 6.4, 2.0, 5, gaps)
    _flag(v, -1.45, -0.95, 2.0, 1.3)
    _flag(v, -1.45, -0.95, 3.9, 1.3)
    _flag(v, 0.95, 1.45, 2.9, 1.3)
    _flag(v, 0.95, 1.45, 4.3, 1.3)
    for y, z in ((2.6, 0.2), (3.4, 0.2)):                                      # 남은 통조림 하나씩
        v.box(-1.62, -1.52, y, y + 0.08, z + 0.03 + 0.5, z + 0.03 + 0.62, (0.88, 0.88, 0.9))
    # 끝벽 배너 (주황 판 + 하얀 발바닥)
    v.box(-1.6, 1.6, 6.96, 6.99, 1.9, 3.0, (1.0, 0.62, 0.2), jit=0)
    pw = (1.0, 0.97, 0.9)
    v.box(-0.35, 0.35, 6.945, 6.96, 2.0, 2.45, pw, jit=0, glow=True)
    for tx, tz in ((-0.55, 2.55), (-0.2, 2.75), (0.2, 2.75), (0.55, 2.55)):
        v.box(tx - 0.11, tx + 0.11, 6.945, 6.96, tz, tz + 0.22, pw, jit=0, glow=True)
    # 바닥 안내선 + 천장 불빛 띠
    v.box(-0.04, 0.04, -3.0, 6.8, 0.0, 0.012, (0.95, 0.75, 0.2), jit=0)
    for y in (0.5, 2.5, 4.5, 6.3):
        v.box(-0.7, 0.7, y, y + 0.35, 3.35, 3.4, (1.0, 1.0, 0.97), jit=0, glow=True)
    for k, y in enumerate((0.4, 2.8, 5.2)):
        v.light(0.0, y, 3.0, 150, (1.0, 0.97, 0.92), 0.6, "ep35_mart_%d" % k)
    v.light(0.0, -1.4, 2.4, 100, (1.0, 0.97, 0.92), 0.8, "ep35_mart_f")


def _year(v, dusk=False):
    """1년 뒤 거실(낮은 가구 + 높은 캣타워): 왼쪽 낮은 소파, 뒷벽 가운데 창(화분 놓인 창턱), 오른쪽 캣타워, 스탠드.
    dusk=True면 같은 방을 노을 창(주황·보라 띠) + 켜진 스탠드 + 낮춘 조명으로 한 번 더 지음(안아 주는 두 줄)."""
    _room3(v, -4.0, 4.0, -4.0, 3.0, (0.93, 0.90, 0.82), (0.88, 0.89, 0.80), (0.72, 0.54, 0.36))
    v.window(-1.7, 0.9, 2.99, 0.95, 2.5, night=False, face=-1)
    if dusk:
        zm = (0.95 + 2.5) / 2 + 0.1
        v.box(-1.7, 0.9, 2.962, 2.968, 0.95, zm, (1.0, 0.45, 0.20), jit=0, glow=True)
        v.box(-1.7, 0.9, 2.962, 2.968, zm, 2.5, (0.82, 0.36, 0.52), jit=0, glow=True)
    cu = (0.90, 0.64, 0.70)
    v.box(-1.97, -1.74, 2.86, 2.95, 0.8, 2.7, cu)
    v.box(0.94, 1.17, 2.86, 2.95, 0.8, 2.7, cu)
    v.box(-2.02, 1.22, 2.88, 2.92, 2.66, 2.72, DWOOD)
    v.box(-1.8, 1.0, 2.80, 2.97, 0.89, 0.94, (0.95, 0.95, 0.93))                          # 창턱
    v.box(-0.35, 0.05, 2.84, 2.94, 0.94, 1.10, (0.35, 0.6, 0.45))                         # 창턱 화분
    v.box(-0.40, 0.10, 2.80, 2.97, 1.10, 1.42, (0.25, 0.55, 0.25), jit=0.1)
    # 낮은 소파 (윗면 0.40)
    v.box(-3.8, -2.0, 1.9, 2.99, 0, 0.28, (0.30, 0.42, 0.62))
    v.box(-3.6, -2.2, 1.9, 2.72, 0.28, 0.40, (0.38, 0.52, 0.74))
    v.box(-3.8, -2.0, 2.72, 2.99, 0.28, 0.78, (0.30, 0.42, 0.62))
    v.box(-3.8, -3.6, 1.9, 2.72, 0.28, 0.56, (0.27, 0.38, 0.58))
    v.box(-2.2, -2.0, 1.9, 2.72, 0.28, 0.56, (0.27, 0.38, 0.58))
    # 러그 · 방석 · 낮은 장 · 스탠드 · 캣타워
    v.floor(-3.4, 1.4, -1.0, 1.9, (0.80, 0.58, 0.45), 0.5, "check", z=0.012)
    v.box(0.3, 0.95, 0.2, 0.85, 0.012, 0.17, (0.88, 0.42, 0.40))
    v.box(-0.55, 0.0, 1.1, 1.65, 0.012, 0.15, (0.45, 0.62, 0.45))
    v.box(-1.85, -1.55, 2.35, 2.65, 0, 0.04, DARK)                                       # 스탠드: 받침·기둥·갓
    v.box(-1.71, -1.69, 2.49, 2.51, 0.04, 1.45, DARK, jit=0)
    v.box(-1.9, -1.5, 2.3, 2.7, 1.45, 1.75, (1.0, 0.88, 0.62), jit=0, glow=True)
    _cat_tower(v)
    if dusk:
        v.light(-0.5, 0.8, 2.7, 60, (1.0, 0.80, 0.62), 0.5, "ep35_yr2_a")
        v.light(-0.4, 2.0, 2.3, 70, (1.0, 0.62, 0.40), 0.8, "ep35_yr2_w")
        v.light(2.2, 0.6, 2.7, 60, (1.0, 0.82, 0.66), 0.6, "ep35_yr2_b")
        v.light(0.0, -2.0, 2.2, 60, (1.0, 0.85, 0.70), 0.8, "ep35_yr2_f")
        v.light(-1.7, 2.3, 1.4, 150, (1.0, 0.75, 0.45), 0.4, "ep35_yr2_lamp")
    else:
        v.light(-0.5, 0.8, 2.7, 140, (1.0, 0.92, 0.78), 0.5, "ep35_yr_a")
        v.light(-0.4, 2.0, 2.3, 100, (0.85, 0.92, 1.0), 0.8, "ep35_yr_w")
        v.light(2.2, 0.6, 2.7, 130, (1.0, 0.95, 0.85), 0.6, "ep35_yr_b")
        v.light(0.0, -2.0, 2.2, 90, (1.0, 0.95, 0.9), 0.8, "ep35_yr_f")


def _year_dusk(v):
    _year(v, True)


def _sets():
    return (("liv", _liv), ("bed", _bed), ("mart", _mart), ("year", _year), ("year2", _year_dusk))



# ───────────────────────── 캐릭터 위치·움직임 ─────────────────────────
def at(st, x, y, yaw, pose, z=0.0, **kw):
    return dict(set=st, x=x, y=y, yaw=yaw, pose=pose, z=z, **kw)


def rel(d, fwd, lat, up):
    """캐릭터 기준 (앞, 왼쪽, 위) → 세트 좌표. 크기 반영."""
    a = math.radians(d["yaw"])
    s = d["scale"]
    return (d["x"] + s * (fwd * math.cos(a) - lat * math.sin(a)), d["y"] + s * (fwd * math.sin(a) + lat * math.cos(a)),
            d["z"] + s * up)


def head_pt(d):
    """지수 머리 꼭대기(세트 좌표)."""
    return rel(d, 0.0, 0.0, hip_of(d["pose"]) + 1.04)


CAT_HEAD = {"stand": (0.47, 0.42), "walk_a": (0.47, 0.42), "walk_b": (0.47, 0.42), "crouch": (0.46, 0.31), "lie0o": (0.45, 0.20),
            "lie0c": (0.45, 0.20), "rb5": (0.20, 0.20), "sit": (0.125, 0.40), "sit_y1": (0.11, 0.42), "sit_y2": (0.10, 0.44),
            "sit_meow": (0.12, 0.41), "sit_happy": (0.125, 0.40), "sit_up": (0.10, 0.43), "sit_blink": (0.125, 0.40),
            "leap": (0.47, 0.42), "eat_a": (0.55, 0.22), "eat_b": (0.52, 0.28)}


def cat_head_pt(d):
    """고양이 머리 꼭대기(세트 좌표)."""
    fx, fz = CAT_HEAD[d["pose"]]
    return rel(d, fx, 0.0, fz)


def walk_pose(tl, step=0.26, names=("walk_a", "walk_b")):
    return names[int(tl / step) % 2]


def mover(keys, st, step=0.26, end="stand", face=None, z=0.0, bob=0.012, names=("walk_a", "walk_b"), **kw):
    """keys = [(줄 안 시각, x, y), ...]를 직선으로 이으며 걷는 함수. 걷는 동안엔 step초마다 발걸음 자세를 바꾸고
    멈추면 end 자세로 face 방향(없으면 마지막으로 가던 방향)을 본다."""
    segs = [(a, b) for a, b in zip(keys, keys[1:]) if abs(b[1] - a[1]) + abs(b[2] - a[2]) > 1e-6]

    def fn(tl):
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
            return at(st, x, y, head, walk_pose(tl, step, names), z + bob * abs(math.sin(math.pi * tl / step)), **kw)
        return at(st, x, y, head if face is None else face, end, z, **kw)
    return fn


# ── 지수 (주황 셔츠 · 긴 머리) ──
def jisu(i, tl, du):
    """줄 i에서 지수 {set, x, y, z, yaw, pose} 또는 None."""
    L = LN
    if i == L["hook"]:                                   # 문가에서 놀라 뒷걸음질: 고양이를 보며(앞 오른쪽) 문 쪽(뒤 왼쪽)으로 물러남
        yaw = -60.0
        k = min(tl, 1.5)
        x, y = -3.0 - math.cos(math.radians(yaw)) * 0.55 * k, 2.0 - math.sin(math.radians(yaw)) * 0.55 * k
        if tl < 1.5:
            return at("liv", x, y, yaw, "shock_a" if int(tl / 0.2) % 2 == 0 else "shock_b", 0.012 * abs(math.sin(math.pi * tl / 0.2)))
        return at("liv", x, y, yaw, "gasp")
    if i == L["wake"]:
        if tl < 0.45 * du:                               # 침대에서 눈 뜨고 → 일어나 앉아 머리를 긁적
            if tl < 0.40:
                return at("bed", 0.0, 1.25, -90, "lieopen", 0.53)
            return at("bed", 0.0, 1.75, -90, "sit_conf", 0.27)
        tt = tl - 0.45 * du                              # 복도에서 문가로 걸어 나와 멈추고 깜짝
        if tt < 0.5:
            return at("liv", -3.05, 3.55 - 0.8 * tt / 0.5, -90, walk_pose(tt, 0.22), 0.012 * abs(math.sin(math.pi * tt / 0.22)))
        return at("liv", -3.05, 2.75, -65, "gasp")
    if i == L["futon"]:                                  # 이불을 안고 와서 요 위에 던지듯 펴고 눕는다
        if tl < 0.85:
            return mover([(0.0, 3.0, 0.7), (0.85, 2.3, 1.15)], "bed", step=0.24, end="carry", names=("carry_a", "carry_b"))(tl)
        if tl < 1.2:
            return at("bed", 2.3, 1.15, 180, "stand")
        hop = 0.16 * math.sin(math.pi * clamp((tl - 1.2) / 0.35))
        return at("bed", 1.9, 0.55, -90, "lie", 0.12 + hop)
    if i == L["mart"]:                                   # 빈 카트를 밀고 오다 텅 빈 진열대 앞에서 머리를 긁적
        return mover([(0.0, 0.15, 4.4), (2.3, 0.15, 2.4)], "mart", step=0.3, end="confused", names=("walk_a", "walk_b"))(tl)
    if i == L["year"]:
        return at("year", -2.7, 2.28, 0, "sit_phone", 0.07)
    if i in (L["meow"], L["wants"]):
        return at("year", -2.5, 2.28, 0, "sit_smile", 0.07)
    if i == L["hug"]:
        if tl < 0.12:
            return at("year2", -2.5, 2.28, 0, "sit_smile", 0.07)
        if tl < 1.0:
            return mover([(0.12, -2.5, 2.28), (1.0, -1.45, 1.6)], "year2", step=0.25, face=0)(tl)
        return at("year2", -1.45, 1.6, 0, "hug")
    if i == L["face"]:
        return at("year2", -1.5, 0.2, 90, "smile")
    return None


# ── 마트 엑스트라 5명 ──
N_EX = 5


def extras(i, tl):
    """줄 i의 마트 엑스트라 [{set, x, y, z, yaw, pose, hair, shirt, pants} 또는 None] x N_EX."""
    if i != LN["mart"]:
        return [None] * N_EX
    ex = [at("mart", 0.55, 6.2 - 0.35 * tl, 90, walk_pose(tl, 0.34), hair=0, shirt=EX_SH[0], pants=X.PANTS[1]),
          at("mart", -1.0, 5.6, 180, "phone", hair=1, shirt=EX_SH[2], pants=X.PANTS[3]),
          at("mart", 1.0, 5.0, 0, "stand", hair=0, shirt=EX_SH[4], pants=X.PANTS[0]),
          at("mart", -0.95, 3.9, 180, "talk", hair=1, shirt=(0.85, 0.20, 0.22), pants=X.PANTS[4]),
          at("mart", 1.0, 3.2, 0, "confused", hair=0, shirt=EX_SH[5], pants=X.PANTS[2])]
    return ex


# ── 소파 (동적 상자): k=0 멀쩡 → 1 주저앉음 ──
def sofa_k(i, tl):
    if i < LN["sofa"]:
        return 0.0
    if i == LN["sofa"]:
        return ramp(tl, T_LAND, T_LAND + 0.42)
    return 1.0


def sofa_seat(k):
    """소파 방석 윗면 높이."""
    return 0.12 * math.cos(1.0 * k) + 0.2 + lerp(0.14, 0.07, k)


def sofa_parts(k):
    """소파 상자 [(중심, 크기, 회전, 색)] (세트 좌표): 몸통·방석·등받이·팔걸이 + 다리 넷(양옆으로 벌어지며 꺾임)."""
    x0, x1, y0, y1 = SOFA["x0"], SOFA["x1"], SOFA["y0"], SOFA["y1"]
    zf = 0.12 * math.cos(1.0 * k)                      # 몸통 바닥 높이 (다리가 벌어질수록 낮아짐)
    th = (1.0 * k, 0.85 * k, 0.8 * k, 1.0 * k)         # 앞왼·앞오른·뒤왼·뒤오른 다리 벌어짐(라디안)
    base, cush, dark = (0.30, 0.42, 0.62), (0.38, 0.52, 0.74), (0.27, 0.38, 0.58)
    out = []
    for (lx, ly, sgn), a in zip(((x0 + 0.14, y0 + 0.14, -1), (x1 - 0.14, y0 + 0.14, 1), (x0 + 0.14, y1 - 0.14, -1),
                                 (x1 - 0.14, y1 - 0.14, 1)), th):
        ln = zf / math.cos(a) if a < 1.2 else zf
        b = -sgn * a                                    # 오른쪽 다리는 바닥이 +x로 벌어지게
        out.append(((lx - math.sin(b) * ln / 2, ly, zf - math.cos(b) * ln / 2), (0.08, 0.08, ln), (0.0, b, 0.0), DWOOD))
    zb = zf + 0.2
    out.append((((x0 + x1) / 2, (y0 + y1) / 2, zf + 0.1), (x1 - x0, y1 - y0, 0.2), (0, 0, 0), base))
    th_c = lerp(0.14, 0.07, k)
    out.append((((x0 + x1) / 2, (y0 + y1 - 0.3) / 2 - 0.0, zb + th_c / 2), (x1 - x0 - 0.44, y1 - y0 - 0.3, th_c), (0, 0, 0), cush))
    out.append((((x0 + x1) / 2, y1 - 0.15, zb + 0.25), (x1 - x0 - 0.1, 0.3, 0.5), (0, 0, 0), base))
    for ax in (x0 + 0.11, x1 - 0.11):
        out.append(((ax, (y0 + y1) / 2 - 0.0, zb + 0.14), (0.22, y1 - y0, 0.28), (0, 0, 0), dark))
    return out


# ── 고양이 4마리 (0 = 거대, 1~3 = 원래 크기) ──
def leap_path(tau, p0, p1, apex_z, lim=0.8):
    """p0→p1을 apex_z(m)까지 솟았다 내려오는 점프: (위치, 몸 기울기(코 위 = 음수), 체공 시간)."""
    g = 9.8
    v0 = math.sqrt(2 * g * max(apex_z - p0[2], 1e-3))
    T = v0 / g + math.sqrt(2 * max(apex_z - p1[2], 1e-3) / g)
    k = clamp(tau / T)
    x, y = lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k)
    z = p0[2] + v0 * tau - 0.5 * g * tau * tau if tau < T else p1[2]
    vh = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / T
    vz = v0 - g * min(tau, T)
    pitch = -max(-lim, min(lim, math.atan2(vz, max(vh, 0.8))))
    return (x, y, z), pitch, T


GIANT_APEX = 0.65                                    # 거대 고양이 점프에서 발이 오르는 높이(m)
SMALL_APEX = SHELF_Z + 0.25                          # 원래 크기 고양이가 선반으로 뛸 때 가장 높은 곳
T_SOFA = leap_path(0.0, (SOFA_CX, -0.1, 0.0), (SOFA_CX, 2.25, SOFA_SEAT), 0.65)[2]      # 소파로 폴짝 뛰어오르는 시간
T_LAND = 0.55 + T_SOFA                                                           # 소파에 올라앉아 주저앉기 시작하는 때(4번 줄)
T_THUD = 0.8 + leap_path(0.0, (2.8, 0.45, 0.0), (2.8, 0.75, 0.0), GIANT_APEX, 0.25)[2]  # 거대 고양이가 쿵 내려앉는 때(12번 줄)


def cat_dict(st, x, y, z, yaw, pose, s, roll=0.0, pitch=0.0):
    return dict(set=st, x=x, y=y, z=z, yaw=yaw, pose=pose, scale=s, roll=roll, pitch=pitch)


SC_PLAT = (0.1, 2.3, 0.8, 1.9)                       # 체중계 발판 (x0, x1, y0, y1) — 윗면 0.12m
TAPE_X0, TAPE_Y = 0.0, 0.55                          # 줄자 시작·줄 (바닥)
CAT_P3 = (2.8, 2.0, 1.42)                            # 캣타워 윗발판 · 중간 · 아랫발판 (고양이가 앉는 자리)
CAT_P2 = (3.25, 2.4, 0.97)
CAT_P1 = (2.5, 1.85, 0.52)
EAT_CAT = (0.35, 2.15)                               # 먹는 거대 고양이 엉덩이 (세트 좌표, 얼굴은 -y 쪽)
BAG_FRONT = (0.35, 0.5)                             # 먹는 사료 포대 자리
TOWER_XY = (-1.0, 1.2)                              # 빈 포대 탑
BAG_P = 0.6                                          # 포대 하나 먹는 데 걸리는 초
BAG_N = 9
FALL_SPECS = ((CAT_P3, (1.95, 1.15), 0.45, -135.0, 0.40, 180.0), (CAT_P2, (2.2, 0.95), 1.30, -120.0, 0.40, 235.0),
              (CAT_P1, (1.7, 1.3), 2.15, -100.0, 0.40, 20.0))
CAT_YR = (-0.35, 1.55)                               # 1년 뒤 거실에서 지수와 마주 앉는 거대 고양이 (왼쪽을 봄)


def cats(i, tl, du):
    """줄 i에서 고양이 네 마리 [dict 또는 None]. 0번 = 거대(S_G), 1~3 = 원래 크기(S_S)."""
    L = LN
    C = [None, None, None, None]
    if i == L["hook"]:                                   # 소파에서 쩍 하품 → 입을 다물고 → 지수를 바라봄
        pose = "sit_y2" if tl < 1.45 else "sit_y1" if tl < 1.8 else "sit_blink" if tl < 2.15 else "sit"
        wob = 0.025 * math.sin(2 * math.pi * 1.2 * tl) * (1.0 if tl < 1.8 else 0.0)
        C[0] = cat_dict("liv", SOFA_CX, 2.25, SOFA_SEAT, -90, pose, S_G, roll=wob)
    elif i == L["wake"]:
        if tl >= 0.45 * du:
            tt = tl - 0.45 * du
            C[0] = cat_dict("liv", SOFA_CX, 2.25, SOFA_SEAT, -90, "sit_blink" if 0.9 < tt < 1.05 else "sit", S_G)
    elif i == L["ruler"]:                                # 줄자 옆에서 46cm → 170cm로 쑥 커짐
        s = lerp(S_S, S_G, pop(tl - 0.35, 1.0, 1.2))
        C[0] = cat_dict("liv", TAPE_X0, 1.2, 0.0, 0, "stand", s)
    elif i == L["scale"]:                                # 체중계 위에 올라선 거대 고양이
        C[0] = cat_dict("liv", 0.5, 1.35, 0.12, 0, "stand", S_G, roll=0.012 * math.sin(2 * math.pi * 1.4 * tl))
    elif i == L["sofa"]:                                 # 소파 앞에서 웅크렸다 폴짝 올라앉자 소파가 주저앉음
        k = sofa_k(i, tl)
        if tl < 0.25:
            C[0] = cat_dict("liv", SOFA_CX, -0.1, 0.0, 90, "stand", S_G)
        elif tl < 0.55:
            C[0] = cat_dict("liv", SOFA_CX, -0.1, 0.0, 90, "crouch", S_G)
        elif tl < T_LAND:
            p, pit, _ = leap_path(tl - 0.55, (SOFA_CX, -0.1, 0.0), (SOFA_CX, 2.25, SOFA_SEAT), 0.65)
            C[0] = cat_dict("liv", p[0], p[1], p[2], 90, "leap", S_G, pitch=pit * 0.5)
        else:
            ta = tl - T_LAND
            bob = 0.02 * math.sin(2 * math.pi * 5 * ta) * max(0.0, 1 - ta / 0.8)
            C[0] = cat_dict("liv", SOFA_CX, 2.25, sofa_seat(k) + bob, 90 - 180 * ramp(ta, 0.05, 0.3),
                            "sit_blink" if 1.75 < tl < 1.9 else "sit", S_G)
    elif i in (L["nap"], L["futon"]):                    # 침대를 통째로 차지하고 몸을 만 채 쿨쿨 (숨쉬는 배)
        c = (0.0, 1.8)
        s = S_G * (1.0 + 0.012 * math.sin(2 * math.pi * 0.45 * tl))
        ox, oy = ring_origin(c, 90.0, s)
        C[0] = cat_dict("bed", ox, oy, 0.60, 90, "rb5", s)
    elif i in (L["eat"], L["tower"]):                    # 사료 포대를 한 포대씩 오물오물
        t = tl if i == L["eat"] else tl + (shot_span(L["eat"])[1] - shot_span(L["eat"])[0])
        k = int((t - 0.15) // BAG_P) if t >= 0.15 else -1
        ph = ((t - 0.15) % BAG_P) if t >= 0.15 else 0.0
        chewing = 0.08 < ph < 0.44
        pose = ("eat_b" if int(t / 0.14) % 2 else "eat_a") if chewing else "eat_a"
        C[0] = cat_dict("liv", EAT_CAT[0], EAT_CAT[1], 0.0, -90, pose, S_G, roll=0.015 * math.sin(2 * math.pi * 3.5 * t))
    elif i == L["look"]:                                 # 선반 앞에서 고개를 쳐들고 올려다봄 (뒷모습)
        C[0] = cat_dict("liv", 2.6, 0.25, 0.0, 90, "sit_up", S_G, roll=0.01 * math.sin(2 * math.pi * 0.9 * tl))
    elif i == L["jump_s"]:                               # 원래 크기 고양이: 올려다보다 웅크렸다 선반으로 휙 → 의기양양
        p0, p1 = (2.8, 1.2, 0.0), (2.8, 2.52, SHELF_Z)
        pos, pit, T = leap_path(0.0, p0, p1, SMALL_APEX)
        t_j = 0.95
        if tl < 0.55:
            C[1] = cat_dict("liv", p0[0], p0[1], 0.0, 90, "sit_up", S_S)
        elif tl < t_j:
            C[1] = cat_dict("liv", p0[0], p0[1], 0.0, 90, "crouch", S_S)
        elif tl < t_j + T:
            pos, pit, T = leap_path(tl - t_j, p0, p1, SMALL_APEX)
            C[1] = cat_dict("liv", pos[0], pos[1], pos[2], 90, "leap", S_S, pitch=pit)
        elif tl < t_j + T + 0.18:
            C[1] = cat_dict("liv", p1[0], p1[1], p1[2], 90, "crouch", S_S)
        else:
            turn = ramp(tl, t_j + T + 0.5, t_j + T + 0.85)
            C[1] = cat_dict("liv", 2.8, 2.72, SHELF_Z, 90 - 180 * turn, "sit_blink" if 2.9 < tl < 3.05 else "sit", S_S)
    elif i == L["jump_g"]:                               # 거대 고양이: 웅크렸다 뛰어 보지만 선반에 못 닿고 쿵
        p0, p1 = (2.8, 0.45, 0.0), (2.8, 0.75, 0.0)
        t_j = 0.8
        if tl < 0.35:
            C[0] = cat_dict("liv", p0[0], p0[1], 0.0, 90, "stand", S_G)
        elif tl < t_j:
            C[0] = cat_dict("liv", p0[0], p0[1], 0.0, 90, "crouch", S_G)
        else:
            pos, pit, T = leap_path(tl - t_j, p0, p1, GIANT_APEX, lim=0.25)
            if tl < t_j + T:
                C[0] = cat_dict("liv", pos[0], pos[1], pos[2], 90, "leap", S_G, pitch=pit)
            elif tl < t_j + T + 0.45:
                C[0] = cat_dict("liv", p1[0], p1[1], 0.0, 90, "crouch", S_G)
            else:
                C[0] = cat_dict("liv", p1[0], p1[1], 0.0, 90, "sit", S_G)
    elif i == L["year"]:                                 # 높은 캣타워를 올려다보며 바닥에 앉음
        C[0] = cat_dict("year", 1.55, 1.3, 0.0, 0, "sit_up", S_G, roll=0.008 * math.sin(2 * math.pi * 0.7 * tl))
    elif i in (L["fall_a"], L["fall_b"]):                # 캣타워에서 사뿐히 뛰어내려 착지, 쓱 걸어감 (원래 크기 셋)
        t = tl if i == L["fall_a"] else tl + (shot_span(L["fall_a"])[1] - shot_span(L["fall_a"])[0])
        for n, (p0, dst, t_j, yaw0, spd, wd) in enumerate(FALL_SPECS):
            C[1 + n] = _small_cat_fall(p0, dst, t_j, t, yaw0, spd, wd)
    elif i == L["bars"]:                                 # 막대 뒤에서 앉아 지켜봄
        C[0] = cat_dict("year", 0.9, 1.5, 0.0, 180, "sit", S_G)
    elif i == L["stand"]:                                # 일어서려다 휘청, 폭삭 주저앉음
        C[0] = _wobble(tl)
    elif i == L["meow"]:
        op = 0.25 < tl < 0.95 and int((tl - 0.25) / 0.17) % 2 == 0
        C[0] = cat_dict("year", CAT_YR[0], CAT_YR[1], 0.0, 180, "sit_meow" if op else "sit", S_G)
    elif i == L["wants"]:
        op = any(t0 < tl < t0 + 0.55 and int((tl - t0) / 0.17) % 2 == 0 for t0 in (0.1, 0.85, 1.6))
        C[0] = cat_dict("year", CAT_YR[0], CAT_YR[1], 0.0, 180, "sit_meow" if op else "sit", S_G)
    elif i == L["hug"]:
        C[0] = cat_dict("year2", CAT_YR[0], CAT_YR[1], 0.0, 180, "sit_happy", S_G, roll=0.012 * math.sin(2 * math.pi * 0.8 * tl))
    elif i == L["face"]:
        blink = 0.9 < tl < 1.05 or 1.8 < tl < 1.95
        C[0] = cat_dict("year2", CAT_YR[0], CAT_YR[1], 0.0, 180, "sit_blink" if blink else "sit", S_G, roll=0.05 * math.sin(2 * math.pi * 0.35 * tl))
    elif i == L["quake"]:                                # 창밖을 내다보는 뒷모습
        C[0] = cat_dict("year", -0.4, 1.35, 0.0, 90, "sit", S_G)
    return C


def _small_cat_fall(p0, dst, t_j, t, yaw0, spd, wd):
    """원래 크기 고양이 하나: 발판에 앉아 있다가 t_j에 뛰어내려(폴짝) 사뿐히 착지 → 쓱 걸어감."""
    d0 = (dst[0], dst[1], 0.0)
    yaw_j = math.degrees(math.atan2(d0[1] - p0[1], d0[0] - p0[0]))
    pos, pit, T = leap_path(max(t - t_j, 0.0), p0, d0, p0[2] + 0.18)
    if t < t_j - 0.15:
        return cat_dict("year", p0[0], p0[1], p0[2], yaw0, "sit", S_S)
    if t < t_j:
        return cat_dict("year", p0[0], p0[1], p0[2], yaw_j, "crouch", S_S)
    if t < t_j + T:
        return cat_dict("year", pos[0], pos[1], pos[2], yaw_j, "leap", S_S, pitch=pit * 0.6)
    ta = t - (t_j + T)
    if ta < 0.2:                                         # 사뿐 착지 (납작했다 일어남)
        return cat_dict("year", d0[0], d0[1], 0.0, yaw_j, "crouch", S_S)
    tw = ta - 0.2
    n = min(tw, 1.3)
    ang = math.radians(wd)
    x, y = d0[0] + math.cos(ang) * spd * n, d0[1] + math.sin(ang) * spd * n
    if tw < 1.3:
        return cat_dict("year", x, y, 0.0, wd, walk_pose(tw, 0.2), S_S)
    return cat_dict("year", x, y, 0.0, -90, "sit_blink" if int(tw / 0.5) % 5 == 4 else "sit", S_S)


def _wobble(tl):
    """거대 고양이가 엎드렸다 일어서려다 후들후들 휘청이다 폭삭 주저앉음 (몸 옆으로 흔들림 = roll)."""
    x, y = -0.2, 1.1
    if tl < 0.35:
        return cat_dict("year", x, y, 0.0, 0, "lie0o", S_G)
    if tl < 0.85:
        return cat_dict("year", x, y, 0.0, 0, "crouch", S_G, roll=0.03 * math.sin(2 * math.pi * 4 * tl))
    if tl < 2.3:
        a = tl - 0.85
        amp = 0.05 + 0.10 * ramp(a, 0.3, 1.2)
        return cat_dict("year", x, y, 0.0, 0, "walk_a" if int(a / 0.1) % 2 == 0 else "walk_b", S_G,
                        roll=amp * math.sin(2 * math.pi * 1.7 * a), pitch=0.04 * math.sin(2 * math.pi * 1.1 * a))
    if tl < 2.5:
        return cat_dict("year", x, y, 0.0, 0, "crouch", S_G, roll=0.04)
    return cat_dict("year", x, y, 0.0, 0, "lie0o", S_G)



# ───────────────────────── 소품·효과 (일반 상자 F · 발광 상자 G) ─────────────────────────
# 상자 = (중심, 크기, 회전(라디안), 색) — 세트 좌표
WHITE = (0.97, 0.97, 0.95)
YEL = (1.0, 0.85, 0.2)
BAG_FULL, BAG_FLAT = (0.46, 0.72, 0.20), (0.46, 0.66, 0.11)
BAG_COL = [(0.95, 0.50, 0.15), (0.90, 0.35, 0.25), (0.95, 0.72, 0.20)]
BAG_LAB = (0.98, 0.93, 0.80)
KIBBLE = (0.55, 0.34, 0.18)
BAR_X, BAR_Y, BAR_U = (-2.5, -1.45), 0.9, 0.03      # 막대 두 개의 가운데 x · y · 눈금 하나의 높이(m)
BAR_C = ((0.12, 0.70, 0.32), (0.88, 0.18, 0.18))
SKY_BLD = [(-1.58, 0.17, 0.55), (-1.38, 0.22, 0.95), (-1.14, 0.18, 0.70), (-0.92, 0.26, 1.25), (-0.66, 0.16, 0.80), (-0.18, 0.2, 1.05),
           (0.08, 0.17, 0.62), (0.32, 0.24, 1.35), (0.58, 0.19, 0.85), (0.78, 0.14, 0.5)]
BOOK = (2.45, 2.88)                                   # 선반 끝에서 쓰러지는 책 (x, y)


def scale_value(tl):
    """체중계 숫자: 4에서 잠깐 있다가 200까지 굴러 올라감."""
    return int(round(lerp(4, 200, ramp(tl, 0.3, 1.25))))


def bag_items(t):
    """사료 포대들(탑 + 지금 먹는 포대). t = 먹기 시작(L8)부터 흐른 초."""
    out = []
    n = len(BAG_COL)
    for k in range(BAG_N):
        tau = t - (0.15 + BAG_P * k)
        if tau < 0:
            continue
        tx = TOWER_XY[0] + 0.04 * math.sin(k * 1.7)
        ty = TOWER_XY[1] + 0.03 * math.cos(k * 2.3)
        tz = 0.055 + 0.11 * k
        rz = 0.18 * math.sin(k * 2.1)
        col = BAG_COL[k % n]
        if tau < 0.08:                                    # 앞에 톡 나타남
            s = pop(tau, 0.08, 1.5)
            pos, size, th, r = (BAG_FRONT[0], BAG_FRONT[1], BAG_FULL[2] / 2 * s), tuple(q * s for q in BAG_FULL), BAG_FULL[2] * s, 0.0
        elif tau < 0.44:                                  # 먹으면서 납작해짐
            f = ramp(tau, 0.08, 0.44)
            th = lerp(BAG_FULL[2], BAG_FLAT[2], f)
            size = (BAG_FULL[0], lerp(BAG_FULL[1], BAG_FLAT[1], f), th)
            pos, r = (BAG_FRONT[0], BAG_FRONT[1], th / 2), 0.0
        elif tau < 0.60:                                  # 탑 위로 휙
            f = (tau - 0.44) / 0.16
            pos = (lerp(BAG_FRONT[0], tx, f), lerp(BAG_FRONT[1], ty, f), lerp(BAG_FLAT[2] / 2, tz, f) + 0.5 * 4 * f * (1 - f))
            size, th, r = BAG_FLAT, BAG_FLAT[2], rz * f + 1.2 * f * (1 - f)
        else:
            pos, size, th, r = (tx, ty, tz), BAG_FLAT, BAG_FLAT[2], rz
        out.append((pos, size, (0.0, 0.0, r), col))
        out.append(((pos[0], pos[1], pos[2] + th / 2 + 0.003), (size[0] * 0.66, size[1] * 0.45, 0.006), (0.0, 0.0, r), BAG_LAB))
    return out


def crumbs(t):
    """오물오물할 때 입가에서 튀는 사료 알갱이."""
    out = []
    k = int((t - 0.15) // BAG_P) if t >= 0.15 else -1
    if k < 0 or k >= BAG_N:
        return out
    ph = (t - 0.15) % BAG_P
    if not 0.08 < ph < 0.44:
        return out
    for m in range(4):
        age = ((ph - 0.08) * 3.0 + m * 0.25) % 1.0
        a = 2 * math.pi * (m / 4.0) + 0.9 * k
        out.append(((BAG_FRONT[0] + (0.25 + 0.2 * age) * math.cos(a), BAG_FRONT[1] - 0.15 + 0.18 * math.sin(a), 0.2 + 0.35 * age * (1 - age) * 2),
                    (0.04, 0.04, 0.04), (a, age * 4, 0), KIBBLE))
    return out


def zzz(tl, c, cam_loc):
    """쿨쿨 Z 셋: 머리 위로 오르며 커졌다 사라짐 (발광 5x7 점 글자, 카메라 쪽으로 돌림)."""
    out = []
    for k in range(3):
        age = (tl * 0.55 + k / 3.0) % 1.0
        cell = (0.028 + 0.040 * age) * (1 - age ** 4)
        if cell < 0.004:
            continue
        ctr = (c[0] + 0.15 + 0.5 * age, c[1] - 0.1, c[2] + 0.85 + 0.9 * age)
        right, up, rz = billboard(ctr, cam_loc)
        out += pix_runs("Z", ctr, cell, right, up, (0.75, 0.88, 1.0), rz)
    return out


def tape_items(tl):
    """바닥 줄자(노랑, 10cm 눈금) + 46cm·170cm 표시 기둥과 숫자."""
    G, F = [], []
    x0, y = TAPE_X0, TAPE_Y
    F.append(((x0 + 1.0, y, 0.011), (2.3, 0.14, 0.022), (0, 0, 0), (0.97, 0.86, 0.25)))
    for k in range(21):
        big = k % 5 == 0
        F.append(((x0 + 0.1 * k, y + 0.03, 0.0245), (0.012, 0.06 if big else 0.035, 0.004), (0, 0, 0), (0.10, 0.10, 0.12)))
    for xm, lab, t0 in ((0.46, "46", 0.0), (1.70, "170", 1.1)):
        s = pop(tl - t0, 0.3, 2.0) if t0 else 1.0
        if s <= 0:
            continue
        G.append(((x0 + xm, y, 0.72 * s), (0.025 * s, 0.025 * s, 1.44 * s), (0, 0, 0), YEL))
        G += seg_digits(lab, x0 + xm, 1.62, y, (1.0, 0.9, 0.3), w=0.12 * s, h=0.24 * s, t=0.04 * s, gap=0.18 * s)
    return F, G


def scale_items(tl):
    """커다란 체중계: 발판 + 기둥 + 숫자판(4 → 200)."""
    x0, x1, y0, y1 = SC_PLAT
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    F = [((cx, cy, 0.06), (x1 - x0, y1 - y0, 0.12), (0, 0, 0), (0.80, 0.82, 0.86)),
         ((cx, cy, 0.123), (x1 - x0 - 0.3, y1 - y0 - 0.2, 0.006), (0, 0, 0), (0.32, 0.34, 0.40)),
         ((cx, y1 + 0.25, 0.8), (0.1, 0.1, 1.6), (0, 0, 0), (0.55, 0.56, 0.60)),
         ((cx, y1 + 0.25, 1.78), (1.1, 0.16, 0.5), (0, 0, 0), (0.12, 0.12, 0.14))]
    v = scale_value(tl)
    col = (0.35, 1.0, 0.5) if v < 120 else (1.0, 0.6, 0.1)
    if tl > 1.3 and int((tl - 1.3) / 0.18) % 2 == 1:
        col = (1.0, 0.22, 0.12)
    G = seg_digits("%3d" % v, cx, 1.78, y1 + 0.25 - 0.09, col, w=0.17, h=0.32, t=0.045, gap=0.27)
    return F, G


def futon_items(tl, J):
    """요 + 베개 + (안고 온 이불 → 펴서 덮은 이불)."""
    fx, fy = 1.9, 1.3
    F = [((fx, fy, 0.06), (1.0, 2.0, 0.12), (0, 0, 0), (0.62, 0.72, 0.90)),
         ((fx, fy + 0.85, 0.16), (0.5, 0.32, 0.08), (0, 0, 0), WHITE)]
    bl = (0.92, 0.50, 0.52)
    if tl < 1.2 and J is not None:
        p = rel(J, 0.62, 0.0, 1.12)
        F.append((p, (0.34, 0.6, 0.26), (0, 0, 0), bl))
    else:
        s = pop(tl - 1.5, 0.35, 1.8) if tl >= 1.5 else 0.0
        if s > 0:
            F.append(((fx, fy - 0.12, 0.17 + 0.12 * (s - 1) if s > 1 else 0.17), (0.96 * min(s, 1.0), 1.2 * min(s, 1.0), 0.09), (0, 0, 0), bl))
    return F


def cart_items(J):
    """빈 쇼핑카트 (지수 앞에서 같이 움직임)."""
    if J is None:
        return []
    cx, cy = J["x"], J["y"] - 0.65
    g = (0.72, 0.74, 0.78)
    F = [((cx, cy, 0.40), (0.52, 0.82, 0.03), (0, 0, 0), g)]
    for sy in (-1, 1):
        F.append(((cx, cy + sy * 0.4, 0.56), (0.52, 0.03, 0.30), (0, 0, 0), g))
    for sx in (-1, 1):
        F.append(((cx + sx * 0.255, cy, 0.56), (0.03, 0.82, 0.30), (0, 0, 0), g))
        F.append(((cx + sx * 0.23, cy + 0.45, 0.70), (0.03, 0.03, 0.55), (0, 0, 0), (0.85, 0.2, 0.2)))
        for sy in (-1, 1):
            F.append(((cx + sx * 0.2, cy + sy * 0.32, 0.06), (0.05, 0.08, 0.12), (0, 0, 0), (0.15, 0.15, 0.17)))
    F.append(((cx, cy + 0.45, 0.97), (0.5, 0.04, 0.04), (0, 0, 0), (0.85, 0.2, 0.2)))
    return F


def bars_items(i, tl):
    """근력(14)·체중(50) 막대: 단면적과 부피 비례를 눈금 하나 4cm 높이로 (16번 줄에서 자람)."""
    k = ramp(tl, 0.2, 1.5) if i == LN["bars"] else 1.0
    F = [(((BAR_X[0] + BAR_X[1]) / 2, BAR_Y, 0.01), (1.8, 0.9, 0.02), (0, 0, 0), WHITE)]
    for x, n, c in ((BAR_X[0], 14, BAR_C[0]), (BAR_X[1], 50, BAR_C[1])):
        h = max(n * BAR_U * k, 0.01)
        F.append(((x, BAR_Y, 0.02 + h / 2), (0.6, 0.6, h), (0, 0, 0), c))
    return F


def sky_city(tl):
    """창 앞(유리 바로 앞)에 선 도시 건물 실루엣 상자 + 창턱 컵: 서서히 커지는 흔들림."""
    F = []
    a = 0.004 + 0.010 * ramp(tl, 0.4, 2.8)
    for k, (x, w, h) in enumerate(SKY_BLD):
        dx = a * math.sin(2 * math.pi * 7.5 * tl + 1.9 * k) * (1 + 0.3 * (k % 3))
        F.append(((x + dx, 2.95, 0.95 + h / 2), (w, 0.03, h), (0, 0, 0.012 * math.sin(2 * math.pi * 6.1 * tl + k)),
                  (0.40, 0.46, 0.58) if k % 2 else (0.52, 0.57, 0.68)))
    cup = 0.012 * math.sin(2 * math.pi * 13 * tl) * ramp(tl, 0.5, 2.5)
    F.append(((0.55 + cup, 2.84, 0.94 + 0.06), (0.07, 0.07, 0.12), (0, 0.0, cup * 8), (0.93, 0.93, 0.95)))
    return F


def props(i, tl, du, u, J, C, cam):
    """줄 i, 줄 시작 후 tl초의 소품. (F 일반 상자, G 발광 상자) 세트 좌표."""
    L = LN
    F, G = [], []
    st = cam["set"]
    if st == "liv":
        k = sofa_k(i, tl)
        F += sofa_parts(k)
        if i in (L["sofa"],) and tl > T_LAND:                                   # 주저앉는 다리 둘레 먼지 + 부러진 나뭇조각
            for lx, ly in ((SOFA["x0"] + 0.14, SOFA["y0"] + 0.14), (SOFA["x1"] - 0.14, SOFA["y0"] + 0.14),
                           (SOFA["x0"] + 0.14, SOFA["y1"] - 0.14), (SOFA["x1"] - 0.14, SOFA["y1"] - 0.14)):
                F += puffs((lx, ly, 0.0), tl, T_LAND, 6, 0.38, 0.9, 0.11)
            for m in range(4):
                p, hit = ballistic((SOFA["x0"] + 0.2 + 0.7 * m, SOFA["y0"] + 0.1, 0.12), (0.3 * (m - 1.5), -1.0 - 0.3 * m, 2.0 + 0.4 * m), tl - T_LAND)
                F.append((p, (0.05, 0.05, 0.05), (m, tl * 6, 0), DWOOD))
        if i >= L["eat"] and i != L["year"]:                                    # 선반 끝 책: 쿵 하면 떨어짐
            if i == L["jump_g"] and tl > T_THUD + 0.12:
                tt = tl - T_THUD - 0.12
                p, hit = ballistic((BOOK[0], BOOK[1], SHELF_Z + 0.13), (0.1, -0.7, 0.6), tt)
                F.append(((p[0], p[1], p[2] if not hit else 0.04), (0.05, 0.16, 0.26) if not hit else (0.05, 0.26, 0.16),
                          (min(tt * 5.0, 1.6) if not hit else 0.0, 0.0, 0.0), (0.9, 0.3, 0.3)))
            else:
                F.append(((BOOK[0], BOOK[1], SHELF_Z + 0.13), (0.05, 0.16, 0.26), (0, 0, 0), (0.9, 0.3, 0.3)))
    if i == L["ruler"]:
        f, g = tape_items(tl)
        F += f
        G += g
    elif i == L["scale"]:
        f, g = scale_items(tl)
        F += f
        G += g
    elif i in (L["nap"], L["futon"]):
        F += futon_items(tl, J) if i == L["futon"] else []
        G += zzz(tl, (0.0, 1.95, 0.6), (cam["loc"][0] - OFF["bed"][0], cam["loc"][1] - OFF["bed"][1], cam["loc"][2]))
    elif i == L["mart"]:
        F += cart_items(J)
    elif i in (L["eat"], L["tower"]):
        t = tl if i == L["eat"] else tl + (shot_span(L["eat"])[1] - shot_span(L["eat"])[0])
        F += bag_items(t) + crumbs(t)
    elif i == L["jump_g"] and tl > T_THUD:                                      # 쿵: 발밑 먼지
        F += puffs((2.8, 0.75 + 0.9, 0.0), tl, T_THUD, 12, 0.9, 0.7, 0.16)
    elif i in (L["fall_a"], L["fall_b"]):                                       # 사뿐 착지 먼지(아주 작게)
        t = tl if i == L["fall_a"] else tl + (shot_span(L["fall_a"])[1] - shot_span(L["fall_a"])[0])
        for p0, dst, t_j, yaw0, spd, wd in FALL_SPECS:
            T = leap_path(0.0, p0, (dst[0], dst[1], 0.0), p0[2] + 0.18)[2]
            F += puffs((dst[0], dst[1], 0.0), t, t_j + T, 5, 0.16, 0.35, 0.035)
    elif i in (L["bars"], L["stand"]):
        F += bars_items(i, tl)
        if i == L["stand"] and tl > 2.5:
            F += puffs((-0.2 + 0.0, 1.1 + 0.0, 0.0), tl, 2.5, 12, 1.1, 0.8, 0.17)
    elif i == L["quake"]:
        F += sky_city(tl)
    if i == L["hug"] and tl > 0.9:
        G += sparkles((-0.9, 1.55, 1.4), tl, 0.9, 12, 0.9, 1.6, 0.045, ((1.0, 0.85, 0.3), (1.0, 0.6, 0.75), (1.0, 1.0, 0.9)))
        G += sparkles((-1.0, 1.55, 1.2), tl, 1.7, 10, 0.8, 1.4, 0.04, ((1.0, 0.85, 0.3), (1.0, 0.6, 0.75), (1.0, 1.0, 0.9)))
    return F, G


# ── 말풍선 ──
N_B = 8


def bb(who, name, t0, ox, oz, cpx=8.0, **kw):
    """말풍선 한 개: 누구 머리 위('jisu'·'cat0') 또는 고정점((x,y,z)) · 그림 · 뜨는 때(줄 시작 후 초) · 꼬리 끝 위치(앵커에서 오른쪽·위로 몇 칸)
    · 한 칸이 화면에서 차지하는 픽셀 · life(초, 지나면 쏙 사라짐)."""
    return dict(who=who, name=name, t0=t0, off=(ox, oz), cpx=cpx, **kw)


def bub_specs(i, du):
    L = LN
    if i == L["wake"]:
        return [bb("jisu", "excl", 0.45 * du + 0.55, 0, 6, 9.0, life=1.0)]
    if i == L["look"]:
        return [bb("cat0", "dots3", 0.35, 0, 5, 9.0)]
    if i == L["bars"]:
        return [bb((BAR_X[0], BAR_Y, 14 * BAR_U + 0.06), "str", 1.35, 0, 3, 5.0), bb((BAR_X[1], BAR_Y, 50 * BAR_U + 0.06), "wgt", 1.5, 0, 3, 5.0)]
    if i == L["meow"]:
        return [bb("cat0", "meow", 0.25, 0, 5, 9.0)]
    if i == L["wants"]:
        return [bb("cat0", "hungry", 0.1, -42, 3, 5.5), bb("cat0", "play", 0.85, 36, 22, 5.5), bb("cat0", "stay", 1.6, -6, 44, 5.5)]
    if i == L["hug"]:
        return [bb("cat0", "heart", 0.9, 8, 8, 8.0), bb("cat0", "heart", 1.35, -26, 26, 7.0), bb("cat0", "heart", 1.8, 30, 40, 7.5)]
    if i == L["face"]:
        return [bb("cat0", "meow", 1.3, 0, 7, 15.0, life=1.3)]
    return []


def bubbles(i, tl, t, A, cam, du):
    """줄 i의 말풍선 → [(꼬리 끝 위치(세트 좌표), 회전, 크기 배율, 그림 번호)]. 카메라 쪽을 보게 돌리고 화면에서 한 칸이 일정 픽셀이 되게 키움."""
    o = OFF[cam["set"]]
    loc = (cam["loc"][0] - o[0], cam["loc"][1] - o[1], cam["loc"][2])
    right, up = cam_axes(cam["az"], cam["el"])
    out = []
    for k, sp in enumerate(bub_specs(i, du)):
        s0 = bub_scale(sp, tl)
        who = sp["who"]
        if s0 <= 0.0:
            continue
        if isinstance(who, tuple):
            a = who
        else:
            d = A.get(who)
            if d is None:
                continue
            a = head_pt(d) if who == "jisu" else cat_head_pt(d)
        cell = sp["cpx"] * math.dist(a, loc) / (cam["lens"] * 80.0)       # 한 칸의 월드 크기(m): 1920px 높이 / 센서 24mm = 80px/mm
        sx, sz = sp["off"]
        p = [a[j] + right[j] * sx * cell + up[j] * sz * cell for j in range(3)]
        p[2] += 0.01 * math.sin(2 * math.pi * 0.8 * t + 1.7 * k)
        roll = 0.035 * math.sin(2 * math.pi * 0.9 * t + k)
        s = cell / C0 * s0
        name = sp["name"]
        if name == "heart":
            s *= 1 + 0.09 * max(0.0, math.sin(2 * math.pi * 1.7 * t + k)) ** 2
        out.append(((p[0] + o[0], p[1] + o[1], p[2]), (roll, 0.0, math.atan2(loc[1] - p[1], loc[0] - p[0])), s, BUB_IX[name]))
    return out


# ───────────────────────── 한 프레임 ─────────────────────────
def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·고양이·소품·말풍선 점 배열, 카메라, 조명."""
    i = line_at(t)
    a, b = shot_span(i)
    du = max(b - a, 1e-3)
    tl = max(t - a, 0.0)
    u = min(tl / du, 1.0)
    cam = cam_pose(i, tl, u)
    J = jisu(i, tl, du)
    EX = extras(i, tl)
    C = cats(i, tl, du)
    A = {"jisu": J, "cat0": C[0]}
    if J is not None:
        J = dict(J, scale=S_J)
        A["jisu"] = J
    if C[0] is not None and cam["set"] != C[0]["set"]:
        A["cat0"] = None
    P, R, CO, C2, SC, PO = [], [], [], [], [], []
    people = [(J, JI_SH, JI_PA, 1, S_J)] + [(e, e["shirt"], e["pants"], e["hair"], 1.0) if e else (None, EX_SH[0], X.PANTS[0], 0, 1.0)
                                          for e in EX]
    for d, sh, pa, hair, s in people:
        CO.append(sh)
        C2.append(pa)
        if d is None:
            P.append((0.0, 0.0, 0.0))
            R.append((0.0, 0.0, 0.0))
            SC.append(0.0)
            PO.append(0)
            continue
        ox, oy = OFF[d["set"]]
        P.append((d["x"] + ox, d["y"] + oy, d["z"]))
        R.append((0.0, 0.0, math.radians(d["yaw"])))
        SC.append(s)
        PO.append(pose_index(d["pose"], hair))
    CP, CR, CS, CI = [], [], [], []
    for c in C:
        if c is None:
            CP.append((0.0, 0.0, 0.0))
            CR.append((0.0, 0.0, 0.0))
            CS.append(0.0)
            CI.append(0)
            continue
        ox, oy = OFF[c["set"]]
        CP.append((c["x"] + ox, c["y"] + oy, c["z"]))
        CR.append((c["roll"], c["pitch"], math.radians(c["yaw"])))
        CS.append(c["scale"])
        CI.append(CAT_IX[c["pose"]])
    F, G = props(i, tl, du, u, J, C, cam)
    o = OFF[cam["set"]]

    def shift(items):
        return [((p[0] + o[0], p[1] + o[1], p[2]), s, r, c) for p, s, r, c in items]
    bub = bubbles(i, tl, t, A, cam, du)
    return dict(i=i, tl=tl, u=u, set=cam["set"], cam=cam, A=A, P=P, R=R, CO=CO, C2=C2, SC=SC, PO=PO, CP=CP, CR=CR, CS=CS, CI=CI,
                fx=shift(F), glow=shift(G), BP=[q[0] for q in bub], BR=[q[1] for q in bub], BS=[q[2] for q in bub],
                BPO=[q[3] for q in bub], env=env(i, tl, du))


N_FX, N_GL = 170, 150


def _mat_glow(name, strength=3.0):
    """인스턴스 'col' 색으로 빛나는 재질 (숫자·글자·반짝임)."""
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
    v = X.Vox(35)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep35_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    mats = X.people_mats()
    protos = X.people_protos(ctx, mats)
    for lh in (False, True):
        for kind in KIND_ORDER:
            protos.append(K.proto(ctx, "ep35_p_%s_%d" % (kind, int(lh)), K.join_bms(_variant(kind, lh)), mats))
    people = K.instancer_multi(ctx, "ep35_people", protos, 1 + N_EX)
    # 고양이: 상자로 만든 원형 17종 (서기·걷기·웅크림·엎드림·몸 말기·앉기·하품·야옹·점프·먹기)
    cm = [K.mat_simple("ep35_c_fur", CAT_COLS[0], 0.9), K.mat_simple("ep35_c_stripe", CAT_COLS[1], 0.9),
          K.mat_simple("ep35_c_cream", CAT_COLS[2], 0.9), K.mat_simple("ep35_c_pink", CAT_COLS[3], 0.7),
          K.mat_simple("ep35_c_iris", CAT_COLS[4], 0.35, 0.0, CAT_COLS[4], 0.45), K.mat_simple("ep35_c_black", CAT_COLS[5], 0.4),
          K.mat_simple("ep35_c_white", CAT_COLS[6], 0.5), K.mat_simple("ep35_c_mouth", CAT_COLS[7], 0.6)]
    cat = K.instancer_multi(ctx, "ep35_cat", [K.proto(ctx, "ep35_cp_" + n, K.join_bms(_cat_parts(n)), cm) for n in CAT_ORDER], 4)
    # 말풍선: 그림마다 원형 하나(판+꼬리+도트 글자), 점마다 'pose'로 그림을 고름
    bmats = [K.mat_simple("ep35_m_bub", (0.97, 0.97, 0.95), 0.6, emit=(1.0, 1.0, 1.0), estr=0.45),
             K.mat_simple("ep35_m_bord", (0.07, 0.08, 0.13), 0.8)]
    for n, ch in enumerate(PAL_ORDER):
        col = tuple(float(c) for c in PAL[ch])
        bmats.append(K.mat_simple("ep35_m_ico_%d" % n, col, 0.5, emit=None if ch == "K" else col, estr=0.9))
    bub = K.instancer_multi(ctx, "ep35_bub", [K.proto(ctx, "ep35_p_bub_" + n, K.join_bms(_bub_parts(K, n)), bmats) for n in BUB_NAMES], N_B)
    try:
        bub.visible_shadow = False
    except AttributeError:
        pass
    cube = lambda: K.bm_cube(1, 1, 1)
    fx = K.instancer(ctx, "ep35_fx", K.proto(ctx, "ep35_p_fx", cube(), [K.mat_inst("ep35_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep35_glow", K.proto(ctx, "ep35_p_glow", cube(), [_mat_glow("ep35_m_glow")]), N_GL, vector_scale=True)

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
        for name, en in e["lt"].items():
            lights[name].data.energy = en
        K.set_points(people, S["P"], scale=S["SC"], rot=S["R"], col=np.array(S["CO"], np.float32),
                     colors={"col2": np.array(S["C2"], np.float32)}, pose=S["PO"])
        K.set_points(cat, S["CP"], scale=S["CS"], rot=S["CR"], pose=S["CI"])
        n = len(S["BS"])
        BP, BR, BS, BPO = (np.zeros((N_B, 3), np.float32), np.zeros((N_B, 3), np.float32), np.zeros(N_B, np.float32),
                           np.zeros(N_B, np.float32))
        if n:
            BP[:n], BR[:n], BS[:n], BPO[:n] = S["BP"][:N_B], S["BR"][:N_B], S["BS"][:N_B], S["BPO"][:N_B]
        K.set_points(bub, BP, scale=BS, rot=BR, pose=BPO)
        boxes(fx, S["fx"], N_FX)
        boxes(gl, S["glow"], N_GL)

    ctx.on_frame(upd)
