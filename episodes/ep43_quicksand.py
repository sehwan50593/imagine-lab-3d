"""EP43 만약에 퀵샌드에 빠진다면? (기준 영상 형식 STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

11-06 오너: 42~49는 '남자가 한 명뿐이라면' 편 형식으로, 내레이션 없이. 소리는 배경음(-23 LUFS)과 효과음뿐.
장면(3D)은 11-05 픽세판 그대로(서해 갯벌 지후·단면판·저울·밀물·해경 보트·지도판·조석표·둔덕), 줄 순서도 그대로(이미 시간순).
D-DAY(발 한 짝에 중형차 힘) → +10분(밀도 2배라 허리까지만) → +1시간(흔들면 풀리고 멈추면 굳는다 → 천천히 흔들기)
→ +6시간(진짜 위험은 밀물, 해경 보트) → 실제로는(올해 1~4월 갯벌 사고 26건) → 반전(대부분 물때를 몰라서, 구조 592명)
→ 지금(힘으로 못 이긴다, 천천히·물때) → 질문 → 다음 편(80억 명이 한 도시에). 효과음: 묶음 '찰싹', 컷 '휙', 당김 되튕김 '쿵', 밀물 '우르릉', 앱 체크 '띵'.

근거(설명란): ※ '지후가 서해 갯벌 퀵샌드에 빠졌다'는 가정의 상상 시나리오. 사람이 다치는 장면은 없고, 알갱이·저울·지도 모양과 비율은 연출.
· 발을 초당 1cm로 뽑으려면 중형차를 들어 올리는 만큼의 힘(저자 추정, 숫자 없이 표현만) · Khaldoun 외, Nature 437:635(2005), National Geographic 2005-09
· 퀵샌드 밀도 약 2g/㎤, 사람 몸 약 1g/㎤ → 허리까지만 잠김 · National Geographic 2005, Live Science 2010
· 흔들면 액체처럼 풀리고 가만두면 굳음(충격 액화) · Nature 437:635(2005)
· 다리를 천천히 흔들면 틈으로 물이 들어가 느슨해짐 · National Geographic 2005
· 진짜 위험은 밀물(만조) · National Geographic 2005, Nature news 2005-09-28(Bonn 인터뷰)
· 2026년 1월~4월 22일 갯벌 사고 26건·사망 4명 · 해양경찰청 발표 보도(2026-04)
· 갯벌 고립 사고 대부분은 물때를 몰라서 · 인천해양경찰서 보도(2023)
· 2021년~2026년 상반기 해루질 중 고립 사고 구조 592명 · 해경청 자료(국회 의원실 보도)
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"flat": (0, 0), "cross": (300, 0), "shore": (600, 0), "map": (900, 0), "knoll": (1200, 0), "city": (1500, 0)}
NAMES = ("hook", "force", "pull", "dens", "waist", "hour", "liquef", "still", "wiggle", "shoe", "tide", "danger", "boat", "count",
         "twist", "chart", "rescued", "walkout", "look", "app", "dusk", "ask", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}

# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
# ease="out": 처음에 빨리 움직이고 천천히 멈춤(훅)
H_A = ("flat", (0.0, 0.0, 1.25), -90, 2, 3.4, 28, 0.72, 3, 0.10)
LINES = [
    dict(d=3.1, sub="서해 갯벌에서\n퀵샌드에 빠진다면?", ease="out", shot=H_A),
    dict(d=3.4, sub="발을 1초에 1cm 빼는 데도\n중형차를 드는 힘이 듭니다.", shot=("flat", (0.35, 0.0, 1.15), -90, 4, 4.0, 30, 0.88, -4, 0.10)),
    dict(d=2.8, sub="있는 힘껏 당겨 봐도\n발은 꿈쩍하지 않습니다.", shot=("flat", (0.0, 0.0, 1.05), -90, 10, 4.6, 28, 0.9, 6, 0.08)),
    dict(d=2.9, sub="퀵샌드는 사람 몸보다\n약 2배 무겁습니다.", shot=("cross", (0.0, 0.0, 2.1), -90, 3, 9.5, 26, 0.92, 2, 0.04)),
    dict(d=2.8, sub="그래서 사람은\n허리까지만 잠깁니다.", shot=("flat", (0.0, 0.0, 0.62), -90, 6, 4.2, 28, 0.9, 3, 0.08)),
    dict(d=2.7, sub="한 시간째,\n지후는 아직 못 나왔습니다.", shot=("flat", (0.9, 0.0, 0.9), -90, 6, 6.2, 26, 0.92, 3, 0.06)),
    dict(d=3.3, sub="퀵샌드는 흔들면 풀리고\n멈추면 단단히 굳습니다.", shot=("cross", (0.0, 0.0, 2.2), -90, 0, 11.5, 26, 0.96, 2, 0.06)),
    dict(d=2.7, sub="지후는 힘을 빼고\n가만히 숨을 고릅니다.", shot=("flat", (0.0, 0.0, 0.72), -90, 5, 3.8, 30, 0.9, 2, 0.08)),
    dict(d=3.0, sub="다리를 천천히 흔들면\n모래 틈으로 물이 스밉니다.", shot=("cross", (0.0, 0.0, 2.2), -90, 2, 11.5, 26, 0.96, -2, 0.06)),
    dict(d=3.0, sub="한 걸음씩 발이 올라옵니다.\n신발 한 짝은 두고요.", shot=("flat", (0.0, 0.0, 0.95), -90, 6, 6.4, 26, 0.92, 2, 0.05)),
    dict(d=2.9, sub="그런데 여기는 바닷가,\n물이 차오르기 시작합니다.", shot=("shore", (0.0, 0.0, 1.1), -90, 8, 5.0, 28, 0.9, 3, 0.08)),
    dict(d=2.8, sub="모래보다 무서운 건\n밀려오는 밀물입니다.", shot=("shore", (0.0, 0.0, 0.9), -90, 5, 5.3, 28, 0.9, 3, 0.03)),
    dict(d=2.6, sub="해경 보트가\n지후에게 달려옵니다.", shot=("shore", (0.0, 4.5, 1.2), -90, 4, 11.0, 26, 0.92, 0, 0.08)),
    dict(d=3.4, sub="올해 1~4월에만 갯벌 사고 26건,\n4명이 숨졌습니다.", shot=("map", (0.0, 0.0, 0.85), -90, 55, 7.8, 24, 0.95, 2, 0.06)),
    dict(d=2.9, sub="사고 대부분은\n물때를 몰라서 생깁니다.", shot=("map", (0.0, 0.0, 0.85), -90, 48, 7.8, 24, 0.95, -3, 0.06)),
    dict(d=2.9, sub="지후는 조석표부터 펼칩니다.\n거꾸로 들긴 했지만요.", shot=("map", (0.0, -3.4, 1.25), -90, 4, 4.4, 28, 0.9, 3, 0.06)),
    dict(d=3.3, sub="2021년부터 갯벌에서\n구조된 사람만 592명.", shot=("shore", (0.0, 0.0, 0.8), -90, 4, 11.5, 22, 0.94, 6, 0.10)),
    dict(d=3.1, sub="지후는 단단한 땅으로\n걸어 나옵니다.", shot=("knoll", (0.0, -3.5, 1.0), -90, 4, 8.0, 26, 0.92, 5, 0.06)),
    dict(d=2.6, sub="퀵샌드는 힘으로\n이기는 게 아닙니다.", shot=("knoll", (0.15, -1.0, 1.2), 90, 16, 5.0, 26, 0.9, -4, 0.06)),
    dict(d=3.1, sub="답은 천천히,\n그리고 물때 확인.", shot=("knoll", (0.0, 0.0, 1.5), -90, 2, 3.4, 28, 0.9, 3, 0.10)),
    dict(d=2.9, sub="모래는 서두르는 사람만\n붙잡습니다.", shot=("knoll", (0.0, 0.2, 1.0), -90, 4, 5.6, 26, 0.95, 0, 0.06)),
    dict(d=2.6, sub="댓글로 알려 주세요.", shot=("knoll", (0.0, 0.0, 1.45), -90, 2, 4.4, 30, 0.9, 0, 0.10)),
    dict(d=3.6, sub="도시 하나에 인류 전체가\n살 수 있을까요?", shot=("city", (0.0, 0.0, 5.0), -90, 28, 26.0, 26, 0.9, 12, 0.0)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="D-DAY", label="발 한 짝 빼는 데", big="중형차 힘", label_color="blue", big_color="red"),
    dict(at="dens", badge="+10분", title="퀵샌드 밀도는 사람의 {yellow}2배{/}", big="허리까지만", big_color="green"),
    dict(at="hour", badge="+1시간", title="흔들면 풀리고\n{cyan}멈추면 굳는다{/}", title_size=72),
    dict(at="wiggle", badge="+1시간", title="빠져나오는 법", big="천천히 흔들기", big_color="green"),
    dict(at="tide", badge="+6시간", title="진짜 위험은", big="밀물", big_color="red"),
    dict(at="count", badge="실제로는", title="올해 1~4월 갯벌 사고", big="26건", big_color="orange"),
    dict(at="twist", badge="반전", title="사고 대부분은", big="물때를 몰라서", big_color="red"),
    dict(at="rescued", badge="반전", title="2021년부터 구조된 사람", big="592명", big_color="orange"),
    dict(at="walkout", badge="지금", title="퀵샌드는 {cyan}힘으로{/} 못 이긴다"),
    dict(at="ask", badge="지금", title="갯벌에 가면\n{cyan}물때표부터{/} 볼 건가요?", title_size=70),
    dict(at="teaser", badge="다음 편", title="내일 낮 12시\n{cyan}80억 명이 한 도시에 산다면?{/}", title_size=64),
]
TWIST = LN["twist"]  # '대부분은 물때를 몰라서' 줄 — 음악이 바뀌는 곳
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
# 당겼다 되튕기는 순간(spring: period×0.62)마다 작은 '쿵', 밀물 '우르릉', 조석표 앱 체크 '띵'
_SNAPS = [[STARTS[LN["hook"]] + 0.434 + 0.7 * n, "thud", 0.35] for n in range(4)] + \
         [[STARTS[LN["pull"]] + 0.341 + 0.55 * n, "thud", 0.25] for n in range(5)]
META = {"id": "ep43", "title": "만약에 퀵샌드에 빠진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"key": "D", "mode": "lydian", "bpm": 98, "seed": 431, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, _SNAPS + [[STARTS[LN["tide"]] + 0.2, "rumble", 0.5, 2.4],
                                                                [STARTS[LN["app"]] + 0.8, "ding", 1.0]])}}
GRADE = {"exposure": 0.92, "bloom": 0.12, "bloom_thr": 1.4, "vignette": 0.16}


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


# 퀵샌드 당김: 스프링 곡선 — period마다 천천히 올라오다(0~62%) 확 되튕겨 내려감
def spring(tau, period=0.7):
    ph = (tau / period) % 1.0
    return smooth(ph / 0.62) if ph < 0.62 else max(0.0, 1.0 - (ph - 0.62) / 0.12)


def snap_age(tau, period=0.7):
    """가장 최근 되튕김 뒤 경과 초 (되튕김 전이면 99)."""
    n = math.floor((tau - 0.62 * period) / period)
    return tau - (0.62 * period + n * period) if n >= 0 else 99.0


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def _shake_spec(i):
    """줄 i의 흔들림 [(시작 τ, 길이, 이동 세기 m, 각도 세기 도, 진동수 Hz, 종류)]. 'hold' 거의 일정, 'hit' 점점 잦아듦."""
    if i == LN["hook"]:
        return [(0.0, 99.0, 0.035, 0.0, 15.0, "hold")] + [(0.62 * 0.7 + 0.7 * n, 0.5, 0.05, 0.5, 13.0, "hit") for n in range(5)]
    if i == LN["pull"]:
        return [(0.62 * 0.55 + 0.55 * n, 0.45, 0.04, 0.4, 13.0, "hit") for n in range(6)]
    if i == LN["force"]:
        return [(0.0, 99.0, 0.012, 0.0, 17.0, "hold")]
    return ()



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



def wdig(G, rows, cx, y, cz, cell, col, k=1.0):
    """세트에 서 있는 도트 글자 (−y쪽을 보는 면, 가운데 맞춤): 칸 하나 = 발광 상자."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        G.b((cx + ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, y, cz + (h / 2.0 - r - 0.5) * cell * k),
            (((c1 - c + 1) - 0.06) * cell * k, 0.03, cell * 0.94 * k), col)


