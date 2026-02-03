#!/usr/bin/env python3
"""
Script para convertir spans de rasgos en enlaces a sus archivos individuales.
De: <span class="feat-trait">Rasgo</span>
A: <a href="/rasgos/rasgo/" class="feat-trait">Rasgo</a>
"""

import re
import unicodedata
from pathlib import Path

# Directorios a procesar
DIRS_TO_PROCESS = [
    Path("/Users/ludo/code/pf2/docs/_clases"),
    Path("/Users/ludo/code/pf2/docs/_ascendencias"),
    Path("/Users/ludo/code/pf2/docs/_equipo"),
    Path("/Users/ludo/code/pf2/docs/_conjuros"),
    Path("/Users/ludo/code/pf2/docs/_reglas"),
    Path("/Users/ludo/code/pf2/docs/_habilidades"),
    Path("/Users/ludo/code/pf2/docs/_dotes"),
]

# Directorio de rasgos
RASGOS_DIR = Path("/Users/ludo/code/pf2/docs/_rasgos")

# Archivos/directorios a excluir
EXCLUDE_PATTERNS = [
    "_rasgos/",
    "_apendices/glosario.md",
]

def normalize_name(name):
    """Normaliza un nombre para generar el slug del archivo."""
    # Convertir a minúsculas
    name = name.lower()
    # Reemplazar espacios por guiones
    name = name.replace(' ', '-')
    # Eliminar acentos
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    # Eliminar caracteres especiales excepto guiones
    name = re.sub(r'[^a-z0-9-]', '', name)
    return name

def get_existing_traits():
    """Obtiene un diccionario de rasgos existentes."""
    traits = {}
    for md_file in RASGOS_DIR.glob('*.md'):
        if md_file.name == 'index.md':
            continue
        # El nombre del archivo sin extensión es el slug
        slug = md_file.stem
        traits[slug] = True
    return traits

def should_process(filepath):
    """Verifica si el archivo debe ser procesado."""
    filepath_str = str(filepath)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in filepath_str:
            return False
    return True

def convert_span_to_link(match, existing_traits, missing_traits):
    """Convierte un span de rasgo a enlace si el rasgo existe."""
    trait_name = match.group(1)
    slug = normalize_name(trait_name)

    if slug in existing_traits:
        return f'<a href="/rasgos/{slug}/" class="feat-trait">{trait_name}</a>'
    else:
        # Guardar rasgos no encontrados para reportar
        missing_traits.add(trait_name)
        # Dejar el span original
        return match.group(0)

def process_content(content, existing_traits, missing_traits):
    """Procesa el contenido y convierte los spans a enlaces."""
    # Patrón para <span class="feat-trait">Rasgo</span>
    pattern = r'<span class="feat-trait">([^<]+)</span>'

    def replacer(match):
        return convert_span_to_link(match, existing_traits, missing_traits)

    new_content = re.sub(pattern, replacer, content)

    return new_content, new_content != content

def process_file(filepath, existing_traits, missing_traits):
    """Procesa un archivo MD."""
    if not should_process(filepath):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si tiene spans de rasgos
    if '<span class="feat-trait">' not in content:
        return False

    new_content, changed = process_content(content, existing_traits, missing_traits)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False

def main():
    print("Convirtiendo spans de rasgos a enlaces")
    print("=" * 50)

    # Obtener rasgos existentes
    existing_traits = get_existing_traits()
    print(f"Rasgos existentes: {len(existing_traits)}")

    missing_traits = set()
    updated = 0
    skipped = 0

    for base_dir in DIRS_TO_PROCESS:
        if not base_dir.exists():
            continue

        for md_file in base_dir.rglob('*.md'):
            if md_file.name == 'index.md':
                skipped += 1
                continue

            if process_file(md_file, existing_traits, missing_traits):
                print(f"  ✓ {md_file.relative_to(base_dir.parent)}")
                updated += 1
            else:
                skipped += 1

    print("\n" + "=" * 50)
    print(f"✓ Actualizados: {updated}")
    print(f"⊘ Sin cambios: {skipped}")

    if missing_traits:
        print(f"\n⚠ Rasgos no encontrados ({len(missing_traits)}):")
        for trait in sorted(missing_traits):
            slug = normalize_name(trait)
            print(f"  - {trait} (slug: {slug})")

if __name__ == "__main__":
    main()
