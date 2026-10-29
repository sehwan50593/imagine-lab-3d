"""블록(복셀) 캐릭터·생활 공간 세트 (10-30 오너 기준 채널 방식: 사람 눈높이 근접 샷, 장면마다 짧은 사건).

- 캐릭터: 네모 머리·몸통·팔다리, 얼굴(눈·눈썹·입), 짧은/긴 머리 2종 × 자세 NPOSE개 → instancer_multi
  자세 번호 = 머리종류 * NPOSE + 자세. 셔츠 색 'col', 바지 색 'col2'. 앞 = +x, 원점 = 발바닥(누운 자세는 발끝).
- 세트: 바닥·벽은 타일(면마다 색 조금씩 다름 → 픽셀 질감), 가구는 상자. 빛나는 면(모니터·창·간판)은 따로 발광 메시.
  세트마다 떨어진 자리(offset)에 두고, 카메라가 장면마다 그 세트로 건너감.
"""
import math

import numpy as np

STAND, WALK_A, WALK_B, SIT, LIE, PHONE, ANGRY, CONFUSED, SIT_PHONE, SIT_CONF, TALK = range(11)
NPOSE = 11
POSES = {"stand": STAND, "walk_a": WALK_A, "walk_b": WALK_B, "sit": SIT, "lie": LIE, "phone": PHONE,
         "angry": ANGRY, "confused": CONFUSED, "sit_phone": SIT_PHONE, "sit_conf": SIT_CONF, "talk": TALK}
SKIN = (0.93, 0.74, 0.58)
HAIR = (0.11, 0.075, 0.055)
SHIRTS = [(0.25, 0.45, 0.80), (0.85, 0.30, 0.28), (0.95, 0.80, 0.35), (0.35, 0.65, 0.40), (0.92, 0.92, 0.90),
          (0.55, 0.38, 0.70), (0.30, 0.30, 0.34), (0.95, 0.55, 0.25), (0.45, 0.75, 0.85), (0.80, 0.55, 0.65)]
PANTS = [(0.15, 0.18, 0.30), (0.20, 0.20, 0.22), (0.35, 0.28, 0.20), (0.45, 0.50, 0.60), (0.12, 0.12, 0.13)]


# ───────────────────────── 캐릭터 ─────────────────────────
def _rot_y(bm, ang, pivot):
    c, s = math.cos(ang), math.sin(ang)
    for v in bm.verts:
        x, z = v.co.x - pivot[0], v.co.z - pivot[2]
        v.co.x, v.co.z = pivot[0] + c * x + s * z, pivot[2] - s * x + c * z
    return bm


def _shift(bm, dx=0.0, dy=0.0, dz=0.0):
    for v in bm.verts:
        v.co.x += dx
        v.co.y += dy
        v.co.z += dz
    return bm


