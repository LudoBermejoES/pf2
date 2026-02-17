#!/usr/bin/env python3
"""
Parser de dotes de Pathfinder 2e
Extrae información de archivos markdown de dotes y genera JSON estructurado
"""

import os
import re
import json
import yaml
from pathlib import Path


def slugify(text):
    """Convierte texto a slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def extract_frontmatter(content):
    """Extrae el frontmatter YAML del contenido"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return {}
    return {}


def extract_traits(content):
    """Extrae los rasgos del div feat-traits-header"""
    traits = []

    # Buscar div con enlaces a rasgos
    div_match = re.search(
        r'<div class="feat-traits-header"[^>]*>(.*?)</div>',
        content,
        re.DOTALL
    )

    if div_match:
        div_content = div_match.group(1)
        # Extraer todos los rasgos de los enlaces
        trait_matches = re.findall(
            r'<a href="[^"]*" class="feat-trait">([^<]+)</a>',
            div_content
        )
        traits.extend(trait_matches)

    return traits


def extract_action_type(content):
    """Extrae el tipo de acción del include de Liquid"""
    # Buscar en el título o en línea separada
    match = re.search(r'\{%\s*include\s+accion\.html\s+tipo="([^"]+)"\s*%\}', content)
    if match:
        return match.group(1)
    return None


def extract_special_sections(content):
    """Extrae secciones especiales (Prerequisites, Requirements, etc.)"""
    sections = {}

    # Lista de campos a buscar (con y sin dos puntos)
    fields = [
        'Prerrequisitos?',
        'Requisitos',
        'Desencadenante',
        'Detonante',  # Variante histórica
        'Frecuencia',
        'Coste?',
        'Efecto',
        'Beneficio',
        'Especial'
    ]

    for field in fields:
        # Intentar con dos puntos
        pattern1 = rf'\*\*({field}):\*\*\s*(.+?)(?=\n\n|\*\*[A-Z]|$)'
        match = re.search(pattern1, content, re.DOTALL | re.MULTILINE)

        if not match:
            # Intentar sin dos puntos
            pattern2 = rf'\*\*({field})\*\*\s+(.+?)(?=\n\n|\*\*[A-Z]|$)'
            match = re.search(pattern2, content, re.DOTALL | re.MULTILINE)

        if match:
            field_name = match.group(1).lower()
            # Normalizar nombres de campos
            if 'prerrequisito' in field_name:
                field_name = 'prerequisites'
            elif 'requisito' in field_name:
                field_name = 'requirements'
            elif 'desencadenante' in field_name or 'detonante' in field_name:
                field_name = 'trigger'
            elif 'frecuencia' in field_name:
                field_name = 'frequency'
            elif 'coste' in field_name or 'costo' in field_name:
                field_name = 'cost'
            elif 'efecto' in field_name:
                field_name = 'effect'
            elif 'beneficio' in field_name:
                field_name = 'benefit'
            elif 'especial' in field_name:
                field_name = 'special'

            sections[field_name] = match.group(2).strip()

    return sections


def extract_results(content):
    """Extrae los resultados de éxito/fallo"""
    results = {}

    result_types = [
        ('critical_success', r'\*\*Exito critico\*\*\s*(.+?)(?=\n\n|\*\*[A-Z]|$)'),
        ('success', r'\*\*Exito\*\*\s*(.+?)(?=\n\n|\*\*[A-Z]|$)'),
        ('failure', r'\*\*Fallo\*\*\s*(.+?)(?=\n\n|\*\*[A-Z]|$)'),
        ('critical_failure', r'\*\*Fallo critico\*\*\s*(.+?)(?=\n\n|\*\*[A-Z]|$)')
    ]

    for result_name, pattern in result_types:
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        if match:
            results[result_name] = match.group(1).strip()

    return results if results else None


