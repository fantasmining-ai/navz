# -*- coding: utf-8 -*-
"""Modulo EYEBORG ejecutable de forma independiente en Blender 4.x."""
import os, sys, math
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
import bpy
from _eyeborg_core import get_collection, set_materials, sweep_ribbon, box_part, cylinder_part, torus_part, mark_modular
from _eyeborg_config import *

"""Bandeja posterior modular y envolventes de referencia; los bloques no son piezas para imprimir."""
def build():
    col = get_collection('EYEBORG_08_ELECTRONICA', clear=True)
    m = set_materials()
    tray = box_part('BANDEJA_ELECTRONICA_104x58x2', (104,2,58), (0,110,-6), col,
                     material=m['blue_light'], bevel=1.5)
    tray['rol'] = 'soporte de pruebas; fijaciones finales y curvatura por validar'
    # Volúmenes en X x Y x Z (X ancho, Y profundidad, Z alto), para una primera revisión de distribución.
    # El inventario guarda largo x ancho x grosor. Aquí se orienta largo en X,
    # grosor en Y (profundidad) y ancho en Z (alto de la bandeja).
    def xyz_on_tray(key):
        d = COMPONENTS[key]['size_mm_xyz']
        return (d[0], d[2], d[1])
    items = [
      ('REF_NODEMCU', xyz_on_tray('nodemcu_esp8266_esp12e'), (-25,119,6), '49x26x13 mm; estimación legacy, medir placa real'),
      ('REF_LIPO', xyz_on_tray('lipo_bat_li_1000'), (25,114,6), '36x18x6 mm; no comprimir la celda'),
      ('REF_TP4056', xyz_on_tray('tp4056_usb_c'), (-41,114,-21), '12x17x5 mm; acceso USB-C pendiente'),
      ('REF_MT3608', xyz_on_tray('mt3608'), (-10,116,-21), '21x20x10 mm; potenciómetro sin orientar'),
      ('REF_DAC_PCM5102A', xyz_on_tray('pcm5102a'), (27,118,-21), '32x18x15 mm; jack y pines pendientes de orientación'),
    ]
    for name, dims, loc, note in items:
        obj = box_part(name, dims, loc, col, material=m['ghost'], bevel=0, wire=True)
        obj['no_imprimir'] = True
        obj['estado'] = 'envolvente de componente; no cavidad final'
        obj['observacion'] = note
    # Apoyos discretos de bandeja, dejando la retención real pendiente.
    for x in (-46,46):
        for z in (-30,18):
             post = cylinder_part('POSTE_BANDEJA_%s_%s' % (x,z), 2.5, 7, (x,114,z-6), col, material=m['blue'])
             mark_modular(post, 'separador provisional; confirmar tornillo e inserto')
    return col

if __name__ == "__main__":
    build()
