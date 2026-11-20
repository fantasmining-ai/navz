# -*- coding: utf-8 -*-
"""Funciones comunes EYEBORG. Requiere Blender 4.x; unidades de entrada en mm."""
import math
import bpy
from mathutils import Vector

BLUE = (0.015, 0.43, 0.58, 1.0)
BLUE_LIGHT = (0.025, 0.58, 0.72, 1.0)
DARK = (0.018, 0.035, 0.045, 1.0)
GHOST = (0.9, 0.48, 0.08, 1.0)


def scene_mm():
    s = bpy.context.scene
    s.unit_settings.system = 'METRIC'
    s.unit_settings.scale_length = 0.001
    s.unit_settings.length_unit = 'MILLIMETERS'


def get_collection(name, clear=False):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    if clear:
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    return col


def clear_eyeborg():
    for col in list(bpy.data.collections):
        if col.name.startswith('EYEBORG_'):
            for obj in list(col.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(col)
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def mat(name, color, roughness=0.34, metallic=0.18):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = color
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
    return m


def link_obj(obj, collection):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def catmull_rom(points, steps=7):
    pts = [Vector(p) for p in points]
    if len(pts) < 2:
        return pts
    padded = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(padded)-2):
        p0, p1, p2, p3 = padded[i-1:i+3]
        for j in range(steps):
            t = j / float(steps)
            t2, t3 = t*t, t*t*t
            v = 0.5 * ((2*p1) + (-p0+p2)*t + (2*p0-5*p1+4*p2-p3)*t2 + (-p0+3*p1-3*p2+p3)*t3)
            out.append(v)
    out.append(pts[-1])
    return out


def _pair(value):
    return (float(value), float(value)) if isinstance(value, (int,float)) else (float(value[0]),float(value[1]))


def sweep_ribbon(name, control_points, width, thickness, collection, width_hint=(1,0,0), material=None, steps=7, sections=12, taper=(1.0,0.72)):
    """Rama orgánica de sección elíptica aplanada. Coordenadas en mm."""
    path = catmull_rom(control_points, steps)
    if len(path) < 2:
        raise ValueError('La trayectoria necesita al menos dos puntos')
    w0,w1 = _pair(width)
    t0,t1 = _pair(thickness)
    ta,tb = taper
    hint = Vector(width_hint).normalized()
    verts, faces = [], []
    frames = []
    for i,p in enumerate(path):
        tangent = (path[min(i+1,len(path)-1)] - path[max(i-1,0)]).normalized()
        wa = tangent.cross(hint)
        if wa.length < 1e-5:
            fallback = Vector((0,0,1)) if abs(tangent.z) < 0.85 else Vector((0,1,0))
            wa = tangent.cross(fallback)
        wa.normalize()
        da = tangent.cross(wa).normalized()
        f = i / float(max(1,len(path)-1))
        taper_scale = ta + (tb-ta)*f
        w = (w0 + (w1-w0)*f) * taper_scale
        th = (t0 + (t1-t0)*f) * taper_scale
        frames.append((p,wa,da,w*0.5,th*0.5))
    for p,wa,da,ra,rb in frames:
        for j in range(sections):
            a = 2*math.pi*j/sections
            v = p + wa*(math.cos(a)*ra) + da*(math.sin(a)*rb)
            verts.append(tuple(v))
    ring_count = len(path)
    for i in range(ring_count-1):
        for j in range(sections):
            a = i*sections+j
            b = i*sections+(j+1)%sections
            c = (i+1)*sections+(j+1)%sections
            d = (i+1)*sections+j
            faces.append((a,b,c,d))
    faces.append(tuple(reversed(tuple(range(sections)))))
    faces.append(tuple((ring_count-1)*sections+j for j in range(sections)))
    mesh = bpy.data.meshes.new(name+'_MESH')
    mesh.from_pydata(verts, [], faces)
    mesh.validate(verbose=False)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    if material:
        mesh.materials.append(material)
    for poly in mesh.polygons:
        poly.use_smooth = True
    obj['familia'] = 'nervadura_exoesqueletica'
    obj['dimensiones_fuente'] = 'geometria organica basada en referencias visuales; no escaneo'
    return obj


