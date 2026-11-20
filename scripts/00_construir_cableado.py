# -*- coding: utf-8 -*-
"""Diseño 2: EYEBORG con cableado discreto simulado + materiales + estudio. Uso:
blender -b --factory-startup -P scripts/00_construir_cableado.py -- salida.blend"""
import os, sys, runpy
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import bpy
runpy.run_path(os.path.join(ROOT, '00_construir_conjunto.py'), run_name='__main__')   # diseño 1 completo
import importlib.util
def _load(fn, nm):
    spec = importlib.util.spec_from_file_location(nm, os.path.join(ROOT, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
cab = _load('eyeborg_part_13_cableado.py', 'eyeborg_cab')
cab.build()
from _eyeborg_materials import build_all
from _eyeborg_studio import assign_materials, studio
M = build_all()
assign_materials(M)
studio(M)
out = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else os.path.join(ROOT, '..', 'output', 'EYEBORG_CABLEADO.blend')
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
print('EYEBORG_CABLEADO guardado en', os.path.abspath(out))
