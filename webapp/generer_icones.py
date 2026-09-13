#!/usr/bin/env python3
"""Genere les icones Android depuis assets/appicon.png (1024x1024)."""
import os
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'assets', 'appicon.png')
RES = os.path.join(REPO, 'webapp', 'android', 'app', 'src', 'main', 'res')

TAILLES = {
    'mipmap-mdpi':    48,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}

TAILLES_FG = {
    'mipmap-mdpi':    108,
    'mipmap-hdpi':    162,
    'mipmap-xhdpi':   216,
    'mipmap-xxhdpi':  324,
    'mipmap-xxxhdpi':  432,
}

img = Image.open(SRC).convert('RGBA')

for dossier, taille in TAILLES.items():
    d = os.path.join(RES, dossier)
    os.makedirs(d, exist_ok=True)
    for nom in ('ic_launcher.png', 'ic_launcher_round.png'):
        icone = img.resize((taille, taille), Image.LANCZOS)
        icone.save(os.path.join(d, nom))

for dossier, taille in TAILLES_FG.items():
    d = os.path.join(RES, dossier)
    os.makedirs(d, exist_ok=True)
    icone = img.resize((taille, taille), Image.LANCZOS)
    icone.save(os.path.join(d, 'ic_launcher_foreground.png'))

print('Icones generees depuis', SRC)
