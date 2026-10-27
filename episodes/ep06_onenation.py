"""EP06 만약 전 세계가 하나의 나라가 된다면?

실제로 계산하는 것:
- 국경선(Natural Earth)이 하나씩 사라짐
- 이주 흐름: 나라별 인구·1인당 GDP(Natural Earth 표)로 만든 중력 모형
  흐름 ∝ √(인구_출발·인구_도착) × ln(소득비) / 거리^0.7  (소득이 높은 쪽으로만)
- 인구 원: 나라별 인구에 비례한 '표' / 반전: 국경이 없어도 남는 나라 안의 분쟁
"""
import json
import math

import numpy as np

from engine.common import ASSETS, FPS, Beat, clamp, frames_of, keyed, ramp

DUR = 56.0
META = {"id": "ep06", "title": "만약 전 세계가 하나의 나라가 된다면?", "duration": DUR,
        "music": {"key": "G", "mode": "major", "bpm": 72, "seed": 6, "twist_at": 40.0}}
GR = 4.0
NFLOW, NMIL, NCOL, NCONF = 1500, 70, 45, 24
CONFLICTS = [(15.5, 32.5), (7.0, 30.0), (-2.0, 23.5), (9.0, 39.5), (5.0, 45.5), (17.0, -2.0), (12.5, -1.5),
             (14.5, 6.0), (10.5, 8.0), (6.0, 12.5), (-13.0, 39.0), (21.0, 96.0), (35.0, 38.5), (15.5, 44.5),
             (34.0, 43.5), (34.5, 67.0), (30.0, 70.0), (4.0, -73.5), (19.0, -72.5), (7.5, 124.5), (-4.0, 29.0),
             (26.0, 92.0), (12.0, 24.0), (3.0, 32.0)]

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY", label="나라", big="195개 → 1개", label_color="orange",
         sub="만약 오늘, 전 세계가\n하나의 나라가 된다면?"),
    Beat(4.5, 10.0, badge="D+1", title="국경 {orange}25만 km{/}가 사라진다", note="육지 국경 총길이 251,060 km (CIA 월드 팩트북)",
         sub="여권도 비자도 필요 없는\n하나의 나라가 됩니다."),
    Beat(10.0, 16.0, badge="D+30", title="{cyan}9억 명{/}이 움직인다", note="다른 나라로 이주하고 싶은 성인 15% (갤럽, 2025)",
         sub="더 잘사는 곳을 향해\n사람들이 이동하기 시작합니다."),
    Beat(16.0, 22.0, badge="1년 후", title="군대가 필요 없다?", big="2조 8,870억 달러", big_size=92,
         note="2025년 세계 군사비 (SIPRI)",
         sub="적국이 사라지면, 세계 GDP의 2.5%를\n다른 곳에 쓸 수 있습니다."),
    Beat(22.0, 28.0, badge="1년 후", title="첫 번째 세계 선거", big="인도+중국 = 35%", big_size=92,
         note="인도 14.6억 · 중국 14.2억 (UN, 2025)",
         sub="인구가 곧 표라면, 두 나라가\n인류 표의 3분의 1을 가집니다."),
    Beat(28.0, 34.0, badge="10년 후", title="말은 {yellow}7,160개{/}, 돈은 {yellow}1개{/}",
         note="언어 수 (에스놀로그) · 화폐 약 180종 → 1종",
         sub="화폐는 하나로 합칠 수 있어도\n수천 개의 언어는 그대로 남습니다."),
    Beat(34.0, 40.0, badge="10년 후", title="세계 정부의 지갑", big="118.5조 달러", big_size=96,
         note="2025년 세계 GDP (IMF)",
         sub="하나의 시장이 된 지구의\n1년 경제 규모입니다."),
    Beat(40.0, 48.0, badge="반전", title="그래도 싸움은 남는다", big="88%", big_size=110, big_color="red",
         note="2025년 무력분쟁 65건 중 57건이 '나라 안'에서 (UCDP)",
         sub="전쟁의 대부분은 이미\n'한 나라 안'에서 일어나고 있습니다."),
    Beat(48.0, 56.0, badge="지금", title="국경이 없는 세상,\n당신은 {orange}어디{/}에서 살고 싶나요?", title_size=70),
]
GRADE = {"exposure": 1.0, "bloom": 0.3, "bloom_thr": 1.0, "vignette": 0.3}


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def xyz(lat, lon, r):
    la, lo = np.radians(lat), np.radians(lon)
    return np.stack([r * np.cos(la) * np.cos(lo), r * np.cos(la) * np.sin(lo), r * np.sin(la)], -1)


