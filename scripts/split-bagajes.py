#!/usr/bin/env python3
"""
Script para dividir bagajes.md en archivos individuales.
Crea un archivo por cada bagaje y actualiza el índice principal.
"""

import os
import re
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent.parent
BAGAJES_FILE = BASE_DIR / "docs/_ascendencias/bagajes.md"
BAGAJES_DIR = BASE_DIR / "docs/_ascendencias/bagajes"
OUTPUT_INDEX = BASE_DIR / "docs/_ascendencias/bagajes.md"

def slugify(text):
    """Convierte texto a slug para nombres de archivo."""
    # Convertir a minúsculas y reemplazar espacios
    slug = text.lower().strip()
    # Reemplazar caracteres especiales
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ü': 'u', ' ': '-'
    }
    for old, new in replacements.items():
        slug = slug.replace(old, new)
    # Eliminar caracteres no alfanuméricos excepto guiones
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug

def extract_short_description(content):
    """Extrae una descripción corta del contenido del bagaje."""
    # Buscar la primera oración del contenido
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('**') and not line.startswith('#'):
            # Tomar la primera oración
            sentences = re.split(r'[.!?]', line)
            if sentences and sentences[0]:
                desc = sentences[0].strip()
                if len(desc) > 80:
                    desc = desc[:77] + "..."
                return desc
    return "Bagaje de personaje"

def parse_bagajes(content):
    """Parsea el contenido del archivo y extrae los bagajes."""
    bagajes = []

    # Dividir por las secciones de bagaje (## Nombre)
    sections = re.split(r'\n## ', content)

    for section in sections[1:]:  # Saltar la introducción
        lines = section.strip().split('\n')
        if not lines:
            continue

        # Primera línea es el nombre
        name = lines[0].strip()

        # El resto es el contenido
        content_lines = lines[1:]
        bagaje_content = '\n'.join(content_lines).strip()

        # Extraer información estructurada
        mejoras = ""
        habilidades = ""
        dote = ""
        descripcion = ""

        for line in content_lines:
            line = line.strip()
            if line.startswith('**Mejoras de atributo:**'):
                mejoras = line.replace('**Mejoras de atributo:**', '').strip()
            elif line.startswith('**Habilidades:**'):
                habilidades = line.replace('**Habilidades:**', '').strip()
            elif line.startswith('**Dote:**'):
                dote = line.replace('**Dote:**', '').strip()
            elif line and not line.startswith('**') and not line.startswith('---') and line != '**Bagaje**':
                if not descripcion:
                    descripcion = line

        if name and descripcion:
            bagajes.append({
                'name': name,
                'slug': slugify(name),
                'descripcion': descripcion,
                'mejoras': mejoras,
                'habilidades': habilidades,
                'dote': dote,
                'short_desc': extract_short_description(descripcion)
            })

    return bagajes

def create_bagaje_file(bagaje, output_dir):
    """Crea el archivo individual para un bagaje."""
    filename = output_dir / f"{bagaje['slug']}.md"

    content = f"""---
layout: page
permalink: /ascendencias/bagajes/{bagaje['slug']}/
title: {bagaje['name']}
chapter: Ascendencias
category: ascendencias
source: PC1
parent: Bagajes
---

# {bagaje['name']}

**Bagaje**

{bagaje['descripcion']}

**Mejoras de atributo:** {bagaje['mejoras']}

**Habilidades:** {bagaje['habilidades']}

**Dote:** {bagaje['dote']}

---

[← Volver a Bagajes]({{{{ '/ascendencias/bagajes/' | relative_url }}}})
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Creado: {filename.name}")

def create_index_file(bagajes, output_file):
    """Crea el archivo índice con la tabla de bagajes."""

    # Crear tabla
    table_rows = []
    for b in sorted(bagajes, key=lambda x: x['name']):
        link = f"[{b['name']}]({{{{ '/ascendencias/bagajes/{b['slug']}/' | relative_url }}}})"
        table_rows.append(f"| {link} | {b['short_desc']} |")

    table = '\n'.join(table_rows)

    content = f"""---
layout: page
permalink: /ascendencias/bagajes/
title: Bagajes
chapter: Ascendencias
category: ascendencias
nav_order: 1
source: PC1
---

# Bagajes

A 1.er nivel, cuando creas tu personaje, obtienes un bagaje a tu elección. Esta decisión es permanente, y no puedes cambiarla a niveles posteriores. Cada bagaje indicado aquí concede dos mejoras, una dote de habilidad y el rango de competencia entrenado en dos habilidades, una de las cuales es de Saber.

Si obtienes el rango de competencia entrenado en una habilidad debido a tu bagaje y después obtendrías el rango de competencia entrenado en la misma habilidad debido a tu clase a 1.er nivel, en su lugar obtienes el rango entrenado en otra habilidad a tu elección.

Las habilidades de Saber representan un conocimiento profundo de un tema específico y se describen en la pág. 244. Si una de ellas implica una elección (por ejemplo, un tipo de terreno), explica tu preferencia al DJ, que tiene la última palabra sobre si es aceptable o no.

Las dotes de habilidad expanden las funciones de tus habilidades y aparecen en el Capítulo 5: Dotes.

---

## Lista de Bagajes

| Bagaje | Descripción |
|--------|-------------|
{table}
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nÍndice actualizado: {output_file}")

def main():
    print("=== Dividiendo bagajes.md ===\n")

    # Crear directorio si no existe
    BAGAJES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Directorio: {BAGAJES_DIR}\n")

    # Leer archivo original
    with open(BAGAJES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parsear bagajes
    bagajes = parse_bagajes(content)
    print(f"Encontrados {len(bagajes)} bagajes:\n")

    # Crear archivos individuales
    for bagaje in bagajes:
        create_bagaje_file(bagaje, BAGAJES_DIR)

    # Crear índice
    create_index_file(bagajes, OUTPUT_INDEX)

    print(f"\n=== Completado: {len(bagajes)} archivos creados ===")

if __name__ == "__main__":
    main()
