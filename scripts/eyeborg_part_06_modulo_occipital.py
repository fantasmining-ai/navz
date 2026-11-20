# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, sweep_ribbon, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Placa occipital externa y soportes de unión; geometría modular tipo escudo, no casco cerrado."""
def build():
    col = get_collection('EYEBORG_06_OCCIPITAL', clear=True)
    m = set_materials()
    panel = box_part('PLACA_OCCIPITAL_CENTRAL_96x66x8', (96,8,66), (0,132,-4), col,
                     material=m['blue'], bevel=6.0)
    panel['referencia_dimensional'] = '108x62x32 mm de volumen en V6; cara visible simplificada aquí a placa 96x66x8 (proporcion de la vista posterior azul)'
    mark_modular(panel, 'tapa posterior desmontable; revisar acceso real a electronica')
    return col

if __name__ == "__main__":
    build()
