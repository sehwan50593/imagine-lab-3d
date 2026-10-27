"""잠실 도시 (오픈스트리트맵, © OpenStreetMap contributors, ODbL) — 1단위 = 1m.

sim 단계: geometry() — 원판(반경 RAD)으로 자른 건물·도로·물·녹지 메시 배열 + 사람/차 경로
Blender 단계: Jamsil — 메시 생성, 롯데월드타워(555m), 나무, 사람(걷기 자세), 차
"""
import math

import numpy as np

from .common import ASSETS, BUILD

CX, CY, RAD = -850.0, 250.0, 1750.0     # 원판 중심·반경 (타워 = 원점)
TOWER_H = 555.0
FLOOR = 3.1
# 동네별 원판 (오픈스트리트맵 자료 이름 → 중심·반경·롯데타워 여부)
AREAS = {"jamsil": dict(cx=-850.0, cy=250.0, rad=1750.0, tower=True),
         # 강남 한강변 자료(원점 37.5150N, 127.0235E): 압구정·청담 쪽 / 반포 쪽
         # river: 한강이 강둑 선의 어느 쪽인지 / fill_heights: 높이 정보 없는 건물(기본값)에 바닥 면적 맞춤 층수
         "apgujeong": dict(file="gangnam", cx=650.0, cy=950.0, rad=1500.0, river="north", fill_heights=True),
         "banpo": dict(file="gangnam", cx=-1950.0, cy=-650.0, rad=1500.0, river="north", fill_heights=True)}


def use_area(name):
    """다른 동네로 바꿀 때: 이 모듈의 원판 상수를 바꾸고 geometry(name)을 부름."""
    global CX, CY, RAD, AREA
    a = AREAS[name]
    CX, CY, RAD = a["cx"], a["cy"], a["rad"]
    AREA = name


AREA = "jamsil"


def _unpack(pts, off):
    return [pts[a:b] for a, b in zip(off[:-1], off[1:])]


def _clip_poly(poly, n=96):
    """원판(볼록 다각형 근사)으로 다각형 자르기 (Sutherland–Hodgman)."""
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    clip = np.stack([CX + RAD * np.cos(ang), CY + RAD * np.sin(ang)], 1)
    out = [tuple(p) for p in poly]
    for i in range(n):
        a, b = clip[i], clip[(i + 1) % n]
        inp, out = out, []
        if not inp:
            break

        def inside(p):
            return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0

        def inter(p, q):
            d1 = np.array(q) - np.array(p)
            d2 = b - a
            den = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(den) < 1e-9:
                return p
            tt = ((a[0] - p[0]) * d2[1] - (a[1] - p[1]) * d2[0]) / den
            return (p[0] + tt * d1[0], p[1] + tt * d1[1])
        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(inter(s, e))
                out.append(e)
            elif inside(s):
                out.append(inter(s, e))
            s = e
    return np.array(out, np.float32).reshape(-1, 2)


def _in_disc(p, margin=0.0):
    return np.hypot(p[..., 0] - CX, p[..., 1] - CY) < RAD - margin


def _area(p):
    return 0.5 * float(np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1]))


