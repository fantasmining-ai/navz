# -*- coding: utf-8 -*-
"""Estudio EYEBORG: asigna materiales, mundo, luces (roles separados) y camaras de producto. Blender 4.x/5.x."""
import bpy, math
from mathutils import Vector


def assign_materials(M):
    f = bpy.data.objects.get('EYEBORG_FUSION')
    if f:
        me = f.data
        me.materials.clear(); me.materials.append(M['body']); me.materials.append(M['carbon'])
        for p in me.polygons:
            c = p.center
            p.material_index = 1 if (c.y > 127.5 and abs(c.x) < 48.5 and -38 < c.z < 30) else 0
    def setm(name, key, hide=False):
        o = bpy.data.objects.get(name)
        if o is None: return
        o.data.materials.clear(); o.data.materials.append(M[key]); o.hide_render = hide; o.display_type = 'TEXTURED'
        for q in o.data.polygons: q.use_smooth = True
    for nm in ('REF_NODEMCU', 'REF_TP4056', 'REF_MT3608', 'REF_DAC_PCM5102A'): setm(nm, 'pcb')
    setm('REF_LIPO', 'lipo')
    for o in bpy.data.objects:
        if o.name.startswith('MANIQUI_OJO_ESCLERA'): setm(o.name, 'sclera')
        elif o.name.startswith('MANIQUI_OJO_IRIS'): setm(o.name, 'iris')
        elif o.name.startswith('MANIQUI_'): setm(o.name, 'head')
        if o.name.startswith('PAD_'): setm(o.name, 'pad')   # arcilla neutra solo en diseños 2 y 3 (el diseño 1 no cambia)
    setm('CARCASA_CAMARA_PROVISIONAL', 'graphite'); setm('ARO_LENTE_CAMARA', 'led_cyan'); setm('LENTE_REFERENCIA_D6', 'graphite')
    setm('BANDEJA_ELECTRONICA_104x58x2', 'carbon')
    for o in bpy.data.objects:
        if o.name.startswith(('OREJA_CAMARA_', 'ARO_FIJACION_CAMARA_', 'POSTE_BANDEJA_')): setm(o.name, 'alu')


def studio(M, estilo='cromo', floor_z=-262):
    """Estudio de producto. estilo 'cromo': oscuro, softboxes y tiras para reflejos largos + luz de borde cian/magenta.
    estilo 'mate': estudio claro y neutro con sombras suaves (acabado resina)."""
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 64; sc.cycles.use_denoising = True
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1050
    w = bpy.data.worlds.new('EYEBORG_ESTUDIO'); sc.world = w; w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange')
    cr = nt.nodes.new('ShaderNodeValToRGB'); bg = nt.nodes.new('ShaderNodeBackground'); out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    mr.inputs['From Min'].default_value = -1.0; mr.inputs['From Max'].default_value = 1.0
    nt.links.new(sep.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], cr.inputs['Fac'])
    if estilo == 'cromo':
        cr.color_ramp.elements[0].color = (0.006, 0.006, 0.008, 1); cr.color_ramp.elements[1].color = (0.30, 0.31, 0.34, 1)
        for pos, colr in ((0.28, (0.02, 0.04, 0.07, 1)), (0.46, (0.0, 0.0, 0.0, 1)), (0.51, (1.0, 1.0, 1.0, 1)),
                          (0.56, (0.0, 0.0, 0.0, 1)), (0.78, (0.10, 0.11, 0.13, 1))):
            e = cr.color_ramp.elements.new(pos); e.color = colr   # banda de horizonte: reflejos largos en el cromo
        bg.inputs['Strength'].default_value = 3.2
    else:
        cr.color_ramp.elements[0].color = (0.22, 0.23, 0.25, 1); cr.color_ramp.elements[1].color = (0.62, 0.64, 0.68, 1)
        bg.inputs['Strength'].default_value = 0.75
    nt.links.new(cr.outputs['Color'], bg.inputs['Color'])
    if estilo == 'cromo':   # fondo visible gris oscuro con degradado suave; el entorno brillante queda para los reflejos
        lp = nt.nodes.new('ShaderNodeLightPath'); dark = nt.nodes.new('ShaderNodeBackground')
        cr2 = nt.nodes.new('ShaderNodeValToRGB')
        cr2.color_ramp.elements[0].color = (0.010, 0.011, 0.014, 1); cr2.color_ramp.elements[1].color = (0.090, 0.095, 0.105, 1)
        nt.links.new(mr.outputs['Result'], cr2.inputs['Fac']); nt.links.new(cr2.outputs['Color'], dark.inputs['Color'])
        mixs = nt.nodes.new('ShaderNodeMixShader')
        nt.links.new(lp.outputs['Is Camera Ray'], mixs.inputs['Fac'])
        nt.links.new(bg.outputs['Background'], mixs.inputs[1]); nt.links.new(dark.outputs['Background'], mixs.inputs[2])
        nt.links.new(mixs.outputs['Shader'], out.inputs['Surface'])
    else:
        nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    # suelo
    bpy.ops.mesh.primitive_plane_add(size=6000, location=(0, 0, floor_z)); fl = bpy.context.object; fl.name = 'SUELO_ESTUDIO'
    fm = bpy.data.materials.new('SUELO_ESTUDIO'); fm.use_nodes = True
    b = fm.node_tree.nodes['Principled BSDF']
    if estilo == 'cromo':
        b.inputs['Base Color'].default_value = (0.018, 0.019, 0.022, 1); b.inputs['Roughness'].default_value = 0.75
    else:
        b.inputs['Base Color'].default_value = (0.62, 0.63, 0.65, 1); b.inputs['Roughness'].default_value = 0.65
    for k_ in ('Specular IOR Level', 'Specular'):
        if k_ in b.inputs: b.inputs[k_].default_value = 0.03 if estilo == 'cromo' else 0.15
    fl.data.materials.append(fm)
    # luces por rol (colecciones separadas)
    col = bpy.data.collections.new('LIGHTING_Estudio'); sc.collection.children.link(col)
    def area(name, loc, power, sx, sy, color=(1, 1, 1)):
        d = bpy.data.lights.new(name, 'AREA'); d.energy = power; d.shape = 'RECTANGLE'; d.size = sx; d.size_y = sy; d.color = color
        o = bpy.data.objects.new(name, d); col.objects.link(o); o.location = loc
        o.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); o['proposito'] = name
    if estilo == 'cromo':
        area('LGT_softbox_superior', (0, -150, 720), 9000, 900, 600)                 # reflejo amplio arriba
        area('LGT_tira_izquierda', (720, -260, 60), 8000, 70, 760, (1.0, 0.98, 0.95)) # reflejos largos a lo largo de las correas
        area('LGT_tira_derecha', (-720, -260, 60), 6000, 70, 760, (0.75, 0.9, 1.0))
        area('LGT_relleno_frontal', (0, -820, 40), 1800, 800, 360, (0.9, 0.95, 1.0))
        area('LGT_borde_cian', (360, 560, 240), 2200, 60, 340, (0.0, 0.85, 1.0))
        area('LGT_borde_magenta', (-380, 560, 200), 1800, 60, 340, (1.0, 0.1, 0.65))
    else:
        area('LGT_softbox_llave', (420, -560, 560), 3600, 800, 620, (1.0, 0.97, 0.93))
        area('LGT_relleno', (-720, -380, 200), 1500, 700, 520, (0.88, 0.93, 1.0))
        area('LGT_contraluz', (150, 620, 380), 2000, 120, 600, (1.0, 1.0, 1.0))
        area('LGT_superior', (0, 0, 760), 1100, 700, 700)
    def cam(name, loc, target, lens):
        cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_end = 8000
        o = bpy.data.objects.new(name, cd); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
    cams = {
      'CAM_hero': cam('CAM_hero', (520, -700, 280), (0, -5, -20), 62),
      'CAM_trasera': cam('CAM_trasera', (-480, 720, 240), (0, 20, -20), 62),
      'CAM_detalle_camara': cam('CAM_detalle_camara', (190, -420, 170), (0, -112, 46), 100),
      'CAM_lateral': cam('CAM_lateral', (760, -20, 15), (0, -5, 5), 85),
    }
    sc.camera = cams['CAM_hero']
    return cams


