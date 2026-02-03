#!/usr/bin/env python3
"""
Script para enriquecer los archivos individuales de armas con datos de las tablas de armas.md.
Añade: Precio, Daño, Impedimenta, Manos, Grupo, Rasgos, y para armas a distancia: Rango, Recarga.
"""

import os
import re
from pathlib import Path

ARMAS_DIR = Path("/Users/ludo/code/pf2/docs/_equipo/armas")
ARMAS_MD = Path("/Users/ludo/code/pf2/docs/_equipo/armas.md")

# Mapa de slugs de rasgos para crear los enlaces
RASGOS_SLUGS = {
    "a dos manos": "a-dos-manos",
    "ágil": "agil",
    "alcance": "alcance",
    "arrojadiza": "arrojadiza",
    "arrojadizo": "arrojadiza",
    "barrido": "barrido",
    "derribo": "derribo",
    "desarme": "desarme",
    "desarmar": "desarme",
    "empujar": "empujon",
    "empujón": "empujon",
    "fatal": "fatal",
    "fijada": "fijada",
    "fijadas al escudo": "fijada",
    "fijado al escudo": "fijada",
    "gemela": "gemela",
    "de justa": "justa-de",
    "letal": "letal",
    "mano libre": "mano-libre",
    "monje": "monje",
    "no letal": "no-letal",
    "ocultable": "ocultable",
    "parada": "parada",
    "presa": "presa",
    "propulsión": "propulsion-de",
    "propulsivo": "propulsion-de",
    "puñalada trapera": "punalada-trapera",
    "revés": "reves",
    "salpicadura": "salpicadura",
    "sin armas": "sin-armas",
    "sutil": "sutil",
    "versátil": "versatil",
    "vigorosa": "vigorosa",
    "volea": "volea",
    # Rasgos de ascendencia
    "enano": "enano",
    "elfo": "elfo",
    "gnomo": "gnomo",
    "goblin": "goblin",
    "mediano": "mediano",
    "orco": "orco",
    "hobgoblin": "hobgoblin",
    "tengu": "tengu",
    "kobold": "kobold",
    "tripkee": "tripkee",
    "amurrun": "amurrun",
    "kholo": "kholo",
    # Rasgos nuevos PC2
    "entorpecedor": "entorpecedor",
    "modular": "modular",
    "arrasador": "arrasador",
    "atado": "atado",
    "fuerte": "fuerte",
    "preciso": "preciso",
    "traicionero": "traicionero",
    "agarrar": "presa",
    "derribo a distancia": "derribo-a-distancia",
    # Poco común
    "poco común": "poco-comun",
}

