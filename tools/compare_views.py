"""Renderiza el modelo en ortografica desde las mismas direcciones que las referencias.
Uso: blender -b modelos/EYEBORG.blend -P tools/compare_views.py   (genera renders_tmp/cmp_*.png)"""
import bpy, os, math
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'renders_tmp')
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x, sc.render.resolution_y = 900, 700
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
sc.world = sc.world or bpy.data.worlds.new('W'); sc.world.color = (0.2, 0.2, 0.22)
for o in bpy.data.objects:
    if o.name.startswith('REF_') or o.display_type == 'WIRE': o.hide_render = True
cd = bpy.data.cameras.new('C'); cd.type = 'ORTHO'; cd.ortho_scale = 340; cd.clip_end = 5000
cam = bpy.data.objects.new('C', cd); sc.collection.objects.link(cam); sc.camera = cam
V = {  # nombre: (posicion, rotacion euler)
  'frente': ((0,-800,10), (math.pi/2,0,0)),
  'lado':   ((800,0,10),  (math.pi/2,0,math.pi/2)),
  'arriba': ((0,0,800),   (0,0,math.pi)),
  'atras':  ((0,800,10),  (math.pi/2,0,math.pi)),
}
for n,(loc,rot) in V.items():
    cam.location = loc; cam.rotation_euler = rot
    sc.render.filepath = os.path.join(out, 'cmp_'+n+'.png'); bpy.ops.render.render(write_still=True)
print('CMP OK')
