# SPEC — Ajuste anatómico (ojos, nariz, orejas) y maniquí realista

**Estado:** investigación, simulación e implementación F1-F5 hechas; maniquí (F2) y simulación facial (F6) con trabajo pendiente · **Rev.:** 2026-11-20 (v3) · **Aplica a:** diseños 1, 2 y 3
**Origen:** el usuario detectó que los modelos *no se adaptan a ojos ni nariz* y que el maniquí *no tiene fisonomía real ni se ve profesional*.

---

## 1. Diagnóstico (qué falló y por qué)

**Reconocimiento del error.** La estructura se construyó para parecerse a las ocho vistas azules (silueta), y la ergonomía se verificó contra un **elipsoide de cabeza** y unas elipsoides de nariz/mentón **colocadas por estimación**. Nunca se definieron puntos de referencia anatómicos (landmarks) ni zonas libres para los ojos. Debió preverse desde el inicio: una pieza que se apoya en la cara se diseña **desde la cara hacia afuera**, no al revés.

**Evidencia medida** (`tools/campo_visual.py`, rayos desde la córnea de cada ojo contra la malla estructural):

| Zona del campo visual | Rayos bloqueados por la estructura actual |
| --- | --- |
| Central (±30°) | **79.0 %** |
| Media (±50°) | **55.8 %** |
| Periférica (±70°) | **66.9 %** |

Las diagonales del frente cruzan precisamente por delante de los ojos (x ≈ 35 mm a la altura z ≈ 5 mm). Además:

1. **Sin anclajes definidos:** nada indica dónde se apoya la pieza (puente nasal, ceja, sienes, orejas). Hoy "flota" alrededor de una elipse.
2. **Maniquí sin fisonomía:** son elipsoides fusionadas (ojos = bultos, nariz = bola, sin cuencas, sin párpados, sin pliegues, orejas planas, sin textura de piel). No sirve para validar nada fino.
3. **Holguras engañosas:** "holgura 6.2 mm al maniquí" se mide contra una forma que no es una cara.

---

## 2. Referencias de diseño (del usuario)

| Referencia | Qué se toma de ella |
| --- | --- |
| **Lentes inuit** (principal para los ojos) | Banda horizontal curva que cruza los ojos con **ranuras estrechas alineadas con las pupilas**; se apoya en el puente nasal, la ceja y los pómulos/sienes; deja libre la nariz y la boca. |
| **Gafas cromadas con espinas** (principal para los ojos) | Marco envolvente que abraza las órbitas con "alas" de espinas hacia las sienes; puente nasal bajo; brazos que se anclan sobre la oreja. |
| **Visor con filigrana** (translúcido sobre los ojos) | Banda/visor continuo sobre los ojos con la estructura de espinas **encima**, no delante de la pupila. |
| **Filigrana sobre rostro realista** | Realismo del maniquí: cuencas, párpados, pliegues, labios, piel; la estructura se adhiere a pómulo y sien. |
| Piezas azules originales | Idioma formal (ramas, ventanas, espinas, cuernos) y la **idea del casco para la ESP-CAM** (barra/plataforma de cámara). |

Imágenes: `references/estetica/` y copia local no versionada en `references/privadas_local/` (contienen rostros reales).

---

## 3. Datos anatómicos de partida

> **Procedencia (actualizada tras la investigación, §9).** Los valores son **medias de poblaciones adultas** de la literatura citada en §9 (no de la persona real). Donde la fuente da un rango, se elige un valor de diseño y se anota el rango. Lo **verificado por el usuario manda siempre**; el resto queda `ESTIMADO` hasta medir a la persona (fotos frontal/perfil con regla o escaneo). Faltan por obtener: espesor de tejido blando por landmark (revisión de 139 estudios, 2024) y percentiles ANSUR II (base pública) — ver D4/D6.

Marco CAD: origen en el centro de la cabeza, `-Y` frente, `+Z` arriba, `+X` lado izquierdo del usuario, mm.

### 3.1 Datos verificados por el usuario (prevalecen)
Cabeza 165 × 202 × 215 · circunferencia 570 · **IPD 65** · **ancho de nariz 35** · cuello 380 · lentes 140.

