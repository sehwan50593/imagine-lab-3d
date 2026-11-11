"""EP44 만약에 80억 명이 한 도시에 산다면? (기준 영상 형식 STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

11-06 오너: 42~49는 '남자가 한 명뿐이라면' 편 형식으로, 내레이션 없이. 소리는 배경음(-23 LUFS)과 효과음뿐.
장면(3D)은 11-05 픽세판 그대로(옥상 빌딩 숲·지하철·댐 단면·쓰레기 산·지도판·지구본 파이·들판), 줄 순서도 그대로(이미 시간순).
D-DAY(한국 땅의 5배, 최대 도시의 190배) → +1일(지하철, 하루 물 4억~8억 톤) → +1주(소양강댐 4~7일) → +1달(쓰레기 하루 550만 톤)
→ +1년(쓰레기 산) → 반전(육지의 0.3%) → 현실(55%) → 2050년(68%) → 결론(도시는 땅을 아끼는 방법) → 다음 편(공룡).

근거(설명란): ※ '80억 명이 서울과 같은 밀도로 한 도시에 산다, 물은 1인 하루 50~100L'라는 가정의 상상 시나리오. 그림 속 크기·비율은 연출.
· 세계 인구 약 80억 · UN(2022-11-15 추정 돌파)
· 서울 605.2㎢·약 963만 명 → 약 15,900명/㎢ → 80억 명이면 약 50만㎢, 대한민국(약 10만㎢)의 약 5배(계산) · 서울시 통계, 국토교통부 지적통계 2025
· 세계 최대 도시 자카르타 약 4,190만 명(새 도시 정의) → 그런 도시 약 190개(계산) · UN World Urbanization Prospects 2025
· 1인 하루 50~100L × 80억 = 하루 4억~8억 톤(계산) · WHO 기준(2차 인용)
· 소양강댐 총저수량 약 29억 톤 → 4~7일치(계산) · 한국수자원공사
· 세계 도시 고형폐기물 연 20.1억 톤(2016) → 하루 약 550만 톤(계산) · World Bank What a Waste 2.0(2018)
· 50만㎢는 지구 육지(약 1억 4,900만㎢)의 약 0.3%(계산)
· 세계 인구의 55%가 도시 거주(2018), 2050년 68% 전망 · UN World Urbanization Prospects 2018
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
# 세트 자리 (서로 400m씩 떨어뜨려 빛이 섞이지 않게). 도시 세트는 x ±140, y -130~270까지 퍼짐
OFF = {"city": (0, 0), "metro": (500, 0), "dam": (900, 0), "trash": (1300, 0), "map": (1700, 0), "space": (2100, 0), "field": (2500, 0)}
NAMES = ("hook", "density", "forest", "jakarta", "need190", "metro", "tap", "dry", "dam", "trash", "trucks", "mount", "map", "twist",
         "pie55", "night", "pie68", "scatter", "green", "icons", "help", "ask", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}

# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
# ease="out": 처음에 빨리 움직이고 천천히 멈춤(훅)
LINES = [
    dict(d=2.9, sub="80억 명이 모두\n한 도시에 산다면?", ease="out", shot=("city", (0.0, 0.0, 1.3), -90, 3, 4.2, 28, 0.85, 55, 0.10)),
    dict(d=3.2, sub="서울만큼 빽빽하게 살면\n넓이만 약 50만㎢.", shot=("city", (0.6, 0.0, 1.3), -80, 4, 6.0, 26, 0.9, 8, 0.08)),
    dict(d=2.7, sub="눈앞에 빌딩이\n끝없이 이어집니다.", shot=("city", (0.0, 0.0, 2.0), 90, 8, 5.5, 26, 0.95, 150, 0.04)),
    dict(d=3.2, sub="지금 가장 큰 도시 자카르타는\n약 4,190만 명.", shot=("city", (-0.5, 0.0, 2.0), -80, 4, 7.5, 26, 0.9, 6, 0.06)),
    dict(d=2.6, sub="그런 도시가\n190개 모인 셈입니다.", shot=("city", (0.0, 2.6, 0.4), -90, 42, 15.0, 28, 0.9, 0, 0.05)),
    dict(d=2.8, sub="출근길 지하철은\n숨 쉴 틈도 없습니다.", shot=("metro", (0.0, 0.0, 1.3), -90, 3, 5.5, 26, 0.85, 10, 0.08)),
    dict(d=3.2, sub="한 사람이 하루 50~100L,\n모두 합치면 4억~8억 톤.", shot=("dam", (0.0, 3.0, 2.2), -90, 6, 9.0, 26, 0.9, 4, 0.04)),
    dict(d=2.5, sub="수도관마다 물이\n빠르게 줄어듭니다.", shot=("dam", (0.0, 5.0, 2.2), -90, 5, 11.0, 26, 0.94, 3, 0.05)),
    dict(d=3.1, sub="소양강댐 29억 톤도\n4~7일이면 바닥납니다.", shot=("dam", (0.0, 5.0, 1.9), -90, 5, 13.0, 26, 0.94, 2, 0.07)),
    dict(d=2.8, sub="한 달 뒤, 거리마다\n쓰레기가 쌓입니다.", shot=("trash", (0.0, 0.0, 1.3), -90, 8, 6.5, 26, 0.88, -6, 0.06)),
    dict(d=3.2, sub="지금도 세계 도시 쓰레기는\n하루 약 550만 톤.", shot=("trash", (0.0, 2.0, 1.2), -75, 6, 9.0, 26, 0.92, 8, 0.08)),
    dict(d=3.3, sub="1년 뒤, 도시 밖에\n쓰레기 산이 솟습니다.", shot=("trash", (0.0, 6.0, 2.0), -100, 7, 14.0, 26, 0.92, 12, 0.07)),
    dict(d=2.7, sub="이 도시를\n지구 지도에 올려 보면", shot=("map", (0.0, 0.3, 1.0), -90, 30, 7.5, 24, 0.9, 3, 0.06)),
    dict(d=2.9, sub="지구 육지의\n0.3%밖에 안 됩니다.", shot=("map", (0.6, 0.0, 0.9), -90, 36, 5.5, 24, 0.85, 2, 0.08)),
    dict(d=3.0, sub="이미 세계 인구의 55%가\n도시에 삽니다.", shot=("space", (-1.6, 0.0, 0.0), -90, 6, 12.5, 26, 0.92, 3, 0.02)),
    dict(d=2.6, sub="지후도 오늘\n도시의 한 칸에 삽니다.", shot=("city", (0.0, 0.0, 1.5), -90, 2, 5.0, 26, 0.9, 5, 0.06)),
    dict(d=2.8, sub="2050년에는\n68%가 됩니다.", shot=("city", (0.0, 0.0, 1.5), -90, 2, 5.5, 26, 0.88, -6, 0.06)),
    dict(d=2.8, sub="80억 명이 한 도시는\n상상일 뿐이지만", shot=("field", (0.0, 0.0, 1.3), -90, 3, 9.0, 24, 0.9, 4, 0.05)),
    dict(d=2.8, sub="도시는 땅을 아끼는\n방법이기도 합니다.", shot=("map", (1.3, 2.0, 1.3), -100, 5, 6.0, 26, 0.88, 8, 0.07)),
    dict(d=2.8, sub="대신 물과 쓰레기가\n늘 숙제가 됩니다.", shot=("city", (0.0, 2.0, 1.6), -90, 3, 8.0, 28, 0.95, 0, 0.0)),
    dict(d=3.3, sub="가까이 사는 만큼\n서로 더 챙겨야 합니다.", shot=("metro", (0.6, -0.5, 0.9), -90, 4, 5.0, 26, 0.9, 5, 0.06)),
    dict(d=2.6, sub="댓글로 알려 주세요.", shot=("field", (0.0, 0.0, 1.45), -90, 2, 5.5, 30, 0.9, 0, 0.06)),
    dict(d=3.6, sub="공룡과 사람이\n함께 산다면?", shot=("field", (0.0, 6.0, 2.1), -90, 4, 13.0, 26, 0.9, 3, 0.04)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="D-DAY", label="80억 명이 사는 도시", big="한국 땅의 5배", label_color="blue", big_color="yellow"),
    dict(at="jakarta", badge="D-DAY", title="지금 가장 큰 도시의", big="190배", big_color="orange"),
    dict(at="metro", badge="+1일", title="출근길은 {red}숨 쉴 틈 없음{/}"),
    dict(at="tap", badge="+1일", title="하루에 쓰는 물", big="4억~8억 톤", big_color="cyan"),
    dict(at="dry", badge="+1주", title="소양강댐 29억 톤도", big="4~7일이면 바닥", big_color="red"),
    dict(at="trash", badge="+1달", title="세계 쓰레기는 지금도", big="하루 550만 톤", big_color="orange"),
    dict(at="mount", badge="+1년", title="도시 밖에 {orange}쓰레기 산{/}"),
    dict(at="map", badge="반전", title="지구 지도에 올리면", big="육지의 0.3%", big_color="green"),
    dict(at="pie55", badge="현실", title="이미 도시에 사는 사람", big="55%", big_color="cyan"),
    dict(at="pie68", badge="2050년", title="도시에 사는 사람", big="68%", big_color="cyan"),
    dict(at="scatter", badge="결론", title="도시는 {green}땅을 아끼는{/} 방법"),
    dict(at="ask", badge="결론", title="내가 사는 도시엔\n{cyan}몇 명이{/} 살까요?", title_size=70),
    dict(at="teaser", badge="다음 편", title="오늘 저녁 7시\n{cyan}공룡이 멸종하지 않았다면?{/}", title_size=64),
]
TWIST = LN["twist"]  # '육지의 0.3%뿐' 반전 줄 — 음악이 바뀌는 곳
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
META = {"id": "ep44", "title": "만약에 80억 명이 한 도시에 산다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"style": "retro", "key": "Bb", "mode": "major", "bpm": 100, "seed": 441, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, [[STARTS[LN["mount"]] + 0.3, "rumble", 0.45, 2.4]])}}
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


def postfx(img, t):
    return img


def _shake_spec(i):
    """줄 i의 흔들림 [(시작 τ, 길이, 이동 세기 m, 각도 세기 도, 진동수 Hz, 종류)]. 'hold' 거의 일정."""
    if i == LN["hook"]:
        return [(0.0, 99.0, 0.035, 0.0, 15.0, "hold")]
    if i == LN["metro"]:
        return [(0.0, 99.0, 0.03, 0.0, 11.0, "hold")]
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


# ───────────────────────── 색 · 도트 글자 ─────────────────────────
GRASS = (0.34, 0.58, 0.26)
SKINC = X.SKIN
OCEAN = (0.08, 0.26, 0.68)
RE = 1.55                                   # 지구 반지름 (그림 크기, 실제 비율 아님)
EX_SH = [(0.85, 0.30, 0.28), (0.95, 0.80, 0.35), (0.35, 0.65, 0.40), (0.45, 0.75, 0.85), (0.80, 0.55, 0.65), (0.25, 0.45, 0.80),
         (0.92, 0.92, 0.90), (0.40, 0.55, 0.50), (0.88, 0.58, 0.30)]      # 시민 (지후의 보라는 피함)
JH_SH, JH_PA = (0.58, 0.32, 0.80), (0.15, 0.18, 0.30)      # 지후: 보라 후드 · 짧은 머리 · 남색 바지
CO_SH, CO_PA = (0.93, 0.93, 0.91), (0.22, 0.24, 0.30)      # 연구원: 흰 가운 (extra='coat')
CZ_SH, CZ_PA = (0.85, 0.30, 0.28), (0.20, 0.20, 0.22)      # 넘어지는 시민
WARM_G = (3.0, 2.4, 0.8)


def wdig(G, rows, cx, y, cz, cell, col, k=1.0):
    """세트에 서 있는 도트 글자 (−y쪽을 보는 면, 가운데 맞춤): 칸 하나 = 발광 상자."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        G.b((cx + ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, y, cz + (h / 2.0 - r - 0.5) * cell * k),
            (((c1 - c + 1) - 0.06) * cell * k, 0.03, cell * 0.94 * k), col)