# ───────────────────────── 색 · 도트 그림 ─────────────────────────
DIG.update({"c": ["###", "#..", "#..", "#..", "###"]})
MUD = (0.58, 0.52, 0.45)
SANDL, SANDD = (0.74, 0.60, 0.40), (0.34, 0.24, 0.15)
WATER, WATER2 = (0.14, 0.36, 0.70), (0.26, 0.52, 0.80)
WHITEC = (0.94, 0.94, 0.92)
SKINC = X.SKIN
EX_SH = [(0.85, 0.30, 0.28), (0.95, 0.80, 0.35), (0.35, 0.65, 0.40), (0.45, 0.75, 0.85), (0.80, 0.55, 0.65), (0.25, 0.45, 0.80),
         (0.92, 0.92, 0.90), (0.40, 0.55, 0.50), (0.88, 0.58, 0.30)]      # 블록 사람 (지후의 보라는 피함)
JH_SH, JH_PA = (0.58, 0.32, 0.80), (0.15, 0.18, 0.30)      # 지후: 보라 후드 · 짧은 머리 · 남색 바지
CO_SH, CO_PA = (0.93, 0.93, 0.91), (0.22, 0.24, 0.30)      # 연구원: 흰 가운 (extra='coat')
GLOWY = (3.0, 2.6, 0.8)
CLK = ["..###..", ".#.#.#.", "#..#..#", "#..##.#", "#.....#", ".#...#.", "..###.."]
CHECK = ["......#", ".....#.", "#...#..", ".#.#...", "..#...."]
ARROW = ["..#..", ".###.", "#.#.#", "..#..", "..#.."]


