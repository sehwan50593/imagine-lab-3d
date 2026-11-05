"""EP48 만약에 사람이 곰처럼 겨울잠을 잔다면? (정보형 v2: 블록 캐릭터·내레이션·정보 카드·경과 배지)

가정: 상상 시나리오. 사람 몸이 곰처럼 바뀌는지는 알려지지 않음. 건강 조언 아님. 하루 2,000kcal·120일·대사 25%는 가정·계산값.
지후(보라 후드·주인공) · 곰 블록 1(귀여운 캐릭터) · 흰 가운 연구원 1명(12·19번) · 환자 1명(12번) · 시민 2명(5번) · 마다가스카르 여우원숭이 작은 상자 1(13~15번).

컷 흐름 (한 줄 = 한 컷, 괄호 = 세트. 7번 줄만 두 컷). 반전 카드(지방 31kg)는 훅 바로 뒤 3~6초:
0 훅(눈 오는 밤 원룸): 0.0초부터 눈보라 창가, 이불 뒤집어쓴 지후, 달력이 휙휙 넘어가고 침대 옆 투명 병의 지방 막대가 줄어듦, 카메라 빠른 push
→ 1 병 눈금 31kg에 노란 표시, 달력 120일(원룸) → 2 지후가 침대에 눕고 커튼이 닫히며 창틀에 눈이 쌓임(원룸) → 3 곰 굴 단면: 에너지 게이지 1→1/4, 체온계는 그대로
→ 4 심박 그래프 55→9로 완만하게(굴) → 5 눈 덮인 도시 거리: 쌓이는 눈·우체통·불 꺼진 창 한 칸(도시) → 6 130칸 달력과 빈 그릇(굴)
→ 7 지후 배의 꼬르륵 소리 파동(원룸) / 곰이 놀라 고개를 듦(굴) → 8 굴 밖에서 바위를 들어 올리는 곰, 근력 막대 78%(굴 앞)
→ 9 거울 속 알통 아이콘이 줄고 일어서다 비틀하는 지후(원룸) → 10 우편물·먼지가 쌓이고 창밖이 밝아지며 눈이 녹음(원룸)
→ 11 체온계 36.6→13.7(응급실) → 12 담요가 푸른색에서 따뜻한 색으로, 가운 입은 사람이 환히 웃음(응급실)
→ 13 나무 구멍 속 꼬리 통통한 여우원숭이 쌔근(밤 숲) → 14 반전: 옆에 사람 그림자와 '=' 표지(밤 숲) → 15 체온계 30°C 위·해, 계속 잠(낮 숲)
→ 16 소변 방울→근육 순환 고리(굴) → 17 봄, 냉장고 문을 열고 라면 줄 세우기(부엌) → 18 투명 병 31kg→7.8kg 눈금(노을 거실)
→ 19 연구원 고개 갸웃, 지후 어깨 으쓱, 병 위 물음표 → 20 이불 두르고 따뜻한 차(소파) → 21 달력 아이콘 질문(카메라 보며)
→ 22 달이 아주 조금 커지는 티저(다음 편 예고).
카드는 연달아 두 줄까지만(1 / 3·4 / 6 / 8 / 11 / 14 / 16 / 18 / 22), 사이마다 사건 줄. 카드 줄은 모두 2.2초 이상.

특수효과 (모두 블렌더 없이 numpy·math로 줄·시간에서 바로 계산):
지방 병 = 상자 틀+노란 막대(눈금 10kg마다), 훅에서 1→0.25, 1번 줄에서 0→1(31kg 표시 노란 막대·도트 '31'). 달력 = 세트 판 + 날짜 도트 글자(훅에서 0→120) + 넘어가는 종이 5장.
눈 = 발광 작은 상자(창밖)·흰 상자(거리), 창틀 눈은 막대가 자람. 커튼 = 두 폭이 창을 덮음. 곰 = 상자 14개(웅크림)·서 있는 곰(바위 들기)·고개 듦은 head_up 0~1.
에너지 게이지·체온계(3번) = 패널 + 발광 막대(게이지 1→1/4, 체온은 거의 제자리). 심박 그래프(4번) = 발광 상자 90개 파형, 박동 간격이 55→9번/분 비율로 벌어지고 숫자도 같이 줄어듦.
130칸 달력(6번) = 점 130개가 하나씩 켜짐+숫자. 근력 막대(8번) 100→78%. 순환 고리(16번) = 점 28개가 돌며 소변 방울↔근육 아이콘 사이를 이음.
거울 알통 아이콘(9번) = 상자 3개, 알통 높이가 줄어듦. 석 달 뒤(10번) = 우편물 쌓임·먼지 뭉치·창 발광판이 밝아짐·창틀 눈이 줄고 물방울.
체온계(11번) = 36.6→13.7로 수은 막대·구가 붉은색→푸른색, 도트 숫자. 응급실(12번) 담요 색이 푸름→따뜻함, 김 점. 여우원숭이(13~15번) = 상자 몸통·꼬리 3마디·반딧불·z 글자.
반전(14번) = 사람 그림자 상자 실루엣 + 노란 '=' 표지. 15번 체온계 20→31°C + 해(발광 구 둘). 냉장고(17번) 문이 경첩 둘레로 열리고 안쪽 불빛·식품, 라면 9개가 하나씩 톡.
노을 병(18번) = 31 눈금선·7.8 눈금선+도트 숫자. 달(22번) = 발광 구 둘(달+후광)이 천천히 커짐 + '+1cm' 도트.
번쩍 없음. 사람 겨울잠 때 눈 감은 얼굴 = 누운 자세는 voxel 원형(눈 감김), 누운 지후는 후드를 입히지 않은 같은 색 몸(jl)으로 두고 앉기·서기 때만 후드(jh)를 씀.

근거(설명란): ※ 이 영상은 '사람이 곰처럼 4개월 겨울잠을 잔다'는 가정의 상상 시나리오입니다. 지후·연구원·곰과 이야기 속 장면은 지어낸 것이고,
병·그래프·그림 속 크기와 비율은 이해를 돕는 연출입니다. 사람 몸이 곰처럼 바뀌는지는 알려진 바 없고 건강 조언이 아닙니다.
0·1줄 · F1 하루 2,000kcal로 120일(넉 달)이면 지방 약 31kg (계산값: 2,000 × 120 = 240,000kcal ÷ 7,700kcal/kg = 31.2kg; 지방 1kg ≈ 7,700kcal은 흔한 근사)
         · 계산 (Wishnofsky 1958 근사) [확인중]
3줄   · F2 흑곰은 겨울잠 때 대사를 기초대사의 25%로 낮추고 체온은 30~36°C 범위 유지(다일 주기로 변동) · Tøien 외 Science 331:906 (2011)
4줄   · F3 심박수 55회/분에서 최저 9회/분까지(평균 약 14회/분 보고도 있음, 5마리 연구) · Tøien 외 Science 2011
6줄   · F4 곰은 약 130일 동안 먹지도 마시지도 않고 소변도 보지 않는다 · Harlow(와이오밍대) 인용 bear.org·Scientific American 보도 [확인중]
8줄   · F5 겨울잠 뒤 곰은 근력이 약 22%만 줄고 단백질 손실 10~15%(연구마다 22~29%) · Harlow 연구 인용 보도(bear.org) [확인중]
9줄   · (연출용 한 줄, 사실 개수에 안 셈) 사람은 누워만 있으면 근육이 쉽게 빠진다 — 일반 서술, 구체 수치 안 씀 [확인중]
11·12줄 · F6 2000년 보고: 몸 온도 13.7°C·순환 정지 상태의 환자가 약 80분 얼음 아래 있다가 소생(이전 기록 14.4°C 어린이) · Gilbert 외 Lancet 355:375 (2000)
         · 카드는 '얼음 속 약 80분'만 표기 [확인중: 소생 시간 80분과 순환 정지 시간의 정확한 분리]
13~15줄 · F7 마다가스카르 난쟁이여우원숭이는 영장류로는 처음 확인된 겨울잠 동물, 기온 30°C 이상에서도 약 7개월 · Dausmann 외 Nature 429:825 (2004)
16줄  · F8 곰은 소변 속 요소의 약 98%를 재활용(사람은 약 10%)해 근육 단백질을 지킨다 · Harlow 연구 인용 NWF·보도 [확인중]
18줄  · F9 대사를 곰처럼 25%로 줄이면 같은 넉 달에 지방 약 7.8kg (계산값: 31.2kg × 0.25 = 7.8kg, 가정)
[확인중] (제작 전 오너 확인): ① F1 지방 1kg≈7,700kcal 원출처(Wishnofsky)와 인간의 실제 겨울잠 대사 변화는 알려진 바 없음
  ② F4·F5·F8 Harlow 연구 원논문(보도로만 확인, 일수는 110~130일로 다름) ③ F6 소생 시간 80분과 순환 정지 시간의 정확한 분리(문헌별 상이)
  ④ 침대 생활 중 근육 소실률(9번 일반 서술, 구체 수치 미사용).
분석 파일 수치 수정: 체온은 겨울잠 때 거의 안 내려감(30~36°C)으로 바로잡음. '인간 실험 연구 있음'은 근거 못 찾아 제외.
제목 카드는 0~1.45초에만(title_span을 짧게. TITLE_FAST라 0초부터 네 줄이 다 떠 있음). 0번 줄 훅 문장은 cap으로 같이 보임.
(다음 편 예고: 48편은 11-21 12:00 슬롯이라 49편은 같은 날 19:00 → '오늘 저녁 7시'. 슬롯이 바뀌면 22번 줄 say·cap과 CARDS 마지막 small을 고칠 것.)
"""
import json
import math
from pathlib import Path

import numpy as np

from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "pixe"
TITLE_FAST = True
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.15, 0.3, 1.6)
GAP = 0.12           # 줄 사이 기본 간격(초)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"room": (0, 0), "cave": (300, 0), "town": (600, 0), "er": (900, 0), "forest": (1200, 0), "kitchen": (1500, 0),
       "dusk": (1800, 0), "moon": (2100, 0)}
NAMES = ("hook", "bottle", "sleep", "metab", "heart", "week", "fast", "growl", "muscle", "mirror", "months", "cold", "doctor",
         "lemur", "twist", "heat", "urea", "spring", "seven", "unknown", "tea", "ask", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}

