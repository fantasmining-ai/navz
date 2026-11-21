# v4 · Visor inuit (maniquí de elipsoides)

> Versión **archivada** (solo lectura). La versión actual está en [`../../modelos/`](../../modelos/) y [`../../vistas/`](../../vistas/).
> Origen: commit `663bcda` del 20/11/2026, 22:17 h. Para volver a este punto del repositorio: `git checkout 663bcda`.

![vista](vistas/diseno_2/con_maniqui/07_isometrica_frontal.jpg)

## Qué es
Primer rediseño anatómico: **visor tipo lentes inuit** con ranuras 48 × 14 mm, 6 almohadillas de anclaje (nariz, frente, oreja), brazos de sien, corona abierta con alas y espinas; sin diagonales ni horquilla cruzando los ojos. Incluye la simulación de movimientos del cuello.

## Contenido
- **Diseños:** 3: igual que v3 (estructura, cromo satinado, resina translúcida).
- **Archivos:** `modelos/EYEBORG.blend`, `modelos/EYEBORG_CABLEADO.blend`, `modelos/EYEBORG_CABLEADO_MATE.blend`, galería `vistas/` (con y sin maniquí), `simulaciones/` (movimiento del cuello), `imagenes/` (renders de esa época).
- **Maniquí:** cabeza **realista de malla base CC0** (Blender Studio) escalada a las medidas, **añadida a posteriori** a esta versión (sin tocar su estructura). El maniquí original era: elipsoides con proporciones de literatura.

## Métricas
Estructura del diseño 1 medida **hoy** con `tools/auditar.py` y `tools/campo_visual.py` (mismos ojos reales de la malla CC0 → comparable entre v1-v3 y la actual).

| Métrica | Valor |
| --- | --- |
| Campo visual central / medio / periférico bloqueado (medido hoy) | 26.6 / 23.9 / 22.6 % |
| Ventana de la ranura bloqueada (medido hoy) | 22.0 % (no comparable: la ranura se diseñó para ojos estimados a z = +6 mm; con los ojos reales de la malla CC0 quedan a z = +2.3 mm) |
| Medido en su momento | campo central 30.5 %, ventana de la ranura 1.0 %, distancia a la córnea 17.0 mm, holgura 5.9 mm, 6/6 anclajes |

## Ajuste de esta versión a la cabeza realista
Medido con `tools/check_ergonomia.py` y `tools/campo_visual.py` (diseño 1 de la versión, estructura **sin modificar**, sobre la cabeza CC0 escalada).

| Comprobación | Resultado |
| --- | --- |
| Vértices dentro de la piel | **0** |
| Vértices a menos de 4 mm de la piel | 33 |
| Holgura mínima a la piel (fuera de anclajes) | **3.8 mm** (objetivo ≥ 6 mm) ✘ |
| Distancia estructura–córnea | 24.1 mm |
| Vértices en la ventana de oreja (68 × 52 mm) | 0 |
| Campo visual central bloqueado | 26.6 % |
| Almohadillas de anclaje | la almohadilla nasal queda a 2.8 mm de la piel (flota); estaban colocadas sobre el maniquí de elipsoides |

> Esta versión no se diseñó para esta cabeza; las cifras muestran **cómo se habría comportado** y justifican los cambios de la versión siguiente.

## Problemas conocidos
Maniquí poco realista; los ojos estaban estimados 10 mm más adelante de lo que resultó con la malla real. Motivo de la versión actual.

## Cómo abrirla en Blender
1. Abre `scripts/ver_disenos.py` en Blender (pestaña *Scripting*).
2. Cambia la línea `VERSION = ''` por `VERSION = 'v4_visor_inuit_maniqui_elipsoides'` y pulsa *Run Script*.
3. Cuando termines, vuelve a poner `VERSION = ''` para ver la versión actual.

Siguiente versión: la versión actual.
