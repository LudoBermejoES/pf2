#!/usr/bin/env python3
"""
Script para extraer rasgos del glosario a ficheros individuales.
Crea ficheros MD en _rasgos/ y un índice con tabla resumen.
"""

import os
import re
from pathlib import Path
import unicodedata

# Directorios
GLOSARIO_PATH = Path("/Users/ludo/code/pf2/docs/_apendices/glosario.md")
RASGOS_DIR = Path("/Users/ludo/code/pf2/docs/_rasgos")

def slugify(text):
    """Convierte texto a slug para nombre de archivo."""
    # Normalizar caracteres unicode
    text = unicodedata.normalize('NFD', text.lower())
    # Quitar acentos
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # Reemplazar espacios por guiones
    text = re.sub(r'\s+', '-', text)
    # Quitar caracteres no alfanuméricos excepto guiones
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def extract_traits_from_glosario():
    """Extrae todos los rasgos del glosario."""
    with open(GLOSARIO_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar entradas con (rasgo)
    pattern = r'\*\*([^*]+)\*\*\s*\(rasgo(?:\s+de\s+[^)]+)?\)\s*(?:—\s*)?(.+?)(?=\n\n|\n\*\*|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)

    traits = []
    for name, description in matches:
        name = name.strip()
        description = description.strip()
        # Limpiar la descripción
        description = re.sub(r'\s+', ' ', description)
        if description:
            traits.append({
                'name': name,
                'description': description,
                'slug': slugify(name)
            })

    return traits

def categorize_trait(name, description):
    """Categoriza el rasgo según su tipo."""
    name_lower = name.lower()
    desc_lower = description.lower()

    # Categorías de rasgos
    if any(x in desc_lower for x in ['clase', 'aptitudes de la clase']):
        return 'clase'
    elif any(x in desc_lower for x in ['ascendencia', 'herencia versátil', 'miembro de la ascendencia']):
        return 'ascendencia'
    elif any(x in desc_lower for x in ['criatura', 'criaturas']):
        if any(x in name_lower for x in ['animal', 'bestia', 'dragón', 'elemental', 'gigante', 'humanoide',
                                          'muerto viviente', 'constructo', 'cieno', 'planta', 'hongo']):
            return 'criatura'
    elif any(x in desc_lower for x in ['daño', 'infligen daño']):
        return 'daño'
    elif any(x in desc_lower for x in ['tradición', 'magia procede']):
        return 'tradición'
    elif any(x in desc_lower for x in ['acción', 'actividad', 'movimiento', 'ataque', 'manipular', 'concentrar']):
        return 'acción'
    elif any(x in desc_lower for x in ['efecto', 'efectos']):
        return 'efecto'
    elif any(x in desc_lower for x in ['arma', 'rasgo de arma']):
        return 'arma'
    elif any(x in desc_lower for x in ['veneno', 'administra']):
        return 'veneno'
    elif any(x in desc_lower for x in ['conjuro', 'lanzar']):
        return 'conjuro'

    return 'general'

def create_trait_file(trait, category):
    """Crea el fichero MD para un rasgo."""
    filename = f"{trait['slug']}.md"
    filepath = RASGOS_DIR / filename

    # Capitalizar el nombre para el título
    title = trait['name'].capitalize()

    content = f"""---
layout: page
permalink: /rasgos/{trait['slug']}/
title: "{title}"
chapter: Rasgos
category: rasgos
trait_type: {category}
source: PC1
---

{trait['description']}
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filename

def create_index_file(traits_by_category):
    """Crea el fichero índice con tabla resumen."""
    index_path = RASGOS_DIR / "index.md"

    # Ordenar categorías
    category_names = {
        'acción': 'Rasgos de Acción',
        'ascendencia': 'Rasgos de Ascendencia',
        'clase': 'Rasgos de Clase',
        'conjuro': 'Rasgos de Conjuro',
        'criatura': 'Rasgos de Criatura',
        'daño': 'Rasgos de Daño',
        'efecto': 'Rasgos de Efecto',
        'tradición': 'Rasgos de Tradición',
        'arma': 'Rasgos de Arma',
        'veneno': 'Rasgos de Veneno',
        'general': 'Otros Rasgos'
    }

    content = """---
layout: page
permalink: /rasgos/
title: Rasgos
chapter: Rasgos
category: rasgos
nav_order: 1
source: PC1
---

Los rasgos son etiquetas que describen propiedades específicas de reglas, criaturas, objetos y aptitudes. Cada rasgo tiene un significado mecánico que afecta cómo funciona algo en el juego.

"""

    # Crear secciones por categoría
    category_order = ['acción', 'daño', 'tradición', 'efecto', 'conjuro', 'clase', 'ascendencia', 'criatura', 'arma', 'veneno', 'general']

    for category in category_order:
        if category not in traits_by_category:
            continue

        traits = traits_by_category[category]
        section_name = category_names.get(category, category.capitalize())

        content += f"## {section_name}\n\n"
        content += "| Rasgo | Descripción |\n"
        content += "|-------|-------------|\n"

        for trait in sorted(traits, key=lambda x: x['name']):
            # Truncar descripción para la tabla
            desc = trait['description']
            if len(desc) > 100:
                desc = desc[:97] + "..."
            # Escapar pipes en la descripción
            desc = desc.replace('|', '\\|')
            content += f"| [{trait['name'].capitalize()}](/rasgos/{trait['slug']}/) | {desc} |\n"

        content += "\n"

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("Extrayendo rasgos del glosario")
    print("=" * 50)

    # Crear directorio si no existe
    RASGOS_DIR.mkdir(parents=True, exist_ok=True)

    # Extraer rasgos
    traits = extract_traits_from_glosario()
    print(f"Encontrados {len(traits)} rasgos")

    # Categorizar y crear ficheros
    traits_by_category = {}
    created = 0

    for trait in traits:
        category = categorize_trait(trait['name'], trait['description'])

        if category not in traits_by_category:
            traits_by_category[category] = []
        traits_by_category[category].append(trait)

        create_trait_file(trait, category)
        created += 1
        print(f"  ✓ {trait['name']}")

    # Crear índice
    create_index_file(traits_by_category)
    print(f"\n✓ Creado índice en {RASGOS_DIR / 'index.md'}")

    print("\n" + "=" * 50)
    print(f"✓ Creados {created} ficheros de rasgos")

    # Mostrar resumen por categoría
    print("\nResumen por categoría:")
    for cat, traits_list in sorted(traits_by_category.items()):
        print(f"  {cat}: {len(traits_list)}")

if __name__ == "__main__":
    main()
