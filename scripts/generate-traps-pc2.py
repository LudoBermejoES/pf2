#!/usr/bin/env python3
"""
Script para generar archivos individuales de trampas de PC2
Lee datos de scripts/data/traps-pc2.json y genera archivos en docs/_equipo/trampas/
"""

import os
import json
from pathlib import Path

# Directorio base
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "scripts" / "data" / "traps-pc2.json"
OUTPUT_DIR = BASE_DIR / "docs" / "_equipo" / "trampas"


def load_trap_data():
    """Carga los datos de trampas desde el archivo JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['traps']


def generate_trap_file(trap):
    """Genera el contenido del archivo markdown para una trampa"""
    name = trap['name']
    slug = trap['slug']
    level = trap['level']
    price = trap['price']
    traits = trap['traits']
    trigger = trap['trigger']
    effect = trap['effect']

    # Formatear rasgos
    traits_str = ", ".join(traits)

    # Generar contenido
    content = f"""---
layout: page
permalink: /equipo/trampas/{slug}/
title: {name}
chapter: Equipo
category: equipo
source: PC2
---

**Nivel** {level}; **Precio** {price}

**Rasgos:** {traits_str}

---

**Desencadenar** {trigger}

**Efecto** {effect}

---

## Ver también

- [Lista de trampas](/equipo/trampas/)
- [Dote Fabricación de trampas](/dotes/generales/fabricacion-de-trampas/)
"""

    return content


def main():
    print(f"Cargando datos desde: {DATA_FILE}")

    # Verificar que el archivo de datos existe
    if not DATA_FILE.exists():
        print(f"ERROR: No se encontró el archivo de datos: {DATA_FILE}")
        return

    # Cargar datos
    traps = load_trap_data()
    print(f"Encontradas {len(traps)} trampas en el archivo de datos")

    # Crear directorio de salida si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generar archivos
    created = 0
    skipped = 0

    for trap in traps:
        slug = trap['slug']
        output_path = OUTPUT_DIR / f"{slug}.md"

        # Verificar si ya existe
        if output_path.exists():
            print(f"  Ya existe: {slug}.md")
            skipped += 1
            continue

        # Generar contenido
        content = generate_trap_file(trap)

        # Escribir archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  Creado: {slug}.md")
        created += 1

    print(f"\n{'='*50}")
    print(f"Resumen:")
    print(f"  Archivos creados: {created}")
    print(f"  Archivos que ya existían: {skipped}")
    print(f"  Total de trampas: {len(traps)}")


if __name__ == "__main__":
    main()
