"""EP36 만약에 서울에 규모 7 지진이 온다면? (정보형 v2: 블록 캐릭터·내레이션·정보 카드·경과 배지)

가정: 상상 시나리오이며 실제 서울 지진 예측이 아님(설명란에 적을 것). 공포 조장·단정 없이 '~할 수 있어요' 톤.
파괴 장면은 가볍게(컵·접시가 떨어지고 건물에 금이 가는 정도, 사람이 다치는 장면 없음).

컷 흐름 (한 줄 = 한 컷, 괄호 = 세트):
0 훅(거실): 0.0초부터 식탁 위 접시·컵이 떨리며 미끄러져 떨어지고 펜던트가 흔들림 — 도현·엄마가 식탁 끝에서 식탁 밑으로 엎드림(세트·카메라 진동)
→ 1 거실 TV에 지진계 선이 그려지며 '경주 5.8' 봉우리(방 약하게 흔들림) → 2 같은 TV에 '포항 5.4' 봉우리
→ 3 막대 방(실험 무대): 규모 5.8 작은 막대 → 6.8 막대가 32배로 솟음 → 4 7.0 막대가 63배로 천장까지 솟아 쿵(먼지)
→ 5 식탁 밑에서 머리를 감싼 도현·엄마(흔들림 계속) → 6 계단실: 엘리베이터 문의 빨간 X, 가족이 계단으로 내려가고 경비 아저씨가 출구를 가리킴
→ 7 폰: 타이머가 5초까지 센 뒤 빨간 재난문자 알림(종 아이콘 팝) → 8 체육관 대피소(칸막이 텐트·구조대·도현 가족)
→ 9 건물 모형 열 채가 차례로 솟고(회색) 끝에서 두 채가 초록으로 → 10 회색 여덟 채에 금이 감(가볍게)
→ 11 텅 빈 교실(칠판 '휴교', 문에 노란 안전점검 테이프) → 12 도현이 벽 달력의 수능 날짜(빨간 동그라미)를 바라봄
→ 13 교문 앞 '연기' 안내판과 수험생들(새벽 눈발) → 14 밤 가로등 아래 벤치에서 책을 펴 든 학생들
→ 15 비계가 쳐진 낡은 건물과 크레인(철골을 들어 올림) → 16 새 건물 정면에 초록 체크
→ 17 반전: 땅속 단면에 지열발전소 관이 내려감 → 18 파란 물이 관을 따라 내려가 바위가 갈라지고 진동 고리
→ 19 폰: 타이머가 8분을 센 뒤에야 문자 → 20 같은 폰에 곧바로 알림 → 21 가족이 비상가방에 물건을 던져 넣음
→ 22 거실을 둘러보는 도현(물음표가 차례로 톡) → 23 노을 창밖에 멈춘 듯 걸린 해(다음 편 예고).

근거(설명란):
1~2줄 · 한국 지진 관측 사상 최대 규모는 2016 경주 5.8, 2위는 2017 포항 5.4 · 기상청
3~4줄 · 규모가 1 커지면 에너지는 약 32배(진폭은 10배) → 규모 7.0은 5.8의 약 63배 (계산값: 10^(1.5×1.2) = 10^1.8 ≈ 63) · USGS 교육 페이지
5~6줄 · 행동요령: 흔들리는 동안 튼튼한 탁자 아래에서 머리·몸 보호 → 멈추면 전기·가스 차단, 출구 확보 → 계단으로(엘리베이터 금지) ·
       행정안전부 국민행동요령(기상청 지진 안내 페이지)
7줄 · 규모 5.0 이상 지진은 최초 관측 후 5~10초 안에 전국 긴급재난문자(2021년 이후) · 기상청 보도자료 2023-12-22
9~10줄 · 전국 건축물 약 732만 동 중 내진 성능 확보 약 94만 동(12.9%, 2022년 6월 기준 · 2022년 말 13.4%) → '약 13%' ·
        국토교통부 자료(국회 제출, 2023.2 보도)
12~13줄 · 2017 포항 지진으로 수능이 11-16에서 11-23으로 1주일 연기 — 자연재해(천재지변)로 수능이 미뤄진 건 처음 · 교육부 2017-11-15 긴급 브리핑
15~16줄 · 2017.2.4부터 2층 이상 신축 건축물도 내진설계 의무(종전 3층 이상) · 국토교통부 2017-02-02 발표
17~18줄 · 포항 지진은 지열발전소의 고압 물 주입이 촉발한 것으로 2019-03-20 정부조사연구단이 결론(지진 후 491일) · 정부조사연구단 발표
19~20줄 · 2016 경주 첫 지진(19:44) 때 첫 재난문자가 8분 늦었다. 조기경보 발표 시간은 2015년 50초 → 2021년 5~10초로 줄었다 ·
        머니투데이 2016-09-20, 기상청 보도자료 2023-12-22
(건물 열 채 그림 · 막대 높이 · 지진계 선 모양 · 땅속 물과 금 · 흔들림 크기는 이해를 돕는 상상 연출이며 실제 수치·모습이 아님)

특수효과 (모두 블렌더 없이 numpy·math로 줄·시간에서 바로 계산, 프레임당 가벼움):
흔들림 = quake(줄, τ)가 줄마다 세기 0~1을 정함(훅 1.0→0.75, TV 0.45→0.12, 엎드림 0.9→0.3, 7.0 막대가 천장에 닿는 순간 쿵, 금 갈 때·물이 스밀 때 약하게).
  세트 메시 두 개(solid·glow)의 location과 사람·소품 점 위치에 같은 사인파 변위(4.7·3.9·6.3Hz, 약 4cm) + 카메라 목표점 이동·방위각·고도각 흔들림(5.3·4.3·6.9·3.7·4.9Hz).
  흔들리는 줄에는 스프라이트를 쓰지 않음(스프라이트는 카메라에 붙어 있어야 하므로).
식탁 위 물건 11개(접시 셋·컵 셋·그릇·물병·사과 셋) = 줄 시작부터 덜덜 떨며 정해 둔 속도로 미끄러지다 식탁 가장자리를 넘으면 포물선으로 떨어져 한 번 튕김(item_pose).
  펜던트 = 천장 레일에 매달린 줄(가는 상자)+갓+발광판이 두 방향으로 흔들리고 점광원이 따라감. 액자 기울기·떨어지는 먼지.
엎드림 = KINDS['duck'](두 손을 뒤통수에·입 벌림) 원형을 인스턴스 pitch로 앞으로 눕힘(식탁 양 끝에서 미끄러져 들어감, 몸을 식탁 높이 아래에 둠).
TV 지진계 = 발광 상자 61칸 선(칸마다 위아래가 이어지는 높이) + 펜 끝 점, 봉우리 옆에 '경주 5.8'·'포항 5.4' 도트 글자.
  한글 도트 글자 = Noto Sans KR(OFL)을 16x16 칸으로 줄여 16진 문자열로 내장(GLYPH, ep27 방식: 굵기 620·0.94 맞춤·칸 평균 0.40 이상 켬), 숫자는 3x5 도트(DIG).
막대 방 = 상자 높이 1 : 32 : 63(0.05·1.6·3.15m, 규모 5.8·6.8·7.0), 천장판 3.25m. 6.8은 easeOutBack으로 솟고 7.0은 천장에 닿는 순간(T_HIT) 불꽃·먼지.
계단 = 아홉 칸(칸 0.2m 낮아짐), 걷는 사람 발 높이는 한 칸에서 머물다 부드럽게 내려가는 _sz(x). 엘리베이터 문 위 큰 빨간 X·초록 화살표 표지는 발광 도트.
폰(7·19·20번 줄) = 화면 좌표 스프라이트(카메라 앞 1.5m 안팎의 납작한 발광 상자): 어두운 판 + 폰 몸통·화면 + 타이머 도트 숫자(0:00~0:05 / 0:00~8:00) + 빨간 화면에 종 아이콘 팝·진동.
체육관 = 칸막이 텐트 8칸(바닥 매트·판 세 장), 앉은 사람은 의자 높이 앉은 자세를 낮춰 바닥에 앉힘(SIT_FLOOR), 구조대는 주황 조끼·흰 헬멧(extra='helmet').
건물 모형 = 상자 열 채(3·3·2·2줄, 높이·창 발광 칸은 솟는 키에 맞춤): 회색 여덟 + 두 채가 끝에서 초록으로 바뀜, 10번 줄에 금(가는 선 세 토막)과 먼지.
교실 = 칠판 도트 글씨 '휴교', 문에 계단식 점으로 만든 X자 노란·검정 테이프, 창가 먼지. 교문 = 빨간 현수막 '수능'·안내판 '연기'(도트 글자), 새벽 눈발·가로등.
거리 = 이동식 크레인 붐(두 마디, 방위각·고도각 변화)·줄·철골 보(흔들림), 비계 기둥·널·난간, 용접 불꽃(발광 점), 새 건물에 초록 체크(도트, 톡 커짐).
땅속 = 층층이 색이 다른 흙·바위 상자, 관이 시간에 따라 길어지고(17) 파란 발광 조각이 관을 따라 내려가 바닥에서 파란 구가 커지며 금(어두운 선)·진동 고리가 번짐(18).
해(23번 줄) = 카메라에서 140m 밖(무한히 먼 해처럼 시차 없음)에 둔 발광 구 둘(+ 바깥 둘레), 창은 벽에 낸 구멍이라 하늘 그라데이션이 보임(sky(t)).
하늘 = 낮 / 새벽(13) / 밤(14) / 노을(23) / 스튜디오(실험 무대)를 sky(t)로 줄마다 바꿈.
(자막 20자 제한: 모든 cap이 20자 이내라 줄인 줄 없음. 13번 줄은 정확히 20자. 줄 사이 gap은 71.4초를 62~68초 목표에 맞추려고 기본 0.3초를 0.12초로 좁힘 — 21번 줄 0.6초·22번 줄 0.25초)
"""
import json
import math
from pathlib import Path

import numpy as np

from engine import voxel as X
from engine.common import clamp, keyed, ramp, smooth

STYLE = "pixe"
TITLE_FAST = True
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.15, 0.3, 1.6)
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게). 집 세트 안에 계단실(HX_ST)·실험 무대 안에 건물 모형(LB_CITY)·땅속 단면(LB_UG)·
# 교문 세트 안에 밤 가로등 자리(GT_LAMP)가 x로 나란히 붙어 있음
OFF = {"home": (0, 0), "gym": (300, 0), "class": (600, 0), "gate": (900, 0), "street": (1200, 0), "lab": (1500, 0)}
HX_ST, GT_LAMP, LB_CITY, LB_UG = 60.0, 50.0, 60.0, 120.0
NAMES = ("hook", "seismo1", "seismo2", "bar1", "bar2", "duck", "stairs", "alert", "gym", "blds", "cracks", "closed",
         "calendar", "gate", "lamp", "scaffold", "newbld", "pipe", "inject", "late", "now", "bag", "around", "teaser")
IX = {n: k for k, n in enumerate(NAMES)}

# say: 내레이션 / cap: 화면 자막(아라비아 숫자) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동])
# ease="out"이면 카메라가 처음에 빨리 움직이고 천천히 멈춤(훅) / tgt2: 줄 끝의 목표점(있으면 목표점이 시간에 따라 옮겨 감)
LINES = [
    dict(say="규모 칠 지진은 경주 지진의 육십삼 배 에너지예요", ease="out",
         shot=("home", (0.0, 0.95, 1.70), -90, 7, 6.0, 24, 0.93, 3, 0.04), tgt2=(0.0, 0.85, 0.55)),
    dict(say="한국에서 가장 센 지진은 규모 오점팔이었어요", cap="한국 최대 지진은 규모 5.8",
         shot=("home", (-4.4, -0.5, 1.7), 0, 4, 5.2, 24, 0.95, -3)),
    dict(say="두 번째는 포항, 규모 오점사였죠", cap="2위는 2017 포항 규모 5.4",
         shot=("home", (-4.4, -0.5, 1.7), -6, 4, 5.2, 24, 0.95, 8)),
    dict(say="규모가 일 커지면 에너지는 서른두 배예요", cap="규모 1 증가 = 에너지 32배",
         shot=("lab", (-0.2, 0.0, 1.62), -90, 3, 9.0, 24, 0.97, 3)),
    dict(say="규모 칠은 경주보다 육십삼 배 강해요", cap="규모 7은 경주의 약 63배",
         shot=("lab", (-0.2, 0.0, 1.62), -80, 4, 9.0, 24, 0.95, 6)),
    dict(say="흔들리면 탁자 밑에서 머리를 지켜요", cap="탁자 밑에서 머리를 지켜요",
         shot=("home", (0.0, 0.8, 0.45), -85, 15, 4.8, 24, 0.92, 5, 0.05)),
    dict(say="멈추면 엘리베이터 말고 계단으로 가요", cap="멈추면 계단으로, 엘리베이터 금지",
         shot=("home", (HX_ST - 0.2, 1.0, 2.6), -90, 6, 9.5, 24, 0.95, 0, 0.0), tgt2=(HX_ST + 3.4, 1.0, 1.2)),
    dict(say="오 초에서 십 초 안에 재난문자가 울려요", cap="5~10초 안에 재난문자가 울려요",
         shot=("home", (0.0, -1.0, 1.2), -90, 0, 3.0, 24, 1.0, 0)),
    dict(say="하루 뒤, 사람들은 체육관으로 모였어요", cap="하루 뒤, 체육관에 모였어요",
         shot=("gym", (-1.0, 2.4, 0.5), -90, 22, 9.5, 24, 0.92, 4)),
    dict(say="우리나라 건물은 열 채 중 여덟 채 넘게", cap="건물 10채 중 8채 넘게",
         shot=("lab", (LB_CITY + 0.5, 0.0, 0.8), -90, 26, 8.5, 24, 0.95, 4)),
    dict(say="내진 성능이 확보되지 않았어요", cap="내진 성능이 확보되지 않았어요",
         shot=("lab", (LB_CITY + 0.5, 0.0, 0.8), -80, 22, 7.6, 24, 0.9, 8)),
    dict(say="일 주일 뒤, 학교는 문을 닫았어요", cap="1주 뒤, 학교는 문을 닫았어요",
         shot=("class", (-0.6, 2.0, 1.2), -90, 8, 8.2, 24, 0.92, 3)),
    dict(say="수능이 코앞이었다면 어떻게 될까요?", cap="수능이 코앞이었다면?",
         shot=("home", (-3.0, 3.0, 1.3), -90, 6, 5.0, 24, 0.94, 0, 0.03)),
    dict(say="이천십칠 년엔 포항 지진으로 수능이 일 주일 미뤄졌어요", cap="2017년엔 수능이 1주일 미뤄졌어요",
         shot=("gate", (0.0, 1.5, 1.2), -88, 6, 7.4, 24, 0.92, 4)),
    dict(say="수험생들은 하루 더 책을 폈어요", cap="수험생들은 하루 더 책을 폈어요",
         shot=("gate", (GT_LAMP, 0.6, 1.0), -82, 5, 6.3, 24, 0.94, 4, 0.03)),
    dict(say="일 년 뒤, 오래된 건물을 보강하기 시작해요", cap="1년 뒤, 오래된 건물을 보강해요",
         shot=("street", (2.6, 5.0, 4.2), -90, 6, 15.5, 24, 0.94, 4)),
    dict(say="신축 건물은 내진설계가 의무고요", cap="신축 건물은 내진설계가 의무",
         shot=("street", (12.5, 5.0, 4.6), -90, 5, 14.5, 24, 0.95, 3)),
    dict(say="그런데 포항 지진은 사람이 촉발한 거였어요", cap="그런데 포항 지진은 촉발 지진",
         shot=("lab", (LB_UG - 0.2, 0.0, -1.3), -90, 3, 9.5, 24, 0.95, 3)),
    dict(say="지열발전소가 땅속에 물을 넣다 일어났대요", cap="땅속에 물을 넣다 일어났대요",
         shot=("lab", (LB_UG - 0.2, 0.0, -1.8), -85, 4, 9.0, 24, 0.92, 4)),
    dict(say="경주 땐 첫 재난문자가 팔 분 늦었지만", cap="경주 땐 첫 문자가 8분 늦었지만",
         shot=("home", (0.0, -1.0, 1.2), -90, 0, 3.0, 24, 1.0, 0)),
    dict(say="지금은 오 초에서 십 초면 울려요", cap="지금은 5~10초면 울려요",
         shot=("home", (0.0, -1.0, 1.2), -90, 0, 3.0, 24, 1.0, 0)),
    dict(say="준비한 만큼 지진은 덜 무서워요", cap="준비한 만큼 지진은 덜 무서워요", gap=0.6,
         shot=("home", (0.0, -2.4, 0.85), -90, 8, 4.6, 24, 0.92, 5, 0.04)),
    dict(say="우리 집에서 가장 안전한 자리는 어디일까요?", cap="우리 집에서 가장 안전한 자리는?",
         shot=("home", (-0.2, -0.3, 1.2), -90, 8, 6.2, 20, 0.92, 4)),
    dict(say="오늘 저녁 일곱 시, 지구가 자전을 멈춘다면?", cap="다음 편 · 지구가 자전을 멈춘다면?",
         shot=("home", (0.0, 3.2, 1.6), -90, 2, 4.4, 24, 0.97, 0, 0.0)),
]
assert len(LINES) == len(NAMES)
for _ln in LINES[:21]:                  # 줄 사이 간격: 기본 0.3초로는 71.4초라 62~68초 목표에 맞추려고 좁힘 (21번 줄 0.6초는 감정 줄 그대로)
    _ln.setdefault("gap", 0.12)
