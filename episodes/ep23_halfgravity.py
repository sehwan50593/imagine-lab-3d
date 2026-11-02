"""EP23 만약에 중력이 지금의 절반이라면? (19·20편식: 블록 캐릭터·생활 장면·내레이션)

장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
운동장 점프 훅 → 아침 침대(이불이 둥실) → 한 발 디뎠더니 몸이 붕 → 계단 세 칸씩 껑충 → 체중계 70→35
→ 제자리 뛰기 두 배(높이 눈금) → 농구 덩크 → 던진 공이 한참 뒤에 내려옴 → 컵의 물이 천천히 쏟아짐
→ 반전: 중력 절반 = 공기 무게 절반 = 기압 절반 (0.5기압 ≈ 해발 5,500m ≈ 에베레스트 베이스캠프쯤): 공기 기둥이 반으로·압력계 바늘·빵빵한 과자 봉지
→ 베이스캠프(같은 옷) 숨참 → 운동장 모두 허리 숙임 → 해질녘 벤치 "공기도 중력이 붙잡아 준 덕분" → 질문 점프.
근거(설명란): 표준대기에서 0.5기압은 해발 약 5.5km (U.S. Standard Atmosphere 1976), 고도와 산소(Peacock, BMJ 1998),
점프 높이 h=v²/2g (같은 이륙 속도면 2배) · 같은 높이에서 떨어지는 시간 t=√(2h/g) (√2≈1.41배).
특수효과: 점프·낙하 전부 g=4.9m/s²로 계산한 포물선(체공 2배) — 사람은 z 오프셋, 공·물방울·이불은 상자·구 인스턴스.
체중계 숫자·압력계 바늘·과자 봉지 부풂·허리 숙인 자세(입김 상자)는 이 파일 안에서 따로 만든 소품.
"""
import json
import math
from pathlib import Path

import numpy as np

from engine.common import ramp, clamp, lerp

STYLE = "pixe"
VOICE = ("ko-KR-SunHiNeural", "+4%")
VOICE_PAD = (0.3, 0.32, 1.6)
G = 4.9                   # 중력 절반 (m/s²). 지구는 9.8
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"yard": (0, 0), "room": (300, 0), "stairs": (600, 0), "class": (900, 0), "camp": (1200, 0),
       "dusk": (1500, 0)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 중력이 지금의 절반이라면 어떻게 될까요?", gap=0.7,
         shot=("yard", (0.0, 2.2, 3.2), -90, 0, 6.8, 22, 0.92, 2)),   # 뛰어오른 주인공 얼굴이 제목 글자 아래(~53%)로
    dict(say="어느 날 아침, 중력이 반으로 줄었어요", shot=("room", (-2.8, 1.5, 0.7), -90, 62, 4.6, 28, 0.94, 0)),
    dict(say="침대에서 일어나 한 발 디뎠더니", shot=("room", (-2.7, 0.55, 1.15), -80, 8, 4.2, 28, 0.94, -3)),
    dict(say="몸이 붕! 둥실 떠올랐어요", shot=("room", (-2.7, 0.2, 1.5), -75, -5, 4.2, 26, 0.95, 0)),
    dict(say="계단은 세 칸씩 껑충껑충", shot=("stairs", (-0.1, 2.98, 3.0), -90, 6, 4.4, 28, 1.0, 0)),
    dict(say="체중계는 70에서 35로!", gap=0.5, shot=("class", (-2.85, 1.65, 1.3), -90, 5, 4.8, 26, 0.94, 0)),
    dict(say="제자리 뛰기는 두 배 높이", gap=0.5, shot=("yard", (0.05, 1.0, 1.3), -90, 3, 5.4, 28, 0.96, 0)),
    dict(say="농구 덩크가 쉬워졌어요", gap=0.65, shot=("yard", (-4.4, 0.0, 2.2), 205, -6, 6.0, 26, 0.95, -4)),
    dict(say="던진 공은 한참 뒤에야 내려오고", shot=("yard", (-0.1, 1.7, 2.3), -90, -2, 7.0, 24, 0.95, 0)),
    dict(say="컵의 물도 천천히 쏟아졌죠", gap=0.6, shot=("class", (1.6, 1.1, 0.5), -80, 0, 4.2, 28, 0.94, 0)),
    dict(say="그런데 진짜 문제는 따로 있었어요", shot=("yard", (-0.2, 1.6, 1.4), -90, 4, 4.2, 28, 0.88, 0)),
    dict(say="공기에도 무게가 있거든요", shot=("class", (1.6, 1.65, 1.75), -90, 6, 5.2, 28, 0.96, 0)),
    dict(say="그 무게가 반이니, 기압도 반!", shot=("class", (1.6, 1.65, 1.7), -90, 6, 4.6, 28, 0.92, 0)),
    dict(say="과자 봉지도 빵빵하게 부풀어요", shot=("class", (1.7, 1.1, 1.1), -90, 8, 3.2, 30, 0.92, 0)),
    dict(say="해발 5,500미터 높이의 공기와 같아요", shot=("camp", (0.0, 3.0, 1.5), -90, 3, 6.6, 24, 0.95, 0)),
    dict(say="에베레스트 베이스캠프쯤 공기예요", gap=0.5, shot=("camp", (0.0, 1.8, 1.3), -90, 5, 4.4, 28, 0.9, 0)),
    dict(say="다들 숨이 차서 주저앉았어요", gap=0.7, shot=("yard", (0.0, 2.2, 1.2), -90, 2, 6.8, 22, 0.8, 0)),
    dict(say="우리가 숨 쉬는 공기도", shot=("dusk", (0.2, 3.2, 1.2), -90, 3, 3.8, 30, 0.93, 0)),
    dict(say="중력이 붙잡아 준 덕분이었어요", gap=0.7, shot=("dusk", (0.15, 3.3, 1.3), -90, 2, 3.8, 30, 0.92, 0)),
    dict(say="중력이 절반이 되면", shot=("dusk", (0.25, 2.7, 1.3), -90, 2, 4.2, 30, 0.95, 0)),
    dict(say="제일 먼저 뭘 해 볼 건가요?", shot=("dusk", (0.35, 2.7, 1.8), -90, -2, 5.0, 28, 1.3, 0)),
]
# 이 줄 동안 카메라 목표점이 움직이는 양 (계단을 껑충껑충 내려오는 주인공을 따라감)
DRIFT = {4: (0.0, -2.5, -1.8)}
TITLE = [("만약에", "white"), ("중력이", "white"), ("지금의 절반이라면", "white"), ("어떻게 될까요?", "yellow")]
TWIST = 10          # '그런데 진짜 문제는' 줄
DUSK_FROM = 17      # 해질녘 벤치부터

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep23_halfgravity" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep23", "title": "만약에 중력이 지금의 절반이라면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "G", "mode": "lydian", "bpm": 88, "seed": 231, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

HERO_SH, HERO_PA = (0.86, 0.24, 0.22), (0.15, 0.18, 0.30)       # 주인공: 빨간 티 · 짧은 머리
FRI_SH, FRI_PA = (0.97, 0.80, 0.30), (0.30, 0.32, 0.38)         # 친구: 노란 티 · 긴 머리
EX_SH = [(0.92, 0.92, 0.90), (0.30, 0.30, 0.34), (0.45, 0.75, 0.85), (0.35, 0.65, 0.40), (0.55, 0.38, 0.70),
         (0.30, 0.45, 0.80)]                                    # 엑스트라는 빨강·노랑 빼고 (주인공이 눈에 띄게)
EX_PA = [(0.15, 0.18, 0.30), (0.20, 0.20, 0.22), (0.12, 0.12, 0.13), (0.35, 0.28, 0.20)]
WATER = (0.35, 0.65, 1.0)
BALL = (0.95, 0.45, 0.12)
PUFF = (0.96, 0.98, 1.0)
AIR = (0.70, 0.86, 1.0)
N_FX, N_GLOW, N_BALL = 220, 80, 4


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
    if line_at(t) >= DUSK_FROM:
        return (0.20, 0.17, 0.42), (0.98, 0.58, 0.38), 0.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


