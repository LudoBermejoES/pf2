#!/usr/bin/env python3
"""
Script completo para:
1. Crear archivos de rasgos faltantes
2. Corregir nombres de rasgos para que coincidan con archivos existentes
3. Convertir spans a enlaces
"""

import re
import unicodedata
from pathlib import Path

# Directorios
RASGOS_DIR = Path("/Users/ludo/code/pf2/docs/_rasgos")
DIRS_TO_PROCESS = [
    Path("/Users/ludo/code/pf2/docs/_clases"),
    Path("/Users/ludo/code/pf2/docs/_ascendencias"),
    Path("/Users/ludo/code/pf2/docs/_equipo"),
    Path("/Users/ludo/code/pf2/docs/_conjuros"),
    Path("/Users/ludo/code/pf2/docs/_reglas"),
    Path("/Users/ludo/code/pf2/docs/_habilidades"),
    Path("/Users/ludo/code/pf2/docs/_dotes"),
]

EXCLUDE_PATTERNS = ["_rasgos/", "_apendices/glosario.md"]

# Mapeo de nombres alternativos al nombre correcto (el que se muestra y el slug del archivo)
# Formato: "nombre incorrecto": ("Nombre Correcto", "slug-archivo")
TRAIT_CORRECTIONS = {
    # Concentrar
    "Concentración": ("Concentrar", "concentrar"),
    "concentración": ("Concentrar", "concentrar"),
    "Concentracion": ("Concentrar", "concentrar"),
    "concentracion": ("Concentrar", "concentrar"),
    "Concentrarse": ("Concentrar", "concentrar"),
    "concentrarse": ("Concentrar", "concentrar"),

    # Floritura
    "Florecer": ("Floritura", "floritura"),
    "Florecimiento": ("Floritura", "floritura"),
    "Flourish": ("Floritura", "floritura"),

    # Polimorfía (diferente de Morfismo)
    "Polimorfo": ("Polimorfía", "polimorfia"),
    "polimorfo": ("Polimorfía", "polimorfia"),
    "Polimórfico": ("Polimorfía", "polimorfia"),
    "polimórfico": ("Polimorfía", "polimorfia"),
    "polimorfia": ("Polimorfía", "polimorfia"),

    # Morfo -> Morfismo
    "Morfo": ("Morfismo", "morfismo"),
    "morfo": ("Morfismo", "morfismo"),
    "Metamorfosis": ("Morfismo", "morfismo"),
    "metamorfosis": ("Morfismo", "morfismo"),

    # Moldeo de conjuros
    "Forma de Conjuro": ("Moldeo de conjuros", "moldeo-de-conjuros"),
    "Forma de conjuro": ("Moldeo de conjuros", "moldeo-de-conjuros"),
    "forma de conjuro": ("Moldeo de conjuros", "moldeo-de-conjuros"),
    "Dar forma al conjuro": ("Moldeo de conjuros", "moldeo-de-conjuros"),
    "dar forma al conjuro": ("Moldeo de conjuros", "moldeo-de-conjuros"),
    "moldear hechizo": ("Moldeo de conjuros", "moldeo-de-conjuros"),

    # Mayúsculas innecesarias
    "GENERAL": ("General", "general"),
    "REACCIÓN": ("Reacción", "reaccion"),
    "CURACIÓN": ("Curación", "curacion"),
    "HABILIDAD": ("Habilidad", "habilidad"),

    # Oráculo
    "Oraculo": ("Oráculo", "oraculo"),
    "oraculo": ("Oráculo", "oraculo"),

    # Vinculado a la maldición -> Maldición
    "Vinculado a la maldicion": ("Maldición", "maldicion"),
    "vinculado a la maldicion": ("Maldición", "maldicion"),

    # Sanación -> Curación
    "Sanación": ("Curación", "curacion"),
    "sanación": ("Curación", "curacion"),
}

