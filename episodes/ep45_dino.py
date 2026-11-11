"""EP45 만약에 공룡이 멸종하지 않았다면? (기준 영상 형식 STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

11-06 오너: 42~49는 '남자가 한 명뿐이라면' 편 형식으로, 내레이션 없이. 소리는 배경음(-23 LUFS)과 효과음뿐.
장면(3D)은 11-05 픽세판 그대로(백악기 숲·불덩이·종 아이콘·한강변·연표 줄자·신호등·박물관·공원 비둘기), 줄 순서도 그대로(이미 시간순).
6,600만 년 전(충돌 각도 60°) → 만약(비껴갔다면 살아남을 종 약 75%, 공룡 시대 1억 6천만 년) → 오늘(한강변, 티라노가 우리와 더 가깝다)
→ 연표(인류 30만 년) → 상상(1982년 디노사우로이드) → 반전(공룡은 새로 살아 있다, 땅에 살던 작은 새만 생존) → 지금 → 다음 편(정육면체 지구).
효과음: 묶음 '찰싹', 컷 '휙', 훅 불덩이 번쩍(T_BURST)에 '우르릉·쿵'.

근거(설명란): ※ '소행성이 비껴갔다'는 가정의 상상 시나리오. 공룡 크기·연표 눈금·그림 속 비율은 연출.
· 칙술루브 충돌각 약 60°(가장 유력, 기후에 가장 치명적) · Collins 외, Nature Communications 11:1480(2020)
· 생물 종의 약 75% 멸종(통칭) · Smithsonian·NASA 계열 보도
· 공룡 시대 약 1억 6천만 년 이상(출현 약 2.3억 년 전 − 멸종 약 6,600만 년 전, 계산) · 고생물 연표(AMNH 등)
· 스테고사우루스(약 1.5억 년 전)~티라노(약 6,800~6,600만 년 전) 약 8,400만 년 > 티라노~오늘 6,600만 년(계산) · Smithsonian Magazine
· 호모 사피엔스 가장 오래된 화석 약 31.5만 년 전 · Hublin 외, Nature 546:289(2017)
· 디노사우로이드 가설(사고 실험) · Russell & Séguin 1982, Syllogeus 37
· 새 약 1만 1천 종은 살아남은 공룡의 후손 · Field Museum, Smithsonian
· 살아남은 새는 땅에 사는 작은 종(숲이 불탄 뒤 나무 새는 멸종) · Field 외, Current Biology 28:1825(2018)
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"cret": (0, 0), "river": (300, 0), "cross": (600, 0), "ruler": (900, 0), "museum": (1200, 0), "park": (1500, 0), "teaser": (1800, 0)}
NAMES = ("hook", "angle", "pass", "icons", "era", "river", "bars", "cross", "mark", "tape", "mice", "model", "shake", "twist", "birds",
         "feed", "burnt", "selfie", "point", "flock", "sil", "ask", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}

# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
# ease="out": 처음에 빨리 움직이고 천천히 멈춤(훅)
LINES = [
    dict(d=3.0, sub="6,600만 년 전,\n소행성이 지구로 날아옵니다.", ease="out", shot=("cret", (0.0, 10.0, 1.9), -90, 3, 10.5, 28, 0.78, 3, 0.08)),
    dict(d=3.2, sub="연구진이 가장 유력하게 본\n충돌 각도는 약 60°.", shot=("cret", (0.1, 0.0, 2.0), -90, 2, 11.0, 28, 0.92, 2, 0.03)),
    dict(d=2.9, sub="그 소행성이 지구를\n비껴갔다고 가정합니다.", shot=("cret", (0.0, 10.0, 1.9), -78, 3, 11.0, 28, 0.90, 4, 0.08)),
    dict(d=3.4, sub="실제로는 생물 종의\n약 75%가 사라졌습니다.", shot=("cret", (0.0, 10.0, 2.2), -95, 4, 12.0, 26, 0.90, -3, 0.04)),
    dict(d=3.0, sub="공룡은 이미 1억 6천만 년 넘게\n살아온 터였습니다.", shot=("cret", (0.0, 10.0, 2.4), -85, 3, 11.0, 26, 0.88, 4, 0.04)),
    dict(d=3.0, sub="그럼 지금 한강변을\n공룡이 걷고 있을까요?", shot=("river", (0.0, 8.0, 2.8), -90, 3, 15.0, 26, 0.90, -3, 0.08)),
    dict(d=3.3, sub="티라노는 스테고보다\n우리와 더 가까운 시대입니다.", shot=("ruler", (0.0, 0.0, 1.6), -90, 8, 9.0, 26, 0.92, 3, 0.0)),
    dict(d=3.2, sub="등굣길 신호등 버튼이\n공룡 목 높이에 있습니다.", shot=("cross", (2.1, -8.0, 1.7), -85, 4, 8.5, 26, 0.90, 5, 0.08)),
    dict(d=2.9, sub="인류가 나타난 건\n겨우 30만 년 전입니다.", shot=("ruler", (9.9, 0.0, 0.18), -90, 10, 2.4, 26, 0.86, 3, 0.05)),
    dict(d=2.7, sub="연표에서 인류는\n눈금 끝 점 하나입니다.", shot=("ruler", (8.2, 0.0, 0.9), -90, 9, 6.2, 26, 0.92, -4, 0.06)),
    dict(d=3.2, sub="공룡 발밑에선 작은 포유류가\n조용히 살았습니다.", shot=("cret", (0.0, 3.0, 0.6), -90, 6, 4.2, 28, 0.90, 3, 0.03)),
    dict(d=3.0, sub="한 학자는 사람을 닮은\n공룡을 상상했습니다.", shot=("museum", (0.1, 3.0, 1.3), -90, 4, 8.0, 26, 0.90, 3, 0.06)),
    dict(d=2.5, sub="지후는 초록 이웃과\n악수를 나눕니다.", shot=("museum", (0.1, 3.2, 1.4), -90, 3, 5.8, 26, 0.92, -3, 0.06)),
    dict(d=2.9, sub="그런데 공룡은 사실\n사라지지 않았습니다.", shot=("museum", (0.0, 8.6, 2.3), -90, 0, 5.6, 26, 0.88, 3, 0.05)),
    dict(d=2.8, sub="비둘기도 참새도\n공룡의 후손입니다.", shot=("park", (0.0, 4.0, 0.5), -90, 6, 5.0, 28, 0.90, 5, 0.03)),
    dict(d=2.8, sub="지후는 오늘도 비둘기에게\n과자를 줍니다.", shot=("park", (0.0, 2.0, 0.8), 90, 30, 7.0, 26, 0.92, -4, -0.02)),
    dict(d=3.2, sub="숲이 불탄 뒤 살아남은 건\n메추리 닮은 새였습니다.", shot=("cret", (0.0, 5.5, 1.5), -90, 8, 9.0, 26, 0.92, 3, 0.0)),
    dict(d=2.9, sub="박물관 화석 앞에서\n지후가 사진을 찍습니다.", shot=("museum", (0.0, 4.0, 1.9), -90, 3, 10.0, 26, 0.90, 3, 0.06)),
    dict(d=2.6, sub="공룡 이야기는\n끝난 게 아니었습니다.", shot=("museum", (0.5, 4.0, 2.0), -80, 4, 6.5, 26, 0.92, -3, 0.04)),
    dict(d=2.7, sub="지금 공룡을 보려면\n창밖을 보면 됩니다.", shot=("museum", (0.0, 8.0, 2.8), -90, 0, 6.0, 26, 0.90, 3, 0.0)),
    dict(d=3.1, sub="공룡은 사라진 게 아니라\n날아간 겁니다.", shot=("museum", (0.0, 8.0, 2.8), -90, 0, 6.0, 26, 0.95, 2, 0.0)),
    dict(d=2.6, sub="댓글로 알려 주세요.", shot=("museum", (0.0, 3.5, 1.0), -90, 2, 5.5, 28, 0.90, 0, 0.05)),
    dict(d=3.6, sub="네모난 지구에서도\n살 수 있을까요?", shot=("teaser", (0.0, 0.0, 0.0), -90, 10, 9.0, 26, 0.90, 3, 0.0)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="6,600만 년 전", label="공룡을 끝낸 소행성", big="충돌 각도 60°", label_color="blue", big_color="red"),
    dict(at="pass", badge="만약", title="비껴갔다면 살아남을 종", big="약 75%", big_color="green"),
    dict(at="era", badge="만약", title="공룡 시대", big="1억 6천만 년+", big_color="orange"),
    dict(at="river", badge="오늘", title="한강변을 걷는 {green}공룡{/}?"),
    dict(at="bars", badge="오늘", title="티라노는 스테고보다", big="우리와 더 가깝다", big_color="yellow"),
    dict(at="mark", badge="연표", title="인류의 역사", big="약 30만 년", big_color="cyan"),
    dict(at="model", badge="상상", title="1982년의 가설", big="사람 닮은 공룡", big_color="green"),
    dict(at="twist", badge="반전", title="공룡은 사라지지 않았다", big="새 약 1만 1천 종", big_color="green"),
    dict(at="burnt", badge="반전", title="살아남은 건", big="땅에 살던 작은 새", big_color="cyan"),
    dict(at="selfie", badge="지금", title="공룡을 보려면 {cyan}창밖을{/}"),
    dict(at="ask", badge="지금", title="오늘 본 새는\n{cyan}어떤 공룡{/}을 닮았나요?", title_size=70),
    dict(at="teaser", badge="다음 편", title="내일 낮 12시\n{cyan}지구가 정육면체라면?{/}", title_size=66),
]
TWIST = LN["twist"]  # '그런데 공룡은 사실 사라지지 않았어요' 줄 — 음악이 단조 느낌으로 바뀌는 곳
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
GRADE = {"exposure": 0.92, "bloom": 0.12, "bloom_thr": 1.4, "vignette": 0.16}
T_BURST = 0.95        # 훅: 불덩이가 번쩍하는 때(줄 시작 후 초)
HK_REF = 0.4          # 훅 하늘 물체의 기준 카메라 시점(τ)
META = {"id": "ep45", "title": "만약에 공룡이 멸종하지 않았다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"style": "epic", "key": "G", "mode": "lydian", "bpm": 96, "seed": 451, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, [[T_BURST - 0.6, "rumble", 0.6, 1.8], [T_BURST, "thud", 0.8]])}}


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



def _shake_spec(i):
    """줄 i의 흔들림 [(시작 τ, 길이, 이동 세기 m, 각도 세기 도, 진동수 Hz, 종류)]. 'hold' 거의 일정, 'hit' 점점 잦아듦."""
    if i == LN["hook"]:
        return [(0.0, 99.0, 0.03, 0.0, 15.0, "hold"), (T_BURST, 0.8, 0.07, 0.8, 13.0, "hit")]
    if i == LN["angle"]:
        return [(1.9, 0.6, 0.04, 0.4, 13.0, "hit")]
    if i == LN["shake"]:
        return [(1.25, 0.7, 0.05, 0.5, 13.0, "hit")]
    if i == LN["feed"]:
        return [(1.0, 0.8, 0.05, 0.6, 13.0, "hit")]
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


R_FAR = 120.0                  # 하늘 물체를 두는 거리(m): 카메라 위치 + 방향 x R_FAR (한강 건너편 도시(150m~)보다 앞이라 도시에 가려지지 않고, 카메라가 몇 m 움직여도 시차가 거의 없음)


def sky_dir(i, tref, nx, ny):
    """줄 i의 τ=tref 기준 카메라에서 화면 (nx, ny)에 보이는 하늘 방향(월드 단위벡터)."""
    return screen_dir(ref_cam(i, tref), nx, ny, True)


def sky_orb(OR, cam, i, tref, nx, ny, dfrac, col, rm=1.0):
    """하늘(기준 카메라 방향)에 발광 구: dfrac = 기준 카메라 화면 높이에 대한 지름 비율. rm > 1이면 그만큼 더 뒤에 놓음(겹친 빛 층 순서)."""
    rc = ref_cam(i, tref)
    OR.orbw(cam["loc"] + sky_dir(i, tref, nx, ny) * R_FAR * rm, dfrac * R_FAR * rm * 24.0 / rc["lens"], col)


def sky_box(G, cam, i, tref, nx, ny, w, h, col):
    """하늘에 납작한 정사각 발광 점 (w·h = 기준 카메라 화면 높이에 대한 비율, 카메라를 향함)."""
    rc = ref_cam(i, tref)
    s = R_FAR * 24.0 / rc["lens"]
    G.cw(cam["loc"] + sky_dir(i, tref, nx, ny) * R_FAR, (2.0, w * s, h * s), col, rot_cam(rc))



def fire_trail(G, OR, cam, i, tref, a, b, f, dh, tail=12, smoke=26, fade=1.0, head=True):
    """하늘의 불덩이와 긴 꼬리. 경로 a→b (기준 카메라 화면 좌표), f = 머리의 진행도(0 = a, 1 = b), dh = 머리 지름(화면 높이 비율).
    머리 = 하얀 속불 + 주황 겉불, 꼬리 = 뒤로 갈수록 작고 붉어지는 발광 구, 그 뒤 = 회색 연기 구. fade < 1이면 꼬리·연기가 가늘어짐(사라지는 중)."""
    (ax, ay), (bx, by) = a, b
    sj = 0.034 / math.hypot((bx - ax) * 0.28125, (by - ay) * 0.5)             # 꼬리 한 칸의 진행도 간격 (화면 높이 0.034)
    px, py = -(by - ay) * 0.5, (bx - ax) * 0.28125                              # 경로에 수직인 방향(출렁임용)
    pn = math.hypot(px, py) or 1.0

    def P(ff, wob=0.0):
        return (ax + (bx - ax) * ff + wob * px / pn / 0.28125, ay + (by - ay) * ff + wob * py / pn / 0.5)
    if head:
        x, y = P(f)
        sky_orb(OR, cam, i, tref, x, y, dh * 2.0, (2.6, 1.0, 0.28), 1.03)
        sky_orb(OR, cam, i, tref, x, y, dh, (7.0, 5.6, 2.6))
    for j in range(1, tail + 1):
        q = j / tail
        x, y = P(f - sj * j, 0.004 * math.sin(j * 1.3))
        col = tuple(lerp(c0, c1, q) * fade for c0, c1 in zip((5.5, 3.2, 1.0), (2.4, 0.8, 0.2)))
        sky_orb(OR, cam, i, tref, x, y, dh * (0.85 - 0.5 * q) * fade, col)
    for j in range(smoke):
        q = j / max(smoke - 1, 1)
        x, y = P(f - sj * (tail + 1.6 * (j + 1)), 0.007 * math.sin(j * 1.7 + 0.5))
        g = (0.88 - 0.3 * q) * (0.35 + 0.65 * fade)
        sky_orb(OR, cam, i, tref, x, y, dh * (0.55 + 0.05 * j) * (0.4 + 0.6 * fade), (g, g, g * 1.04))


def blast(OR, cam, i, tref, c, s, scale=1.0):
    """공중 폭발: 번쩍 커지는 하얀 속불·주황 겉불(s초 사이 식으며 작아짐) + 남는 회갈색 연기 덩어리. s = 폭발한 뒤 초."""
    if s < 0:
        return
    d = (0.12 + 0.55 * ramp(s, 0.0, 0.30)) * scale
    vis = 1.0 - ramp(s, 0.75, 1.9)
    col = tuple(lerp(a_, b_, ramp(s, 0.05, 0.9)) for a_, b_ in zip((7.5, 6.2, 3.8), (3.4, 1.3, 0.4)))
    if vis > 0.01:
        sky_orb(OR, cam, i, tref, c[0], c[1], d * 1.35 * vis, (2.4, 0.9, 0.25), 1.04)
        sky_orb(OR, cam, i, tref, c[0], c[1], d * vis, col)
    g = ramp(s, 0.35, 2.4)
    for n in range(8):
        a = 0.8 + n * 0.79
        r = (0.04 + 0.16 * g) * (0.6 + 0.8 * _h(n + 40))
        gray = 0.56 - 0.12 * g
        sky_orb(OR, cam, i, tref, c[0] + r * math.cos(a) / 0.28125 * 0.9, c[1] + r * math.sin(a) / 0.5 * 0.9,
                (0.07 + 0.10 * g) * (0.7 + 0.6 * _h(n + 50)) * scale, (gray, gray * 0.92, gray * 0.88), 0.98)


def ring_wave(G, cam, i, tref, c, s, rm=1.0, br=1.0, n=72, rmax=1.9, speed=1.0):
    """충격파 고리: 폭발 지점 c(화면 좌표)에서 s초 동안 빠르게 퍼지는 가는 발광 고리 (하늘 방향에 놓은 상자 n개가 이어짐).
    rm = 반지름 배율, br = 밝기 배율, speed = 퍼지는 빠르기 배율. 밝기는 화면 밖으로 나갈 즈음 꺼짐."""
    s = s * speed
    if s <= 0.0:
        return
    rh = rmax * rm * (1.0 - math.exp(-2.6 * s))
    thick = 0.016 * (1.0 - ramp(s, 0.35, 0.9)) + 0.004
    k = br * (1.0 - ramp(s, 0.45, 0.95))
    if k <= 0.01:
        return
    col = (2.6 * k, 2.2 * k, 1.6 * k)
    rc = ref_cam(i, tref)
    sc = R_FAR * 24.0 / rc["lens"]
    sp = [(c[0] + rh * math.cos(2 * math.pi * q / n) / 0.28125, c[1] + rh * math.sin(2 * math.pi * q / n) / 0.5) for q in range(n + 1)]
    pts = [cam["loc"] + sky_dir(i, tref, x, y) * R_FAR for x, y in sp]
    for q in range(n):
        if all(abs(p[0]) > 1.6 or abs(p[1]) > 1.4 for p in (sp[q], sp[q + 1])):
            continue
        d = pts[q + 1] - pts[q]
        L = float(np.linalg.norm(d))
        G.cw((pts[q] + pts[q + 1]) / 2, (L * 1.06, thick * sc, thick * sc), col, rot_to(d / L))



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

EX_SH = [(0.85, 0.30, 0.28), (0.95, 0.80, 0.35), (0.35, 0.65, 0.40), (0.45, 0.75, 0.85), (0.80, 0.55, 0.65), (0.25, 0.45, 0.80),
         (0.92, 0.92, 0.90), (0.40, 0.55, 0.50), (0.88, 0.58, 0.30)]      # 시민 (지후의 보라는 피함)
JH_SH, JH_PA = (0.58, 0.32, 0.80), (0.15, 0.18, 0.30)      # 지후: 보라 후드 · 짧은 머리 · 남색 바지
CO_SH, CO_PA = (0.93, 0.93, 0.91), (0.22, 0.24, 0.30)      # 연구원: 흰 가운 (extra='coat')

DIG.update({"T": ["###", ".#.", ".#.", ".#.", ".#."], "N": ["###", "#.#", "#.#", "#.#", "#.#"], "c": ["###", "#..", "#..", "#..", "###"]})


def wdig(G, rows, cx, y, cz, cell, col, k=1.0):
    """세트에 서 있는 도트 글자 (−y쪽을 보는 면, 가운데 맞춤): 칸 하나 = 발광 상자."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        G.b((cx + ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, y, cz + (h / 2.0 - r - 0.5) * cell * k),
            (((c1 - c + 1) - 0.06) * cell * k, 0.03, cell * 0.94 * k), col)



