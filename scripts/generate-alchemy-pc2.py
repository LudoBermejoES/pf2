#!/usr/bin/env python3
"""
Script para generar archivos individuales de objetos alquímicos de PC2
Lee datos de scripts/data/alchemy-pc2.json y genera archivos en docs/_equipo/alquimia/
"""

import os
import json
from pathlib import Path

# Directorio base
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "scripts" / "data" / "alchemy-pc2.json"
OUTPUT_BASE = BASE_DIR / "docs" / "_equipo"


def load_alchemy_data():
    """Carga los datos de alquimia desde el archivo JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['categories']


def generate_elixir_file(item):
    """Genera el contenido del archivo markdown para un elixir con variantes"""
    name = item['name']
    slug = item['slug']
    traits = item['traits']
    usage = item['usage']
    bulk = item['bulk']
    activate = item['activate']
    description = item['description']
    variants = item['variants']

    traits_str = ", ".join(traits)

    # Determinar niveles para frontmatter
    levels = [str(v['level']) for v in variants]
    levels_str = ", ".join(levels)

    # Generar tabla de variantes
    variants_table = "| Tipo | Nivel | Precio | Efecto |\n|------|-------|--------|--------|\n"
    for v in variants:
        variants_table += f"| {v['type']} | {v['level']} | {v['price']} | {v['effect']} |\n"

    content = f"""---
layout: page
permalink: /equipo/alquimia/elixires/{slug}/
title: {name}
chapter: Equipo
category: alquimia
subcategory: elixir
source: PC2
item_level: "{levels_str}"
---

**Rasgos:** {traits_str}

**Uso:** {usage}; **Impedimenta** {bulk}

**Activar** {activate}

---

{description}

## Variantes

{variants_table}

---

## Ver también

- [Elixires](/equipo/alquimia/elixires/)
- [Objetos alquímicos](/equipo/alquimia/)
"""
    return content


def generate_mutagen_file(item):
    """Genera el contenido del archivo markdown para un mutágeno con variantes"""
    name = item['name']
    slug = item['slug']
    traits = item['traits']
    usage = item['usage']
    bulk = item['bulk']
    activate = item['activate']
    description = item['description']
    effect_intro = item.get('effect_intro', '')
    drawback = item.get('drawback', '')
    variants = item['variants']

    traits_str = ", ".join(traits)

    # Determinar niveles para frontmatter
    levels = [str(v['level']) for v in variants]
    levels_str = ", ".join(levels)

    # Generar tabla de variantes
    variants_table = "| Tipo | Nivel | Precio | Duración | Beneficio/Inconveniente |\n|------|-------|--------|----------|-------------------------|\n"
    for v in variants:
        variants_table += f"| {v['type']} | {v['level']} | {v['price']} | {v['duration']} | {v['benefit']} |\n"

    content = f"""---
layout: page
permalink: /equipo/alquimia/mutagenos/{slug}/
title: {name}
chapter: Equipo
category: alquimia
subcategory: mutageno
source: PC2
item_level: "{levels_str}"
---

**Rasgos:** {traits_str}

**Uso:** {usage}; **Impedimenta** {bulk}

**Activar** {activate}

---

{description}

{effect_intro}

{drawback}

## Variantes

{variants_table}

---

## Ver también

- [Mutágenos](/equipo/alquimia/mutagenos/)
- [Objetos alquímicos](/equipo/alquimia/)
"""
    return content


def generate_poison_file(item):
    """Genera el contenido del archivo markdown para un veneno"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    usage = item['usage']
    bulk = item['bulk']
    activate = item['activate']
    description = item['description']
    saving_throw = item['saving_throw']
    max_duration = item['max_duration']
    stages = item['stages']
    onset = item.get('onset', None)

    traits_str = ", ".join(traits)
    onset_line = f"\n\n**Comienzo** {onset}" if onset else ""

    content = f"""---
layout: page
permalink: /equipo/alquimia/venenos/{slug}/
title: {name}
chapter: Equipo
category: alquimia
subcategory: veneno
source: PC2
item_level: "{level}"
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Uso:** {usage}; **Impedimenta** {bulk}

**Activar** {activate}

---

{description}

**Salvación** {saving_throw}{onset_line}

**Duración máxima** {max_duration}

{stages}

---

## Ver también

- [Venenos](/equipo/alquimia/venenos/)
- [Objetos alquímicos](/equipo/alquimia/)
"""
    return content


def generate_tool_file(item):
    """Genera el contenido del archivo markdown para una herramienta alquímica"""
    name = item['name']
    slug = item['slug']
    level = item['level']
    price = item['price']
    traits = item['traits']
    usage = item['usage']
    bulk = item['bulk']
    activate = item['activate']
    description = item['description']
    effect = item['effect']

    traits_str = ", ".join(traits)

    content = f"""---
layout: page
permalink: /equipo/alquimia/herramientas/{slug}/
title: {name}
chapter: Equipo
category: alquimia
subcategory: herramienta
source: PC2
item_level: "{level}"
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

**Uso:** {usage}; **Impedimenta** {bulk}

**Activar** {activate}

---

{description}

**Efecto** {effect}

---

## Ver también

- [Herramientas alquímicas](/equipo/alquimia/herramientas/)
- [Objetos alquímicos](/equipo/alquimia/)
"""
    return content


# Mapeo de categorías a funciones generadoras
GENERATORS = {
    'elixires': generate_elixir_file,
    'mutagenos': generate_mutagen_file,
    'venenos': generate_poison_file,
    'herramientas': generate_tool_file,
}


def main():
    print(f"Cargando datos desde: {DATA_FILE}")

    # Verificar que el archivo de datos existe
    if not DATA_FILE.exists():
        print(f"ERROR: No se encontró el archivo de datos: {DATA_FILE}")
        return

    # Cargar datos
    categories = load_alchemy_data()

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
            content = generator(item)

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
