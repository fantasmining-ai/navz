# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, box_part, cylinder_part, torus_part, mark_modular, visor_point
from _eyeborg_config import *

"""Puente de camara (barra frontal superior) y brazos tipo mariposa hacia las diagonales principales."""
def build():
    col = get_collection('EYEBORG_02_CORONA_PUENTES', clear=True)
    m = set_materials()
    strap('BARRA_PUENTE_CAMARA', [(-26,-114,43),(-13,-116,44.5),(0,-116.5,45),(13,-116,44.5),(26,-114,43)],
          (13,15,13), 7.0, col, material=m['blue'], xyz=True, center=(0,-10,0), cap=(0.03,0.03))
    for s, side in ((1,'IZQ'),(-1,'DER')):
        strap('BRAZO_MARIPOSA_'+side, [(24,-114,43),(38,-114,47),(52,-108,50),(66,-92,47),(73,-79,45)],
              [(0,13),(0.5,12),(1,9)], 5.5, col, material=m['blue_light'], mirror=(s<0),
              xyz=True, center=(0,-10,0), cap=(0.03,0.05))
        # puntal de camara: baja desde la barra al borde superior del visor (el visor queda libre de la linea de vision)
        vt = visor_point(s*14.0, CONFIG['visor']['z_center_mm'] + CONFIG['visor']['height_mm']/2.0 - 2.0, CONFIG['visor'])[0]
        strap('PUNTAL_CAMARA_'+side, [(s*14.0,-116,42),(s*14.0,float(vt.y)+1.0,float(vt.z))], 7.0, 4.0, col, material=m['blue'],
              xyz=True, nhint=(1,0,0), clear=False, cap=(0.1,0.1), steps=4)
    return col

if __name__ == "__main__":
    build()
