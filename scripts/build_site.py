#!/usr/bin/env python3
"""
Build script for Pathfinder 2 Player Core GitHub Pages site.
Processes markdown files from docs/player_core and generates:
1. Properly formatted Jekyll pages with front matter
2. Search index (JSON) for Lunr.js
3. Navigation data
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
SOURCE_DIR = Path("docs/player_core")
OUTPUT_DIR = Path("docs")
SEARCH_INDEX_PATH = OUTPUT_DIR / "assets/js/search-index.json"

# Chapter mapping
CHAPTER_MAP = {
    "00-introduccion": {
        "collection": "_introduccion",
        "category": "introduccion",
        "title": "Introducción",
        "order": 0
    },
    "01-ascendencias": {
        "collection": "_ascendencias",
        "category": "ascendencias",
        "title": "Ascendencias",
        "order": 1
    },
    "02-clases": {
        "collection": "_clases",
        "category": "clases",
        "title": "Clases",
        "order": 2
    },
    "03-habilidades": {
        "collection": "_habilidades",
        "category": "habilidades",
        "title": "Habilidades",
        "order": 3
    },
    "04-dotes": {
        "collection": "_dotes",
        "category": "dotes",
        "title": "Dotes",
        "order": 4
    },
    "05-equipo": {
        "collection": "_equipo",
        "category": "equipo",
        "title": "Equipo",
        "order": 5
    },
    "06-conjuros": {
        "collection": "_conjuros",
        "category": "conjuros",
        "title": "Conjuros",
        "order": 6
    },
    "07-como-jugar": {
        "collection": "_reglas",
        "category": "reglas",
        "title": "Cómo Jugar",
        "order": 7
    },
    "08-apendices": {
        "collection": "_apendices",
        "category": "apendices",
        "title": "Apéndices",
        "order": 8
    }
}

# File title mappings for better display
TITLE_MAP = {
    "que-es-jdr": "¿Qué es un Juego de Rol?",
    "como-se-juega": "Cómo se Juega",
    "creacion-personajes": "Creación de Personajes",
    "atributos": "Atributos",
    "puntos-basicos": "Puntos Básicos",
    "herramientas": "Herramientas del Juego",
    "dados": "Los Dados",
    "primera-regla": "La Primera Regla",
    "terminos-clave": "Términos Clave",
    "encuentros": "Modo Encuentro",
    "exploracion": "Modo Exploración",
    "tiempo-libre": "Tiempo Libre",
    "subir-nivel": "Subir de Nivel",
    "jugar-para-todos": "Jugar para Todos",
    "golarion": "El Mundo de Golarion",
    "religion": "Religión",
    "descripcion": "Descripción",
    "caracteristicas": "Características",
    "dotes": "Dotes",
    "herencias": "Herencias",
    "bagajes": "Bagajes",
    "idiomas": "Idiomas",
    "introduccion": "Introducción",
    "multiclase": "Multiclase",
    "animales": "Compañeros Animales",
    "familiares": "Familiares",
    "tabla": "Tabla de Referencia",
    "acciones-generales": "Acciones Generales",
    "generales": "Dotes Generales",
    "habilidad": "Dotes de Habilidad",
    "armas": "Armas",
    "armaduras": "Armaduras",
    "escudos": "Escudos",
    "objetos": "Objetos",
    "acciones": "Acciones",
    "acciones-basicas": "Acciones Básicas",
    "acciones-especialidad": "Acciones de Especialidad",
    "ataques-defensas": "Ataques y Defensas",
    "pruebas": "Pruebas",
    "movimiento": "Movimiento",
    "cobertura-flanqueo": "Cobertura y Flanqueo",
    "dano": "Daño",
    "puntos-golpe": "Puntos de Golpe",
    "efectos": "Efectos",
    "aflicciones": "Aflicciones",
    "modo-encuentro": "Modo Encuentro",
    "modo-exploracion": "Modo Exploración",
    "modo-tiempo-libre": "Modo Tiempo Libre",
    "percepcion-deteccion": "Percepción y Detección",
    "batallas-especiales": "Batallas Especiales",
    "glosario": "Glosario",
    "estados-a-e": "Estados (A-E)",
    "estados-f-z": "Estados (F-Z)"
}

# Ancestry names
ANCESTRIES = {
    "humano": "Humano",
    "elfo": "Elfo",
    "enano": "Enano",
    "mediano": "Mediano",
    "gnomo": "Gnomo",
    "orco": "Orco",
    "goblin": "Goblin",
    "leshy": "Leshy"
}

# Class names
CLASSES = {
    "guerrero": "Guerrero",
    "picaro": "Pícaro",
    "explorador": "Explorador",
    "clerigo": "Clérigo",
    "mago": "Mago",
    "druida": "Druida",
    "bardo": "Bardo",
    "brujo": "Brujo"
}

# Skill names
SKILLS = {
    "acrobacias": "Acrobacias",
    "arcanos": "Arcanos",
    "artesania": "Artesanía",
    "atletismo": "Atletismo",
    "diplomacia": "Diplomacia",
    "engano": "Engaño",
    "interpretacion": "Interpretación",
    "intimidacion": "Intimidación",
    "latrocinio": "Latrocinio",
    "medicina": "Medicina",
    "naturaleza": "Naturaleza",
    "ocultismo": "Ocultismo",
    "religion": "Religión",
    "saber": "Saber",
    "sigilo": "Sigilo",
    "sociedad": "Sociedad",
    "supervivencia": "Supervivencia"
}


def clean_text(text):
    """Remove markdown formatting for search indexing."""
    # Remove headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Remove table formatting
    text = re.sub(r'\|', ' ', text)
    text = re.sub(r'-{3,}', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_title(content, filename):
    """Extract title from markdown content or generate from filename."""
    # Look for first H1
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Use filename mapping
    name = Path(filename).stem
    if name in TITLE_MAP:
        return TITLE_MAP[name]

    # Capitalize filename
    return name.replace('-', ' ').title()


def get_file_url(source_path, chapter_info, filename):
    """Generate URL for a file."""
    category = chapter_info["category"]
    name = Path(filename).stem

    # Handle subdirectories
    parts = source_path.relative_to(SOURCE_DIR).parts
    if len(parts) > 2:
        # Has subdirectory (e.g., ascendencias/humano/descripcion.md)
        subdir = parts[1]
        return f"/{category}/{subdir}/{name}/"

    return f"/{category}/{name}/"


def extract_tags(content, category):
    """Extract relevant tags from content for search."""
    tags = [category]

    # Add trait tags
    trait_matches = re.findall(r'\*\*([A-Za-záéíóúñü]+)\*\*', content)
    tags.extend([t.lower() for t in trait_matches[:5]])

    return list(set(tags))


def process_markdown_file(filepath, chapter_key, chapter_info):
    """Process a single markdown file and return page data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = filepath.name
    title = extract_title(content, filename)
    url = get_file_url(filepath, chapter_info, filename)

    # Build front matter
    front_matter = {
        "layout": "page",
        "title": title,
        "chapter": chapter_info["title"],
        "category": chapter_info["category"],
        "nav_order": chapter_info["order"]
    }

    # Add specific layout for ancestries and classes
    parts = filepath.relative_to(SOURCE_DIR).parts
    if chapter_key == "01-ascendencias" and len(parts) > 1:
        ancestry = parts[1]
        if ancestry in ANCESTRIES:
            front_matter["ancestry"] = ANCESTRIES[ancestry]
    elif chapter_key == "02-clases" and len(parts) > 1:
        class_name = parts[1]
        if class_name in CLASSES:
            front_matter["class_name"] = CLASSES[class_name]

    # Create search entry
    search_entry = {
        "title": title,
        "url": url,
        "category": chapter_info["category"],
        "content": clean_text(content)[:2000],  # Limit content for search
        "tags": extract_tags(content, chapter_info["category"])
    }

    return {
        "filepath": filepath,
        "filename": filename,
        "front_matter": front_matter,
        "content": content,
        "search_entry": search_entry,
        "url": url
    }