def slerp(a, b, u):
    a, b = a / np.linalg.norm(a, axis=-1, keepdims=True), b / np.linalg.norm(b, axis=-1, keepdims=True)
    dot = np.clip((a * b).sum(-1, keepdims=True), -1, 1)
    om = np.arccos(dot)
    so = np.sin(om) + 1e-6
    return (np.sin((1 - u) * om) / so) * a + (np.sin(u * om) / so) * b


def simulate(build_dir):
    from engine.tex import city_lights, elev_png, save_rgb
    if not (build_dir / "elev.png").exists():
        elev_png(build_dir / "elev.png")
    save_rgb(build_dir / "night.png", city_lights(4096, 2048, gain=0.8))
    rs = np.random.default_rng(66)
    cs = [c for c in json.load(open(ASSETS / "geo" / "countries.json", encoding="utf-8"))
          if c["pop"] > 2e6 and c["gdp"] > 0]
    P = np.array([c["pop"] for c in cs], np.float64)
    G = np.array([c["gdp"] * 1e6 / c["pop"] for c in cs], np.float64)
    L = np.array([[c["lat"], c["lon"]] for c in cs])
    V = xyz(L[:, 0], L[:, 1], 1.0)
    dist = np.arccos(np.clip(V @ V.T, -1, 1)) * 6371 + 300
    ratio = np.log(np.maximum(G[None, :] / G[:, None], 1.0))
    F = np.sqrt(P[:, None] * P[None, :]) * ratio / dist ** 0.7
    np.fill_diagonal(F, 0)
    Fp = (F / F.sum()).ravel()
    pick = rs.choice(len(Fp), NFLOW, p=Fp)
    src, dst = pick // len(cs), pick % len(cs)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    t0 = 10.0 + rs.random(NFLOW) * 26.0
    dur = 1.6 + dist[src, dst] / 20000 * 2.5
    a = xyz(L[src, 0], L[src, 1], 1.0) + rs.normal(0, 0.01, (NFLOW, 3))
    b = xyz(L[dst, 0], L[dst, 1], 1.0) + rs.normal(0, 0.01, (NFLOW, 3))
    hgt = 0.04 + 0.22 * (dist[src, dst] / 20000)
    fl_p = np.zeros((nf, NFLOW, 3), np.float32)
    fl_s = np.zeros((nf, NFLOW), np.float32)
    for i, t in enumerate(ts):
        u = np.clip((t - t0) / dur, 0, 1)[:, None]
        d = slerp(a, b, u)
        r = GR * (1.0 + 0.005 + hgt[:, None] * 4 * u * (1 - u))
        fl_p[i] = d * r
        on = (t >= t0) & (t < t0 + dur)
        fl_s[i] = np.where(on, 1.0, 0.0) * (1 - ramp(t, 39.5, 41.0))
    # 군사 기지(상징): 인구·경제 규모로 뽑은 위치
    wm = P * np.log(G + 10)
    mi = rs.choice(len(cs), NMIL, p=wm / wm.sum())
    mil = xyz(L[mi, 0] + rs.normal(0, 1.5, NMIL), L[mi, 1] + rs.normal(0, 1.5, NMIL), GR * 1.004)
    # 인구 기둥 (상위 NCOL개 나라)
    top = np.argsort(-P)[:NCOL]
    col_pos = xyz(L[top, 0], L[top, 1], GR)
    col_h = P[top] / P.max()
    col_c = np.array([(1.0, 0.55, 0.15) if cs[k]["a3"] == "IND" else (1.0, 0.25, 0.2) if cs[k]["a3"] == "CHN"
                      else (0.35, 0.65, 1.0) for k in top], np.float32)
    conf = xyz(np.array([c[0] for c in CONFLICTS]), np.array([c[1] for c in CONFLICTS]), GR * 1.006)
    return dict(fl_p=fl_p, fl_s=fl_s, mil=mil.astype(np.float32), col_pos=col_pos.astype(np.float32),
                col_h=col_h.astype(np.float32), col_c=col_c, conf=conf.astype(np.float32),
                conf_ph=rs.uniform(0, 6.28, NCONF).astype(np.float32))


CLOCK = [(0.0, 0.0), (4.5, 0.0), (5.3, 1.0), (10.0, 2.0), (10.8, 30.0), (16.0, 60.0), (16.8, 365.0),
         (27.5, 500.0), (28.5, 3652.0), (56.0, 3800.0)]


