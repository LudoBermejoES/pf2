#!/usr/bin/env python3
"""
Script para crear los archivos de rasgos faltantes.
"""

import unicodedata
from pathlib import Path

RASGOS_DIR = Path("/Users/ludo/code/pf2/docs/_rasgos")

# Rasgos faltantes con sus descripciones y tipos
MISSING_TRAITS = {
    # Clases
    "alquimista": ("clase", "Esto indica aptitudes de la clase alquimista."),
    "barbaro": ("clase", "Esto indica aptitudes de la clase bárbaro."),
    "campeon": ("clase", "Esto indica aptitudes de la clase campeón."),
    "espadachin": ("clase", "Esto indica aptitudes de la clase espadachín."),
    "hechicero": ("clase", "Esto indica aptitudes de la clase hechicero."),
    "investigador": ("clase", "Esto indica aptitudes de la clase investigador."),
    "oraculo": ("clase", "Esto indica aptitudes de la clase oráculo."),

    # Ascendencias
    "catfolk": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia catfolk."),
    "dhampir": ("ascendencia", "Una criatura con este rasgo es un dhampir, descendiente de un vampiro."),
    "hobgoblin": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia hobgoblin."),
    "kholo": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia kholo (gnoll)."),
    "kobold": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia kobold."),
    "tengu": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia tengu."),
    "tripkee": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia tripkee."),
    "ysoki": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia ysoki (ratfolk)."),
    "iruxi": ("ascendencia", "Una criatura con este rasgo es un miembro de la ascendencia iruxi (hombre lagarto)."),
    "caminante-del-ocaso": ("ascendencia", "Una criatura con este rasgo es un caminante del ocaso, descendiente de un plano de sombras."),
    "sangre-de-dragon": ("ascendencia", "Una criatura con este rasgo tiene sangre de dragón en sus venas."),

    # Escuelas de magia
    "abjuracion": ("conjuro", "Los efectos y conjuros de abjuración protegen y apartan otras cosas."),
    "adivinacion": ("conjuro", "Los conjuros de adivinación revelan información."),
    "conjuracion": ("conjuro", "Los efectos y conjuros de conjuración transportan criaturas o crean objetos."),
    "encantamiento": ("conjuro", "Los efectos y conjuros de encantamiento afectan las mentes de otras criaturas."),
    "evocacion": ("conjuro", "Los efectos y conjuros de evocación crean energía o manipulan las existentes."),
    "transmutacion": ("conjuro", "Los efectos y conjuros de transmutación cambian las propiedades físicas de las cosas."),
    "videncia": ("conjuro", "Los efectos de videncia revelan información oculta o permiten ver a distancia."),

    # Tradiciones
    "oculto": ("tradicion", "Este conjuro o efecto usa la tradición oculta de magia."),

    # Otros rasgos comunes
    "general": ("dote", "Una dote con este rasgo está disponible para todos los personajes que cumplan sus prerrequisitos."),
    "floritura": ("accion", "Las acciones con este rasgo son especialmente llamativas. Solo puedes usar una acción con el rasgo floritura por turno."),
    "postura": ("accion", "Una postura es una posición de combate general que adoptas que dura hasta que te quedas inconsciente, usas otra postura o un efecto finaliza la postura."),
    "reaccion": ("accion", "Una reacción es una acción que puedes usar fuera de tu turno en respuesta a un desencadenante específico."),
    "consumible": ("equipo", "Un objeto con este rasgo puede usarse solo una vez. A menos que se indique lo contrario, el objeto se destruye al activarlo."),
    "baculo": ("equipo", "Este objeto mágico largo y delgado se usa típicamente para canalizar energía mágica."),
    "mutageno": ("equipo", "Un mutágeno es un elixir que causa cambios temporales físicos o mentales en quien lo consume."),
    "infundido": ("equipo", "Un objeto tiene este rasgo si fue creado por un alquimista usando la característica de clase de infusiones avanzadas."),
    "polimorfo": ("efecto", "Estos efectos transforman al objetivo en una nueva forma. Un objetivo no puede estar bajo los efectos de más de un efecto de polimorfo a la vez."),
    "metamorfosis": ("efecto", "Estos efectos cambian el cuerpo del objetivo de alguna manera."),
    "morfo": ("efecto", "Un efecto morfo cambia la forma del objetivo."),
    "teletransportacion": ("efecto", "Los efectos de teletransportación te permiten moverte instantáneamente de un punto a otro."),
    "sanacion": ("efecto", "Un efecto de sanación restaura los Puntos de Golpe de una criatura o reduce la gravedad de una aflicción."),
    "bueno": ("alineamiento", "Los efectos con este rasgo son efectos del bien, a menudo dañinos para criaturas malvadas."),
    "primitivo": ("tradicion", "Un objeto o conjuro con este rasgo usa métodos y materiales que son accesibles para culturas sin acceso a la metalurgia avanzada."),
    "precioso": ("equipo", "Un material precioso es especialmente valioso y a menudo tiene propiedades mágicas."),
    "complejo": ("peligro", "Este peligro tiene un bloque de estadísticas completo y puede actuar en combate."),
    "aditivo": ("alquimia", "Los aditivos son sustancias especiales que pueden añadirse a bombas u otros objetos alquímicos para mejorarlos."),
    "invertir": ("equipo", "Un objeto con este rasgo debe ser investido para que funcionen sus beneficios mágicos continuos."),
    "ingerido": ("veneno", "Este veneno se introduce en el cuerpo cuando lo tragas."),
    "agua": ("elemental", "Los efectos con este rasgo usan agua o tienen poder sobre el agua."),
    "bravura": ("emocion", "Este efecto inspira valor y determinación."),
    "ira": ("emocion", "Este efecto causa o se relaciona con la emoción de ira."),
    "desgracia": ("efecto", "Una desgracia es un efecto negativo basado en la suerte."),
    "fortuna-adversa": ("efecto", "Un efecto de fortuna adversa te obliga a tirar dos veces y tomar el peor resultado."),
    "remate": ("accion", "Una acción con este rasgo solo puede usarse como la última acción de tu turno."),
    "vinculado-a-la-maldicion": ("oraculo", "Este efecto está vinculado a la maldición de un oráculo."),
    "justiciero": ("arquetipo", "Esto indica aptitudes del arquetipo justiciero."),
    "forma-de-conjuro": ("metamagia", "Las acciones con este rasgo alteran la forma física de un conjuro."),
    "dar-forma-al-conjuro": ("metamagia", "Las acciones con este rasgo te permiten modificar un conjuro de alguna manera."),
    "florecimiento": ("accion", "Las acciones con este rasgo son especialmente llamativas. Equivale a floritura."),
}