def env(i):
    """줄별 햇빛·주변광 (해질녘은 낮고 주황)."""
    if i >= DUSK_FROM:
        return dict(sun=2.6, sun_col=(1.0, 0.66, 0.42), sun_rot=(78, 0, 30), amb=0.2, amb_col=(0.55, 0.45, 0.66))
    return dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82))


# ───────────────────────── 물리: 중력 절반 ─────────────────────────
def hang(h):
    """정점 높이 h(m)까지 뛰어올랐다 내려오는 체공 시간(초). 같은 높이를 지구(9.8)에서 뛸 때의 √2배 (이륙 속도가 같으면 높이도 시간도 2배)."""
    return 2.0 * math.sqrt(2.0 * h / G)


def arc(tt, h):
    """뛰어오른 지 tt초 뒤의 발 높이(m). 정점 h, 공중이 아니면 0."""
    T = hang(h)
    return h - 0.5 * G * (tt - T / 2) ** 2 if 0.0 < tt < T else 0.0


def rpt(p, ang, pivot):
    """x-z 평면 점 회전 (voxel._rot_y와 같은 식): 양수 = 위쪽이 앞(+x)으로."""
    c, s = math.cos(ang), math.sin(ang)
    dx, dz = p[0] - pivot[0], p[1] - pivot[1]
    return pivot[0] + c * dx + s * dz, pivot[1] - s * dx + c * dz


def hopper(h, start, rest=0.14, air="star", **base):
    """같은 높이로 되풀이해 뛰는 사람. start = 첫 이륙 시각(줄 시작 기준, 음수면 이미 공중). base = 같이 덮어쓸 x·y·yaw."""
    P = hang(h) + rest

    def fn(tl, du, u):
        if tl < start:
            return dict(z=0.0, pose="stand", **base)
        z = arc((tl - start) % P, h)
        return dict(z=z, pose=air if z > 0.02 else "stand", **base)
    return fn


def bounce_z(z0, v0, tau, e=0.55, r=0.12):
    """공이 z0에서 아래쪽 속도 v0로 시작해 바닥에서 두 번 튕기는 높이(m)."""
    z = z0 - v0 * tau - 0.5 * G * tau * tau
    if z > r:
        return z
    t1 = (-v0 + math.sqrt(v0 * v0 + 2 * G * (z0 - r))) / G
    vb = e * (v0 + G * t1)
    t = tau - t1
    for _ in range(2):
        T = 2 * vb / G
        if t < T:
            return r + vb * t - 0.5 * G * t * t
        t -= T
        vb *= e
    return r


def ballistic(p0, v0, tt, floor=0.02):
    """p0에서 v0로 던진 작은 물체의 tt초 뒤 위치 (g=4.9). 바닥에 닿으면 (그 자리, True)."""
    x, y = p0[0] + v0[0] * tt, p0[1] + v0[1] * tt
    z = p0[2] + v0[2] * tt - 0.5 * G * tt * tt
    if z <= floor:
        # 바닥에 닿은 시각까지의 이동만 반영
        disc = v0[2] ** 2 + 2 * G * (p0[2] - floor)
        t1 = (v0[2] + math.sqrt(max(disc, 0.0))) / G
        return (p0[0] + v0[0] * t1, p0[1] + v0[1] * t1, floor), True
    return (x, y, z), False


# ───────────────────────── 줄별 움직임 ─────────────────────────
def _r2(tl, du, u):
    """침대 끝에 앉았다가 일어나 한 걸음씩 침대 앞으로."""
    if tl < 0.55:
        return dict(x=-2.8, y=0.80, z=0.0, pose="sit")
    if tl < 0.9:
        return dict(x=-2.8, y=0.38, z=0.0, pose="stand")
    k = tl - 0.9
    return dict(x=-2.8, y=max(0.38 - 0.2 * k, 0.08), z=0.0, pose="walk_a" if int(k / 0.22) % 2 == 0 else "walk_b")


def _r3(tl, du, u):
    """몸이 붕: 높이 0.8m 점프(체공 1.14초) 뒤 작은 통통."""
    z = arc(tl + 0.08, 0.8)
    if z > 0.0:
        return dict(x=-2.8, y=0.2 - 0.05 * tl, z=z, pose="star")
    z2 = arc(tl - 1.3, 0.45) + arc(tl - 2.5, 0.2)
    return dict(x=-2.8, y=0.14, z=z2, pose="star" if z2 > 0.02 else "stand")


BOUND, DROP, VZ0 = 0.84, 0.6, 1.0                      # 계단 3칸: 런 0.84, 높이 0.6, 이륙 상승 1.0m/s
T_B = (VZ0 + math.sqrt(VZ0 ** 2 + 2 * G * DROP)) / G   # 한 번 껑충하는 시간


