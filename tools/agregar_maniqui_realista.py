"""Añade el maniquí realista (malla base CC0, escalada a las medidas) a un .blend de una versión archivada, SIN tocar la estructura.
Reemplaza cualquier maniquí previo (MANIQUI_*), asigna el material según el diseño (estructura / cromo / resina) y baja el suelo de estudio
si cortaría el cuello. Guarda sobre el mismo archivo.
Uso: blender -b versiones/<version>/modelos/<archivo>.blend -P tools/agregar_maniqui_realista.py"""
import bpy, os, sys, importlib.util
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sc_dir = os.path.join(root, 'scripts')
if sc_dir not in sys.path: sys.path.insert(0, sc_dir)
# 1) quitar maniquí previo (elipsoides o versión anterior)
for o in [o for o in bpy.data.objects if o.name.startswith('MANIQUI_')]:
    me = o.data; bpy.data.objects.remove(o, do_unlink=True)
    if me is not None and getattr(me, 'users', 1) == 0: bpy.data.meshes.remove(me)
# 2) construir el maniquí con la malla CC0 (módulo 14 actual)
spec = importlib.util.spec_from_file_location('m14', os.path.join(sc_dir, 'eyeborg_part_14_maniqui.py'))
m14 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m14)
m14.build()
# 3) material por diseño (solo los 3 materiales del maniquí; no se tocan los materiales de la estructura)
fn = os.path.basename(bpy.data.filepath).upper()
if 'CABLEADO' in fn:
    from _eyeborg_materials import plastic
    mate = 'MATE' in fn
    head = plastic('MANIQUI_ARCILLA', (0.82, 0.82, 0.84, 1) if mate else (0.30, 0.31, 0.33, 1), 0.55, grain=0.02)
    scl = plastic('OJO_ESCLERA_SATINADA', (0.82, 0.80, 0.76, 1), 0.22); iris = plastic('OJO_IRIS_PINTADO', (0.11, 0.07, 0.035, 1), 0.18)
    for o in bpy.data.objects:
        if not o.name.startswith('MANIQUI_'): continue
        mt = scl if 'ESCLERA' in o.name else (iris if 'IRIS' in o.name else head)
        o.data.materials.clear(); o.data.materials.append(mt)
# 4) el suelo de estudio no debe cortar cuello y hombros (llegan a z = -236 mm)
fl = bpy.data.objects.get('SUELO_ESTUDIO')
if fl is not None and fl.location.z > -262: fl.location.z = -262
# 5) limpiar huérfanos y guardar
for m in [m for m in bpy.data.materials if m.users == 0]: bpy.data.materials.remove(m)
for m in [m for m in bpy.data.meshes if m.users == 0]: bpy.data.meshes.remove(m)
bpy.ops.wm.save_mainfile()
print('MANIQUI_REALISTA_OK', os.path.basename(bpy.data.filepath))
