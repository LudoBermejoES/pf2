#!/usr/bin/env python3

from pathlib import Path

# 8 Arquetipos multiclase PC2
MULTICLASS_ARCHETYPES = {
    "alquimista-multiclass": {
        "title": "Dedicación a Alquimista",
        "slug": "alquimista-multiclass",
        "rarity": "common",
        "related_class": "Alquimista",
        "level": "2º nivel"
    },
    "barbaro-multiclass": {
        "title": "Dedicación a Bárbaro",
        "slug": "barbaro-multiclass",
        "rarity": "common",
        "related_class": "Bárbaro",
        "level": "2º nivel"
    },
    "campeon-multiclass": {
        "title": "Dedicación a Campeón",
        "slug": "campeon-multiclass",
        "rarity": "common",
        "related_class": "Campeón",
        "level": "2º nivel"
    },
    "espadachin-multiclass": {
        "title": "Dedicación a Espadachín",
        "slug": "espadachin-multiclass",
        "rarity": "common",
        "related_class": "Espadachín",
        "level": "2º nivel"
    },
    "hechicero-multiclass": {
        "title": "Dedicación a Hechicero",
        "slug": "hechicero-multiclass",
        "rarity": "common",
        "related_class": "Hechicero",
        "level": "2º nivel"
    },
    "investigador-multiclass": {
        "title": "Dedicación a Investigador",
        "slug": "investigador-multiclass",
        "rarity": "common",
        "related_class": "Investigador",
        "level": "2º nivel"
    },
    "monje-multiclass": {
        "title": "Dedicación a Monje",
        "slug": "monje-multiclass",
        "rarity": "common",
        "related_class": "Monje",
        "level": "2º nivel"
    },
    "oraculo-multiclass": {
        "title": "Dedicación a Oráculo",
        "slug": "oraculo-multiclass",
        "rarity": "common",
        "related_class": "Oráculo",
        "level": "2º nivel"
    }
}

def create_multiclass_archetype(slug, data):
    """Crea un archivo de arquetipo multiclase."""
    content = f"""---
layout: page
permalink: /arquetipos/{slug}/
title: {data['title']}
chapter: Arquetipos
category: arquetipos
source: PC2
nav_order: 10
archetype_type: multiclass
rarity: {data['rarity']}
related_class: {data['related_class']}
min_level: {data['level']}
description: {data['title']} para dedicarse a {data['related_class']}
---

## {data['title']}

### Descripción

Este arquetipo te permite dedicarte a las habilidades y poderes del {data['related_class']}. [Descripción detallada a completar según PC2]

### Requisitos

- Eres de **{data['level']}** o superior
- No posees la capacidad de clase de {data['related_class']}

### Efectos

Al tomar este arquetipo, obtienes acceso a los dotes de {data['related_class']} como si fueras un miembro de esa clase.

[Beneficios y poderes específicos del arquetipo a documentar según PC2]

### Dotes de Dedicación Posteriores

A medida que avanzas de nivel, puedes tomar dotes de dedicación adicionales para profundizar en tus habilidades de {data['related_class']}.

[Dotes posteriores a documentar según PC2]

---

## Temas Relacionados

- [{data['related_class']} (Clase)](/clases/{data['related_class'].lower().replace(' ', '-')})
- [Arquetipos](/arquetipos/)
- [Dotes](/dotes/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    archetypes_dir = docs_dir / 'arquetipos'

    print("🎭 Generando arquetipos multiclase PC2...")
    print("=" * 60)

    stats = {'created': 0, 'errors': 0}

    for archetype_key, data in MULTICLASS_ARCHETYPES.items():
        slug = data['slug']
        title = data['title']

        try:
            archetypes_dir.mkdir(parents=True, exist_ok=True)

            # Crear archivo de arquetipo
            archetype_path = archetypes_dir / f'{slug}.md'
            content = create_multiclass_archetype(slug, data)
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
    print(f"   🎭 Arquetipos multiclase: {len(MULTICLASS_ARCHETYPES)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
