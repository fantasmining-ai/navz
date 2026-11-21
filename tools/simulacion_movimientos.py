"""Simulación cinemática de movimientos del cuello con la estructura puesta.
Mide la holgura entre todo lo que viaja con la cabeza (estructura, cámara, bandeja, componentes, cables, jack) y el torso
(busto + trapecios + cuello) en cada pose, y renderiza una hoja de poses y una animación.
Uso:
  blender -b modelos/EYEBORG_CABLEADO.blend -P tools/simulacion_movimientos.py -- [informe] [render] [gif]
Salida: simulaciones/ (informe_movimientos.md, datos_movimientos.json, poses.jpg, movimiento_cuello.gif)"""
import bpy, math, json, os, sys
import numpy as np
from mathutils import Matrix, Vector

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, 'simulaciones'); os.makedirs(out, exist_ok=True)
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
DO_REPORT = (not args) or 'informe' in args; DO_RENDER = (not args) or 'render' in args or 'gif' in args
cfg = json.load(open(os.path.join(root, 'scripts', 'eyeborg_config.json'), encoding='utf-8'))
K = cfg['kinematics']; MQ = cfg['mannequin']
P_UP = np.array(K['pivot_upper_mm'], float); P_LOW = np.array(K['pivot_lower_mm'], float)
SPLIT = K['split_upper']