# say: 내레이션 / cap: 화면 자막(아라비아 숫자, 20자 이내) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
# cuts: 한 줄 안의 짧은 연속 컷 [(끝 u, shot), ...]  ease="out": 처음에 빨리 움직이고 천천히 멈춤(훅)
H_A = ("room", (-0.42, 3.6, 1.45), -90, 4, 4.8, 26, 0.82, 4, 0.08)
GR_R = ("room", (-1.0, 2.9, 0.9), -72, 20, 3.6, 28, 0.9, 6, 0.06)
GR_C = ("cave", (0.0, 3.3, 0.9), -90, 6, 5.2, 28, 0.9, 3, 0.06)
LINES = [
    dict(say="사람 겨울잠엔 지방 삼십 킬로가 필요해요", cap="사람 겨울잠엔 지방 30kg 필요", ease="out", shot=H_A),
    dict(say="하루 이천 칼로리로 넉 달이면 삼십일 킬로예요", cap="넉 달 겨울잠이면 지방 31kg",
         shot=("room", (0.25, 3.7, 0.85), -90, 4, 3.6, 28, 0.88, 3, 0.05)),
    dict(say="지후는 눈 오는 날 침대에 누워 잠들어요", cap="지후는 눈 오는 날 침대에 누워요",
         shot=("room", (-0.5, 3.2, 1.0), -86, 6, 5.4, 28, 0.9, 5, 0.04)),
    dict(say="곰은 대사를 사 분의 일로 낮춰요", cap="곰은 대사량을 25%로 낮춰요", gap=0.2,
         shot=("cave", (0.0, 4.6, 1.3), -90, 4, 6.8, 24, 0.92, 3, 0.04)),
    dict(say="심장은 일 분에 아홉 번까지 느려져요", cap="심장은 1분에 9번까지 느려져요",
         shot=("cave", (0.0, 5.6, 1.6), -90, 5, 7.0, 24, 0.9, -3, 0.04)),
    dict(say="일주일 뒤, 도시는 조용히 눈에 덮여요", cap="일주일 뒤, 도시가 눈에 덮여요",
         shot=("town", (0.9, 4.0, 1.7), -90, 3, 9.0, 26, 0.88, 3, -0.02)),
    dict(say="곰은 백삼십 일 동안 먹지도 마시지도 않아요", cap="곰은 130일 먹지도 마시지도 않아",
         shot=("cave", (0.0, 4.2, 1.0), -90, 4, 6.4, 26, 0.9, 3, 0.04)),
    dict(say="지후 배에선 꼬르륵 소리가 들려와요", cap="지후 배에서 꼬르륵 소리가 나요", cuts=[(0.55, GR_R), (1.0, GR_C)], shot=GR_R),
    dict(say="그런데 곰은 근력이 이십이 퍼센트만 줄어요", cap="곰은 근력이 22%만 줄어요",
         shot=("cave", (0.0, -2.6, 1.5), -90, 3, 5.8, 24, 0.9, 3, 0.04)),
    dict(say="사람은 누워만 있으면 근육이 쉽게 빠져요", cap="사람은 누우면 근육이 쉽게 빠져요",
         shot=("room", (-2.9, 3.0, 1.1), -88, 4, 6.0, 28, 0.9, -3, 0.05)),
    dict(say="석 달 뒤에도 지후는 침대 위에 있어요", cap="석 달 뒤에도 지후는 침대 위",
         shot=("room", (0.6, 3.4, 1.2), -90, 5, 7.0, 20, 0.9, 3, 0.04)),
    dict(say="사람 몸도 십삼 점 칠 도까지 식고 살아난 적 있어요", cap="몸 온도 13.7도에서 살아난 사례",
         shot=("er", (1.1, 3.3, 1.3), -90, 3, 7.5, 28, 0.9, 3, 0.04)),
    dict(say="얼음 아래 팔십 분 있던 사람이 지금은 의사예요", cap="얼음 아래 80분, 지금은 의사",
         shot=("er", (-0.7, 3.0, 1.0), -90, 4, 6.6, 28, 0.9, 3, 0.04)),
    dict(say="마다가스카르 나무 구멍에서 누가 잠들어 있어요", cap="나무 구멍에서 누가 잠들어요",
         shot=("forest", (-0.8, 4.6, 1.7), -90, 3, 5.0, 28, 0.82, 3, 0.04)),
    dict(say="영장류 중에도 일곱 달 겨울잠 자는 종이 있어요", cap="영장류도 7개월 겨울잠 자는 종",
         shot=("forest", (0.55, 4.8, 1.4), -90, 4, 7.0, 24, 0.9, 3, 0.04)),
    dict(say="그 여우원숭이는 삼십 도가 넘는 더위에도 잠들어요", cap="30도가 넘는 더위에도 잠들어요",
         shot=("forest", (0.0, 4.8, 1.6), -86, 4, 7.4, 26, 0.9, 3, 0.04)),
    dict(say="곰은 소변 성분을 재활용해 근육을 지켜요", cap="곰은 소변 성분을 재활용해요",
         shot=("cave", (0.0, 5.7, 1.7), -90, 4, 6.0, 26, 0.9, 3, 0.04)),
    dict(say="봄이 오면 지후는 냉장고부터 열어요", cap="봄이 오면 냉장고부터 열어요",
         shot=("kitchen", (0.9, 3.0, 1.1), -90, 9, 8.2, 24, 0.9, 3, 0.04)),
    dict(say="곰처럼 대사를 줄이면 지방 팔 킬로면 돼요", cap="대사 25%면 지방 약 8kg",
         shot=("dusk", (-0.4, 2.6, 1.3), -90, 4, 5.0, 28, 0.88, 3, 0.02)),
    dict(say="하지만 사람 몸이 그렇게 바뀌는지는 몰라요", cap="사람이 그렇게 되는지는 몰라요",
         shot=("dusk", (0.0, 2.8, 1.1), -90, 4, 6.4, 24, 0.9, 3, 0.04)),
    dict(say="겨울잠은 곰의 기술이고 이불은 사람의 기술이에요", cap="겨울잠은 곰의, 이불은 사람의 기술", gap=0.5,
         shot=("dusk", (0.4, 2.8, 0.95), -90, 4, 5.0, 24, 0.9, 3, 0.04)),
    dict(say="한 달만 겨울잠 잘 수 있다면 언제 잘래요?", cap="한 달만 겨울잠 잔다면 언제?",
         shot=("dusk", (0.5, 3.0, 1.2), -90, 3, 4.4, 28, 0.9, 0, 0.04)),
    dict(say="오늘 저녁 일곱 시, 달이 하루 일 센티미터씩 다가온다면?", cap="다음 편 · 달이 하루 1cm씩?",
         shot=("moon", (0.0, 60.0, 22.0), -90, -14, 45.0, 26, 0.9, 0, 0.0)),
]
assert len(LINES) == len(NAMES)
for _ln in LINES:
    _ln.setdefault("gap", GAP)