def box_part(name, dimensions, location, collection, material=None, bevel=1.2, wire=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    link_obj(obj, collection)
    if material:
        obj.data.materials.append(material)
    if wire:
        obj.display_type = 'WIRE'
        obj.hide_render = True
        obj['solo_referencia'] = True
    elif bevel > 0:
        mod = obj.modifiers.new('Bisel_organico', 'BEVEL')
        mod.width = bevel
        mod.segments = 4
        mod.profile = 0.5
        mod2 = obj.modifiers.new('Normales_suaves', 'WEIGHTED_NORMAL')
        mod2.keep_sharp = True
    return obj


def cylinder_part(name, radius, depth, location, collection, material=None, rotation=(0,0,0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    link_obj(obj, collection)
    if material:
        obj.data.materials.append(material)
    bevel = obj.modifiers.new('Borde_suave', 'BEVEL')
    bevel.width = min(0.7, radius*0.15)
    bevel.segments = 3
    obj.modifiers.new('Normales', 'WEIGHTED_NORMAL')

    return obj


def torus_part(name, major_radius, minor_radius, location, collection, material=None, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=48, minor_segments=12, location=location, rotation=rotation,
                                     major_radius=major_radius, minor_radius=minor_radius)
    obj = bpy.context.object
    obj.name = name
    link_obj(obj, collection)
    if material:
        obj.data.materials.append(material)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def create_head_reference(name, dims, collection, clearance=0.0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, location=(0,0,0))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (dims[0]+2*clearance, dims[1]+2*clearance, dims[2]+2*clearance)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    link_obj(obj, collection)
    obj.display_type = 'WIRE'
    obj.hide_render = True
    obj['solo_referencia_no_imprimir'] = True
    return obj


def mark_modular(obj, interface, note='union separable; comprobar tornilleria real'):
    obj['interfaz_modular'] = interface
    obj['nota_fabricacion'] = note
    return obj


def set_materials():
    d = {
        'blue': mat('EYEBORG_AZUL_REFERENCIA', (0.015,0.43,0.58,1), 0.28, 0.22),
        'light': mat('EYEBORG_AZUL_CLARO', (0.025,0.58,0.72,1), 0.3, 0.18),
        'dark': mat('EYEBORG_NEGRO_TECNICO', (0.02,0.035,0.045,1), 0.48, 0.25),
        'ghost': mat('EYEBORG_ENVELOPE_REFERENCIA', (0.95,0.45,0.06,1), 0.65, 0.0),
    }
    d['blue_light'] = d['light']  # alias: varios modulos usan ambas claves
    return d


# ---------------------------------------------------------------------------
# Correas planas sobre una superficie tipo casco (rev. azul: nervaduras anchas)
# ---------------------------------------------------------------------------
SHELL_DEFAULT = {'A': 88.0, 'B': 135.0, 'C': 90.0, 'cz': 5.0}
try:
    import json as _json, os as _os
    with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'eyeborg_config.json'), encoding='utf-8') as _f:
        SHELL_DEFAULT.update({k: v for k, v in _json.load(_f).get('shell', {}).items() if isinstance(v, (int, float))})
except Exception:
    pass


HEAD_SEMI = (82.5, 101.0, 107.5)   # semiejes de la envolvente de cabeza verificada (165x202x215 mm)
HEAD_GAP = 6.0
try:
    with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'eyeborg_config.json'), encoding='utf-8') as _f2:
        _cfg = _json.load(_f2)
    HEAD_SEMI = tuple(v / 2.0 for v in _cfg['anthropometry']['head_envelope_xyz_mm'])
    HEAD_GAP = float(_cfg['fit']['head_clearance_mm'])
except Exception:
    pass


def head_gap_mm(p):
    """Distancia aproximada (mm) de p a la superficie de la cabeza; negativa si esta dentro."""
    a, b, c = HEAD_SEMI
    r2 = (p.x / a) ** 2 + (p.y / b) ** 2 + (p.z / c) ** 2
    g = Vector((p.x / a ** 2, p.y / b ** 2, p.z / c ** 2))
    return (r2 - 1.0) / (2.0 * g.length) if g.length > 1e-9 else -min(HEAD_SEMI)