def _person(pose, long_hair):
    """[(bmesh, 재질번호)] — 0 셔츠 · 1 바지 · 2 피부 · 3 머리카락 · 4 흰자 · 5 검정 · 6 입 · 7 화면."""
    from . import bkit as K

    def box(cx, cy, z0, sx, sy, sz):
        return K.bm_cube(sx, sy, sz, (cx, cy, z0), bottom=True)
    sit = pose in (SIT, SIT_PHONE, SIT_CONF)
    hip = 0.47 if sit else 0.78
    up = hip - 0.78                     # 윗몸 높이 보정
    P = []
    # 다리
    if sit:
        for sy in (-0.11, 0.11):
            P += [(box(0.2, sy, hip - 0.11, 0.46, 0.2, 0.22), 1), (box(0.36, sy, 0.08, 0.2, 0.2, hip - 0.19), 1),
                  (box(0.39, sy, 0.0, 0.26, 0.2, 0.09), 5)]
    else:
        swing = {WALK_A: 0.42, WALK_B: -0.42}.get(pose, 0.0)
        for sy, sg in ((-0.11, 1), (0.11, -1)):
            leg = box(0, sy, 0.09, 0.22, 0.2, hip - 0.09)
            shoe = box(0.03, sy, 0.0, 0.27, 0.2, 0.09)
            P += [(_rot_y(leg, sg * swing, (0, 0, hip)), 1), (_rot_y(shoe, sg * swing, (0, 0, hip)), 5)]
    # 몸통·머리
    P.append((box(0, 0, hip, 0.3, 0.52, 0.58), 0))
    hz = hip + 0.58
    P.append((box(0, 0, hz, 0.46, 0.46, 0.46), 2))
    fx = 0.232
    closed = pose == LIE
    for sy in (-0.1, 0.1):
        if closed:
            P.append((box(fx, sy, hz + 0.17, 0.02, 0.11, 0.025), 5))
        else:
            P.append((box(fx, sy, hz + 0.13, 0.02, 0.11, 0.1), 4))
            P.append((box(fx + 0.006, sy - 0.018 * np.sign(sy), hz + 0.14, 0.02, 0.06, 0.075), 5))
        brow_z = hz + (0.245 if pose == ANGRY else 0.27)
        P.append((box(fx + 0.004, sy, brow_z, 0.02, 0.13, 0.03), 3))
    open_mouth = pose in (ANGRY, TALK)
    P.append((box(fx, 0, hz + (0.04 if open_mouth else 0.065), 0.02, 0.13 if open_mouth else 0.12,
                  0.07 if open_mouth else 0.028), 6))
    # 머리카락
    P.append((box(-0.02, 0, hz + 0.37, 0.5, 0.5, 0.13), 3))
    P.append((box(0.215, 0, hz + 0.35, 0.07, 0.5, 0.07), 3))      # 앞머리
    if long_hair:
        P.append((box(-0.24, 0, hz - 0.42, 0.1, 0.54, 0.92), 3))
        for sy in (-0.255, 0.255):
            P.append((box(-0.02, sy, hz - 0.2, 0.44, 0.05, 0.7), 3))
    else:
        P.append((box(-0.24, 0, hz + 0.08, 0.08, 0.5, 0.36), 3))
        for sy in (-0.245, 0.245):
            P.append((box(-0.08, sy, hz + 0.22, 0.3, 0.04, 0.22), 3))
    # 팔: 어깨 회전 (음수 = 앞으로 듦)
    arms = {SIT: (-0.6, -0.6), SIT_PHONE: (-1.05, -0.6), SIT_CONF: (-2.75, -0.6), PHONE: (-1.05, 0.0),
            ANGRY: (-2.5, -2.5), CONFUSED: (-2.75, 0.05), TALK: (-0.9, 0.05),
            WALK_A: (0.35, -0.35), WALK_B: (-0.35, 0.35)}.get(pose, (0.0, 0.0))
    for sy, ang in ((-0.34, arms[0]), (0.34, arms[1])):
        sleeve = box(0, sy, hip + 0.12, 0.18, 0.16, 0.46)
        hand = box(0, sy, hip - 0.02, 0.17, 0.15, 0.14)
        piv = (0, 0, hip + 0.54)
        P += [(_rot_y(sleeve, ang, piv), 0), (_rot_y(hand, ang, piv), 2)]
    if pose in (PHONE, SIT_PHONE):
        P.append((box(0.47, -0.27, hip + 0.18 + 0.0, 0.03, 0.11, 0.18), 5))
        P.append((box(0.452, -0.27, hip + 0.19, 0.012, 0.09, 0.15), 7))
    if pose == LIE:   # 선 모습을 뒤로 눕힘: 발끝이 원점, 머리는 -x, 얼굴은 위
        for bm, _ in P:
            _rot_y(bm, -math.pi / 2, (0, 0, 0))
            _shift(bm, dz=0.24)
    return P


def people_protos(ctx, mats):
    from . import bkit as K
    out = []
    for lh in (False, True):
        for p in range(NPOSE):
            out.append(K.proto(ctx, f"p_vox_{int(lh)}_{p:02d}", K.join_bms(_person(p, lh)), mats))
    return out


def people_mats():
    from . import bkit as K
    return [K.mat_inst("m_vshirt", 0.8), K.mat_inst2("m_vpants", rough=0.85),
            K.mat_simple("m_vskin", SKIN, 0.7), K.mat_simple("m_vhair", HAIR, 0.8),
            K.mat_simple("m_vwhite", (0.96, 0.96, 0.96), 0.4), K.mat_simple("m_vblack", (0.015, 0.015, 0.02), 0.4),
            K.mat_simple("m_vmouth", (0.42, 0.10, 0.10), 0.6),
            K.mat_emit("m_vscreen", (0.6, 0.85, 1.0), 3.0)]


