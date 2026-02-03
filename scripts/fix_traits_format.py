#!/usr/bin/env python3
"""
Script para corregir el formato de rasgos en los archivos de habilidades.
Convierte **Rasgos:** X, Y, Z a <div class="feat-traits-header">...</div>
"""

import os
import re
from pathlib import Path

def fix_traits_in_file(filepath):
    """Corrige el formato de rasgos en un archivo."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar el patrón **Rasgos:** seguido de una lista de rasgos
    pattern = r'\*\*Rasgos:\*\*\s*([^\n]+)'
    match = re.search(pattern, content)

    if not match:
        return False

    traits_text = match.group(1).strip()
    # Separar los rasgos por coma
    traits = [t.strip() for t in traits_text.split(',')]

    # Crear el nuevo formato HTML
    spans = ''.join([f'<span class="feat-trait">{t}</span>' for t in traits])
    new_format = f'<div class="feat-traits-header" markdown="0">{spans}</div>'

    # Reemplazar
    new_content = re.sub(pattern, new_format, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    base_path = Path('/Users/ludo/code/pf2/docs/_habilidades')

    # Carpetas de habilidades específicas (no 'acciones')
    skill_folders = [
        'sigilo', 'latrocinio', 'medicina', 'naturaleza', 'acrobacias',
        'atletismo', 'engano', 'diplomacia', 'intimidacion', 'artesania',
        'interpretacion', 'sociedad', 'supervivencia', 'arcanos'
    ]

    fixed_count = 0
    for folder in skill_folders:
        folder_path = base_path / folder
        if not folder_path.exists():
            continue

        for md_file in folder_path.glob('*.md'):
            if fix_traits_in_file(md_file):
                print(f'Corregido: {md_file.name}')
                fixed_count += 1

    print(f'\nTotal de archivos corregidos: {fixed_count}')

if __name__ == '__main__':
    main()
