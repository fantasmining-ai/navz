# Guía paso a paso: ver los diseños EYEBORG en Blender (Mac y Windows)

Esta guía está pensada para alguien **sin experiencia en comandos**. Sigue los pasos en orden y no te saltes ninguno.
Al final verás en Blender, lado a lado:

- **Diseño 1:** la estructura exoesquelética (acabado azul satinado).
- **Diseño 2:** la estructura en **cromo satinado** con **cableado discreto simulado**, componentes y materiales.
- **Diseño 3:** igual que el 2 pero en **resina translúcida esmerilada** (sin cromo), con texturas realistas de impresión 3D.

> ¿Solo quieres *mirar* sin instalar nada? Las imágenes de todas las vistas (con y sin maniquí) están en la carpeta **`vistas/`** del proyecto: se abren con cualquier visor de imágenes. Hay un índice en `vistas/README.md`.

> Tiempo estimado: 20-30 minutos la primera vez (casi todo es descargar e instalar).
> Necesitas: una computadora Mac o Windows, conexión a internet y unos **2 GB** libres en disco.

---

## Índice

1. [Instalar Blender](#1-instalar-blender)
2. [Descargar el proyecto](#2-descargar-el-proyecto) (opción A sin comandos · opción B con `git clone`)
3. [Abrir los diseños con el script](#3-abrir-los-diseños-con-el-script)
4. [Moverte por el modelo](#4-moverte-por-el-modelo)
5. [Ver el cableado (rayos X)](#5-ver-el-cableado-rayos-x)
6. [Ver el diseño 2 con luces de estudio y hacer un render](#6-ver-el-diseño-2-con-luces-de-estudio-y-hacer-un-render)
7. [Actualizar el proyecto cuando haya cambios](#7-actualizar-el-proyecto)
8. [Problemas frecuentes](#8-problemas-frecuentes)
9. [Avanzado: reconstruir los diseños desde el código](#9-avanzado-reconstruir-desde-el-código)

---

## 1. Instalar Blender

Blender es un programa **gratuito** de modelado 3D. Necesitas la **versión 5.1 o más reciente**
(los archivos del proyecto se crearon con Blender 5.1; con versiones muy antiguas, como 3.x o 4.0, pueden no abrir bien).

### En Mac

1. Abre el navegador y entra a **https://www.blender.org/download/**
2. Pulsa el botón de descarga. La página detecta tu Mac; si te deja elegir, usa:
   - **macOS Apple Silicon** si tu Mac es de 2020 o más nueva (chip M1, M2, M3, M4…).
   - **macOS Intel** si es una Mac más antigua.
   - *No sabes cuál tienes?* Menú  (arriba a la izquierda) → **Acerca de este Mac**. Si dice "Chip: Apple M…" es Apple Silicon; si dice "Procesador: Intel…" es Intel.
3. Abre el archivo `.dmg` que se descargó (carpeta **Descargas**).
4. Arrastra el icono de **Blender** a la carpeta **Aplicaciones**.
5. Abre **Blender** desde Aplicaciones (o con Spotlight: `Cmd + Espacio`, escribe "Blender", Enter).
6. La primera vez macOS puede avisar *"Blender es una app descargada de internet"*. Pulsa **Abrir**.
   Si lo bloquea: **Ajustes del Sistema → Privacidad y seguridad →** baja hasta ver el aviso de Blender y pulsa **Abrir de todos modos**.
7. Aparece una pantalla de bienvenida: pulsa fuera de ella (o en cualquier espacio gris) para cerrarla.

### En Windows

1. Abre el navegador y entra a **https://www.blender.org/download/**
2. Pulsa **Download Blender** (instalador `.msi` o `.zip`; el `.msi` es lo más fácil).
3. Abre el archivo descargado y sigue el instalador: **Next → Next → Install → Finish**.
4. Abre **Blender** desde el menú Inicio (escribe "Blender").
5. Si Windows muestra *"Windows protegió su PC"*: pulsa **Más información → Ejecutar de todas formas**.
6. En la pantalla de bienvenida pulsa fuera de ella para cerrarla.

---

## 2. Descargar el proyecto

El proyecto está en: **https://github.com/rslnt1270/Navy_Project**

Elige **una** de las dos opciones. **La opción A es la más fácil.**

### Opción A: sin comandos (descargar el ZIP)

1. Entra a **https://github.com/rslnt1270/Navy_Project**
2. Pulsa el botón verde **`<> Code`** → **Download ZIP**.
3. Cuando termine:
   - **Mac:** haz doble clic en el ZIP (se descomprime solo) y mueve la carpeta `Navy_Project-main` a **Documentos**.
   - **Windows:** clic derecho en el ZIP → **Extraer todo…** → elige **Documentos** → **Extraer**.
4. Apunta la ubicación: la carpeta debe quedar como `Documentos/Navy_Project-main` y dentro verás `scripts`, `modelos`, `docs`…

Salta a [3. Abrir los diseños con el script](#3-abrir-los-diseños-con-el-script).

### Opción B: con `git clone` (recomendada si vas a recibir actualizaciones)

`git` es un programa que descarga y mantiene al día un proyecto. Solo necesitas **copiar y pegar** los comandos.

#### Mac

1. Abre la **Terminal**: `Cmd + Espacio`, escribe **Terminal** y pulsa Enter. Se abre una ventana con letras (no te asustes).
2. Comprueba si ya tienes `git`: copia, pega y pulsa Enter:

   ```bash
   git --version
   ```

   - Si responde algo como `git version 2.x.x`, ya lo tienes. Sigue al paso 3.
   - Si aparece una ventana *"Se requieren las herramientas de línea de comandos"*, pulsa **Instalar**, acepta y **espera a que termine** (puede tardar varios minutos). Luego repite `git --version`.
3. Ve a la carpeta Documentos:

   ```bash
   cd ~/Documents
   ```

   > Si tu Mac está en español y falla, prueba `cd ~/Documentos`.
4. Descarga el proyecto (esto es el **`git clone`**):

   ```bash
   git clone https://github.com/rslnt1270/Navy_Project.git
   ```

   Verás líneas como `Cloning into 'Navy_Project'…` y `Receiving objects: 100%`. Cuando vuelva a aparecer el cursor, terminó.
5. Entra a la carpeta (opcional, para comprobar):

   ```bash
   cd Navy_Project
   ls
   ```

   Debes ver: `README.md  docs  modelos  references  scripts  tools  vistas`.

#### Windows

1. Instala **Git para Windows**: entra a **https://git-scm.com/download/win**, descarga el instalador, ábrelo y pulsa **Next** en todas las pantallas (los valores por defecto sirven) → **Install** → **Finish**.
   *(Alternativa: abre PowerShell y escribe `winget install --id Git.Git -e`)*
2. Abre una terminal. La forma más fácil: abre el menú Inicio, escribe **Git Bash** y pulsa Enter.
   (También sirve **PowerShell**: los comandos de abajo son iguales.)
3. Ve a la carpeta Documentos:

   - En **Git Bash**:

     ```bash
     cd ~/Documents
     ```
   - En **PowerShell**:

     ```powershell
     cd "$HOME\Documents"
     ```

   > Si tu Windows está en español y la carpeta se llama *Documentos*, prueba `cd ~/Documentos` (Git Bash) o `cd "$HOME\Documentos"` (PowerShell).
4. Descarga el proyecto (esto es el **`git clone`**):

   ```bash
   git clone https://github.com/rslnt1270/Navy_Project.git
   ```

   Cuando vuelva a aparecer el cursor, terminó.
5. Entra a la carpeta (opcional):

   ```bash
   cd Navy_Project
   dir
   ```

   (En Git Bash usa `ls`). Debes ver: `README.md  docs  modelos  references  scripts  tools  vistas`.

> **No necesitas cuenta de GitHub ni llaves SSH.** Si te pidiera usuario y contraseña, avisa a quien te pasó el proyecto: puede que el repositorio sea privado y haya que darte acceso.

---

## 3. Abrir los diseños con el script

1. Abre **Blender** (si no está abierto).
2. Arriba de la ventana hay pestañas: *Layout, Modeling, Sculpting, UV Editing…* Pulsa la que dice **Scripting**.
   *(Si no la ves, pulsa la flecha `>` al final de las pestañas, o desliza con la rueda del ratón sobre ellas.)*
3. En el panel de la **izquierda-centro** (el editor de texto, fondo oscuro) pulsa el botón **Open** (o menú *Text → Open*).
4. Se abre un explorador de archivos. Busca la carpeta del proyecto y entra a **`scripts`**:

   - **Mac:** pulsa `Cmd + Shift + G`, pega la ruta y Enter:
     - Si usaste **git clone**: `~/Documents/Navy_Project/scripts`
     - Si usaste **ZIP**: `~/Documents/Navy_Project-main/scripts`
   - **Windows:** haz clic en la barra de dirección del explorador de Blender (arriba) y escribe la ruta:
     - **git clone:** `C:\Users\TU_USUARIO\Documents\Navy_Project\scripts`
     - **ZIP:** `C:\Users\TU_USUARIO\Documents\Navy_Project-main\scripts`
     (cambia `TU_USUARIO` por tu nombre de usuario de Windows).
5. Selecciona el archivo **`ver_disenos.py`** y pulsa **Open Text** (o *Abrir texto*).
6. Pulsa el botón del **triángulo ▶ "Run Script"** (arriba del editor de texto), o presiona `Alt + P` (Mac: `Option + P`).
7. Espera de **10 a 30 segundos**. Cuando termine, ve a la pestaña **Layout** (arriba): verás los tres diseños lado a lado.
   - A la **izquierda**: *DISEÑO 1 - ESTRUCTURA*.
   - En el **centro**: *DISEÑO 2 - CROMO SATINADO + CABLEADO*.
   - A la **derecha**: *DISEÑO 3 - RESINA TRANSLÚCIDA + CABLEADO*.

Si todo salió bien, en la parte inferior de la ventana (o en *Window → Toggle System Console* en Windows) verás líneas que empiezan con `EYEBORG: … cargado` (una por diseño).

---

## 4. Moverte por el modelo

| Acción | Ratón con rueda (Windows / Mac con ratón) | Trackpad de Mac |
| --- | --- | --- |
| **Girar** la vista | Mantén pulsada la **rueda** (botón central) y mueve | Activa *Edit → Preferences → Input → Emulate 3 Button Mouse*; luego `Option` + arrastrar con un dedo |
| **Acercar / alejar** | Gira la **rueda** | Pellizca con dos dedos, o desliza dos dedos arriba/abajo |
| **Mover** (desplazar) | `Shift` + rueda pulsada y mover | `Shift` + `Option` + arrastrar (con *Emulate 3 Button Mouse*) |
| **Encuadrar todo** | Tecla `Inicio` / `Home` | Menú **View → Frame All** |

Más trucos:

- **Vistas rápidas** (si tienes teclado numérico): `1` frente, `3` lado, `7` arriba, `5` perspectiva/ortográfica.
  Sin teclado numérico: menú **View → Viewpoint**.
- Arriba a la derecha de la vista 3D hay **4 esferitas** que cambian el modo de visualización:
  1. *Wireframe* (alambre) · 2. *Solid* (sólido, rápido) · 3. **Material Preview** (materiales; el que usa el script) · 4. *Rendered* (calidad final, más lento).
- Si el programa va lento, cambia a **Solid** (segunda esferita).

---

## 5. Ver el cableado (rayos X)

En los **diseños 2 y 3** los cables van por la **cara interna** de la estructura (discretos), por eso al inicio no se ven bien. Para verlos:

- Pulsa **`Alt + Z`** (Mac: `Option + Z`) con el cursor sobre la vista 3D → activa los **rayos X** y la estructura se vuelve transparente. Vuelve a pulsarlo para desactivar.
- Para ocultar piezas: en el panel **Outliner** (arriba a la derecha, lista de objetos) pulsa el **ojito 👁** junto al nombre.
  - Colección **`DISENO_2` (o `DISENO_3`) → `EYEBORG_20_CABLEADO`**: todos los cables, conectores y capacitores.
  - Objeto **`EYEBORG_FUSION`** (diseño 1), **`EYEBORG_FUSION.001`** (diseño 2) o **`EYEBORG_FUSION.002`** (diseño 3): la estructura. Ocúltalo para ver solo cables y componentes.
  - Objetos **`VISOR_INUIT`** (visor con ranuras), **`BRAZO_SIEN_*`** (brazos de sien) y **`PAD_*`** (almohadillas de anclaje: se pueden ocultar para ver mejor).
  - Objetos **`MANIQUI_CUERPO`** (colección `EYEBORG_14_MANIQUI`) y **`REF_CABEZA_BLOCKOUT`**: el maniquí anatómico esquemático de referencia (cabeza con rasgos, cuello y busto).

Qué es cada cable (colores de ayuda visual):

| Color | Qué representa | Estado |
| --- | --- | --- |
| Rojo y negro | Alimentación (+5 V y GND) de la bandeja trasera a la ESP32-CAM, por el riel izquierdo | Esquema conceptual |
| Cian (3 hilos finos) | Bus de audio I2S de la cámara al DAC, por el riel derecho | **Pines sin asignar** |
| Negro con conector dorado | Salida de audio hacia el amplificador externo | Conceptual |
| Rojo / blanco cortos | Puentes entre módulos en la bandeja posterior | Conceptual |
| Cilindros azules | Capacitores de desacople (3) | **Capacitancia por definir** |

> ⚠️ **Es una simulación visual.** No es un plano de cableado ni autoriza conectar o energizar nada.
> Ver la sección 08 del expediente técnico en el [README](../README.md).

---

## 6. Ver el diseño 2 o 3 con luces de estudio y hacer un render

El script del paso 3 muestra los modelos con la iluminación estándar de Blender. Los archivos de los **diseños 2 y 3** traen además **luces de estudio y cámaras** ya preparadas (el cromo y la resina se aprecian de verdad solo con esas luces):

1. Menú **File → Open…** y elige **`modelos/EYEBORG_CABLEADO.blend`** (cromo) o **`modelos/EYEBORG_CABLEADO_MATE.blend`** (resina)
   (si Blender pregunta por guardar cambios, elige *Don't Save* / *No guardar*).
2. Pulsa las esferitas de arriba a la derecha de la vista 3D y elige la **cuarta (Rendered)** para ver los reflejos del cromo.
3. Cámaras listas: en el **Outliner** (arriba a la derecha) haz clic en `CAM_hero`, `CAM_trasera`, `CAM_detalle_camara` o `CAM_lateral`; con el cursor sobre la vista 3D pulsa **View → Cameras → Set Active Object as Camera** y luego **View → Cameras → Active Camera** para mirar a través de ella.
4. Para generar una imagen final: menú **Render → Render Image** (`F12`). Tarda entre **1 y 5 minutos** según el equipo. Se guarda con **Image → Save As…** (si solo quieres imágenes, ya están hechas en `vistas/`).

---

## 7. Actualizar el proyecto

Si te avisan que hay cambios nuevos:

- **Si usaste git clone:** abre la terminal (ver paso 2B), entra a la carpeta y actualiza:

  ```bash
  cd ~/Documents/Navy_Project        # Windows PowerShell: cd "$HOME\Documents\Navy_Project"
  git pull
  ```

  Después vuelve a ejecutar `ver_disenos.py` en Blender (paso 3). El script limpia lo anterior y carga lo nuevo.
- **Si usaste el ZIP:** descarga de nuevo el ZIP y reemplaza la carpeta.

---

## 8. Problemas frecuentes

| Problema | Qué hacer |
| --- | --- |
| **No encuentro la pestaña Scripting** | Desliza las pestañas con la rueda del ratón sobre ellas o pulsa la flecha `>` del extremo derecho. |
| **"Falta el archivo … EYEBORG.blend"** | Descargaste el proyecto incompleto. Vuelve a hacer *Download ZIP* o `git clone` y comprueba que existe la carpeta `modelos` con dos archivos `.blend`. |
| **"No encuentro la ruta de ver_disenos.py"** | Abre el script con el botón **Open** del editor (no lo pegues). Así Blender conoce su carpeta. |
| **Ventana en blanco o va muy lento** | Cambia a modo **Solid** (segunda esferita). Cierra otros programas pesados. |
| **Todo se ve negro o gris** | Estás en Solid o Wireframe; pasa a **Material Preview** (tercera esferita). |
| **Los modelos salen muy pequeños o fuera de vista** | Con el cursor sobre la vista 3D pulsa `Inicio`/`Home` o menú **View → Frame All**. |
| **Mac: "no se puede abrir Blender porque no se puede verificar"** | Ajustes del Sistema → Privacidad y seguridad → **Abrir de todos modos**. |
| **Windows: "Windows protegió su PC"** | **Más información → Ejecutar de todas formas.** |
| **`git` no se reconoce como comando (Windows)** | Cierra y vuelve a abrir la terminal tras instalar Git; si sigue igual, reinicia el PC. |
| **`git clone` pide usuario/contraseña** | El repositorio podría ser privado: pide que te den acceso en GitHub. |
| **Aparece una versión de Blender muy vieja al abrir los `.blend`** | Instala Blender **5.1 o superior** (paso 1). |
| **Quiero ver un error exacto** | Windows: *Window → Toggle System Console*. Mac: abre Blender desde Terminal con `/Applications/Blender.app/Contents/MacOS/Blender`. |

---

## 9. Avanzado: reconstruir desde el código

Los diseños se generan con scripts de Python (carpeta `scripts/`). Normalmente **no necesitas** esto: los `.blend` ya están listos.
Si quieres regenerarlos desde cero (requiere ~30 segundos y Blender 5.1+):

- **Mac** (Terminal, desde la carpeta del proyecto):

  ```bash
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P scripts/00_construir_conjunto.py --python-expr "import bpy; bpy.ops.wm.save_as_mainfile(filepath='salida_diseno1.blend')"
  ```

- **Windows** (PowerShell, desde la carpeta del proyecto):

  ```powershell
  & "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b --factory-startup -P scripts/00_construir_conjunto.py --python-expr "import bpy; bpy.ops.wm.save_as_mainfile(filepath='salida_diseno1.blend')"
  ```

  > Ajusta `5.1` a tu versión instalada. `00_construir_cableado.py` genera el diseño 2 (cromo) o el 3 (añade `mate` tras la ruta) y, por defecto, **sobrescribe** el `.blend` correspondiente de `modelos/`; pasa otra ruta tras `--` (por ejemplo `-- mi_diseno2.blend`, o `-- mi_diseno3.blend mate`) para no pisarlo.

Parámetros del diseño (medidas, holguras, espinas, fusión): `scripts/eyeborg_config.json`.
Comprobación ergonómica: `tools/check_ergonomia.py`. Comparación contra las referencias: `tools/compare_views.py`.