def _s4(tl, du, u):
    """위층 참에서 계단을 세 칸씩 껑충껑충 내려옴."""
    t0, rest = 0.12, 0.08
    if tl < t0:
        return dict(x=-0.1, y=2.98, z=1.8, pose="stand")
    P = T_B + rest
    k = tl - t0
    n = int(k // P)
    if n >= 3:
        return dict(x=-0.1, y=0.46, z=0.0, pose="stand")
    kk = k - n * P
    y0, z0 = 2.98 - BOUND * n, 1.8 - DROP * n
    if kk < T_B:
        return dict(x=-0.1, y=y0 - BOUND * kk / T_B, z=z0 + VZ0 * kk - 0.5 * G * kk * kk, pose="leap")
    return dict(x=-0.1, y=y0 - BOUND, z=z0 - DROP, pose="stand")


def scale_value(tl, du):
    """체중계 숫자: 70에서 잠깐 있다가 35까지 굴러 내려감."""
    t_sw = 0.4 * du
    return int(round(lerp(70, 35, clamp((tl - t_sw) / 0.45))))


def _c5(tl, du, u):
    t_hop = 0.4 * du + 0.5
    if tl < t_hop:
        return dict(z=0.085, pose="stand")
    z = arc(tl - t_hop, 0.3)
    return dict(z=0.085 + z, pose="star" if z > 0.02 else "talk")


CUP_X, CUP_Y0, TABLE_TOP, EDGE_Y = 1.62, 0.80, 0.74, 0.60
T_BUMP, V_SLIDE, CUP_H = 0.55, 0.9, 0.17


def cup_path(tl):
    """(위치, 기울기 rad, 상태) — 컵이 밀려 탁자 끝에서 떨어져 바닥에 눕는다."""
    z_cup = TABLE_TOP + CUP_H / 2
    t_leave = T_BUMP + (CUP_Y0 - EDGE_Y) / V_SLIDE
    if tl < T_BUMP:
        return (CUP_X, CUP_Y0, z_cup), 0.0, "table"
    if tl < t_leave:
        return (CUP_X, CUP_Y0 - V_SLIDE * (tl - T_BUMP), z_cup), 0.0, "slide"
    tau = tl - t_leave
    z_floor = 0.06
    T_fall = math.sqrt(2 * (z_cup - z_floor) / G)
    if tau < T_fall:
        return (CUP_X, EDGE_Y - V_SLIDE * tau, z_cup - 0.5 * G * tau * tau), 1.6 * tau / T_fall, "fall"
    return (CUP_X, EDGE_Y - V_SLIDE * T_fall, z_floor), 1.6, "floor"


def _c9h(tl, du, u):
    return dict(pose="sit" if tl < T_BUMP + 0.1 else "sit_oh")


def _c9f(tl, du, u):
    return dict(pose="sit" if tl < T_BUMP + 0.3 else "sit_oh")


def bag_swell(tl, du):
    return ramp(tl, 0.25 * du, 0.25 * du + 1.1)


def _c13h(tl, du, u):
    return dict(pose="sit" if bag_swell(tl, du) < 0.15 else "sit_oh")


def _c13f(tl, du, u):
    return dict(pose="sit" if bag_swell(tl, du) < 0.3 else "sit_oh")


DUNK_X0, DUNK_XT, DUNK_XA, DUNK_Y = -2.9, -3.5, -5.25, -0.34    # 출발 · 이륙 · 정점(공이 림 중앙 위) x, 몸 y
DUNK_H, DUNK_TO = 1.37, 0.28                                     # 점프 높이, 이륙 시각
RIM = (-5.65, 0.0, 3.05)
DUNK_HAND = (0.40, -0.34, 1.83)                                  # 덩크 자세에서 공 위치(캐릭터 기준 앞·옆·위)


def _y7(tl, du, u):
    """주인공 덩크: 달려와 → 이륙 → 정점에서 림 위로 공을 꽂음."""
    T = hang(DUNK_H)
    if tl < DUNK_TO:
        x = lerp(DUNK_X0, DUNK_XT, tl / DUNK_TO)
        return dict(x=x, y=DUNK_Y, yaw=180, z=0.0, pose="walk_a" if int(tl / 0.14) % 2 == 0 else "walk_b")
    k = tl - DUNK_TO
    if k < T:
        x = DUNK_XT + (DUNK_XA - DUNK_XT) * min(k / (T / 2), 1.0)
        return dict(x=x, y=DUNK_Y, yaw=180, z=arc(k, DUNK_H), pose="dunk")
    return dict(x=DUNK_XA, y=DUNK_Y, yaw=180, z=0.0, pose="stand")


TOSS_X, TOSS_Y, TOSS_T0, TOSS_V, TOSS_Z = -0.6, 1.8, 0.35, 5.0, 1.15
CATCH = (0.45, 1.6, 1.98)            # 주인공이 두 손 들어 공을 받는 자리


def _y8f(tl, du, u):
    return dict(x=TOSS_X, y=TOSS_Y, yaw=-90, pose="stand" if tl < TOSS_T0 else "up")


def _d19(h, start, x, y):
    return hopper(h, start, 0.25, "star", x=x, y=y)


# ───────────────────────── 세트 ─────────────────────────
def _school(v, dusk):
    """운동장 뒤 2층 학교: 낮엔 하늘색 창, 해질녘엔 노랗게 켜진 창."""
    rs = v.rs
    v.box(-17, 17, 9.0, 15.0, 0, 7.6, (0.80, 0.68, 0.62) if dusk else (0.91, 0.85, 0.72), jit=0.03)
    v.box(-17, 17, 8.7, 15.0, 7.0, 7.6, (0.55, 0.36, 0.32), jit=0.03)                 # 처마 띠
    v.box(-2.2, 2.2, 8.85, 9.0, 0, 3.4, (0.62, 0.50, 0.42), jit=0.03)                   # 현관
    v.box(-1.4, 1.4, 8.82, 8.85, 0, 2.6, (0.18, 0.20, 0.24), jit=0)
    for fl in range(2):
        z = 1.5 + 3.3 * fl
        for k in range(-7, 8):
            x = 2.3 * k
            if fl == 0 and abs(x) < 3.0:
                continue
            on = dusk and rs.random() < 0.6
            col = (1.0, 0.82, 0.5) if on else ((0.14, 0.16, 0.24) if dusk else (0.58, 0.78, 0.94))
            v.box(x - 0.85, x + 0.85, 8.97, 9.0, z, z + 1.6, col, jit=0, glow=bool(on))


def _bench(v, cx, cy, w=3.1):
    x0, x1 = cx - w / 2, cx + w / 2
    col, dk = (0.62, 0.42, 0.25), (0.30, 0.31, 0.34)
    v.box(x0, x1, cy - 0.2, cy + 0.25, 0.40, 0.45, col)                                  # 앉는 판
    v.box(x0, x1, cy + 0.22, cy + 0.28, 0.45, 0.92, col)                                 # 등받이
    for x in (x0 + 0.1, x1 - 0.1):
        v.box(x - 0.04, x + 0.04, cy - 0.15, cy + 0.2, 0, 0.40, dk)


def _yard(v, dusk=False):
    from engine import voxel as X
    v.floor(-17, 17, -10, 9, (0.74, 0.62, 0.52) if dusk else (0.80, 0.68, 0.50), 1.0, "check")
    v.floor(-17, 17, 5.2, 8.6, (0.74, 0.36, 0.30), 0.5, "check", z=0.012)                # 달리기 트랙
    for yy in (6.3, 7.4):
        v.box(-17, 17, yy - 0.03, yy + 0.03, 0.012, 0.02, (0.95, 0.95, 0.92), jit=0)
    v.floor(-7.6, 4.2, -4.6, 4.6, (0.30, 0.50, 0.62), 0.5, "check", z=0.012)           # 농구장
    ln = (0.96, 0.96, 0.94)
    for x0, x1, y0, y1 in ((-7.3, 3.9, -4.3, -4.22), (-7.3, 3.9, 4.22, 4.3), (-7.3, -7.22, -4.3, 4.3),
                           (3.82, 3.9, -4.3, 4.3), (-7.3, -1.5, -2.49, -2.41), (-7.3, -1.5, 2.41, 2.49),
                           (-1.58, -1.5, -2.49, 2.49)):
        v.box(x0, x1, y0, y1, 0.012, 0.022, ln, jit=0)
    # 골대: 백보드 없이 림·그물·옆 기둥 (뒤에서도 훤히 보이게)
    pole, org = (0.28, 0.30, 0.34), (1.0, 0.45, 0.10)
    v.box(-5.73, -5.57, 1.32, 1.48, 0, 3.45, pole)
    v.box(-5.69, -5.61, 0.27, 1.34, 3.0, 3.08, pole)
    cx, cy = RIM[0], RIM[1]
    for x0, x1, y0, y1 in ((cx - 0.25, cx + 0.25, 0.21, 0.25), (cx - 0.25, cx + 0.25, -0.25, -0.21),
                           (cx - 0.25, cx - 0.21, -0.25, 0.25), (cx + 0.21, cx + 0.25, -0.25, 0.25)):
        v.box(x0, x1, y0, y1, 3.03, 3.07, org, jit=0)
    for z0, z1, hh in ((2.78, 3.03, 0.2), (2.55, 2.78, 0.13)):                            # 그물: 세로 줄 두 단
        for dx, dy in ((-hh, -hh), (hh, -hh), (-hh, hh), (hh, hh), (0, -hh), (0, hh), (-hh, 0), (hh, 0)):
            v.box(cx + dx - 0.008, cx + dx + 0.008, cy + dy - 0.008, cy + dy + 0.008, z0, z1, (0.95, 0.95, 0.95), jit=0)
    _bench(v, 6.5, 3.2) if not dusk else _bench(v, 0.05, 3.5)
    for x, y in ((-3.0, 6.3), (4.2, 6.8), (-12.0, 6.5), (11.0, 6.6)):
        X.tree(v, x, y)
    for yy in (-2.5, 2.5):                                                               # 축구 골대
        v.box(11.5 - 0.05, 11.5 + 0.05, yy - 0.05, yy + 0.05, 0, 2.2, (0.95, 0.95, 0.95), jit=0)
    v.box(11.45, 11.55, -2.5, 2.5, 2.15, 2.25, (0.95, 0.95, 0.95), jit=0)
    _school(v, dusk)
    if dusk:
        for x in (-2.6, 3.2):
            X.street_lamp(v, x, 4.1, h=4.2, energy=150)


def _room(v):
    from engine import voxel as X
    v.floor(-3.6, 3.6, -2.6, 2.6, (0.72, 0.55, 0.38), 0.25, "wood")
    v.wall((-3.6, 2.6), (3.6, 2.6), 0, 2.6, (0.93, 0.90, 0.84), 0.25, face=-1)
    v.wall((-3.6, -2.6), (-3.6, 2.6), 0, 2.6, (0.86, 0.90, 0.88), 0.25, face=-1)
    v.wall((3.6, -2.6), (3.6, 2.6), 0, 2.6, (0.86, 0.90, 0.88), 0.25, face=1)
    v.window(0.5, 2.3, 2.59, 0.9, 2.2, night=False)
    v.box(-3.5, -2.1, 0.5, 2.55, 0.0, 0.26, (0.55, 0.38, 0.24))                       # 침대 틀
    v.box(-3.47, -2.13, 0.53, 2.52, 0.26, 0.46, (0.95, 0.95, 0.93), jit=0.02)         # 매트리스
    v.box(-3.3, -2.3, 2.05, 2.47, 0.46, 0.58, (0.97, 0.97, 0.97), jit=0.01)           # 베개
    v.box(-3.5, -2.1, 2.52, 2.58, 0.0, 1.05, (0.38, 0.25, 0.15))                      # 머리판
    v.box(-1.95, -1.5, 2.1, 2.55, 0, 0.5, (0.62, 0.42, 0.25))                         # 협탁 + 알람시계
    v.box(-1.82, -1.62, 2.2, 2.4, 0.5, 0.62, (0.2, 0.2, 0.22))
    v.box(-1.8, -1.64, 2.19, 2.2, 0.53, 0.59, (1.0, 0.3, 0.2), jit=0, glow=True)
    X.table(v, 2.8, 2.15, 1.5, 0.7, 0.74, (0.82, 0.68, 0.5))                           # 책상 + 노트북
    X.chair(v, 2.6, 1.55, 90)
    v.box(2.45, 2.95, 2.1, 2.4, 0.74, 0.77, (0.7, 0.72, 0.75))
    v.box(2.45, 2.95, 2.38, 2.4, 0.77, 1.1, (0.15, 0.15, 0.17))
    v.box(2.5, 2.9, 2.36, 2.38, 0.8, 1.06, (0.55, 0.78, 1.0), jit=0, glow=True)
    v.floor(-1.5, 1.2, -1.2, 1.4, (0.82, 0.5, 0.42), 0.25, "plain", z=0.01)             # 러그
    v.box(3.1, 3.55, -2.2, -1.75, 0, 0.45, (0.35, 0.6, 0.45))                           # 화분
    v.box(3.05, 3.6, -2.25, -1.7, 0.45, 1.15, (0.25, 0.55, 0.25), jit=0.1)
    for k, c in enumerate(((0.85, 0.3, 0.3), (0.3, 0.5, 0.85), (0.95, 0.8, 0.3), (0.35, 0.65, 0.4))):  # 책꽂이
        v.box(-3.55, -3.2, -2.0 + 0.32 * k, -1.7 + 0.32 * k, 0, 1.5, c if k % 2 else (0.8, 0.8, 0.78))
    v.light(-0.3, 0.5, 2.3, 110, (1.0, 0.95, 0.86), 0.5)
    v.light(1.4, 2.2, 1.7, 100, (0.85, 0.92, 1.0), 0.8)


def stair_z(y):
    """계단실 바닥 높이: y<0.6 바닥, 9칸(런 0.28·높이 0.2), y≥3.12 위층 참."""
    if y < 0.6:
        return 0.0
    return min(0.2 * (int((y - 0.6) / 0.28) + 1), 1.8)


def _stairs(v):
    v.floor(-1.4, 1.4, -3.0, 0.6, (0.80, 0.78, 0.74), 0.4, "check")
    for n in range(1, 10):
        y0 = 0.6 + 0.28 * (n - 1)
        v.box(-1.39, 1.39, y0, y0 + 0.28, 0, 0.2 * n, (0.84, 0.80, 0.74) if n % 2 else (0.52, 0.60, 0.74))
        v.box(-1.39, 1.39, y0, y0 + 0.05, 0.2 * n, 0.2 * n + 0.012, (0.95, 0.80, 0.20), jit=0)
    v.box(-1.39, 1.39, 3.12, 4.59, 0, 1.8, (0.78, 0.76, 0.72))                          # 위층 참
    v.wall((-1.4, -3.0), (-1.4, 4.6), 0, 4.8, (0.95, 0.92, 0.80), 0.4, face=-1)
    v.wall((1.4, -3.0), (1.4, 4.6), 0, 4.8, (0.95, 0.92, 0.80), 0.4, face=1)
    v.wall((-1.4, 4.6), (1.4, 4.6), 0, 4.8, (0.92, 0.94, 0.88), 0.4, face=-1)
    v.window(-0.8, 0.8, 4.59, 2.6, 4.0, night=False)
    for n in range(1, 10):                                                                # 오른쪽 난간
        y0 = 0.6 + 0.28 * (n - 1)
        v.box(1.18, 1.28, y0, y0 + 0.28, 0.2 * n + 0.86, 0.2 * n + 0.92, (0.28, 0.30, 0.34), jit=0)
        if n % 3 == 1:
            v.box(1.2, 1.26, y0 + 0.1, y0 + 0.16, 0.2 * n, 0.2 * n + 0.88, (0.28, 0.30, 0.34), jit=0)
    v.box(1.18, 1.28, 3.12, 4.4, 2.66, 2.72, (0.28, 0.30, 0.34), jit=0)
    v.light(0.0, 1.8, 3.4, 140, (1.0, 0.97, 0.9), 0.5)
    v.light(0.0, -0.5, 2.6, 90, (1.0, 0.97, 0.9), 0.5)


def _class(v):
    from engine import voxel as X
    v.floor(-4.5, 4.5, -3.0, 3.0, (0.76, 0.62, 0.44), 0.5, "wood")
    v.wall((-4.5, 3.0), (4.5, 3.0), 0, 3.0, (0.94, 0.92, 0.84), 0.5, face=-1)
    v.wall((-4.5, -3.0), (-4.5, 3.0), 0, 3.0, (0.88, 0.92, 0.88), 0.5, face=-1)
    v.wall((4.5, -3.0), (4.5, 3.0), 0, 3.0, (0.88, 0.92, 0.88), 0.5, face=1)
    v.window(-2.0, 1.2, -4.49, 0.9, 2.4, night=False, face=1, axis="x")
    v.box(-3.4, 0.8, 2.94, 2.98, 0.84, 2.36, (0.52, 0.38, 0.24))                         # 칠판
    v.box(-3.3, 0.7, 2.92, 2.94, 0.94, 2.26, (0.10, 0.28, 0.22), jit=0.015)
    for x0, x1, z0, z1 in ((-2.9, -1.5, 1.7, 1.73), (-2.9, -2.2, 1.5, 1.53), (-1.0, 0.1, 1.2, 1.23),
                           (-3.0, -2.97, 1.1, 1.9), (-0.4, 0.4, 1.8, 1.83)):
        v.box(x0, x1, 2.91, 2.92, z0, z1, (0.93, 0.93, 0.9), jit=0)
    # 압력계(벽걸이): 값 0~1.2기압이 -120°~+120° 호. 바늘은 따로 움직임
    v.box(GAUGE[0] - 0.45, GAUGE[0] + 0.45, 2.94, 2.98, 1.85, 2.75, (0.22, 0.22, 0.25), jit=0)
    v.box(GAUGE[0] - 0.4, GAUGE[0] + 0.4, 2.92, 2.94, 1.9, 2.7, (0.96, 0.96, 0.93), jit=0)
    for k in range(13):
        th = math.radians(-120 + 20 * k)
        val = 0.1 * k
        col = (0.9, 0.25, 0.2) if val < 0.65 else ((0.95, 0.78, 0.2) if val < 0.95 else (0.3, 0.7, 0.35))
        x, z = GAUGE[0] + 0.28 * math.sin(th), GAUGE[1] + 0.28 * math.cos(th)
        v.box(x - 0.022, x + 0.022, 2.915, 2.92, z - 0.022, z + 0.022, col, jit=0)
    v.box(GAUGE[0] - 0.03, GAUGE[0] + 0.03, 2.9, 2.92, GAUGE[1] - 0.03, GAUGE[1] + 0.03, (0.15, 0.15, 0.17), jit=0)
    # 점심 탁자 + 의자 둘 + 식판
    X.table(v, 1.55, 1.0, 1.8, 0.8, 0.74, (0.86, 0.72, 0.52))
    X.chair(v, 1.9, 1.65, -90)
    X.chair(v, 1.2, 1.65, -90)
    for x in (1.2, 1.9):
        v.box(x - 0.25, x + 0.25, 0.85, 1.2, 0.74, 0.77, (0.78, 0.8, 0.84))
        v.box(x - 0.2, x - 0.05, 0.95, 1.1, 0.77, 0.82, (0.97, 0.97, 0.95))
        v.box(x + 0.02, x + 0.2, 0.95, 1.1, 0.77, 0.80, (0.85, 0.35, 0.25))
    # 체중계 발판 + 숫자 화면 기둥
    v.box(-2.9, -1.9, 1.3, 2.0, 0, 0.08, (0.22, 0.24, 0.28))
    v.box(-2.86, -1.94, 1.34, 1.96, 0.08, 0.085, (0.55, 0.57, 0.6), jit=0.02)
    v.box(-3.42, -3.32, 1.66, 1.74, 0, 1.1, (0.25, 0.27, 0.3))
    v.box(-3.8, -2.98, 1.6, 1.78, 1.1, 1.64, (0.12, 0.12, 0.14), jit=0)
    v.box(-3.76, -3.02, 1.585, 1.6, 1.14, 1.6, (0.02, 0.05, 0.04), jit=0)
    for (x, y) in ((-3.9, 0.0), (-3.9, -1.2), (3.9, 1.4)):                              # 책상 몇 개
        X.table(v, x, y, 0.8, 0.6, 0.72, (0.86, 0.72, 0.52))
    v.box(3.0, 4.4, 2.94, 2.98, 1.2, 2.2, (0.65, 0.5, 0.35))                             # 게시판
    for k, c in enumerate(((0.95, 0.8, 0.3), (0.5, 0.75, 0.95), (0.95, 0.55, 0.6), (0.6, 0.85, 0.5))):
        v.box(3.1 + 0.33 * k, 3.38 + 0.33 * k, 2.92, 2.94, 1.5 + 0.1 * (k % 2), 1.95 + 0.1 * (k % 2), c, jit=0)
    for x in (-2.2, 0.6, 3.0):
        v.box(x - 0.6, x + 0.6, -0.1, 0.5, 2.95, 3.0, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.2, 2.7, 110, (0.95, 0.97, 1.0), 0.6)


def _camp(v):
    rs = v.rs
    v.floor(-30, 30, -8, 40, (0.64, 0.58, 0.50), 1.0, "plain")
    for _ in range(40):                                                                   # 눈 얼룩·돌
        x, y, w = float(rs.uniform(-18, 18)), float(rs.uniform(3.5, 30)), float(rs.uniform(0.8, 2.5))
        v.box(x, x + w, y, y + w * 0.7, 0, 0.03, (0.93, 0.95, 0.97), jit=0.02)
    for _ in range(30):
        x, y, w = float(rs.uniform(-18, 18)), float(rs.uniform(3.5, 28)), float(rs.uniform(0.3, 0.9))
        if abs(x) < 3.0 and y < 5.0:
            continue
        v.box(x, x + w, y, y + w, 0, w * 0.7, (0.45, 0.43, 0.42), jit=0.08)
    for x, y, c in ((-2.5, 4.0, (0.95, 0.55, 0.15)), (2.7, 4.6, (0.2, 0.55, 0.85)), (-8.5, 7.5, (0.85, 0.2, 0.25)),
                    (9.0, 6.0, (0.95, 0.8, 0.2)), (0.0, 7.0, (0.3, 0.7, 0.4))):            # 텐트 (계단식 상자)
        v.box(x - 1.3, x + 1.3, y - 1.0, y + 1.0, 0, 0.65, c)
        v.box(x - 1.0, x + 1.0, y - 0.85, y + 0.85, 0.65, 1.2, tuple(0.95 * q for q in c))
        v.box(x - 0.6, x + 0.6, y - 0.7, y + 0.7, 1.2, 1.55, tuple(0.9 * q for q in c))
        v.box(x - 0.35, x + 0.15, y - 1.03, y - 1.0, 0, 0.5, (0.1, 0.1, 0.12), jit=0)
    for x in (-6.6, 6.6):                                                                 # 룽다(깃발 줄)
        v.box(x - 0.05, x + 0.05, 8.95, 9.05, 0, 3.6, (0.4, 0.3, 0.2))
    flag = [(0.25, 0.45, 0.9), (0.95, 0.95, 0.95), (0.9, 0.25, 0.2), (0.3, 0.75, 0.35), (0.95, 0.8, 0.2)]
    for k in range(27):
        x = -6.3 + 0.47 * k
        zt = 3.45 - 0.6 * math.sin(math.pi * (x + 6.6) / 13.2)
        v.box(x, x + 0.47, 8.99, 9.01, zt, zt + 0.015, (0.85, 0.85, 0.82), jit=0)
        v.box(x + 0.05, x + 0.35, 8.985, 9.015, zt - 0.38, zt, flag[k % 5], jit=0.03)
    # 먼 산 (계단식 상자). 산끼리 x가 겹치므로 앞면이 같은 평면에 놓이면 서로 그림자를 드리워 새까맣게 나옴 → 산마다 y를 0.7m씩 비킴
    for m, (cx, w, hh) in enumerate(((-12, 34, 17), (10, 40, 21), (32, 26, 14))):
        lv = (0.0, 0.28, 0.5, 0.68, 0.84, 1.0)
        y0 = 30 + 0.7 * m
        for k in range(5):
            f = 1 - 0.19 * k
            c = (0.42, 0.46, 0.58) if k < 3 else (0.96, 0.97, 1.0)
            v.box(cx - w * f / 2, cx + w * f / 2, y0 + 1.2 * k, y0 + 14 - 1.2 * k, hh * lv[k], hh * lv[k + 1], c, jit=0.03)


# ───────────────────────── 캐릭터 ─────────────────────────
EXTRA = ["star", "up", "dunk", "leap", "bent", "sit_oh"]
LEAN, HEADBACK, ARM_W = 1.08, 0.80, 0.80                 # 허리 숙인 자세: 몸 기울기·고개 젖힘·팔(월드 기준 뒤로)
HEAD_BENT = rpt(rpt((0.0, 1.59), -HEADBACK, (0.0, 1.36)), LEAN, (0.0, 0.78))            # (앞, 높이)
MOUTH_BENT = rpt(rpt((0.235, 1.425), -HEADBACK, (0.0, 1.36)), LEAN, (0.0, 0.78))


def pose_index(pose, hair):
    from engine import voxel as X
    if pose in X.POSES:
        return hair * X.NPOSE + X.POSES[pose]
    return 2 * X.NPOSE + 2 * EXTRA.index(pose) + hair


def _rot_x(bm, ang, pivot):
    """x축(앞) 둘레 회전: 팔다리를 옆으로 벌림. 왼쪽(+y) 팔다리는 양수=바깥."""
    c, s = math.cos(ang), math.sin(ang)
    for v in bm.verts:
        y, z = v.co.y - pivot[1], v.co.z - pivot[2]
        v.co.y, v.co.z = pivot[1] + c * y - s * z, pivot[2] + s * y + c * z
    return bm


def _variant(kind, lh):
    """voxel._person 으로 만든 서 있는(또는 앉은) 사람에서 입을 벌리고 팔다리·몸을 돌린 새 자세."""
    from engine import bkit as K
    from engine import voxel as X
    sit = kind == "sit_oh"
    P = X._person(X.SIT if sit else X.STAND, lh)
    hip = 0.47 if sit else 0.78
    hz = hip + 0.58
    for k, (bm, mi) in enumerate(P):
        if mi == 6:                                    # 입: 크게 벌림
            bm.free()
            P[k] = (K.bm_cube(0.02, 0.13, 0.07, (0.232, 0, hz + 0.04), bottom=True), 6)
    legs, body, arms = P[:4], P[4:-4], P[-4:]

    def arm(k, pitch=0.0, roll=0.0):                   # k 0=오른팔(-y) 1=왼팔(+y)
        for bm, _ in arms[2 * k:2 * k + 2]:
            if roll:
                _rot_x(bm, roll, (0, -0.34 if k == 0 else 0.34, hip + 0.54))
            if pitch:
                X._rot_y(bm, pitch, (0, 0, hip + 0.54))

    def leg(k, pitch=0.0, roll=0.0):
        for bm, _ in legs[2 * k:2 * k + 2]:
            if roll:
                _rot_x(bm, roll, (0, -0.11 if k == 0 else 0.11, hip))
            if pitch:
                X._rot_y(bm, pitch, (0, 0, hip))

    if kind == "star":
        arm(0, roll=-2.5), arm(1, roll=2.5), leg(0, roll=-0.3), leg(1, roll=0.3)
    elif kind == "up":
        arm(0, pitch=-3.05), arm(1, pitch=-3.05), leg(0, roll=-0.08), leg(1, roll=0.08)
    elif kind == "dunk":
        arm(0, pitch=-2.3), arm(1, roll=1.1), leg(0, pitch=0.55), leg(1, pitch=-0.45)
    elif kind == "leap":
        arm(0, roll=-1.35), arm(1, roll=1.35), leg(0, pitch=-0.5, roll=-0.12), leg(1, pitch=0.45, roll=0.12)
    elif kind == "bent":
        arm(0, pitch=ARM_W - LEAN), arm(1, pitch=ARM_W - LEAN)
        for bm, _ in body[1:]:                         # 머리·얼굴·머리카락: 목을 젖혀 앞을 봄
            X._rot_y(bm, -HEADBACK, (0, 0, hz))
        for bm, _ in body + arms:
            X._rot_y(bm, LEAN, (0, 0, hip))
    elif kind == "sit_oh":
        arm(0, pitch=-0.9), arm(1, pitch=-0.5)
    return P


def _extra_protos(ctx, mats):
    from engine import bkit as K
    out = []
    for kind in EXTRA:
        for lh in (False, True):
            out.append(K.proto(ctx, f"ep23_p_{kind}_{int(lh)}", K.join_bms(_variant(kind, lh)), mats))
    return out


def head_pt(d):
    """머리 중심(세트 좌표)과 얼굴이 향한 방향 단위벡터."""
    s = d["scale"]
    a = math.radians(d["yaw"])
    ca, sa = math.cos(a), math.sin(a)
    p = d["pose"]
    if p == "lie":
        return (d["x"] + ca * -1.59 * s, d["y"] + sa * -1.59 * s, d["z"] + 0.24 * s), (0.0, 0.0, 1.0)
    if p == "bent":
        fw, hh = HEAD_BENT
        pit = LEAN - HEADBACK
        return ((d["x"] + ca * fw * s, d["y"] + sa * fw * s, d["z"] + hh * s),
                (ca * math.cos(pit), sa * math.cos(pit), -math.sin(pit)))
    hz = 1.28 if p.startswith("sit") else 1.59
    return (d["x"], d["y"], d["z"] + hz * s), (ca, sa, 0.0)


def mouth_pt(d):
    s = d["scale"]
    a = math.radians(d["yaw"])
    ca, sa = math.cos(a), math.sin(a)
    if d["pose"] == "bent":
        fw, hh = MOUTH_BENT
    else:
        fw, hh = 0.235, (1.115 if d["pose"].startswith("sit") else 1.425)
    return d["x"] + ca * fw * s, d["y"] + sa * fw * s, d["z"] + hh * s


_CAST = []


def cast():
    """[dict(set, x, y, yaw, pose, hair, shirt, pants, scale, z, over={줄: dict 또는 함수(tl, du, u)}, only=보이는 줄 집합, tag)]"""
    if _CAST:
        return _CAST
    rs = np.random.default_rng(231)
    C = _CAST

    def add(st, x, y, yaw, pose, hair, shirt, pants, scale=1.0, z=0.0, over=None, only=None, tag=""):
        C.append(dict(set=st, x=x, y=y, yaw=yaw, pose=pose, hair=hair, shirt=shirt, pants=pants, scale=scale, z=z,
                      over=over or {}, only=only, tag=tag))
    H = lambda st, x, y, yaw, pose, **kw: add(st, x, y, yaw, pose, 0, HERO_SH, HERO_PA, tag="hero", **kw)
    F = lambda st, x, y, yaw, pose, **kw: add(st, x, y, yaw, pose, 1, FRI_SH, FRI_PA, tag="friend", **kw)
    # 방: L1 잠 → L2 침대 끝에서 일어나 한 걸음 → L3 둥실
    H("room", -2.8, 0.62, -90, "lie", z=0.46, only={1, 2, 3}, over={2: _r2, 3: _r3})
    # 계단 L4
    H("stairs", -0.1, 2.98, -90, "stand", z=1.8, only={4}, over={4: _s4})
    # 교실: 체중계 L5, 점심 L9(컵)·L11~L12(압력계·공기 기둥)·L13(과자 봉지) (주인공 오른쪽·친구 왼쪽)
    H("class", -2.4, 1.65, -90, "stand", z=0.085, only={5}, over={5: _c5})
    H("class", 1.9, 1.65, -90, "sit", only={9, 11, 12, 13},
      over={9: _c9h, 11: dict(pose="sit_conf"), 12: dict(pose="sit_conf"), 13: _c13h})
    F("class", 1.2, 1.65, -90, "sit", only={9, 11, 12, 13}, over={9: _c9f, 13: _c13f})
    # 운동장: 훅 L0 · 제자리 뛰기 L6 · 덩크 L7 · 공 던지기 L8 · 반전 L10 · 숨참 L16
    H("yard", 0.0, 0.9, -90, "stand", only={0, 6, 7, 8, 10, 16},
      over={0: hopper(1.15, -0.6, 0.15, "up"), 6: hopper(0.92, 0.25, 0.22, "up", x=0.1, y=1.0), 7: _y7,
            8: dict(x=0.45, y=1.7, pose="up"), 10: dict(x=0.0, y=1.6, pose="confused"),
            16: dict(pose="bent")})
    F("yard", -0.9, 2.0, -90, "stand", only={0, 6, 8, 10, 16},
      over={0: hopper(0.9, -0.3, 0.2, "star", x=-0.9, y=2.0), 6: dict(x=-0.6, y=1.2, pose="talk"), 8: _y8f,
            10: dict(x=-0.85, y=1.75), 16: dict(x=-0.8, pose="bent")})
    for x, y, hair, h, st, air in ((-1.9, 3.0, 0, 0.85, 0.2, "star"), (-0.55, 3.4, 1, 0.7, -0.5, "up"),
                                   (0.85, 3.0, 0, 0.95, -0.1, "star"), (2.05, 3.4, 0, 0.8, -0.45, "up"),
                                   (-2.7, 4.2, 1, 1.0, -0.35, "star"), (2.8, 4.3, 0, 0.75, 0.0, "up"),
                                   (0.3, 4.5, 1, 0.9, -0.3, "star"), (1.0, 2.0, 1, 0.8, -0.2, "up")):
        back = y > 2.5                                       # 반전 컷(L10)에선 주인공 뒤쪽 아이들만 계속 뜀 (앞을 가리지 않게)
        add("yard", x, y, -90, "stand", hair, EX_SH[int(rs.integers(len(EX_SH)))], EX_PA[int(rs.integers(len(EX_PA)))],
            only={0, 10, 16} if back else {0, 16},
            over={0: hopper(h, st, 0.16, air), 16: dict(pose="bent"), **({10: hopper(h, st, 0.16, air)} if back else {})})
    # 베이스캠프 L14·L15: 같은 옷
    H("camp", 0.25, 1.7, -90, "bent", only={14, 15})
    F("camp", -0.5, 2.15, -90, "bent", only={14, 15})
    # 해질녘 벤치 L17~L20
    H("dusk", 0.55, 3.5, -90, "sit", only={17, 18, 19, 20},
      over={19: dict(y=2.7, pose="talk"), 20: _d19(1.0, 0.9, 0.55, 2.7)})
    F("dusk", -0.45, 3.5, -90, "sit", only={17, 18, 19, 20},
      over={19: dict(y=2.7, pose="stand"), 20: _d19(0.8, 1.0, -0.45, 2.7)})
    return C


# ───────────────────────── 소품·효과 ─────────────────────────
GAUGE = (1.3, 2.3)                       # 압력계 중심 (교실 벽, x·z)
SEG = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg",
       9: "abcdfg"}