### 3.2 Puntos de referencia (landmarks) — valores propuestos (`config → landmarks`)

| Landmark | Posición propuesta (x, y, z) mm | Nota |
| --- | --- | --- |
| Vértex (coronilla) | (0, 6, +107) | extremo superior de la envolvente |
| Glabela (entrecejo, punto más anterior de la frente baja) | (0, −101, +16) | referencia del plano facial |
| Nasion (raíz nasal; hundida respecto a la glabela) | (0, −92, +8) | ~10 mm detrás de la glabela |
| Centro de pupila / córnea (izq./der.) | (±32.5, −97, +6) | IPD 65; ojos a mitad de la altura de la cabeza |
| Centro del globo ocular | (±32.5, −85, +6) | radio ≈ 12 mm; ápex corneal 4 mm detrás de la glabela |
| Punta de pestañas | (±32.5, −109, +6) | ≈ 12 mm delante de la córnea |
| Reborde orbitario superior (ceja ósea) | z ≈ +22 … +26 | punto de apoyo frontal |
| Reborde orbitario inferior | z ≈ −14 | |
| Órbita (apertura ósea) | ≈ 40 ancho × 35 alto | |
| Fisura palpebral (apertura del ojo) | ≈ **30 largo × 8.5–11 alto** (rangos de 23–30 largo según estudio) | ranura del visor debe superar la altura de la fisura para no limitar la vista |
| Pronasal (punta nasal) | (0, −124, −40) | protrusión de la punta ≈ **21 mm**; longitud del dorso ≈ 47 mm |
| Subnasal | (0, −103, −47) | altura nasal nasion–subnasal ≈ **54–56 mm** (varones adultos, §9) |
| Alas nasales | (±17.5, −106, −43) | ancho 35 (**verificado**; la literatura da 37–41 mm: usar 35 + holgura) |
| Dorso nasal (ancho a la altura del nasion → mitad) | 12 → 20 mm | zona de apoyo de pads |
| Cigomático (pómulo) máx. | (±68, −58, −14) | ancho bicigomático ≈ 140 |
| Pómulo anterior | (±50, −88, −20) | zona de apoyo opcional |
| Sien (fosa temporal) | (±78, −20, +24) | superficie casi plana, apoyo de brazos |
| Tragus / conducto auditivo | (±77, +6, −18) | eje de oreja (dato del usuario) |
| Pabellón auricular | alto ≈ **60**, ancho ≈ **31**; distancia oreja–cráneo ≈ **9 mm**; ángulo cefalo-auricular ≈ 58° | hélix superior ≈ z +10; un brazo entre oreja y cráneo debe ser ≤ 5 mm de espesor |
| Lóbulo | z ≈ −50 | |
| Estomion (boca) | (0, −97, −66) | apertura bucal máx. **44–53 mm** (varones) |
| Mentón | (0, −104, −107) | |

### 3.3 Visión y óptica (criterios, no medidas del usuario)
- Campo visual humano: superior ≈ 50–60°, inferior ≈ 70–75°, nasal ≈ 60°, temporal ≈ 100–107°; campo binocular horizontal ≈ 114–120° (las fuentes difieren, §9). La **ceja, la nariz y el pómulo** ya lo limitan de forma natural.
- Distancia córnea–pieza: la lente de gafas típica está a ≈ **13 mm** de la córnea, con ≈ **10°** de inclinación pantoscópica y ≈ **5°** de curvatura envolvente (12–25° en gafas de sol envolventes). Objetivo de diseño: **≥ 15 mm** córnea–visor y **≥ 3 mm** sobre la punta de las pestañas (el parpadeo las barre).
- Presión tolerable (mapa de umbrales de molestia por presión, TU Delft): **umbral bajo** en nariz, mejilla/pómulo, boca, mentón y cuello anterior; **medio** en frente y sienes; **alto** en la parte posterior de la cabeza. **Consecuencia de diseño:** la carga va al **occipital, frente y sienes**; la nariz solo estabiliza con presión mínima.
- Piezas que tocan la piel: **solo** puente nasal (pads laterales, no la punta), ceja ósea/frente, sienes y oreja. **Nunca** párpado, globo, pestañas, aletas nasales ni labios.

