# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection
from _eyeborg_config import *
from mathutils import Vector
from _eyeborg_materials import build_all

"""Cableado discreto SIMULADO (esquema conceptual, no energizar): cables por la cara interna de los rieles,
conectores, capacitores y puentes en la bandeja. Valores y pines por definir (ver expediente tecnico, seccion 08)."""

def _pts(obj, f0, f1, inward, lateral=0.0, step=4):
    a = list(obj['linea_central'])
    P = [(Vector(a[i:i+3]), Vector(a[i+3:i+6])) for i in range(0, len(a), 6)]
    n = len(P)
    i0, i1 = int(round(f0*(n-1))), int(round(f1*(n-1)))
    idx = list(range(i0, i1 + (1 if i1 >= i0 else -1), step if i1 >= i0 else -step))
    out = []
    for i in idx:
        i = max(1, min(n-2, i))
        p, nr = P[i]
        T = (P[i+1][0] - P[i-1][0]).normalized()
        W = nr.cross(T).normalized()
        out.append(p - nr*inward + W*lateral)
    return out

def _cable(name, pts, r, mat, col, note=''):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = r; cu.bevel_resolution = 3; cu.use_fill_caps = True; cu.resolution_u = 6
    sp = cu.splines.new('NURBS'); sp.points.add(len(pts)-1)
    for i, p in enumerate(pts):
        sp.points[i].co = (p.x, p.y, p.z, 1.0)
    sp.order_u = 4; sp.use_endpoint_u = True
    ob = bpy.data.objects.new(name, cu); col.objects.link(ob); cu.materials.append(mat)
    ob['esquema_conceptual'] = 'visualizacion; no es plano de cableado ni autoriza energizar'
    if note: ob['nota'] = note
    return ob