def sand_col(f):
    return tuple(lerp(a, b, clamp(f)) for a, b in zip(SANDL, SANDD))


# ───────────────────────── 세트 ─────────────────────────
def _flat(v):
    """서해 갯벌: 회갈색 평지 + 먼 수평선 바다 + 얕은 물웅덩이(서로 안 겹치게)."""
    v.floor(-60, 60, -20, 96, MUD, 2.0)
    for k in range(12):
        x0 = -50 + 8.5 * k
        y0 = 9 + 6.5 * ((k * 5) % 7)
        v.box(x0, x0 + 4.0 + 0.4 * (k % 3), y0, y0 + 1.6 + 0.3 * (k % 2), 0.0, 0.012, (0.40, 0.52, 0.62), jit=0.03)
    v.box(-140, 140, 96, 150, 0.0, 0.15, (0.20, 0.40, 0.62))
    for k in range(5):                                        # 먼 섬 (y를 조금씩 비껴 놓음)
        x0 = -70 + 31 * k
        v.box(x0, x0 + 12, 104 + 2.3 * k, 112 + 2.3 * k, 0.15, 1.5 + 0.9 * (k % 3), (0.30, 0.45 + 0.02 * k, 0.34), jit=0.05)


def _cross(v):
    v.floor(-14, 14, -14, 6, (0.80, 0.78, 0.72), 0.5, "check")
    v.wall((-14, 6), (14, 6), 0, 12, (0.62, 0.76, 0.86), 0.5, face=-1)


COAST = lambda y: 0.35 * math.sin(2.1 * y) + 0.15
MCELL = 0.15
_NY = 13


def map_cells():
    """지도판 칸 [(x, y, 종류)] 종류: 'sea'는 바닥 상자가 대신하니 'mud'·'land'만."""
    out = []
    for a in range(20):
        x = -1.5 + MCELL * (a + 0.5)
        for b in range(_NY):
            y = -1.0 + (2.0 / _NY) * (b + 0.5)
            xc = COAST(y)
            if x >= xc:
                out.append((x, y, "land"))
            elif x >= xc - 0.45:
                out.append((x, y, "mud"))
    return out


MCELLS = map_cells()
_rp = np.random.default_rng(4343)
_mud = [(x, y) for x, y, k in MCELLS if k == "mud"]
PINS = [_mud[int(j)] for j in sorted(_rp.permutation(len(_mud))[:26])]
assert len(PINS) == 26


def _map(v):
    v.floor(-10, 10, -10, 8, (0.50, 0.36, 0.24), 0.5, "wood")
    v.wall((-10, 7), (10, 7), 0, 6, (0.30, 0.50, 0.55), 0.5, face=-1)
    v.box(-1.9, 1.9, -1.4, 1.4, 0.72, 0.80, (0.60, 0.42, 0.26))
    for sx in (-1.75, 1.75):
        for sy in (-1.25, 1.25):
            v.box(sx - 0.1, sx + 0.1, sy - 0.1, sy + 0.1, 0.0, 0.72, (0.45, 0.31, 0.20))
    v.box(-1.5, 1.5, -1.0, 1.0, 0.80, 0.84, (0.16, 0.38, 0.72))              # 바다
    for x, y, k in MCELLS:
        dy = 2.0 / _NY
        if k == "land":
            v.box(x - MCELL / 2, x + MCELL / 2, y - dy / 2, y + dy / 2, 0.84, 0.865, (0.78, 0.66, 0.42), jit=0.05)
        else:
            v.box(x - MCELL / 2, x + MCELL / 2, y - dy / 2, y + dy / 2, 0.84, 0.855, (0.46, 0.42, 0.38), jit=0.05)


def _knoll(v):
    """노을 둔덕: 앞은 갯벌, 뒤는 풀 계단 5단 (단마다 앞·뒤·옆 끝을 다르게 해 같은 평면을 피함)."""
    v.floor(-60, 60, -100, 2, MUD, 2.0)
    v.floor(-60, 60, 2, 140, (0.36, 0.55, 0.28), 2.0)
    for k in range(5):
        v.box(-16 + 2.2 * k, 16 - 2.2 * k, 2.0 + 1.5 * k, 22 - 1.3 * k, 0.0, 0.35 * (k + 1),
              (0.34 + 0.02 * k, 0.52 + 0.02 * k, 0.26 + 0.01 * k), jit=0.05)
    v.box(-200, 200, -150, -100, 0.0, 0.15, (0.20, 0.36, 0.58))


