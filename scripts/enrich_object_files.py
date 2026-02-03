#!/usr/bin/env python3
"""
Script para enriquecer los archivos individuales de objetos con datos de las tablas de objetos.md.
Añade: Precio, Impedimenta, Manos, y nivel si aplica.
"""

import os
import re
from pathlib import Path

OBJETOS_DIR = Path("/Users/ludo/code/pf2/docs/_equipo/objetos")
OBJETOS_MD = Path("/Users/ludo/code/pf2/docs/_equipo/objetos.md")

def parse_objects_from_md():
    """Parsea objetos.md y extrae los datos de cada objeto."""
    with open(OBJETOS_MD, 'r', encoding='utf-8') as f:
        content = f.read()

    objects = {}
    is_uncommon = False

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Detectar sección poco común
        if '## Equipo de aventura poco común' in line:
            is_uncommon = True

        # Parsear líneas de tabla con enlaces
        # Formato: | [Nombre](/enlace/) | Precio | Imp. | Manos |
        if '| [' in line and '/equipo/objetos/' in line:
            # Extraer nombre y enlace
            match = re.search(r'\[([^\]]+)\]\((/equipo/objetos/[^)]+/)\)', line)
            if match:
                name = match.group(1)
                link = match.group(2)
                slug = link.rstrip('/').split('/')[-1]

                # Parsear columnas
                cols = [c.strip() for c in line.split('|')[1:-1]]

                # Las columnas pueden variar, buscar patrones
                if len(cols) >= 4:
                    # Buscar el precio (columna que contiene po, pp, pc, mo)
                    precio = cols[1] if len(cols) > 1 else '—'
                    impedimenta = cols[2] if len(cols) > 2 else '—'
                    manos = cols[3] if len(cols) > 3 else '—'

                    # Extraer nivel si está en el nombre
                    nivel_match = re.search(r'\(nivel (\d+)\)', name, re.IGNORECASE)
                    nivel = nivel_match.group(1) if nivel_match else None

                    # Si el slug ya existe, puede ser una variante
                    if slug not in objects or nivel:
                        objects[slug] = {
                            'nombre': name,
                            'precio': precio,
                            'impedimenta': impedimenta,
                            'manos': manos,
                            'nivel': nivel,
                            'poco_comun': is_uncommon,
                        }

    return objects

def enrich_object_file(filepath, object_data):
    """Enriquece un archivo de objeto con los datos."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar frontmatter del contenido
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2].strip()

    # Verificar si ya tiene datos (evitar duplicar)
    if '**Precio**' in body:
        return False

    # Construir nuevo contenido
    new_body_parts = []

    # Línea de precio y nivel
    precio = object_data.get('precio', '—')
    nivel = object_data.get('nivel')

    if nivel:
        new_body_parts.append(f"**Nivel** {nivel}; **Precio** {precio}")
    else:
        new_body_parts.append(f"**Precio** {precio}")

    new_body_parts.append("")

    # Rasgo poco común si aplica
    if object_data.get('poco_comun'):
        new_body_parts.append('<div class="feat-traits-header" markdown="0"><a href="/apendices/rasgos/poco-comun/" class="feat-trait">Poco común</a></div>')
        new_body_parts.append("")

    new_body_parts.append("---")
    new_body_parts.append("")

    # Datos mecánicos
    stats = []

    impedimenta = object_data.get('impedimenta', '—')
    if impedimenta and impedimenta != '—':
        stats.append(f"**Impedimenta** {impedimenta}")

    manos = object_data.get('manos', '—')
    if manos and manos != '—':
        stats.append(f"**Manos** {manos}")

    if stats:
        new_body_parts.append("; ".join(stats))
        new_body_parts.append("")
        new_body_parts.append("---")
        new_body_parts.append("")

    # Descripción original
    if body:
        new_body_parts.append(body)

    # Sección "Ver también"
    new_body_parts.append("")
    new_body_parts.append("---")
    new_body_parts.append("")
    new_body_parts.append("## Ver también")
    new_body_parts.append("")
    new_body_parts.append("- [Lista de objetos](/equipo/objetos/)")

    new_content = f"---{frontmatter}---\n\n" + "\n".join(new_body_parts) + "\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    # Parsear datos de objetos.md
    print("Parseando objetos.md...")
    objects = parse_objects_from_md()
    print(f"Encontrados {len(objects)} objetos en las tablas")

    # Listar archivos de objetos
    object_files = list(OBJETOS_DIR.glob("*.md"))
    print(f"Encontrados {len(object_files)} archivos de objetos")

    enriched = 0
    not_found = []
    already_enriched = []

    for filepath in object_files:
        slug = filepath.stem

        # Saltar archivos especiales
        if slug in ['index']:
            continue

        if slug in objects:
            if enrich_object_file(filepath, objects[slug]):
                print(f"Enriquecido: {slug}")
                enriched += 1
            else:
                already_enriched.append(slug)
        else:
            not_found.append(slug)

    print(f"\nResumen:")
    print(f"  Enriquecidos: {enriched}")
    print(f"  Ya tenían datos: {len(already_enriched)}")
    print(f"  No encontrados en tablas: {len(not_found)}")

    if not_found:
        print(f"\nObjetos sin datos en tablas:")
        for slug in sorted(not_found):
            print(f"  - {slug}")

if __name__ == "__main__":
    main()
