#!/usr/bin/env python3
"""
Script para regenerar archivos PC2 usando el contenido REAL de /original/player_core_2_es/
"""

import os
from pathlib import Path
import re

# Rutas base
SOURCE_DIR = Path('/Users/ludo/code/pf2/original/player_core_2_es')
DOCS_DIR = Path('/Users/ludo/code/pf2/docs')

# Ascendencias PC2
ANCESTRIES = ['catfolk', 'hobgoblin', 'kholo', 'kobold', 'lizardfolk', 'ratfolk', 'tengu', 'tripkee']

# Clases PC2
CLASSES = ['alquimista', 'barbaro', 'campeon', 'espadachin', 'hechicero', 'investigador', 'monje', 'oraculo']

def get_title_from_content(content):
    """Extrae el título del contenido markdown."""
    match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1) if match else "Sin título"

def create_frontmatter(layout, permalink, title, chapter, category, source="PC2", nav_order=100, extra=None):
    """Crea el frontmatter YAML."""
    fm = f"""---
layout: {layout}
permalink: {permalink}
title: {title}
chapter: {chapter}
category: {category}
source: {source}
nav_order: {nav_order}
"""
    if extra:
        for key, value in extra.items():
            fm += f"{key}: {value}\n"
    fm += "---\n\n"
    return fm

def process_ancestries():
    """Procesa todas las ascendencias PC2."""
    print("\n🧬 PROCESANDO ASCENDENCIAS PC2")
    print("=" * 60)

    source_base = SOURCE_DIR / '01-ascendencias'
    dest_base = DOCS_DIR / '_ascendencias'

    nav_order = 100
    stats = {'created': 0, 'errors': 0}

    for ancestry in ANCESTRIES:
        source_dir = source_base / ancestry
        dest_dir = dest_base / ancestry

        if not source_dir.exists():
            print(f"❌ No existe: {source_dir}")
            stats['errors'] += 1
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)

        # Procesar descripcion.md -> index.md
        desc_file = source_dir / 'descripcion.md'
        if desc_file.exists():
            content = desc_file.read_text(encoding='utf-8')
            title = get_title_from_content(content)

            frontmatter = create_frontmatter(
                layout='page',
                permalink=f'/ascendencias/{ancestry}/',
                title=title,
                chapter='Ascendencias',
                category='ascendencias',
                nav_order=nav_order,
                extra={'ancestry': title, 'rarity': 'uncommon'}
            )

            output = frontmatter + content
            (dest_dir / 'index.md').write_text(output, encoding='utf-8')
            print(f"✅ {ancestry}/index.md")
            stats['created'] += 1

        # Procesar herencias.md
        her_file = source_dir / 'herencias.md'
        if her_file.exists():
            content = her_file.read_text(encoding='utf-8')
            title = get_title_from_content(content) or f"Herencias de {ancestry.title()}"

            frontmatter = create_frontmatter(
                layout='page',
                permalink=f'/ascendencias/{ancestry}/herencias/',
                title=title,
                chapter='Ascendencias',
                category='ascendencias',
                nav_order=nav_order + 1,
                extra={'ancestry': ancestry.title()}
            )

            output = frontmatter + content
            (dest_dir / 'herencias.md').write_text(output, encoding='utf-8')
            print(f"✅ {ancestry}/herencias.md")
            stats['created'] += 1

        # Procesar dotes.md
        dotes_file = source_dir / 'dotes.md'
        if dotes_file.exists():
            content = dotes_file.read_text(encoding='utf-8')
            title = get_title_from_content(content) or f"Dotes de {ancestry.title()}"

            frontmatter = create_frontmatter(
                layout='page',
                permalink=f'/ascendencias/{ancestry}/dotes/',
                title=title,
                chapter='Ascendencias',
                category='ascendencias',
                nav_order=nav_order + 2,
                extra={'ancestry': ancestry.title()}
            )

            output = frontmatter + content
            (dest_dir / 'dotes.md').write_text(output, encoding='utf-8')
            print(f"✅ {ancestry}/dotes.md")
            stats['created'] += 1

        nav_order += 10

    print(f"\n📊 Ascendencias: {stats['created']} creados, {stats['errors']} errores")
    return stats

