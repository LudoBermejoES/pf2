#!/usr/bin/env python3
"""
Script para eliminar títulos H1 duplicados en archivos markdown.
Los títulos ya se muestran desde el campo 'title' del front matter,
por lo que no es necesario repetirlos como H1 en el contenido.
"""

import os
import re
from pathlib import Path

def eliminar_h1_duplicado(file_path):
    """Elimina el primer título H1 si está duplicando el campo title del front matter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividir el contenido en front matter y cuerpo
    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    front_matter = parts[1]
    body = parts[2]

    # Extraer el título del front matter
    title_match = re.search(r'^title:\s*(.+)$', front_matter, re.MULTILINE)
    if not title_match:
        return False

    title = title_match.group(1).strip()

    # Buscar el primer H1 en el cuerpo
    h1_match = re.search(r'^\s*#\s+(.+?)(?:\n|$)', body, re.MULTILINE)
    if not h1_match:
        return False

    h1_text = h1_match.group(1).strip()

    # Comparar títulos (ignorando mayúsculas/minúsculas y artículos)
    title_normalized = title.lower().replace('el ', '').replace('la ', '').replace('los ', '').replace('las ', '')
    h1_normalized = h1_text.lower().replace('el ', '').replace('la ', '').replace('los ', '').replace('las ', '')

    # Si son similares, eliminar el H1
    if title_normalized in h1_normalized or h1_normalized in title_normalized:
        # Eliminar el H1 y la línea en blanco siguiente si existe
        body_lines = body.split('\n')
        new_body_lines = []
        skip_next_blank = False

        for i, line in enumerate(body_lines):
            # Si es el primer H1, saltarlo
            if i == 0 and line.strip() == '':
                continue  # Saltar línea en blanco inicial
            if line.strip().startswith('# ') and i <= 2:  # Solo considerar H1 al inicio
                skip_next_blank = True
                continue
            if skip_next_blank and line.strip() == '':
                skip_next_blank = False
                continue
            new_body_lines.append(line)

        # Reconstruir el archivo
        new_body = '\n'.join(new_body_lines)
        new_content = f'---{front_matter}---{new_body}'

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    return False

def main():
    # Buscar todos los archivos .md en _ambientacion
    ambientacion_dir = Path('docs/_ambientacion')
    archivos_corregidos = []

    for md_file in ambientacion_dir.rglob('*.md'):
        if eliminar_h1_duplicado(md_file):
            archivos_corregidos.append(str(md_file))
            print(f"✓ H1 duplicado eliminado: {md_file}")

    print(f"\n✅ Total de archivos corregidos: {len(archivos_corregidos)}")

    if archivos_corregidos:
        print("\nArchivos modificados:")
        for archivo in archivos_corregidos:
            print(f"  - {archivo}")

if __name__ == '__main__':
    main()
