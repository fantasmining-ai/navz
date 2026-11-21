"""Simulación de proporciones: ¿qué rango de caras tolera el diseño (fijo)?
Escala el maniquí (ancho X, profundidad Y, alto Z) y el IPD, y mide para cada variante:
  - alineación ojo–ranura (mm), distancia córnea–visor, holgura mínima a la piel (fuera de anclajes),
  - separación de cada grupo de almohadillas respecto a la piel (+ flota / − penetra), campo libre por la ranura.
Uso: blender -b modelos/EYEBORG.blend -P tools/simulacion_proporciones.py
Salida: simulaciones/proporciones.md, datos_proporciones.json, proporciones.jpg (hoja de variantes, vista frontal)."""
import bpy, math, json, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, 'simulaciones'); os.makedirs(out, exist_ok=True); fr = os.path.join(out, '_frames_prop'); os.makedirs(fr, exist_ok=True)
cfg = json.load(open(os.path.join(root, 'scripts', 'eyeborg_config.json'), encoding='utf-8'))
LM = cfg['landmarks']; V = cfg['visor']; ipd = cfg['anthropometry']['ipd_mm']
man = bpy.data.objects['MANIQUI_CUERPO']
eyes = [o for o in bpy.data.objects if o.name.startswith('MANIQUI_OJO_')]
pads = sorted([o for o in bpy.data.objects if o.name.startswith('PAD_')], key=lambda o: o.name)
fus = next(o for o in bpy.data.objects if o.name.startswith('EYEBORG_FUSION'))
def coords(o):
    a = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get('co', a); return a.reshape(-1, 3)
base = {o.name: coords(o) for o in [man] + eyes}
def apply(sx, sy, sz):
    for o in [man] + eyes:
        o.data.vertices.foreach_set('co', (base[o.name] * np.array([sx, sy, sz])).ravel()); o.data.update()
    bpy.context.view_layer.update()
dg0 = bpy.context.evaluated_depsgraph_get()
fbvh = BVHTree.FromObject(fus, dg0)
fv = coords(fus); fv_s = fv[::3]
pad_pts = {p.name: np.array([[*(p.matrix_world @ v.co)] for v in p.data.vertices]) for p in pads}
allpad = np.concatenate(list(pad_pts.values()))

# variantes: nombre, sx, sy, sz (escalas de la cabeza respecto a las medidas verificadas)
VAR = [('base (medidas del usuario)', 1, 1, 1), ('cabeza estrecha −6 % X', .94, 1, 1), ('cabeza ancha +6 % X', 1.06, 1, 1),
       ('cabeza corta −5 % Y', 1, .95, 1), ('cabeza larga +5 % Y', 1, 1.05, 1), ('cabeza baja −5 % Z', 1, 1, .95), ('cabeza alta +5 % Z', 1, 1, 1.05),
       ('IPD 58 mm', 58 / ipd, 1, 1), ('IPD 72 mm', 72 / ipd, 1, 1), ('pequeña (−5 % X,Y,Z)', .95, .95, .95), ('grande (+5 % X,Y,Z)', 1.05, 1.05, 1.05)]
datos = []
for nombre, sx, sy, sz in VAR:
    apply(sx, sy, sz)
    dg = bpy.context.evaluated_depsgraph_get(); sbvh = BVHTree.FromObject(man, dg)
    ce = {s: Vector((s * ipd / 2.0 * sx, LM['cornea_apex_y'] * sy, LM['eye_center_z'] * sz)) for s in (1, -1)}
    # alineación ojo-ranura y distancia a la estructura
    dx = ipd / 2.0 * sx - V['slit']['center_x_mm']; dz = LM['eye_center_z'] * sz - V['slit']['z_mm']
    margen_x = V['slit']['length_mm'] / 2.0 - 15.0 - abs(dx)          # fisura palpebral ~30 mm de largo
    margen_z = V['slit']['height_mm'] / 2.0 - 5.0 - abs(dz)           # fisura ~10 mm de alto
    dist_c = min(fbvh.find_nearest(ce[s])[3] for s in (1, -1))
    # campo libre por la ranura
    blk = 0; tot = 0
    for s in (1, -1):
        for az in range(-30, 31, 3):
            for el in range(-12, 13, 3):
                d = Vector((math.sin(math.radians(az)) * s, -math.cos(math.radians(az)), math.tan(math.radians(el)))).normalized()
                tot += 1
                if fbvh.ray_cast(ce[s], d, 400.0)[0] is not None: blk += 1
    # holgura minima a la piel fuera de anclajes
    mn = 1e9; dentro = 0
    for p in fv_s:
        if ((allpad - p) ** 2).sum(1).min() < 81.0: continue
        loc, nrm, idx, dist = sbvh.find_nearest(Vector(p))
        g = dist if (Vector(p) - loc).dot(nrm) >= 0 else -dist
        if g < 0: dentro += 1
        mn = min(mn, g)
    # almohadillas: separacion con signo respecto a la piel (+ flota, - penetra)
    grp = {}
    for n, P in pad_pts.items():
        sg = []
        for q in P:
            loc, nrm, idx, dist = sbvh.find_nearest(Vector(q)); sg.append(dist if (Vector(q) - loc).dot(nrm) >= 0 else -dist)
        grp.setdefault(n.split('_')[1], []).append((min(sg)))
    pad_g = {k: round(float(np.mean(v)), 1) for k, v in grp.items()}
    datos.append({'variante': nombre, 'sx': round(sx, 3), 'sy': round(sy, 3), 'sz': round(sz, 3), 'desalineo_x_mm': round(dx, 1), 'desalineo_z_mm': round(dz, 1),
                  'margen_ranura_x_mm': round(margen_x, 1), 'margen_ranura_z_mm': round(margen_z, 1), 'cornea_a_estructura_mm': round(dist_c, 1),
                  'holgura_min_piel_mm': round(mn, 1), 'vertices_dentro_piel': dentro, 'ventana_ranura_bloqueada_pct': round(100.0 * blk / tot, 1), 'almohadillas_mm': pad_g})
    print('PROP', nombre, round(dist_c, 1), round(mn, 1), pad_g)
