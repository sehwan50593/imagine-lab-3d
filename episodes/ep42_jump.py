"""EP42 만약에 전 세계 80억 명이 같은 순간 점프한다면? (기준 영상 형식 STYLE='ref': 위 칩·제목 + 아래 자막, 내레이션 없음)

11-06 오너: "42~49 너가 알아서 형식대로(남자가 한 명뿐이라면 편), 나레이션은 너무 짜치니까 없애고" — 소리는 배경음(-23 LUFS)과 효과음뿐.
장면(3D)은 11-05 픽세판 상징 장면을 그대로 쓰고(지구·원자·TNT 막대·서울 판·블록 군중) 줄 순서만 시간순으로 바꿨다.
D-DAY 정오(훅: 들판 군중이 쿵쿵 점프, 끝 0.6초 작은 지구) → 점프 직전(한자리에 모임·40cm 줄자·하나 둘 셋)
→ 착지(먼지 고리, TNT 470 막대, 히로시마 구름) → +1초(지구 단면·원자 격자 1/800) → +1시간(발자국) → +1일(궤도)
→ 왜?(사람 점 80억·체중계 62·5억 톤 덩어리·저울) → 반전(지도판, 서울 1㎡에 13명) → 지금(노을, 물음표) → 다음 편(모래 구멍).
위 칩·제목은 묶음(GROUPS) 단위로 그대로 있고 아래 자막만 줄마다 바뀐다(engine/refstyle). 효과음: 0초·묶음 바뀜 '찰싹', 컷 '휙', 착지 '쿵'.

근거(설명란): ※ '80억 명이 같은 순간 40cm씩 점프하고 한곳에 모였다'는 가정의 상상 시나리오. 지후·시민과 그림 속 크기·비율은 연출.
· 세계 인구 약 80억: UN(2022-11-15 추정 돌파, World Population Prospects 2022)
· 성인 평균 체중 약 62kg: Walpole 외, BMC Public Health 12:439(2012) → 합계 약 5억 톤(8×10⁹×62kg, 상한 계산)
· 지구 질량 5.97×10²⁴kg → 인류 합계의 약 12조 배(계산) · NASA NSSDC, xkcd What If #8
· 점프 40cm는 가정(일반인 25~50cm). 에너지 62×9.8×0.4×8×10⁹ ≈ 1.9×10¹²J = TNT 약 470톤, 히로시마(약 15kt)의 약 1/32 · OSTI, Britannica
· 지구가 밀린 거리 ≈ 1.3×10⁻¹³m = 원자 지름(약 1.1×10⁻¹⁰m)의 약 1/800(운동량 보존 계산) · NIST CODATA, xkcd What If #8
· 자전·궤도 변화 없음, 몇 초 이어지는 굉음 · xkcd What If #8
· 서울(605.2㎢)에 세우면 1㎡에 약 13명(계산), 서 있는 군중은 1㎡에 5명 넘으면 위험 · 서울시 통계, G. Keith Still 군중 밀도 지침
"""
import math

import numpy as np

from engine import refstyle as R
from engine import voxel as X
from engine.common import clamp, keyed, lerp, ramp, smooth

STYLE = "ref"
# 세트 자리 (서로 300m씩 떨어뜨려 빛이 섞이지 않게). 들판 세트 안 x=60 자리에 체중계(FS)
OFF = {"field": (0, 0), "space": (300, 0), "energy": (600, 0), "atom": (900, 0), "map": (1200, 0), "sand": (1500, 0)}
FS = 60.0
# 시간순 줄 순서 (11-05 픽세판은 결과 먼저·되돌아가기였음). 'chel'(지난 편 소행성 비교)은 뺐다.
NAMES = ("hook", "gather", "ruler", "count", "land", "tnt", "hiro", "push", "atom", "prints", "orbit", "pop", "scale", "lump",
         "balance", "twist", "seoul", "scatter", "dusk", "ask", "teaser")
LN = {n: k for k, n in enumerate(NAMES)}