# ───────────────────────── 세트 만들기 ─────────────────────────
class Vox:
    """상자·타일을 모아 두 메시(일반·발광)로 만듦. 좌표는 세트 기준 + offset."""

    def __init__(self, seed=0):
        self.rs = np.random.default_rng(seed)
        self.o = np.zeros(3)
        self.solid = ([], [], [])
        self.glow = ([], [], [])
        self.lights = []

    def at(self, x, y, z=0.0):
        self.o = np.array((x, y, z), float)
        return self

    def _jit(self, col, j):
        return tuple(float(np.clip(c * (1 + j * self.rs.normal()), 0, 1)) for c in col)

    def _quad(self, dst, pts, col):
        V, F, C = dst
        b = len(V)
        V.extend(tuple(p + self.o) for p in pts)
        F.append([b, b + 1, b + 2, b + 3])
        C.append((*col, 1.0))

    def box(self, x0, x1, y0, y1, z0, z1, col, jit=0.04, glow=False, bottom=False):
        dst = self.glow if glow else self.solid
        c = self._jit(col, jit) if jit else tuple(col)
        p = np.array
        q = [p((x0, y0, z1)), p((x1, y0, z1)), p((x1, y1, z1)), p((x0, y1, z1))]
        b = [p((x0, y0, z0)), p((x1, y0, z0)), p((x1, y1, z0)), p((x0, y1, z0))]
        sh = lambda k: tuple(min(1.0, v * k) for v in c)   # 옆면은 조금 어둡게 (블록 느낌)
        self._quad(dst, q, c)
        self._quad(dst, [b[0], b[1], q[1], q[0]], sh(0.9))
        self._quad(dst, [b[1], b[2], q[2], q[1]], sh(0.84))
        self._quad(dst, [b[2], b[3], q[3], q[2]], sh(0.9))
        self._quad(dst, [b[3], b[0], q[0], q[3]], sh(0.84))
        if bottom:
            self._quad(dst, [b[3], b[2], b[1], b[0]], sh(0.7))

    def tiles(self, p0, du, dv, nu, nv, colfn, glow=False):
        """p0에서 du·dv 방향으로 nu×nv 타일 (면 하나씩). colfn(i, j) → 색."""
        dst = self.glow if glow else self.solid
        p0, du, dv = (np.array(v, float) for v in (p0, du, dv))
        for i in range(nu):
            for j in range(nv):
                a = p0 + du * i + dv * j
                self._quad(dst, [a, a + du, a + du + dv, a + dv], colfn(i, j))

    def floor(self, x0, x1, y0, y1, col, tile=0.5, kind="plain", z=0.0):
        nu, nv = int(round((x1 - x0) / tile)), int(round((y1 - y0) / tile))

        def fn(i, j):
            if kind == "wood":   # 긴 널빤지: 줄마다 이음새 위치가 다름
                k = (i + 3 * (j % 3)) // 4
                g = 1 + 0.10 * math.sin(k * 12.9898 + j * 78.233)
            elif kind == "check":
                g = 1.0 if (i + j) % 2 else 0.86
            else:
                g = 1.0
            return self._jit(tuple(c * g for c in col), 0.05)
        self.tiles((x0, y0, z), ((x1 - x0) / nu, 0, 0), (0, (y1 - y0) / nv, 0), nu, nv, fn)

    def wall(self, a, b, z0, z1, col, tile=0.5, face=1, kind="plain"):
        """a=(x,y)→b=(x,y) 수직 벽 한 면. face=+1이면 왼쪽(진행 방향 기준)으로 향함."""
        a, b = np.array(a, float), np.array(b, float)
        L = float(np.linalg.norm(b - a))
        nu, nv = max(1, int(round(L / tile))), max(1, int(round((z1 - z0) / tile)))
        du = np.r_[(b - a) / nu, 0]
        dv = np.array((0, 0, (z1 - z0) / nv))
        p0 = np.r_[a, z0]
        if face < 0:
            p0, du = np.r_[b, z0], -du

        def fn(i, j):
            g = 1.0
            if kind == "brick":
                g = 1.0 if (i + (j % 2)) % 2 else 0.9
            if j == 0:
                g *= 0.75           # 걸레받이
            return self._jit(tuple(c * g for c in col), 0.04)
        self.tiles(p0, du, dv, nu, nv, fn)

    def window(self, x0, x1, y, z0, z1, night=True, lights=14, face=-1, axis="y"):
        """밤 창문: 남색 발광판 + 먼 건물 불빛 점 + 흰 창틀. axis='y'면 y=상수 벽, 'x'면 x=상수 벽(x0,x1을 y로)."""
        rs = self.rs
        base = (0.03, 0.05, 0.13) if night else (0.55, 0.75, 0.95)

        def B(a0, a1, b0, b1, c0, c1, col, **kw):
            if axis == "y":
                self.box(a0, a1, b0, b1, c0, c1, col, **kw)
            else:
                self.box(b0, b1, a0, a1, c0, c1, col, **kw)
        d = 0.02 * face
        B(x0, x1, min(y, y + d), max(y, y + d), z0, z1, base, jit=0, glow=True)
        for _ in range(lights if night else 0):
            u = rs.uniform(x0 + 0.08, x1 - 0.12)
            v = rs.uniform(z0 + 0.05, z0 + (z1 - z0) * 0.55)
            c = (1.0, 0.78, 0.4) if rs.random() < 0.75 else (0.7, 0.85, 1.0)
            B(u, u + 0.06, min(y + d, y + 2 * d), max(y + d, y + 2 * d), v, v + 0.06, c, jit=0, glow=True)
        fr = (0.95, 0.95, 0.93)
        t = 0.06
        for a0, a1, c0, c1 in ((x0 - t, x1 + t, z0 - t, z0), (x0 - t, x1 + t, z1, z1 + t),
                               (x0 - t, x0, z0, z1), (x1, x1 + t, z0, z1), ((x0 + x1) / 2 - t / 2, (x0 + x1) / 2 + t / 2, z0, z1)):
            B(a0, a1, min(y, y + 3 * d), max(y, y + 3 * d), c0, c1, fr)

    def light(self, x, y, z, energy, col=(1.0, 0.85, 0.65), radius=0.4, name=""):
        self.lights.append(((x + self.o[0], y + self.o[1], z + self.o[2]), energy, col, radius, name))

    def build(self, ctx, glow_strength=3.0):
        from . import bkit as K
        import bpy
        obs = {}
        for key, dst in (("solid", self.solid), ("glow", self.glow)):
            V, F, C = dst
            if not F:
                continue
            m, nt, out = K.new_mat("m_vox_" + key)
            a = nt.nodes.new("ShaderNodeAttribute")
            a.attribute_name = "fcol"
            if key == "solid":
                b = K.principled(nt, a.outputs["Color"], 0.82, spec=0.3)
                K.ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
            else:
                e = nt.nodes.new("ShaderNodeEmission")
                K.ln(nt, a.outputs["Color"], e.inputs["Color"])
                K.ln(nt, ctx.ctl_node(nt, "glow", glow_strength), e.inputs["Strength"])
                K.ln(nt, e.outputs[0], out.inputs["Surface"])
                m.cycles.emission_sampling = "NONE"
            me = bpy.data.meshes.new("vox_" + key)
            me.from_pydata(V, [], F)
            me.attributes.new("fcol", "FLOAT_COLOR", "FACE").data.foreach_set(
                "color", np.asarray(C, np.float32).ravel())
            me.materials.append(m)
            obs[key] = K.link(bpy.data.objects.new("vox_" + key, me))
        lights = {}
        for i, (loc, en, col, rad, name) in enumerate(self.lights):
            ob = K.point_light(ctx, loc, energy=en, color=col, radius=rad, name=name or f"vl_{i}")
            lights[name or f"vl_{i}"] = ob
        return obs, lights


