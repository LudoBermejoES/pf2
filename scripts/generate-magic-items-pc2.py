#!/usr/bin/env python3
"""
Script para generar archivos individuales de objetos mágicos de PC2
Lee datos de scripts/data/magic-items-pc2.json y genera archivos en docs/_equipo/magia/
"""

import os
import json
from pathlib import Path

# Directorio base
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "scripts" / "data" / "magic-items-pc2.json"
OUTPUT_BASE = BASE_DIR / "docs" / "_equipo"


def load_item_data():
    """Carga los datos de objetos mágicos desde el archivo JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['categories']


def generate_armor_file(item, category_info):
    """Genera el contenido del archivo markdown para una armadura mágica"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    base_type = item['base_type']
    usage = item['usage']
    bulk = item['bulk']
    description = item['description']
    activation = item['activation']
    effect = item['effect']

    traits_str = ", ".join(traits)

    content = f"""---
layout: page
permalink: /equipo/magia/armaduras/{slug}/
title: {name}
chapter: Equipo
category: equipo
source: PC2
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Tipo base:** {base_type}

**Uso:** {usage}; **Impedimenta** {bulk}

---

{description}

**Activar** {activation}

**Efecto** {effect}

---

## Ver también

- [Armaduras mágicas](/equipo/magia/armaduras/)
- [Armaduras mundanas](/equipo/armaduras/)
"""
    return content


def generate_shield_file(item, category_info):
    """Genera el contenido del archivo markdown para un escudo mágico"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    hardness = item['hardness']
    hp = item['hp']
    usage = item['usage']
    bulk = item['bulk']
    description = item['description']
    activation = item['activation']
    effect = item['effect']

    traits_str = ", ".join(traits)

    content = f"""---
layout: page
permalink: /equipo/magia/escudos/{slug}/
title: {name}
chapter: Equipo
category: equipo
source: PC2
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Dureza** {hardness}; **PG** {hp}

**Uso:** {usage}; **Impedimenta** {bulk}

---

{description}

**Activar** {activation}

**Efecto** {effect}

---

## Ver también

- [Escudos mágicos](/equipo/magia/escudos/)
- [Escudos mundanos](/equipo/escudos/)
"""
    return content


def generate_weapon_file(item, category_info):
    """Genera el contenido del archivo markdown para un arma mágica"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    base_type = item['base_type']
    usage = item['usage']
    bulk = item['bulk']
    description = item['description']
    activation = item['activation']
    effect = item['effect']

    traits_str = ", ".join(traits)

    content = f"""---
layout: page
permalink: /equipo/magia/armas/{slug}/
title: {name}
chapter: Equipo
category: equipo
source: PC2
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Tipo base:** {base_type}

**Uso:** {usage}; **Impedimenta** {bulk}

---

{description}

**Activar** {activation}

**Efecto** {effect}

---

## Ver también

- [Armas mágicas](/equipo/magia/armas/)
- [Armas mundanas](/equipo/armas/)
"""
    return content


def generate_consumable_file(item, category_info):
    """Genera el contenido del archivo markdown para un consumible mágico"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    item_type = item['item_type']
    usage = item['usage']
    bulk = item['bulk']
    description = item['description']
    activation = item['activation']
    effect = item['effect']

    traits_str = ", ".join(traits)

    content = f"""---
layout: page
permalink: /equipo/magia/consumibles/{slug}/
title: {name}
chapter: Equipo
category: equipo
source: PC2
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Tipo:** {item_type}

**Uso:** {usage}; **Impedimenta** {bulk}

---

{description}

**Activar** {activation}

**Efecto** {effect}

---

## Ver también

- [Consumibles mágicos](/equipo/magia/consumibles/)
"""
    return content


def generate_held_file(item, category_info):
    """Genera el contenido del archivo markdown para un objeto sostenido"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    usage = item['usage']
    bulk = item['bulk']
    description = item['description']
    activation = item['activation']
    effect = item['effect']

    # Charges es opcional
    charges = item.get('charges', None)

    traits_str = ", ".join(traits)

    charges_line = f"\n\n**Cargas** {charges}" if charges else ""

    content = f"""---
layout: page
permalink: /equipo/magia/sostenidos/{slug}/
title: {name}
chapter: Equipo
category: equipo
source: PC2
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Uso:** {usage}; **Impedimenta** {bulk}{charges_line}

---

{description}

**Activar** {activation}

**Efecto** {effect}

---

## Ver también

- [Objetos sostenidos](/equipo/magia/sostenidos/)
"""
    return content


def generate_worn_file(item, category_info):
    """Genera el contenido del archivo markdown para un objeto de vestir"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    slot = item['slot']
    usage = item['usage']
    bulk = item['bulk']
    description = item['description']
    activation = item['activation']
    effect = item['effect']

    traits_str = ", ".join(traits)

    content = f"""---
layout: page
permalink: /equipo/magia/vestir/{slug}/
title: {name}
chapter: Equipo
category: equipo
source: PC2
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Ranura:** {slot}

**Uso:** {usage}; **Impedimenta** {bulk}

---

{description}

**Activar** {activation}

**Efecto** {effect}

---

## Ver también

- [Objetos de vestir](/equipo/magia/vestir/)
"""
    return content


# Mapeo de categorías a funciones generadoras
GENERATORS = {
    'armaduras': generate_armor_file,
    'escudos': generate_shield_file,
    'armas': generate_weapon_file,
    'consumibles': generate_consumable_file,
    'sostenidos': generate_held_file,
    'vestir': generate_worn_file,
}


def main():
    print(f"Cargando datos desde: {DATA_FILE}")

    # Verificar que el archivo de datos existe
    if not DATA_FILE.exists():
        print(f"ERROR: No se encontró el archivo de datos: {DATA_FILE}")
        return

    # Cargar datos
    categories = load_item_data()

    total_created = 0
    total_skipped = 0

    for category_name, category_info in categories.items():
        print(f"\n{'='*50}")
        print(f"Procesando categoría: {category_name}")
        print(f"{'='*50}")

        output_dir = OUTPUT_BASE / category_info['output_dir']
        items = category_info['items']

        print(f"Directorio de salida: {output_dir}")
        print(f"Objetos a procesar: {len(items)}")

        # Crear directorio de salida si no existe
        output_dir.mkdir(parents=True, exist_ok=True)

        # Obtener la función generadora apropiada
        generator = GENERATORS.get(category_name)
        if not generator:
            print(f"  ADVERTENCIA: No hay generador para la categoría '{category_name}'")
            continue

        # Generar archivos
        created = 0
        skipped = 0

        for item in items:
            slug = item['slug']
            output_path = output_dir / f"{slug}.md"

            # Verificar si ya existe
            if output_path.exists():
                print(f"  Ya existe: {slug}.md")
                skipped += 1
                continue

            # Generar contenido
            content = generator(item, category_info)

            # Escribir archivo
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  Creado: {slug}.md")
            created += 1

        print(f"\n  Resumen de {category_name}:")
        print(f"    Creados: {created}")
        print(f"    Ya existían: {skipped}")

        total_created += created
        total_skipped += skipped

    print(f"\n{'='*50}")
    print(f"RESUMEN TOTAL:")
    print(f"  Archivos creados: {total_created}")
    print(f"  Archivos que ya existían: {total_skipped}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