# d: 줄 길이(초) / sub: 아래 자막(두 줄까지) / shot: (세트, 목표점, 방위각, 고도각, 거리, 렌즈, 끝 거리 비율, 방위각 변화[, 렌즈 세로 이동[, 고도각 변화]])
# cuts: 한 줄 안의 짧은 연속 컷 [(끝 u, shot), ...]  ease="out": 처음에 빨리 움직이고 천천히 멈춤(훅)
H_A = ("field", (0.0, 0.0, 1.45), -90, 2, 3.6, 28, 0.74, 3, 0.10)
H_B = ("space", (0.0, 0.0, 0.0), -90, -10, 13.0, 26, 1.15, 0, 0.0, 22)
LINES = [
    dict(d=3.4, sub="오늘 정오, 80억 명이\n같은 순간 점프한다면?", ease="out", shot=H_A, cuts=[(0.8, H_A), (1.0, H_B)]),
    dict(d=2.8, sub="80억 명이 한자리에\n모였다고 가정합니다.", shot=("field", (0.0, 0.0, 1.0), -90, 3, 7.5, 26, 0.92, 3, 0.06)),
    dict(d=2.6, sub="모두 똑같이\n40cm씩 뜁니다.", shot=("field", (0.5, 0.0, 0.85), -90, 4, 4.8, 28, 0.9, -3, 0.06)),
    dict(d=3.2, sub="하나, 둘, 셋… 점프!", shot=("field", (0.0, 8.0, 1.5), -90, -3, 14.0, 24, 0.9, 0, 0.08, 7)),
    dict(d=2.8, sub="쿵! 먼지가 땅 위로\n둥글게 퍼집니다.", shot=("field", (0.0, 5.0, 1.0), -90, 8, 9.0, 24, 0.9, 0, 0.06, -4)),
    dict(d=3.0, sub="모두의 점프 에너지를 더하면\nTNT 약 470톤.", shot=("energy", (0.0, 0.0, 1.3), -90, 4, 9.0, 24, 0.92, 2, 0.05)),
    dict(d=3.0, sub="히로시마 원폭의\n약 30분의 1입니다.", shot=("energy", (0.0, 0.0, 2.1), -90, 3, 13.0, 24, 0.95, 0, 0.06)),
    dict(d=3.0, sub="사람들이 뛴 만큼\n지구도 반대로 밀렸지만", shot=("space", (0.0, 0.0, -0.25), -90, 2, 12.0, 26, 0.9, 2, 0.0)),
    dict(d=3.2, sub="그 거리는 원자 지름의\n800분의 1입니다.", shot=("atom", (0.0, 0.0, 0.0), -90, 2, 11.5, 26, 0.85, 0, 0.04)),
    dict(d=3.0, sub="땅에는 발자국만 가득,\n몇 초 이어진 굉음도 그쳤습니다.", shot=("field", (0.0, 6.0, 0.8), -90, 26, 12.0, 26, 0.92, 3, 0.03)),
    dict(d=2.8, sub="지구는 어제처럼 돌고\n궤도도 그대로입니다.", shot=("space", (0.0, 2.2, 0.0), -90, 22, 15.0, 26, 0.95, 5, 0.0)),
    dict(d=2.6, sub="지구에 사는 사람은\n약 80억 명.", shot=("space", (0.1, 0.0, 0.0), -90, 0, 15.5, 26, 0.95, 0, 0.0)),
    dict(d=2.6, sub="어른 평균 체중은\n약 62kg입니다.", shot=("field", (FS + 0.4, 0.0, 1.0), -72, 6, 6.6, 28, 0.9, -4, 0.07)),
    dict(d=2.8, sub="다 합치면 약 5억 톤.", shot=("space", (0.3, 0.0, 0.0), -84, 3, 16.5, 26, 0.92, 2, 0.0)),
    dict(d=3.0, sub="지구는 그보다\n약 12조 배 무겁습니다.", shot=("space", (0.0, 0.0, 1.5), -90, 4, 20.0, 26, 0.92, 3, 0.05)),
    dict(d=3.0, sub="어려운 건 점프가 아니라\n80억 명이 한자리에 서는 일.", shot=("map", (0.0, 1.0, 1.4), -90, 10, 10.0, 28, 0.88, 2, 0.04)),
    dict(d=3.6, sub="서울에 세우면 1㎡에 13명.\n5명만 넘어도 위험한 밀도입니다.", shot=("map", (0.0, -1.2, 0.85), -90, 42, 5.0, 24, 0.92, 2, 0.0)),
    dict(d=3.0, sub="그래서 동시 점프는\n상상 속에서만 가능합니다.", shot=("field", (0.0, 0.0, 1.0), -90, 3, 7.5, 26, 0.92, 3, 0.06)),
    dict(d=2.8, sub="인류는 가볍고,\n지구는 너무 무겁습니다.", shot=("field", (0.0, 0.0, 1.0), -80, 4, 6.5, 26, 0.9, -4, 0.06)),
    dict(d=3.2, sub="몇 명이면 될지\n댓글로 알려 주세요.", shot=("field", (0.0, 0.0, 1.45), -90, 2, 5.5, 30, 0.9, 0, 0.06)),
    dict(d=3.4, sub="발버둥 칠수록\n더 깊이 빠질까요?", shot=("sand", (0.0, 0.0, 0.4), -90, 38, 14.5, 26, 0.9, 3, 0.0)),
]
assert len(LINES) == len(NAMES)
GROUPS = [
    dict(at="hook", badge="D-DAY 정오", label="전 세계", big="80억 명", label_color="blue"),
    dict(at="gather", badge="점프 직전", title="모두 {yellow}40cm{/}씩 뛴다면"),
    dict(at="land", badge="착지", title="점프 에너지 합계", big="TNT 470톤", big_color="orange"),
    dict(at="push", badge="+1초", title="지구가 밀린 거리", big="원자의 1/800", big_color="yellow"),
    dict(at="prints", badge="+1시간", title="남은 건 {cyan}발자국{/}뿐"),
    dict(at="orbit", badge="+1일", title="자전도 공전도", big="그대로", big_color="green"),
    dict(at="pop", badge="왜?", title="80억 명을 다 합쳐도", big="약 5억 톤", big_color="orange"),
    dict(at="twist", badge="반전", title="진짜 문제는 {red}모이는 것{/}"),
    dict(at="seoul", badge="반전", title="서울에 다 세우면", big="1㎡에 13명", big_color="red"),
    dict(at="dusk", badge="지금", title="지구를 움직이려면\n{cyan}몇 명이 더{/} 필요할까요?", title_size=70),
    dict(at="teaser", badge="다음 편", title="오늘 저녁 7시\n{cyan}퀵샌드에 빠진다면?{/}", title_size=70),
]
TWIST = LN["twist"]  # 음악이 단조 느낌으로 바뀌는 곳
STARTS, DUR = R.starts_of(LINES)
BEATS = R.beats_of(LINES, STARTS, DUR, GROUPS, LN)
GRADE = {"exposure": 0.92, "bloom": 0.12, "bloom_thr": 1.4, "vignette": 0.16}
# 훅의 둘째 컷(우주)은 마지막 0.6초
LINES[0]["cuts"][0] = (max(0.5, 1.0 - 0.6 / max(STARTS[1], 1.0)), H_A)
# 점프 시간표: 모두 같은 위상 (period 주기, air 공중에 떠 있는 시간, JH 높이 m = 가정한 40cm)
JH = 0.40
HK_P, HK_AIR, HK_T0 = 0.75, 0.60, -0.12          # 훅: τ=0에서 이미 공중 상승 중 (착지 0.48, 1.23, 1.98초)


def t_jump6():
    """'점프!' 줄에서 점프가 시작하는 때(줄 시작 후 초)."""
    return 0.66 * LINES[LN["count"]]["d"]


