# -*- coding: utf-8 -*-
"""Materiales procedurales EYEBORG (cromo azul, fibra de carbono, mangas de cable, emisivos). Blender 4.x/5.x."""
import bpy


def _principled(m):
    """Reinicia el arbol de nodos del material y crea una salida + Principled BSDF limpios.
    (Se borran TODOS los nodos: en archivos guardados con otro idioma la salida no se llama 'Material Output'
    y dejaba dos salidas, una sin conectar -> superficie negra.)"""
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return nt, b


def _set(b, **kw):
    for k, v in kw.items():
        key = k.replace('_', ' ')
        if key in b.inputs:
            b.inputs[key].default_value = v


def chrome_blue(name='EYEBORG_PLATA_SATINADA'):
    """Plata satinada (ref. mascara de plata): metal casi neutro, rugosidad media con micro-variacion, anisotropia suave
    y recesos oscuros por oclusion ambiental que dan definicion a las nervaduras."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Metallic=1.0, Anisotropic=0.35, Coat_Weight=0.0)
    tc = nt.nodes.new('ShaderNodeTexCoord'); no = nt.nodes.new('ShaderNodeTexNoise')
    no.inputs['Scale'].default_value = 0.3; no.inputs['Detail'].default_value = 5
    ao = nt.nodes.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = 7.0
    nt.links.new(tc.outputs['Object'], no.inputs['Vector'])
    # color: recesos gris pizarra -> plata neutra en zonas abiertas
    mixc = nt.nodes.new('ShaderNodeMix'); mixc.data_type = 'RGBA'
    rgba = [i for i in mixc.inputs if i.type == 'RGBA']
    rgba[0].default_value = (0.045, 0.050, 0.058, 1); rgba[1].default_value = (0.86, 0.87, 0.90, 1)
    nt.links.new(ao.outputs['AO'], mixc.inputs['Factor'])
    nt.links.new([o for o in mixc.outputs if o.type == 'RGBA'][0], b.inputs['Base Color'])
    # rugosidad: satinada 0.18-0.30 en zonas abiertas, mas alta en recesos
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.18; mr.inputs['To Max'].default_value = 0.30
    nt.links.new(no.outputs['Fac'], mr.inputs['Value'])
    mixr = nt.nodes.new('ShaderNodeMix'); mixr.data_type = 'FLOAT'
    mixr.inputs[2].default_value = 0.55
    nt.links.new(mr.outputs['Result'], mixr.inputs[3]); nt.links.new(ao.outputs['AO'], mixr.inputs['Factor'])
    nt.links.new([o for o in mixr.outputs if o.type == 'VALUE'][0], b.inputs['Roughness'])
    return m


def resin(name='EYEBORG_RESINA_AZUL'):
    """Resina SLA translucida esmerilada (ref. gafas de resina azul): transmision parcial, grano fino, bordes pulidos."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Metallic=0.0, Specular_IOR_Level=0.5, IOR=1.45, Transmission_Weight=0.62, Subsurface_Weight=0.15, Coat_Weight=0.15, Coat_Roughness=0.25)
    tc = nt.nodes.new('ShaderNodeTexCoord'); geo = nt.nodes.new('ShaderNodeNewGeometry')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.50; ramp.color_ramp.elements[1].position = 0.62
    nt.links.new(geo.outputs['Pointiness'], ramp.inputs['Fac'])
    mixc = nt.nodes.new('ShaderNodeMix'); mixc.data_type = 'RGBA'
    rgba = [i for i in mixc.inputs if i.type == 'RGBA']
    rgba[0].default_value = (0.30, 0.45, 0.86, 1); rgba[1].default_value = (0.55, 0.68, 0.96, 1)   # azul-lavanda esmerilado, bordes mas claros
    nt.links.new(ramp.outputs['Color'], mixc.inputs['Factor'])
    nt.links.new([o for o in mixc.outputs if o.type == 'RGBA'][0], b.inputs['Base Color'])
    mixr = nt.nodes.new('ShaderNodeMix'); mixr.data_type = 'FLOAT'
    mixr.inputs[2].default_value = 0.34; mixr.inputs[3].default_value = 0.22
    nt.links.new(ramp.outputs['Color'], mixr.inputs['Factor'])
    nt.links.new([o for o in mixr.outputs if o.type == 'VALUE'][0], b.inputs['Roughness'])
    bev = nt.nodes.new('ShaderNodeBevel'); bev.inputs['Radius'].default_value = 0.8; bev.samples = 6
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 3.2; n1.inputs['Detail'].default_value = 9
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector'])
    bump1 = nt.nodes.new('ShaderNodeBump'); bump1.inputs['Strength'].default_value = 0.14; bump1.inputs['Distance'].default_value = 0.05
    nt.links.new(n1.outputs['Fac'], bump1.inputs['Height']); nt.links.new(bev.outputs['Normal'], bump1.inputs['Normal'])
    nt.links.new(bump1.outputs['Normal'], b.inputs['Normal'])
    return m