json.dump(datos, open(os.path.join(out, 'datos_proporciones.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
def estado(d):
    ok = d['holgura_min_piel_mm'] >= 6 and d['cornea_a_estructura_mm'] >= 15 and d['margen_ranura_x_mm'] >= 0 and d['margen_ranura_z_mm'] >= 0 and d['vertices_dentro_piel'] == 0
    pad_ok = all(-2.5 <= v <= 3.0 for v in d['almohadillas_mm'].values())
    return ('✔ ajusta' if ok and pad_ok else ('⚠ ajusta con almohadillas ajustables' if ok else '✘ no ajusta'))
md = ['# Simulación de proporciones\n',
      'El diseño es **fijo**; se varía el tamaño de la cabeza y el IPD (escalas sobre las medidas verificadas del usuario) para ver **cuánto tolera** y qué debe ser **ajustable**. Maniquí de la malla base CC0, **no** un escaneo.\n',
      '- *Desalineo ojo–ranura*: distancia entre el centro del ojo y el centro de la ranura (48 × 14 mm); *margen* = holgura que queda respecto a la fisura palpebral (≈ 30 × 10 mm); negativo = el ojo se sale de la ranura.',
      '- *Almohadillas*: separación media del grupo respecto a la piel: **+ flota** (no apoya), **− penetra** (aprieta). Con almohadillas EVA de 5 mm se toleran ≈ −2.5 a +3 mm.\n',
      '| Variante | Desalineo X / Z (mm) | Margen ranura X / Z (mm) | Córnea–estructura (mm) | Holgura mín. a piel (mm) | Ventana bloqueada | Almohadillas nariz / frente / oreja (mm) | Estado |',
      '| --- | --- | --- | --- | --- | --- | --- | --- |']
for d in datos:
    pg = d['almohadillas_mm']
    md.append('| %s | %.1f / %.1f | %.1f / %.1f | %.1f | %.1f | %.1f %% | %.1f / %.1f / %.1f | %s |' % (d['variante'], d['desalineo_x_mm'], d['desalineo_z_mm'], d['margen_ranura_x_mm'], d['margen_ranura_z_mm'],
        d['cornea_a_estructura_mm'], d['holgura_min_piel_mm'], d['ventana_ranura_bloqueada_pct'], pg.get('NASAL', 0), pg.get('FRONTAL', 0), pg.get('OREJA', 0), estado(d)))
open(os.path.join(out, 'proporciones.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
# hoja de variantes (vista frontal, workbench)
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x, sc.render.resolution_y = 420, 380
sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'OBJECT'
sc.world = sc.world or bpy.data.worlds.new('W'); sc.world.color = (0.6, 0.62, 0.66)
fus.color = (0.25, 0.75, 0.95, 1); man.color = (0.6, 0.6, 0.62, 1)
for o in eyes: o.color = (0.95, 0.95, 0.95, 1)
for p in pads: p.color = (0.05, 0.05, 0.06, 1)
for o in bpy.data.objects:
    if o.type in ('LIGHT',) or o.name.startswith(('REF_', 'SUELO')) or o.display_type == 'WIRE': o.hide_render = True
cd = bpy.data.cameras.new('PC'); cd.type = 'ORTHO'; cd.ortho_scale = 300; cam = bpy.data.objects.new('PC', cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, -900, 10); cam.rotation_euler = (math.pi / 2, 0, 0)
for i, (nombre, sx, sy, sz) in enumerate(VAR):
    apply(sx, sy, sz); sc.render.filepath = os.path.join(fr, 'v%02d.png' % i); bpy.ops.render.render(write_still=True)
apply(1, 1, 1)
print('PROP_OK')