_HOOK_LAND = [HK_T0 + HK_AIR + HK_P * n for n in range(5) if HK_T0 + HK_AIR + HK_P * n < STARTS[1] * LINES[0]["cuts"][0][0]]
_JUMP_LAND = STARTS[LN["count"]] + t_jump6() + HK_AIR
META = {"id": "ep42", "title": "만약에 전 세계 80억 명이 같은 순간 점프한다면?", "duration": DUR,
        "render": {"pct": 67, "samples": 12, "bounces": 3, "chunks": 9},
        "music": {"style": "pop", "key": "C", "mode": "major", "bpm": 100, "seed": 421, "twist_at": STARTS[TWIST],
                  "sfx": R.sfx_of(STARTS, GROUPS, LN, [[t, "thud", 0.6] for t in _HOOK_LAND] +
                                  [[_JUMP_LAND, "thud", 0.9], [_JUMP_LAND + 0.05, "rumble", 0.6, 1.6]])}}
assert 60.5 <= DUR <= 70.0, DUR   # 틱톡 수익화 1분 넘김


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


def jump_h(tau, t0, period, air, h):
    """t0부터 period마다 air초 동안 포물선으로 h m 솟았다 내려옴 (period가 크면 한 번)."""
    if period > 50.0 and tau < t0:
        return 0.0
    s = ((tau - t0) % period) / air
    return h * 4.0 * s * (1.0 - s) if s < 1.0 else 0.0


def hops(tau, dur):
    """'하나, 둘, 셋' 작은 도약 셋."""
    return sum(0.07 * max(0.0, 1.0 - ((tau - c * dur) / 0.14) ** 2) for c in (0.16, 0.30, 0.44))


def landings(i, tau):
    """줄 i에서 아직 퍼지는 중인 착지들의 경과 시간 [age, ...] (착지 뒤 1.1초까지)."""
    if i == LN["hook"]:
        ts = [HK_T0 + HK_AIR + HK_P * n for n in range(5)]
    elif i == LN["count"]:
        ts = [t_jump6() + HK_AIR]
    elif i == LN["land"]:
        ts = [-landing_lag()]
    else:
        return []
    return [tau - tl for tl in ts if 0.0 <= tau - tl < 1.1]


def landing_lag():
    """11번 줄(점프) 착지 순간부터 12번 줄(먼지) 시작까지 지난 시간 — 먼지 고리와 흔들림이 줄 경계를 넘어 이어짐."""
    a, b = shot_span(LN["count"])
    return b - (a + t_jump6() + HK_AIR)


# ───────────────────────── 카메라 (블렌더 없이 계산) ─────────────────────────
def _shake_spec(i):
    """줄 i의 흔들림 [(시작 τ, 길이, 이동 세기 m, 각도 세기 도, 진동수 Hz, 종류)]. 'hold' 거의 일정, 'hit' 점점 잦아듦."""
    if i == LN["hook"]:
        return [(0.0, 99.0, 0.035, 0.0, 15.0, "hold")] + [(HK_T0 + HK_AIR + HK_P * n, 0.6, 0.05, 0.5, 13.0, "hit") for n in range(3)]
    if i == LN["count"]:
        return [(t_jump6() + HK_AIR, 0.9, 0.10, 0.5, 13.0, "hit")]
    if i == LN["land"]:
        return [(-landing_lag(), 0.9, 0.10, 0.5, 13.0, "hit")]
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


# ───────────────────────── 색 · 군중 · 도트 글자 ─────────────────────────
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


def _make_crowd():
    """사람 점 군중: 행 간격 1.22배씩 늘려 지평선(y≈80)까지. 카메라 앞 가운데(지후 자리)는 비움."""
    rs = np.random.default_rng(421)
    out, y = [], 2.2
    while y < 85.0:
        hw = 0.30 * (y + 3.6) + 1.5
        n = int(2 * hw / 0.9)
        for x in np.linspace(-hw, hw, n) + rs.uniform(-0.25, 0.25, n):
            if y < 8.0 and abs(float(x)) < 0.75:
                continue
            out.append((float(x), y + float(rs.uniform(-0.3, 0.3)), EX_SH[int(rs.integers(len(EX_SH)))],
                        X.PANTS[int(rs.integers(len(X.PANTS)))]))
        y *= 1.22
    return out


CROWD = _make_crowd()


def crowd_draw(F, z=0.0, spread=0.0):
    """군중 전원을 같은 높이 z로 (spread 0→1: 바깥으로 흩어지며 작아짐)."""
    k = 1.3 * (1.0 - spread)
    if k <= 0.03:
        return
    for x, y, sh, pa in CROWD:
        px, py = x * (1.0 + 1.2 * spread), y * (1.0 + 0.4 * spread)
        F.b((px, py, z + 0.25 * k), (0.34 * k, 0.20 * k, 0.50 * k), pa)
        F.b((px, py, z + 0.75 * k), (0.40 * k, 0.22 * k, 0.50 * k), sh)
        F.b((px, py, z + 1.13 * k), (0.26 * k, 0.26 * k, 0.26 * k), SKINC)


def shock_ring(F, age, c=(0.0, 0.0), speed=28.0, n=64, z0=0.1):
    """착지 먼지 고리: 지후 둘레에서 초당 speed m로 퍼지다 작아져 사라짐."""
    fade = 1.0 - ramp(age, 0.5, 1.1)
    if fade <= 0.01:
        return
    r = 0.4 + age * speed
    sz = (0.35 + 0.012 * r) * fade
    for q in range(n):
        a = 2 * math.pi * (q + 0.5 * _h(q)) / n
        F.b((c[0] + r * math.cos(a), c[1] + r * math.sin(a), z0 + 0.4 * sz), (sz, sz, sz * 0.8), DUSTC)


# ───────────────────────── 세트 ─────────────────────────
def _field(v):
    v.floor(-70, 90, -10, 125, GRASS, 2.5)
    rs = v.rs
    for k in range(14):                                       # 먼 언덕 (y를 조금씩 비껴 놓음)
        x0 = -130 + 22 * k
        h = float(rs.uniform(5, 14))
        v.box(x0, x0 + 26, 128 + 3.1 * (k % 4), 150 + 3.1 * (k % 4), 0, h, (0.28 + 0.03 * (k % 3), 0.46, 0.34 + 0.02 * (k % 2)), jit=0.05)
    # 체중계 (x = FS)
    v.box(FS - 0.8, FS + 0.8, -0.7, 0.7, 0.0, 0.12, (0.80, 0.80, 0.82))
    v.box(FS - 0.65, FS + 0.65, -0.55, 0.55, 0.12, 0.14, (0.30, 0.30, 0.34), jit=0)
    v.box(FS + 1.2, FS + 1.4, 0.15, 0.25, 0.0, 0.9, (0.30, 0.32, 0.38))
    v.box(FS + 0.9, FS + 1.7, 0.1, 0.3, 0.9, 1.7, (0.07, 0.08, 0.10), jit=0)


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


