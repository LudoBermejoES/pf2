#!/usr/bin/env python3

import os
from pathlib import Path
import json

# Datos de ascendencias PC2 a crear
ANCESTRIES = {
    "catfolk": {
        "title": "Catfolk",
        "slug": "catfolk",
        "rarity": "common",
        "boosts": ["Destreza", "Inteligencia", "Sabiduría"],
        "flaws": ["Fuerza"],
        "hp": 8,
        "speed": 25,
        "languages": ["Común", "Felino"],
        "traits": ["Humanoides", "Catfolk"]
    },
    "hobgoblin": {
        "title": "Hobgoblin",
        "slug": "hobgoblin",
        "rarity": "common",
        "boosts": ["Constitución", "Inteligencia", "Carisma"],
        "flaws": ["Sabiduría"],
        "hp": 10,
        "speed": 25,
        "languages": ["Común", "Goblin"],
        "traits": ["Humanoides", "Goblin"]
    },
    "kholo": {
        "title": "Kholo",
        "slug": "kholo",
        "rarity": "common",
        "boosts": ["Fuerza", "Constitución", "Sabiduría"],
        "flaws": ["Inteligencia"],
        "hp": 10,
        "speed": 25,
        "languages": ["Común", "Kholo"],
        "traits": ["Humanoides", "Kholo"]
    },
    "kobold": {
        "title": "Kobold",
        "slug": "kobold",
        "rarity": "common",
        "boosts": ["Destreza", "Carisma", "Constitución"],
        "flaws": ["Sabiduría"],
        "hp": 6,
        "speed": 25,
        "languages": ["Común", "Dracónico"],
        "traits": ["Humanoides", "Kobold"]
    },
    "lizardfolk": {
        "title": "Lizardfolk",
        "slug": "lizardfolk",
        "rarity": "common",
        "boosts": ["Fuerza", "Sabiduría", "Destreza"],
        "flaws": ["Inteligencia"],
        "hp": 10,
        "speed": 25,
        "languages": ["Común", "Reptiliano"],
        "traits": ["Humanoides", "Reptiliano"]
    },
    "ratfolk": {
        "title": "Ratfolk",
        "slug": "ratfolk",
        "rarity": "common",
        "boosts": ["Destreza", "Inteligencia", "Carisma"],
        "flaws": ["Fuerza"],
        "hp": 6,
        "speed": 25,
        "languages": ["Común", "Roedor"],
        "traits": ["Humanoides", "Ratfolk"]
    },
    "tengu": {
        "title": "Tengu",
        "slug": "tengu",
        "rarity": "common",
        "boosts": ["Destreza", "Sabiduría", "Carisma"],
        "flaws": ["Constitución"],
        "hp": 8,
        "speed": 25,
        "languages": ["Común", "Tengu"],
        "traits": ["Humanoides", "Tengu"]
    },
    "tripkee": {
        "title": "Tripkee",
        "slug": "tripkee",
        "rarity": "uncommon",
        "boosts": ["Sabiduría", "Carisma", "Constitución"],
        "flaws": ["Inteligencia"],
        "hp": 8,
        "speed": 30,
        "languages": ["Común", "Tripkee"],
        "traits": ["Humanoides", "Tripkee"]
    }
}

def create_ancestry_index(slug, data, nav_order):
    """Crea el archivo index de ascendencia."""
    boosts_str = ", ".join(data["boosts"])
    flaws_str = data["flaws"][0] if data["flaws"] else "Ninguna"
    languages_str = ", ".join(data["languages"])
    traits_str = ", ".join(data["traits"])

    content = f"""---
layout: page
permalink: /ascendencias/{slug}/
title: {data['title']}
chapter: Ascendencias
category: ascendencias
source: PC2
nav_order: {nav_order}
ancestry: {data['title']}
rarity: {data['rarity']}
description: Los {data['title'].lower()} son una raza versátil y única de Golarion.
---

## Descripción

Los **{data['title']}** son una ascendencia distinta con su propia cultura, historia y capacidades. [Descripción general de la ascendencia a completar desde el PDF de Player Core 2]

### Características Generales

- **Ajuste de Puntos de Atributo**: +2 {data['boosts'][0]}, +2 {data['boosts'][1]}, +2 {data['boosts'][2]}
- **Penalidad de Atributo**: -{data['flaws'][0] if data['flaws'] else 'N/A'}
- **Puntos de Golpe**: {data['hp']}
- **Velocidad**: {data['speed']} pies
- **Idiomas**: {languages_str}
- **Rasgos**: {traits_str}

## Herencias

Las herencias de {data['title']} definen características adicionales y especializaciones.

→ [Ver Herencias de {data['title']}](/ascendencias/{slug}/herencias/)

## Dotes de Ascendencia

Los {data['title']} tienen acceso a dotes únicos de ascendencia.

→ [Ver Dotes de Ascendencia](/ascendencias/{slug}/dotes/)

---

## Temas Relacionados

- [Herencias de {data['title']}](/ascendencias/{slug}/herencias/)
- [Dotes de Ascendencia](/ascendencias/{slug}/dotes/)
- [Todas las Ascendencias](/ascendencias/)
- [Herencias Versatiles](/ascendencias/herencias-versatiles/)
"""

    return content

