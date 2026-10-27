"""시뮬레이션 단계(일반 파이썬)에서 만드는 텍스처."""
import cv2
import numpy as np

from .common import ASSETS, imwrite


def world_elev():
    z = np.load(ASSETS / "geo" / "world_elev_0p1.npz")
    return z["elev"].astype(np.float32)  # 북→남, 경도 -180→180


def elev_png(path, w=4096, h=2048):
    e = cv2.resize(world_elev(), (w, h), interpolation=cv2.INTER_LINEAR)
    v = np.clip((e + 11000.0) / 20000.0, 0, 1)
    imwrite(path, (v * 65535 + 0.5).astype(np.uint16))
    return path


def korea_elev():
    z = np.load(ASSETS / "geo" / "korea_elev_1m.npz")
    return z["elev"].astype(np.float32), float(z["lat_top"]), float(z["lon_left"]), float(z["cell"])
