# -*- coding: utf-8 -*-
"""Aplica el azul vivo de la v1 (con textura) al EYEBORG_FUSION de un .blend del diseño 1 y lo guarda.
Uso: blender -b modelos/EYEBORG.blend -P tools/aplicar_azul_v1.py"""
import os, sys, bpy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
import _eyeborg_studio as S
m = S.material_azul_v1()
f = bpy.data.objects['EYEBORG_FUSION']
f.data.materials.clear(); f.data.materials.append(m)
for p in f.data.polygons: p.material_index = 0
bpy.ops.wm.save_mainfile()
print('azul v1 aplicado')
