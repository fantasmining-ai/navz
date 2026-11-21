"""Genera las hojas resumen (JPG) y el índice vistas/README.md a partir de vistas/. Requiere Pillow:  pip install pillow
Uso: python tools/hojas_contacto.py"""
import os, glob
from PIL import Image, ImageDraw
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISENOS = (('diseno_1', 'Diseño 1 · Estructura (azul satinado)', 'modelos/EYEBORG.blend'),
           ('diseno_2', 'Diseño 2 · Cromo satinado + cableado', 'modelos/EYEBORG_CABLEADO.blend'),
           ('diseno_3', 'Diseño 3 · Resina translúcida + cableado', 'modelos/EYEBORG_CABLEADO_MATE.blend'))
VARIANTES = (('con_maniqui', 'Con maniquí'), ('sin_maniqui', 'Sin maniquí'))
md = ['# Vistas de los diseños EYEBORG\n',
      'Imágenes de cada vista de los tres diseños, **con y sin maniquí esquemático** (cráneo 165 × 202 × 215 mm, nariz, mentón y cuello de 380 mm; no es un escaneo).\n',
      'Vistas ortográficas: frente, trasera, lateral izquierda/derecha (del usuario), superior e inferior. Perspectivas: isométrica frontal, isométrica trasera y detalle de la cámara. '
      'Los diseños 2 y 3 añaden vistas en rayos X del cableado (solo sin maniquí).\n',
      '> Generadas con `tools/render_vistas.py` (Blender Cycles). Los archivos fuente están en `modelos/`.\n']
for d, titulo, blend in DISENOS:
    md.append('\n## %s\n\nArchivo: `%s`\n' % (titulo, blend))
    for sub, nombre in VARIANTES:
        fs = sorted(glob.glob(os.path.join(raiz, 'vistas', d, sub, '*.jpg')))
        if not fs: continue
        w, h = 560, 420; cols = 3; rows = (len(fs) + cols - 1) // cols
        hoja = Image.new('RGB', (cols * w, rows * h), (14, 16, 20)); dr = ImageDraw.Draw(hoja)
        for i, f in enumerate(fs):
            im = Image.open(f).convert('RGB').resize((w, h)); x, y = (i % cols) * w, (i // cols) * h
            hoja.paste(im, (x, y)); dr.rectangle((x, y, x + w - 1, y + 22), fill=(0, 0, 0))
            dr.text((x + 8, y + 5), os.path.basename(f)[:-4], fill=(220, 235, 245))
        hoja_png = os.path.join(raiz, 'vistas', d, 'hoja_%s.jpg' % sub)
        hoja.save(hoja_png, quality=88)
        md.append('\n### %s\n\n![hoja](%s/hoja_%s.jpg)\n\n| Vista | Archivo |\n| --- | --- |' % (nombre, d, sub))
        for f in fs:
            rel = '%s/%s/%s' % (d, sub, os.path.basename(f))
            md.append('| %s | [`%s`](%s) |' % (os.path.basename(f)[:-4].replace('_', ' ', 1).replace('_', ' '), rel, rel))
        md.append('')
open(os.path.join(raiz, 'vistas', 'README.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print('hojas e índice generados')
