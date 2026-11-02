"""EP26 만약에 나이를 거꾸로 먹는다면? (19편식: 블록 캐릭터·생활 장면·내레이션)

모두 80살 얼굴로 태어나 해마다 한 살씩 젊어져 아기 얼굴로 떠난다 (얼굴 나이 = 80 - 실제 나이).
장면마다 짧은 사건 하나 (내레이션 한 줄 = 한 컷):
신생아실 백발 아기들(훅) → 50대 얼굴 엄마가 날 안아 줌 → 백발 1학년 입학식 → 스무 살 첫 출근(60대 얼굴)
→ 정년퇴직하는 부장님은 20대 얼굴 → 서른 살 결혼식(50대 얼굴), 엄마는 나보다 30년 어려 보임 → 해마다 젊어져 뛰는 공원
→ 반전: 작은보호탑해파리는 늙거나 다치면 어린 폴립으로 돌아감 → 엄마는 어린이 → 아기
→ 엄마가 날 안아 키웠듯, 이번엔 내가 엄마를 안아 줌 → 부모님을 마지막으로 안은 게 언제인가요?
근거(설명란): Piraino, Boero, Aeschbach & Schmid 1996, Biological Bulletin 190:302-312.
특수효과: 백발 = 머리카락 재질만 회색인 캐릭터 원형(ep26_), 안는 자세·달리기 = 새 자세 원형,
해파리 = 인스턴스 발광 블록(갓 → 공 → 바위 위 폴립으로 한 칸씩 변형), 색종이·꽃잎 = 떨어지는 작은 상자 인스턴스.
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
OFF = {"nursery": (0, 0), "school": (300, 0), "office": (600, 0), "wedding": (900, 0), "park": (1200, 0),
       "sea": (1500, 0), "home": (1800, 0)}
# say: 내레이션 = 자막 / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화)
LINES = [
    dict(say="만약에 나이를 거꾸로 먹는다면 어떻게 될까요?", gap=0.7, shot=("nursery", (0.0, 1.57, 1.38), -90, 5, 3.0, 28, 0.95, 2)),
    dict(say="아기는 백발 할아버지 얼굴로 태어나요", shot=("nursery", (0.37, 1.57, 1.1), -90, 8, 4.4, 24, 0.95, -3)),
    dict(say="엄마는 50대 얼굴로 날 안아 줬죠", gap=0.5, shot=("nursery", (2.45, -0.05, 1.05), -70, 20, 2.3, 28, 0.92, 4)),
    dict(say="입학식엔 백발 1학년이 줄을 서고", shot=("school", (0.0, 0.0, 1.15), -90, 5, 3.4, 28, 0.93, 3)),
    dict(say="스무 살 첫 출근, 얼굴은 벌써 60대", shot=("office", (-0.28, 0.1, 1.3), -90, 5, 3.4, 28, 0.93, 0)),
    dict(say="정년퇴직하는 부장님은 20대 얼굴", shot=("office", (0.0, 0.1, 1.35), -90, 5, 3.0, 28, 0.93, 0)),
    dict(say="서른 살 결혼식, 신랑 얼굴은 50대", shot=("wedding", (0.31, 2.6, 1.55), -90, 3, 4.2, 28, 0.93, 0)),
    dict(say="엄마는 나보다 30년 어려 보였죠", gap=0.5, shot=("wedding", (-0.31, 2.6, 1.55), -90, 3, 3.6, 28, 0.93, 0)),
    dict(say="해마다 젊어져서 공원을 뛰어다녔어요", gap=0.7, shot=("park", (0.0, 0.5, 1.2), -90, 4, 5.5, 28, 1.0, 0)),
    dict(say="그런데 사실, 거꾸로 사는 생물이 있어요", shot=("sea", (0.0, 1.05, 1.05), -90, 4, 4.0, 26, 0.9, 3)),
    dict(say="작은보호탑해파리는 늙거나 다치면", shot=("sea", (0.0, 1.05, 1.05), -90, 3, 2.3, 30, 0.9, 0)),
    dict(say="아기 시절 모습, 폴립으로 돌아가요", shot=("sea", (0.0, 1.05, 0.8), -90, 3, 2.3, 28, 0.9, 0)),
    dict(say="그래서 불사 해파리라고 불려요", gap=0.7, shot=("sea", (0.0, 1.05, 0.75), -80, 5, 1.7, 30, 1.2, 4)),
    dict(say="엄마는 어린이가 되어 숙제를 했고", shot=("home", (0.43, 1.6, 1.15), -90, 6, 3.4, 28, 0.93, 0)),
    dict(say="어느 날, 엄마는 아기가 되었어요", gap=0.9, shot=("home", (2.0, 1.4, 1.1), -90, 8, 3.0, 28, 0.93, 0)),
    dict(say="엄마가 날 안아 키웠듯", gap=0.7, shot=("nursery", (2.45, -0.05, 1.05), -95, 20, 2.3, 28, 0.92, -4)),
    dict(say="이번엔 내가 엄마를 안아 줍니다", gap=0.9, shot=("home", (-1.72, 1.74, 1.1), -62, 24, 2.3, 28, 0.92, 4)),
    dict(say="부모님을 마지막으로 안은 게 언제인가요?", shot=("home", (-1.72, 1.74, 1.1), -66, 20, 2.6, 26, 1.35, 3)),
]
TITLE = [("만약에", "white"), ("나이를", "white"), ("거꾸로 먹는다면", "white"), ("어떻게 될까요?", "yellow")]
_NAMES = ["title", "newborn", "momhug", "school", "work", "retire", "wedding", "momyoung", "run",
          "tw0", "tw1", "tw2", "tw3", "kidmom", "babymom", "flash", "hug", "ask"]
LN = {n: i for i, n in enumerate(_NAMES)}
assert len(_NAMES) == len(LINES)
TWIST = LN["tw0"]       # '그런데 사실' 줄

_TL = Path(__file__).resolve().parents[1] / "assets" / "voice" / "ep26_agebackward" / "timeline.json"
TIMELINE = json.load(open(_TL, encoding="utf-8")) if _TL.exists() else {
    "dur": 56.0, "lines": [[0.3 + 2.6 * i, 2.6 * i + 2.7, ln["say"]] for i, ln in enumerate(LINES)]}
DUR = float(TIMELINE["dur"])
STARTS = [float(s) for s, _, _ in TIMELINE["lines"]]
META = {"id": "ep26", "title": "만약에 나이를 거꾸로 먹는다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 7},
        "music": {"key": "F", "mode": "major", "bpm": 92, "seed": 261, "twist_at": STARTS[TWIST]}}
BEATS = []
GRADE = {"exposure": 0.9, "bloom": 0.1, "bloom_thr": 1.5, "vignette": 0.16}

# 세트별 빛: (해 세기, 주변광 세기, 주변광 색)
ENV = {"nursery": (3.0, 0.42, (0.62, 0.68, 0.82)), "school": (3.2, 0.45, (0.62, 0.70, 0.86)),
       "office": (3.0, 0.42, (0.62, 0.68, 0.82)), "wedding": (2.8, 0.45, (0.66, 0.68, 0.80)),
       "park": (3.4, 0.48, (0.60, 0.72, 0.90)), "sea": (0.0, 0.55, (0.10, 0.42, 0.80)),
       "home": (0.0, 0.12, (0.35, 0.42, 0.65))}


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
    st = LINES[line_at(t)]["shot"][0]
    if st == "sea":
        return (0.02, 0.10, 0.24), (0.04, 0.20, 0.42), 0.0
    if st == "home":
        return (0.004, 0.006, 0.02), (0.012, 0.016, 0.04), 1.0
    return (0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0


# ───────────────────────── 캐릭터 몸 (자세 · 나이 · 소품) ─────────────────────────
# 자세: (앉음, 오른팔, 왼팔(어깨 앞으로 들기 rad, 음수=앞), 팔을 안쪽으로 모으는 각(도), 다리 벌림 rad, 입, 눈 감음)
POSES = {
    "stand": (0, 0.0, 0.0, 0, 0.0, "c", 0),
    "talk": (0, -0.9, 0.05, 0, 0.0, "o", 0),
    "sit": (1, -0.6, -0.6, 0, 0.0, "c", 0),
    "sitc": (1, -2.3, -2.3, 0, 0.0, "w", 0),            # 앉아서 팔 번쩍 우는 아기
    "cheer": (0, -2.7, -2.7, 0, 0.0, "o", 0),
    "run_a": (0, -1.1, 0.8, 0, 0.62, "o", 0),
    "run_b": (0, 0.8, -1.1, 0, -0.62, "o", 0),
    "hold": (0, -1.25, -1.25, 30, 0.0, "c", 0),         # 두 팔을 앞으로 모아 안음
    "hold_sit": (1, -1.25, -1.25, 30, 0.0, "c", 0),
    "clap": (0, -1.3, -1.3, 36, 0.0, "o", 0),           # 박수
    "lie": (0, 0.0, 0.0, 0, 0.0, "c", 1),               # 누움 (얼굴은 위, 머리는 -x)
}
# 얼굴 나이: (머리카락 색, 주름 단계, 안경, 콧수염)
KINDS = {
    "adult": ((0.11, 0.075, 0.055), 0, 0, 0),
    "mid": ((0.46, 0.45, 0.47), 1, 0, 0),               # 50대 희끗희끗
    "gray": ((0.68, 0.68, 0.71), 2, 1, 1),              # 60대
    "white": ((0.93, 0.93, 0.97), 2, 1, 1),             # 70~80대 백발
    "baby": ((0.11, 0.075, 0.055), 0, 0, 0),            # 아기: 정수리 한 가닥만
}
ACC = [("yellow", (1.0, 0.82, 0.15)), ("red", (0.86, 0.14, 0.17)), ("pink", (1.0, 0.62, 0.75)),
       ("green", (0.30, 0.65, 0.30)), ("sky", (0.55, 0.78, 1.0)), ("brown", (0.45, 0.30, 0.20))]
# 재질 번호: 0 셔츠 1 바지 2 피부 3 머리카락 4 흰자 5 검정 6 입 7 화면 | 8 주름 9 노랑 10 빨강 11 분홍 12 초록 13 하늘 14 갈색


def _rot_z(bm, ang, pivot):
    """pivot=(x, y)를 지나는 세로축 둘레로 회전 (팔을 안쪽으로 모을 때)."""
    c, s = math.cos(ang), math.sin(ang)
    for v in bm.verts:
        x, y = v.co.x - pivot[0], v.co.y - pivot[1]
        v.co.x, v.co.y = pivot[0] + c * x - s * y, pivot[1] + s * x + c * y
    return bm


def _p26(pose, long_hair, kind, style):
    """[(bmesh, 재질번호)] — voxel._person과 같은 몸에 나이(주름·안경·수염)·소품(style, '+'로 이음)을 더함."""
    from engine import bkit as K
    from engine import voxel as X
    sit, ar, al, inn, swing, mouth, shut = POSES[pose]
    tok = set(style.split("+"))
    _, wr, glasses, stache = KINDS[kind]
    baby = kind == "baby"
    swad = "swaddle" in tok

    def box(cx, cy, z0, sx, sy, sz):
        return K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True)
    hip = 0.47 if sit else 0.78
    hz = hip + 0.58
    P = []
    if swad:
        P.append((box(0, 0, -0.02, 0.42, 0.62, hz + 0.04), 0))            # 포대기 (셔츠 색)
        P.append((box(0, 0, 0.5, 0.435, 0.635, 0.1), 4))
        P.append((box(0, 0, 0.1, 0.435, 0.635, 0.06), 4))
    else:
        if sit:
            for sy in (-0.11, 0.11):
                P += [(box(0.2, sy, hip - 0.11, 0.46, 0.2, 0.22), 1), (box(0.36, sy, 0.08, 0.2, 0.2, hip - 0.19), 1),
                      (box(0.39, sy, 0.0, 0.26, 0.2, 0.09), 5)]
        else:
            for sy, sg in ((-0.11, 1), (0.11, -1)):
                leg = box(0, sy, 0.09, 0.22, 0.2, hip - 0.09)
                shoe = box(0.03, sy, 0.0, 0.27, 0.2, 0.09)
                P += [(X._rot_y(leg, sg * swing, (0, 0, hip)), 1), (X._rot_y(shoe, sg * swing, (0, 0, hip)), 5)]
        P.append((box(0, 0, hip, 0.3, 0.52, 0.58), 0))
    P.append((box(0, 0, hz, 0.46, 0.46, 0.46), 2))
    fx = 0.232
    for sy in (-0.1, 0.1):
        if shut:
            P.append((box(fx, sy, hz + 0.17, 0.02, 0.11, 0.025), 5))
        else:
            P.append((box(fx, sy, hz + 0.13, 0.02, 0.11, 0.1), 4))
            P.append((box(fx + 0.006, sy - 0.018 * np.sign(sy), hz + 0.14, 0.02, 0.06, 0.075), 5))
        P.append((box(fx + 0.004, sy, hz + 0.27, 0.02, 0.13, 0.03), 8 if baby else 3))
    mz, mw, mh = {"c": (0.065, 0.12, 0.028), "o": (0.04, 0.13, 0.07), "w": (0.03, 0.17, 0.10)}[mouth]
    P.append((box(fx, 0, hz + mz, 0.02, mw, mh), 6))
    # 머리카락 (아기는 정수리 한 가닥)
    if baby:
        P.append((box(0.02, 0, hz + 0.46, 0.1, 0.1, 0.08), 3))
    else:
        P.append((box(-0.02, 0, hz + 0.37, 0.5, 0.5, 0.13), 3))
        P.append((box(0.215, 0, hz + 0.35, 0.07, 0.5, 0.07), 3))
        if long_hair:
            P.append((box(-0.24, 0, hz - 0.42, 0.1, 0.54, 0.92), 3))
            for sy in (-0.255, 0.255):
                P.append((box(-0.02, sy, hz - 0.2, 0.44, 0.05, 0.7), 3))
        else:
            P.append((box(-0.24, 0, hz + 0.08, 0.08, 0.5, 0.36), 3))
            for sy in (-0.245, 0.245):
                P.append((box(-0.08, sy, hz + 0.22, 0.3, 0.04, 0.22), 3))
    # 나이: 주름 · 안경 · 콧수염
    if wr:
        for sy in (-0.1, 0.1):
            P.append((box(fx + 0.001, sy, hz + 0.112, 0.02, 0.12, 0.012), 8))      # 눈 밑 주름
        P.append((box(fx + 0.001, 0, hz + 0.315, 0.02, 0.30, 0.012), 8))            # 이마 주름
    if wr >= 2:
        for sy in (-0.15, 0.15):
            P.append((box(fx + 0.001, sy, hz + 0.03, 0.02, 0.014, 0.09), 8))        # 팔자 주름
    if glasses:
        for sy in (-0.1, 0.1):
            P.append((box(0.256, sy, hz + 0.232, 0.012, 0.17, 0.014), 5))
            P.append((box(0.256, sy, hz + 0.114, 0.012, 0.17, 0.014), 5))
            for dy in (-0.078, 0.078):
                P.append((box(0.256, sy + dy, hz + 0.114, 0.012, 0.014, 0.132), 5))
        P.append((box(0.256, 0, hz + 0.19, 0.012, 0.04, 0.014), 5))
        for sy in (-0.238, 0.238):
            P.append((box(0.13, sy, hz + 0.2, 0.26, 0.012, 0.014), 5))
    if stache and not long_hair:
        P.append((box(0.247, 0, hz + 0.094, 0.028, 0.18, 0.032), 3))
    # 소품
    if "beard" in tok:
        P.append((box(0.238, 0, hz - 0.11, 0.034, 0.27, 0.165), 3))
    if "paci" in tok:
        P.append((box(0.262, 0, hz + 0.03, 0.016, 0.13, 0.09), 13))
        P.append((box(0.285, 0, hz + 0.045, 0.03, 0.045, 0.06), 13))
    if "kid" in tok:                                                   # 노란 모자 · 책가방 · 어깨끈
        P.append((box(0.0, 0, hz + 0.455, 0.52, 0.52, 0.1), 9))
        P.append((box(0.30, 0, hz + 0.425, 0.14, 0.40, 0.03), 9))
        P.append((box(-0.24, 0, hip + 0.02, 0.2, 0.42, 0.52), 10))
        for sy in (-0.2, 0.2):
            P.append((box(0.02, sy, hip + 0.1, 0.32, 0.05, 0.48), 9))
    if "bride" in tok:                                                 # 면사포 · 머리띠 · 꽃
        P.append((box(-0.28, 0, hz - 0.62, 0.1, 0.56, 1.08), 4))
        P.append((box(0.0, 0, hz + 0.455, 0.54, 0.54, 0.05), 4))
        P.append((box(0.2, 0.2, hz + 0.43, 0.08, 0.08, 0.08), 11))
    if "groom" in tok:                                                 # 나비넥타이 · 가슴 꽃
        P.append((box(0.17, 0, hz - 0.07, 0.05, 0.17, 0.07), 10))
        P.append((box(0.185, 0, hz - 0.065, 0.05, 0.05, 0.05), 10))
        P.append((box(0.16, 0.14, hip + 0.35, 0.04, 0.06, 0.07), 4))
    if "tie" in tok:                                                   # 넥타이 · 사원증
        P.append((box(0.16, 0, hip + 0.12, 0.03, 0.08, 0.44), 10))
        P.append((box(0.17, 0, hip + 0.5, 0.04, 0.07, 0.06), 10))
        P.append((box(0.165, 0.14, hip + 0.25, 0.02, 0.10, 0.14), 4))
        P.append((box(0.158, 0.14, hip + 0.38, 0.012, 0.012, 0.2), 5))
    if "bouquet" in tok:                                               # 두 손 앞 꽃다발 (hold·clap 자세용)
        zb = hip + 0.34
        P.append((box(0.5, 0, zb, 0.2, 0.24, 0.16), 11))
        P.append((box(0.52, 0.06, zb + 0.14, 0.1, 0.1, 0.08), 9))
        P.append((box(0.47, -0.07, zb + 0.14, 0.1, 0.1, 0.08), 10))
        P.append((box(0.46, 0, zb - 0.16, 0.12, 0.12, 0.18), 12))
    # 팔
    if not swad:
        for sy, ang, sg in ((-0.34, ar, 1), (0.34, al, -1)):
            piv = (0, 0, hip + 0.54)
            for bm, m in ((box(0, sy, hip + 0.12, 0.18, 0.16, 0.46), 0), (box(0, sy, hip - 0.02, 0.17, 0.15, 0.14), 2)):
                X._rot_y(bm, ang, piv)
                if inn:
                    _rot_z(bm, sg * math.radians(inn), (0, sy))
                P.append((bm, m))
    if swing:                                                          # 달릴 때 발이 땅에 닿게 몸 전체를 내림
        for bm, _ in P:
            X._shift(bm, dz=-hip * (1 - math.cos(abs(swing))))
    if pose == "lie":                                                  # 선 모습을 뒤로 눕힘: 발끝이 원점, 머리는 -x
        for bm, _ in P:
            X._rot_y(bm, -math.pi / 2, (0, 0, 0))
            X._shift(bm, dz=0.24)
    return P


def _kind_mats(K, base):
    """나이별 재질 목록: 머리카락(3번)만 다르고 나머지는 voxel과 같음 + 주름·색 소품."""
    wr = K.mat_simple("ep26_m_wrinkle", (0.70, 0.48, 0.38), 0.8)
    acc = [K.mat_simple("ep26_m_" + n, c, 0.6) for n, c in ACC]
    out = {}
    for k, (hc, *_r) in KINDS.items():
        hair = base[3] if k in ("adult", "baby") else K.mat_simple("ep26_m_hair_" + k, hc, 0.8)
        out[k] = base[:3] + [hair] + base[4:] + [wr] + acc
    return out


def _all_keys(C):
    """캐릭터가 쓸 수 있는 (자세, 긴머리, 나이, 소품) 조합 전부 — 원형을 미리 만들어 둠."""
    ks = set()
    for c in C:
        for d in [c] + [dict(c, **o) for o in c["over"].values()]:
            poses = {d["pose"]}
            if d["anim"]:
                poses.add(d["anim"][0])
            if d["run"]:
                poses |= {"run_a", "run_b"}
            kinds = {d["kind"]} | ({d["kind2"][1]} if d["kind2"] else set())
            for p in poses:
                for k in kinds:
                    ks.add((p, d["hair"], k, d["style"]))
    return ks


# ───────────────────────── 세트 ─────────────────────────
BX = (-1.11, -0.37, 0.37, 1.11)       # 신생아실 아기 침대 가로 자리
BCY = 1.5                             # 아기 침대 세로 자리
BABY_Z = 0.66 - 0.36 * 0.6            # 앉은 아기(크기 0.6)가 요 위에 앉는 높이
MOMCH = (2.35, 0.2)                   # 신생아실 엄마 의자
SOFA = (-1.9, 2.0)                    # 집 소파
HOME_TABLE = (0.0, 1.0)
CRIB = (2.0, 1.35)


def _bassinet(v, cx, cy, band):
    w = (0.96, 0.96, 0.98)
    for dx in (-0.28, 0.28):
        for dy in (-0.22, 0.22):
            v.box(cx + dx - 0.025, cx + dx + 0.025, cy + dy - 0.025, cy + dy + 0.025, 0.06, 0.38, (0.62, 0.64, 0.68), jit=0.02)
            v.box(cx + dx - 0.04, cx + dx + 0.04, cy + dy - 0.04, cy + dy + 0.04, 0.0, 0.06, (0.1, 0.1, 0.12), jit=0)
    v.box(cx - 0.34, cx + 0.34, cy - 0.30, cy + 0.30, 0.38, 0.62, w, jit=0.02)                 # 몸통
    v.box(cx - 0.345, cx + 0.345, cy - 0.305, cy + 0.305, 0.50, 0.56, band, jit=0.02)           # 띠
    v.box(cx - 0.31, cx + 0.31, cy - 0.27, cy + 0.27, 0.62, 0.66, (1.0, 0.95, 0.72), jit=0.02)  # 요
    v.box(cx - 0.34, cx + 0.34, cy + 0.27, cy + 0.30, 0.62, 0.98, w, jit=0.02)                 # 뒤판
    v.box(cx - 0.34, cx - 0.31, cy - 0.30, cy + 0.27, 0.62, 0.84, w, jit=0.02)                 # 옆판
    v.box(cx + 0.31, cx + 0.34, cy - 0.30, cy + 0.27, 0.62, 0.84, w, jit=0.02)
    v.box(cx - 0.34, cx + 0.34, cy - 0.30, cy - 0.27, 0.62, 0.78, w, jit=0.02)                 # 앞판(낮게)
    v.box(cx - 0.345, cx + 0.345, cy - 0.305, cy - 0.265, 0.76, 0.80, band, jit=0.02)
    v.box(cx - 0.12, cx + 0.12, cy - 0.312, cy - 0.30, 0.64, 0.74, (1, 1, 1), jit=0)            # 이름표
    v.box(cx - 0.09, cx + 0.09, cy - 0.318, cy - 0.312, 0.68, 0.70, band, jit=0)


def _nursery(v):
    from engine import voxel as X
    v.floor(-4, 4, -3, 3, (0.97, 0.92, 0.80), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, 3.0, (0.46, 0.67, 0.90), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, 3.0, (0.95, 0.83, 0.85), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, 3.0, (0.80, 0.92, 0.84), 0.5, face=1)
    v.window(1.9, 3.3, 2.99, 1.0, 2.4, night=False)
    for cx, cz, w in ((-3.0, 2.2, 0.9), (-1.0, 2.55, 0.7), (0.7, 2.3, 0.6)):                     # 구름
        v.box(cx - w / 2, cx + w / 2, 2.94, 2.98, cz, cz + 0.16, (1, 1, 1), jit=0.02)
        v.box(cx - w / 3, cx + w / 3, 2.94, 2.98, cz + 0.16, cz + 0.3, (1, 1, 1), jit=0.02)
    v.box(-2.9, -2.1, 2.95, 2.98, 1.6, 2.4, (1, 1, 1), jit=0)                                     # 병원 십자
    v.box(-2.56, -2.44, 2.94, 2.97, 1.68, 2.32, (0.9, 0.2, 0.2), jit=0)
    v.box(-2.82, -2.18, 2.94, 2.97, 1.94, 2.06, (0.9, 0.2, 0.2), jit=0)
    for cx, band in zip(BX, ((0.98, 0.7, 0.8), (0.6, 0.78, 1.0), (0.6, 0.78, 1.0), (0.98, 0.85, 0.5))):
        _bassinet(v, cx, BCY, band)
    v.box(1.3, 3.4, -0.9, 1.3, 0, 0.015, (0.96, 0.78, 0.82), jit=0.02)                           # 러그
    X.chair(v, MOMCH[0], MOMCH[1], -90, (0.85, 0.7, 0.55))
    v.box(-3.4, -2.7, -1.9, -1.2, 0, 0.5, (0.9, 0.75, 0.55))                                      # 장난감 상자
    v.box(-3.3, -3.0, -1.8, -1.5, 0.5, 0.8, (0.95, 0.3, 0.3))
    v.box(-3.05, -2.8, -1.7, -1.45, 0.5, 0.75, (0.3, 0.55, 0.95))
    v.light(0.0, 0.3, 2.4, 80, (1.0, 0.97, 0.92), 0.6)
    v.light(2.4, -0.2, 2.2, 60, (1.0, 0.95, 0.88), 0.6)


def _sakura(v, x, y, h=3.4):
    v.box(x - 0.15, x + 0.15, y - 0.15, y + 0.15, 0, h * 0.55, (0.38, 0.26, 0.2))
    for dz, r, c in ((0.5, 1.1, (1.0, 0.72, 0.8)), (0.75, 0.9, (1.0, 0.8, 0.86)), (0.95, 0.55, (1.0, 0.86, 0.9))):
        v.box(x - r, x + r, y - r, y + r, h * dz, h * dz + 0.6, c, jit=0.06)


def _school(v):
    rs = v.rs
    v.floor(-7, 7, -4, 6, (0.80, 0.72, 0.56), 0.5, "plain")
    v.floor(-1.5, 1.5, -4, 6, (0.78, 0.55, 0.45), 0.5, "check", z=0.01)
    v.box(-7, 7, 6.0, 8.0, 0, 7.5, (0.92, 0.86, 0.74), jit=0.02)                                  # 학교 건물
    for k in range(2):
        for i in range(7):
            x = -6.0 + i * 2.0
            v.box(x, x + 1.2, 5.97, 6.0, 3.2 + k * 2.0, 4.4 + k * 2.0, (0.58, 0.78, 0.95), jit=0, glow=True)
    v.box(-0.9, 0.9, 5.96, 6.0, 0, 2.4, (0.45, 0.30, 0.2), jit=0.02)                              # 현관
    for sx in (-1, 1):                                                                            # 꽃 아치 기둥 + 풍선
        x = sx * 2.4
        v.box(x - 0.15, x + 0.15, 2.75, 3.05, 0, 2.7, (0.98, 0.78, 0.86), jit=0.06)
        for q in range(5):
            c = [(0.95, 0.3, 0.3), (0.3, 0.6, 0.95), (1.0, 0.85, 0.2), (0.4, 0.8, 0.45), (0.95, 0.5, 0.8)][q]
            v.box(x + sx * 0.35 - 0.12, x + sx * 0.35 + 0.12, 2.8, 3.04, 2.1 + 0.12 * q, 2.34 + 0.12 * q, c, jit=0.03)
    v.box(-2.6, 2.6, 2.75, 3.05, 2.7, 3.1, (1.0, 0.8, 0.88), jit=0.06)                           # 꽃 아치 윗보
    for i in range(14):
        x = -2.5 + 0.38 * i
        v.box(x, x + 0.2, 2.73, 2.8, 3.1, 3.25, [(1, 1, 1), (1.0, 0.7, 0.8)][i % 2], jit=0.03)
    v.box(-1.9, 1.9, 2.72, 2.76, 2.15, 2.6, (1.0, 0.92, 0.45), jit=0)                              # 현수막
    for i in range(5):
        v.box(-1.5 + 0.7 * i, -1.2 + 0.7 * i, 2.7, 2.73, 2.28, 2.48, (0.9, 0.3, 0.35), jit=0)
    v.box(-2.1, 2.1, 0.45, 1.3, 0, 0.3, (0.72, 0.70, 0.66), jit=0.03)                            # 뒷줄 단
    for x, y in ((-3.6, 1.6), (3.6, 1.6), (-5.4, 3.5), (5.4, 3.5), (-3.2, 4.4), (3.2, 4.4)):
        _sakura(v, x, y)
    v.light(0.0, -0.5, 3.2, 90, (1.0, 0.97, 0.92), 0.6)


def _office(v):
    from engine import voxel as X
    v.floor(-4, 4, -3, 3, (0.56, 0.58, 0.62), 0.5, "check")
    v.wall((-4, 3), (4, 3), 0, 3.2, (0.86, 0.87, 0.90), 0.5, face=-1)
    v.wall((-4, -3), (-4, 3), 0, 3.2, (0.82, 0.84, 0.88), 0.5, face=-1)
    v.wall((4, -3), (4, 3), 0, 3.2, (0.82, 0.84, 0.88), 0.5, face=1)
    for x0 in (-3.4, -0.7, 2.0):
        v.window(x0, x0 + 2.0, 2.99, 0.9, 2.7, night=False)
    for x in (-2.2, -0.75, 0.75, 2.2):                                  # 책상 + 옆을 보는 모니터 + 의자
        X.table(v, x, 1.85, 1.3, 0.7, 0.74, (0.92, 0.92, 0.9))
        X.monitor(v, x - 0.5, 1.85, 0.74, 0)
        X.chair(v, x, 2.45, -90, (0.2, 0.22, 0.26))
        v.box(x - 0.15, x + 0.25, 1.65, 1.8, 0.74, 0.76, (0.96, 0.96, 0.96))
    v.box(3.3, 3.8, -2.6, -2.1, 0, 0.5, (0.35, 0.6, 0.45))               # 화분
    v.box(3.25, 3.85, -2.65, -2.05, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    v.box(-3.8, -3.3, -2.6, -2.1, 0, 0.5, (0.35, 0.6, 0.45))
    v.box(-3.85, -3.25, -2.65, -2.05, 0.5, 1.3, (0.25, 0.55, 0.25), jit=0.1)
    for x in (-2.5, 0.5, 3.0):
        v.box(x - 0.6, x + 0.6, -0.1, 0.5, 3.15, 3.2, (0.95, 0.97, 1.0), jit=0, glow=True)
        v.light(x, 0.2, 2.8, 110, (0.95, 0.97, 1.0), 0.6)


def _wedding(v):
    from engine import voxel as X
    rs = v.rs
    v.floor(-5, 5, -4, 4, (0.88, 0.80, 0.66), 0.5, "wood")
    v.wall((-5, 4), (5, 4), 0, 4.2, (0.96, 0.94, 0.90), 0.5, face=-1)
    v.wall((-5, -4), (-5, 4), 0, 4.2, (0.94, 0.92, 0.88), 0.5, face=-1)
    v.wall((5, -4), (5, 4), 0, 4.2, (0.94, 0.92, 0.88), 0.5, face=1)
    v.window(-4.0, -1.8, 3.99, 0.8, 3.6, night=False)
    v.window(1.8, 4.0, 3.99, 0.8, 3.6, night=False)
    v.box(-0.65, 0.65, -4, 2.0, 0, 0.02, (0.72, 0.14, 0.2), jit=0.02)                         # 붉은 카펫
    v.box(-2.8, 2.8, 1.9, 3.9, 0, 0.18, (0.92, 0.9, 0.86))                                    # 단상
    for sx in (-1, 1):                                                                        # 꽃 아치
        x = sx * 1.5
        for q in range(14):
            c = [(1.0, 0.75, 0.82), (1, 1, 1), (0.45, 0.75, 0.5), (1.0, 0.6, 0.7)][q % 4]
            v.box(x - 0.2, x + 0.2, 3.3, 3.7, 0.18 + 0.2 * q, 0.38 + 0.2 * q, c, jit=0.06)
    for q in range(16):
        x = -1.5 + 0.2 * q
        c = [(1.0, 0.75, 0.82), (1, 1, 1), (0.45, 0.75, 0.5), (1.0, 0.6, 0.7)][q % 4]
        v.box(x - 0.2, x + 0.2, 3.3, 3.7, 2.9, 3.3, c, jit=0.06)
    for sx in (-1, 1):                                                                        # 촛대 · 꽃 장식
        v.box(sx * 2.3 - 0.05, sx * 2.3 + 0.05, 2.2, 2.3, 0.18, 1.2, (0.8, 0.8, 0.82))
        v.box(sx * 2.3 - 0.05, sx * 2.3 + 0.05, 2.2, 2.3, 1.2, 1.4, (1.0, 0.9, 0.5), jit=0, glow=True)
    for yy in (-0.5, 0.4, 1.3):                                                               # 하객 의자 (카메라는 가운데 길에)
        for k in range(4):
            for sx in (-1, 1):
                X.chair(v, sx * (1.05 + 0.55 * k), yy, 90, (0.97, 0.97, 0.95))
    for x in (-2.0, 0.0, 2.0):
        v.box(x - 0.6, x + 0.6, 0.0, 0.6, 4.15, 4.2, (1.0, 0.97, 0.9), jit=0, glow=True)
        v.light(x, 0.8, 3.7, 130, (1.0, 0.96, 0.9), 0.6)


def _park(v):
    from engine import voxel as X
    rs = v.rs
    v.floor(-10, 10, -7, 14, (0.40, 0.64, 0.30), 0.5, "check")
    v.floor(-1.1, 1.1, -7, 14, (0.88, 0.78, 0.60), 0.5, "plain", z=0.012)
    for sx in (-1, 1):
        v.box(sx * 1.1 - 0.05, sx * 1.1 + 0.05, -7, 14, 0, 0.06, (0.8, 0.8, 0.78), jit=0.02)
    x = -10.0
    while x < 10:                                                          # 뒤쪽 숲
        w = float(rs.uniform(1.4, 2.4))
        v.box(x, x + w, 14, 16, 0, float(rs.uniform(5.5, 8.5)), (0.16 + float(rs.uniform(0, 0.08)), 0.42 + float(rs.uniform(0, 0.12)), 0.22), jit=0.05)
        x += w
    for y in (-3.0, 2.0, 6.0, 10.0):
        for sx in (-1, 1):
            X.tree(v, sx * 3.6, y, 3.6 + 0.4 * float(rs.random()))
    for y in (0.0, 5.0):                                                   # 벤치
        for sx in (-1, 1):
            x = sx * 1.9
            v.box(x - 0.2, x + 0.2, y - 0.6, y + 0.6, 0.4, 0.46, (0.62, 0.42, 0.25))
            v.box(x + sx * 0.18, x + sx * 0.22, y - 0.6, y + 0.6, 0.46, 0.9, (0.62, 0.42, 0.25))
            for dy in (-0.5, 0.5):
                v.box(x - 0.15, x + 0.15, y + dy - 0.04, y + dy + 0.04, 0, 0.4, (0.25, 0.25, 0.28))
    for y in (-1.0, 4.0, 9.0):
        for sx in (-1, 1):
            X.street_lamp(v, sx * 2.5, y, energy=1.0)
    v.floor(-8.5, -4.8, 2.0, 8.0, (0.30, 0.55, 0.82), 0.5, "plain", z=0.03)                # 연못
    for i in range(30):                                                    # 꽃
        x, y = float(rs.uniform(-9, 9)), float(rs.uniform(-6, 12))
        if abs(x) < 1.6 or (-8.7 < x < -4.6 and 1.8 < y < 8.2):
            continue
        c = [(1.0, 0.5, 0.6), (1.0, 0.85, 0.3), (0.95, 0.95, 0.95), (0.7, 0.5, 0.95)][i % 4]
        v.box(x, x + 0.14, y, y + 0.14, 0, 0.22, c, jit=0.05)


JC = (0.0, 1.05, 1.15)      # 해파리 갓 가운데(세트 기준)
RP = (0.0, 1.05, 0.5)       # 바위 위 폴립 자리


def _sea(v):
    rs = v.rs
    v.floor(-5, 5, -3.5, 3.5, (0.74, 0.66, 0.48), 0.5, "plain")
    nv = 10

    def fn(i, j):
        t = j / (nv - 1)
        return v._jit(tuple(a + (b - a) * t for a, b in zip((0.02, 0.07, 0.17), (0.11, 0.40, 0.66))), 0.04)
    v.tiles((-5, 3.5, 0), (1, 0, 0), (0, 0, 0.6), 10, nv, fn)               # 뒷벽 (위로 갈수록 밝은 파랑)
    v.tiles((-5, -3.5, 0), (0, 0.7, 0), (0, 0, 0.6), 10, nv, fn)
    v.tiles((5, 3.5, 0), (0, -0.7, 0), (0, 0, 0.6), 10, nv, fn)
    rock, rock2 = (0.34, 0.40, 0.46), (0.40, 0.46, 0.52)
    v.box(-0.75, 0.75, 0.55, 1.6, 0, 0.32, rock, jit=0.06)                  # 가운데 바위 (윗면 z=0.5)
    v.box(-0.55, 0.55, 0.65, 1.45, 0.32, 0.5, rock2, jit=0.06)
    for x, y, s in ((-2.1, 0.4, 0.5), (2.0, 1.9, 0.6), (-1.5, 2.4, 0.45), (2.6, -0.6, 0.4)):
        v.box(x - s, x + s, y - s * 0.8, y + s * 0.8, 0, s * 0.9, rock, jit=0.07)
    for k in range(30):                                                      # 미역
        side = 1 if k % 2 else -1
        x, y = side * float(rs.uniform(1.5, 4.4)), float(rs.uniform(-2.0, 3.2))
        if k >= 22:
            x, y = float(rs.uniform(-4, 4)), float(rs.uniform(2.4, 3.3))
        for q in range(int(float(rs.uniform(0.7, 1.9)) / 0.25)):
            ox = 0.08 * math.sin(q * 0.9 + k)
            v.box(x + ox - 0.04, x + ox + 0.04, y - 0.04, y + 0.04, q * 0.25, q * 0.25 + 0.27,
                  (0.12, 0.50 + 0.1 * float(rs.random()), 0.32), jit=0.08)
    for cx, cy, col in ((-2.5, 0.8, (0.95, 0.45, 0.55)), (2.6, 1.2, (0.95, 0.65, 0.30)), (-1.8, 2.2, (0.70, 0.40, 0.80))):
        for q in range(7):
            ox, oy, h = float(rs.uniform(-0.3, 0.3)), float(rs.uniform(-0.3, 0.3)), float(rs.uniform(0.2, 0.6))
            v.box(cx + ox - 0.06, cx + ox + 0.06, cy + oy - 0.06, cy + oy + 0.06, 0, h, col, jit=0.08)
    for i in range(70):                                                      # 거품·플랑크톤
        s = float(rs.uniform(0.02, 0.05))
        x, y, z = float(rs.uniform(-4, 4)), float(rs.uniform(-2.5, 3.2)), float(rs.uniform(0.3, 3.6))
        v.box(x, x + s, y, y + s, z, z + s, (0.55, 0.85, 1.0), jit=0, glow=True)
    v.light(0.0, 0.5, 3.2, 220, (0.45, 0.8, 1.0), 0.8)
    v.light(JC[0], JC[1], JC[2] + 0.1, 45, (0.5, 0.9, 1.0), 0.25, "ep26_jelly_lt")


def _home(v):
    from engine import voxel as X
    v.floor(-3.5, 3.5, -3, 3, (0.70, 0.52, 0.34), 0.5, "wood")
    v.wall((-3.5, 3), (3.5, 3), 0, 2.7, (0.93, 0.88, 0.80), 0.5, face=-1)
    v.wall((-3.5, -3), (-3.5, 3), 0, 2.7, (0.86, 0.86, 0.78), 0.5, face=-1)
    v.wall((3.5, -3), (3.5, 3), 0, 2.7, (0.86, 0.86, 0.78), 0.5, face=1)
    v.window(0.9, 2.1, 2.99, 1.0, 2.3, night=True, lights=14)
    tx, ty = HOME_TABLE                                                       # 식탁 + 공책 + 컵
    X.table(v, tx, ty, 1.6, 0.9, 0.74, (0.85, 0.72, 0.52))
    X.chair(v, tx, ty + 0.75, -90)
    v.box(tx - 0.22, tx + 0.22, ty - 0.2, ty + 0.12, 0.74, 0.76, (0.35, 0.55, 0.85))
    v.box(tx - 0.12, tx + 0.12, ty - 0.12, ty + 0.04, 0.76, 0.765, (0.97, 0.97, 0.95), jit=0)
    v.box(tx + 0.45, tx + 0.57, ty - 0.1, ty + 0.02, 0.74, 0.86, (0.95, 0.6, 0.2))
    v.box(tx - 0.04, tx + 0.04, ty - 0.04, ty + 0.04, 1.9, 2.7, (0.2, 0.2, 0.2), jit=0)       # 펜던트 등
    v.box(tx - 0.22, tx + 0.22, ty - 0.22, ty + 0.22, 1.82, 1.9, (1.0, 0.85, 0.6), jit=0, glow=True)
    v.light(tx, ty, 1.7, 120, (1.0, 0.78, 0.5), 0.3)
    sx, sy = SOFA                                                              # 소파 (앉는 높이 0.45)
    v.box(sx - 0.9, sx + 0.9, sy - 0.5, sy + 0.3, 0, 0.40, (0.75, 0.38, 0.35))
    v.box(sx - 0.9, sx + 0.9, sy - 0.5, sy + 0.3, 0.40, 0.45, (0.82, 0.45, 0.40), jit=0.02)
    v.box(sx - 0.9, sx + 0.9, sy + 0.1, sy + 0.35, 0.45, 1.0, (0.75, 0.38, 0.35))
    for dx in (-1, 1):
        v.box(min(sx + dx * 0.9, sx + dx * 1.05), max(sx + dx * 0.9, sx + dx * 1.05), sy - 0.5, sy + 0.35, 0, 0.7,
              (0.70, 0.34, 0.32))
    lx = sx - 1.3                                                              # 플로어 램프 (소파 왼쪽)
    v.box(lx - 0.04, lx + 0.04, 2.3, 2.38, 0, 1.5, (0.2, 0.2, 0.2), jit=0)
    v.box(lx - 0.25, lx + 0.25, 2.1, 2.6, 1.5, 1.85, (1.0, 0.82, 0.55), jit=0, glow=True)
    v.light(lx, 2.35, 1.6, 90, (1.0, 0.8, 0.55), 0.3)
    for k, c in enumerate(((0.8, 0.6, 0.4), (0.4, 0.55, 0.75), (0.85, 0.75, 0.4))):          # 벽 액자
        v.box(sx - 0.9 + 0.7 * k, sx - 0.45 + 0.7 * k, 2.96, 2.98, 1.5, 2.0, (0.35, 0.25, 0.18), jit=0)
        v.box(sx - 0.86 + 0.7 * k, sx - 0.49 + 0.7 * k, 2.95, 2.97, 1.54, 1.96, c, jit=0.04)
    cx, cy = CRIB                                                              # 아기 침대 (앞은 열려 있음)
    v.box(cx - 0.55, cx + 0.55, cy - 0.35, cy + 0.35, 0.3, 0.5, (0.78, 0.58, 0.38))
    for dx in (-0.5, 0.5):
        for dy in (-0.3, 0.3):
            v.box(cx + dx - 0.04, cx + dx + 0.04, cy + dy - 0.04, cy + dy + 0.04, 0, 0.3, (0.62, 0.42, 0.25))
    v.box(cx - 0.52, cx + 0.52, cy - 0.32, cy + 0.32, 0.5, 0.54, (1.0, 0.95, 0.85), jit=0.02)    # 요
    for dx in (-1, 1):
        x = cx + dx * 0.54
        v.box(x - 0.03, x + 0.03, cy - 0.35, cy + 0.35, 0.5, 1.05, (0.72, 0.52, 0.34))
        for q in range(7):
            y = cy - 0.3 + 0.1 * q
            v.box(x - 0.02, x + 0.02, y - 0.015, y + 0.015, 0.54, 1.0, (0.85, 0.7, 0.5), jit=0.02)
    for dy in (-1, 1):
        v.box(cx - 0.55, cx + 0.55, cy + dy * 0.35 - 0.02, cy + dy * 0.35 + 0.02, 0.5, 0.64, (0.78, 0.58, 0.38))
    v.box(cx - 0.35, cx + 0.35, 2.94, 2.98, 1.5, 1.7, (1.0, 0.85, 0.5), jit=0, glow=True)      # 야간등
    v.light(cx, 2.7, 1.4, 40, (1.0, 0.8, 0.55), 0.3)
    v.light(1.8, 2.5, 2.0, 15, (0.55, 0.65, 1.0), 0.6)


# ───────────────────────── 해파리 (발광 블록) ─────────────────────────
BELL, RIM, TENT, CORE = (0.30, 0.65, 1.0), (0.75, 0.95, 1.0), (0.70, 0.90, 1.0), (1.0, 0.18, 0.12)
PEACH, STALK, HEAD, CROWN = (1.0, 0.72, 0.55), (1.0, 0.55, 0.62), (1.0, 0.30, 0.40), (1.0, 0.85, 0.90)
_JELLY = {}


def _jelly_layout():
    """칸 하나하나의 네 모습(갓 → 공 → 바위 위 공 → 폴립)을 미리 정해 둔다. 위치는 중심 기준(m)."""
    if _JELLY:
        return _JELLY
    rs = np.random.default_rng(261)
    c, R = 0.05, 0.34
    P, S, Cl, T, TA, TQ = [], [], [], [], [], []

    def add(p, s, col, typ, ang=0.0, q=0):
        P.append(p), S.append(s), Cl.append(col), T.append(typ), TA.append(ang), TQ.append(q)
    n = int(R / c) + 2
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(0, n + 1):
                p = np.array((i, j, k), float) * c
                r = float(np.linalg.norm(p))
                if k == 0 and R - 1.2 * c < r <= R + 0.6 * c:
                    add(p, (c, c, c), RIM, 1)
                elif k > 0 and R - 1.4 * c < r <= R and (i + j + k) % 2 == 0:
                    add(p, (c, c, c), BELL, 0)
    for m in range(24):                                                         # 촉수
        a = 2 * math.pi * m / 24
        for q in range(9):
            add(np.array((R * 0.95 * math.cos(a), R * 0.95 * math.sin(a), -0.04 - 0.05 * q)), (0.022, 0.022, 0.05), TENT, 2, a, q)
    for z in (0.08, 0.13, 0.18, 0.23):                                          # 빨간 위장 (십자)
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            if z > 0.15 and (dx or dy):
                continue
            add(np.array((dx * c * 0.9, dy * c * 0.9, z)), (c * 0.9, c * 0.9, 0.05), CORE, 3)
    N = len(P)
    P0, S0, C0 = np.array(P, float), np.array(S, float), np.array(Cl, float)
    P1 = P0 * 0.28 + rs.normal(0, 0.006, (N, 3))                                # 공: 갓·촉수가 가운데로 오그라듦
    S1 = S0 * 0.5
    # 폴립 자리 (바위 위 기준): 가지 셋 + 기는줄기
    slots, ssz, scol = [], [], []
    for hx, hy, h in ((-0.2, 0.0, 0.34), (0.02, 0.06, 0.46), (0.22, -0.04, 0.30)):
        for q in range(6):
            slots.append((hx + 0.03 * math.sin(q * 0.8), hy, q * h / 6 + h / 12)), ssz.append((0.045, 0.045, h / 6)), scol.append(STALK)
        slots.append((hx, hy, h + 0.04)), ssz.append((0.085, 0.085, 0.075)), scol.append(HEAD)
        for q in range(8):
            a = 2 * math.pi * q / 8
            slots.append((hx + 0.075 * math.cos(a), hy + 0.075 * math.sin(a), h + 0.075)), ssz.append((0.022, 0.022, 0.09)), scol.append(CROWN)
    for q in range(8):
        slots.append((-0.2 + 0.06 * q, -0.02 * q / 8, 0.0125)), ssz.append((0.06, 0.04, 0.025)), scol.append(STALK)
    perm = rs.permutation(N)[:len(slots)]
    P3, S3, C3 = np.zeros((N, 3)), np.zeros((N, 3)), np.tile(np.array(PEACH), (N, 1))
    P3[:] = (0.0, 0.0, 0.02)
    P3[perm], S3[perm], C3[perm] = np.array(slots), np.array(ssz), np.array(scol)
    _JELLY.update(n=N, P0=P0, S0=S0, C0=C0, T=np.array(T), TA=np.array(TA), TQ=np.array(TQ, float), P1=P1, S1=S1,
                  P3=P3, S3=S3, C3=C3)
    return _JELLY


def morph_span():
    """해파리가 변하기 시작·끝나는 시각: '다치면'을 말할 때 시작 → 폴립 줄 앞쪽 40%에 완성."""
    a0, b0 = shot_span(LN["tw1"])
    a1, b1 = shot_span(LN["tw2"])
    return a0 + 0.55 * (b0 - a0), a1 + 0.40 * (b1 - a1)


def jelly_state(t, m):
    """(위치 N×3 세트 기준, 크기 N×3, 색 N×3, 불빛 중심, 불빛 세기, 불빛 색). m=변신 진행도 0~1."""
    J = _jelly_layout()
    s1, s2, s3 = ramp(m, 0.0, 0.41), ramp(m, 0.41, 0.68), ramp(m, 0.68, 1.0)
    bob = 0.05 * math.sin(2 * math.pi * t / 2.6) * (1 - s2)
    P0 = J["P0"].copy()
    ten = J["T"] == 2
    q = J["TQ"][ten] / 8.0
    P0[ten, 0] += 0.03 * q * np.sin(2.4 * t + J["TA"][ten] * 2 + q * 3.6) * (1 - s1)
    P0[ten, 1] += 0.03 * q * np.cos(2.0 * t + J["TA"][ten] + q * 3.2) * (1 - s1)
    jc, rp = np.array(JC), np.array(RP)
    W0, W1, W2, W3 = jc + P0, jc + J["P1"], rp + J["P1"] * (1, 1, 0.8) + (0, 0, 0.0), rp + J["P3"]
    pos = W0 + (W1 - W0) * s1 + (W2 - W1) * s2 + (W3 - W2) * s3
    pos[:, 2] += bob
    S0, S1 = J["S0"], J["S1"]
    siz = S0 + (S1 - S0) * s1 + (S1 * (1, 1, 0.8) - S1) * s2 + (J["S3"] - S1 * (1, 1, 0.8)) * s3
    C0, C1 = J["C0"], np.tile(np.array(PEACH), (J["n"], 1))
    col = C0 + (C1 - C0) * s1 + (J["C3"] - C1) * s3
    hurt = 0.5 * (1 + math.sin(60 * m)) * (1 - ramp(m, 0.0, 0.16)) if 0 < m < 0.16 else 0.0   # 다친 순간 빨갛게 깜빡
    col = col + (np.array((1.0, 0.1, 0.1)) - col) * hurt
    lc = jc + (rp - jc) * s2 + (0, 0, 0.12 + bob)
    lcol = tuple(float(x) for x in np.array((0.5, 0.9, 1.0)) + (np.array((1.0, 0.65, 0.75)) - np.array((0.5, 0.9, 1.0))) * s1)
    return pos, siz, col, tuple(float(x) for x in lc), float(45.0 - 24.0 * s3), lcol


# ───────────────────────── 캐릭터 배치 ─────────────────────────
BLUE, NAVY = (0.25, 0.45, 0.80), (0.15, 0.18, 0.30)            # 나 (파란 셔츠로 계속 알아봄)
PINK, BROWN = (0.92, 0.55, 0.60), (0.35, 0.28, 0.20)           # 엄마 (분홍 셔츠)
WHITE = (0.97, 0.97, 0.97)


def cast():
    """[dict(set, x, y, z, yaw, pose, kind, hair, shirt, pants, scale, style, over={줄: 덮어쓰기}, only=보이는 줄 집합 or None,
    anim=(바뀌는 자세, 주기초) or None, run=(x0, y0, x1, y1) or None, kind2=(줄 진행도, 바뀐 나이) or None)]"""
    rs = np.random.default_rng(26)
    C = []

    def add(st, x, y, yaw, pose, kind="adult", hair=0, shirt=BLUE, pants=NAVY, scale=1.0, z=0.0, style="",
            over=None, only=None, anim=None, run=None, kind2=None):
        C.append(dict(set=st, x=x, y=y, z=z, yaw=yaw, pose=pose, kind=kind, hair=hair, shirt=shirt, pants=pants,
                      scale=scale, style=style, over=over or {}, only=only, anim=anim, run=run, kind2=kind2))
    pastel = [(0.98, 0.68, 0.78), (0.97, 0.85, 0.45), (0.45, 0.75, 0.45), (0.6, 0.78, 1.0), (0.95, 0.6, 0.35),
              (0.75, 0.6, 0.9), (0.95, 0.95, 0.9)]
    # 신생아실: 백발 아기들 (왼쪽 할머니는 울고, 나는 쪽쪽이)
    f = {LN["title"], LN["newborn"]}
    add("nursery", BX[1], BCY + 0.07, -90, "sit", "white", 1, (0.98, 0.68, 0.78), (0.98, 0.68, 0.78), 0.6, BABY_Z,
        anim=("sitc", 0.5), only=f)
    add("nursery", BX[2], BCY + 0.07, -90, "sit", "white", 0, BLUE, BLUE, 0.6, BABY_Z, style="paci", only=f)
    add("nursery", BX[3], BCY + 0.07, -90, "sit", "white", 0, (0.45, 0.75, 0.45), (0.45, 0.75, 0.45), 0.6, BABY_Z,
        style="beard", anim=("sitc", 0.7), only=f)
    add("nursery", BX[0], BCY + 0.07, -90, "sit", "white", 1, (0.97, 0.85, 0.45), (0.97, 0.85, 0.45), 0.6, BABY_Z,
        style="paci", only=f)
    # 엄마(50대 얼굴)가 포대기 아기(나)를 안음 — 마지막 '엄마가 날 안아 키웠듯'에서 다시
    g = {LN["momhug"], LN["flash"]}
    add("nursery", MOMCH[0], MOMCH[1], -90, "hold_sit", "mid", 1, PINK, BROWN, only=g)
    add("nursery", 1.87, -0.2, -180, "lie", "white", 0, BLUE, BLUE, 0.5, 0.90, style="swaddle+paci", only=g)
    # 입학식: 백발 1학년 (노란 모자·책가방), 가운데 앞줄이 나
    h = {LN["school"]}
    add("school", 0.0, 0.0, -90, "stand", "white", 0, BLUE, NAVY, 0.78, style="kid", only=h)
    for k, x in enumerate((-1.1, -0.55, 0.55, 1.1)):
        add("school", x, 0.0, -90, "cheer" if k == 1 else "stand", "white" if k % 2 == 0 else "gray", k % 2,
            pastel[k], pastel[(k + 3) % 7], 0.78, style="kid", only=h)
    for k, x in enumerate((-1.375, -0.825, -0.275, 0.275, 0.825, 1.375)):
        add("school", x, 0.85, -90, "stand", "white" if k % 3 else "gray", (k + 1) % 2, pastel[(k + 2) % 7],
            pastel[(k + 5) % 7], 0.78, 0.3, style="kid", only=h)
    # 회사: 첫 출근(60대 얼굴 나) · 20대 얼굴 부장님 · 동료
    w, r = {LN["work"]}, {LN["retire"]}
    add("office", 0.05, 0.0, -90, "stand", "gray", 0, BLUE, NAVY, style="tie", only=w)
    add("office", -0.6, 0.12, -80, "talk", "adult", 0, (0.3, 0.3, 0.34), (0.15, 0.15, 0.18), style="tie", only=w)
    add("office", 0.0, 0.0, -90, "hold", "adult", 0, (0.3, 0.3, 0.34), (0.15, 0.15, 0.18), style="tie+bouquet", only=r)
    add("office", -1.5, 0.35, -80, "clap", "mid", 0, BLUE, NAVY, style="tie", only=r)
    for k, (x, y, hr) in enumerate(((-0.95, 0.55, 1), (0.95, 0.55, 0), (1.9, 0.35, 1), (-2.2, 0.6, 0))):
        add("office", x, y, -100 + 8 * k, "clap", "adult", hr, pastel[k], (0.2, 0.2, 0.25), only=r)
    for k, x in enumerate((-2.2, -0.75, 0.75, 2.2)):
        add("office", x, 2.45, -90, "sit", "adult", k % 2, pastel[k + 2], (0.2, 0.2, 0.25))
    # 결혼식: 신랑(나, 50대) · 신부 · 엄마(20대 얼굴)
    wd = {LN["wedding"], LN["momyoung"]}
    add("wedding", 0.0, 2.6, -90, "stand", "mid", 0, BLUE, NAVY, z=0.18, style="groom", only=wd)
    add("wedding", 0.62, 2.6, -90, "hold", "mid", 1, WHITE, WHITE, z=0.18, style="bride+bouquet", only=wd)
    add("wedding", -0.62, 2.6, -90, "clap", "adult", 1, PINK, BROWN, z=0.18, only={LN["momyoung"]})
    for k, (x, y) in enumerate(((-1.05, -0.5), (1.05, -0.5), (-1.6, 0.4), (1.6, 0.4), (-1.05, 1.3), (1.6, 1.3),
                                (-2.15, -0.5), (2.15, 0.4))):
        add("wedding", x, y, 90, "sit", ("adult", "mid", "gray", "adult")[k % 4], k % 2, pastel[k % 7], (0.2, 0.2, 0.25),
            only=wd)
    # 공원: 해마다 젊어지며 달려옴 (달리는 동안 희끗희끗 → 검은 머리)
    add("park", 0.0, 4.5, -90, "run_a", "mid", 0, BLUE, NAVY, run=(0.0, 4.5, 0.0, -1.8), kind2=(0.5, "adult"),
        only={LN["run"]})
    # 집: 어린이가 된 엄마 숙제 / 아기가 된 엄마 / 소파에서 안아 줌
    tx, ty = HOME_TABLE
    add("home", tx, ty + 0.75, -90, "sit", "adult", 1, PINK, BROWN, 0.72, 0.19, only={LN["kidmom"]})
    add("home", 0.85, 1.75, -105, "talk", "adult", 0, BLUE, NAVY, only={LN["kidmom"]})
    add("home", CRIB[0], CRIB[1], -90, "sit", "baby", 0, PINK, PINK, 0.5, 0.5 - 0.36 * 0.5 + 0.04, style="paci",
        only={LN["babymom"]})
    add("home", CRIB[0], CRIB[1] + 0.75, -90, "hold", "adult", 0, BLUE, NAVY, only={LN["babymom"]})
    q = {LN["hug"], LN["ask"]}
    sx, sy = SOFA
    add("home", sx, sy - 0.05, -90, "hold_sit", "adult", 0, BLUE, NAVY, only=q)
    add("home", sx - 0.48, sy - 0.45, -180, "lie", "baby", 0, PINK, PINK, 0.5, 0.90, style="swaddle+paci", only=q)
    return C


# ───────────────────────── 떨어지는 색종이·꽃잎 ─────────────────────────
FALL_N = 90
FALL = {LN["school"]: ("petal", [(1.0, 0.72, 0.8), (1.0, 0.86, 0.9), (1, 1, 1)]),
        LN["retire"]: ("paper", [(0.95, 0.3, 0.3), (0.3, 0.6, 0.95), (1.0, 0.85, 0.2), (0.4, 0.8, 0.45), (0.95, 0.5, 0.8)]),
        LN["wedding"]: ("petal", [(1.0, 0.75, 0.82), (1, 1, 1)]), LN["momyoung"]: ("petal", [(1.0, 0.75, 0.82), (1, 1, 1)])}


def fall_pieces(i, t, tg):
    """줄 i에서 목표점 tg 둘레로 떨어지는 조각들: (위치, 크기, 회전, 색) 또는 None."""
    if i not in FALL:
        return None
    kind, cols = FALL[i]
    rs = np.random.default_rng(1000 + i)
    n = FALL_N
    dx, dy = rs.uniform(-1.5, 1.5, n), rs.uniform(-1.0, 1.0, n)
    ph, sp = rs.uniform(0, 1, n), rs.uniform(0.35, 0.7, n)
    H = 3.0
    z = tg[2] + H * 0.6 - H * ((ph + sp * t) % 1.0)
    sway = 0.12 * np.sin(2.0 * t + ph * 6.28)
    pos = np.stack([tg[0] + dx + sway, tg[1] + dy, z], 1)
    sz = np.tile((0.06, 0.04, 0.006) if kind == "paper" else (0.05, 0.035, 0.005), (n, 1))
    rot = np.stack([ph * 6.28 + 3 * t * sp, ph * 3.1 + 2 * t, ph * 5 + 1.5 * t], 1)
    col = np.array([cols[k % len(cols)] for k in range(n)], np.float32)
    return pos, sz, rot, col


def _glow_mat(name, strength=2.6):
    """인스턴스 'col' 색으로 빛나는 재질 (engine.home.mat_glow_inst와 같은 방식)."""
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
    from engine import voxel as X
    v = X.Vox(26)
    for name, fn in (("nursery", _nursery), ("school", _school), ("office", _office), ("wedding", _wedding),
                     ("park", _park), ("sea", _sea), ("home", _home)):
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep26_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)
    jl = lights["ep26_jelly_lt"]

    C = cast()
    keys = sorted(_all_keys(C))
    PI = {k: n for n, k in enumerate(keys)}
    mats = _kind_mats(K, X.people_mats())
    protos = [K.proto(ctx, f"ep26_p_{n:02d}", K.join_bms(_p26(*k)), mats[k[2]]) for n, k in enumerate(keys)]
    people = K.instancer_multi(ctx, "ep26_people", protos, len(C))
    J = _jelly_layout()
    jelly = K.instancer(ctx, "ep26_jelly", K.proto(ctx, "ep26_p_jelly", K.bm_cube(1, 1, 1), [_glow_mat("ep26_m_jelly")]),
                        J["n"], vector_scale=True)
    fall = K.instancer(ctx, "ep26_fall", K.proto(ctx, "ep26_p_fall", K.bm_cube(1, 1, 1), [K.mat_inst("ep26_m_fall", 0.6)]),
                       FALL_N, vector_scale=True)
    m0, m1 = morph_span()

    def upd(t, f):
        i = line_at(t)
        a, b = shot_span(i)
        u = (t - a) / max(b - a, 1e-3)
        st, tg, az, el, dist, lens, push, daz = LINES[i]["shot"]
        o = OFF[st]
        cam.set((tg[0] + o[0], tg[1] + o[1], tg[2]), az + daz * u, el, dist * (1 + (push - 1) * u), lens)
        sun_e, amb, amb_c = ENV[st]
        sun.data.energy = sun_e
        ctx.set_ctl("ambient", amb)
        ctx.set_rgb("ambient_col", amb_c)
        # 사람
        P, R, CO, C2, SC, PO = [], [], [], [], [], []
        for c in C:
            d = dict(c)
            d.update(c["over"].get(i, {}))
            show = c["only"] is None or i in c["only"]
            ox, oy = OFF[d["set"]]
            x, y, z, pose, kind = d["x"], d["y"], d["z"], d["pose"], d["kind"]
            if d["anim"] and int(t / d["anim"][1]) % 2:
                pose = d["anim"][0]
            if d["kind2"] and u >= d["kind2"][0]:
                kind = d["kind2"][1]
            if d["run"]:
                x0, y0, x1, y1 = d["run"]
                x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                step = int(t / 0.17) % 2
                pose = "run_a" if step == 0 else "run_b"
                z += 0.07 * abs(math.sin(t * 2 * math.pi / 0.34))
            P.append((x + ox, y + oy, z))
            R.append((0, 0.16 if d["run"] else 0, math.radians(d["yaw"])))
            CO.append(d["shirt"])
            C2.append(d["pants"])
            SC.append(d["scale"] if show else 0.0)
            PO.append(PI[(pose, d["hair"], kind, d["style"])])
        K.set_points(people, P, scale=SC, rot=R, col=np.array(CO, np.float32), colors={"col2": np.array(C2, np.float32)},
                     pose=PO)
        # 해파리 (바다 줄에서만)
        if st == "sea":
            m = float(np.clip((t - m0) / max(m1 - m0, 1e-3), 0.0, 1.0))
            pos, siz, col, lc, le, lcol = jelly_state(t, m)
            K.set_points(jelly, pos + (o[0], o[1], 0), scale=np.ones(J["n"], np.float32), size=siz,
                         rot=np.zeros((J["n"], 3)), col=col.astype(np.float32))
            jl.location = (lc[0] + o[0], lc[1] + o[1], lc[2])
            jl.data.energy = le
            jl.data.color = lcol
        else:
            K.set_points(jelly, np.zeros((J["n"], 3)), scale=np.zeros(J["n"], np.float32))
        # 색종이·꽃잎
        fp = fall_pieces(i, t, (tg[0] + o[0], tg[1] + o[1], tg[2]))
        if fp:
            K.set_points(fall, fp[0], scale=np.ones(FALL_N, np.float32), size=fp[1], rot=fp[2], col=fp[3])
        else:
            K.set_points(fall, np.zeros((FALL_N, 3)), scale=np.zeros(FALL_N, np.float32))

    ctx.on_frame(upd)