---

## 4. Concepto de diseño: visor "inuit" + anclajes

La estructura pasa de "corona abierta que rodea una elipse" a **"visor curvo sobre los ojos, anclado a la cara, con la corona abierta encima"**:

```
        espinas / cuernos (idioma azul)          barra de cámara ESP-CAM (frente, sobre la ceja)
              \   |   /                                  ▲
   ───────────┴───┴───┴───────────  ◄── arco de ceja ───┘  (apoyo frontal, pad EVA 5 mm)
  ╭─────────────────────────────────╮
  │  ══════ ranura ══╗  ╔══ ranura ═│ ◄── VISOR: banda curva, ranuras 48 × 8 mm alineadas a cada pupila
  ╰──╮               ╚══╝          ╭─╯      (altura de ranura z = +6 ± 4)
     │ sien/oreja ◄── brazos       ╰──► brazo → apoyo sobre la oreja (gancho superior del hélix)
          ╲    ╱  ◄── puente nasal (2 pads laterales en el dorso, a la altura del nasion)
           nariz libre (corredor ±22.5 mm)   ·   boca libre
```

### 4.1 Elementos y parámetros iniciales

| Elemento | Parámetro | Valor |
| --- | --- | --- |
| Visor (banda) | extensión vertical | z ∈ [−4, +22] (cubre ojos y ceja; queda **por encima** del dorso nasal, donde la nariz aún no sobresale) |
| | offset desde la córnea | ≥ 15 mm (medido **17.0 mm**); separación 19 mm al centro → 11.5 mm en las sienes |
| | espesor de pared | 3.2 mm (+ nervaduras de rigidez en espinas) |
| Ranuras oculares | tamaño | **48 × 14 mm** (la V6 usaba 8 mm; se subió a 14 para que la ranura supere la altura de la fisura palpebral, ≈ 8–11 mm, y deje ±12° libres), centradas en la pupila (x = ±32.5, z = +6) |
| | opcional | ranura continua con "puente" nasal (variante "inuit puro") |
| Puente nasal | 2 pads laterales | sobre el dorso, z ≈ +4 … −6, separación interior ≈ 14 mm; **no** toca la punta |
| Apoyo frontal | ceja ósea | arco con pad EVA 5 mm, z ≈ +22 |
| Sienes | brazos | recorren la fosa temporal (x ≈ ±80, z ≈ +24) hacia la oreja |
| Oreja | gancho | apoya **sobre el hélix** (z ≈ +10 … +14), sin cubrir el pabellón (ventana 68 × 52 libre) |
| Pómulos | alas de espinas | opcional, sin contacto (offset ≥ 8 mm) |
| Cámara ESP-CAM | barra/plataforma | sobre la ceja, centrada, **sin entrar en el campo visual**; pod 46 × 34 × 35 provisional |
| Corona abierta (ramas, cuernos, espinas) | | **sobre** la frente/cráneo: idioma de las referencias azules, ahora separado del frente visual |

> **Decisión abierta D1:** ¿el usuario ve a través del visor (ranuras/translúcido) o la pieza es solo para cámara (ciega)? El spec asume que **debe poder ver** por las ranuras. Si fuera ciega, los criterios de campo visual no aplican.

---

## 5. Requisitos y criterios de aceptación (medibles)

