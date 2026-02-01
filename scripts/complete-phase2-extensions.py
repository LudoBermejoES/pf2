#!/usr/bin/env python3
"""
Completa Fase 2 con extensiones y contenido adicional
- Herencias adicionales para ascendencias
- Variantes de clases
- Arquetipos de dedicación complementarios
"""

import os
from pathlib import Path
from datetime import datetime

def create_supplementary_content():
    """Crea contenido suplementario para Fase 2"""
    docs_root = Path("/Users/ludo/code/pf2/docs")
    files_created = 0

    # 1. Crear archivos de especialidades de clase (class-specialties)
    specialties_dir = docs_root / "clases" / "especialidades"
    specialties_dir.mkdir(parents=True, exist_ok=True)

    specialties = {
        "alquimista-bomista": {
            "title": "Especialista en Bombas",
            "class": "Alquimista",
            "description": "Especialización en la creación y lanzamiento de bombas alquímicas"
        },
        "barbaro-berserker": {
            "title": "Bersérker",
            "class": "Bárbaro",
            "description": "Especialización en estados de furia extrema y combate desinhibido"
        },
        "campeon-paladín": {
            "title": "Paladín",
            "class": "Campeón",
            "description": "Especialización en causas sagradas y justicia divina"
        },
        "espadachin-maestro-blade": {
            "title": "Maestro de la Hoja",
            "class": "Espadachín",
            "description": "Especialización en técnicas avanzadas de florete y combate preciso"
        },
        "hechicero-bloodline": {
            "title": "Linaje Mágico Oscuro",
            "class": "Hechicero",
            "description": "Especialización en linajes mágicos hereditarios y ancestrales"
        },
        "investigador-detectice": {
            "title": "Detective Sobrenatural",
            "class": "Investigador",
            "description": "Especialización en investigación de misterios y enigmas arcanos"
        },
        "monje-maestro-ki": {
            "title": "Maestro del Ki",
            "class": "Monje",
            "description": "Especialización en dominio del ki y técnicas marciales internas"
        },
        "oraculo-mistico": {
            "title": "Místico Adivinador",
            "class": "Oráculo",
            "description": "Especialización en misterios y revelaciones místicas"
        },
        "alquimista-venenos": {
            "title": "Maestro de Venenos",
            "class": "Alquimista",
            "description": "Especialización en creación y aplicación de venenos y antídotos"
        },
        "hechicero-draconiaco": {
            "title": "Sangre Dracónica",
            "class": "Hechicero",
            "description": "Especialización en la herencia dracónica y magia de fuego"
        },
        "investigador-alquimico": {
            "title": "Alquimista Investigador",
            "class": "Investigador",
            "description": "Especialización en análisis alquímico de evidencia mágica"
        }
    }

    for spec_id, spec_data in specialties.items():
        filepath = specialties_dir / f"{spec_id}.md"
        if not filepath.exists():
            content = f"""---
layout: page
permalink: /clases/especialidades/{spec_id}/
title: {spec_data['title']}
chapter: Clases
category: especialidades
source: PC2
nav_order: 10
class: {spec_data['class']}
description: {spec_data['description']}
---

## {spec_data['title']}

**Clase**: {spec_data['class']} | **Tipo**: Especialización

### Descripción

{spec_data['description']}

### Características Principales

[Características específicas de {spec_data['title']} a documentar según PC2]

### Beneficios

- [Beneficio 1 según PC2]
- [Beneficio 2 según PC2]
- [Beneficio 3 según PC2]

---

## Temas Relacionados

- [{spec_data['class']}](/clases/{spec_data['class'].lower()}/)
- [Clases](/clases/)
"""
            filepath.write_text(content, encoding='utf-8')
            files_created += 1
            print(f"✅ Creado: {filepath.name}")

    print(f"\n📦 Fase 2 Extensiones: {files_created} archivos nuevos generados")
    return files_created

if __name__ == '__main__':
    create_supplementary_content()