def _city(v):
    v.floor(-70, 70, -70, 70, (0.42, 0.43, 0.46), 2.0)
    rs = v.rs
    for i in range(-6, 7):
        for j in range(-5, 8):
            cx, cy = 10 * i, 10 * j
            if abs(cx) < 8 and cy < 40:                       # 가운데 큰길은 비움 (카메라 시야)
                continue
            w, d = 5.0 + float(rs.uniform(0, 2.2)), 5.0 + float(rs.uniform(0, 2.2))
            h = float(rs.uniform(5.0, 30.0))
            g = float(rs.uniform(0.55, 0.85))
            col = (g, g * float(rs.uniform(0.92, 1.05)), g * float(rs.uniform(0.95, 1.12)))
            v.box(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, 0.0, h, col, jit=0.03)


def _sets():
    return (("flat", _flat), ("cross", _cross), ("shore", _flat), ("map", _map), ("knoll", _knoll), ("city", _city))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR) ─────────────────────────
N_FX, N_GL, N_OR = 1100, 400, 6


def pit(F, f, wob=0.0, t=0.0):
    """퀵샌드 구덩이: 납작한 판 + 둘레 상자 16개. f = 굳음(0 밝음~1 짙음), wob = 출렁임."""
    col = sand_col(f)
    F.b((0.0, 0.0, 0.02), (2.1, 2.1, 0.04), col)
    for q in range(16):
        a = 2 * math.pi * (q + 0.5 * _h(q)) / 16
        r = 0.56 + 0.10 * wob * math.sin(7 * a + 9 * t)
        s = 0.20 + 0.05 * _h(q + 9)
        F.b((r * math.cos(a), r * math.sin(a), 0.04 + 0.35 * s), (s, s, s * 0.7), tuple(c * 0.92 for c in col))


def spray(F, age, col):
    """되튕김 순간 튀는 모래 알갱이 8개."""
    if not 0.0 <= age < 0.4:
        return
    for q in range(8):
        a = 2 * math.pi * _h(q + 40)
        r = 0.55 + age * (1.0 + 1.2 * _h(q + 50))
        z = 0.12 + 2.4 * age * (0.6 + _h(q + 60)) - 6.0 * age * age
        F.b((r * math.cos(a), r * math.sin(a), max(z, 0.06)), (0.07, 0.07, 0.07), col)


def gull(F, x, y, z, flap, yaw=0.0):
    """갈매기: 몸통 상자 + 날개 상자 둘 (날갯짓 flap 라디안, 진행 방향 yaw 라디안)."""
    cy, sy = math.cos(yaw), math.sin(yaw)
    F.c((x, y, z), (0.34, 0.14, 0.12), (0.95, 0.95, 0.93), (0.0, 0.0, yaw))
    F.c((x + 0.2 * cy, y + 0.2 * sy, z + 0.02), (0.12, 0.09, 0.09), (0.95, 0.75, 0.25), (0.0, 0.0, yaw))
    for s in (-1, 1):
        ly, lz = s * 0.28 * math.cos(flap), 0.28 * math.sin(flap) * 1.0
        F.c((x - sy * ly, y + cy * ly, z + lz), (0.20, 0.55, 0.03), (0.90, 0.90, 0.90), (s * flap, 0.0, yaw))


def props_hook(i, tau, dur, u, S, t, cam, F, G, OR):
    sp = spring(tau)
    pit(F, 0.55 + 0.25 * sp, 1.0 - sp, tau)
    spray(F, snap_age(tau), sand_col(0.3))


def props_force(i, tau, dur, u, S, t, cam, F, G, OR):
    pit(F, 0.7, 0.15 * math.sin(14 * tau), tau)
    s = pop(tau - 0.15, 0.3)
    F.b((0.45, -0.28, 0.04 + 0.5 * s), (0.10, 0.03, 1.0 * s), (0.93, 0.90, 0.76))
    for k in range(1, 10):
        big = k % 5 == 0
        F.b((0.45 + 0.09 + (0.03 if big else 0.0), -0.30, 0.04 + 0.1 * k * s), (0.08 + (0.06 if big else 0.0), 0.02, 0.012), (0.2, 0.2, 0.2))
    k2 = pop(tau - 0.5, 0.3)
    wdig(G, num_rows("1cm"), 0.85, -0.2, 1.2, 0.03, GLOWY, k2)
    wdig(G, ARROW, 0.85, -0.2, 0.98, 0.03, GLOWY, k2)


def props_pull(i, tau, dur, u, S, t, cam, F, G, OR):
    pit(F, 0.5 + 0.5 * u, 1.0 - spring(tau, 0.55), tau)
    spray(F, snap_age(tau, 0.55), sand_col(0.4))


# ── 3 · 저울 (모래 상자 2 vs 사람 상자 1)
BAL_C, BAL_L, BAL_RY = np.array((0.0, 0.0, 2.4)), 3.0, -0.30


def bal_geom(tau):
    ry = BAL_RY + 0.10 * math.exp(-3.0 * tau) * math.sin(14 * tau)
    half = _rmat(0.0, ry, 0.0) @ np.array((BAL_L / 2, 0.0, 0.0))
    return ry, BAL_C - half, BAL_C + half


def props_dens(i, tau, dur, u, S, t, cam, F, G, OR):
    ry, left, right = bal_geom(tau)
    F.c(tuple(BAL_C), (BAL_L, 0.25, 0.2), (0.62, 0.62, 0.66), (0.0, ry, 0.0))
    F.b((0.0, 0.0, 1.15), (0.25, 0.25, 2.3), (0.45, 0.45, 0.5))
    F.b((0.0, 0.0, 0.1), (1.6, 1.0, 0.2), (0.40, 0.40, 0.45))
    for p in (left, right):
        F.b((p[0], p[1], p[2] + 0.10), (1.2, 0.9, 0.1), (0.80, 0.70, 0.35))
    sc = pop(tau - 0.1, 0.3)
    for n in range(2):                                          # 모래 큐브 2개
        F.b((left[0], 0.0, left[2] + 0.15 + 0.35 + 0.7 * n), (0.7 * sc, 0.7 * sc, 0.7 * sc), sand_col(0.25 + 0.2 * n))
    F.b((right[0], 0.0, right[2] + 0.15 + 0.35), (0.7 * sc, 0.7 * sc, 0.7 * sc), JH_SH)             # 사람 큐브 1개
    F.b((right[0], 0.0, right[2] + 0.15 + 0.7 + 0.12), (0.30 * sc, 0.30 * sc, 0.30 * sc), SKINC)
    wdig(G, num_rows("2"), left[0], -0.5, left[2] + 0.15 + 1.4 + 0.45, 0.1, GLOWY, pop(tau - 0.5, 0.3))
    wdig(G, num_rows("1"), right[0], -0.5, right[2] + 0.15 + 0.7 + 0.55, 0.1, GLOWY, pop(tau - 0.5, 0.3))