def create_trait_file(slug, trait_type, description):
    """Crea un archivo de rasgo."""
    # Formatear el título
    title = slug.replace('-', ' ').title()
    # Casos especiales
    title_map = {
        "Abjuracion": "Abjuración",
        "Adivinacion": "Adivinación",
        "Conjuracion": "Conjuración",
        "Evocacion": "Evocación",
        "Transmutacion": "Transmutación",
        "Oraculo": "Oráculo",
        "Campeon": "Campeón",
        "Espadachin": "Espadachín",
        "Barbaro": "Bárbaro",
        "Reaccion": "Reacción",
        "Teletransportacion": "Teletransportación",
        "Sanacion": "Sanación",
        "Mutageno": "Mutágeno",
    }
    title = title_map.get(title, title)

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

def main():
    print("Creando archivos de rasgos faltantes")
    print("=" * 50)

    created = 0
    skipped = 0

    for slug, (trait_type, description) in MISSING_TRAITS.items():
        filepath = RASGOS_DIR / f"{slug}.md"
        if filepath.exists():
            print(f"  ⊘ {slug} (ya existe)")
            skipped += 1
        else:
            create_trait_file(slug, trait_type, description)
            print(f"  ✓ {slug}")
            created += 1

    print("\n" + "=" * 50)
    print(f"✓ Creados: {created}")
    print(f"⊘ Ya existían: {skipped}")

if __name__ == "__main__":
    main()