def blk(F, x, y, z, sh, pa, k=1.0, sk=SKINC):
    """상자 세 개로 쌓은 시민 한 명 (발 위치 z)."""
    F.b((x, y, z + 0.25 * k), (0.34 * k, 0.20 * k, 0.50 * k), pa)
    F.b((x, y, z + 0.75 * k), (0.40 * k, 0.22 * k, 0.50 * k), sh)
    F.b((x, y, z + 1.13 * k), (0.26 * k, 0.26 * k, 0.26 * k), sk)


# ───────────────────────── 세트 ─────────────────────────
def _make_city():
    """끝없는 빌딩 숲: 10m 칸마다 건물 하나(폭·깊이 5.5~7.5, 칸 안 위치 ±0.8 비껴 놓음). 지후 둘레 17m 안은 옥상보다 낮게."""
    rs = np.random.default_rng(4401)
    pal = [(0.55, 0.62, 0.74), (0.70, 0.72, 0.76), (0.78, 0.70, 0.60), (0.50, 0.56, 0.62), (0.66, 0.58, 0.62), (0.42, 0.50, 0.62)]
    out = []
    for ix in range(-13, 14):
        for iy in range(-12, 27):
            cx, cy = ix * 10.0 + float(rs.uniform(-0.8, 0.8)), iy * 10.0 + float(rs.uniform(-0.8, 0.8))
            w, d = float(rs.uniform(5.5, 7.5)), float(rs.uniform(5.5, 7.5))
            r = math.hypot(cx, cy)
            top = float(rs.uniform(-12.0, -3.0)) if r < 17.0 else float(rs.uniform(-8.0, 12.0 + 0.22 * r))
            out.append((cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, top, pal[int(rs.integers(len(pal)))]))
    return out


