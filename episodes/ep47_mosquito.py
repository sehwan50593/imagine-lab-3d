"""EP47 만약에 모기가 전부 사라진다면? (기준 영상 형식 STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

11-06 오너: 42~49는 '남자가 한 명뿐이라면' 편 형식으로, 내레이션 없이. 소리는 배경음(-23 LUFS)과 효과음뿐.
장면(3D)은 11-05 픽세판 그대로(야영장 텐트·연구실·마을 마당·접경 야영장·연못·툰드라·하와이·마당), 줄 순서도 그대로(이미 시간순).
D-DAY(모기가 사라지면 연 60만 명 생존) → 바로(약 3,500종) → +1주(모기 등 매개체 병 연 70만 명↑) → +1달(75%가 5살 미만, 국내 659명)
→ +1년(생태계 충격은 크지 않을 듯) → 반전(하와이에선 모기가 새를 멸종시킨다) → 지금(새 모기장·백신 100만 명) → 질문 → 다음 편(겨울잠).
효과음: 묶음 '찰싹', 컷 '휙', 모기 '앵~', 훅에서 모기가 사라질 때 '띵', 뺨 때리기 '찰싹'.

근거(설명란): ※ '모기가 모두 사라졌다'는 가정의 상상 시나리오. 그림 속 크기와 비율은 연출.
· 말라리아 사망 2023년 59.7만 명, 2024년 약 61만 명 추정, 말라리아는 모기만 옮김 · WHO World Malaria Report 2024·2025
· 모기 약 3,500종, 사람 피를 노리는 건 수백 종, 흡혈은 암컷만 · Fang, Nature 466:432(2010)
· 모기·진드기 등 매개체 감염병 사망 연 70만 명 이상 · WHO Vector-borne diseases fact sheet(2024)
· 말라리아 사망의 약 75%가 5세 미만 · WHO World Malaria Report 2025 보도
· 국내 말라리아 2024년 국내 발생 659명 · 질병관리청 감염병포털
· 물고기·새·박쥐는 대체로 다른 먹이를 찾을 것(일부 이견, 북극 철새 감소 의견) · Fang, Nature 466:432(2010)
· 하와이 1826년 집모기 유입 → 조류 말라리아로 토종 꿀먹이새 급감·멸종, 남은 새는 고지대에 · USGS PIERC, 미국조류보전협회
· 새 모기장·백신 등 새 예방 도구가 약 100만 명 사망을 막은 것으로 추정 · WHO World Malaria Report 2025 보도
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게)
OFF = {"camp": (0, 0), "lab": (300, 0), "village": (600, 0), "dmz": (900, 0), "pond": (1200, 0), "tundra": (1500, 0),
       "hawaii": (1800, 0), "yard": (2100, 0), "snow": (2400, 0)}
NAMES = ("hook", "world", "slap", "species", "pick", "quiet", "toll", "village", "under5", "dmz", "korea", "pond", "web", "tundra",
         "twist", "ship", "summit", "reduce", "million", "scales", "dusk", "button", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}

XL = 1.0                                   # 훅: 누운 지후의 발끝 x (머리는 -1.59 쪽)
HK_SIT = 0.95                              # 훅: 지후가 놀라 일어나는 때(줄 시작 후 초)
HK_MOS = 0.85                              # 훅: 모기가 반짝 사라지는 때
SLAP_T = 1.35                              # 2번 줄: 모기가 맴돌다 뺨을 때리는 때(props_slap과 같은 값)


def LAB(tgt=(0.0, 0.0, 1.45), dist=6.0, push=0.9, daz=2, shift=0.08, el=3):
    return ("lab", tgt, -90, el, dist, 28, push, daz, shift)


# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
H_A = ("camp", (XL - 1.59, 0.6, 0.24), -90, 32, 2.4, 28, 0.7, 4, 0.10)
LINES = [
    dict(d=2.8, sub="오늘 밤, 지구의 모기가\n전부 사라진다면?", ease="out", shot=H_A),
    dict(d=3.0, sub="말라리아로만 해마다\n약 60만 명이 숨지니까요.", shot=LAB((0.0, 0.0, 1.45), 6.0, 0.9, 2)),
    dict(d=3.2, sub="윙 소리에 손뼉을 쳤다가\n지후는 제 뺨을 때립니다.", shot=("camp", (4.0, -5.0, 0.95), -90, 3, 4.8, 28, 0.85, -3, 0.0)),
    dict(d=3.0, sub="모기는 전 세계에\n약 3,500종이 있습니다.", shot=LAB((0.0, 0.0, 1.45), 6.0, 0.88, -2)),
    dict(d=2.8, sub="그중 사람 피를 노리는 건\n수백 종뿐입니다.", shot=LAB((0.0, 0.0, 1.45), 5.2, 0.9, 2)),
    dict(d=2.8, sub="일주일 뒤,\n밤이 조용해졌습니다.", shot=("camp", (3.4, -4.0, 0.6), -90, 14, 6.8, 28, 0.9, 4, 0.04)),
    dict(d=3.2, sub="모기 등이 옮기는 병으로\n해마다 70만 명 넘게 숨집니다.", shot=LAB((0.0, 0.0, 1.35), 6.0, 0.9, -2)),
    dict(d=3.0, sub="한 달 뒤, 아이들이\n밤새 마당에서 놉니다.", shot=("village", (0.5, 0.0, 0.75), -90, 6, 6.5, 28, 0.88, 3, 0.0)),
    dict(d=3.1, sub="말라리아 사망의 75%가\n5살 미만 아이였습니다.", shot=LAB((0.0, 0.0, 1.45), 6.0, 0.9, 2)),
    dict(d=2.8, sub="경기 북부 접경 야영장도\n조용해졌습니다.", shot=("dmz", (1.4, 2.0, 0.95), -90, 3, 4.8, 28, 0.88, 3, 0.0)),
    dict(d=3.0, sub="우리나라도 2024년에만\n말라리아 환자가 659명.", shot=LAB((0.0, 0.0, 1.45), 6.0, 0.9, -2)),
    dict(d=3.5, sub="1년 뒤, 물고기와 새는\n다른 먹이를 찾습니다.", shot=("pond", (0.8, 5.0, 0.7), -90, 10, 6.5, 28, 0.9, 3, 0.08)),
    dict(d=3.2, sub="연구자들은 생태계 충격이\n크지 않을 거라 봤습니다.", shot=LAB((0.0, 0.0, 1.45), 6.0, 0.9, 2)),
    dict(d=3.2, sub="다만 북극 철새는\n줄 수 있다는 의견도 있습니다.", shot=("tundra", (0.0, 3.0, 0.95), -90, 3, 6.0, 28, 0.9, 3, 0.0)),
    dict(d=3.3, sub="그런데 하와이에선 모기가\n새를 멸종시키고 있습니다.", shot=("hawaii", (0.0, 2.0, 1.4), -90, 4, 6.0, 28, 0.9, 3, 0.06)),
    dict(d=2.7, sub="1826년 배를 타고\n들어온 모기 탓입니다.", shot=("hawaii", (22.0, 6.0, 2.2), -90, 4, 10.0, 28, 0.9, 4, 0.04)),
    dict(d=3.0, sub="남은 새들은 모기가 못 사는\n고지대로 올라갔습니다.", shot=("hawaii", (-30.0, 4.5, 7.0), -90, 5, 5.0, 28, 0.92, 3, 0.0)),
    dict(d=2.8, sub="하와이는 모기를 줄이는\n연구를 하고 있습니다.", shot=LAB((-0.2, 0.0, 1.2), 6.0, 0.9, -2)),
    dict(d=3.2, sub="새 모기장과 백신은\n약 100만 명을 지켰습니다.", shot=LAB((0.0, 0.0, 1.45), 6.0, 0.9, 2)),
    dict(d=2.7, sub="모기는 없애기 전에\n알아야 할 것이 많습니다.", shot=LAB((0.0, 0.0, 1.2), 7.0, 0.9, 2)),
    dict(d=3.1, sub="작은 모기 하나가\n세상을 이렇게 흔듭니다.", shot=("yard", (0.0, 0.0, 1.0), -90, 3, 5.5, 28, 0.88, 3, 0.0)),
    dict(d=2.6, sub="댓글로 알려 주세요.", shot=("yard", (0.4, 0.0, 1.0), -90, 3, 4.8, 30, 0.9, 0, 0.0)),
    dict(d=3.6, sub="석 달을 자고 일어나면\n어떻게 될까요?", shot=("snow", (0.0, 0.0, 1.0), -90, 6, 9.0, 26, 0.92, 3, 0.0)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="D-DAY", label="모기가 사라지면 해마다", big="약 60만 명 생존", label_color="blue", big_color="green"),
    dict(at="species", badge="바로", title="전 세계 모기", big="약 3,500종", big_color="yellow"),
    dict(at="quiet", badge="+1주", title="모기 등이 옮기는 병", big="연 70만 명↑", big_color="orange"),
    dict(at="village", badge="+1달", title="말라리아 사망의", big="75%가 5살 미만", big_color="red"),
    dict(at="dmz", badge="+1달", title="국내 말라리아 2024년", big="659명", big_color="cyan"),
    dict(at="pond", badge="+1년", title="생태계 충격은", big="크지 않을 듯", big_color="green"),
    dict(at="twist", badge="반전", title="하와이에선 모기가", big="새를 멸종시킨다", big_color="red"),
    dict(at="reduce", badge="지금", title="새 모기장·백신", big="100만 명 보호", big_color="green"),
    dict(at="button", badge="지금", title="모기 없애는 버튼\n{cyan}누를 건가요?{/}", title_size=70),
    dict(at="teaser", badge="다음 편", title="내일 낮 12시\n{cyan}곰처럼 겨울잠을 잔다면?{/}", title_size=66),
]
TWIST = LN["twist"]     # 하와이 반전(음악이 바뀌는 곳)
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
_SLAP = STARTS[LN["slap"]]
META = {"id": "ep47", "title": "만약에 모기가 전부 사라진다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"key": "F", "mode": "major", "bpm": 100, "seed": 471, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, [[0.0, "buzz", 1.0, HK_MOS], [HK_MOS, "ding", 1.0],
                                                       [_SLAP + 0.1, "buzz", 1.0, SLAP_T - 0.1], [_SLAP + SLAP_T, "hit", 1.3]])}}
GRADE = {"exposure": 0.95, "bloom": 0.12, "bloom_thr": 1.4, "vignette": 0.14}


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



# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def _shake_spec(i):
    """줄 i의 흔들림 [(시작 τ, 길이, 이동 세기 m, 각도 세기 도, 진동수 Hz, 종류)]. 훅만 가볍게 계속 흔들림."""
    if i == LN["hook"]:
        return [(0.0, 99.0, 0.02, 0.0, 15.0, "hold")]
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


def _head_hook(tau):
    """훅 카메라가 따라가는 지후 머리: 누운 머리(z 0.24) → 놀라 일어난 머리(z 1.28)."""
    return (XL - 1.59, 0.6, lerp(0.24, 1.28, smooth(clamp((tau - HK_SIT) / 0.35))))


TRACK[(0, 0)] = _head_hook

# ───────────────────────── 색 · 도트 글자 ─────────────────────────
OCEAN = (0.08, 0.26, 0.68)
SKINC = X.SKIN
EX_SH = [(0.85, 0.30, 0.28), (0.95, 0.80, 0.35), (0.35, 0.65, 0.40), (0.45, 0.75, 0.85), (0.80, 0.55, 0.65), (0.25, 0.45, 0.80),
         (0.92, 0.92, 0.90), (0.88, 0.58, 0.30)]
JH_SH, JH_PA = (0.58, 0.32, 0.80), (0.15, 0.18, 0.30)      # 지후: 보라 후드 · 짧은 머리 · 남색 바지
CO_SH, CO_PA = (0.93, 0.93, 0.91), (0.22, 0.24, 0.30)      # 연구원: 흰 가운 (extra='coat')
DARK = (0.14, 0.13, 0.15)
HOT = (3.0, 1.0, 0.5)
GLOWY = (3.0, 2.6, 0.8)


def wdig(G, rows, cx, y, cz, cell, col, k=1.0):
    """세트에 서 있는 도트 글자 (−y쪽을 보는 면, 가운데 맞춤): 칸 하나 = 발광 상자."""
    if k <= 0.01:
        return
    h, w = len(rows), len(rows[0])
    for r, c, c1 in _runs(rows):
        G.b((cx + ((c + c1 + 1) / 2.0 - w / 2.0) * cell * k, y, cz + (h / 2.0 - r - 0.5) * cell * k),
            (((c1 - c + 1) - 0.06) * cell * k, 0.03, cell * 0.94 * k), col)


# ───────────────────────── 세트 ─────────────────────────
def _camp(v):
    v.floor(-40, 40, -20, 70, (0.30, 0.52, 0.30), 2.5)
    for k in range(12):                                       # 먼 언덕 (y를 조금씩 비껴 놓음)
        x0 = -90 + 18 * k
        v.box(x0, x0 + 22, 72 + 3.1 * (k % 4), 92 + 3.1 * (k % 4), 0, 6 + 2.0 * (k % 5), (0.16 + 0.02 * (k % 3), 0.30, 0.26), jit=0.05)
    for x, y in ((-11, 12), (12, 14), (-18, 6), (18, 8), (-6, 24), (8, 28), (-24, 30), (24, 26)):
        X.tree(v, x, y, 5.0)
    orange, dark = (0.92, 0.58, 0.25), (0.78, 0.44, 0.20)     # 지후의 텐트 (앞이 열림)
    v.box(-3.3, 3.3, -2.0, 2.7, 0, 0.06, (0.55, 0.50, 0.40), jit=0.02)
    v.box(-3.35, -3.2, -2.0, 2.7, 0.06, 2.4, orange)
    v.box(3.2, 3.35, -2.0, 2.7, 0.06, 2.4, orange)
    v.box(-3.2, 3.2, 2.55, 2.7, 0.06, 2.4, dark)
    v.box(-3.5, 3.5, -2.1, 2.8, 2.4, 2.46, orange)
    v.box(-1.4, 1.3, 0.1, 1.1, 0.06, 0.12, (0.25, 0.35, 0.60), jit=0.02)                 # 잠자리 매트
    v.box(-0.12, 0.12, 0.38, 0.62, 1.55, 2.0, (0.30, 0.22, 0.14))                         # 천장에 매단 랜턴 걸이
    v.box(-0.2, 0.2, 0.3, 0.7, 1.75, 1.95, (1.0, 0.85, 0.55), jit=0, glow=True)
    v.light(0.0, 0.5, 1.7, 80, (1.0, 0.82, 0.58), 0.3, "ep47_c0")
    v.box(1.9, 3.8, -4.5, -3.5, 0, 0.04, (0.25, 0.35, 0.60), jit=0.02)                    # 바깥 매트 (5번 줄)
    v.box(4.66, 4.74, -4.04, -3.96, 0, 0.9, (0.38, 0.26, 0.15))                           # 바깥 랜턴 기둥
    v.box(4.55, 4.85, -4.15, -3.85, 0.9, 1.2, (1.0, 0.85, 0.55), jit=0, glow=True)
    v.light(4.7, -4.0, 1.3, 130, (1.0, 0.82, 0.58), 0.3, "ep47_c1")
    v.box(-15.0, -11.0, 8.0, 11.0, 0, 1.8, (0.25, 0.45, 0.75))                            # 먼 파란 텐트


def _lab(v):
    v.floor(-14, 14, -10, 9, (0.10, 0.13, 0.20), 0.5, "check")
    v.wall((-14, 7), (14, 7), 0, 9, (0.12, 0.16, 0.26), 0.5, face=-1)
    v.box(-8, 8, 6.93, 6.99, 0.18, 0.22, (0.35, 0.80, 1.0), jit=0, glow=True)
    v.box(-8, 8, 6.93, 6.99, 4.9, 4.94, (0.35, 0.80, 1.0), jit=0, glow=True)
    v.light(0.0, 1.0, 6.0, 260, (0.85, 0.92, 1.0), 1.0, "ep47_l0")
    v.light(-3.0, -1.0, 5.0, 160, (1.0, 0.92, 0.8), 0.8, "ep47_l1")


def _village(v):
    v.floor(-30, 30, -15, 40, (0.76, 0.62, 0.42), 2.5)
    for k in range(10):
        x0 = -70 + 16 * k
        v.box(x0, x0 + 20, 48 + 3.1 * (k % 4), 66 + 3.1 * (k % 4), 0, 4 + 1.5 * (k % 3), (0.45, 0.50, 0.30), jit=0.05)
    v.box(-8, 8, 9.0, 9.4, 0, 3.0, (0.82, 0.68, 0.48))                                    # 마을 집 뒷벽
    v.box(-3.0, -1.0, 8.95, 9.0, 1.0, 2.2, (0.30, 0.22, 0.16), jit=0.02)
    for bx in (-1.8, 2.4):                                                                 # 침대 (모기장은 동적)
        v.box(bx - 0.55, bx + 0.55, 5.4, 7.6, 0.0, 0.35, (0.45, 0.31, 0.20))
        v.box(bx - 0.5, bx + 0.5, 5.45, 7.55, 0.35, 0.5, (0.35, 0.50, 0.82))
    for x, y in ((-12, 14), (13, 18), (-6, 26), (9, 30)):
        X.tree(v, x, y, 6.0)


def _dmz(v):
    v.floor(-30, 30, -15, 60, (0.34, 0.50, 0.28), 2.5)
    for k in range(10):
        x0 = -70 + 16 * k
        v.box(x0, x0 + 20, 62 + 3.1 * (k % 4), 80 + 3.1 * (k % 4), 0, 6 + 1.8 * (k % 4), (0.28, 0.42, 0.30), jit=0.05)
    for x in range(-18, 19, 2):                                                           # 철책: 기둥 + 철선
        v.box(x - 0.06, x + 0.06, 11.0, 11.12, 0, 2.6, (0.45, 0.46, 0.50))
    for z in (0.7, 1.4, 2.1):
        v.box(-18, 18, 11.02, 11.1, z, z + 0.04, (0.55, 0.56, 0.60), jit=0.02)
    v.box(-0.5, 0.5, 10.8, 10.88, 1.2, 2.0, (0.92, 0.85, 0.30))                           # 접경 표지판
    v.box(-0.45, 0.45, 10.76, 10.8, 1.25, 1.95, (0.80, 0.18, 0.15), jit=0)
    v.box(0.2, 3.2, 6.0, 8.5, 0, 1.6, (0.30, 0.50, 0.32))                                 # 초록 텐트
    v.box(0.2, 3.2, 5.95, 6.0, 0.0, 1.2, (0.12, 0.14, 0.12), jit=0)
    v.box(1.5, 2.5, 1.7, 2.7, 0.0, 0.75, (0.60, 0.42, 0.25), jit=0.02)                    # 접이식 탁자(상판 아래 기둥 하나)
    v.box(1.3, 2.7, 1.5, 2.9, 0.75, 0.82, (0.68, 0.48, 0.30))


def _pond(v):
    v.floor(-30, 30, -15, 40, (0.32, 0.54, 0.30), 2.5)
    v.box(-4.0, 4.0, 2.5, 9.0, 0.0, 0.1, (0.22, 0.50, 0.78), jit=0.03)                    # 웅덩이
    for k in range(14):                                                                    # 갈대
        x = -4.4 + 0.65 * k
        v.box(x, x + 0.1, 9.3 + 0.12 * (k % 3), 9.4 + 0.12 * (k % 3), 0, 1.0 + 0.3 * (k % 4), (0.42, 0.62, 0.28), jit=0.05)
    for x, y in ((-9, 14), (10, 16), (-4, 22), (5, 26), (14, 8), (-13, 8)):
        X.tree(v, x, y, 5.5)
    for k in range(8):
        x0 = -70 + 18 * k
        v.box(x0, x0 + 22, 52 + 3.1 * (k % 4), 70 + 3.1 * (k % 4), 0, 5 + 1.5 * (k % 3), (0.30, 0.46, 0.34), jit=0.05)


def _tundra(v):
    v.floor(-40, 40, -15, 60, (0.80, 0.84, 0.90), 2.5)
    for k in range(10):
        x0 = -80 + 18 * k
        v.box(x0, x0 + 22, 62 + 3.1 * (k % 4), 80 + 3.1 * (k % 4), 0, 5 + 2.2 * (k % 4), (0.70 + 0.02 * (k % 3), 0.76, 0.84), jit=0.03)


def _hawaii(v):
    v.floor(-45, 45, -20, 50, (0.20, 0.42, 0.22), 2.5)
    for k in range(8):                                                                     # 화산 (쌓은 상자) — 먼 곳
        w = 40 - 4 * k
        v.box(-w / 2 + 3.1 * (k % 2), w / 2 + 3.1 * (k % 2), 56 + 1.1 * (k % 3), 56 + w + 1.1 * (k % 3), 4 * k, 4 * k + 4,
              (0.28 + 0.03 * k, 0.22 + 0.01 * k, 0.20), jit=0.04)
    v.box(-2.5, 2.5, 63, 68, 32, 32.2, (3.0, 0.9, 0.3), jit=0, glow=True)
    for x, y in ((-3.2, 4.2), (0.2, 4.6), (3.4, 4.0), (-6.5, 5.0), (7.0, 5.2), (-10, 9), (11, 9)):
        X.tree(v, x, y, 4.6)
    v.box(12, 45, -1, 16, 0.0, 0.15, (0.12, 0.32, 0.62), jit=0.03)                         # 바다
    for k in range(5):                                                                     # 정상 계단 (고지대, x≈-30)
        w = 12 - 2.4 * k
        v.box(-30 - w / 2, -30 + w / 2, 4.5 - w / 2, 4.5 + w / 2, 1.2 * k + 0.0, 1.2 * k + 1.2,
              (0.55 - 0.03 * k, 0.60 - 0.02 * k, 0.50 + 0.05 * k), jit=0.05)
    v.box(-31.5, -28.5, 3.0, 6.0, 6.0, 6.1, (0.88, 0.92, 0.95), jit=0.02)                  # 정상 바닥 (z=6)


def _yard(v):
    v.floor(-70, 90, -10, 125, (0.34, 0.46, 0.30), 2.5)
    for k in range(10):
        x0 = -130 + 24 * k
        v.box(x0, x0 + 26, 128 + 3.1 * (k % 4), 150 + 3.1 * (k % 4), 0, 6 + 2.0 * (k % 5), (0.26 + 0.02 * (k % 3), 0.30, 0.34), jit=0.05)
    for x in range(-8, 9, 2):
        v.box(x - 0.05, x + 0.05, 7.0, 7.1, 0, 1.2, (0.55, 0.45, 0.36))
    v.box(-8, 8, 6.96, 7.14, 1.0, 1.06, (0.55, 0.45, 0.36))
    net = (0.88, 0.90, 0.95)                                                               # 모기장 (앞이 열림)
    for px in (-1.2, 1.2):
        v.box(px - 0.04, px + 0.04, -1.04, -0.96, 0, 2.3, (0.45, 0.31, 0.20))
        v.box(px - 0.04, px + 0.04, 1.26, 1.34, 0, 2.3, (0.45, 0.31, 0.20))
        v.box(px - 0.015, px + 0.015, -1.0, 1.3, 0.05, 2.25, net, jit=0.01)
    v.box(-1.17, 1.17, 1.28, 1.31, 0.05, 2.2, net, jit=0.01)
    v.box(-1.3, 1.3, -1.1, 1.4, 2.3, 2.34, net, jit=0.01)
    v.box(-0.9, 0.9, -0.8, 1.0, 0.0, 0.08, (0.5, 0.4, 0.3), jit=0.02)
    for x, y in ((-12, 14), (14, 16), (-18, 30)):
        X.tree(v, x, y, 5.5)
    v.light(1.4, -1.6, 2.4, 60, (1.0, 0.8, 0.55), 0.3, "ep47_y0")


def _snow(v):
    v.floor(-40, 40, -15, 60, (0.78, 0.84, 0.94), 2.5)
    for k in range(10):
        x0 = -80 + 18 * k
        v.box(x0, x0 + 22, 40 + 3.1 * (k % 4), 58 + 3.1 * (k % 4), 0, 4 + 2.0 * (k % 4), (0.62 + 0.02 * (k % 3), 0.70, 0.84), jit=0.03)
    for x, y in ((-10, 10), (11, 12), (-16, 18)):
        X.tree(v, x, y, 4.5)
    v.light(0.0, -3.0, 5.0, 100, (0.7, 0.8, 1.0), 0.8, "ep47_s0")


def _sets():
    return (("camp", _camp), ("lab", _lab), ("village", _village), ("dmz", _dmz), ("pond", _pond), ("tundra", _tundra),
            ("hawaii", _hawaii), ("yard", _yard), ("snow", _snow))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 2600, 800, 40, 40


def mos(F, x, y, z, t, k=1.0, ph=0.0, col=DARK):
    """모기 한 마리: 몸 + 날개 둘(펄럭임) + 주둥이 + 다리. k = 크기 배율. 얼굴 앞으로 향함(+x)."""
    f = 0.5 + 0.5 * math.sin(2 * math.pi * (t * 16 + ph))
    F.b((x, y, z), (0.10 * k, 0.05 * k, 0.05 * k), col)
    w = (0.03 + 0.06 * f) * k
    for sy in (-1, 1):
        F.b((x - 0.01 * k, y + sy * (0.025 * k + w / 2), z + 0.03 * k), (0.05 * k, w, 0.01 * k), (0.92, 0.94, 0.98))
    F.b((x + 0.075 * k, y, z - 0.005 * k), (0.06 * k, 0.012 * k, 0.012 * k), (0.30, 0.30, 0.32))
    for sx in (-0.025, 0.025):
        F.b((x + sx * k, y, z - 0.045 * k), (0.01 * k, 0.07 * k, 0.012 * k), (0.25, 0.25, 0.28))


def sparkle(G, c, age, n=16, R=1.4, size=0.07):
    """하얀 반짝 가루: 한 점에서 사방으로 퍼지며 작아져 사라짐 (age 0~0.7초)."""
    if age < 0.0 or age > 0.7:
        return
    f = age / 0.7
    for q in range(n):
        a = 2 * math.pi * (q + 0.3 * _h(q)) / n
        e = (q % 4 - 1.5) * 0.5
        r = R * smooth(f) * (0.6 + 0.4 * _h(q + 9))
        s = size * (1.0 - f) + 0.005
        G.b((c[0] + math.cos(a) * math.cos(e) * r, c[1] + math.sin(a) * math.cos(e) * r, c[2] + math.sin(e) * r), (s, s, s), (3.0, 3.0, 3.4))


def bird(F, x, y, z, col, k=1.0, t=0.0, ph=0.0, d=1, fly=True, sc=1.0):
    """작은 새: 몸·머리·부리·꼬리·날개(fly이면 펄럭임). d=±1 보는 방향(x)."""
    k = k * sc
    F.b((x, y, z), (0.30 * k, 0.16 * k, 0.16 * k), col)
    F.b((x + 0.19 * k * d, y, z + 0.07 * k), (0.13 * k, 0.12 * k, 0.12 * k), col)
    F.b((x + 0.28 * k * d, y, z + 0.06 * k), (0.08 * k, 0.04 * k, 0.03 * k), (1.0, 0.7, 0.2))
    F.b((x - 0.2 * k * d, y, z), (0.14 * k, 0.08 * k, 0.03 * k), tuple(c * 0.8 for c in col))
    wf = (0.04 + 0.14 * abs(math.sin(2 * math.pi * (t * 3.2 + ph)))) if fly else 0.03
    for sy in (-1, 1):
        F.b((x, y + sy * (0.1 * k + wf * k * 0.5), z + 0.05 * k + wf * k * 0.3), (0.16 * k, (wf + 0.04) * k, 0.02 * k), tuple(c * 0.75 for c in col))


def globe_items(F, BL, c, R, sp):
    """지구본: 파란 구 + 앞(−y) 반구의 땅·극지 조각."""
    BL.orb(c, 2 * R, OCEAN)
    Rm = earth_rot(sp)
    patch = 0.125 * R
    for k in LAND_IDX:
        n = Rm @ EARTH_PTS[k]
        if n[1] > -0.05:
            continue
        F.c((c[0] + n[0] * (R + 0.012), c[1] + n[1] * (R + 0.012), c[2] + n[2] * (R + 0.012)), (0.05, patch, patch), LAND_COL[k], rot_n(n))


def fish(F, cx, cy, r, t, ph, col=(0.95, 0.5, 0.2)):
    a = 2 * math.pi * (t * 0.35 + ph)
    F.c((cx + r * math.cos(a), cy + 0.6 * r * math.sin(a), 0.14), (0.40, 0.14, 0.12), col, (0.0, 0.0, a + math.pi / 2))
    F.c((cx + r * math.cos(a) - 0.25 * math.cos(a + math.pi / 2), cy + 0.6 * r * math.sin(a) - 0.25 * math.sin(a + math.pi / 2), 0.14),
        (0.14, 0.2, 0.05), col, (0.0, 0.0, a + math.pi / 2))


def reindeer(F, x, y, t, k=1.0, ph=0.0, d=1):
    c = (0.62, 0.48, 0.34)
    F.b((x, y, 0.85 * k), (1.0 * k, 0.38 * k, 0.5 * k), c)
    for lx in (-0.38, 0.38):
        for ly in (-0.12, 0.12):
            sw = 0.08 * k * math.sin(2 * math.pi * (t * 1.4 + ph) + (math.pi if (lx > 0) == (ly > 0) else 0.0))
            F.b((x + lx * k * d + sw, y + ly * k, 0.3 * k), (0.12 * k, 0.12 * k, 0.6 * k), (0.52, 0.40, 0.28))
    F.b((x + 0.55 * k * d, y, 1.12 * k), (0.2 * k, 0.2 * k, 0.4 * k), c)
    F.b((x + 0.68 * k * d, y, 1.28 * k), (0.28 * k, 0.24 * k, 0.28 * k), c)
    for sy in (-1, 1):
        F.b((x + 0.66 * k * d, y + sy * 0.12 * k, 1.55 * k), (0.04 * k, 0.04 * k, 0.28 * k), (0.35, 0.25, 0.2))
        F.b((x + 0.72 * k * d, y + sy * 0.2 * k, 1.75 * k), (0.04 * k, 0.2 * k, 0.04 * k), (0.35, 0.25, 0.2))


def kidbox(F, x, z, col, k=1.0):
    """블록 아이 하나(상자 몸·머리)."""
    F.b((x, 0.0, z + 0.2 * k), (0.30 * k, 0.2 * k, 0.4 * k), col)
    F.b((x, 0.0, z + 0.55 * k), (0.26 * k, 0.24 * k, 0.26 * k), SKINC)


# ── 0: 훅 — 텐트 안, 모기가 얼굴 앞을 휙 지나가다 반짝 사라지고 지후가 놀라 깸
def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    xs = XL - 1.59
    if tau < HK_MOS:
        p = tau / HK_MOS
        mos(F, lerp(xs - 1.8, xs + 1.6, p), lerp(0.1, 0.9, p) + 0.04 * math.sin(40 * tau), 0.80 + 0.22 * math.sin(2 * math.pi * p * 1.5), t, 3.2)
    else:
        sparkle(G, (xs + 1.6, 0.9, 0.80), tau - HK_MOS)


# ── 1: 지구본 + 사망 숫자 판 60만
def props_world(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    globe_items(F, BL, (-0.6, 0.3, 1.65), 0.5, 0.5 * t)
    mos(F, 0.85, 0.0, 1.65, t, 5.0)
    v = int(600000 * smooth(ramp(tau, 0.1, 1.7)))
    wdig(G, num_rows(f"{v:,}"), 0.0, -0.15, 0.95, 0.075, HOT, pop(tau - 0.1, 0.25))


# ── 2: 지후가 모기를 잡으려다 제 뺨을 침
def props_slap(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    if tau < 1.35:
        w = 5.2 * t
        mos(F, 4.0 + 0.62 * math.cos(w), -5.0 + 0.62 * math.sin(w), 1.62 + 0.1 * math.sin(2.3 * w), t, 2.6)
    else:
        a = tau - 1.35
        mos(F, 4.6 + 3.0 * a, -4.6 + 0.5 * a, 1.65 + 1.4 * a, t, 2.6)
    jh = S.get("jh")
    if jh and tau >= 1.35:
        c = rel(jh, 0.245, 0.17, 1.5)
        F.b(c, (0.03, 0.14, 0.12), (0.95, 0.35, 0.35))
        sparkle(G, c, tau - 1.35, 10, 0.55, 0.06)


# ── 3 · 4: 모기 아이콘 격자 (3,500종) — 4번에서 사람 피를 노리는 일부만 빨갛게
GRID = [(c, r) for r in range(12) for c in range(25)]
GRID_RANK = [_h(k * 7 + 3) for k in range(len(GRID))]


def _grid(G, t, red=0.0):
    for k, (c, r) in enumerate(GRID):
        s = 0.5 + 0.5 * math.sin(2 * math.pi * (t * 1.3 + _h(k) * 3.0)) ** 2
        hot = GRID_RANK[k] < red
        G.b(((c - 12) * 0.075, 0.0, 1.0 + 0.075 * r), (0.055 * s, 0.03, 0.055 * s), (3.0, 0.35, 0.25) if hot else (1.4, 1.7, 2.2))


def props_species(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    _grid(G, t)
    wdig(G, num_rows("3,500"), 0.0, 0.0, 2.15, 0.07, GLOWY, pop(tau - 0.1, 0.25))


def props_pick(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    _grid(G, t, 0.09 * ramp(tau, 0.2, dur * 0.8))
    wdig(G, num_rows("3,500"), 0.0, 0.0, 2.15, 0.07, GLOWY)


# ── 5: 모기 사라진 밤 — 랜턴 주위 날벌레가 하나씩 사라지고 지후가 편히 누움
def props_quiet(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for k in range(14):
        a = 2 * math.pi * (_h(k) + 0.6 * t * (1 + 0.3 * _h(k + 5)))
        r = 0.35 + 0.35 * _h(k + 3)
        s = vanish(tau, 0.25 + 1.7 * _h(k + 11))
        if s > 0.01:
            F.b((4.7 + r * math.cos(a), -4.0 + r * math.sin(a), 1.0 + 0.3 * math.sin(a * 2 + k)), (0.07 * s, 0.07 * s, 0.07 * s), DARK)


# ── 6: 사망 숫자 60만 → 70만
def props_toll(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    v = int(lerp(600000, 700000, smooth(ramp(tau, 0.2, 1.8))))
    wdig(G, num_rows(f"{v:,}"), 0.0, -0.15, 1.75, 0.085, HOT)
    L = 1.8 * v / 700000.0
    G.b((-0.9 + L / 2, 0.0, 1.1), (L, 0.05, 0.12), (3.0, 0.9, 0.35))
    mos(F, -1.15, 0.0, 1.1, t, 3.0)
    mos(F, 1.2, 0.0, 1.1, t, 3.0, 0.3)


# ── 7: 아프리카 마을 마당 — 침대 모기장이 걷힘
def nets(F, bx, by, lift):
    net = (0.88, 0.90, 0.95)
    h = max(0.04, 1.65 * (1.0 - lift))
    zt = 1.7
    F.b((bx, by, zt + 0.02), (1.8, 2.3, 0.04), net)
    for sy in (-1, 1):
        F.b((bx, by + sy * 1.15, zt - h / 2), (1.8, 0.03, h), net)
    for sx in (-1, 1):
        F.b((bx + sx * 0.9, by, zt - h / 2), (0.03, 2.3, h), net)


def props_village(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    lift = smooth(ramp(tau, 0.2, 1.1))
    nets(F, -1.8, 6.5, lift)
    nets(F, 2.4, 6.5, lift)


# ── 8: 블록 아이 4명 중 3명이 강조 (75%)
def props_under5(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for k in range(4):
        x = -0.9 + 0.6 * k
        kidbox(F, x, 1.0, EX_SH[(k * 3) % len(EX_SH)] if k < 3 else (0.55, 0.57, 0.62), 1.3)
        if k < 3:
            s = pop(tau - 0.35 - 0.4 * k, 0.25)
            G.b((x, -0.05, 0.95), (0.5 * s, 0.03, 0.03), (3.0, 2.4, 0.5))
            G.b((x, -0.05, 1.8), (0.5 * s, 0.03, 0.03), (3.0, 2.4, 0.5))
    wdig(G, num_rows("75%"), 0.0, 0.0, 2.2, 0.07, GLOWY, pop(tau - 0.15, 0.25))


# ── 9: 접경 야영장 — 모기향을 치움
def props_dmz(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    p = ramp(tau, 0.7, 1.4)
    s = 1.0 - ramp(tau, 1.5, 1.8)
    c = (lerp(2.0, 0.95, p), lerp(2.2, 1.7, p), lerp(0.84, 1.3, p))
    if s > 0.02:
        for w, h in ((0.5, 0.0), (0.34, 0.04), (0.18, 0.08)):
            F.b((c[0], c[1], c[2] + h * s), (w * s, w * s, 0.04 * s), (0.30, 0.32, 0.20))
    for q in range(7):                                                                    # 모기향 연기: 치우기 전까지만
        ph = (_h(q) + 0.5 * t) % 1.0
        if tau < 1.4 and ph < 1.0:
            sz = 0.08 + 0.14 * ph
            F.b((2.0 + 0.1 * math.sin(7 * ph + q), 2.2, 0.95 + 0.9 * ph), (sz, sz, sz), (0.7, 0.7, 0.72))


# ── 10: 한반도 도트 지도 + 접경 지역에 몰린 빨간 점 + 659
KOREA = ["......#####..", ".....#######.", ".....#######.", "......######.", "......#####..", ".....######..", "....#######..", "....#######..",
         ".....######..", ".....######..", ".....#####...", "....######...", "....#####....", ".....####....", "......###....", ".......#....."]


def props_korea(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    wdig(G, KOREA, -0.75, 0.0, 1.45, 0.07, (0.45, 0.7, 1.1))
    G.b((-0.75, -0.02, 1.69), (0.95, 0.02, 0.025), (3.0, 2.4, 0.5))                  # 접경 선
    for q in range(34):
        if q / 34.0 < ramp(tau, 0.2, dur * 0.7):
            G.b((-1.0 + 0.5 * _h(q), -0.05, 1.73 + 0.24 * _h(q + 6)), (0.045, 0.03, 0.045), (3.0, 0.3, 0.25))
    wdig(G, num_rows("659"), 0.75, 0.0, 1.5, 0.08, GLOWY, pop(tau - 0.15, 0.25))


# ── 11: 물가 — 물고기가 다른 먹이를 먹고 새가 고개를 갸웃
def props_pond(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for k in range(3):
        fish(F, 0.0, 5.5, 1.3 + 0.35 * k, t, 0.3 * k)
    tl = 1.2
    s = vanish(tau, tl, 0.2)
    if s > 0.01:
        F.b((1.0 + 0.12 * math.sin(6 * t), 5.0, 0.7 + 0.1 * math.sin(9 * t)), (0.16 * s, 0.1 * s, 0.1 * s), (0.45, 0.55, 0.2))
    j = ramp(tau, tl - 0.35, tl)
    F.c((1.0, 5.0, 0.14 + 0.6 * math.sin(math.pi * j) if 0 < j < 1 else 0.14), (0.40, 0.14, 0.12), (0.95, 0.5, 0.2), (0.0, 0.0, 0.3))
    bird(F, 2.8, 4.0, 0.9, (0.92, 0.92, 0.96), 2.4, t, 0.0, -1, False)
    F.b((2.78, 4.0, 0.4), (0.06, 0.06, 0.8), (0.55, 0.45, 0.30))
    for q in range(5):                                                                    # 물 위 다른 벌레 (모기 아님)
        a = 2 * math.pi * (_h(q) + 0.2 * t)
        F.b((-1.8 + 0.4 * math.cos(a) + q * 0.7, 5.0 + 0.5 * math.sin(a), 0.75 + 0.15 * math.sin(3 * a)), (0.1, 0.07, 0.07), (0.45, 0.55, 0.2))


# ── 12: 먹이 그물 — 모기 칸이 빠져도 선이 다른 곳으로 이어짐
NODES = {"mos": (0.0, 1.45), "fish": (-0.9, 1.95), "bird": (0.0, 2.05), "bat": (0.9, 1.95), "bug": (0.0, 0.95)}
NODE_COL = {"mos": DARK, "fish": (3.0, 1.3, 0.4), "bird": (3.0, 0.4, 0.4), "bat": (1.8, 0.9, 2.4), "bug": (0.6, 2.4, 0.9)}


def _line(G, a, b, col, w=0.03):
    (x0, z0), (x1, z1) = a, b
    G.c(((x0 + x1) / 2, -0.05, (z0 + z1) / 2), (math.hypot(x1 - x0, z1 - z0), 0.02, w), col, (0.0, -math.atan2(z1 - z0, x1 - x0), 0.0))


def props_web(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    f = smooth(ramp(tau, 0.7, 1.3))                                                         # 모기 칸이 빠지는 정도
    ms = 1.0 - f
    for k, (x, z) in NODES.items():
        s = 0.30 * (ms if k == "mos" else 1.0)
        if s > 0.01:
            OR.orb((x, 0.0, z), s, NODE_COL[k])
    for k in ("fish", "bird", "bat"):
        if ms > 0.02:
            _line(G, NODES["mos"], NODES[k], (1.4 * ms, 1.4 * ms, 1.6 * ms))
        if f > 0.02:
            _line(G, NODES["bug"], NODES[k], (0.5 * f, 2.4 * f, 0.9 * f))


# ── 13: 툰드라 — 순록과 철새, 의견 갈림 표지 둘
def props_tundra(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for k in range(5):
        reindeer(F, -3.5 + 1.7 * k + 0.35 * t, 7.5 + 1.2 * (k % 3), t, 0.9, 0.3 * k)
    for k in range(11):
        row, col = k // 2, k % 2
        bird(F, -4.0 + 0.5 * t * 2 + 0.55 * row, 4.0 + (0.5 * row if col else -0.5 * row), 3.4 + 0.2 * math.sin(t * 2 + k), (0.85, 0.85, 0.9), 0.9, t, 0.1 * k)
    bob = 0.05 * math.sin(2 * math.pi * t / 0.9)
    for sx, col, gl, gc in ((-1, (0.25, 0.65, 0.35), "?", (2.5, 3.0, 2.6)), (1, (0.90, 0.55, 0.20), "!", (3.0, 2.8, 2.0))):
        F.b((sx * 0.95, 1.6, 0.9 + bob), (0.05, 0.05, 1.8), (0.55, 0.45, 0.30))
        F.b((sx * 0.95, 1.6, 1.75 + bob), (0.7, 0.05, 0.5), col)
        wdig(G, DIG[gl], sx * 0.95, 1.55, 1.75 + bob, 0.075, gc)


# ── 14 · 15 · 16: 하와이
def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for k in range(5):
        x, z = -1.5 + 0.75 * k, 1.1 + 0.5 * (k % 3)
        F.b((x, 2.2, z - 0.1), (0.9, 0.08, 0.08), (0.40, 0.28, 0.16))
        t0 = 0.4 + 0.45 * k
        s = vanish(tau, t0, 0.3)
        if s > 0.01:
            bird(F, x, 2.2, z, (0.9, 0.12, 0.10), 1.2, t, 0.0, 1, False, s)
        sparkle(G, (x, 2.2, z), tau - t0 - 0.05, 8, 0.5, 0.05)
    for q in range(2):
        a = 2 * math.pi * (0.4 * t + 0.5 * q)
        mos(F, 0.8 * math.cos(a) + 0.2 * q, 1.4 + 0.3 * math.sin(a), 1.8 + 0.25 * math.sin(2 * a), t, 3.0, 0.4 * q)


def props_ship(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    sx, sy = 22.0, 6.0
    bob = 0.06 * math.sin(2 * math.pi * t / 1.6)
    F.b((sx, sy, 0.5 + bob), (4.2, 1.4, 0.7), (0.45, 0.30, 0.18))
    F.b((sx + 0.3, sy, 0.95 + bob), (3.4, 1.2, 0.3), (0.58, 0.42, 0.26))
    F.b((sx + 2.3, sy, 0.8 + bob), (0.6, 0.9, 0.3), (0.40, 0.27, 0.16))
    F.b((sx - 0.2, sy, 2.4 + bob), (0.18, 0.18, 3.0), (0.38, 0.26, 0.16))
    F.b((sx - 0.2, sy - 0.2, 2.9 + bob), (0.08, 1.9, 1.9), (0.94, 0.92, 0.84))
    for q in range(34):                                                                    # 모기 떼가 배에서 날아오름
        ph = (_h(q + 40) + 0.25 * t) % 1.0
        f = ramp(tau, 0.2 + 0.03 * (q % 10), 1.6)
        a = 2 * math.pi * _h(q + 80) + 3.0 * ph
        r = 0.3 + 3.0 * ph * f
        mos(F, sx + 0.4 + r * math.cos(a), sy - 0.2 + 0.6 * r * math.sin(a), 1.4 + 3.2 * ph * f + 0.2 * math.sin(a * 3), t, 2.2, _h(q))
    wdig(G, num_rows("1826"), sx, sy - 1.2, 4.0, 0.16, GLOWY, pop(tau - 0.3, 0.3))


def props_summit(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    jh = S.get("jh")
    if jh is None:
        return
    sh = rel(jh, 0.0, 0.34, 1.46)
    if tau < 1.2:
        p = smooth(tau / 1.2)
        b = (lerp(sh[0] + 2.4, sh[0], p), lerp(sh[1] - 0.5, sh[1], p), lerp(sh[2] + 1.8, sh[2] + 0.13, p) + 0.12 * math.sin(math.pi * p))
        bird(F, b[0], b[1], b[2], (0.9, 0.12, 0.10), 1.3, t, 0.0, -1, True)
    elif tau < 2.0:
        bird(F, sh[0], sh[1], sh[2] + 0.13, (0.9, 0.12, 0.10), 1.3, t, 0.0, -1, False)
    else:
        a = tau - 2.0
        bird(F, sh[0] - 2.6 * a * a - 0.3 * a, sh[1] - 0.2 * a, sh[2] + 0.13 + 1.6 * a, (0.9, 0.12, 0.10), 1.3, t, 0.0, -1, True)
    if tau > 1.5:
        a = tau - 1.5
        mos(F, sh[0] + 0.9 - 0.3 * a + 0.12 * math.sin(30 * a), sh[1] - 0.2, sh[2] + 0.25 + 0.15 * math.sin(11 * a), t, 3.0)


# ── 17: 연구원이 모기 칸을 줄이면 새 아이콘이 늘어남
def props_reduce(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    F.b((-1.15, 0.0, 0.225), (0.8, 0.8, 0.45), (0.30, 0.32, 0.40))
    f = ramp(tau, 0.3, dur * 0.85)
    for k in range(18):
        r, c = k // 6, k % 6
        s = 1.0 - smooth(clamp((f * 18.0 - (17 - k)) / 1.0)) if k >= 6 else 1.0
        if s > 0.02:
            F.b((0.0 + 0.2 * c, 0.0, 1.65 - 0.25 * r), (0.15 * s, 0.1, 0.15 * s), (0.70, 0.72, 0.78))
    for k in range(10):
        if k / 10.0 < f + 0.1:
            bird(F, 0.1 + 0.22 * (k % 5), 0.0, 0.75 + 0.22 * (k // 5), (0.9, 0.12, 0.10), 0.9, t, 0.0, 1, False, pop(f * 10 - k + 1, 0.4))


# ── 18: 모기장·주사기 아이콘이 100만 막대로 쌓임
def props_million(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    net = (0.88, 0.90, 0.95)
    F.b((-0.95, 0.0, 1.05), (0.5, 0.3, 0.4), net)
    F.b((-0.95, -0.17, 1.05), (0.5, 0.03, 0.04), (0.45, 0.31, 0.20))
    F.b((-0.35, 0.0, 1.05), (0.6, 0.1, 0.1), (0.85, 0.88, 0.92))                               # 주사기 몸통
    F.b((-0.04, 0.0, 1.05), (0.2, 0.03, 0.03), (0.7, 0.7, 0.74))
    F.b((-0.7, 0.0, 1.05), (0.08, 0.2, 0.2), (0.55, 0.57, 0.62))
    f = smooth(ramp(tau, 0.2, dur * 0.8))
    n = int(round(14 * f))
    for k in range(n):
        G.b((0.85, 0.0, 0.8 + 0.1 * k), (0.8, 0.1, 0.085), (0.5, 2.6, 0.9))
    v = int(1000000 * f)
    wdig(G, num_rows(f"{v:,}"), 0.0, 0.0, 2.2, 0.055, (0.7, 3.0, 1.0))


# ── 19: 두 저울 (이득 · 손실)
def props_scales(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    ang = 0.14 * math.sin(2 * math.pi * t / 1.4) * math.exp(-0.9 * tau)
    bz = 1.9
    for sx in (-1, 1):
        F.b((sx * 1.35, 0.0, 0.225), (0.8, 0.8, 0.45), (0.30, 0.32, 0.40))
    F.b((0.0, 0.3, bz / 2), (0.1, 0.1, bz), (0.45, 0.45, 0.5))
    F.b((0.0, 0.3, 0.05), (0.7, 0.5, 0.1), (0.40, 0.40, 0.45))
    F.c((0.0, 0.3, bz), (1.4, 0.08, 0.08), (0.62, 0.62, 0.66), (0.0, ang, 0.0))
    for sx, cols in ((-1, [(0.3, 0.8, 0.4)] * 3), (1, [(0.85, 0.28, 0.25)] * 3)):
        px, pz = sx * 0.7 * math.cos(ang), bz - sx * 0.7 * math.sin(ang)
        F.b((px, 0.3, pz - 0.4), (0.02, 0.02, 0.8), (0.55, 0.55, 0.6))
        F.b((px, 0.3, pz - 0.8), (0.6, 0.5, 0.06), (0.80, 0.70, 0.35))
        for q, c in enumerate(cols):
            F.b((px, 0.3, pz - 0.74 + 0.12 * q + 0.06), (0.24, 0.24, 0.12), c)


# ── 20 · 21: 노을 마당
def props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    OR.orb((-12.0, 110.0, 6.0), 12.0, (3.0, 1.5, 0.5))
    OR.orb((-12.0, 116.0, 6.0), 24.0, (1.3, 0.55, 0.25))
    for q in range(3):
        a = 2 * math.pi * (0.2 * t + q / 3.0)
        mos(F, 1.8 * math.cos(a) + 0.2, -2.2 + 0.5 * math.sin(a), 1.9 + 0.3 * math.sin(2 * a), t, 2.0, 0.3 * q, (0.45, 0.4, 0.45))


def props_button(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    p = 1.0 + 0.06 * math.sin(2 * math.pi * t / 0.8)
    F.b((0.9, -0.3, 0.35), (0.45, 0.45, 0.7), (0.50, 0.52, 0.58))
    F.b((0.9, -0.3, 0.8 * p), (0.36, 0.36, 0.14), (0.88, 0.14, 0.12))
    wdig(G, DIG["?"], 0.9, -0.3, 1.5 + 0.04 * math.sin(2 * math.pi * t / 1.1), 0.12, GLOWY, pop(tau - 0.3, 0.3))


# ── 22: 눈 내리는 밤 곰 실루엣
def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    c = (0.20, 0.14, 0.10)
    F.b((0.0, 4.0, 1.0), (2.8, 1.4, 1.3), c)
    F.b((1.7, 4.0, 1.5), (0.9, 0.9, 0.85), c)
    F.b((2.2, 3.97, 1.4), (0.3, 0.5, 0.3), (0.12, 0.09, 0.07))
    for ey in (-0.3, 0.3):
        F.b((1.5, 4.0 + ey, 2.0), (0.22, 0.22, 0.25), c)
    for lx in (-1.0, 1.0):
        for ly in (-0.4, 0.4):
            F.b((lx, 4.0 + ly, 0.35), (0.5, 0.45, 0.7), c)
    for k in range(60):
        ph = (_h(k + 500) + 0.12 * t) % 1.0
        G.b((-5.0 + 10.0 * _h(k + 1) + 0.3 * math.sin(2 * math.pi * (t * 0.5 + _h(k))), 1.0 + 6.0 * _h(k + 77), 5.0 * (1.0 - ph)), (0.07, 0.07, 0.07), (2.4, 2.5, 2.8))


PROPS = {LN["hook"]: props_hook, LN["world"]: props_world, LN["slap"]: props_slap, LN["species"]: props_species, LN["pick"]: props_pick,
         LN["quiet"]: props_quiet, LN["toll"]: props_toll, LN["village"]: props_village, LN["under5"]: props_under5, LN["dmz"]: props_dmz,
         LN["korea"]: props_korea, LN["pond"]: props_pond, LN["web"]: props_web, LN["tundra"]: props_tundra, LN["twist"]: props_twist,
         LN["ship"]: props_ship, LN["summit"]: props_summit, LN["reduce"]: props_reduce, LN["million"]: props_million,
         LN["scales"]: props_scales, LN["dusk"]: props_dusk, LN["button"]: props_button, LN["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR, BL, LT = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off), Items(N_BL, off), []
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
def _hide(tau, t):
    return dict(z=-80.0)


def _kid(ph):
    return lambda tau, t: dict(z=0.14 * abs(math.sin(2 * math.pi * (t * 1.8 + ph))), yaw=-90 + 25 * math.sin(2 * math.pi * (t * 0.7 + ph)))


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    a0, b0 = shot_span(L["hook"])
    us = min(0.9, HK_SIT / max(b0 - a0, 1e-3))                     # 훅: 이 진행도부터 누운 지후 대신 일어난 지후
    add("jl", 0, JH_SH, JH_PA, {
        L["hook"]: [(0.0, st("camp", XL, 0.6, 0, "lie")), (us, st("camp", XL, 0.6, 0, "lie", fn=_hide))],
        L["quiet"]: st("camp", 3.6, -4.0, 0, "lie")})
    add("jh", 0, JH_SH, JH_PA, {
        L["hook"]: [(0.0, st("camp", 0.0, 0.0, 0, "sit_conf", fn=_hide)),
                    (us, st("camp", XL - 1.59, 0.6, 0, "sit_conf",
                            keys=[(0.0, (XL - 1.59, 0.6, 0.0, 0.0)), (0.12, (XL - 1.59, 0.6, 0.35, -30.0)), (0.4, (XL - 1.59, 0.6, 0.0, -90.0))]))],
        L["slap"]: st("camp", 4.0, -5.0, -90, "stand", seq=[(1.15, "shock"), (1.35, "think"), (2.1, "confused")]),
        L["dmz"]: st("dmz", 0.7, 2.0, -90, "think", seq=[(0.7, "point"), (1.2, "carry"), (2.0, "smile")]),
        L["summit"]: st("hawaii", -30.0, 4.5, -90, "smile", z=6.1, seq=[(1.2, "point"), (2.2, "smile")]),
        L["dusk"]: st("yard", 0.0, 0.0, -90, "look_up"),
        L["button"]: st("yard", -0.5, 0.0, -90, "point", seq=[(1.0, "smile")])}, extra="hood")
    add("rs", 1, CO_SH, CO_PA, {
        L["tundra"]: st("tundra", 0.0, 2.2, -90, "carry", seq=[(1.2, "point")]),
        }, extra="coat")
    # 연구실(17·19번 줄)은 몸을 0.8배로 줄여 낮은 받침 위에 세움 — 발이 자막 영역(아래 27%)에 안 걸리게
    add("rsl", 1, CO_SH, CO_PA, {
        L["reduce"]: st("lab", -1.15, 0.0, -90, "point", z=0.45, alt=("point", "think", 1.1, 0.3)),
        L["scales"]: st("lab", 1.35, 0.0, -90, "think", z=0.45, seq=[(1.0, "point")])}, scale=0.8, extra="coat")
    add("jhl", 0, JH_SH, JH_PA, {
        L["scales"]: st("lab", -1.35, 0.0, -90, "think", z=0.45, seq=[(1.0, "point")])}, scale=0.8, extra="hood")
    for n, (x, y, ph) in enumerate(((-0.7, 0.0, 0.0), (0.1, -0.8, 0.3), (0.9, 0.2, 0.55), (1.6, -0.6, 0.8), (0.5, 1.2, 0.15))):
        add("kid%d" % n, n % 2, EX_SH[(n * 2 + 1) % len(EX_SH)], X.PANTS[n % len(X.PANTS)], {
            L["village"]: st("village", x, y, -90, "walk_a_s", alt=("walk_a_s", "walk_b_s", 0.3, ph), fn=_kid(ph))}, scale=0.62)
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
NIGHT_SKY = ((0.03, 0.05, 0.16), (0.10, 0.16, 0.34), 0.8)
DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
ROOM_SKY = ((0.04, 0.05, 0.09), (0.10, 0.12, 0.18), 0.0)


def sky(t):
    s = cam_of(t)["set"]
    if s in ("camp", "snow"):
        return NIGHT_SKY
    if s == "lab":
        return ROOM_SKY
    return DUSK_SKY if s == "yard" else DAY_SKY


def env(i, st_):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.5, amb_col=(0.62, 0.68, 0.82), lt={})
    if st_ == "camp":
        e.update(sun=1.4, sun_col=(0.62, 0.72, 1.0), sun_rot=(55, 0, 35), amb=0.62, amb_col=(0.45, 0.55, 0.9), lt={"ep47_c0": 80.0, "ep47_c1": 130.0})
    elif st_ == "lab":
        e.update(sun=0.4, amb=0.62, amb_col=(0.72, 0.78, 0.95), lt={"ep47_l0": 260.0, "ep47_l1": 160.0})
    elif st_ == "yard":
        e.update(sun=2.4, sun_col=(1.0, 0.62, 0.38), sun_rot=(72, 0, 20), amb=0.34, amb_col=(0.72, 0.52, 0.62), lt={"ep47_y0": 60.0})
    elif st_ == "snow":
        e.update(sun=1.6, sun_col=(0.6, 0.7, 1.0), sun_rot=(60, 0, 30), amb=0.58, amb_col=(0.5, 0.6, 0.9), lt={"ep47_s0": 100.0})
    elif st_ == "tundra":
        e.update(sun=2.4, amb=0.55)
    return e


def postfx(img, t):
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
    v = X.Vox(47)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.5, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep47_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep47_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep47_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep47_fx", K.proto(ctx, "ep47_p_fx", cube(), [K.mat_inst("ep47_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep47_glow", K.proto(ctx, "ep47_p_glow", cube(), [_mat_glow("ep47_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep47_orb", K.proto(ctx, "ep47_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep47_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep47_bl", K.proto(ctx, "ep47_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep47_m_bl", 0.8)]),
                     N_BL, vector_scale=True)
    for ob in (gl, orb):                                              # 발광 상자가 햇빛을 가리지 않게
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