def carbon(name='EYEBORG_CARBONO'):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=(0.012, 0.014, 0.018, 1), Metallic=0.25, Roughness=0.26, Coat_Weight=0.8, Coat_Roughness=0.03)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Rotation'].default_value = (0.0, 0.0, 0.785398)          # sarga a 45 grados
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    ck = nt.nodes.new('ShaderNodeTexChecker'); ck.inputs['Scale'].default_value = 0.2
    wa = nt.nodes.new('ShaderNodeTexWave'); wa.wave_type = 'BANDS'; wa.bands_direction = 'X'
    wb = nt.nodes.new('ShaderNodeTexWave'); wb.wave_type = 'BANDS'; wb.bands_direction = 'Y'
    for w in (wa, wb):
        w.inputs['Scale'].default_value = 1.5; w.inputs['Distortion'].default_value = 0.0
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'FLOAT'
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35; bump.inputs['Distance'].default_value = 0.15
    for n_ in (ck, wa, wb):
        nt.links.new(mp.outputs['Vector'], n_.inputs['Vector'])
    nt.links.new(ck.outputs['Fac'], mix.inputs['Factor'])
    nt.links.new(wa.outputs['Fac'], mix.inputs[2]); nt.links.new(wb.outputs['Fac'], mix.inputs[3])
    nt.links.new(mix.outputs['Result'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def sleeve(name, color, rough=0.5):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=color, Roughness=rough, Sheen_Weight=0.3)
    tc = nt.nodes.new('ShaderNodeTexCoord'); no = nt.nodes.new('ShaderNodeTexNoise'); no.inputs['Scale'].default_value = 4.0
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.2
    nt.links.new(tc.outputs['Object'], no.inputs['Vector']); nt.links.new(no.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def emissive(name, color, strength=4.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=(0.02, 0.02, 0.02, 1), Roughness=0.3, Emission_Color=color, Emission_Strength=strength)
    return m


def metal(name, color, rough=0.3, brushed=False):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=color, Metallic=1.0, Roughness=rough)
    if brushed:   # cepillado: ruido estirado en un eje
        tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (1.0, 60.0, 1.0)
        no = nt.nodes.new('ShaderNodeTexNoise'); no.inputs['Scale'].default_value = 6.0; no.inputs['Detail'].default_value = 4
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.12; bump.inputs['Distance'].default_value = 0.05
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], no.inputs['Vector'])
        nt.links.new(no.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def plastic(name, color, rough=0.45, grain=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=color, Roughness=rough)
    if grain:     # grano fino (plastico texturizado / piel de naranja)
        tc = nt.nodes.new('ShaderNodeTexCoord'); no = nt.nodes.new('ShaderNodeTexNoise')
        no.inputs['Scale'].default_value = 5.0; no.inputs['Detail'].default_value = 8
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = grain; bump.inputs['Distance'].default_value = 0.05
        nt.links.new(tc.outputs['Object'], no.inputs['Vector']); nt.links.new(no.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def build_all(acabado='cromo'):
    """acabado: 'cromo' (diseño 2) o 'mate' (diseño 3: resina satinada sin cromo)."""
    body = chrome_blue() if acabado == 'cromo' else resin()
    return {
        'body': body, 'chrome': body, 'carbon': carbon(),
        'cable_black': sleeve('CABLE_NEGRO_MANGA', (0.012, 0.012, 0.016, 1)),
        'cable_red': sleeve('CABLE_ROJO_5V', (0.55, 0.02, 0.02, 1), 0.45),
        'cable_cyan': sleeve('CABLE_CIAN_I2S', (0.0, 0.45, 0.62, 1), 0.45),
        'cable_white': sleeve('CABLE_BLANCO_SENAL', (0.7, 0.7, 0.72, 1), 0.45),
        'led_cyan': emissive('LED_CIAN', (0.0, 0.85, 1.0, 1), 5.0),
        'led_magenta': emissive('LED_MAGENTA', (1.0, 0.05, 0.6, 1), 4.0),
        'gold': metal('ORO_CONECTOR', (1.0, 0.72, 0.28, 1), 0.22),
        'alu': metal('ALUMINIO_ANODIZADO', (0.78, 0.8, 0.84, 1), 0.34, brushed=True),
        'graphite': plastic('GRAFITO_MATE', (0.035, 0.038, 0.045, 1), 0.42, grain=0.08),
        'pcb': plastic('PCB_VERDE_OSCURO', (0.01, 0.16, 0.09, 1), 0.5),
        'lipo': plastic('LIPO_FUNDA', (0.10, 0.16, 0.42, 1), 0.3),
        'cap_blue': plastic('CAP_MANGA_AZUL', (0.02, 0.07, 0.34, 1), 0.35),
        'pad': plastic('EVA_PAD_NEGRO', (0.02, 0.02, 0.024, 1), 0.85, grain=0.12),
        'jst': plastic('CONECTOR_BLANCO', (0.82, 0.82, 0.78, 1), 0.5),
        'sclera': plastic('OJO_ESCLERA_SATINADA', (0.82, 0.80, 0.76, 1), 0.22),
        'iris': plastic('OJO_IRIS_PINTADO', (0.11, 0.07, 0.035, 1), 0.18),
        'head': plastic('MANIQUI_ARCILLA', (0.30, 0.31, 0.33, 1) if acabado == 'cromo' else (0.82, 0.82, 0.84, 1), 0.55, grain=0.02),
    }
