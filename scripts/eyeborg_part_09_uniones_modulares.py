# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, sweep_ribbon, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Orejas, abrazaderas y anillos de referencia para desmontaje por módulos."""
def build():
    col = get_collection('EYEBORG_09_UNIONES', clear=True)
    m = set_materials()
    for s, side in ((1,'IZQ'),(-1,'DER')):
        # Patillas en el tramo de sien, sobre el eje del oído.
        lug = box_part('PATILLA_MODULAR_SIEN_'+side, (16,8,20), (s*93,2,25), col, material=m['blue_light'], bevel=2.2)
        mark_modular(lug, 'coliso longitudinal de ajuste; posicion definitiva segun prueba ergonomica')
        torus_part('ARO_TORNILLO_SIEN_'+side, 2.6, 0.9, (s*93,-2,28), col, material=m['dark'], rotation=(math.pi/2,0,0))
        # Punto de union hacia nuca.
        lug2 = box_part('PATILLA_MODULAR_NUCA_'+side, (14,8,18), (s*61,106,4), col, material=m['blue_light'], bevel=2.0)
        mark_modular(lug2, 'union a puente occipital; taladro final depende de tornilleria real')
        torus_part('ARO_TORNILLO_NUCA_'+side, 2.4, 0.8, (s*61,101.7,4), col, material=m['dark'], rotation=(math.pi/2,0,0))
    for o in col.objects:
        o.display_type = 'WIRE'; o.hide_render = True   # marcadores conceptuales: no alteran la silueta
    return col

if __name__ == "__main__":
    build()
