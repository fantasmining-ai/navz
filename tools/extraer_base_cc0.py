"""Extrae cabeza + ojos de 'Human Base Meshes v1.4.1' (Blender Studio, CC0) a assets/maniqui/cabeza_base_cc0.blend.
Uso: blender -b --disable-autoexec <human_base_meshes_bundle.blend> -P tools/extraer_base_cc0.py -- <salida.blend>
Fuente: https://download.blender.org/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.4.1.zip (CC0)"""
import bpy, sys, numpy as np
out = sys.argv[sys.argv.index('--') + 1]
SRC = {'BASE_CABEZA': 'GEO-head_animation_realistic', 'BASE_ESCLERA_L': 'GEO-head_animation_realistic.sclera.L',
       'BASE_ESCLERA_R': 'GEO-head_animation_realistic.sclera.R', 'BASE_IRIS_L': 'GEO-head_animation_realistic.iris.L',
       'BASE_IRIS_R': 'GEO-head_animation_realistic.iris.R'}
dg = bpy.context.evaluated_depsgraph_get()
pack = []
for new, old in SRC.items():
    o = bpy.data.objects[old]; oe = o.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(oe, depsgraph=dg)
    me.transform(o.matrix_world)           # coordenadas de mundo (metros)
    me.name = new + '_MESH'; pack.append((new, me))
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene
for new, me in pack:
    ob = bpy.data.objects.new(new, me); sc.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
for m in list(bpy.data.meshes):
    if m.users == 0: bpy.data.meshes.remove(m)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print('EXTRAIDO', out)
