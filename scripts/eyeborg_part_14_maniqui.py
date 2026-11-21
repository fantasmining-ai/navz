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

def build_procedural():
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

def build_base():
    """Ruta B: cabeza real de la malla base CC0 (Human Base Meshes v1.4.1), escalada a las medidas del usuario."""
    import numpy as np
    M = CONFIG['mannequin']; B = M['base_mesh']
    path = os.path.join(os.path.dirname(_SCRIPT_DIR), B['asset'])
    names = [B['objetos']['cuerpo']] + B['objetos']['esclera'] + B['objetos']['iris']
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in names if n in src.objects]
    col = get_collection('EYEBORG_14_MANIQUI', clear=True)
    mat_ = plastic('MANIQUI_MATE', (0.16, 0.16, 0.17, 1), 0.5)
    esc_m = plastic('OJO_ESCLERA', (0.80, 0.78, 0.74, 1), 0.25)
    iris_m = plastic('OJO_IRIS', (0.10, 0.06, 0.03, 1), 0.2)
    sc = B['escala_mm_por_m']; cx, cy, cz = B['centro_x_m'], B['centro_y_m'], B['centro_z_m']
    alias = {B['objetos']['cuerpo']: ('MANIQUI_CUERPO', mat_)}
    for k, n in enumerate(B['objetos']['esclera']): alias[n] = ('MANIQUI_OJO_ESCLERA_' + ('L' if k == 0 else 'R'), esc_m)
    for k, n in enumerate(B['objetos']['iris']): alias[n] = ('MANIQUI_OJO_IRIS_' + ('L' if k == 0 else 'R'), iris_m)
    for o in dst.objects:
        me = o.data; n_ = len(me.vertices)
        a = np.empty(n_ * 3); me.vertices.foreach_get('co', a); a = a.reshape(-1, 3)
        a[:, 0] = (a[:, 0] - cx) * sc[0]; a[:, 1] = (a[:, 1] - cy) * sc[1]; a[:, 2] = (a[:, 2] - cz) * sc[2]
        me.vertices.foreach_set('co', a.ravel()); me.update()
        nuevo, mt = alias[o.name]
        o.name = nuevo; o.data.name = nuevo + '_MESH'; col.objects.link(o)
        me.materials.clear(); me.materials.append(mt)
        for p_ in me.polygons: p_.use_smooth = True
        o['nota'] = 'maniqui con malla base CC0 (Blender Studio); escalado a las medidas del usuario; no es un escaneo de la persona'
    from _eyeborg_core import set_head_mesh
    set_head_mesh(bpy.data.objects['MANIQUI_CUERPO'])      # la ergonomia se calcula contra la piel real
    return col

def build():
    B = CONFIG['mannequin'].get('base_mesh', {})
    if B.get('activo') and os.path.isfile(os.path.join(os.path.dirname(_SCRIPT_DIR), B.get('asset', ''))):
        return build_base()
    return build_procedural()

if __name__ == "__main__":
    build()
