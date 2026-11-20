"""Ejecutar dentro de Blender GUI: recarga output/EYEBORG.blend cuando cambia en disco."""
import bpy, os
P = os.path.expanduser('~/Documentos/Navy_Project/output/EYEBORG.blend')
_state = {'m': os.path.getmtime(P) if os.path.exists(P) else 0}
def _tick():
    try:
        m = os.path.getmtime(P)
        if m != _state['m']:
            _state['m'] = m
            bpy.ops.wm.open_mainfile(filepath=P)
    except Exception as e:
        print('live_reload:', e)
    return 1.5
bpy.app.timers.register(_tick, persistent=True)
print('live_reload activo sobre', P)
