#!/usr/bin/env python3

import os
import re
from pathlib import Path

def add_source_pc1_to_file(filepath):
    """Add source: PC1 to a markdown file with Jekyll frontmatter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has Jekyll frontmatter
        if not content.startswith('---'):
            return None

        # Check if it already has a source field
        if re.search(r'^\s*source:', content, re.MULTILINE):
            return 'skip'

        # Find the closing --- of the frontmatter
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return None

        frontmatter = match.group(1)
        rest_of_file = content[match.end():]

        # Add source: PC1 to frontmatter
        new_frontmatter = frontmatter + '\nsource: PC1'
        new_content = f'---\n{new_frontmatter}\n---\n{rest_of_file}'

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return 'added'
    except Exception as e:
        print(f"❌ Error en {filepath}: {e}")
        return 'error'

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')

    print("📝 Añadiendo source: PC1 a archivos existentes...")
    print("=" * 50)

    stats = {'added': 0, 'skip': 0, 'error': 0, 'none': 0}

    # Find all .md files recursively
    for md_file in sorted(docs_dir.rglob('*.md')):
        result = add_source_pc1_to_file(md_file)

        if result == 'added':
            stats['added'] += 1
            rel_path = md_file.relative_to(docs_dir)
            print(f"✅ {rel_path}")
        elif result == 'skip':
            stats['skip'] += 1
        elif result == 'error':
            stats['error'] += 1
        else:
            stats['none'] += 1

    print("")
    print("=" * 50)
    print(f"✨ Proceso completado:")
    print(f"   ✅ Archivos actualizados: {stats['added']}")
    print(f"   ⏭️  Archivos ya tenían source: {stats['skip']}")
    print(f"   ⚠️  Archivos sin frontmatter válido: {stats['none']}")
    print(f"   ❌ Errores: {stats['error']}")
    print("=" * 50)

if __name__ == '__main__':
    main()
