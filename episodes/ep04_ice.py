"""EP04 만약 남극과 북극의 얼음이 다 녹는다면?

실제로 계산하는 것:
- 지구본: NOAA ETOPO1 고도 + 해수면 → 잠기는 해안선 (셰이더에서 매 프레임 비교)
- 얼음: 북극 해빙(부력, 해수면 변화 없음) → 그린란드 7.4m → 남극 58m, 가장자리부터 녹음
- 한반도 3D 지형(1분 격자): 해수면을 올리고 내리며 잠기는 땅 / 빙하기(−120m) 황해 노출
"""
import math

import numpy as np

from engine.common import FPS, Beat, clamp, frames_of, keyed, ramp

DUR = 56.0
META = {"id": "ep04", "title": "만약 남극과 북극의 얼음이 다 녹는다면?", "duration": DUR,
        "music": {"key": "Eb", "mode": "major", "bpm": 68, "seed": 4, "twist_at": 44.0}}
GLOBE_R = 4.0
TERRAIN_AT = (300.0, 0.0, 0.0)
S = 1.0          # 위도 1도 = 1 단위
EXAG = 0.0003    # 1m = 0.0003 단위 (수직 과장)
LAT0, LON0 = 36.5, 126.0

# 해수면(m): 북극 해빙(4.5~10초)은 그대로, 그린란드(10~16초), 남극(16~28초), 반전(44~52초)
SEA_KEYS = [(0.0, 0.0), (10.0, 0.0), (16.0, 7.4), (28.0, 66.0), (44.0, 66.0), (46.0, 0.0), (49.5, -120.0),
            (56.0, -120.0)]
ICE_KEYS = {  # 남은 비율
    "arc": [(0.0, 1.0), (4.8, 1.0), (9.5, 0.0), (44.0, 0.0), (46.5, 1.0), (56.0, 1.0)],
    "gre": [(0.0, 1.0), (10.0, 1.0), (16.0, 0.0), (44.0, 0.0), (46.5, 1.0), (56.0, 1.0)],
    "ant": [(0.0, 1.0), (16.0, 1.0), (21.0, 0.0), (44.0, 0.0), (46.5, 1.0), (56.0, 1.0)],
}

CITIES = [("서울", 37.5665, 126.978), ("인천", 37.456, 126.705), ("부산", 35.1796, 129.0756),
          ("광주", 35.1595, 126.8526), ("대전", 36.3504, 127.3845), ("대구", 35.8714, 128.6014),
          ("평양", 39.0392, 125.7625), ("목포", 34.8118, 126.3922)]
PLACES = [("중국", 36.6, 118.6), ("황해", 35.8, 123.6), ("일본", 33.2, 131.0)]


def sea_at(t):
    return keyed(t, SEA_KEYS)


BEATS = [
    Beat(0.0, 4.5, badge="현재", label="지구의 얼음", big="해수면 66m 분량", label_color="cyan",
         sub="만약 남극과 북극의 얼음이\n전부 녹는다면?"),
    Beat(4.5, 10.0, badge="1단계", title="{cyan}북극{/} 얼음이 녹으면", big="해수면 +0m", big_size=96,
         note="바다에 뜬 얼음은 녹아도 그대로 (부력)",
         sub="북극 얼음은 대부분 바다에 떠 있어서\n녹아도 해수면이 거의 오르지 않습니다."),
    Beat(10.0, 16.0, badge="2단계", title="그린란드", big="+7.4m", big_size=104,
         sub="땅 위에 쌓인 얼음이 바다로 들어가야\n해수면이 오릅니다."),
    Beat(16.0, 20.6, badge="3단계", title="남극", big="+58m", big_size=104, note="남극 얼음 2,717만 km³ (Bedmap3)",
         sub="남극 얼음이 다 녹으면\n해수면이 58m 오릅니다."),
    Beat(20.6, 28.0, badge="합계 +66m", title="{blue}한반도{/}는?",
         sub="해발 66m보다 낮은 땅은\n모두 바다가 됩니다."),
    Beat(28.0, 34.0, badge="+66m", title="서울의 약 {blue}70%{/} 잠김", note="남한 땅의 약 23% (지형 자료로 계산)",
         sub="바닷물이 한강을 따라\n서울 한가운데까지 들어옵니다."),
    Beat(34.0, 40.0, badge="+66m", title="{orange}8.96억 명{/}", note="해발 10m 이하에 사는 세계 인구 (IPCC, 2020)",
         sub="해안 대도시들은\n10m만 올라도 위험해집니다."),
    Beat(40.0, 44.0, badge="얼마나 걸릴까?", title="다 녹는 데 {orange}5,000년+{/}", note="지금은 1년에 약 4.4mm씩 상승 (NASA)",
         sub="하지만 바다는 지금도\n해마다 조금씩 높아지고 있습니다."),
    Beat(44.0, 52.0, badge="반전", title="2만 년 전엔 {cyan}정반대{/}", big="해수면 −120m", big_size=96,
         sub="마지막 빙하기엔 바다가 약 120m 낮아\n황해 대부분이 육지였습니다."),
    Beat(52.0, 56.0, badge="2만 년 전", title="한반도에서 중국까지\n{orange}걸어서{/} 갈 수 있었습니다", title_size=70),
]
GRADE = {"exposure": 1.0, "bloom": 0.22, "bloom_thr": 1.1, "vignette": 0.3}
FLASH = [(20.6, 0.35, (0.85, 0.92, 1.0))]


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def to_xy(lat, lon):
    return ((lon - LON0) * math.cos(math.radians(LAT0)) * S, (lat - LAT0) * S)


