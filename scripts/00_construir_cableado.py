# -*- coding: utf-8 -*-
"""Diseño 2: EYEBORG con cableado discreto simulado + materiales + estudio. Uso:
blender -b --factory-startup -P scripts/00_construir_cableado.py -- salida.blend [cromo|mate]"""
import os, sys, runpy
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import bpy
runpy.run_path(os.path.join(ROOT, '00_construir_conjunto.py'), run_name='__main__', init_globals={'EYEBORG_SKIP_FINISH': True})   # diseño 1 completo
import importlib.util
def _load(fn, nm):
    spec = importlib.util.spec_from_file_location(nm, os.path.join(ROOT, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
cab = _load('eyeborg_part_13_cableado.py', 'eyeborg_cab')
cab.build()
from _eyeborg_materials import build_all
for _n in ('Cube', 'Light', 'Camera'):
    _o = bpy.data.objects.get(_n)
    if _o: bpy.data.objects.remove(_o, do_unlink=True)
from _eyeborg_studio import assign_materials, studio
_args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
acabado = _args[1] if len(_args) > 1 else 'cromo'      # 'cromo' (diseño 2) | 'mate' (diseño 3)
M = build_all(acabado)
assign_materials(M)
studio(M, acabado)
_def = 'EYEBORG_CABLEADO.blend' if acabado == 'cromo' else 'EYEBORG_CABLEADO_MATE.blend'
out = _args[0] if _args else os.path.join(ROOT, '..', 'modelos', _def)
for _m in [m for m in bpy.data.materials if m.users == 0]:     # sin materiales huerfanos (p. ej. el 'Material' por defecto)
    bpy.data.materials.remove(_m)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
print('EYEBORG_CABLEADO (%s) guardado en' % acabado, os.path.abspath(out))
