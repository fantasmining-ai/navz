# v1 · Primer modelo

> Versión **archivada** (solo lectura). La versión actual está en [`../../modelos/`](../../modelos/) y [`../../vistas/`](../../vistas/).
> Origen: commit `911d088` del 20/11/2026, 16:18 h. Para volver a este punto del repositorio: `git checkout 911d088`.

![vista](vistas/diseno_2/con_maniqui/07_isometrica_frontal.jpg)

## Qué es
Primera versión publicada: estructura paramétrica de esqueleto 3D (diagonal con cuerno, rieles, correas de abanico, paredes de la ranura nasal y horquilla de punta), fusión orgánica, plataforma de cámara con bolsa, agujeros de montaje y espinas de acento.

## Contenido
- **Diseños:** 2: `EYEBORG.blend` (estructura, azul satinado) y `EYEBORG_CABLEADO.blend` (cableado + cromo azulado).
- **Archivos:** `modelos/EYEBORG.blend`, `modelos/EYEBORG_CABLEADO.blend`, `imagenes/` (renders de esa época).
- **Maniquí:** cabeza **realista de malla base CC0** (Blender Studio) escalada a las medidas, **añadida a posteriori** a esta versión (sin tocar su estructura). El maniquí original era: cabeza de elipsoide + nariz/mentón sueltos (solo referencia).

## Métricas
Estructura del diseño 1 medida **hoy** con `tools/auditar.py` y `tools/campo_visual.py` (mismos ojos reales de la malla CC0 → comparable entre v1-v3 y la actual).

| Métrica | Valor |
| --- | --- |
| Campo visual central / medio / periférico bloqueado (medido hoy) | 79.5 / 51.1 / 69.9 % |
| Ventana de la ranura bloqueada (medido hoy) | — |
| Medido en su momento | no medido |

## Ajuste de esta versión a la cabeza realista
Medido con `tools/check_ergonomia.py` y `tools/campo_visual.py` (diseño 1 de la versión, estructura **sin modificar**, sobre la cabeza CC0 escalada).

| Comprobación | Resultado |
| --- | --- |
| Vértices dentro de la piel | **0** |
| Vértices a menos de 4 mm de la piel | 2802 |
| Holgura mínima a la piel (fuera de anclajes) | **1.1 mm** (objetivo ≥ 6 mm) ✘ |
| Distancia estructura–córnea | 20.6 mm |
| Vértices en la ventana de oreja (68 × 52 mm) | 4 |
| Campo visual central bloqueado | 79.5 % |
| Almohadillas de anclaje | no tiene |

> Esta versión no se diseñó para esta cabeza; las cifras muestran **cómo se habría comportado** y justifican los cambios de la versión siguiente.

## Problemas conocidos
41 islas desconectadas (puntas de espina desprendidas por el remallado); ergonomía solo contra un elipsoide.

## Cómo abrirla en Blender
1. Abre `scripts/ver_disenos.py` en Blender (pestaña *Scripting*).
2. Cambia la línea `VERSION = ''` por `VERSION = 'v1_primer_modelo'` y pulsa *Run Script*.
3. Cuando termines, vuelve a poner `VERSION = ''` para ver la versión actual.

Siguiente versión: v2.
