# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Fusion organica visual: une la estructura azul en una malla continua (como la referencia). No toca los originales."""
FUSE = ['EYEBORG_01_COLUMNA_FRONTAL','EYEBORG_02_CORONA_PUENTES','EYEBORG_04_RAMA_IZQUIERDA',
        'EYEBORG_04_RAMA_DERECHA','EYEBORG_06_OCCIPITAL','EYEBORG_07_ARCOS_POSTERIORES','EYEBORG_15_VISOR']
def build():
    from _eyeborg_core import fuse_objects
    cfg = CONFIG.get('fusion', {})
    col = get_collection('EYEBORG_11_FUSION_ORGANICA', clear=True)
    m = set_materials()
    objs = []
    for name in FUSE:
        c = bpy.data.collections.get(name)
        if c: objs += [o for o in c.objects if o.type == 'MESH' and not o.name.startswith(('REF_', 'PAD_'))]
    cam = bpy.data.collections.get('EYEBORG_03_CAMARA')
    if cam: objs += [o for o in cam.objects if o.name.startswith('PLATAFORMA_')]
    fused = fuse_objects('EYEBORG_FUSION', objs, col, material=m['blue'],
                         voxel_mm=cfg.get('voxel_mm', 1.6), smooth_iters=cfg.get('smooth_iterations', 8))
    # Los originales siguen como piezas modulares; se ocultan en viewport/render para ver la fusion.
    for o in objs:
        o.hide_viewport = True; o.hide_render = True
    return col

if __name__ == "__main__":
    build()