def _box(name, size, loc, mat, col, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.data.materials.append(mat)
    mod = o.modifiers.new('Bisel', 'BEVEL'); mod.width = 0.35; mod.segments = 2
    return o

def _cyl(name, r, h, loc, mat, col, rot=(0,0,0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.data.materials.append(mat)
    for p in o.data.polygons: p.use_smooth = True
    return o

def _band(name, pts, k, r, mat, col):
    """Anillo de termorretractil de color en el punto k de la trayectoria."""
    k = max(1, min(len(pts)-2, k))
    d = (pts[k+1] - pts[k-1]).normalized()
    rot = d.to_track_quat('Z', 'Y').to_euler()
    return _cyl(name, r*1.5, 2.2, tuple(pts[k]), mat, col, rot=rot, verts=16)

def _capacitor(name, loc, mat, alu, col, note):
    body = _cyl(name+'_CUERPO', 3.2, 8.0, loc, mat, col)
    _cyl(name+'_TAPA', 3.25, 0.5, (loc[0], loc[1], loc[2]+4.2), alu, col)
    for k_, dx in enumerate((-1.1, 1.1)):
        _cyl(name+'_PATA_%d' % (k_+1), 0.28, 5.0, (loc[0]+dx, loc[1], loc[2]-6.0), alu, col, verts=8)
    body['valor'] = 'POR DEFINIR (decoupling; no inventar capacitancia)'
    body['nota'] = note
    return body

def build():
    M = build_all()
    col = get_collection('EYEBORG_20_CABLEADO', clear=True)
    obj = bpy.data.objects
    rails = {'IZQ': obj['RIEL_SUPERIOR_IZQUIERDA'], 'DER': obj['RIEL_SUPERIOR_DERECHA']}
    arms = {'IZQ': obj['BRAZO_MARIPOSA_IZQ'], 'DER': obj['BRAZO_MARIPOSA_DER']}
    bar = obj['BARRA_PUENTE_CAMARA']
    inward = 6.0 / 2 + 0.9 + 0.5
    # ---- Riel izquierdo: potencia (+5 V y GND) desde la bandeja hasta la camara
    for tag, lat, mat in (('5V', 1.3, 'cable_red'), ('GND', -1.3, 'cable_black')):
        path = _pts(rails['IZQ'], 1.0, 0.0, inward, lat) + _pts(arms['IZQ'], 1.0, 0.0, inward, lat, 2) + _pts(bar, 1.0, 0.5, inward, lat, 3)
        path += [Vector((lat*0.6, -112.0, 44.0))]
        tray_start = [Vector((-10+lat*2, 117, -18)), Vector((-8+lat, 124, -2)), Vector((8, 127, 16)), Vector((24, 127.5, 28))]
        path = tray_start + path
        c = _cable('CABLE_POTENCIA_'+tag, path, 0.9, M[mat], col, 'MT3608 -> ESP32-CAM; tension y corriente por medir')
        _band('MANGA_'+tag+'_CAM', path, len(path)-4, 0.9, M['led_magenta'] if tag=='5V' else M['jst'], col)
    # ---- Riel derecho: bus I2S (3 lineas) camara -> DAC; pines SIN ASIGNAR
    for k, lat in enumerate((-1.6, 0.0, 1.6)):
        path = [Vector((lat*0.5, -112.0, 44.0))] + _pts(bar, 0.5, 0.0, inward, lat, 3) + _pts(arms['DER'], 0.0, 1.0, inward, lat, 2) + _pts(rails['DER'], 0.0, 1.0, inward, lat)
        path += [Vector((-24, 126, 24)), Vector((-4, 125, 4)), Vector((16, 122, -12)), Vector((27+lat, 118.5, -14))]
        _cable('CABLE_I2S_%d_POR_ASIGNAR' % (k+1), path, 0.55, M['cable_cyan'], col, 'BCK/LRCK/DIN: GPIO no asignados (ver 07/08 del expediente)')
    # ---- Salida de audio hacia amplificador externo (colgante con jack)
    aud = [Vector((27, 118.5, -26)), Vector((32, 123, -44)), Vector((34, 130, -66)), Vector((30, 140, -88)), Vector((26, 146, -104))]
    _cable('CABLE_AUDIO_SALIDA', aud, 1.0, M['cable_black'], col, 'PCM5102A -> amplificador externo; jack/alivio por definir')
    _cyl('JACK_AUDIO_PUNTA', 3.0, 14.0, (26, 146, -111), M['gold'], col, rot=(0.15, 0, 0))
    _cyl('JACK_AUDIO_CUERPO', 3.6, 8.0, (26.5, 145.5, -102), M['graphite'], col, rot=(0.15, 0, 0))
    # ---- Puentes cortos en la bandeja (colores de ayuda visual)
    jumps = [
      ('LIPO_TP4056', (25,114,6), (-41,114,-21), 'cable_red'), ('TP4056_MT3608', (-41,114,-21), (-10,116,-21), 'cable_red'),
      ('MT3608_NODEMCU', (-10,116,-21), (-25,119,6), 'cable_white'), ('MT3608_DAC', (-10,116,-21), (27,118,-21), 'cable_white'),
    ]
    for nm, a, b, mk in jumps:
        A, B = Vector(a), Vector(b)
        mid = (A + B) / 2 + Vector((0, 6, 7))
        _cable('PUENTE_'+nm, [A + Vector((0, 4, 4)), (A+mid)/2 + Vector((0,2,3)), mid, (B+mid)/2 + Vector((0,2,3)), B + Vector((0, 4, 4))], 0.45, M[mk], col, 'conexion conceptual de bandeja')
    # ---- Conectores (JST blockout)
    _box('CONECTOR_JST_CAMARA', (8, 5, 4), (0, -112, 41.5), M['jst'], col)
    _box('CONECTOR_JST_TRAY_PWR', (8, 5, 4), (-8, 112, -20), M['jst'], col)
    _box('PUERTO_USB_C_BLOCKOUT', (3.2, 9, 7), (-53.5, 113, -21), M['alu'], col)
    # ---- Capacitores (valores por definir)
    _capacitor('CAP_CAMARA', (-9, -108, 39.5), M['cap_blue'], M['alu'], col, 'desacople 5 V junto a la ESP32-CAM; capacitancia por definir')
    _capacitor('CAP_MT3608', (-22, 114, -5), M['cap_blue'], M['alu'], col, 'filtro de salida MT3608; capacitancia por definir')
    _capacitor('CAP_DAC', (2, 112, -33), M['cap_blue'], M['alu'], col, 'desacople PCM5102A; capacitancia por definir')
    # ---- LED de estado en la barra (acento cyberpunk, 1 mm)
    led = _cable('LED_BARRA', [Vector((x, -119.8, 45.5)) for x in (-18, -9, 0, 9, 18)], 0.55, M['led_cyan'], col, 'acento visual; no es un circuito')
    _maniqui(M, col)
    return col


def _maniqui(M, col):
    """Maniqui esquematico (NO escaneo): nariz, menton y cuello con las medidas del expediente; sirve para ver el corredor nasal."""
    import bmesh
    from mathutils import Matrix
    def ell(name, c, r, mat_):
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=24, radius=1.0,
            matrix=Matrix.Translation(Vector(c)) @ Matrix.Diagonal(Vector((r[0], r[1], r[2], 1.0))))
        me = bpy.data.meshes.new(name+'_MESH'); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(mat_)
        for p_ in me.polygons: p_.use_smooth = True
        o['nota'] = 'maniqui esquematico; no es un escaneo'
        return o
    nose_len = ANTHROPOMETRY.get('nasal_bridge_to_tip_mm', 40.0); nose_w = ANTHROPOMETRY.get('nose_width_mm', 35.0)
    ell('MANIQUI_NARIZ', (0, -104, -14), (nose_w*0.32, nose_len*0.42, nose_len*0.55), M['head'])
    ell('MANIQUI_MENTON', (0, -84, -88), (30, 26, 22), M['head'])
    neck_r = 380.0 / (2 * math.pi)     # circunferencia de cuello 380 mm
    cyl = _cyl('MANIQUI_CUELLO', neck_r, 120.0, (0, 6, -150), M['head'], col, verts=48)
    cyl['nota'] = 'radio calculado de la circunferencia de cuello verificada (380 mm)'

if __name__ == "__main__":
    build()