# ───────────────────────── 색 · 도트 그림 · 공룡 ─────────────────────────
DIG.update({"°": ["##.", "##.", "...", "...", "..."]})
CRET_G = (0.27, 0.46, 0.22)
GRASS = (0.30, 0.52, 0.24)
SKINC = X.SKIN
SAU_C, SAU_L = (0.50, 0.60, 0.40), (0.42, 0.50, 0.34)
TRI_C, TRI_L = (0.62, 0.48, 0.36), (0.52, 0.40, 0.30)
RAP_C, RAP_L = (0.52, 0.36, 0.30), (0.44, 0.30, 0.26)
NEI_C, NEI_L = (0.30, 0.66, 0.36), (0.24, 0.54, 0.30)
BONE = (0.90, 0.86, 0.74)
HORN = (0.92, 0.88, 0.78)
PIG_C, PIG_N, SPA_C = (0.52, 0.54, 0.60), (0.30, 0.48, 0.42), (0.55, 0.40, 0.26)
CHAR = (0.16, 0.12, 0.10)
BEAK = (0.92, 0.62, 0.20)

SAURO = ["..........##..", ".........####.", "..........##..", ".........##...", "...#####.##...", "..##########..", ".############.",
         "..##..##..##..", "..##..##..##.."]
TREX = ["......####..", ".....######.", ".....#######", ".....#####..", "#...######..", "##.#######..", ".########...", "..###.###...", "..##...##..."]
PERSON = ["..#..", ".###.", "#.#.#", "..#..", ".#.#."]
BIRD = ["....#..", "..####.", "#######", ".##.##.", "..#..#."]


