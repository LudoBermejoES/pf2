#!/usr/bin/env python3
"""
Script para corregir el campo 'chapter' en archivos de _ambientacion
que todavía tienen 'Introducción' en lugar de 'Ambientación'
"""

import os
import re
from pathlib import Path

def corregir_chapter(file_path):
    """Corrige el campo chapter de Introducción a Ambientación"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar y reemplazar solo dentro del front matter
    if content.startswith('---'):
        # Dividir el contenido en front matter y cuerpo
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            body = parts[2]

            # Reemplazar chapter: Introducción por chapter: Ambientación
            if 'chapter: Introducción' in front_matter:
                front_matter = front_matter.replace('chapter: Introducción', 'chapter: Ambientación')
                new_content = f'---{front_matter}---{body}'

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                return True

    return False

def main():
    # Buscar todos los archivos .md en _ambientacion
    ambientacion_dir = Path('docs/_ambientacion')
    archivos_corregidos = []

    for md_file in ambientacion_dir.rglob('*.md'):
        if corregir_chapter(md_file):
            archivos_corregidos.append(str(md_file))
            print(f"✓ Corregido: {md_file}")

    print(f"\n✅ Total de archivos corregidos: {len(archivos_corregidos)}")

    if archivos_corregidos:
        print("\nArchivos modificados:")
        for archivo in archivos_corregidos:
            print(f"  - {archivo}")

if __name__ == '__main__':
    main()