def acabado_diseno1():
    """Diseño 1: acabado azul satinado, luz de estudio sencilla y camara; elimina los objetos por defecto."""
    for nm in ('Cube', 'Light', 'Camera'):
        o = bpy.data.objects.get(nm)
        if o: bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    m = bpy.data.materials.get('EYEBORG_AZUL_SATINADO') or bpy.data.materials.new('EYEBORG_AZUL_SATINADO')
    m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.02, 0.38, 0.60, 1); b.inputs['Metallic'].default_value = 0.55
    b.inputs['Roughness'].default_value = 0.30
    if 'Coat Weight' in b.inputs: b.inputs['Coat Weight'].default_value = 0.3
    f = bpy.data.objects.get('EYEBORG_FUSION')
    if f:
        f.data.materials.clear(); f.data.materials.append(m)
        for p in f.data.polygons: p.material_index = 0
    # mundo gris claro de estudio
    w = bpy.data.worlds.new('EYEBORG_D1'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.55, 0.58, 0.62, 1); bg.inputs['Strength'].default_value = 0.9
    col = bpy.data.collections.new('LIGHTING_Diseno1'); sc.collection.children.link(col)
    def luz(name, loc, power, size):
        d = bpy.data.lights.new(name, 'AREA'); d.energy = power; d.size = size
        o = bpy.data.objects.new(name, d); col.objects.link(o); o.location = loc
        o.rotation_euler = (Vector((0, 0, 10)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    luz('LGT_key', (520, -420, 380), 4000, 420); luz('LGT_fill', (-520, -380, 120), 900, 500)
    cd = bpy.data.cameras.new('CAM_diseno1'); cd.lens = 70; cd.clip_end = 8000
    cam = bpy.data.objects.new('CAM_diseno1', cd); sc.collection.objects.link(cam)
    cam.location = (430, -560, 230)
    cam.rotation_euler = (Vector((0, -5, 5)) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam
    sc.render.engine = 'BLENDER_EEVEE' if 'BLENDER_EEVEE' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE_NEXT'
    sc.render.resolution_x, sc.render.resolution_y = 1100, 850
    for m_ in [m for m in bpy.data.materials if m.users == 0]:   # material por defecto huerfano
        bpy.data.materials.remove(m_)
