"""Blender 장면 도구 모음 (Blender 4.2 LTS, Cycles). blender_main.py 안에서만 import."""
import math

import bmesh
import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Euler, Vector


# ───────────────────────── 기본 ─────────────────────────
class Ctx:
    def __init__(self, sim, args, build_dir):
        self.sim = sim
        self.args = args
        self.build_dir = build_dir
        self.scene = bpy.context.scene
        self.updaters = []
        self.anchor_fns = {}
        self.ctl = {}          # 이름 → (노드 소켓 목록)
        self.proto = bpy.data.collections.new("_proto")
        self.scene.collection.children.link(self.proto)
        self.proto.hide_render = True
        self.proto.hide_viewport = True

    def on_frame(self, fn):
        self.updaters.append(fn)
        return fn

    def anchor(self, key, fn):
        self.anchor_fns[key] = fn

    def set_ctl(self, name, value):
        for sock in self.ctl.get(name, []):
            sock.default_value = value

    def ctl_node(self, nt, name, value=0.0):
        n = nt.nodes.new("ShaderNodeValue")
        n.outputs[0].default_value = value
        n.label = name
        self.ctl.setdefault(name, []).append(n.outputs[0])
        return n.outputs[0]

    def anchors(self, t):
        cam = self.scene.camera
        out = {}
        for k, fn in self.anchor_fns.items():
            p = fn(t)
            if p is None:
                continue
            v = world_to_camera_view(self.scene, cam, Vector(p))
            vis = 1 if (v.z > 0 and -0.1 <= v.x <= 1.1 and -0.1 <= v.y <= 1.1) else 0
            out[k] = [round(v.x, 5), round(v.y, 5), round(v.z, 3), vis]
        return out


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def link(obj, coll=None):
    (coll or bpy.context.scene.collection).objects.link(obj)
    return obj


def mesh_obj(name, bm, mat=None, coll=None, smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    if mat:
        me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    return link(ob, coll)


def join_bms(parts):
    """[(bmesh, material_index)] → 하나의 bmesh."""
    out = bmesh.new()
    for bm, mi in parts:
        me = bpy.data.meshes.new("_tmp")
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.material_index = mi
        out.from_mesh(me)
        bpy.data.meshes.remove(me)
    return out


def bm_cube(sx=1, sy=1, sz=1, loc=(0, 0, 0), bottom=False):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = v.co.x * sx + loc[0]
        v.co.y = v.co.y * sy + loc[1]
        v.co.z = (v.co.z + (0.5 if bottom else 0)) * sz + loc[2]
    return bm


def bm_sphere(r=1, loc=(0, 0, 0), seg=16, rings=8, scale=(1, 1, 1), uv=False):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r, calc_uvs=uv)
    for v in bm.verts:
        v.co.x = v.co.x * scale[0] + loc[0]
        v.co.y = v.co.y * scale[1] + loc[1]
        v.co.z = v.co.z * scale[2] + loc[2]
    return bm


def bm_cone(r1, r2, depth, loc=(0, 0, 0), seg=12):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2, depth=depth)
    for v in bm.verts:
        v.co.x += loc[0]
        v.co.y += loc[1]
        v.co.z += loc[2] + depth / 2
    return bm


def bm_ico(r=1, loc=(0, 0, 0), sub=1, scale=(1, 1, 1)):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    for v in bm.verts:
        v.co.x = v.co.x * scale[0] + loc[0]
        v.co.y = v.co.y * scale[1] + loc[1]
        v.co.z = v.co.z * scale[2] + loc[2]
    return bm


# ───────────────────────── 재질 ─────────────────────────
def new_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, out