def push_out_of_head(p, required):
    """Desplaza p a lo largo del gradiente de la cabeza hasta cumplir la holgura requerida (mm)."""
    a, b, c = HEAD_SEMI
    q = Vector(p)
    for _ in range(4):
        gap = head_gap_mm(q)
        if gap >= required:
            break
        n = Vector((q.x / a ** 2, q.y / b ** 2, q.z / c ** 2))
        if n.length < 1e-9:
            n = Vector((0, -1, 0))
        q = q + n.normalized() * (required - gap)
    return q


NOSE_HALF = 20.5   # semiancho de la muesca nasal (mm), de front_features.nasal_notch_half_width_mm
try:
    NOSE_HALF = float(_cfg['front_features']['nasal_notch_half_width_mm'])
except Exception:
    pass


def nose_keepout(q, w_half):
    """Mantiene libre el corredor de la nariz: |x| >= NOSE_HALF + 2 + w_half para z entre -45 y +5 (rampa suave)."""
    z = q.z
    if q.y > -55 or z < -58 or z > 18:
        return q
    if z >= -45 and z <= 5:
        fz = 1.0
    elif z < -45:
        fz = (z + 58) / 13.0
    else:
        fz = (18 - z) / 13.0
    fz = fz * fz * (3 - 2 * fz)
    need = (NOSE_HALF + 2.0 + w_half) * fz
    if abs(q.x) < need:
        sg = 1.0 if q.x >= 0 else -1.0
        return Vector((sg * need, q.y, q.z))
    return q


def shell_point(u, v, off=0.0, shell=None):
    """Punto y normal sobre el elipsoide guia. u: acimut desde el frente (-Y) hacia +X (grados);
    v: elevacion (grados); off: separacion normal en mm."""
    s = shell or SHELL_DEFAULT
    ur, vr = math.radians(u), math.radians(v)
    dx = math.sin(ur) * math.cos(vr)
    dy = -math.cos(ur) * math.cos(vr)
    dz = math.sin(vr)
    p = Vector((s['A'] * dx, s['B'] * dy, s['cz'] + s['C'] * dz))
    n = Vector((dx / s['A'], dy / s['B'], dz / s['C'])).normalized()
    return p + n * off, n


def _profile(prof, f):
    """Interpola (f, valor) con coseno; admite escalar."""
    if isinstance(prof, (int, float)):
        return float(prof)
    if isinstance(prof[0], (int, float)):  # valores equiespaciados (inicio, ..., fin)
        n = len(prof) - 1
        prof = [(i / float(n), v) for i, v in enumerate(prof)] if n else [(0.0, prof[0])]
    if f <= prof[0][0]:
        return float(prof[0][1])
    for (f0, a), (f1, b) in zip(prof, prof[1:]):
        if f <= f1:
            t = (f - f0) / max(1e-9, (f1 - f0))
            t = 0.5 - 0.5 * math.cos(math.pi * t)
            return a + (b - a) * t
    return float(prof[-1][1])


