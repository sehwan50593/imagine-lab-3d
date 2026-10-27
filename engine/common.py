"""Blender와 일반 파이썬 양쪽에서 쓰는 공통 상수·유틸 (bpy 사용 금지)."""
import math
from pathlib import Path

import numpy as np

FPS = 30
W, H = 1080, 1920
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = ASSETS / "fonts" / "NotoSansKR-VF.ttf"
BUILD = ROOT / "build"

COLORS = {
    "white": (255, 255, 255),
    "blue": (90, 170, 255),
    "red": (255, 82, 82),
    "orange": (255, 178, 64),
    "cyan": (110, 232, 255),
    "yellow": (255, 220, 90),
    "green": (98, 228, 140),
    "purple": (190, 150, 255),
    "gray": (170, 178, 196),
    "pink": (255, 140, 190),
}


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def smoother(x):
    x = clamp(x)
    return x * x * x * (x * (x * 6 - 15) + 10)


def ramp(t, t0, t1):
    """t0→t1 구간에서 0→1 (부드럽게)."""
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return smooth((t - t0) / (t1 - t0))


def keyed(t, keys, ease=smooth):
    """keys=[(t, value), ...] 사이를 부드럽게 보간. value는 숫자/튜플."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (ta, va), (tb, vb) in zip(keys, keys[1:]):
        if t <= tb:
            u = ease((t - ta) / (tb - ta)) if tb > ta else 1.0
            if isinstance(va, (tuple, list)):
                return tuple(lerp(a, b, u) for a, b in zip(va, vb))
            return lerp(va, vb, u)
    return keys[-1][1]


def logkeyed(t, keys):
    """시뮬레이션 시간처럼 자릿수가 크게 변하는 값을 로그 공간에서 보간 (0은 1e-6 취급)."""
    lk = [(a, math.log10(max(b, 1e-6))) for a, b in keys]
    v = keyed(t, lk, ease=lambda u: u)
    return 10 ** v


class Beat:
    """화면 문구 한 단락. 시간은 영상 초."""

    def __init__(self, t0, t1, badge="", title="", label="", big="", sub="",
                 label_color="blue", big_color="white", title_size=80, big_size=112,
                 note="", note_color="orange"):
        self.t0, self.t1 = t0, t1
        self.badge = badge
        self.title = title          # "{red}82억 명{/}" 식 색 표기 가능
        self.label = label
        self.big = big              # 문자열 또는 callable(t, sim) -> str
        self.sub = sub
        self.label_color = label_color
        self.big_color = big_color
        self.title_size = title_size
        self.big_size = big_size
        self.note = note            # 제목 아래 작은 보조 문구
        self.note_color = note_color


def beat_at(beats, t):
    for b in beats:
        if b.t0 <= t < b.t1:
            return b
    return beats[-1] if t >= beats[-1].t1 else None


def frames_of(duration):
    return int(round(duration * FPS))


def fmt_int(n):
    return f"{int(round(n)):,}"


def fmt_korean(n, unit=""):
    """1.2억, 3,400만 같은 한국식 큰 수."""
    n = float(n)
    if n >= 1e12:
        return f"{n / 1e12:.1f}조{unit}".replace(".0조", "조")
    if n >= 1e8:
        v = n / 1e8
        return (f"{v:.1f}억{unit}" if v < 100 else f"{v:,.0f}억{unit}").replace(".0억", "억")
    if n >= 1e4:
        return f"{n / 1e4:,.0f}만{unit}"
    return f"{n:,.0f}{unit}"


def rng(seed):
    return np.random.default_rng(seed)


def imwrite(path, img, params=None):
    """cv2.imwrite는 윈도우 한글 경로를 못 씀 → imencode 후 직접 저장."""
    import cv2
    ok, buf = cv2.imencode(Path(path).suffix, img, params or [])
    if not ok:
        raise RuntimeError(f"이미지 인코딩 실패: {path}")
    Path(path).write_bytes(buf.tobytes())


def imread(path, flags):
    import cv2
    data = np.frombuffer(Path(path).read_bytes(), np.uint8)
    return cv2.imdecode(data, flags)