| ID | Requisito | Criterio de aceptación | Herramienta |
| --- | --- | --- | --- |
| R1 | Campo visual libre por las ranuras | **Ventana de la ranura (±30° horizontal × ±12° vertical) libre ≤ 2 %**. Nota: con una ranura de 14 mm a ≈ 17 mm de la córnea la banda del visor ocluye por diseño parte del campo vertical fuera de la ranura (como los lentes inuit), por lo que no se exige ≤ 25 % del campo central completo | `tools/campo_visual.py` |
| R2 | Sin contacto con ojo/pestañas | Distancia mínima visor–punta de pestañas **≥ 3 mm**; córnea–visor **≥ 15 mm** | `tools/check_ergonomia.py` (ampliar) |
| R3 | Nariz libre | 0 vértices dentro del corredor nasal (|x| < 22.5, z −45…+5, delante de la cara) salvo pads del puente; holgura a alas/punta **≥ 6 mm** | `tools/check_ergonomia.py` |
| R4 | Anclajes definidos y con contacto real | Cada anclaje (puente, ceja, sienes ×2, orejas ×2) tiene una superficie de apoyo a **0–1 mm** de la piel (pad) y área ≥ definida | `tools/anclajes.py` (nuevo) |
| R5 | Oreja libre | 0 vértices en la ventana 68 × 52; el gancho solo sobre el hélix | `tools/check_ergonomia.py` |
| R6 | Holgura a la piel (zonas sin contacto) | ≥ 6 mm (objetivo del expediente) contra **la superficie real del maniquí** | `tools/check_ergonomia.py` |
| R7 | Estructura estanca e imprimible | manifold, 1 isla, 0 aristas no manifold (se mantiene) | `tools/auditar.py` |
| R8 | Silueta | La corona abierta conserva ramas, ventanas, cuernos y espinas de las referencias azules y la estética cyberpunk | comparación visual (`docs/img/comparacion_*`) |
| R9 | Cámara | Plataforma sobre la ceja; la línea de visión de la ESP-CAM no queda tapada por el visor ni las ramas | revisión visual + tool |
| R11 | Movimiento del cuello | Sin colisión con torso/cuello en flexión 60°, extensión 60°, giro 80° e inclinación 45° (rangos de §9), holgura ≥ 6 mm | `tools/simulacion_movimientos.py` |
| R12 | Equilibrio de masas | Par neto del equipo respecto al pivote suboccipital ≤ 10 % del par de la cabeza sola en neutra y flexión 30° (masas medidas, no estimadas) | `tools/simulacion_movimientos.py` |
| R13 | Holgura dinámica facial | Holgura estática ≥ 6 mm **y** tras aplicar el presupuesto de expresión (sonrisa ≈ 6.4 mm comisura, ceño ≈ 3–5 mm, parpadeo/pestañas 10–12 mm, apertura bucal 44–53 mm) ≥ 3 mm | simulación facial (F6) |
| R14 | Cable de audio | El jack/cable colgante no toca cuello ni hombros en ningún movimiento (hoy holgura mínima 21.8 mm en extensión 60°) | `tools/simulacion_movimientos.py` |
| R10 | Maniquí creíble | Cuencas orbitarias, párpados, ceja, dorso/alas/punta nasal, filtrum, labios, pómulos, mandíbula, oreja con hélix/antihélix/lóbulo, cuello y trapecios; piel con textura; ojos con córnea/iris/esclera | revisión visual en vistas de cerca |

---

## 6. Maniquí realista (profesionalismo)

### 6.1 Geometría
- **Landmark-driven:** la malla se ajusta a los landmarks de §3.2 (config), no a elipsoides sueltas. Cualquier cambio de medida regenera el maniquí.
- **Dos rutas** (decisión D2):
  - **A. Procedural mejorado (sin descargas):** cráneo + cuencas (resta de elipsoides) + globos oculares + párpados + ceja + dorso nasal con alas y fosas + filtrum + labios con arco de cupido + pómulos + ángulo mandibular + oreja (hélix/antihélix/trago/lóbulo) + cuello con esternocleidomastoideos + trapecios; fusión voxel y suavizado; ajuste de escala a landmarks. Resultado: maniquí estilizado de buena calidad.
  - **B. Malla base CC0 (mayor realismo):** importar una cabeza de una malla base libre de licencia (p. ej. *Human Base Meshes* de Blender Studio, CC0) y **escalarla/deformarla a los landmarks**. Requiere descargar un archivo: **necesito permiso explícito del usuario** (fuente, nombre y tamaño se indicarán antes).
- Los dos diseños comparten un único maniquí; se puede ocultar (`EYEBORG_14_MANIQUI`).

