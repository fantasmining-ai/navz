"""Auditoria estructural de un .blend EYEBORG.
Uso: blender -b modelos/EYEBORG.blend -P tools/auditar.py   (imprime un informe 'AUD ...')"""
import bpy, bmesh, math, random, re
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def P(*a): print('AUD', *a)

sc = bpy.context.scene
P('escena', sc.name, 'motor', sc.render.engine, 'unidades', sc.unit_settings.length_unit, sc.unit_settings.scale_length)
objs = list(bpy.data.objects)
P('objetos', len(objs), 'colecciones', len(bpy.data.collections), 'mallas', len(bpy.data.meshes), 'materiales', len(bpy.data.materials))
# duplicados .001 y huerfanos
dups = [o.name for o in objs if re.search(r'\.\d{3}$', o.name)]
P('duplicados_.001', len(dups), dups[:6])
orph_m = [m.name for m in bpy.data.meshes if m.users == 0]
orph_mat = [m.name for m in bpy.data.materials if m.users == 0]
P('mallas_huerfanas', len(orph_m), 'materiales_sin_uso', len(orph_mat), orph_mat[:8])
# materiales: objetos mesh sin material visible en render
nomat = [o.name for o in objs if o.type in ('MESH', 'CURVE') and not o.hide_render and not any(s.material for s in o.material_slots)]
P('objetos_renderizables_sin_material', len(nomat), nomat[:10])
# camara activa y luces
P('camara_activa', sc.camera.name if sc.camera else None, 'camaras', [o.name for o in objs if o.type == 'CAMERA'], 'luces', len([o for o in objs if o.type == 'LIGHT']))

# malla principal
f = None
for o in objs:
    if o.name.startswith('EYEBORG_FUSION') and o.type == 'MESH':
        f = o
if f is None:
    P('SIN EYEBORG_FUSION'); raise SystemExit
me = f.data
bm = bmesh.new(); bm.from_mesh(me)
bm.edges.ensure_lookup_table()
nm_e = [e for e in bm.edges if not e.is_manifold]
loose_v = [v for v in bm.verts if not v.link_edges]
zero = [fc for fc in bm.faces if fc.calc_area() < 1e-6]
P('FUSION caras', len(bm.faces), 'vertices', len(bm.verts), 'aristas_no_manifold', len(nm_e), 'vertices_sueltos', len(loose_v), 'caras_area0', len(zero))
vol = bm.calc_volume(signed=True)
P('volumen_mm3', round(vol, 1), '(negativo = normales invertidas)')
ls = [e.calc_length() for e in bm.edges]
P('arista_mm min/media/max', round(min(ls), 3), round(sum(ls) / len(ls), 3), round(max(ls), 3))
bb = [f.matrix_world @ Vector(c) for c in f.bound_box]
dim = [max(v[i] for v in bb) - min(v[i] for v in bb) for i in range(3)]
P('dimensiones_mm', [round(d, 1) for d in dim])
# islas conectadas
seen = set(); islands = 0
for v in bm.verts:
    if v.index in seen: continue
    islands += 1; stack = [v]
    while stack:
        a = stack.pop()
        if a.index in seen: continue
        seen.add(a.index)
        stack += [e.other_vert(a) for e in a.link_edges if e.other_vert(a).index not in seen]
P('islas_conectadas', islands)
# espesor de pared: rayo hacia dentro desde puntos al azar
bm.faces.ensure_lookup_table(); bm.normal_update()
tree = BVHTree.FromBMesh(bm)
random.seed(1); th = []
for fc in random.sample(list(bm.faces), min(6000, len(bm.faces))):
    o = fc.calc_center_median() - fc.normal * 0.02
    hit = tree.ray_cast(o, -fc.normal, 60.0)
    if hit[0] is not None: th.append(hit[3])
th.sort()
if th:
    q = lambda p: round(th[int(p * (len(th) - 1))], 2)
    P('espesor_mm p1/p5/mediana/p95', q(0.01), q(0.05), q(0.5), q(0.95), 'muestras', len(th))
    P('pct_espesor<1.2mm', round(100 * sum(1 for t in th if t < 1.2) / len(th), 1), 'pct_espesor<2.0mm', round(100 * sum(1 for t in th if t < 2.0) / len(th), 1))
bm.free()
P('FIN')
