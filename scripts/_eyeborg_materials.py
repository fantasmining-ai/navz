# -*- coding: utf-8 -*-
"""Materiales procedurales EYEBORG (cromo azul, fibra de carbono, mangas de cable, emisivos). Blender 4.x/5.x."""
import bpy


def _principled(m):
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL':
            nt.nodes.remove(n)
    out = nt.nodes.get('Material Output') or nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return nt, b


def _set(b, **kw):
    for k, v in kw.items():
        key = k.replace('_', ' ')
        if key in b.inputs:
            b.inputs[key].default_value = v


def chrome_blue(name='EYEBORG_CROMO_AZUL'):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=(0.42, 0.80, 0.97, 1), Metallic=1.0, Roughness=0.14, Coat_Weight=0.5, Coat_Roughness=0.04)
    # microvariacion de rugosidad (huella de acabado) para que el cromo no se vea plano
    tc = nt.nodes.new('ShaderNodeTexCoord'); no = nt.nodes.new('ShaderNodeTexNoise')
    no.inputs['Scale'].default_value = 0.35; no.inputs['Detail'].default_value = 6
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.10; mr.inputs['To Max'].default_value = 0.22
    nt.links.new(tc.outputs['Object'], no.inputs['Vector'])
    nt.links.new(no.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])
    return m


def carbon(name='EYEBORG_CARBONO'):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=(0.012, 0.014, 0.018, 1), Metallic=0.25, Roughness=0.26, Coat_Weight=0.8, Coat_Roughness=0.03)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    ck = nt.nodes.new('ShaderNodeTexChecker'); ck.inputs['Scale'].default_value = 0.2
    wa = nt.nodes.new('ShaderNodeTexWave'); wa.wave_type = 'BANDS'; wa.bands_direction = 'X'
    wb = nt.nodes.new('ShaderNodeTexWave'); wb.wave_type = 'BANDS'; wb.bands_direction = 'Y'
    for w in (wa, wb):
        w.inputs['Scale'].default_value = 1.5; w.inputs['Distortion'].default_value = 0.0
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'FLOAT'
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35; bump.inputs['Distance'].default_value = 0.15
    for n_ in (ck, wa, wb):
        nt.links.new(tc.outputs['Object'], n_.inputs['Vector'])
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


def metal(name, color, rough=0.3):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=color, Metallic=1.0, Roughness=rough)
    return m


def plastic(name, color, rough=0.45):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nt, b = _principled(m)
    _set(b, Base_Color=color, Roughness=rough)
    return m


def build_all():
    return {
        'chrome': chrome_blue(), 'carbon': carbon(),
        'cable_black': sleeve('CABLE_NEGRO_MANGA', (0.012, 0.012, 0.016, 1)),
        'cable_red': sleeve('CABLE_ROJO_5V', (0.55, 0.02, 0.02, 1), 0.45),
        'cable_cyan': sleeve('CABLE_CIAN_I2S', (0.0, 0.45, 0.62, 1), 0.45),
        'cable_white': sleeve('CABLE_BLANCO_SENAL', (0.7, 0.7, 0.72, 1), 0.45),
        'led_cyan': emissive('LED_CIAN', (0.0, 0.85, 1.0, 1), 5.0),
        'led_magenta': emissive('LED_MAGENTA', (1.0, 0.05, 0.6, 1), 4.0),
        'gold': metal('ORO_CONECTOR', (1.0, 0.72, 0.28, 1), 0.22),
        'alu': metal('ALUMINIO_ANODIZADO', (0.78, 0.8, 0.84, 1), 0.32),
        'graphite': plastic('GRAFITO_MATE', (0.035, 0.038, 0.045, 1), 0.38),
        'pcb': plastic('PCB_VERDE_OSCURO', (0.01, 0.16, 0.09, 1), 0.5),
        'lipo': plastic('LIPO_FUNDA', (0.10, 0.16, 0.42, 1), 0.3),
        'cap_blue': plastic('CAP_MANGA_AZUL', (0.02, 0.07, 0.34, 1), 0.35),
        'jst': plastic('CONECTOR_BLANCO', (0.82, 0.82, 0.78, 1), 0.5),
        'head': plastic('MANIQUI_MATE', (0.11, 0.115, 0.13, 1), 0.5),
    }
