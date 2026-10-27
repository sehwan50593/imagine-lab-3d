"""EP07 만약 세상의 모든 집이 사라진다면? (잠실 아파트 단지)

실제로 계산하는 것:
- 오픈스트리트맵 '아파트' 건물이 사라지고, 그 자리에 살던 사람(에이전트)이 밖에 남음
- 대피: 가장 가까운 '집이 아닌 건물'(몰·학교·상가)로 걸어가 정원(바닥면적 비례)이 차면 다음 건물로
- 넘친 사람은 공원에 모닥불·텐트 (텐트 수는 날짜에 따라 로지스틱 증가) / 1년 뒤 재건
"""
import math

import numpy as np

from engine.common import FPS, Beat, frames_of, keyed, ramp
from engine.jamsil_ep import CAR_COLORS, crowd, light_keys, people_colors, pose_of, set_cam, sky_at, traffic

DUR = 56.0
META = {"id": "ep07", "title": "만약 세상의 모든 집이 사라진다면?", "duration": DUR,
        "render": {"pct": 50, "samples": 10, "bounces": 2, "chunks": 7},
        "music": {"key": "Bb", "mode": "major", "bpm": 66, "seed": 7, "twist_at": 40.0}}
FOCUS = np.array([-1500.0, -600.0])
NR, NW, NC, NT = 900, 260, 90, 160

BEATS = [
    Beat(0.0, 4.5, badge="D-DAY 18:00", label="집", big="23억 가구 → 0", label_color="orange",
         sub="만약 오늘 저녁, 세상의 모든 집이\n한순간에 사라진다면?"),
    Beat(4.5, 10.0, badge="D-DAY 18:05", title="잠실 아파트가 {orange}텅{/}", note="송파구 인구 64만 8천 명 (2026)",
         sub="퇴근길 사람들이 돌아갈 곳이\n한순간에 사라졌습니다."),
    Beat(10.0, 16.0, badge="D-DAY 23:00", title="하루의 {orange}90%{/}를 보내던 곳",
         note="사람은 하루의 약 90%를 실내에서 보낸다 (미국 EPA)",
         sub="지붕도 벽도 없는 첫날 밤,\n사람들은 불빛이 있는 곳으로 모입니다."),
    Beat(16.0, 22.0, badge="D+1", title="몰·학교·역이 {cyan}대피소{/}로", note="롯데월드몰 하루 방문객 약 17만 명",
         sub="집이 아닌 건물은 그대로라\n사람들이 한꺼번에 몰려듭니다."),
    Beat(22.0, 28.0, badge="D+7", title="{orange}28억 명{/}은 원래 이랬다",
         note="부적절한 주거 28억 명 · 노숙 약 3억 명 (UN-Habitat, 2025)",
         sub="집이 없는 삶은 누군가에겐\n이미 일상입니다."),
    Beat(28.0, 34.0, badge="D+30", title="공원이 {green}텐트 도시{/}로",
         sub="공원과 호숫가에\n임시 거처가 빼곡히 들어섭니다."),
    Beat(34.0, 40.0, badge="1년 후", title="다시 짓는다", note="세계 건물 바닥 면적 2,730억 m² (2024)",
         sub="인류가 지어 온 건물을\n처음부터 다시 쌓아 올려야 합니다."),
    Beat(40.0, 48.0, badge="반전", title="인류는 원래 {green}집이 없었다{/}", big="95%", big_size=112,
         note="호모 사피엔스 약 31.5만 년, 첫 정착 마을은 약 1.5만 년 전 (계산)",
         sub="인류 역사의 95% 이상은\n붙박이 집 없이 살았습니다."),
    Beat(48.0, 56.0, badge="지금", title="집이 사라진 첫날 밤,\n당신은 {orange}어디{/}로 가실 건가요?", title_size=70),
]
GRADE = {"exposure": 0.95, "bloom": 0.3, "bloom_thr": 1.0, "vignette": 0.32}
SKY = [(0.0, "DUSK"), (5.0, "DUSK"), (7.5, "NIGHT"), (15.4, "NIGHT"), (16.6, "MORNING"), (17.6, "DAY"), (27.6, "DAY"),
       (28.6, "DUSK"), (33.4, "DUSK"), (34.4, "DAY"), (39.4, "DAY"), (40.6, "NIGHT"), (56.0, "NIGHT")]