def geometry(area=None):
    """한 번 계산해 build/_<동네>_geo.npz 에 저장 (같은 동네 편 공용)."""
    if area and area != AREA:
        use_area(area)
    name = AREA
    cache = BUILD / f"_{name}_geo_v3.npz"
    if cache.exists():
        return dict(np.load(cache, allow_pickle=False))
    z = np.load(ASSETS / "geo" / f"{AREAS[name].get('file', name)}.npz")
    has_tower = AREAS[name].get("tower", False)
    fill_h = AREAS[name].get("fill_heights", False)
    rs = np.random.default_rng(7)
    rh = np.random.default_rng(11)
    # ── 건물 ──
    bv, bf, bfs, bfid, bvid, bvz = [], [], [], [], [], []
    cent, hts, kinds, fps = [], [], [], []
    tower_idx = None
    polys = _unpack(z["b_pts"], z["b_off"])
    for i, p in enumerate(polys):
        c = p.mean(0)
        if not _in_disc(c, 30):
            continue
        h = float(z["b_h"][i])
        area = abs(_area(p))
        if fill_h and h in (10.0, 25.0):   # building=yes(10m)·commercial(25m) 기본값 → 면적에 맞춘 층수
            fl = (4.6 if h == 10.0 else 7.5) + 1.1 * math.log(max(area, 40.0) / 200.0) + rh.normal(0, 1.2)
            h = float(np.clip(round(fl), 2, 16)) * 3.3 + 1.0
        if has_tower and p[:, 0].min() < 0 < p[:, 0].max() and p[:, 1].min() < 0 < p[:, 1].max() and area < 9000:
            tower_idx = len(cent)
            h = TOWER_H
        k = int(z["b_kind"][i])
        if h < 4:
            h = 4.0
        bid = len(cent)
        cent.append(c)
        hts.append(h)
        kinds.append(k)
        fps.append(area)
        if _area(p) < 0:
            p = p[::-1]
        n = len(p)
        base = len(bv)
        levels = [0.0, h] if bid != tower_idx else list(np.linspace(0, h, 14))
        for li, zz in enumerate(levels):
            if bid == tower_idx:
                u = zz / h
                sc = 1.0 - 0.62 * u ** 1.25          # 위로 갈수록 가늘어짐
                q = c + (p - c) * sc
            else:
                q = p
            for x, y in q:
                bv.append((x, y, zz))
                bvid.append(bid)
                bvz.append(zz)
        nl = len(levels)
        for li in range(nl - 1):
            r0, r1 = base + li * n, base + (li + 1) * n
            for j in range(n):
                k2 = (j + 1) % n
                bf.extend((r0 + j, r0 + k2, r1 + k2, r1 + j))
                bfs.append(4)
                bfid.append(bid)
        top = base + (nl - 1) * n
        bf.extend(range(top, top + n))
        bfs.append(n)
        bfid.append(bid)
    # ── 도로 띠 ──
    rv, rf, rkind = [], [], []
    rpolys = _unpack(z["r_pts"], z["r_off"])
    walk_lines, car_lines = [], []
    for i, p in enumerate(rpolys):
        keep = _in_disc(p, 5)
        if keep.sum() < 2:
            continue
        w = float(z["r_w"][i])
        kd = int(z["r_kind"][i])
        zz = {2: 0.12, 0: 0.10, 1: 0.14}[kd]
        seg_pts = []
        for a, b, ka, kb in zip(p[:-1], p[1:], keep[:-1], keep[1:]):
            if not (ka and kb):
                if len(seg_pts) > 1:
                    (car_lines if kd == 2 else walk_lines).append(np.array(seg_pts))
                seg_pts = []
                continue
            d = b - a
            L = np.hypot(*d)
            if L < 0.01:
                continue
            nrm = np.array([-d[1], d[0]]) / L * (w / 2)
            base = len(rv)
            for q in (a - nrm, a + nrm, b + nrm, b - nrm):
                rv.append((q[0], q[1], zz))
            rf.append((base, base + 1, base + 2, base + 3))
            rkind.append(kd)
            if not seg_pts:
                seg_pts.append(a)
            seg_pts.append(b)
        if len(seg_pts) > 1:
            (car_lines if kd == 2 else walk_lines).append(np.array(seg_pts))
    # ── 물·녹지 다각형 ──
    def polyset(polys):
        vs, fs, fsz = [], [], []
        for p in polys:
            q = _clip_poly(p)
            if len(q) < 3 or abs(_area(q)) < 20:
                continue
            if _area(q) < 0:
                q = q[::-1]
            base = len(vs)
            vs.extend((x, y, 0.0) for x, y in q)
            fs.extend(range(base, base + len(q)))
            fsz.append(len(q))
        return np.array(vs, np.float32).reshape(-1, 3), np.array(fs, np.int32), np.array(fsz, np.int32)
    wpolys = _unpack(z["w_pts"], z["w_off"])
    side = AREAS[name].get("river")
    if side and "wb_pts" in z:
        # 자료 범위 밖으로 이어지는 강둑(열린 선) → 물 쪽으로 멀리 닫아 다각형, 원판을 지나는 것만
        far = 2e4 if side == "north" else -2e4
        for p in _unpack(z["wb_pts"], z["wb_off"]):
            if _in_disc(p).any():
                wpolys.append(np.vstack([p, [[p[-1, 0], far], [p[0, 0], far]]]).astype(np.float32))
    wv, wf, wfs = polyset(wpolys)
    gv, gf, gfs = polyset(_unpack(z["g_pts"], z["g_off"]))
    # ── 나무: 녹지 안 무작위 + 보도 옆 가로수 ──
    trees = []
    gpolys = [_clip_poly(p) for p in _unpack(z["g_pts"], z["g_off"])]
    for q in gpolys:
        if len(q) < 3:
            continue
        a = abs(_area(q))
        k = int(min(60, a / 450))
        if k == 0:
            continue
        lo, hi = q.min(0), q.max(0)
        cand = rs.uniform(lo, hi, (k * 3, 2))
        # 점-다각형 포함 판정
        x, y = cand[:, 0:1], cand[:, 1:2]
        xi, yi = q[None, :, 0], q[None, :, 1]
        xj, yj = np.roll(xi, 1, 1), np.roll(yi, 1, 1)
        cross = ((yi > y) != (yj > y)) & (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi)
        ins = cross.sum(1) % 2 == 1
        trees.extend(cand[ins][:k])
    street = []
    for ln_ in car_lines:
        for a, b in zip(ln_[:-1], ln_[1:]):
            d = b - a
            L = np.hypot(*d)
            if L < 1:
                continue
            nrm = np.array([-d[1], d[0]]) / L
            for u in np.arange(0, L, 34.0):
                for sgn in (-1, 1):
                    street.append(a + d / L * u + nrm * sgn * 14.0)
    street = np.array(street, np.float32).reshape(-1, 2)
    # 차도 위(다른 차선 위)에 놓인 가로수 제거: 차도 사각형 중심과 너무 가까우면 뺌
    rq = np.array(rv, np.float32).reshape(-1, 4, 3)
    rk_ = np.array(rkind)
    rc = rq[rk_ == 2, :, :2].mean(1)
    rwid = np.linalg.norm(rq[rk_ == 2, 0, :2] - rq[rk_ == 2, 1, :2], axis=1)
    keep = np.ones(len(street), bool)
    for s0 in range(0, len(street), 1500):
        dd = np.hypot(street[s0:s0 + 1500, None, 0] - rc[None, :, 0], street[s0:s0 + 1500, None, 1] - rc[None, :, 1])
        keep[s0:s0 + 1500] = ~(dd < rwid[None, :] * 0.5 + 6.0).any(1)
    trees = np.array(list(trees) + list(street[keep]), np.float32).reshape(-1, 2)
    trees = trees[_in_disc(trees, 10)]
    # 물 위 나무 제거 (호수를 덮는 공원 다각형 안에 뿌려진 것)
    s0 = 0
    for n in wfs:
        q = wv[wf[s0:s0 + n], :2]
        s0 += n
        x, y = trees[:, 0:1], trees[:, 1:2]
        xi, yi = q[None, :, 0], q[None, :, 1]
        xj, yj = np.roll(xi, 1, 1), np.roll(yi, 1, 1)
        wet = (((yi > y) != (yj > y)) & (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi)).sum(1) % 2 == 1
        trees = trees[~wet]
    # 건물 안 나무 제거 (중심 기준 대략)
    cent_a = np.array(cent, np.float32)
    if len(trees) and len(cent_a):
        rad = np.sqrt(np.array(fps) / np.pi)
        keep = np.ones(len(trees), bool)
        for s in range(0, len(trees), 2000):
            d = np.hypot(trees[s:s + 2000, None, 0] - cent_a[None, :, 0], trees[s:s + 2000, None, 1] - cent_a[None, :, 1])
            keep[s:s + 2000] = ~(d < rad[None, :] * 1.05).any(1)
        trees = trees[keep]
    # 경로 묶음 (사람·차)
    def pack_lines(lines):
        pts, off = [], [0]
        for l_ in lines:
            pts.extend(l_)
            off.append(len(pts))
        return np.array(pts, np.float32).reshape(-1, 2), np.array(off, np.int32)
    wl_p, wl_o = pack_lines(walk_lines)
    cl_p, cl_o = pack_lines(car_lines)
    out = dict(bv=np.array(bv, np.float32), bf=np.array(bf, np.int32), bfs=np.array(bfs, np.int32),
               bfid=np.array(bfid, np.int32), bvid=np.array(bvid, np.int32), bvz=np.array(bvz, np.float32),
               b_cent=cent_a, b_h=np.array(hts, np.float32), b_kind=np.array(kinds, np.int8),
               b_area=np.array(fps, np.float32), tower=np.array([tower_idx if tower_idx is not None else -1]),
               rv=np.array(rv, np.float32), rf=np.array(rf, np.int32), rkind=np.array(rkind, np.int8),
               wv=wv, wf=wf, wfs=wfs, gv=gv, gf=gf, gfs=gfs, trees=trees,
               wl_p=wl_p, wl_o=wl_o, cl_p=cl_p, cl_o=cl_o)
    BUILD.mkdir(parents=True, exist_ok=True)
    np.savez(cache, **out)
    return out


