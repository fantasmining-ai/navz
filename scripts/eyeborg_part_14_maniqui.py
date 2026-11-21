# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection
from _eyeborg_config import *
from mathutils import Vector, Matrix
from _eyeborg_materials import plastic

"""Maniqui esquematico (NO escaneo): cráneo 165x202x215 mm con rasgos faciales (cejas, párpados, nariz, labios, mejillas, orejas),
cuello de 380 mm de circunferencia y busto, fundidos en UNA malla organica. Parametros en eyeborg_config.json -> mannequin.
Sirve para ver el ajuste y el corredor nasal; se puede ocultar (coleccion EYEBORG_14_MANIQUI) sin afectar el diseño."""
def _part(name, c, r, col):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=28, radius=1.0,
                              matrix=Matrix.Translation(Vector(c)) @ Matrix.Diagonal(Vector((r[0], r[1], r[2], 1.0))))
    me = bpy.data.meshes.new(name + '_TMP'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); return o

def build():
    import bmesh
    from _eyeborg_core import fuse_objects
    M = CONFIG['mannequin']
    col = get_collection('EYEBORG_14_MANIQUI', clear=True)
    mat_ = plastic('MANIQUI_MATE', (0.16, 0.16, 0.17, 1), 0.5)
    parts = []
    ipd_half = ANTHROPOMETRY['ipd_mm'] / 2.0
    for p in M['parts']:
        c = list(p['c'])
        if p.get('ipd_x'): c[0] = ipd_half          # ojos separados por la IPD verificada (65 mm)
        parts.append(_part(p['name'], c, p['r'], col))
        if p.get('mirror'):
            parts.append(_part(p['name'] + '_esp', (-c[0], c[1], c[2]), p['r'], col))
    nk = M['neck']; neck_r = ANTHROPOMETRY['neck_circumference_mm'] / (2 * math.pi)   # 380 mm -> r 60.5
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=48, radius1=neck_r, radius2=neck_r, depth=nk['depth'],
                          matrix=Matrix.Translation(Vector(nk['c'])))
    me = bpy.data.meshes.new('cuello_TMP'); bm.to_mesh(me); bm.free()
    nobj = bpy.data.objects.new('cuello', me); col.objects.link(nobj); parts.append(nobj)
    parts.append(_part('busto', M['bust']['c'], M['bust']['r'], col))
    body = fuse_objects('MANIQUI_CUERPO', parts, col, material=mat_, voxel_mm=M['voxel_mm'], smooth_iters=M['smooth_iterations'])
    for o in parts:
        me_ = o.data; bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me_)
    body['nota'] = 'maniqui esquematico; no es un escaneo. Cuello: radio de la circunferencia verificada (380 mm)'
    return col

if __name__ == "__main__":
    build()