CLOCK = [(0.0, 0.75), (4.5, 0.75), (5.0, 0.7535), (10.0, 0.76), (10.6, 0.958), (16.0, 0.96), (16.6, 1.5),
         (22.0, 1.6), (22.6, 7.5), (28.0, 7.6), (28.6, 30.0), (34.0, 31.0), (34.6, 365.0), (56.0, 366.0)]


def day_at(t):
    return keyed(t, CLOCK, ease=lambda u: u)


def fi(t):
    return int(min(frames_of(DUR) - 1, max(0, round(t * FPS))))


def simulate(build_dir):
    from engine.jamsil import geometry
    g = geometry()
    rs = np.random.default_rng(707)
    nf = frames_of(DUR)
    ts = np.arange(nf) / FPS
    days = np.array([day_at(t) for t in ts])
    cent, hts, kind, area = g["b_cent"], g["b_h"], g["b_kind"], g["b_area"]
    nb = len(hts)
    dist = np.hypot(cent[:, 0] - FOCUS[0], cent[:, 1] - FOCUS[1])
    tower = int(g["tower"][0])
    shelter_mask = ((kind == 0) & (area >= 900) & (hts >= 8)) | (area >= 2500)
    shelter_mask[tower] = True
    home = ~shelter_mask
    # 사라짐: 초점에서 가까운 순서로 1.8~3.2초 사이
    vanish_t = 1.8 + 1.4 * np.clip(dist / 2500, 0, 1) + rs.uniform(0, 0.25, nb)
    rebuild_t = 34.6 + 4.0 * rs.random(nb)
    hscale = np.ones((nf, nb), np.float32)
    for i, t in enumerate(ts):
        down = np.clip(1 - (t - vanish_t) / 0.5, 0, 1)
        up = np.clip((t - rebuild_t) / 1.4, 0, 1)
        if t >= 40.0:  # 반전 장면은 다시 '집 없는' 밤
            up = up * np.clip(1 - (t - 40.0) / 0.6, 0, 1)
        hscale[i] = np.where(home, np.maximum(np.maximum(down, up), 0.6 / np.maximum(hts, 1)), 1.0)  # 기초 판만 남음
    sparkle_t = vanish_t
    # 남은 사람(주민): 사라진 아파트 둘레에서 생겨남
    near_home = np.where(home & (dist < 260))[0]
    pick = rs.choice(near_home, NR)
    rad = np.sqrt(area[pick] / np.pi)
    ang = rs.uniform(0, 2 * np.pi, NR)
    start = cent[pick] + np.stack([np.cos(ang), np.sin(ang)], 1) * (rad * rs.uniform(0.3, 1.1, NR))[:, None]
    appear = vanish_t[pick] + 0.2
    # 대피소: 초점 900m 안의 '집 아닌' 큰 건물, 정원 = 바닥면적/2.5㎡
    shel = np.where((~home) & (dist < 900))[0]
    cap = (area[shel] / 2.5).astype(int)
    load = np.zeros(len(shel), int)
    target = np.zeros((NR, 2), np.float32)
    go_shelter = np.zeros(NR, bool)
    # 야영지: 초점 근처 공원 3곳(오픈스트리트맵 녹지)에 모임
    sites = np.array([(-1659.0, -713.0), (-1629.0, -654.0), (-1406.0, -487.0)], np.float32)
    sk = rs.choice(len(sites), NT, p=[0.45, 0.35, 0.2])
    camp_pick = sites[sk] + rs.normal(0, 13, (NT, 2))
    for k in np.argsort(rs.random(NR)):
        d = np.hypot(cent[shel, 0] - start[k, 0], cent[shel, 1] - start[k, 1])
        order = np.argsort(d)
        placed = False
        for j in order[:6]:
            if load[j] < cap[j] * 0.01 + 4:   # 화면에 보이는 사람 수에 맞춘 정원 축소
                load[j] += 1
                target[k] = cent[shel[j]] + rs.normal(0, 6, 2)
                go_shelter[k] = True
                placed = True
                break
        if not placed or rs.random() < 0.45:
            target[k] = camp_pick[rs.integers(0, NT)] + rs.normal(0, 3, 2)
            go_shelter[k] = False
    shel_fill = np.zeros((nf, len(shel)), np.float32)
    r_pos = np.zeros((nf, NR, 2), np.float32)
    r_yaw = np.zeros((nf, NR), np.float32)
    r_on = np.zeros((nf, NR), np.float32)
    r_walk = np.zeros((nf, NR), np.float32)
    speed = rs.uniform(9.0, 14.0, NR)  # 화면용 (밤사이 몇 시간을 몇 초에)
    pos = start.copy()
    for i, t in enumerate(ts):
        act = t >= appear
        moving = act & (t >= 10.2) & (t < 40.0)
        d = target - pos
        L = np.hypot(d[:, 0], d[:, 1]) + 1e-6
        step = np.minimum(L, speed / FPS)
        mv = moving & (L > 1.5)
        pos[mv] += (d[mv] / L[mv, None]) * step[mv, None]
        r_pos[i] = pos
        r_yaw[i] = np.where(L > 1.5, np.arctan2(d[:, 1], d[:, 0]), r_yaw[i - 1] if i else 0)
        inside = go_shelter & (L <= 1.5) & (t < 40.0)
        r_on[i] = act & ~inside
        r_walk[i] = mv
        if t >= 40.0:  # 반전: 모두 밖, 모닥불 둘레
            r_on[i] = 1.0
        # 대피소 불빛 = 도착 비율
        arrived = go_shelter & (L <= 1.5)
        for j in range(len(shel)):
            pass
    tents_n = np.clip(1 / (1 + np.exp(-(np.log10(np.maximum(days, 0.01)) - np.log10(7)) * 5)), 0, 1)
    tents_n = np.where(ts < 34.6, tents_n, np.clip(1 - (ts - 34.6) / 3.0, 0, 1)) * (ts < 40.0)
    shelter_glow = np.clip((ts - 11.0) / 4.0, 0, 1) * (ts < 34.6)
    fire = np.where((ts > 10.5) & ((ts < 16.6) | (ts > 40.0)), 1.0, 0.0) + np.where((ts > 28.6) & (ts < 34.4), 0.6, 0.0)
    pp, py, ph = crowd(rs, nf, NW, (-1500, -600), 500)
    shirt, pants = people_colors(rs, NW)
    r_shirt, r_pants = people_colors(rs, NR)
    cp, cy = traffic(rs, nf, NC, (-1500, -600), 900, stop=lambda t: 1.0 if t < 2.0 else 0.0)
    walkers_on = np.clip(1 - (ts - 2.0) / 1.0, 0, 1)  # 길 가던 사람은 주민 무리에 섞임
    camp_c = np.array([-1645.0, -690.0], np.float32)
    return dict(camp_c=camp_c.astype(np.float32), home=home.astype(np.float32), days=days, hscale=hscale, shel=shel.astype(np.int32), shelter_glow=shelter_glow.astype(np.float32),
                r_pos=r_pos, r_yaw=r_yaw, r_on=r_on, r_walk=r_walk, r_shirt=r_shirt, r_pants=r_pants,
                camp=camp_pick.astype(np.float32), tents=tents_n.astype(np.float32), fire=fire.astype(np.float32),
                pp=pp, py=py, ph=ph, shirt=shirt, pants=pants, walkers_on=walkers_on.astype(np.float32), cp=cp, cy=cy,
                ccol=CAR_COLORS[rs.integers(0, len(CAR_COLORS), NC)], sparkle_t=sparkle_t.astype(np.float32))