def props_waist(i, tau, dur, u, S, t, cam, F, G, OR):
    pit(F, 1.0, 0.3 * (1.0 - ramp(tau, 0.0, 1.4)), tau)
    m = pop(tau - 1.3, 0.3)
    if m > 0.02:
        for q in range(20):
            a = 2 * math.pi * q / 20
            G.b((0.8 * math.cos(a), 0.8 * math.sin(a), 0.08), (0.14 * m, 0.14 * m, 0.04), GLOWY)


def props_hour(i, tau, dur, u, S, t, cam, F, G, OR):
    pit(F, 1.0, 0.0, tau)
    for q in range(5):                                          # 갈매기 5마리가 머리 위를 돎
        ph = 2 * math.pi * (q / 5.0 + t / 4.2)
        gx, gy, gz = 0.9 + 1.3 * math.cos(ph), 2.5 + 1.3 * math.sin(ph), 2.2 + 0.15 * math.sin(2 * t + q)
        gull(F, gx, gy, gz, 0.55 * math.sin(2 * math.pi * (3.0 * t + 0.2 * q)), ph + math.pi / 2)


def props_still(i, tau, dur, u, S, t, cam, F, G, OR):
    pit(F, 0.85 + 0.15 * u, 0.0, tau)
    d = S.get("jh")
    if d is not None:
        sx, sy, sz = rel(d, 0.0, -0.30, hip_of(d["pose"]) + 0.66)
        k = smooth((tau - 0.15) / 0.9)                            # 하늘에서 어깨로 내려앉음
        gull(F, lerp(sx + 1.4, sx, k), lerp(sy - 0.6, sy, k), lerp(sz + 1.3, sz, k), 0.55 * (1.0 - k) * math.sin(30 * tau), -1.2 * (1.0 - k) + math.pi / 2)


# ── 6 · 8 단면판 (알갱이 14x8 격자)
GC, GR, CELL = 14, 8, 0.27


def cross_frame(F):
    F.b((0.0, 0.36, 2.2), (4.8, 0.04, 2.9), (0.22, 0.28, 0.38))
    for sz in (-1, 1):
        F.b((0.0, 0.30, 2.2 + sz * 1.49), (4.9, 0.08, 0.08), (0.92, 0.92, 0.90))
    for sx in (-1, 1):
        F.b((sx * 2.46, 0.30, 2.2), (0.08, 0.08, 2.9), (0.92, 0.92, 0.90))


def grain_xz(k, sc):
    r, c = divmod(k, GC)
    return (c - (GC - 1) / 2) * CELL * sc, 2.2 + ((GR - 1) / 2 - r) * CELL * sc


def draw_grains(F, loose, amp, hz, t):
    sc = 1.0 + 0.18 * loose
    for k in range(GC * GR):
        x, z = grain_xz(k, sc)
        x += amp * math.sin(t * 21 * hz + k * 1.7)
        z += amp * math.sin(t * 17 * hz + k * 2.3)
        s = CELL * (0.94 - 0.16 * loose) * (1.0 - 0.1 * _h(k))
        j = 0.06 * (_h(k + 5) - 0.5)
        col = tuple(clamp(lerp(a, b, loose) + j) for a, b in zip((0.42, 0.30, 0.19), (0.80, 0.64, 0.42)))
        F.b((x, 0.15, z), (0.22, s, s), col)


def props_liquef(i, tau, dur, u, S, t, cam, F, G, OR):
    cross_frame(F)
    loose = 1.0 - smooth((tau - 0.5 * dur) / (0.22 * dur))
    draw_grains(F, loose, 0.07 * loose, 1.0, t)


_rw = np.random.default_rng(8)
WRANK = _rw.random((GR - 1) * (GC - 1))


def props_wiggle(i, tau, dur, u, S, t, cam, F, G, OR):
    cross_frame(F)
    loose = 0.15 + 0.85 * ramp(tau, 0.2, 0.55 * dur)
    draw_grains(F, loose, 0.03, 0.25, t)
    sc = 1.0 + 0.18 * loose
    f = ramp(tau, 0.3, 0.85 * dur)
    for n in range((GR - 1) * (GC - 1)):
        r, c = divmod(n, GC - 1)
        if f > WRANK[n] * 0.9:
            x0, z0 = grain_xz(r * GC + c, sc)
            x1, z1 = grain_xz((r + 1) * GC + c + 1, sc)
            s = 0.10 * pop((f - WRANK[n] * 0.9) * dur * 0.6, 0.2)
            F.b(((x0 + x1) / 2, 0.16, (z0 + z1) / 2), (0.12, s, s), (0.20, 0.55, 0.95))


def props_shoe(i, tau, dur, u, S, t, cam, F, G, OR):
    pit(F, 0.1, 0.25 * math.sin(3 * tau), tau)
    for q in range(8):                                          # 스며든 물
        a = 2 * math.pi * (q + 0.5 * _h(q + 70)) / 8
        F.b((0.9 * math.cos(a), 0.9 * math.sin(a), 0.05), (0.14, 0.14, 0.012), WATER2)
    s = pop(tau - 0.65 * dur, 0.3)
    if s > 0.01:
        F.b((0.0, -0.02, 0.04 + 0.05 * s), (0.30 * s, 0.14 * s, 0.10 * s), (0.75, 0.15, 0.15))
        F.b((0.0, -0.02, 0.04 + 0.01 * s), (0.31 * s, 0.15 * s, 0.02 * s), (0.9, 0.9, 0.88))


# ── 10~12 밀물
def tide_water(F, yf, zw):
    """납작한 물 상자 세 겹 (앞이 낮고 뒤가 높음). yf = 앞 끝 y, zw = 가장 높은 겹의 물 깊이."""
    for l in range(3):
        zl = zw * (0.45 + 0.275 * l)
        F.b((0.0, yf + 5.0 * l + 35.0, zl / 2), (120.0, 70.0, zl), tuple(lerp(a, b, l / 2.0) for a, b in zip(WATER2, WATER)))


