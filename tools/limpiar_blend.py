"""Quita datos huérfanos (materiales/mallas sin uso) de un .blend y lo guarda sobre sí mismo.
Uso: blender -b modelos/EYEBORG.blend -P tools/limpiar_blend.py"""
import bpy
n = 0
for m in [m for m in bpy.data.materials if m.users == 0]: bpy.data.materials.remove(m); n += 1
for m in [m for m in bpy.data.meshes if m.users == 0]: bpy.data.meshes.remove(m); n += 1
if bpy.data.filepath: bpy.ops.wm.save_mainfile()
print('LIMPIEZA', n, 'datos huerfanos eliminados')
