# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Barra posterior inferior que pasa bajo la placa occipital (la referencia no tiene arcos superiores)."""
def build():
    col = get_collection('EYEBORG_07_ARCOS_POSTERIORES', clear=True)
    m = set_materials()
    strap('BARRA_POSTERIOR_INFERIOR', [(-54,118,-14),(-34,128,-27),(0,134,-31),(34,128,-27),(54,118,-14)],
          (14,16,14), 5.5, col, material=m['blue'], xyz=True, center=(0,0,0), cap=(0.03,0.03))
    return col

if __name__ == "__main__":
    build()