def strap(name, uv_points, width, thickness, collection, material=None, shell=None,
          steps=10, sections=20, power=3.2, cap=(0.07, 0.07), mirror=False, xyz=False, nhint=None, center=None, sharp=(None, None), clear=True):
    """Correa plana de bordes redondeados que sigue la superficie guia.
    uv_points: [(u, v)] o [(u, v, off)]; width/thickness: escalar o [(f, mm)].
    xyz=True: los puntos son (x, y, z) libres en mm y nhint da la normal (eje de espesor), p. ej. para cuernos."""
    if xyz:
        sg = -1.0 if mirror else 1.0
        path = catmull_rom([(sg * q[0], q[1], q[2]) for q in uv_points], steps)
        P = list(path); n_ring = len(path)
        if clear:   # ergonomia: holgura minima a la cabeza (superficie interior de la correa)
            tmax = max(_profile(thickness, i / float(max(1, n_ring - 1))) for i in range(0, n_ring, max(1, n_ring // 8)))
            P = [push_out_of_head(q, HEAD_GAP + 0.5 * tmax + 0.5) for q in P]
            P = [nose_keepout(q, 0.5 * _profile(width, i / float(max(1, n_ring - 1))))
                 if abs(q.x) > 0.5 else q for i, q in enumerate(P)]
        if center is not None:   # normal radial respecto a un centro; None = usa la coordenada del propio punto
            cx = (center[0] * sg) if center[0] is not None else None
            N = []
            for q in P:
                c = Vector((q.x if cx is None else cx, q.y if center[1] is None else center[1],
                            q.z if center[2] is None else center[2]))
                v = q - c
                N.append(v.normalized() if v.length > 1e-6 else Vector((sg, 0, 0)))
        else:
            h = nhint if nhint is not None else (1, 0, 0)
            hint = Vector((sg * h[0], h[1], h[2])).normalized()
            N = [hint] * n_ring
    else:
        pts = [(-p[0] if mirror else p[0], p[1], p[2] if len(p) > 2 else 0.0) for p in uv_points]
        path = catmull_rom(pts, steps)
        n_ring = len(path)
        P, N = [], []
        for q in path:
            p3, nn = shell_point(q.x, q.y, q.z, shell)
            P.append(p3); N.append(nn)
    verts, faces = [], []
    for i in range(n_ring):
        T = (P[min(i + 1, n_ring - 1)] - P[max(i - 1, 0)]).normalized()
        W = N[i].cross(T)
        if W.length < 1e-6:
            W = Vector((0, 0, 1)).cross(T)
        W.normalize()
        D = T.cross(W).normalized()
        f = i / float(max(1, n_ring - 1))
        k = 1.0
        kt = None
        if f < cap[0] and cap[0] > 0:
            if sharp[0]:   # punta de aguja al inicio
                k = kt = max(((f / cap[0]) ** sharp[0]), 0.012)
            else:
                k = math.sqrt(max(0.0, 1 - ((cap[0] - f) / cap[0]) ** 2))
        elif f > 1 - cap[1] and cap[1] > 0:
            if sharp[1]:   # punta de aguja al final (afinado progresivo)
                k = kt = max((((1 - f) / cap[1]) ** sharp[1]), 0.012)
            else:
                k = math.sqrt(max(0.0, 1 - ((f - (1 - cap[1])) / cap[1]) ** 2))
        if kt is None:
            k = max(k, 0.12)
            kt = max(k, 0.35)
        hw = _profile(width, f) * 0.5 * k
        ht = _profile(thickness, f) * 0.5 * kt
        for j in range(sections):
            a = 2 * math.pi * j / sections
            c, s_ = math.cos(a), math.sin(a)
            x = math.copysign(abs(c) ** (2.0 / power), c) * hw
            y = math.copysign(abs(s_) ** (2.0 / power), s_) * ht
            verts.append(tuple(P[i] + W * x + D * y))
    for i in range(n_ring - 1):
        for j in range(sections):
            a = i * sections + j
            b = i * sections + (j + 1) % sections
            c2 = (i + 1) * sections + (j + 1) % sections
            d = (i + 1) * sections + j
            faces.append((a, b, c2, d))
    faces.append(tuple(reversed(range(sections))))
    faces.append(tuple((n_ring - 1) * sections + j for j in range(sections)))
    mesh = bpy.data.meshes.new(name + '_MESH')
    mesh.from_pydata(verts, [], faces)
    mesh.validate(verbose=False)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    if material:
        mesh.materials.append(material)
    for poly in mesh.polygons:
        poly.use_smooth = True
    obj['familia'] = 'correa_organica_sobre_superficie_guia'
    obj['linea_central'] = [float(c) for pnt, nn in zip(P, N) for c in (pnt.x, pnt.y, pnt.z, nn.x, nn.y, nn.z)]
    obj['dimensiones_fuente'] = 'reconstruccion por vistas azules; no escaneo'
    return obj


def fuse_objects(name, objects, collection, material=None, voxel_mm=1.6, smooth_iters=8):
    """Une objetos en una sola malla organica (remesh por voxel + suavizado) sin modificar los originales."""
    verts, faces = [], []
    for o in objects:
        mw = o.matrix_world
        base = len(verts)
        verts += [tuple(mw @ v.co) for v in o.data.vertices]
        faces += [tuple(base + i for i in p.vertices) for p in o.data.polygons]
    tmp_mesh = bpy.data.meshes.new(name + '_TMP')
    tmp_mesh.from_pydata(verts, [], faces)
    tmp = bpy.data.objects.new(name + '_TMP', tmp_mesh)
    bpy.context.scene.collection.objects.link(tmp)
    r = tmp.modifiers.new('Remesh', 'REMESH')
    r.mode = 'VOXEL'; r.voxel_size = voxel_mm; r.use_smooth_shade = True
    s = tmp.modifiers.new('Suavizado', 'LAPLACIANSMOOTH')   # conserva volumen: no come las puntas finas
    s.iterations = smooth_iters; s.lambda_factor = 0.5; s.lambda_border = 0.0
    s.use_volume_preserve = True; s.use_normalized = True
    r2 = tmp.modifiers.new('Remesh2', 'REMESH')   # segunda pasada: garantiza malla estanca tras el suavizado
    r2.mode = 'VOXEL'; r2.voxel_size = voxel_mm; r2.use_smooth_shade = True
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg), depsgraph=dg)
    me.name = name + '_MESH'
    bpy.data.objects.remove(tmp, do_unlink=True)
    bpy.data.meshes.remove(tmp_mesh)
    obj = bpy.data.objects.new(name, me)
    collection.objects.link(obj)
    if material:
        me.materials.append(material)
    for poly in me.polygons:
        poly.use_smooth = True
    obj['familia'] = 'fusion_organica_visual'
    obj['nota'] = 'malla fusionada para visualizacion; revisar espesores antes de imprimir'
    return obj


def _cutter_mesh(specs):
    """Malla combinada de cortadores. specs: ('cyl', centro, direccion, radio, profundidad) o ('box', centro, (dx,dy,dz))."""
    import bmesh
    bm = bmesh.new()
    for sp in specs:
        if sp[0] == 'cyl':
            _, c, d, r, depth = sp
            rot = Vector(d).normalized().to_track_quat('Z', 'Y').to_matrix().to_4x4()
            mat_ = __import__('mathutils').Matrix.Translation(Vector(c)) @ rot
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=20, radius1=r, radius2=r,
                                  depth=depth, matrix=mat_)
        else:
            _, c, dims = sp
            m_ = __import__('mathutils').Matrix.Translation(Vector(c)) @ __import__('mathutils').Matrix.Diagonal(Vector((dims[0], dims[1], dims[2], 1.0)))
            bmesh.ops.create_cube(bm, size=1.0, matrix=m_)
    me = bpy.data.meshes.new('CORTADORES_MESH')
    bm.to_mesh(me)
    bm.free()
    return me


