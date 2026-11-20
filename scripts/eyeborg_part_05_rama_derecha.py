# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x/5.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, strap, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *
from _eyeborg_core import thorn_from_strap, node_blob

"""Ramas laterales (esqueleto 3D medido sobre las 8 vistas azules): diagonal principal con cuerno barrido,
rieles inferior/superior, dos correas de abanico, poste de sien y pala posterior. side=+1 izquierda del usuario."""
def build_side(side, label):
    col = get_collection('EYEBORG_04_RAMA_'+label, clear=True)
    m = set_materials()
    mirror = side < 0
    ws = CONFIG.get('branch_style', {}).get('width_scale', 1.0)
    ts = CONFIG.get('branch_style', {}).get('thickness_scale', 1.0)
    def prof(p):
        return p if isinstance(p, (int, float)) else [(f, w*ws) for f, w in p]
    def thk(p):
        return p*ts if isinstance(p, (int, float)) else [(f, x*ts) for f, x in p]
    # (nombre, puntos (x,y,z) mm, ancho, grosor, material, centro para normales, cap)
    straps = [
        ('DIAGONAL_PRINCIPAL', [(10,-123,-50),(22,-119,-32),(35,-113,-10),(50,-105,18),(64,-96,44),(70,-84,66),
                                (64,-70,84),(54,-56,95),(44,-47,100)],
         [(0,12),(0.15,17),(0.5,22),(0.68,13),(0.85,6.5),(1,1)], [(0,7),(0.6,6),(1,1)], 'blue', (0,-30,0), (0.04,0.34)),
        ('RIEL_INFERIOR', [(12,-124,-56),(30,-118,-47),(52,-108,-37),(70,-88,-16),(82,-60,2),(89,-30,16),(88,0,25),
                           (84,30,28),(78,60,25),(68,85,17),(60,104,4),(54,118,-14)],
         [(0,10),(0.2,14),(0.4,20),(0.58,11),(0.78,17),(1,13)], 6.0, 'blue', (0,0,-10), (0.05,0.03)),
        ('CORREA_ABANICO_1', [(14,-123,-54),(40,-116,-42),(62,-103,-22),(76,-84,0),(84,-60,24),(86,-42,36)],
         [(0,8),(0.5,11),(1,10)], 5.5, 'blue', (0,0,-10), (0.05,0.03)),
        ('CORREA_ABANICO_2', [(13,-123,-53),(34,-118,-33),(52,-110,-10),(66,-97,12),(76,-76,34),(82,-52,48),(85,-30,56)],
         [(0,8),(0.5,10),(1,10)], 5.5, 'blue', (0,0,-10), (0.05,0.03)),
        ('RIEL_SUPERIOR', [(68,-96,44),(76,-76,46),(82,-48,52),(85,-22,62),(85,-7,76),(83,9,68),(78,32,63),
                           (72,55,60),(64,80,53),(56,96,46),(46,114,40),(38,127,34)],
         [(0,16),(0.25,25),(0.42,14),(0.6,22),(0.82,12),(1,13)], 6.0, 'blue', (0,0,10), (0.03,0.03)),
        ('POSTE_SIEN', [(88,-12,27),(87,-8,45),(86,-7,64)],
         [(0,28),(0.5,26),(1,28)], 6.5, 'blue', (0,None,None), (0.05,0.05)),
        ('ESPINA_POSTERIOR_A', [(58,94,46),(63,86,70),(56,74,100),(42,58,128)],
         [(0,18),(0.5,9),(1,1)], [(0,6),(1,1)], 'light', (0,None,None), (0.03,0.7)),
        ('ESPINA_POSTERIOR_B', [(57,96,44),(68,92,64),(74,84,92),(70,70,116)],
         [(0,15),(0.5,8),(1,1)], [(0,5),(1,1)], 'light', (0,None,None), (0.03,0.7)),
    ]
    made = {}
    for name, pts, width, thick, mk, ctr, cap in straps:
        sh = (None, 1.2) if name in ('DIAGONAL_PRINCIPAL',) or name.startswith('ESPINA_') else (None, None)
        obj = strap(name+'_'+label, pts, prof(width), thk(thick), col, material=m[mk], mirror=mirror,
                    xyz=True, center=ctr, cap=cap, sharp=sh)
        mark_modular(obj, 'union modular con puente frontal y modulo occipital')
        made[name] = obj
    # Espinas laterales barridas (estetica de las referencias metalicas): (correa, fraccion, lado, largo, base)
    thorns = [   # solo acentos: unas pocas espinas largas y barridas
        ('RIEL_SUPERIOR', 0.58, 1, 46, 10),
        ('RIEL_INFERIOR', 0.66, -1, 44, 10),
        ('DIAGONAL_PRINCIPAL', 0.46, 1, 34, 9),
    ]
    # Nodos de union: engrosan los cruces y dejan las ventanas en forma de gota.
    nodes = [
        ('NODO_SIEN_INF', (88,-12,27), (1,0,0), 9, 13, 3.6),
        ('NODO_SIEN_SUP', (86,-7,64), (1,0,0), 9, 14, 3.6),
        ('NODO_ARCO_CAMARA', (64,-104,46), (0.6,-0.8,0.1), 7, 9, 3.4),
        ('NODO_PLACA_INF', (54,118,-14), (1,0,0), 8, 14, 3.6),
        ('NODO_PLACA_SUP', (40,127,34), (1,0,0), 8, 14, 3.6),
    ]
    for nm, c_, n_, rx, ry, rz in nodes:
        node_blob(nm+'_'+label, c_, n_, rx, ry, rz, col, material=m['blue'], mirror=mirror)
    ls_ = CONFIG.get('spikes', {}).get('length_scale', 1.0)
    for key, f, sd, ln, bw in thorns:
        thorn_from_strap(made[key], f, sd, ln*ls_, bw*(0.85+0.15*ls_), col, material=m['light'], mirror=mirror,
                         name='ESPINA_%s_%d_%s' % (key.split('_')[0][:4], int(f*100), label))
    return col

if __name__ == "__main__":
    build_side(-1, "DERECHA")