# Rasgos que necesitan ser creados
TRAITS_TO_CREATE = {
    # Clases que faltan (PC2)
    "alquimista": ("clase", "Esto indica aptitudes de la clase alquimista."),
    "barbaro": ("clase", "Esto indica aptitudes de la clase bárbaro."),
    "campeon": ("clase", "Esto indica aptitudes de la clase campeón."),
    "espadachin": ("clase", "Esto indica aptitudes de la clase espadachín."),
    "hechicero": ("clase", "Esto indica aptitudes de la clase hechicero."),
    "investigador": ("clase", "Esto indica aptitudes de la clase investigador."),
    "oraculo": ("clase", "Esto indica aptitudes de la clase oráculo."),

    # General y otros comunes
    "general": ("dote", "Una dote con este rasgo está disponible para todos los personajes que cumplan sus prerrequisitos."),
    "floritura": ("accion", "Las acciones con este rasgo son técnicas especiales que requieren demasiado cuidado como para que las ejecutes a menudo. Solo puedes utilizar 1 acción con el rasgo floritura por turno."),
    "postura": ("accion", "Una postura es una posición de combate que adoptas y que dura hasta que quedas inconsciente, usas otra postura o acaba un efecto."),
    "reaccion": ("accion", "Una reacción es una acción que puedes usar fuera de tu turno en respuesta a un desencadenante específico."),
    "polimorfía": ("efecto", "Estos efectos transforman por completo al objetivo en una nueva forma. Un objetivo no puede estar bajo los efectos de más de una polimorfía a la vez."),

    # Ascendencias que faltan
    "catfolk": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia catfolk."),
    "dhampir": ("ascendencia", "Una criatura con este rasgo es un dhampir, descendiente de un vampiro."),
    "hobgoblin": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia hobgoblin."),
    "kholo": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia kholo (gnoll)."),
    "kobold": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia kobold."),
    "tengu": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia tengu."),
    "tripkee": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia tripkee."),
    "ysoki": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia ysoki (ratfolk)."),
    "iruxi": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia iruxi (hombre lagarto)."),
    "caminante-del-ocaso": ("ascendencia", "Una criatura con este rasgo es un caminante del ocaso."),
    "sangre-de-dragon": ("ascendencia", "Una criatura con este rasgo tiene sangre de dragón en sus venas."),

    # Escuelas de magia (para objetos mágicos)
    "abjuracion": ("magia", "Los efectos de abjuración protegen y apartan otras cosas."),
    "conjuracion": ("magia", "Los efectos de conjuración transportan criaturas u objetos, o crean cosas de la nada."),
    "encantamiento": ("magia", "Los efectos de encantamiento afectan las mentes de otras criaturas."),
    "evocacion": ("magia", "Los efectos de evocación crean o manipulan energía."),
    "transmutacion": ("magia", "Los efectos de transmutación cambian las propiedades físicas de las cosas."),
    "adivinacion": ("magia", "Los efectos de adivinación revelan información."),

    # Otros rasgos comunes
    "consumible": ("equipo", "Un objeto con este rasgo puede usarse solo una vez. A menos que se indique lo contrario, el objeto se destruye al activarlo."),
    "baculo": ("equipo", "Un báculo mágico es un objeto largo y delgado que contiene conjuros."),
    "mutageno": ("equipo", "Un mutágeno es un elixir alquímico que causa cambios físicos temporales."),
    "infundido": ("equipo", "Un objeto tiene este rasgo si fue creado por un alquimista usando infusiones."),
    "invertir": ("equipo", "Un objeto con este rasgo debe ser investido para que funcionen sus beneficios mágicos continuos."),
    "ingerido": ("veneno", "Este veneno se introduce en el cuerpo cuando lo tragas."),
    "agua": ("elemental", "Los efectos con este rasgo usan agua o tienen poder sobre el agua."),
    "complejo": ("peligro", "Este peligro tiene un bloque de estadísticas complejo y puede actuar en combate."),
    "aditivo": ("alquimia", "Los aditivos son sustancias especiales que pueden añadirse a objetos alquímicos."),
    "oculto": ("tradicion", "Este conjuro o efecto usa la tradición oculta de magia."),
    "bueno": ("alineamiento", "Los efectos con este rasgo son efectos del bien."),
    "primitivo": ("equipo", "Un objeto con este rasgo usa métodos y materiales accesibles para culturas sin metalurgia avanzada."),
    "precioso": ("material", "Un material precioso es especialmente valioso y a menudo tiene propiedades mágicas."),
    "desgracia": ("efecto", "Una desgracia es un efecto negativo basado en la suerte."),
    "fortuna-adversa": ("efecto", "Un efecto de fortuna adversa te obliga a tirar dos veces y tomar el peor resultado."),
    "remate": ("accion", "Una acción con este rasgo solo puede usarse como la última acción de tu turno."),
    "justiciero": ("arquetipo", "Esto indica aptitudes del arquetipo justiciero."),
    "bravura": ("emocion", "Este efecto inspira valor y determinación."),
    "ira": ("emocion", "Este efecto causa o se relaciona con la emoción de ira."),
}