LINES[22]["gap"] = 0.25
TITLE = [("만약에", "white"), ("서울에 규모 7", "white"), ("지진이 온다면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = 17          # '그런데 포항 지진은 사람이 촉발한 거였어요' 줄

CLOCK = [(1, "경과", "바로"), (8, "경과", "하루 뒤"), (11, "경과", "1주 뒤"), (15, "경과", "1년 뒤"),
         (17, "경과", "지금"), (19, None)]
CARDS = [
    dict(lines=(1, 2), big="규모 5.8", small="관측 사상 최대 · 2016 경주 (2위 2017 포항 5.4)", color="yellow", src="기상청"),
    dict(lines=(3, 4), big="× 32", small="규모 1 차이의 에너지 비 · 규모 7은 경주의 약 63배(계산값)", color="yellow", src="USGS"),
    dict(lines=(5, 6), big="탁자 밑 → 계단", small="흔들리는 동안 머리 보호, 멈추면 계단으로", color="cyan", src="행정안전부"),
    dict(lines=(7, 7), big="5~10초", small="규모 5.0 이상 지진의 전국 재난문자", color="yellow", src="기상청"),
    dict(lines=(9, 10), big="내진 약 13%", small="전국 건축물 중 내진 성능 확보 비율(2022)", color="orange", src="국토교통부 자료(국회 제출)"),
    dict(lines=(12, 13), big="수능 1주 연기", small="2017 포항 지진 · 자연재해로는 처음", color="yellow", src="교육부 2017-11-15 브리핑"),
    dict(lines=(15, 16), big="2층 이상", small="신축 건물 내진설계 의무(2017.2~, 종전 3층)", color="green", src="국토교통부 2017-02-02"),
    dict(lines=(17, 18), big="지열발전", small="땅속에 물을 넣다 촉발(2019-03 결론)", color="red", src="정부조사연구단"),
    dict(lines=(19, 19), big="8분 늦음", small="2016 경주 첫 지진(규모 5.1) 때 첫 재난문자", color="orange", src="머니투데이 2016-09-20"),
    dict(lines=(20, 20), big="50초 → 5~10초", small="지진 조기경보 발표 시간(2015 → 2021)", color="green", src="기상청 보도자료 2023-12-22"),
    dict(lines=(23, 23), big="다음 편", small="오늘 저녁 7시 · 지구가 자전을 멈춘다면?", color="cyan", src="구독하면 놓치지 않아요"),
]
for _ln in LINES[1:]:
    assert len(_ln.get("cap", _ln["say"])) <= 20, _ln.get("cap", _ln["say"])
assert all(0 < c["lines"][0] <= c["lines"][1] < len(LINES) for c in CARDS)

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep36_quake7" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 66.0, "lines": [[0.15 + 2.7 * i, 2.7 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep36", "title": "만약에 서울에 규모 7 지진이 온다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"key": "D", "mode": "major", "bpm": 96, "seed": 361, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.12, "bloom_thr": 1.4, "vignette": 0.16}


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


# ───────────────────────── 흔들림 · 카메라 (블렌더 없이 계산) ─────────────────────────
QK = {IX["hook"]: (1.0, 0.75), IX["seismo1"]: (0.45, 0.30), IX["seismo2"]: (0.30, 0.12), IX["duck"]: (0.9, 0.3), IX["cracks"]: (0.30, 0.12)}
T_HIT = 1.55            # 7.0 막대가 천장에 닿는 순간(4번 줄 시작 후 초)
R_FAR = 140.0           # 하늘의 해를 두는 거리(m): 카메라 위치 + 방향 x R_FAR (무한히 먼 해처럼 시차 없음)


def quake(i, tau, dur):
    """줄 i, 줄 시작 후 tau초의 흔들림 세기 0~1. 0이면 세트·카메라가 가만히 있음."""
    if i in QK:
        a, b = QK[i]
        return a + (b - a) * clamp(tau / max(dur, 1e-3))
    if i == IX["bar2"]:                                      # 막대가 천장에 닿을 때 쿵 한 번
        d = tau - T_HIT
        return 0.7 * math.exp(-4.0 * d) if d > 0 else 0.0
    if i == IX["inject"]:                                    # 물이 스며들며 땅이 살짝 떨림
        return 0.35 * ramp(tau, 0.5, 1.0)
    return 0.0


def world_shake(t, a, sc):
    """세트 전체에 주는 사인파 변위(m). a = 세기, sc = 카메라 거리에 맞춘 배율."""
    if a <= 0.0:
        return np.zeros(3)
    w = 2 * math.pi
    return a * sc * np.array((0.040 * math.sin(w * 4.7 * t), 0.032 * math.sin(w * 3.9 * t + 1.3), 0.016 * math.sin(w * 6.3 * t + 0.4)))


def cam_shake(t, a, sc):
    """카메라 진동: (목표점 이동 m, 방위각 변화, 고도각 변화)."""
    if a <= 0.0:
        return np.zeros(3), 0.0, 0.0
    w = 2 * math.pi
    return (a * sc * np.array((0.030 * math.sin(w * 5.3 * t + 0.7), 0.026 * math.sin(w * 4.3 * t + 2.1), 0.034 * math.sin(w * 6.9 * t))),
            a * 0.55 * math.sin(w * 3.7 * t + 0.2), a * 0.40 * math.sin(w * 4.9 * t + 1.0))


def cam_pose(i, u, t=None):
    """줄 i, 진행도 u의 카메라: dict(set, tgt, az, el, dist, lens, loc, shift, fwd, right, up, amp, shk) — 월드 좌표. CamRig.set과 같은 규칙.
    t(영상 초)를 주면 흔들림(amp>0인 줄)이 더해짐. shk = 세트·소품에 줄 변위."""
    ln = LINES[i]
    st_, tg, az, el, dist, lens, push, daz = ln["shot"][:8]
    shift = ln["shot"][8] if len(ln["shot"]) > 8 else 0.0
    if ln.get("ease") == "out":
        u = 1.0 - (1.0 - u) ** 2
    o = OFF[st_]
    tg = np.array(tg, float)
    if "tgt2" in ln:
        tg = tg + (np.array(ln["tgt2"], float) - tg) * u
    tgt = np.array((tg[0] + o[0], tg[1] + o[1], tg[2]), float)
    a, e, dd = az + daz * u, float(el), dist * (1 + (push - 1) * u)
    amp, shk = 0.0, np.zeros(3)
    if t is not None:
        s0, s1 = shot_span(i)
        amp = quake(i, max(t - s0, 0.0), max(s1 - s0, 1e-3))
        if amp > 0.0:
            d, da, de = cam_shake(t, amp, dd / 4.6)
            tgt, a, e = tgt + d, a + da, e + de
            shk = world_shake(t, amp, dd / 4.6)
    ea = math.radians(e)
    loc = tgt + np.array((math.cos(ea) * math.cos(math.radians(a)), math.cos(ea) * math.sin(math.radians(a)), math.sin(ea))) * dd
    fwd = tgt - loc
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, (0.0, 0.0, 1.0))
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return dict(set=st_, tgt=tgt, az=a, el=e, dist=dd, lens=lens, loc=loc, shift=shift, fwd=fwd, right=right, up=up, amp=amp, shk=shk)


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
    """상자 인스턴스 모음. 상자 원점 = 뒷면 가운데, +x로 뻗음(size로 늘림). c()는 가운데 기준으로 넣음. 구는 orb()(원점 = 가운데, size = 지름)."""

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

    def arrays(self, off=None):
        n = len(self.P)
        assert n <= self.cap, f"인스턴스 칸 부족: {n} > {self.cap}"
        pad = self.cap - n
        z3 = [(0.0, 0.0, 0.0)] * pad
        P = np.array(self.P + z3, np.float32)
        if off is not None and n:
            P[:n] += np.asarray(off, np.float32)
        return (P, np.array([1.0] * n + [0.0] * pad, np.float32),
                np.array(self.S + z3, np.float32), np.array(self.R + z3, np.float32), np.array(self.C + z3, np.float32))


def rot_cam(cam):
    """카메라 화면과 나란한 납작한 판의 오일러 회전: 상자 x = 앞(두께), y = 화면 가로, z = 화면 세로."""
    R = np.stack([cam["fwd"], -cam["right"], cam["up"]], 1)
    ry = -math.asin(max(-1.0, min(1.0, float(R[2, 0]))))
    return (math.atan2(float(R[2, 1]), float(R[2, 2])), ry, math.atan2(float(R[1, 0]), float(R[0, 0])))


def rot_to(d):
    """상자의 +x 축이 방향 d(단위벡터)를 향하게 하는 오일러 회전."""
    return (0.0, -math.asin(max(-1.0, min(1.0, float(d[2])))), math.atan2(float(d[1]), float(d[0])))


def sprite(G, cam, nx, ny, w, h, col, dist=2.0, thick=0.02, dx=0.0):
    """화면 좌표 (nx 오른쪽 +, ny 위 +, 둘 다 -1~1)에 정면을 보는 납작한 상자를 카메라에서 dist m 앞에 둠. w·h = 화면 높이에 대한 비율."""
    f = cam["lens"]
    d = cam["fwd"] + nx * (6.75 / f) * cam["right"] + (ny + 2.0 * cam["shift"]) * (12.0 / f) * cam["up"]
    d = d / np.linalg.norm(d)
    dist *= 0.75                                      # 바닥·가구보다 확실히 앞에 놓이게(바닥이 판 아래로 비치지 않게)
    s = dist * 24.0 / f
    G.c(cam["loc"] + d * dist + cam["right"] * dx, (thick, w * s, h * s), col, rot_cam(cam))


def pop(tau, dur=0.30, over=3.0):
    """톡 튀어나오는 크기: 0 → 살짝 커졌다 → 1 (easeOutBack). tau<0이면 0."""
    if tau <= 0:
        return 0.0
    if tau >= dur:
        return 1.0
    x = tau / dur - 1.0
    return 1.0 + (over + 1.0) * x ** 3 + over * x ** 2


def _h(n):
    """결정적 의사난수 0~1."""
    return (math.sin(n * 12.9898 + 4.1414) * 43758.5453) % 1.0


# ───────────────────────── 도트 글자 (숫자 3x5 · 한글 16x16) ─────────────────────────
DIG = {"0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"], "2": ["###", "..#", "###", "#..", "###"],
       "3": ["###", "..#", "###", "..#", "###"], "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
       "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", ".#.", ".#.", ".#."], "8": ["###", "#.#", "###", "#.#", "###"],
       "9": ["###", "#.#", "###", "..#", "###"], ".": ["...", "...", "...", "...", ".#."], ":": ["...", ".#.", "...", ".#.", "..."],
       "!": [".#.", ".#.", ".#.", "...", ".#."], "?": ["###", "..#", ".##", "...", ".#."], "~": ["...", ".#.", "#.#", "...", "..."], "x": ["...", "#.#", ".#.", "#.#", "..."],
       " ": ["..", "..", "..", "..", ".."]}
# 한글 16x16: 한 줄(가로 16칸)을 16진 4자리로, 맨 윗줄부터 16줄 이어 붙임(왼쪽 칸 = 가장 높은 비트).
# 만든 법: assets/fonts/NotoSansKR-VF.ttf(OFL)를 굵기 620으로 크게 그려 글자 경계 상자를 16칸 격자 가운데에 꽉 차게(0.94) 줄이고, 칸 평균이 0.40 이상이면 켬.
GLYPH = {
    "경": "000c1f8c3f8c01fc01fc030c077c1e7c380c01e007f80e1c0c0c0e1c07f800e0",
    "주": "3ffc3ffc03c003c007e01e783c3c00007ffe7ffe018001800180018001800180",
    "포": "00003ffc3ffc0c300c300c300c300c303ffc3ffc018001800180ffff7ffe0000",
    "항": "04000e187fd87fd80f1e3f9e319831981f980e1807e00ff818181c180ff003c0",
    "연": "000c0e0c1f8c3bfc71cc71cc31fc3ffc1f0c000c040c0c0c0c000c000ffe0ffc",
    "기": "000c000c3fcc1fcc01cc018c018c038c030c0e0c1c0c380c300c000c000c000c",
    "휴": "018001803ffc3ffc07e01ff818181c380ff000007ffe7ffe0c700c700c700420",
    "교": "00003ffc3ffc000c000c000c000c0ccc0ccc0cdc0ccc0cc01cc0ffff7ffe0000",
    "수": "0180018001c003c007e03e7c381c00007ffe7ffe018001800180018001800180",
    "능": "10001800180018001ff81ff800007ffe7ffe00000ff01e78181818381ff00380",
}


def _glyph_rows(c):
    """글자 하나 → 줄 문자열 목록('#'=칸 켬), 비어 있는 좌우 열은 잘라 냄."""
    if c in DIG:
        return DIG[c]
    hx = GLYPH[c]
    rows = [format(int(hx[k * 4:k * 4 + 4], 16), "016b") for k in range(16)]
    on = [x for x in range(16) if any(r[x] == "1" for r in rows)]
    return [r[min(on):max(on) + 1].replace("1", "#").replace("0", ".") for r in rows]


def text_rows(txt, gap=1):
    """글 → 줄 문자열 목록(켜진 칸 = '#'). 글자 사이 gap칸."""
    parts = [_glyph_rows(c) for c in txt]
    h = max(len(p) for p in parts)
    out = [""] * h
    for n, p in enumerate(parts):
        for r in range(h):
            out[r] += (p[r] if r < len(p) else "." * len(p[0])) + ("." * gap if n + 1 < len(parts) else "")
    return out


def cells(G, rows, c0, psi, cell, col, thick=0.02):
    """발광 상자 인스턴스로 도트 그림: rows의 '#'를 칸으로. c0 = 왼쪽 위 칸 가운데, psi = 가로줄 방향의 방위각(0 → +x쪽으로 읽힘, 정면 -y).
    같은 줄에서 이어진 칸은 상자 하나로 합침."""
    cp, sp = math.cos(psi), math.sin(psi)
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] != "#":
                c += 1
                continue
            c1 = c
            while c1 + 1 < len(row) and row[c1 + 1] == "#":
                c1 += 1
            m = (c + c1) / 2.0
            G.c((c0[0] + m * cell * cp, c0[1] + m * cell * sp, c0[2] - r * cell), ((c1 - c + 1) * cell - 0.06 * cell, thick, cell * 0.94), col,
                (0.0, 0.0, psi))
            c = c1 + 1


def vcells(v, rows, x, y, z, cell, col, face="y", glow=False, depth=0.03):
    """세트(Vox)에 도트 그림을 상자로 박음. face='y'면 -y쪽을 봄(가로 = +x), 'x'면 +x쪽을 봄(가로 = +y). (x, y, z) = 왼쪽 위 칸 가운데."""
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] != "#":
                c += 1
                continue
            c1 = c
            while c1 + 1 < len(row) and row[c1 + 1] == "#":
                c1 += 1
            z1, z0 = z - r * cell + cell / 2, z - r * cell - cell / 2
            if face == "y":
                v.box(x + (c - 0.5) * cell, x + (c1 + 0.5) * cell, y - depth, y, z0, z1, col, jit=0, glow=glow)
            else:
                v.box(x - depth, x, y + (c - 0.5) * cell, y + (c1 + 0.5) * cell, z0, z1, col, jit=0, glow=glow)
            c = c1 + 1


