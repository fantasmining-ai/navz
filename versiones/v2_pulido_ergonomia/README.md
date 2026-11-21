# v2 · Pulido y ergonomía

> Versión **archivada** (solo lectura). La versión actual está en [`../../modelos/`](../../modelos/) y [`../../vistas/`](../../vistas/).
> Origen: commit `5f14621` del 20/11/2026, 16:35 h. Para volver a este punto del repositorio: `git checkout 5f14621`.

![vista](imagenes/d1_iso_frontal.png)

## Qué es
Misma estructura que v1, pero **estanca y de una sola pieza** (segundo remallado y suavizado que conserva volumen), diseño 1 con acabado propio, maniquí esquemático (nariz, mentón, cuello), suelo mate y entorno de reflejos para el cromo; añade `tools/auditar.py` y el chequeo ergonómico.

## Contenido
- **Diseños:** 2: `EYEBORG.blend` y `EYEBORG_CABLEADO.blend`.
- **Archivos:** `modelos/EYEBORG.blend`, `modelos/EYEBORG_CABLEADO.blend`, `imagenes/` (renders de esa época).
- **Maniquí:** Elipsoides con nariz, mentón y cuello de 380 mm.

## Métricas
Estructura del diseño 1 medida **hoy** con `tools/auditar.py` y `tools/campo_visual.py` (mismos ojos reales de la malla CC0 → comparable entre v1-v3 y la actual).

| Métrica | Valor |
| --- | --- |
| Campo visual central / medio / periférico bloqueado (medido hoy) | 71.5 / 47.7 / 66.2 % |
| Ventana de la ranura bloqueada (medido hoy) | — |
| Medido en su momento | no medido todavía (la herramienta de campo visual se creó después) |

## Problemas conocidos
El frente sigue cruzando la mirada; el cromo azulado se veía poco profesional.

## Cómo abrirla en Blender
1. Abre `scripts/ver_disenos.py` en Blender (pestaña *Scripting*).
2. Cambia la línea `VERSION = ''` por `VERSION = 'v2_pulido_ergonomia'` y pulsa *Run Script*.
3. Cuando termines, vuelve a poner `VERSION = ''` para ver la versión actual.

Siguiente versión: v3.