def hud(t, sim):
    d = keyed(t, CLOCK)
    s = f"D+{int(d)}" if d < 365 else f"{d / 365.25:.0f}년"
    nb = 195 if t < 4.5 else (1 if t > 10 else int(round(195 - 194 * ramp(t, 4.6, 9.8))))
    return {"left": "SIMULATION", "right": "경과 " + s, "right2": f"국경으로 나뉜 나라 {nb}개"}


def build(ctx):
    from engine import bkit as K
    sim = ctx.sim
    K.world_space(ctx, ambient=(0.3, 0.36, 0.55), ambient_strength=0.18)
    sun = K.sun(ctx, 3.0, color=(1.0, 0.95, 0.9), angle=2.0)
    g, at = K.globe(ctx, GR, tex=ASSETS / "geo" / "land_mask.png", elev=ctx.build_dir / "elev.png",
                    borders=ASSETS / "geo" / "borders_rank.png", night=ctx.build_dir / "night.png",
                    ice=ASSETS / "geo" / "ice_mask.png")
    flm = K.mat_emit("m_flow", (0.45, 0.9, 1.0), 7.0)
    flo = K.instancer(ctx, "flows", K.proto(ctx, "p_flow", K.bm_ico(0.012, sub=1), [flm]), NFLOW)
    mil = K.instancer(ctx, "mil", K.proto(ctx, "p_mil", K.bm_ico(0.035, sub=1),
                                          [K.mat_emit("m_mil", (1.0, 0.2, 0.15), 6.0)]), NMIL)
    cm, nt, out = K.new_mat("m_colm")
    em = nt.nodes.new("ShaderNodeEmission")
    K.ln(nt, K.inst_attr(nt, "col"), em.inputs["Color"])
    em.inputs["Strength"].default_value = 1.3
    K.ln(nt, em.outputs[0], out.inputs["Surface"])
    cm.cycles.emission_sampling = "NONE"
    colp = K.proto(ctx, "p_col", K.bm_ico(1.0, sub=3), [cm])
    colo = K.instancer(ctx, "cols", colp, NCOL)
    cfo = K.instancer(ctx, "conf", K.proto(ctx, "p_conf", K.bm_ico(0.06, sub=2),
                                            [K.mat_emit("m_conf", (1.0, 0.15, 0.1), 8.0)]), NCONF)
    cam = K.CamRig(ctx, 35, fstop=0)
    cp = sim["col_pos"]
    # 카메라: (t, 위도, 경도, 거리)
    CAM = [(0.0, 25, 10, 25.0), (4.5, 30, 20, 21.0), (10.0, 20, 40, 23.0), (16.0, 25, 70, 24.0),
           (22.0, 22, 88, 20.0), (28.0, 15, 60, 24.0), (34.0, 10, 30, 24.0), (40.0, 8, 25, 20.0),
           (48.0, 12, 10, 23.0), (56.0, 20, -10, 26.0)]

    def upd(t, f):
        la, lo, dist = keyed(t, [(k[0], k[1:]) for k in CAM])
        p = K.latlon_to_xyz(la, lo, 1.0)
        az = math.degrees(math.atan2(p[1], p[0]))
        cam.set((0, 0, 0), az, la, dist, 35)
        sd = K.aim_sun(sun, az, la, side=55.0, up=10.0)
        ctx.set_rgb("sun_dir", tuple(sd))
        ctx.set_ctl("night_lights", 1.0)
        ctx.set_ctl("borders_gone", ramp(t, 4.6, 9.8) * 1.01)
        ctx.set_ctl("borders_glow", 3.0)
        n = NFLOW
        K.set_points(flo, sim["fl_p"][f], scale=sim["fl_s"][f], rot=np.zeros((n, 3)), col=np.ones((n, 3)))
        ms = (ramp(t, 16.0, 16.8) * (1 - ramp(t, 18.5, 21.0))) * np.ones(NMIL)
        K.set_points(mil, sim["mil"], scale=ms, rot=np.zeros((NMIL, 3)), col=np.ones((NMIL, 3)))
        grow = ramp(t, 22.2, 24.0) * (1 - ramp(t, 27.5, 28.5))
        rad = (0.05 + 0.5 * np.sqrt(sim["col_h"])) * grow
        K.set_points(colo, cp * 1.01, scale=rad, rot=np.zeros((NCOL, 3)), col=sim["col_c"])
        pulse = ramp(t, 40.3, 41.5) * (0.55 + 0.45 * np.sin(t * 6 + sim["conf_ph"]))
        K.set_points(cfo, sim["conf"], scale=pulse, rot=np.zeros((NCONF, 3)), col=np.ones((NCONF, 3)))

    ctx.on_frame(upd)