CITY = _make_city()


def _make_windows():
    """밤 야경용 창문 후보 520개 (건물 앞면 y0 쪽, 무작위 순서 = 켜지는 순서)."""
    rs = np.random.default_rng(4402)
    cand = []
    for x0, x1, y0, y1, top, col in CITY:
        if not (18.0 <= y0 <= 120.0 and abs((x0 + x1) / 2) < 55.0 and top > 3.0):
            continue
        for wx in np.arange(x0 + 1.0, x1 - 1.0, 1.7):
            for wz in np.arange(1.0, top - 1.0, 2.6):
                if rs.random() < 0.45:
                    cand.append((float(wx), float(y0), float(wz)))
    return [cand[k] for k in rs.permutation(len(cand))[:520]]


WINS = _make_windows()


def _city(v):
    v.floor(-140, 150, -130, 270, (0.24, 0.25, 0.28), 10.0, z=-60.0)
    v.box(-9, 9, -9, 9, -0.6, 0.0, (0.56, 0.57, 0.62), jit=0.02)                 # 옥상
    v.box(-8.0, -6.4, 6.0, 7.6, 0.0, 1.1, (0.70, 0.72, 0.75))                    # 실외기
    v.box(5.4, 8.0, 5.6, 8.0, 0.0, 2.4, (0.62, 0.60, 0.58))                      # 계단실
    for x0, x1, y0, y1, top, col in CITY:
        v.box(x0, x1, y0, y1, -60.0, top, col, jit=0.05)
    v.light(0.0, 1.0, 5.0, 260, (1.0, 0.85, 0.65), 1.0, "ep44_city0")


def _metro(v):
    v.floor(-9, 9, -6, 3.5, (0.58, 0.59, 0.63), 0.5, "check")
    v.floor(-9, 9, 3.5, 7, (0.18, 0.18, 0.20), 0.5, z=-0.6)                      # 선로
    v.box(-9, 9, 3.5, 3.56, -0.6, 0.0, (0.40, 0.40, 0.44))                        # 승강장 모서리
    v.box(-9, 9, 2.6, 2.8, 0.0, 0.015, (0.95, 0.80, 0.10), jit=0)                 # 안전선
    v.box(-9, 9, 3.62, 6.1, -0.3, 3.1, (0.82, 0.84, 0.88))                         # 전동차
    v.box(-9.02, 9.02, 3.60, 6.12, 1.2, 1.5, (0.20, 0.45, 0.80), jit=0)
    for k in range(6):                                                           # 문
        x = -7.5 + 3.0 * k
        v.box(x - 0.55, x + 0.55, 3.56, 3.60, 0.0, 2.4, (0.75, 0.88, 1.0), jit=0, glow=True)
    v.wall((-9, 7), (9, 7), -0.6, 5, (0.55, 0.60, 0.68), 0.5, face=-1)
    for x in (-6.5, 0.0, 6.5):
        v.box(x - 0.3, x + 0.3, 1.0, 1.6, 0.0, 4.5, (0.60, 0.60, 0.64))
    v.box(-9, 9, 0.9, 1.7, 4.5, 4.7, (0.45, 0.45, 0.50))


def _dam(v):
    v.floor(-16, 16, -10, 16, (0.46, 0.58, 0.40), 1.0)
    rs = v.rs
    for k in range(10):                                                          # 먼 언덕 (y를 비껴 놓음)
        x0 = -40 + 9 * k
        v.box(x0, x0 + 11, 28 + 2.3 * (k % 4), 40 + 2.3 * (k % 4), 0, float(rs.uniform(3, 8)), (0.30 + 0.03 * (k % 3), 0.48, 0.36), jit=0.05)
    v.box(-3.55, 3.55, 4.4, 10.2, 0.0, 0.1, (0.35, 0.35, 0.38), jit=0.02)         # 수조 바닥
    v.box(-3.55, -3.35, 4.4, 10.2, 0.1, 5.4, (0.62, 0.62, 0.66))                   # 왼벽
    v.box(3.35, 3.55, 4.4, 10.2, 0.1, 5.4, (0.62, 0.62, 0.66))                     # 오른벽
    v.wall((-3.35, 10.0), (3.35, 10.0), 0.1, 5.4, (0.58, 0.58, 0.62), 0.5, face=-1)  # 단면 뒤 벽(돌)


