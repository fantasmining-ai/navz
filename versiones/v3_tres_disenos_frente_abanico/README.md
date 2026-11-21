# v3 · Tres diseños, frente de abanico

> Versión **archivada** (solo lectura). La versión actual está en [`../../modelos/`](../../modelos/) y [`../../vistas/`](../../vistas/).
> Origen: commit `b1f1a92 (y 574d79a)` del 20/11/2026, 18:10 h. Para volver a este punto del repositorio: `git checkout b1f1a92`.

![vista](vistas/diseno_2/con_maniqui/07_isometrica_frontal.jpg)

## Qué es
**La versión que te gustó.** Tres diseños con acabados profesionales: 1 estructura (azul satinado), 2 **plata/cromo satinado** + cableado, 3 **resina azul translúcida** + cableado, más galería de 58 vistas con y sin maniquí. Frente con horquilla de punta, diagonales de abanico y ranura nasal.

## Contenido
- **Diseños:** 3: `EYEBORG.blend`, `EYEBORG_CABLEADO.blend`, `EYEBORG_CABLEADO_MATE.blend`.
- **Archivos:** `modelos/EYEBORG.blend`, `modelos/EYEBORG_CABLEADO.blend`, `modelos/EYEBORG_CABLEADO_MATE.blend`, galería `vistas/` (con y sin maniquí), `imagenes/` (renders de esa época).
- **Maniquí:** Maniquí anatómico esquemático de elipsoides fusionadas (cráneo, cejas, párpados, nariz, labios, orejas, cuello, busto).

## Métricas
Estructura del diseño 1 medida **hoy** con `tools/auditar.py` y `tools/campo_visual.py` (mismos ojos reales de la malla CC0 → comparable entre v1-v3 y la actual).

| Métrica | Valor |
| --- | --- |
| Campo visual central / medio / periférico bloqueado (medido hoy) | 71.5 / 47.7 / 66.2 % |
| Ventana de la ranura bloqueada (medido hoy) | — |
| Medido en su momento | 79.0 / 55.8 / 66.9 % (línea base del spec; ojos estimados) |

## Problemas conocidos
Las diagonales y correas pasan por delante de los ojos (campo central bloqueado ≈ 79 %), sin anclajes definidos y sin zona libre para la mirada. Motivo del rediseño.

## Cómo abrirla en Blender
1. Abre `scripts/ver_disenos.py` en Blender (pestaña *Scripting*).
2. Cambia la línea `VERSION = ''` por `VERSION = 'v3_tres_disenos_frente_abanico'` y pulsa *Run Script*.
3. Cuando termines, vuelve a poner `VERSION = ''` para ver la versión actual.

Siguiente versión: v4.