def outline(rows):
    """도트 그림에서 가장자리 칸만 남긴 그림(윤곽)."""
    h, w = len(rows), len(rows[0])

    def on(r, c):
        return 0 <= r < h and 0 <= c < w and rows[r][c] == "#"
    return ["".join("#" if on(r, c) and not (on(r - 1, c) and on(r + 1, c) and on(r, c - 1) and on(r, c + 1)) else "." for c in range(w))
            for r in range(h)]


TREX_OUT = outline(TREX)


def _yw(x, y, yaw):
    a = math.radians(yaw)
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def dp(F, o, yaw, s, lc, size, col, tilt=0.0, roll=0.0):
    """공룡 몸 부품: o = 공룡 발밑 자리(세트), lc = 몸 기준 가운데(앞 +x), s = 배율. tilt>0이면 앞쪽이 내려감."""
    dx, dy = _yw(lc[0] * s, lc[1] * s, yaw)
    F.c((o[0] + dx, o[1] + dy, o[2] + lc[2] * s), (size[0] * s, size[1] * s, size[2] * s), col, (roll, tilt, math.radians(yaw)))


def dpw(o, yaw, s, p):
    dx, dy = _yw(p[0] * s, p[1] * s, yaw)
    return np.array((o[0] + dx, o[1] + dy, o[2] + p[2] * s))


def _lift(ph, k, amp):
    return 0.0 if ph is None else amp * max(0.0, math.sin(ph + k * 1.6))


def sauropod(F, o, yaw, s, col, lcol, ph=None, head=None, up=1.0, look=0.0):
    """목 긴 공룡: 몸·다리 넷·꼬리·곡선 목(상자 여섯)·머리. head = 머리 자리(세트 좌표)를 주면 목이 거기까지 휨. look>0이면 머리를 들어 하늘을 봄."""
    dp(F, o, yaw, s, (0, 0, 2.0), (3.4, 1.5, 1.2), col)
    for k, (lx, ly) in enumerate(((1.1, 0.5), (1.1, -0.5), (-1.1, 0.5), (-1.1, -0.5))):
        dp(F, o, yaw, s, (lx, ly, 0.7 + _lift(ph, k, 0.22)), (0.55, 0.5, 1.4), lcol)
    dp(F, o, yaw, s, (-2.5, 0, 2.0), (2.0, 0.8, 0.7), col, tilt=-0.15)
    dp(F, o, yaw, s, (-3.9, 0, 1.55), (1.1, 0.5, 0.45), col, tilt=-0.35)
    p0 = dpw(o, yaw, s, (1.5, 0, 2.4))
    p2 = np.asarray(head, float) if head is not None else dpw(o, yaw, s, (3.3, 0, 2.4 + 3.0 * up))
    p1 = np.array((lerp(p0[0], p2[0], 0.25), lerp(p0[1], p2[1], 0.25), lerp(p0[2], p2[2], 0.8)))
    pts = [(1 - q) ** 2 * p0 + 2 * (1 - q) * q * p1 + q * q * p2 for q in np.linspace(0.0, 1.0, 7)]
    for k in range(6):
        d = pts[k + 1] - pts[k]
        L = float(np.linalg.norm(d))
        w = lerp(0.62, 0.36, k / 5.0) * s
        F.c((pts[k] + pts[k + 1]) / 2, (L * 1.1, w, w), col, rot_to(d / L))
    d = pts[6] - pts[5]
    hd = np.array((d[0], d[1], 0.0))
    hd = hd / (np.linalg.norm(hd) or 1.0)
    pit = 0.15 + 0.8 * look
    dh = hd * math.cos(pit) + np.array((0.0, 0.0, math.sin(pit)))
    F.c(p2 + dh * 0.4 * s, (0.95 * s, 0.5 * s, 0.42 * s), col, rot_to(dh))


def trice(F, o, yaw, s, ph=None, look=0.0, col=TRI_C, lcol=TRI_L):
    """뿔 달린 공룡: 몸·다리 넷·꼬리·머리·주름 방패·뿔 셋."""
    dp(F, o, yaw, s, (0, 0, 1.1), (2.6, 1.4, 1.1), col)
    for k, (lx, ly) in enumerate(((0.9, 0.5), (0.9, -0.5), (-0.9, 0.5), (-0.9, -0.5))):
        dp(F, o, yaw, s, (lx, ly, 0.35 + _lift(ph, k, 0.15)), (0.4, 0.4, 0.7), lcol)
    dp(F, o, yaw, s, (-1.9, 0, 1.0), (1.4, 0.5, 0.5), col, tilt=-0.2)
    hz = 1.2 + 0.5 * look
    dp(F, o, yaw, s, (1.8, 0, hz), (1.1, 0.8, 0.8), col, tilt=-0.5 * look)
    dp(F, o, yaw, s, (1.3, 0, hz + 0.65), (0.25, 1.5, 1.2), lcol, tilt=-0.3 - 0.35 * look)
    for ly in (-0.3, 0.3):
        dp(F, o, yaw, s, (2.5, ly, hz + 0.35), (0.8, 0.12, 0.12), HORN, tilt=-0.4 - 0.4 * look)
    dp(F, o, yaw, s, (2.4, 0, hz - 0.05), (0.4, 0.14, 0.14), HORN)