_rw = np.random.default_rng(2310)
RW = _rw.uniform(-1, 1, (120, 6))        # 물방울마다 다른 무작위 값
MOTES = _rw.uniform(0, 1, (26, 6))       # 해질녘 반짝이는 먼지(공기 알갱이)


def digits(value, cx, cz, y, w=0.14, h=0.34, t=0.035, gap=0.22):
    """두 자리 7-세그먼트 숫자 → 발광 상자 목록."""
    out = []
    for k, ch in enumerate(f"{value:02d}"):
        x0 = cx + (k - 0.5) * gap
        seg = {"a": (x0, cz + h / 2 - t / 2, w, t), "d": (x0, cz - h / 2 + t / 2, w, t), "g": (x0, cz, w, t),
               "b": (x0 + w / 2 - t / 2, cz + h / 4, t, h / 2), "c": (x0 + w / 2 - t / 2, cz - h / 4, t, h / 2),
               "f": (x0 - w / 2 + t / 2, cz + h / 4, t, h / 2), "e": (x0 - w / 2 + t / 2, cz - h / 4, t, h / 2)}
        for s in SEG[int(ch)]:
            px, pz, sx, sz = seg[s]
            out.append(((px, y, pz), (sx, 0.012, sz), (0, 0, 0), (0.35, 1.0, 0.5)))
    return out


