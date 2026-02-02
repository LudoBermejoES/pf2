#!/usr/bin/env python3
"""
Script para generar archivos individuales de conjuros de PC2
basados en el formato existente en docs/_conjuros/spell-individual/
"""

import os
import re
from pathlib import Path

# Directorio base
BASE_DIR = Path("/Users/ludo/code/pf2")
OUTPUT_DIR = BASE_DIR / "docs" / "_conjuros" / "spell-individual"

# Mapeo de tradiciones a nombres completos
TRADICIONES_MAP = {
    "arcana": "arcana",
    "divina": "divina",
    "oculta": "ocultista",
    "primigenia": "primigenia"
}

def slugify(name):
    """Convierte un nombre a slug para URLs"""
    slug = name.lower()
    # Reemplazar caracteres especiales
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ü': 'u', 'ñ': 'n', ' ': '-', '·': '', '◆': '', '◇': '',
        '/': '-', "'": '', '"': '', ',': '', '.': ''
    }
    for old, new in replacements.items():
        slug = slug.replace(old, new)
    # Limpiar guiones múltiples
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug

def extract_spell_level(header):
    """Extrae el nivel del conjuro del encabezado"""
    # Buscar patrones como "Truco 1", "Conjuro 2", etc.
    truco_match = re.search(r'Truco\s*(\d+)?', header, re.IGNORECASE)
    if truco_match:
        return "TRUCO"

    conjuro_match = re.search(r'Conjuro\s*(\d+)', header, re.IGNORECASE)
    if conjuro_match:
        return conjuro_match.group(1)

    return "1"

def extract_actions(header):
    """Extrae los símbolos de acción del encabezado"""
    actions = ""
    if "◆◆◆" in header:
        actions = "◆◆◆"
    elif "◆◆" in header:
        actions = "◆◆"
    elif "◆" in header:
        actions = "◆"
    elif "◇" in header:
        actions = "◇"
    return actions

def parse_spell(text):
    """Parsea el texto de un conjuro y retorna sus componentes"""
    lines = text.strip().split('\n')
    if not lines:
        return None

    # Primera línea: nombre y acciones
    header = lines[0].replace('## ', '')

    # Extraer nombre (antes del ·)
    name_match = re.match(r'^([^·]+)', header)
    if not name_match:
        return None

    name = name_match.group(1).strip()
    actions = extract_actions(header)
    level = extract_spell_level(header)

    # Procesar el resto del contenido
    content_lines = []
    rasgos = []
    tradiciones = []

    i = 1
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith('**Rasgos:**'):
            rasgos_text = line.replace('**Rasgos:**', '').strip()
            rasgos = [r.strip() for r in rasgos_text.split(',')]
        elif line.startswith('**Tradiciones:**'):
            trad_text = line.replace('**Tradiciones:**', '').strip()
            tradiciones = [t.strip() for t in trad_text.split(',')]
        else:
            content_lines.append(lines[i])
        i += 1

    # Reconstruir contenido
    content = '\n'.join(content_lines).strip()

    return {
        'name': name,
        'actions': actions,
        'level': level,
        'rasgos': rasgos,
        'tradiciones': tradiciones,
        'content': content
    }

def generate_spell_file(spell):
    """Genera el contenido del archivo markdown para un conjuro"""
    name = spell['name']
    slug = slugify(name)
    level = spell['level']
    actions = spell['actions']
    rasgos = spell['rasgos']
    tradiciones = spell['tradiciones']
    content = spell['content']

    # Formatear tradiciones
    trad_formatted = []
    for t in tradiciones:
        t_lower = t.lower()
        if t_lower in TRADICIONES_MAP:
            trad_formatted.append(TRADICIONES_MAP[t_lower])
        else:
            trad_formatted.append(t_lower)

    tradiciones_str = ", ".join(trad_formatted) if trad_formatted else ""

    # Construir encabezado del conjuro
    if level == "TRUCO":
        level_display = "TRUCO 1"
    else:
        level_display = level

    action_str = f" {actions}" if actions else ""

    # Generar rasgos HTML
    trait_tags = ""
    if rasgos:
        trait_tags = '<div class="spell-traits-wrapper" markdown="0">\n'
        for rasgo in rasgos:
            trait_tags += f'<span class="trait-tag">{rasgo}</span>\n'
        trait_tags += '</div>\n'

    # Separar metadatos del contenido principal
    meta_lines = []
    main_content_lines = []
    in_meta = True

    for line in content.split('\n'):
        stripped = line.strip()
        # Los metadatos son líneas que empiezan con ** o están vacías al inicio
        if in_meta:
            if stripped.startswith('**') or stripped == '':
                meta_lines.append(line)
            else:
                in_meta = False
                main_content_lines.append(line)
        else:
            main_content_lines.append(line)

    meta_section = '\n'.join(meta_lines).strip()
    main_content = '\n'.join(main_content_lines).strip()

    # Construir el archivo según el formato de luz.md
    output = f"""---
layout: spell
permalink: /conjuros/{slug}/
title: {name}
chapter: Conjuros
spell_level: {level}
source: PC2
---
## {name}{action_str} [{level_display}]

**Tradiciones:** {tradiciones_str}
{meta_section}

{trait_tags}
---

{main_content}
"""

    return output, slug

def parse_spell_file(filepath):
    """Lee un archivo de conjuros y extrae todos los conjuros individuales"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividir por ## que marca cada conjuro
    spell_blocks = re.split(r'\n(?=## )', content)

    spells = []
    for block in spell_blocks:
        if block.strip().startswith('## ') and not block.strip().startswith('# '):
            spell = parse_spell(block)
            if spell and spell['tradiciones']:  # Solo conjuros con tradiciones
                spells.append(spell)

    return spells

def main():
    # Archivos fuente
    source_files = [
        BASE_DIR / "original" / "player_core_2_es" / "05-hechizos" / "conjuros" / "a-c.md",
        BASE_DIR / "original" / "player_core_2_es" / "05-hechizos" / "conjuros" / "d-f.md",
        BASE_DIR / "original" / "player_core_2_es" / "05-hechizos" / "conjuros" / "g-p.md",
        BASE_DIR / "original" / "player_core_2_es" / "05-hechizos" / "conjuros" / "r-s.md",
        BASE_DIR / "original" / "player_core_2_es" / "05-hechizos" / "conjuros" / "t-w.md",
    ]

    all_spells = []
    for source_file in source_files:
        print(f"Procesando: {source_file.name}")
        spells = parse_spell_file(source_file)
        all_spells.extend(spells)
        print(f"  Encontrados: {len(spells)} conjuros")

    print(f"\nTotal de conjuros: {len(all_spells)}")

    # Crear directorio de salida si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generar archivos
    created = 0
    for spell in all_spells:
        content, slug = generate_spell_file(spell)
        output_path = OUTPUT_DIR / f"{slug}.md"

        # Verificar si ya existe
        if output_path.exists():
            print(f"  Ya existe: {slug}.md")
            continue

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Creado: {slug}.md")
        created += 1

    print(f"\nArchivos creados: {created}")
    print(f"Archivos que ya existían: {len(all_spells) - created}")

if __name__ == "__main__":
    main()