def create_ancestry_heritages(slug, title, nav_order):
    """Crea el archivo de herencias de ascendencia."""
    content = f"""---
layout: page
permalink: /ascendencias/{slug}/herencias/
title: Herencias de {title}
chapter: Ascendencias
category: ascendencias
source: PC2
nav_order: {nav_order}
ancestry: {title}
description: Las herencias de {title} representan variaciones especiales dentro de la ascendencia.
---

## Herencias de {title}

Las herencias permiten especificar variaciones dentro de la ascendencia de {title}. Selecciona una herencia al crear tu personaje.

### Descripción de Herencias

[Las herencias específicas del {title} serán documentadas aquí según el PDF de Player Core 2]

---

## Temas Relacionados

- [{title} - Página Principal](/ascendencias/{slug}/)
- [Dotes de Ascendencia](/ascendencias/{slug}/dotes/)
- [Todas las Ascendencias](/ascendencias/)
"""

    return content

def create_ancestry_feats(slug, title, nav_order):
    """Crea el archivo de dotes de ascendencia."""
    content = f"""---
layout: page
permalink: /ascendencias/{slug}/dotes/
title: Dotes de Ascendencia de {title}
chapter: Ascendencias
category: ascendencias
source: PC2
nav_order: {nav_order}
ancestry: {title}
description: Dotes de ascendencia únicos para {title}.
---

## Dotes de Ascendencia de {title}

Los {title} tienen acceso a los siguientes dotes de ascendencia:

### Dotes de 1.er Nivel

[Dotes de 1er nivel para {title} a documentar según PC2]

### Dotes de 5.º Nivel

[Dotes de 5º nivel para {title} a documentar según PC2]

### Dotes de 9.º Nivel

[Dotes de 9º nivel para {title} a documentar según PC2]

---

## Temas Relacionados

- [{title} - Página Principal](/ascendencias/{slug}/)
- [Herencias de {title}](/ascendencias/{slug}/herencias/)
- [Todas las Ascendencias](/ascendencias/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    ancestries_dir = docs_dir / 'ascendencias'

    print("🧬 Generando archivos de ascendencias PC2...")
    print("=" * 60)

    nav_order = 100
    stats = {'created': 0, 'errors': 0}

    for ancestry_key, data in ANCESTRIES.items():
        slug = data['slug']
        title = data['title']

        # Crear directorio para ascendencia
        ancestry_folder = ancestries_dir / slug
        ancestry_folder.mkdir(parents=True, exist_ok=True)

        try:
            # 1. Archivo index
            index_path = ancestry_folder / 'index.md'
            index_content = create_ancestry_index(slug, data, nav_order)
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"✅ {slug}/index.md")
            stats['created'] += 1

            # 2. Archivo de herencias
            herencias_path = ancestry_folder / 'herencias.md'
            herencias_content = create_ancestry_heritages(slug, title, nav_order + 1)
            with open(herencias_path, 'w', encoding='utf-8') as f:
                f.write(herencias_content)
            print(f"✅ {slug}/herencias.md")
            stats['created'] += 1

            # 3. Archivo de dotes
            dotes_path = ancestry_folder / 'dotes.md'
            dotes_content = create_ancestry_feats(slug, title, nav_order + 2)
            with open(dotes_path, 'w', encoding='utf-8') as f:
                f.write(dotes_content)
            print(f"✅ {slug}/dotes.md")
            stats['created'] += 1

            nav_order += 10

        except Exception as e:
            print(f"❌ Error en {slug}: {e}")
            stats['errors'] += 1

    print("")
    print("=" * 60)
    print(f"✨ Generación completada:")
    print(f"   ✅ Archivos creados: {stats['created']}")
    print(f"   ❌ Errores: {stats['errors']}")
    print(f"   📊 Ascendencias: {len(ANCESTRIES)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
