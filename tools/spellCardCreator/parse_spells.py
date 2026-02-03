#!/usr/bin/env python3
"""
Parse spell markdown files from the PF2e wiki and extract spell data
Outputs JSON file with all spells for card generation
"""

import os
import re
import json
import glob

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
SPELLS_DIR = os.path.join(WIKI_PATH, '_conjuros', 'spell-individual')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'spells.json')

# Trait descriptions from the wiki
TRAIT_DESCRIPTIONS = {
    "adivinación": "Los conjuros de adivinación revelan información.",
    "agua": "Efectos que crean o manipulan agua, o afectan a criaturas de agua.",
    "aire": "Efectos que crean o manipulan aire, o afectan a criaturas de aire.",
    "arcano": "Procedente de la tradición arcana de magia.",
    "audible": "Requiere que el objetivo pueda oír para tener efecto.",
    "aura": "El efecto se origina en una emanación que se mueve contigo.",
    "concentrar": "Requiere concentración mental sostenida.",
    "conjuración": "Conjuros que traen criaturas u objetos.",
    "curación": "Efectos que restauran puntos de golpe o vitalidad.",
    "curativo": "Efectos que restauran puntos de golpe o vitalidad.",
    "daño": "Inflige daño a una criatura u objeto.",
    "detección": "Detecta la presencia de algo cercano.",
    "disimulado": "Oculta información sobre el efecto mágico.",
    "divino": "Procedente de la tradición divina de magia.",
    "encantamiento": "Afecta o controla la mente de las criaturas.",
    "evocación": "Crea energía, objetos o criaturas de la nada.",
    "frío": "Efectos de frío o hielo. Inflige daño por frío.",
    "fuego": "Efectos de fuego o calor. Inflige daño por fuego.",
    "ilusión": "Crea imágenes falsas o engaña los sentidos.",
    "incapacitante": "El efecto puede incapacitar al objetivo.",
    "invocación": "Trae criaturas de otros planos o lugares.",
    "lenguaje": "Requiere que el objetivo entienda el idioma.",
    "luz": "Genera luz o brillo.",
    "maldición": "Impone un efecto negativo persistente.",
    "manipular": "Requiere gestos o manipulación de componentes.",
    "mental": "Afecta a la mente. No funciona contra criaturas sin mente.",
    "metamagia": "Modifica otros conjuros o hechizos.",
    "miedo": "Causa la condición de asustado.",
    "muerte": "Relacionado con la muerte o el paso al más allá.",
    "necromancia": "Manipula las fuerzas de la vida y la muerte.",
    "ocultista": "Procedente de la tradición ocultista de magia.",
    "olfativo": "Relacionado con olores o el sentido del olfato.",
    "oscuridad": "Crea oscuridad o reduce la luz.",
    "planta": "Afecta o crea vegetación.",
    "poco común": "No está disponible para todos los personajes.",
    "predicción": "Revela información sobre el futuro.",
    "primigenia": "Procedente de la tradición primigenia de magia.",
    "protección": "Proporciona defensa o protección.",
    "raro": "Muy difícil de encontrar o aprender.",
    "revelación": "Revela información oculta o invisible.",
    "sónico": "Efectos de sonido. Inflige daño sónico.",
    "sueño": "Relacionado con el sueño o los sueños.",
    "teletransporte": "Mueve criaturas u objetos instantáneamente.",
    "tierra": "Efectos de tierra o piedra, o afectan a criaturas de tierra.",
    "transmutación": "Cambia la forma o propiedades de algo.",
    "truco": "Un conjuro menor que se puede lanzar a voluntad.",
    "veneno": "Efectos venenosos o tóxicos.",
    "verbal": "Requiere que hables palabras de poder.",
    "visual": "Requiere que el objetivo pueda ver para tener efecto.",
}