def biped(F, o, yaw, s, col=RAP_C, lcol=RAP_L, ph=None, arm=0.0, bob=0.0):
    """작은 이족 공룡: 몸·두 다리와 발·꼬리·목·머리·앞팔 둘(arm 0~1로 오른팔이 앞으로 길어짐)."""
    dp(F, o, yaw, s, (0, 0, 1.55), (1.8, 0.9, 1.0), col, tilt=-0.3)
    for k, ly in enumerate((0.32, -0.32)):
        lf = 0.0 if ph is None else 0.2 * max(0.0, math.sin(ph + k * math.pi))
        dp(F, o, yaw, s, (0.1, ly, 0.65 + lf), (0.45, 0.4, 1.3), lcol)
        dp(F, o, yaw, s, (0.35, ly, 0.08 + lf), (0.7, 0.4, 0.16), lcol)
    dp(F, o, yaw, s, (-1.5, 0, 1.35), (1.8, 0.5, 0.45), col, tilt=-0.25)
    dp(F, o, yaw, s, (1.0, 0, 2.3), (0.5, 0.5, 1.0), col)
    dp(F, o, yaw, s, (1.55, 0, 2.75), (1.1, 0.6, 0.55), col)
    L = 0.4 + 0.7 * arm
    dp(F, o, yaw, s, (0.95 + L / 2, -0.45, 1.55 + bob), (L, 0.15, 0.15), col)
    dp(F, o, yaw, s, (1.1, 0.45, 1.5), (0.4, 0.15, 0.15), col)


def bird(F, o, yaw, s, col, flap=None, peck=0.0):
    """새: 몸·머리(쪼기)·부리·꼬리, 걸을 땐 다리 둘, 날 땐 날개 둘(flap 위상)."""
    dp(F, o, yaw, s, (0, 0, 0.3), (0.55, 0.34, 0.3), col)
    dp(F, o, yaw, s, (0.3, 0, 0.52 - 0.25 * peck), (0.22, 0.2, 0.2), col, tilt=0.9 * peck)
    dp(F, o, yaw, s, (0.46, 0, 0.5 - 0.3 * peck), (0.12, 0.07, 0.07), BEAK)
    dp(F, o, yaw, s, (-0.38, 0, 0.3), (0.34, 0.2, 0.06), col, tilt=-0.2)
    if flap is None:
        for ly in (-0.07, 0.07):
            dp(F, o, yaw, s, (0.0, ly, 0.1), (0.05, 0.05, 0.2), BEAK)
    else:
        for sg in (-1, 1):
            a = math.sin(flap)
            dp(F, o, yaw, s, (0.0, sg * 0.36, 0.36 + 0.1 * a), (0.3, 0.55, 0.05), col, roll=sg * 0.9 * a)


def mouse(F, o, yaw, s=1.0, col=(0.45, 0.38, 0.32)):
    dp(F, o, yaw, s, (0, 0, 0.13), (0.45, 0.22, 0.2), col)
    dp(F, o, yaw, s, (0.28, 0, 0.15), (0.2, 0.16, 0.16), col)
    dp(F, o, yaw, s, (-0.42, 0, 0.1), (0.45, 0.05, 0.05), (0.8, 0.6, 0.55))


def skeleton(F, o, s, nod, yaw=0.0):
    """뼈 색 상자로 쌓은 이족 골격(정면에서 옆모습). nod 0~1: 두개골이 고개를 숙임."""
    for k in range(13):
        dp(F, o, yaw, s, (-3.4 + 0.42 * k, 0, 2.4 + 0.5 * min(k, 9) / 9.0), (0.4, 0.3, 0.3), BONE)
    for k in range(4, 10):
        for ly in (-0.3, 0.3):
            dp(F, o, yaw, s, (-3.4 + 0.42 * k, ly, 1.95), (0.12, 0.1, 1.2), BONE)
    for ly in (-0.5, 0.5):
        dp(F, o, yaw, s, (-0.2, ly, 1.6), (0.35, 0.3, 1.3), BONE)
        dp(F, o, yaw, s, (0.1, ly, 0.55), (0.3, 0.26, 1.1), BONE)
        dp(F, o, yaw, s, (0.45, ly, 0.08), (0.8, 0.3, 0.16), BONE)
    for q in range(4):
        dp(F, o, yaw, s, (0.9 + 0.25 * q, 0, 3.0 + 0.28 * q - 0.12 * nod * q), (0.35, 0.3, 0.3), BONE)
    dp(F, o, yaw, s, (1.95, 0, 4.0 - 0.5 * nod), (1.4, 0.6, 0.7), BONE, tilt=0.4 * nod)
    dp(F, o, yaw, s, (1.9, 0, 3.65 - 0.5 * nod), (1.2, 0.45, 0.2), BONE, tilt=0.4 * nod)


# ───────────────────────── 세트 ─────────────────────────
def _cret(v):
    v.floor(-70, 70, -25, 125, CRET_G, 2.5)
    rs = v.rs
    for k in range(14):                                       # 먼 언덕 (y를 조금씩 비껴 놓음)
        x0 = -130 + 22 * k
        h = float(rs.uniform(4, 11))
        v.box(x0, x0 + 26, 130 + 3.1 * (k % 4), 152 + 3.1 * (k % 4), 0, h, (0.26 + 0.03 * (k % 3), 0.42, 0.32 + 0.02 * (k % 2)), jit=0.05)
    for z0, z1, w, d, y0 in ((0.0, 5.0, 14.0, 10.0, 92.0), (5.0, 9.0, 10.0, 7.0, 95.5), (9.0, 12.5, 6.0, 4.5, 98.5), (12.5, 14.5, 3.0, 2.5, 100.8)):
        v.box(-w, w, y0, y0 + 2 * d, z0, z1, (0.40, 0.32, 0.30), jit=0.05)            # 화산 층
    v.box(-2.2, 2.2, 100.6, 103.4, 14.5, 14.9, (3.0, 1.2, 0.3), jit=0, glow=True)     # 분화구 용암
    v.box(-0.5, 0.5, 91.96, 91.99, 0.2, 5.0, (2.4, 0.9, 0.2), jit=0, glow=True)      # 흘러내리는 용암
    v.box(-5, 6, 99.0, 108.0, 15.0, 19.0, (0.45, 0.43, 0.43), jit=0.04)               # 연기
    for k in range(150):                                      # 고사리
        x, y = float(rs.uniform(-45, 45)), float(rs.uniform(1, 70))
        if y < 6 and abs(x) < 8:
            continue
        h = float(rs.uniform(0.4, 1.2))
        g = float(rs.uniform(0.85, 1.15))
        v.box(x - 0.3, x + 0.3, y - 0.3, y + 0.3, 0, h, (0.18 * g, 0.42 * g, 0.20 * g), jit=0.08)
    for k in range(12):                                       # 소철 나무
        x = (-1) ** k * float(rs.uniform(12, 42))
        y = float(rs.uniform(16, 62))
        h = float(rs.uniform(5, 9))
        v.box(x - 0.25, x + 0.25, y - 0.25, y + 0.25, 0, h, (0.38, 0.28, 0.18), jit=0.05)
        v.box(x - 1.7, x + 1.7, y - 1.7, y + 1.7, h, h + 0.35, (0.16, 0.40, 0.18), jit=0.05)
        v.box(x - 1.2, x + 1.2, y - 1.2, y + 1.2, h + 0.35, h + 0.65, (0.22, 0.47, 0.22), jit=0.05)


def _river(v):
    v.floor(-60, 60, -25, 4, (0.74, 0.72, 0.66), 2.0)
    v.floor(-60, 60, 4, 12, GRASS, 2.0)
    v.floor(-60, 60, 12, 46, (0.07, 0.24, 0.42), 2.0, z=-0.25)
    v.box(-60, 60, 11.9, 12.0, -0.25, -0.01, (0.5, 0.5, 0.45), jit=0.03)
    v.floor(-60, 60, 46, 70, GRASS, 2.0)
    v.box(-60, 60, 24, 30, 5.0, 5.6, (0.62, 0.62, 0.65))                       # 다리 상판
    for x in range(-54, 60, 12):
        v.box(x - 0.6, x + 0.6, 25.5, 28.5, -0.25, 5.0, (0.5, 0.5, 0.53))
    v.box(-60, 60, 23.85, 24.0, 5.6, 6.4, (0.40, 0.55, 0.75))
    for k in range(15):                                       # 건너편 건물 (y를 비껴 놓음)
        x0 = -72 + 9 * k
        v.box(x0, x0 + 7.5, 74 + 2.7 * (k % 4), 86 + 2.7 * (k % 4), 0, 9 + 4.5 * ((k * 7) % 5), (0.70 - 0.03 * (k % 3), 0.72, 0.76 - 0.02 * (k % 4)), jit=0.04)
    for x in range(-24, 25, 8):                                # 산책길 가로등
        v.box(x - 0.1, x + 0.1, 3.0, 3.2, 0, 4.0, (0.30, 0.32, 0.36))
        v.box(x - 0.25, x + 0.25, 2.9, 3.3, 4.0, 4.3, (3.0, 2.7, 1.8), jit=0, glow=True)


