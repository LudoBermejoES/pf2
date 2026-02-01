#!/usr/bin/env python3
"""
Script para dividir las clases PC2 en 3 archivos como PC1:
- index.md (resumen)
- caracteristicas.md (progresión + características)
- dotes.md (placeholder - no existen en fuente)
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path('/Users/ludo/code/pf2/docs/_clases')

# Clases PC2 y sus nav_order
CLASSES = {
    'alquimista': 100,
    'barbaro': 110,
    'campeon': 120,
    'espadachin': 130,
    'hechicero': 140,
    'investigador': 150,
    'monje': 160,
    'oraculo': 170
}

# Títulos en español
TITLES = {
    'alquimista': 'Alquimista',
    'barbaro': 'Bárbaro',
    'campeon': 'Campeón',
    'espadachin': 'Espadachín',
    'hechicero': 'Hechicero',
    'investigador': 'Investigador',
    'monje': 'Monje',
    'oraculo': 'Oráculo'
}

def extract_sections(content):
    """Extrae las diferentes secciones del contenido."""

    # Encontrar donde empieza la progresión
    prog_match = re.search(r'^## Progresión', content, re.MULTILINE)
    prog_start = prog_match.start() if prog_match else len(content)

    # El contenido antes de la progresión es la descripción
    descripcion = content[:prog_start].strip()

    # Todo desde la progresión en adelante son características
    caracteristicas = content[prog_start:].strip() if prog_match else ""

    return descripcion, caracteristicas

def create_index(class_name, title, nav_order, descripcion):
    """Crea el archivo index.md con el resumen."""

    frontmatter = f"""---
layout: class
permalink: /clases/{class_name}/
title: {title}
chapter: Clases
category: clases
source: PC2
nav_order: {nav_order}
class_name: {title}
---

"""
    return frontmatter + descripcion

def create_caracteristicas(class_name, title, nav_order, caracteristicas):
    """Crea el archivo caracteristicas.md."""

    frontmatter = f"""---
layout: page
permalink: /clases/{class_name}/caracteristicas/
title: Características del {title}
chapter: Clases
category: clases
source: PC2
nav_order: {nav_order + 1}
class_name: {title}
---

"""
    return frontmatter + caracteristicas

def create_dotes_placeholder(class_name, title, nav_order):
    """Crea un placeholder para dotes.md."""

    content = f"""---
layout: page
permalink: /clases/{class_name}/dotes/
title: Dotes de {title}
chapter: Clases
category: clases
source: PC2
nav_order: {nav_order + 2}
class_name: {title}
---

# Dotes de {title}

En cada nivel en el que obtienes una dote de {title.lower()}, puedes seleccionar una de las siguientes. Debes cumplir todos los requisitos antes de seleccionarla.

---

> ⚠️ **Nota:** Las dotes de clase del {title} del Player Core 2 aún no han sido incorporadas a esta documentación. El material fuente no incluía las descripciones detalladas de las dotes de clase.

---

## Niveles de Dotes

Las dotes de {title.lower()} están disponibles en los siguientes niveles:

- **Nivel 1:** Dotes iniciales
- **Nivel 2, 4, 6, 8:** Dotes de niveles pares bajos
- **Nivel 10, 12, 14:** Dotes de niveles pares medios
- **Nivel 16, 18, 20:** Dotes de niveles pares altos

---

*Contenido pendiente de incorporación desde Player Core 2.*
"""
    return content

def process_class(class_name):
    """Procesa una clase y la divide en archivos."""

    class_dir = DOCS_DIR / class_name
    index_file = class_dir / 'index.md'

    if not index_file.exists():
        print(f"❌ No existe: {index_file}")
        return False

    # Leer contenido actual
    content = index_file.read_text(encoding='utf-8')

    # Extraer frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        print(f"❌ No se encontró frontmatter en {class_name}")
        return False

    # Contenido sin frontmatter
    body = content[fm_match.end():].strip()

    title = TITLES[class_name]
    nav_order = CLASSES[class_name]

    # Extraer secciones
    descripcion, caracteristicas = extract_sections(body)

    # Crear archivos
    # 1. index.md (reescribir con solo descripción)
    index_content = create_index(class_name, title, nav_order, descripcion)
    index_file.write_text(index_content, encoding='utf-8')
    print(f"✅ {class_name}/index.md (descripción)")

    # 2. caracteristicas.md
    caract_file = class_dir / 'caracteristicas.md'
    caract_content = create_caracteristicas(class_name, title, nav_order, caracteristicas)
    caract_file.write_text(caract_content, encoding='utf-8')
    print(f"✅ {class_name}/caracteristicas.md (progresión + características)")

    # 3. dotes.md (placeholder)
    dotes_file = class_dir / 'dotes.md'
    dotes_content = create_dotes_placeholder(class_name, title, nav_order)
    dotes_file.write_text(dotes_content, encoding='utf-8')
    print(f"✅ {class_name}/dotes.md (placeholder)")

    return True

def main():
    print("=" * 60)
    print("📚 DIVIDIENDO CLASES PC2 EN 3 ARCHIVOS")
    print("=" * 60)

    success = 0
    errors = 0

    for class_name in CLASSES:
        print(f"\n--- {TITLES[class_name]} ---")
        if process_class(class_name):
            success += 1
        else:
            errors += 1

    print("\n" + "=" * 60)
    print(f"✅ Clases procesadas: {success}")
    print(f"❌ Errores: {errors}")
    print("=" * 60)

if __name__ == '__main__':
    main()
