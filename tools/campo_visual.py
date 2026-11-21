"""Oclusión del campo visual por la estructura. Lanza rayos desde cada ojo y mide qué % es bloqueado por EYEBORG_FUSION.
Uso: blender -b modelos/EYEBORG.blend -P tools/campo_visual.py
Ojos: centro de la córnea (x = ±IPD/2). Zonas: central ±30°, media ±50°, periférica ±70° (horizontal) y -40..+30° (vertical)."""
import bpy, math, json, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(root, 'scripts', 'eyeborg_config.json'), encoding='utf-8'))
L = cfg.get('landmarks', {})
ipd = cfg['anthropometry']['ipd_mm']
eye_z = L.get('eye_center_z', 5.0); cornea_y = L.get('cornea_apex_y', -97.0)
f = next(o for o in bpy.data.objects if o.name.startswith('EYEBORG_FUSION'))
dg = bpy.context.evaluated_depsgraph_get(); bvh = BVHTree.FromObject(f, dg)
def zona(az, el):
    a = max(abs(az), abs(el) * 1.0)
    return 'central' if a <= 30 else ('media' if a <= 50 else 'periferica')
dbg = []
res = {'central': [0, 0], 'media': [0, 0], 'periferica': [0, 0], 'ventana_ranura': [0, 0]}
for sgn in (-1, 1):
    o = Vector((sgn * ipd / 2.0, cornea_y, eye_z))
    for az in range(-70, 71, 2):
        for el in range(-40, 31, 2):
            # azimut hacia afuera positivo; direccion de mirada = -Y
            x = math.sin(math.radians(az)) * sgn; y = -math.cos(math.radians(az)); z = math.tan(math.radians(el))
            d = Vector((x, y, z)).normalized()
            hit = bvh.ray_cast(o, d, 400.0)[0]
            k = zona(az, el); res[k][1] += 1
            if hit is not None: res[k][0] += 1
            if abs(el) <= 12 and abs(az) <= 30:      # ventana de la ranura (48x12 mm a ~15 mm de la cornea)
                res['ventana_ranura'][1] += 1
                if hit is not None:
                    res['ventana_ranura'][0] += 1
                    dbg.append((round(hit.x), round(hit.y), round(hit.z)))
for k, (b, n) in res.items():
    print('CAMPO', k, 'bloqueado_%', round(100.0 * b / n, 1), 'rayos', n)
import collections
print('CAMPO_HITS_VENTANA', collections.Counter((round(h[0]/10)*10, round(h[1]/10)*10, round(h[2]/10)*10) for h in dbg).most_common(6))
print('CAMPO_OK')
