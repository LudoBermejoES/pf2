#!/usr/bin/env python3
"""
Script para añadir bagajes de PC2 a la estructura existente.
Lee bagajes-comunes.md y bagajes-raros.md, crea archivos individuales
y actualiza el índice principal.
"""

import os
import re
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent.parent
BAGAJES_COMUNES = BASE_DIR / "original/player_core_2_es/01-ascendencias/bagajes-comunes.md"
BAGAJES_RAROS = BASE_DIR / "original/player_core_2_es/01-ascendencias/bagajes-raros.md"
BAGAJES_DIR = BASE_DIR / "docs/_ascendencias/bagajes"
BAGAJES_INDEX = BASE_DIR / "docs/_ascendencias/bagajes.md"

# Descripciones cortas para cada bagaje PC2
SHORT_DESCRIPTIONS = {
    # Comunes
    "Astrólogo": "Lector de estrellas y presagios celestiales",
    "Barbero": "Cirujano y sanador con navaja",
    "Contable": "Experto en números y finanzas",
    "Mensajero": "Corredor urbano de recados",
    "Conductor": "Experto en vehículos de todo tipo",
    "Insurgente": "Revolucionario y luchador por una causa",
    "Jinete explorador": "Vanguardia a caballo de tierras lejanas",
    "Peregrino": "Viajero devoto de lugares sagrados",
    "Refugiado": "Forastero desplazado de tierras lejanas",
    "Curandero de raíces": "Sanador ritual con remedios naturales",
    "Saboteador": "Experto en destrucción y puntos débiles",
    "Rebuscador": "Superviviente que vive de lo desechado",
    "Sirviente": "Criado de confianza de familias nobles",
    "Escudero": "Aprendiz de caballero en formación",
    "Recaudador de impuestos": "Cobrador al servicio del estado",
    "Pupilo": "Huérfano criado por otra familia",
    # Raros
    "Amnésico": "Sin recuerdos de tu pasado",
    "Bendecido": "Tocado por el favor divino",
    "Maldito": "Víctima de una maldición persistente",
    "Niño salvaje": "Criado por animales en la naturaleza",
    "Vinculado al Primer Mundo": "Marcado por un pacto con las hadas",
    "Embrujado": "Acompañado por una entidad misteriosa",
    "Retornado": "Regresaste de entre los muertos",
    "Realeza": "Miembro de una familia real",
}

def slugify(text):
    """Convierte texto a slug para nombres de archivo."""
    slug = text.lower().strip()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ü': 'u', ' ': '-'
    }
    for old, new in replacements.items():
        slug = slug.replace(old, new)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug

def parse_bagajes_comunes(content):
    """Parsea bagajes comunes de PC2."""
    bagajes = []
    sections = re.split(r'\n## ', content)

    for section in sections[1:]:
        lines = section.strip().split('\n')
        name = lines[0].strip()

        # Extraer contenido
        full_content = '\n'.join(lines[1:]).strip()

        # Buscar descripción (primer párrafo después del nombre)
        paragraphs = [p.strip() for p in full_content.split('\n\n') if p.strip()]
        descripcion = paragraphs[0] if paragraphs else ""

        # Buscar mejoras, habilidades y dote
        mejoras = ""
        habilidades = ""
        dote = ""

        for line in lines:
            if "mejoras de atributo" in line.lower():
                mejoras = line.strip()
            elif "Estás entrenado en" in line:
                # Parsear habilidades y dote de esta línea
                parts = line.split("Obtienes")
                if parts:
                    hab_match = re.search(r'entrenado en \*\*(.+?)\*\*', parts[0])
                    saber_match = re.search(r'en \*\*Saber[^*]+\*\*', parts[0])
                    if hab_match:
                        habilidades = hab_match.group(1)
                        if saber_match:
                            habilidades += ", " + saber_match.group(0).replace("en **", "").replace("**", "")
                if len(parts) > 1:
                    dote_match = re.search(r'dote de habilidad \*\*(.+?)\*\*', parts[1])
                    if dote_match:
                        dote = dote_match.group(1)

        if name:
            bagajes.append({
                'name': name,
                'slug': slugify(name),
                'descripcion': descripcion,
                'mejoras': mejoras,
                'habilidades': habilidades,
                'dote': dote,
                'raro': False,
                'short_desc': SHORT_DESCRIPTIONS.get(name, "Bagaje de PC2"),
                'full_content': full_content
            })

    return bagajes