def normalize_slug(name):
    """Normaliza un nombre para generar el slug del archivo."""
    name = name.lower()
    name = name.replace(' ', '-')
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = re.sub(r'[^a-z0-9-]', '', name)
    return name

def create_trait_file(slug, trait_type, description):
    """Crea un archivo de rasgo."""
    title_map = {
        "abjuracion": "Abjuración", "adivinacion": "Adivinación", "conjuracion": "Conjuración",
        "evocacion": "Evocación", "transmutacion": "Transmutación", "oraculo": "Oráculo",
        "campeon": "Campeón", "espadachin": "Espadachín", "barbaro": "Bárbaro",
        "reaccion": "Reacción", "polimorfia": "Polimorfía", "mutageno": "Mutágeno",
        "curacion": "Curación", "baculo": "Báculo",
    }
    title = slug.replace('-', ' ').title()
    title = title_map.get(slug, title)

    content = f'''---
layout: page
permalink: /rasgos/{slug}/
title: "{title}"
chapter: Rasgos
category: rasgos
trait_type: {trait_type}
source: PC1
---

{description}
'''
    filepath = RASGOS_DIR / f"{slug}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def get_existing_traits():
    """Obtiene un set de slugs de rasgos existentes."""
    traits = set()
    for md_file in RASGOS_DIR.glob('*.md'):
        if md_file.name != 'index.md':
            traits.add(md_file.stem)
    return traits

def should_process(filepath):
    filepath_str = str(filepath)
    return not any(p in filepath_str for p in EXCLUDE_PATTERNS)

def process_trait_span(trait_name, existing_traits, missing_traits):
    """Procesa un nombre de rasgo y devuelve el HTML correcto."""
    # Verificar si necesita corrección
    if trait_name in TRAIT_CORRECTIONS:
        correct_name, slug = TRAIT_CORRECTIONS[trait_name]
    else:
        correct_name = trait_name
        slug = normalize_slug(trait_name)

    # Verificar si existe el archivo
    if slug in existing_traits:
        return f'<a href="/rasgos/{slug}/" class="feat-trait">{correct_name}</a>'
    else:
        missing_traits.add((trait_name, slug))
        return f'<span class="feat-trait">{correct_name}</span>'

def process_file(filepath, existing_traits, missing_traits):
    """Procesa un archivo MD."""
    if not should_process(filepath):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patrón para spans de rasgos
    span_pattern = r'<span class="feat-trait">([^<]+)</span>'

    def replacer(match):
        return process_trait_span(match.group(1), existing_traits, missing_traits)

    new_content = re.sub(span_pattern, replacer, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    print("=" * 60)
    print("PASO 1: Crear archivos de rasgos faltantes")
    print("=" * 60)

    existing_traits = get_existing_traits()
    print(f"Rasgos existentes: {len(existing_traits)}")

    created = 0
    for slug, (trait_type, description) in TRAITS_TO_CREATE.items():
        if slug not in existing_traits:
            create_trait_file(slug, trait_type, description)
            existing_traits.add(slug)
            print(f"  ✓ Creado: {slug}")
            created += 1

    print(f"\nRasgos creados: {created}")

    print("\n" + "=" * 60)
    print("PASO 2: Corregir nombres y añadir enlaces")
    print("=" * 60)

    missing_traits = set()
    updated = 0

    for base_dir in DIRS_TO_PROCESS:
        if not base_dir.exists():
            continue
        for md_file in base_dir.rglob('*.md'):
            if md_file.name == 'index.md':
                continue
            if process_file(md_file, existing_traits, missing_traits):
                updated += 1

    print(f"\nArchivos actualizados: {updated}")

    if missing_traits:
        print(f"\n⚠ Rasgos sin archivo ({len(missing_traits)}):")
        for name, slug in sorted(missing_traits):
            print(f"  - {name} (slug: {slug})")

if __name__ == "__main__":
    main()