# ───────────────────────── 가구 ─────────────────────────
WOOD = (0.62, 0.42, 0.25)
DARKWOOD = (0.38, 0.25, 0.15)
WHITE = (0.92, 0.92, 0.90)
GREYC = (0.55, 0.56, 0.58)


def table(v, cx, cy, sx, sy, h, col=WOOD):
    v.box(cx - sx / 2, cx + sx / 2, cy - sy / 2, cy + sy / 2, h - 0.05, h, col)
    for dx in (-1, 1):
        for dy in (-1, 1):
            x, y = cx + dx * (sx / 2 - 0.05), cy + dy * (sy / 2 - 0.05)
            v.box(x - 0.03, x + 0.03, y - 0.03, y + 0.03, 0, h - 0.05, col)


def chair(v, cx, cy, face_deg, col=DARKWOOD, h=0.45):
    v.box(cx - 0.22, cx + 0.22, cy - 0.22, cy + 0.22, h - 0.05, h, col)
    for dx in (-1, 1):
        for dy in (-1, 1):
            v.box(cx + dx * 0.18 - 0.025, cx + dx * 0.18 + 0.025, cy + dy * 0.18 - 0.025, cy + dy * 0.18 + 0.025,
                  0, h - 0.05, col)
    a = math.radians(face_deg)   # 등받이는 앉는 사람 뒤쪽
    bx, by = cx - 0.2 * math.cos(a), cy - 0.2 * math.sin(a)
    if abs(math.cos(a)) > 0.5:
        v.box(bx - 0.03, bx + 0.03, cy - 0.22, cy + 0.22, h, h + 0.45, col)
    else:
        v.box(cx - 0.22, cx + 0.22, by - 0.03, by + 0.03, h, h + 0.45, col)


