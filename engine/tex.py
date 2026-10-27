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


def land_ice(w, h):
    from .common import imread
    land = cv2.resize(imread(ASSETS / "geo" / "land_mask.png", cv2.IMREAD_GRAYSCALE), (w, h),
                      interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    ice = cv2.resize(imread(ASSETS / "geo" / "ice_mask.png", cv2.IMREAD_GRAYSCALE), (w, h),
                     interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return land, ice


def earth_day(w=2048, h=1024, sea=0.0, ice_keep=1.0):
    """낮 지구 색 (선형 RGB 0..1)."""
    e = cv2.resize(world_elev(), (w, h), interpolation=cv2.INTER_AREA)
    land, ice = land_ice(w, h)
    lat = np.linspace(90, -90, h)[:, None]
    is_land = (land > 0.5) & (e > sea)
    depth = np.clip((sea - e) / 5000.0, 0, 1)[..., None]
    ocean = (1 - depth) * np.array([0.05, 0.22, 0.38]) + depth * np.array([0.012, 0.05, 0.16])
    hi = np.clip((e - sea) / 3000.0, 0, 1)[..., None]
    arid = np.clip(1 - np.abs(np.abs(lat) - 24) / 14, 0, 1)[..., None] * 0.6
    low = (1 - arid) * np.array([0.10, 0.26, 0.08]) + arid * np.array([0.42, 0.34, 0.18])
    landc = (1 - hi) * low + hi * np.array([0.38, 0.33, 0.26])
    img = np.where(is_land[..., None], landc, ocean)
    icem = (ice > 0.5)[..., None] & is_land[..., None]
    if ice_keep < 1.0:
        icem &= (np.abs(lat) > 90 - 30 * ice_keep)[..., None] if False else icem
    img = np.where(icem, np.array([0.80, 0.86, 0.92]), img)
    return img.astype(np.float32)


def city_lights(w=2048, h=1024, n=2500, gain=1.0):
    import json
    cities = json.load(open(ASSETS / "geo" / "cities.json", encoding="utf-8"))[:n]
    img = np.zeros((h, w), np.float32)
    for c in cities:
        x = int((c["lon"] + 180) / 360 * w) % w
        y = int((90 - c["lat"]) / 180 * h)
        if 0 <= y < h:
            img[y, x] += (max(c["pop"], 1e4) / 1e6) ** 0.5
    img = cv2.GaussianBlur(img, (0, 0), 1.2) * 6 + cv2.GaussianBlur(img, (0, 0), 4.0) * 3
    img = np.clip(img * gain, 0, 1.5)
    return img[..., None] * np.array([1.0, 0.72, 0.38], np.float32)


def save_rgb(path, rgb_lin):
    """선형 RGB → sRGB 8비트 PNG (Blender가 sRGB로 읽음)."""
    x = np.clip(rgb_lin, 0, 1)
    s = np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)
    imwrite(path, (s[..., ::-1] * 255 + 0.5).astype(np.uint8))


def planet_textures(build_dir):
    save_rgb(build_dir / "earth_day.png", earth_day())
    save_rgb(build_dir / "earth_night.png", city_lights())
