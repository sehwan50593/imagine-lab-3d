"""동아시아 1분 격자 지형(NOAA ETOPO1) → assets/geo/eastasia_elev_1m.npz, 남한 침수 통계 출력."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

RAW = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "assets" / "geo"
with open(RAW / "etopo_eastasia.asc") as f:
    hdr = {}
    for _ in range(6):
        k, v = f.readline().split()
        hdr[k.lower()] = float(v)
    e = np.loadtxt(f, dtype=np.float32)
cell = hdr["cellsize"]
lat_top = hdr["yllcenter"] + (hdr["nrows"] - 1) * cell
lon_left = hdr["xllcenter"]
np.savez_compressed(OUT / "eastasia_elev_1m.npz", elev=e.astype(np.int16), lat_top=lat_top, lon_left=lon_left,
                    cell=cell)
h, w = e.shape
kor = json.load(open(OUT / "korea_outline.json"))


def mask(code):
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    for poly in kor[code]:
        pts = [((x - lon_left) / cell, (lat_top - y) / cell) for x, y in poly[0]]
        d.polygon(pts, fill=1)
    return np.array(im).astype(bool)


lat = lat_top - np.arange(h) * cell
area = np.cos(np.radians(lat))[:, None] * np.ones((1, w))  # 셀 면적 비례
for code in ("KOR", "PRK"):
    m = mask(code) & (e > 0)
    tot = (area * m).sum()
    for sl in (7.4, 58, 66):
        print(code, f"+{sl}m 잠김 {100 * (area * (m & (e <= sl))).sum() / tot:.1f}%")
# 서울 (시청 기준 반경 14km 원 ≈ 서울 면적 605km²)
yy, xx = np.mgrid[0:h, 0:w]
la, lo = lat_top - yy * cell, lon_left + xx * cell
dkm = np.hypot((la - 37.5665) * 111.0, (lo - 126.978) * 111.0 * np.cos(np.radians(37.57)))
seoul = (dkm < 14.0) & (e > 0)
for sl in (7.4, 58, 66):
    print("서울(반경14km)", f"+{sl}m 잠김 {100 * (seoul & (e <= sl)).sum() / seoul.sum():.1f}%")
for name, la0, lo0 in (("서울시청", 37.5665, 126.978), ("인천", 37.456, 126.705), ("부산", 35.1796, 129.0756),
                       ("광주", 35.1595, 126.8526), ("대전", 36.3504, 127.3845), ("대구", 35.8714, 128.6014),
                       ("평양", 39.0392, 125.7625), ("목포", 34.8118, 126.3922)):
    r, c = int(round((lat_top - la0) / cell)), int(round((lo0 - lon_left) / cell))
    print(name, int(e[r, c]), "m")
print("황해 최대 수심", int(-e[int((lat_top - 36) / cell), int((123.5 - lon_left) / cell)]))