def sky(t):
    return sky_at(t, SKY)


def fmt_clock(d):
    if d < 1:
        h = d * 24
        return f"D-DAY {int(h):02d}:{int((h % 1) * 60):02d}"
    if d < 300:
        return f"D+{int(d)}"
    return "1년 후"


def hud(t, sim):
    f = fi(t)
    d = float(sim["days"][f])
    outside = int(sim["r_on"][f].sum())
    r2 = f"이 구역 밖에 있는 사람 {outside}명" if 2.0 < t < 40.0 else ("집이 사라지기 전" if t <= 2.0 else "약 1.5만 년 전까지의 인류")
    return {"left": "SIMULATION", "right": fmt_clock(d), "right2": r2}


CAM = [(0.0, (-1500.0, -600.0, 20.0), 240, 34, 340.0, 30), (4.4, (-1500.0, -600.0, 10.0), 250, 34, 300.0, 30),
       (9.8, (-1500.0, -600.0, 3.0), 260, 34, 170.0, 30), (10.4, ("camp", 0, 2.0), 235, 28, 55.0, 30),
       (15.8, ("camp", 0, 2.0), 250, 30, 62.0, 30), (16.4, (-1500.0, -600.0, 5.0), 210, 40, 230.0, 30),
       (21.8, (-1500.0, -600.0, 5.0), 225, 42, 260.0, 30), (22.4, ("camp", 0, 2.0), 300, 28, 48.0, 30),
       (27.8, ("camp", 0, 2.0), 315, 30, 56.0, 30), (28.4, ("camp", 0, 3.0), 200, 42, 120.0, 30),
       (33.8, ("camp", 0, 3.0), 215, 45, 140.0, 30), (34.4, (-1500.0, -600.0, 30.0), 230, 30, 420.0, 30),
       (39.8, (-1500.0, -600.0, 30.0), 250, 32, 460.0, 30), (40.4, ("camp", 0, 2.0), 260, 22, 42.0, 30),
       (47.8, ("camp", 0, 2.0), 280, 24, 48.0, 30), (48.4, ("camp", 0, 4.0), 290, 34, 150.0, 30),
       (56.0, ("camp", 0, 4.0), 305, 38, 200.0, 30)]