def monitor(v, cx, cy, z, face_deg, w=0.55):
    """책상 위 모니터: 화면(발광)이 face_deg 쪽을 봄."""
    a = math.radians(face_deg)
    fx, fy = math.cos(a), math.sin(a)
    if abs(fx) > 0.5:
        v.box(cx - 0.03, cx + 0.03, cy - w / 2, cy + w / 2, z + 0.12, z + 0.47, (0.08, 0.08, 0.09))
        v.box(cx + fx * 0.031 - 0.004, cx + fx * 0.031 + 0.004, cy - w / 2 + 0.03, cy + w / 2 - 0.03, z + 0.15,
              z + 0.44, (0.55, 0.78, 1.0), jit=0, glow=True)
    else:
        v.box(cx - w / 2, cx + w / 2, cy - 0.03, cy + 0.03, z + 0.12, z + 0.47, (0.08, 0.08, 0.09))
        v.box(cx - w / 2 + 0.03, cx + w / 2 - 0.03, cy + fy * 0.031 - 0.004, cy + fy * 0.031 + 0.004, z + 0.15,
              z + 0.44, (0.55, 0.78, 1.0), jit=0, glow=True)
    v.box(cx - 0.05, cx + 0.05, cy - 0.05, cy + 0.05, z, z + 0.12, (0.1, 0.1, 0.1))


def bed(v, x0, x1, y0, y1, blanket=(0.35, 0.5, 0.82), head="+y"):
    v.box(x0, x1, y0, y1, 0, 0.32, WOOD)
    v.box(x0 + 0.03, x1 - 0.03, y0 + 0.03, y1 - 0.03, 0.32, 0.52, WHITE, jit=0.02)
    L = y1 - y0
    if head == "+y":
        v.box(x0 + 0.02, x1 - 0.02, y0 + 0.02, y0 + 0.62 * L, 0.52, 0.6, blanket)
        v.box(x0 + 0.15, x1 - 0.15, y1 - 0.42, y1 - 0.08, 0.52, 0.64, (0.97, 0.97, 0.97), jit=0.01)
        v.box(x0, x1, y1 - 0.06, y1, 0, 1.0, DARKWOOD)
    else:
        v.box(x0 + 0.02, x1 - 0.02, y1 - 0.62 * L, y1 - 0.02, 0.52, 0.6, blanket)
        v.box(x0 + 0.15, x1 - 0.15, y0 + 0.08, y0 + 0.42, 0.52, 0.64, (0.97, 0.97, 0.97), jit=0.01)
        v.box(x0, x1, y0, y0 + 0.06, 0, 1.0, DARKWOOD)


def shelf(v, x0, x1, y0, y1, h, rows=4, seed_cols=None):
    """편의점 진열대: 칸마다 알록달록한 상품 블록."""
    v.box(x0, x1, y0, y1, 0, 0.1, GREYC)
    v.box(x0 + (x1 - x0) * 0.4, x1 - (x1 - x0) * 0.4, y0, y1, 0.1, h, (0.7, 0.72, 0.75))
    cols = seed_cols or [(0.9, 0.25, 0.2), (0.95, 0.75, 0.2), (0.25, 0.55, 0.9), (0.3, 0.75, 0.35),
                         (0.95, 0.55, 0.75), (0.95, 0.95, 0.92), (0.6, 0.35, 0.2)]
    for r in range(rows):
        z = 0.12 + r * (h - 0.15) / rows
        v.box(x0, x1, y0, y1, z, z + 0.03, (0.8, 0.8, 0.82))
        y = y0 + 0.04
        while y < y1 - 0.12:
            w = v.rs.uniform(0.08, 0.16)
            hh = v.rs.uniform(0.12, (h - 0.15) / rows - 0.06)
            c = cols[int(v.rs.integers(len(cols)))]
            for side in ((x0 + 0.02, x0 + (x1 - x0) * 0.38), (x1 - (x1 - x0) * 0.38, x1 - 0.02)):
                v.box(side[0], side[1], y, y + w, z + 0.03, z + 0.03 + hh, c, jit=0.08)
            y += w + 0.015