def props_tide(i, tau, dur, u, S, t, cam, F, G, OR):
    f = smooth(u)
    tide_water(F, lerp(62.0, 14.0, f), 0.05 + 0.07 * f)
    for k, (px, py) in enumerate(((-2.6, 2.2), (2.8, 1.4), (-1.4, 4.2), (1.6, 4.8), (-3.8, 6.0), (3.6, 6.4))):
        s = 0.2 + 1.3 * ramp(u, 0.0, 1.0) * (0.7 + 0.3 * _h(k))
        F.b((px, py, 0.012), (s, s * 0.8, 0.024), WATER2)


def clock_icon(G, cam, tau, nx=-0.62, ny=0.02):
    srows(G, cam, CLK, nx, ny, 0.022, GLOWY, 1.8, pop(tau - 0.3, 0.3))


def props_danger(i, tau, dur, u, S, t, cam, F, G, OR):
    tide_water(F, lerp(3.5, -2.5, smooth(u)), 0.06 + 0.10 * ramp(u, 0.0, 1.0))
    clock_icon(G, cam, tau)


def boat_bow(F, G, cx, cy, t):
    """해경 보트(뱃머리가 -y). 세트 좌표."""
    bob = 0.025 * math.sin(6 * t)
    F.b((cx, cy, 0.22 + bob), (1.7, 4.2, 0.35), WHITEC)
    for sx in (-1, 1):
        F.b((cx + sx * 0.85, cy, 0.52 + bob), (0.12, 4.2, 0.30), WHITEC)
        F.b((cx + sx * 0.92, cy - 0.3, 0.30 + bob), (0.04, 3.4, 0.08), (0.10, 0.25, 0.60))
    F.b((cx, cy - 2.5, 0.28 + bob), (1.2, 0.9, 0.30), (0.10, 0.25, 0.60))
    F.b((cx, cy + 0.9, 0.80 + bob), (1.0, 1.2, 0.70), (0.85, 0.88, 0.95))
    F.b((cx, cy + 0.9, 1.20 + bob), (1.1, 1.3, 0.10), (0.10, 0.25, 0.60))
    q = 0.5 + 0.5 * math.sin(2 * math.pi * t * 2.5)
    G.b((cx - 0.2, cy + 0.9, 1.33 + bob), (0.22, 0.12, 0.10), (3.0 * q, 0.2, 0.2))
    G.b((cx + 0.2, cy + 0.9, 1.33 + bob), (0.22, 0.12, 0.10), (0.2, 0.5 * (1 - q), 3.0 * (1 - q) + 0.3))
    for n in range(12):                                         # 항적
        s = n % 2 * 2 - 1
        d = 0.8 + 0.5 * (n // 2)
        F.b((cx + s * (0.9 + 0.35 * (n // 2)), cy - 1.2 + d + 0.3 * math.sin(7 * t + n), 0.15), (0.24, 0.5, 0.05), (0.95, 0.97, 1.0))


def props_boat(i, tau, dur, u, S, t, cam, F, G, OR):
    tide_water(F, -30.0, 0.13)
    boat_bow(F, G, 1.2, lerp(48.0, 4.0, smooth(u)), t)


def props_rescued(i, tau, dur, u, S, t, cam, F, G, OR):
    tide_water(F, -30.0, 0.13)
    bob = 0.03 * math.sin(2.5 * t)
    F.b((0.0, 0.0, 0.22 + bob), (5.0, 1.6, 0.35), WHITEC)
    for sy in (-1, 1):
        F.b((0.0, sy * 0.75, 0.52 + bob), (5.0, 0.12, 0.30), WHITEC)
        F.b((0.0, sy * 0.82, 0.30 + bob), (5.0, 0.04, 0.08), (0.80, 0.18, 0.15))
    F.b((2.75, 0.0, 0.28 + bob), (0.8, 1.0, 0.30), (0.10, 0.25, 0.60))
    F.b((0.0, 0.0, 0.46 + bob), (4.6, 0.4, 0.06), (0.55, 0.40, 0.25))
    for n in range(7):
        s = pop(tau - 0.15 - 0.18 * n, 0.3)
        if s < 0.01:
            continue
        x = -2.1 + 0.7 * n
        sh = EX_SH[(n * 4) % len(EX_SH)]
        F.b((x, 0.0, 0.52 + bob + 0.25 * s), (0.40 * s, 0.34 * s, 0.50 * s), sh)
        F.b((x, -0.01, 0.66 + bob + 0.25 * s), (0.42 * s, 0.36 * s, 0.14 * s), (0.95, 0.55, 0.15))
        F.b((x, 0.0, 0.52 + bob + 0.5 * s + 0.15 * s), (0.26 * s, 0.26 * s, 0.26 * s), SKINC)
    for n in range(14):                                         # 선체 둘레 물결
        a = 2 * math.pi * n / 14 + 0.5 * t
        F.b((3.3 * math.cos(a), 1.5 * math.sin(a), 0.14), (0.4, 0.14, 0.04), (0.95, 0.97, 1.0))


# ── 13~14 지도판
def props_count(i, tau, dur, u, S, t, cam, F, G, OR):
    for k, (x, y) in enumerate(PINS):
        s = pop(tau - 0.45 * dur * k / 26.0 - 0.05, 0.25)
        blink = 0.65 + 0.35 * math.sin(2 * math.pi * (1.8 * t + _h(k)))
        G.b((x, y, 0.93), (0.05 * s, 0.05 * s, 0.14 * s), (3.0 * blink, 0.4 * blink, 0.3 * blink))


def props_twist(i, tau, dur, u, S, t, cam, F, G, OR):
    for k, (x, y) in enumerate(PINS):
        sp = 1.0 - ramp(tau, 0.1 + 0.02 * k, 0.5 + 0.02 * k)
        if sp > 0.02:
            G.b((x, y, 0.93), (0.05 * sp, 0.05 * sp, 0.14 * sp), (3.0, 0.4, 0.3))
        c = pop(tau - 0.3 - 0.03 * k, 0.3)
        if c > 0.02:
            a = 3.0 * t + k
            F.b((x, y, 0.885), (0.14 * c, 0.14 * c, 0.03 * c), (0.15, 0.15, 0.2))
            F.b((x, y, 0.905), (0.11 * c, 0.11 * c, 0.02 * c), WHITEC)
            F.c((x + 0.025 * c * math.cos(a), y + 0.025 * c * math.sin(a), 0.925), (0.05 * c, 0.012, 0.012), (0.1, 0.1, 0.1), (0.0, 0.0, a))
            F.c((x + 0.012 * c * math.cos(a / 6), y + 0.012 * c * math.sin(a / 6), 0.927), (0.025 * c, 0.014, 0.012), (0.1, 0.1, 0.1), (0.0, 0.0, a / 6))


# ── 15 조석표 (거꾸로 → 뒤집음)
BARS = (0.10, 0.22, 0.34, 0.20, 0.08, 0.20, 0.32)


def flip_s(tau):
    """-1(거꾸로) → +1(바로): 1.25초에서 0.4초 동안 판이 납작해졌다 뒤집힘."""
    return -1.0 + 2.0 * smooth((tau - 1.25) / 0.4)


def tide_panel(F, c, s):
    a = max(abs(s), 0.03)
    F.b(c, (0.80, 0.03, 0.46 * a), (0.95, 0.93, 0.82))
    F.b((c[0], c[1] - 0.02, c[2] + s * 0.17), (0.74, 0.03, 0.09 * a), (0.15, 0.30, 0.65))
    for j, h in enumerate(BARS):
        F.b((c[0] + (j - 3) * 0.10, c[1] - 0.02, c[2] + s * (-0.19 + h * 0.5)), (0.06, 0.03, h * 0.7 * a), (0.20, 0.50, 0.85))


def props_chart(i, tau, dur, u, S, t, cam, F, G, OR):
    d = S.get("jh")
    if d is not None:
        px, py, pz = rel(d, 0.55, 0.0, 1.2)
        tide_panel(F, (px, py, pz), flip_s(tau))


def props_look(i, tau, dur, u, S, t, cam, F, G, OR):
    tide_water(F, lerp(-62.0, -46.0, u), 0.10)
    OR.orb((12.0, -120.0, 6.0), 12.0, (3.0, 1.5, 0.5))


def props_dusk(i, tau, dur, u, S, t, cam, F, G, OR):
    OR.orb((-12.0, 110.0, 6.0), 12.0, (3.0, 1.5, 0.5))
    OR.orb((-12.0, 116.0, 6.0), 24.0, (1.3, 0.55, 0.25))


def props_walkout(i, tau, dur, u, S, t, cam, F, G, OR):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR)


def props_app(i, tau, dur, u, S, t, cam, F, G, OR):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR)
    d = S.get("jh")
    if d is not None:
        hx, hy, hz = hand_pt(d, "R", 0.12)
        F.b((hx, hy - 0.04, hz + 0.18), (0.30, 0.03, 0.52), (0.08, 0.09, 0.12))
        G.b((hx, hy - 0.07, hz + 0.18), (0.26, 0.02, 0.46), (0.25, 0.55, 0.85))
        k = pop(tau - 0.4, 0.3)
        wdig(G, CLK, hx - 0.05, hy - 0.10, hz + 0.20, 0.032, GLOWY, k)
        wdig(G, CHECK, hx + 0.05, hy - 0.10, hz + 0.34, 0.016, (0.4, 2.6, 0.6), k)


def props_dusk20(i, tau, dur, u, S, t, cam, F, G, OR):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR)
    F.b((-0.7, -0.2, 0.09), (0.30, 0.14, 0.10), (0.75, 0.15, 0.15))
    F.b((-0.7, -0.2, 0.04), (0.31, 0.15, 0.02), (0.9, 0.9, 0.88))


def props_ask(i, tau, dur, u, S, t, cam, F, G, OR):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR)
    srows(G, cam, CLK, 0.5, 0.12 + 0.02 * math.sin(2 * math.pi * t / 1.1), 0.022, GLOWY, 1.8, pop(tau - 0.3, 0.3))


def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR):
    for k in range(120):
        ph = (_h(k + 500) + 0.12 * t) % 1.0
        x = -6.0 + 12.0 * _h(k + 700)
        y = -20.0 + 60.0 * ph
        F.b((x, y, 0.35 + 0.1 * abs(math.sin(8 * t + k))), (0.5, 0.5, 0.7), EX_SH[k % len(EX_SH)])