def _trash(v):
    v.floor(-10, 10, -14, 30, (0.30, 0.30, 0.33), 1.0)
    v.box(-1.2, 1.2, -14, 30, 0.0, 0.012, (0.85, 0.82, 0.30), jit=0)
    rs = v.rs
    for side in (-1, 1):
        y = -14.0
        k = 0
        while y < 30:
            d = float(rs.uniform(6.0, 8.0))
            h = float(rs.uniform(6.0, 13.0))
            x0, x1 = (-17.0 - 0.4 * (k % 3), -10.0) if side < 0 else (10.0, 17.0 + 0.4 * (k % 3))
            v.box(x0, x1, y, y + d, 0.0, h, (0.62 + 0.04 * (k % 3), 0.58, 0.52 + 0.05 * (k % 2)))
            y += d + float(rs.uniform(0.6, 1.4))
            k += 1
    for k in range(8):
        v.box(-40 + 12 * k, -30 + 12 * k, 38 + 2.5 * (k % 3), 46 + 2.5 * (k % 3), 0, 8 + 3 * (k % 4), (0.55, 0.60, 0.68), jit=0.05)


MAPR = [
    "......................................",
    "..#######......##..###########........",
    ".#########....####.#############.....",
    ".########....######.###########......",
    "..######......####..###########.....",
    "...####.......#####..##########.....",
    "....###........####...#######...###.",
    ".....###........###....####.....###.",
    ".....####.........##.....##........#",
    ".....####..................##.....##",
    "......###..................###.....#",
    "......##.......................###..",
    ".......#..............................",
]
MAPR = [r[:38].ljust(38, ".") for r in MAPR]
MAP_CELL = 0.1


def _map(v):
    v.floor(-7, 7, -9, 8, (0.50, 0.36, 0.24), 0.5, "wood")
    v.wall((-7, 6.5), (7, 6.5), 0, 5, (0.16, 0.30, 0.33), 0.5, face=-1)
    v.box(-2.4, 2.4, -1.4, 1.4, 0.7, 0.8, (0.60, 0.42, 0.26))
    for sx in (-2.25, 2.25):
        for sy in (-1.25, 1.25):
            v.box(sx - 0.1, sx + 0.1, sy - 0.1, sy + 0.1, 0.0, 0.7, (0.45, 0.31, 0.20))
    v.box(-2.0, 2.0, -1.0, 1.0, 0.80, 0.84, (0.30, 0.55, 0.80), jit=0.02)         # 바다 종이 판
    h, w = len(MAPR), len(MAPR[0])
    for r, c, c1 in _runs(MAPR):                                                  # 대륙 윤곽 (칸 0.1)
        x0 = (c - w / 2.0) * MAP_CELL
        x1 = (c1 + 1 - w / 2.0) * MAP_CELL
        y1 = (h / 2.0 - r) * MAP_CELL * 0.7
        v.box(x0, x1, y1 - MAP_CELL * 0.7, y1, 0.845, 0.865, (0.40, 0.65, 0.32), jit=0.05)
    v.light(0.0, 0.0, 4.5, 170, (1.0, 0.95, 0.85), 0.9, "ep44_map0")
    v.light(0.0, -4.0, 3.0, 100, (1.0, 0.92, 0.8), 0.8, "ep44_map1")


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


def _field(v):
    v.floor(-70, 90, -10, 125, GRASS, 2.5)
    rs = v.rs
    for k in range(14):                                       # 먼 언덕 (y를 조금씩 비껴 놓음)
        x0 = -130 + 22 * k
        h = float(rs.uniform(5, 14))
        v.box(x0, x0 + 26, 128 + 3.1 * (k % 4), 150 + 3.1 * (k % 4), 0, h, (0.28 + 0.03 * (k % 3), 0.46, 0.34 + 0.02 * (k % 2)), jit=0.05)


def _sets():
    return (("city", _city), ("metro", _metro), ("dam", _dam), ("trash", _trash), ("map", _map), ("space", _space), ("field", _field))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 1500, 900, 40, 40


def sp_of(t):
    return 0.35 * t


def earth_items(F, BL, cam, center, R, sp):
    """지구: 파란 구(조명 받음) + 앞쪽 반구에 보이는 땅·극지 조각(자전 sp). center = 세트 좌표."""
    ox, oy = OFF["space"]
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
    return cw, view, Rm


def frame_sp(G, cam, nx, ny, w, h, col, t=0.012):
    """화면 좌표 (nx, ny) 가운데에 w×h (화면 높이 비율) 테두리."""
    for sgn in (-1, 1):
        sprite(G, cam, nx, ny + sgn * (h / 2) / 0.5, w + t, t, col, 2.0, 0.012)
        sprite(G, cam, nx + sgn * (w / 2) / 0.28125, ny, t, h, col, 2.0, 0.012)


KOREA = ["..####..", ".######.", ".######.", "..#####.", "..#####.", "...####.", "...####.", "....###.", "....##..", "...###..", "..###...", "..##...."]
FAUCET = ["..####.", "..#..#.", "..#####", "###....", "#.#....", "..#....", "..#.#.."]
BAG = ["..###..", "...#...", ".#####.", "#######", "#######", "#######", ".#####."]


def pie_rows(frac, n=13):
    """원 안 칸을 위(12시)부터 시계방향으로 frac만큼 채운 도트 파이: (채운 칸 그림, 나머지 칸 그림)."""
    on, off = [], []
    for r in range(n):
        a, b = "", ""
        for c in range(n):
            dx, dy = c - (n - 1) / 2.0, (n - 1) / 2.0 - r
            if math.hypot(dx, dy) > n / 2.0:
                a += "."
                b += "."
                continue
            ang = (math.atan2(dx, dy) / (2 * math.pi)) % 1.0
            a += "#" if ang < frac else "."
            b += "." if ang < frac else "#"
        on.append(a)
        off.append(b)
    return on, off


def pie_draw(G, cam, frac, nx, ny, cell=0.0145):
    on, off = pie_rows(frac)
    srows(G, cam, off, nx, ny, cell, (0.35, 0.45, 0.65), 1.8)
    if frac > 0.02:
        srows(G, cam, on, nx, ny, cell, (3.0, 2.4, 0.6), 1.7)
    txt = "%d%%" % int(round(frac * 100))
    srows(G, cam, num_rows(txt), nx, ny - 0.30, 0.011, (3.0, 3.0, 2.6), 1.8)


