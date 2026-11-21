"""Genera las vistas estándar de un diseño, CON y SIN maniquí, en vistas/<diseno>/<con|sin>_maniqui/.
Uso:
  blender -b modelos/EYEBORG.blend          -P tools/render_vistas.py -- diseno_1 [muestras] [ancho_px] [reanudar]
  blender -b modelos/EYEBORG_CABLEADO.blend -P tools/render_vistas.py -- diseno_2 [muestras] [ancho_px] [reanudar]
  (con 'reanudar' se omiten las imágenes que ya existen; útil si el proceso se interrumpe)
Diseños: diseno_1 (estructura), diseno_2 (cromo + cableado), diseno_3 (resina satinada + cableado).
Vistas: frente, trasera, lateral izquierda/derecha (del usuario), superior, inferior (ortográficas),
isométrica frontal/trasera y detalle de cámara (perspectiva). Diseño 2 añade rayos X del cableado."""
import bpy, os, sys, math
from mathutils import Vector

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
if not args or args[0] not in ('diseno_1', 'diseno_2', 'diseno_3'):
    raise SystemExit('Indica diseno_1, diseno_2 o diseno_3 tras "--"')
design = args[0]; samples = int(args[1]) if len(args) > 1 else 40; resx = int(args[2]) if len(args) > 2 else 1400
REANUDAR = 'reanudar' in args
SALIDA = next((a.split('=', 1)[1] for a in args if a.startswith('salida=')), None)   # p. ej. salida=versiones/v3_... -> versiones/v3_.../vistas/
PRUEBA = 'prueba' in args                       # escribe en renders_tmp/ y solo 3 vistas
SOLO = [a.split('=', 1)[1] for a in args if a.startswith('solo=')]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_ROOT = None
sc = bpy.context.scene; C = bpy.data.objects
sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.render.resolution_x = resx; sc.render.resolution_y = int(resx * 0.75); sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'AgX'
if design == 'diseno_1':      # versiones antiguas sin mundo de estudio: gris claro como el diseño 1 actual
    w = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True
    bgn = w.node_tree.nodes.get('Background')
    if bgn: bgn.inputs['Color'].default_value = (0.55, 0.58, 0.62, 1); bgn.inputs['Strength'].default_value = 0.9
mann = [o for o in C if o.name.startswith('MANIQUI_')]
for o in C:
    if o.name.startswith('REF_') or o.display_type == 'WIRE':
        o.hide_render = True
# cámara + luz de relleno acoplada a la cámara (para que ninguna vista quede a oscuras)
cd = bpy.data.cameras.new('CAM_VISTAS'); cd.clip_end = 8000
cam = bpy.data.objects.new('CAM_VISTAS', cd); sc.collection.objects.link(cam); sc.camera = cam
ld = bpy.data.lights.new('LGT_camara', 'AREA'); ld.size = 320; ld.energy = {'diseno_1': 2500, 'diseno_2': 600, 'diseno_3': 1200}[design]
lg = bpy.data.objects.new('LGT_camara', ld); sc.collection.objects.link(lg)

def poner(loc, tgt, ortho=None, lens=60):
    cam.location = loc
    rot = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cam.rotation_euler = rot
    if ortho:
        cd.type = 'ORTHO'; cd.ortho_scale = ortho; cd.dof.use_dof = False
    else:
        cd.type = 'PERSP'; cd.lens = lens
        if design != 'diseno_1':      # profundidad de campo sutil en las perspectivas (diseños 2 y 3)
            cd.dof.use_dof = True; cd.dof.focus_distance = (Vector(tgt) - Vector(loc)).length; cd.dof.aperture_fstop = 9.0
    lg.location = Vector(loc) + (cam.matrix_world.to_3x3() @ Vector((-120, 120, 0)))
    lg.rotation_euler = rot
    bpy.context.view_layer.update()

D = 1000
# nombre: (ubicación relativa a un objetivo, orto?)
def vistas(con):
    t = Vector((0, 10, -75)) if con else Vector((0, 0, 8))      # centro de encuadre
    s = 560 if con else 340                                       # escala ortográfica
    up = Vector((0, 0, 1))
    return [
        ('01_frente',            t + Vector((0, -D, 0)), t, s, None),
        ('02_trasera',           t + Vector((0, D, 0)), t, s, None),
        ('03_lateral_izquierda', t + Vector((D, 0, 0)), t, s, None),
        ('04_lateral_derecha',   t + Vector((-D, 0, 0)), t, s, None),
        ('05_superior',          Vector((0, 0, D)) + Vector((0, 0.01, 0)), Vector((0, 0, 0)), s, None),
        ('06_inferior',          Vector((0, 0, -D)) + Vector((0, 0.01, 0)), Vector((0, 0, 0)), s, None),
        ('07_isometrica_frontal', t + (Vector((520, -680, 330)) if con else Vector((430, -560, 230))), t, None, 62),
        ('08_isometrica_trasera', t + (Vector((-520, 700, 300)) if con else Vector((-420, 600, 210))), t, None, 62),
        ('09_detalle_camara',    Vector((190, -420, 170)), Vector((0, -112, 46)), None, 100),
    ]

def render(path):
    if SALIDA:
        path = path.replace(os.path.join(root, 'vistas'), os.path.join(os.path.abspath(os.path.join(root, SALIDA)), 'vistas'), 1)
    if PRUEBA:
        path = os.path.join(root, 'renders_tmp', design + '_' + os.path.basename(path))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if REANUDAR and os.path.isfile(path) and os.path.getsize(path) > 10000:
        print('OMITIDA', os.path.relpath(path, root)); return
    sc.render.filepath = path; bpy.ops.render.render(write_still=True); print('SHOT', os.path.relpath(path, root))

for con in (True, False):
    for o in mann: o.hide_render = not con
    sub = 'con_maniqui' if con else 'sin_maniqui'
    for nombre, loc, tgt, ortho, lens in vistas(con):
        if SOLO and not any(s in nombre for s in SOLO): continue
        if PRUEBA and not SOLO and nombre not in ('07_isometrica_frontal', '08_isometrica_trasera', '09_detalle_camara'): continue
        poner(loc, tgt, ortho, lens or 60)
        render(os.path.join(root, 'vistas', design, sub, ('' if not PRUEBA else sub + '_') + nombre + '.jpg'))
# rayos X del cableado (solo diseño 2, sin maniquí)
if design in ('diseno_2', 'diseno_3'):
    for o in mann: o.hide_render = True
    fus = next((o for o in C if o.name.startswith('EYEBORG_FUSION')), None)
    chrome = fus.data.materials[0] if fus and fus.data.materials else None
    if chrome and not PRUEBA:
        chrome.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.10
        for nombre, loc, tgt, ortho, lens in (('10_rayos_x_lateral', Vector((700, -20, 15)), Vector((0, -5, 5)), None, 85),
                                              ('11_rayos_x_isometrica', Vector((430, -560, 230)), Vector((0, -5, 5)), None, 62)):
            poner(loc, tgt, ortho, lens)
            render(os.path.join(root, 'vistas', design, 'sin_maniqui', nombre + '.jpg'))
print('VISTAS OK', design)