def parse_weapons_from_md():
    """Parsea armas.md y extrae los datos de cada arma."""
    with open(ARMAS_MD, 'r', encoding='utf-8') as f:
        content = f.read()

    weapons = {}
    current_category = None
    current_type = None  # "melee" o "ranged"
    is_uncommon = False
    is_advanced = False

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Detectar categoría
        if line.startswith('## Ataques sin armas'):
            current_category = "Ataque sin armas"
            current_type = "melee"
            is_uncommon = False
            is_advanced = False
        elif line.startswith('## Armas cuerpo a cuerpo sencillas'):
            current_category = "Arma cuerpo a cuerpo sencilla"
            current_type = "melee"
            is_uncommon = False
            is_advanced = False
        elif line.startswith('### Armas sencillas poco comunes'):
            current_category = "Arma cuerpo a cuerpo sencilla"
            current_type = "melee"
            is_uncommon = True
            is_advanced = False
        elif line.startswith('## Armas cuerpo a cuerpo marciales'):
            current_category = "Arma cuerpo a cuerpo marcial"
            current_type = "melee"
            is_uncommon = False
            is_advanced = False
        elif line.startswith('### Armas marciales poco comunes'):
            current_category = "Arma cuerpo a cuerpo marcial"
            current_type = "melee"
            is_uncommon = True
            is_advanced = False
        elif line.startswith('## Armas cuerpo a cuerpo avanzadas'):
            current_category = "Arma cuerpo a cuerpo avanzada"
            current_type = "melee"
            is_uncommon = True  # Las avanzadas son poco comunes
            is_advanced = True
        elif line.startswith('## Armas a distancia sencillas'):
            current_category = "Arma a distancia sencilla"
            current_type = "ranged"
            is_uncommon = False
            is_advanced = False
        elif line.startswith('## Armas a distancia marciales'):
            current_category = "Arma a distancia marcial"
            current_type = "ranged"
            is_uncommon = False
            is_advanced = False
        elif line.startswith('### Armas marciales a distancia poco comunes'):
            current_category = "Arma a distancia marcial"
            current_type = "ranged"
            is_uncommon = True
            is_advanced = False
        elif line.startswith('### Armas a distancia avanzadas'):
            current_category = "Arma a distancia avanzada"
            current_type = "ranged"
            is_uncommon = True
            is_advanced = True

        # Parsear líneas de tabla
        if line.startswith('| [') and current_category:
            # Extraer nombre y enlace
            match = re.match(r'\| \[([^\]]+)\]\(([^)]+)\)', line)
            if match:
                name = match.group(1)
                link = match.group(2)
                slug = link.rstrip('/').split('/')[-1]

                # Parsear columnas
                cols = [c.strip() for c in line.split('|')[1:-1]]

                if current_type == "melee":
                    # | Arma | Precio | Daño | Imp. | Manos | Grupo | Rasgos |
                    if len(cols) >= 7:
                        weapons[slug] = {
                            'nombre': name,
                            'categoria': current_category,
                            'tipo': current_type,
                            'precio': cols[1],
                            'dano': cols[2],
                            'impedimenta': cols[3],
                            'manos': cols[4],
                            'grupo': cols[5],
                            'rasgos': cols[6],
                            'poco_comun': is_uncommon,
                            'avanzada': is_advanced,
                        }
                elif current_type == "ranged":
                    # | Arma | Precio | Daño | R. dist. | Recarga | Imp. | Manos | Grupo | Rasgos |
                    if len(cols) >= 9:
                        weapons[slug] = {
                            'nombre': name,
                            'categoria': current_category,
                            'tipo': current_type,
                            'precio': cols[1],
                            'dano': cols[2],
                            'rango': cols[3],
                            'recarga': cols[4],
                            'impedimenta': cols[5],
                            'manos': cols[6],
                            'grupo': cols[7],
                            'rasgos': cols[8],
                            'poco_comun': is_uncommon,
                            'avanzada': is_advanced,
                        }

    return weapons

def parse_trait(trait_text):
    """Convierte un texto de rasgo a su slug y formato de enlace."""
    trait_text = trait_text.strip()
    if not trait_text or trait_text == '—':
        return None

    # Manejar rasgos con valores (ej: "A dos manos d8", "Fatal d12", "Arrojadiza 20 pies")
    trait_lower = trait_text.lower()

    # Buscar coincidencia exacta primero
    for key, slug in RASGOS_SLUGS.items():
        if trait_lower == key:
            return (slug, trait_text)

    # Buscar coincidencia parcial (para rasgos con valores)
    for key, slug in RASGOS_SLUGS.items():
        if trait_lower.startswith(key):
            return (slug, trait_text)

    # Si no encontramos, intentar slug directo
    slug = trait_text.lower().replace(' ', '-').replace(',', '')
    # Limpiar caracteres especiales
    slug = re.sub(r'[áà]', 'a', slug)
    slug = re.sub(r'[éè]', 'e', slug)
    slug = re.sub(r'[íì]', 'i', slug)
    slug = re.sub(r'[óò]', 'o', slug)
    slug = re.sub(r'[úù]', 'u', slug)
    slug = re.sub(r'[ñ]', 'n', slug)
    slug = re.sub(r'\s*d\d+.*', '', slug)  # Quitar valores de dado
    slug = re.sub(r'\s*\d+\s*pies.*', '', slug)  # Quitar distancias
    slug = slug.strip('-')

    return (slug, trait_text)