def write_jekyll_page(page_data, output_path):
    """Write a Jekyll-compatible page with front matter."""
    os.makedirs(output_path.parent, exist_ok=True)

    # Build YAML front matter
    fm = page_data["front_matter"]
    yaml_lines = ["---"]
    for key, value in fm.items():
        if isinstance(value, str):
            yaml_lines.append(f'{key}: "{value}"')
        else:
            yaml_lines.append(f"{key}: {value}")
    yaml_lines.append("---")
    yaml_lines.append("")

    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(yaml_lines))
        f.write(page_data["content"])

    print(f"  Created: {output_path}")


def create_collection_index(collection_path, title, description, items):
    """Create an index page for a collection."""
    os.makedirs(collection_path, exist_ok=True)

    content = f"""---
layout: page
title: "{title}"
description: "{description}"
---

# {title}

{description}

"""

    if items:
        content += "## Contenido\n\n"
        for item in items:
            content += f"- [{item['title']}]({item['url']})\n"

    index_path = collection_path / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Created index: {index_path}")


def main():
    print("=" * 60)
    print("Pathfinder 2 Player Core - Site Builder")
    print("=" * 60)
    print(f"Source: {SOURCE_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    if not SOURCE_DIR.exists():
        print(f"ERROR: Source directory not found: {SOURCE_DIR}")
        return

    # Collect all search entries
    search_index = []

    # Process each chapter
    for chapter_key, chapter_info in CHAPTER_MAP.items():
        chapter_path = SOURCE_DIR / chapter_key
        if not chapter_path.exists():
            print(f"Skipping missing chapter: {chapter_key}")
            continue

        print(f"\nProcessing: {chapter_info['title']}")

        collection_path = OUTPUT_DIR / chapter_info["collection"]
        collection_items = []

        # Find all markdown files
        for md_file in sorted(chapter_path.rglob("*.md")):
            try:
                page_data = process_markdown_file(md_file, chapter_key, chapter_info)

                # Determine output path
                rel_path = md_file.relative_to(chapter_path)
                output_path = collection_path / rel_path

                write_jekyll_page(page_data, output_path)
                search_index.append(page_data["search_entry"])
                collection_items.append({
                    "title": page_data["front_matter"]["title"],
                    "url": page_data["url"]
                })

            except Exception as e:
                print(f"  ERROR processing {md_file}: {e}")

        # Create collection index
        if collection_items:
            create_collection_index(
                collection_path,
                chapter_info["title"],
                f"Contenido del capítulo {chapter_info['title']}",
                collection_items
            )

    # Write search index
    print(f"\nWriting search index with {len(search_index)} entries...")
    os.makedirs(SEARCH_INDEX_PATH.parent, exist_ok=True)
    with open(SEARCH_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    print(f"  Created: {SEARCH_INDEX_PATH}")

    print("\n" + "=" * 60)
    print("Build complete!")
    print(f"Total pages: {len(search_index)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
