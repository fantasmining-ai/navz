# v3 · Tres diseños, frente de abanico

> Versión **archivada** (solo lectura). La versión actual está en [`../../modelos/`](../../modelos/) y [`../../vistas/`](../../vistas/).
> Origen: commit `b1f1a92 (y 574d79a)` del 20/11/2026, 18:10 h. Para volver a este punto del repositorio: `git checkout b1f1a92`.

![vista](vistas/diseno_2/con_maniqui/07_isometrica_frontal.jpg)

## Qué es
**La versión que te gustó.** Tres diseños con acabados profesionales: 1 estructura (azul satinado), 2 **plata/cromo satinado** + cableado, 3 **resina azul translúcida** + cableado, más galería de 58 vistas con y sin maniquí. Frente con horquilla de punta, diagonales de abanico y ranura nasal.

## Contenido
- **Diseños:** 3: `EYEBORG.blend`, `EYEBORG_CABLEADO.blend`, `EYEBORG_CABLEADO_MATE.blend`.
- **Archivos:** `modelos/EYEBORG.blend`, `modelos/EYEBORG_CABLEADO.blend`, `modelos/EYEBORG_CABLEADO_MATE.blend`, galería `vistas/` (con y sin maniquí), `imagenes/` (renders de esa época).
- **Maniquí:** cabeza **realista de malla base CC0** (Blender Studio) escalada a las medidas, **añadida a posteriori** a esta versión (sin tocar su estructura). El maniquí original era: elipsoides fusionadas con rasgos.

## Métricas
Estructura del diseño 1 medida **hoy** con `tools/auditar.py` y `tools/campo_visual.py` (mismos ojos reales de la malla CC0 → comparable entre v1-v3 y la actual).

| Métrica | Valor |
| --- | --- |
| Campo visual central / medio / periférico bloqueado (medido hoy) | 71.5 / 47.7 / 66.2 % |
| Ventana de la ranura bloqueada (medido hoy) | — |
| Medido en su momento | 79.0 / 55.8 / 66.9 % (línea base del spec; ojos estimados) |

## Ajuste de esta versión a la cabeza realista
Medido con `tools/check_ergonomia.py` y `tools/campo_visual.py` (diseño 1 de la versión, estructura **sin modificar**, sobre la cabeza CC0 escalada).

| Comprobación | Resultado |
| --- | --- |
| Vértices dentro de la piel | **0** |
| Vértices a menos de 4 mm de la piel | 7 |
| Holgura mínima a la piel (fuera de anclajes) | **4.0 mm** (objetivo ≥ 6 mm) ✘ |
| Distancia estructura–córnea | 23.7 mm |
| Vértices en la ventana de oreja (68 × 52 mm) | 0 |
| Campo visual central bloqueado | 71.5 % |
| Almohadillas de anclaje | no tiene |

> Esta versión no se diseñó para esta cabeza; las cifras muestran **cómo se habría comportado** y justifican los cambios de la versión siguiente.

## Problemas conocidos
Las diagonales y correas pasan por delante de los ojos (campo central bloqueado ≈ 79 %), sin anclajes definidos y sin zona libre para la mirada. Motivo del rediseño.

## Cómo abrirla en Blender
1. Abre `scripts/ver_disenos.py` en Blender (pestaña *Scripting*).
2. Cambia la línea `VERSION = ''` por `VERSION = 'v3_tres_disenos_frente_abanico'` y pulsa *Run Script*.
3. Cuando termines, vuelve a poner `VERSION = ''` para ver la versión actual.

Siguiente versión: v4.