def gauge_value(i, tl, du):
    if i < 12:
        return 1.0
    if i > 12:
        return 0.5
    return lerp(1.0, 0.5, ramp(tl, 0.15 * du, 0.75 * du))


def puffs(d, tl, k0=0.0, n=3, life=0.9, size=0.075):
    """허리 숙인 사람 입에서 나오는 하얀 입김 상자."""
    out = []
    mx, my, mz = mouth_pt(d)
    a = math.radians(d["yaw"])
    for s in range(n):
        age = (tl + k0 + s * life / n) % life
        f = age / life
        fwd = 0.04 + 0.5 * age
        sz = size * (1.0 - 0.6 * f) * d["scale"]
        out.append(((mx + math.cos(a) * fwd, my + math.sin(a) * fwd, mz - 0.05 + 0.32 * age), (sz, sz, sz),
                    (0.4 * s, 0.3 * s, 0.5 * s), PUFF))
    return out


def props(i, tl, du, chars):
    """줄 i, 줄 시작 후 tl초의 소품. [(위치, 크기, 회전, 색)] 상자 · 발광 상자 · 공[(위치, 지름, 색)]  (세트 좌표)."""
    B, Gl, Ba = [], [], []
    who = {d["tag"]: d for d in chars if d["show"] and d["tag"] in ("hero", "friend")}
    if i in (1, 2, 3):                                                   # 침대 이불
        if i == 1:                                                       # 걷어찬 이불이 발치 쪽으로 둥실 떠올랐다 내려앉음
            t0, v0, vy = 0.5, 2.4, -0.5
            y, z, rx, c = 1.15, 0.46 + 0.22, 0.0, (0.35, 0.5, 0.82)
            tau, T = tl - t0, 2 * v0 / G
            if 0 < tau < T:
                y += vy * tau * (1 - tau / T)
                z += v0 * tau - 0.5 * G * tau * tau
                rx = -0.4 * math.sin(math.pi * tau / T)
            B.append(((-2.8, y, z), (1.32, 1.25, 0.44), (rx, 0, 0), c))
        else:
            B.append(((-2.8, 1.5, 0.46 + 0.07), (1.3, 1.9, 0.14), (0, 0, 0), (0.35, 0.5, 0.82)))
    if i == 0:                                                           # 훅: 손 위에서 통통 튀는 공
        P = 2.0
        z = 3.9 - 0.5 * G * (((tl + 0.9) % P) - P / 2) ** 2
        Ba.append(((0.7, 1.1, z), 0.24, BALL))
    if i == 5:                                                           # 체중계 숫자
        Gl += digits(scale_value(tl, du), -3.4, 1.37, 1.57)
    if i == 6:                                                           # 점프 높이 눈금: 옛 높이(회색)·지금(노랑)
        B.append(((0.8, 1.6, 1.25), (0.5, 0.04, 2.5), (0, 0, 0), (0.96, 0.96, 0.94)))
        for k in range(1, 13):
            B.append(((0.72 if k % 5 else 0.68, 1.575, 0.1 * k), (0.2 if k % 5 else 0.3, 0.012, 0.02),
                      (0, 0, 0), (0.15, 0.15, 0.18) if k % 5 else (0.85, 0.2, 0.2)))
        Gl.append(((0.15, 1.5, 0.45), (2.0, 0.03, 0.04), (0, 0, 0), (0.85, 0.85, 0.9)))
        Gl.append(((0.15, 1.5, 0.92), (2.0, 0.03, 0.04), (0, 0, 0), (1.0, 0.82, 0.15)))
    if i == 7:                                                           # 덩크 공
        T = hang(DUNK_H)
        t_slam = DUNK_TO + T / 2
        if tl < t_slam:
            d = who["hero"]
            a = math.radians(d["yaw"])
            fx, fy, fz = DUNK_HAND if d["pose"] == "dunk" else (0.35, -0.25, 1.05)
            Ba.append(((d["x"] + math.cos(a) * fx - math.sin(a) * fy, d["y"] + math.sin(a) * fx + math.cos(a) * fy,
                        d["z"] + fz), 0.24, BALL))
        else:
            Ba.append(((RIM[0], RIM[1], bounce_z(DUNK_HAND[2] + DUNK_H, 1.5, tl - t_slam)), 0.24, BALL))
    if i == 8:                                                           # 친구가 높이 띄운 공: 체공 1.9초, 두 손으로 받음
        t_catch = (TOSS_V + math.sqrt(TOSS_V ** 2 - 2 * G * (CATCH[2] - TOSS_Z))) / G
        tau = tl - TOSS_T0
        if tau < 0:
            p = (TOSS_X, TOSS_Y - 0.25, TOSS_Z)
        elif tau < t_catch:
            k = tau / t_catch
            p = (lerp(TOSS_X, CATCH[0], k), lerp(TOSS_Y, CATCH[1], k), TOSS_Z + TOSS_V * tau - 0.5 * G * tau * tau)
        else:
            p = CATCH
        Ba.append((p, 0.24, BALL))
    if i == 9:                                                           # 컵·물
        pos, rx, st = cup_path(tl)
        B.append((pos, (0.13, 0.13, CUP_H), (rx, 0, 0), (0.75, 0.88, 1.0)))
        t_leave = T_BUMP + (CUP_Y0 - EDGE_Y) / V_SLIDE
        T_fall = math.sqrt(2 * (TABLE_TOP + CUP_H / 2 - 0.06) / G)
        for j in range(40):                                              # 떨어지는 동안 쏟아지는 물
            ts = t_leave + 0.02 + j * 0.0125
            if tl < ts:
                continue
            tau = ts - t_leave
            p0 = (CUP_X + 0.04 * RW[j, 0], EDGE_Y - V_SLIDE * tau - 0.04, TABLE_TOP + 0.065 - 0.5 * G * tau * tau)
            v0 = (0.3 * RW[j, 1], -V_SLIDE - 0.25 - 0.2 * abs(RW[j, 2]), -G * tau + 0.2 * RW[j, 3])
            p, on_floor = ballistic(p0, v0, tl - ts)
            B.append((p, (0.06, 0.06, 0.012) if on_floor else (0.06, 0.06, 0.06), (RW[j, 4], RW[j, 5], 0), WATER))
        t_hit = t_leave + T_fall
        if tl > t_hit:                                                   # 바닥에 부딪혀 튀는 물
            pc = (CUP_X, EDGE_Y - V_SLIDE * T_fall, 0.06)
            for j in range(40, 66):
                v0 = (0.6 * RW[j, 0], 0.6 * RW[j, 1], 0.8 + 1.8 * abs(RW[j, 2]))
                p, on_floor = ballistic(pc, v0, tl - t_hit)
                B.append((p, (0.09, 0.09, 0.012) if on_floor else (0.065, 0.065, 0.065), (RW[j, 4], RW[j, 5], 0), WATER))
    if i in (9, 11, 12, 13):                                             # 교실 압력계 바늘
        th = math.radians(-120 + 240 * gauge_value(i, tl, du) / 1.2)
        L = 0.27
        B.append(((GAUGE[0] + 0.5 * L * math.sin(th), 2.895, GAUGE[1] + 0.5 * L * math.cos(th)), (0.03, 0.025, L),
                  (0, th, 0), (0.1, 0.1, 0.12)))
    if i in (11, 12):                                                    # 공기 기둥: 위에 쌓인 공기의 무게 → 반으로
        n = int(16 * ramp(tl, 0.1, 1.0) + 0.5) if i == 11 else int(round(lerp(16, 8, ramp(tl, 0.15 * du, 0.75 * du))))
        for k in range(n):
            B.append(((1.9, 1.62, 1.8 + 0.13 * k), (0.11, 0.11, 0.11), (0, 0, 0.3 * k), AIR))
    if i == 13:                                                          # 빵빵해지는 과자 봉지
        s = bag_swell(tl, du)
        w, t, h = 0.20 + 0.07 * s, 0.05 + 0.11 * s, 0.28 + 0.05 * s
        wob = 0.04 * s * math.sin(tl * 9)
        B.append(((1.55, 1.0, TABLE_TOP + h / 2), (w, t, h), (0, 0, wob), (0.95, 0.35, 0.2)))
        B.append(((1.55, 1.0 - t / 2 - 0.004, TABLE_TOP + h * 0.55), (w * 0.8, 0.008, 0.09), (0, 0, wob), (0.98, 0.85, 0.25)))
    if i in (14, 15, 16):                                                # 숨찬 입김
        for k, d in enumerate(c for c in chars if c["show"] and c["pose"] == "bent"):
            B += puffs(d, tl, 0.31 * k)
    if i in (17, 18):                                                    # 해질녘 반짝이는 공기 알갱이
        for m in MOTES:
            x = -1.7 + 3.4 * m[0] + 0.12 * math.sin(0.8 * tl + 6.3 * m[3])
            y = 2.4 + 1.8 * m[1] + 0.1 * math.sin(0.6 * tl + 6.3 * m[4])
            z = 0.4 + 2.3 * ((m[2] - 0.05 * tl) % 1.0)
            Gl.append(((x, y, z), (0.035, 0.035, 0.035), (m[5] * 3, m[3] * 3, 0), (1.0, 0.88, 0.55)))
    return B, Gl, Ba