def build(ctx):
    from engine import bkit as K
    from engine.jamsil import Jamsil, geometry
    sim = ctx.sim
    g = geometry()
    J = Jamsil(ctx, g)
    ro = J.people(NR, "residents")
    po = J.people(NW, "walkers")
    co = J.cars(NC)
    nb = J.nb
    cyan = np.tile((0.4, 0.85, 1.0), (nb, 1)).astype(np.float32)
    J.set_buildings(gcol=cyan, glow=np.zeros(nb), dark=np.zeros(nb))
    fire = K.instancer(ctx, "fires", K.proto(ctx, "p_fire7", K.bm_ico(0.7, sub=1),
                                              [K.mat_emit("m_fire7", (1.0, 0.5, 0.15), 9.0, ctx, "fire")]), len(sim["camp"]))
    tent_bm = K.bm_cone(2.2, 0.0, 2.5, seg=4)
    tent = K.instancer(ctx, "tents", K.proto(ctx, "p_tent", tent_bm, [K.mat_inst("m_tent", 0.7)]), len(sim["camp"]))
    rs = np.random.default_rng(3)
    tent_col = np.array([(0.85, 0.55, 0.2), (0.2, 0.45, 0.75), (0.6, 0.6, 0.62), (0.3, 0.55, 0.3)],
                        np.float32)[rs.integers(0, 4, len(sim["camp"]))]
    tent_xy = sim["camp"] + rs.normal(0, 5, sim["camp"].shape).astype(np.float32)
    tent_rank = rs.random(len(sim["camp"]))
    sp = K.instancer(ctx, "vanish_sparks", K.proto(ctx, "p_vsp", K.bm_ico(1.2, sub=1),
                                                    [K.mat_emit("m_vsp", (0.8, 0.9, 1.0), 6.0)]), nb)
    cent = g["b_cent"]
    home = sim["home"] > 0.5
    lk = light_keys(SKY)
    for k_, v_ in lk:
        if v_["amb"] < 0.1:  # 이 편의 밤은 조금 더 밝게 (사람이 보이게)
            v_ = dict(v_, energy=0.75, amb=0.12)
    lk = [(k_, dict(v_, energy=max(v_["energy"], 0.75), amb=max(v_["amb"], 0.12))) for k_, v_ in lk]
    shel = sim["shel"]

    cc = tuple(float(v) for v in sim["camp_c"])
    CAMX = [(k[0], (cc[0], cc[1], k[1][2]) if k[1][0] == "camp" else k[1], *k[2:]) for k in CAM]

    def upd(t, f):
        set_cam(J, t, CAMX)
        night = J.light(t, lk)
        ctx.set_ctl("lights", 0.1 + 0.55 * night)
        ctx.set_ctl("carlights", 0.3 + 0.7 * night)
        ctx.set_ctl("fire", float(sim["fire"][f]) * (0.75 + 0.25 * math.sin(t * 13)))
        glow = np.zeros(nb, np.float32)
        glow[shel] = float(sim["shelter_glow"][f]) * (0.25 + 0.4 * night)
        J.set_buildings(hscale=sim["hscale"][f], glow=glow)
        # 사라지는 순간 반짝임
        dt_ = t - sim["sparkle_t"]
        ss = np.where(home & (dt_ > 0) & (dt_ < 0.8), (1 - dt_ / 0.8) * 3.0, 0.0)
        zz = np.where(home, g["b_h"] * 0.5 * np.clip(1 - dt_ / 0.8, 0, 1), 0)
        K.set_points(sp, np.c_[cent, zz], scale=ss, rot=np.zeros((nb, 3)), col=np.ones((nb, 3)))
        rp = sim["r_pos"][f]
        rpose = pose_of((t * 1.7 + np.arange(NR) * 0.31) % 1.0, sim["r_walk"][f] > 0.5)
        K.set_points(ro, np.c_[rp, np.zeros(NR)], scale=sim["r_on"][f], rot=np.c_[np.zeros((NR, 2)), sim["r_yaw"][f]],
                     col=sim["r_shirt"], colors={"col2": sim["r_pants"]}, pose=rpose)
        won = float(sim["walkers_on"][f])
        K.set_points(po, np.c_[sim["pp"][f], np.zeros(NW)], scale=np.full(NW, won),
                     rot=np.c_[np.zeros((NW, 2)), sim["py"][f]], col=sim["shirt"], colors={"col2": sim["pants"]},
                     pose=pose_of(sim["ph"][f]))
        K.set_points(co, np.c_[sim["cp"][f], np.zeros(NC)], scale=np.full(NC, 10.0),
                     rot=np.c_[np.zeros((NC, 2)), sim["cy"][f]], col=sim["ccol"])
        nfire = len(sim["camp"])
        fs = np.full(nfire, float(sim["fire"][f]) > 0.05, np.float32) * (0.8 + 0.3 * np.sin(t * 9 + np.arange(nfire)))
        K.set_points(fire, np.c_[sim["camp"], np.full(nfire, 0.4)], scale=fs, rot=np.zeros((nfire, 3)),
                     col=np.ones((nfire, 3)))
        tn = float(sim["tents"][f])
        K.set_points(tent, np.c_[tent_xy, np.zeros(nfire)], scale=(tent_rank < tn).astype(np.float32),
                     rot=np.c_[np.zeros((nfire, 2)), tent_rank * 6.28], col=tent_col)

    ctx.on_frame(upd)
