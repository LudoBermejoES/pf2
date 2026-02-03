#!/usr/bin/env python3
"""
Script para actualizar los permalinks de rasgos de /rasgos/ a /apendices/rasgos/
y actualizar todos los enlaces en el proyecto.
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path("/Users/ludo/code/pf2/docs")
RASGOS_DIR = DOCS_DIR / "_apendices" / "rasgos"

def update_rasgo_permalinks():
    """Actualiza los permalinks en los archivos de rasgos."""
    updated = 0
    for filepath in RASGOS_DIR.glob("*.md"):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Cambiar permalink: /rasgos/X/ a permalink: /apendices/rasgos/X/
        new_content = re.sub(
            r'permalink:\s*/rasgos/([^/\n]+)/',
            r'permalink: /apendices/rasgos/\1/',
            content
        )

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1
            print(f"Actualizado permalink: {filepath.name}")

    return updated

def update_all_links():
    """Actualiza todos los enlaces a rasgos en el proyecto."""
    updated_files = 0
    total_links = 0

    # Buscar en todos los archivos markdown del proyecto
    for filepath in DOCS_DIR.rglob("*.md"):
        # Saltar archivos en _apendices/rasgos (ya procesados sus permalinks)
        if "_apendices/rasgos" in str(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar y reemplazar enlaces a rasgos
        # Patrón: href="/rasgos/X/" -> href="/apendices/rasgos/X/"
        new_content = re.sub(
            r'href="/rasgos/([^"]+)"',
            r'href="/apendices/rasgos/\1"',
            content
        )

        if new_content != content:
            links_changed = content.count('href="/rasgos/') - new_content.count('href="/rasgos/')
            total_links += links_changed
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files += 1
            print(f"Actualizado {links_changed} enlaces en: {filepath.relative_to(DOCS_DIR)}")

    return updated_files, total_links

def main():
    print("=" * 60)
    print("Actualizando permalinks de rasgos...")
    print("=" * 60)

    permalinks_updated = update_rasgo_permalinks()
    print(f"\nPermalinks actualizados: {permalinks_updated}")

    print("\n" + "=" * 60)
    print("Actualizando enlaces en todo el proyecto...")
    print("=" * 60)

    files_updated, links_updated = update_all_links()
    print(f"\nArchivos actualizados: {files_updated}")
    print(f"Total de enlaces actualizados: {links_updated}")

if __name__ == "__main__":
    main()
