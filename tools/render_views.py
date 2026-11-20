"""Renderiza vistas del modelo EYEBORG (Workbench). Uso: blender -b output/EYEBORG.blend -P tools/render_views.py"""
import bpy, math, os
from mathutils import Vector
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'renders')
os.makedirs(out, exist_ok=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.resolution_x, sc.render.resolution_y = 900, 700
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
sc.world = sc.world or bpy.data.worlds.new('W'); sc.world.color = (0.12, 0.13, 0.15)
for o in bpy.data.objects:
    if o.name.startswith('REF_'): o.hide_render = True
cam = bpy.data.objects.new('CAM', bpy.data.cameras.new('CAM')); sc.collection.objects.link(cam); sc.camera = cam
d = 650
views = {'frente': (0,-d,0), 'atras': (0,d,0), 'izq': (d,0,0), 'arriba': (0,0,d), 'iso1': (d*.6,-d*.6,d*.5), 'iso2': (-d*.6,d*.6,d*.5)}
for n, loc in views.items():
    cam.location = loc
    cam.rotation_euler = (Vector((0,0,0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cam.data.clip_end = 5000
    sc.render.filepath = os.path.join(out, n + '.png'); bpy.ops.render.render(write_still=True)
print('RENDERS OK')