def parse_bagajes_raros(content):
    """Parsea bagajes raros de PC2."""
    bagajes = []
    sections = re.split(r'\n## ', content)

    for section in sections[1:]:
        lines = section.strip().split('\n')
        name = lines[0].strip()

        # Extraer contenido completo
        full_content = '\n'.join(lines[1:]).strip()

        # Buscar descripción (después de **Rasgos:** Raro)
        desc_lines = []
        in_desc = False
        for line in lines[1:]:
            if line.strip().startswith("**Rasgos:**"):
                in_desc = True
                continue
            if in_desc and line.strip() and not line.strip().startswith("Elige") and not line.strip().startswith("Obtienes") and not line.strip().startswith("Estás"):
                desc_lines.append(line.strip())
            elif line.strip().startswith("Elige") or line.strip().startswith("Obtienes"):
                break

        descripcion = ' '.join(desc_lines)

        if name:
            bagajes.append({
                'name': name,
                'slug': slugify(name),
                'descripcion': descripcion,
                'raro': True,
                'short_desc': SHORT_DESCRIPTIONS.get(name, "Bagaje raro de PC2"),
                'full_content': full_content
            })

    return bagajes

def create_bagaje_file(bagaje, output_dir):
    """Crea el archivo individual para un bagaje PC2."""
    filename = output_dir / f"{bagaje['slug']}.md"

    raro_tag = "\n\n**Rasgos:** Raro" if bagaje['raro'] else ""

    content = f"""---
layout: page
permalink: /ascendencias/bagajes/{bagaje['slug']}/
title: {bagaje['name']}
chapter: Ascendencias
category: ascendencias
source: PC2
parent: Bagajes
---

# {bagaje['name']}

**Bagaje**{raro_tag}

{bagaje['full_content']}

---

[← Volver a Bagajes]({{{{ '/ascendencias/bagajes/' | relative_url }}}})
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Creado: {filename.name}")

def update_index_file(new_bagajes, index_file):
    """Actualiza el índice añadiendo los nuevos bagajes en orden alfabético."""

    # Leer índice actual
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer bagajes existentes de la tabla
    existing_bagajes = []
    table_match = re.search(r'\| Bagaje \| Descripción \|\n\|[-]+\|[-]+\|\n((?:\|[^\n]+\|\n?)+)', content)

    if table_match:
        table_rows = table_match.group(1).strip().split('\n')
        for row in table_rows:
            # Parsear cada fila: | [Nombre](url) | Descripción |
            match = re.match(r'\| \[([^\]]+)\]\(([^)]+)\) \| ([^|]+) \|', row)
            if match:
                name = match.group(1)
                url = match.group(2)
                desc = match.group(3).strip()
                # Extraer slug de la URL
                slug_match = re.search(r'/bagajes/([^/]+)/', url)
                slug = slug_match.group(1) if slug_match else slugify(name)
                existing_bagajes.append({
                    'name': name,
                    'slug': slug,
                    'short_desc': desc
                })

    # Añadir nuevos bagajes
    all_bagajes = existing_bagajes + [{
        'name': b['name'],
        'slug': b['slug'],
        'short_desc': b['short_desc']
    } for b in new_bagajes]

    # Ordenar alfabéticamente
    all_bagajes.sort(key=lambda x: x['name'].lower())

    # Generar nueva tabla
    table_rows = []
    for b in all_bagajes:
        link = f"[{b['name']}]({{{{ '/ascendencias/bagajes/{b['slug']}/' | relative_url }}}})"
        table_rows.append(f"| {link} | {b['short_desc']} |")

    new_table = "| Bagaje | Descripción |\n|--------|-------------|\n" + '\n'.join(table_rows)

    # Reemplazar tabla en el contenido
    new_content = re.sub(
        r'\| Bagaje \| Descripción \|\n\|[-]+\|[-]+\|\n(?:\|[^\n]+\|\n?)+',
        new_table,
        content
    )

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nÍndice actualizado: {index_file}")
    print(f"  Total bagajes: {len(all_bagajes)}")

def main():
    print("=== Añadiendo bagajes de PC2 ===\n")

    # Crear directorio si no existe
    BAGAJES_DIR.mkdir(parents=True, exist_ok=True)

    # Leer y parsear archivos fuente
    with open(BAGAJES_COMUNES, 'r', encoding='utf-8') as f:
        content_comunes = f.read()

    with open(BAGAJES_RAROS, 'r', encoding='utf-8') as f:
        content_raros = f.read()

    bagajes_comunes = parse_bagajes_comunes(content_comunes)
    bagajes_raros = parse_bagajes_raros(content_raros)

    all_new_bagajes = bagajes_comunes + bagajes_raros

    print(f"Bagajes comunes: {len(bagajes_comunes)}")
    print(f"Bagajes raros: {len(bagajes_raros)}")
    print(f"Total nuevos: {len(all_new_bagajes)}\n")

    # Crear archivos individuales
    print("Creando archivos individuales:")
    for bagaje in all_new_bagajes:
        create_bagaje_file(bagaje, BAGAJES_DIR)

    # Actualizar índice
    update_index_file(all_new_bagajes, BAGAJES_INDEX)

    print(f"\n=== Completado: {len(all_new_bagajes)} bagajes PC2 añadidos ===")

if __name__ == "__main__":
    main()
