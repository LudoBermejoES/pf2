#!/usr/bin/env python3

from pathlib import Path

# 9 Clases nuevas de PC2
CLASSES = {
    "alquimista": {
        "title": "Alquimista",
        "slug": "alquimista",
        "rarity": "common",
        "key_ability": "Inteligencia",
        "hit_points": 8,
        "archetype": "Alquimista"
    },
    "barbaro": {
        "title": "Bárbaro",
        "slug": "barbaro",
        "rarity": "common",
        "key_ability": "Fuerza",
        "hit_points": 12,
        "archetype": "Bárbaro"
    },
    "campeon": {
        "title": "Campeón",
        "slug": "campeon",
        "rarity": "common",
        "key_ability": "Fuerza o Carisma",
        "hit_points": 10,
        "archetype": "Campeón"
    },
    "espadachin": {
        "title": "Espadachín",
        "slug": "espadachin",
        "rarity": "common",
        "key_ability": "Destreza",
        "hit_points": 10,
        "archetype": "Espadachín"
    },
    "hechicero": {
        "title": "Hechicero",
        "slug": "hechicero",
        "rarity": "common",
        "key_ability": "Carisma",
        "hit_points": 6,
        "archetype": "Hechicero"
    },
    "investigador": {
        "title": "Investigador",
        "slug": "investigador",
        "rarity": "common",
        "key_ability": "Inteligencia",
        "hit_points": 8,
        "archetype": "Investigador"
    },
    "monje": {
        "title": "Monje",
        "slug": "monje",
        "rarity": "common",
        "key_ability": "Sabiduría",
        "hit_points": 10,
        "archetype": "Monje"
    },
    "oraculo": {
        "title": "Oráculo",
        "slug": "oraculo",
        "rarity": "common",
        "key_ability": "Carisma",
        "hit_points": 8,
        "archetype": "Oráculo"
    }
}

def create_class_index(slug, data, nav_order):
    """Crea el archivo index de clase."""
    content = f"""---
layout: class
permalink: /clases/{slug}/
title: {data['title']}
chapter: Clases
category: clases
source: PC2
nav_order: {nav_order}
class_name: {data['title']}
rarity: {data['rarity']}
key_ability: {data['key_ability']}
hit_points: {data['hit_points']}
description: Descripción de la clase {data['title']}
---

## {data['title']}

### Descripción General

El **{data['title']}** es una clase versátil y poderosa en Pathfinder 2. [Descripción detallada a completar desde PC2]

### Estadísticas Básicas

- **Habilidad Clave**: {data['key_ability']}
- **Puntos de Golpe**: {data['hit_points']}

### Características de Clase

[Características principales del {data['title']} a documentar según PC2]

## Características de la Clase

Cada nivel del {data['title']} otorga características y mejoras específicas.

→ [Ver Características](/clases/{slug}/caracteristicas/)

## Dotes de la Clase

Los {data['title']} tienen acceso a dotes únicos de clase.

→ [Ver Dotes](/clases/{slug}/dotes/)

---

## Temas Relacionados

- [Características de {data['title']}](/clases/{slug}/caracteristicas/)
- [Dotes de {data['title']}](/clases/{slug}/dotes/)
- [Todas las Clases](/clases/)
- [Arquetipos](/arquetipos/)
"""

    return content

def create_class_features(slug, title, nav_order):
    """Crea el archivo de características de clase."""
    content = f"""---
layout: page
permalink: /clases/{slug}/caracteristicas/
title: Características de {title}
chapter: Clases
category: clases
source: PC2
nav_order: {nav_order}
class_name: {title}
description: Características y habilidades de {title}
---

## Características de {title}

### Nivel 1

[Características de nivel 1 para {title} a documentar según PC2]

### Nivel 2

[Características de nivel 2 para {title} a documentar según PC2]

### Nivel 3 y Superior

[Características de nivel 3+ para {title} a documentar según PC2]

---

## Temas Relacionados

- [{title} - Página Principal](/clases/{slug}/)
- [Dotes de {title}](/clases/{slug}/dotes/)
- [Todas las Clases](/clases/)
"""

    return content

def create_class_feats(slug, title, nav_order):
    """Crea el archivo de dotes de clase."""
    content = f"""---
layout: page
permalink: /clases/{slug}/dotes/
title: Dotes de {title}
chapter: Clases
category: clases
source: PC2
nav_order: {nav_order}
class_name: {title}
description: Dotes únicos para {title}
---

## Dotes de {title}

Los {title} tienen acceso a los siguientes dotes de clase:

### Dotes de 1.er Nivel

[Dotes de 1er nivel para {title} a documentar según PC2]

### Dotes de 2.º Nivel

[Dotes de 2º nivel para {title} a documentar según PC2]

### Dotes de Nivel Superior

[Dotes de 4.º, 6.º, 8.º y 10.º nivel para {title} a documentar según PC2]

---

## Temas Relacionados

- [{title} - Página Principal](/clases/{slug}/)
- [Características de {title}](/clases/{slug}/caracteristicas/)
- [Todas las Clases](/clases/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    classes_dir = docs_dir / 'clases'

    print("📚 Generando clases PC2...")
    print("=" * 60)

    nav_order = 100
    stats = {'created': 0, 'errors': 0}

    for class_key, data in CLASSES.items():
        slug = data['slug']
        title = data['title']

        # Crear directorio para clase
        class_folder = classes_dir / slug
        class_folder.mkdir(parents=True, exist_ok=True)

        try:
            # 1. Archivo index
            index_path = class_folder / 'index.md'
            index_content = create_class_index(slug, data, nav_order)
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"✅ {slug}/index.md")
            stats['created'] += 1

            # 2. Archivo de características
            features_path = class_folder / 'caracteristicas.md'
            features_content = create_class_features(slug, title, nav_order + 1)
            with open(features_path, 'w', encoding='utf-8') as f:
                f.write(features_content)
            print(f"✅ {slug}/caracteristicas.md")
            stats['created'] += 1

            # 3. Archivo de dotes
            feats_path = class_folder / 'dotes.md'
            feats_content = create_class_feats(slug, title, nav_order + 2)
            with open(feats_path, 'w', encoding='utf-8') as f:
                f.write(feats_content)
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
    print(f"   📚 Clases: {len(CLASSES)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