def simulate(build_dir):
    from engine.tex import eastasia, elev_png, ice_regions
    if not (build_dir / "elev.png").exists():
        elev_png(build_dir / "elev.png")
    ice_regions(build_dir / "ice_regions.png")
    import cv2
    full, lat_top, lon_left, cell = eastasia()
    e = cv2.GaussianBlur(full, (0, 0), 1.0)[::2, ::2]
    cell2 = cell * 2
    ny, nx = e.shape
    lats = lat_top - np.arange(ny) * cell2
    lons = lon_left + np.arange(nx) * cell2
    LON, LAT = np.meshgrid(lons, lats)
    X = (LON - LON0) * math.cos(math.radians(LAT0)) * S
    Y = (LAT - LAT0) * S
    Z = np.maximum(e, -400.0) * EXAG
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    sea = np.array([sea_at(t) for t in ts], np.float32)
    ice = {k: np.array([keyed(t, v) for t in ts], np.float32) for k, v in ICE_KEYS.items()}
    # 도시 고도 (격자 보간 없이 가장 가까운 칸)
    ce = []
    for _, la, lo in CITIES:
        r, c = int(round((lat_top - la) / cell)), int(round((lo - lon_left) / cell))
        ce.append(float(full[r, c]))
    remain = np.clip((66.0 - np.maximum(sea, 0)) / 66.0, 0, 1)
    return dict(X=X.astype(np.float32), Y=Y.astype(np.float32), Z=Z.astype(np.float32), sea=sea,
                ice_arc=ice["arc"], ice_gre=ice["gre"], ice_ant=ice["ant"], city_e=np.array(ce, np.float32),
                remain=remain)


def hud(t, sim):
    f = fi(t)
    s = float(sim["sea"][f])
    right = f"해수면 {s:+.1f}m" if abs(s) >= 0.05 else "해수면 ±0.0m"
    r2 = "빙하기 (약 2만 년 전)" if t >= 46.5 else f"남은 얼음 {int(round(100 * float(sim['remain'][f])))}%"
    return {"left": "SIMULATION", "right": right, "right2": r2}


def labels(t, anchors, sim):
    out = []
    if t < 21.0:
        return out
    f = fi(t)
    s = float(sim["sea"][f])
    for i, (nm, la, lo) in enumerate(CITIES):
        a = anchors.get(f"c{i}")
        if a and a[3]:
            sunk = s > float(sim["city_e"][i])
            out.append({"x": a[0], "y": a[1], "text": nm + (" 잠김" if sunk and s > 5 else ""),
                        "color": "blue" if sunk and s > 5 else "white", "size": 26, "lift": 8})
    if t > 46.0:
        for i, (nm, la, lo) in enumerate(PLACES):
            a = anchors.get(f"p{i}")
            if a and a[3]:
                out.append({"x": a[0], "y": a[1], "text": nm + (" (육지)" if nm == "황해" else ""),
                            "color": "orange" if nm == "황해" else "white", "size": 28, "lift": 4,
                            "alpha": ramp(t, 46.0, 47.0)})
    return out


