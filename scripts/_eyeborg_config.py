# -*- coding: utf-8 -*-
"""Adaptador Python del JSON dimensional compartido."""
import json, os
_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eyeborg_config.json')
with open(_PATH, encoding='utf-8') as _f:
    CONFIG = json.load(_f)
ANTHROPOMETRY = CONFIG['anthropometry']
FIT = CONFIG['fit']
FRONT_FEATURES = CONFIG['front_features']
COMPONENTS = CONFIG['components']
CAMERA = CONFIG['camera']
COORDINATES = CONFIG['coordinate_system']
