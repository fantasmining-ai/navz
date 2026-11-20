"""Renders del diseño 1 (Cycles). Uso: blender -b output/EYEBORG.blend -P tools/render_diseno1.py -- [muestras] [escala%]"""
import bpy, os, sys, math
from mathutils import Vector
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
samples = int(args[0]) if args else 32; pct = int(args[1]) if len(args) > 1 else 100
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'renders')
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
sc.render.resolution_percentage = pct; sc.view_settings.view_transform = 'AgX'
for o in bpy.data.objects:
    if o.name.startswith('REF_') or o.display_type == 'WIRE': o.hide_render = True
cd = bpy.data.cameras.new('TMP'); cd.lens = 70; cd.clip_end = 8000
cam = bpy.data.objects.new('TMP', cd); sc.collection.objects.link(cam); sc.camera = cam
V = {'d1_iso_frontal': ((430, -560, 230), (0, -5, 5)), 'd1_iso_trasera': ((-420, 600, 210), (0, 20, 0)),
     'd1_frente': ((0, -700, 20), (0, -5, 5)), 'd1_lateral': ((700, -20, 15), (0, -5, 5))}
for n, (loc, tgt) in V.items():
    cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(out, n + '.png'); bpy.ops.render.render(write_still=True); print('SHOT', n)
