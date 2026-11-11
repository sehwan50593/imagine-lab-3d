"""EP46 만약에 지구가 정육면체라면? (기준 영상 형식 STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

11-06 오너: 42~49는 '남자가 한 명뿐이라면' 편 형식으로, 내레이션 없이. 소리는 배경음(-23 LUFS)과 효과음뿐.
장면(3D)은 11-05 픽세판 그대로(꼭짓점 산·대각 단면·바다 면·평평한 면·홀로그램 별·지구본·창가), 줄 순서도 그대로(이미 시간순).
D-DAY(꼭짓점 2,523km, 에베레스트 285배) → 바로(면 중앙 1,236km 아래, 바다가 모임, 꼭짓점 중력 약함) → +1주(공기도 낮은 곳으로)
→ 왜?(바위 천체는 반지름 400km 넘으면 둥글어짐) → 결국(무너짐) → 반전(화성 올림푸스산도 22km뿐) → 지금(적도 21km 불룩) → 다음 편(모기).

근거(설명란): ※ '지금 지구와 같은 부피의 균질한 정육면체' 가정의 상상 시나리오. 산·모형·그림의 크기와 비율은 연출.
바닷물·공기가 면 중앙으로 흐르고 꼭짓점 중력이 약하다는 설명은 물리 추론(점질량 근사)이며 숫자를 쓰지 않았다.
· 지구 평균 반지름 6,371km → 같은 부피 정육면체 한 변 약 10,270km(계산) · NASA NSSDC Earth Fact Sheet
· 꼭짓점은 중심에서 8,894km → 해수면보다 약 2,523km 높음, 면 중앙 5,135km → 1,236km 낮음(계산)
· 에베레스트 8,848.86m(2020 중·네팔 측량)의 약 285배, 국제우주정거장 고도 약 400km의 약 6배(계산) · NASA
· 바위 천체는 반지름 약 400km를 넘으면 자체 중력으로 둥글어짐(연구마다 200~500km) · Astronomy 2017, Big Think
· 화성 올림푸스산 약 21.9km · NASA MOLA
· 적도가 극보다 약 21km 불룩(6,378.137 − 6,356.752km) · NASA NSSDC
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"peak": (0, 0), "summit": (300, 0), "diag": (600, 0), "sea": (900, 0), "flat": (1200, 0), "field": (1500, 0),
       "holo": (1800, 0), "globe": (2100, 0), "window": (2400, 0)}
NAMES = ("hook", "wire", "cloud", "evr", "iss", "summit", "dent", "lake", "float", "jump", "air", "holo", "erode", "twist", "crumble",
         "round", "oblate", "tape", "spin", "walk", "dusk", "ask", "mosq")
LN = {n: k for k, n in enumerate(NAMES)}

# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
H_A = ("peak", (0.0, 0.0, 1.9), -90, 3, 5.5, 28, 1.0, 0, 0.0, -8)
DG_A = ("diag", (0.0, 6.9, 3.2), -90, 2, 10.0, 26, 0.92, 3, 0.0)
LINES = [
    dict(d=3.0, sub="지구가 같은 부피의\n정육면체라면?", ease="out", shot=H_A),
    dict(d=3.2, sub="꼭짓점은 지금 해수면보다\n2,523km 높습니다.", shot=DG_A),
    dict(d=3.0, sub="꼭짓점 산은 구름을\n한참 뚫고 솟습니다.", shot=("peak", (0.0, 0.0, 3.0), -90, -10, 8.0, 28, 1.15, 0, 0.0)),
    dict(d=2.8, sub="에베레스트보다\n약 285배 높습니다.", shot=("peak", (0.9, 3.0, 0.5), -88, 6, 3.8, 28, 3.0, 4, 0.04)),
    dict(d=2.9, sub="국제우주정거장보다도\n6배 높습니다.", shot=("peak", (1.5, 5.0, 8.0), -90, 3, 9.0, 26, 5.5, 0, 0.0)),
    dict(d=2.9, sub="그 높이엔 숨 쉴 공기가\n거의 없습니다.", shot=("summit", (0.0, 0.0, 1.4), -90, 5, 5.2, 28, 0.92, 3, 0.05)),
    dict(d=3.1, sub="면 한가운데는 지금보다\n1,236km 낮습니다.", shot=("diag", (0.0, 6.9, 3.2), -90, 2, 10.0, 26, 0.92, -3, 0.0)),
    dict(d=2.7, sub="그래서 바닷물은\n면 가운데로 모입니다.", shot=("sea", (0.0, 11.0, 1.0), -88, 16, 32.0, 26, 0.9, 3, 0.0)),
    dict(d=2.9, sub="꼭짓점은 중심에서 멀어\n중력이 약합니다.", shot=("flat", (0.0, 0.0, 1.4), -90, 4, 6.0, 28, 0.9, 3, 0.06)),
    dict(d=2.6, sub="지후는 점프 한 번에\n한참 떠 있습니다.", shot=("flat", (0.0, 0.0, 2.8), -90, 4, 12.0, 24, 0.95, 0, 0.0, 6)),
    dict(d=3.1, sub="공기도 낮은 곳에 몰려\n꼭짓점은 텅 빕니다.", shot=("sea", (0.0, 16.0, 3.0), -88, 14, 30.0, 26, 0.92, 3, 0.0)),
    dict(d=3.3, sub="바위 천체는 반지름이 400km를\n넘으면 스스로 둥글어집니다.", shot=("holo", (0.0, 0.0, 1.5), -90, 4, 8.0, 32, 0.92, 3, 0.04)),
    dict(d=2.6, sub="정육면체 별은 결국\n스스로 무너집니다.", shot=("holo", (0.0, 0.0, 2.0), -90, 6, 7.0, 28, 0.9, 5, 0.03)),
    dict(d=3.6, sub="화성의 올림푸스산도\n약 22km뿐입니다.", shot=("peak", (1.7, 3.2, 1.2), -85, 5, 7.0, 28, 1.4, 4, 0.05)),
    dict(d=2.6, sub="그 높이는 바위가\n버티지 못합니다.", shot=("peak", (0.0, 12.0, 40.0), -90, -6, 26.0, 26, 0.9, 3, 0.0)),
    dict(d=2.7, sub="깎인 정육면체가\n점점 둥글어집니다.", shot=("holo", (0.0, 0.0, 2.0), -55, 8, 7.0, 28, 0.9, -8, 0.03)),
    dict(d=2.6, sub="지금 지구도\n완벽한 구는 아닙니다.", shot=("diag", (0.0, 6.9, 3.2), -90, 2, 9.5, 26, 0.9, 3, 0.0)),
    dict(d=3.0, sub="적도가 극보다\n약 21km 불룩합니다.", shot=("globe", (0.1, 0.0, 1.4), -90, 4, 6.0, 28, 0.9, 3, 0.03)),
    dict(d=2.9, sub="그래도 지구는\n거의 완벽한 공 모양입니다.", shot=("globe", (-0.5, 0.0, 1.5), -80, 5, 4.2, 28, 0.9, -3, 0.03)),
    dict(d=3.2, sub="둥근 덕분에 어디서나\n비슷한 높이에서 삽니다.", shot=("field", (0.0, 6.0, 1.0), -90, 4, 9.0, 26, 0.92, 0, 0.04)),
    dict(d=3.3, sub="평평한 길을 걷는 것도\n지구의 선물이죠.", shot=("window", (0.0, 4.0, 1.6), -90, 4, 6.5, 28, 0.9, 3, 0.03)),
    dict(d=2.8, sub="댓글로 알려 주세요.", shot=("window", (0.0, 2.0, 1.4), -90, 4, 4.8, 28, 0.92, 3, 0.03)),
    dict(d=3.6, sub="모기가 없으면\n세상은 더 좋아질까요?", shot=("window", (0.0, 3.0, 1.6), -90, 0, 2.4, 28, 0.9, 0, 0.0)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="D-DAY", label="정육면체 지구의 꼭짓점", big="높이 2,523km", label_color="blue", big_color="red"),
    dict(at="evr", badge="D-DAY", title="에베레스트의", big="285배", big_color="yellow"),
    dict(at="dent", badge="바로", title="면 한가운데는", big="1,236km 아래", big_color="cyan"),
    dict(at="air", badge="+1주", title="공기도 {cyan}낮은 곳{/}으로"),
    dict(at="holo", badge="왜?", title="바위 천체는 반지름", big="400km 넘으면 둥글다", big_color="green"),
    dict(at="erode", badge="결국", title="정육면체 지구는", big="스스로 무너진다", big_color="orange"),
    dict(at="twist", badge="반전", title="화성 최고봉 올림푸스산도", big="22km뿐", big_color="orange"),
    dict(at="oblate", badge="지금", title="지금 지구도", big="적도가 21km 불룩", big_color="cyan"),
    dict(at="walk", badge="지금", title="둥근 지구의 {green}선물{/}"),
    dict(at="ask", badge="지금", title="꼭짓점과 면 중앙\n{cyan}어디서{/} 살래요?", title_size=70),
    dict(at="mosq", badge="다음 편", title="오늘 저녁 7시\n{cyan}모기가 전부 사라진다면?{/}", title_size=64),
]
TWIST = LN["twist"]  # 올림푸스도 22km뿐 — 꼭짓점 2,523km와 비교하는 반전 줄
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
META = {"id": "ep46", "title": "만약에 지구가 정육면체라면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"style": "mystery", "key": "Ab", "mode": "major", "bpm": 100, "seed": 461, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, [[STARTS[LN["crumble"]] + 0.1, "rumble", 0.55, 2.2]])}}
GRADE = {"exposure": 0.95, "bloom": 0.10, "bloom_thr": 1.4, "vignette": 0.14}


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
        return [(0.0, 99.0, 0.03, 0.0, 14.0, "hold")]
    if i == LN["crumble"]:
        return [(0.45, 1.8, 0.05, 0.5, 12.0, "hit")]
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

GRASS = (0.34, 0.58, 0.26)
SKINC = X.SKIN
DUSTC = (0.86, 0.80, 0.66)
OCEAN = (0.08, 0.26, 0.68)
RE = 1.7                                    # 지구 반지름 (그림 크기, 실제 비율 아님)
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



# ───────────────────────── 새 자세 · 우주복 헬멧 ─────────────────────────
KINDS.update({"both": dict(base="stand", arms=((0.0, -1.3), (0.0, 1.3)), mouth="smile"),     # 두 팔을 양옆으로 벌려 각각 가리킴
              "look_dn": dict(base="stand", head=0.35)})                                      # 고개를 숙여 내려다봄
for _k in ("both", "look_dn"):
    _sp = KINDS[_k]
    ARMS[_k] = tuple(a[0] for a in _sp["arms"]) if _sp.get("arms") else ARMS[_sp["base"]]
    ROLLS[_k] = tuple(a[1] for a in _sp["arms"]) if _sp.get("arms") else (0.0, 0.0)


def _person_parts(pose, hair, extra=""):
    """표준 자세면 voxel 원형, 새 자세면 _variant. extra: 'hood'(지후 후드) · 'coat'(연구원 흰 가운) · 'suit'(우주복 헬멧: 얼굴 앞은 열림)."""
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
    elif extra == "suit":                                          # 하얀 헬멧(윗판·뒤판·옆판·앞 위쪽 테) + 등 산소통
        P.append((K.bm_cube(0.62, 0.62, 0.10, (-0.01, 0, hz + 0.43), bottom=True), 4))
        P.append((K.bm_cube(0.08, 0.62, 0.62, (-0.33, 0, hz - 0.06), bottom=True), 4))
        for sy in (-0.30, 0.30):
            P.append((K.bm_cube(0.58, 0.07, 0.62, (-0.01, sy, hz - 0.06), bottom=True), 4))
        P.append((K.bm_cube(0.06, 0.62, 0.06, (0.28, 0, hz + 0.38), bottom=True), 4))
        P.append((K.bm_cube(0.20, 0.36, 0.55, (-0.20, 0, hip + 0.05), bottom=True), 4))
    return P


# ───────────────────────── 색 · 산 · 구름 ─────────────────────────
ROCK = (0.46, 0.41, 0.37)
GOLD = (3.0, 2.5, 0.6)
HOLO, HOLO2 = (0.30, 1.45, 1.95), (0.22, 1.10, 1.60)
CLOUD = (0.88, 0.91, 0.96)
WATER = (0.10, 0.38, 0.88)
WATERB = (0.20, 0.52, 1.0)
AIRC = (0.95, 0.97, 1.0)
PK_C = (0.0, 22.0)           # 꼭짓점 산 중심 (세트 좌표)
PK_N, PK_H = 16, 3.0         # 16단 x 3m = 48m (2,523km에 해당하는 그림 높이)


def tier_geo(j):
    h = 0.5 + 13.5 * (1.0 - (j + 0.5) / PK_N)
    return PK_C[0] + 0.35 * math.sin(1.7 * j), PK_C[1] + 0.40 * math.cos(2.3 * j), h, 0.92 * h


def tier_col(j):
    k = j / (PK_N - 1.0)
    g = 1.0 + 0.06 * math.sin(j * 3.1)
    return (lerp(0.40, 0.62, k) * g, lerp(0.35, 0.57, k) * g, lerp(0.31, 0.53, k) * g)


_rp = np.random.default_rng(4601)
PUFFS = []
for _zc in (9.0, 17.0, 27.0):                       # 구름 띠 세 층 (같은 높이 평면이 겹치지 않게 z를 조금씩 비껴 놓음)
    for _q in range(18):
        PUFFS.append((float(_rp.uniform(-48, 48)), float(_rp.uniform(9, 75)), _zc + float(_rp.uniform(-0.7, 0.7)),
                      float(_rp.uniform(5, 11)), float(_rp.uniform(3, 6))))
PEAK_BOX = []                                       # 카메라가 상자 안으로 들어가지 않는지 점검용


def _peak(v):
    v.floor(-70, 70, -60, 100, (0.40, 0.37, 0.34), 2.5)
    for j in range(12):                              # 아래 12단은 세트, 위 4단은 매 프레임 덩어리로
        cx, cy, hx, hy = tier_geo(j)
        box = (cx - hx, cx + hx, cy - hy, cy + hy, PK_H * j, PK_H * j + PK_H)
        v.box(*box, tier_col(j), jit=0.05)
        PEAK_BOX.append(box)
    for x, y, z, w, d in PUFFS:
        box = (x - w / 2, x + w / 2, y - d / 2, y + d / 2, z, z + 1.3)
        v.box(*box, CLOUD, jit=0.03)
        PEAK_BOX.append(box)


def peak_top(F, ft=None):
    """위 4단(12~15)을 3x3 덩어리로. ft = 금 간 뒤 떨어지기 시작하는 τ(None이면 멀쩡). 덩어리 사이 틈이 금."""
    for j in range(12, PK_N):
        cx, cy, hx, hy = tier_geo(j)
        for a in range(3):
            for b in range(3):
                x, y, z = cx + (a - 1) * 2 * hx / 3, cy + (b - 1) * 2 * hy / 3, PK_H * j + PK_H / 2
                if ft is not None:
                    s = max(0.0, ft - (0.35 + 0.16 * (PK_N - 1 - j) + 0.05 * (a + 3 * b)))
                    z -= 7.0 * s * s
                    x += (a - 1) * 2.4 * s
                    y -= (0.6 + 0.9 * b / 2.0) * s
                F.b((x, y, z), (0.96 * 2 * hx / 3, 0.96 * 2 * hy / 3, PK_H * 0.98), tier_col(j + ((a + b) % 2) * 0.6))
    if ft is not None and ft > 0.7:                  # 부서질 때 먼지 덩이
        k = ramp(ft, 0.7, 2.2)
        for q in range(12):
            a = 2 * math.pi * q / 12 + 0.4
            r = 1.0 + 4.0 * k
            sz = (1.1 + 1.2 * _h(q)) * (1.0 - 0.5 * k)
            F.b((PK_C[0] + r * math.cos(a), PK_C[1] - 2.0 + 0.6 * r * math.sin(a), 40.0 + 2.0 * _h(q + 9) - 3.0 * k), (sz, sz, sz), CLOUD)


def cloud_drift(F, t):
    """앞쪽을 빠르게 지나가는 구름 9개 (0.0초부터 움직임)."""
    for q in range(9):
        x = ((q * 13.7 + 6.0 * t) % 64.0) - 32.0
        F.b((x, 2.5 + 0.35 * (q % 4), 3.0 + 0.9 * q), (4.0 + (q % 3), 1.8, 0.9), CLOUD)


def iss_model(F, G, c, k):
    """우주정거장 아이콘: 트러스 + 태양전지판 넷 + 모듈. k = 크기."""
    F.b(c, (2.4 * k, 0.14 * k, 0.14 * k), (0.85, 0.85, 0.88))
    F.b((c[0], c[1], c[2] + 0.02 * k), (0.5 * k, 0.32 * k, 0.30 * k), (0.92, 0.92, 0.9))
    for sx in (-1, 1):
        for sz in (-1, 1):
            F.b((c[0] + sx * 0.9 * k, c[1], c[2] + sz * 0.47 * k), (0.55 * k, 0.03 * k, 0.78 * k), (0.15, 0.25, 0.62))
    for q in range(14):                              # 눈에 띄게 하는 청록 고리
        a = 2 * math.pi * q / 14
        G.b((c[0] + 1.7 * k * math.cos(a), c[1] - 0.2 * k, c[2] + 1.7 * k * math.sin(a)), (0.12 * k, 0.05 * k, 0.12 * k), (0.4, 1.3, 1.5))


# ── 사다리꼴 비탈 (바다·공기 세트): 4m 계단 8개, 높이 1.5m씩
def ramp_z(y):
    return 0.0 if y < 8.0 else 1.5 * min(int((y - 8.0) // 4.0) + 1, 8)


def _sea(v):
    v.floor(-40, 40, -60, 100, (0.40, 0.37, 0.34), 2.5)
    for k in range(8):
        g = 1.0 + 0.05 * math.sin(k * 2.7)
        v.box(-14, 14, 8 + 4 * k, 12 + 4 * k, 0, 1.5 * (k + 1), (0.46 * g, 0.41 * g, 0.37 * g), jit=0.05)
    v.box(-14, 14, 40, 70, 0, 12.0, (0.50, 0.45, 0.40), jit=0.05)
    for j, (hw, z0) in enumerate(((5.0, 12.0), (3.4, 15.0), (1.9, 18.0), (0.8, 21.0))):       # 꼭짓점 뾰족바위
        v.box(-hw + 0.15 * j, hw + 0.15 * j, 52 - hw, 52 + hw, z0, z0 + 3.0, (0.55 + 0.03 * j, 0.50 + 0.03 * j, 0.45 + 0.03 * j), jit=0.05)


_rw = np.random.default_rng(4602)
NW = 220
WX, WR, WV = _rw.uniform(-9.0, 9.0, NW), _rw.uniform(0.0, 1.0, NW), _rw.uniform(0.7, 1.3, NW)
WY2, WZ2 = _rw.uniform(-2.0, 6.0, NW), _rw.uniform(0.0, 1.0, NW)


# ───────────────────────── 세트 ─────────────────────────
def _stars(v, n, seed):
    rs = np.random.default_rng(seed)
    for k in range(n):
        d = rs.normal(size=3)
        d = d / np.linalg.norm(d)
        r = float(rs.uniform(70, 100))
        s = float(rs.uniform(0.25, 0.6))
        c = ((0.95, 0.95, 1.0), (1.0, 0.9, 0.6), (0.6, 0.75, 1.0))[k % 3]
        x, y, z = d * r
        v.box(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z - s / 2, z + s / 2, c, jit=0, glow=True)


def _summit(v):
    v.floor(-14, 14, -10, 14, (0.50, 0.45, 0.41), 1.0)
    rs = np.random.default_rng(4603)
    for k in range(14):                              # 정상 둘레 바위
        x = float(rs.uniform(-13, 13))
        y = float(rs.uniform(5, 13))
        w = float(rs.uniform(0.8, 2.0))
        v.box(x - w, x + w, y - w, y + w, 0, float(rs.uniform(0.5, 1.8)), ROCK, jit=0.06)
    _stars(v, 260, 4604)


def _diag(v):
    v.floor(-14, 14, -14, 7.5, (0.30, 0.36, 0.50), 1.0, "check")
    v.wall((-14, 7.0), (14, 7.0), 0, 10, (0.17, 0.27, 0.46), 1.0, face=-1)
    v.light(0.0, 2.0, 7.0, 190, (0.9, 0.95, 1.0), 1.0, "ep46_di0")
    v.light(-4.0, -2.0, 4.0, 110, (1.0, 0.95, 0.9), 0.8, "ep46_di1")


def _flat(v):
    v.floor(-40, 40, -40, 80, (0.44, 0.40, 0.37), 2.0)
    rs = np.random.default_rng(4605)
    for k in range(18):
        x = float(rs.uniform(-30, 30))
        y = float(rs.uniform(10, 60))
        w = float(rs.uniform(0.8, 2.2))
        v.box(x - w, x + w, y - w, y + w, 0, float(rs.uniform(0.6, 2.4)), ROCK, jit=0.06)
    _stars(v, 120, 4606)


def _field(v):
    v.floor(-70, 90, -10, 125, GRASS, 2.5)
    rs = np.random.default_rng(4607)
    for k in range(14):                              # 먼 언덕 (y를 조금씩 비껴 놓음)
        x0 = -130 + 22 * k
        h = float(rs.uniform(5, 14))
        v.box(x0, x0 + 26, 128 + 3.1 * (k % 4), 150 + 3.1 * (k % 4), 0, h, (0.28 + 0.03 * (k % 3), 0.46, 0.34 + 0.02 * (k % 2)), jit=0.05)
    v.box(-1.5, 1.5, -6.0, 90.0, 0.0, 0.03, (0.50, 0.50, 0.53), jit=0.02)          # 평평한 길
    for k in range(10):
        X.tree(v, (-1 if k % 2 else 1) * (5.0 + 1.3 * (k % 3)), 6.0 + 7.0 * k + 0.4 * (k % 2), 3.0 + 0.3 * (k % 3))


def _holo(v):
    v.floor(-9, 9, -12, 6, (0.34, 0.40, 0.52), 1.0, "check")
    v.wall((-9, 6), (9, 6), 0, 7, (0.22, 0.32, 0.50), 1.0, face=-1)
    v.box(-1.9, 1.9, -0.8, 0.8, 0.0, 0.8, (0.80, 0.82, 0.86))
    v.box(-1.8, 1.8, -0.75, 0.75, 0.8, 0.84, (0.25, 0.30, 0.38), jit=0)
    v.box(-8, 8, 5.93, 5.99, 0.3, 0.34, (0.35, 0.8, 1.0), jit=0, glow=True)
    v.light(0.0, 1.0, 6.0, 200, (0.9, 0.95, 1.0), 1.0, "ep46_ho0")
    v.light(-3.0, -2.0, 4.5, 120, (1.0, 0.95, 0.9), 0.8, "ep46_ho1")


def _globe(v):
    v.floor(-8, 8, -9, 6, (0.58, 0.40, 0.26), 1.0, "wood")
    v.wall((-8, 6), (8, 6), 0, 6, (0.62, 0.52, 0.42), 1.0, face=-1)
    v.box(-2.4, 2.4, -1.4, 1.4, 0.72, 0.80, (0.60, 0.42, 0.26))
    for sx in (-2.2, 2.2):
        for sy in (-1.2, 1.2):
            v.box(sx - 0.1, sx + 0.1, sy - 0.1, sy + 0.1, 0.0, 0.72, (0.45, 0.31, 0.20))
    v.light(0.0, 0.0, 5.0, 200, (1.0, 0.93, 0.82), 1.0, "ep46_gl0")
    v.light(-3.0, -3.0, 3.5, 110, (1.0, 0.92, 0.8), 0.8, "ep46_gl1")


def _window(v):
    v.floor(-5, 5, -5, 6, (0.58, 0.40, 0.26), 1.0, "wood")
    wall = (0.70, 0.55, 0.50)
    v.wall((-6, 6), (-1.2, 6), 0, 3.6, wall, 0.6, face=-1)
    v.wall((1.2, 6), (6, 6), 0, 3.6, wall, 0.6, face=-1)
    v.wall((-1.2, 6), (1.2, 6), 0, 1.0, wall, 0.6, face=-1)
    v.wall((-1.2, 6), (1.2, 6), 2.6, 3.6, wall, 0.6, face=-1)
    fr = (0.95, 0.93, 0.88)
    v.box(-1.35, 1.35, 5.72, 6.08, 0.94, 1.0, fr, jit=0)
    v.box(-1.26, -1.2, 5.88, 5.97, 1.0, 2.6, fr, jit=0)
    v.box(1.2, 1.26, 5.88, 5.97, 1.0, 2.6, fr, jit=0)
    v.box(-0.03, 0.03, 5.9, 5.96, 1.0, 2.6, fr, jit=0)
    v.box(-1.26, 1.26, 5.88, 5.97, 2.6, 2.66, fr, jit=0)
    v.floor(-14, 14, 6.1, 80, (0.40, 0.32, 0.30), 2.0, z=-4.0)               # 골목 바닥
    rs = np.random.default_rng(4608)
    for side in (-1, 1):
        for k in range(10):                                                 # 골목 양쪽 집 (높이·색이 제각각)
            y0 = 9.0 + 5.2 * k + 0.4 * side
            x0, x1 = sorted((side * 3.0, side * (7.0 + float(rs.uniform(0, 2.5)))))
            h = float(rs.uniform(1.0, 5.0))
            v.box(x0, x1, y0, y0 + 4.5, -4.0, h, (0.58 + 0.08 * float(rs.random()), 0.42 + 0.06 * float(rs.random()), 0.40), jit=0.05)
    v.light(0.0, 1.0, 3.2, 150, (1.0, 0.85, 0.65), 0.6, "ep46_wi0")
    v.light(-2.0, -2.5, 2.5, 80, (1.0, 0.9, 0.75), 0.6, "ep46_wi1")


def _sets():
    return (("peak", _peak), ("summit", _summit), ("diag", _diag), ("sea", _sea), ("flat", _flat), ("field", _field),
            ("holo", _holo), ("globe", _globe), ("window", _window))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 1900, 900, 40, 40


def sp_of(t):
    return 0.35 * t


def earth_items(F, BL, cam, center, R, sp):
    """지구본: 파란 구(조명 받음) + 앞쪽 반구에 보이는 땅·극지 조각(자전 sp). center = 지금 세트 좌표."""
    ox, oy = OFF[cam["set"]]
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


def _ph(i, tau):
    a, b = shot_span(i)
    return clamp(tau / max(b - a, 1e-3))


# 올라가는 카메라: 목표점이 시간에 따라 움직이는 컷
TRACK[(LN["hook"], 0)] = lambda tau: (0.0, 11.0 * smooth((tau - 0.3) / 2.6), 1.9 + 41.0 * smooth((tau - 0.3) / 2.6))      # 0.3초 머문 뒤 위로
TRACK[(LN["cloud"], 0)] = lambda tau: (0.0, 5.0 * smooth(_ph(LN["cloud"], tau)), 3.0 + 17.0 * smooth(_ph(LN["cloud"], tau)))
TRACK[(LN["iss"], 0)] = lambda tau: (1.5, 5.0 + 4.0 * smooth(_ph(LN["iss"], tau)), 8.0 + 5.5 * smooth(_ph(LN["iss"], tau)))


# ── 소품 함수 (줄마다)
def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    cloud_drift(F, t)
    peak_top(F)


def props_evr(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    peak_top(F)
    for k, (w, z0) in enumerate(((0.40, 0.0), (0.26, 0.06), (0.13, 0.12))):          # 에베레스트 점 모형 (산 높이의 1/285 → 0.17m)
        F.b((1.3, 3.1, z0 + 0.03), (w, w, 0.06), (0.62 + 0.04 * k, 0.60 + 0.04 * k, 0.58 + 0.04 * k))
    b = 0.05 * math.sin(2 * math.pi * t / 0.6)
    G.b((1.3, 3.1, 0.52 + b), (0.04, 0.04, 0.18), GOLD)
    G.b((1.3, 3.1, 0.38 + b), (0.16, 0.04, 0.07), GOLD)


def props_iss(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    peak_top(F)
    iss_model(F, G, (1.5, 5.0, 7.6), 1.3)


def props_summit(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    F.b((-1.6, 0.3, 1.2), (0.5, 0.06, 1.4), (0.18, 0.18, 0.20))
    fill = max(0.0, 1.0 - 1.2 * u)
    blink = 0.6 + 0.4 * math.sin(2 * math.pi * t / 0.4)
    if fill > 0.005:
        col = (0.4, 1.7, 0.5) if fill > 0.3 else (2.2 * blink, 0.4, 0.3)
        G.b((-1.6, 0.25, 0.55 + 0.65 * fill), (0.28, 0.03, 1.3 * fill), col)
    else:
        wdig(G, num_rows("0"), -1.6, 0.22, 1.2, 0.18, (2.2 * blink, 0.4, 0.3), pop(tau - 0.5 * dur, 0.3))


def _dots(G, verts, col, frac, step=0.11, sz=0.075, closed=True):
    """벽 위(y=6.9) x-z 평면의 점선: 꼭짓점 목록을 따라 점을 찍되 앞쪽 frac(0~1)만."""
    pts = []
    vs = list(verts) + ([verts[0]] if closed else [])
    for (x0, z0), (x1, z1) in zip(vs[:-1], vs[1:]):
        n = max(1, int(round(math.hypot(x1 - x0, z1 - z0) / step)))
        pts += [(lerp(x0, x1, q / n), lerp(z0, z1, q / n)) for q in range(n)]
    for x, z in pts[:int(len(pts) * clamp(frac))]:
        G.b((x, 6.9, z), (sz, 0.03, sz), col)


def _circ(r, n=76, c=(0.0, 3.2)):
    return [(c[0] + r * math.cos(2 * math.pi * q / n), c[1] + r * math.sin(2 * math.pi * q / n)) for q in range(n)]


DC, DR = (0.0, 3.2), 1.3
C_RING, C_CUBE, C_RED, C_CYAN = (0.7, 1.0, 1.4), (1.4, 1.1, 0.4), (2.2, 0.35, 0.3), (0.3, 1.5, 1.8)


def props_wire(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    _dots(G, _circ(DR), C_RING, ramp(tau, 0.05, dur * 0.4))
    r = 1.396 * DR                                   # 같은 부피 정육면체의 꼭짓점을 지나는 단면 직사각형
    v = [(DC[0] + r * math.cos(math.radians(a)), DC[1] + r * math.sin(math.radians(a))) for a in (90.0, 160.53, 270.0, 340.53)]
    _dots(G, v, C_CUBE, ramp(tau, dur * 0.2, dur * 0.7))
    s = pop(tau - dur * 0.62, 0.3)
    if s > 0.01:
        for q in range(8):                           # 점선(구)을 넘어 튀어나온 부분
            G.b((DC[0], 6.88, DC[1] + DR + (r - DR) * (q + 0.5) / 8), (0.11 * s, 0.05, 0.07 * s), C_RED)


def props_dent(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    _dots(G, _circ(DR), C_RING, 1.0)
    a = 0.806 * DR                                   # 같은 부피 정육면체의 면과 나란한 단면(정사각형), 면 중앙은 구 안쪽
    v = [(DC[0] - a, DC[1] - a), (DC[0] + a, DC[1] - a), (DC[0] + a, DC[1] + a), (DC[0] - a, DC[1] + a)]
    _dots(G, v, C_CUBE, ramp(tau, 0.05, dur * 0.5))
    s = pop(tau - dur * 0.45, 0.3)
    if s > 0.01:
        for sx in (-1, 1):
            for q in range(5):
                G.b((DC[0] + sx * (a + (DR - a) * (q + 0.5) / 5), 6.88, DC[1]), (0.07 * s, 0.05, 0.11 * s), C_CYAN)


def props_oblate(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    b = 0.88 * DR                                    # 적도 불룩함은 눈에 보이게 크게 그림(연출)
    _dots(G, _circ(b), C_RING, ramp(tau, 0.05, dur * 0.4))
    ell = [(DC[0] + DR * math.cos(2 * math.pi * q / 80), DC[1] + b * math.sin(2 * math.pi * q / 80)) for q in range(80)]
    _dots(G, ell, C_CUBE, ramp(tau, dur * 0.2, dur * 0.7), step=0.08)
    s = pop(tau - dur * 0.6, 0.3)
    if s > 0.01:
        for sx in (-1, 1):
            for q in range(4):
                G.b((DC[0] + sx * (b + (DR - b) * (q + 0.5) / 4), 6.88, DC[1]), (0.05 * s, 0.05, 0.12 * s), C_CYAN)


def props_lake(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    h = 0.6 + 2.4 * ramp(tau, 0.0, dur)
    F.b((0.0, 2.0, h / 2), (20.0, 10.0, h), WATER)
    for k in range(NW):                              # 꼭짓점 쪽에서 비탈을 따라 쏟아져 내리는 물방울
        s = (0.34 * tau * WV[k] + WR[k]) % 1.0
        if s > 0.96:
            continue
        y = 40.0 - 33.0 * s
        F.b((WX[k] * (0.3 + 0.7 * s), y, ramp_z(y) + 0.45), (0.55, 0.55, 0.55), WATERB)


def props_air(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    F.b((0.0, 2.0, 1.5), (20.0, 10.0, 3.0), WATER)
    for k in range(NW):                              # 공기 입자: 높은 쪽에서 비탈 아래로 흘러 낮은 곳에 모임 → 위쪽이 비어 감
        s = 0.05 + 0.9 * WR[k] ** 1.3 + 0.20 * tau * WV[k]
        if s < 1.0:
            y = 38.0 - 32.0 * s
            F.b((WX[k] * (0.3 + 0.7 * s), y, ramp_z(y) + 1.2 + 0.3 * math.sin(2 * math.pi * (t * 0.8 + WR[k]))), (0.5, 0.5, 0.5), AIRC)
        else:
            F.b((WX[k] * 0.95, WY2[k], 3.5 + 3.0 * WZ2[k] + 0.2 * math.sin(2 * math.pi * (t * 0.7 + WR[k]))), (0.5, 0.5, 0.5), AIRC)


POTATO = [(0.0, 0.0, 0.0, 0.55, 0.46, 0.40), (0.30, 0.04, 0.10, 0.38, 0.34, 0.36), (-0.28, -0.05, -0.04, 0.40, 0.40, 0.30),
          (0.06, 0.12, -0.20, 0.30, 0.28, 0.22), (-0.05, -0.10, 0.22, 0.33, 0.30, 0.20), (0.35, -0.08, -0.12, 0.22, 0.24, 0.20)]


def props_holo(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for dx, dy, dz, sx, sy, sz in POTATO:            # 감자 모양 작은 천체 (왼쪽)
        F.b((-0.8 + dx, dy, 1.30 + dz), (sx, sy, sz), (0.58, 0.52, 0.46))
    BL.orb((0.8, 0.0, 1.45), 1.15, (0.40, 0.60, 0.90))     # 둥근 천체 (오른쪽)


_G8 = (np.arange(8) + 0.5) / 4.0 - 1.0
GX, GY, GZ = np.meshgrid(_G8, _G8, _G8, indexing="ij")


def holo_cube(G, c, s, m):
    """홀로그램 정육면체: m 0이면 큐브, 1이면 공. (1−m)·최대좌표 + m·거리 ≤ 1 인 칸 중 겉면만 발광 상자로."""
    inside = (1 - m) * np.maximum(np.maximum(abs(GX), abs(GY)), abs(GZ)) + m * np.sqrt(GX ** 2 + GY ** 2 + GZ ** 2) <= 1.0
    pad = np.pad(inside, 1, constant_values=False)
    nb = (pad[:-2, 1:-1, 1:-1] & pad[2:, 1:-1, 1:-1] & pad[1:-1, :-2, 1:-1] & pad[1:-1, 2:, 1:-1] &
          pad[1:-1, 1:-1, :-2] & pad[1:-1, 1:-1, 2:])
    cell = 0.25 * s * 0.92
    for a, b, d in zip(*np.nonzero(inside & ~nb)):
        G.b((c[0] + float(GX[a, b, d]) * s, c[1] + float(GY[a, b, d]) * s, c[2] + float(GZ[a, b, d]) * s), (cell, cell, cell),
            HOLO if (a + b + d) % 2 else HOLO2)


def props_erode(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    holo_cube(G, (0.0, 0.0, 2.1 + 0.04 * math.sin(2 * math.pi * t / 1.6)), 1.05, 0.55 * smooth(tau / dur))


def props_round(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    holo_cube(G, (0.0, 0.0, 2.1 + 0.04 * math.sin(2 * math.pi * t / 1.6)), 1.05, 0.55 + 0.45 * smooth(tau / (dur * 0.9)))


def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    peak_top(F)
    for k, (w, z0) in enumerate(((2.2, 0.0), (1.6, 0.14), (1.0, 0.28))):             # 올림푸스 몬스 모형 (산 높이의 21.9/2523 → 0.42m, 아주 넓적)
        F.b((2.2, 3.2, z0 + 0.07), (w, w, 0.14), (0.58 + 0.03 * k, 0.40 + 0.03 * k, 0.32 + 0.03 * k))
    b = 0.06 * math.sin(2 * math.pi * t / 0.6)
    G.b((2.2, 3.2, 0.95 + b), (0.05, 0.05, 0.22), GOLD)
    G.b((2.2, 3.2, 0.78 + b), (0.20, 0.05, 0.09), GOLD)


def props_crumble(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    peak_top(F, tau)


GL_C, GL_R = (-0.65, 0.0, 1.62), 0.62


def props_tape(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    earth_items(F, BL, cam, GL_C, GL_R, 0.5 * t)
    F.b((GL_C[0], 0.0, 0.83), (0.5, 0.5, 0.06), (0.30, 0.20, 0.12))
    F.b((GL_C[0], 0.0, 0.93), (0.08, 0.08, 0.16), (0.30, 0.20, 0.12))
    F.b((GL_C[0], -GL_R - 0.04, GL_C[2]), (1.7, 0.02, 0.07), (0.95, 0.85, 0.20))        # 줄자
    for q in range(17):
        F.b((GL_C[0] - 0.8 + 0.1 * q, -GL_R - 0.065, GL_C[2]), (0.012, 0.012, 0.05 + (0.04 if q % 5 == 0 else 0.0)), (0.15, 0.15, 0.15))
    s = 0.8 + 0.7 * u                                # 헛도는 돋보기: 점점 커지지만 21km 눈금은 그려지지 않음
    mx, mz = GL_C[0] + 0.5 * math.cos(1.8 * t), GL_C[2] + 0.14 * math.sin(2.2 * t)
    for q in range(18):
        a = 2 * math.pi * q / 18
        G.b((mx + 0.2 * s * math.cos(a), -GL_R - 0.22, mz + 0.2 * s * math.sin(a)), (0.045 * s, 0.03, 0.045 * s), (2.0, 1.9, 1.0))
    F.c((mx + 0.3 * s, -GL_R - 0.22, mz - 0.3 * s), (0.34 * s, 0.045, 0.045), (0.45, 0.30, 0.18), (0.0, 0.785, 0.0))


def props_spin(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    earth_items(F, BL, cam, GL_C, GL_R, 2.6 * t)
    F.b((GL_C[0], 0.0, 0.83), (0.5, 0.5, 0.06), (0.30, 0.20, 0.12))
    F.b((GL_C[0], 0.0, 0.93), (0.08, 0.08, 0.16), (0.30, 0.20, 0.12))


def props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    OR.orb((-6.0, 80.0, 6.0), 12.0, (3.0, 1.5, 0.5))
    OR.orb((-6.0, 86.0, 6.0), 24.0, (1.3, 0.55, 0.25))
    for k in range(4):                               # 노을 구름 띠
        G.b((10.0 - 8.0 * k, 78.0 + 0.7 * k, 11.0 + 1.6 * k), (14.0, 0.2, 0.5), (1.4, 0.7, 0.45))


def props_mosq(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    th = 2 * math.pi * 0.55 * t
    c = np.array((0.5 * math.cos(th), 3.0 + 0.25 * math.sin(2 * th), 1.55 + 0.22 * math.sin(1.5 * th)))
    yaw = th + math.pi / 2
    dirv = np.array((math.cos(yaw), math.sin(yaw), 0.0))
    side = np.array((-math.sin(yaw), math.cos(yaw), 0.0))
    rot = (0.0, 0.0, yaw)
    dark = (0.16, 0.14, 0.14)
    F.c(c, (0.30, 0.07, 0.07), dark, rot)
    F.c(c - 0.19 * dirv, (0.14, 0.09, 0.09), (0.55, 0.10, 0.10), rot)
    F.c(c + 0.24 * dirv, (0.16, 0.014, 0.014), dark, rot)
    w = 0.35 + 0.65 * abs(math.sin(2 * math.pi * 26.0 * t))
    for sgn in (-1, 1):
        F.c(c + side * sgn * (0.06 + 0.11 * w) + np.array((0.0, 0.0, 0.05)), (0.15, 0.22 * w, 0.014), (0.86, 0.90, 0.95), rot)
    for q in range(3):
        for sgn in (-1, 1):
            F.c(c + dirv * (0.07 - 0.07 * q) + side * sgn * 0.07 + np.array((0.0, 0.0, -0.07)), (0.012, 0.014, 0.13), dark, rot)


PROPS = {LN["hook"]: props_hook, LN["wire"]: props_wire, LN["cloud"]: props_hook, LN["evr"]: props_evr, LN["iss"]: props_iss,
         LN["summit"]: props_summit, LN["dent"]: props_dent, LN["lake"]: props_lake, LN["air"]: props_air, LN["holo"]: props_holo,
         LN["erode"]: props_erode, LN["twist"]: props_twist, LN["crumble"]: props_crumble, LN["round"]: props_round,
         LN["oblate"]: props_oblate, LN["tape"]: props_tape, LN["spin"]: props_spin, LN["dusk"]: props_dusk, LN["ask"]: props_dusk,
         LN["mosq"]: props_mosq}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR, BL, LT = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off), Items(N_BL, off), []
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
JS_SH = JH_SH


def jh_float(tau, t):
    return dict(z=0.12 + 0.07 * math.sin(2 * math.pi * t / 1.6))


def jh_jump(tau, t):
    a, b = shot_span(LN["jump"])
    s = clamp((tau - 0.15) / max(b - a - 0.05, 0.5))
    z = 3.6 * 4.0 * s * (1.0 - s)
    return dict(z=z, pose="shock" if z > 0.5 else "smile")


def jh_gauge(tau, t):
    a, b = shot_span(LN["summit"])
    return dict(pose="gape" if tau > 0.8 * (b - a) else "smile")


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    add("js", 0, JH_SH, JH_PA, {                                       # 지후 (우주복 헬멧, 꼭짓점 장면)
        L["hook"]: st("peak", 0.0, 0.0, -90, "aw_up", also=("aw_up",)),
        L["cloud"]: st("peak", 0.0, 0.0, -90, "aw_up", alt=("aw_up", "gape", 0.5, 0.0)),
        L["evr"]: st("peak", -0.1, 2.5, -40, "point"),
        L["summit"]: st("summit", 0.0, 0.0, -90, "smile", fn=jh_gauge, also=("gape",)),
        L["float"]: st("flat", 0.0, 0.0, -90, "gape", fn=jh_float),
        L["jump"]: st("flat", 0.0, 0.0, -90, "smile", fn=jh_jump, also=("shock",)),
        L["twist"]: st("peak", 0.2, 2.8, -30, "point")}, extra="suit")
    add("jh", 0, JH_SH, JH_PA, {                                       # 지후 (보라 후드)
        L["holo"]: st("holo", -1.45, 0.4, -90, "look_up_h"),
        L["erode"]: st("holo", -1.45, 0.4, -90, "gape"),
        L["round"]: st("holo", -1.45, 0.4, -90, "smile"),
        L["tape"]: st("globe", 0.9, 1.7, -90, "think", alt=("think", "point", 0.8, 0.0), also=("point",)),
        L["spin"]: st("globe", 0.9, 1.4, -90, "smile", alt=("point", "smile", 0.6, 0.0)),
        L["walk"]: st("field", 0.0, 3.0, 90, "walk_a_s", pair=("walk_a_s", "walk_b_s"), cad=0.30, seq=[(1.95, "smile")],
                      keys=[(0.0, (0.0, 3.0, 0.0, 90.0)), (1.4, (0.0, 8.0, 0.0, 90.0)), (1.95, (0.0, 8.0, 0.0, -90.0))]),
        L["dusk"]: st("window", 0.0, 2.6, 90, "look_dn"),
        L["ask"]: st("window", 0.0, 2.0, -90, "both")}, extra="hood")
    add("rs", 1, CO_SH, CO_PA, {
        L["holo"]: st("holo", 1.45, 0.5, 180, "point"),
        L["erode"]: st("holo", 1.45, 0.5, 180, "point_up"),
        L["round"]: st("holo", 1.45, 0.5, 180, "think")}, extra="coat")
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
THIN_SKY = ((0.06, 0.12, 0.34), (0.28, 0.40, 0.70), 0.4)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
SPACE_SKY = ((0.003, 0.004, 0.014), (0.010, 0.013, 0.034), 1.8)
ROOM_SKY = ((0.10, 0.14, 0.26), (0.24, 0.30, 0.46), 0.0)
SKIES = {"peak": DAY_SKY, "summit": SPACE_SKY, "diag": ROOM_SKY, "sea": DAY_SKY, "flat": THIN_SKY, "field": DAY_SKY,
         "holo": ROOM_SKY, "globe": ROOM_SKY, "window": DUSK_SKY}


def sky(t):
    return SKIES[cam_of(t)["set"]]


def env(i, st_):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if st_ == "summit":
        e.update(sun=4.2, sun_col=(1.0, 0.97, 0.92), sun_rot=(55, 0, 50), amb=0.36, amb_col=(0.45, 0.52, 0.75))
    elif st_ == "flat":
        e.update(sun=3.8, sun_col=(1.0, 0.95, 0.88), sun_rot=(55, 0, 40), amb=0.38, amb_col=(0.50, 0.58, 0.82))
    elif st_ == "diag":
        e.update(sun=0.4, amb=0.5, amb_col=(0.75, 0.80, 0.95), lt={"ep46_di0": 190.0, "ep46_di1": 110.0})
    elif st_ == "holo":
        e.update(sun=0.4, amb=0.5, amb_col=(0.75, 0.80, 0.95), lt={"ep46_ho0": 200.0, "ep46_ho1": 120.0})
    elif st_ == "globe":
        e.update(sun=0.4, amb=0.5, amb_col=(0.85, 0.80, 0.78), lt={"ep46_gl0": 200.0, "ep46_gl1": 110.0})
    elif st_ == "window":
        e.update(sun=2.0, sun_col=(1.0, 0.62, 0.38), sun_rot=(72, 0, 20), amb=0.40, amb_col=(0.80, 0.62, 0.68),
                 lt={"ep46_wi0": 150.0, "ep46_wi1": 80.0})
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
    v = X.Vox(46)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep46_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep46_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep46_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep46_fx", K.proto(ctx, "ep46_p_fx", cube(), [K.mat_inst("ep46_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep46_glow", K.proto(ctx, "ep46_p_glow", cube(), [_mat_glow("ep46_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep46_orb", K.proto(ctx, "ep46_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep46_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep46_bl", K.proto(ctx, "ep46_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep46_m_bl", 0.8)]),
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