def tree(v, x, y, h=3.2):
    v.box(x - 0.15, x + 0.15, y - 0.15, y + 0.15, 0, h * 0.5, (0.42, 0.28, 0.16))
    for dz, r, c in ((0.45, 0.9, (0.22, 0.5, 0.2)), (0.75, 0.7, (0.26, 0.58, 0.24)), (0.95, 0.45, (0.3, 0.62, 0.26))):
        v.box(x - r, x + r, y - r, y + r, h * dz, h * dz + 0.6, c, jit=0.08)


def street_lamp(v, x, y, h=4.2, energy=200.0):
    v.box(x - 0.06, x + 0.06, y - 0.06, y + 0.06, 0, h, (0.25, 0.26, 0.28))
    v.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, h, h + 0.12, (0.25, 0.26, 0.28))
    v.box(x - 0.16, x + 0.16, y - 0.16, y + 0.16, h - 0.05, h, (1.0, 0.85, 0.55), jit=0, glow=True)
    v.light(x, y, h - 0.3, energy, (1.0, 0.8, 0.55), 0.3)


def storefront(v, x0, x1, y, depth, h, sign_col, face=-1, rs=None, lit=0.6):
    """길가 건물: 1층 가게(유리 불빛·간판) + 위층 창문 격자. face=-1이면 -y 쪽(길)을 봄."""
    rs = rs or v.rs
    yb = y + (depth if face < 0 else -depth)
    walls = [(0.62, 0.36, 0.3), (0.42, 0.45, 0.55), (0.66, 0.58, 0.45), (0.5, 0.42, 0.36), (0.38, 0.5, 0.45)]
    v.box(x0, x1, min(y, yb), max(y, yb), 0, h, walls[int(rs.integers(len(walls)))], jit=0.03)
    f = y + 0.03 * face
    v.box(x0 + 0.3, x1 - 0.3, min(y, f), max(y, f), 0.25, 2.6, (0.62, 0.5, 0.34), jit=0, glow=True)
    v.box(x0 + 0.2, x1 - 0.2, min(y, y + 0.12 * face), max(y, y + 0.12 * face), 2.8, 3.5, tuple(c * 0.7 for c in sign_col), jit=0, glow=True)
    nx = max(1, int((x1 - x0) / 1.6))
    for k in range(int((h - 4.2) / 2.6)):
        z = 4.2 + k * 2.6
        for i in range(nx):
            xx = x0 + (i + 0.5) * (x1 - x0) / nx
            on = rs.random() < lit
            c = (0.75, 0.58, 0.32) if on else (0.05, 0.06, 0.09)
            v.box(xx - 0.45, xx + 0.45, min(y, f), max(y, f), z, z + 1.3, c, jit=0, glow=on)


def brain_voxels(cell=0.2, R=(2.0, 1.6, 1.35), seed=5):
    """뇌 모양 겉껍질 블록: 반구 사이 홈 + 주름(줄무늬 잡음). [(x, y, z, 색)]"""
    rs = np.random.default_rng(seed)
    n = [int(math.ceil(r / cell)) + 1 for r in R]
    xs, ys, zs = (np.arange(-k, k + 1) * cell for k in n)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    inside = (X / R[0]) ** 2 + (Y / R[1]) ** 2 + ((Z + 0.15 * (X / R[0]) ** 2) / R[2]) ** 2 <= 1.0
    inside &= ~((np.abs(Y) < cell * 0.6) & (Z > -0.2))     # 좌우 반구 사이 홈
    inside &= Z > -R[2] * 0.75
    sh = np.zeros_like(inside)
    for ax in range(3):
        for d in (-1, 1):
            sh |= ~np.roll(inside, d, ax)
    surf = inside & sh
    out = []
    ph = rs.uniform(0, 6, 3)
    for x, y, z in zip(X[surf], Y[surf], Z[surf]):
        g = math.sin(3.1 * x + ph[0] + 2.2 * math.sin(2.3 * z + ph[1])) * math.sin(2.7 * z + 1.7 * y + ph[2])
        c = (0.93, 0.55, 0.62) if g > -0.15 else (0.72, 0.36, 0.45)
        out.append((x, y, z, c))
    return out