def rot(axis, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    if axis == 'x': return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == 'y': return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def about(R, P):
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = P - R @ P; return M

def pose_matrix(flex, rotz, lat):
    """flex + = flexión (barbilla al pecho); rotz + = giro a la izquierda del usuario (+X); lat + = inclinación a la izquierda."""
    Ru = rot('x', flex * SPLIT['sagittal']) @ rot('z', rotz * SPLIT['axial']) @ rot('y', lat * SPLIT['lateral'])
    Rl = rot('x', flex * (1 - SPLIT['sagittal'])) @ rot('z', rotz * (1 - SPLIT['axial'])) @ rot('y', lat * (1 - SPLIT['lateral']))
    return about(Rl, P_LOW) @ about(Ru, P_UP)

# poses: nombre, flexion, giro, inclinacion, origen del rango
POSES = [
 ('neutra', 0, 0, 0, 'referencia'),
 ('flexion_30_lectura', 30, 0, 0, 'tarea diaria: lectura/teléfono'),
 ('flexion_50', 50, 0, 0, 'norma clínica ~50°'),
 ('flexion_60', 60, 0, 0, 'rango medido ~68°'),
 ('extension_30', -30, 0, 0, 'mirar hacia arriba'),
 ('extension_45', -45, 0, 0, 'extensión moderada'),
 ('extension_60', -60, 0, 0, 'norma clínica ~60°'),
 ('giro_izq_45', 0, 45, 0, 'cruzar la calle (~54°)'),
 ('giro_izq_80', 0, 80, 0, 'rotación máxima (~78°)'),
 ('giro_der_80', 0, -80, 0, 'rotación máxima (~77°)'),
 ('inclinacion_izq_45', 0, 0, 45, 'norma clínica 45°'),
 ('inclinacion_der_45', 0, 0, -45, 'norma clínica 45°'),
 ('mirar_sobre_hombro', -15, 70, 15, 'retroceder en coche (92 % de la rotación)'),
 ('extension_30_giro_45', -30, 45, 0, 'combinado'),
]

def ell_gap(P, c, r):
    q = (P - c) / r
    r2 = (q ** 2).sum(1); g = np.sqrt(((P - c) / r ** 2) ** 2).sum(1) if False else np.sqrt((((P - c) / r ** 2) ** 2).sum(1))
    return (r2 - 1.0) / (2.0 * np.maximum(g, 1e-9))

def torso_gap(P):
    """Holgura aproximada (mm) a las proxys del torso y al cuello; negativa = interpenetra."""
    gaps = []
    for t in MQ['torso_proxies']:
        gaps.append(ell_gap(P, np.array(t['c'], float), np.array(t['r'], float)))
    nk = MQ['neck']; ax_y = MQ.get('neck_axis_y', 12.0); nr = cfg['anthropometry']['neck_circumference_mm'] / (2 * math.pi)
    zc, hz = nk['c'][2], nk['depth'] / 2.0
    dxy = np.sqrt(P[:, 0] ** 2 + (P[:, 1] - ax_y) ** 2) - nr
    dz = np.maximum(np.abs(P[:, 2] - zc) - hz, 0)
    gaps.append(np.sqrt(np.maximum(dxy, 0) ** 2 + dz ** 2) * np.where((dxy < 0) & (dz == 0), -1.0, 1.0))
    return np.min(np.stack(gaps), axis=0)

# ---------------- piezas que viajan con la cabeza ----------------
D = bpy.context.evaluated_depsgraph_get()
def world_pts(o):
    oe = o.evaluated_get(D)
    me = oe.to_mesh()
    n = len(me.vertices); a = np.empty(n * 3); me.vertices.foreach_get('co', a); a = a.reshape(-1, 3)
    M = np.array(o.matrix_world); a = a @ M[:3, :3].T + M[:3, 3]
    oe.to_mesh_clear(); return a
MOVE = []
for o in bpy.data.objects:
    n = o.name
    if o.type == 'MESH' and (n.startswith('EYEBORG_FUSION') or n.startswith(('CARCASA_CAMARA', 'BANDEJA_ELECTRONICA', 'REF_NODEMCU', 'REF_LIPO', 'REF_TP4056', 'REF_MT3608', 'REF_DAC', 'JACK_AUDIO', 'PUERTO_USB', 'CONECTOR_JST', 'CAP_'))):
        MOVE.append((n, world_pts(o)))
    elif o.type == 'CURVE' and n.startswith(('CABLE_', 'LED_')):
        MOVE.append((n, world_pts(o)))
print('SIM piezas que viajan con la cabeza:', len(MOVE), sum(len(p) for _, p in MOVE), 'puntos')

def evaluate(flex, rz, lat):
    M = pose_matrix(flex, rz, lat); worst = (1e9, '', None)
    neg = 0
    for n, P in MOVE:
        Q = P @ M[:3, :3].T + M[:3, 3]
        g = torso_gap(Q); i = int(np.argmin(g)); neg += int((g < 0).sum())
        if g[i] < worst[0]: worst = (float(g[i]), n, Q[i].round(1).tolist())
    return worst, neg

datos = []
if DO_REPORT:
    for name, fl, rz, la, src in POSES:
        (g, parte, pt), neg = evaluate(fl, rz, la)
        datos.append({'pose': name, 'flexion': fl, 'giro_izq': rz, 'inclinacion_izq': la, 'origen': src,
                      'holgura_min_mm': round(g, 1), 'pieza_critica': parte, 'punto': pt, 'puntos_en_colision': neg})
        print('SIM', name, round(g, 1), parte)
    json.dump(datos, open(os.path.join(out, 'datos_movimientos.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    # busca el límite de extensión (primer ángulo con colisión)
    lim = None
    for a in range(0, 71, 1):
        (g, parte, pt), neg = evaluate(-a, 0, 0)
        if g < 0: lim = (a, parte); break
    lim_f = None
    for a in range(0, 71, 1):
        (g, parte, pt), neg = evaluate(a, 0, 0)
        if g < 0: lim_f = (a, parte); break
    md = ['# Simulación de movimientos del cuello con la estructura puesta\n',
          'Cinemática de dos articulaciones (suboccipital + cervical inferior) con rangos de la literatura (ver `docs/SPEC_AJUSTE_ANATOMICO.md`). '
          'Se mide la holgura mínima entre **todo lo que viaja con la cabeza** (estructura, cámara, bandeja, componentes, cables y jack de audio) y el **torso** (busto + trapecios + cuello). '
          'Holgura negativa = la pieza choca con el cuerpo. Es un modelo **esquemático** (torso de elipsoides, cables rígidos), no un análisis de tejidos.\n',
          '| Pose | Flexión | Giro izq. | Incl. izq. | Holgura mín. (mm) | Pieza crítica | Estado |', '| --- | --- | --- | --- | --- | --- | --- |']
    for d_ in datos:
        est = '✔' if d_['holgura_min_mm'] >= 6 else ('⚠ < 6 mm' if d_['holgura_min_mm'] >= 0 else '✘ colisión')
        md.append('| %s | %d° | %d° | %d° | %.1f | %s | %s |' % (d_['pose'], d_['flexion'], d_['giro_izq'], d_['inclinacion_izq'], d_['holgura_min_mm'], d_['pieza_critica'], est))
    md.append('\n**Límite de extensión sin colisión:** ' + ('%d° (pieza: %s)' % lim if lim else '> 70°'))
    md.append('**Límite de flexión sin colisión:** ' + ('%d° (pieza: %s)' % lim_f if lim_f else '> 70°'))
    # equilibrio estatico respecto a la articulacion suboccipital (masas ESTIMADAS)
    ME = cfg['mass_estimates']; G = 9.81e-3   # N por gramo
    allp = np.concatenate([P for n, P in MOVE if n.startswith('EYEBORG_FUSION')]); com_est = allp.mean(0)
    masas = [('cabeza', ME['cabeza_g'], np.array(ME['cabeza_com_mm'], float)), ('estructura', ME['estructura_g'], com_est),
             ('pod+ESP32-CAM', ME['pod_camara_g'], np.array(ME['pod_camara_com_mm'], float)),
             ('bandeja+componentes', ME['bandeja_componentes_g'], np.array(ME['bandeja_com_mm'], float))]
    md.append('\n## Equilibrio estático respecto al pivote suboccipital (masas estimadas)\n')
    md.append('Par = masa·g·brazo horizontal (+ = tiende a extender la cabeza hacia atrás; − = a flexionarla hacia delante). Masas **estimadas, no verificadas** (ver `config → mass_estimates`).\n')
    md.append('| Pose | Cabeza sola (N·m) | Cabeza + equipo (N·m) | Equipo solo (N·m) |'); md.append('| --- | --- | --- | --- |')
    for nm_, fl_ in (('neutra', 0), ('flexion_30', 30), ('extension_30', -30)):
        M_ = pose_matrix(fl_, 0, 0); tq = {}
        for n_, m_, c_ in masas:
            cw = M_[:3, :3] @ c_ + M_[:3, 3]; tq[n_] = m_ * G * (cw[1] - P_UP[1]) / 1000.0
        eq = sum(v for k, v in tq.items() if k != 'cabeza')
        md.append('| %s | %.2f | %.2f | %.2f |' % (nm_, tq['cabeza'], tq['cabeza'] + eq, eq))
    md.append('\n**Masa total del equipo:** %d g (estructura %d + pod/ESP32-CAM %d + bandeja/componentes %d) — estimación.' % (ME['estructura_g'] + ME['pod_camara_g'] + ME['bandeja_componentes_g'], ME['estructura_g'], ME['pod_camara_g'], ME['bandeja_componentes_g']))
    open(os.path.join(out, 'informe_movimientos.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print('SIM_LIMITE_EXT', lim, 'SIM_LIMITE_FLEX', lim_f)

if DO_RENDER:
    import bmesh
    fr_dir = os.path.join(out, '_frames'); os.makedirs(fr_dir, exist_ok=True)
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x, sc.render.resolution_y = 560, 520
    sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'OBJECT'; sh.show_cavity = True
    sc.world = sc.world or bpy.data.worlds.new('W'); sc.world.color = (0.55, 0.57, 0.60)
    src = bpy.data.objects['MANIQUI_CUERPO']
    def mitad(nombre, arriba):
        bm = bmesh.new(); bm.from_mesh(src.data)
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if (f.calc_center_median().z > -100.0) != arriba], context='FACES')
        me = bpy.data.meshes.new(nombre); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(nombre, me); sc.collection.objects.link(o); return o
    cab = mitad('SIM_CABEZA', True); tor = mitad('SIM_TORSO', False); src.hide_render = True; src.hide_viewport = True
    cab.color = (0.72, 0.72, 0.74, 1); tor.color = (0.55, 0.55, 0.58, 1)
    emp = bpy.data.objects.new('SIM_PIVOTE_CABEZA', None); sc.collection.objects.link(emp)
    cab.parent = emp
    for o in bpy.data.objects:
        n = o.name
        if o.get('esquema_conceptual') or n.startswith(('EYEBORG_FUSION', 'CARCASA_CAMARA', 'BANDEJA_ELECTRONICA', 'JACK_', 'CAP_')) or n.startswith('REF_') and o.display_type != 'WIRE':
            o.parent = emp
            if n.startswith('EYEBORG_FUSION'): o.color = (0.25, 0.75, 0.95, 1)
            elif n.startswith('CABLE_POT') or n.startswith('MANGA_5V'): o.color = (0.9, 0.1, 0.1, 1)
            elif n.startswith('CABLE_I2S'): o.color = (0.0, 0.8, 0.9, 1)
            elif n.startswith('CABLE_'): o.color = (0.1, 0.1, 0.1, 1)
            else: o.color = (0.3, 0.3, 0.32, 1)
        if o.name.startswith(('MANIQUI_', 'SUELO')) and o is not src and not n.startswith('SIM_'): o.hide_render = True
        if o.type == 'MESH' and (o.display_type == 'WIRE'): o.hide_render = True
    for o in list(bpy.data.objects):
        if o.type in ('LIGHT',): o.hide_render = True
    cd = bpy.data.cameras.new('SIMCAM'); cd.type = 'ORTHO'; cd.ortho_scale = 560; cam = bpy.data.objects.new('SIMCAM', cd); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (900, 10, -70); cam.rotation_euler = (Vector((0, 10, -70)) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
    def poner(fl, rz, la):
        emp.matrix_world = Matrix(pose_matrix(fl, rz, la).tolist()); bpy.context.view_layer.update()
    for name, fl, rz, la, src_ in POSES:
        poner(fl, rz, la); sc.render.filepath = os.path.join(fr_dir, 'pose_%s.png' % name); bpy.ops.render.render(write_still=True)
    # animacion continua entre poses clave
    claves = [(0,0,0), (-60,0,0), (0,0,0), (50,0,0), (0,0,0), (0,80,0), (0,-80,0), (0,0,0), (0,0,45), (0,0,-45), (0,0,0), (-15,70,15), (0,0,0)]
    k = 0
    for a, b in zip(claves[:-1], claves[1:]):
        for s in range(8):
            f = s / 8.0; f = f * f * (3 - 2 * f)
            poner(*[a[i] + (b[i] - a[i]) * f for i in range(3)])
            sc.render.filepath = os.path.join(fr_dir, 'anim_%03d.png' % k); bpy.ops.render.render(write_still=True); k += 1
    print('SIM_FRAMES', k)
print('SIM_OK')
