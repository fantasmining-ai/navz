# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Puente de camara (barra frontal superior) y brazos tipo mariposa hacia las diagonales principales."""
def build():
    col = get_collection('EYEBORG_02_CORONA_PUENTES', clear=True)
    m = set_materials()
    strap('BARRA_PUENTE_CAMARA', [(-26,-114,43),(-13,-116,44.5),(0,-116.5,45),(13,-116,44.5),(26,-114,43)],
          (13,15,13), 7.0, col, material=m['blue'], xyz=True, center=(0,-10,0), cap=(0.03,0.03))
    for s, side in ((1,'IZQ'),(-1,'DER')):
        strap('BRAZO_MARIPOSA_'+side, [(24,-114,43),(38,-114,47),(52,-111,50),(64,-104,46)],
              [(0,13),(0.5,12),(1,9)], 5.5, col, material=m['blue_light'], mirror=(s<0),
              xyz=True, center=(0,-10,0), cap=(0.03,0.05))
        strap('BRAZO_INFERIOR_'+side, [(20,-116,38),(30,-114,28),(40,-111,22)],
              [(0,10),(1,6)], 5.0, col, material=m['blue_light'], mirror=(s<0),
              xyz=True, center=(0,-10,0), cap=(0.03,0.2))
    return col

if __name__ == "__main__":
    build()
