"""Renders del diseño 2. Uso: blender -b output/EYEBORG_CABLEADO.blend -P tools/render_cableado.py -- [muestras] [escala%] [shots...]
shots: hero trasera detalle lateral xray"""
import bpy, os, sys
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
samples = int(args[0]) if args else 48
pct = int(args[1]) if len(args) > 1 else 100
shots = args[2:] or ['hero', 'trasera', 'detalle', 'xray']
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'renders')
sc = bpy.context.scene; sc.cycles.samples = samples; sc.render.resolution_percentage = pct
C = bpy.data.objects
head = C.get('REF_CABEZA_BLOCKOUT')
chrome = bpy.data.materials['EYEBORG_CROMO_AZUL']
def shot(name, cam, xray=False):
    sc.camera = C[cam]
    if head: head.hide_render = xray
    b = chrome.node_tree.nodes['Principled BSDF']
    b.inputs['Alpha'].default_value = 0.10 if xray else 1.0

    sc.render.filepath = os.path.join(out, 'cable_%s.png' % name); bpy.ops.render.render(write_still=True); print('SHOT', name)
M = {'hero': ('CAM_hero', False), 'trasera': ('CAM_trasera', False), 'detalle': ('CAM_detalle_camara', False),
     'lateral': ('CAM_lateral', False), 'xray': ('CAM_lateral', True)}
for s in shots: shot(s, *M[s])