def nn(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items():
        setattr(n, k, v)
    return n


def ln(nt, a, b):
    nt.links.new(a, b)


def math_node(nt, op, a=None, b=None, c=None, clamp=False):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = op
    n.use_clamp = clamp
    for i, v in enumerate((a, b, c)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            n.inputs[i].default_value = v
        else:
            ln(nt, v, n.inputs[i])
    return n.outputs[0]


def mix_rgb(nt, fac, c1, c2, blend="MIX"):
    n = nt.nodes.new("ShaderNodeMixRGB")
    n.blend_type = blend
    for sock, v in ((n.inputs["Fac"], fac), (n.inputs["Color1"], c1), (n.inputs["Color2"], c2)):
        if isinstance(v, (int, float)):
            sock.default_value = v
        elif isinstance(v, tuple):
            sock.default_value = (*v[:3], 1.0)
        else:
            ln(nt, v, sock)
    return n.outputs["Color"]


def rgb(nt, c):
    n = nt.nodes.new("ShaderNodeRGB")
    n.outputs[0].default_value = (*c[:3], 1.0)
    return n.outputs[0]


def principled(nt, color, rough=0.6, metal=0.0, emit=None, estr=0.0, coat=0.0, spec=0.5):
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    if isinstance(color, tuple):
        b.inputs["Base Color"].default_value = (*color[:3], 1.0)
    else:
        ln(nt, color, b.inputs["Base Color"])
    if isinstance(rough, (int, float)):
        b.inputs["Roughness"].default_value = rough
    else:
        ln(nt, rough, b.inputs["Roughness"])
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    if coat:
        b.inputs["Coat Weight"].default_value = coat
    if emit is not None:
        if isinstance(emit, tuple):
            b.inputs["Emission Color"].default_value = (*emit[:3], 1.0)
        else:
            ln(nt, emit, b.inputs["Emission Color"])
        if isinstance(estr, (int, float)):
            b.inputs["Emission Strength"].default_value = estr
        else:
            ln(nt, estr, b.inputs["Emission Strength"])
    return b


def mat_simple(name, color, rough=0.6, metal=0.0, emit=None, estr=0.0, coat=0.0):
    m, nt, out = new_mat(name)
    b = principled(nt, color, rough, metal, emit, estr, coat)
    ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    if emit is not None:
        m.cycles.emission_sampling = "NONE"
    return m


def mat_emit(name, color, strength=5.0, ctx=None, ctl=None, sample=False):
    m, nt, out = new_mat(name)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*color[:3], 1.0)
    if ctx and ctl:
        s = math_node(nt, "MULTIPLY", ctx.ctl_node(nt, ctl, 1.0), strength)
        ln(nt, s, e.inputs["Strength"])
    else:
        e.inputs["Strength"].default_value = strength
    ln(nt, e.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "FRONT" if sample else "NONE"
    return m


def inst_attr(nt, name, kind="Color"):
    a = nt.nodes.new("ShaderNodeAttribute")
    a.attribute_type = "INSTANCER"
    a.attribute_name = name
    return a.outputs[kind]


def mat_inst(name, rough=0.55, emit_attr=None, emit_color=(1, 0.8, 0.5), emit_strength=6.0, coat=0.0):
    """인스턴스별 색('col' 속성)을 쓰는 재질."""
    m, nt, out = new_mat(name)
    c = inst_attr(nt, "col")
    if emit_attr:
        e = math_node(nt, "MULTIPLY", inst_attr(nt, emit_attr, "Fac"), emit_strength)
        b = principled(nt, c, rough, emit=emit_color, estr=e, coat=coat)
        m.cycles.emission_sampling = "NONE"
    else:
        b = principled(nt, c, rough, coat=coat)
    ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    return m


# ───────────────────────── 월드(우주 배경) ─────────────────────────
def world_space(ctx, ambient=(0.30, 0.36, 0.55), ambient_strength=0.35, ground=(0.05, 0.05, 0.08)):
    """조명용 월드. 카메라에 보이는 배경(남색 그라데이션+별)은 post.py에서 그림 (film_transparent)."""
    w = bpy.data.worlds.new("World")
    ctx.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ln(nt, tc.outputs["Generated"], sep.inputs[0])
    up = math_node(nt, "MULTIPLY_ADD", sep.outputs["Z"], 0.5, 0.5, clamp=True)
    col = mix_rgb(nt, up, ground, ambient)
    bg = nt.nodes.new("ShaderNodeBackground")
    ln(nt, col, bg.inputs["Color"])
    ln(nt, ctx.ctl_node(nt, "ambient", ambient_strength), bg.inputs["Strength"])
    ln(nt, bg.outputs[0], out.inputs["Surface"])
    return w


def sun(ctx, energy=3.0, color=(1.0, 0.92, 0.8), rot=(50, 0, 35), angle=6.0, name="Sun"):
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy = energy
    ld.color = color
    ld.angle = math.radians(angle)
    ob = link(bpy.data.objects.new(name, ld))
    ob.rotation_euler = Euler([math.radians(a) for a in rot])
    return ob


def point_light(ctx, loc, energy=200, color=(1, 0.8, 0.6), radius=0.3, name="Point"):
    ld = bpy.data.lights.new(name, "POINT")
    ld.energy = energy
    ld.color = color
    ld.shadow_soft_size = radius
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    return ob


# ───────────────────────── 카메라 ─────────────────────────
class CamRig:
    """궤도형 카메라: 목표점 기준 방위각·고도각·거리로 지정."""

    def __init__(self, ctx, lens=35.0, fstop=4.0):
        cd = bpy.data.cameras.new("Cam")
        cd.lens = lens
        cd.clip_start = 0.05
        cd.clip_end = 5000
        cd.sensor_fit = "VERTICAL"
        cd.sensor_height = 24.0
        cd.dof.use_dof = fstop > 0
        cd.dof.aperture_fstop = max(fstop, 0.5)
        self.ob = link(bpy.data.objects.new("Cam", cd))
        ctx.scene.camera = self.ob

    def set(self, target, az, el, dist, lens=None, focus=None, roll=0.0):
        t = Vector(target)
        a, e = math.radians(az), math.radians(el)
        loc = t + Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))) * dist
        self.ob.location = loc
        q = (t - loc).to_track_quat("-Z", "Y")
        self.ob.rotation_euler = q.to_euler()
        if roll:
            self.ob.rotation_euler.rotate_axis("Z", math.radians(roll))
        if lens:
            self.ob.data.lens = lens
        self.ob.data.dof.focus_distance = focus if focus else (t - loc).length


