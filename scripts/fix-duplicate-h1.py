#!/usr/bin/env python3
"""
Detecta y elimina H1 duplicados cuando el título del frontmatter coincide con el H1 del contenido.
"""

import re
from pathlib import Path

def fix_duplicate_h1():
    docs_root = Path("/Users/ludo/code/pf2/docs")

    # Directorios a revisar
    dirs_to_check = [
        docs_root / "_ascendencias",
        docs_root / "_clases"
    ]

    fixed_files = []
    checked_files = 0

    for dir_path in dirs_to_check:
        if not dir_path.exists():
            continue

        for filepath in dir_path.rglob("*.md"):
            checked_files += 1
            content = filepath.read_text(encoding='utf-8')

            # Extraer frontmatter
            frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            if not frontmatter_match:
                continue

            frontmatter = frontmatter_match.group(1)
            body = frontmatter_match.group(2)

            # Extraer título del frontmatter
            title_match = re.search(r'^title:\s*(.+)$', frontmatter, re.MULTILINE)
            if not title_match:
                continue

            title = title_match.group(1).strip().strip('"').strip("'")

            # Buscar H1 al inicio del body que coincida con el título
            h1_pattern = rf'^#\s+{re.escape(title)}\s*\n'
            h1_match = re.match(h1_pattern, body.lstrip(), re.IGNORECASE)

            if h1_match:
                # Eliminar el H1 duplicado
                new_body = re.sub(h1_pattern, '', body.lstrip(), count=1, flags=re.IGNORECASE)
                new_content = f"---\n{frontmatter}\n---\n\n{new_body.lstrip()}"

                filepath.write_text(new_content, encoding='utf-8')
                fixed_files.append(str(filepath.relative_to(docs_root)))
                print(f"✅ Corregido: {filepath.relative_to(docs_root)}")

    print(f"\n📊 Resumen:")
    print(f"   Archivos revisados: {checked_files}")
    print(f"   Archivos corregidos: {len(fixed_files)}")

    return fixed_files

if __name__ == '__main__':
    fix_duplicate_h1()