def burn_attr_out(nt, K):
    a = nt.nodes.new("ShaderNodeAttribute")
    a.attribute_name = "burn"
    return a.outputs["Fac"]


class PathWalkers:
    """선(폴리라인) 위를 오가는 에이전트. 끝에 닿으면 되돌아가거나 근처 다른 선으로 옮김."""

    def __init__(self, rs, lines, n, speed, offset=0.0, near=None, near_r=None):
        self.lines = [l_ for l_ in lines if len(l_) >= 2 and np.hypot(*(l_[-1] - l_[0])) > 5]
        if near is not None:
            self.lines = [l_ for l_ in self.lines if np.min(np.hypot(*(l_ - np.array(near)).T)) < near_r]
        lens = np.array([np.sum(np.hypot(*np.diff(l_, axis=0).T)) for l_ in self.lines])
        self.cum = [np.r_[0, np.cumsum(np.hypot(*np.diff(l_, axis=0).T))] for l_ in self.lines]
        self.rs = rs
        p = lens / lens.sum()
        self.li = rs.choice(len(self.lines), n, p=p)
        self.s = rs.random(n) * lens[self.li]
        self.dir = rs.choice([-1.0, 1.0], n)
        self.speed = np.asarray(speed) * np.ones(n)
        self.off = offset * rs.choice([-1.0, 1.0], n) if np.isscalar(offset) else offset
        self.lens = lens
        self.n = n

    def step(self, dt, speed_mul=1.0):
        self.s += self.dir * self.speed * dt * speed_mul
        pos = np.zeros((self.n, 2), np.float32)
        yaw = np.zeros(self.n, np.float32)
        for i in range(self.n):
            L = self.lens[self.li[i]]
            if self.s[i] > L or self.s[i] < 0:
                self.dir[i] *= -1
                self.s[i] = np.clip(self.s[i], 0, L)
            l_, c = self.lines[self.li[i]], self.cum[self.li[i]]
            k = int(np.clip(np.searchsorted(c, self.s[i]) - 1, 0, len(l_) - 2))
            seg = l_[k + 1] - l_[k]
            sl = max(c[k + 1] - c[k], 1e-6)
            u = (self.s[i] - c[k]) / sl
            d = seg / sl
            nrm = np.array([-d[1], d[0]])
            off = self.off[i] if not np.isscalar(self.off) else self.off
            pos[i] = l_[k] + seg * u + nrm * off
            yaw[i] = math.atan2(d[1] * self.dir[i], d[0] * self.dir[i])
        return pos, yaw


