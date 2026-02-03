#!/usr/bin/env python3
"""
Script para cambiar el formato de las imágenes de acciones:
- Usar clase CSS en lugar de estilos inline
- Mover la imagen debajo de feat-traits-header
- Cambiar ancho a 300px
"""

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
    Cambia el formato de imagen:
    1. Quita la imagen de su posición actual
    2. Cambia estilos inline por clase CSS
    3. La coloca después del div de traits (si existe) o después del frontmatter
    """
    # Patrón para la imagen con estilos inline
    img_pattern = r'<img src="(\{\{[^}]+\}\})" style="[^"]*" alt="Carta de acción">\n*'

    # Buscar la imagen
    img_match = re.search(img_pattern, content)
    if not img_match:
        return content, False

    image_src = img_match.group(1)

    # Quitar la imagen de su posición actual
    content = re.sub(img_pattern, '', content)

    # Nueva imagen con clase CSS
    new_img = f'<img src="{image_src}" class="action-card-image" alt="Carta de acción">'

    # Buscar el div de traits y colocar la imagen después
    traits_pattern = r'(<div class="feat-traits-header"[^>]*>.*?</div>)\n*'
    traits_match = re.search(traits_pattern, content)

    if traits_match:
        # Si hay div de traits, colocar imagen después
        def insert_image_after_traits(match):
            return match.group(1) + '\n\n' + new_img + '\n\n'
        new_content = re.sub(traits_pattern, insert_image_after_traits, content)
    else:
        # Si no hay div de traits, colocar después del frontmatter
        frontmatter_pattern = r'(---\n.*?\n---)\n*'
        def insert_image_after_frontmatter(match):
            return match.group(1) + '\n\n' + new_img + '\n\n'
        new_content = re.sub(frontmatter_pattern, insert_image_after_frontmatter, content, flags=re.DOTALL)

    return new_content, new_content != content

def process_file(filepath):
    """Procesa un fichero MD."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si tiene imagen de acción con estilo inline
    if 'style="float: right;' not in content:
        return False

    new_content, changed = fix_image_format(content)

    if changed:
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

        for md_file in base_dir.rglob('*.md'):
            if md_file.name == 'index.md':
                continue

            if process_file(md_file):
                print(f"  ✓ {md_file.name}")
                updated += 1
            else:
                skipped += 1

    print("\n" + "=" * 50)
    print(f"✓ Actualizados: {updated}")
    print(f"⊘ Sin cambios: {skipped}")

if __name__ == "__main__":
    main()
