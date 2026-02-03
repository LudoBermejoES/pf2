#!/usr/bin/env python3
"""
Script para enriquecer los archivos individuales de armaduras con datos de las tablas de armaduras.md.
Añade: Precio, Bon. CA, Tope Des., Pen. pruebas, Pen. Velocidad, Fuerza, Impedimenta, Grupo, Rasgos, Categoría.
"""

import os
import re
from pathlib import Path

ARMADURAS_DIR = Path("/Users/ludo/code/pf2/docs/_equipo/armaduras")
ARMADURAS_MD = Path("/Users/ludo/code/pf2/docs/_equipo/armaduras.md")

# Mapa de slugs de rasgos
RASGOS_SLUGS = {
    "baluarte": "baluarte",
    "comoda": "comoda",
    "cómoda": "comoda",
    "flexible": "flexible",
    "ruidosa": "ruidosa",
    "poco común": "poco-comun",
}

def parse_armors_from_md():
    """Parsea armaduras.md y extrae los datos de cada armadura."""
    with open(ARMADURAS_MD, 'r', encoding='utf-8') as f:
        content = f.read()

    armors = {}
    current_category = None

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Detectar categoría
        if line.startswith('### Defensa sin Armadura'):
            current_category = "Sin armadura"
        elif line.startswith('### Armadura Ligera'):
            current_category = "Armadura ligera"
        elif line.startswith('### Armadura Intermedia'):
            current_category = "Armadura intermedia"
        elif line.startswith('### Armadura Pesada'):
            current_category = "Armadura pesada"

        # Parsear líneas de tabla con enlaces
        if line.startswith('| [') and current_category:
            # Extraer nombre y enlace
            match = re.match(r'\| \[([^\]]+)\]\(([^)]+)\)', line)
            if match:
                name = match.group(1)
                link = match.group(2)
                slug = link.rstrip('/').split('/')[-1]

                # Parsear columnas
                cols = [c.strip() for c in line.split('|')[1:-1]]

                if current_category == "Sin armadura":
                    # | Sin armadura | Precio | Bon. CA | Tope Des. | Pen. pruebas | Pen. Velocidad | Imp. | Grupo | Rasgos |
                    if len(cols) >= 8:
                        armors[slug] = {
                            'nombre': name,
                            'categoria': current_category,
                            'precio': cols[1],
                            'bon_ca': cols[2],
                            'tope_des': cols[3],
                            'pen_pruebas': cols[4],
                            'pen_velocidad': cols[5],
                            'fuerza': '—',
                            'impedimenta': cols[6],
                            'grupo': cols[7],
                            'rasgos': cols[8] if len(cols) > 8 else '—',
                        }
                else:
                    # | Armadura | Precio | Bon. CA | Tope Des. | Pen. pruebas | Pen. Velocidad | Fuerza | Imp. | Grupo | Rasgos |
                    if len(cols) >= 10:
                        armors[slug] = {
                            'nombre': name,
                            'categoria': current_category,
                            'precio': cols[1],
                            'bon_ca': cols[2],
                            'tope_des': cols[3],
                            'pen_pruebas': cols[4],
                            'pen_velocidad': cols[5],
                            'fuerza': cols[6],
                            'impedimenta': cols[7],
                            'grupo': cols[8],
                            'rasgos': cols[9] if len(cols) > 9 else '—',
                        }

    return armors

def format_traits_html(rasgos_text):
    """Convierte texto de rasgos a HTML con enlaces."""
    if not rasgos_text or rasgos_text.strip() == '—':
        return ""

    traits = [t.strip() for t in rasgos_text.split(',')]

    html_parts = []
    for trait in traits:
        trait_lower = trait.lower()
        if trait_lower in RASGOS_SLUGS:
            slug = RASGOS_SLUGS[trait_lower]
            html_parts.append(f'<a href="/apendices/rasgos/{slug}/" class="feat-trait">{trait}</a>')

    if html_parts:
        return '<div class="feat-traits-header" markdown="0">' + ''.join(html_parts) + '</div>'
    return ""

def enrich_armor_file(filepath, armor_data):
    """Enriquece un archivo de armadura con los datos mecánicos."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar frontmatter del contenido
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2].strip()

    # Verificar si ya tiene datos (evitar duplicar)
    if '**Precio**' in body or '**Bon. CA**' in body:
        return False

    # Construir nuevo contenido
    new_body_parts = []

    # Línea de precio
    precio = armor_data.get('precio', '—')
    new_body_parts.append(f"**Precio** {precio}")
    new_body_parts.append("")

    # Rasgos en HTML
    traits_html = format_traits_html(armor_data.get('rasgos', ''))
    if traits_html:
        new_body_parts.append(traits_html)
        new_body_parts.append("")

    new_body_parts.append("---")
    new_body_parts.append("")

    # Datos mecánicos
    stats = []

    bon_ca = armor_data.get('bon_ca', '—')
    if bon_ca and bon_ca != '—':
        stats.append(f"**Bon. CA** {bon_ca}")

    tope_des = armor_data.get('tope_des', '—')
    if tope_des and tope_des != '—':
        stats.append(f"**Tope Des.** {tope_des}")

    pen_pruebas = armor_data.get('pen_pruebas', '—')
    if pen_pruebas and pen_pruebas != '—':
        stats.append(f"**Pen. pruebas** {pen_pruebas}")

    pen_velocidad = armor_data.get('pen_velocidad', '—')
    if pen_velocidad and pen_velocidad != '—':
        stats.append(f"**Pen. Velocidad** {pen_velocidad}")

    fuerza = armor_data.get('fuerza', '—')
    if fuerza and fuerza != '—':
        stats.append(f"**Fuerza** {fuerza}")

    impedimenta = armor_data.get('impedimenta', '—')
    if impedimenta and impedimenta != '—':
        stats.append(f"**Impedimenta** {impedimenta}")

    grupo = armor_data.get('grupo', '—')
    if grupo and grupo != '—':
        stats.append(f"**Grupo** {grupo}")

    categoria = armor_data.get('categoria', '')
    if categoria:
        stats.append(f"**Categoría** {categoria}")

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
    new_body_parts.append("- [Lista de armaduras](/equipo/armaduras/)")

    new_content = f"---{frontmatter}---\n\n" + "\n".join(new_body_parts) + "\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    # Parsear datos de armaduras.md
    print("Parseando armaduras.md...")
    armors = parse_armors_from_md()
    print(f"Encontradas {len(armors)} armaduras en las tablas")
    for slug in armors:
        print(f"  - {slug}")

    # Listar archivos de armaduras
    armor_files = list(ARMADURAS_DIR.glob("*.md"))
    print(f"\nEncontrados {len(armor_files)} archivos de armaduras")

    enriched = 0
    not_found = []
    already_enriched = []

    for filepath in armor_files:
        slug = filepath.stem

        # Saltar archivos especiales
        if slug in ['index']:
            continue

        if slug in armors:
            if enrich_armor_file(filepath, armors[slug]):
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
        print(f"\nArmaduras sin datos en tablas:")
        for slug in sorted(not_found):
            print(f"  - {slug}")

if __name__ == "__main__":
    main()