def build(ctx):
    from engine import bkit as K
    from engine.common import ASSETS
    sim = ctx.sim
    K.world_space(ctx, ambient=(0.35, 0.42, 0.6), ambient_strength=0.3)
    sun = K.sun(ctx, 3.2, color=(1.0, 0.95, 0.88), angle=3.0)
    g, at = K.globe(ctx, GLOBE_R, tex=ASSETS / "geo" / "land_mask.png", elev=ctx.build_dir / "elev.png",
                    ice_regions=ctx.build_dir / "ice_regions.png")
    # 한반도 지형 조각
    X, Y, Z = sim["X"], sim["Y"], sim["Z"]
    tm = K.mat_terrain(ctx, EXAG)
    ter = K.grid_mesh("terrain", X, Y, Z, tm, skirt_z=-0.45)
    ter.location = TERRAIN_AT
    wm = K.mat_water()
    x0, x1, y0, y1 = float(X.min()), float(X.max()), float(Y.min()), float(Y.max())
    water = K.box_obj("water", x0 - 0.01, x1 + 0.01, y0 - 0.01, y1 + 0.01, -1.0, 0.0, wm)
    water.location = TERRAIN_AT
    side = K.box_obj("base", x0, x1, y0, y1, -0.75, -0.45, K.mat_earth_side())
    side.location = TERRAIN_AT
    cam = K.CamRig(ctx, 35, fstop=0)
    TA = np.array(TERRAIN_AT)

    def tpos(lat, lon, dz=0.0):
        x, y = to_xy(lat, lon)
        # 지형 높이 (가장 가까운 격자점)
        iy = int(np.abs(Y[:, 0] - y).argmin())
        ix = int(np.abs(X[iy, :] - x).argmin())
        return (float(TA[0] + x), float(TA[1] + y), float(TA[2] + max(Z[iy, ix], 0.0) + dz))

    seoul = tpos(37.5665, 126.978)
    center = tpos(36.6, 127.2)
    west = tpos(36.2, 123.5)

    # 지구본 카메라: (t, 위도, 경도, 거리, 렌즈)
    GLOBE_CAM = [(0.0, 58, -25, 27.0, 35), (4.5, 66, -30, 25.0, 35), (10.0, 55, -42, 22.0, 35),
                 (15.6, 30, -40, 25.0, 35), (16.8, -62, 20, 25.0, 35), (19.2, -45, 70, 24.0, 35),
                 (20.2, 33, 124, 12.0, 38), (20.6, 36, 127, 7.5, 40)]
    # 지형 카메라: (t, 목표, 방위, 고도, 거리, 렌즈)
    TER_CAM = [(20.6, center, -95, 58, 17.0, 32), (24.0, center, -100, 52, 15.0, 32),
               (28.0, seoul, -110, 56, 8.5, 34), (33.6, seoul, -125, 52, 9.0, 34),
               (34.4, center, -120, 55, 16.0, 32), (43.5, center, -100, 56, 17.0, 32),
               (46.0, west, -100, 60, 19.0, 30), (56.0, west, -80, 52, 18.5, 30)]

    def upd(t, f):
        s = float(sim["sea"][f])
        ctx.set_ctl("sea", s)
        ctx.set_ctl("sea_m", s)
        for k in ("arc", "gre", "ant"):
            ctx.set_ctl("ice_" + k, float(sim["ice_" + k][f]))
        zw = max(s * EXAG, -0.44)
        # 물 상자: 위 = zw, 아래 = -0.45
        water.location = (TA[0], TA[1], TA[2] + zw)
        water.scale = (1, 1, zw + 0.45)
        if t < 20.6:
            v = keyed(t, [(k[0], k[1:]) for k in GLOBE_CAM])
            la, lo, dist, lens = v
            p = K.latlon_to_xyz(la, lo, 1.0)
            az = math.degrees(math.atan2(p[1], p[0]))
            cam.set((0, 0, 0), az, la, dist, lens)
            K.aim_sun(sun, az, la, side=30.0, up=20.0)
        else:
            v = keyed(t, [(k[0], (*k[1], *k[2:])) for k in TER_CAM])
            cam.set(v[:3], v[3], v[4], v[5], v[6])
            sun.rotation_euler = (math.radians(40), 0, math.radians(-150))

    ctx.on_frame(upd)
    for i, (nm, la, lo) in enumerate(CITIES):
        ctx.anchor(f"c{i}", (lambda la, lo: lambda t: tpos(la, lo, 0.08))(la, lo))
    for i, (nm, la, lo) in enumerate(PLACES):
        ctx.anchor(f"p{i}", (lambda la, lo: lambda t: tpos(la, lo, 0.1))(la, lo))
