# -*- coding: utf-8 -*-
"""EYEBORG - Visor de los tres diseños en Blender (macOS, Windows y Linux).

Muestra lado a lado:
  * DISEÑO 1  -> estructura exoesqueletica, acabado azul satinado (modelos/EYEBORG.blend)
  * DISEÑO 2  -> estructura en cromo satinado + cableado discreto + materiales (modelos/EYEBORG_CABLEADO.blend)
  * DISEÑO 3  -> igual que el 2 pero en resina translucida esmerilada, sin cromo (modelos/EYEBORG_CABLEADO_MATE.blend)

COMO USARLO (resumen; el detalle esta en docs/INSTRUCCIONES.md):
  1. Abre Blender 5.1 (o superior).
  2. Pestaña "Scripting" (arriba) -> boton "Open" -> elige este archivo -> boton "Run Script" (triangulo).
  3. Espera unos segundos. Gira con el boton central del raton y haz zoom con la rueda.

Puedes ejecutarlo varias veces: limpia lo que cargo antes.
"""
import os
import bpy

# ----------------------------- configuracion -----------------------------
VERSION = ''              # '' = version actual (carpeta modelos/). Para una anterior: p. ej. 'v3_tres_disenos_frente_abanico' (ver versiones/README.md)
SEPARACION_MM = 270.0     # distancia entre diseños (cada modelo mide ~194 x 283 x 159 mm)
ARCHIVOS = (
    ('DISENO_1', 'DISEÑO 1 - ESTRUCTURA', 'EYEBORG.blend', -SEPARACION_MM),
    ('DISENO_2', 'DISEÑO 2 - CROMO SATINADO + CABLEADO', 'EYEBORG_CABLEADO.blend', 0.0),
    ('DISENO_3', 'DISEÑO 3 - RESINA TRANSLUCIDA + CABLEADO', 'EYEBORG_CABLEADO_MATE.blend', SEPARACION_MM),
)
MARCA = 'eyeborg_visor'


def _raiz_repo():
    """Carpeta raiz del repositorio (la que contiene 'modelos' y 'scripts')."""
    try:
        ruta = os.path.abspath(__file__)
    except NameError:                      # al ejecutar desde el editor de texto
        ruta = ''
        for t in bpy.data.texts:
            if t.filepath and t.filepath.endswith('ver_disenos.py'):
                ruta = bpy.path.abspath(t.filepath)
        if not ruta:
            raise RuntimeError('No encuentro la ruta de ver_disenos.py. Abre el archivo con "Open" en la pestaña Scripting.')
    return os.path.dirname(os.path.dirname(ruta))


def _limpiar():
    """Borra lo cargado por una ejecucion anterior."""
    for ob in [o for o in bpy.data.objects if o.get(MARCA)]:
        bpy.data.objects.remove(ob, do_unlink=True)
    for col in [c for c in bpy.data.collections if c.get(MARCA)]:
        bpy.data.collections.remove(col)


def _importar(ruta, nombre_col, dx):
    if not os.path.isfile(ruta):
        raise FileNotFoundError('Falta el archivo: %s\n¿Hiciste "git pull" / descargaste todo el repositorio?' % ruta)
    with bpy.data.libraries.load(ruta, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c.startswith('EYEBORG_')]
    padre = bpy.data.collections.new(nombre_col)
    padre[MARCA] = True
    bpy.context.scene.collection.children.link(padre)
    for col in dst.collections:
        if col is not None:
            col[MARCA] = True
            padre.children.link(col)
    n = 0
    for ob in padre.all_objects:
        ob.location.x += dx
        ob[MARCA] = nombre_col
        n += 1
    return padre, n


def _etiqueta(texto, x):
    cu = bpy.data.curves.new('TXT_' + texto, 'FONT')
    cu.body = texto
    cu.size = 12.0
    cu.align_x = 'CENTER'
    cu.extrude = 0.6
    ob = bpy.data.objects.new('TXT_' + texto, cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (x, 0.0, -150.0)
    ob.rotation_euler = (1.5708, 0.0, 0.0)
    ob[MARCA] = 'etiqueta'
    return ob


def _vista():
    """Pone el visor en Material Preview y encuadra todo."""
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            sp = area.spaces.active
            sp.shading.type = 'MATERIAL'
            sp.clip_end = 20000.0
            sp.clip_start = 1.0
            region = next((r for r in area.regions if r.type == 'WINDOW'), None)
            if region is None:
                continue
            with bpy.context.temp_override(window=win, area=area, region=region):
                bpy.ops.view3d.view_all(center=True)


def main():
    raiz = _raiz_repo()
    esc = bpy.context.scene
    esc.unit_settings.system = 'METRIC'
    esc.unit_settings.scale_length = 0.001
    esc.unit_settings.length_unit = 'MILLIMETERS'
    _limpiar()
    for clave, titulo, archivo, dx in ARCHIVOS:
        base = os.path.join(raiz, 'versiones', VERSION, 'modelos') if VERSION else os.path.join(raiz, 'modelos')
        ruta = os.path.join(base, archivo)
        if VERSION and not os.path.isfile(ruta):
            print('EYEBORG: %s no existe en la version %s (se omite)' % (titulo, VERSION)); continue
        padre, n = _importar(ruta, clave, dx)
        _etiqueta(titulo, dx)
        print('EYEBORG: %s cargado (%d objetos) desde %s' % (titulo, n, archivo))
    _vista()
    print('EYEBORG: listo. Rueda = zoom, boton central = girar, Shift+boton central = mover. '
          'Para ver el diseño 2 o 3 con luces de estudio abre su archivo en modelos/ y pulsa Z -> Rendered.')


main()
