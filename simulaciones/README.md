# Simulaciones

Ver [`docs/SPEC_AJUSTE_ANATOMICO.md`](../docs/SPEC_AJUSTE_ANATOMICO.md) (§9-§11b).

## Movimiento del cuello con la estructura puesta

| Archivo | Contenido |
| --- | --- |
| [`informe_movimientos.md`](informe_movimientos.md) | Holgura mínima al torso en 14 poses + equilibrio de masas (estimado) |
| [`datos_movimientos.json`](datos_movimientos.json) | Datos crudos por pose |
| [`poses.jpg`](poses.jpg) | Hoja de las 14 poses (vista lateral izquierda) |
| [`movimiento_cuello.gif`](movimiento_cuello.gif) | Animación: extensión, flexión, giros e inclinaciones |

## Proporciones (cuánto tolera el diseño)

| Archivo | Contenido |
| --- | --- |
| [`proporciones.md`](proporciones.md) | 11 variantes de cabeza e IPD: alineación ojo–ranura, distancia a la córnea, holgura a la piel, almohadillas, campo libre |
| [`datos_proporciones.json`](datos_proporciones.json) | Datos crudos |
| [`proporciones.jpg`](proporciones.jpg) | Hoja de variantes (vista frontal) |

Regenerar:

```bash
blender -b modelos/EYEBORG_CABLEADO.blend -P tools/simulacion_movimientos.py
blender -b modelos/EYEBORG.blend -P tools/simulacion_proporciones.py
python tools/ensamblar_simulacion.py     # requiere Pillow
```

> Movimiento: modelo **esquemático** (torso de elipsoides, cables rígidos, masas estimadas). Proporciones: maniquí de malla base CC0 escalado, **no** un escaneo. No simula tejidos ni deslizamiento de la pieza sobre la piel.
