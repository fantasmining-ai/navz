"""Primeros planos: blender -b output/EYEBORG_v3.blend -P tools/render_detail.py"""
import bpy, os
from mathutils import Vector
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'renders')
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x, sc.render.resolution_y = 900, 700
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
sc.display.shading.show_cavity = True
sc.world = sc.world or bpy.data.worlds.new('W'); sc.world.color = (0.12, 0.13, 0.15)
for o in bpy.data.objects:
    if o.name.startswith('REF_') or o.display_type == 'WIRE': o.hide_render = True
cam = bpy.data.objects.new('CAM', bpy.data.cameras.new('CAM')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.clip_end = 5000
views = {'det_camara': ((0,-170,200),(0,-80,55)), 'det_lateral': ((330,-60,60),(60,-20,20)), 'det_punta': ((0,-250,-110),(0,-112,-35))}
for n,(loc,tgt) in views.items():
    cam.location = loc
    cam.rotation_euler = (Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y').to_euler()
    cam.data.lens = 50 if n!='det_lateral' else 35
    sc.render.filepath = os.path.join(out, n+'.png'); bpy.ops.render.render(write_still=True)
print('DETAIL OK')