def _cross(v):
    v.floor(-40, 40, -6, 6, (0.30, 0.30, 0.33), 2.0)
    v.box(-40, 40, -30, -6, 0.0, 0.15, (0.74, 0.70, 0.64), jit=0.03)
    v.box(-40, 40, 6, 30, 0.0, 0.15, (0.74, 0.70, 0.64), jit=0.03)
    for k in range(-5, 5):                                    # 횡단보도
        v.box(k + 0.2, k + 0.75, -5.9, 5.9, 0.0, 0.012, (0.92, 0.92, 0.90), jit=0)
    v.box(2.1, 2.3, -7.2, -7.0, 0.15, 4.4, (0.35, 0.37, 0.42))                  # 신호등 기둥
    v.box(1.95, 2.45, -7.4, -6.9, 3.9, 4.7, (0.18, 0.19, 0.22))
    v.box(2.05, 2.35, -7.43, -7.4, 4.25, 4.55, (3.0, 0.5, 0.35), jit=0, glow=True)
    v.box(2.1, 2.3, -7.3, -7.2, 3.0, 3.3, (0.62, 0.22, 0.20), jit=0)            # 버튼 상자
    for x0, w, h, c in ((-30, 24, 9.0, (0.78, 0.62, 0.50)), (4, 14, 6.5, (0.70, 0.72, 0.60)), (-34, 6, 14.0, (0.66, 0.68, 0.74))):
        v.box(x0, x0 + w, 34 + (x0 % 3), 46 + (x0 % 3), 0.15, h, c)
    for x in (-12, -6, 8, 14):
        X.tree(v, x, -20, 3.4)


def _ruler(v):
    v.floor(-16, 16, -12, 8, (0.58, 0.50, 0.40), 1.0, "wood")
    v.wall((-16, 8), (16, 8), 0, 6, (0.18, 0.30, 0.40), 0.5, face=-1)
    v.wall((-16, -12), (-16, 8), 0, 6, (0.20, 0.32, 0.42), 0.5, face=-1)
    v.wall((16, -12), (16, 8), 0, 6, (0.20, 0.32, 0.42), 0.5, face=1)
    v.box(-10.5, 10.5, -0.3, 0.3, 0.0, 0.03, (0.95, 0.88, 0.55), jit=0)          # 줄자 (21m)
    for k in range(-10, 11):
        v.box(k - 0.02, k + 0.02, -0.3, 0.3, 0.03, 0.045, (0.20, 0.20, 0.20), jit=0)
    for k, x in enumerate((-9.0, 0.0, 9.0)):
        v.light(x, 0.0, 4.5, 200, (1.0, 0.95, 0.85), 1.0, "ep45_r%d" % k)


MUS_W = (0.82, 0.78, 0.70)


def _museum(v):
    v.floor(-10, 10, -10, 8, (0.80, 0.74, 0.64), 1.0, "check")
    v.wall((-10, 8), (-3.2, 8), 0, 6, MUS_W, 0.5, face=-1)
    v.wall((3.2, 8), (10, 8), 0, 6, MUS_W, 0.5, face=-1)
    v.wall((-3.2, 8), (3.2, 8), 0, 1.4, MUS_W, 0.5, face=-1)
    v.wall((-3.2, 8), (3.2, 8), 4.2, 6, MUS_W, 0.5, face=-1)
    v.wall((-10, -10), (-10, 8), 0, 6, MUS_W, 0.5, face=-1)
    v.wall((10, -10), (10, 8), 0, 6, MUS_W, 0.5, face=1)
    fr = (0.95, 0.95, 0.93)
    v.box(-3.3, -3.2, 7.88, 8.02, 1.3, 4.3, fr, jit=0)                                # 창틀
    v.box(3.2, 3.3, 7.88, 8.02, 1.3, 4.3, fr, jit=0)
    v.box(-3.2, 3.2, 7.88, 8.02, 4.2, 4.3, fr, jit=0)
    v.box(-3.2, 3.2, 7.88, 8.02, 1.3, 1.4, fr, jit=0)
    for mx in (-1.6, 1.6):
        v.box(mx - 0.05, mx + 0.05, 7.9, 8.0, 1.4, 4.2, fr, jit=0)
    v.box(-3.4, 3.4, 7.7, 9.3, 1.40, 1.48, (0.82, 0.80, 0.76), jit=0.02)            # 창밖 턱
    v.box(-2.0, 0.6, 2.0, 4.4, 0.0, 0.25, (0.45, 0.40, 0.35))                       # 초록 이웃 받침
    v.box(-2.6, 3.8, 4.6, 7.4, 0.0, 0.30, (0.45, 0.40, 0.35))                       # 화석 받침
    for k, (x, e) in enumerate(((0.0, 220), (-6.0, 120), (6.0, 120))):
        v.light(x, 3.0, 5.4, e, (1.0, 0.95, 0.85), 1.0, "ep45_m%d" % k)


def _park(v):
    v.floor(-30, 30, -20, 40, GRASS, 2.0)
    v.box(-3, 3, -20, 40, 0.0, 0.03, (0.78, 0.72, 0.60), jit=0.03)
    v.box(-6.0, -4.2, 6.8, 7.3, 0.4, 0.5, (0.62, 0.42, 0.25))
    v.box(-6.0, -4.2, 7.2, 7.3, 0.5, 1.0, (0.62, 0.42, 0.25))
    for sx in (-5.9, -4.3):
        v.box(sx - 0.05, sx + 0.05, 6.9, 7.1, 0.0, 0.4, (0.30, 0.30, 0.34))
    for x, y in ((-9, 10), (8, 12), (-12, 22), (12, 26), (-8, -12), (9, -13)):
        X.tree(v, x, y, 4.2)
    v.box(-20, 20, -16.0, -14.5, 0.0, 1.4, (0.20, 0.45, 0.20))
    for k in range(10):
        x0 = -48 + 10 * k
        v.box(x0, x0 + 8, 52 + 2.7 * (k % 4), 62 + 2.7 * (k % 4), 0, 8 + 4 * ((k * 5) % 4), (0.74 - 0.03 * (k % 3), 0.70, 0.66), jit=0.04)
        v.box(x0, x0 + 8, -34 - 2.7 * (k % 4), -26 - 2.7 * (k % 4), 0, 8 + 4 * ((k * 3) % 4), (0.72, 0.72 - 0.03 * (k % 3), 0.70), jit=0.04)


def _teaser(v):
    rs = v.rs
    for k in range(200):
        d = rs.normal(size=3)
        d = d / np.linalg.norm(d)
        r = float(rs.uniform(40, 60))
        s = float(rs.uniform(0.2, 0.5))
        x, y, z = d * r
        v.box(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z - s / 2, z + s / 2, ((0.95, 0.95, 1.0), (1.0, 0.9, 0.6), (0.6, 0.75, 1.0))[k % 3], jit=0, glow=True)


def _sets():
    return (("cret", _cret), ("river", _river), ("cross", _cross), ("ruler", _ruler), ("museum", _museum), ("park", _park), ("teaser", _teaser))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 1900, 600, 60, 8


def jump_h(tau, t0, period, air, h):
    """t0부터 period마다 air초 동안 포물선으로 h m 솟았다 내려옴."""
    s = ((tau - t0) % period) / air if tau >= t0 else 9.0
    return h * 4.0 * s * (1.0 - s) if s < 1.0 else 0.0


def herd(F, tau, t, look=1.0, sway=0.0):
    """백악기 군집: 뿔 공룡 둘 앞, 목 긴 공룡 둘 뒤 (서 있음). look = 하늘을 올려다보는 정도."""
    trice(F, (0.2, 7.0, 0.0), -95 + sway, 0.9, None, look)
    trice(F, (-1.4, 9.2, 0.0), -80 - sway, 0.8, None, look)
    sauropod(F, (-1.7, 14.0, 0.0), -75, 0.7, SAU_C, SAU_L, None, up=0.5, look=look)
    sauropod(F, (1.8, 13.0, 0.0), -115, 0.7, SAU_C, SAU_L, None, up=0.5, look=look)


# ── 0: 훅
FA, FB = (-0.35, 1.05), (0.40, 0.32)        # 불덩이 경로 (기준 카메라 화면 좌표, 약 60도 기울기)