TITLE = [("만약에", "white"), ("사람이 곰처럼", "white"), ("겨울잠을 잔다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = LN["twist"]  # 14번: 영장류도 7개월 겨울잠 — 반전 카드 1번(지방 31kg)은 3~6초에 이미 나옴
CLOCK = [(1, "경과", "바로"), (5, "경과", "1주 뒤"), (9, "경과", "1달 뒤"), (10, "경과", "3달 뒤"), (14, "경과", "지금"), (17, None)]
CARDS = [
    dict(lines=(1, 1), big="지방 약 31kg", small="2,000kcal × 120일 ÷ 7,700kcal/kg(계산·가정)", color="red", src="계산"),
    dict(lines=(3, 3), big="대사 25%", small="흑곰 겨울잠 · 체온은 30~36°C 유지", color="cyan", src="Tøien · Science 2011"),
    dict(lines=(4, 4), big="55 → 9번/분", small="심박수가 평소에서 최저까지", color="cyan", src="Tøien · Science 2011"),
    dict(lines=(6, 6), big="130일 금식", small="먹지도 마시지도 소변도 보지 않음", color="orange", src="Harlow 인용 보도"),
    dict(lines=(8, 8), big="근력 −22%", small="5~7개월 겨울잠 뒤 흑곰(단백질 손실 10~15%)", color="green", src="Harlow 인용 보도"),
    dict(lines=(11, 11), big="13.7°C", small="체온 이 정도에서 소생한 2000년 보고 · 얼음 속 약 80분", color="yellow", src="Lancet 2000"),
    dict(lines=(14, 14), big="7개월 겨울잠", small="마다가스카르 난쟁이여우원숭이 · 30°C 넘는 날에도", color="green", src="Nature 2004"),
    dict(lines=(16, 16), big="요소 98% 재활용", small="곰 98% vs 사람 약 10%", color="cyan", src="Harlow · NWF 보도"),
    dict(lines=(18, 18), big="지방 약 7.8kg", small="31.2kg × 25%(계산·가정)", color="yellow", src="계산"),
    dict(lines=(22, 22), big="다음 편", small="오늘 저녁 7시 · 달이 하루 1cm씩 다가온다면?", color="cyan", src="구독하면 놓치지 않아요"),
]
for _ln in LINES:
    assert len(_ln.get("cap", _ln["say"])) <= 20, (_ln.get("cap", _ln["say"]), len(_ln.get("cap", _ln["say"])))
assert all(0 < c["lines"][0] <= c["lines"][1] < len(LINES) for c in CARDS)
assert len(CARDS) >= 5 and len([c for c in CLOCK if c[1] is not None]) >= 3
_cl = sorted({k for c in CARDS for k in range(c["lines"][0], c["lines"][1] + 1)})
assert all(not {k, k + 1, k + 2} <= set(_cl) for k in _cl), "카드 줄이 3개 이상 연속"

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep48_hibernate" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 66.0, "lines": [[0.15 + 2.8 * i, 2.8 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep48", "title": "만약에 사람이 곰처럼 겨울잠을 잔다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"key": "Eb", "mode": "lydian", "bpm": 96, "seed": 481, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.95, "bloom": 0.10, "bloom_thr": 1.4, "vignette": 0.14}
# 훅 한 줄에 컷이 하나뿐이라 따로 만지지 않음


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
    """[(시작, 끝, 글)] — 자막은 cap(아라비아 숫자·단위)을 씀. 0번 줄 훅 문장도 제목 카드와 함께 아래 자막으로 보임."""
    return [(s, e, LINES[k].get("cap", txt)) for k, (s, e, txt) in enumerate(TIMELINE["lines"])]


def title_span():
    """제목 카드가 떠 있는 때. TITLE_FAST라 0초부터 네 줄이 떠 있고 끝+0.35초에 사라지므로, 0번 줄 끝(≈3초)까지 두면
    0초와 2초 미리보기에 같은 카드가 두 번 보임 → 1.45초로 줄여 1.8초에는 없앰(제목 카드는 한 번만)."""
    s, e, _ = TIMELINE["lines"][0]
    return s, min(e, 1.45)


def simulate(build_dir):
    return {"dur": np.float32(DUR)}


def _shake_spec(i):
    """줄 i의 흔들림 [(시작 τ, 길이, 이동 세기 m, 각도 세기 도, 진동수 Hz, 종류)]. 'hold' 거의 일정, 'hit' 점점 잦아듦."""
    if i == LN["hook"]:
        return [(0.0, 99.0, 0.03, 0.0, 14.0, "hold")]
    if i == LN["growl"]:
        return [(0.1, 0.9, 0.04, 0.4, 12.0, "hit")]
    if i == LN["muscle"]:
        return [(0.4, 0.8, 0.03, 0.3, 11.0, "hit")]
    return ()


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
TRACK = {}                    # {(줄, 컷 번호): 함수(τ) → 목표점}  — 움직이는 것을 따라가는 카메라


def shake(i, tau, dist=4.0):
    """(이동 x, y, z m, 방위각 도, 고도각 도) — 멀리서 찍는 컷은 거리에 맞춰 이동량을 키움."""
    out = [0.0, 0.0, 0.0, 0.0, 0.0]
    sc = clamp(dist / 4.0, 1.0, 12.0)
    for t0, dur, amp, ang, hz, kind in _shake_spec(i):
        if tau < t0:
            continue
        if kind == "hit":
            k = (1.0 - clamp((tau - t0) / dur)) ** 2
        elif kind == "ramp":
            k = ramp(tau, t0, t0 + 1.5)
        else:
            k = 1.0 - 0.45 * clamp((tau - t0) / 4.0)
        w = 2 * math.pi * hz
        out[0] += amp * sc * k * math.sin(w * tau + 1.3)
        out[1] += 0.5 * amp * sc * k * math.sin(w * 0.83 * tau + 0.4)
        out[2] += amp * sc * k * math.sin(w * 1.21 * tau + 2.1)
        out[3] += ang * k * math.sin(w * 0.9 * tau + 0.7)
        out[4] += 0.7 * ang * k * math.sin(w * 1.1 * tau + 1.9)
    return out


def cut_at(i, u):
    """줄 i의 지금 컷: (shot, 컷 번호, 그 컷 안 진행도)."""
    cuts = LINES[i].get("cuts")
    if not cuts:
        return LINES[i]["shot"], 0, u
    u0 = 0.0
    for k, (ue, sh) in enumerate(cuts):
        if u <= ue or k == len(cuts) - 1:
            return sh, k, clamp((u - u0) / max(ue - u0, 1e-3))
        u0 = ue


def _basis(loc, tgt):
    fwd = tgt - loc
    fwd = fwd / np.linalg.norm(fwd)
    right = np.cross(fwd, (0.0, 0.0, 1.0))
    right = right / np.linalg.norm(right)
    return fwd, right, np.cross(right, fwd)


def cam_pose(i, tau, u, shaken=True):
    """줄 i, 줄 시작 후 τ초(진행도 u)의 카메라: dict(set, cut, tgt, az, el, dist, lens, loc, shift, fwd, right, up, fwd0, right0, up0) — 월드 좌표.
    CamRig.set과 같은 규칙. fwd0·right0·up0 = 흔들림을 뺀 방향(하늘 물체를 놓을 때 씀)."""
    shot, k, ul = cut_at(i, u)
    st_, tg, az, el, dist, lens, push, daz = shot[:8]
    shift = shot[8] if len(shot) > 8 else 0.0
    if LINES[i].get("ease") == "out":
        ul = 1.0 - (1.0 - ul) ** 2
    o = OFF[st_]
    tr = TRACK.get((i, k))
    tg = np.array(tr(tau) if tr else tg, float)
    a, e, dd = az + daz * ul, el + (shot[9] if len(shot) > 9 else 0.0) * ul, dist * (1 + (push - 1) * ul)
    tgt0 = np.array((tg[0] + o[0], tg[1] + o[1], tg[2]), float)

    def place(tgt, a_, e_):
        ea = math.radians(e_)
        return tgt + np.array((math.cos(ea) * math.cos(math.radians(a_)), math.cos(ea) * math.sin(math.radians(a_)), math.sin(ea))) * dd
    loc0 = place(tgt0, a, e)
    fwd0, right0, up0 = _basis(loc0, tgt0)
    tgt, a1, e1 = tgt0, a, e
    if shaken:
        sx, sy, sz, da, de = shake(i, tau, dd)
        tgt, a1, e1 = tgt0 + np.array((sx, sy, sz)), a + da, e + de
    loc = place(tgt, a1, e1)
    fwd, right, up = _basis(loc, tgt)
    return dict(set=st_, cut=k, tgt=tgt, az=a1, el=e1, dist=dd, lens=lens, loc=loc, shift=shift, fwd=fwd, right=right, up=up,
                fwd0=fwd0, right0=right0, up0=up0)


def project(cam, p):
    """월드 점 → (화면 x 0~1 왼쪽부터, y 0~1 위부터, 깊이). CamRig(센서 세로 24mm) + 렌즈 세로 이동(shift)과 같은 규칙."""
    d = np.asarray(p, float) - cam["loc"]
    z = float(d @ cam["fwd"])
    k = cam["lens"] / 24.0
    return 0.5 + (float(d @ cam["right"]) / z) * k / (1080.0 / 1920.0), 0.5 - (float(d @ cam["up"]) / z) * k + cam["shift"], z


def cam_of(t, shaken=True):
    i = line_at(t)
    a, b = shot_span(i)
    tau = max(t - a, 0.0)
    return cam_pose(i, tau, min(tau / max(b - a, 1e-3), 1.0), shaken)


_REF = {}


def ref_cam(i, tau):
    """줄 i의 τ초 카메라(흔들림 없음) — 하늘 물체의 방향을 화면 좌표로 정할 때의 기준."""
    key = (i, round(tau, 3))
    if key not in _REF:
        a, b = shot_span(i)
        _REF[key] = cam_pose(i, tau, min(tau / max(b - a, 1e-3), 1.0), False)
    return _REF[key]


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

# ───────────────────────── 색 · 도트 글자 ─────────────────────────
JH_SH, JH_PA = (0.58, 0.32, 0.80), (0.15, 0.18, 0.30)      # 지후: 보라 후드 · 짧은 머리 · 남색 바지
CO_SH, CO_PA = (0.93, 0.93, 0.91), (0.22, 0.24, 0.30)      # 연구원: 흰 가운 (extra='coat')
PT_SH, PT_PA = (0.55, 0.75, 0.85), (0.50, 0.60, 0.70)      # 환자복
EX1, EX2 = ((0.85, 0.30, 0.28), (0.20, 0.20, 0.22)), ((0.25, 0.45, 0.80), (0.35, 0.28, 0.20))
WOODC, DARKW = (0.62, 0.42, 0.25), (0.38, 0.25, 0.15)
BLANKET = (0.30, 0.42, 0.74)
FAT = (0.95, 0.80, 0.25)
BROWN, BROWN2, BROWN3 = (0.45, 0.30, 0.18), (0.38, 0.25, 0.15), (0.72, 0.56, 0.40)
INK = (0.04, 0.04, 0.06)
ROCK = (0.40, 0.36, 0.34)
GLASS = (0.70, 0.86, 0.95)
SNOWC = (0.78, 0.82, 0.90)
YEL, CYAN, ORA, GRN = (3.0, 2.5, 0.5), (0.5, 2.4, 3.0), (3.0, 1.5, 0.4), (0.6, 3.0, 0.9)
DIG.update({"z": ["###", "..#", ".#.", "#..", "###"], "c": ["###", "#..", "#..", "#..", "###"]})
N_FX, N_GL, N_OR, N_BL = 1100, 520, 12, 8


def wdig(G, rows, cx, y, cz, cell, col, k=1.0):
    """세트에 서 있는 도트 글자 (−y쪽을 보는 면, 가운데 맞춤): 칸 하나 = 발광 상자."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        G.b((cx + ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, y, cz + (h / 2.0 - r - 0.5) * cell * k),
            (((c1 - c + 1) - 0.06) * cell * k, 0.03, cell * 0.94 * k), col)


def lamp(v, x, y, h, name, energy):
    v.box(x - 0.06, x + 0.06, y - 0.06, y + 0.06, 0, h, (0.25, 0.26, 0.28))
    v.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, h, h + 0.12, (0.25, 0.26, 0.28))
    v.box(x - 0.16, x + 0.16, y - 0.16, y + 0.16, h - 0.05, h, (1.0, 0.85, 0.55), jit=0, glow=True)
    v.light(x, y, h - 0.3, energy, (1.0, 0.8, 0.55), 0.3, name)


# ───────────────────────── 세트 ─────────────────────────
def win(v, x0, x1, z0, z1, y, night=True, lights=14):
    """뒤벽(y=상수)의 창: 발광판 + 불빛 점 + 흰 창틀. voxel.window와 같되 틀 뒷면이 벽 면과 겹치지 않게 벽에서 0.02 띄움."""
    rs = v.rs
    base = (0.03, 0.05, 0.13) if night else (0.55, 0.75, 0.95)
    v.box(x0, x1, y - 0.02, y, z0, z1, base, jit=0, glow=True)
    for n in range(lights if night else 0):
        u = rs.uniform(x0 + 0.08, x1 - 0.12)
        w = rs.uniform(z0 + 0.05, z0 + (z1 - z0) * 0.55)
        c = (1.0, 0.78, 0.4) if rs.random() < 0.75 else (0.7, 0.85, 1.0)
        v.box(u, u + 0.06, y - 0.04 - 0.001 * n, y - 0.02 - 0.0004 * n, w, w + 0.06, c, jit=0, glow=True)     # 불빛 점끼리 앞면 높이를 조금씩 다르게
    fr, t, cx = (0.95, 0.95, 0.93), 0.06, (x0 + x1) / 2
    for a0, a1, c0, c1 in ((x0 - t, x1 + t, z0 - t, z0), (x0 - t, x1 + t, z1, z1 + t), (x0 - t, x0, z0, z1), (x1, x1 + t, z0, z1),
                           (cx - t / 2, cx + t / 2, z0, z1)):
        v.box(a0, a1, y - 0.08, y - 0.04, c0, c1, fr)


def _room(v):
    """눈 오는 밤 원룸. 뒤벽 y=4.6, 침대(x -1.9~-0.3, 머리 +y), 거울(왼쪽), 달력·병 자리(가운데), 창(오른쪽)."""
    v.floor(-4.6, 4.6, -6, 4.6, (0.58, 0.40, 0.26), 0.5, "wood")
    v.wall((-4.6, 4.6), (4.6, 4.6), 0, 3.4, (0.50, 0.52, 0.64), 0.5, face=-1)
    v.wall((-4.6, -3), (-4.6, 4.6), 0, 3.4, (0.52, 0.50, 0.60), 0.5, face=-1)
    v.wall((4.6, -3), (4.6, 4.6), 0, 3.4, (0.52, 0.50, 0.60), 0.5, face=1)
    v.box(-1.9, -0.3, 1.8, 4.4, 0, 0.32, WOODC)                                    # 침대 틀
    v.box(-1.87, -0.33, 1.83, 4.37, 0.32, 0.5, (0.66, 0.68, 0.76), jit=0.02)       # 요 (흰색 날림 방지로 회청색)
    v.box(-1.6, -0.6, 3.6, 4.2, 0.5, 0.63, (0.78, 0.80, 0.88), jit=0.01)           # 베개
    v.box(-1.92, -0.28, 4.38, 4.5, 0, 1.1, DARKW)                                   # 머리판
    win(v, 1.4, 3.4, 1.0, 2.5, 4.6, night=True, lights=14)
    v.box(-4.3, -2.7, 4.52, 4.58, 0.5, 2.3, (0.35, 0.25, 0.18))                      # 거울 틀
    v.box(-4.15, -2.85, 4.48, 4.52, 0.65, 2.15, (0.38, 0.52, 0.64), jit=0, glow=True)
    v.box(-0.15, 0.65, 4.52, 4.58, 1.35, 2.35, (0.70, 0.66, 0.55))                   # 달력 판
    v.box(-0.15, 0.65, 4.50, 4.52, 2.1, 2.35, (0.72, 0.24, 0.22), jit=0.01)
    v.box(-0.2, 0.7, 3.5, 4.2, 0.0, 0.02, (0.34, 0.26, 0.26), jit=0.0)              # 병 밑 깔개
    v.box(-3.6, -2.4, -2.0, 0.2, 0.0, 0.02, (0.40, 0.34, 0.34), jit=0.0)            # 거울 앞 매트
    v.light(0.0, 1.0, 2.9, 260, (1.0, 0.9, 0.75), 0.5, "ep48_rm0")
    v.light(-1.5, 3.0, 2.3, 170, (1.0, 0.85, 0.7), 0.4, "ep48_rm1")
    v.light(-3.0, 1.0, 2.6, 140, (0.95, 0.9, 0.85), 0.4, "ep48_rm2")


def _cave(v):
    """곰 굴 단면: 안쪽 y 0~6, 앞(y<0)은 눈 덮인 바깥. 뒤벽 y=6에 패널."""
    v.floor(-14, 14, -12, 0, (0.60, 0.66, 0.74), 1.0)
    v.floor(-3.4, 3.4, 0, 6, (0.40, 0.30, 0.22), 0.5)
    v.box(-14, -3.4, 0.0, 8, 0.02, 5.4, ROCK, jit=0.05)                              # 왼쪽 바위 덩어리 (안쪽 +x면이 굴 벽)
    v.wall((3.4, 0), (3.4, 6), 0.02, 3.6, (0.36, 0.32, 0.30), 0.5, face=1)          # 오른쪽 굴 벽
    v.box(3.45, 14, 0.0, 8, 0.02, 5.2, (0.44, 0.40, 0.38), jit=0.05)
    v.box(-3.4, 3.4, 6.0, 8.2, 0.02, 5.0, (0.34, 0.30, 0.28), jit=0.04)              # 뒤벽
    v.box(-3.4, 3.4, 0.0, 6.0, 3.6, 5.2, (0.42, 0.38, 0.36), jit=0.04, bottom=True)  # 천장
    v.box(-2.4, 2.4, 5.9, 6.0, 0.6, 3.0, (0.05, 0.07, 0.11), jit=0.0)                # 뒤벽 패널
    for z in (0.9, 1.35, 1.8, 2.25, 2.7):                                            # 패널 눈금선
        v.box(-2.3, 2.3, 5.86, 5.88, z, z + 0.02, (0.08, 0.28, 0.34), jit=0, glow=True)
    for k in range(5):                                                               # 바깥 눈 바위
        v.box(-9 + 4.5 * k, -7.5 + 4.5 * k, -9.5 - 1.0 * (k % 3), -8 - 1.0 * (k % 3), 0, 0.9 + 0.3 * (k % 2), (0.52, 0.56, 0.64), jit=0.05)
    v.light(0.0, 2.0, 3.0, 240, (1.0, 0.85, 0.65), 0.5, "ep48_cv0")
    v.light(0.0, 4.6, 2.8, 210, (1.0, 0.9, 0.75), 0.5, "ep48_cv1")


def _town(v):
    """눈 덮인 도시 거리: 길 y 0~6, 가게 줄 y≈7~8(조금씩 비껴), 뒤 건물 줄 y≈13."""
    v.floor(-18, 18, -6, 16, (0.62, 0.67, 0.76), 1.0)
    rs = v.rs
    xs = [-18, -11.5, -6, 0.5, 6.5, 12.5, 18]
    for k in range(len(xs) - 1):
        y = 7.0 + 0.55 * (k % 3)
        h = 6.5 + 2.2 * (k % 4)
        v.box(xs[k] - 0.1, xs[k + 1] + 0.1, y - 0.12, y + 4.5, h, h + 0.22, (0.80, 0.84, 0.90), jit=0.02)    # 지붕 눈
        X.storefront(v, xs[k], xs[k + 1], y, 4.5, h, [(0.9, 0.3, 0.3), (0.3, 0.6, 0.9), (0.9, 0.75, 0.3)][k % 3], face=-1, rs=rs, lit=0.9)
    v.box(-0.8, 0.18, 7.95, 8.0, 4.15, 5.55, (0.04, 0.05, 0.08), jit=0)             # 불 꺼진 창 한 칸 (지후 집)
    for k in range(5):                                                               # 뒤 건물 줄
        x0 = -20 + 9.5 * k
        v.box(x0, x0 + 8.0, 13.0 + 1.3 * (k % 3), 18, 0, 11.0 + 3.0 * (k % 2), (0.34 + 0.03 * (k % 3), 0.38, 0.48), jit=0.04)
    v.box(1.0, 1.55, 3.0, 3.4, 0.0, 1.0, (0.78, 0.22, 0.20))                         # 우체통
    v.box(1.15, 1.4, 3.1, 3.3, 1.0, 1.12, (0.62, 0.17, 0.16))
    v.box(1.18, 1.37, 3.06, 3.08, 0.55, 0.75, (0.96, 0.88, 0.5), jit=0, glow=True)
    lamp(v, -3.2, 5.2, 4.2, "ep48_tw0", 260)
    lamp(v, 5.4, 5.6, 4.2, "ep48_tw1", 260)
    v.light(0.0, 2.0, 4.0, 150, (0.85, 0.9, 1.0), 0.6, "ep48_tw2")


def _er(v):
    """설원 옆 응급실: 밝은 방. 뒤벽 y=5, 왼쪽 침대, 가운데 체온계, 오른쪽에 얼음 구멍 그림과 설원이 보이는 창."""
    v.floor(-5, 5, -6, 5, (0.70, 0.80, 0.82), 0.5, "check")
    v.wall((-5, 5), (5, 5), 0, 3.4, (0.56, 0.72, 0.76), 0.5, face=-1)
    v.wall((-5, -6), (-5, 5), 0, 3.4, (0.58, 0.72, 0.76), 0.5, face=-1)
    v.wall((5, -6), (5, 5), 0, 3.4, (0.58, 0.72, 0.76), 0.5, face=1)
    win(v, 3.3, 4.8, 1.0, 2.6, 5.0, night=False, lights=0)
    v.box(1.7, 3.0, 4.7, 4.9, 0.8, 1.95, (0.62, 0.82, 0.94))                          # 얼음판 그림
    v.box(2.05, 2.65, 4.62, 4.68, 1.05, 1.5, (0.05, 0.2, 0.4), jit=0)                 # 얼음 구멍
    v.box(-2.6, -0.8, 2.2, 4.2, 0.45, 0.6, (0.62, 0.64, 0.70))                       # 침대 틀
    v.box(-2.57, -0.83, 2.23, 4.17, 0.6, 0.72, (0.58, 0.70, 0.82), jit=0.02)
    for sx in (-2.5, -0.9):
        for sy in (2.3, 4.1):
            v.box(sx - 0.04, sx + 0.04, sy - 0.04, sy + 0.04, 0, 0.45, (0.5, 0.52, 0.56))
    v.light(0.0, 2.5, 3.2, 300, (1.0, 0.97, 0.9), 0.5, "ep48_er0")
    v.light(-2.0, 0.5, 2.8, 150, (1.0, 0.95, 0.9), 0.4, "ep48_er1")


def _forest(v):
    """마다가스카르 밤 숲: 굵은 나무 줄기(x -2.1~0.5, y 4.4~6.6)에 구멍(x -1.25~-0.35, z 1.1~2.1)."""
    v.floor(-16, 16, -6, 22, (0.17, 0.30, 0.19), 1.0)
    rs = v.rs
    for k in range(10):                                                              # 먼 언덕 (y를 비껴 놓음)
        x0 = -30 + 7 * k
        v.box(x0, x0 + 6, 24 + 2.3 * (k % 4), 30 + 2.3 * (k % 4), 0, 6 + float(rs.uniform(0, 5)), (0.12 + 0.02 * (k % 3), 0.24, 0.20), jit=0.05)
    v.box(-2.1, -1.25, 4.4, 6.6, 0, 4.4, (0.40, 0.28, 0.18))                          # 줄기 왼쪽
    v.box(-0.35, 0.5, 4.4, 6.6, 0, 4.4, (0.40, 0.28, 0.18))                           # 줄기 오른쪽
    v.box(-1.25, -0.35, 4.4, 6.6, 0, 1.1, (0.38, 0.26, 0.17))                         # 구멍 아래
    v.box(-1.25, -0.35, 4.4, 6.6, 2.1, 4.4, (0.38, 0.26, 0.17), bottom=True)          # 구멍 위
    v.box(-1.25, -0.35, 5.7, 6.6, 1.1, 2.1, (0.18, 0.12, 0.09))                       # 구멍 안쪽 벽
    v.box(-2.8, 1.2, 4.0, 5.2, 4.5, 5.7, (0.16, 0.34, 0.20), jit=0.06)                # 잎 덩어리
    v.box(-1.9, 2.0, 4.6, 6.0, 5.8, 6.7, (0.18, 0.38, 0.22), jit=0.06)
    for k, (x, y) in enumerate([(-6, 3), (5, 7), (-9, 9), (8, 3.5), (-4, 14), (3, 13)]):   # 작은 나무들
        X.tree(v, x, y, 3.0 + 0.5 * (k % 3))
    for k in range(6):                                                                # 풀 덤불
        v.box(-5 + 2.2 * k, -4.4 + 2.2 * k, 1.5 + 0.35 * (k % 3), 2.1 + 0.35 * (k % 3), 0, 0.35, (0.14, 0.34, 0.18), jit=0.08)
    v.light(-0.8, 3.4, 1.9, 70, (1.0, 0.82, 0.6), 0.3, "ep48_fo0")
    v.light(0.5, 1.0, 3.6, 220, (0.75, 0.85, 1.0), 0.6, "ep48_fo1")


def _kitchen(v):
    """봄 아침 부엌: 뒤벽 y=4.2, 가운데 조리대(x -0.6~1.2), 오른쪽 냉장고(x 1.4~2.4, y 2.55~3.55)."""
    v.floor(-4.4, 4.4, -6, 4.2, (0.80, 0.74, 0.60), 0.5, "check")
    v.wall((-4.4, 4.2), (4.4, 4.2), 0, 3.4, (0.76, 0.70, 0.52), 0.5, face=-1)
    v.wall((-4.4, -3), (-4.4, 4.2), 0, 3.4, (0.72, 0.68, 0.52), 0.5, face=-1)
    v.wall((4.4, -3), (4.4, 4.2), 0, 3.4, (0.72, 0.68, 0.52), 0.5, face=1)
    win(v, -0.7, 1.0, 1.1, 2.4, 4.2, night=False, lights=0)
    v.box(-0.6, 1.2, 3.0, 3.9, 0, 0.9, WOODC)                                        # 조리대
    v.box(-0.65, 1.25, 2.95, 3.95, 0.9, 0.96, (0.55, 0.55, 0.60), jit=0.02)
    v.box(1.4, 2.4, 2.55, 3.55, 0, 1.9, (0.60, 0.66, 0.72), jit=0.02)                 # 냉장고 몸통
    v.light(0.0, 1.5, 3.0, 270, (1.0, 0.95, 0.85), 0.5, "ep48_kt0")
    v.light(-2.0, 2.5, 2.6, 130, (1.0, 0.95, 0.85), 0.4, "ep48_kt1")


def _dusk(v):
    """노을 창가 거실: 뒤벽 y=4.2, 가운데 작은 탁자(병), 오른쪽 소파."""
    v.floor(-4.4, 4.4, -6, 4.2, (0.58, 0.40, 0.28), 0.5, "wood")
    v.wall((-4.4, 4.2), (4.4, 4.2), 0, 3.4, (0.62, 0.44, 0.44), 0.5, face=-1)
    v.wall((-4.4, -3), (-4.4, 4.2), 0, 3.4, (0.60, 0.44, 0.44), 0.5, face=-1)
    v.wall((4.4, -3), (4.4, 4.2), 0, 3.4, (0.60, 0.44, 0.44), 0.5, face=1)
    for z0, z1, c in ((1.2, 1.6, (1.0, 0.78, 0.38)), (1.6, 2.0, (1.0, 0.58, 0.30)), (2.0, 2.4, (0.88, 0.40, 0.34)), (2.4, 2.8, (0.50, 0.30, 0.48))):
        v.box(-0.6, 2.2, 4.17, 4.19, z0, z1, c, jit=0, glow=True)                      # 노을 하늘 띠
    v.box(0.3, 0.7, 4.14, 4.16, 1.3, 1.7, (1.0, 0.92, 0.55), jit=0, glow=True)         # 해
    for a0, a1, c0, c1 in ((-0.7, 2.3, 1.1, 1.2), (-0.7, 2.3, 2.8, 2.9), (-0.7, -0.6, 1.2, 2.8), (2.2, 2.3, 1.2, 2.8), (0.75, 0.85, 1.2, 2.8)):
        v.box(a0, a1, 4.10, 4.14, c0, c1, (0.82, 0.74, 0.62))
    v.box(-1.2, -0.4, 2.0, 2.8, 0.66, 0.72, WOODC)                                    # 탁자 윗판
    for sx in (-1.15, -0.45):
        for sy in (2.05, 2.75):
            v.box(sx - 0.03, sx + 0.03, sy - 0.03, sy + 0.03, 0, 0.66, DARKW)
    v.box(0.3, 1.9, 2.4, 3.4, 0, 0.45, (0.56, 0.30, 0.30), jit=0.03)                  # 소파 자리
    v.box(0.3, 1.9, 3.2, 3.4, 0.45, 1.05, (0.50, 0.26, 0.28), jit=0.03)               # 등받이
    v.box(0.2, 0.3, 2.4, 3.4, 0.45, 0.8, (0.50, 0.26, 0.28), jit=0.03)                # 팔걸이
    v.box(1.9, 2.0, 2.4, 3.4, 0.45, 0.8, (0.50, 0.26, 0.28), jit=0.03)
    v.light(0.0, 0.5, 2.9, 240, (1.0, 0.85, 0.65), 0.5, "ep48_dk0")
    v.light(1.2, 2.0, 2.4, 150, (1.0, 0.8, 0.6), 0.4, "ep48_dk1")


def _moon(v):
    """달 티저: 어두운 언덕 + 별 + 도시 실루엣."""
    v.floor(-90, 90, -40, 100, (0.08, 0.11, 0.18), 2.0)
    rs = v.rs
    for k in range(260):
        d = rs.normal(size=3)
        d = d / np.linalg.norm(d)
        d[2] = abs(d[2]) + 0.1
        r = float(rs.uniform(70, 100))
        s = float(rs.uniform(0.25, 0.6))
        c = ((0.95, 0.95, 1.0), (1.0, 0.9, 0.6), (0.6, 0.75, 1.0))[k % 3]
        x, y, z = d * r
        v.box(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z - s / 2, z + s / 2, c, jit=0, glow=True)
    for k in range(14):                                                              # 도시 실루엣 (y를 비껴 놓음)
        x0 = -42 + 6.5 * k
        v.box(x0, x0 + 5.0, 32 + 1.7 * (k % 4), 38 + 1.7 * (k % 4), 0, 3.0 + 2.2 * ((k * 5) % 4), (0.06, 0.08, 0.14), jit=0.04)
        if k % 2 == 0:
            v.box(x0 + 1.0, x0 + 1.5, 31.9 + 1.7 * (k % 4), 32.0 + 1.7 * (k % 4), 1.5 + 0.8 * (k % 3), 2.1 + 0.8 * (k % 3), (1.0, 0.78, 0.4), jit=0, glow=True)
    v.light(0.0, 10.0, 12.0, 200, (0.8, 0.88, 1.0), 1.0, "ep48_mn0")


def _sets():
    return (("room", _room), ("cave", _cave), ("town", _town), ("er", _er), ("forest", _forest), ("kitchen", _kitchen),
            ("dusk", _dusk), ("moon", _moon))


# ───────────────────────── 동적 소품 ─────────────────────────
def snow(G, t, n, x0, x1, y, z0, z1, spd, size=0.045, col=(1.6, 1.7, 2.0), sway=0.06, seed=0):
    """창밖 눈송이 n개 (발광 작은 상자, 구역 x0~x1·z0~z1, 높이 y 고정)."""
    for k in range(n):
        ph = (_h(k + 77 + seed) + spd * t * (0.6 + 0.8 * _h(k + 5 + seed))) % 1.0
        x = x0 + (x1 - x0) * _h(k + 11 + seed) + sway * math.sin(2.7 * t + k)
        G.b((x, y, z1 - (z1 - z0) * ph), (size, size, size), col)


def snow3d(F, t, n, x0, x1, y0, y1, z1, spd, size=0.07, seed=0):
    """거리에 내리는 눈 n개."""
    for k in range(n):
        ph = (_h(k + 31 + seed) + spd * t * (0.6 + 0.8 * _h(k + 9 + seed))) % 1.0
        F.b((x0 + (x1 - x0) * _h(k + 3 + seed) + 0.12 * math.sin(2.1 * t + k), y0 + (y1 - y0) * _h(k + 19 + seed), z1 * (1.0 - ph) + 0.05),
            (size, size, size), (0.88, 0.91, 0.97))


def bottle(F, cx, cy, z0, level):
    """투명 병(세로 1.15m = 31.2kg 눈금) + 노란 지방 막대. level 0~1 (1 = 31kg). 눈금은 10kg마다."""
    h = max(1.15 * level, 0.01)
    for sx in (-0.21, 0.21):
        for sy in (-0.21, 0.21):
            F.b((cx + sx, cy + sy, z0 + 0.06 + 0.65), (0.04, 0.04, 1.3), GLASS)
    F.b((cx, cy, z0 + 0.03), (0.5, 0.5, 0.06), (0.55, 0.58, 0.62))
    F.b((cx, cy, z0 + 1.38), (0.5, 0.5, 0.06), (0.55, 0.58, 0.62))
    F.b((cx, cy, z0 + 0.06 + h / 2), (0.34, 0.34, h), FAT)
    for kg in (10, 20, 30):
        F.b((cx + 0.3, cy - 0.2, z0 + 0.06 + 1.15 * kg / 31.2), (0.12, 0.02, 0.02), (0.16, 0.16, 0.2))


def calendar(F, G, day, t=0.0, flip=0.0):
    """뒤벽 달력(판은 세트): 날짜 숫자 + 넘어가는 종이 조각."""
    wdig(G, num_rows(str(int(day))), 0.25, 4.45, 1.72, 0.065, (0.14, 0.12, 0.18))
    if flip > 0.01:
        for k in range(5):
            p = (t * 4.0 * flip + k / 5.0) % 1.0
            sgn = 1 if k % 2 else -1
            F.c((0.25 + sgn * 0.7 * p, 4.3 - 0.5 * p, 1.85 - 1.2 * p), (0.5, 0.012, 0.4), (0.84, 0.80, 0.68), (0.9 * p * sgn, 0.0, 2.5 * p * sgn))


def cape(F):
    """앉은 지후를 감싼 이불 (보라 후드 위로 뒤집어쓴 모습)."""
    c = BLANKET
    F.b((-1.0, 3.60, 1.12), (1.1, 0.14, 1.1), c)
    F.b((-1.54, 3.28, 0.95), (0.12, 0.7, 0.8), c)
    F.b((-0.46, 3.28, 0.95), (0.12, 0.7, 0.8), c)
    F.b((-1.0, 3.4, 1.9), (0.9, 0.6, 0.12), c)
    F.b((-1.0, 2.7, 0.72), (0.95, 0.55, 0.22), (0.26, 0.38, 0.68))


def sill_snow(F, h):
    F.b((2.4, 4.35, 0.98 + h / 2), (1.9, 0.14, h), SNOWC)          # 창틀 위에 쌓이는 눈


def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    p = smooth(tau / dur)
    bottle(F, 0.25, 3.85, 0.0, lerp(1.0, 0.25, p))
    calendar(F, G, 120 * p, t, 1.0)
    cape(F)
    snow(G, t, 46, 1.45, 3.35, 4.5, 1.05, 2.45, 1.7)
    sill_snow(F, 0.05 + 0.1 * p)


def props_bottle(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    lv = smooth(tau / 0.9)
    bottle(F, 0.25, 3.85, 0.0, lv)
    zt = 0.06 + 1.15 * lv * 31.0 / 31.2
    if tau > 0.5:
        G.b((0.62, 3.6, zt), (0.3, 0.04, 0.05), YEL)
        wdig(G, num_rows("31"), 1.0, 3.58, zt, 0.075, YEL, pop(tau - 0.5, 0.3))
    calendar(F, G, 120, t, 0.0)
    G.b((0.25, 4.43, 1.45), (0.62, 0.02, 0.03), ORA)
    sill_snow(F, 0.15)
    snow(G, t, 24, 1.45, 3.35, 4.5, 1.05, 2.45, 0.9)


def props_sleep(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    c = smooth(tau / 1.8)
    for sgn, x0 in ((1, 1.4), (-1, 3.4)):                                # 커튼 두 폭이 창을 덮음
        w = 1.0 * smooth((tau - 0.4) / 1.8) + 0.05
        F.b((x0 + sgn * w / 2, 4.42, 1.75), (w, 0.1, 1.9), (0.66, 0.30, 0.36))
    if tau > 1.0:
        F.b((-1.0, 2.7, 1.0), (1.0, 1.4, 0.22 * pop(tau - 1.0, 0.3)), BLANKET)    # 누운 지후의 이불
    for k in range(3):                                                    # 잠꼬대 z
        if tau > 1.2 + 0.4 * k:
            q = tau - 1.2 - 0.4 * k
            wdig(G, DIG["z"], -0.9 + 0.25 * k, 3.5, 1.5 + 0.28 * k + 0.1 * math.sin(3 * q), 0.07 + 0.02 * k, (2.0, 2.2, 3.0), pop(q, 0.3))
    snow(G, t, 36, 1.45, 3.35, 4.5, 1.05, 2.45, 1.1)
    sill_snow(F, 0.15 + 0.12 * c)
    bottle(F, 0.25, 3.85, 0.0, 0.25 + 0.05 * c)
    calendar(F, G, 1, t, 0.0)


# ── 곰
def bear(F, cx, cy, t, k=1.0, head_up=0.0):
    """웅크린 곰(귀여운 블록): 몸 + 등 + 머리(앞 = −y) + 귀 + 주둥이 + 앞발. head_up 0~1이면 고개를 듦·눈을 뜸."""
    br = 1.0 + 0.035 * math.sin(2 * math.pi * t / 2.4)
    F.b((cx, cy, 0.48 * k), (1.7 * k, 1.3 * k, 0.9 * k * br), BROWN)
    F.b((cx - 0.15 * k, cy + 0.12 * k, 1.04 * k * br), (1.15 * k, 0.9 * k, 0.3 * k), BROWN2)
    hz = (0.46 + 0.42 * head_up) * k
    hx, hy = cx + 0.3 * k, cy - 0.78 * k
    F.b((hx, hy, hz), (0.7 * k, 0.62 * k, 0.58 * k), BROWN)
    for sx in (-0.25, 0.25):
        F.b((hx + sx * k, hy + 0.05 * k, hz + 0.34 * k), (0.17 * k, 0.15 * k, 0.17 * k), BROWN2)
    F.b((hx, hy - 0.36 * k, hz - 0.08 * k), (0.32 * k, 0.16 * k, 0.24 * k), BROWN3)
    F.b((hx, hy - 0.45 * k, hz - 0.01 * k), (0.12 * k, 0.04 * k, 0.08 * k), INK)
    for sx in (-0.17, 0.17):
        if head_up > 0.2:
            F.b((hx + sx * k, hy - 0.32 * k, hz + 0.1 * k), (0.12 * k, 0.04 * k, 0.12 * k), (0.95, 0.95, 0.95))
            F.b((hx + sx * k, hy - 0.345 * k, hz + 0.1 * k), (0.07 * k, 0.03 * k, 0.08 * k), INK)
        else:
            F.b((hx + sx * k, hy - 0.32 * k, hz + 0.1 * k), (0.15 * k, 0.03 * k, 0.03 * k), INK)
    for sx in (-0.3, 0.3):
        F.b((hx + sx * k, cy - 0.82 * k, 0.12 * k), (0.28 * k, 0.3 * k, 0.24 * k), BROWN2)


def bear_up(F, cx, cy, k, lift):
    """두 발로 서서 바위를 들어 올리는 곰 (lift 0~1)."""
    F.b((cx, cy, 0.9 * k), (1.0 * k, 0.7 * k, 1.1 * k), BROWN)
    F.b((cx, cy - 0.37 * k, 0.8 * k), (0.62 * k, 0.04 * k, 0.7 * k), BROWN3)
    for sx in (-0.28, 0.28):
        F.b((cx + sx * k, cy, 0.25 * k), (0.36 * k, 0.4 * k, 0.5 * k), BROWN2)
    F.b((cx, cy - 0.05 * k, 1.78 * k), (0.62 * k, 0.56 * k, 0.5 * k), BROWN)
    for sx in (-0.24, 0.24):
        F.b((cx + sx * k, cy, 2.05 * k), (0.16 * k, 0.14 * k, 0.16 * k), BROWN2)
    F.b((cx, cy - 0.35 * k, 1.7 * k), (0.28 * k, 0.14 * k, 0.2 * k), BROWN3)
    F.b((cx, cy - 0.43 * k, 1.75 * k), (0.1 * k, 0.04 * k, 0.07 * k), INK)
    for sx in (-0.15, 0.15):
        F.b((cx + sx * k, cy - 0.31 * k, 1.84 * k), (0.12 * k, 0.04 * k, 0.1 * k), (0.95, 0.95, 0.95))
        F.b((cx + sx * k, cy - 0.335 * k, 1.84 * k), (0.07 * k, 0.03 * k, 0.07 * k), INK)
    for sx in (-0.42, 0.42):
        F.b((cx + sx * k, cy, (1.55 + 0.35 * lift) * k), (0.22 * k, 0.24 * k, (0.7 + 0.2 * lift) * k), BROWN2)
    rz = (1.9 + 0.35 * lift) * k
    F.b((cx, cy, rz + 0.55 * k), (1.1 * k, 0.9 * k, 0.8 * k), (0.48, 0.50, 0.56))
    F.b((cx - 0.15 * k, cy - 0.46 * k, rz + 0.65 * k), (0.4 * k, 0.04 * k, 0.3 * k), (0.58, 0.60, 0.66))


def ecg(G, p, t, zc=1.8, y=5.84):
    """심박 그래프: 박동 사이가 55 → 9로 넓어지며 흐름. 선 하나 = 발광 상자 90개."""
    hr = lerp(55.0, 9.0, smooth(p))
    sp = min(0.5 * 60.0 / hr, 2.6)
    x0, x1, N = -2.0, 2.0, 90
    scroll = (t * 0.55) % sp
    for k in range(N):
        x = x0 + (x1 - x0) * k / (N - 1)
        q = ((x - x0 + scroll) % sp) - 0.3 * sp
        a = math.exp(-(q / 0.07) ** 2) * 0.55 - math.exp(-((q - 0.17) / 0.06) ** 2) * 0.18
        G.b((x, y, zc + a), (0.05, 0.03, 0.05), GRN)
    return int(round(hr))


def props_metab(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bear(F, 0.0, 3.2, t)
    lv = lerp(1.0, 0.25, smooth(tau / (dur * 0.8)))                      # 에너지 게이지: 1 → 1/4
    F.b((-1.45, 5.7, 1.7), (0.55, 0.18, 2.2), (0.1, 0.12, 0.16))
    G.b((-1.45, 5.58, 0.7 + lv * 0.95), (0.34, 0.04, lv * 1.9), ORA if lv > 0.4 else YEL)
    G.b((-1.45, 5.56, 0.7 + 0.25 * 1.9), (0.46, 0.03, 0.03), (2.0, 2.0, 2.2))      # 25% 눈금
    wdig(G, num_rows("25%"), -1.45, 5.56, 2.95, 0.1, YEL if lv < 0.5 else ORA, pop(tau - 0.2, 0.3))
    F.b((1.45, 5.7, 1.7), (0.5, 0.18, 2.2), (0.1, 0.12, 0.16))              # 체온계: 거의 안 변함
    mv = 0.66 + 0.015 * math.sin(2 * math.pi * t / 1.6)
    G.b((1.45, 5.58, 0.7 + mv * 0.95), (0.2, 0.04, mv * 1.9), (3.0, 0.5, 0.45))
    G.b((1.74, 5.56, 0.7 + 0.66 * 1.9), (0.08, 0.03, 0.12 * 1.9), CYAN)           # 30~36°C 범위 띠


def props_heart(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bear(F, 0.0, 3.2, t)
    hr = ecg(G, tau / (dur * 0.85), t)
    wdig(G, num_rows(str(hr)), -1.45, 5.82, 2.55, 0.14, YEL if hr > 20 else ORA)


def props_fast(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bear(F, -0.4, 3.4, t)
    n = int(130 * smooth(tau / (dur * 0.85)))
    for q in range(130):                                                  # 130칸 달력: 하루 = 점 하나
        if q < n:
            G.b((-1.75 + 0.12 * (q % 13), 5.84, 1.15 + 0.19 * (q // 13)), (0.08, 0.03, 0.14), ORA)
    wdig(G, num_rows(str(n)), 1.05, 5.84, 1.85, 0.15, YEL)
    for bx in (1.5, 2.5):                                                 # 빈 밥그릇 · 빈 물그릇
        F.b((bx, 2.2, 0.1), (0.7, 0.7, 0.2), (0.55, 0.55, 0.60))
        F.b((bx, 2.2, 0.22), (0.5, 0.5, 0.03), (0.30, 0.30, 0.34))
    wdig(G, DIG["?"], 2.0, 2.2, 0.75 + 0.05 * math.sin(2 * math.pi * t / 1.2), 0.1, (2.0, 2.0, 2.4), pop(tau - 0.6, 0.3))


def props_growl(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    if cam["set"] == "room":
        F.b((-1.0, 2.7, 1.0), (1.0, 1.4, 0.22), BLANKET)
        for r in (0.5, 0.85, 1.2):                                        # 꼬르륵 소리 파동 (배 위로 퍼짐)
            w = max(0.0, math.sin(2 * math.pi * (t * 2.0 - r * 0.8)))
            for a in range(-60, 61, 15):
                ra = math.radians(a)
                G.b((-1.0 + r * math.sin(ra) * 0.9, 2.9, 1.25 + r * math.cos(ra) * 0.6), (0.1, 0.05, 0.1), (2.8 * (0.2 + w), 2.5 * (0.2 + w), 1.0))
        bottle(F, 0.25, 3.85, 0.0, 0.25)
        sill_snow(F, 0.15)
    else:
        bear(F, 0.0, 3.2, t, head_up=smooth((tau - 0.2) / 0.5))
        wdig(G, DIG["!"], 0.3, 2.35, 1.75 + 0.04 * math.sin(10 * t), 0.14, YEL, pop(tau - 0.3, 0.3))


def props_muscle(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bear_up(F, 0.0, -2.6, 0.95, smooth(tau / 1.4))
    F.b((1.25, -2.6, 1.0), (0.4, 0.2, 2.0), (0.14, 0.16, 0.20))
    h = 1.96 * lerp(1.0, 0.78, smooth(tau / 1.2))                          # 근력 막대 100% → 78%
    G.b((1.25, -2.72, 0.02 + h / 2), (0.3, 0.04, h), GRN)
    wdig(G, num_rows("78%"), 1.25, -2.72, 2.3, 0.08, GRN, pop(tau - 0.5, 0.3))


def props_urea(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bear(F, 0.0, 3.2, t)
    cz, R = 1.85, 1.0
    for q in range(28):
        a = 2 * math.pi * q / 28 + 1.3 * t
        m = 0.5 + 0.5 * math.cos(a)
        G.b((R * math.cos(a), 5.84, cz + R * math.sin(a)), (0.1, 0.03, 0.1), (0.5 + 2.5 * m, 1.8, 3.0 - 2.4 * m))
    s = pop(tau - 0.3, 0.3)
    F.b((-R, 5.72, cz), (0.32 * s, 0.1, 0.32 * s), (0.25, 0.55, 0.95))                 # 소변 방울
    F.b((-R, 5.72, cz + 0.22 * s), (0.14 * s, 0.1, 0.14 * s), (0.25, 0.55, 0.95))
    F.b((R, 5.72, cz - 0.05), (0.5 * s, 0.1, 0.18 * s), (0.88, 0.50, 0.30))            # 근육(굽힌 팔)
    F.b((R + 0.05, 5.72, cz + 0.1), (0.28 * s, 0.1, 0.28 * s), (0.95, 0.60, 0.38))
    wdig(G, num_rows("98"), 0.0, 5.82, cz, 0.13, YEL, pop(tau - 0.5, 0.3))


# ── 도시 (1주 뒤)
def props_week(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    f = smooth(tau / (dur * 0.9))
    snow3d(F, t, 90, -9, 9, 0.5, 9, 6.5, 0.6)
    h = 0.08 + 0.22 * f
    F.b((1.275, 3.2, 1.0 + h / 2), (0.7, 0.55, h), (0.82, 0.86, 0.92))              # 우체통 위 눈
    for dx, dy, w in ((-2.0, 3.8, 3.0), (2.8, 4.5, 3.6), (-5.0, 5.5, 3.4)):           # 길 위 눈더미
        F.b((dx, dy, (0.03 + 0.25 * f) / 2), (w, 1.6, 0.03 + 0.25 * f), (0.74, 0.79, 0.88))
    F.b((-3.2, 5.2, 4.34 + (0.04 + 0.12 * f) / 2), (0.62, 0.62, 0.04 + 0.12 * f), (0.82, 0.86, 0.92))   # 가로등 머리 눈


# ── 침대 방: 근육 · 석 달
def props_mirror(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    p = smooth((tau - 0.3) / (dur * 0.7))
    bump = 0.30 * (1.0 - 0.75 * p)                                          # 거울 속 팔 아이콘: 알통이 줄어듦
    F.b((-3.5, 4.4, 1.35), (0.7, 0.07, 0.17), (0.88, 0.66, 0.50))
    F.b((-3.62, 4.4, 1.35 + 0.085 + bump / 2), (0.32, 0.07, bump), (0.92, 0.70, 0.54))
    F.b((-3.12, 4.4, 1.42), (0.2, 0.07, 0.22), (0.90, 0.68, 0.52))
    G.b((-3.5, 4.43, 0.92), (0.35, 0.03, 0.06 + 0.04 * math.sin(6 * t)), (3.0, 0.4, 0.35))   # 빨간 아래 표시


def props_months(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    f = ramp(tau, 0.2, dur * 0.9)
    for k in range(int(7 * smooth(tau / (dur * 0.8)))):
        F.c((0.9 + 0.04 * math.sin(k * 2.0), 1.1, 0.03 + 0.035 * k), (0.42, 0.28, 0.03), (0.92 - 0.04 * (k % 2), 0.86, 0.72), (0.0, 0.0, 0.25 * math.sin(k * 3.1)))
    for k in range(9):                                                      # 먼지 뭉치
        if f > k / 10.0:
            s = 0.14 + 0.1 * _h(k + 40)
            F.b((-3.6 + 7.0 * _h(k + 50), -1.5 + 4.8 * _h(k + 60), s / 2), (s, s, s * 0.7), (0.46, 0.44, 0.42))
    G.b((2.4, 4.47, 1.75), (2.0, 0.02, 1.5), (0.03 + 0.52 * f, 0.05 + 0.70 * f, 0.13 + 0.82 * f))   # 창밖이 밝아짐
    sill_snow(F, 0.02 + 0.13 * (1.0 - f))
    if f > 0.3:
        for k in range(3):                                                  # 처마 물방울
            q = (t * 1.6 + 0.3 * k) % 1.0
            G.b((1.9 + 0.5 * k, 4.42, 2.4 - 1.3 * q), (0.04, 0.04, 0.08), (0.7, 1.6, 3.0))
    calendar(F, G, 90, t, 0.0)
    bottle(F, 0.25, 3.85, 0.0, 0.2)
    F.b((-1.0, 2.7, 1.0), (1.0, 1.4, 0.22), BLANKET)


# ── 응급실
def props_cold(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    T = lerp(36.6, 13.7, smooth(tau / (dur * 0.7)))
    lvl = 0.3 + 1.9 * (T / 42.0)
    cx, cy = 0.3, 3.3
    cold = 1.0 - clamp((T - 13.7) / 22.9)
    col = (0.9 - 0.7 * cold, 0.15 + 0.45 * cold, 0.12 + 0.8 * cold)
    F.b((cx, cy, 1.25), (0.2, 0.16, 2.1), (0.82, 0.88, 0.92))
    F.b((cx, cy, 0.18), (0.45, 0.4, 0.06), (0.55, 0.58, 0.62))
    BL.orb((cx, cy - 0.05, 0.3), 0.34, col)
    F.b((cx, cy - 0.1, (0.3 + lvl) / 2), (0.09, 0.07, lvl - 0.3), col)
    for kk in range(5):
        F.b((cx + 0.17, cy - 0.1, 0.3 + 1.9 * (10 * kk) / 42.0), (0.1, 0.03, 0.025), (0.16, 0.16, 0.2))
    wdig(G, num_rows("%.1f" % T), cx, cy - 0.3, 2.7, 0.13, (3.0, 0.8, 0.5) if cold < 0.5 else (0.5, 1.6, 3.0))


def props_doctor(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    f = ramp(tau, 0.2, dur * 0.9)
    F.b((-1.7, 3.1, 1.02), (0.95, 1.5, 0.22), (0.45 + 0.4 * f, 0.55 + 0.1 * f, 0.85 - 0.45 * f))   # 푸른 담요 → 따뜻한 색
    if f > 0.15:
        for k in range(5):                                                  # 김이 모락모락
            q = (t * 0.7 + 0.2 * k) % 1.0
            G.b((-1.9 + 0.15 * k + 0.05 * math.sin(4 * t + k), 3.1, 1.25 + 0.7 * q), (0.06, 0.06, 0.06), (2.0, 1.4, 0.9))
    s = pop(tau - 0.8, 0.3)                                                 # 벽의 빨간 십자 표지
    F.b((0.9, 4.9, 2.2), (0.6 * s, 0.05, 0.6 * s), (0.9, 0.3, 0.3))
    G.b((0.9, 4.85, 2.2), (0.36 * s, 0.03, 0.1 * s), (3.0, 3.0, 3.0))
    G.b((0.9, 4.85, 2.2), (0.1 * s, 0.03, 0.36 * s), (3.0, 3.0, 3.0))


# ── 숲 · 여우원숭이
def lemur(F, t):
    br = 1.0 + 0.05 * math.sin(2 * math.pi * t / 1.8)
    cx, cy, z0 = -0.8, 5.1, 1.1
    F.b((cx, cy, z0 + 0.22 * br), (0.46, 0.34, 0.4 * br), (0.55, 0.50, 0.48))
    F.b((cx, cy - 0.2, z0 + 0.42), (0.34, 0.3, 0.3), (0.62, 0.57, 0.54))
    F.b((cx, cy - 0.4, z0 + 0.38), (0.12, 0.1, 0.1), INK)
    for sx in (-0.1, 0.1):
        F.b((cx + sx, cy - 0.355, z0 + 0.5), (0.1, 0.03, 0.025), INK)
        F.b((cx + sx * 2.1, cy - 0.15, z0 + 0.62), (0.1, 0.1, 0.12), (0.45, 0.40, 0.40))
    for z in (0.14, 0.26, 0.38):                                          # 꼬리에 지방이 오동통
        F.b((cx + 0.28, cy - 0.04, z0 + z), (0.3, 0.28, 0.14), (0.52 + 0.1 * (z > 0.3), 0.38, 0.28))


def fireflies(G, t):
    for k in range(10):
        ph = t * 0.25 + _h(k + 90)
        G.b((-3.5 + 6.0 * _h(k + 91) + 0.3 * math.sin(2 * ph * 6.28 + k), 3.4 + 0.8 * math.sin(ph * 6.28 + k), 0.7 + 1.9 * _h(k + 92)),
            (0.045, 0.045, 0.045), (2.8, 3.0, 0.8))


def props_lemur(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    lemur(F, t)
    for k in range(3):
        q = (t * 0.45 + k / 3.0) % 1.0
        wdig(G, DIG["z"], -0.2 + 0.25 * k + 0.1 * q, 4.3, 2.3 + 0.9 * q, 0.06 + 0.03 * q, (2.0, 2.2, 3.0), 1.0 - ramp(q, 0.8, 1.0))
    fireflies(G, t)


def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    lemur(F, t)
    s = pop(tau - 0.35, 0.35)
    cx = 1.85
    dk = (0.05, 0.07, 0.14)
    for sx in (-0.12, 0.12):
        F.b((cx + sx, 4.6, 0.4 * s), (0.2, 0.2, 0.8 * s), dk)
    F.b((cx, 4.6, 1.15 * s), (0.4, 0.26, 0.7 * s), dk)
    F.b((cx, 4.6, 1.72 * s), (0.3, 0.3, 0.3 * s), dk)
    for sx in (-0.3, 0.3):
        F.b((cx + sx, 4.6, 1.1 * s), (0.14, 0.16, 0.66 * s), dk)
    G.b((1.0, 4.35, 1.55), (0.5 * s, 0.04, 0.1 * s), YEL)                    # 둘을 잇는 '=' 표지
    G.b((1.0, 4.35, 1.3), (0.5 * s, 0.04, 0.1 * s), YEL)
    fireflies(G, t)


def props_heat(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    lemur(F, t)
    T = lerp(20.0, 31.0, smooth(tau / (dur * 0.7)))
    cx, cy = 0.9, 4.2
    F.b((cx, cy, 1.3), (0.2, 0.16, 2.0), (0.82, 0.88, 0.92))
    F.b((cx, cy, 0.18), (0.44, 0.4, 0.06), (0.55, 0.58, 0.62))
    BL.orb((cx, cy - 0.05, 0.3), 0.34, (0.9, 0.15, 0.12))
    h = 0.1 + 1.8 * (T / 40.0)
    F.b((cx, cy - 0.1, 0.3 + h / 2), (0.09, 0.07, h), (0.9, 0.15, 0.12))
    F.b((cx + 0.17, cy - 0.1, 0.3 + 1.8 * 30.0 / 40.0), (0.14, 0.03, 0.03), (0.1, 0.1, 0.12))
    wdig(G, num_rows(str(int(T))), cx, cy - 0.3, 2.65, 0.13, ORA)
    OR.orb((1.3, 9.0, 3.7), 1.8 + 0.06 * math.sin(2 * math.pi * t / 1.4), (3.0, 2.4, 0.8))
    OR.orb((1.3, 9.5, 3.7), 3.4, (1.2, 0.8, 0.3))


# ── 부엌
def props_spring(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    th = smooth((tau - 0.3) / 0.9) * 1.9                                   # 문이 열림 (오른쪽 경첩 둘레로 앞쪽으로 젖혀짐)
    hx, hy = 2.4, 2.5
    F.c((hx - 0.5 * math.cos(th), hy - 0.5 * math.sin(th), 0.95), (1.0, 0.07, 1.9), (0.66, 0.72, 0.78), (0.0, 0.0, th))
    if th > 0.25:
        G.b((1.9, 2.52, 0.95), (0.8, 0.02, 1.6), (2.0, 2.0, 2.2))
        for x, z, c in ((1.65, 0.62, (0.95, 0.95, 0.9)), (2.15, 0.62, (0.9, 0.6, 0.2)), (1.75, 1.1, (0.85, 0.25, 0.25)),
                        (2.1, 1.1, (0.35, 0.65, 0.4)), (1.9, 1.64, (0.95, 0.85, 0.4))):
            F.b((x, 2.45, z), (0.22, 0.16, 0.26), c)
    for k in range(9):                                                      # 라면 줄 세우기
        s = pop(tau - 1.0 - 0.17 * k, 0.25)
        if s > 0.01:
            F.b((-0.5 + 0.2 * k, 3.45, 0.96 + 0.17 * s), (0.17, 0.07, 0.32 * s), (0.9, 0.35, 0.2))
            F.b((-0.5 + 0.2 * k, 3.405, 0.96 + 0.17 * s), (0.15, 0.02, 0.08 * s), (0.96, 0.82, 0.3))


# ── 노을 창가
def props_seven(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bottle(F, -0.8, 2.4, 0.72, 0.25)
    top = 0.72 + 0.06 + 1.15
    G.b((-0.45, 2.15, top), (0.3, 0.03, 0.03), (1.4, 1.1, 0.35))
    wdig(G, num_rows("31"), 0.05, 2.1, top, 0.07, (1.8, 1.4, 0.4), pop(tau - 0.1, 0.3))
    m = 0.72 + 0.06 + 1.15 * 0.25
    G.b((-0.45, 2.15, m), (0.3, 0.04, 0.05), YEL)
    wdig(G, num_rows("7.8"), 0.12, 2.1, m, 0.075, YEL, pop(tau - 0.6, 0.3))


def props_unknown(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bottle(F, -0.8, 2.4, 0.72, 0.25)
    wdig(G, DIG["?"], -0.8, 2.3, 2.45 + 0.05 * math.sin(2 * math.pi * t / 1.1), 0.17, (3.0, 2.6, 0.9), pop(tau - 0.3, 0.3))


def props_tea(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bottle(F, -0.8, 2.4, 0.72, 0.25)
    c = (0.78, 0.45, 0.30)
    F.b((1.0, 2.45, 0.66), (0.9, 0.8, 0.22), c)                              # 이불을 두른 모습
    F.b((0.42, 2.95, 1.0), (0.14, 0.5, 0.7), c)
    F.b((1.58, 2.95, 1.0), (0.14, 0.5, 0.7), c)
    F.b((1.0, 3.0, 1.46), (0.95, 0.45, 0.14), c)
    F.b((1.0, 2.35, 0.98), (0.14, 0.14, 0.14), (0.9, 0.85, 0.75))             # 찻잔
    for k in range(3):
        q = (t * 0.6 + k / 3.0) % 1.0
        G.b((1.0 + 0.05 * math.sin(5 * q + k), 2.35, 1.12 + 0.5 * q), (0.05, 0.05, 0.05), (1.8, 1.6, 1.4))


def props_ask(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bottle(F, -0.8, 2.4, 0.72, 0.25)
    s = pop(tau - 0.3, 0.3)
    F.b((1.55, 2.5, 1.95), (0.7 * s, 0.05, 0.7 * s), (0.78, 0.74, 0.62))      # 달력 아이콘
    F.b((1.55, 2.46, 2.2), (0.7 * s, 0.03, 0.18 * s), (0.78, 0.25, 0.22))
    for r in range(4):
        for c in range(5):
            on = int(t * 4.0) % 20 == r * 5 + c
            G.b((1.3 + 0.12 * c, 2.43, 2.0 - 0.1 * r), (0.07 * s, 0.02, 0.07 * s), (3.0, 2.4, 0.5) if on else (0.5, 0.45, 0.4))


# ── 달 티저
def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    d = 14.0 * (1.0 + 0.05 * smooth(tau / dur))
    OR.orb((0.0, 60.0, 22.0), d, (2.6, 2.5, 2.2))
    OR.orb((0.0, 60.6, 22.0), d * 1.35, (0.5, 0.5, 0.45))
    wdig(G, num_rows("+1cm"), 0.0, 50.0, 14.0, 0.55, YEL, pop(tau - 0.4, 0.4))


PROPS = {LN["hook"]: props_hook, LN["bottle"]: props_bottle, LN["sleep"]: props_sleep, LN["metab"]: props_metab,
         LN["heart"]: props_heart, LN["week"]: props_week, LN["fast"]: props_fast, LN["growl"]: props_growl,
         LN["muscle"]: props_muscle, LN["mirror"]: props_mirror, LN["months"]: props_months, LN["cold"]: props_cold,
         LN["doctor"]: props_doctor, LN["lemur"]: props_lemur, LN["twist"]: props_twist, LN["heat"]: props_heat,
         LN["urea"]: props_urea, LN["spring"]: props_spring, LN["seven"]: props_seven, LN["unknown"]: props_unknown,
         LN["tea"]: props_tea, LN["ask"]: props_ask, LN["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR, BL, LT = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off), Items(N_BL, off), []
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
HID = -80.0                       # 안 보이는 자리 (세트 바깥 y)


def jh_bed(tau, t):
    """2번 jh: 앉아 있다가 눕는 순간 사라짐(눕는 모습은 jl)."""
    return dict(y=3.3 if tau < 1.0 else HID)


def jl_bed(tau, t):
    """2번 jl: 앉은 지후가 눕는 모습."""
    if tau < 1.0:
        return dict(y=HID)
    k = smooth((tau - 1.0) / 0.5)
    return dict(x=-1.0, y=lerp(3.3, 2.0, k), z=lerp(0.14, 0.5, k), yaw=-90, pose="lie" if k > 0.5 else "sit")


def jl_stand(tau, t):
    """9번 jl: 누워 있다가 일어서는 순간 사라짐."""
    return dict(y=2.0 if tau < 0.5 else HID)


def jh_stand(tau, t):
    """9번 jh: 일어서서 비틀거림."""
    if tau < 0.5:
        return dict(y=HID)
    k = smooth((tau - 0.5) / 0.6)
    return dict(x=lerp(-1.0, -2.35, k), y=lerp(2.0, 1.3, k), z=lerp(0.5, 0.0, k), yaw=-90 + 14.0 * math.sin(2 * math.pi * (tau - 0.5) / 0.7) * k,
                pose="stand" if tau < 1.7 else "gape")


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    add("jh", 0, JH_SH, JH_PA, {
        L["hook"]: st("room", -1.0, 3.3, -90, "sit", z=0.14, sway=(5, 0.5, 0.0), alt=("sit", "sit_conf", 0.9, 0.0)),
        L["bottle"]: st("room", -1.0, 3.3, -90, "sit", z=0.14, alt=("sit", "sit_conf", 1.1, 0.3)),
        L["sleep"]: st("room", -1.0, 3.3, -90, "sit", z=0.14, fn=jh_bed),
        L["mirror"]: st("room", -1.0, 2.0, -90, "stand", fn=jh_stand, also=("stand", "gape")),
        L["spring"]: st("kitchen", 1.0, 1.2, 50, "gape", seq=[(1.0, "smile")]),
        L["unknown"]: st("dusk", 1.3, 1.9, -135, "smile", alt=("gape", "stand", 0.9, 0.0)),
        L["tea"]: st("dusk", 1.0, 3.0, -90, "sit", z=0.09),
        L["ask"]: st("dusk", 0.3, 1.8, -90, "point", seq=[(0.9, "smile")])}, extra="hood")
    add("jl", 0, JH_SH, JH_PA, {                                           # 누운 지후 (후드는 누운 몸에 안 맞아 빼고 같은 색)
        L["sleep"]: st("room", -1.0, 3.3, -90, "sit", z=0.14, fn=jl_bed, also=("lie",)),
        L["growl"]: st("room", -1.0, 2.0, -90, "lie", z=0.5),
        L["mirror"]: st("room", -1.0, 2.0, -90, "lie", z=0.5, fn=jl_stand),
        L["months"]: st("room", -1.0, 2.0, -90, "lie", z=0.5)})
    add("rs", 1, CO_SH, CO_PA, {
        L["doctor"]: st("er", 0.3, 2.6, -110, "point", alt=("point", "smile", 1.1, 0.3)),
        L["unknown"]: st("dusk", -2.0, 1.9, -50, "think", alt=("think", "smile", 1.3, 0.3))}, extra="coat")
    add("pt", 1, PT_SH, PT_PA, {L["doctor"]: st("er", -1.7, 2.45, -90, "lie", z=0.72)})
    add("e1", 0, EX1[0], EX1[1], {L["week"]: st("town", -5.0, 2.0, 0, "walk_a", pair=("walk_a", "walk_b"), v=(0.5, 0.0))})
    add("e2", 1, EX2[0], EX2[1], {L["week"]: st("town", 4.5, 1.2, 180, "walk_a", pair=("walk_a", "walk_b"), v=(-0.5, 0.0))})
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
NIGHT_SKY = ((0.03, 0.05, 0.12), (0.10, 0.14, 0.26), 0.5)
DAY_SKY = ((0.30, 0.42, 0.62), (0.66, 0.74, 0.86), 0.0)
GREY_SKY = ((0.30, 0.34, 0.44), (0.58, 0.63, 0.72), 0.0)
FOREST_NIGHT = ((0.02, 0.04, 0.10), (0.06, 0.10, 0.20), 1.0)
FOREST_DAY = ((0.18, 0.40, 0.70), (0.60, 0.78, 0.92), 0.0)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
SPACE_SKY = ((0.003, 0.004, 0.014), (0.010, 0.013, 0.034), 1.8)


def sky(t):
    i = line_at(t)
    s = cam_of(t)["set"]
    if s == "room":
        return DAY_SKY if i == LN["months"] else NIGHT_SKY
    if s in ("cave", "er", "kitchen"):
        return DAY_SKY
    if s == "town":
        return GREY_SKY
    if s == "forest":
        return FOREST_DAY if i == LN["heat"] else FOREST_NIGHT
    if s == "dusk":
        return DUSK_SKY
    return SPACE_SKY


def env(i, st_):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=2.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if st_ == "room":
        e.update(sun=0.5 if i != LN["months"] else 1.6, sun_col=(0.7, 0.78, 1.0), amb=0.5, amb_col=(0.66, 0.70, 0.88),
                 lt={"ep48_rm0": 260.0, "ep48_rm1": 170.0, "ep48_rm2": 140.0})
    elif st_ == "cave":
        e.update(sun=2.2, sun_col=(0.85, 0.92, 1.0), amb=0.5, amb_col=(0.70, 0.76, 0.90), lt={"ep48_cv0": 240.0, "ep48_cv1": 210.0})
    elif st_ == "town":
        e.update(sun=0.9, sun_col=(0.75, 0.82, 1.0), amb=0.55, amb_col=(0.62, 0.68, 0.84), lt={"ep48_tw0": 260.0, "ep48_tw1": 260.0, "ep48_tw2": 150.0})
    elif st_ == "er":
        e.update(sun=0.6, amb=0.5, amb_col=(0.78, 0.86, 0.92), lt={"ep48_er0": 300.0, "ep48_er1": 150.0})
    elif st_ == "forest":
        if i == LN["heat"]:
            e.update(sun=3.2, sun_col=(1.0, 0.9, 0.7), amb=0.45, amb_col=(0.70, 0.78, 0.9), lt={"ep48_fo0": 60.0})
        else:
            e.update(sun=0.4, sun_col=(0.6, 0.7, 1.0), amb=0.38, amb_col=(0.45, 0.55, 0.85), lt={"ep48_fo0": 70.0, "ep48_fo1": 220.0})
    elif st_ == "kitchen":
        e.update(sun=1.2, sun_col=(1.0, 0.95, 0.8), amb=0.5, amb_col=(0.85, 0.85, 0.78), lt={"ep48_kt0": 270.0, "ep48_kt1": 130.0})
    elif st_ == "dusk":
        e.update(sun=1.4, sun_col=(1.0, 0.62, 0.38), sun_rot=(72, 0, 20), amb=0.42, amb_col=(0.85, 0.66, 0.66),
                 lt={"ep48_dk0": 240.0, "ep48_dk1": 150.0})
    elif st_ == "moon":
        e.update(sun=0.6, sun_col=(0.8, 0.88, 1.0), amb=0.25, amb_col=(0.35, 0.42, 0.7), lt={"ep48_mn0": 200.0})
    return e


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
                env=env(i, cam["set"]))


# ───────────────────────── Blender 원형(프로토) ─────────────────────────
def build(ctx):
    from engine import bkit as K
    v = X.Vox(48)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep48_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep48_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep48_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep48_fx", K.proto(ctx, "ep48_p_fx", cube(), [K.mat_inst("ep48_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep48_glow", K.proto(ctx, "ep48_p_glow", cube(), [_mat_glow("ep48_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep48_orb", K.proto(ctx, "ep48_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep48_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep48_bl", K.proto(ctx, "ep48_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep48_m_bl", 0.8)]),
                     N_BL, vector_scale=True)
    for ob in (gl, orb):                                              # 발광 상자·구가 햇빛을 가리지 않게
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
