# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *
from mathutils import Vector
from _eyeborg_core import cut_with_specs

"""Agujeros de tornillo y bolsa de camara, cortados (booleano) sobre la malla fusionada. Patron provisional."""
# Fracciones (0-1) a lo largo de la linea central de cada correa donde va un agujero pasante.
HOLES_ON = {   # pocos agujeros de montaje, en los tramos anchos
    'DIAGONAL_PRINCIPAL': (0.30, 0.46),
    'RIEL_INFERIOR': (0.42, 0.72),
    'RIEL_SUPERIOR': (0.25, 0.60),
    'POSTE_SIEN': (0.5,),
    'BARRA_POSTERIOR_INFERIOR': (0.2, 0.8),
}
TIP_HOLES = (0.5,)   # fila de tres agujeros en la punta

def _centerline(obj):
    a = list(obj['linea_central'])
    pts = [(Vector(a[i:i+3]), Vector(a[i+3:i+6])) for i in range(0, len(a), 6)]
    return pts

def _at(pts, f):
    return pts[min(len(pts)-1, max(0, int(round(f*(len(pts)-1)))))]

def build():
    F = CONFIG['fasteners']
    fused = bpy.data.objects.get('EYEBORG_FUSION')
    if fused is None:
        print('EYEBORG: no hay malla fusionada; se omiten los agujeros.')
        return None
    r = F['hole_diameter_mm'] / 2.0
    rt = F['tip_hole_diameter_mm'] / 2.0
    specs = []
    for o in list(bpy.data.objects):
        if 'linea_central' not in o.keys():
            continue
        base = o.name.rsplit('_', 1)[0] if o.name.rsplit('_', 1)[-1] in ('IZQUIERDA','DERECHA','IZQ','DER','USUARIO') else o.name
        for key, fr in HOLES_ON.items():
            if o.name.startswith(key):
                pts = _centerline(o)
                for f in fr:
                    p, n = _at(pts, f)
                    specs.append(('cyl', tuple(p), tuple(n), r, 16.0))
        if o.name.startswith('HORQUILLA_PUNTA'):
            pts = _centerline(o)
            for f in TIP_HOLES:
                p, n = _at(pts, f)
                specs.append(('cyl', tuple(p), tuple(n), rt, 14.0))
    # Plataforma de camara: bolsa, ranura de cable, hilera frontal y esquinas traseras.
    cx, cy, cz = F['camera_plate_center_mm']
    px, py, pz = F['camera_plate_mm_xyz']
    bx, by, bz = F['camera_pocket_mm_xyz']
    top = cz + pz/2.0
    specs.append(('box', (cx, cy+1.0, top - bz/2.0 + 0.01), (bx, by, bz)))               # bolsa abierta por arriba
    sx, sy = F['camera_cable_slot_mm']
    specs.append(('box', (cx, cy - py/2.0 + sy/2.0 - 0.5, cz), (sx, sy, pz + 4)))          # ranura de cable frontal
    for sgn in (1, -1):
        for x in (16.0, 24.0):
            specs.append(('cyl', (sgn*x, cy - py/2.0 + 3.5, cz), (0,0,1), rt, pz + 6))     # hilera frontal
        specs.append(('cyl', (sgn*24.5, cy + py/2.0 - 3.5, cz), (0,0,1), rt, pz + 6))      # esquinas traseras
    n = cut_with_specs(fused, specs)
    fused['cortadores'] = n
    fused['agujeros_estado'] = F['status']
    return fused

if __name__ == "__main__":
    build()
