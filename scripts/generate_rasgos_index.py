#!/usr/bin/env python3
"""
Script para generar el index.md de rasgos con todos los rasgos organizados por categoría.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

RASGOS_DIR = Path("/Users/ludo/code/pf2/docs/_apendices/rasgos")

# Categorías de rasgos y sus miembros
CATEGORIAS = {
    "Rasgos de Acción": [
        "ataque", "concentrar", "exploracion", "floritura", "fortuna", "fortuna-adversa",
        "manipular", "movimiento", "tiempo-libre", "reaccion"
    ],
    "Rasgos de Tipo de Daño": [
        "acido", "electricidad", "frio", "fuego", "fuerza", "mental", "sonico", "veneno"
    ],
    "Rasgos de Tradición Mágica": [
        "arcano", "divino", "oculto", "primigenio", "magico"
    ],
    "Rasgos de Escuela de Magia": [
        "abjuracion", "adivinacion", "conjuracion", "encantamiento", "evocacion",
        "ilusion", "transmutacion"  # Escuelas pre-remaster para objetos mágicos
    ],
    "Rasgos de Conjuro": [
        "consagracion", "disimulado", "escudrinamiento", "foco", "moldeo-de-conjuros",
        "prediccion", "revelacion", "santificado", "truco", "composicion"
    ],
    "Rasgos de Efecto": [
        "aura", "curacion", "deteccion", "enfermedad", "emocion", "extradimensional",
        "incapacitacion", "luz", "maldicion", "miedo", "muerte", "oscuridad", "polimorfia",
        "posesion", "sueno", "teletransporte", "teletransportacion"
    ],
    "Rasgos de Clase": [
        "alquimista", "barbaro", "bardo", "brujo", "campeon", "clerigo", "druida",
        "espadachin", "explorador", "guerrero", "hechicero", "investigador", "mago",
        "monje", "oraculo", "picaro"
    ],
    "Rasgos de Clase Específicos": [
        "aditivo", "composicion", "dedicacion", "ira", "furia", "maleficio",
        "mutageno", "punalada-trapera", "postura", "remate"
    ],
    "Rasgos de Ascendencia": [
        "aiuvarin", "caminante-del-ocaso", "catfolk", "changeling", "dhampir", "dromaar",
        "elfo", "gnomo", "goblin", "hobgoblin", "hryngar", "humano", "iruxi", "kholo",
        "kobold", "leshy", "mediano", "nefilim", "orco", "sangre-de-dragon", "tengu",
        "tripkee", "ysoki"
    ],
    "Rasgos de Tipo de Criatura": [
        "animal", "bestia", "celestial", "cieno", "constructo", "descerebrado", "dragon",
        "elemental", "espiritu", "etereo", "hada", "gigante", "hongo", "humanoide",
        "infernal", "monitor", "muerto-viviente", "planta"
    ],
    "Rasgos de Subtipo de Criatura": [
        "acuatico", "anfibio", "angel", "arconte", "azata", "daimonion", "demonio",
        "diablo", "dinosaurio"
    ],
    "Rasgos de Elemento": [
        "agua", "aire", "fuego", "tierra", "madera", "metal", "sombra", "vacio"
    ],
    "Rasgos de Alineamiento y Esencia": [
        "bueno", "sacrilego", "sagrado", "vitalidad"
    ],
    "Rasgos de Arma": [
        "a-dos-manos", "agil", "alcance", "arrojadiza", "baluarte", "barrido", "comoda",
        "derribo", "desarme", "empujon", "fatal", "fijada", "flexible", "gemela",
        "justa-de", "letal", "mano-libre", "no-letal", "ocultable", "parada", "presa",
        "propulsion-de", "reves", "ruidosa", "salpicadura", "sin-armas", "versatil",
        "volea"
    ],
    "Rasgos de Objeto": [
        "alquimico", "baculo", "bomba", "consumible", "elixir", "estructura", "infundido",
        "invertir", "pergamino", "pocion", "precioso", "talisman", "varita"
    ],
    "Rasgos de Veneno": [
        "contacto", "herida", "ingerido", "inhalado", "virulento"
    ],
    "Rasgos de Peligro": [
        "aparicion", "complejo", "mecanico", "trampa"
    ],
    "Rasgos de Rareza": [
        "poco-comun", "raro", "unico"
    ],
    "Rasgos de Dote": [
        "arquetipo", "dedicacion", "general", "habilidad", "linaje", "multiclase"
    ],
    "Rasgos Sensoriales": [
        "auditivo", "linguistico", "olfativo", "visual"
    ],
    "Otros Rasgos": [
        "aprovechar", "bravura", "convocado", "desgracia", "desventura", "entre-descansos",
        "esbirro", "justiciero", "lesion", "morfismo", "ocultismo", "ocultista", "posicion",
        "primitivo", "saga", "secreto", "sutil", "videncia"
    ]
}

def get_rasgo_info(slug):
    """Obtiene el título y descripción de un rasgo desde su archivo."""
    filepath = RASGOS_DIR / f"{slug}.md"
    if not filepath.exists():
        return None, None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer título del frontmatter
    title_match = re.search(r'^title:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else slug.replace('-', ' ').title()

    # Extraer primera línea de descripción (después del frontmatter)
    parts = content.split('---', 2)
    if len(parts) >= 3:
        body = parts[2].strip()
        # Obtener primera línea significativa
        for line in body.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Truncar a 100 caracteres
                desc = line[:100] + "..." if len(line) > 100 else line
                return title, desc

    return title, ""

def get_all_rasgo_slugs():
    """Obtiene todos los slugs de rasgos existentes."""
    slugs = []
    for filepath in RASGOS_DIR.glob("*.md"):
        if filepath.name != "index.md":
            slugs.append(filepath.stem)
    return set(slugs)

def find_uncategorized(all_slugs, categorized):
    """Encuentra rasgos que no están en ninguna categoría."""
    return all_slugs - categorized

def generate_index():
    """Genera el contenido del index.md"""
    all_slugs = get_all_rasgo_slugs()
    categorized = set()

    # Recopilar todos los rasgos categorizados
    for rasgos in CATEGORIAS.values():
        categorized.update(rasgos)

    # Encontrar rasgos sin categorizar
    uncategorized = find_uncategorized(all_slugs, categorized)
    if uncategorized:
        print(f"Rasgos sin categorizar: {sorted(uncategorized)}")

    # Generar contenido
    lines = [
        "---",
        "layout: page",
        "permalink: /apendices/rasgos/",
        "title: Rasgos",
        "chapter: Apéndices",
        "category: rasgos",
        "nav_order: 1",
        "source: PC1",
        "---",
        "",
        "Los rasgos son etiquetas que describen propiedades específicas de reglas, criaturas, objetos y aptitudes. Cada rasgo tiene un significado mecánico que afecta cómo funciona algo en el juego.",
        ""
    ]

    for categoria, rasgos in CATEGORIAS.items():
        # Filtrar solo los rasgos que existen
        rasgos_existentes = [r for r in rasgos if r in all_slugs]
        if not rasgos_existentes:
            continue

        lines.append(f"## {categoria}")
        lines.append("")
        lines.append("| Rasgo | Descripción |")
        lines.append("|-------|-------------|")

        for slug in sorted(rasgos_existentes):
            title, desc = get_rasgo_info(slug)
            if title:
                lines.append(f"| [{title}](/apendices/rasgos/{slug}/) | {desc} |")

        lines.append("")

    # Añadir rasgos sin categorizar si los hay
    if uncategorized:
        # Añadirlos a "Otros Rasgos"
        print(f"\nAñadiendo {len(uncategorized)} rasgos a 'Otros Rasgos'")

    return "\n".join(lines)

def main():
    # Primero, mostrar qué rasgos faltan en las categorías
    all_slugs = get_all_rasgo_slugs()
    categorized = set()
    for rasgos in CATEGORIAS.values():
        categorized.update(rasgos)

    missing_from_categories = all_slugs - categorized
    extra_in_categories = categorized - all_slugs

    if missing_from_categories:
        print("Rasgos existentes que NO están en ninguna categoría:")
        for slug in sorted(missing_from_categories):
            print(f"  - {slug}")

    if extra_in_categories:
        print("\nRasgos en categorías que NO existen como archivo:")
        for slug in sorted(extra_in_categories):
            print(f"  - {slug}")

    # Generar el index
    content = generate_index()

    # Guardar
    output_path = RASGOS_DIR / "index.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nIndex generado en: {output_path}")

if __name__ == "__main__":
    main()
