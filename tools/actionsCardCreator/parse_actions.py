#!/usr/bin/env python3
"""
Parse action markdown files from the PF2e wiki
Extracts action data and generates actions.json
"""

import os
import re
import json
import sys

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'actions.json')

# Action type patterns
ACTION_TYPE_PATTERNS = {
    r'tipo="1"': '1',
    r'tipo="2"': '2',
    r'tipo="3"': '3',
    r'tipo="reaccion"': 'reaction',
    r'tipo="libre"': 'free',
}

def extract_action_type(content):
    """Extract action type from markdown content"""
    for pattern, action_type in ACTION_TYPE_PATTERNS.items():
        if re.search(pattern, content):
            return action_type
    return '1'  # Default to single action

def extract_traits(content):
    """Extract traits from the content"""
    traits = []

    # New format: <span class="feat-trait">Rasgo</span>
    html_traits = re.findall(r'<span class="feat-trait">([^<]+)</span>', content)
    for trait in html_traits:
        trait = trait.strip()
        if trait and trait.capitalize() not in traits:
            traits.append(trait.capitalize())

    # If no HTML traits found, try old formats
    if not traits:
        # Look for bold traits like **ATAQUE**, **MOVIMIENTO**, etc.
        trait_matches = re.findall(r'\*\*([A-ZÁÉÍÓÚÑ]+)\*\*', content)
        for trait in trait_matches:
            if trait.upper() not in ['ÉXITO', 'FALLO', 'DESENCADENANTE', 'REQUISITOS', 'RASGOS']:
                traits.append(trait.capitalize())

        # Also look for **Rasgos:** Concentrar, Manipular pattern
        rasgos_match = re.search(r'\*\*Rasgos:\*\*\s*([A-Za-záéíóúñÁÉÍÓÚÑ,\s]+?)(?=\*\*|$|\n)', content)
        if rasgos_match:
            rasgos_text = rasgos_match.group(1)
            # Split by comma or space and clean
            for rasgo in re.split(r'[,\s]+', rasgos_text):
                rasgo = rasgo.strip()
                if rasgo and rasgo.capitalize() not in traits:
                    traits.append(rasgo.capitalize())

    return traits

