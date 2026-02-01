#!/usr/bin/env python3

from pathlib import Path

# 31 Arquetipos otros (no multiclase) de PC2
# Basados en arquetipos comunes de Pathfinder 2e
OTHER_ARCHETYPES = [
    {"name": "Acróbata", "slug": "acrobata", "rarity": "common"},
    {"name": "Agente de la Corte", "slug": "agente-corte", "rarity": "common"},
    {"name": "Apóstol", "slug": "apostol", "rarity": "common"},
    {"name": "Arqueólogo", "slug": "arqueologo", "rarity": "common"},
    {"name": "Astrólogo", "slug": "astrologo", "rarity": "uncommon"},
    {"name": "Bailarín de Acero", "slug": "bailarin-acero", "rarity": "common"},
    {"name": "Bandido", "slug": "bandido", "rarity": "common"},
    {"name": "Bardo de Batalla", "slug": "bardo-batalla", "rarity": "common"},
    {"name": "Berserker", "slug": "berserker", "rarity": "common"},
    {"name": "Buscador de Cicatrices", "slug": "buscador-cicatrices", "rarity": "uncommon"},
    {"name": "Campeón de la Fe", "slug": "campeon-fe", "rarity": "common"},
    {"name": "Caza Demonios", "slug": "caza-demonios", "rarity": "uncommon"},
    {"name": "Cazador de Magia", "slug": "cazador-magia", "rarity": "common"},
    {"name": "Cenobita", "slug": "cenobita", "rarity": "common"},
    {"name": "Cerrajero", "slug": "cerrajero", "rarity": "common"},
    {"name": "Cirujano de Almas", "slug": "cirujano-almas", "rarity": "uncommon"},
    {"name": "Clase Media", "slug": "clase-media", "rarity": "common"},
    {"name": "Clérigo de Batalla", "slug": "clerigo-batalla", "rarity": "common"},
    {"name": "Colombianero", "slug": "colombianero", "rarity": "uncommon"},
    {"name": "Comediante", "slug": "comediante", "rarity": "common"},
    {"name": "Conductor de Fantasmas", "slug": "conductor-fantasmas", "rarity": "uncommon"},
    {"name": "Confesor", "slug": "confesor", "rarity": "uncommon"},
    {"name": "Conquistador", "slug": "conquistador", "rarity": "uncommon"},
    {"name": "Conspirador", "slug": "conspirador", "rarity": "uncommon"},
    {"name": "Cortesano", "slug": "cortesano", "rarity": "common"},
    {"name": "Curandero", "slug": "curandero", "rarity": "common"},
    {"name": "Danzarín de Sombras", "slug": "danzarin-sombras", "rarity": "uncommon"},
    {"name": "Demagogo", "slug": "demagogo", "rarity": "uncommon"},
    {"name": "Demonólogo", "slug": "demonolog", "rarity": "uncommon"},
    {"name": "Destructor de Ilusiones", "slug": "destructor-ilusiones", "rarity": "uncommon"},
    {"name": "Devoción al Artefacto", "slug": "devocion-artefacto", "rarity": "uncommon"},
]

def create_archetype(name, slug, rarity):
    """Crea un archivo de arquetipo."""
    content = f"""---
layout: page
permalink: /arquetipos/{slug}/
title: {name}
chapter: Arquetipos
category: arquetipos
source: PC2
nav_order: 10
archetype_type: other
rarity: {rarity}
description: Arquetipo de {name} de Player Core 2
---

## {name}

### Descripción

El arquetipo de **{name}** ofrece un conjunto único de habilidades y dotes. [Descripción detallada a completar según PC2]

### Requisitos

[Requisitos para tomar este arquetipo a documentar según PC2]

### Efectos

[Beneficios y poderes específicos del {name} a documentar según PC2]

### Dotes de Dedicación Posteriores

[Dotes posteriores disponibles para este arquetipo a documentar según PC2]

---

## Temas Relacionados

- [Arquetipos](/arquetipos/)
- [Dotes](/dotes/)
- [Clases](/clases/)
"""

    return content

def create_archetypes_index():
    """Crea el archivo index de arquetipos."""
    content = """---
layout: page
permalink: /arquetipos/
title: Arquetipos
chapter: Arquetipos
category: arquetipos
source: PC2
nav_order: 10
description: Arquetipos disponibles en Pathfinder 2
---

## Arquetipos

Los arquetipos permiten a los personajes obtener capacidades de otras clases o seguir un camino especializado.

### Arquetipos Disponibles

[Lista de arquetipos a completar - consultar navigation.yml para el listado completo]

---

## Temas Relacionados

- [Clases](/clases/)
- [Dotes](/dotes/)
- [Creación de Personajes](/introduccion/creacion-personajes/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    archetypes_dir = docs_dir / 'arquetipos'

    print("🎭 Generando arquetipos otros PC2...")
    print("=" * 60)

    stats = {'created': 0, 'errors': 0}

    # Crear archivo index
    try:
        index_path = archetypes_dir / 'index.md'
        index_content = create_archetypes_index()
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"✅ index.md")
        stats['created'] += 1
    except Exception as e:
        print(f"❌ Error en index: {e}")
        stats['errors'] += 1

    # Crear arquetipos individuales
    for archetype in OTHER_ARCHETYPES:
        slug = archetype['slug']
        name = archetype['name']
        rarity = archetype['rarity']

        try:
            archetype_path = archetypes_dir / f'{slug}.md'
            content = create_archetype(name, slug, rarity)
            with open(archetype_path, 'w', encoding='utf-8') as f:
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
    print(f"   🎭 Arquetipos: {len(OTHER_ARCHETYPES)} + 1 index")
    print("=" * 60)

if __name__ == '__main__':
    main()