def extract_description(content, frontmatter):
    """Extrae la descripción principal de la dote"""
    # Buscar después del div de rasgos y campos especiales
    # Tomar el primer párrafo sustancial

    # Primero, remover el frontmatter
    content_no_fm = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Remover el título
    content_no_title = re.sub(r'^##\s+.+?\n', '', content_no_fm, flags=re.MULTILINE)

    # Remover el div de rasgos
    content_no_traits = re.sub(
        r'<div class="feat-traits-header"[^>]*>.*?</div>',
        '',
        content_no_title,
        flags=re.DOTALL
    )

    # Remover campos especiales conocidos
    special_fields = [
        r'\*\*Prerrequisitos?:?\*\*[^\n]+',
        r'\*\*Requisitos:?\*\*[^\n]+',
        r'\*\*Desencadenante:?\*\*[^\n]+',
        r'\*\*Detonante:?\*\*[^\n]+',
        r'\*\*Frecuencia:?\*\*[^\n]+',
        r'\*\*Coste?:?\*\*[^\n]+',
    ]

    for pattern in special_fields:
        content_no_traits = re.sub(pattern, '', content_no_traits)

    # Buscar el primer párrafo sustancial
    lines = content_no_traits.strip().split('\n')
    description_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            if description_lines:  # Si ya tenemos contenido, parar en línea vacía
                break
            continue
        if line.startswith('**'):  # Parar en siguiente campo especial
            break
        if line.startswith('---'):  # Parar en separador
            break
        description_lines.append(line)

    description = ' '.join(description_lines).strip()

    # Limpiar markdown
    description = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', description)  # Links
    description = re.sub(r'\(pág\. \d+\)', '', description)  # Páginas

    return description


def parse_feat_file(file_path):
    """Parsea un archivo de dote y extrae toda la información"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extraer frontmatter
        frontmatter = extract_frontmatter(content)

        if not frontmatter:
            return None

        # Extraer información
        feat_data = {
            'id': slugify(frontmatter.get('title', '')),
            'name': frontmatter.get('title', ''),
            'level': frontmatter.get('level', 0),
            'traits': extract_traits(content),
            'action_type': extract_action_type(content),
            'source_file': str(file_path)
        }

        # Agregar categoría
        if 'clase' in frontmatter:
            feat_data['category'] = 'class'
            feat_data['class'] = frontmatter['clase']
        elif 'ascendencia' in frontmatter:
            feat_data['category'] = 'ancestry'
            feat_data['ancestry'] = frontmatter['ascendencia']
        elif 'archetype' in frontmatter:
            feat_data['category'] = 'archetype'
            feat_data['archetype'] = frontmatter['archetype']
            feat_data['archetype_type'] = frontmatter.get('archetype_type', 'other')
        elif 'habilidad' in frontmatter:
            feat_data['category'] = 'skill'
        else:
            feat_data['category'] = 'general'

        # Extraer secciones especiales
        special_sections = extract_special_sections(content)
        feat_data.update(special_sections)

        # Extraer resultados
        results = extract_results(content)
        if results:
            feat_data['results'] = results

        # Extraer descripción
        feat_data['description'] = extract_description(content, frontmatter)

        return feat_data

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def parse_all_feats(base_dir='../../docs/_dotes'):
    """Parsea todos los archivos de dotes"""
    feats = []
    errors = []

    base_path = Path(__file__).parent / base_dir

    print(f"🔍 Buscando archivos de dotes en {base_path}...\n")

    # Buscar todos los archivos .md recursivamente
    feat_files = list(base_path.rglob('*.md'))

    print(f"📋 Encontrados {len(feat_files)} archivos markdown\n")

    for i, feat_file in enumerate(feat_files, 1):
        if i % 100 == 0:
            print(f"  Procesando {i}/{len(feat_files)}...")

        feat_data = parse_feat_file(feat_file)

        if feat_data:
            feats.append(feat_data)
        else:
            errors.append(str(feat_file))

    print(f"\n✅ Parseadas {len(feats)} dotes exitosamente")

    if errors:
        print(f"⚠️  {len(errors)} archivos con errores")

    return feats, errors


def save_to_json(feats, output_file='data/feats.json'):
    """Guarda las dotes en un archivo JSON"""
    output_path = Path(__file__).parent / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        'feats': feats,
        'total': len(feats)
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Datos guardados en {output_path}")

    # Estadísticas
    categories = {}
    for feat in feats:
        cat = feat.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print("\n📊 Estadísticas por categoría:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")


if __name__ == '__main__':
    print("=" * 60)
    print("Parser de Dotes de Pathfinder 2e")
    print("=" * 60)
    print()

    feats, errors = parse_all_feats()

    if feats:
        save_to_json(feats)

    print("\n" + "=" * 60)
    print("✨ Parseo completado")
    print("=" * 60)
