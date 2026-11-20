"""Chequeo de holgura contra la envolvente de cabeza (elipsoide verificado por el usuario).
Uso: blender -b output/EYEBORG.blend -P tools/check_ergonomia.py"""
import bpy, math
H = (82.5, 101.0, 107.5)          # semiejes cabeza 165x202x215
GAP = 6.0                         # holgura nominal cabeza-estructura (mm)
f = bpy.data.objects['EYEBORG_FUSION']
vs = [v.co for v in f.data.vertices]
def gap_mm(p):
    r = math.sqrt((p.x/H[0])**2 + (p.y/H[1])**2 + (p.z/H[2])**2)
    # distancia aproximada a la superficie del elipsoide a lo largo del gradiente
    g = math.sqrt((p.x/H[0]**2)**2 + (p.y/H[1]**2)**2 + (p.z/H[2]**2)**2)
    return (r*r - 1) / (2*g) if g > 1e-9 else 0.0
gs = [(gap_mm(p), p) for p in vs]
inside = [g for g in gs if g[0] < 0]
tight = [g for g in gs if 0 <= g[0] < GAP]
print('VERTICES', len(gs), 'dentro_de_cabeza', len(inside), 'holgura<%.0fmm' % GAP, len(tight))
if inside:
    w = min(inside, key=lambda g: g[0])
    print('PEOR_PENETRACION_mm', round(w[0],1), 'en', [round(c,1) for c in w[1]])
mn = min(gs, key=lambda g: g[0]); print('HOLGURA_MIN_mm', round(mn[0],1), [round(c,1) for c in mn[1]])
# ventana de oreja (68x52 mm) y eje de oido (y=+6, z=-18): libre en |x|>=70 alrededor
ear = [g for g in gs if abs(g[1].y-6) < 34 and abs(g[1].z+18) < 26 and g[1].x*g[1].x > 60**2 and g[0] < 0]
print('VERTICES_EN_VENTANA_OREJA', len(ear))
# corredor nasal: |x|<20.5, z entre -45 y 5, delante de la cara (y<-60): debe estar libre
nose = [p for p in vs if abs(p.x) < 20.5 and -45 < p.z < 5 and p.y < -60]
print('VERTICES_EN_CORREDOR_NASAL', len(nose))
# oreja: cualquier vertice de estructura en la ventana 68x52 centrada en el eje del oido (y=6, z=-18), |x|>60
ear_any = [p for p in vs if abs(p.y-6) < 34 and abs(p.z+18) < 26 and abs(p.x) > 60]
print('VERTICES_EN_VENTANA_OREJA_TOTAL', len(ear_any))
print('CHECK OK')
