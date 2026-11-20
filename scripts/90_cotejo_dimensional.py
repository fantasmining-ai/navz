# -*- coding: utf-8 -*-
"""Cotejo de parámetros del proyecto; no sustituye una prueba de ajuste físico."""
import os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT,'eyeborg_config.json'),encoding='utf-8') as f:
    C = json.load(f)
A = C['anthropometry']
F = C['fit']
COMP = C['components']
CAM = C['camera']
rows = []
def add(label, value, status): rows.append((label, str(value), status))
add('Cabeza X/Y/Z (mm)', A['head_envelope_xyz_mm'], A['status'])
add('Circunferencia cabeza (mm)', A['head_circumference_mm'], A['head_circumference_status'])
add('Curvatura (mm)', A['head_curvature_reference_mm'], A['head_curvature_status'])
add('Lentes (mm)', A['lens_span_mm'], A['lens_span_status'])
add('IPD (mm)', A['ipd_mm'], A['ipd_status'])
add('Mandíbula (mm)', A['mandible_measurement_mm'], A['mandible_measurement_status'])
add('Circunferencia cuello (mm)', A['neck_circumference_mm'], A['neck_circumference_status'])
add('Espacio cráneo-carcasa (mm)', F['head_clearance_mm'], F['status'])
add('EVA (mm)', F['eva_pad_thickness_mm'], 'objetivo provisional')
add('Pared nominal (mm)', F['nominal_wall_mm'], 'objetivo provisional')
add('ESP32-CAM completa (mm)', COMP['esp32_cam_ai_thinker_complete']['size_mm_xyz'], COMP['esp32_cam_ai_thinker_complete']['status'])
add('Caja antigua cámara (mm)', CAM['legacy_case_mm_xyz'], 'CONFLICTO: altura/profundidad no contiene el volumen completo actual')
add('Nueva caja blockout (mm)', CAM['blockout_case_outer_mm_xyz'], CAM['status'])
add('NodeMCU (mm)', COMP['nodemcu_esp8266_esp12e']['size_mm_xyz'], COMP['nodemcu_esp8266_esp12e']['status'])
add('Cavidad lateral por lado (mm)', C['legacy_fit_assumptions']['cavity_lateral_clearance_each_side_mm'], 'supuesto legacy; probar coupon')
add('Cavidad profundidad total (mm)', C['legacy_fit_assumptions']['cavity_depth_clearance_total_mm'], 'supuesto legacy; probar coupon')
print('EYEBORG — COTEJO DE PARÁMETROS (mm)')
print('='*92)

for label,value,status in rows: print(f'{label:<36} {value:<28} {status}')
print('\nNOTA: el script no valida la anatomía real ni la seguridad eléctrica; solo imprime el registro.')
