# Versiones anteriores de los diseños

Cada carpeta es una **versión archivada** del proyecto, extraída del historial de git (20/11/2026). La **versión actual (v5)** vive en [`../modelos/`](../modelos/) y [`../vistas/`](../vistas/): cabeza realista de malla base CC0, visor inuit con anclajes y ergonomía medida contra la piel real.

| Versión | Commit | Qué es | Frente | Campo central bloqueado (hoy) | Holgura mín. a la piel real | Carpeta |
| --- | --- | --- | --- | --- | --- | --- |
| **v1** Primer modelo | `911d088` | Esqueleto 3D con diagonales y abanico; 2 diseños | horquilla + abanico | 79.5 % 1.1 mm ✘ | | [`v1_primer_modelo/`](v1_primer_modelo/README.md) |
| **v2** Pulido y ergonomía | `5f14621` | Malla estanca, una sola pieza, auditoría | horquilla + abanico | 71.5 % 4.0 mm ✘ | | [`v2_pulido_ergonomia/`](v2_pulido_ergonomia/README.md) |
| **v3** Tres diseños, frente de abanico ⭐ | `b1f1a92` | **La que te gustó:** plata satinada y resina translúcida, 58 vistas | horquilla + abanico | 71.5 % 4.0 mm ✘ | | [`v3_tres_disenos_frente_abanico/`](v3_tres_disenos_frente_abanico/README.md) |
| **v4** Visor inuit (maniquí de elipsoides) | `663bcda` | Visor con ranuras, 6 anclajes, simulación del cuello | visor | 26.6 % 3.8 mm ✘ | | [`v4_visor_inuit_maniqui_elipsoides/`](v4_visor_inuit_maniqui_elipsoides/README.md) |
| **v5** Actual | `main` | Malla CC0, ergonomía real, simulación de proporciones | visor | 36.5 % | **7.9 mm ✔** | [`../modelos/`](../modelos/) |

> *Campo central bloqueado (hoy)*: porcentaje del campo visual de ±30° tapado por la estructura, medido con los **ojos reales** de la malla CC0 (`tools/campo_visual.py`). En v1-v3 el frente cruza la mirada (≈ 70-80 %); desde v4 la mirada pasa por las ranuras. La cifra de v4 no es comparable en su ranura porque se diseñó para ojos estimados.

> **A todas las versiones se les añadió la cabeza realista CC0** (sin tocar sus estructuras) para poder compararlas en igualdad de condiciones: sus imágenes `vistas/` y las cifras de arriba usan esa cabeza. *Holgura mín. a la piel real*: distancia mínima de la estructura a la piel (objetivo ≥ 6 mm); solo la versión actual la cumple.

## Cómo usarlas
- **Mirar las imágenes:** abre `vX/vistas/` o `vX/imagenes/`.
- **Abrir los modelos:** en `scripts/ver_disenos.py` cambia `VERSION = ''` por el nombre de la carpeta (por ejemplo `'v3_tres_disenos_frente_abanico'`) y ejecútalo en Blender. Las versiones v1 y v2 solo tienen dos diseños.
- **Volver el repositorio entero a una versión:** `git checkout <commit>` (y `git checkout main` para regresar).

## Peso
Los archivos de `versiones/` son copias de blobs que **ya estaban en el historial de git**, así que no agrandan la descarga del repositorio; sí ocupan disco al clonar (≈ 110 MB). Si no los necesitas, puedes borrar la carpeta en tu copia local sin afectar el resto.