def cut_with_specs(obj, specs, name='CORTADORES'):
    """Resta (booleano exacto) agujeros/bolsas al objeto y reemplaza su malla. Devuelve nº de cortadores."""
    cut_me = _cutter_mesh(specs)
    cutter = bpy.data.objects.new(name, cut_me)
    bpy.context.scene.collection.objects.link(cutter)
    mod = obj.modifiers.new('Agujeros', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.operand_type = 'OBJECT'
    mod.object = cutter
    mod.solver = 'EXACT'
    mod.use_self = True
    dg = bpy.context.evaluated_depsgraph_get()
    new_me = bpy.data.meshes.new_from_object(obj.evaluated_get(dg), depsgraph=dg)
    old = obj.data
    obj.modifiers.remove(mod)
    obj.data = new_me
    for mat_ in old.materials:
        new_me.materials.append(mat_)
    for poly in new_me.polygons:
        poly.use_smooth = True
    bpy.data.objects.remove(cutter, do_unlink=True)
    bpy.data.meshes.remove(cut_me)
    bpy.data.meshes.remove(old)
    return len(specs)


def thorn_from_strap(obj, f, side, length, base_width, collection, material=None, name=None,
                     sweep=0.8, lift=0.15, mirror=False, thick=3.2):
    """Espina afilada que nace del lateral de una correa en la fraccion f (0-1) de su linea central.
    side: +1/-1 lado lateral (eje ancho de la correa); length en mm; sweep: cuanto sigue la tangente (barrido)."""
    a = list(obj['linea_central'])
    pts = [(Vector(a[i:i+3]), Vector(a[i+3:i+6])) for i in range(0, len(a), 6)]
    i = min(len(pts) - 2, max(1, int(round(f * (len(pts) - 1)))))
    c, n = pts[i]
    T = (pts[i + 1][0] - pts[i - 1][0]).normalized()
    W = n.cross(T)
    if W.length < 1e-6:
        return None
    W.normalize()
    s = side * (-1.0 if mirror else 1.0)
    d1 = (W * s * (1 - sweep * 0.5) + T * sweep + n * lift).normalized()
    d2 = (W * s * 0.45 + T * (sweep + 0.25) + n * lift * 1.6).normalized()
    p0 = c + W * s * (base_width * 0.25)
    p1 = p0 + d1 * (length * 0.42)
    p2 = p1 + d2 * (length * 0.36)
    p3 = p2 + d2 * (length * 0.30) + n * (length * 0.04)
    nm = name or (obj.name + '_ESPINA_%d' % int(f * 100))
    sp = strap(nm, [tuple(p0), tuple(p1), tuple(p2), tuple(p3)], [(0, base_width), (0.5, base_width * 0.42), (1, 0.4)],
               [(0, thick), (1, 0.4)], collection, material=material, xyz=True, nhint=tuple(n),
               cap=(0.0, 0.85), sharp=(None, 1.15), steps=8, sections=14, power=2.4, clear=False)
    sp['familia'] = 'espina_decorativa'
    sp['nota'] = 'punta afilada decorativa; verificar que no contacte piel/ojos y redondear la punta al imprimir'
    return sp


def node_blob(name, center, normal, rx, ry, rz, collection, material=None, mirror=False, clear=True):
    """Nodo de union organico (elipsoide achatado) que engrosa los cruces de correas, como en las referencias cromadas."""
    import bmesh
    from mathutils import Matrix
    c = Vector(center)
    n = Vector(normal)
    if mirror:
        c.x = -c.x; n.x = -n.x
    if clear:
        c = push_out_of_head(c, HEAD_GAP + rz + 0.5)
    n.normalize()
    bm = bmesh.new()
    m_ = Matrix.Translation(c) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4() @ Matrix.Diagonal(Vector((rx, ry, rz, 1.0)))
    bmesh.ops.create_uvsphere(bm, u_segments=28, v_segments=18, radius=1.0, matrix=m_)
    me = bpy.data.meshes.new(name + '_MESH')
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    collection.objects.link(obj)
    if material:
        me.materials.append(material)
    for poly in me.polygons:
        poly.use_smooth = True
    obj['familia'] = 'nodo_union_organico'
    return obj


def clean_mesh(obj, min_verts=1500):
    """Elimina caras degeneradas y fragmentos sueltos (< min_verts vertices). Devuelve (islas_eliminadas, vertices)."""
    import bmesh
    bm = bmesh.new(); bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    seen = set(); small = []; n_isl = 0
    for v in bm.verts:
        if v.index in seen:
            continue
        comp = []; st = [v]
        while st:
            a = st.pop()
            if a.index in seen:
                continue
            seen.add(a.index); comp.append(a)
            st += [e.other_vert(a) for e in a.link_edges if e.other_vert(a).index not in seen]
        if len(comp) < min_verts:
            small += comp; n_isl += 1
    if small:
        bmesh.ops.delete(bm, geom=small, context='VERTS')
    # reparacion manifold: aristas compartidas por >2 caras (puntas de aguja colapsadas por el suavizado)
    for _ in range(4):
        bad = [e for e in bm.edges if len(e.link_faces) > 2]
        if not bad:
            break
        faces = list({f for e in bad for f in e.link_faces})
        bmesh.ops.delete(bm, geom=faces, context='FACES')
        loose = [v for v in bm.verts if not v.link_faces]
        if loose:
            bmesh.ops.delete(bm, geom=loose, context='VERTS')
        bnd = [e for e in bm.edges if e.is_boundary]
        if bnd:
            bmesh.ops.holes_fill(bm, edges=bnd, sides=12)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(obj.data); bm.free(); obj.data.update()
    return n_isl, len(small)
