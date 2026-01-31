#!/usr/bin/env python3
"""
Script para reorganizar los archivos de conjuros con mejor estructura y rasgos.
- Convierte rasgos en HTML con las clases de CSS mejoradas
- Añade mejor espaciado entre secciones
- Normaliza el formato de todos los conjuros
"""

import os
import re
from pathlib import Path

SPELLS_DIR = Path("/Users/ludo/code/pf2/docs/_conjuros/spell-individual")

def parse_traits(traits_str):
    """Convierte una cadena de rasgos en HTML con divs."""
    if not traits_str:
        return ""

    # Dividir rasgos por comas y limpiar espacios
    traits = [t.strip().capitalize() for t in traits_str.split(',')]

    html_traits = '<div class="spell-traits-wrapper">\n'
    for trait in traits:
        html_traits += f'<span class="trait-tag">{trait}</span>\n'
    html_traits += '</div>'

    return html_traits

def reorganize_spell(file_path):
    """Reorganiza un archivo de conjuro individual."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Dividir frontmatter del contenido
        if not content.startswith('---'):
            return False

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        frontmatter = parts[1]
        body = parts[2].strip()

        # Parsear el cuerpo del conjuro
        lines = body.split('\n')

        # Encontrar la línea del título
        title_idx = -1
        for i, line in enumerate(lines):
            if line.startswith('##'):
                title_idx = i
                break

        if title_idx == -1:
            return False

        # Procesar el contenido
        new_content = f"---{frontmatter}---\n"

        # Agregar título
        title_line = lines[title_idx]
        new_content += f"{title_line}\n\n"

        # Procesar metadatos
        i = title_idx + 1
        traits_line = ""
        while i < len(lines):
            line = lines[i].strip()

            # Encontrar y procesar rasgos
            if line.startswith('**Rasgos:**'):
                traits_text = line.replace('**Rasgos:**', '').strip()
                traits_line = parse_traits(traits_text)
                i += 1
                continue

            # Procesar líneas de metadatos (negrita)
            if line.startswith('**') and ':' in line:
                new_content += f"{line}\n"
                i += 1
                continue

            # Si encontramos una línea vacía después de metadatos, salir del bucle
            if not line:
                i += 1
                if i < len(lines) and lines[i].strip():
                    break
                continue

            # Si no es metadata, paramos
            if not line.startswith('**'):
                break

            i += 1

        # Agregar rasgos si los encontramos
        if traits_line:
            new_content += f"\n{traits_line}\n"

        # Agregar el resto del contenido
        remaining = '\n'.join(lines[i:]).strip()
        if remaining:
            new_content += f"\n---\n\n{remaining}"

        # Escribir el archivo actualizado
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"Error procesando {file_path.name}: {e}")
        return False

def main():
    """Procesa todos los archivos de conjuros."""
    if not SPELLS_DIR.exists():
        print(f"Directorio no encontrado: {SPELLS_DIR}")
        return

    spell_files = sorted(SPELLS_DIR.glob('*.md'))
    total = len(spell_files)
    processed = 0
    failed = 0

    print(f"Procesando {total} archivos de conjuros...")

    for i, spell_file in enumerate(spell_files, 1):
        if reorganize_spell(spell_file):
            processed += 1
            if i % 50 == 0:
                print(f"  [{i}/{total}] Procesados: {processed}, Errores: {failed}")
        else:
            failed += 1

    print(f"\n✓ Completado:")
    print(f"  Total: {total}")
    print(f"  Procesados: {processed}")
    print(f"  Errores: {failed}")

if __name__ == '__main__':
    main()
