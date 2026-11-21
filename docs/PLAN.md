# EYEBORG — Plan y estado

Alcance y criterios: [`SPEC.md`](SPEC.md) y [`SPEC_AJUSTE_ANATOMICO.md`](SPEC_AJUSTE_ANATOMICO.md).

## Hecho
- [x] Código y configuración del expediente extraídos a `scripts/` y ejecutados en Blender 5.1.2.
- [x] Estructura reconstruida desde las 8 vistas azules, fusión orgánica, plataforma de cámara con bolsa, agujeros de montaje, espinas de acento y nodos.
- [x] **Tres diseños:** 1 estructura (azul satinado) · 2 cromo satinado + cableado · 3 resina translúcida + cableado, con estudio de iluminación propio.
- [x] Cableado discreto simulado (potencia, I2S, audio), conectores y capacitores (valores por definir). *No es un plano de cableado.*
- [x] **Ajuste anatómico:** investigación con fuentes, spec, visor inuit con ranuras alineadas a las pupilas, 6 anclajes (nariz, frente, oreja), brazos de sien.
- [x] **Maniquí con malla base CC0** (Blender Studio) escalada a las medidas verificadas; ergonomía medida contra la piel real.
- [x] Auditoría (`tools/auditar.py`), ergonomía (`check_ergonomia.py`), campo visual (`campo_visual.py`).
- [x] Simulación de movimientos del cuello (14 poses) y de proporciones (11 variantes) en `simulaciones/`.
- [x] Galería `vistas/` (58 imágenes con y sin maniquí), visor `ver_disenos.py` y guía Mac/Windows.
- [x] Versiones anteriores archivadas en `versiones/` (v1-v4) con fichas, métricas y visor por versión.
- [x] Repositorio ordenado (`modelos/`, `vistas/`, `assets/`, `simulaciones/`, `tools/dev/`).

## Pendiente
- [ ] Verificar landmarks con fotos/escaneo de la persona; aclarar el ancho de 165 mm de la envolvente (el craneo escalado mide ~157 mm).
- [ ] Tallas S/M/L generadas del mismo script y almohadillas ajustables (conclusión de la simulación de proporciones).
- [ ] F6: simulación facial dinámica (expresiones) y presión real en almohadillas.
- [ ] Reducir el bloqueo de la ranura por los puntales del puente nasal (hoy 4.2 %).
- [ ] Reconfirmar medidas nasales y de oído heredadas; definir recorrido de “curvatura” y “mandíbula”.
- [ ] Elegir tornillería/insertos y fijar el patrón final de agujeros.
- [ ] Medir módulos reales; resolver TP4056 y capacidad de la LiPo; asignar GPIO I2S; definir capacitancias.
- [ ] Revisión en laminador (espesores, puntas) y prototipo de baja resolución.
- [ ] Envío de imágenes y archivos al contacto (pendiente de conectar la extensión de Chrome).
- [ ] Licencia del proyecto.

## Entorno de desarrollo (opcional)
- Blender 5.1.2 *headless*; MCP local `fnf-blender-mcp` (no versionado).
- Herramientas: `auditar.py`, `check_ergonomia.py`, `campo_visual.py`, `simulacion_movimientos.py`, `simulacion_proporciones.py`, `render_vistas.py`, `compare_views.py`, `hojas_contacto.py`, `ensamblar_simulacion.py`, `limpiar_blend.py`, `extraer_base_cc0.py`; utilidades en `tools/dev/`.
