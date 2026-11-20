#!/bin/sh
# Abre Blender con el modelo y recarga automatica al guardar desde el MCP.
exec "$HOME/Apps/blender/blender" "$HOME/Documentos/Navy_Project/output/EYEBORG.blend" --python "$HOME/Documentos/Navy_Project/tools/live_reload.py"
