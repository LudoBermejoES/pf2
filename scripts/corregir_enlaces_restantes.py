#!/usr/bin/env python3
"""Corregir enlaces restantes que no usan comillas o que están en parent_url"""

import re
from pathlib import Path

def corregir_enlaces(filepath):
    """Corrige enlaces en formato sin comillas y parent_url"""
    with open(filepath, 'r', encoding='utf-8') as f:
        contenido = f.read()

    contenido_original = contenido

    # Corregir enlaces sin comillas (en tablas markdown)
    cambios = {
        r'\(/introduccion/dioses/': r'(/ambientacion/religion/dioses/',
        r'\(/introduccion/facciones/': r'(/ambientacion/organizaciones/',
        r'\(/introduccion/regiones/': r'(/ambientacion/regiones/',
        r'\(/introduccion/escenario/': r'(/ambientacion/golarion/',
        r'\(/introduccion/religion/': r'(/ambientacion/religion/',
        r'\(/introduccion/sociedad/': r'(/ambientacion/sociedad/',
        r'\(/introduccion/calendario/': r'(/ambientacion/sociedad/calendario/',
        r'\(/introduccion/clima/': r'(/ambientacion/sociedad/clima/',
        r'\(/introduccion/comercio/': r'(/ambientacion/sociedad/comercio/',
        r'\(/introduccion/fauna-flora/': r'(/ambientacion/sociedad/fauna-flora/',
        r'\(/introduccion/tecnologia/': r'(/ambientacion/sociedad/tecnologia/',
        r'\(/introduccion/golarion-presagios/': r'(/ambientacion/era-presagios/',
    }

    for old, new in cambios.items():
        contenido = re.sub(old, new, contenido)

    # Corregir parent_url
    contenido = re.sub(
        r'parent_url: /introduccion/facciones/',
        'parent_url: /ambientacion/organizaciones/',
        contenido
    )
    contenido = re.sub(
        r'parent_url: /introduccion/dioses/',
        'parent_url: /ambientacion/religion/dioses/',
        contenido
    )

    if contenido != contenido_original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return True
    return False

# Procesar archivos
docs_path = Path('docs')
archivos_actualizados = 0

print("Corrigiendo enlaces restantes...")
print("=" * 60)

for filepath in docs_path.rglob('*.md'):
    if corregir_enlaces(filepath):
        archivos_actualizados += 1
        print(f"✓ {filepath.relative_to('docs')}")

print("=" * 60)
print(f"✓ {archivos_actualizados} archivos actualizados")
