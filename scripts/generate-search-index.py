#!/usr/bin/env python3
"""
Script para generar el índice de búsqueda para la web de Pathfinder 2.
Lee todos los archivos markdown de las colecciones y genera un JSON indexable.
"""

import os
import re
import json
import glob
import yaml
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent.parent / "docs"

# Colecciones a indexar con su categoría
COLLECTIONS = {
    "_introduccion": "introduccion",
    "_ambientacion": "ambientacion",
    "_ascendencias": "ascendencias",
    "_clases": "clases",
    "_habilidades": "habilidades",
    "_dotes": "dotes",
    "_equipo": "equipo",
    "_conjuros": "conjuros",
    "_reglas": "reglas",
    "_apendices": "apendices",
}

# Patrones para limpiar el contenido
FRONTMATTER_PATTERN = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)
LIQUID_PATTERN = re.compile(r'\{[%{].*?[%}]\}', re.DOTALL)
HTML_PATTERN = re.compile(r'<[^>]+>')
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\([^)]+\)')
HEADING_PATTERN = re.compile(r'^#+\s*', re.MULTILINE)
MULTIPLE_SPACES = re.compile(r'\s+')
MULTIPLE_NEWLINES = re.compile(r'\n{3,}')


def extract_frontmatter(content):
    """Extrae el frontmatter YAML de un archivo markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return {}
    return {}


def clean_content(content):
    """Limpia el contenido markdown para el índice."""
    # Eliminar frontmatter
    content = FRONTMATTER_PATTERN.sub('', content)
    # Eliminar etiquetas Liquid
    content = LIQUID_PATTERN.sub('', content)
    # Eliminar HTML
    content = HTML_PATTERN.sub(' ', content)
    # Convertir links a solo texto
    content = LINK_PATTERN.sub(r'\1', content)
    # Eliminar marcadores de encabezado
    content = HEADING_PATTERN.sub('', content)
    # Normalizar espacios
    content = MULTIPLE_SPACES.sub(' ', content)
    content = MULTIPLE_NEWLINES.sub('\n\n', content)
    # Eliminar caracteres especiales problemáticos
    content = content.replace('|', ' ').replace('*', '').replace('_', ' ')

    return content.strip()


def extract_tags(content, title, category):
    """Extrae tags relevantes del contenido."""
    tags = [category]

    # Palabras clave por categoría
    keyword_patterns = {
        'clases': ['prerrequisitos', 'nivel', 'rasgo', 'aptitud'],
        'conjuros': ['rango', 'tradicion', 'componentes', 'duracion', 'alcance'],
        'dotes': ['prerrequisitos', 'nivel', 'rasgo', 'beneficio'],
        'equipo': ['precio', 'peso', 'dano', 'alcance'],
        'habilidades': ['accion', 'reaccion', 'actividad'],
    }

    content_lower = content.lower()

    # Agregar tags de atributos si se mencionan
    atributos = ['fuerza', 'destreza', 'constitucion', 'inteligencia', 'sabiduria', 'carisma']
    for attr in atributos:
        if attr in content_lower:
            tags.append(attr)

    # Agregar tags específicos de categoría
    if category in keyword_patterns:
        for keyword in keyword_patterns[category]:
            if keyword in content_lower:
                tags.append(keyword)

    # Limitar a 10 tags únicos
    return list(set(tags))[:10]


def get_url_from_path(file_path, collection_dir, category):
    """Genera la URL a partir del path del archivo."""
    rel_path = file_path.relative_to(BASE_DIR / collection_dir)

    # Convertir path a URL
    url_parts = list(rel_path.parts)

    # Si es index.md, usar el directorio padre
    if url_parts[-1] == 'index.md':
        url_parts = url_parts[:-1]
        if not url_parts:
            return f"/{category}/"
        return f"/{category}/{'/'.join(url_parts)}/"

    # Eliminar extensión .md
    url_parts[-1] = url_parts[-1].replace('.md', '')

    return f"/{category}/{'/'.join(url_parts)}/"


def process_file(file_path, collection_dir, category):
    """Procesa un archivo markdown y devuelve su entrada de índice."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return None

    # Extraer frontmatter
    fm = extract_frontmatter(content)

    # Obtener título
    title = fm.get('title', '')
    if not title:
        # Intentar extraer del primer H1
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1)
        else:
            title = file_path.stem.replace('-', ' ').title()

    # Limpiar contenido
    clean = clean_content(content)

    # Truncar contenido a 2000 caracteres para el índice
    if len(clean) > 2000:
        clean = clean[:2000]

    # Obtener URL
    url = fm.get('permalink', get_url_from_path(file_path, collection_dir, category))

    # Extraer tags
    tags = extract_tags(clean, title, category)

    # Agregar tags del frontmatter si existen
    if 'tags' in fm and isinstance(fm['tags'], list):
        tags.extend(fm['tags'])
        tags = list(set(tags))[:10]

    return {
        'title': title,
        'url': url,
        'category': category,
        'content': clean,
        'tags': tags
    }


def main():
    """Función principal que genera el índice."""
    index = []

    for collection_dir, category in COLLECTIONS.items():
        collection_path = BASE_DIR / collection_dir

        if not collection_path.exists():
            print(f"Colección no encontrada: {collection_dir}")
            continue

        # Buscar todos los archivos .md en la colección
        md_files = list(collection_path.rglob('*.md'))
        print(f"Procesando {len(md_files)} archivos en {collection_dir}...")

        for md_file in md_files:
            entry = process_file(md_file, collection_dir, category)
            if entry and entry['title']:
                index.append(entry)

    # Ordenar por categoría y título
    index.sort(key=lambda x: (x['category'], x['title']))

    # Guardar índice
    output_path = BASE_DIR / 'assets' / 'js' / 'search-index.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"\nÍndice generado: {output_path}")
    print(f"Total de documentos: {len(index)}")

    # Estadísticas por categoría
    stats = {}
    for entry in index:
        cat = entry['category']
        stats[cat] = stats.get(cat, 0) + 1

    print("\nDocumentos por categoría:")
    for cat, count in sorted(stats.items()):
        print(f"  {cat}: {count}")


if __name__ == '__main__':
    main()
