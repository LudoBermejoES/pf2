#!/usr/bin/env python3
"""
Script para agregar imágenes de tarjetas de acción a los ficheros MD de acciones.
Añade la imagen después del frontmatter YAML.
"""

import os
import re
from pathlib import Path

# Directorios
HABILIDADES_DIR = Path("/Users/ludo/code/pf2/docs/_habilidades")
REGLAS_DIR = Path("/Users/ludo/code/pf2/docs/_reglas")
IMAGES_DIR = Path("/Users/ludo/code/pf2/docs/assets/images/acciones")

def get_image_filename(md_filename):
    """Obtiene el nombre del archivo de imagen correspondiente al MD."""
    # El nombre de la imagen es el mismo que el del fichero MD pero con .png
    base_name = md_filename.replace('.md', '')
    png_name = f"{base_name}.png"
    return png_name

def has_action_image(content):
    """Verifica si el contenido ya tiene una imagen de acción."""
    return 'assets/images/acciones/' in content

def add_image_to_content(content, image_path):
    """Añade la referencia de imagen después del frontmatter."""
    # Buscar el final del frontmatter (segundo ---)
    match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        rest_of_content = content[len(frontmatter):]

        # Crear la línea de imagen con estilo para que flote a la derecha
        image_line = f"\n![Carta de acción]({{{{ '{image_path}' | relative_url }}}})"
        image_line += "{: .action-card-image }\n"

        return frontmatter + image_line + rest_of_content
    return content

def process_skill_subfolders():
    """Procesa las subcarpetas de habilidades con acciones individuales."""
    processed = 0
    skipped = 0
    not_found = 0

    # Subcarpetas de habilidades que contienen acciones individuales
    skill_folders = [
        'acrobacias', 'atletismo', 'sigilo', 'latrocinio', 'medicina',
        'naturaleza', 'engano', 'diplomacia', 'intimidacion', 'artesania',
        'interpretacion', 'sociedad', 'supervivencia', 'arcanos', 'acciones'
    ]

    for skill in skill_folders:
        skill_path = HABILIDADES_DIR / skill
        if not skill_path.exists():
            continue

        for md_file in skill_path.glob('*.md'):
            # Saltar archivos index
            if md_file.name == 'index.md':
                continue

            # Obtener nombre de imagen
            image_filename = get_image_filename(md_file.name)
            image_full_path = IMAGES_DIR / image_filename

            # Verificar si la imagen existe
            if not image_full_path.exists():
                print(f"  ⚠ Imagen no encontrada: {image_filename}")
                not_found += 1
                continue

            # Leer contenido
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verificar si ya tiene imagen
            if has_action_image(content):
                skipped += 1
                continue

            # Añadir imagen
            image_path = f"/assets/images/acciones/{image_filename}"
            new_content = add_image_to_content(content, image_path)

            # Guardar
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"  ✓ {md_file.name}")
            processed += 1

    return processed, skipped, not_found

def process_reglas_folder():
    """Procesa las carpetas de acciones en _reglas (básicas y especialidad)."""
    processed = 0
    skipped = 0
    not_found = 0

    if not REGLAS_DIR.exists():
        return processed, skipped, not_found

    # Subcarpetas de acciones en _reglas
    action_folders = ['acciones-basicas', 'acciones-especialidad']

    for folder_name in action_folders:
        folder_path = REGLAS_DIR / folder_name
        if not folder_path.exists():
            continue

        for md_file in folder_path.glob('*.md'):
            if md_file.name == 'index.md':
                continue

            image_filename = get_image_filename(md_file.name)
            image_full_path = IMAGES_DIR / image_filename

            if not image_full_path.exists():
                print(f"  ⚠ Imagen no encontrada: {image_filename}")
                not_found += 1
                continue

            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if has_action_image(content):
                skipped += 1
                continue

            image_path = f"/assets/images/acciones/{image_filename}"
            new_content = add_image_to_content(content, image_path)

            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"  ✓ {md_file.name}")
            processed += 1

    return processed, skipped, not_found

def main():
    print("Agregando imágenes a ficheros de acciones")
    print("=" * 50)

    print("\nProcesando habilidades...")
    h_processed, h_skipped, h_not_found = process_skill_subfolders()

    print("\nProcesando acciones básicas/especiales...")
    a_processed, a_skipped, a_not_found = process_reglas_folder()

    total_processed = h_processed + a_processed
    total_skipped = h_skipped + a_skipped
    total_not_found = h_not_found + a_not_found

    print("\n" + "=" * 50)
    print(f"✓ Ficheros actualizados: {total_processed}")
    print(f"⊘ Ya tenían imagen: {total_skipped}")
    print(f"⚠ Imagen no encontrada: {total_not_found}")

if __name__ == "__main__":
    main()
