# -*- coding: utf-8 -*-
"""Construye el conjunto EYEBORG modular. Blender 4.x. Ejecutar desde este archivo externo."""
import os, sys, importlib.util
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import bpy
from _eyeborg_core import scene_mm, clear_eyeborg
scene_mm()
clear_eyeborg()

def load_module(filename, module_name):
    path = os.path.join(ROOT, filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

mods = [
  ('eyeborg_part_10_referencia_anatomica.py','eyeborg_ref'),
  ('eyeborg_part_01_columna_frontal.py','eyeborg_spine'),
  ('eyeborg_part_02_corona_y_puentes.py','eyeborg_crown'),
  ('eyeborg_part_03_soporte_camara.py','eyeborg_camera'),
  ('eyeborg_part_04_rama_izquierda.py','eyeborg_left'),
  ('eyeborg_part_05_rama_derecha.py','eyeborg_right'),
  ('eyeborg_part_06_modulo_occipital.py','eyeborg_occipital'),
  ('eyeborg_part_07_arcos_occipitales.py','eyeborg_rear_arches'),
  ('eyeborg_part_08_portacomponentes.py','eyeborg_carrier'),
  ('eyeborg_part_09_uniones_modulares.py','eyeborg_joints'),
  ('eyeborg_part_11_fusion.py','eyeborg_fusion'),
  ('eyeborg_part_12_agujeros.py','eyeborg_holes'),
]
for filename, name in mods:
    mod = load_module(filename, name)
    if name == 'eyeborg_left':
         mod.build_side(1, 'IZQUIERDA')
    elif name == 'eyeborg_right':
         mod.build_side(-1, 'DERECHA')
    else:
         mod.build()

# Enmarcar visualmente la escena en el viewport.
for area in bpy.context.screen.areas if bpy.context.screen else []:
    if area.type == 'VIEW_3D':
        area.spaces.active.region_3d.view_distance = 390
        area.spaces.active.region_3d.view_location = (0,0,0)
if not globals().get('EYEBORG_SKIP_FINISH'):
    from _eyeborg_studio import acabado_diseno1
    acabado_diseno1()
print('EYEBORG: conjunto modular creado. Las piezas REF_* son envolventes y NO se imprimen.')