def format_traits_html(rasgos_text, poco_comun=False):
    """Convierte texto de rasgos a HTML con enlaces."""
    if not rasgos_text or rasgos_text.strip() == '—':
        traits = []
    else:
        # Separar por comas
        traits = [t.strip() for t in rasgos_text.split(',')]

    # Añadir poco común si corresponde
    if poco_comun:
        traits.insert(0, "Poco común")

    if not traits:
        return ""

    html_parts = []
    for trait in traits:
        parsed = parse_trait(trait)
        if parsed:
            slug, display = parsed
            html_parts.append(f'<a href="/apendices/rasgos/{slug}/" class="feat-trait">{display}</a>')

    if html_parts:
        return '<div class="feat-traits-header" markdown="0">' + ''.join(html_parts) + '</div>'
    return ""

def enrich_weapon_file(filepath, weapon_data):
    """Enriquece un archivo de arma con los datos mecánicos."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar frontmatter del contenido
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2].strip()

    # Verificar si ya tiene datos (evitar duplicar)
    if '**Precio**' in body or '**Daño**' in body:
        return False

    # Construir nuevo contenido
    new_body_parts = []

    # Línea de precio
    precio = weapon_data.get('precio', '—')
    if precio and precio != '—':
        new_body_parts.append(f"**Precio** {precio}")
    else:
        new_body_parts.append("**Precio** —")

    new_body_parts.append("")

    # Rasgos en HTML
    traits_html = format_traits_html(
        weapon_data.get('rasgos', ''),
        weapon_data.get('poco_comun', False)
    )
    if traits_html:
        new_body_parts.append(traits_html)
        new_body_parts.append("")

    new_body_parts.append("---")
    new_body_parts.append("")

    # Datos mecánicos
    stats = []

    dano = weapon_data.get('dano', '—')
    if dano and dano != '—':
        stats.append(f"**Daño** {dano}")

    if weapon_data.get('tipo') == 'ranged':
        rango = weapon_data.get('rango', '—')
        if rango and rango != '—':
            stats.append(f"**Rango** {rango}")

        recarga = weapon_data.get('recarga', '—')
        if recarga and recarga != '—':
            stats.append(f"**Recarga** {recarga}")

    manos = weapon_data.get('manos', '—')
    if manos and manos != '—':
        stats.append(f"**Manos** {manos}")

    impedimenta = weapon_data.get('impedimenta', '—')
    if impedimenta and impedimenta != '—':
        stats.append(f"**Impedimenta** {impedimenta}")

    grupo = weapon_data.get('grupo', '—')
    if grupo and grupo != '—':
        stats.append(f"**Grupo** {grupo}")

    categoria = weapon_data.get('categoria', '')
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
    new_body_parts.append("- [Lista de armas](/equipo/armas/)")

    new_content = f"---{frontmatter}---\n\n" + "\n".join(new_body_parts) + "\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    # Parsear datos de armas.md
    print("Parseando armas.md...")
    weapons = parse_weapons_from_md()
    print(f"Encontradas {len(weapons)} armas en las tablas")

    # Listar archivos de armas
    weapon_files = list(ARMAS_DIR.glob("*.md"))
    print(f"Encontrados {len(weapon_files)} archivos de armas")

    enriched = 0
    not_found = []
    already_enriched = []

    for filepath in weapon_files:
        slug = filepath.stem

        # Saltar archivos especiales
        if slug in ['index', 'bala-honda', 'dardo-cerbatana', 'flecha', 'virote', 'bomba-alquimica']:
            continue

        if slug in weapons:
            if enrich_weapon_file(filepath, weapons[slug]):
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
        print(f"\nArmas sin datos en tablas:")
        for slug in sorted(not_found):
            print(f"  - {slug}")

if __name__ == "__main__":
    main()
