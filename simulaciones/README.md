# Simulaciones de movimiento

Cinemática del cuello con la estructura puesta (ver [`docs/SPEC_AJUSTE_ANATOMICO.md`](../docs/SPEC_AJUSTE_ANATOMICO.md), §10-§11).

| Archivo | Contenido |
| --- | --- |
| [`informe_movimientos.md`](informe_movimientos.md) | Holgura mínima al torso en 14 poses + equilibrio de masas (estimado) |
| [`datos_movimientos.json`](datos_movimientos.json) | Datos crudos por pose |
| [`poses.jpg`](poses.jpg) | Hoja de las 14 poses (vista lateral izquierda) |
| [`movimiento_cuello.gif`](movimiento_cuello.gif) | Animación: extensión, flexión, giros e inclinaciones |

Regenerar:

```bash
blender -b modelos/EYEBORG_CABLEADO.blend -P tools/simulacion_movimientos.py
python tools/ensamblar_simulacion.py     # requiere Pillow
```

> Modelo **esquemático**: torso de elipsoides, cables rígidos y masas estimadas. No simula tejidos ni deslizamiento de la pieza sobre la piel.
