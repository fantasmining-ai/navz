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

"""Visor tipo lentes inuit: banda curva sobre los ojos (las ranuras se cortan en el modulo 12), brazos de sien y gancho sobre la
oreja con almohadilla en el helix. Ver docs/SPEC_AJUSTE_ANATOMICO.md."""
def build():
    col = get_collection('EYEBORG_15_VISOR', clear=True)
    m = set_materials()
    vz = V['z_center_mm']; hs = V['half_span_mm']
    xs = [-hs + 10.0 * i for i in range(int(2 * hs / 10.0) + 1)]
    pts = [tuple(visor_point(x, vz, V)[0]) for x in xs]
    vis = strap('VISOR_INUIT', pts, V['height_mm'], V['thickness_mm'], col, material=m['blue'], xyz=True,
                center=(0, 0, None), clear=False, cap=(0.02, 0.02), power=4.0, steps=6)
    mark_modular(vis, 'visor con ranuras 48x12 mm alineadas a las pupilas; offset >= 15 mm de la cornea')
    for s, side in ((1, 'IZQ'), (-1, 'DER')):
        end = visor_point(s * hs, vz, V)[0]
        # brazo de sien: recorre la fosa temporal hacia la oreja y la bordea por arriba
        arm = [tuple(end)] + [tuple(side_point(y, z, off, s)[0]) for (y, z, off) in
               ((-12, 19, 8), (0, 22, 8), (9, 20, 8), (17, 18, 8), (24, 14.5, 7))]
        a = strap('BRAZO_SIEN_' + side, arm, [(0, 9), (0.6, 8), (1, 6)], 4.0, col, material=m['blue'], xyz=True,
                  center=(0, None, None), clear=False, cap=(0.03, 0.15))
        mark_modular(a, 'brazo de sien con gancho sobre el helix; espesor <= 5 mm entre oreja y craneo')
        # almohadilla sobre el helix (arriba de la oreja)
        r = snap_to_skin((s * 84.0, 8.0, 90.0), (0, 0, -1))   # desde arriba, sobre el hélix (centro de la oreja x=84)
        if r:
            hit, n = r
            pad('PAD_OREJA_' + side, hit, n, (6.0, 9.0, V['pad_thickness_mm'] / 2.0), col, m['dark'])
            tgt = side_point(9, 19, 8, s)[0]
            rod('PUNTAL_OREJA_' + side, hit + n * V['pad_thickness_mm'], tgt, 4.5, 3.0, col, m['blue'], 'union del gancho a la almohadilla del helix')
    return col

if __name__ == "__main__":
    build()
