"""Natural Earth(퍼블릭 도메인) + NOAA ETOPO1(퍼블릭 도메인) 원본을 렌더용 작은 자산으로 변환.

사용: python -I tools/prep_geo.py <raw_geo 폴더>
"""
import json
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

RAW = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "assets" / "geo"
OUT.mkdir(parents=True, exist_ok=True)
TW, TH = 4096, 2048  # 등장방형 텍스처


def load(name):
    return json.load(open(RAW / name, encoding="utf-8"))


def read_asc(path):
    with open(path, "r") as f:
        hdr = {}
        for _ in range(6):
            k, v = f.readline().split()
            hdr[k.lower()] = float(v)
        data = np.loadtxt(f, dtype=np.float32)
    # ERDDAP esriAscii: 첫 행이 북쪽
    return hdr, data


def polys(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    return []


def lines(geom):
    if geom["type"] == "LineString":
        return [geom["coordinates"]]
    if geom["type"] == "MultiLineString":
        return geom["coordinates"]
    return []


def to_px(lon, lat):
    return ((lon + 180.0) / 360.0 * TW, (90.0 - lat) / 180.0 * TH)


def raster_polys(features, value=255, size=(TW, TH)):
    img = Image.new("L", size, 0)
    d = ImageDraw.Draw(img)
    for ft in features:
        for poly in polys(ft["geometry"]):
            outer = [to_px(x, y) for x, y in poly[0]]
            if len(outer) > 2:
                d.polygon(outer, fill=value)
            for hole in poly[1:]:
                h = [to_px(x, y) for x, y in hole]
                if len(h) > 2:
                    d.polygon(h, fill=0)
    return img


# 1) 육지 마스크 (호수 제외)
land = raster_polys(load("ne_50m_land.geojson")["features"])
lakes = raster_polys(load("ne_50m_lakes.geojson")["features"])
land_np = np.array(land)
land_np[np.array(lakes) > 0] = 0
Image.fromarray(land_np).save(OUT / "land_mask.png", optimize=True)

# 2) 빙하(그린란드·남극 대륙 빙상 포함) 마스크
glac = raster_polys(load("ne_50m_glaciated_areas.geojson")["features"])
g = np.array(glac)
yy = np.arange(TH)[:, None]
lat = 90.0 - (yy + 0.5) / TH * 180.0
g[(lat < -60.0).repeat(TW, 1) & (land_np > 0)] = 255  # 남극 대륙 전체
Image.fromarray(g).save(OUT / "ice_mask.png", optimize=True)

# 3) 국경선: 선마다 0~1 랜덤 소멸 순서를 밝기로 저장 (1..255, 0 = 없음)
rnd = random.Random(7)
bimg = Image.new("L", (TW, TH), 0)
bd = ImageDraw.Draw(bimg)
for ft in load("ne_50m_admin_0_boundary_lines_land.geojson")["features"]:
    v = rnd.randint(1, 255)
    for ln in lines(ft["geometry"]):
        pts = [to_px(x, y) for x, y in ln]
        for a, b in zip(pts, pts[1:]):
            if abs(a[0] - b[0]) > TW / 2:  # 날짜변경선 넘김
                continue
            bd.line([a, b], fill=v, width=3)
bimg.save(OUT / "borders_rank.png", optimize=True)

# 4) 세계 고도 (0.1도) → int16 압축
hdr, w = read_asc(RAW / "etopo_world10.asc")
np.savez_compressed(OUT / "world_elev_0p1.npz", elev=w.astype(np.int16),
                    lat_top=90.0, lon_left=-180.0, cell=hdr["cellsize"])

# 5) 한반도 고도 (1분)
hdr, k = read_asc(RAW / "etopo_korea.asc")
lat_top = hdr["yllcenter"] + (hdr["nrows"] - 1) * hdr["cellsize"]
np.savez_compressed(OUT / "korea_elev_1m.npz", elev=k.astype(np.int16),
                    lat_top=lat_top, lon_left=hdr["xllcenter"], cell=hdr["cellsize"])

# 6) 한반도 윤곽(남·북) 과 군사분계선(두 나라 공유 경계)
c10 = load("ne_10m_admin_0_countries.geojson")["features"]
kor = {}
for ft in c10:
    a3 = ft["properties"].get("ADM0_A3")
    if a3 in ("KOR", "PRK"):
        kor[a3] = [[[(round(x, 4), round(y, 4)) for x, y in ring] for ring in poly]
                   for poly in polys(ft["geometry"])]
json.dump(kor, open(OUT / "korea_outline.json", "w"), separators=(",", ":"))

# 7) 도시 (인구 상위)
pp = load("ne_10m_populated_places_simple.geojson")["features"]
cities = []
for ft in pp:
    p = ft["properties"]
    cities.append((p["pop_max"] or 0, round(p["latitude"], 3), round(p["longitude"], 3),
                   p["nameascii"], p["adm0_a3"]))
cities.sort(reverse=True)
json.dump([dict(pop=c[0], lat=c[1], lon=c[2], name=c[3], cc=c[4]) for c in cities[:2500]],
          open(OUT / "cities.json", "w"), separators=(",", ":"))

# 8) 나라별 대표점(라벨/흐름용) + 인구
c50 = load("ne_50m_admin_0_countries.geojson")["features"]
cents = []
for ft in c50:
    p = ft["properties"]
    best = max(polys(ft["geometry"]), key=lambda pl: len(pl[0]))
    xs = [x for x, _ in best[0]]
    ys = [y for _, y in best[0]]
    cents.append(dict(a3=p["ADM0_A3"], name=p["NAME"], pop=p.get("POP_EST") or 0,
                      gdp=p.get("GDP_MD") or 0, lon=round(sum(xs) / len(xs), 2),
                      lat=round(sum(ys) / len(ys), 2)))
json.dump(cents, open(OUT / "countries.json", "w"), separators=(",", ":"))

for f in sorted(OUT.iterdir()):
    print(f.name, f.stat().st_size)
