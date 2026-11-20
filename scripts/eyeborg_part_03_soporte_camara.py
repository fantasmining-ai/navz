# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, sweep_ribbon, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Módulo visual de cámara basado en el volumen completo del inventario más reciente."""
def build():
    col = get_collection('EYEBORG_03_CAMARA', clear=True)
    m = set_materials()
    # Caja exterior provisional: 46x34x35 mm; el volumen del módulo es 40x28x29 mm.
    case = CAMERA['blockout_case_outer_mm_xyz']
    board_xyz = COMPONENTS['esp32_cam_ai_thinker_complete']['size_mm_xyz']
    housing = box_part('CARCASA_CAMARA_PROVISIONAL', tuple(case), (0,-118,55), col,
                        material=m['dark'], bevel=3.0)
    housing['modulo_ref_mm'] = str(board_xyz) + ' mm; verificar orientación exacta'
    housing['cavidad_ref_mm'] = '42x30x31 estimada con 1 mm total por eje; todavía no es cavidad final'
    # La carcasa se muestra en alambre para que se vea la bolsa de la plataforma; no se renderiza.
    housing.display_type = 'WIRE'
    housing.hide_render = True
    # Plataforma de camara: placa plana bajo el pod; la bolsa y los agujeros se cortan en 12 tras la fusion.
    F = CONFIG['fasteners']
    plate = box_part('PLATAFORMA_CAMARA', tuple(F['camera_plate_mm_xyz']), tuple(F['camera_plate_center_mm']), col,
                     material=m['blue'], bevel=0)
    mark_modular(plate, 'plataforma de camara con bolsa; fijaciones provisionales')
    # Envolvente transparente de referencia para visualizar el espacio ocupado por la placa.
    board = box_part('REF_ESP32_CAM_COMPLETA', tuple(board_xyz), (0,-118,55), col,
                     material=m['ghost'], bevel=0, wire=True)
    board['no_imprimir'] = True
    # Lente orientada hacia el frente (-Y); el aro es un detalle visual, no un taladro funcional.
    torus_part('ARO_LENTE_CAMARA', 4.1, 1.0, (0,-134.4,56), col, material=m['light'], rotation=(math.pi/2,0,0))
    cylinder_part('LENTE_REFERENCIA_D6', 3.0, 1.8, (0,-134.7,56), col, material=m['dark'], rotation=(math.pi/2,0,0))
    # Orejas de montaje laterales con taladros representados por aros independientes.
    for s, side in ((1,'IZQ'),(-1,'DER')):
        tab = box_part('OREJA_CAMARA_'+side, (9,5,12), (s*26,-116,48), col, material=m['blue'], bevel=1.4)
        mark_modular(tab, 'dos fijaciones simetricas; diametro final pendiente de tornillo seleccionado')
        torus_part('ARO_FIJACION_CAMARA_'+side, 2.2, 0.8, (s*26,-119,50), col, material=m['light'], rotation=(math.pi/2,0,0))
    return col

if __name__ == "__main__":
    build()