# ───────────────────────── Blender ─────────────────────────
class Jamsil:
    def __init__(self, ctx, geo, night_windows=True):
        import bpy
        from . import bkit as K
        self.K, self.ctx, self.g = K, ctx, geo
        self.bpy = bpy
        K.world_space(ctx, ambient=(0.45, 0.55, 0.78), ambient_strength=0.4)
        self.sun = K.sun(ctx, 3.0, angle=1.5)
        self.nb = len(geo["b_h"])
        self.b_mesh = self._mesh("buildings", geo["bv"], geo["bf"], geo["bfs"], self._mat_building())
        me = self.b_mesh.data
        me.attributes.new("bid", "FLOAT", "FACE").data.foreach_set("value", geo["bfid"].astype(np.float32))
        for a in ("glow", "dark", "burn"):
            me.attributes.new(a, "FLOAT", "FACE")
        me.attributes.new("gcol", "FLOAT_COLOR", "FACE")
        self.bv0 = geo["bv"].copy()
        self._mesh("roads", geo["rv"], geo["rf"].ravel(), np.full(len(geo["rf"]), 4, np.int32), self._mat_road())
        rd = bpy.data.objects["roads"].data
        rd.attributes.new("rk", "FLOAT", "FACE").data.foreach_set("value", geo["rkind"].astype(np.float32))
        if len(geo["wv"]):
            # 물은 녹지(0.06)보다 위: 호수를 통째로 덮는 공원 다각형에 가려지지 않게
            w = self._mesh("water", geo["wv"] + np.array([0, 0, 0.08], np.float32), geo["wf"], geo["wfs"],
                           K.mat_water("m_jwater", color=(0.03, 0.10, 0.18), rough=0.06))
            w.location.z = 0.0
        if len(geo["gv"]):
            self._mesh("green", geo["gv"] + np.array([0, 0, 0.06], np.float32), geo["gf"], geo["gfs"],
                       K.mat_simple("m_grass", (0.16, 0.32, 0.12), 0.9))
        # 바닥 원판 + 흙 옆면
        top, side = K.island(ctx, RAD, thick=25.0, depth=420.0, top_mat=self._mat_ground())
        top.location = side.location = (CX, CY, 0.0)
        # 나무
        leaf = K.mat_inst("m_jleaf", 0.85)
        trunk = K.mat_simple("m_jtrunk", (0.22, 0.14, 0.08), 0.9)
        tr = geo["trees"]
        self.to = K.instancer(ctx, "jtrees", K.proto_tree(ctx, leaf, trunk, "round"), len(tr))
        rs = np.random.default_rng(9)
        tc = np.array([(0.13, 0.36, 0.10), (0.18, 0.42, 0.12), (0.10, 0.30, 0.12)], np.float32)[rs.integers(0, 3, len(tr))]
        self.tree_xy = tr
        self.tree_s0 = rs.uniform(7, 11, len(tr)).astype(np.float32)
        K.set_points(self.to, np.c_[tr, np.zeros(len(tr))], scale=self.tree_s0,
                     rot=np.c_[np.zeros((len(tr), 2)), rs.uniform(0, 6.28, len(tr))], col=tc)
        self.cam = K.CamRig(ctx, 30, fstop=0)
        self.cam.ob.data.clip_end = 12000

    def _mesh(self, name, verts, faces, sizes, mat):
        bpy = self.bpy
        me = bpy.data.meshes.new(name)
        me.vertices.add(len(verts))
        me.vertices.foreach_set("co", np.asarray(verts, np.float32).ravel())
        me.loops.add(len(faces))
        me.loops.foreach_set("vertex_index", np.asarray(faces, np.int32))
        me.polygons.add(len(sizes))
        starts = np.r_[0, np.cumsum(sizes)[:-1]].astype(np.int32)
        me.polygons.foreach_set("loop_start", starts)
        me.polygons.foreach_set("loop_total", np.asarray(sizes, np.int32))
        me.update(calc_edges=True)
        me.validate()
        me.materials.append(mat)
        ob = bpy.data.objects.new(name, me)
        return self.K.link(ob)

    def _mat_building(self):
        K, ctx = self.K, self.ctx
        m, nt, out = K.new_mat("m_jbld")
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        K.ln(nt, geo.outputs["Position"], sep.inputs[0])
        nsep = nt.nodes.new("ShaderNodeSeparateXYZ")
        K.ln(nt, geo.outputs["Normal"], nsep.inputs[0])
        wall = K.math_node(nt, "LESS_THAN", K.math_node(nt, "ABSOLUTE", nsep.outputs["Z"]), 0.5)
        u = K.math_node(nt, "DIVIDE", K.math_node(nt, "ADD", sep.outputs["X"], sep.outputs["Y"]), 2.6)
        v = K.math_node(nt, "DIVIDE", sep.outputs["Z"], FLOOR)
        fu, fv = K.math_node(nt, "FRACT", u), K.math_node(nt, "FRACT", v)
        win = K.math_node(nt, "MULTIPLY",
                          K.math_node(nt, "MULTIPLY", K.math_node(nt, "GREATER_THAN", fu, 0.18),
                                      K.math_node(nt, "LESS_THAN", fu, 0.82)),
                          K.math_node(nt, "MULTIPLY", K.math_node(nt, "GREATER_THAN", fv, 0.3),
                                      K.math_node(nt, "LESS_THAN", fv, 0.82)))
        win = K.math_node(nt, "MULTIPLY", win, K.math_node(nt, "MULTIPLY", wall,
                                                           K.math_node(nt, "GREATER_THAN", sep.outputs["Z"], 3.0)))
        bid = nt.nodes.new("ShaderNodeAttribute")
        bid.attribute_name = "bid"
        rnd = nt.nodes.new("ShaderNodeTexWhiteNoise")
        rnd.noise_dimensions = "1D"
        K.ln(nt, bid.outputs["Fac"], rnd.inputs["W"])
        cell = nt.nodes.new("ShaderNodeCombineXYZ")
        K.ln(nt, K.math_node(nt, "FLOOR", u), cell.inputs[0])
        K.ln(nt, K.math_node(nt, "FLOOR", v), cell.inputs[1])
        K.ln(nt, bid.outputs["Fac"], cell.inputs[2])
        wn = nt.nodes.new("ShaderNodeTexWhiteNoise")
        wn.noise_dimensions = "3D"
        K.ln(nt, cell.outputs[0], wn.inputs["Vector"])
        dark = nt.nodes.new("ShaderNodeAttribute")
        dark.attribute_name = "dark"
        lit_frac = K.math_node(nt, "MULTIPLY", ctx.ctl_node(nt, "lights", 0.6),
                               K.math_node(nt, "SUBTRACT", 1.0, dark.outputs["Fac"]))
        lit_frac = K.math_node(nt, "MULTIPLY", lit_frac,
                               K.math_node(nt, "SUBTRACT", 1.0, burn_attr_out(nt, K)))
        lit = K.math_node(nt, "LESS_THAN", wn.outputs["Value"], lit_frac)
        pal = nt.nodes.new("ShaderNodeValToRGB")
        K.ln(nt, rnd.outputs["Value"], pal.inputs[0])
        e = pal.color_ramp.elements
        pal.color_ramp.interpolation = "CONSTANT"
        e[0].position, e[0].color = 0.0, (0.80, 0.78, 0.74, 1)
        e[1].position, e[1].color = 0.8, (0.62, 0.66, 0.72, 1)
        for pos_, c_ in ((0.2, (0.72, 0.70, 0.66)), (0.4, (0.86, 0.84, 0.80)), (0.6, (0.56, 0.60, 0.64))):
            el = e.new(pos_)
            el.color = (*c_, 1)
        base = K.mix_rgb(nt, win, pal.outputs["Color"], (0.05, 0.07, 0.10))
        roof = K.math_node(nt, "GREATER_THAN", nsep.outputs["Z"], 0.5)
        base = K.mix_rgb(nt, roof, base, (0.35, 0.36, 0.38))
        burn = nt.nodes.new("ShaderNodeAttribute")
        burn.attribute_name = "burn"
        bn = nt.nodes.new("ShaderNodeTexNoise")
        bn.inputs["Scale"].default_value = 0.08
        K.ln(nt, geo.outputs["Position"], bn.inputs["Vector"])
        soot = K.mix_rgb(nt, bn.outputs["Fac"], (0.035, 0.03, 0.028), (0.16, 0.13, 0.11))
        base = K.mix_rgb(nt, burn.outputs["Fac"], base, soot)
        wc = K.mix_rgb(nt, wn.outputs["Color"], (1.0, 0.75, 0.45), (1.0, 0.92, 0.78))
        g = nt.nodes.new("ShaderNodeAttribute")
        g.attribute_name = "glow"
        gc = nt.nodes.new("ShaderNodeAttribute")
        gc.attribute_name = "gcol"
        win_e = K.mix_rgb(nt, 1.0, wc, K.math_node(nt, "MULTIPLY", K.math_node(nt, "MULTIPLY", win, lit), 3.2),
                          "MULTIPLY")
        gmask = K.math_node(nt, "MULTIPLY_ADD", win, 2.6, 0.25)   # 창문 위주로 빛남
        glow_e = K.mix_rgb(nt, 1.0, gc.outputs["Color"],
                           K.math_node(nt, "MULTIPLY", K.math_node(nt, "MULTIPLY", g.outputs["Fac"], 2.2), gmask),
                           "MULTIPLY")
        emis = K.mix_rgb(nt, 1.0, win_e, glow_e, "ADD")
        b = K.principled(nt, base, K.math_node(nt, "MULTIPLY_ADD", win, -0.65, 0.8), emit=emis, estr=1.0)
        K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
        m.cycles.emission_sampling = "NONE"
        return m

    def _farm(self, nt, col):
        """ctl 'farm'(0~1): 옛 논밭(이랑 줄무늬)으로 섞기."""
        K, ctx = self.K, self.ctx
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        K.ln(nt, geo.outputs["Position"], sep.inputs[0])
        rows = K.math_node(nt, "SINE", K.math_node(nt, "MULTIPLY", K.math_node(nt, "ADD", sep.outputs["X"],
                                                                                  K.math_node(nt, "MULTIPLY", sep.outputs["Y"], 0.35)), 0.9))
        fn = nt.nodes.new("ShaderNodeTexNoise")
        fn.inputs["Scale"].default_value = 0.004
        K.ln(nt, geo.outputs["Position"], fn.inputs["Vector"])
        field = K.mix_rgb(nt, K.math_node(nt, "GREATER_THAN", fn.outputs["Fac"], 0.5), (0.30, 0.42, 0.14), (0.42, 0.36, 0.20))
        field = K.mix_rgb(nt, K.math_node(nt, "MULTIPLY_ADD", rows, 0.12, 0.12), field, (0.18, 0.14, 0.08))
        return K.mix_rgb(nt, ctx.ctl_node(nt, "farm", 0.0), col, field)

    def _mat_ground(self):
        K = self.K
        m, nt, out = K.new_mat("m_city_ground")
        b = K.principled(nt, self._farm(nt, (0.30, 0.30, 0.31)), 0.9)
        K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
        return m

    def _mat_road(self):
        K = self.K
        m, nt, out = K.new_mat("m_jroad")
        rk = nt.nodes.new("ShaderNodeAttribute")
        rk.attribute_name = "rk"
        is_walk = K.math_node(nt, "COMPARE", rk.outputs["Fac"], 1.0)
        is_walk.node.inputs[2].default_value = 0.1
        col = K.mix_rgb(nt, is_walk, (0.06, 0.065, 0.075), (0.42, 0.40, 0.37))
        col = self._farm(nt, K.mix_rgb(nt, self.ctx.ctl_node(nt, "farm", 0.0), col, (0.36, 0.30, 0.20)))
        b = K.principled(nt, col, 0.85)
        K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
        return m

    def set_buildings(self, hscale=None, glow=None, gcol=None, dark=None, burn=None):
        """건물별(nb) 값 → 면/꼭짓점 속성."""
        g, me = self.g, self.b_mesh.data
        if hscale is not None:
            v = self.bv0.copy()
            v[:, 2] = g["bvz"] * np.asarray(hscale, np.float32)[g["bvid"]]
            me.vertices.foreach_set("co", v.ravel())
        fid = g["bfid"]
        if glow is not None:
            me.attributes["glow"].data.foreach_set("value", np.asarray(glow, np.float32)[fid])
        if dark is not None:
            me.attributes["dark"].data.foreach_set("value", np.asarray(dark, np.float32)[fid])
        if burn is not None:
            me.attributes["burn"].data.foreach_set("value", np.asarray(burn, np.float32)[fid])
        if gcol is not None:
            c = np.asarray(gcol, np.float32)
            c4 = np.c_[c, np.ones(len(c))][fid].astype(np.float32)
            me.attributes["gcol"].data.foreach_set("color", c4.ravel())
        me.update()

    def people(self, n, name="jpeople"):
        K, ctx = self.K, self.ctx
        poses = K.person_poses(ctx, K.mat_inst("m_jshirt", 0.75), K.mat_inst2("m_jpants"),
                               K.mat_simple("m_jskin", (0.86, 0.68, 0.55), 0.6),
                               K.mat_simple("m_jhair", (0.05, 0.04, 0.035), 0.6))
        return K.instancer_multi(ctx, name, poses, n)

    def cars(self, n, name="jcars"):
        K, ctx = self.K, self.ctx
        pc = K.proto_car(ctx, K.mat_inst("m_jcar", 0.35, coat=0.6), K.mat_simple("m_jglass", (0.05, 0.07, 0.1), 0.1),
                         K.mat_emit("m_jhead", (1.0, 0.95, 0.8), 6.0, ctx, "carlights"),
                         K.mat_emit("m_jtail", (1.0, 0.1, 0.05), 6.0, ctx, "carlights"))
        return K.instancer(ctx, name, pc, n)

    def light(self, t, keys):
        from .common import keyed
        lk = [(k, (v["elev"], v["az"], v["energy"], *v["col"], v["amb"], *v["amb_col"])) for k, v in keys]
        L = keyed(t, lk)
        self.sun.rotation_euler = (math.radians(90 - L[0]), 0, math.radians(L[1]))
        self.sun.data.energy = L[2]
        self.sun.data.color = L[3:6]
        self.ctx.set_ctl("ambient", L[6])
        self.ctx.set_rgb("ambient_col", L[7:10])
        return max(0.0, min(1.0, (0.3 - L[6]) / 0.2))