def process_classes():
    """Procesa todas las clases PC2."""
    print("\n📚 PROCESANDO CLASES PC2")
    print("=" * 60)

    source_base = SOURCE_DIR / '02-clases'
    dest_base = DOCS_DIR / '_clases'

    nav_order = 100
    stats = {'created': 0, 'errors': 0}

    for class_name in CLASSES:
        source_dir = source_base / class_name
        dest_dir = dest_base / class_name

        if not source_dir.exists():
            print(f"❌ No existe: {source_dir}")
            stats['errors'] += 1
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)

        # Procesar descripcion.md -> index.md
        desc_file = source_dir / 'descripcion.md'
        if desc_file.exists():
            content = desc_file.read_text(encoding='utf-8')
            title = get_title_from_content(content)

            frontmatter = create_frontmatter(
                layout='class',
                permalink=f'/clases/{class_name}/',
                title=title,
                chapter='Clases',
                category='clases',
                nav_order=nav_order,
                extra={'class_name': title}
            )

            output = frontmatter + content
            (dest_dir / 'index.md').write_text(output, encoding='utf-8')
            print(f"✅ {class_name}/index.md")
            stats['created'] += 1

        # Procesar dotes.md si existe
        dotes_file = source_dir / 'dotes.md'
        if dotes_file.exists():
            content = dotes_file.read_text(encoding='utf-8')
            title = get_title_from_content(content) or f"Dotes de {class_name.title()}"

            frontmatter = create_frontmatter(
                layout='page',
                permalink=f'/clases/{class_name}/dotes/',
                title=title,
                chapter='Clases',
                category='clases',
                nav_order=nav_order + 1,
                extra={'class_name': class_name.title()}
            )

            output = frontmatter + content
            (dest_dir / 'dotes.md').write_text(output, encoding='utf-8')
            print(f"✅ {class_name}/dotes.md")
            stats['created'] += 1

        nav_order += 10

    print(f"\n📊 Clases: {stats['created']} creados, {stats['errors']} errores")
    return stats

def process_versatile_heritages():
    """Procesa herencias versátiles PC2."""
    print("\n🌟 PROCESANDO HERENCIAS VERSÁTILES PC2")
    print("=" * 60)

    source_dir = SOURCE_DIR / '01-ascendencias' / 'herencias-versatiles'
    dest_dir = DOCS_DIR / '_ascendencias' / 'herencias-versatiles'

    stats = {'created': 0, 'errors': 0}

    if not source_dir.exists():
        print(f"❌ No existe: {source_dir}")
        return stats

    nav_order = 200

    for md_file in source_dir.glob('*.md'):
        if md_file.name == 'index.md':
            continue

        content = md_file.read_text(encoding='utf-8')
        title = get_title_from_content(content)
        slug = md_file.stem

        frontmatter = create_frontmatter(
            layout='page',
            permalink=f'/ascendencias/herencias-versatiles/{slug}/',
            title=title,
            chapter='Ascendencias',
            category='ascendencias',
            nav_order=nav_order
        )

        output = frontmatter + content
        (dest_dir / md_file.name).write_text(output, encoding='utf-8')
        print(f"✅ herencias-versatiles/{md_file.name}")
        stats['created'] += 1
        nav_order += 1

    print(f"\n📊 Herencias Versátiles: {stats['created']} creados")
    return stats