def parse_spell_file(filepath):
    """Parse a single spell markdown file and extract data"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    spell_data = {}

    # Get spell ID from filename
    filename = os.path.basename(filepath)
    spell_data['id'] = filename.replace('.md', '')

    # Parse frontmatter
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)

        # Title
        title_match = re.search(r'title:\s*(.+)', frontmatter)
        if title_match:
            spell_data['name'] = title_match.group(1).strip()

        # Spell level
        level_match = re.search(r'spell_level:\s*(.+)', frontmatter)
        if level_match:
            level = level_match.group(1).strip()
            spell_data['level'] = level
            spell_data['isCantrip'] = level.upper() == 'TRUCO'

    # Get body content after frontmatter
    body_match = re.search(r'^---\s*\n.*?\n---\s*\n(.+)', content, re.DOTALL)
    if not body_match:
        return None

    body = body_match.group(1)

    # Extract header line for action type
    header_match = re.search(r'##\s+.*?\{%\s*include\s+accion\.html\s+tipo="(\d+)"\s*%\}', body)
    if header_match:
        action_type = header_match.group(1)
        spell_data['actions'] = int(action_type)
    else:
        spell_data['actions'] = None  # Variable or 10 minutes, etc.

    # Parse traditions
    traditions_match = re.search(r'\*\*Tradiciones?:\*\*\s*(.+?)(?:\n|$)', body)
    if traditions_match:
        traditions_text = traditions_match.group(1).strip()
        traditions = [t.strip() for t in traditions_text.split(',')]
        spell_data['traditions'] = traditions

    # Parse casting time (if not standard actions)
    casting_match = re.search(r'\*\*Lanzamiento:\*\*\s*(.+?)(?:\n|;|$)', body)
    if casting_match:
        spell_data['casting_time'] = casting_match.group(1).strip()

    # Parse range/distance
    range_match = re.search(r'\*\*Rango(?:\s+de\s+distancia)?:\*\*\s*(.+?)(?:;|\n|$)', body)
    if range_match:
        spell_data['range'] = range_match.group(1).strip()

    # Parse area
    area_match = re.search(r'\*\*[AÁ]rea:\*\*\s*(.+?)(?:;|\n|$)', body)
    if area_match:
        spell_data['area'] = area_match.group(1).strip()

    # Parse targets
    targets_match = re.search(r'\*\*Objetivos?:\*\*\s*(.+?)(?:;|\n|$)', body)
    if targets_match:
        spell_data['targets'] = targets_match.group(1).strip()

    # Parse duration
    duration_match = re.search(r'\*\*Duraci[oó]n:\*\*\s*(.+?)(?:;|\n|$)', body)
    if duration_match:
        spell_data['duration'] = duration_match.group(1).strip()

    # Parse defense/save
    defense_match = re.search(r'\*\*Defensa:\*\*\s*(.+?)(?:;|\n|$)', body)
    if defense_match:
        spell_data['defense'] = defense_match.group(1).strip()

    # Parse traits from trait-tag spans
    traits = []
    trait_matches = re.findall(r'<span\s+class="trait-tag">([^<]+)</span>', body)
    for trait in trait_matches:
        traits.append(trait.strip())
    spell_data['traits'] = traits

    # Add trait descriptions
    trait_descriptions = []
    for trait in traits:
        trait_lower = trait.lower()
        if trait_lower in TRAIT_DESCRIPTIONS:
            trait_descriptions.append({
                'name': trait,
                'description': TRAIT_DESCRIPTIONS[trait_lower]
            })
    spell_data['trait_descriptions'] = trait_descriptions

    # Parse description (after the horizontal rule ---)
    # Use regex to split on --- that is on its own line (not table separator like |---|)
    desc_parts = re.split(r'\n---\s*\n', body)
    if len(desc_parts) >= 2:
        # Get the main description part (after first ---)
        description_text = desc_parts[1].strip()

        # Remove trait wrapper divs
        description_text = re.sub(r'<div[^>]*>.*?</div>', '', description_text, flags=re.DOTALL)

        # Split out heightened effects
        heightened_match = re.search(r'\*\*Potenciado[^*]*\*\*', description_text)
        if heightened_match:
            main_desc = description_text[:heightened_match.start()].strip()
            heightened_text = description_text[heightened_match.start():].strip()
        else:
            main_desc = description_text.strip()
            heightened_text = ""

        # Parse save results from description
        results = {}
        result_patterns = [
            (r'\*\*[ÉE]xito cr[íi]tico\*\*\s*(.+?)(?=\*\*[ÉE]xito\*\*|\*\*Fallo\*\*|\*\*Potenciado|\Z)', 'criticalSuccess'),
            (r'\*\*[ÉE]xito\*\*\s*(.+?)(?=\*\*Fallo\*\*|\*\*Potenciado|\Z)', 'success'),
            (r'\*\*Fallo\*\*\s*(.+?)(?=\*\*Fallo cr[íi]tico\*\*|\*\*Potenciado|\Z)', 'failure'),
            (r'\*\*Fallo cr[íi]tico\*\*\s*(.+?)(?=\*\*Potenciado|\Z)', 'criticalFailure'),
        ]

        for pattern, key in result_patterns:
            match = re.search(pattern, main_desc, re.DOTALL | re.IGNORECASE)
            if match:
                result_text = match.group(1).strip()
                # Clean up the result text
                result_text = re.sub(r'\n+', ' ', result_text)
                results[key] = result_text

        if results:
            spell_data['results'] = results
            # Remove results from main description
            for pattern, key in result_patterns:
                main_desc = re.sub(pattern, '', main_desc, flags=re.DOTALL | re.IGNORECASE)
            main_desc = main_desc.strip()

        spell_data['description'] = main_desc

        # Parse heightened effects
        if heightened_text:
            heightened_effects = []
            # Pattern: **Potenciado (X)** or **Potenciado (+X)**
            pattern = r'\*\*Potenciado\s*\(([^)]+)\)\*\*\s*(.+?)(?=\*\*Potenciado|\Z)'
            for match in re.finditer(pattern, heightened_text, re.DOTALL):
                level = match.group(1).strip()
                effect = match.group(2).strip()
                heightened_effects.append({
                    'level': level,
                    'effect': effect
                })
            spell_data['heightened'] = heightened_effects

    return spell_data


def main():
    """Main function to parse all spell files"""
    print("PF2e Spell Parser")
    print("=" * 40)
    print()

    # Create output directory
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Find all spell files
    spell_files = sorted(glob.glob(os.path.join(SPELLS_DIR, '*.md')))
    print(f"Found {len(spell_files)} spell files")
    print()

    spells = []
    errors = []

    for filepath in spell_files:
        filename = os.path.basename(filepath)
        try:
            spell_data = parse_spell_file(filepath)
            if spell_data and 'name' in spell_data:
                spells.append(spell_data)
                print(f"  ✓ {spell_data['name']}")
            else:
                errors.append(f"{filename}: Could not parse")
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")

    print()
    print(f"Successfully parsed: {len(spells)} spells")

    if errors:
        print()
        print("Errors:")
        for error in errors:
            print(f"  - {error}")

    # Group by level for summary
    by_level = {}
    for spell in spells:
        level = spell.get('level', 'Unknown')
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(spell['name'])

    print()
    print("Spells by level:")
    for level in sorted(by_level.keys(), key=lambda x: (x != 'TRUCO', x)):
        print(f"  {level}: {len(by_level[level])} spells")

    # Save to JSON
    output_data = {
        'spells': spells,
        'total': len(spells)
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print()
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
