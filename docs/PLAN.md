# EYEBORG — Plan y estado

Ver [`SPEC.md`](SPEC.md) para alcance y criterios.

## Hecho
- [x] Extracción del código y la configuración del expediente a `scripts/` (sintaxis y ejecución verificadas en Blender 5.1.2).
- [x] Reconstrucción de la estructura desde un esqueleto 3D medido sobre las 8 vistas azules (diagonales, rieles, abanico, poste de sien, cuernos).
- [x] Fusión orgánica, plataforma de cámara con bolsa, agujeros de montaje, espinas de acento y nodos de unión.
- [x] Ergonomía: holgura ≥ 6 mm a la cabeza, corredor nasal, ventana de oído (`tools/check_ergonomia.py`).
- [x] Diseño 2: cableado discreto simulado, componentes, capacitores (valores por definir), materiales procedurales y estudio de iluminación.
- [x] Visor `scripts/ver_disenos.py` y guía `docs/INSTRUCCIONES.md` (Mac y Windows).
- [x] Auditoría estructural (`tools/auditar.py`): malla estanca, una sola pieza; maniquí esquemático.
- [x] Diseño 2 en cromo satinado (referencia: máscara de plata; estudio con softboxes y tiras de luz) y diseño 3 en resina translúcida esmerilada sin cromo (referencia: gafas de resina azul; grano fino, bordes pulidos, carbono en sarga, aluminio cepillado). Maniquí anatómico esquemático con rasgos faciales.
- [x] Galería `vistas/`: 9 vistas con y sin maniquí por diseño + rayos X del cableado.
- [x] Repositorio reorganizado (`modelos/`, `vistas/`, `tools/dev/`).

- [x] Ajuste anatómico (spec + investigación con fuentes + simulación de movimientos): visor inuit con ranuras alineadas a las pupilas, anclajes (nariz, frente, oreja), campo visual y distancias medidas.

## Pendiente
- [ ] Verificar landmarks con fotos/escaneo de la persona; elegir ruta B para el maniquí (malla base CC0, requiere permiso de descarga).
- [ ] F6: simulación facial dinámica (expresiones) y presión en almohadillas.
- [ ] Reconfirmar medidas nasales y de oído heredadas; definir recorrido de “curvatura” y “mandíbula”.
- [ ] Validar holguras con prototipo de baja resolución; escaneo 3D de cabeza si es posible.
- [ ] Elegir tornillería/insertos y fijar el patrón final de agujeros.
- [ ] Medir módulos reales; resolver TP4056 y capacidad de la LiPo; asignar GPIO I2S; definir capacitancias.
- [ ] Revisión de manifold/espesores y redondeo de puntas antes de imprimir.
- [ ] Licencia del proyecto.

## Entorno de desarrollo (opcional)
- Blender 5.1.2 en modo *headless*; MCP `fnf-blender-mcp` registrado localmente (no se versiona `.mcp.json`).
- Herramientas: `tools/render_views.py`, `tools/compare_views.py`, `tools/render_detail.py`, `tools/render_cableado.py`, `tools/check_ergonomia.py`.