# ───────────────────────── 한 프레임 ─────────────────────────
def frame(t):
    """시각 t의 카메라·캐릭터·소품 (Blender 없이 계산). 캐릭터·소품 좌표는 세트 기준, 카메라 목표점만 월드."""
    i = line_at(t)
    a, b = shot_span(i)
    du = max(b - a, 1e-3)
    tl = max(t - a, 0.0)
    u = min(tl / du, 1.0)
    st, tg, az, el, dist, lens, push, daz = LINES[i]["shot"]
    o = OFF[st]
    dr = DRIFT.get(i, (0.0, 0.0, 0.0))
    cam = ((tg[0] + dr[0] * u + o[0], tg[1] + dr[1] * u + o[1], tg[2] + dr[2] * u), az + daz * u, el,
           dist * (1 + (push - 1) * u), lens)
    chars = []
    for c in cast():
        d = dict(c)
        ov = c["over"].get(i)
        if callable(ov):
            ov = ov(tl, du, u)
        d.update(ov or {})
        d["show"] = c["only"] is None or i in c["only"]
        chars.append(d)
    B, Gl, Ba = props(i, tl, du, chars)
    return dict(i=i, tl=tl, du=du, u=u, set=st, cam=cam, chars=chars, fx=B, glow=Gl, balls=Ba, env=env(i))


