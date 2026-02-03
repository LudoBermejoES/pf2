#!/usr/bin/env python3
"""
Script para convertir **Rasgos:** texto al formato con spans:
<div class="feat-traits-header" markdown="0"><span class="feat-trait">Rasgo1</span><span class="feat-trait">Rasgo2</span></div>
"""

import re
from pathlib import Path

# Directorios a procesar (excluir glosario y rasgos individuales)
DIRS_TO_PROCESS = [
    Path("/Users/ludo/code/pf2/docs/_clases"),
    Path("/Users/ludo/code/pf2/docs/_ascendencias"),
    Path("/Users/ludo/code/pf2/docs/_equipo"),
    Path("/Users/ludo/code/pf2/docs/_conjuros"),
    Path("/Users/ludo/code/pf2/docs/_reglas"),
]

# Archivos/directorios a excluir
EXCLUDE_PATTERNS = [
    "_apendices/glosario.md",
    "_rasgos/",
]

def should_process(filepath):
    """Verifica si el archivo debe ser procesado."""
    filepath_str = str(filepath)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in filepath_str:
            return False
    return True

def convert_traits_line(match):
    """Convierte una línea **Rasgos:** a formato con spans."""
    traits_text = match.group(1).strip()

    # Separar los rasgos por coma
    traits = [t.strip() for t in traits_text.split(',')]

    # Crear spans para cada rasgo
    spans = ''.join(f'<span class="feat-trait">{trait}</span>' for trait in traits if trait)

    return f'<div class="feat-traits-header" markdown="0">{spans}</div>'

def process_content(content):
    """Procesa el contenido y convierte los rasgos."""
    # Patrón para **Rasgos:** seguido de texto hasta el final de línea
    pattern = r'\*\*Rasgos:\*\*\s*(.+?)(?:\n|$)'

    new_content = re.sub(pattern, lambda m: convert_traits_line(m) + '\n', content)

    return new_content, new_content != content

def process_file(filepath):
    """Procesa un archivo MD."""
    if not should_process(filepath):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si tiene **Rasgos:**
    if '**Rasgos:**' not in content:
        return False

    new_content, changed = process_content(content)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False

def main():
    print("Convirtiendo **Rasgos:** a formato con spans")
    print("=" * 50)

    updated = 0
    skipped = 0

    for base_dir in DIRS_TO_PROCESS:
        if not base_dir.exists():
            continue

        for md_file in base_dir.rglob('*.md'):
            if md_file.name == 'index.md':
                skipped += 1
                continue

            if process_file(md_file):
                print(f"  ✓ {md_file.relative_to(base_dir.parent)}")
                updated += 1
            else:
                skipped += 1

    print("\n" + "=" * 50)
    print(f"✓ Actualizados: {updated}")
    print(f"⊘ Sin cambios: {skipped}")

if __name__ == "__main__":
    main()
