"""오픈스트리트맵(© OpenStreetMap contributors, ODbL) 동네 자료 → assets/geo/<이름>.npz

사용: python -I tools/prep_jamsil.py <osm.json> [이름 위도0 경도0]
기본: 잠실 (롯데월드타워 근처 37.5126N, 127.1025E 원점), 미터 단위 평면.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

NAME = sys.argv[2] if len(sys.argv) > 2 else "jamsil"
LAT0 = float(sys.argv[3]) if len(sys.argv) > 3 else 37.5126
LON0 = float(sys.argv[4]) if len(sys.argv) > 4 else 127.1025
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0
OUT = Path(__file__).resolve().parent.parent / "assets" / "geo" / f"{NAME}.npz"

ROAD_W = {"motorway": 22, "trunk": 20, "primary": 18, "secondary": 14, "tertiary": 11, "unclassified": 8,
          "residential": 7, "service": 5, "living_street": 6, "pedestrian": 6, "footway": 2.5, "path": 2.2,
          "cycleway": 2.2, "steps": 2.0, "motorway_link": 9, "trunk_link": 9, "primary_link": 8,
          "secondary_link": 7, "tertiary_link": 6}
CAR = {"motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link",
       "secondary_link"}
WALK = {"footway", "pedestrian", "path", "living_street", "steps"}


def xy(pt):
    return ((pt["lon"] - LON0) * KX, (pt["lat"] - LAT0) * KY)


def height_of(tags):
    for k in ("height", "building:height"):
        v = tags.get(k)
        if v:
            try:
                return float(str(v).replace("m", "").strip().split(";")[0])
            except ValueError:
                pass
    lv = tags.get("building:levels")
    if lv:
        try:
            return float(str(lv).split(";")[0]) * 3.1 + 1.5
        except ValueError:
            pass
    b = tags.get("building", "yes")
    return {"apartments": 60.0, "commercial": 25.0, "retail": 12.0, "office": 40.0, "house": 7.0,
            "school": 15.0, "church": 14.0, "stadium": 25.0, "roof": 5.0, "kiosk": 3.5}.get(b, 10.0)


def ring_area(pts):
    p = np.asarray(pts)
    return 0.5 * float(np.sum(p[:-1, 0] * p[1:, 1] - p[1:, 0] * p[:-1, 1]))


def pack(polys):
    pts, off = [], [0]
    for p in polys:
        pts.extend(p)
        off.append(len(pts))
    return np.array(pts, np.float32).reshape(-1, 2), np.array(off, np.int32)


def split_none(geom):
    """자료 범위(bbox)로 잘린 관계 멤버: 범위 밖 점은 None → 이어진 조각들로 나눔."""
    out, seg = [], []
    for p in list(geom or []) + [None]:
        if p:
            seg.append(xy(p))
            continue
        if len(seg) >= 2:
            out.append(np.array(seg))
        seg = []
    return out


def chain(parts, tol=0.5):
    """끝점이 맞닿는 조각을 이어 붙임 → 닫힌 고리 또는 열린 사슬(범위 밖으로 이어지는 강둑)."""
    parts, out = list(parts), []
    while parts:
        cur = parts.pop(0)
        grown = True
        while grown:
            grown = False
            for i, p in enumerate(parts):
                if np.allclose(cur[-1], p[0], atol=tol):
                    cur = np.vstack([cur, p[1:]])
                elif np.allclose(cur[-1], p[-1], atol=tol):
                    cur = np.vstack([cur, p[::-1][1:]])
                elif np.allclose(cur[0], p[-1], atol=tol):
                    cur = np.vstack([p, cur[1:]])
                elif np.allclose(cur[0], p[0], atol=tol):
                    cur = np.vstack([p[::-1], cur[1:]])
                else:
                    continue
                parts.pop(i)
                grown = True
                break
        out.append(cur)
    return out


data = json.load(open(sys.argv[1], encoding="utf-8"))
blds, bh, bkind = [], [], []
roads, rw, rk = [], [], []
water, green, banks = [], [], []
for el in data["elements"]:
    tags = el.get("tags", {})
    if el["type"] == "way" and "geometry" in el:
        g = [xy(p) for p in el["geometry"] if p]
        if len(g) < 2:
            continue
        if "building" in tags and tags.get("building") not in ("no",) and len(g) >= 4:
            if g[0] != g[-1]:
                g.append(g[0])
            if ring_area(g) < 0:
                g = g[::-1]
            if abs(ring_area(g)) < 12:
                continue
            blds.append(g[:-1])
            bh.append(height_of(tags))
            bkind.append(1 if tags.get("building") == "apartments" else 0)
        elif "highway" in tags:
            hw = tags["highway"]
            if hw in ROAD_W:
                roads.append(g)
                rw.append(ROAD_W[hw])
                rk.append(2 if hw in CAR else (1 if hw in WALK else 0))
        elif tags.get("natural") == "water" and len(g) >= 4:
            water.append(g[:-1] if g[0] == g[-1] else g)
        elif tags.get("leisure") in ("park", "garden", "pitch", "stadium") or \
                tags.get("landuse") in ("grass", "forest", "recreation_ground") or \
                tags.get("natural") in ("wood", "scrub"):
            if len(g) >= 4:
                green.append(g[:-1] if g[0] == g[-1] else g)
    elif el["type"] == "relation" and tags.get("natural") == "water":
        ms = el.get("members", [])
        for c in chain([s for m in ms if m.get("role") == "outer" for s in split_none(m.get("geometry"))]):
            if len(c) >= 4 and np.allclose(c[0], c[-1], atol=0.5):
                water.append([tuple(q) for q in c[:-1]])
            else:
                banks.append([tuple(q) for q in c])
        for c in chain([s for m in ms if m.get("role") == "inner" for s in split_none(m.get("geometry"))]):
            if len(c) >= 4 and np.allclose(c[0], c[-1], atol=0.5):
                green.append([tuple(q) for q in c[:-1]])   # 강 속 섬은 땅(녹지)으로
bp, bo = pack(blds)
rp, ro = pack(roads)
wp, wo = pack(water)
gp, go = pack(green)
kp, ko = pack(banks)
np.savez_compressed(OUT, b_pts=bp, b_off=bo, b_h=np.array(bh, np.float32), b_kind=np.array(bkind, np.int8),
                    r_pts=rp, r_off=ro, r_w=np.array(rw, np.float32), r_kind=np.array(rk, np.int8),
                    w_pts=wp, w_off=wo, g_pts=gp, g_off=go, wb_pts=kp, wb_off=ko)
print("buildings", len(blds), "tall(>100m)", int(np.sum(np.array(bh) > 100)), "max h", max(bh) if bh else 0)
print("roads", len(roads), "water", len(water), "green", len(green), "banks", len(banks), "->", OUT, OUT.stat().st_size)
