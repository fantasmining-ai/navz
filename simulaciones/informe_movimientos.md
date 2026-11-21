# Simulación de movimientos del cuello con la estructura puesta

Cinemática de dos articulaciones (suboccipital + cervical inferior) con rangos de la literatura (ver `docs/SPEC_AJUSTE_ANATOMICO.md`). Se mide la holgura mínima entre **todo lo que viaja con la cabeza** (estructura, cámara, bandeja, componentes, cables y jack de audio) y el **torso** (busto + trapecios + cuello). Holgura negativa = la pieza choca con el cuerpo. Es un modelo **esquemático** (torso de elipsoides, cables rígidos), no un análisis de tejidos.

| Pose | Flexión | Giro izq. | Incl. izq. | Holgura mín. (mm) | Pieza crítica | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| neutra | 0° | 0° | 0° | 51.2 | JACK_AUDIO_PUNTA | ✔ |
| flexion_30_lectura | 30° | 0° | 0° | 50.9 | JACK_AUDIO_PUNTA | ✔ |
| flexion_50 | 50° | 0° | 0° | 62.9 | JACK_AUDIO_PUNTA | ✔ |
| flexion_60 | 60° | 0° | 0° | 72.3 | EYEBORG_FUSION | ✔ |
| extension_30 | -30° | 0° | 0° | 41.5 | JACK_AUDIO_PUNTA | ✔ |
| extension_45 | -45° | 0° | 0° | 33.8 | JACK_AUDIO_PUNTA | ✔ |
| extension_60 | -60° | 0° | 0° | 21.8 | JACK_AUDIO_PUNTA | ✔ |
| giro_izq_45 | 0° | 45° | 0° | 46.4 | JACK_AUDIO_PUNTA | ✔ |
| giro_izq_80 | 0° | 80° | 0° | 37.2 | JACK_AUDIO_PUNTA | ✔ |
| giro_der_80 | 0° | -80° | 0° | 36.5 | JACK_AUDIO_PUNTA | ✔ |
| inclinacion_izq_45 | 0° | 0° | 45° | 46.4 | JACK_AUDIO_PUNTA | ✔ |
| inclinacion_der_45 | 0° | 0° | -45° | 51.9 | BANDEJA_ELECTRONICA_104x58x2 | ✔ |
| mirar_sobre_hombro | -15° | 70° | 15° | 34.6 | JACK_AUDIO_PUNTA | ✔ |
| extension_30_giro_45 | -30° | 45° | 0° | 34.8 | JACK_AUDIO_PUNTA | ✔ |

**Límite de extensión sin colisión:** > 70°
**Límite de flexión sin colisión:** > 70°

## Equilibrio estático respecto al pivote suboccipital (masas estimadas)

Par = masa·g·brazo horizontal (+ = tiende a extender la cabeza hacia atrás; − = a flexionarla hacia delante). Masas **estimadas, no verificadas** (ver `config → mass_estimates`).

| Pose | Cabeza sola (N·m) | Cabeza + equipo (N·m) | Equipo solo (N·m) |
| --- | --- | --- | --- |
| neutra | -0.71 | -0.69 | 0.01 |
| flexion_30 | -4.16 | -4.28 | -0.12 |
| extension_30 | 2.97 | 3.12 | 0.15 |

**Masa total del equipo:** 155 g (estructura 90 + pod/ESP32-CAM 25 + bandeja/componentes 40) — estimación.