def _energy(v):
    v.floor(-9, 9, -3, 6, (0.10, 0.12, 0.18), 0.5, "check")
    v.wall((-9, 6), (9, 6), 0, 7, (0.12, 0.15, 0.24), 0.5, face=-1)
    v.box(-6, 6, 5.93, 5.99, 0.18, 0.22, (0.35, 0.80, 1.0), jit=0, glow=True)
    v.box(-6, 6, 5.93, 5.99, 4.9, 4.94, (0.35, 0.80, 1.0), jit=0, glow=True)
    v.light(0.0, 1.0, 6.0, 170, (0.85, 0.92, 1.0), 1.0, "ep42_en0")
    v.light(-3.0, -1.0, 5.0, 110, (1.0, 0.92, 0.8), 0.8, "ep42_en1")


def _atom(v):
    v.floor(-6, 6, -4, 6, (0.07, 0.10, 0.14), 0.5, "check")
    v.wall((-6, 6), (6, 6), 0, 6, (0.07, 0.11, 0.16), 0.5, face=-1)
    for k in range(-4, 5):
        v.box(k - 0.015, k + 0.015, 5.93, 5.97, 0.0, 6.0, (0.10, 0.30, 0.40), jit=0, glow=True)
    v.light(0.0, -1.0, 4.5, 150, (0.85, 0.92, 1.0), 0.9, "ep42_at0")


def _map(v):
    v.floor(-7, 7, -5, 8, (0.50, 0.36, 0.24), 0.5, "wood")
    v.wall((-7, 6.5), (7, 6.5), 0, 5, (0.16, 0.30, 0.33), 0.5, face=-1)
    v.box(-2.2, 2.2, -2.4, 2.4, 0.7, 0.8, (0.60, 0.42, 0.26))
    for sx in (-2.05, 2.05):
        for sy in (-2.25, 2.25):
            v.box(sx - 0.1, sx + 0.1, sy - 0.1, sy + 0.1, 0.0, 0.7, (0.45, 0.31, 0.20))
    v.light(0.0, 0.0, 4.5, 150, (1.0, 0.95, 0.85), 0.9, "ep42_map0")
    v.light(0.0, -4.0, 3.0, 90, (1.0, 0.92, 0.8), 0.8, "ep42_map1")


def _sand(v):
    v.floor(-30, 30, -20, 40, (0.86, 0.74, 0.50), 1.0)
    v.box(-0.55, 0.55, -0.55, 0.55, 0.0, 0.012, (0.35, 0.26, 0.16), jit=0)
    for j in range(7):                                        # 깔때기: 안쪽이 낮고 바깥이 높은 단
        a, w, h = 0.6 + 0.5 * j, 0.5, 0.12 * (j + 1)
        col = (0.82 - 0.02 * j, 0.68 - 0.02 * j, 0.44 - 0.02 * j)
        v.box(-(a + w), a + w, a, a + w, 0, h, col)
        v.box(-(a + w), a + w, -(a + w), -a, 0, h, col)
        v.box(a, a + w, -a, a, 0, h, col)
        v.box(-(a + w), -a, -a, a, 0, h, col)


def _sets():
    return (("field", _field), ("space", _space), ("energy", _energy), ("atom", _atom), ("map", _map), ("sand", _sand))


# ───────────────────────── 소품 · 효과 (상자 F · 발광 상자 G · 발광 구 OR · 조명 받는 구 BL) ─────────────────────────
N_FX, N_GL, N_OR, N_BL = 1900, 600, 40, 40


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