def build(ctx):
    from engine import bkit as K
    from engine import voxel as X
    v = X.Vox(23)
    for name, fn in (("room", _room), ("stairs", _stairs), ("class", _class), ("camp", _camp)):
        v.at(*OFF[name])
        fn(v)
    for name, dusk in (("yard", False), ("dusk", True)):
        v.at(*OFF[name])
        _yard(v, dusk)
    v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep23_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    mats = X.people_mats()
    protos = X.people_protos(ctx, mats) + _extra_protos(ctx, mats)
    C = cast()
    people = K.instancer_multi(ctx, "ep23_people", protos, len(C))
    cube = lambda: K.bm_cube(1, 1, 1)
    fx = K.instancer(ctx, "ep23_fx", K.proto(ctx, "ep23_p_fx", cube(), [K.mat_inst("ep23_m_fx", 0.7)]), N_FX,
                     vector_scale=True)
    gl = K.instancer(ctx, "ep23_glow", K.proto(ctx, "ep23_p_glow", cube(), [_mat_glow("ep23_m_glow", 4.0)]), N_GLOW,
                     vector_scale=True)
    ball = K.instancer(ctx, "ep23_ball", K.proto(ctx, "ep23_p_ball", K.bm_sphere(0.5, (0, 0, 0), 10, 6),
                                                 [K.mat_inst("ep23_m_ball", 0.5)]), N_BALL)

    def boxes(ob, items, cap, off):
        P, S, R, Cc = (np.zeros((cap, 3), np.float32) for _ in range(4))
        for k, (p, s, r, c) in enumerate(items[:cap]):
            P[k] = (p[0] + off[0], p[1] + off[1], p[2])
            S[k], R[k], Cc[k] = s, r, c
        K.set_points(ob, P, scale=(S[:, 0] > 0).astype(np.float32), size=S, rot=R, col=Cc)

    def upd(t, f):
        S = frame(t)
        cam.set(*S["cam"])
        e = S["env"]
        sun.data.energy = e["sun"]
        sun.data.color = e["sun_col"]
        sun.rotation_euler = tuple(math.radians(q) for q in e["sun_rot"])
        ctx.set_ctl("ambient", e["amb"])
        ctx.set_rgb("ambient_col", e["amb_col"])
        P, R, CO, C2, SC, PO = [], [], [], [], [], []
        for d in S["chars"]:
            ox, oy = OFF[d["set"]]
            P.append((d["x"] + ox, d["y"] + oy, d["z"]))
            R.append((0, 0, math.radians(d["yaw"])))
            CO.append(d["shirt"])
            C2.append(d["pants"])
            SC.append(d["scale"] if d["show"] else 0.0)
            PO.append(pose_index(d["pose"], d["hair"]))
        K.set_points(people, P, scale=SC, rot=R, col=np.array(CO, np.float32),
                     colors={"col2": np.array(C2, np.float32)}, pose=PO)
        off = OFF[S["set"]]
        boxes(fx, S["fx"], N_FX, off)
        boxes(gl, S["glow"], N_GLOW, off)
        Pb, Sb, Cb = (np.zeros((N_BALL, 3), np.float32) for _ in range(3))
        sc = np.zeros(N_BALL, np.float32)
        for k, (p, dia, c) in enumerate(S["balls"][:N_BALL]):
            Pb[k] = (p[0] + off[0], p[1] + off[1], p[2])
            sc[k], Cb[k] = dia, c
        K.set_points(ball, Pb, scale=sc, col=Cb)

    ctx.on_frame(upd)


def _mat_glow(name, strength=4.0):
    """인스턴스 'col' 색으로 빛나는 재질 (숫자·눈금·반짝임)."""
    from engine import bkit as K
    m, nt, out = K.new_mat(name)
    e = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, K.inst_attr(nt, "col"), e.inputs["Color"])
    e.inputs["Strength"].default_value = strength
    K.ln(nt, e.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m
