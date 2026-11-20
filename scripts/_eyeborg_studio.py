# -*- coding: utf-8 -*-
"""Estudio EYEBORG: asigna materiales, mundo, luces (roles separados) y camaras de producto. Blender 4.x/5.x."""
import bpy, math
from mathutils import Vector


def assign_materials(M):
    f = bpy.data.objects.get('EYEBORG_FUSION')
    if f:
        me = f.data
        me.materials.clear(); me.materials.append(M['chrome']); me.materials.append(M['carbon'])
        for p in me.polygons:
            c = p.center
            p.material_index = 1 if (c.y > 127.5 and abs(c.x) < 48.5 and -38 < c.z < 30) else 0
    def setm(name, key, hide=False):
        o = bpy.data.objects.get(name)
        if o is None: return
        o.data.materials.clear(); o.data.materials.append(M[key]); o.hide_render = hide; o.display_type = 'TEXTURED'
        for q in o.data.polygons: q.use_smooth = True
    for nm in ('REF_NODEMCU', 'REF_TP4056', 'REF_MT3608', 'REF_DAC_PCM5102A'): setm(nm, 'pcb')
    setm('REF_LIPO', 'lipo'); setm('REF_CABEZA_BLOCKOUT', 'head')
    setm('CARCASA_CAMARA_PROVISIONAL', 'graphite'); setm('ARO_LENTE_CAMARA', 'led_cyan'); setm('LENTE_REFERENCIA_D6', 'graphite')
    setm('BANDEJA_ELECTRONICA_104x58x2', 'carbon')
    for o in bpy.data.objects:
        if o.name.startswith(('OREJA_CAMARA_', 'ARO_FIJACION_CAMARA_', 'POSTE_BANDEJA_')): setm(o.name, 'alu')


def studio(M, floor_z=-150):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 48; sc.cycles.use_denoising = True
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast' if hasattr(sc.view_settings, 'look') else 'None'
    sc.render.resolution_x, sc.render.resolution_y = 1100, 850
    # mundo: degradado oscuro cian-azulado (reflejos del cromo)
    w = bpy.data.worlds.new('EYEBORG_ESTUDIO'); sc.world = w; w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    tc = nt.nodes.new('ShaderNodeTexCoord'); gr = nt.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange'); cr = nt.nodes.new('ShaderNodeValToRGB')
    bg = nt.nodes.new('ShaderNodeBackground'); out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    mr.inputs['From Min'].default_value = -1.0; mr.inputs['From Max'].default_value = 1.0
    nt.links.new(sep.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], cr.inputs['Fac'])
    cr.color_ramp.elements[0].color = (0.002, 0.004, 0.008, 1); cr.color_ramp.elements[1].color = (0.10, 0.18, 0.26, 1)
    for pos, colr in ((0.30, (0.01, 0.02, 0.03, 1)), (0.47, (0.0, 0.0, 0.0, 1)), (0.52, (1.0, 1.0, 1.0, 1)), (0.57, (0.0, 0.0, 0.0, 1)), (0.80, (0.0, 0.45, 0.6, 1))):
        e = cr.color_ramp.elements.new(pos); e.color = colr
    nt.links.new(cr.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 2.5
    # fondo visible oscuro (rayos de camara) manteniendo el degradado para reflejos del cromo
    lp = nt.nodes.new('ShaderNodeLightPath'); dark = nt.nodes.new('ShaderNodeBackground')
    dark.inputs['Color'].default_value = (0.004, 0.007, 0.014, 1); dark.inputs['Strength'].default_value = 1.0
    mixs = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lp.outputs['Is Camera Ray'], mixs.inputs['Fac'])
    nt.links.new(bg.outputs['Background'], mixs.inputs[1]); nt.links.new(dark.outputs['Background'], mixs.inputs[2])
    nt.links.new(mixs.outputs['Shader'], out.inputs['Surface'])
    # suelo oscuro y pulido
    bpy.ops.mesh.primitive_plane_add(size=4000, location=(0, 0, floor_z)); fl = bpy.context.object; fl.name = 'SUELO_ESTUDIO'
    fm = bpy.data.materials.new('SUELO_NEGRO_PULIDO'); fm.use_nodes = True
    b = fm.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.004, 0.005, 0.007, 1); b.inputs['Roughness'].default_value = 0.55
    for k_ in ('Specular IOR Level', 'Specular'):
        if k_ in b.inputs: b.inputs[k_].default_value = 0.12
    fl.data.materials.append(fm)
    # luces por rol
    col = bpy.data.collections.new('LIGHTING_Estudio'); sc.collection.children.link(col)
    def area(name, loc, target, power, size, color, shape='RECTANGLE', sy=None):
        d = bpy.data.lights.new(name, 'AREA'); d.energy = power; d.size = size; d.color = color
        d.shape = shape
        if shape == 'RECTANGLE': d.size_y = sy or size
        o = bpy.data.objects.new(name, d); col.objects.link(o); o.location = loc
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        o['proposito'] = name
        return o
    area('LGT_key', (520, -420, 380), (0, 0, 10), 5000, 420, (1.0, 0.97, 0.92), sy=70)
    area('LGT_fill', (-520, -380, 120), (0, 0, 10), 900, 500, (0.7, 0.85, 1.0), sy=300)
    area('LGT_rim_cian', (-300, 520, 260), (0, 0, 10), 6000, 300, (0.0, 0.85, 1.0), sy=40)
    area('LGT_rim_magenta', (380, 480, 180), (0, 0, 10), 4500, 300, (1.0, 0.1, 0.65), sy=40)
    # camaras de producto
    def cam(name, loc, target, lens):
        cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_end = 8000
        o = bpy.data.objects.new(name, cd); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
    cams = {
      'CAM_hero': cam('CAM_hero', (430, -560, 230), (0, -5, 5), 70),
      'CAM_trasera': cam('CAM_trasera', (-420, 600, 210), (0, 20, 0), 70),
      'CAM_detalle_camara': cam('CAM_detalle_camara', (150, -400, 150), (0, -112, 44), 100),
      'CAM_lateral': cam('CAM_lateral', (700, -20, 15), (0, -5, 5), 85),
    }
    sc.camera = cams['CAM_hero']
    return cams