### 6.2 Materiales y texturas
- **Piel/porcelana de maniquí:** mate cálido, subsurface suave (radio por canal), micro-relieve de poro (bump), variación de tono (cejas, labios, párpados, mejillas) por máscaras procedurales.
- **Ojos:** esclera (blanco ligeramente tintado), iris radial procedural, pupila, córnea con reflejo (capa clara), párpados con línea de pestañas.
- **Cejas y pestañas:** curvas de pelo (o textura) discretas; densidad baja.
- **Labios:** tono más oscuro, roughness menor.
- Iluminación de estudio por diseño (ya existente): cromo (oscuro), resina (claro), estructura (gris claro).

---

## 7. Plan de implementación (fases y entregables)

| Fase | Trabajo | Archivos | Entregable / verificación |
| --- | --- | --- | --- |
| **F0** | Spec (este documento), referencias, línea base de campo visual | `docs/SPEC_AJUSTE_ANATOMICO.md`, `tools/campo_visual.py`, `references/` | ✔ hecho |
| **F1 ✔** | Bloque `landmarks` en `eyeborg_config.json` (valores §3.2, con estado `ESTIMADO`/`VERIFICADO`) y lector común | `scripts/eyeborg_config.json`, `_eyeborg_config.py` | tests de lectura |
| **F2 ◐** (rasgos y proporciones de literatura hechos; sin escultura realista ni texturas de piel finas) | Maniquí anatómico landmark-driven (ruta A) + materiales de piel/ojos | `eyeborg_part_14_maniqui.py`, `_eyeborg_materials.py` | vistas de cerca; `check_ergonomia` contra la malla nueva |
| **F3 ✔** | **Visor inuit + anclajes + brazos + puente nasal** como módulo nuevo; reubicar la barra de cámara; reconectar la corona abierta al visor | `eyeborg_part_15_visor.py` (+ ajustes en 01, 02, 04/05) | R1, R2, R3, R4, R5 en verde |
| **F4 ◐** (campo visual, ojos, oreja, anclajes y maniquí hechos; falta `tools/anclajes.py` independiente) | Herramientas: ampliar `check_ergonomia` (ojo/pestañas/pads), `tools/anclajes.py`, `campo_visual.py` con ranuras | `tools/*.py` | informe de auditoría de 3 diseños |
| **F6 ☐ pendiente** | Simulación facial: *shape keys* del maniquí (apertura bucal, sonrisa, ceño, parpadeo) y barrido de holguras por expresión; pads con compresión de tejido blando (4–6 mm) | `tools/simulacion_facial.py` (nuevo) | R13 en verde |
| **F5 ✔** | Reconstruir los 3 diseños, regenerar las 58 vistas, auditoría final, actualizar README/INSTRUCCIONES/PLAN | `modelos/`, `vistas/`, `docs/` | repo sincronizado |

**Orden de dependencias:** F1 → F2 y F3 en paralelo (ambos leen landmarks) → F4 → F5.
**Criterio de cierre:** todos los R1–R10 en verde o con desviación documentada y aceptada por el usuario.

---

## 8. Riesgos y decisiones pendientes

| # | Riesgo / decisión | Impacto |
| --- | --- | --- |
| D1 ✔ | ¿Se ve a través del visor? **Resuelta por el usuario** (referencia: lentes inuit → se ve por ranuras) | Define R1 |
| D2 | Ruta A (procedural) vs B (malla base CC0 descargada) para el maniquí | Realismo del maniquí; B requiere permiso de descarga |
| D3 | Medidas faciales reales de la persona (nasion, alas, pómulo, oreja) | Sin ellas los landmarks son **estimados**; el ajuste fino exige fotos o escaneo |
| D4 | Datos de §3 no verificados con fuentes en esta sesión | Verificar antes de fabricar |
| D6 | Descargar la base pública ANSUR II (CSV) para percentiles de cabeza/cara y elegir el rango de tallas | Requiere permiso de descarga |
| D5 | Rediseño del frente cambia la silueta frente a las vistas azules | Se preserva la corona abierta y el idioma; confirmar con el usuario |
| R-a | Las espinas cerca de ojos/mejillas pueden ser un riesgo de lesión | Offset ≥ 8 mm, puntas redondeadas al imprimir, sin espinas hacia el ojo |
| R-b | Peso y presión en el puente nasal | Pads anchos, distribuir carga en ceja/sienes/orejas |

