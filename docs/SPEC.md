# EYEBORG — Spec de modelado Blender (rev. 2026-11-20)

Fuente: `EYEBORG_Expediente_Tecnico_Equipo.pdf` (26 págs). Este spec cubre solo la parte **modelo 3D vía Blender + MCP**.
Electrónica, firmware y red quedan documentados en el PDF; no se tocan aquí.

## 1. Objetivo
Generar en Blender 4.x, de forma reproducible y paramétrica, el exoesqueleto orgánico azul abierto de EYEBORG
(colecciones `EYEBORG_00..13` y `EYEBORG_20_CABLEADO`), a partir de los scripts del Anexo A y `eyeborg_config.json`, ejecutándolos
a través del MCP de Blender, y validar visualmente contra las 8 vistas de referencia.

## 2. Entregables
| # | Entregable | Estado |
|---|-----------|--------|
| 1 | `scripts/*.py` + `scripts/eyeborg_config.json` | Hecho |
| 2 | Blender 5.1.2 + MCP headless | Hecho |
| 3 | `output/EYEBORG.blend` (diseño 1) | Hecho |
| 4 | `output/EYEBORG_CABLEADO.blend` (diseño 2) | Hecho |
| 5 | Renders y comparación con referencias (`docs/img/`) | Hecho |
| 6 | Cotejo ergonómico (`tools/check_ergonomia.py`) | Hecho (elipsoide, no escaneo) |
| 7 | Export STL por módulo | Pendiente / opcional |

## 3. Restricciones no negociables (del PDF)
- Unidades: 1 unidad Blender = 1 mm. Ejes: frente −Y, atrás +Y, arriba +Z, lado izquierdo del usuario +X.
- **Preservar silueta abierta**: horquilla frontal con ranura central, 2 ramas principales, ramas secundarias con ventanas, arcos de corona, puentes, placa occipital. No cerrar ni rellenar.
- Electrónica se adapta a la estructura (pods/bandejas extraíbles), nunca al revés.
- Antropometría verificada (cabeza 570 mm, envolvente 165×202×215, IPD 65, cuello 380, lentes 140): no reinterpretar “curvatura 27×35.5” ni “mandíbula 25” como radios/perímetros.
- Mantener etiquetas PROVISIONAL / PENDIENTE; el modelo es **blockout**, no apto para imprimir sin validar ajuste.
- Conflicto de cámara abierto: caja V6 41.5×28×14.5 vs módulo actual 40×28×29 (pod blockout 46×34×35).
- Objetos `REF_*` = referencias, ocultar antes de exportar.

## 4. Arquitectura de código
`00_construir_conjunto.py` (entrada) → carga 10 módulos `eyeborg_part_NN_*.py` → comparten `_eyeborg_core.py`
(sweep_ribbon, box_part, torus_part, catmull_rom, materiales) y `_eyeborg_config.py` (lee JSON). `90_cotejo_dimensional.py` imprime estado.

## 5. Estrategia MCP
- Servidor: `blender-mcp` (uvx) + addon en Blender (socket TCP, puerto 9876 por defecto).
- El MCP ejecuta código en el proceso de Blender: usar `exec` de `00_construir_conjunto.py` con `__file__` definido
  (o `bpy.ops.script.python_file_run`) para que las importaciones relativas funcionen.
- Verificación por MCP: listar colecciones/objetos, conteo de objetos, dimensiones totales, screenshot de viewport desde cámaras alineadas a las 8 vistas.

## 6. Criterios de aceptación
1. `00_construir_conjunto.py` termina sin excepciones en Blender 4.x.
2. Existen colecciones `EYEBORG_00..09` con objetos no vacíos.
3. Bounding box del conjunto estructural coherente con la envolvente de cabeza + holguras (≈165×202×215 mm + 6 mm).
4. Revisión visual: ranura frontal abierta, ventanas en ramas, arcos de corona y placa occipital reconocibles frente a vistas 01–08.
5. Cotejo dimensional impreso y sin valores fuera de `eyeborg_config.json`.
6. Reporte honesto de lo no verificable (manifold, impresión, ajuste anatómico).

## 7. Riesgos
| Riesgo | Mitigación |
|--------|-----------|
| Código solo probado con AST, nunca en Blender (el PDF lo dice) | Ejecutar por módulo, corregir errores de API 4.x iterativamente |
| Reconstrucción por vistas, sin malla original → fidelidad limitada | Aceptar blockout; iterar rutas de `sweep_ribbon` contra capturas |
| Extracción desde PDF pudo alterar indentación (se corrigió `_eyeborg_core.py` ~l.70) | Revisar diff lógico; el PDF recomienda usar el repo original si existe |
| Ejecutar código por MCP es ejecución arbitraria en Blender | Solo código del propio proyecto, revisado |
