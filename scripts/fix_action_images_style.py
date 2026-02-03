#!/usr/bin/env python3
"""
Script para cambiar el formato de las imágenes de acciones
de markdown a HTML con float:right para que aparezcan a la derecha.
"""

import os
import re
from pathlib import Path

# Directorios a procesar
DIRS_TO_PROCESS = [
    Path("/Users/ludo/code/pf2/docs/_habilidades"),
    Path("/Users/ludo/code/pf2/docs/_reglas/acciones-basicas"),
    Path("/Users/ludo/code/pf2/docs/_reglas/acciones-especialidad"),
]

def fix_image_format(content):
    """
    Cambia el formato de imagen de:
    ![Carta de acción]({{ '/assets/images/acciones/X.png' | relative_url }}){: .action-card-image }

    A:
    <img src="{{ '/assets/images/acciones/X.png' | relative_url }}" style="float: right; width: 150px; margin-left: 15px; margin-bottom: 10px;" alt="Carta de acción">
    """
    # Patrón para encontrar la imagen markdown con clase
    pattern = r"!\[Carta de acción\]\(\{\{\s*'(/assets/images/acciones/[^']+)'\s*\|\s*relative_url\s*\}\}\)\{:\s*\.action-card-image\s*\}"

    def replace_func(match):
        image_path = match.group(1)
        return f'<img src="{{{{ \'{image_path}\' | relative_url }}}}" style="float: right; width: 150px; margin-left: 15px; margin-bottom: 10px;" alt="Carta de acción">'

    return re.sub(pattern, replace_func, content)

def process_file(filepath):
    """Procesa un fichero MD."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si tiene imagen de acción
    if 'assets/images/acciones/' not in content:
        return False

    # Verificar si ya está en formato HTML
    if '<img src="{{ \'/assets/images/acciones/' in content:
        return False

    new_content = fix_image_format(content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False

def main():
    print("Actualizando formato de imágenes de acciones")
    print("=" * 50)

    updated = 0
    skipped = 0

    for base_dir in DIRS_TO_PROCESS:
        if not base_dir.exists():
            continue

        # Procesar archivos MD recursivamente
        for md_file in base_dir.rglob('*.md'):
            if md_file.name == 'index.md':
                continue

            if process_file(md_file):
                print(f"  ✓ {md_file.relative_to(base_dir.parent.parent)}")
                updated += 1
            else:
                skipped += 1

    print("\n" + "=" * 50)
    print(f"✓ Actualizados: {updated}")
    print(f"⊘ Sin cambios: {skipped}")

if __name__ == "__main__":
    main()