PROPS = {LN["hook"]: props_hook, LN["force"]: props_force, LN["pull"]: props_pull, LN["dens"]: props_dens, LN["waist"]: props_waist,
         LN["hour"]: props_hour, LN["liquef"]: props_liquef, LN["still"]: props_still, LN["wiggle"]: props_wiggle,
         LN["shoe"]: props_shoe, LN["tide"]: props_tide, LN["danger"]: props_danger, LN["boat"]: props_boat,
         LN["count"]: props_count, LN["twist"]: props_twist, LN["chart"]: props_chart, LN["rescued"]: props_rescued,
         LN["walkout"]: props_walkout, LN["look"]: props_look, LN["app"]: props_app, LN["dusk"]: props_dusk20,
         LN["ask"]: props_ask, LN["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off)
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR)
    return F, G, OR


# ───────────────────────── 등장인물 ─────────────────────────
def jh_hook(tau, t):
    sp = spring(tau)
    return dict(z=-0.40 + 0.28 * sp, yaw=-90 + 6 * math.sin(7 * tau), pose="angry" if sp > 0.35 else "shock")


def jh_force(tau, t):
    return dict(z=-0.30 + 0.025 * math.sin(17 * tau))


def jh_pull(tau, t):
    sp = spring(tau, 0.55)
    return dict(z=-0.40 + 0.26 * sp, yaw=-90 + 10 * math.sin(9 * tau), pose="angry" if sp > 0.35 else "shock")


def jh_still(tau, t):
    return dict(z=-0.78 + 0.02 * math.sin(2 * math.pi * tau / 2.2))


def jh_chart(tau, t):
    return dict(pose="carry" if tau < 1.4 else "carry_o", yaw=-90 + 4 * math.sin(2.0 * tau))


def span_of(name):
    a, b = shot_span(LN[name])
    return b - a


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    dsh, dw, dh = span_of("shoe"), span_of("walkout"), span_of("dusk")
    # 9번 줄: 발이 한 칸씩 올라옴(-0.78 → -0.6 → -0.4 → -0.2) → 쑥 빠져 옆으로 깡충
    sk = [(0.0, (0.0, 0.0, -0.78, -90.0)), (0.12, (0.0, 0.0, -0.78, -90.0)), (0.22, (0.0, 0.0, -0.60, -85.0)), (0.34, (0.0, 0.0, -0.60, -95.0)),
          (0.44, (0.0, 0.0, -0.40, -85.0)), (0.56, (0.0, 0.0, -0.40, -95.0)), (0.66, (0.0, 0.0, -0.18, -90.0)), (0.74, (0.0, 0.0, 0.0, -90.0)),
          (0.84, (0.5, 0.0, 0.3, -90.0)), (0.94, (0.9, 0.0, 0.0, -90.0))]
    add("jh", 0, JH_SH, JH_PA, {
        L["hook"]: st("flat", 0.0, 0.0, -90, "shock", fn=jh_hook, also=("angry", "shock")),
        L["force"]: st("flat", 0.0, 0.0, -90, "angry", fn=jh_force),
        L["pull"]: st("flat", 0.0, 0.0, -90, "shock", fn=jh_pull, also=("angry", "shock")),
        L["waist"]: st("flat", 0.0, 0.0, -90, "shock", keys=[(0.0, (0.0, 0.0, -0.32, -90.0)), (1.3, (0.0, 0.0, -0.78, -90.0))], seq=[(1.4, "gape")]),
        L["hour"]: st("flat", 0.0, 0.0, -90, "gape", z=-0.78, alt=("gape", "confused", 1.3, 0.0)),
        L["still"]: st("flat", 0.0, 0.0, -90, "stand", fn=jh_still),
        L["shoe"]: st("flat", 0.0, 0.0, -90, "gape", keys=[(f * dsh, p) for f, p in sk], seq=[(0.74 * dsh, "shock"), (0.94 * dsh, "stand")]),
        L["tide"]: st("shore", 0.0, 0.0, -90, "confused", alt=("confused", "stand", 1.0, 0.0)),
        L["danger"]: st("shore", 0.0, 0.0, -90, "shock", alt=("shock", "confused", 0.45, 0.0)),
        L["boat"]: st("shore", 0.0, -1.5, -90, "stand", alt=("shock", "stand", 0.5, 0.0)),
        L["chart"]: st("map", 0.0, -3.4, -90, "carry", fn=jh_chart, also=("carry_o",)),
        L["walkout"]: st("knoll", -0.5, -7.0, 90, "walk_a_s", pair=("walk_a_s", "walk_b_s"), cad=0.30,
                         keys=[(0.0, (-0.5, -7.0, 0.0, 90.0)), (0.85 * dw, (-0.5, -1.4, 0.0, 90.0))], ease=lambda x: x),
        L["look"]: st("knoll", -0.05, 0.8, -90, "point"),
        L["app"]: st("knoll", 0.0, 0.0, -90, "film"),
        L["dusk"]: st("knoll", 0.0, -1.5, 90, "walk_a_s", pair=("walk_a_s", "walk_b_s"), cad=0.34,
                      keys=[(0.0, (0.0, -1.5, 0.0, 90.0)), (0.9 * dh, (0.0, 1.3, 0.0, 90.0))], ease=lambda x: x),
        L["ask"]: st("knoll", 0.0, 0.0, -90, "think", seq=[(0.9, "smile")])}, extra="hood")
    add("rs", 1, CO_SH, CO_PA, {
        L["hour"]: st("flat", 1.9, 0.1, 190, "think", alt=("think", "talk", 1.7, 0.4)),
        L["shoe"]: st("flat", -1.35, 0.2, 10, "talk", alt=("talk", "think", 1.2, 0.0)),
        L["walkout"]: st("knoll", 0.55, -7.4, 90, "walk_b_s", pair=("walk_b_s", "walk_a_s"), cad=0.30,
                         keys=[(0.0, (0.55, -7.4, 0.0, 90.0)), (0.85 * dw, (0.55, -1.8, 0.0, 90.0))], ease=lambda x: x),
        L["look"]: st("knoll", 0.7, 0.8, -90, "talk", alt=("talk", "stand", 1.2, 0.0))}, extra="coat")
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
WARM_SKY = ((0.30, 0.38, 0.62), (0.98, 0.76, 0.54), 0.0)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
ROOM_SKY = ((0.30, 0.45, 0.70), (0.75, 0.82, 0.90), 0.0)

WARM_LINES = (LN["hour"], LN["tide"], LN["danger"], LN["boat"], LN["rescued"])
DUSK_LINES = (LN["walkout"], LN["look"], LN["app"], LN["dusk"], LN["ask"])


def sky(t):
    i = line_at(t)
    if i in DUSK_LINES:
        return DUSK_SKY
    if i in WARM_LINES:
        return WARM_SKY
    return DAY_SKY


def env(i, st_):
    """줄(컷 세트)별 해·주변광. 점광원은 쓰지 않음(해가 모든 세트를 밝힘 — 어두운 방 없음)."""
    e = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if i in WARM_LINES:
        e.update(sun=2.8, sun_col=(1.0, 0.80, 0.55), sun_rot=(60, 0, 30), amb=0.40, amb_col=(0.78, 0.70, 0.74))
    elif i in DUSK_LINES:
        e.update(sun=2.4, sun_col=(1.0, 0.62, 0.38), sun_rot=(72, 0, 20), amb=0.30, amb_col=(0.72, 0.52, 0.62))
        if i == LN["look"]:
            e.update(sun_rot=(72, 0, 200))                        # 카메라 뒤에서 비춤
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
    F, G, OR = props(i, tau, dur, u, S, t, cam)
    return dict(i=i, tau=tau, u=u, set=cam["set"], cam=cam, A=S, P=P, R=R, CO=CO, C2=C2, SC=SC, PO=PO, F=F, G=G, OR=OR,
                env=env(i, cam["set"]))


# ───────────────────────── Blender 원형(프로토) ─────────────────────────
def build(ctx):
    from engine import bkit as K
    v = X.Vox(43)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep43_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep43_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep43_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep43_fx", K.proto(ctx, "ep43_p_fx", cube(), [K.mat_inst("ep43_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep43_glow", K.proto(ctx, "ep43_p_glow", cube(), [_mat_glow("ep43_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep43_orb", K.proto(ctx, "ep43_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep43_m_orb")]),
                      N_OR, vector_scale=True)
    for ob in (gl, orb):                                              # 발광 상자·해가 햇빛을 가리지 않게
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
        for ob, items in ((fx, S["F"]), (gl, S["G"]), (orb, S["OR"])):
            Pp, Sc, Sz, Rt, Co = items.arrays()
            K.set_points(ob, Pp, scale=Sc, size=Sz, rot=Rt, col=Co)

    ctx.on_frame(upd)