def props_hook(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    if cam["set"] == "field":
        crowd_draw(F, jump_h(tau, HK_T0, HK_P, HK_AIR, JH))
        for age in landings(i, tau):
            shock_ring(F, age)
    else:
        earth_items(F, BL, cam, (0.0, 0.0, 0.0), RE, sp_of(t))


# ── 1 · 3: 지구 옆 사람 점 → 큰 상자
EARTH_L = (-1.9, 0.0, 0.0)
_rd = np.random.default_rng(4242)
DOTS = [(1.0 + 0.2 * c, -1.9 + 0.2 * r) for c in range(12) for r in range(20)]
DOT_COL = [EX_SH[int(_rd.integers(len(EX_SH)))] for _ in DOTS]
RANK = _rd.permutation(len(DOTS)) / float(len(DOTS))
_grid = [(2.2 + (a / 5.0 - 0.5) * 1.5, (b / 4.0 - 0.5) * 1.5, (c / 7.0 - 0.5) * 1.5) for a in range(6) for b in range(5) for c in range(8)]
TGT = [_grid[j] for j in _rd.permutation(len(_grid))]


def props_pop(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    earth_items(F, BL, cam, EARTH_L, RE, sp_of(t))
    f = ramp(tau, 0.15, dur * 0.9)
    for k, (x, z) in enumerate(DOTS):
        if f > RANK[k]:
            s = pop((f - RANK[k]) * dur * 0.9, 0.22)
            F.b((x, 0.0, z), (0.14 * s, 0.14 * s, 0.14 * s), DOT_COL[k])


def props_lump(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    earth_items(F, BL, cam, EARTH_L, RE, sp_of(t))
    m = smooth(tau / (dur * 0.75))
    for k, (x, z) in enumerate(DOTS):
        tx, ty, tz = TGT[k]
        F.b((lerp(x, tx, m), lerp(0.0, ty, m), lerp(z, tz, m)), (0.14, 0.14, 0.14), DOT_COL[k])
    s = ramp(tau, dur * 0.55, dur * 0.95)
    if s > 0.02:
        F.b((2.2, 0.0, 0.0), (1.8 * s, 1.8 * s, 1.8 * s), (0.82, 0.58, 0.28))


# ── 2: 체중계
def props_scale(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    if tau > 0.75:
        wdig(G, num_rows("62"), FS + 1.3, 0.07, 1.3, 0.11, (1.0, 0.95, 0.5), pop(tau - 0.75, 0.3))


# ── 4: 저울 (지구 쪽이 내려가 꿈쩍 않음, 지후가 오른쪽 쟁반에서 비틀)
BAL_C, BAL_L, BAL_RY, BAL_RB = np.array((0.0, 0.0, 1.4)), 7.0, -0.33, 1.2


def bal_geom(t):
    ry = BAL_RY + 0.007 * math.sin(2 * math.pi * t / 0.55)         # 지후가 뛰어도 아주 조금만 떨림
    half = _rmat(0.0, ry, 0.0) @ np.array((BAL_L / 2, 0.0, 0.0))
    return ry, BAL_C - half, BAL_C + half


def jh_bal(tau, t):
    _, left, right = bal_geom(t)
    hop = 0.07 * abs(math.sin(2 * math.pi * t / 0.55))
    return dict(x=right[0] + 0.55 + 0.12 * math.sin(2 * math.pi * t / 1.1), z=right[2] + 0.1 + hop, yaw=-90 + 12 * math.sin(2 * math.pi * t / 0.9),
                pose="shock" if int(t / 0.55) % 2 else "stand")


def props_balance(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    ry, left, right = bal_geom(t)
    F.c(tuple(BAL_C), (BAL_L, 0.30, 0.25), (0.62, 0.62, 0.66), (0.0, ry, 0.0))
    F.b((0.0, 0.0, 0.1), (0.3, 0.3, 2.4), (0.45, 0.45, 0.5))
    F.b((0.0, 0.0, -1.0), (2.0, 1.0, 0.2), (0.40, 0.40, 0.45))
    for p in (left, right):
        F.b((p[0], p[1], p[2] + 0.08), (2.0, 1.1, 0.1), (0.80, 0.70, 0.35))
    earth_items(F, BL, cam, (left[0], left[1], left[2] + 0.13 + BAL_RB), BAL_RB, sp_of(t))
    F.b((right[0] - 0.6, 0.0, right[2] + 0.13 + 0.25), (0.5, 0.5, 0.5), (0.82, 0.58, 0.28))


# ── 5: 줄자
def props_ruler(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    crowd_draw(F, 0.0)
    xr = 0.95
    F.b((xr, 0.06, 0.85), (0.10, 0.03, 1.7), (0.93, 0.90, 0.76))
    for k in range(1, 17):
        big = k % 5 == 0
        F.b((xr - 0.09 - (0.03 if big else 0.0), 0.05, 0.1 * k), (0.08 + (0.06 if big else 0.0), 0.02, 0.012), (0.2, 0.2, 0.2))
    p = 0.6 + 0.4 * math.sin(2 * math.pi * t / 0.6)
    G.b((0.55, 0.03, 0.4), (1.2, 0.03, 0.025), (3.0 * p, 2.4 * p, 0.4 * p))
    wdig(G, num_rows("40cm"), 0.5, 0.03, 1.75, 0.06, (3.0, 2.6, 0.8), pop(tau - 0.3, 0.3))


# ── 6: 하나·둘·셋·점프
def props_count(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    crowd_draw(F, jump_h(tau, t_jump6(), 99.0, HK_AIR, JH) + hops(tau, dur))
    for age in landings(i, tau):
        shock_ring(F, age)


# ── 7~9: 에너지 비교판
def tnt_crate(F, G, cx, cz, s):
    F.b((cx, 0.0, cz), (s, s * 0.8, s * 0.7), (0.80, 0.18, 0.14))
    F.b((cx - s * 0.32, 0.0, cz), (s * 0.1, s * 0.84, s * 0.74), (0.25, 0.08, 0.07))
    F.b((cx + s * 0.32, 0.0, cz), (s * 0.1, s * 0.84, s * 0.74), (0.25, 0.08, 0.07))
    wdig(G, num_rows("TNT"), cx, -(s * 0.4) - 0.03, cz, s * 0.8 / 11.0, (1.0, 0.95, 0.8))


def props_tnt(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    age = tau
    if age < 0.7:                                             # 착지 먼지 고리 (작게)
        fade = 1.0 - ramp(age, 0.3, 0.7)
        for q in range(28):
            a = 2 * math.pi * q / 28
            sz = 0.25 * fade
            F.b((1.4 * math.cos(a) * (0.3 + age * 3.0), -1.0 + 0.5 * math.sin(a) * (0.3 + age * 3.0), 0.05 + 0.4 * sz), (sz, sz, sz * 0.8), DUSTC)
    tnt_crate(F, G, -1.6, 1.3, 1.1)
    L = 4.3 * ramp(tau, 0.3, dur * 0.7)
    if L > 0.02:
        F.b((-2.3 + L / 2, 0.0, 0.5), (L, 0.3, 0.3), (0.95, 0.5, 0.15))
    wdig(G, num_rows("470"), 0.7, -0.1, 1.45, 0.2, (3.0, 2.6, 0.8), pop(tau - 0.6, 0.3))


def props_hiro(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    g = ramp(tau, 0.0, 0.9)
    cx = 2.2
    F.b((cx, 0.0, 1.15 * g + 0.02), (0.75, 0.75, 2.3 * g + 0.04), (0.58, 0.54, 0.50))
    F.b((cx, 0.0, 2.55 * g), (1.6, 1.6, 0.7), (0.95, 0.50, 0.20))
    F.b((cx, 0.0, 3.2 * g), (2.4, 2.2, 0.6), (0.85, 0.40, 0.15))
    F.b((cx, 0.0, 3.75 * g), (1.8, 1.8, 0.5), (0.55, 0.50, 0.48))
    tnt_crate(F, G, -2.3, 0.25, 0.4)
    F.b((-1.65, 0.0, 0.2), (0.16, 0.12, 0.12), (0.95, 0.5, 0.15))


def _disc():
    out = []
    for a in range(-10, 11):
        for b in range(-10, 11):
            x, z = 0.2 * a, 0.2 * b
            r = math.hypot(x, z) / 2.0
            if r > 1.0:
                continue
            if r < 0.19:
                c = (1.0, 0.85, 0.35)
            elif r < 0.55:
                c = (0.95, 0.50, 0.15)
            elif r < 0.93:
                c = (0.62, 0.26, 0.15)
            else:
                c = (0.15, 0.36, 0.72) if _h(a * 31 + b) < 0.6 else (0.22, 0.52, 0.28)
            out.append((x, z, c))
    return out


DISC = _disc()


def props_push(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for x, z, c in DISC:
        F.b((x, 0.0, z), (0.19, 0.08, 0.19), c)
    s = pop(tau - 0.5, 0.3)
    if s > 0.01:
        d = 0.9 + 0.1 * math.sin(2 * math.pi * t / 0.5)
        for dz, w in ((0.0, 0.05), (-0.1, 0.20), (-0.17, 0.12), (-0.22, 0.05)):
            G.b((0.0, -0.1, -2.3 + dz * d), (w * s, 0.05, 0.06 * s), (3.0, 2.6, 0.5))


# ── 11: 원자 격자 + 헛도는 돋보기
def props_atom(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for r in range(4):
        for c in range(5):
            x, z = (c - 2) * 1.0, (r - 1.5) * 1.0 + 0.3
            j = 0.03 * math.sin(2 * math.pi * t / 0.4 + 1.7 * (r * 5 + c))
            BL.orb((x + j, 0.0, z), 0.7, (0.88, 0.72, 0.30) if (r + c) % 2 else (0.55, 0.72, 0.95))
    F.b((0.0, 0.05, -2.2), (6.0, 0.05, 0.12), (0.80, 0.80, 0.82))
    for k in range(-3, 4):
        F.b((float(k), 0.02, -2.4), (0.04, 0.04, 0.3), (0.2, 0.2, 0.2))
    s = 0.6 + 0.9 * (tau / dur)
    mx, mz = 1.0 * math.cos(1.8 * t), -1.9 + 0.35 * math.sin(2.2 * t)
    for q in range(20):
        a = 2 * math.pi * q / 20
        G.b((mx + 0.45 * s * math.cos(a), -0.4, mz + 0.45 * s * math.sin(a)), (0.09 * s, 0.05, 0.09 * s), (2.4, 2.2, 1.2))
    F.c((mx + 0.62 * s, -0.4, mz - 0.62 * s), (0.8 * s, 0.1 * s, 0.1 * s), (0.45, 0.30, 0.18), (0.0, 0.785, 0.0))


# ── 12: 자전하는 지구와 변함없는 궤도선
def props_orbit(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    earth_items(F, BL, cam, (0.0, 0.0, 0.0), 1.5, 1.2 * t)
    for q in range(96):
        a = 2 * math.pi * q / 96
        G.b((4.2 * math.cos(a), 4.2 + 4.2 * math.sin(a), 0.0), (0.09, 0.09, 0.09), (0.5, 2.0, 2.4))
    OR.orb((0.0, 4.2, 0.0), 1.6, (3.0, 2.4, 0.8))


# ── 13: 발자국 + 소리 파동
_rp = np.random.default_rng(1313)
PRINTS = [(float(_rp.uniform(-2.2, 2.2)), float(_rp.uniform(3.0, 10.0)), float(_rp.uniform(-0.5, 0.5)), float(_rp.random())) for _ in range(220)]


def props_prints(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    f = ramp(tau, 0.1, dur * 0.8)
    for x, y, yaw, rk in PRINTS:
        if f > rk:
            F.c((x, y, 0.014), (0.30, 0.13, 0.02), (0.22, 0.30, 0.16), (0.0, 0.0, yaw))
    F.b((-0.6, 8.0, 1.4), (0.5, 0.4, 0.7), (0.15, 0.15, 0.18))
    F.b((-0.2, 8.0, 1.4), (0.4, 0.8, 0.9), (0.25, 0.25, 0.30))
    for r in (0.7, 1.2, 1.7):
        w = max(0.0, math.sin(2 * math.pi * (t * 1.4 - r * 0.5)))
        for a in range(-40, 41, 10):
            ra = math.radians(a)
            G.b((-0.1 + r * math.cos(ra), 7.95, 1.4 + r * math.sin(ra)), (0.12, 0.05, 0.12), (2.6 * (0.3 + w), 2.4 * (0.3 + w), 1.0))


# ── 16·17: 지도판 (서울 한 장)
PAPER = (0.94, 0.88, 0.70)
SE_C = (0.0, -1.2)


def _tiles(cx, cy, nx, ny, size=0.2):
    return [(cx - nx * size / 2 + size * (i + 0.5), cy - ny * size / 2 + size * (j + 0.5)) for i in range(nx) for j in range(ny)]


TILES_SE = _tiles(*SE_C, 6, 4)
_rm = np.random.default_rng(1515)
SLOTS = [[((a % 4 - 1.5) * 0.045, (a // 4 - 1.5) * 0.045) for a in _rm.permutation(16)] for _ in range(len(TILES_SE))]
DRANK = [[float(_rm.random()) for _ in range(13)] for _ in range(len(TILES_SE))]
GREEN, ORANGE, RED = (0.30, 0.85, 0.35), (1.0, 0.62, 0.15), (0.95, 0.15, 0.12)


def dens_col(m):
    """0 초록 → 0.5 주황 → 1 빨강."""
    return tuple(lerp(a, b, m * 2.0) for a, b in zip(GREEN, ORANGE)) if m < 0.5 else tuple(lerp(a, b, m * 2.0 - 1.0) for a, b in zip(ORANGE, RED))


def map_frame(F, c, w, h, col):
    for dy in (-1, 1):
        F.b((c[0], c[1] + dy * (h / 2 + 0.015), 0.855), (w + 0.06, 0.03, 0.03), col)
    for dx in (-1, 1):
        F.b((c[0] + dx * (w / 2 + 0.015), c[1], 0.855), (0.03, h, 0.03), col)


def map_dots(F, tiles, base, per, f, col, tcol):
    for k, (x, y) in enumerate(tiles):
        kk = base + k
        F.b((x, y, 0.843), (0.19, 0.19, 0.006), tcol)
        for q in range(per):
            if f > DRANK[kk][q % 13] * 0.9 + 0.05 * (q // 13):
                ox, oy = SLOTS[kk][q]
                F.b((x + ox, y + oy, 0.896), (0.04, 0.04, 0.10), col)


def props_twist(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    sp = 0.2 + 0.8 * ramp(tau, 0.0, 0.9)
    F.b((0.0, 0.0, 0.82), (3.9 * sp, 4.3 * sp, 0.04), PAPER)


def props_seoul(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    F.b((0.0, 0.0, 0.82), (3.9, 4.3, 0.04), PAPER)
    m = ramp(tau, 0.2, dur * 0.9)
    map_frame(F, SE_C, 1.2, 0.8, (0.30, 0.62, 1.0))
    map_dots(F, TILES_SE, 0, 13, ramp(tau, 0.05, dur * 0.6), dens_col(m), tuple(0.5 * c + 0.5 for c in dens_col(m)))


# ── 9 · 12: 모여듦 · 착지 뒤 먼지
def props_gather(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    crowd_draw(F, 0.0, 1.0 - ramp(tau, 0.1, dur * 0.8))


def props_land(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    crowd_draw(F, 0.0)
    for age in landings(i, tau):
        shock_ring(F, age)
    shock_ring(F, 0.45 * (tau + landing_lag()))               # 느리게 번지는 둘째 먼지 고리


# ── 18~20 들판 마무리, 21 모래 구멍
def props_scatter(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    crowd_draw(F, 0.0, ramp(tau, 0.15, dur * 0.95))


def props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    OR.orb((-12.0, 110.0, 6.0), 12.0, (3.0, 1.5, 0.5))
    OR.orb((-12.0, 116.0, 6.0), 24.0, (1.3, 0.55, 0.25))


def props_ask(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    props_dusk(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    wdig(G, DIG["?"], 0.62, 0.8, 1.75 + 0.05 * math.sin(2 * math.pi * t / 1.1), 0.20, (3.0, 2.6, 0.9), pop(tau - 0.3, 0.3))


def props_teaser(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT):
    for k in range(60):
        ph = (_h(k + 500) + 0.35 * t) % 1.0
        a = 2 * math.pi * _h(k + 700) + 2.0 * ph
        r = 3.4 * (1.0 - ph) + 0.3
        F.b((r * math.cos(a), r * math.sin(a), 0.3 + 0.8 * (1.0 - ph) ** 2), (0.12, 0.12, 0.12), (0.84, 0.70, 0.46))


PROPS = {LN["hook"]: props_hook, LN["pop"]: props_pop, LN["scale"]: props_scale, LN["lump"]: props_lump, LN["balance"]: props_balance,
         LN["gather"]: props_gather, LN["ruler"]: props_ruler, LN["count"]: props_count, LN["land"]: props_land, LN["tnt"]: props_tnt,
         LN["hiro"]: props_hiro, LN["push"]: props_push, LN["atom"]: props_atom, LN["orbit"]: props_orbit,
         LN["prints"]: props_prints, LN["twist"]: props_twist, LN["seoul"]: props_seoul, LN["scatter"]: props_scatter,
         LN["dusk"]: props_dusk, LN["ask"]: props_ask, LN["teaser"]: props_teaser}


def props(i, tau, dur, u, S, t, cam):
    """i번째 줄의 소품: (상자 F, 발광 상자 G, 발광 구 OR, 조명 받는 구 BL, 점광원 LT) — 좌표는 세트 기준(Items가 세트 자리를 더함)."""
    off = OFF[cam["set"]]
    F, G, OR, BL, LT = Items(N_FX, off), Items(N_GL, off), Items(N_OR, off), Items(N_BL, off), []
    fn = PROPS.get(i)
    if fn:
        fn(i, tau, dur, u, S, t, cam, F, G, OR, BL, LT)
    return F, G, OR, BL, LT


# ───────────────────────── 등장인물 ─────────────────────────
def jh_hook(tau, t):
    z = jump_h(tau, HK_T0, HK_P, HK_AIR, JH)
    return dict(z=z, pose="shock" if z > 0.04 else "smile")


def jh_count(tau, t):
    z = jump_h(tau, t_jump6(), 99.0, HK_AIR, JH)
    dur = shot_span(LN["count"])[1] - shot_span(LN["count"])[0]
    z += hops(tau, dur)
    return dict(z=z, pose="shock" if z > 0.04 else "smile")


def jh_dusk(tau, t):
    z = jump_h(tau, 0.3, 1.6, 0.9, JH)
    return dict(z=z, pose="shock" if z > 0.1 else "smile")


def cast():
    """[dict(name, hair, extra, shirt, pants, scale, at={줄: 상태 또는 [(시작 u, 상태), ...]})] — at에 없는 줄엔 안 보임."""
    C = []
    L = LN

    def add(name, hair, shirt, pants, at, scale=1.0, extra=""):
        C.append(dict(name=name, hair=hair, extra=extra, shirt=shirt, pants=pants, at=at, scale=scale))
    add("jh", 0, JH_SH, JH_PA, {
        L["hook"]: st("field", 0.0, 0.0, -90, "smile", fn=jh_hook, also=("shock", "smile")),
        L["scale"]: st("field", FS, 0.0, -90, "stand", keys=[(0.0, (FS - 1.0, 0.0, 0.0, -90.0)), (0.7, (FS, 0.0, 0.14, -90.0))],
                       seq=[(0.9, "smile")]),
        L["balance"]: st("space", 3.0, 0.0, -90, "stand", fn=jh_bal, also=("shock",)),
        L["ruler"]: st("field", 0.0, 0.0, -90, "think", seq=[(1.0, "point")]),
        L["count"]: st("field", 0.0, 0.0, -90, "smile", fn=jh_count, also=("shock",)),
        L["twist"]: st("map", 0.0, 3.4, -90, "point", seq=[(1.2, "smile")]),
        L["gather"]: st("field", 0.0, 0.0, -90, "point", alt=("point", "smile", 0.35, 0.0)),
        L["land"]: st("field", 0.0, 0.0, -90, "gape", seq=[(0.9, "smile")]),
        L["scatter"]: st("field", 0.0, 0.0, -90, "point", alt=("point", "smile", 0.35, 0.0)),
        L["dusk"]: st("field", 0.0, 0.0, -80, "smile", fn=jh_dusk, also=("shock",)),
        L["ask"]: st("field", 0.0, 0.0, -90, "think", seq=[(0.9, "smile")])}, extra="hood")
    add("rs", 1, CO_SH, CO_PA, {
        L["seoul"]: st("map", -1.0, -1.2, 0, "point", alt=("point", "think", 1.1, 0.3))}, extra="coat")
    return C


# ───────────────────────── 빛 · 하늘 · 장면 상태 ─────────────────────────
def set_of(i):
    return LINES[i]["shot"][0]


DAY_SKY = ((0.16, 0.30, 0.62), (0.52, 0.64, 0.82), 0.0)
DUSK_SKY = ((0.30, 0.22, 0.46), (0.98, 0.55, 0.30), 0.0)
SPACE_SKY = ((0.003, 0.004, 0.014), (0.010, 0.013, 0.034), 1.8)
ROOM_SKY = ((0.04, 0.05, 0.09), (0.10, 0.12, 0.18), 0.0)
SAND_SKY = ((0.25, 0.45, 0.75), (0.95, 0.82, 0.62), 0.0)


def sky(t):
    i = line_at(t)
    s = LINES[i]["cuts"][-1][1][0] if False else cam_of(t)["set"]
    if s == "space":
        return SPACE_SKY
    if s in ("energy", "atom", "map"):
        return ROOM_SKY
    if s == "sand":
        return SAND_SKY
    return DUSK_SKY if i in (LN["dusk"], LN["ask"]) else DAY_SKY


def env(i, st_):
    """줄(컷 세트)별 해·주변광 + 켜 둘 조명 {이름: 세기}."""
    e = dict(sun=3.0, sun_col=(1.0, 0.92, 0.8), sun_rot=(50, 0, 35), amb=0.42, amb_col=(0.62, 0.68, 0.82), lt={})
    if st_ == "field" and i in (LN["dusk"], LN["ask"]):
        e.update(sun=2.4, sun_col=(1.0, 0.62, 0.38), sun_rot=(72, 0, 20), amb=0.30, amb_col=(0.72, 0.52, 0.62))
    elif st_ == "space":
        e.update(sun=4.2, sun_col=(1.0, 0.96, 0.9), sun_rot=(55, 0, 60), amb=0.08, amb_col=(0.30, 0.36, 0.62))
    elif st_ == "energy":
        e.update(sun=0.4, amb=0.45, amb_col=(0.70, 0.76, 0.92), lt={"ep42_en0": 170.0, "ep42_en1": 110.0})
    elif st_ == "atom":
        e.update(sun=0.4, amb=0.40, amb_col=(0.70, 0.76, 0.92), lt={"ep42_at0": 150.0})
    elif st_ == "map":
        e.update(sun=0.5, amb=0.45, amb_col=(0.80, 0.82, 0.90), lt={"ep42_map0": 150.0, "ep42_map1": 90.0})
    elif st_ == "sand":
        e.update(sun=3.2, sun_col=(1.0, 0.88, 0.70), sun_rot=(55, 0, 30), amb=0.40, amb_col=(0.80, 0.78, 0.72))
    return e


# 번쩍 (줄, 줄 시작 후 초, 세기, 길이 초) — STYLE='pixe'에선 overlay의 FLASH가 안 쓰여서 postfx에서 화면 전체에 얹음
def _flashes():
    return [(LN["hook"], HK_T0 + HK_AIR, 0.30, 0.16), (LN["count"], t_jump6() + HK_AIR, 0.30, 0.16)]


WARM = np.array((1.0, 0.95, 0.86), np.float32)


def flash_level(t):
    a = 0.0
    for i, tau0, peak, dur in _flashes():
        t0 = shot_span(i)[0] + tau0
        a = max(a, peak * clamp((t - t0 + 0.02) / 0.03) * (1.0 - clamp((t - t0 - 0.01) / dur)))
    return a


def postfx(img, t):
    """번쩍(전체 화면): 훅 첫 착지, 6번 줄 착지."""
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
    v = X.Vox(42)
    for name, fn in _sets():
        v.at(*OFF[name])
        fn(v)
    obs, lights = v.build(ctx, glow_strength=3.0)
    K.world_space(ctx, ambient=(0.62, 0.68, 0.82), ambient_strength=0.42, ground=(0.2, 0.2, 0.22))
    sun = K.sun(ctx, 3.0, name="ep42_sun")
    cam = K.CamRig(ctx, lens=28, fstop=0)

    W = _world()
    mats = X.people_mats()
    protos = [K.proto(ctx, "ep42_p_%02d" % n, K.join_bms(_person_parts(*k)), mats) for n, k in enumerate(W["keys"])]
    people = K.instancer_multi(ctx, "ep42_people", protos, len(W["C"]))
    cube = lambda: K.bm_cube(1, 1, 1, (0.5, 0, 0))                    # 원점 = 뒷면 가운데, +x로 뻗음 (size로 늘림)
    fx = K.instancer(ctx, "ep42_fx", K.proto(ctx, "ep42_p_fx", cube(), [K.mat_inst("ep42_m_fx", 0.7)]), N_FX, vector_scale=True)
    gl = K.instancer(ctx, "ep42_glow", K.proto(ctx, "ep42_p_glow", cube(), [_mat_glow("ep42_m_glow")]), N_GL, vector_scale=True)
    orb = K.instancer(ctx, "ep42_orb", K.proto(ctx, "ep42_p_orb", K.bm_sphere(0.5, (0, 0, 0), 24, 12), [_mat_glow("ep42_m_orb")]),
                      N_OR, vector_scale=True)
    bl = K.instancer(ctx, "ep42_bl", K.proto(ctx, "ep42_p_bl", K.bm_sphere(0.5, (0, 0, 0), 28, 14), [K.mat_inst("ep42_m_bl", 0.8)]),
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