def process_archetypes():
    """Procesa arquetipos PC2."""
    print("\n⚔️ PROCESANDO ARQUETIPOS PC2")
    print("=" * 60)

    # Arquetipos otros (archivo grande)
    otros_file = SOURCE_DIR / '03-arquetipos' / 'otros' / 'arquetipos-otros.md'
    dest_dir = DOCS_DIR / '_clases' / 'arquetipos' / 'pc2'

    stats = {'created': 0, 'errors': 0}

    if not otros_file.exists():
        print(f"❌ No existe: {otros_file}")
        return stats

    dest_dir.mkdir(parents=True, exist_ok=True)

    content = otros_file.read_text(encoding='utf-8')

    # Dividir por arquetipos (cada uno empieza con ## Nombre)
    archetype_sections = re.split(r'\n(?=## [A-ZÁÉÍÓÚ])', content)

    nav_order = 300

    for section in archetype_sections:
        if not section.strip() or section.startswith('# Otros'):
            continue

        # Extraer nombre del arquetipo
        match = re.match(r'^## (.+)$', section, re.MULTILINE)
        if not match:
            continue

        title = match.group(1).strip()
        slug = title.lower()
        slug = re.sub(r'[áàäâ]', 'a', slug)
        slug = re.sub(r'[éèëê]', 'e', slug)
        slug = re.sub(r'[íìïî]', 'i', slug)
        slug = re.sub(r'[óòöô]', 'o', slug)
        slug = re.sub(r'[úùüû]', 'u', slug)
        slug = re.sub(r'[ñ]', 'n', slug)
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')

        frontmatter = create_frontmatter(
            layout='page',
            permalink=f'/clases/arquetipos/otros/{slug}/',
            title=title,
            chapter='Clases',
            category='clases',
            nav_order=nav_order,
            extra={'archetype_type': 'other'}
        )

        output = frontmatter + section
        output_file = dest_dir / f'{slug}.md'
        output_file.write_text(output, encoding='utf-8')
        print(f"✅ arquetipos/pc2/{slug}.md")
        stats['created'] += 1
        nav_order += 1

    print(f"\n📊 Arquetipos: {stats['created']} creados")
    return stats

def process_multiclass_archetypes():
    """Procesa arquetipos multiclase PC2."""
    print("\n🔄 PROCESANDO ARQUETIPOS MULTICLASE PC2")
    print("=" * 60)

    source_dir = SOURCE_DIR / '03-arquetipos' / 'multiclase'
    dest_dir = DOCS_DIR / '_clases' / 'arquetipos' / 'multiclase'

    stats = {'created': 0, 'errors': 0}

    if not source_dir.exists():
        print(f"❌ No existe: {source_dir}")
        return stats

    nav_order = 400

    for md_file in source_dir.glob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        title = get_title_from_content(content)
        slug = md_file.stem

        frontmatter = create_frontmatter(
            layout='page',
            permalink=f'/clases/arquetipos/multiclase/{slug}/',
            title=f'Arquetipo de {title} Multiclase',
            chapter='Clases',
            category='clases',
            nav_order=nav_order,
            extra={'archetype_type': 'multiclass'}
        )

        output = frontmatter + content
        (dest_dir / md_file.name).write_text(output, encoding='utf-8')
        print(f"✅ multiclase/{md_file.name}")
        stats['created'] += 1
        nav_order += 1

    print(f"\n📊 Multiclase: {stats['created']} creados")
    return stats

def main():
    print("=" * 60)
    print("🔄 REGENERANDO ARCHIVOS PC2 DESDE CONTENIDO REAL")
    print("=" * 60)
    print(f"📂 Fuente: {SOURCE_DIR}")
    print(f"📂 Destino: {DOCS_DIR}")

    total_stats = {'created': 0, 'errors': 0}

    # Procesar cada categoría
    stats = process_ancestries()
    total_stats['created'] += stats['created']
    total_stats['errors'] += stats['errors']

    stats = process_classes()
    total_stats['created'] += stats['created']
    total_stats['errors'] += stats['errors']

    stats = process_versatile_heritages()
    total_stats['created'] += stats['created']
    total_stats['errors'] += stats.get('errors', 0)

    stats = process_archetypes()
    total_stats['created'] += stats['created']
    total_stats['errors'] += stats.get('errors', 0)

    stats = process_multiclass_archetypes()
    total_stats['created'] += stats['created']
    total_stats['errors'] += stats.get('errors', 0)

    print("\n" + "=" * 60)
    print("✨ RESUMEN FINAL")
    print("=" * 60)
    print(f"✅ Total archivos creados: {total_stats['created']}")
    print(f"❌ Total errores: {total_stats['errors']}")
    print("=" * 60)

if __name__ == '__main__':
    main()
