# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Punta frontal con ranura central: puente inferior cerrado y dos paredes verticales que suben al puente de camara."""
def build():
    col = get_collection('EYEBORG_01_COLUMNA_FRONTAL', clear=True)
    m = set_materials()
    tip = strap('HORQUILLA_PUNTA', [(-15,-122,-53),(-7,-125,-56),(0,-126,-57),(7,-125,-56),(15,-122,-53)],
                (13,15,13), 6.5, col, material=m['blue'], xyz=True, center=(0,-30,0), cap=(0.1,0.1))
    mark_modular(tip, 'solapa de union en punta; revisar antes de fabricar')
    for s, side in ((1,'IZQ_USUARIO'),(-1,'DER_USUARIO')):
        strap('PARED_RANURA_'+side, [(10,-122,-52),(20,-120,-34),(25,-119,-12),(24,-118,10),(20,-117,30),(17,-116,44)],
              [(0,11),(0.5,15),(1,14)], [(0,7),(1,6)], col, material=m['blue'], mirror=(s<0),
              xyz=True, center=(0,-30,0), cap=(0.04,0.04))
    return col

if __name__ == "__main__":
    build()