def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """작은 한반도 윤곽(청록)이 5배 큰 도시 틀(주황) 한구석에 덮임 — 틀이 커지며 맥동 (0.0초부터 움직임)."""
    g = 0.55 + 0.45 * smooth(ramp(tau, 0.0, 0.7)) + 0.025 * math.sin(2 * math.pi * t / 0.6)
    frame_sp(G, cam, -0.60, -0.10, 0.19 * g, 0.19 * g, (3.0, 1.3, 0.4))
    srows(G, cam, KOREA, -0.80 - (1 - g) * 0.1, -0.20, 0.0065 * g, (0.5, 2.6, 3.0), 1.8)
    srows(G, cam, num_rows("x5"), -0.46, -0.04, 0.012 * g, (3.0, 2.6, 0.6), 1.8)


def props_density(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """서울 밀도 표지판: 1㎢당 15900명 (도트 글자)."""
    s = pop(tau - 0.2, 0.3)
    F.b((1.5, 0.30, 0.0), (0.12, 0.12, 1.4), (0.35, 0.35, 0.40))
    F.b((1.5, 0.30, 1.3), (1.5, 0.08, 0.9), (0.12, 0.17, 0.30))
    wdig(G, num_rows("15900"), 1.5, 0.25, 1.75, 0.075, (3.0, 2.6, 0.7), s)


def props_jakarta(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """지금 가장 큰 도시 = 기둥 하나 (노란 탑 + 깃발)."""
    s = pop(tau - 0.1, 0.5)
    F.b((-1.8, 1.6, 0.0), (1.4, 1.4, 3.4 * s), (0.95, 0.78, 0.30))
    F.b((-1.8, 1.6, 3.42 * s), (0.9, 0.9, 0.12), (3.0, 2.4, 0.8))
    F.b((-1.8, 1.6, 3.5 * s), (0.07, 0.07, 0.9), (0.4, 0.4, 0.45))
    F.b((-1.5, 1.6, 4.1 * s), (0.5, 0.05, 0.3), (0.2, 0.7, 0.9))


def props_need190(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """기둥 190개 격자 (19×10) + 맨 앞 노란 기둥 = 자카르타 한 개."""
    k = 190
    F.b((-4.4, -0.3, 0.0), (0.5, 0.5, 1.6), (0.95, 0.78, 0.30))
    span = dur * 0.85
    for j in range(k):
        c, r = j % 19, j // 19
        s = pop(tau - (0.1 + j / k * span), 0.18)
        if s <= 0.01:
            continue
        F.b((-3.24 + 0.36 * c, 0.5 + 0.36 * r, 0.0), (0.26, 0.26, 0.7 * s), (0.30 + 0.03 * r, 0.65, 0.85 - 0.04 * r))


_rm = np.random.default_rng(4405)
METRO = []
while len(METRO) < 80:
    _x, _y = float(_rm.uniform(-6.5, 6.5)), float(_rm.uniform(-2.2, 2.6))
    if abs(_x) < 1.3 and _y < 1.2:
        continue
    METRO.append((_x, _y, EX_SH[int(_rm.integers(len(EX_SH)))], X.PANTS[int(_rm.integers(len(X.PANTS)))], float(_rm.random())))


def metro_crowd(F, t, n, skip=None):
    for x, y, sh, pa, ph in METRO[:n]:
        if skip and skip[0] < x < skip[1] and skip[2] < y < skip[3]:
            continue
        blk(F, x + 0.12 * math.sin(2 * math.pi * (t * 1.6 + ph)), y, 0.0, sh, pa)


def props_metro(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    metro_crowd(F, t, 80)


# ── 6~8: 수도꼭지 · 수조(댐 단면)
FAUCETS = [(-3.15 + 0.35 * c, 0.8 + 0.8 * r) for r in range(4) for c in range(19)]
TANK_H = 4.6


def water_level(i, tau, dur):
    if i == LN["tap"]:
        return 1.0
    f = smooth(ramp(tau, 0.2, dur * 0.9))
    return 1.0 - 0.58 * f if i == LN["dry"] else 0.42 * (1.0 - f)


def tank_items(F, G, i, tau, dur, t):
    lv = water_level(i, tau, dur)
    hh = TANK_H * lv
    if hh > 0.03:
        F.b((0.0, 4.6, 0.1), (6.5, 5.3, hh), (0.20, 0.45, 0.85))
        F.b((0.0, 4.6, 0.1 + hh + 0.02), (6.5, 5.3, 0.05), (0.55, 0.78, 1.0))
    for k in range(11):                                       # 눈금
        F.b((-3.1, 4.5, 0.4 + 0.41 * k), (0.5 if k % 5 == 0 else 0.3, 0.04, 0.05), (0.92, 0.92, 0.92))
    return lv


def props_tap(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    tank_items(F, G, i, tau, dur, t)
    for r in range(4):
        F.b((0.0, 0.8 + 0.8 * r, 3.15), (6.9, 0.18, 0.18), (0.55, 0.57, 0.62))
    for j, (x, y) in enumerate(FAUCETS):
        F.b((x, y + 0.02, 2.85), (0.14, 0.14, 0.3), (0.40, 0.42, 0.48))
        for q in range(2):
            ph = (t * 1.4 + _h(j * 2 + q) + 0.5 * q) % 1.0
            F.b((x, y + 0.05, 2.8 - 2.8 * ph * ph), (0.09, 0.09, 0.16), (0.25, 0.55, 1.0))
    wdig(G, num_rows("4-8"), 0.0, 4.40, 2.4, 0.26, (3.0, 2.8, 0.8), pop(tau - 0.3, 0.3))


def props_dry(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    tank_items(F, G, i, tau, dur, t)
    for j in range(10):                                       # 바닥 배수구에서 줄줄 새는 물방울
        ph = (t * 1.3 + _h(j + 90)) % 1.0
        F.b((-2.2 + 0.5 * j, 4.2, 0.9 - 0.9 * ph * ph), (0.1, 0.1, 0.18), (0.25, 0.55, 1.0))


def props_dam(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    lv = tank_items(F, G, i, tau, dur, t)
    v = int(round(29 * lv / 0.42))
    wdig(G, num_rows(str(max(v, 0))), 0.0, 4.40, 4.05, 0.22, (3.0, 2.8, 0.8))


# ── 9~11: 쓰레기
BAGC = [(0.10, 0.10, 0.12), (0.12, 0.34, 0.18), (0.85, 0.85, 0.80), (0.22, 0.30, 0.60)]


def props_trash(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """봉투 상자가 쌓여 지후(안 보임)가 파묻히고 손만 흔듦."""
    hmax = 2.4 * smooth(ramp(tau, 0.1, dur * 0.8))
    for a in range(9):
        for b in range(9):
            x, y = -3.2 + 0.8 * a, -3.2 + 0.8 * b
            r = math.hypot(x, y)
            hc = hmax * max(0.0, 1.0 - r / 3.5) ** 0.8
            for n in range(int(math.ceil(hc / 0.6 - 1e-6))):
                F.b((x + 0.06 * _h(a * 9 + b + n), y - 0.28, 0.6 * n), (0.7, 0.56, 0.6), BAGC[int(_h(a * 17 + b * 5 + n) * 4) % 4])
    top = math.ceil(hmax / 0.6 - 1e-6) * 0.6
    ry = -math.pi / 2 + 0.45 * math.sin(2 * math.pi * t * 2.2)
    d = np.array((math.cos(ry), 0.0, -math.sin(ry)))
    base = np.array((0.0, 0.0, top))
    F.c(tuple(base + d * 0.3), (0.6, 0.16, 0.18), JH_SH, (0.0, ry, 0.0))
    F.c(tuple(base + d * 0.7), (0.2, 0.2, 0.2), SKINC, (0.0, ry, 0.0))


def props_trucks(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """쓰레기 트럭 행렬 (오른쪽으로 흘러감) + 550 숫자판."""
    for j in range(8):
        x = (j * 3.4 + 3.2 * t) % 27.2 - 13.6
        F.b((x, 2.0, 0.35), (2.6, 1.2, 1.0), (0.20, 0.60, 0.35))
        F.b((x + 1.0, 2.0, 0.35), (0.9, 1.2, 1.35), (0.92, 0.92, 0.88))
        F.b((x, 2.1, 1.38), (2.4, 1.0, 0.25), (0.10, 0.12, 0.12))
        for wx in (-0.9, 0.0, 1.1):
            F.b((x + wx, 1.95, 0.0), (0.5, 1.3, 0.5), (0.08, 0.08, 0.09))
    F.b((0.0, 6.0, 2.5), (2.4, 0.1, 1.2), (0.10, 0.10, 0.16))
    wdig(G, num_rows("550"), 0.0, 5.95, 3.1, 0.16, (3.0, 2.8, 0.8), pop(tau - 0.3, 0.3))


def props_mount(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """도시 가장자리 봉투 산: 층이 하나씩 올라오고 갈매기 떼가 돎."""
    f = 5.5 * smooth(ramp(tau, 0.0, dur * 0.9))
    for k in range(6):
        hk = 0.9 * clamp(f - k)
        if hk > 0.03:
            F.b((0.0, 7.0 - (9.0 - 1.5 * k) / 2, 0.9 * k - 0.02 * k), (11.0 - 1.9 * k, 9.0 - 1.5 * k, hk), BAGC[k % 4] if k % 3 else (0.35, 0.33, 0.30))
    for j in range(70):
        k = j % 5
        if f > k + 0.4:
            F.b((-4.5 + 9.0 * _h(j + 300) * (1 - 0.15 * k), 7.0 - 3.5 + 7.0 * _h(j + 400) * (1 - 0.1 * k), 0.9 * (k + 1)),
                (0.5, 0.4, 0.4), BAGC[int(_h(j) * 4) % 4])
    for j in range(14):
        a = 2 * math.pi * _h(j + 500) + 0.9 * t * (0.6 + 0.8 * _h(j + 600))
        rr = 2.5 + 3.0 * _h(j + 700)
        x, y, z = rr * math.cos(a), 7.0 + 0.6 * rr * math.sin(a), 5.2 + 0.8 * math.sin(2 * math.pi * (0.5 * t + _h(j)))
        wv = 0.12 * math.sin(2 * math.pi * 3.0 * t + j)
        F.b((x, y, z), (0.3, 0.12, 0.1), (0.95, 0.95, 0.95))
        F.b((x, y - 0.22, z + wv), (0.36, 0.2, 0.04), (0.85, 0.85, 0.88))
        F.b((x, y + 0.12, z + wv), (0.36, 0.2, 0.04), (0.85, 0.85, 0.88))


# ── 12~14: 지도판 · 지구
TILE_C = (0.6, 0.0)


def props_map(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """연구원과 지후가 큰 사각 칸(주황)을 대륙 지도판에 올려 놓음 (위에서 떨어져 톡)."""
    z = 0.905 + 0.9 * max(0.0, 1.0 - tau / 0.6) ** 2
    s = 0.7
    F.b((TILE_C[0], TILE_C[1] - s / 2, z), (s, s, 0.06), (0.95, 0.35, 0.20))


def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """사각 칸이 대륙 윤곽 대비 아주 작은 점으로 줄어듦 (그림 크기, 실제 비율 아님) + 깜박이는 표시."""
    f = smooth(ramp(tau, 0.3, 1.3))
    s = lerp(0.7, 0.045, f)
    F.b((TILE_C[0], TILE_C[1] - s / 2, 0.905), (s, s, 0.06), (0.95, 0.35, 0.20))
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t / 0.5)
    if f > 0.9:
        for dx, dy in ((-0.14, 0.0), (0.14, 0.0), (0.0, -0.14), (0.0, 0.14)):
            G.b((TILE_C[0] + dx, TILE_C[1] + dy, 0.99), (0.04, 0.04, 0.04), (3.0 * p, 1.4 * p, 0.4 * p))


def props_pie55(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """지구본(도시 불빛 반짝) + 도시 거주 55% 파이."""
    cw, view, Rm = earth_items(F, BL, cam, (0.0, 0.0, 0.0), RE, sp_of(t))
    for k in LAND_IDX[::7]:
        n = Rm @ EARTH_PTS[k]
        if n @ view < 0.2:
            continue
        p = 0.45 + 0.55 * math.sin(2 * math.pi * (1.1 * t + _h(k)))
        if p > 0.3:
            G.cw(cw + n * (RE + 0.03), (0.04, 0.07, 0.07), (3.0 * p, 2.3 * p, 0.7 * p), rot_n(n))
    pie_draw(G, cam, 0.55 * smooth(ramp(tau, 0.0, 1.0)), -0.52, 0.0)


def lit_windows(G, k):
    for wx, wy, wz in WINS[:k]:
        G.b((wx, wy - 0.05, wz), (0.8, 0.04, 1.1), (2.6, 2.0, 0.8) if _h(wx + wz) < 0.8 else (1.6, 2.2, 2.8))


def props_night(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """야경: 건물 창에 하나씩 불이 켜짐 (시간 경과)."""
    lit_windows(G, int(len(WINS) * 0.5 * ramp(tau, 0.0, dur * 0.95)))


def props_pie68(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """파이가 55%에서 68%로 자라고 불빛이 늘어남."""
    lit_windows(G, int(len(WINS) * (0.5 + 0.45 * ramp(tau, 0.0, dur * 0.9))))
    pie_draw(G, cam, lerp(0.55, 0.68, smooth(ramp(tau, 0.1, 1.2))), -0.52, 0.02)


TREES = [(float(x), float(y)) for x, y in zip(np.random.default_rng(4407).uniform(-9, 9, 16), np.random.default_rng(4408).uniform(8, 30, 16))]
BLDS = [(float(x), float(y), float(w), float(h), c) for x, y, w, h, c in zip(
    np.random.default_rng(4409).uniform(-10, 10, 26), np.random.default_rng(4410).uniform(8, 40, 26),
    np.random.default_rng(4411).uniform(2.5, 4.5, 26), np.random.default_rng(4412).uniform(5, 16, 26),
    [(0.55, 0.62, 0.74), (0.70, 0.72, 0.76), (0.78, 0.70, 0.60), (0.50, 0.56, 0.62)] * 7)]


def props_scatter(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """빌딩 숲이 하나씩 땅으로 가라앉고 그 자리에 나무가 자라는 푸른 들판."""
    for j, (x, y, w, h, c) in enumerate(BLDS):
        f = smooth(ramp(tau, 0.1 + 0.025 * j, 0.1 + 0.025 * j + dur * 0.4))
        hh = h * (1.0 - f)
        if hh > 0.05:
            F.b((x, y, 0.0), (w, w, hh), c)
    for j, (x, y) in enumerate(TREES):
        s = pop(tau - (dur * 0.35 + 0.05 * j), 0.4)
        if s > 0.02:
            F.b((x, y, 0.0), (0.3, 0.3, 0.9 * s), (0.45, 0.30, 0.18))
            F.b((x, y - 0.5, 0.8 * s), (1.3 * s, 1.3 * s, 1.1 * s), (0.22, 0.52, 0.22))


def props_green(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """남는 초록 대륙(지도판)을 하늘색으로 반짝이는 테두리로 가리킴."""
    p = 0.6 + 0.4 * math.sin(2 * math.pi * t / 0.7)
    for dy in (-1, 1):
        G.b((-0.2, -0.45 + dy * 0.45 + 0.45 - 0.0, 0.88), (1.5, 0.03, 0.03), (0.4 * p, 2.2 * p, 3.0 * p))
    for dx in (-1, 1):
        G.b((-0.2 + dx * 0.75, -0.45, 0.88), (0.03, 0.9, 0.03), (0.4 * p, 2.2 * p, 3.0 * p))


def props_icons(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """수도꼭지와 쓰레기봉투 아이콘이 나란히 번갈아 깜박."""
    a = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(2 * math.pi * t / 0.8))
    b = 0.45 + 0.55 * (0.5 - 0.5 * math.sin(2 * math.pi * t / 0.8))
    srows(G, cam, FAUCET, -0.38, 0.0, 0.032, (0.5 * a, 1.8 * a, 3.0 * a), 1.8)
    srows(G, cam, BAG, 0.38, 0.0, 0.032, (0.5 * b, 2.6 * b, 0.9 * b), 1.8)


def props_help(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    metro_crowd(F, t, 14, skip=(-1.8, 3.0, -1.6, 0.9))


def props_ask(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    wdig(G, DIG["?"], 0.62, 0.8, 1.75 + 0.05 * math.sin(2 * math.pi * t / 1.1), 0.20, (3.0, 2.6, 0.9), pop(tau - 0.3, 0.3))


def props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    OR.orb((0.0, 110.0, 5.0), 12.0, (3.0, 1.5, 0.5))
    OR.orb((0.0, 116.0, 5.0), 24.0, (1.3, 0.55, 0.25))


DINOC = (0.10, 0.07, 0.12)


def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    """공룡 실루엣 티저 (저녁 해 앞, 꼬리가 천천히 흔들림)."""
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    s = pop(tau - 0.1, 0.5)
    sw = 0.18 * math.sin(2 * math.pi * t / 1.6)
    F.b((-0.1, 5.4, 1.7), (3.0 * s, 1.2, 1.5 * s), DINOC)
    F.c((-2.7, 6.0, 2.4 * s), (2.2, 0.8, 0.9 * s), DINOC, (0.0, 0.05, sw))
    F.c((-4.7 + 0.3 * sw * 3, 6.0, 2.5 * s), (1.8, 0.5, 0.6 * s), DINOC, (0.0, 0.1, sw * 1.8))
    for lx in (-0.3, 0.8):
        F.b((lx, 5.5, 0.0), (0.6, 0.6, 1.75 * s), DINOC)
        F.b((lx + 0.15, 5.5, 0.0), (0.9, 0.7, 0.18), DINOC)
    F.b((1.1, 5.6, 2.9 * s), (0.6, 0.8, 1.5 * s), DINOC)
    F.b((1.55, 5.45, 4.0 * s), (1.5, 1.1, 0.9 * s), DINOC)
    F.b((1.55, 5.45, 3.7 * s), (1.2, 1.0, 0.3), (0.16, 0.10, 0.14))
    F.b((0.95, 5.35, 2.7 * s), (0.5, 0.3, 0.2), DINOC)
    G.b((1.9, 5.40, 4.65 * s), (0.12, 0.05, 0.12), (3.0, 2.4, 0.6))


PROPS = {LN["hook"]: props_hook, LN["density"]: props_density, LN["jakarta"]: props_jakarta, LN["need190"]: props_need190,
         LN["metro"]: props_metro, LN["tap"]: props_tap, LN["dry"]: props_dry, LN["dam"]: props_dam, LN["trash"]: props_trash,
         LN["trucks"]: props_trucks, LN["mount"]: props_mount, LN["map"]: props_map, LN["twist"]: props_twist,
         LN["pie55"]: props_pie55, LN["night"]: props_night, LN["pie68"]: props_pie68, LN["scatter"]: props_scatter,
         LN["green"]: props_green, LN["icons"]: props_icons, LN["help"]: props_help, LN["ask"]: props_ask, LN["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR, BL, LT = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off), Items(N_BL, off), []
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
def jh_metro(tau, t):
    """지하철에서 인파에 밀려 한 바퀴 돎."""
    a, b = shot_span(LN["metro"])
    return dict(yaw=-90.0 + 360.0 * smooth(ramp(tau, 0.3, (b - a) * 0.8)), x=0.3 * math.sin(2 * math.pi * t / 0.9),
                pose="shock" if int(t / 0.4) % 2 else "confused")


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    add("jh", 0, JH_SH, JH_PA, {
        L["hook"]: st("city", 0.0, 0.0, -90, "gape", alt=("gape", "aw_up", 0.45, 0.0)),
        L["density"]: st("city", -0.3, 0.0, -90, "point", seq=[(1.0, "smile")]),
        L["forest"]: st("city", 0.0, 0.0, -90, "aw_up"),
        L["jakarta"]: st("city", 0.9, 0.0, -90, "point", seq=[(1.2, "smile")]),
        L["metro"]: st("metro", 0.0, 0.0, -90, "confused", fn=jh_metro, also=("shock", "confused")),
        L["twist"]: st("map", -1.3, 2.0, -90, "smile", seq=[(1.0, "gape")]),
        L["map"]: st("map", -1.3, 2.0, -90, "carry", seq=[(1.0, "smile")]),
        L["night"]: st("city", 0.0, 0.0, -90, "look_up_h"),
        L["pie68"]: st("city", 0.0, 0.0, -90, "smile", sway=(10.0, 3.0, 0.0)),
        L["scatter"]: st("field", 0.0, 0.0, -90, "aw_up", seq=[(1.5, "smile")]),
        L["help"]: st("metro", -0.1, -0.5, -60, "carry", seq=[(1.4, "smile")]),
        L["ask"]: st("field", 0.0, 0.0, -90, "think", seq=[(0.9, "smile")])}, extra="hood")
    add("rs", 1, CO_SH, CO_PA, {
        L["map"]: st("map", 1.3, 2.0, -90, "point", alt=("point", "think", 1.1, 0.3)),
        L["twist"]: st("map", 1.3, 2.0, -90, "point", alt=("point", "think", 1.1, 0.3)),
        L["green"]: st("map", 1.4, 2.3, -90, "point", alt=("point", "smile", 0.9, 0.0))}, extra="coat")
    add("cz", 0, CZ_SH, CZ_PA, {
        L["help"]: st("metro", 0.3, -0.5, 0, "lie", z=0.04,
                      keys=[(0.0, (0.3, -0.5, 0.04, 0.0)), (1.3, (0.3, -0.5, 0.04, 0.0)), (1.45, (1.1, -0.5, 0.0, -90.0))],
                      seq=[(1.4, "stand"), (2.0, "smile")])})
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
NIGHT_SKY = ((0.01, 0.015, 0.05), (0.06, 0.08, 0.18), 0.0)
SPACE_SKY = ((0.003, 0.004, 0.014), (0.010, 0.013, 0.034), 1.8)
ROOM_SKY = ((0.04, 0.05, 0.09), (0.10, 0.12, 0.18), 0.0)


def sky(t):
    i = line_at(t)
    s = cam_of(t)["set"]
    if s == "space":
        return SPACE_SKY
    if s == "map":
        return ROOM_SKY
    if i in (LN["night"], LN["pie68"]):
        return NIGHT_SKY
    if i in (LN["ask"], LN["teaser"]):
        return DUSK_SKY
    return DAY_SKY


def env(i, st_):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if st_ == "city" and i in (LN["night"], LN["pie68"]):
        e.update(sun=0.5, sun_col=(0.55, 0.65, 1.0), sun_rot=(60, 0, 20), amb=0.26, amb_col=(0.35, 0.42, 0.75), lt={"ep44_city0": 260.0})
    elif st_ == "field" and i in (LN["ask"], LN["teaser"]):
        e.update(sun=2.4, sun_col=(1.0, 0.62, 0.38), sun_rot=(72, 0, 20), amb=0.30, amb_col=(0.72, 0.52, 0.62))
    elif st_ == "space":
        e.update(sun=4.2, sun_col=(1.0, 0.96, 0.9), sun_rot=(55, 0, 60), amb=0.08, amb_col=(0.30, 0.36, 0.62))
    elif st_ == "map":
        e.update(sun=0.5, amb=0.45, amb_col=(0.80, 0.82, 0.90), lt={"ep44_map0": 170.0, "ep44_map1": 100.0})
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


def build(ctx):
    from engine import bkit as K
    v = X.Vox(44)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep44_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep44_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep44_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep44_fx", K.proto(ctx, "ep44_p_fx", cube(), [K.mat_inst("ep44_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep44_glow", K.proto(ctx, "ep44_p_glow", cube(), [_mat_glow("ep44_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep44_orb", K.proto(ctx, "ep44_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep44_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep44_bl", K.proto(ctx, "ep44_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep44_m_bl", 0.8)]),
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
