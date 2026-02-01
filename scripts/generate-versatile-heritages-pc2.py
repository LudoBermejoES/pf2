#!/usr/bin/env python3

from pathlib import Path

# Herencias versatiles PC2
VERSATILE_HERITAGES = {
    "dhampir": {
        "title": "Dhampir",
        "slug": "dhampir",
        "rarity": "uncommon",
        "ancestry_compatibility": "Todas",
        "description": "Los dhampir tienen sangre vampírica pero no son vampiros completos."
    },
    "sangre-de-dragon": {
        "title": "Sangre de Dragón",
        "slug": "sangre-de-dragon",
        "rarity": "uncommon",
        "ancestry_compatibility": "Todas",
        "description": "Tienes sangre dracónica en tu linaje."
    },
    "caminante-del-ocaso": {
        "title": "Caminante del Ocaso",
        "slug": "caminante-del-ocaso",
        "rarity": "uncommon",
        "ancestry_compatibility": "Todas",
        "description": "Eres una criatura del crepúsculo, existiendo entre dos mundos."
    }
}

def create_versatile_heritage(slug, data):
    """Crea un archivo de herencia versatile."""
    content = f"""---
layout: page
permalink: /ascendencias/herencias-versatiles/{slug}/
title: {data['title']}
chapter: Ascendencias
category: ascendencias
source: PC2
nav_order: 10
heritage_type: versatile
rarity: {data['rarity']}
ancestry_compatibility: {data['ancestry_compatibility']}
description: {data['description']}
---

## {data['title']}

### Descripción

{data['description']} [Descripción detallada a completar según PC2]

### Requisitos

- Puedes tener esta herencia si eres miembro de cualquier ascendencia

### Efectos

[Efectos específicos de la herencia a documentar según PC2]

---

## Temas Relacionados

- [Herencias Versatiles](/ascendencias/herencias-versatiles/)
- [Todas las Ascendencias](/ascendencias/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    heritages_dir = docs_dir / 'ascendencias' / 'herencias-versatiles'

    print("👑 Generando herencias versatiles PC2...")
    print("=" * 60)

    stats = {'created': 0, 'errors': 0}

    for heritage_key, data in VERSATILE_HERITAGES.items():
        slug = data['slug']
        title = data['title']

        try:
            heritages_dir.mkdir(parents=True, exist_ok=True)

            # Crear archivo de herencia
            heritage_path = heritages_dir / f'{slug}.md'
            content = create_versatile_heritage(slug, data)
            with open(heritage_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {slug}.md")
            stats['created'] += 1

        except Exception as e:
            print(f"❌ Error en {slug}: {e}")
            stats['errors'] += 1

    print("")
    print("=" * 60)
    print(f"✨ Generación completada:")
    print(f"   ✅ Archivos creados: {stats['created']}")
    print(f"   ❌ Errores: {stats['errors']}")
    print(f"   👑 Herencias versatiles: {len(VERSATILE_HERITAGES)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
