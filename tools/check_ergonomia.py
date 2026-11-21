"""Chequeo de holgura contra la envolvente de cabeza (elipsoide verificado por el usuario).
Uso: blender -b modelos/EYEBORG.blend -P tools/check_ergonomia.py"""
import bpy, bmesh, math
from mathutils import Vector
H = (82.5, 101.0, 107.5)          # semiejes cabeza 165x202x215
GAP = 6.0                         # holgura nominal cabeza-estructura (mm)
f = bpy.data.objects['EYEBORG_FUSION']
vs = [v.co for v in f.data.vertices]
def gap_mm(p):
    r = math.sqrt((p.x/H[0])**2 + (p.y/H[1])**2 + (p.z/H[2])**2)
    # distancia aproximada a la superficie del elipsoide a lo largo del gradiente
    g = math.sqrt((p.x/H[0]**2)**2 + (p.y/H[1]**2)**2 + (p.z/H[2]**2)**2)
    return (r*r - 1) / (2*g) if g > 1e-9 else 0.0
gs = [(gap_mm(p), p) for p in vs]
inside = [g for g in gs if g[0] < 0]
tight = [g for g in gs if 0 <= g[0] < GAP]
print('VERTICES', len(gs), 'dentro_de_cabeza', len(inside), 'holgura<%.0fmm' % GAP, len(tight))
if inside:
    w = min(inside, key=lambda g: g[0])
    print('PEOR_PENETRACION_mm', round(w[0],1), 'en', [round(c,1) for c in w[1]])
mn = min(gs, key=lambda g: g[0]); print('HOLGURA_MIN_mm', round(mn[0],1), [round(c,1) for c in mn[1]])
# ventana de oreja (68x52 mm) y eje de oido (y=+6, z=-18): libre en |x|>=70 alrededor
ear = [g for g in gs if abs(g[1].y-6) < 34 and abs(g[1].z+18) < 26 and g[1].x*g[1].x > 60**2 and g[0] < 0]
print('VERTICES_EN_VENTANA_OREJA', len(ear))
# ojos: distancia de la estructura al centro de la cornea de cada ojo (R2: >= 15 mm) y a la superficie del parpado
import json, os
import json as _j
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_C = _j.load(open(os.path.join(_root, 'scripts', 'eyeborg_config.json'), encoding='utf-8'))
_LM = _C['landmarks']; _LM_X = _C['anthropometry']['ipd_mm'] / 2.0
from mathutils.bvhtree import BVHTree as _B
_bm = bmesh.new(); _bm.from_mesh(f.data); _tree = _B.FromBMesh(_bm)
for sgn in (1, -1):
    cp = Vector((sgn * _LM_X, _LM['cornea_apex_y'], _LM['eye_center_z']))
    loc, nrm, idx, dist = _tree.find_nearest(cp)
    print('OJO_%s_DISTANCIA_MIN_A_ESTRUCTURA_mm' % ('IZQ' if sgn > 0 else 'DER'), round(dist, 1), [round(c, 1) for c in loc])
_bm.free()
# oreja: ventana 68x52 (z -44..8). Se cuentan vertices de estructura dentro de la ventana
ear_any = [p for p in vs if abs(p.y-6) < 34 and abs(p.z+18) < 26 and abs(p.x) > 60]
print('VERTICES_EN_VENTANA_OREJA_TOTAL', len(ear_any))
# maniqui esquematico (malla real MANIQUI_CUERPO): distancia de la estructura a la piel del maniqui
man = next((o for o in bpy.data.objects if o.name.startswith('MANIQUI_CUERPO')), None)
if man is not None:
    from mathutils.bvhtree import BVHTree
    dgm = bpy.context.evaluated_depsgraph_get()
    bvh = BVHTree.FromObject(man, dgm)
    # las almohadillas (PAD_*) son contactos de diseño: se excluyen los vertices a < 9 mm de una almohadilla
    pv = []
    for po in [o for o in bpy.data.objects if o.name.startswith('PAD_')]:
        pv += [po.matrix_world @ v.co for v in po.data.vertices]
    pbvh = None
    if pv:
        pb = bmesh.new()
        for q in pv: pb.verts.new(q)
        pb.verts.ensure_lookup_table()
        pbvh = None
    import numpy as _np
    pad_arr = _np.array([[q.x, q.y, q.z] for q in pv]) if pv else None
    dentro = 0; cerca = 0; mn_gap = 1e9; mn_p = None
    for p in vs:
        if pad_arr is not None and ((pad_arr - _np.array([p.x, p.y, p.z])) ** 2).sum(1).min() < 81.0:
            continue
        loc, nrm, idx, dist = bvh.find_nearest(p)
        if loc is None: continue
        sg = (p - loc).dot(nrm)
        gap = dist if sg >= 0 else -dist
        if gap < 0: dentro += 1
        elif gap < 4.0: cerca += 1
        if gap < mn_gap: mn_gap, mn_p = gap, p
    print('MANIQUI_VERTICES_DENTRO', dentro, 'a_menos_de_4mm', cerca, 'holgura_min_mm', round(mn_gap, 1), [round(c, 1) for c in mn_p])
    # anclajes: distancia de cada almohadilla a la piel (debe ser ~0: contacto)
    for po in sorted([o for o in bpy.data.objects if o.name.startswith('PAD_')], key=lambda o: o.name):
        dmin = min(bvh.find_nearest(po.matrix_world @ v.co)[3] for v in po.data.vertices)
        print('ANCLAJE', po.name, 'distancia_a_piel_mm', round(dmin, 2))
else:
    print('SIN MANIQUI_CUERPO')
print('CHECK OK')
