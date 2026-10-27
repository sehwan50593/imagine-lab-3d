"""도시 섬 공통 장면 (EP03 법 / EP07 집 / EP09 AI).

sim 단계: base_sim() — 건물·나무·가로등·사람·차 기본 배치와 걸음 (numpy)
Blender 단계: City — 섬·땅·건물·사람·차·나무·가로등을 만들고 프레임마다 갱신
"""
import math

import numpy as np

from .common import FPS, keyed
from .layout import RoadWalkers, city_layout, push_out_of_rects, river_y

R = 10.5
SPACING = 2.8
ROAD_W = 0.58
RIVER = (0.22, -2.6, 1.3, 0.55)
PALETTE = np.array([(0.78, 0.74, 0.66), (0.66, 0.70, 0.76), (0.80, 0.62, 0.50), (0.60, 0.64, 0.62),
                    (0.86, 0.82, 0.74), (0.52, 0.56, 0.66), (0.74, 0.56, 0.46)], np.float32)


def base_sim(rs, nf, n_people=120, n_cars=26, tree_n=90, people_speed=(0.5, 0.85)):
    bld = city_layout(rs, R, SPACING, ROAD_W, river=RIVER, margin=0.7)
    nb = len(bld)
    col = PALETTE[rs.integers(0, len(PALETTE), nb)] * rs.uniform(0.85, 1.05, (nb, 1))
    walkers = RoadWalkers(rs, R, n_people, rs.uniform(*people_speed, n_people), SPACING, sidewalk=0.4)
    cars = RoadWalkers(rs, R, n_cars, rs.uniform(1.6, 2.4, n_cars), SPACING, lane=0.15)
    ppl_p = np.zeros((nf, n_people, 2), np.float32)
    ppl_yaw = np.zeros((nf, n_people), np.float32)
    car_p = np.zeros((nf, n_cars, 2), np.float32)
    car_yaw = np.zeros((nf, n_cars), np.float32)
    for i in range(nf):
        ppl_p[i], ppl_yaw[i] = walkers.step(1 / FPS)
        car_p[i], car_yaw[i] = cars.step(1 / FPS)
    trees = []
    rects = bld[:, :4]
    tries = 0
    while len(trees) < tree_n and tries < 20000:
        tries += 1
        p = rs.uniform(-R * 0.92, R * 0.92, 2)
        if np.hypot(*p) > R - 0.5 or abs(p[1] - river_y(p[0], RIVER)) < RIVER[2] / 2 + 0.1:
            continue
        q = push_out_of_rects(p[None].astype(np.float32), rects, pad=0.25)[0]
        if np.abs(q - p).sum() > 1e-4:
            continue
        # 도로 위는 피함
        dx = abs(((p[0] + SPACING / 2) % SPACING) - SPACING / 2)
        dy = abs(((p[1] + SPACING / 2) % SPACING) - SPACING / 2)
        if min(dx, dy) < ROAD_W / 2 + 0.25:
            continue
        trees.append(p)
    lamps = []
    for i in range(-4, 5):
        for j in range(-4, 5):
            for ox, oy in ((0.45, 0.45), (-0.45, -0.45)):
                p = np.array([i * SPACING + ox + SPACING / 2, j * SPACING + oy], np.float32)
                if np.hypot(*p) < R - 0.8 and abs(p[1] - river_y(p[0], RIVER)) > 1.2:
                    lamps.append(p)
    return dict(bld=bld, bld_col=col.astype(np.float32), bld_lit=rs.uniform(0.35, 1.0, nb).astype(np.float32),
                bld_seed=rs.uniform(0, 100, nb).astype(np.float32), ppl_p=ppl_p, ppl_yaw=ppl_yaw, car_p=car_p,
                car_yaw=car_yaw, tree_xy=np.array(trees, np.float32), lamp_xy=np.array(lamps, np.float32),
                ppl_col=rs.uniform(0.15, 0.95, (n_people, 3)).astype(np.float32),
                car_col=np.array([(0.75, 0.1, 0.1), (0.1, 0.25, 0.6), (0.85, 0.85, 0.85), (0.1, 0.1, 0.12),
                                  (0.9, 0.7, 0.1)], np.float32)[rs.integers(0, 5, n_cars)])