def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    s = tau - T_BURST
    herd(F, tau, t, 1.0 if s < 0 else 0.5, 0.0 if s < 0 else 9.0 * math.exp(-3.0 * s) * math.sin(18.0 * s))
    if s < 0:
        k = tau / T_BURST
        fire_trail(G, OR, cam, i, HK_REF, FA, FB, 0.30 + 0.70 * k, 0.05 + 0.06 * k * k, tail=9, smoke=10)
    else:
        fire_trail(G, OR, cam, i, HK_REF, FA, FB, 1.0, 0.07, tail=9, smoke=10, fade=1.0 - ramp(s, 0.5, 2.5), head=False)
        blast(OR, cam, i, HK_REF, FB, s)
        ring_wave(G, cam, i, HK_REF, FB, s)
    if tau > 1.15:
        srows(G, cam, num_rows("60°"), -0.45, -0.12, 0.024, (3.0, 2.6, 0.6), 1.8, pop(tau - 1.15, 0.3))


# ── 1: 각도기 (숲 옆면에 놓은 기준선·점선·호)
IMP = (0.6, 0.4)
DIR = (-0.5, 0.866)


def props_angle(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    trice(F, (-2.0, 6.0, 0.0), -95, 0.55, None, 0.2)
    sauropod(F, (2.4, 8.0, 0.0), -105, 0.6, SAU_C, SAU_L, None, look=0.2)
    G.b((0.1, 0.0, IMP[1]), (4.6, 0.06, 0.06), (2.6, 2.6, 2.8))
    f = ramp(tau, 0.05, 1.0)
    for k in range(12):
        if f > k / 12.0:
            sd = 0.3 + 0.3 * k
            G.c((IMP[0] + DIR[0] * sd, 0.0, IMP[1] + DIR[1] * sd), (0.18, 0.05, 0.05), (2.8, 1.6, 0.5), rot_to((DIR[0], 0.0, DIR[1])))
    fall = ramp(tau, 0.5, 1.9)
    if fall < 1.0:
        sd = 3.6 * (1.0 - fall) + 0.15
        OR.orb((IMP[0] + DIR[0] * sd, 0.0, IMP[1] + DIR[1] * sd), 0.55, (7.0, 5.5, 2.4))
        OR.orb((IMP[0] + DIR[0] * sd, 0.1, IMP[1] + DIR[1] * sd), 0.95, (2.6, 1.0, 0.28))
        for j in range(1, 6):
            OR.orb((IMP[0] + DIR[0] * (sd + 0.35 * j), 0.1, IMP[1] + DIR[1] * (sd + 0.35 * j)), 0.45 - 0.06 * j, (2.4, 0.9, 0.25))
    else:
        s = tau - 1.9
        k = 1.0 - ramp(s, 0.25, 0.9)
        if k > 0.02:
            OR.orb((IMP[0], 0.0, IMP[1] + 0.2), (0.5 + 1.6 * ramp(s, 0.0, 0.3)) * k, (4.0, 2.4, 0.8))
    if tau > 0.9:
        for q in range(10):
            th = math.radians(120.0 + 60.0 * q / 9.0)
            sz = 0.09 * pop(tau - 0.9 - 0.04 * q, 0.2)
            G.b((IMP[0] + 1.2 * math.cos(th), 0.0, IMP[1] + 1.2 * math.sin(th)), (sz, 0.05, sz), (0.5, 2.4, 3.0))
    wdig(G, num_rows("60°"), IMP[0] - 2.0, 0.0, IMP[1] + 1.0, 0.11, (3.0, 2.6, 0.6), pop(tau - 1.2, 0.3))


# ── 2: 불덩이가 지구 옆을 스쳐 지나감
def props_pass(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    herd(F, tau, t, 0.6, 10.0 * math.sin(2 * math.pi * t / 1.4))
    f = lerp(0.05, 1.25, tau / max(dur, 1e-3))
    fire_trail(G, OR, cam, i, 0.6, (-1.1, 0.95), (1.3, 0.62), f, 0.05, tail=9, smoke=10, fade=1.0 - ramp(f, 1.0, 1.25))


# ── 3: 종 아이콘 100개 중 75개가 꺼짐
ICON_ORD = np.random.default_rng(7575).permutation(100)


def props_icons(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    herd(F, tau, t, 0.2)
    f = ramp(tau, 0.45, dur * 0.8)
    for n in range(100):
        r, c = divmod(n, 10)
        s = pop(tau - 0.003 * n, 0.2)
        if s <= 0.01:
            continue
        dark = ICON_ORD[n] < 75 and f * 75.0 > ICON_ORD[n]
        sprite(G, cam, (c - 4.5) * 0.036 / 0.28125, -0.05 + (4.5 - r) * 0.036 / 0.5, 0.028 * s, 0.028 * s,
               (0.08, 0.10, 0.08) if dark else (0.45, 2.2, 0.7), 2.0, 0.012)


# ── 4: 연표 막대에 공룡 실루엣
def props_era(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    herd(F, tau, t, 0.0)
    k = ramp(tau, 0.1, 0.9)
    sprite(G, cam, 0.0, -0.30, 0.50 * k, 0.016, (2.4, 1.6, 0.4), 1.8, 0.012)
    for j, (rows, nx, ny) in enumerate(((SAURO, -0.58, -0.05), (TREX, 0.0, -0.05), (SAURO, 0.58, -0.05), (TREX, -0.29, 0.17), (SAURO, 0.29, 0.17))):
        srows(G, cam, rows, nx, ny, 0.0105, (2.4, 2.0, 0.7), 1.8, pop(tau - 0.3 - 0.15 * j, 0.3))


# ── 5: 한강변을 걷는 목 긴 공룡
def props_river(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    sauropod(F, (-4.5 + 1.3 * tau, 11.0, 0.0), 0, 0.85, SAU_C, SAU_L, 5.0 * t, up=1.0, look=0.0)


# ── 6: 막대 둘 (84 대 66)
def props_bars(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    ruler_extras(F, G, t)
    x0, L1 = -0.20, 0.40
    L2 = L1 * 66.0 / 84.0
    k1, k2 = ramp(tau, 0.1, dur * 0.5), ramp(tau, dur * 0.4, dur * 0.8)
    sprite(G, cam, (x0 + L1 * k1 / 2) / 0.28125, 0.10, L1 * k1, 0.022, (2.6, 1.4, 0.3), 1.8, 0.012)
    sprite(G, cam, (x0 + L2 * k2 / 2) / 0.28125, -0.12, L2 * k2, 0.022, (0.4, 2.0, 2.6), 1.8, 0.012)
    srows(G, cam, SAURO, x0 / 0.28125, 0.27, 0.0105, (2.4, 2.0, 0.7), 1.8, pop(tau - 0.1, 0.3))
    srows(G, cam, TREX, (x0 + L1) / 0.28125, 0.27, 0.0105, (2.4, 2.0, 0.7), 1.8, pop(tau - 0.5, 0.3))
    srows(G, cam, TREX, x0 / 0.28125, 0.05, 0.0105, (2.4, 2.0, 0.7), 1.8, pop(tau - dur * 0.4, 0.3))
    srows(G, cam, PERSON, (x0 + L2) / 0.28125, 0.05, 0.0105, (3.0, 2.6, 0.5), 1.8, pop(tau - dur * 0.75, 0.3))
    srows(G, cam, num_rows("84"), (x0 + L1 / 2) / 0.28125, 0.19, 0.012, (3.0, 2.2, 0.5), 1.8, pop(tau - 0.7, 0.3))
    srows(G, cam, num_rows("66"), (x0 + L2 / 2) / 0.28125, -0.04, 0.012, (0.5, 2.6, 3.0), 1.8, pop(tau - dur * 0.65, 0.3))


# ── 7: 신호등 버튼은 공룡 목 높이
def props_cross(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    hd = np.array((3.3, -7.0, 3.5 + 0.15 * math.sin(2 * math.pi * t / 1.3)))
    sauropod(F, (5.6, -2.4, 0.0), 200, 1.0, SAU_C, SAU_L, None, head=hd)
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t / 0.6)
    G.b((2.2, -7.36, 3.15), (0.14, 0.06, 0.14), (3.0 * p + 0.3, 0.9 * p, 0.2))


# ── 8·9: 줄자 끝의 사람 표지
def ruler_extras(F, G, t):
    p = 0.6 + 0.4 * math.sin(2 * math.pi * t / 0.5)
    G.b((9.96, 0.0, 0.05), (0.06, 0.06, 0.06), (3.0 * p, 2.4 * p, 0.5 * p))
    G.b((9.96, 0.0, 0.62), (0.012, 0.012, 1.0), (1.2, 1.0, 0.3))
    sauropod(F, (-10.0, -1.2, 0.0), 0, 0.25, SAU_C, SAU_L)
    biped(F, (1.2, -1.2, 0.0), 0, 0.3, RAP_C, RAP_L)


def props_mark(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    ruler_extras(F, G, t)
    for k in range(9):
        F.b((9.55 + 0.1 * k, 0.0, 0.037), (0.012, 0.5, 0.012), (0.20, 0.20, 0.20))


def props_tape(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    ruler_extras(F, G, t)


# ── 10: 공룡 발밑 작은 포유류
def props_mice(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    F.b((-1.15, 3.4, 1.75), (0.9, 0.9, 3.5), SAU_L)
    F.b((1.15, 3.0, 1.75), (0.9, 0.9, 3.5), SAU_C)
    for k in range(6):
        ph = (0.35 * t + k * 0.17) % 1.0
        mouse(F, (1.8 - 3.6 * ph, 2.2 + 0.4 * (k % 3), 0.03 * abs(math.sin(2 * math.pi * (t * 3.0 + k)))), 180, 1.0)


# ── 11·12: 박물관 모형과 악수
def props_model(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    biped(F, (-0.9, 3.2, 0.25), -70, 0.6, NEI_C, NEI_L)
    F.b((0.0, 1.8, 0.45), (1.6, 0.2, 0.9), (0.20, 0.20, 0.26))
    wdig(G, num_rows("1982"), 0.0, 1.58, 0.55, 0.09, (3.0, 2.8, 2.0), pop(tau - 0.2, 0.3))


def props_shake(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    arm = ramp(tau, 0.2, 1.0)
    bob = 0.07 * math.sin(2 * math.pi * t * 3.0) * ramp(tau, 1.0, 1.2)
    biped(F, (-0.7, 3.2, 0.25), 0, 0.6, NEI_C, NEI_L, None, arm, bob)


# ── 13: 반전 — 창밖 새 위에 공룡 윤곽
def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    bird(F, (0.0, 9.0, 1.48), -90, 1.8, PIG_C)
    wdig(G, TREX_OUT, 0.0, 8.5, 2.45, 0.2, (0.4, 2.0, 2.4), pop(tau - 0.5, 0.35))


# ── 14: 공원 비둘기·참새, 뼈 윤곽
BIRDS14 = [(-0.9, 5.0, 0, 0.0), (-0.3, 4.0, 0, 0.3), (0.4, 5.2, 0, 0.6), (0.95, 3.9, 0, 0.1), (0.1, 6.0, 0, 0.8),
           (-0.7, 3.0, 1, 0.5), (0.55, 3.0, 1, 0.2), (-0.1, 2.5, 1, 0.9)]


def props_birds(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for n, (x, y, kind, ph) in enumerate(BIRDS14):
        hop = 0.06 * abs(math.sin(2 * math.pi * (t * 1.8 + ph)))
        peck = max(0.0, math.sin(2 * math.pi * (t * 1.2 + ph))) ** 4
        bird(F, (x + 0.15 * math.sin(2 * math.pi * (t * 0.5 + ph)), y, 0.03 + hop), -90 + 28 * math.sin(2 * math.pi * (t * 0.4 + ph)),
             1.5 if kind == 0 else 0.9, PIG_C if kind == 0 and n % 2 == 0 else (PIG_N if kind == 0 else SPA_C), None, peck)
    b = math.sin(math.pi * clamp((tau - 0.5) / 1.1)) if 0.5 < tau < 1.6 else 0.0
    if b > 0.02:                                     # 두 번째 비둘기의 뼈 윤곽이 잠깐 비침
        x, y = BIRDS14[1][0], BIRDS14[1][1]
        G.b((x, y - 0.5, 0.68), (0.04 * b, 0.8, 0.04 * b), (0.4, 2.4, 3.0))
        for q in range(4):
            G.b((x, y - 0.55 + 0.1 * q, 0.6), (0.36 * b, 0.04, 0.04 * b), (0.4, 2.4, 3.0))
        G.b((x, y - 0.95, 0.74), (0.14 * b, 0.14, 0.14 * b), (0.4, 2.4, 3.0))


# ── 15: 비둘기 떼가 몰려와 지후가 뒤로 밀림, 그림자에 공룡 실루엣
def props_feed(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for n in range(14):
        sx, sy = (n - 6.5) * 0.55, 5.5 + 0.35 * (n % 4)
        f = smooth(ramp(tau, 0.4 + 0.02 * (n % 5), 1.6))
        x, y = lerp(sx, 0.45 * (n % 3 - 1), f), lerp(sy, 2.0 + 0.2 * (n % 4), f)
        hop = 0.08 * abs(math.sin(2 * math.pi * (t * 3.5 + n * 0.31))) * (0.3 + 0.7 * f)
        bird(F, (x, y, 0.03 + hop), -90 + 12 * math.sin(n * 1.7), 1.3, PIG_C if n % 3 else PIG_N, None, 0.0)
    for k in range(8):                                # 과자 부스러기
        fl = ramp(tau, 0.2, 0.7)
        F.b((lerp(0.0, (k - 3.5) * 0.28, fl), lerp(1.4, 2.4 + 0.15 * (k % 3), fl), 1.2 * (1.0 - fl) + 0.05 + 0.5 * math.sin(math.pi * fl) * 0.4),
            (0.07, 0.07, 0.07), (0.9, 0.75, 0.4))
    sh = pop(tau - dur * 0.55, 0.4)
    if sh > 0.02:
        frows(F, TREX, (0.0, 2.5, 0.04), 0.15, (0.04, 0.04, 0.05), sh, 0.012, math.pi)


# ── 16: 불탄 숲 — 나무 위 새는 사라지고 땅 새만 남음
def props_burnt(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for n, (tx, ty) in enumerate(((-1.6, 6.0), (0.1, 6.8), (1.7, 5.8))):
        F.b((tx, ty, 1.5), (0.35, 0.35, 3.0), CHAR)
        F.c((tx + 0.5, ty, 2.4), (1.0, 0.14, 0.14), CHAR, (0.0, -0.6, 0.0))
        F.c((tx - 0.5, ty, 2.7), (1.0, 0.14, 0.14), CHAR, (0.0, 0.6, 0.0))
        for q in range(3):
            fl = 0.5 + 0.5 * math.sin(2 * math.pi * (t * 2.3 + 0.37 * q + 0.21 * n))
            G.b((tx + 0.22 * math.sin(q * 2.0 + n), ty - 0.3, 0.35 + 0.45 * q + 0.1 * fl), (0.26, 0.18, 0.32 + 0.12 * fl), (3.0, 1.2 + 0.6 * fl, 0.2))
        v = vanish(tau, 0.6 + 0.45 * n, 0.25)
        if v > 0.02:
            bird(F, (tx, ty - 0.1, 3.0), -90, 1.0 * v, (0.25, 0.45, 0.80))
    for n, (qx, qy) in enumerate(((-0.9, 4.0), (0.8, 4.4), (0.0, 3.4))):
        hop = 0.05 * abs(math.sin(2 * math.pi * (t * 2.0 + n * 0.4)))
        bird(F, (qx + 0.2 * math.sin(2 * math.pi * (t * 0.4 + n)), qy, 0.03 + hop), -90 + 25 * math.sin(n + t), 1.0, SPA_C, None,
             max(0.0, math.sin(2 * math.pi * (t * 1.1 + n * 0.3))) ** 4)


# ── 17·18: 화석 앞 셀카, 창밖 새를 가리킴
def props_selfie(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    skeleton(F, (1.4, 6.0, 0.3), 0.8, ramp(tau, 0.5, dur * 0.9), 180.0)


def props_point(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    skeleton(F, (1.4, 6.0, 0.3), 0.8, 1.0, 180.0)
    bird(F, (0.5, 9.0, 1.48), -90, 1.2, PIG_C, None, max(0.0, math.sin(2 * math.pi * t * 1.0)) ** 4)


# ── 19: 창밖 새 떼
def sunset(OR, cam, i, nx, ny, d):
    sky_orb(OR, cam, i, 0.5, nx, ny, d, (3.0, 1.5, 0.5), 1.03)
    sky_orb(OR, cam, i, 0.5, nx, ny, d * 1.7, (1.3, 0.55, 0.25), 1.06)


def props_flock(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    sunset(OR, cam, i, -0.5, -0.05, 0.20)
    for n in range(26):
        ph = (0.37 * n + 0.33 * t) % 1.0
        bird(F, (-9.0 + 18.0 * ph, 10.0 + 9.0 * _h(n + 40), 1.8 + 2.8 * _h(n + 80) + 0.15 * math.sin(t * 3 + n)), 0, 1.6,
             (0.20, 0.18, 0.22), 12.0 * t + n)


# ── 20: 노을 속 새 떼가 공룡 실루엣을 그리며 멀어짐
SIL_CELLS = [(c - 6.5, 4 - r) for r, row in enumerate(SAURO) for c, ch in enumerate(row) if ch == "#"]
_r20 = np.random.default_rng(2020)
SIL_START = [(float(_r20.uniform(-0.9, 0.9)), float(_r20.uniform(-0.28, 0.28))) for _ in SIL_CELLS]


def props_sil(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    sunset(OR, cam, i, 0.0, 0.08, 0.30)
    f = smooth(ramp(tau, 0.15, dur * 0.55))
    away = ramp(tau, dur * 0.6, dur * 0.98)
    sc = 1.0 - 0.55 * away
    for n, (cx, cy) in enumerate(SIL_CELLS):
        tx, ty = cx * 0.0225 / 0.28125 * sc + 0.35 * away, cy * 0.0225 / 0.5 * sc + 0.10 + 0.12 * away
        sx, sy = SIL_START[n]
        x = lerp(sx + 0.05 * math.sin(t * 5 + n), tx, f)
        y = lerp(sy + 0.04 * math.sin(t * 4 + 1.7 * n), ty, f)
        sky_box(G, cam, i, 0.5, x, y, 0.017 * sc, 0.017 * sc, (0.02, 0.015, 0.03))


# ── 21: 질문 (새 아이콘)
def props_ask(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    srows(G, cam, BIRD, 0.55, 0.10, 0.02, (2.4, 2.2, 0.6), 1.8, pop(tau - 0.3, 0.3))
    srows(G, cam, DIG["?"], 0.55, 0.34 + 0.01 * math.sin(2 * math.pi * t / 1.1), 0.02, (3.0, 2.6, 0.9), 1.8, pop(tau - 0.5, 0.3))


# ── 22: 네모난 지구 티저
def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    rot = (0.5, 0.35, 0.8 * t)
    R = _rmat(*rot)
    F.c((0.0, 0.0, 0.0), (2.6, 2.6, 2.6), (0.10, 0.30, 0.70), rot)
    for k, n in enumerate(((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))):
        nw = R @ np.array(n, float)
        F.c(nw * 1.33, (0.04, 1.3 - 0.15 * (k % 3), 0.9 + 0.1 * (k % 2)), (0.22, 0.55, 0.25), rot_n(nw))


PROPS = {LN["hook"]: props_hook, LN["angle"]: props_angle, LN["pass"]: props_pass, LN["icons"]: props_icons, LN["era"]: props_era,
         LN["river"]: props_river, LN["bars"]: props_bars, LN["cross"]: props_cross, LN["mark"]: props_mark, LN["tape"]: props_tape,
         LN["mice"]: props_mice, LN["model"]: props_model, LN["shake"]: props_shake, LN["twist"]: props_twist, LN["birds"]: props_birds,
         LN["feed"]: props_feed, LN["burnt"]: props_burnt, LN["selfie"]: props_selfie, LN["point"]: props_point, LN["flock"]: props_flock,
         LN["sil"]: props_sil, LN["ask"]: props_ask, LN["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR, BL, LT = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off), Items(N_BL, off), []
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
TRACK[(LN["tape"], 0)] = lambda tau: (7.3 + 1.1 * min(tau, 1.7), 0.0, 0.9)


def jh_jump(tau, t):
    z = jump_h(tau, 0.25, 0.85, 0.5, 0.65)
    return dict(z=0.15 + z, pose="shock" if z > 0.03 else "smile")


CITS = [("c1", EX_SH[0], 0, -2.1, 3.0, "aw_up"), ("c2", EX_SH[2], 1, -0.8, 3.4, "film"), ("c3", EX_SH[4], 0, 0.7, 3.1, "look_up_h"),
        ("c4", EX_SH[6], 1, 2.0, 3.3, "gape")]


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    add("jh", 0, JH_SH, JH_PA, {
        L["cross"]: st("cross", 1.1, -8.6, 0, "smile", z=0.15, fn=jh_jump, also=("shock",)),
        L["tape"]: st("ruler", 6.8, -0.9, 0, "walk_a_s", v=(1.1, 0.0), stop=1.7, pair=("walk_a_s", "walk_b_s"), then=(1.7, "peer")),
        L["model"]: st("museum", 1.2, 3.4, -150, "gape", sway=(8, 2.4, 0.0), also=("smile",)),
        L["shake"]: st("museum", 1.05, 3.2, 180, "point", also=("shock",), seq=[(1.25, "shock")],
                       keys=[(0.0, (1.05, 3.2, 0.0, 180.0)), (1.25, (1.05, 3.2, 0.0, 180.0)), (1.6, (1.45, 3.2, 0.0, 180.0))]),
        L["feed"]: st("park", 0.0, 1.2, 90, "point", also=("shock",), seq=[(1.0, "shock")],
                      keys=[(0.0, (0.0, 1.2, 0.0, 90.0)), (1.0, (0.0, 1.2, 0.0, 90.0)), (1.9, (0.0, 0.2, 0.0, 90.0))]),
        L["selfie"]: st("museum", -0.2, 3.0, -90, "phone", sway=(8, 2.4, 0.0)),
        L["point"]: st("museum", 1.1, 3.4, 90, "look_up_h"),
        L["ask"]: st("museum", 0.0, 3.5, -90, "smile", seq=[(0.9, "point")])}, extra="hood")
    add("rs", 1, CO_SH, CO_PA, {
        L["tape"]: st("ruler", 6.8, 0.9, 0, "walk_a_s", v=(1.1, 0.0), stop=1.7, pair=("walk_a_s", "walk_b_s"), then=(1.7, "peer")),
        L["point"]: st("museum", -0.2, 3.4, 90, "point_up")}, extra="coat")
    for name, sh, hair, x, y, pose in CITS:
        add(name, hair, sh, X.PANTS[hair + 1], {L["river"]: st("river", x, y, -90 + 20 * (x > 0) - 20 * (x < 0), pose, sway=(10, 3.0, 0.2 * x))})
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
SMOKE_SKY = ((0.30, 0.27, 0.28), (0.80, 0.50, 0.34), 0.0)
SPACE_SKY = ((0.003, 0.004, 0.014), (0.010, 0.013, 0.034), 1.8)
ROOM_SKY = ((0.04, 0.05, 0.09), (0.10, 0.12, 0.18), 0.0)


def sky(t):
    i = line_at(t)
    s = cam_of(t)["set"]
    if s == "teaser":
        return SPACE_SKY
    if s == "ruler":
        return ROOM_SKY
    if s == "museum":
        return DUSK_SKY if i >= LN["selfie"] else DAY_SKY
    return SMOKE_SKY if i == LN["burnt"] else DAY_SKY


def env(i, st_):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if st_ == "ruler":
        e.update(sun=0.4, amb=0.45, amb_col=(0.70, 0.76, 0.92), lt={"ep45_r0": 200.0, "ep45_r1": 200.0, "ep45_r2": 200.0})
    elif st_ == "museum":
        if i >= LN["selfie"]:
            e.update(sun=2.2, sun_col=(1.0, 0.62, 0.38), sun_rot=(78, 0, 20), amb=0.34, amb_col=(0.80, 0.66, 0.62),
                     lt={"ep45_m0": 200.0, "ep45_m1": 110.0, "ep45_m2": 110.0})
        else:
            e.update(sun=0.5, amb=0.45, amb_col=(0.80, 0.82, 0.90), lt={"ep45_m0": 220.0, "ep45_m1": 120.0, "ep45_m2": 120.0})
    elif st_ == "teaser":
        e.update(sun=3.5, sun_rot=(50, 0, 60), amb=0.12, amb_col=(0.30, 0.36, 0.62))
    elif i == LN["burnt"]:
        e.update(sun=2.2, sun_col=(1.0, 0.72, 0.52), sun_rot=(68, 0, 25), amb=0.34, amb_col=(0.72, 0.60, 0.60))
    return e


# 번쩍 (줄, 줄 시작 후 초, 세기, 길이 초) — STYLE='pixe'에선 overlay의 FLASH가 안 쓰여서 postfx에서 화면 전체에 얹음
def _flashes():
    return [(LN["hook"], T_BURST, 0.35, 0.18)]


WARM = np.array((1.0, 0.95, 0.86), np.float32)


def flash_level(t):
    a = 0.0
    for i, tau0, peak, dur in _flashes():
        t0 = shot_span(i)[0] + tau0
        a = max(a, peak * clamp((t - t0 + 0.02) / 0.03) * (1.0 - clamp((t - t0 - 0.01) / dur)))
    return a


def postfx(img, t):
    """번쩍(전체 화면): 훅 불덩이가 땅에 닿는 순간."""
    a = flash_level(t)
    if a > 0.0:
        img = img + (WARM - img) * np.float32(a)
    return img


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
    v = X.Vox(45)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep45_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep45_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep45_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep45_fx", K.proto(ctx, "ep45_p_fx", cube(), [K.mat_inst("ep45_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep45_glow", K.proto(ctx, "ep45_p_glow", cube(), [_mat_glow("ep45_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep45_orb", K.proto(ctx, "ep45_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep45_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep45_bl", K.proto(ctx, "ep45_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep45_m_bl", 0.8)]),
                     N_BL, vector_scale=True)
    for ob in (gl, orb):                                              # 발광 상자·불덩이가 햇빛을 가리지 않게
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