# ───────────────────────── 인스턴스(군집) ─────────────────────────
def instancer(ctx, name, proto, n, vector_scale=False):
    """점 n개에 proto를 복제. 점 속성: scale(float) 또는 size(vec3), rot(vec3), col(color), 추가 float들."""
    me = bpy.data.meshes.new(name)
    me.vertices.add(n)
    me.attributes.new("scale", "FLOAT", "POINT")
    me.attributes.new("size", "FLOAT_VECTOR", "POINT")
    me.attributes.new("rot", "FLOAT_VECTOR", "POINT")
    me.attributes.new("col", "FLOAT_COLOR", "POINT")
    ob = link(bpy.data.objects.new(name, me))
    ng = bpy.data.node_groups.new(name + "_gn", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    gi = ng.nodes.new("NodeGroupInput")
    go = ng.nodes.new("NodeGroupOutput")
    sc = ng.nodes.new("GeometryNodeInputNamedAttribute")
    sc.data_type = "FLOAT"
    sc.inputs["Name"].default_value = "scale"
    cmp = ng.nodes.new("FunctionNodeCompare")
    cmp.data_type = "FLOAT"
    cmp.operation = "LESS_THAN"
    ng.links.new(sc.outputs["Attribute"], cmp.inputs[0])
    cmp.inputs[1].default_value = 1e-4
    dl = ng.nodes.new("GeometryNodeDeleteGeometry")
    dl.domain = "POINT"
    ng.links.new(gi.outputs[0], dl.inputs["Geometry"])
    ng.links.new(cmp.outputs[0], dl.inputs["Selection"])
    iop = ng.nodes.new("GeometryNodeInstanceOnPoints")
    ng.links.new(dl.outputs[0], iop.inputs["Points"])
    oi = ng.nodes.new("GeometryNodeObjectInfo")
    oi.inputs["Object"].default_value = proto
    ng.links.new(oi.outputs["Geometry"], iop.inputs["Instance"])
    rt = ng.nodes.new("GeometryNodeInputNamedAttribute")
    rt.data_type = "FLOAT_VECTOR"
    rt.inputs["Name"].default_value = "rot"
    ng.links.new(rt.outputs["Attribute"], iop.inputs["Rotation"])
    if vector_scale:
        sz = ng.nodes.new("GeometryNodeInputNamedAttribute")
        sz.data_type = "FLOAT_VECTOR"
        sz.inputs["Name"].default_value = "size"
        mul = ng.nodes.new("ShaderNodeVectorMath")
        mul.operation = "SCALE"
        ng.links.new(sz.outputs["Attribute"], mul.inputs[0])
        ng.links.new(sc.outputs["Attribute"], mul.inputs["Scale"])
        ng.links.new(mul.outputs[0], iop.inputs["Scale"])
    else:
        ng.links.new(sc.outputs["Attribute"], iop.inputs["Scale"])
    ng.links.new(iop.outputs["Instances"], go.inputs[0])
    mod = ob.modifiers.new("GN", "NODES")
    mod.node_group = ng
    return ob


def add_attr(ob, name, kind="FLOAT"):
    ob.data.attributes.new(name, kind, "POINT")


def set_points(ob, pos, scale=None, rot=None, col=None, size=None, **floats):
    me = ob.data
    n = len(me.vertices)
    pos = np.asarray(pos, np.float32).reshape(-1, 3)
    if len(pos) != n:
        p = np.zeros((n, 3), np.float32)
        p[:min(n, len(pos))] = pos[:n]
        pos = p
    me.vertices.foreach_set("co", pos.ravel())

    def fit(a, width):
        a = np.asarray(a, np.float32).reshape(-1, width) if width > 1 else np.asarray(a, np.float32).ravel()
        if len(a) != n:
            b = np.zeros((n, width) if width > 1 else n, np.float32)
            b[:min(n, len(a))] = a[:n]
            a = b
        return a.ravel()

    if scale is not None:
        me.attributes["scale"].data.foreach_set("value", fit(scale, 1))
    if size is not None:
        me.attributes["size"].data.foreach_set("vector", fit(size, 3))
    if rot is not None:
        me.attributes["rot"].data.foreach_set("vector", fit(rot, 3))
    if col is not None:
        c = np.asarray(col, np.float32)
        if c.shape[-1] == 3:
            c = np.concatenate([c.reshape(-1, 3), np.ones((len(c.reshape(-1, 3)), 1), np.float32)], 1)
        me.attributes["col"].data.foreach_set("color", fit(c, 4))
    for k, v in floats.items():
        me.attributes[k].data.foreach_set("value", fit(v, 1))
    me.update()


# ───────────────────────── 원형(프로토) 모델 ─────────────────────────
def proto(ctx, name, bm, mats, smooth=False):
    ob = mesh_obj(name, bm, None, ctx.proto, smooth)
    for m in mats:
        ob.data.materials.append(m)
    return ob


def proto_box(ctx, mat, name="p_box"):
    return proto(ctx, name, bm_cube(1, 1, 1, bottom=True), [mat])


def proto_person(ctx, mat_body, mat_skin):
    parts = [(bm_cone(0.16, 0.12, 0.42, (0, 0, 0.02), 10), 0),
             (bm_sphere(0.11, (0, 0, 0.56), 12, 8), 1)]
    return proto(ctx, "p_person", join_bms(parts), [mat_body, mat_skin], smooth=True)


def proto_cat(ctx, mat_fur, mat_eye):
    parts = [
        (bm_sphere(0.16, (0, 0, 0.15), 14, 8, scale=(1.55, 0.85, 0.8)), 0),   # 몸
        (bm_sphere(0.115, (0.27, 0, 0.27), 14, 8, scale=(1.0, 1.0, 0.92)), 0),  # 머리
        (bm_cone(0.05, 0.0, 0.1, (0.27, 0.055, 0.34), 4), 0),                   # 귀
        (bm_cone(0.05, 0.0, 0.1, (0.27, -0.055, 0.34), 4), 0),
        (bm_sphere(0.022, (0.375, 0.04, 0.29), 6, 4), 1),                         # 눈
        (bm_sphere(0.022, (0.375, -0.04, 0.29), 6, 4), 1),
    ]
    # 꼬리: 위로 휜 짧은 마디들
    for i in range(6):
        u = i / 5.0
        parts.append((bm_sphere(0.034 - 0.003 * i, (-0.25 - 0.06 * u, 0, 0.17 + 0.2 * u * u), 6, 4), 0))
    for dx in (-0.12, 0.12):  # 다리
        for dy in (-0.07, 0.07):
            parts.append((bm_cone(0.035, 0.03, 0.12, (dx, dy, 0.0), 6), 0))
    return proto(ctx, "p_cat", join_bms(parts), [mat_fur, mat_eye], smooth=True)


def proto_rat(ctx, mat):
    parts = [(bm_sphere(0.07, (0, 0, 0.06), 10, 6, scale=(1.6, 0.9, 0.8)), 0),
             (bm_sphere(0.04, (0.12, 0, 0.07), 8, 6), 0)]
    for i in range(5):
        parts.append((bm_sphere(0.012, (-0.12 - 0.04 * i, 0, 0.04), 4, 3), 0))
    return proto(ctx, "p_rat", join_bms(parts), [mat], smooth=True)


def proto_tree(ctx, mat_leaf, mat_trunk, kind="round"):
    if kind == "pine":
        parts = [(bm_cone(0.05, 0.04, 0.3, (0, 0, 0), 6), 1),
                 (bm_cone(0.34, 0.0, 0.55, (0, 0, 0.22), 7), 0),
                 (bm_cone(0.26, 0.0, 0.45, (0, 0, 0.5), 7), 0)]
    else:
        parts = [(bm_cone(0.05, 0.04, 0.35, (0, 0, 0), 6), 1),
                 (bm_ico(0.32, (0, 0, 0.55), 1, (1, 1, 0.9)), 0),
                 (bm_ico(0.2, (0.15, 0.08, 0.72), 1), 0)]
    return proto(ctx, "p_tree_" + kind, join_bms(parts), [mat_leaf, mat_trunk])


def proto_car(ctx, mat_body, mat_glass, mat_head, mat_tail):
    parts = [(bm_cube(0.46, 0.22, 0.1, (0, 0, 0.04), True), 0),
             (bm_cube(0.26, 0.2, 0.08, (-0.03, 0, 0.14), True), 1),
             (bm_cube(0.02, 0.05, 0.03, (0.235, 0.07, 0.08)), 2),
             (bm_cube(0.02, 0.05, 0.03, (0.235, -0.07, 0.08)), 2),
             (bm_cube(0.02, 0.05, 0.03, (-0.235, 0.07, 0.08)), 3),
             (bm_cube(0.02, 0.05, 0.03, (-0.235, -0.07, 0.08)), 3)]
    return proto(ctx, "p_car", join_bms(parts), [mat_body, mat_glass, mat_head, mat_tail])


def proto_lamp(ctx, mat_pole, mat_bulb):
    parts = [(bm_cone(0.02, 0.015, 0.5, (0, 0, 0), 6), 0),
             (bm_sphere(0.05, (0, 0, 0.53), 8, 6), 1)]
    return proto(ctx, "p_lamp", join_bms(parts), [mat_pole, mat_bulb])


# ───────────────────────── 떠 있는 섬(디오라마) ─────────────────────────
def mat_earth_side(name="m_side"):
    m, nt, out = new_mat(name)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ln(nt, geo.outputs["Position"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ln(nt, math_node(nt, "MULTIPLY_ADD", sep.outputs["Z"], 0.18, 1.0), ramp.inputs[0])
    e = ramp.color_ramp.elements
    e[0].position, e[0].color = 0.0, (0.10, 0.07, 0.06, 1)
    e[1].position, e[1].color = 0.97, (0.30, 0.20, 0.12, 1)
    g = e.new(0.985)
    g.color = (0.16, 0.30, 0.10, 1)
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 3.0
    col = mix_rgb(nt, 0.25, ramp.outputs["Color"], noise.outputs["Color"], "MULTIPLY")
    b = principled(nt, col, 0.9)
    ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    return m


def island(ctx, R=10.0, thick=1.1, depth=6.0, top_mat=None, seg=128, seed=3):
    rs = np.random.default_rng(seed)
    # 윗면
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False, segments=seg, radius=R)
    top = mesh_obj("island_top", bm, top_mat)
    # 옆면 + 아래 바위
    bm = bmesh.new()
    rings = [(R, 0.0), (R, -thick), (R * 0.93, -thick - 0.35), (R * 0.72, -thick - depth * 0.35),
             (R * 0.42, -thick - depth * 0.7), (R * 0.12, -thick - depth)]
    vs = []
    for ri, (rr, z) in enumerate(rings):
        row = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            jit = 1.0 if ri < 2 else 1.0 + rs.normal(0, 0.025)
            zz = z + (rs.normal(0, 0.08) if ri >= 2 else 0.0)
            row.append(bm.verts.new((math.cos(a) * rr * jit, math.sin(a) * rr * jit, zz)))
        vs.append(row)
    for r0, r1 in zip(vs, vs[1:]):
        for i in range(seg):
            bm.faces.new((r0[i], r0[(i + 1) % seg], r1[(i + 1) % seg], r1[i]))
    tip = bm.verts.new((0, 0, -thick - depth - 0.6))
    last = vs[-1]
    for i in range(seg):
        bm.faces.new((last[i], last[(i + 1) % seg], tip))
    side = mesh_obj("island_side", bm, mat_earth_side())
    return top, side


def mat_ground(ctx, name="m_ground", spacing=3.2, road_w=0.62, river=None, park=0.35,
               grass=(0.20, 0.36, 0.14), concrete=(0.30, 0.30, 0.31), asphalt=(0.055, 0.058, 0.065),
               overgrow=True, roads=True):
    """도로 격자·인도·공원·강·녹지화(ctl 'overgrow')를 셰이더로 그리는 땅."""
    m, nt, out = new_mat(name)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ln(nt, geo.outputs["Position"], sep.inputs[0])
    x, y = sep.outputs["X"], sep.outputs["Y"]

    def grid_dist(c):
        # 가장 가까운 격자선까지 거리
        f = math_node(nt, "FRACT", math_node(nt, "DIVIDE", math_node(nt, "ADD", c, spacing / 2), spacing))
        return math_node(nt, "MULTIPLY", math_node(nt, "ABSOLUTE", math_node(nt, "SUBTRACT", f, 0.5)), spacing)

    dx, dy = grid_dist(x), grid_dist(y)
    dmin = math_node(nt, "MINIMUM", dx, dy)
    road = math_node(nt, "LESS_THAN", dmin, road_w / 2) if roads else math_node(nt, "MULTIPLY", dmin, 0.0)
    walk = math_node(nt, "LESS_THAN", dmin, road_w / 2 + 0.22) if roads else math_node(nt, "MULTIPLY", dmin, 0.0)
    # 차선(점선)
    dash_x = math_node(nt, "LESS_THAN", math_node(nt, "FRACT", math_node(nt, "MULTIPLY", y, 1.6)), 0.5)
    dash_y = math_node(nt, "LESS_THAN", math_node(nt, "FRACT", math_node(nt, "MULTIPLY", x, 1.6)), 0.5)
    lane_x = math_node(nt, "MULTIPLY", math_node(nt, "LESS_THAN", dx, 0.025), dash_x)
    lane_y = math_node(nt, "MULTIPLY", math_node(nt, "LESS_THAN", dy, 0.025), dash_y)
    lane = math_node(nt, "MULTIPLY", math_node(nt, "MAXIMUM", lane_x, lane_y), road)
    # 공원(노이즈)
    pn = nt.nodes.new("ShaderNodeTexNoise")
    pn.inputs["Scale"].default_value = 0.09
    pn.inputs["Detail"].default_value = 2.0
    ln(nt, geo.outputs["Position"], pn.inputs["Vector"])
    parkm = math_node(nt, "GREATER_THAN", pn.outputs["Fac"], 1.0 - park)
    base = mix_rgb(nt, walk, mix_rgb(nt, parkm, concrete, grass), (0.42, 0.42, 0.42))
    base = mix_rgb(nt, road, base, asphalt)
    base = mix_rgb(nt, lane, base, (0.75, 0.72, 0.6))
    rough = math_node(nt, "MULTIPLY_ADD", road, -0.15, 0.85)
    water_mask = None
    if river:
        # river = (기울기, 절편, 폭, 굽이 크기)
        k, b0, wdt, amp = river
        wave = math_node(nt, "MULTIPLY", math_node(nt, "SINE", math_node(nt, "MULTIPLY", x, 0.35)), amp)
        center = math_node(nt, "ADD", math_node(nt, "MULTIPLY_ADD", x, k, b0), wave)
        d = math_node(nt, "ABSOLUTE", math_node(nt, "SUBTRACT", y, center))
        water_mask = math_node(nt, "LESS_THAN", d, wdt / 2)
        bank = math_node(nt, "LESS_THAN", d, wdt / 2 + 0.35)
        base = mix_rgb(nt, bank, base, (0.22, 0.32, 0.15))
    if overgrow:
        on = nt.nodes.new("ShaderNodeTexNoise")
        on.inputs["Scale"].default_value = 0.55
        on.inputs["Detail"].default_value = 6.0
        ln(nt, geo.outputs["Position"], on.inputs["Vector"])
        g = math_node(nt, "LESS_THAN", on.outputs["Fac"], math_node(nt, "MULTIPLY", ctx.ctl_node(nt, "overgrow", 0.0), 1.05))
        green = mix_rgb(nt, on.outputs["Fac"], (0.12, 0.30, 0.08), (0.28, 0.46, 0.14))
        base = mix_rgb(nt, g, base, green)
        rough = math_node(nt, "MAXIMUM", rough, math_node(nt, "MULTIPLY", g, 0.9))
    bsdf = principled(nt, base, rough)
    shader = bsdf.outputs["BSDF"]
    if water_mask is not None:
        wb = principled(nt, (0.015, 0.05, 0.09), 0.06, spec=0.7)
        mx = nt.nodes.new("ShaderNodeMixShader")
        ln(nt, water_mask, mx.inputs[0])
        ln(nt, shader, mx.inputs[1])
        ln(nt, wb.outputs["BSDF"], mx.inputs[2])
        shader = mx.outputs[0]
    ln(nt, shader, out.inputs["Surface"])
    return m


def mat_building(ctx, name="m_bld", wcol=(1.0, 0.72, 0.38), wstr=7.0, density=3.2, floor_h=0.32):
    """창문 불빛(ctl 'lights' 비율 × 인스턴스 'lit'), 녹지화('overgrow'), 낡음('decay')."""
    m, nt, out = new_mat(name)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    pos = geo.outputs["Position"]
    tco = nt.nodes.new("ShaderNodeTexCoord")
    loc = nt.nodes.new("ShaderNodeVectorMath")
    loc.operation = "MULTIPLY"
    ln(nt, tco.outputs["Object"], loc.inputs[0])
    ln(nt, inst_attr(nt, "size", "Vector"), loc.inputs[1])
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ln(nt, loc.outputs[0], sep.inputs[0])
    nsep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ln(nt, geo.outputs["Normal"], nsep.inputs[0])
    wall = math_node(nt, "LESS_THAN", math_node(nt, "ABSOLUTE", nsep.outputs["Z"]), 0.5)
    u = math_node(nt, "MULTIPLY_ADD", math_node(nt, "ADD", sep.outputs["X"], sep.outputs["Y"]), density, 0.5)
    v = math_node(nt, "DIVIDE", sep.outputs["Z"], floor_h)
    fu = math_node(nt, "FRACT", u)
    fv = math_node(nt, "FRACT", v)
    wu = math_node(nt, "MULTIPLY", math_node(nt, "GREATER_THAN", fu, 0.22), math_node(nt, "LESS_THAN", fu, 0.78))
    wv = math_node(nt, "MULTIPLY", math_node(nt, "GREATER_THAN", fv, 0.28), math_node(nt, "LESS_THAN", fv, 0.78))
    ground_floor = math_node(nt, "GREATER_THAN", sep.outputs["Z"], floor_h * 0.9)
    win = math_node(nt, "MULTIPLY", math_node(nt, "MULTIPLY", wu, wv), math_node(nt, "MULTIPLY", wall, ground_floor))
    cell = nt.nodes.new("ShaderNodeCombineXYZ")
    ln(nt, math_node(nt, "FLOOR", u), cell.inputs[0])
    ln(nt, math_node(nt, "FLOOR", v), cell.inputs[1])
    ln(nt, inst_attr(nt, "seed", "Fac"), cell.inputs[2])
    wn = nt.nodes.new("ShaderNodeTexWhiteNoise")
    wn.noise_dimensions = "3D"
    ln(nt, cell.outputs[0], wn.inputs["Vector"])
    frac = math_node(nt, "MULTIPLY", ctx.ctl_node(nt, "lights", 1.0), inst_attr(nt, "lit", "Fac"))
    lit = math_node(nt, "LESS_THAN", wn.outputs["Value"], frac)
    glow = math_node(nt, "MULTIPLY", win, lit)
    wc = mix_rgb(nt, wn.outputs["Color"], wcol, (1.0, 0.9, 0.7))
    base_c = inst_attr(nt, "col")
    dark_glass = (0.03, 0.04, 0.06)
    base = mix_rgb(nt, win, base_c, dark_glass)
    roof = math_node(nt, "GREATER_THAN", nsep.outputs["Z"], 0.5)
    base = mix_rgb(nt, roof, base, mix_rgb(nt, 0.4, base_c, (0.12, 0.12, 0.13)))
    dec = ctx.ctl_node(nt, "decay", 0.0)
    base = mix_rgb(nt, math_node(nt, "MULTIPLY", dec, 0.6), base, (0.10, 0.09, 0.08))
    # 덩굴: 아래부터 초록
    on = nt.nodes.new("ShaderNodeTexNoise")
    on.inputs["Scale"].default_value = 1.6
    on.inputs["Detail"].default_value = 5.0
    ln(nt, pos, on.inputs["Vector"])
    reach = math_node(nt, "SUBTRACT", math_node(nt, "MULTIPLY", ctx.ctl_node(nt, "overgrow", 0.0), 1.25),
                      math_node(nt, "MULTIPLY", sep.outputs["Z"], 0.16))
    vine = math_node(nt, "LESS_THAN", on.outputs["Fac"], reach)
    base = mix_rgb(nt, vine, base, mix_rgb(nt, on.outputs["Fac"], (0.10, 0.26, 0.07), (0.25, 0.42, 0.12)))
    glow = math_node(nt, "MULTIPLY", glow, math_node(nt, "SUBTRACT", 1.0, vine))
    rough = math_node(nt, "MULTIPLY_ADD", win, -0.6, 0.8)
    b = principled(nt, base, rough, emit=wc, estr=math_node(nt, "MULTIPLY", glow, wstr))
    ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def city_layout(R, spacing=3.2, road_w=0.62, seed=1, river=None, park_fn=None, margin=0.9,
                hmin=0.5, hmax=4.5, center_boost=1.6):
    """도로 격자 사이 블록에 건물 배치 → [(x, y, w, d, h)]."""
    rs = np.random.default_rng(seed)
    out = []
    half = spacing / 2
    n = int(R / spacing) + 2
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            cx, cy = i * spacing, j * spacing
            inner = spacing - road_w - 0.5
            # 블록당 1~4개 건물
            k = rs.choice([1, 2, 2, 3, 4])
            subs = [(0, 0, inner, inner)] if k == 1 else \
                [(-inner / 4, 0, inner / 2 - 0.08, inner), (inner / 4, 0, inner / 2 - 0.08, inner)] if k == 2 else \
                [(-inner / 4, -inner / 4, inner / 2 - 0.08, inner / 2 - 0.08), (inner / 4, -inner / 4, inner / 2 - 0.08, inner / 2 - 0.08),
                 (0, inner / 4, inner - 0.08, inner / 2 - 0.08)] if k == 3 else \
                [(sx * inner / 4, sy * inner / 4, inner / 2 - 0.08, inner / 2 - 0.08) for sx in (-1, 1) for sy in (-1, 1)]
            for ox, oy, w, d in subs:
                x, y = cx + ox, cy + oy
                r = math.hypot(x, y) + max(w, d) * 0.7
                if r > R - margin:
                    continue
                if river:
                    kk, b0, wdt, amp = river
                    if abs(y - (kk * x + b0 + amp * math.sin(0.35 * x))) < wdt / 2 + 0.6 + max(w, d) / 2:
                        continue
                if park_fn and park_fn(x, y):
                    continue
                cen = 1.0 - min(1.0, math.hypot(x, y) / R)
                h = rs.uniform(hmin, hmax) * (0.55 + center_boost * cen * cen)
                out.append((x, y, w * rs.uniform(0.8, 1.0), d * rs.uniform(0.8, 1.0), h))
    return out


def road_points(R, spacing=3.2, step=0.4, margin=0.6):
    """도로 중심선 위의 점들 (차·사람 이동용) → (pts(N,2), dir(N,2))."""
    pts, dirs = [], []
    n = int(R / spacing) + 1
    for i in range(-n, n + 1):
        c = i * spacing
        for t in np.arange(-R, R, step):
            for (x, y, dx, dy) in ((c, t, 0, 1), (t, c, 1, 0)):
                if math.hypot(x, y) < R - margin:
                    pts.append((x, y))
                    dirs.append((dx, dy))
    return np.array(pts, np.float32), np.array(dirs, np.float32)


# ───────────────────────── 지구본 ─────────────────────────
def load_image(path, non_color=False):
    img = bpy.data.images.load(str(path), check_existing=True)
    if non_color:
        img.colorspace_settings.name = "Non-Color"
    return img


def globe(ctx, radius=4.0, tex=None, elev=None, ice=None, borders=None, seg=128,
          ocean=(0.03, 0.12, 0.30), land=(0.10, 0.30, 0.30), land_hi=(0.30, 0.36, 0.30)):
    """등장방형 텍스처 기반 지구. ctl: 'sea'(해수면 m), 'ice'(얼음 남은 비율), 'borders'(국경 표시 비율)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=radius, calc_uvs=True)
    m, nt, out = new_mat("m_globe")
    uv = nt.nodes.new("ShaderNodeTexCoord").outputs["UV"]
    base = None
    if elev:
        ti = nt.nodes.new("ShaderNodeTexImage")
        ti.image = load_image(elev, True)
        ti.interpolation = "Linear"
        ln(nt, uv, ti.inputs["Vector"])
        # elev png: (m + 11000) / 20000
        e_m = math_node(nt, "MULTIPLY_ADD", ti.outputs["Color"], 20000.0, -11000.0)
        sea = ctx.ctl_node(nt, "sea", 0.0)
        land_m = nt.nodes.new("ShaderNodeTexImage")
        land_m.image = load_image(tex, True)
        ln(nt, uv, land_m.inputs["Vector"])
        is_land = math_node(nt, "MULTIPLY", math_node(nt, "GREATER_THAN", land_m.outputs["Color"], 0.5),
                            math_node(nt, "GREATER_THAN", e_m, sea))
        hi = math_node(nt, "DIVIDE", math_node(nt, "SUBTRACT", e_m, sea), 2500.0, clamp=True)
        lc = mix_rgb(nt, hi, land, land_hi)
        depth = math_node(nt, "DIVIDE", math_node(nt, "SUBTRACT", sea, e_m), 5000.0, clamp=True)
        oc = mix_rgb(nt, depth, (0.06, 0.26, 0.46), ocean)
        base = mix_rgb(nt, is_land, oc, lc)
        rough = math_node(nt, "MULTIPLY_ADD", is_land, 0.45, 0.22)
    else:
        base = rgb(nt, ocean)
        rough = 0.3
    if ice:
        ii = nt.nodes.new("ShaderNodeTexImage")
        ii.image = load_image(ice, True)
        ln(nt, uv, ii.inputs["Vector"])
        icef = math_node(nt, "MULTIPLY", math_node(nt, "GREATER_THAN", ii.outputs["Color"],
                                                   math_node(nt, "SUBTRACT", 1.0, ctx.ctl_node(nt, "ice", 1.0))), 1.0)
        base = mix_rgb(nt, icef, base, (0.85, 0.92, 1.0))
    emit = None
    estr = 0.0
    if borders:
        bi = nt.nodes.new("ShaderNodeTexImage")
        bi.image = load_image(borders, True)
        bi.interpolation = "Closest"
        ln(nt, uv, bi.inputs["Vector"])
        has = math_node(nt, "GREATER_THAN", bi.outputs["Color"], 0.001)
        alive = math_node(nt, "GREATER_THAN", bi.outputs["Color"], ctx.ctl_node(nt, "borders_gone", 0.0))
        bl = math_node(nt, "MULTIPLY", has, alive)
        emit = (1.0, 0.75, 0.3)
        estr = math_node(nt, "MULTIPLY", bl, ctx.ctl_node(nt, "borders_glow", 3.0))
    b = principled(nt, base, rough, emit=emit, estr=estr, coat=0.35)
    ln(nt, b.outputs["BSDF"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    ob = mesh_obj("globe", bm, m, smooth=True)
    # 대기 빛무리
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=radius * 1.035)
    am, nt, out = new_mat("m_atmo")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    fac = math_node(nt, "POWER", lw.outputs["Facing"], 3.0)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (0.25, 0.55, 1.0, 1)
    ln(nt, math_node(nt, "MULTIPLY", fac, 2.2), em.inputs["Strength"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    add = nt.nodes.new("ShaderNodeAddShader")
    ln(nt, tr.outputs[0], add.inputs[0])
    ln(nt, em.outputs[0], add.inputs[1])
    ln(nt, add.outputs[0], out.inputs["Surface"])
    am.cycles.emission_sampling = "NONE"
    atmo = mesh_obj("atmo", bm, am, smooth=True)
    return ob, atmo


def latlon_to_xyz(lat, lon, r):
    """UV 구 기준 (u=0 → 경도 -180)."""
    la, lo = np.radians(lat), np.radians(lon)
    x = r * np.cos(la) * np.cos(lo + math.pi)
    y = r * np.cos(la) * np.sin(lo + math.pi)
    z = r * np.sin(la)
    return np.stack([x, y, z], -1)


# ───────────────────────── 렌더 설정 ─────────────────────────
def configure(scene, pct=67, samples=24, device="CPU", fast=False):
    r = scene.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y = 1080, 1920
    r.resolution_percentage = pct
    r.use_persistent_data = True
    r.film_transparent = True
    c = scene.cycles
    c.samples = samples
    c.use_adaptive_sampling = True
    c.adaptive_threshold = 0.05 if not fast else 0.1
    c.use_denoising = True
    c.denoiser = "OPENIMAGEDENOISE"
    c.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    c.denoising_prefilter = "FAST"
    c.max_bounces = 4
    c.diffuse_bounces = 2
    c.glossy_bounces = 2
    c.transmission_bounces = 4
    c.volume_bounces = 0
    c.transparent_max_bounces = 8
    c.caustics_reflective = False
    c.caustics_refractive = False
    c.blur_glossy = 1.0
    c.sample_clamp_indirect = 4.0
    c.use_animated_seed = True
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    im = r.image_settings
    im.file_format = "OPEN_EXR"
    im.color_depth = "16"
    im.exr_codec = "ZIP"
    im.color_mode = "RGBA"
    if device == "GPU":
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for kind in ("OPTIX", "CUDA"):
            try:
                prefs.compute_device_type = kind
                prefs.get_devices()
                ok = [d for d in prefs.devices if d.type == kind]
                if ok:
                    for d in prefs.devices:
                        d.use = d.type == kind
                    c.device = "GPU"
                    break
            except Exception:
                continue
    else:
        c.device = "CPU"