DAY = dict(elev=42, az=40, energy=3.2, col=(1.0, 0.93, 0.82), amb=0.42, amb_col=(0.45, 0.55, 0.78))
MORNING = dict(elev=16, az=-30, energy=2.6, col=(1.0, 0.78, 0.58), amb=0.32, amb_col=(0.42, 0.48, 0.70))
DUSK = dict(elev=4, az=150, energy=1.6, col=(1.0, 0.48, 0.25), amb=0.16, amb_col=(0.30, 0.25, 0.45))
NIGHT = dict(elev=55, az=200, energy=0.55, col=(0.55, 0.65, 1.0), amb=0.09, amb_col=(0.12, 0.15, 0.32))
GOLD = dict(elev=12, az=120, energy=2.6, col=(1.0, 0.70, 0.42), amb=0.26, amb_col=(0.45, 0.42, 0.55))
BLUE = dict(elev=10, az=170, energy=1.1, col=(0.70, 0.72, 1.0), amb=0.2, amb_col=(0.30, 0.34, 0.62))


class City:
    """Blender 장면 구성 (build 안에서만 생성)."""

    def __init__(self, ctx, sim, people_proto="person", extra_bld_attrs=()):
        from . import bkit as K
        self.K, self.ctx, self.sim = K, ctx, sim
        K.world_space(ctx, ambient=(0.45, 0.55, 0.78), ambient_strength=0.4)
        self.sun = K.sun(ctx, 3.0)
        ground = K.mat_ground(ctx, spacing=SPACING, road_w=ROAD_W, river=RIVER, park=0.3)
        K.island(ctx, R, top_mat=ground)
        bld = sim["bld"]
        self.nb = len(bld)
        bm = self.building_mat()
        pb = K.proto_box(ctx, bm)
        self.bo = K.instancer(ctx, "blds", pb, self.nb, vector_scale=True)
        for a in ("lit", "seed", "glow") + tuple(extra_bld_attrs):
            K.add_attr(self.bo, a)
        K.add_attr(self.bo, "gcol", "FLOAT_COLOR")
        n = sim["ppl_p"].shape[1]
        self.np_ = n
        pp = K.proto_person(ctx, K.mat_inst("m_shirt", 0.7, emit_attr="pglow", emit_color=(1, 1, 1),
                                            emit_strength=3.0),
                            K.mat_simple("m_skin", (0.85, 0.66, 0.52), 0.6))
        self.po = K.instancer(ctx, "people", pp, n)
        K.add_attr(self.po, "pglow")
        nc = sim["car_p"].shape[1]
        self.nc = nc
        pc = K.proto_car(ctx, K.mat_inst("m_car", 0.35, coat=0.6, ctx=ctx, decay_to=(0.22, 0.12, 0.07)),
                         K.mat_simple("m_glass", (0.05, 0.07, 0.1), 0.1),
                         K.mat_emit("m_head", (1.0, 0.95, 0.8), 6.0, ctx, "carlights"),
                         K.mat_emit("m_tail", (1.0, 0.1, 0.05), 6.0, ctx, "carlights"))
        self.co = K.instancer(ctx, "cars", pc, nc)
        leaf = K.mat_inst("m_leaf", 0.85)
        trunk = K.mat_simple("m_trunk", (0.22, 0.14, 0.08), 0.9)
        self.txy = sim["tree_xy"]
        self.to = K.instancer(ctx, "trees", K.proto_tree(ctx, leaf, trunk, "round"), len(self.txy))
        rs = np.random.default_rng(3)
        self.tree_s = rs.uniform(0.8, 1.4, len(self.txy))
        self.tree_c = np.array([(0.13, 0.36, 0.10), (0.18, 0.42, 0.12), (0.10, 0.30, 0.12)],
                               np.float32)[rs.integers(0, 3, len(self.txy))]
        lamp = K.proto_lamp(ctx, K.mat_simple("m_pole", (0.15, 0.15, 0.17), 0.5),
                            K.mat_emit("m_bulb", (1.0, 0.8, 0.5), 9.0, ctx, "lamps"))
        self.lxy = sim["lamp_xy"]
        self.lo = K.instancer(ctx, "lamps", lamp, len(self.lxy))
        self.cam = K.CamRig(ctx, 30, fstop=9.0)
        self.static_done = False

    def building_mat(self):
        """mat_building + 인스턴스 'glow'×'gcol' 발광(벽 전체)."""
        K, ctx = self.K, self.ctx
        m = K.mat_building(ctx, wstr=3.4)
        nt = m.node_tree
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        old_c = bsdf.inputs["Emission Color"].links[0].from_socket
        old_s = bsdf.inputs["Emission Strength"].links[0].from_socket
        g = K.inst_attr(nt, "glow", "Fac")
        gc = K.inst_attr(nt, "gcol")
        a = K.mix_rgb(nt, 1.0, old_c, old_s, "MULTIPLY")
        b = K.mix_rgb(nt, 1.0, gc, K.math_node(nt, "MULTIPLY", g, 4.0), "MULTIPLY")
        K.ln(nt, K.mix_rgb(nt, 1.0, a, b, "ADD"), bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].links[0].from_node.outputs[0]  # noqa
        nt.links.remove(bsdf.inputs["Emission Strength"].links[0])
        bsdf.inputs["Emission Strength"].default_value = 1.0
        return m

    def light(self, t, keys):
        K, ctx = self.K, self.ctx
        lk = [(k, (v["elev"], v["az"], v["energy"], *v["col"], v["amb"], *v["amb_col"])) for k, v in keys]
        L = keyed(t, lk)
        self.sun.rotation_euler = (math.radians(90 - L[0]), 0, math.radians(L[1]))
        self.sun.data.energy = L[2]
        self.sun.data.color = L[3:6]
        ctx.set_ctl("ambient", L[6])
        ctx.set_rgb("ambient_col", L[7:10])
        return max(0.0, min(1.0, (0.3 - L[6]) / 0.2))  # 밤 정도

    def camera(self, t, keys, drift=1.2):
        ks = [(k[0], (*k[1], k[2], k[3], k[4], k[5])) for k in keys]
        v = keyed(t, ks)
        close = max(0.0, min(1.0, (32 - v[5]) / 20))
        self.cam.set(v[:3], v[3] + t * drift, v[4], v[5], v[6], shift=0.07 * (1 - close))

    def update(self, f, bld_h=None, bld_scale=None, bld_glow=None, bld_gcol=None, bld_lit=None, bld_rot=None,
               ppl_p=None, ppl_scale=None, ppl_col=None, ppl_glow=None, car_scale=None, car_p=None, car_yaw=None,
               tree_scale=None, lamp_scale=1.4):
        K, sim = self.K, self.sim
        bld = sim["bld"]
        nb = self.nb
        h = bld[:, 4] if bld_h is None else bld_h
        K.set_points(self.bo, np.c_[bld[:, :2], np.zeros(nb)],
                     scale=np.ones(nb) if bld_scale is None else bld_scale,
                     size=np.c_[bld[:, 2:4], h], rot=np.zeros((nb, 3)) if bld_rot is None else bld_rot,
                     col=sim["bld_col"], lit=sim["bld_lit"] if bld_lit is None else bld_lit, seed=sim["bld_seed"],
                     glow=np.zeros(nb) if bld_glow is None else bld_glow,
                     colors={"gcol": np.ones((nb, 3)) if bld_gcol is None else bld_gcol})
        n = self.np_
        p = sim["ppl_p"][f] if ppl_p is None else ppl_p
        K.set_points(self.po, np.c_[p, np.zeros(n)], scale=np.ones(n) * 1.05 if ppl_scale is None else ppl_scale,
                     rot=np.c_[np.zeros((n, 2)), sim["ppl_yaw"][f]],
                     col=sim["ppl_col"] if ppl_col is None else ppl_col,
                     pglow=np.zeros(n) if ppl_glow is None else ppl_glow)
        cp = sim["car_p"][f] if car_p is None else car_p
        cy = sim["car_yaw"][f] if car_yaw is None else car_yaw
        K.set_points(self.co, np.c_[cp, np.zeros(self.nc)],
                     scale=np.full(self.nc, 1.3) if car_scale is None else car_scale,
                     rot=np.c_[np.zeros((self.nc, 2)), cy], col=sim["car_col"])
        if not self.static_done or tree_scale is not None:
            ts = self.tree_s if tree_scale is None else tree_scale
            K.set_points(self.to, np.c_[self.txy, np.zeros(len(self.txy))], scale=ts,
                         rot=np.c_[np.zeros((len(self.txy), 2)), np.arange(len(self.txy)) * 2.4 % 6.28],
                         col=self.tree_c)
            K.set_points(self.lo, np.c_[self.lxy, np.zeros(len(self.lxy))], scale=np.full(len(self.lxy), lamp_scale),
                         rot=np.zeros((len(self.lxy), 3)), col=np.ones((len(self.lxy), 3)))
            self.static_done = True
