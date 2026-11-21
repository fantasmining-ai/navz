# EYEBORG — Spec de modelado Blender (rev. 2026-11-20, v4)

Fuente: `EYEBORG_Expediente_Tecnico_Equipo.pdf` (26 págs). Este spec cubre la parte **modelo 3D paramétrico en Blender**.
Electrónica, firmware y red están en el expediente y en el README; el **ajuste anatómico** (ojos, nariz, orejas) tiene su propio spec:
[`SPEC_AJUSTE_ANATOMICO.md`](SPEC_AJUSTE_ANATOMICO.md).

## 1. Objetivo
Generar en Blender 5.x, de forma reproducible y paramétrica, el exoesqueleto orgánico abierto de EYEBORG en **tres diseños**
(estructura / cromo satinado + cableado / resina translúcida + cableado), con maniquí de referencia, y validarlo con herramientas medibles
(auditoría de malla, ergonomía contra la piel del maniquí, campo visual, simulación de movimientos y de proporciones).

## 2. Entregables
| # | Entregable | Estado |
|---|-----------|--------|
| 1 | `scripts/*.py` (módulos 01-15, núcleo, materiales, estudio) + `eyeborg_config.json` | Hecho |
| 2 | `modelos/EYEBORG.blend` (diseño 1: estructura) | Hecho |
| 3 | `modelos/EYEBORG_CABLEADO.blend` (diseño 2: cromo satinado + cableado) | Hecho |
| 4 | `modelos/EYEBORG_CABLEADO_MATE.blend` (diseño 3: resina translúcida + cableado) | Hecho |
| 5 | `vistas/`: 9 vistas por diseño con y sin maniquí + rayos X del cableado (58 imágenes) | Hecho |
| 6 | `assets/maniqui/`: cabeza base CC0 (Blender Studio) ajustada a las medidas | Hecho |
| 7 | Herramientas de verificación (`tools/`): auditoría, ergonomía, campo visual, simulaciones | Hecho |
| 8 | `simulaciones/`: movimiento del cuello (14 poses) y proporciones (11 variantes) | Hecho |
| 9 | Visor para tercero (`scripts/ver_disenos.py`) y guía Mac/Windows (`docs/INSTRUCCIONES.md`) | Hecho |
| 10 | Export STL por módulo | Pendiente / opcional |

## 3. Restricciones (del expediente, con la revisión v3)
- Unidades: 1 unidad Blender = 1 mm. Ejes: frente −Y, atrás +Y, arriba +Z, lado izquierdo del usuario +X.
- **Silueta abierta:** ramas, rieles, cuernos, espinas, ventanas y placa occipital; no cerrar ni rellenar. *(La horquilla frontal con ranura central fue sustituida por el visor con ranuras para ajustar a ojos y nariz.)*
- Electrónica se adapta a la estructura (pods/bandejas extraíbles), nunca al revés.
- Antropometría verificada por el usuario: cabeza 570 mm, envolvente 165 × 202 × 215, **IPD 65**, nariz 35, cuello 380, lentes 140. No reinterpretar “curvatura” ni “mandíbula”.
- Mantener etiquetas PROVISIONAL / PENDIENTE; el modelo es **blockout validado geométricamente**, no producto.
- Conflicto de cámara abierto: caja V6 41.5 × 28 × 14.5 vs módulo actual 40 × 28 × 29 (pod blockout 46 × 34 × 35).
- Objetos `REF_*` y `MANIQUI_*` son referencias: ocultar antes de exportar STL.

## 4. Arquitectura de código
`00_construir_conjunto.py` (diseño 1) → módulos en este orden: 10 referencia · **14 maniquí** (malla CC0 o procedural) · 01 anclajes centrales ·
02 barra de cámara · 03 cámara · 04/05 ramas · **15 visor y brazos** · 06 occipital · 07 barra posterior · 08 bandeja · 09 uniones ·
11 fusión orgánica · 12 agujeros, ranuras y bolsa. `00_construir_cableado.py` añade el módulo 13 (cableado), materiales y estudio y admite `cromo` o `mate`.
Comparten `_eyeborg_core.py` (correas, nodos, espinas, fusión, ergonomía contra la piel), `_eyeborg_materials.py`, `_eyeborg_studio.py` y `eyeborg_config.json`.

## 5. Entorno
- Blender 5.1.2. Los scripts se ejecutan en modo *headless* (`blender -b … -P …`); para desarrollo se usó el MCP local `fnf-blender-mcp` (sin addon ni socket), no versionado (`.mcp.json`).
- Lanzadores y utilidades: ver [`README.md`](../README.md#estructura-del-repositorio).

## 6. Criterios de aceptación (estado actual)
1. Los scripts terminan sin excepciones en Blender 5.x y reproducen los tres `.blend`. ✔
2. Malla estructural manifold y de una sola pieza (`tools/auditar.py`). ✔
3. Holgura a la piel del maniquí ≥ 6 mm fuera de anclajes (`check_ergonomia.py`): **7.9 mm**. ✔
4. Campo libre por las ranuras (`campo_visual.py`): ventana bloqueada **4.2 %** (umbral ≤ 5 %). ✔
5. Anclajes con contacto real: **6 de 6**. ✔
6. Sin colisión con el torso en 14 movimientos del cuello (`simulacion_movimientos.py`). ✔
7. Tolerancia a distintas cabezas (`simulacion_proporciones.py`): ≈ −6 %…+3 % ancho, −5 %…+2 % largo, IPD 58-68 mm; más rango requiere tallas S/M/L. ⚠ parcial
8. Revisión visual frente a las referencias (`docs/img/comparacion_referencia_vs_modelo.png`, `references/`). ✔ (silueta frontal cambiada a propósito)

## 7. Riesgos
| Riesgo | Mitigación |
| --- | --- |
| Reconstrucción por vistas, sin malla original → fidelidad limitada | Aceptar blockout; iterar trayectorias contra las capturas |
| Landmarks derivados de una cabeza genérica escalada, no de la persona | Verificar con fotos/escaneo; ancho craneal ~157 mm vs envolvente 165 mm por aclarar |
| Espinas y puntas finas (6 % de la malla < 1.2 mm) | Redondear puntas al imprimir; offset ≥ 8 mm de ojos y mejillas |
| Cableado es simulación visual | No energizar; ver README, sección de cableado |
| Sin impresión ni laminador probados | Probeta de tolerancias y prototipo económico |