# ───────────────────────── 캐릭터 자세 (표준 자세 위에 팔·고개·입만 바꾼 원형 + 모자·후드·헬멧) ─────────────────────────
SITS = ("sit", "sit_phone", "sit_conf", "sit_read")
# base = 바탕 자세, arms = ((오른팔 앞뒤, 옆), (왼팔 앞뒤, 옆)) 어깨 회전각(앞뒤 음수 = 앞으로 듦, 양수 = 뒤로 젖힘, 옆: 오른팔 +가 몸 쪽·왼팔 +가 바깥),
# mouth = open/smile/frown, head = 고개 숙임(+)/젖힘(−)
KINDS = {
    "duck": dict(base="stand", arms=((2.5, 0.55), (2.5, -0.55)), head=0.15, mouth="open"),      # 두 손을 뒤통수에 (엎드릴 때 pitch를 줌)
    "point": dict(base="stand", arms=((-1.5, 0.0), (0.0, 0.0))),
    "dig": dict(base="stand", arms=((-0.9, 0.0), (-0.9, 0.0)), head=0.3),
    "read": dict(base="stand", arms=((-1.15, 0.0), (-1.15, 0.0)), head=0.35),
    "sit_read": dict(base="sit", arms=((-1.1, 0.0), (-1.1, 0.0)), head=0.35),
    "think": dict(base="stand", arms=((-2.7, 0.0), (0.0, 0.0)), head=0.1),
    "look_up": dict(base="stand", head=-0.45, mouth="smile"),
    "look_h": dict(base="stand", head=0.1, mouth="smile"),
    "wave": dict(base="stand", arms=((-2.4, 0.0), (0.0, 0.0)), mouth="smile"),
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
    sit = sp["base"] in SITS
    P = X._person(X.POSES[sp["base"]], lh)
    hip = 0.47 if sit else 0.78
    hz = hip + 0.58
    nl = 6 if sit else 4
    legs, torso, head, arms = P[:nl], P[nl], list(P[nl + 1:-4]), P[-4:]

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
    """표준 자세면 voxel 원형, 새 자세면 _variant. extra: 'hood'(도현 후드) · 'cap'(경비 모자) · 'helmet'(구조대 헬멧)."""
    from engine import bkit as K
    P = _variant(pose, bool(hair)) if pose in KINDS else X._person(X.POSES[pose], bool(hair))
    hz = hip_of(pose) + 0.58
    if extra == "hood":                                            # 목 뒤 후드 (셔츠 색)
        P.append((K.bm_cube(0.14, 0.40, 0.22, (-0.20, 0, hz - 0.13), bottom=True), 0))
    elif extra == "cap":                                           # 경비 모자: 남색(바지 색) 윗판 + 검은 챙
        P.append((K.bm_cube(0.52, 0.52, 0.10, (0, 0, hz + 0.455), bottom=True), 1))
        P.append((K.bm_cube(0.14, 0.44, 0.03, (0.30, 0, hz + 0.455), bottom=True), 5))
    elif extra == "helmet":                                        # 구조대 헬멧: 흰색 + 앞챙
        P.append((K.bm_cube(0.54, 0.54, 0.16, (-0.01, 0, hz + 0.40), bottom=True), 4))
        P.append((K.bm_cube(0.12, 0.40, 0.03, (0.28, 0, hz + 0.40), bottom=True), 4))
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
    then (τ, 바뀐 자세) · alt (자세A, 자세B, 주기, 위상) 번갈아 · seq [(τ, 자세)...] 자세 순서 · zfn x→바닥 높이 ·
    keys [(τ, (x, y, z, yaw, pitch))...] 부드럽게 이어지는 경로(있으면 x, y, yaw가 이걸로 정해짐) · ease 경로 보간(기본 부드럽게)."""
    return dict(set=set_, x=x, y=y, z=z, yaw=yaw, pose=pose, **kw)


_LIN = lambda u: u


def _poses_of(s):
    out = {s["pose"]}
    for k in ("pair", "alt"):
        if k in s:
            out |= set(s[k][:2])
    if "then" in s:
        out.add(s["then"][1])
    for _, p in s.get("seq", []):
        out.add(p)
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
    d["pitch"] = 0.0
    if "keys" in a:
        d["x"], d["y"], d["z"], d["yaw"], d["pitch"] = keyed(tau, a["keys"], a.get("ease", smooth))
        moving = tau < a["keys"][-1][0]
    else:
        vx, vy = a.get("v", (0.0, 0.0))
        tt = min(max(tau, 0.0), a.get("stop", 1e9))
        d["x"], d["y"] = a["x"] + vx * tt, a["y"] + vy * tt
        moving = (vx != 0.0 or vy != 0.0) and tau < a.get("stop", 1e9)
    if "zfn" in a:
        d["z"] = a["zfn"](d["x"])
    if "then" in a and tau >= a["then"][0]:
        d["pose"] = a["then"][1]
    for t0, p in a.get("seq", []):
        if tau >= t0:
            d["pose"] = p
    al = a.get("alt")
    if al:
        d["pose"] = al[int((t + al[3]) / al[2]) % 2]
    if moving and "pair" in a:
        cad = a.get("cad", 0.28)
        d["pose"] = a["pair"][int(t / cad) % 2]
        d["z"] += 0.03 * abs(math.sin(math.pi * t / cad))
    d["scale"] = c["scale"]
    return d


# ───────────────────────── 세트: 집 (거실·식탁 · 계단실) ─────────────────────────
RX0, RX1, RY0, RY1, RH = -4.5, 4.5, -7.0, 3.2, 2.7        # 거실 범위(앞 -y는 터짐)와 벽 높이
TB_X, TB_Y, TB_L, TB_W, TB_H = 0.0, 0.8, 2.0, 1.5, 0.76     # 식탁 가운데 · 길이(x) · 폭(y) · 높이
TV_Y0, TV_Y1, TV_Z0, TV_Z1 = -1.8, 0.6, 1.1, 2.3            # TV 화면 범위 (왼쪽 벽 x = RX0)
DOOR_Y = (-4.3, -3.3)                                       # 현관문 (오른쪽 벽)
CREAM, SAGE, OAK = (0.93, 0.90, 0.82), (0.86, 0.88, 0.80), (0.72, 0.54, 0.36)
WHITE = (0.95, 0.95, 0.93)


def _lamp_post(v, x, y, name, h=4.2, energy=230.0, col=(1.0, 0.85, 0.55)):
    """가로등: 기둥 + 머리 + 발광판. 점광원 이름은 env()가 켜고 끔."""
    v.box(x - 0.06, x + 0.06, y - 0.06, y + 0.06, 0, h, (0.25, 0.26, 0.28))
    v.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, h, h + 0.12, (0.25, 0.26, 0.28))
    v.box(x - 0.16, x + 0.16, y - 0.16, y + 0.16, h - 0.05, h, col, jit=0, glow=True)
    v.light(x, y, h - 0.3, energy, col, 0.3, name)


def _home(v):
    """거실·식탁 (낮): 나무 바닥 · 벽(창은 구멍이라 하늘이 보임) · 식탁과 의자 · TV벽 · 소파 · 주방 · 현관문 · 창밖 건물.
    컵·접시·펜던트·액자·TV 그래프는 매 프레임(흔들리고 떨어지니까) 소품으로."""
    v.floor(RX0, RX1, RY0, RY1, OAK, 0.25, "wood")
    for a, b, z0, z1 in (((RX0, RY1), (-1.8, RY1), 0, RH), ((1.8, RY1), (RX1, RY1), 0, RH),
                         ((-1.8, RY1), (1.8, RY1), 0, 0.9), ((-1.8, RY1), (1.8, RY1), 2.3, RH)):    # 뒷벽 (창 구멍 x -1.8~1.8, z 0.9~2.3)
        v.wall(a, b, z0, z1, CREAM, 0.5, face=-1)
    v.wall((RX0, RY0), (RX0, RY1), 0, RH, SAGE, 0.5, face=-1)
    v.wall((RX1, RY0), (RX1, RY1), 0, RH, SAGE, 0.5, face=1)
    # 창틀·커튼
    v.box(-1.9, 1.9, 3.0, 3.25, 0.84, 0.9, WHITE)
    v.box(-1.9, 1.9, 3.0, 3.25, 2.3, 2.38, WHITE)
    v.box(-1.9, -1.8, 3.0, 3.25, 0.9, 2.3, WHITE)
    v.box(1.8, 1.9, 3.0, 3.25, 0.9, 2.3, WHITE)
    v.box(-0.04, 0.04, 3.05, 3.2, 0.9, 2.3, WHITE)
    v.box(-2.6, -2.0, 3.0, 3.15, 0.1, 2.55, (0.90, 0.72, 0.70))
    v.box(2.0, 2.6, 3.0, 3.15, 0.1, 2.55, (0.90, 0.72, 0.70))
    # 창밖 도시 (멀리 낮은 건물 줄 · y를 조금씩 어긋나게)
    for k, x in enumerate(np.arange(-70.0, 70.0, 9.0)):
        v.box(x, x + 8.0, 40.0 + 0.9 * (k % 4), 52.0, 0, 6.0 + 7.0 * _h(k + 3), (0.40, 0.45, 0.56) if k % 2 else (0.47, 0.50, 0.58), jit=0.03)
    # 식탁 + 의자 (의자는 식탁에서 조금 뺌)
    X.table(v, TB_X, TB_Y, TB_L, TB_W, TB_H, (0.86, 0.72, 0.52))
    for x in (-0.5, 0.5):                                                                      # 카메라 쪽(앞)은 비워 둠
        X.chair(v, x, TB_Y + TB_W / 2 + 0.40, -90)
    # TV벽: TV장 · TV(검은 틀 + 화면) · 소파 · 탁자 · 러그
    v.box(RX0, RX0 + 0.45, -2.6, 1.6, 0, 0.5, (0.45, 0.32, 0.22))
    v.box(RX0 + 0.02, RX0 + 0.12, TV_Y0 - 0.12, TV_Y1 + 0.12, TV_Z0 - 0.1, TV_Z1 + 0.1, (0.07, 0.07, 0.08), jit=0)
    v.box(RX0 + 0.13, RX0 + 0.14, TV_Y0, TV_Y1, TV_Z0, TV_Z1, (0.012, 0.025, 0.040), jit=0, glow=True)
    for z in (1.4, 1.7, 2.0):                                                                  # 화면 눈금
        v.box(RX0 + 0.14, RX0 + 0.145, TV_Y0, TV_Y1, z - 0.004, z + 0.004, (0.05, 0.16, 0.22), jit=0, glow=True)
    v.box(-3.5, -2.6, -1.9, 1.3, 0, 0.45, (0.30, 0.50, 0.55))                                  # 소파
    v.box(-2.78, -2.6, -1.9, 1.3, 0.45, 0.95, (0.27, 0.46, 0.51))
    for y0 in (-2.0, 1.2):
        v.box(-3.5, -2.64, y0, y0 + 0.14, 0.45, 0.72, (0.27, 0.46, 0.51))
    v.box(-2.3, -1.7, -0.9, 0.3, 0, 0.4, (0.60, 0.45, 0.30))
    v.box(-3.4, -0.9, -1.8, 1.2, 0.0, 0.02, (0.78, 0.62, 0.55), jit=0.02)
    v.box(-4.3, -4.0, 2.3, 2.6, 0, 1.4, (0.35, 0.30, 0.25))                                    # 스탠드
    v.box(-4.4, -3.9, 2.2, 2.7, 1.4, 1.65, (1.0, 0.9, 0.7), jit=0, glow=True)
    # 주방 (오른쪽 벽): 조리대 · 윗장 · 냉장고
    v.box(3.6, RX1, -1.2, 2.0, 0, 0.9, (0.93, 0.93, 0.91))
    v.box(3.58, RX1, -1.2, 2.0, 0.9, 0.95, (0.55, 0.57, 0.60))
    v.box(3.9, RX1, 0.0, 3.2, 1.55, 2.25, (0.93, 0.93, 0.91))
    v.box(3.5, RX1, 2.0, 3.2, 0, 1.95, (0.82, 0.84, 0.87))
    # 현관문 (오른쪽 벽) + 신발장
    v.box(RX1 - 0.07, RX1 - 0.02, DOOR_Y[0], DOOR_Y[1], 0, 2.1, (0.55, 0.38, 0.25), jit=0.02)
    v.box(RX1 - 0.09, RX1 - 0.07, DOOR_Y[0] - 0.06, DOOR_Y[1] + 0.06, 0, 2.16, (0.88, 0.88, 0.85), jit=0)
    v.box(RX1 - 0.12, RX1 - 0.07, DOOR_Y[1] - 0.14, DOOR_Y[1] - 0.10, 1.0, 1.1, (0.8, 0.8, 0.82), jit=0)
    v.box(3.9, 4.4, -2.9, -2.1, 0, 0.45, (0.82, 0.72, 0.58))
    # 불빛 (펜던트 점광원은 매 프레임 따라감)
    v.light(0.0, 0.8, 1.7, 70, (1.0, 0.88, 0.70), 0.3, "ep36_h_pend")
    v.light(0.0, -3.0, 2.4, 110, (1.0, 0.96, 0.88), 0.6, "ep36_h_fill")
    v.light(3.2, -2.4, 2.3, 60, (1.0, 0.96, 0.88), 0.6, "ep36_h_fill2")
    v.light(-2.5, -1.0, 2.5, 50, (0.95, 0.97, 1.0), 0.6, "ep36_h_tv")


STEP_N, STEP_RISE, STEP_RUN = 9, 0.2, 0.3
STAIR_TOP = STEP_N * STEP_RISE + 0.2                        # 위층 복도 바닥 높이 2.0
STAIR_X1 = STEP_N * STEP_RUN                                # 계단이 끝나는 x (아래 층 바닥 시작)


def stair_z(x):
    """계단실 바닥 높이 (x는 HX_ST 기준 지역 좌표): 위층 2.0 → 한 칸씩 내려가 0."""
    if x <= 0.0:
        return STAIR_TOP
    if x >= STAIR_X1:
        return 0.0
    return STAIR_TOP - STEP_RISE * (int(x / STEP_RUN) + 1)


def _stairs(v):
    """계단실 (집 세트 안 x=HX_ST, 지역 좌표): 위층 복도(z 2.0) · 엘리베이터(빨간 X 표지) · 계단 아홉 칸 · 아래 출입구(z 0)."""
    conc, stl = (0.66, 0.67, 0.70), (0.72, 0.75, 0.80)
    v.box(-3.5, 0.0, -1.2, 2.0, 0, STAIR_TOP, (0.74, 0.72, 0.68))                   # 위층 복도 바닥
    for k in range(STEP_N):
        v.box(STEP_RUN * k, STEP_RUN * (k + 1), 0.0, 2.0, 0, STAIR_TOP - STEP_RISE * (k + 1), (0.70, 0.68, 0.64))
    v.floor(STAIR_X1, 7.0, -1.2, 2.0, (0.72, 0.70, 0.66), 0.5, "check")                 # 아래 층 바닥
    v.floor(0.0, STAIR_X1, -1.2, 0.0, (0.72, 0.70, 0.66), 0.5, "check")                 # 계단 앞 옆 바닥
    v.floor(-3.5, 7.0, -9.0, -1.2, (0.70, 0.68, 0.64), 0.5, "check")                    # 앞 바닥(카메라 아래가 하늘로 안 보이게)
    v.wall((-3.5, 2.0), (7.0, 2.0), 0, 5.4, conc, 0.5, face=-1)
    v.wall((-3.5, -1.2), (-3.5, 2.0), 0, 5.4, conc, 0.5, face=-1)
    v.wall((7.0, -1.2), (7.0, 2.0), 0, 5.4, conc, 0.5, face=1)
    # 엘리베이터 문 (위층 뒷벽) + 빨간 X 표지
    v.box(-2.4, -1.75, 1.93, 1.97, STAIR_TOP, STAIR_TOP + 2.1, stl, jit=0.01)
    v.box(-1.75, -1.1, 1.93, 1.97, STAIR_TOP, STAIR_TOP + 2.1, stl, jit=0.01)
    v.box(-2.48, -2.4, 1.91, 1.97, STAIR_TOP, STAIR_TOP + 2.18, (0.30, 0.31, 0.34), jit=0)
    v.box(-1.1, -1.02, 1.91, 1.97, STAIR_TOP, STAIR_TOP + 2.18, (0.30, 0.31, 0.34), jit=0)
    v.box(-2.48, -1.02, 1.90, 1.97, STAIR_TOP + 2.1, STAIR_TOP + 2.2, (0.30, 0.31, 0.34), jit=0)
    v.box(-0.92, -0.78, 1.93, 1.96, STAIR_TOP + 1.0, STAIR_TOP + 1.2, (0.9, 0.9, 0.9), jit=0)
    vcells(v, ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"], -2.09, 1.93, STAIR_TOP + 1.72, 0.17, (3.2, 0.3, 0.25), "y", True)       # 문 위 큰 빨간 X
    # 계단 안내 (초록 화살표 표지)
    v.box(0.5, 1.5, 1.90, 1.93, STAIR_TOP + 1.4, STAIR_TOP + 2.0, (0.04, 0.12, 0.08), jit=0)
    vcells(v, ["..#....", "..##...", "#######", "..##...", "..#...."], 0.6, 1.90, STAIR_TOP + 1.85, 0.11, (0.5, 3.0, 0.9), "y", True)
    # 난간 (칸마다 기둥 + 짧은 윗대)
    for k in range(STEP_N):
        zt = STAIR_TOP - STEP_RISE * (k + 1)
        v.box(STEP_RUN * k + 0.12, STEP_RUN * k + 0.18, -0.06, -0.02, zt, zt + 0.9, (0.25, 0.26, 0.30), jit=0)
        v.box(STEP_RUN * k, STEP_RUN * (k + 1), -0.065, -0.015, zt + 0.88, zt + 0.92, (0.35, 0.36, 0.42), jit=0)
    # 아래 출입구 (뒷벽 오른쪽): 문 + 초록 비상구 표지
    v.box(5.5, 6.6, 1.93, 1.97, 0, 2.1, (0.58, 0.40, 0.26))
    v.box(5.42, 5.5, 1.91, 1.97, 0, 2.18, (0.30, 0.31, 0.34), jit=0)
    v.box(6.6, 6.68, 1.91, 1.97, 0, 2.18, (0.30, 0.31, 0.34), jit=0)
    v.box(5.42, 6.68, 1.90, 1.97, 2.1, 2.2, (0.30, 0.31, 0.34), jit=0)
    v.box(5.55, 6.55, 1.90, 1.93, 2.35, 2.9, (0.04, 0.12, 0.08), jit=0)
    vcells(v, ["..#..", ".###.", "#####", "..#..", "..#.."], 5.75, 1.90, 2.80, 0.12, (0.5, 3.0, 0.9), "y", True)
    v.light(-1.5, 0.5, STAIR_TOP + 2.6, 90, (1.0, 0.96, 0.88), 0.4, "ep36_st_a")
    v.light(3.5, -0.4, 2.8, 110, (1.0, 0.96, 0.88), 0.5, "ep36_st_b")
    v.light(0.8, -2.2, 3.4, 120, (1.0, 0.96, 0.88), 0.8, "ep36_st_c")


# ───────────────────────── 세트: 체육관 · 교실 · 교문 · 거리 · 실험 무대 ─────────────────────────
CUB_X, CUB_Y = (-5.4, -1.8, 1.8, 5.4), (1.0, 4.6)           # 체육관 칸막이 텐트 가운데 (열 4 × 줄 2)
CUB_H = 1.0


def _gym(v):
    """체육관 대피소 (낮): 나무 마루 · 농구 골대 · 높은 창 · 천장 조명 · 칸막이 텐트 8칸(바닥 매트) · 구호 물품 탁자."""
    v.floor(-9.5, 9.5, -12.0, 8.0, (0.80, 0.62, 0.40), 0.5, "wood")
    for x in (-8.4, 8.4):
        v.box(x - 0.04, x + 0.04, -7.0, 7.4, 0, 0.012, (0.95, 0.93, 0.85), jit=0)
    v.box(-8.4, 8.4, 7.36, 7.44, 0, 0.013, (0.95, 0.93, 0.85), jit=0)
    v.wall((-9.5, 8.0), (9.5, 8.0), 0, 6.0, (0.90, 0.88, 0.82), 1.0, face=-1)
    v.wall((-9.5, -12.0), (-9.5, 8.0), 0, 6.0, (0.88, 0.86, 0.80), 1.0, face=-1)
    v.wall((9.5, -12.0), (9.5, 8.0), 0, 6.0, (0.88, 0.86, 0.80), 1.0, face=1)
    v.box(-9.49, -9.44, -12.0, 8.0, 0, 1.2, (0.25, 0.40, 0.66))
    v.box(9.44, 9.49, -12.0, 8.0, 0, 1.2, (0.25, 0.40, 0.66))
    v.box(-9.5, 9.5, 7.94, 7.99, 0, 1.201, (0.25, 0.40, 0.66))
    for x in (-7.5, -4.5, 4.5, 7.5):
        v.box(x - 1.0, x + 1.0, 7.95, 7.97, 3.6, 5.3, (0.55, 0.75, 0.95), jit=0, glow=True)
    v.box(-0.9, 0.9, 7.70, 7.74, 3.0, 4.0, WHITE)                                      # 농구 골대
    v.box(-0.3, 0.3, 7.67, 7.70, 3.1, 3.5, (0.85, 0.2, 0.2), jit=0)
    v.box(-0.3, 0.3, 7.2, 7.7, 2.95, 2.99, (0.95, 0.5, 0.15), jit=0)
    v.box(-0.04, 0.04, 7.74, 8.0, 3.0, 3.12, (0.3, 0.3, 0.32), jit=0)
    for x in (-5.4, -1.8, 1.8, 5.4):                                                   # 매달린 조명판(줄 + 판)
        for y in (1.0, 4.6):
            v.box(x - 0.8, x + 0.8, y - 0.3, y + 0.3, 5.4, 5.45, (1.0, 1.0, 0.95), jit=0, glow=True)
            v.box(x - 0.02, x + 0.02, y - 0.02, y + 0.02, 5.45, 6.0, (0.25, 0.25, 0.28), jit=0)
    mats = [(0.35, 0.60, 0.45), (0.80, 0.50, 0.35), (0.40, 0.50, 0.75), (0.75, 0.65, 0.35)]
    for ix, cx in enumerate(CUB_X):
        for iy, cy in enumerate(CUB_Y):
            v.box(cx - 1.35, cx + 1.35, cy - 1.15, cy + 1.15, 0, 0.05, mats[(ix + iy) % 4])            # 바닥 매트
            v.box(cx - 1.5, cx - 1.45, cy - 1.2, cy + 1.3, 0, CUB_H, (0.60, 0.68, 0.78), jit=0.05)     # 칸막이 텐트(양옆·뒤)
            v.box(cx + 1.45, cx + 1.5, cy - 1.2, cy + 1.3, 0, CUB_H, (0.60, 0.68, 0.78), jit=0.05)
            v.box(cx - 1.45, cx + 1.45, cy + 1.25, cy + 1.3, 0, CUB_H + 0.01, (0.55, 0.63, 0.74), jit=0.05)
    for cx, cy, c in ((-5.4, 1.0, (0.88, 0.45, 0.30)), (1.8, 4.6, (0.88, 0.45, 0.30)), (-1.8, 4.6, (0.45, 0.60, 0.85))):    # 담요 더미
        v.box(cx + 0.7, cx + 1.2, cy - 0.9, cy - 0.3, 0.05, 0.25, c)
    X.table(v, 6.2, -3.0, 2.2, 0.8, 0.75, (0.92, 0.92, 0.90))                               # 구호 물품 탁자 (물·담요)
    for k in range(5):
        v.box(5.3 + 0.38 * k, 5.62 + 0.38 * k, -3.25, -2.75, 0.75, 1.0, (0.35, 0.6, 0.9))
    v.box(7.0, 7.5, -3.3, -2.7, 0.75, 1.15, (0.95, 0.55, 0.25))
    for x, y in ((-3.6, 7.0), (3.6, 7.0)):
        v.box(x - 0.5, x + 0.5, y - 0.4, y + 0.4, 0, 0.6, (0.62, 0.50, 0.35))
    for k, (x, y) in enumerate(((-2.2, 2.8), (0.0, 2.8), (2.2, 2.8))):                         # 가운데 통로 보급 상자
        v.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, 0, 0.35, (0.70, 0.55, 0.38), jit=0.06)
    for k, (x, y) in enumerate(((-3.6, -1.5), (3.6, -1.5), (0.0, -1.5), (-6.0, -2.4), (6.0, -0.5))):
        v.light(x, y, 4.8, 120, (1.0, 0.97, 0.90), 0.8, "ep36_g%d" % k)


def _class(v):
    """교실 (낮): 마루 · 칠판('휴교') · 책상 열여섯 · 닫힌 문(안전점검 노란 테이프, 계단식 점 대각선) · 오른쪽 창."""
    v.floor(-4.5, 4.5, -7.0, 4.5, (0.80, 0.68, 0.48), 0.5, "wood")
    v.wall((-4.5, 4.5), (4.5, 4.5), 0, 3.0, (0.92, 0.92, 0.86), 0.5, face=-1)
    v.wall((-4.5, -7.0), (-4.5, 4.5), 0, 3.0, (0.88, 0.90, 0.85), 0.5, face=-1)
    v.wall((4.5, -7.0), (4.5, 4.5), 0, 3.0, (0.88, 0.90, 0.85), 0.5, face=1)
    for y0, y1 in ((-4.4, -2.8), (-2.2, -0.6), (0.0, 1.6)):
        v.window(y0, y1, 4.5, 0.9, 2.5, night=False, face=-1, axis="x")
    v.box(-3.3, -0.1, 4.43, 4.5, 0.85, 2.35, (0.08, 0.25, 0.18), jit=0.02)                           # 칠판 + 틀
    v.box(-3.36, -0.04, 4.41, 4.45, 0.80, 0.85, (0.55, 0.42, 0.28), jit=0)
    v.box(-3.36, -0.04, 4.41, 4.45, 2.35, 2.40, (0.55, 0.42, 0.28), jit=0)
    vcells(v, text_rows("휴교"), -2.54, 4.40, 2.25, 0.06, (0.96, 0.96, 0.90), "y", False, 0.02)    # 분필 글씨
    for x in (-3.0, -1.0, 1.0, 3.0):
        for k, y in enumerate((-2.8, -1.4, 0.0, 1.4)):
            X.table(v, x, y, 0.7, 0.5, 0.72, (0.86, 0.76, 0.56))
            X.chair(v, x, y - 0.55, 90, (0.45, 0.55, 0.70), 0.43)
            if (int(x) + k) % 3 == 0:
                v.box(x - 0.2, x + 0.1, y - 0.15, y + 0.1, 0.72, 0.77, ((0.85, 0.3, 0.3), (0.3, 0.55, 0.85), (0.95, 0.8, 0.3))[k % 3])
    v.box(0.6, 1.7, 4.42, 4.5, 0, 2.1, (0.55, 0.40, 0.28))                                          # 닫힌 문
    v.box(0.52, 0.6, 4.40, 4.5, 0, 2.18, (0.88, 0.88, 0.85), jit=0)
    v.box(1.7, 1.78, 4.40, 4.5, 0, 2.18, (0.88, 0.88, 0.85), jit=0)
    v.box(0.52, 1.78, 4.395, 4.5, 2.1, 2.2, (0.88, 0.88, 0.85), jit=0)
    v.box(0.85, 1.45, 4.40, 4.42, 1.35, 1.9, (0.55, 0.70, 0.80), jit=0)
    for n, (yy, flip) in enumerate(((4.36, 1), (4.32, -1))):                                          # 안전점검 노란 테이프: X 모양, 한 칸씩 어긋난 점 상자
        for k in range(24):
            z = 0.22 + 0.075 * k
            xx = 0.45 + (1.40 * k / 23 if flip > 0 else 1.40 - 1.40 * k / 23)
            c = (0.97, 0.80, 0.08) if (k // 2) % 2 == 0 else (0.08, 0.08, 0.10)
            v.box(xx - 0.07, xx + 0.07, yy + 0.004 * (k % 2), yy + 0.03 + 0.004 * (k % 2), z - 0.05, z + 0.05, c, jit=0)
    for k, x in enumerate((-2.5, 0.0, 2.5)):
        v.light(x, -0.5, 2.7, 80, (1.0, 0.98, 0.92), 0.6, "ep36_c%d" % k)
    v.light(0.0, -4.5, 2.5, 90, (1.0, 0.98, 0.92), 0.6, "ep36_c3")


def _gate_area(v, fx):
    """교문 앞 한 구역 (x 기준 fx): 학교 건물 + 담."""
    v.box(fx - 22, fx + 22, 9.0, 16.0, 0, 11.0, (0.80, 0.72, 0.62), jit=0.03)
    rs = v.rs
    for r in range(4):
        for k in range(14):
            on = rs.random() < 0.55
            c = (0.95, 0.80, 0.50) if on else (0.18, 0.24, 0.34)
            v.box(fx - 20.6 + 3.0 * k, fx - 18.8 + 3.0 * k, 8.97, 9.0, 1.2 + 2.5 * r, 2.6 + 2.5 * r, c, jit=0, glow=on)


def _gate(v):
    """교문 (새벽 → 밤): 보도 · 학교 건물 · 교문 기둥과 현수막('수능') · 안내판('연기') · 가로등 · 나무. 밤 가로등 자리(GT_LAMP)는 같은 세트 안 x로 떨어진 곳."""
    ox, oy = OFF["gate"]
    v.floor(-30, 90, -14, 6, (0.58, 0.58, 0.60), 1.0, "check")
    v.floor(-30, 90, 6, 9, (0.72, 0.66, 0.55), 1.0, "check")
    _gate_area(v, 0.0)
    _gate_area(v, GT_LAMP)
    for sx in (-1, 1):                                                                              # 교문 기둥 · 담
        v.box(sx * 3.0 - 0.3, sx * 3.0 + 0.3, 4.7, 5.3, 0, 3.0, (0.80, 0.77, 0.72))
        v.box(sx * 3.0 - 0.4, sx * 3.0 + 0.4, 4.6, 5.4, 3.0, 3.15, (0.70, 0.67, 0.62))
        v.box(sx * 3.3 if sx > 0 else -30.0, 30.0 if sx > 0 else sx * 3.3, 4.9, 5.2, 0, 1.5, (0.70, 0.45, 0.38))
        for k in range(7):                                                                          # 열린 철문 창살
            x = sx * (2.55 - 0.2 * k)
            v.box(x - 0.025, x + 0.025, 4.95, 5.0, 0, 1.7, (0.15, 0.17, 0.20), jit=0)
    v.box(-3.3, 3.3, 4.82, 4.9, 3.25, 4.35, (0.78, 0.10, 0.12))                                      # 빨간 현수막 + 흰 글씨
    vcells(v, text_rows("수능"), -0.95, 4.82, 4.22, 0.065, (0.97, 0.97, 0.94), "y", False, 0.02)
    v.box(-1.0, 1.0, 1.50, 1.56, 0.65, 1.80, (0.96, 0.96, 0.93))                                    # 안내판 '연기'
    for x in (-0.82, 0.76):
        v.box(x, x + 0.06, 1.50, 1.56, 0, 0.65, (0.35, 0.35, 0.38), jit=0)
    vcells(v, text_rows("연기"), -0.72, 1.50, 1.70, 0.05, (0.85, 0.08, 0.10), "y", False, 0.02)
    for x in (-8.0, 8.0, -14.0, 14.0):
        X.tree(v, x, 3.2)
    _lamp_post(v, -5.0, 0.5, "ep36_gt_l1", 3.6, 160, (1.0, 0.85, 0.55))
    _lamp_post(v, 5.0, 0.5, "ep36_gt_l2", 3.6, 160, (1.0, 0.85, 0.55))
    v.at(ox + GT_LAMP, oy)                                                                           # 밤 가로등 자리: 벤치 + 가로등 + 나무
    v.box(-1.3, 1.3, 1.0, 1.45, 0.38, 0.43, (0.50, 0.34, 0.20))
    v.box(-1.3, 1.3, 1.42, 1.5, 0.43, 0.88, (0.50, 0.34, 0.20))
    for x in (-1.15, 1.1):
        v.box(x, x + 0.06, 1.05, 1.4, 0, 0.38, (0.25, 0.26, 0.28), jit=0)
    _lamp_post(v, -2.0, 0.3, "ep36_lp", 3.2, 260, (1.0, 0.85, 0.55))
    for x in (-5.0, 5.0):
        X.tree(v, x, 3.2)
    v.box(-8, 8, 3.6, 4.1, 0, 0.9, (0.14, 0.28, 0.14))
    v.at(ox, oy)


def _street(v):
    """거리 (낮): 차도 · 보도 · 낡은 건물 + 비계(주황 기둥·널·난간) · 이동식 크레인 차 · 새 건물. 크레인 붐·줄·보는 매 프레임."""
    v.floor(-45, 45, -15, 1.0, (0.30, 0.30, 0.33), 1.0)
    for x in np.arange(-44.0, 44.0, 4.0):
        v.box(x, x + 2.0, -4.06, -3.94, 0, 0.012, (0.95, 0.95, 0.9), jit=0)
    v.box(-45, 45, 1.0, 4.2, 0, 0.12, (0.62, 0.62, 0.62), jit=0)
    v.floor(-45, 45, 1.0, 4.2, (0.74, 0.70, 0.64), 1.0, "check", z=0.121)
    v.box(-9, 3, 4.2, 10, 0, 7.2, (0.76, 0.70, 0.60), jit=0.03)                                       # 낡은 건물
    v.box(-9.1, 3.1, 4.1, 10.1, 7.2, 7.4, (0.55, 0.50, 0.45))
    for r in range(3):
        for k in range(6):
            x = -8.3 + 2.0 * k
            v.box(x, x + 1.1, 4.16, 4.2, 0.9 + 2.3 * r, 2.2 + 2.3 * r, (0.22, 0.30, 0.42), jit=0.03)
    v.box(-3.15, -2.35, 4.14, 4.2, 0, 2.2, (0.55, 0.40, 0.28))
    for k in range(7):                                                                                 # 비계 기둥 (앞·뒤 두 줄)
        x = -8.6 + 1.8 * k
        for y in (3.4, 4.05):
            v.box(x - 0.04, x + 0.04, y - 0.04, y + 0.04, 0, 8.5, (0.92, 0.55, 0.12), jit=0.02)
    for z in (2.4, 4.8, 7.2):                                                                          # 널 · 난간
        v.box(-8.8, 2.4, 3.4, 4.05, z, z + 0.06, (0.70, 0.55, 0.35), jit=0.03)
        v.box(-8.8, 2.4, 3.365, 3.435, z + 0.95, z + 1.0, (0.92, 0.55, 0.12), jit=0)
        v.box(-8.8, 2.4, 3.365, 3.435, z + 0.5, z + 0.55, (0.92, 0.55, 0.12), jit=0)
    v.box(-8.8, 2.4, 3.3, 3.32, 7.2, 8.2, (0.45, 0.75, 0.45), jit=0.02)                                # 맨 위 안전망
    v.box(2.0, 8.5, -2.2, 0.2, 0.55, 1.35, (0.95, 0.75, 0.12))                                         # 크레인 차 몸통
    v.box(7.6, 8.9, -2.15, 0.15, 0.55, 2.2, (0.95, 0.75, 0.12))
    v.box(8.4, 8.92, -1.9, -0.1, 1.45, 2.1, (0.55, 0.75, 0.85), jit=0)
    v.box(3.3, 5.0, -1.7, -0.1, 1.35, 2.0, (0.30, 0.31, 0.34))                                         # 회전대
    for x in (3.0, 4.3, 7.8):
        v.box(x - 0.5, x + 0.5, -2.35, -2.0, 0, 1.0, (0.08, 0.08, 0.1), jit=0)
        v.box(x - 0.5, x + 0.5, 0.0, 0.35, 0, 1.0, (0.08, 0.08, 0.1), jit=0)
    for x, y in ((0.5, -1.5), (0.9, -1.5), (1.3, -1.5), (-0.5, -2.2)):                                 # 고깔
        v.box(x - 0.12, x + 0.12, y - 0.12, y + 0.12, 0, 0.5, (0.95, 0.45, 0.1))
    v.box(8.0, 17.0, 4.2, 10, 0, 9.5, (0.74, 0.78, 0.84), jit=0.02)                                    # 새 건물
    v.box(7.9, 17.1, 4.1, 10.1, 9.5, 9.7, (0.55, 0.60, 0.68))
    for r in range(4):
        v.box(8.4, 16.6, 4.17, 4.2, 1.4 + 2.0 * r, 2.5 + 2.0 * r, (0.30, 0.45, 0.62), jit=0.02)
    v.box(11.6, 13.4, 4.12, 4.2, 0, 2.3, (0.30, 0.40, 0.55))
    for x in (-14.0, 5.5, 20.0):
        X.tree(v, x, 3.6)
    v.light(0.0, -3.0, 5.0, 300, (1.0, 0.97, 0.90), 1.0, "ep36_sr_fill")


LB_BAR = 0.0


def _lab(v):
    """실험 무대 (스튜디오): 먼 배경 벽 · 막대 방(천장 포함) · 건물 모형 무대(LB_CITY) · 땅속 단면 모형(LB_UG).
    밝기는 해(스튜디오 조명)와 주변광으로."""
    ox, oy = OFF["lab"]
    v.wall((-14, 12), (140, 12), -5, 11, (0.16, 0.20, 0.32), 1.0, face=-1)
    v.floor(-14, 30, -14, 12, (0.34, 0.38, 0.48), 1.0, "check")
    v.floor(40, 80, -14, 12, (0.34, 0.38, 0.48), 1.0, "check")
    v.floor(100, 140, -14, 12, (0.20, 0.23, 0.30), 1.0, "check", z=-3.6)
    # 막대 방: 양옆·뒤 벽 + 천장판 (z 3.25~3.4) — 7.0 막대가 닿는 곳
    wl = (0.80, 0.82, 0.86)
    v.wall((-2.9, -1.3), (-2.9, 1.5), 0, 3.25, wl, 0.5, face=-1)
    v.wall((2.9, -1.3), (2.9, 1.5), 0, 3.25, wl, 0.5, face=1)
    v.wall((-2.9, 1.5), (2.9, 1.5), 0, 3.25, (0.74, 0.78, 0.84), 0.5, face=-1)
    v.box(-3.0, 3.0, -1.4, 1.6, 3.25, 3.4, (0.60, 0.62, 0.66), jit=0.02)
    v.box(-2.9, 2.9, -1.2, 1.4, 0, 0.02, (0.20, 0.22, 0.30), jit=0)
    v.light(0.0, -3.0, 3.0, 160, (1.0, 0.97, 0.92), 1.0, "ep36_l0")
    # 땅속 단면 모형: 층층이 색이 다른 흙·바위 + 지열발전소(탑 · 건물)
    cx = LB_UG
    layers = ((-0.15, 0.0, (0.35, 0.62, 0.28)), (-0.9, -0.15, (0.50, 0.34, 0.20)), (-1.8, -0.9, (0.62, 0.45, 0.28)),
              (-2.6, -1.8, (0.66, 0.60, 0.52)), (-3.6, -2.6, (0.45, 0.47, 0.54)))
    for z0, z1, c in layers:
        v.box(cx - 3.2, cx + 3.2, -0.1, 1.6, z0, z1, c, jit=0.07)
    for sx in (-0.35, 0.35):                                                                           # 탑(데릭): 기둥 넷 · 고리
        for sy in (0.25, 0.85):
            v.box(cx + sx - 0.04, cx + sx + 0.04, sy - 0.04, sy + 0.04, 0, 2.0, (0.85, 0.55, 0.15), jit=0.02)
    for z in (0.4, 1.0, 1.6):
        v.box(cx - 0.39, cx + 0.39, 0.20, 0.30, z, z + 0.05, (0.85, 0.55, 0.15), jit=0)
        v.box(cx - 0.39, cx + 0.39, 0.80, 0.90, z, z + 0.05, (0.85, 0.55, 0.15), jit=0)
    v.box(cx - 0.45, cx + 0.45, 0.15, 0.95, 2.0, 2.12, (0.30, 0.31, 0.34))
    v.box(cx + 1.2, cx + 2.8, 0.2, 1.3, 0, 0.8, (0.92, 0.93, 0.95))                                    # 발전소 건물
    v.box(cx + 1.15, cx + 2.85, 0.15, 1.35, 0.8, 0.9, (0.25, 0.45, 0.70))
    v.box(cx + 2.3, cx + 2.6, 0.6, 0.9, 0.9, 1.7, (0.65, 0.66, 0.70))                                  # 굴뚝
    v.box(cx - 2.8, cx - 1.6, 0.4, 1.2, 0, 0.5, (0.78, 0.78, 0.80))                                    # 저장 탱크
    # 건물 모형 무대는 위치만 (건물은 매 프레임). 무대 바닥에 눈금선
    for k in range(-5, 6):
        v.box(LB_CITY + k * 0.9 - 0.01, LB_CITY + k * 0.9 + 0.01, -1.6, 1.8, 0, 0.015, (0.20, 0.26, 0.38), jit=0)


def _home_all(v):
    """집 세트 = 거실(0) + 계단실(HX_ST)이 x로 나란히."""
    ox, oy = OFF["home"]
    _home(v)
    v.at(ox + HX_ST, oy)
    _stairs(v)
    v.at(ox, oy)


def _sets():
    return (("home", _home_all), ("gym", _gym), ("class", _class), ("gate", _gate), ("street", _street), ("lab", _lab))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL · 점광원 LT) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 200, 400, 24, 8
LABX = OFF['lab'][0]
GREEN_G, RED_G, YEL_G, CYAN_G, WARM_G = (0.25, 2.0, 0.5), (3.2, 0.35, 0.3), (3.4, 2.8, 0.5), (0.6, 2.4, 3.2), (3.2, 2.2, 1.0)
G_ACC = 9.8


def _lt(LT, name, pos, en):
    LT.append((tuple(float(q) for q in pos), name, float(en)))


# ── 집 식탁 위 물건 · 펜던트 · 액자 · 먼지 (규모 7이 오는 동안 흔들려 떨어짐)
# (종류, 크기, 색, x, y, 미끄러지기 시작하는 때, 속도 x, 속도 y, 도는 속도, 떨어진 뒤 눕는지)
ITEMS = [
    ("plate", (0.38, 0.38, 0.035), (0.97, 0.97, 0.94), -0.55, 1.05, 0.10, -0.35, -1.25, 5.0, 0),
    ("plate", (0.38, 0.38, 0.035), (0.97, 0.97, 0.94), 0.45, 1.20, 0.20, 0.55, -1.05, -6.0, 0),
    ("plate", (0.38, 0.38, 0.035), (0.92, 0.95, 0.99), 0.05, 0.60, 0.00, 0.05, -1.55, 4.0, 0),
    ("cup", (0.11, 0.11, 0.14), (0.92, 0.25, 0.20), -0.25, 0.95, 0.05, -0.75, -0.85, 9.0, 1),
    ("cup", (0.11, 0.11, 0.14), (0.25, 0.50, 0.92), 0.75, 0.85, 0.15, 0.85, -0.55, -8.0, 1),
    ("cup", (0.11, 0.11, 0.14), (0.97, 0.82, 0.25), -0.80, 0.55, 0.10, -1.10, -0.30, 7.0, 1),
    ("bowl", (0.28, 0.28, 0.12), (0.95, 0.55, 0.25), 0.25, 0.45, 0.00, 0.00, -0.07, 3.0, 0),
    ("bottle", (0.10, 0.10, 0.32), (0.40, 0.82, 0.96), 0.90, 1.15, 0.30, 0.90, 0.40, 0.0, 1),
    ("apple", (0.10, 0.10, 0.10), (0.90, 0.18, 0.15), -0.30, 0.30, 0.90, -0.30, -1.10, 6.0, 0),
    ("apple", (0.10, 0.10, 0.10), (0.90, 0.18, 0.15), 0.60, 1.25, 1.30, 0.55, 0.70, 6.0, 0),
    ("apple", (0.10, 0.10, 0.10), (0.55, 0.78, 0.20), -0.10, 1.10, 1.70, -0.95, -0.35, 6.0, 0),
]
EDGE_Y0, EDGE_X = TB_Y - TB_W / 2, TB_L / 2          # 식탁 가장자리 (앞 y, 양 끝 |x|)


def _exit_time(it):
    """물건이 식탁 가장자리를 넘어 떨어지기 시작하는 때(초). 안 떨어지면 큰 수."""
    _, _, _, x0, y0, ts, vx, vy, _, _ = it[:10]
    ts_ = []
    if vy < -0.2:
        ts_.append((y0 - EDGE_Y0) / -vy)
    if vy > 0.2:
        ts_.append((TB_Y + TB_W / 2 - y0) / vy)
    if abs(vx) > 0.2:
        ts_.append((EDGE_X - x0 * (1 if vx > 0 else -1)) / abs(vx))
    return ts + min(ts_) if ts_ else 1e9


def item_pose(it, T, quaking=True):
    """식탁 위 물건 하나의 (중심 x, y, z, 오일러 회전) — 사건 시각 T(초). quaking=False면 가만히 놓인 모습."""
    kind, size, col, x0, y0, ts, vx, vy, spin, lay = it
    top = TB_H + size[2] / 2
    if not quaking:
        return x0, y0, top, (0.0, 0.0, 0.0)
    te = _exit_time(it)
    if T < te:                                                       # 식탁 위: 덜덜 떨며 미끄러짐
        s = max(T - ts, 0.0)
        ph = 3.1 * x0 + 1.7 * y0
        vib = 0.012 if T < 3.0 else 0.0
        return (x0 + vx * s + vib * math.sin(2 * math.pi * 13 * T + ph), y0 + vy * s + vib * math.sin(2 * math.pi * 11 * T + 2 * ph), top,
                (0.05 * math.sin(2 * math.pi * 12 * T + ph), 0.05 * math.sin(2 * math.pi * 10 * T), math.radians(spin) * T))
    tau = T - te                                                     # 가장자리를 넘음: 포물선으로 떨어지고 한 번 튕김
    xe, ye = x0 + vx * (te - ts), y0 + vy * (te - ts)
    zf = size[0] / 2 if lay else size[2] / 2
    tf = math.sqrt(2 * max(top - zf, 0.0) / G_ACC)
    if tau < tf:
        z, hd = top - 0.5 * G_ACC * tau * tau, 0.7 * tau
    else:
        t2 = tau - tf
        vb = 0.28 * G_ACC * tf
        z = zf + max(vb * t2 - 0.5 * G_ACC * t2 * t2, 0.0)
        hd = 0.7 * tf + 0.7 * (1 - math.exp(-4 * t2)) / 4
    fr = min(tau / tf, 1.0)
    ry = (math.pi / 2 if lay else 0.18) * fr
    return xe + vx * hd, ye + vy * hd, z, (0.0, ry, math.radians(spin) * (te + 0.5 * tau))


def room_items(F, T, quaking=True):
    for it in ITEMS:
        x, y, z, rot = item_pose(it, T, quaking)
        F.c((x, y, z), it[1], it[2], rot)


def pendant(F, G, LT, T, amp):
    """천장 레일에 매달린 식탁 등: 줄 + 갓 + 발광판. amp = 흔들림 크기(0~1)."""
    pv = np.array((TB_X, TB_Y, 2.65))
    sx = 0.50 * amp * math.sin(2 * math.pi * 0.95 * T + 0.4)
    sy = 0.34 * amp * math.sin(2 * math.pi * 1.3 * T)
    d = np.array((sx, sy, -1.0))
    d /= np.linalg.norm(d)
    L = 0.95
    F.o(pv, (L, 0.03, 0.03), (0.12, 0.12, 0.14), rot_to(d))
    c = pv + d * (L + 0.06)
    tilt = (sy / (1.0 + 1e-9), -sx, 0.0)
    F.c(c, (0.55, 0.55, 0.16), (0.14, 0.16, 0.18), (tilt[0], tilt[1], 0.0))
    G.c(c + d * 0.09, (0.46, 0.46, 0.03), WARM_G, (tilt[0], tilt[1], 0.0))
    _lt(LT, "ep36_h_pend", c + d * 0.3, 60)


def room_pics(F, T, amp):
    """뒷벽 액자 둘: 흔들리면 기울어짐."""
    for k, (x, z, w, h, col) in enumerate(((2.95, 1.7, 0.62, 0.46, (0.40, 0.62, 0.80)),)):
        a = 0.22 * amp * math.sin(2 * math.pi * (2.1 + 0.4 * k) * T + k)
        F.c((x, RY1 - 0.05, z), (w, 0.04, h), (0.92, 0.9, 0.84), (0.0, a, 0.0))
        F.c((x, RY1 - 0.075, z), (w - 0.08, 0.02, h - 0.08), col, (0.0, a, 0.0))


def room_dust(F, T):
    for n in range(14):
        h = _h(n + 11)
        z = 2.65 - ((0.55 * T + h * 3.0) % 2.7)
        x = -1.6 + 3.2 * _h(n + 41) + 0.12 * math.sin(3 * T + n)
        y = -0.1 + 1.9 * _h(n + 71)
        s = 0.03 + 0.03 * _h(n + 5)
        F.c((x, y, z), (s, s, s), (0.82, 0.78, 0.70))


def props_room(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """훅(0)·엎드림(5): 규모 7 흔들림 — 식탁 위 물건이 미끄러져 떨어지고, 펜던트가 흔들리고, 액자가 기울고, 먼지가 내림."""
    T = t if i == IX["hook"] else tau + 2.4
    amp = cam["amp"]
    room_items(F, T, True)
    pendant(F, G, LT, T, 0.60 * min(1.0, amp + 0.15))
    room_pics(F, T, amp)
    room_dust(F, T)


def room_calm(F, G, LT, pend=True):
    """흔들리지 않는 집: 물건이 식탁에 가만히, 펜던트도 가만히."""
    room_items(F, 0.0, False)
    if pend:
        pendant(F, G, LT, 0.0, 0.0)
    room_pics(F, 0.0, 0.0)


# ── 거실 TV: 지진계 그래프 (1·2번 줄)
TRACE_N = 62
TV_YC, TV_ZC = (TV_Y0 + TV_Y1) / 2, 1.7
PEAKS = ((0.30, 0.52, "경주", "5.8", 0.40), (0.72, 0.40, "포항", "5.4", 0.38))     # (가로 위치 0~1, 키, 이름, 규모, 라벨 시작 s 아님)


def wave(s):
    w = 0.025 * math.sin(2 * math.pi * 9 * s + 1.0) + 0.016 * math.sin(2 * math.pi * 23 * s + 0.3)
    for p, a, _, _, _ in PEAKS:
        w += a * math.exp(-((s - p) / 0.024) ** 2) * math.sin(2 * math.pi * (s - p) / 0.030)
    return w


def cells_pop(G, rows, center, psi, cell, col, k):
    """도트 그림을 중심 고정으로 k배(0~) 키워 그림 (톡 튀어나오는 효과)."""
    if k <= 0.01:
        return
    cp, sp = math.cos(psi), math.sin(psi)
    nc, nr = len(rows[0]), len(rows)
    c0 = (center[0] - cp * (nc - 1) / 2 * cell * k, center[1] - sp * (nc - 1) / 2 * cell * k, center[2] + (nr - 1) / 2 * cell * k)
    cells(G, rows, c0, psi, cell * k, col)


def props_tv(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """1·2번 줄: TV 화면에 지진계 선이 그려지고 큰 봉우리(경주 5.8 → 포항 5.4)가 솟음. 방은 약하게 흔들림."""
    first = i == IX["seismo1"]
    prog = (0.0 + 0.48 * ramp(tau, 0.10, 2.60)) if first else (0.48 + 0.52 * ramp(tau, 0.0, 2.30))
    xw = RX0 + 0.16
    ys = np.linspace(TV_Y0 + 0.12, TV_Y1 - 0.12, TRACE_N)
    zs = TV_ZC + np.array([wave(k / (TRACE_N - 1)) for k in range(TRACE_N)])
    for k in range(TRACE_N - 1):
        if k / (TRACE_N - 1) > prog:
            break
        a, b = zs[k], zs[k + 1]
        G.c((xw, (ys[k] + ys[k + 1]) / 2, (a + b) / 2), (0.02, (ys[k + 1] - ys[k]) * 1.08, abs(a - b) + 0.034), GREEN_G)
    kk = min(int(prog * (TRACE_N - 1)), TRACE_N - 1)
    G.c((xw + 0.01, ys[kk], zs[kk]), (0.02, 0.07, 0.07), (4.0, 4.0, 3.6))                               # 펜 끝
    for n, (p, a, name, mag, _) in enumerate(PEAKS):
        reach = prog - p
        if reach < 0.02:
            continue
        k = pop((reach - 0.02) / 0.05 * 0.3, 0.3, 1.6)
        y = ys[0] + (ys[-1] - ys[0]) * p + 0.30
        cells_pop(G, text_rows(name), (xw + 0.01, y + 0.14, TV_ZC + 0.34), math.pi / 2, 0.015, YEL_G, k)
        cells_pop(G, text_rows(mag), (xw + 0.01, y + 0.14, TV_ZC + 0.10), math.pi / 2, 0.034, (4.0, 4.0, 4.0), k)


# ── 막대 방: 규모 5.8 → 6.8 → 7.0 에너지 막대 (3·4번 줄)
BAR_X = (-1.3, -0.2, 0.9)
BAR_H = (0.05, 1.6, 3.15)                                  # 1 : 32 : 63 (규모 5.8 / 6.8 / 7.0)
BAR_COL = ((0.96, 0.82, 0.25), (0.96, 0.56, 0.16), (0.90, 0.18, 0.15))
BAR_CAP = ((3.4, 2.8, 0.7), (3.4, 1.8, 0.4), (3.4, 0.6, 0.5))


def bar_heights(i, tau):
    """세 막대의 높이(m). 3번 줄: 5.8 나타남 → 6.8이 솟음(×32). 4번 줄: 7.0이 천장까지(×63)."""
    h1 = BAR_H[0] * pop(tau - 0.10, 0.25, 2.0) if i == IX["bar1"] else BAR_H[0]
    if i == IX["bar1"]:
        h2 = BAR_H[1] * pop(tau - 1.00, 0.85, 1.4)
        h3 = 0.0
    else:
        h2 = BAR_H[1]
        h3 = BAR_H[2] * ramp(tau, 0.15, T_HIT)
    return h1, max(h2, 0.0), h3


def props_bars(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    h = bar_heights(i, tau)
    bx = [LABX + x for x in BAR_X]
    for k in range(3):
        if h[k] <= 0.004:
            continue
        F.c((bx[k], 0.0, h[k] / 2), (0.7, 0.7, h[k]), BAR_COL[k])
        if h[k] > 0.1:
            G.c((bx[k], -0.352, h[k] - 0.005), (0.7, 0.012, 0.035), BAR_CAP[k])
    G.c((bx[0], -0.352, h[0] + 0.03), (0.72, 0.012, 0.012), BAR_CAP[0])
    labels = [(0, "5.8", 0.25 if i == IX["bar1"] else -1.0), (1, "6.8", 1.5 if i == IX["bar1"] else -1.0),
              (2, "7.0", 0.5 if i == IX["bar2"] else 99.0)]
    for k, txt, t_on in labels:
        s = pop(tau - t_on, 0.3, 1.6) if t_on >= 0 else 1.0
        cells_pop(G, text_rows(txt, 1), (bx[k], -0.55, 0.28), 0.0, 0.055, (4.0, 4.0, 4.0), s)
    # '×배수' 표시: 6.8 옆 x32, 7.0 옆 x63
    s32 = pop(tau - 1.35, 0.3, 1.6) if i == IX["bar1"] else 1.0
    cells_pop(G, text_rows("x32", 1), (bx[1] + 0.78, -0.45, 1.45), 0.0, 0.065, YEL_G, s32)
    if i == IX["bar2"]:
        s63 = pop(tau - 1.0, 0.3, 1.6)
        cells_pop(G, text_rows("x63", 1), (bx[2] - 0.82, -0.45, 2.7), 0.0, 0.065, RED_G, s63)
        if tau > T_HIT:                                           # 천장에 닿은 순간: 충격 불꽃 + 먼지가 떨어짐
            te = tau - T_HIT
            for n in range(6):
                a = n * math.pi / 3 + 0.3
                r = 0.25 + 0.9 * min(te / 0.3, 1.0)
                s = 0.14 * (1.0 - min(te / 0.5, 1.0))
                if s > 0.01:
                    G.c((bx[2] + r * math.cos(a), -0.4, 3.2 + 0.3 * r * math.sin(a)), (s, 0.03, s), (4.0, 3.2, 0.8), (0.0, 0.0, a))
            for n in range(10):
                z = 3.2 - ((te * 0.9 + _h(n + 3)) % 1.0) * 3.0 * min(te * 3, 1.0)
                F.c((LABX - 1.2 + 2.4 * _h(n + 20), -0.5 + _h(n + 50), max(z, 0.02)), (0.04, 0.04, 0.04), (0.82, 0.78, 0.70))


# ── 폰 화면 (7·19·20번 줄): 화면 좌표에 앞면 판을 놓는 '스프라이트'. 뒤에 어두운 판을 깔아 폰이 돋보이게.
PH_Y = -0.04                                              # 폰 가운데 높이(화면 반높이 단위)
BELL = ["....#....", "..#####..", ".#######.", ".#######.", ".#######.", "#########", "....#...."]


def phone_frame(G, cam, jit=0.0, scr=(0.03, 0.045, 0.10)):
    sprite(G, cam, 0, 0, 1.4, 1.4, (0.04, 0.05, 0.09), 2.6)
    sprite(G, cam, jit, PH_Y, 0.205, 0.40, (0.42, 0.44, 0.50), 2.0)
    sprite(G, cam, jit, PH_Y, 0.183, 0.365, scr, 1.97)
    sprite(G, cam, jit, PH_Y + 0.35, 0.045, 0.006, (0.10, 0.10, 0.12), 1.95)                    # 스피커 홈


def sprite_text(G, cam, rows, nx, ny, cell, col, dist=1.94, k=1.0):
    """도트 글자를 화면 좌표 (nx, ny)에 가운데 맞춰 그림. cell = 화면 높이에 대한 칸 크기."""
    if k <= 0.01:
        return
    nc, nr = len(rows[0]), len(rows)
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] != "#":
                c += 1
                continue
            c1 = c
            while c1 + 1 < len(row) and row[c1 + 1] == "#":
                c1 += 1
            m = (c + c1) / 2.0 - (nc - 1) / 2.0
            # nx 단위: 화면 반폭 = 0.5625/2 화면높이 → 1 nx = 0.28125 화면높이
            sprite(G, cam, nx + m * cell * k / 0.28125, ny - ((r - (nr - 1) / 2.0) * cell * k) * 2.0,
                   (c1 - c + 1) * cell * k * 0.96, cell * k * 0.94, col, dist)
            c = c1 + 1


def props_phone(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """7번 줄: 타이머가 5초까지 세고 → 폰이 울리며 빨간 경고(종 아이콘). 19번 줄: 타이머가 8분까지 한참 간 뒤에야 문자. 20번 줄: 곧바로."""
    if i == IX["alert"]:
        t_alert = 1.15
        n = min(int(tau / t_alert * 5), 5)
        timer = "0:0%d" % n
    elif i == IX["late"]:
        t_alert = 2.05
        m = min(int(8 * ramp(tau, 0.15, t_alert - 0.1)), 8)
        timer = "%d:00" % m
    else:
        t_alert = 0.62
        n = min(int(tau / t_alert * 5), 5)
        timer = "0:0%d" % n
    ringing = tau >= t_alert
    jit = 0.012 * math.sin(2 * math.pi * 22 * tau) if ringing and tau < t_alert + 1.4 else 0.0
    phone_frame(G, cam, jit, (2.6, 0.22, 0.20) if ringing else (0.03, 0.045, 0.10))
    ring_k = pop(tau - t_alert, 0.30, 2.0) if ringing else 0.0
    if not ringing or ring_k < 0.9:
        sprite_text(G, cam, text_rows(timer, 1), jit, PH_Y, 0.014, (1.6, 2.4, 3.2), 1.94, 1.0 if not ringing else max(0.0, 1.0 - ring_k))
    if ringing:
        sprite(G, cam, jit, PH_Y + 0.27, 0.165, 0.07, (4.0, 4.0, 4.0), 1.95, 0.02)                  # 문자 알림 띠
        sprite(G, cam, jit, PH_Y + 0.29, 0.12, 0.011, (0.25, 0.25, 0.30), 1.93)
        sprite(G, cam, jit - 0.07, PH_Y + 0.25, 0.07, 0.009, (0.45, 0.45, 0.50), 1.93)
        sprite_text(G, cam, BELL, jit, PH_Y + 0.02, 0.0115, (4.0, 3.6, 3.0), 1.94, ring_k)
        for sgn in (-1, 1):
            for r_, h_ in ((0.25, 0.05), (0.31, 0.09)):
                sprite(G, cam, jit + sgn * r_, PH_Y + 0.02, 0.009, h_ * ring_k, (4.0, 3.6, 3.0), 1.94)
        sprite_text(G, cam, text_rows("!", 1), jit, PH_Y - 0.25, 0.014, (4.0, 3.6, 3.0), 1.94, ring_k)


# ── 건물 모형 열 채 (9·10번 줄): 여덟 채는 회색(내진 성능 없음), 두 채는 초록. 10번 줄에 회색 건물에 금이 감.
CITY_POS = ((-1.0, -1.6, 1.0), (0.0, -1.6, 1.2), (1.0, -1.6, 1.1), (-1.0, -0.6, 1.4), (0.0, -0.6, 1.3), (1.0, -0.6, 1.5),
            (-0.5, 0.4, 1.7), (0.5, 0.4, 1.8), (-0.5, 1.4, 2.0), (0.5, 1.4, 1.9))      # (x, y, 높이): 앞에서 뒤로 4줄 · 3 3 2 2채
CITY = [(LABX + LB_CITY + x, y, 0.72, h, k in (1, 7)) for k, (x, y, h) in enumerate(CITY_POS)]      # 초록은 1번(앞줄 가운데)·7번(셋째 줄 오른쪽)
CITY_ORDER = (0, 3, 6, 8, 2, 5, 4, 9, 1, 7)                 # 솟는 순서: 앞에서 뒤로 번갈아
GRAY_B, GREEN_B = (0.58, 0.60, 0.64), (0.30, 0.78, 0.42)


def props_city(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    nine = i == IX["blds"]
    grays = [k for k, b in enumerate(CITY) if not b[4]]
    for k, (x, y, w, h, green) in enumerate(CITY):
        tp = 0.10 + 0.19 * CITY_ORDER.index(k)
        s = pop(tau - tp, 0.35, 1.5) if nine else 1.0
        if s <= 0.01:
            continue
        g = (ramp(tau, 2.05, 2.30) if nine else 1.0) if green else 0.0
        col = tuple(GRAY_B[q] * (1 - g) + GREEN_B[q] * g + 0.03 * math.sin(7 * k + q) for q in range(3))
        pulse = 1.0 + (0.05 * math.sin(2 * math.pi * 2.0 * tau) if (green and not nine) else 0.0)
        hh = h * s * pulse
        F.c((x, y, hh / 2), (w, w, hh), col)
        F.c((x, y, hh + 0.025), (w + 0.07, w + 0.07, 0.05), (0.40, 0.42, 0.46) if not green else (0.18, 0.55, 0.30))
        yf = y - w / 2 - 0.008
        for r in range(max(2, int(h / 0.36))):
            z = 0.22 + 0.34 * r
            if z + 0.12 > hh:
                break
            for cc in (-1, 0, 1):
                G.c((x + cc * 0.2, yf, z), (0.12, 0.012, 0.16), (0.9, 1.4, 1.9) if not green else (1.0, 3.0, 1.4))
    if not nine:                                              # 회색 건물마다 차례로 금이 감 (가볍게: 가는 선 몇 줄 + 먼지)
        for j, k in enumerate(grays):
            x, y, w, h, _ = CITY[k]
            tc = 0.12 + 0.12 * j
            g = ramp(tau, tc, tc + 0.28)
            if g <= 0.0:
                continue
            yf = y - w / 2 - 0.02
            ztop = h - 0.12
            pts = [(x - 0.10, ztop), (x + 0.02, ztop - 0.28), (x - 0.07, ztop - 0.50), (x + 0.10, ztop - 0.75)]
            for (xa, za), (xb, zb) in zip(pts, pts[1:]):
                d = np.array((xb - xa, 0.0, zb - za))
                ln = float(np.linalg.norm(d)) * g
                F.o((xa, yf, za), (ln, 0.025, 0.03), (0.05, 0.05, 0.07), rot_to(d / np.linalg.norm(d)))
            te = tau - tc
            if 0.0 < te < 0.8:                                # 금 갈 때 먼지 두어 점
                for n in range(3):
                    z = ztop - 0.2 - 0.5 * te - 0.1 * n
                    F.c((x + 0.09 * (n - 1), yf - 0.03, max(z, 0.04)), (0.045, 0.045, 0.045), (0.85, 0.82, 0.76))


# ── 교실 (11번 줄): 햇살 속 먼지
def props_class(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for n in range(20):
        x = -2.5 + 6.0 * _h(n + 3) + 0.15 * math.sin(0.8 * t + n)
        y = -3.5 + 5.0 * _h(n + 9) + 0.12 * math.cos(0.7 * t + 2 * n)
        z = 0.5 + ((0.12 * t + _h(n + 31) * 2.2) % 2.2)
        G.c((OFF["class"][0] + x, y, z), (0.03, 0.03, 0.03), (2.6, 2.4, 1.9))


# ── 집 벽 달력 (12번 줄): 수능 날짜에 빨간 동그라미가 톡
CAL = (-3.3, 3.14, 1.50)                                   # 달력 가운데 (x, y, z)
CAL_COLS, CAL_ROWS = 7, 5


def props_calendar(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    cx, cy, cz = CAL
    F.c((cx, cy, cz), (1.40, 0.03, 1.25), (0.97, 0.97, 0.94))
    F.c((cx, cy - 0.02, cz + 0.55), (1.40, 0.02, 0.18), (0.80, 0.25, 0.25))
    x0, z0 = cx - 0.65, cz + 0.38
    cw, ch = 1.3 / CAL_COLS, 0.19
    for k in range(CAL_COLS + 1):
        F.c((x0 + k * cw, cy - 0.02, z0 - ch * CAL_ROWS / 2), (0.008, 0.01, ch * CAL_ROWS), (0.45, 0.45, 0.50))
    for k in range(CAL_ROWS + 1):
        F.c((cx, cy - 0.02, z0 - k * ch), (1.3, 0.01, 0.008), (0.45, 0.45, 0.50))
    for r in range(CAL_ROWS):
        for c in range(CAL_COLS):
            if (r, c) in ((0, 0), (0, 1), (4, 5), (4, 6)):
                continue
            F.c((x0 + (c + 0.5) * cw, cy - 0.025, z0 - (r + 0.5) * ch), (0.06, 0.012, 0.04), (0.30, 0.30, 0.35) if c else (0.8, 0.25, 0.25))
    tx, tz = x0 + 4.5 * cw, z0 - 2.5 * ch                  # 동그라미 칠 날 (넷째 줄 가운데)
    k = pop(tau - 0.55, 0.35, 1.8)
    if k > 0.01:
        pulse = 1.0 + 0.07 * math.sin(2 * math.pi * 2.2 * tau)
        for n in range(14):
            a = 2 * math.pi * n / 14
            G.c((tx + 0.13 * k * pulse * math.cos(a), cy - 0.04, tz + 0.12 * k * pulse * math.sin(a)), (0.06, 0.012, 0.06), RED_G, (0.0, a, 0.0))
        F.c((tx, cy - 0.03, tz), (0.16, 0.012, 0.14), (0.97, 0.80, 0.80))


# ── 교문 앞·가로등 밤 (13·14번 줄): 눈발 · 책 · 나방
def snow(G, t, fx, n=22):
    for k in range(n):
        x = fx - 3.5 + 7.0 * _h(k + 2) + 0.2 * math.sin(1.3 * t + k)
        y = -1.5 + 3.5 * _h(k + 17)
        z = 3.2 - ((0.55 * t + 3.2 * _h(k + 40)) % 3.2)
        G.c((x, y, z), (0.04, 0.04, 0.04), (3.0, 3.0, 3.2))


def props_gate(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    snow(G, t, OFF["gate"][0])


BOOK_COL = ((0.90, 0.85, 0.30), (0.35, 0.60, 0.90), (0.92, 0.45, 0.35), (0.40, 0.75, 0.50), (0.95, 0.95, 0.92))


def props_lamp(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    ox = OFF["gate"][0]
    snow(G, t, ox + GT_LAMP)
    for n in range(5):                                       # 읽는 책: 가슴 앞에 펼친 책
        d = S.get("rd%d" % n)
        if d is None:
            continue
        p = rel(d, 0.36, 0.0, hip_of(d["pose"]) + 0.55)
        p = (p[0] + ox, p[1], p[2])
        F.c(p, (0.04, 0.30, 0.22), BOOK_COL[n], (0.0, -0.45, math.radians(d["yaw"])))
        F.c((p[0], p[1], p[2] + 0.002), (0.045, 0.012, 0.22), (0.2, 0.2, 0.25), (0.0, -0.45, math.radians(d["yaw"])))
    for n in range(6):                                       # 가로등 불빛 둘레 나방
        a = 3.0 * t + n * 1.05
        r = 0.25 + 0.12 * math.sin(2 * t + n)
        G.c((ox + GT_LAMP - 2.0 + r * math.cos(a), 0.3 + 0.8 * r * math.sin(a), 3.0 + 0.1 * math.sin(5 * t + n)), (0.05, 0.05, 0.03), (3.0, 3.0, 2.4))


# ── 거리 (15·16번 줄): 이동식 크레인 붐 · 줄 · 철골 / 용접 불꽃 / 새 건물에 초록 체크
CR_P = np.array((4.1, -0.9, 2.0))
CHECK = ["........#", ".......##", "......###", "#....###.", "##..###..", "#######..", ".#####...", "..###....", "...#....."]


def props_street(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    ox = OFF["street"][0]
    first = i == IX["scaffold"]
    el = math.radians(50.0 + 5.0 * (u if first else 1.0))
    sw = math.radians(120.0 + 8.0 * math.sin(0.5 * t))                       # 붐 방향(건물 쪽, 방위각)
    dh = np.array((math.cos(sw), math.sin(sw)))
    d = np.array((math.cos(el) * dh[0], math.cos(el) * dh[1], math.sin(el)))
    P0 = CR_P + np.array((ox, 0.0, 0.0))
    F.o(P0, (3.9, 0.36, 0.36), (0.95, 0.75, 0.12), rot_to(d))
    F.o(P0 + d * 3.7, (3.2, 0.27, 0.27), (0.85, 0.65, 0.10), rot_to(d))
    tip = P0 + d * 6.8
    ln = 3.4 - 0.5 * math.sin(0.9 * t)
    F.o(tip, (ln, 0.045, 0.045), (0.12, 0.12, 0.14), rot_to(np.array((0.0, 0.0, -1.0))))
    hk = tip - np.array((0.0, 0.0, ln))
    F.c(hk - np.array((0.0, 0.0, 0.12)), (0.22, 0.22, 0.26), (0.95, 0.55, 0.1))
    sway = 0.12 * math.sin(1.4 * t)
    F.c(hk - np.array((sway, 0.0, 0.60)), (2.1, 0.16, 0.20), (0.62, 0.36, 0.2), (0.0, 0.0, 0.05 * math.sin(1.4 * t)))
    for sg in (-1, 1):
        dv = np.array((sg * 0.9, 0.0, -0.38))
        F.o(hk - np.array((0.0, 0.0, 0.22)), (float(np.linalg.norm(dv)), 0.015, 0.015), (0.12, 0.12, 0.14), rot_to(dv / np.linalg.norm(dv)))
    if first:                                                # 용접 불꽃 (비계 위 작업자 손 근처)
        w = S.get("wk0")
        if w is not None:
            p = rel(w, 0.45, 0.0, 0.95)
            p = (p[0] + ox, p[1], p[2])
            for n in range(7):
                ph = (t * 6.0 + n * 0.37) % 1.0
                a = 6.0 * n + 1.3
                G.c((p[0] + 0.3 * ph * math.cos(a), p[1] - 0.05, p[2] + 0.35 * ph * math.sin(a) - 0.4 * ph * ph),
                    (0.04, 0.04, 0.04), (4.0, 2.6, 0.5) if _h(n + int(t * 6)) > 0.4 else (3.0, 2.0, 0.4))
    else:                                                    # 새 건물 정면에 큰 초록 체크가 톡
        k = pop(tau - 0.55, 0.40, 1.7)
        cells_pop(G, CHECK, (ox + 12.5, 4.1, 4.0), 0.0, 0.34, GREEN_G, k)


# ── 땅속 단면 (17·18번 줄): 지열발전소 관이 내려가고 → 물이 관을 따라 내려가 → 바위가 갈라짐
UG_BOT = -2.95
RING_N = 14


def props_ug(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    cx = LABX + LB_UG
    first = i == IX["pipe"]
    y0 = -0.14
    plen = 3.05 * (ramp(tau, 0.15, 2.3) if first else 1.0)
    F.o((cx, y0, 0.15), (plen, 0.17, 0.17), (0.48, 0.50, 0.56), rot_to(np.array((0.0, 0.0, -1.0))))
    G.c((cx, y0 - 0.095, 1.95), (0.1, 0.05, 0.1), (3.4, 2.4, 0.5) if int(t * 4) % 2 else (1.0, 0.8, 0.3))      # 탑 꼭대기 점멸등
    for n in range(4):                                       # 굴뚝 연기
        ph = (0.4 * t + n * 0.25) % 1.0
        s = 0.12 + 0.25 * ph
        F.c((cx + 2.45 + 0.1 * math.sin(3 * ph + n), 0.75, 1.75 + 1.6 * ph), (s, s, s), (0.95 * (1 - ph) + 0.5 * ph,) * 3)
    if first:
        return
    # 18번 줄: 파란 물
    for n in range(8):
        ph = (0.9 * tau + n / 8.0) % 1.0
        z = 0.1 - ph * 3.0
        if z > UG_BOT + 0.1:
            G.c((cx, y0 - 0.095, z), (0.10, 0.03, 0.22), CYAN_G)
    r = 0.12 + 0.72 * ramp(tau, 0.7, 2.2)
    OR.orb((cx, y0 - 0.06, UG_BOT), 2 * r, (0.25, 1.3, 3.0))
    for n in range(5):
        a = 2 * math.pi * n / 5 + 0.4
        OR.orb((cx + r * 0.9 * math.cos(a), y0 - 0.07, UG_BOT + r * 0.9 * math.sin(a)), 0.18 * min(r / 0.5, 1.0), (0.4, 1.6, 3.2))
    br = ((-0.45, 0.88), (0.55, 0.83), (-1.0, 0.30), (1.0, 0.25), (-0.6, -0.55), (0.65, -0.5))
    for j, (dx, dz) in enumerate(br):                        # 금: 물웅덩이에서 바깥으로 뻗는 갈라진 선
        g = ramp(tau, 1.2 + 0.12 * j, 2.2 + 0.12 * j)
        if g <= 0.0:
            continue
        a_ = np.array((cx, UG_BOT))
        dirv = np.array((dx, dz)) / math.hypot(dx, dz)
        p = a_ + dirv * r * 0.8
        for seg in range(3):
            jig = 0.28 * math.sin(5.0 * j + 2.0 * seg)
            dv = np.array((dirv[0] * math.cos(jig) - dirv[1] * math.sin(jig), dirv[0] * math.sin(jig) + dirv[1] * math.cos(jig)))
            L = 0.55 * g
            F.o((p[0], y0 - 0.03, p[1]), (L, 0.02, 0.05), (0.05, 0.04, 0.04), rot_to(np.array((dv[0], 0.0, dv[1]))))
            p = p + dv * L
    k = ramp(tau, 1.3, 2.9)                                  # 번지는 진동 고리
    for rr in range(2):
        rad = 0.4 + 2.2 * ((k + 0.5 * rr) % 1.0) if k > 0 else 0.0
        if k > 0:
            for n in range(RING_N):
                a = 2 * math.pi * n / RING_N
                zz = UG_BOT + 0.8 * rad * math.sin(a)
                if -3.45 < zz < -0.2 and abs(rad * math.cos(a)) < 3.0:
                    G.c((cx + rad * math.cos(a), y0 - 0.1, zz), (0.07, 0.02, 0.07), (2.4, 2.0, 0.6) if rr == 0 else (1.6, 1.4, 0.5))


# ── 비상가방 (21번 줄): 세 사람이 물건을 던져 넣음
BAG_AT = (0.0, -2.4)
BAG_ITEMS = ((0.35, (0.35, 0.60, 0.95), (0.09, 0.09, 0.28), "mom"), (0.85, (0.95, 0.85, 0.25), (0.07, 0.07, 0.22), "dad"),
             (1.35, (0.55, 0.55, 0.60), (0.20, 0.10, 0.14), "dh"), (1.85, (0.90, 0.30, 0.25), (0.14, 0.10, 0.09), "mom"))


def props_bag(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bx, by = BAG_AT
    land = [ta for ta, *_ in BAG_ITEMS if tau > ta + 0.45]
    sw = 1.0 + 0.06 * sum(math.exp(-8 * (tau - ta - 0.45)) for ta in land)
    F.c((bx, by, 0.30 * sw), (0.44, 0.32, 0.60 * sw), (0.95, 0.50, 0.15))
    F.c((bx, by, 0.62 * sw), (0.46, 0.34, 0.10), (0.78, 0.38, 0.10))
    F.c((bx - 0.19, by, 0.30), (0.04, 0.26, 0.40), (0.85, 0.42, 0.10))
    F.c((bx, by - 0.18, 0.22), (0.30, 0.04, 0.22), (0.85, 0.42, 0.10))
    for ta, col, size, who in BAG_ITEMS:
        s = (tau - ta) / 0.45
        if s < 0.0 or s >= 1.0:
            continue
        d = S.get(who)
        a = rel(d, 0.3, 0.0, 1.0) if d is not None else (bx - 0.7, by, 1.0)
        z = a[2] + (0.7 - a[2]) * s + 0.55 * 4 * s * (1 - s)
        F.c((a[0] + (bx - a[0]) * s, a[1] + (by - a[1]) * s, z), size, col, (6.0 * s, 4.0 * s, 0.0))


# ── 집 둘러보기 (22번 줄): 안전한 자리는 어디? — 곳곳에 물음표가 차례로 톡
ASK = ((-2.0, -0.3, 1.05), (-0.9, TB_Y, 1.40), (1.4, 3.0, 2.35))


def props_around(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    room_calm(F, G, LT)
    for n, (x, y, z) in enumerate(ASK):
        k = pop(tau - 0.25 - 0.45 * n, 0.30, 1.8)
        if k <= 0.01:
            continue
        # 카메라 쪽을 보는 물음표 (판은 항상 카메라 쪽)
        psi = math.atan2(cam["loc"][0] - x, y - cam["loc"][1])
        bob = 0.05 * math.sin(2 * math.pi * 1.6 * (tau - 0.45 * n))
        cells_pop(G, DIG["?"], (x, y, z + bob), psi, 0.20, YEL_G, k)


# ── 다음 편 예고 (23번 줄): 창밖 노을 하늘에 멈춘 듯 걸린 해
SUN_AT = (0.22, -0.12, 6.0)


def sun_dir(i):
    cam = cam_pose(i, 0.5)
    f = cam["lens"]
    nx, ny = SUN_AT[:2]
    d = cam["fwd"] + nx * (6.75 / f) * cam["right"] + (ny + 2.0 * cam["shift"]) * (12.0 / f) * cam["up"]
    return d / np.linalg.norm(d)


def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    room_calm(F, G, LT, False)
    D = sun_dir(i)
    rs = R_FAR * math.tan(math.radians(SUN_AT[2]))
    c = cam["loc"] + D * R_FAR
    pul = 1.0 + 0.012 * math.sin(2 * math.pi * 0.8 * tau)
    OR.orb(c, 2 * rs * pul, (5.0, 2.6, 0.9))
    OR.orb(c, 2 * rs * 1.18 * pul, (2.2, 0.9, 0.35))


def props_calm(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    room_calm(F, G, LT)


PROPS = {IX["hook"]: props_room, IX["duck"]: props_room, IX["seismo1"]: props_tv, IX["seismo2"]: props_tv,
         IX["bar1"]: props_bars, IX["bar2"]: props_bars, IX["alert"]: props_phone, IX["late"]: props_phone, IX["now"]: props_phone,
         IX["blds"]: props_city, IX["cracks"]: props_city, IX["closed"]: props_class, IX["calendar"]: props_calendar,
         IX["gate"]: props_gate, IX["lamp"]: props_lamp, IX["scaffold"]: props_street, IX["newbld"]: props_street,
         IX["pipe"]: props_ug, IX["inject"]: props_ug, IX["bag"]: props_bag, IX["around"]: props_around, IX["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 월드 좌표."""
    F, G, OR, BL, LT = Items(N_FX), Items(N_GL), Items(N_OR), Items(N_BL), []
    PROPS.get(i, props_calm if set_of(i) == "home" and i != IX["stairs"] else (lambda *a: None))(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
DH_SH, DH_PA = (0.30, 0.70, 0.40), (0.15, 0.18, 0.30)      # 도현: 초록 후드·남색 바지
MOM_SH, MOM_PA = (0.92, 0.55, 0.62), (0.35, 0.28, 0.20)    # 엄마: 분홍
DAD_SH, DAD_PA = (0.25, 0.45, 0.80), (0.20, 0.20, 0.22)    # 아빠: 파랑
GD_SH, GD_PA = (0.14, 0.20, 0.42), (0.12, 0.14, 0.28)      # 경비 아저씨: 남색
RS_SH, RS_PA = (0.95, 0.50, 0.10), (0.15, 0.17, 0.25)      # 구조대: 주황 조끼
WK_SH = (0.95, 0.80, 0.25)                                 # 공사 작업자: 노란 조끼
EX_SH = [(0.85, 0.30, 0.28), (0.92, 0.92, 0.90), (0.30, 0.30, 0.34), (0.95, 0.80, 0.35), (0.55, 0.38, 0.70), (0.80, 0.55, 0.65),
         (0.45, 0.75, 0.85), (0.62, 0.62, 0.66)]            # 엑스트라 (초록·분홍·파랑·주황 주인공 색은 피함)
SIT_FLOOR = -0.33                                          # 바닥에 앉기: 의자 높이 앉은 자세를 낮춰 허벅지만 바닥에 놓이게


def _sz(x):
    """계단을 걷는 사람의 발 높이: 한 칸 위에서 머물다 다음 칸으로 부드럽게 내려감 (x는 세트 좌표)."""
    lx = x - HX_ST
    if lx <= 0.0:
        return STAIR_TOP
    if lx >= STAIR_X1:
        return 0.0
    k = int(lx / STEP_RUN)
    f = clamp((lx / STEP_RUN - k - 0.45) / 0.55)
    return STAIR_TOP - STEP_RISE * (k + f * f * (3 - 2 * f))


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    rs = np.random.default_rng(36)
    C = []
    L = IX

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))

    def ex(name, at, hair=None):
        add(name, int(rs.random() < 0.5) if hair is None else hair, EX_SH[int(rs.integers(len(EX_SH)))],
            X.PANTS[int(rs.integers(len(X.PANTS)))], at)
    walk = dict(pair=("walk_a", "walk_b"))
    # ── 도현 (초록 후드): 훅에서 식탁 밑으로 → 계단 → 달력 → 비상가방 → 거실 → 창가
    add("dh", 0, DH_SH, DH_PA, {
        L["hook"]: st("home", -1.30, 0.47, 0, "duck", keys=[(0.0, (-1.30, 0.47, 0.0, 0, 0.30)), (0.35, (-1.25, 0.47, 0.0, 0, 0.55)),
                                                          (0.80, (-1.12, 0.47, 0.10, 0, 1.05)), (1.30, (-0.96, 0.47, 0.20, 0, 1.50)),
                                                          (9.0, (-0.93, 0.47, 0.20, 0, 1.50))], ease=_LIN),
        L["duck"]: st("home", -0.93, 0.47, 0, "duck", keys=[(0.0, (-0.93, 0.47, 0.20, 0, 1.50))]),
        L["stairs"]: st("home", HX_ST - 1.0, 1.0, 0, "walk_a", v=(0.9, 0.0), cad=0.40, zfn=_sz, **walk),
        L["calendar"]: st("home", -2.4, 2.4, 150, "think"),
        L["bag"]: st("home", BAG_AT[0], BAG_AT[1] + 0.85, -90, "talk", alt=("talk", "stand", 0.9, 0.3)),
        L["around"]: st("home", -1.3, -1.9, -150, "look_h", keys=[(0.0, (-1.3, -1.9, 0.0, -150, 0.0)), (3.0, (-1.3, -1.9, 0.0, -30, 0.0))],
                        ease=_LIN),
        L["gym"]: st("gym", -1.8, 0.7, -90, "sit_conf", z=SIT_FLOOR),
        L["teaser"]: st("home", -1.0, 1.9, 75, "look_up")}, scale=0.95, extra="hood")
    add("mom", 1, MOM_SH, MOM_PA, {
        L["hook"]: st("home", 1.30, 1.13, 180, "duck", keys=[(0.0, (1.30, 1.13, 0.0, 180, 0.30)), (0.45, (1.25, 1.13, 0.0, 180, 0.55)),
                                                            (0.90, (1.12, 1.13, 0.10, 180, 1.05)), (1.40, (0.96, 1.13, 0.19, 180, 1.50)),
                                                            (9.0, (0.93, 1.13, 0.19, 180, 1.50))], ease=_LIN),
        L["duck"]: st("home", 0.93, 1.13, 180, "duck", keys=[(0.0, (0.93, 1.13, 0.19, 180, 1.50))]),
        L["stairs"]: st("home", HX_ST - 0.55, 1.0, 0, "walk_a", v=(0.9, 0.0), cad=0.40, zfn=_sz, **walk),
        L["bag"]: st("home", BAG_AT[0] - 0.8, BAG_AT[1], 0, "dig"),
        L["gym"]: st("gym", -2.6, 0.9, -90, "sit", z=SIT_FLOOR)}, scale=0.90)
    add("dad", 0, DAD_SH, DAD_PA, {
        L["stairs"]: st("home", HX_ST + 0.2, 1.0, 0, "walk_a", v=(0.9, 0.0), cad=0.40, zfn=_sz, **walk),
        L["bag"]: st("home", BAG_AT[0] + 0.8, BAG_AT[1], 180, "dig"),
        L["gym"]: st("gym", -1.0, 0.9, -90, "sit", z=SIT_FLOOR)})
    # ── 경비 아저씨 (남색 · 모자): 계단 아래에서 출구를 가리킴
    add("gd", 0, GD_SH, GD_PA, {L["stairs"]: st("home", HX_ST + 4.3, 1.0, 0, "point")}, extra="cap")
    # ── 체육관: 구조대(주황 조끼 · 헬멧) + 칸막이 텐트 안 사람들
    add("rs0", 0, RS_SH, RS_PA, {L["gym"]: st("gym", 1.8, -0.55, 90, "talk")}, extra="helmet")
    add("rs1", 1, RS_SH, RS_PA, {L["gym"]: st("gym", -4.0, 2.9, 0, "walk_a", v=(0.8, 0.0), cad=0.42, **walk)}, extra="helmet")
    ex("gx0", {L["gym"]: st("gym", -4.5, 1.2, 0, "lie", z=0.05)})
    ex("gx1", {L["gym"]: st("gym", -5.4, 4.3, -90, "sit_conf", z=SIT_FLOOR)})
    ex("gx2", {L["gym"]: st("gym", -1.0, 4.9, 0, "lie", z=0.05)})
    ex("gx3", {L["gym"]: st("gym", 1.8, 0.6, -90, "sit", z=SIT_FLOOR)})
    ex("gx4", {L["gym"]: st("gym", 6.3, 1.2, 0, "lie", z=0.05)})
    ex("gx5", {L["gym"]: st("gym", 5.4, 4.3, -90, "sit_conf", z=SIT_FLOOR)})
    # ── 교문 앞 수험생들: 안내판 '연기'를 보며 어리둥절
    for k, (x, y, yaw, p0) in enumerate(((-1.7, 0.5, 60, "confused"), (-2.5, 1.0, 70, "stand"), (1.7, 0.6, 120, "stand"),
                                         (2.4, 0.3, 115, "phone"), (3.2, 1.1, 110, "confused"))):
        ex("ge%d" % k, {L["gate"]: st("gate", x, y, yaw, p0, alt=(p0, "confused" if p0 != "confused" else "stand", 1.2 + 0.2 * (k % 3), 0.3 * k))})
    # ── 밤 가로등 아래 책 읽는 학생들 (벤치 셋 + 서서 둘)
    for k, (x, y, yaw, p0) in enumerate(((-0.8, 1.2, -90, "sit_read"), (0.0, 1.2, -90, "sit_read"), (0.8, 1.2, -90, "sit_read"),
                                         (-1.9, 0.5, -60, "read"), (1.9, 0.4, -120, "read"))):
        ex("rd%d" % k, {L["lamp"]: st("gate", GT_LAMP + x, y, yaw, p0)})
    # ── 공사 작업자 (비계 위) + 보행자
    add("wk0", 0, WK_SH, RS_PA, {L["scaffold"]: st("street", -4.0, 3.75, 90, "dig", z=4.86, alt=("dig", "point", 0.55, 0.0))}, extra="helmet")
    add("wk1", 1, WK_SH, RS_PA, {L["scaffold"]: st("street", -7.0, 3.75, 90, "point", z=2.46, alt=("point", "dig", 0.7, 0.3))}, extra="helmet")
    for k, (x, y, v_) in enumerate(((3.0, 2.6, 0.9), (4.2, 2.2, 0.8), (-2.0, 3.2, -0.85))):
        ex("pd%d" % k, {L["scaffold"]: st("street", x, y, 0 if v_ > 0 else 180, "walk_a", z=0.12, v=(v_, 0.0), cad=0.36, **walk),
                        L["newbld"]: st("street", x + 6, y, 0 if v_ > 0 else 180, "walk_a", z=0.12, v=(v_, 0.0), cad=0.36, **walk)})
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
def set_of(i):
    return LINES[i]["shot"][0]


DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)


def sky(t):
    i = line_at(t)
    if i == IX["gate"]:                                                    # 수능 날 새벽
        return (0.10, 0.14, 0.34), (0.95, 0.62, 0.48), 0.2
    if i == IX["lamp"]:                                                    # 밤
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0
    if i == IX["teaser"]:                                                  # 노을
        return (0.13, 0.11, 0.34), (1.0, 0.50, 0.24), 0.3
    if set_of(i) == "lab":
        return (0.05, 0.07, 0.15), (0.12, 0.16, 0.28), 0.0
    return DAY_SKY


def env(i, tau):
    """줄별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    st_ = set_of(i)
    e = dict(sun=3.0, sun_col=(1.0, 0.95, 0.85), sun_rot=(50, 0, 15), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if st_ == "home":
        e["lt"] = {"ep36_h_fill": 90.0, "ep36_h_fill2": 50.0, "ep36_h_tv": 40.0}
        if i == IX["stairs"]:
            e.update(sun=2.4)
            e["lt"] = {"ep36_st_a": 90.0, "ep36_st_b": 110.0, "ep36_st_c": 120.0}
        elif i == IX["teaser"]:
            e.update(sun=1.6, sun_col=(1.0, 0.62, 0.42), sun_rot=(80, 0, 180), amb=0.30, amb_col=(0.78, 0.58, 0.66))
    elif st_ == "gym":
        e.update(sun=2.2, amb=0.46)
        e["lt"] = {"ep36_g%d" % k: 150.0 for k in range(5)}
    elif st_ == "class":
        e.update(sun=2.4, amb=0.36, amb_col=(0.66, 0.72, 0.88))
        e["lt"] = {"ep36_c%d" % k: 60.0 for k in range(4)}
    elif st_ == "gate":
        if i == IX["lamp"]:
            e.update(sun=0.0, amb=0.15, amb_col=(0.35, 0.42, 0.65))
            e["lt"] = {"ep36_lp": 260.0}
        else:
            e.update(sun=2.0, sun_col=(1.0, 0.72, 0.55), sun_rot=(72, 0, 20), amb=0.42, amb_col=(0.52, 0.58, 0.82))
            e["lt"] = {"ep36_gt_l1": 160.0, "ep36_gt_l2": 160.0}
    elif st_ == "street":
        e["lt"] = {"ep36_sr_fill": 300.0}
    elif st_ == "lab":
        e.update(sun=2.8, sun_rot=(55, 0, 20), amb=0.55, amb_col=(0.75, 0.80, 0.95))
        if i in (IX["bar1"], IX["bar2"]):
            e["lt"] = {"ep36_l0": 160.0}
    return e


def frame_state(t):
    """t초의 장면 상태(블렌더 없이 계산): 사람·소품 점 배열, 카메라, 조명, 세트 흔들림."""
    W = _world()
    i = line_at(t)
    a, b = shot_span(i)
    dur = max(b - a, 1e-3)
    tau = max(t - a, 0.0)             # 줄 시작 0.02초 전부터 그 줄로 치므로 음수 방지
    u = min(tau / dur, 1.0)
    cam = cam_pose(i, u, t)
    D = cam["shk"]
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
        P.append((d["x"] + ox + D[0], d["y"] + oy + D[1], d["z"] + D[2]))
        R.append((0.0, d["pitch"], math.radians(d["yaw"])))
        SC.append(d["scale"])
        PO.append(W["PI"][(d["pose"], c["hair"], c["extra"])])
    F, G, OR, BL, LT = props(i, tau, dur, u, S, t, cam)
    return dict(i=i, tau=tau, u=u, set=cam["set"], cam=cam, A=S, P=P, R=R, CO=CO, C2=C2, SC=SC, PO=PO, F=F, G=G, OR=OR, BL=BL, LT=LT,
                D=D, env=env(i, tau))


# ───────────────────────── Blender 원형(프로토) ─────────────────────────
def _mat_glow(name, strength=1.0):
    """인스턴스 'col' 색으로 빛나는 재질 (TV 선·숫자·알림·불꽃·해 등). 색 값이 1보다 크면 더 밝게 번짐."""
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
    v = X.Vox(36)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep36_sun")
    cam = K.CamRig(ctx, lens=24, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep36_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep36_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep36_fx", K.proto(ctx, "ep36_p_fx", cube(), [K.mat_inst("ep36_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep36_glow", K.proto(ctx, "ep36_p_glow", cube(), [_mat_glow("ep36_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep36_orb", K.proto(ctx, "ep36_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep36_m_orb")]),
                      N_OR, vector_scale=True)
    for ob in (gl, orb):                                              # 발광 상자·해가 그림자를 드리우지 않게
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
        for pos, name, en in S["LT"]:                                 # 움직이는 조명(펜던트) 따라가기
            ob = lights.get(name)
            if ob is not None:
                ob.location = (pos[0] + S["D"][0], pos[1] + S["D"][1], pos[2] + S["D"][2])
                ob.data.energy = en
        for key in ("solid", "glow"):                                 # 세트 전체 흔들림 (사인파 변위)
            ob = obs.get(key)
            if ob is not None:
                ob.location = tuple(float(q) for q in S["D"])
        K.set_points(people, S["P"], scale=S["SC"], rot=S["R"], col=np.array(S["CO"], np.float32),
                     colors={"col2": np.array(S["C2"], np.float32)}, pose=S["PO"])
        for ob, items in ((fx, S["F"]), (gl, S["G"]), (orb, S["OR"])):
            Pp, Sc, Sz, Rt, Co = items.arrays(S["D"])
            K.set_points(ob, Pp, scale=Sc, size=Sz, rot=Rt, col=Co)

    ctx.on_frame(upd)
