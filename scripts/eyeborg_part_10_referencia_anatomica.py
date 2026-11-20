# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, sweep_ribbon, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Referencia anatómica elipsoidal de blockout; no es un escaneo ni se imprime."""
def build():
    col = get_collection('EYEBORG_00_REFERENCIA', clear=True)
    from _eyeborg_core import create_head_reference
    dims = tuple(ANTHROPOMETRY['head_envelope_xyz_mm'])
    head = create_head_reference('REF_CABEZA_BLOCKOUT', dims, col, clearance=0)
    head['estado_medidas'] = ANTHROPOMETRY.get('head_envelope_status', 'verificado por el usuario')
    head['fuente_medidas'] = 'Medidas anatómicas verificadas por el usuario; el objeto es una simplificación CAD, no un escaneo 3D'
    gap = create_head_reference('REF_ENVOLVENTE_AIRE_6mm', dims, col, clearance=FIT['head_clearance_mm'])
    gap['estado_medidas'] = 'envolvente CAD derivada de dimensiones verificadas por el usuario; no escaneo 3D'
    return col

if __name__ == "__main__":
    build()