def extract_trigger(content):
    """Extract trigger text for reactions"""
    # Match **Desencadenante:** with optional colon, followed by text until double newline or next **section**
    match = re.search(r'\*\*Desencadenante:?\*\*\s*(.+?)(?:\n\n|\n\*\*[A-Z]|$)', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_requirements(content):
    """Extract requirements text"""
    # Match **Requisitos:** with optional colon, followed by text until double newline or next section
    match = re.search(r'\*\*Requisitos:?\*\*\s*(.+?)(?:\n\n|\n\*\*[A-Z]|\n[A-Z][a-z]|$)', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_description(content):
    """Extract main description text"""
    # Remove frontmatter
    content_body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

    # Remove title line
    content_body = re.sub(r'^##[^\n]+\n+', '', content_body)

    # Remove HTML traits div
    content_body = re.sub(r'<div class="feat-traits-header"[^>]*>.*?</div>\s*\n*', '', content_body, flags=re.DOTALL)

    # Remove **Rasgos:** line
    content_body = re.sub(r'\*\*Rasgos:?\*\*[^\n]*\n+', '', content_body)

    # Remove standalone trait lines like **ATAQUE**
    content_body = re.sub(r'^\*\*[A-ZÁÉÍÓÚÑ]+\*\*\s*\n+', '', content_body)

    # Remove **Desencadenante:** line
    content_body = re.sub(r'\*\*Desencadenante:?\*\*[^\n]*\n+', '', content_body)

    # Remove **Requisitos:** line
    content_body = re.sub(r'\*\*Requisitos:?\*\*[^\n]*\n+', '', content_body)

    # Get text before results section
    match = re.search(r'^(.+?)(?:\*\*Éxito|\*\*Fallo|>\s*###|$)', content_body, re.DOTALL)
    if match:
        desc = match.group(1).strip()
        # Clean up markdown
        desc = re.sub(r'\[ver\]\([^)]+\)', '', desc)
        desc = re.sub(r'\(pag\.\s*\d+[^)]*\)', '', desc)
        desc = re.sub(r'\s+', ' ', desc)
        return desc.strip()

    return ""

def extract_examples(content):
    """Extract examples table from content"""
    examples = {}

    # Find ### Ejemplos section with table
    # Pattern: ### Ejemplos de tareas de X\n\n| Rango | Ejemplos |\n|---|---|\n| No entrenado | ... |
    examples_match = re.search(r'###\s*Ejemplos[^\n]*\n+\|[^\n]+\|\n\|[-|\s]+\|\n((?:\|[^\n]+\|\n?)+)', content)
    if examples_match:
        table_rows = examples_match.group(1)
        for row in re.findall(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', table_rows):
            rank = row[0].strip()
            example_text = row[1].strip()
            if rank and example_text:
                examples[rank] = example_text

    return examples if examples else None


def extract_results(content):
    """Extract success/failure results"""
    results = {
        'criticalSuccess': None,
        'success': None,
        'failure': None,
        'criticalFailure': None
    }

    # End delimiters: next result, ### header, table, or blockquote
    end_pattern = r'(?:\*\*Éxito|\*\*Fallo|\n###|\n\||\n\n>|$)'

    # Critical success
    match = re.search(r'\*\*Éxito cr[ií]tico:?\*\*\s*(.+?)' + end_pattern, content, re.DOTALL | re.IGNORECASE)
    if match:
        results['criticalSuccess'] = match.group(1).strip()

    # Success (not critical) - match **Éxito** but not **Éxito crítico**
    match = re.search(r'\*\*Éxito:?\*\*(?!\s*cr[ií]tico)\s*(.+?)(?:\*\*Fallo|\n###|\n\||\n\n>|$)', content, re.DOTALL)
    if match:
        results['success'] = match.group(1).strip()

    # Critical failure
    match = re.search(r'\*\*Fallo cr[ií]tico:?\*\*\s*(.+?)(?:\n###|\n\||\n\n>|$)', content, re.DOTALL | re.IGNORECASE)
    if match:
        results['criticalFailure'] = match.group(1).strip()

    # Failure (not critical) - match **Fallo** but not **Fallo crítico**
    match = re.search(r'\*\*Fallo:?\*\*(?!\s*cr[ií]tico)\s*(.+?)(?:\*\*Fallo cr[ií]tico|\n###|\n\||\n\n>|$)', content, re.DOTALL | re.IGNORECASE)
    if match:
        results['failure'] = match.group(1).strip()

    # Clean up results
    for key in results:
        if results[key]:
            results[key] = re.sub(r'\s+', ' ', results[key]).strip()

    return results

def parse_action_file(filepath, category):
    """Parse a single action markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return None

    frontmatter = frontmatter_match.group(1)

    # Get title from frontmatter
    title_match = re.search(r'title:\s*(.+)', frontmatter)
    title = title_match.group(1).strip() if title_match else os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()

    # Get ID from filename
    action_id = os.path.basename(filepath).replace('.md', '')

    action_data = {
        'id': action_id,
        'name': title,
        'actionType': extract_action_type(content),
        'traits': extract_traits(content),
        'category': category,
        'trigger': extract_trigger(content),
        'requirements': extract_requirements(content),
        'description': extract_description(content),
        'results': extract_results(content),
        'examples': extract_examples(content)
    }

    return action_data

def parse_individual_skill_action(filepath, skill_name):
    """Parse a single skill action from its individual file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return None

    frontmatter = frontmatter_match.group(1)

    # Get title from frontmatter
    title_match = re.search(r'title:\s*(.+)', frontmatter)
    title = title_match.group(1).strip() if title_match else os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()

    # Get action_cost from frontmatter if available
    action_cost_match = re.search(r'action_cost:\s*(\S+)', frontmatter)
    if action_cost_match:
        cost_value = action_cost_match.group(1).strip()
        # 0 = exploration/downtime (no combat action cost)
        action_type_map = {'0': 'exploration', '1': '1', '2': '2', '3': '3', 'reaction': 'reaction', 'reaccion': 'reaction', 'free': 'free', 'libre': 'free'}
        action_type = action_type_map.get(cost_value, 'exploration')
    else:
        action_type = extract_action_type(content)

    # Get skill from frontmatter if available
    skill_match = re.search(r'skill:\s*(.+)', frontmatter)
    if skill_match:
        skill_name = skill_match.group(1).strip().lower()

    # Get ID from filename
    action_id = os.path.basename(filepath).replace('.md', '')

    action_data = {
        'id': action_id,
        'name': title,
        'actionType': action_type,
        'traits': extract_traits(content),
        'category': f'habilidad-{skill_name}',
        'trigger': extract_trigger(content),
        'requirements': extract_requirements(content),
        'description': extract_description(content),
        'examples': extract_examples(content),
        'results': extract_results(content)
    }

    return action_data


def parse_skill_subfolder(skills_dir, skill_name):
    """Parse all action files in a skill subfolder"""
    actions = []
    subfolder = os.path.join(skills_dir, skill_name)

    if os.path.isdir(subfolder):
        for filename in sorted(os.listdir(subfolder)):
            if filename.endswith('.md'):
                filepath = os.path.join(subfolder, filename)
                action = parse_individual_skill_action(filepath, skill_name)
                if action:
                    actions.append(action)

    return actions


def parse_embedded_actions(filepath, skill_name):
    """Parse actions embedded within a skill file (like Acrobacias, Atletismo, etc.)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    actions = []

    # Find all ## headings (both with and without action icons)
    # Pattern 1: ## Action Name {% include accion.html tipo="X" %}
    # Pattern 2: ## Action Name (without include - these are free/exploration actions)
    all_h2_pattern = r'\n##\s+([^\n{#]+?)(?:\s*\{%\s*include\s+accion\.html\s+tipo="([^"]+)"\s*%\})?(?:\s*\(entrenado\))?\s*\n'
    matches = list(re.finditer(all_h2_pattern, content))

    for i, match in enumerate(matches):
        action_name = match.group(1).strip()
        action_type_raw = match.group(2)  # May be None for free/exploration actions

        # Skip section headers that aren't actions (like "Acciones entrenadas de X")
        if 'Acciones' in action_name and ('entrenadas' in action_name or 'de ' in action_name):
            continue
        # Skip "Grados de éxito" headers
        if 'Grados de éxito' in action_name or 'Ejemplos' in action_name:
            continue

        # Map action type - None means free/exploration action
        action_type_map = {'1': '1', '2': '2', '3': '3', 'reaccion': 'reaction', 'libre': 'free'}
        if action_type_raw:
            action_type = action_type_map.get(action_type_raw, '1')
        else:
            action_type = 'free'  # Actions without icon are free/exploration

        # Extract section content (from this match to next section delimiter)
        start_pos = match.end()
        remaining_content = content[start_pos:]

        # Find closest delimiter
        end_candidates = []

        # Next ## heading in our matches list
        if i + 1 < len(matches):
            end_candidates.append(matches[i + 1].start() - start_pos + 1)  # +1 for the \n

        # Horizontal rule separator (--- on its own line)
        hr_match = re.search(r'\n---\s*\n', remaining_content)
        if hr_match:
            end_candidates.append(hr_match.start())

        # Use the closest delimiter, or end of content
        if end_candidates:
            end_offset = min(end_candidates)
            end_pos = start_pos + end_offset
        else:
            end_pos = len(content)

        section_content = content[start_pos:end_pos]

        # Skip if it's a sub-section header (### level)
        if action_name.startswith('#'):
            continue

        # Generate ID from name
        action_id = re.sub(r'[^a-záéíóúñ\s]', '', action_name.lower())
        action_id = re.sub(r'\s+', '-', action_id.strip())

        # Extract traits (bold uppercase words at start, or **Word** patterns)
        traits = []
        trait_line_match = re.match(r'\s*\n+\*\*([A-Za-záéíóúñÁÉÍÓÚÑ,\s]+)\*\*', section_content)
        if trait_line_match:
            trait_text = trait_line_match.group(1)
            for t in re.split(r'[,\s]+', trait_text):
                t = t.strip()
                if t and t.upper() not in ['REQUISITOS', 'DESENCADENANTE']:
                    traits.append(t.capitalize())

        # Extract requirements
        req_match = re.search(r'\*\*Requisitos:?\*\*\s*(.+?)(?:\n\n|\n[A-Z]|\n\*\*)', section_content, re.DOTALL)
        requirements = req_match.group(1).strip() if req_match else None

        # Extract trigger
        trig_match = re.search(r'\*\*Desencadenante:?\*\*\s*(.+?)(?:\n\n|\n\*\*[A-Z])', section_content, re.DOTALL)
        trigger = trig_match.group(1).strip() if trig_match else None

        # Extract description (text before results)
        desc_content = section_content
        # Remove trait line
        desc_content = re.sub(r'^\s*\n+\*\*[A-Za-záéíóúñÁÉÍÓÚÑ,\s]+\*\*\s*\n+', '', desc_content)
        # Remove requirements
        desc_content = re.sub(r'\*\*Requisitos:?\*\*[^\n]*\n+', '', desc_content)
        # Remove trigger
        desc_content = re.sub(r'\*\*Desencadenante:?\*\*[^\n]*\n+', '', desc_content)

        # Get text before results or tables or sub-sections
        desc_match = re.search(r'^(.+?)(?:\*\*Éxito|\*\*Fallo|\n###|\n\|)', desc_content, re.DOTALL)
        description = ""
        if desc_match:
            description = desc_match.group(1).strip()
            description = re.sub(r'\[ver\]\([^)]+\)', '', description)
            description = re.sub(r'\(p[aá]g\.?\s*\d+[^)]*\)', '', description)
            description = re.sub(r'\s+', ' ', description).strip()

        # Extract results
        results = {
            'criticalSuccess': None,
            'success': None,
            'failure': None,
            'criticalFailure': None
        }

        crit_success = re.search(r'\*\*Éxito cr[ií]tico:?\*\*\s*(.+?)(?:\*\*Éxito\*\*|\*\*Fallo|\n###|\n\||$)', section_content, re.DOTALL | re.IGNORECASE)
        if crit_success:
            results['criticalSuccess'] = re.sub(r'\s+', ' ', crit_success.group(1)).strip()

        success = re.search(r'(?<![Cc]r[ií]tico)\s*\*\*Éxito:?\*\*\s*(.+?)(?:\*\*Fallo|\n###|\n\||$)', section_content, re.DOTALL)
        if success:
            results['success'] = re.sub(r'\s+', ' ', success.group(1)).strip()

        crit_failure = re.search(r'\*\*Fallo cr[ií]tico:?\*\*\s*(.+?)(?:\n###|\n\||$)', section_content, re.DOTALL | re.IGNORECASE)
        if crit_failure:
            results['criticalFailure'] = re.sub(r'\s+', ' ', crit_failure.group(1)).strip()

        failure = re.search(r'(?<![Cc]r[ií]tico)\s*\*\*Fallo:?\*\*\s*(.+?)(?:\*\*Fallo cr[ií]tico|\n###|\n\||$)', section_content, re.DOTALL | re.IGNORECASE)
        if failure:
            results['failure'] = re.sub(r'\s+', ' ', failure.group(1)).strip()

        action_data = {
            'id': action_id,
            'name': action_name,
            'actionType': action_type,
            'traits': traits,
            'category': f'habilidad-{skill_name}',
            'trigger': trigger,
            'requirements': requirements,
            'description': description,
            'results': results
        }

        actions.append(action_data)

    return actions

def parse_all_actions():
    """Parse all action files and generate actions.json"""
    actions = []

    # Parse basic actions
    print("Parsing acciones básicas...")
    basic_actions_dir = os.path.join(WIKI_PATH, '_reglas', 'acciones-basicas')
    if os.path.exists(basic_actions_dir):
        for filename in sorted(os.listdir(basic_actions_dir)):
            if filename.endswith('.md'):
                filepath = os.path.join(basic_actions_dir, filename)
                action = parse_action_file(filepath, 'basica')
                if action:
                    actions.append(action)
                    print(f"  {action['name']} ({action['actionType']})")

    # Parse specialty actions
    print("\nParsing acciones de especialidad...")
    specialty_actions_dir = os.path.join(WIKI_PATH, '_reglas', 'acciones-especialidad')
    if os.path.exists(specialty_actions_dir):
        for filename in sorted(os.listdir(specialty_actions_dir)):
            if filename.endswith('.md'):
                filepath = os.path.join(specialty_actions_dir, filename)
                action = parse_action_file(filepath, 'especialidad')
                if action:
                    actions.append(action)
                    print(f"  {action['name']} ({action['actionType']})")

    # Parse skill actions from individual files in subfolders
    print("\nParsing acciones de habilidades (archivos individuales)...")
    skills_dir = os.path.join(WIKI_PATH, '_habilidades')
    skill_names = [
        'acrobacias', 'arcanos', 'artesania', 'atletismo',
        'diplomacia', 'engano', 'interpretacion', 'intimidacion',
        'latrocinio', 'medicina', 'naturaleza', 'ocultismo',
        'religion', 'sigilo', 'sociedad', 'supervivencia'
    ]

    for skill_name in skill_names:
        skill_actions = parse_skill_subfolder(skills_dir, skill_name)
        if skill_actions:
            print(f"  {skill_name}: {len(skill_actions)} acciones")
            for action in skill_actions:
                print(f"    - {action['name']} ({action['actionType']})")
            actions.extend(skill_actions)

    # Parse general skill actions from 'acciones' subfolder
    print("\nParsing acciones generales de habilidades...")
    acciones_dir = os.path.join(skills_dir, 'acciones')
    if os.path.isdir(acciones_dir):
        general_actions = []
        for filename in sorted(os.listdir(acciones_dir)):
            if filename.endswith('.md'):
                filepath = os.path.join(acciones_dir, filename)
                action = parse_individual_skill_action(filepath, 'general')
                if action:
                    general_actions.append(action)
        if general_actions:
            print(f"  acciones: {len(general_actions)} acciones")
            for action in general_actions:
                print(f"    - {action['name']} ({action['actionType']})")
            actions.extend(general_actions)

    return actions

def main():
    print("Parsing PF2e action files...")
    print(f"Wiki path: {WIKI_PATH}")
    print()

    actions = parse_all_actions()

    # Save to JSON
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    output_data = {'actions': actions}
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print()
    print(f"✓ Parsed {len(actions)} actions")
    print(f"✓ Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
