# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, node_blob, mark_modular, face_point, side_point, visor_point, snap_to_skin
from _eyeborg_config import *
from mathutils import Vector

V = CONFIG['visor']

def rod(name, a, b, w, t, col, mat, mark=None):
    """Puntal recto entre dos puntos (union rigida, sin empuje fuera de la cabeza: toca la piel en el anclaje)."""
    o = strap(name, [tuple(a), tuple(b)], w, t, col, material=mat, xyz=True, nhint=(0, 0, 1), clear=False, cap=(0.2, 0.2), steps=4, sections=14)
    if mark: mark_modular(o, mark)
    return o

def pad(name, hit, n, size, col, mat):
    """Almohadilla EVA (pieza blanda separada, no se funde): apoyada en la piel en 'hit' con la cara plana contra la normal."""
    rx, ry, rz = size
    o = node_blob(name, tuple(hit + n * rz), tuple(n), rx, ry, rz, col, material=mat, clear=False)
    o['material_real'] = 'EVA 5 mm (por definir)'; o['anclaje'] = True
    return o

"""Anclajes centrales: puente nasal (2 almohadillas laterales sobre el dorso, nunca en la punta) y apoyo frontal sobre la ceja.
Las posiciones se proyectan sobre la piel REAL del maniqui (snap_to_skin); si no hay maniqui, sobre la envolvente."""
def _skin(x, z, y0=-250.0):
    r = snap_to_skin((x, y0, z), (0, 1, 0))
    if r: return r[0], r[1]
    p, n = face_point(x, z, 0.0); return p, n

def build():
    col = get_collection('EYEBORG_01_COLUMNA_FRONTAL', clear=True)
    m = set_materials()
    vz = V['z_center_mm']
    for s, side in ((1, 'IZQ'), (-1, 'DER')):
        # --- puente nasal: pad sobre la pared lateral del dorso, a la altura del nasion
        hit, n = _skin(s * 8.0, 2.0)
        if abs(n.x) < 0.3:  # el rayo frontal da normal casi frontal; inclinar hacia el lado para apoyar en la pared lateral
            n = (n + Vector((s * 0.55, 0, 0))).normalized()
        pad('PAD_NASAL_' + side, hit, n, (4.0, 8.0, V['pad_thickness_mm'] / 2.0), col, m['dark'])
        vp, vn = visor_point(s * 9.0, vz, V)
        rod('PUNTAL_NASAL_' + side, hit + n * V['pad_thickness_mm'], Vector((vp.x, vp.y + 1.2, 2.0)), 5.0, 3.0, col, m['blue'],
            'union de puente nasal al visor')
        # --- apoyo frontal (sobre la ceja osea): pad + puntal al borde superior del visor
        hit, n = _skin(s * 24.0, 28.0)
        pad('PAD_FRONTAL_' + side, hit, n, (7.0, 10.0, V['pad_thickness_mm'] / 2.0), col, m['dark'])
        vt, _ = visor_point(s * 24.0, vz + V['height_mm'] / 2.0 - 2.0, V)
        rod('PUNTAL_FRONTAL_' + side, hit + n * V['pad_thickness_mm'], Vector((vt.x, vt.y + 1.2, vt.z)), 6.0, 3.2, col, m['blue'],
            'union de apoyo frontal al visor')
    return col

if __name__ == "__main__":
    build()