---

## 9. Investigación (fuentes y hallazgos)

Búsquedas realizadas el 2026-11-20. Los números son los que devolvieron las fuentes; entre estudios hay diferencias de método y población, por eso se dan **rangos**.

| Tema | Hallazgo | Fuente |
| --- | --- | --- |
| **Rango del cuello** | Norma clínica: flexión ≈ 50°, extensión ≈ 60°, inclinación lateral ≈ 45°, rotación ≈ 80°. Medido en adultos sanos: flexión ≈ 68°, extensión ≈ 68°, inclinación ≈ 50°, rotación ≈ 78° por lado (rangos más altos con medición 3D). | [Normal functional ROM of the cervical spine (PSU)](https://pure.psu.edu/en/publications/normal-functional-range-of-motion-of-the-cervical-spine-during-15/) · [PMC2899663](https://pmc.ncbi.nlm.nih.gov/articles/PMC2899663) · [Chiropractic & Manual Therapies 2018](https://link.springer.com/doi/10.1186/s12998-018-0223-x) |
| **Uso funcional del cuello** | En 15 actividades diarias se usa 12–92 % de la rotación (mediana ≈ 19 %, 18°); retroceder en coche exige 92 % de la rotación, 32 % sagital y 26 % lateral; cruzar la calle: 31.7° izq. / 54.3° der.; el 90–92 % de los movimientos tiene < 25° de inclinación lateral. | [PSU](https://pure.psu.edu/en/publications/normal-functional-range-of-motion-of-the-cervical-spine-during-15/) · [Task-specific frequencies of neck motion](https://pubmed.ncbi.nlm.nih.gov/19282725) |
| **Aceleración de la cabeza** | En actividades cotidianas (incl. caminar y correr) los picos de aceleración lineal de la cabeza son < 15 g: envolvente de diseño para la **retención** del equipo. | [Envelope of linear and rotational head motion](https://pubmed.ncbi.nlm.nih.gov/31786677/) |
| **Nariz (varones adultos)** | Altura nasal (nasion–subnasal) ≈ 54–56 mm; longitud del dorso ≈ 47; **protrusión de la punta ≈ 21 mm**; longitud alar ≈ 29; ancho ≈ 37–41 mm (según población). | [Anthropometric analysis of the external nose](https://www.springermedicine.com/anthropometric-analysis-of-the-external-nose-of-the-egyptian-mal/20766454) · [PMC8820299](https://pmc.ncbi.nlm.nih.gov/articles/PMC8820299) |
| **Ojo / párpados** | Fisura palpebral ≈ 30 mm de largo (23–30 según estudio) × 8–11 mm de alto. | [EyeWiki: Dysmorphology of the Eye and Periorbital Region](https://eyewiki.aao.org/Dysmorphology_of_the_Eye_and_Periorbital_Region) · [PMC8805858](https://pmc.ncbi.nlm.nih.gov/articles/PMC8805858/table/t0003) |
| **Oreja (varones)** | Largo ≈ 59.9 mm, ancho ≈ 30.7 mm, distancia oreja–cráneo ≈ 8.7 mm, ángulo cefalo-auricular ≈ 57.6° (n = 200); proyección media ≈ 30° en la literatura quirúrgica. | [Anatomical Sciences Journal 2020](https://doaj.org/article/4ad62b8df3b44dd5a76831b93cd2b265) · [Morphometry of the normal human ear](https://pubmed.ncbi.nlm.nih.gov/10731092/) |
| **Apertura bucal** | Máxima apertura interincisal en varones ≈ 44–53 mm según población (Grecia 52.9; India 51.3 / 48.0; Turquía 44.2; Jordania 45.3). | [PMC11621472](https://pmc.ncbi.nlm.nih.gov/articles/PMC11621472) · [JCDA](https://cda-adc.ca/jcda/vol-69/issue-11/737.pdf) |
| **Campo visual** | Temporal ≈ 100–107°, nasal ≈ 60°, superior ≈ 50–60°, inferior ≈ 70–75°; binocular ≈ 114–120°. La nariz limita el campo nasal y la ceja/pómulo los límites vertical. | [Lens.com: total visual field](https://www.lens.com/what-is/total-visual-field/) · [Visual field (Wikipedia)](https://wikipedia.com/wiki/Visual_field) |
| **Ajuste de gafas** | Promedios: distancia al vértice ≈ 13 mm, inclinación pantoscópica ≈ 10°, curvatura envolvente ≈ 5° (12–25° en gafas envolventes). | [2020 Mag: vertex, tilt and wrap](https://2020mag.com/article/the-real-details-of-vertex-tilt-and-wrap-part-two-of-three) |
| **Presión tolerable** | Umbrales de molestia bajos en nariz, mejilla/pómulo, boca, mentón y cuello anterior; medios en frente y sienes; altos en la parte posterior de la cabeza. Los HMD usan almohadillas nasales solo para estabilizar. | [Dense 3D pressure discomfort threshold map of the head, face and neck (TU Delft)](https://repository.tudelft.nl/record/uuid:b4e52a96-cdbb-446f-b26e-4c509d30d016) |
| **Movimiento facial** | Sonrisa: la comisura labial se mueve ≈ 6.4 mm (hacia arriba y afuera), poco movimiento en nariz/ojos/cejas; el ceño mueve la piel de la frente sobre todo en vertical; la topografía facial estática varía 0.55–0.7 mm y hasta ≈ 5 mm en expresiones. | [Smile landmark tracking (eScholarship)](https://escholarship.org/uc/item/6m022427) · [Frontalis skin vectors (PMC8356875)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356875) · [ISPRS 2025](https://isprs-archives.copernicus.org/articles/XLVIII-2-W9-2025/275/2025/) |
| **Bases de datos** | ANSUR II (4 082 varones; incluye anchos interpupilar, de oreja, etc.) con CSV público; informe técnico con percentiles. | [ANSUR II (US Army Public Health)](https://ph.health.mil/topics/workplacehealth/ergo/Pages/Anthropometric-Database.aspx) · [DTIC ADA611869](https://apps.dtic.mil/sti/pdfs/ADA611869.pdf) |

**Huecos de la investigación (pendientes):** espesor de tejido blando por landmark (glabela, nasion, cigomático, sien; ver revisión de 139 estudios en *Int. J. Legal Medicine*, 2024), longitud de pestañas, desplazamiento milimétrico de la ceja y percentiles ANSUR II. Hasta tenerlos, los pads se dimensionan con 4–6 mm de compresión **estimada**.

## 10. Simulación de movimientos corporales (resultados)

`tools/simulacion_movimientos.py` modela el cuello con dos articulaciones (suboccipital y cervical inferior) y mueve **todo lo que viaja con la cabeza** (estructura, cámara, bandeja, componentes, cables y jack) contra un torso de elipsoides. Resultados completos en [`simulaciones/informe_movimientos.md`](../simulaciones/informe_movimientos.md), hoja de poses [`simulaciones/poses.jpg`](../simulaciones/poses.jpg) y animación [`simulaciones/movimiento_cuello.gif`](../simulaciones/movimiento_cuello.gif).

| Hallazgo | Dato |
| --- | --- |
| Choque con torso/cuello | **Ninguno** en 14 poses (flexión hasta 60°, extensión hasta 60°, giro ±80°, inclinación ±45°, "mirar sobre el hombro") |
| Holgura mínima al torso | 21.8 mm (extensión 60°; pieza crítica: jack de audio colgante); 34–60 mm en el resto |
| Limitación real | **No está en el cuello sino en la cara**: la estructura bloquea el 79 % del campo visual central y no tiene anclajes anatómicos (§1) |
| Equilibrio de masas (estimado) | Equipo ≈ 155 g; par del equipo ≈ ±0.01 N·m en neutra frente a ≈ 0.7 N·m de la cabeza sola → **bien equilibrado** (la barra de cámara delante compensa la bandeja trasera) |
| Alcance de la simulación | Torso esquemático, cables rígidos y masas estimadas. No hay simulación de tejidos ni deslizamiento; eso es F6 |

## 11. Resultados de la implementación (los 3 diseños, rev. v3)

Medido con `tools/campo_visual.py`, `tools/check_ergonomia.py` y `tools/auditar.py` sobre los tres `.blend` (comparten la misma malla estructural).

| Métrica | Antes (rev. anterior) | **Ahora** | Criterio | Estado |
| --- | --- | --- | --- | --- |
| Campo visual central (±30°) bloqueado | 79.0 % | **30.5 %** | (la banda del visor ocluye por diseño; ver R1) | mejora de 48 puntos |
| Campo visual medio (±50°) bloqueado | 55.8 % | **30.8 %** | — | ✔ |
| Campo visual periférico (±70°) bloqueado | 66.9 % | **31.3 %** | — | ✔ |
| **Ventana de la ranura** (±30° × ±12°) bloqueada | — | **1.0 %** | ≤ 2 % (R1) | ✔ |
| Distancia estructura–córnea | no medida | **17.0 mm** | ≥ 15 mm (R2) | ✔ |
| Vértices en la ventana de oreja 68 × 52 | 0 | **0** | 0 (R5) | ✔ |
| Anclajes (6 almohadillas: nariz ×2, frente ×2, oreja ×2) | no existían | **contacto 0.0 mm** con la piel del maniquí | R4 | ✔ |
| Vértices dentro del maniquí | 0 | **0** | 0 | ✔ |
| Holgura mínima a la piel (fuera de anclajes) | 6.2 mm | **5.9 mm** | ≥ 6 mm (R6) | ⚠ desviación de 0.1 mm en el riel superior trasero (sin impacto en ojos/nariz) |
| Malla manifold / islas | ✔ / 1 | **✔ / 1** | R7 | ✔ |
| Dimensiones (X × Y × Z) | 194 × 283 × 159 mm | **193 × 283 × 137 mm** | — | más baja |
| Volumen de la estructura | 249 cm³ | **184 cm³** | — | −26 % |
| Colisión con el torso en 14 poses | ninguna | **ninguna** (mín. 21.8 mm) | R11 | ✔ |

**Qué cambió en el diseño**
- **Eliminado del frente:** las diagonales, correas de abanico, paredes de ranura nasal y la horquilla de punta que cruzaban ojos y nariz.
- **Nuevo:** visor inuit curvo (z −4…+22) con **dos ranuras 48 × 14 mm** alineadas a las pupilas; **almohadillas EVA** en el dorso nasal (2), la frente (2) y sobre el hélix (2); **brazos de sien** con gancho sobre la oreja; puntales de cámara desde el visor a la barra de la ESP-CAM.
- **Conservado:** corona abierta (diagonal principal con cuerno, rieles, espinas de acento, alas), placa occipital, plataforma de cámara con bolsa.
- **Maniquí:** rasgos con proporciones de literatura (dorso nasal en 3 tramos con punta a 21 mm de protrusión, alas, párpados separados por la IPD de 65 mm, ceja ósea, pómulos, orejas de 60 × 31 mm).

**Pendiente / limitaciones**
- Los landmarks son **estimados de literatura**, no medidos en la persona (D3). Hay que verificar con fotos/escaneo antes de fabricar.
- El maniquí es mejor que el anterior pero **sigue siendo esquemático**: sin escultura realista ni piel fina. La ruta B (malla base CC0) requiere permiso de descarga (D2).
- F6 (expresiones faciales dinámicas) y verificación de presión en las almohadillas no están hechas.
- La ranura de 14 mm no se contrastó con un usuario real; si se quisiera la ranura estrecha tradicional, el campo visual vertical se reduce.

## 12. Fuera de alcance
Certificación de seguridad, resistencia mecánica, ajuste médico/óptico real, impresión y pruebas de usuario. El resultado sigue siendo **blockout validado geométricamente**, no producto.
