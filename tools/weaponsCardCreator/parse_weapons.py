#!/usr/bin/env python3
"""
Parse weapon markdown files from the PF2e wiki
Extracts weapon data and trait descriptions, generates weapons.json
"""

import os
import re
import json
import glob

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
WEAPONS_DIR = os.path.join(WIKI_PATH, '_equipo', 'armas')
TRAITS_DIR = os.path.join(WIKI_PATH, '_apendices', 'rasgos')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'weapons.json')


def load_trait_descriptions():
    """Load all trait descriptions from rasgos folder"""
    traits = {}

    for filepath in glob.glob(os.path.join(TRAITS_DIR, '*.md')):
        filename = os.path.basename(filepath)
        if filename == 'index.md':
            continue

        slug = filename.replace('.md', '')

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title from frontmatter
            title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
            title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()

            # Extract description (content after frontmatter)
            parts = content.split('---', 2)
            if len(parts) >= 3:
                description = parts[2].strip()
                # Clean up description
                description = re.sub(r'^#+\s+.*\n', '', description)  # Remove headers
                description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', description)  # Remove links
                description = description.strip()

                if description:
                    traits[slug] = {
                        'name': title,
                        'description': description
                    }
        except Exception as e:
            print(f"Warning: Could not parse trait {filepath}: {e}")

    return traits


def extract_frontmatter(content):
    """Extract frontmatter as dict"""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        frontmatter = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')
        return frontmatter
    return {}


def extract_traits_from_html(content):
    """Extract trait names and slugs from HTML trait divs"""
    traits = []

    # Pattern: <a href="/apendices/rasgos/slug/" class="feat-trait">Display Name</a>
    pattern = r'<a href="/apendices/rasgos/([^/]+)/" class="feat-trait">([^<]+)</a>'
    matches = re.findall(pattern, content)

    for slug, display_name in matches:
        traits.append({
            'slug': slug,
            'display': display_name.strip()
        })

    return traits


def extract_stats(content):
    """Extract weapon stats from the stats line"""
    stats = {}

    # Find the stats line - it's the line that starts with **Daño**
    stats_match = re.search(r'\*\*Daño\*\*[^\n]+', content)
    if not stats_match:
        return stats

    stats_line = stats_match.group(0)

    # Pattern: **Label** Value; (with ; delimiter or end of line)
    # Split by ; first, then parse each segment
    segments = stats_line.split(';')

    for segment in segments:
        segment = segment.strip()
        match = re.match(r'\*\*([^*]+)\*\*\s*(.+)', segment)
        if match:
            label = match.group(1).strip()
            value = match.group(2).strip()

            if label == 'Daño':
                stats['damage'] = value
            elif label == 'Manos':
                stats['hands'] = value
            elif label == 'Impedimenta':
                stats['bulk'] = value
            elif label == 'Grupo':
                stats['group'] = value
            elif label == 'Categoría':
                stats['category'] = value
            elif label == 'Rango':
                stats['range'] = value
            elif label == 'Recarga':
                stats['reload'] = value

    return stats


def extract_price(content):
    """Extract price from **Precio** line"""
    match = re.search(r'\*\*Precio\*\*\s*([^\n]+)', content)
    if match:
        return match.group(1).strip()
    return None


def extract_description(content):
    """Extract weapon description text"""
    # Find content after stats section (after the second ---)
    parts = content.split('---')

    if len(parts) >= 5:  # frontmatter(2) + price/traits(1) + stats(1) + description(1)
        # Get the description part (usually 4th section)
        for i, part in enumerate(parts[3:], start=3):
            text = part.strip()
            # Skip "Ver también" sections
            if text.startswith('## Ver también'):
                continue
            # Skip if it's just stats
            if text.startswith('**Daño**') or text.startswith('**Bon.'):
                continue
            # Skip empty
            if not text:
                continue
            # This should be the description
            if not text.startswith('#') and not text.startswith('**'):
                # Remove any markdown tables (lines starting with |)
                lines = text.split('\n')
                clean_lines = []
                for line in lines:
                    # Stop at tables or empty lines followed by tables
                    if line.strip().startswith('|'):
                        break
                    clean_lines.append(line)

                return '\n'.join(clean_lines).strip()

    return None


def parse_weapon_file(filepath, trait_descriptions):
    """Parse a single weapon markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter = extract_frontmatter(content)

    # Extract basic info
    weapon = {
        'id': os.path.basename(filepath).replace('.md', ''),
        'name': frontmatter.get('title', ''),
        'source': frontmatter.get('source', 'PC1'),
        'permalink': frontmatter.get('permalink', ''),
    }

    # Extract price
    price = extract_price(content)
    if price:
        weapon['price'] = price

    # Extract traits with their slugs
    traits = extract_traits_from_html(content)
    weapon['traits'] = []
    weapon['trait_descriptions'] = []

    for trait in traits:
        weapon['traits'].append(trait['display'])

        # Get trait description if available
        slug = trait['slug']
        if slug in trait_descriptions:
            weapon['trait_descriptions'].append({
                'name': trait['display'],
                'description': trait_descriptions[slug]['description']
            })

    # Extract stats
    stats = extract_stats(content)
    weapon.update(stats)

    # Extract description
    description = extract_description(content)
    if description:
        weapon['description'] = description

    # Determine if ranged weapon
    weapon['isRanged'] = 'range' in stats

    return weapon


def main():
    """Main function to parse all weapons"""
    print("PF2e Weapons Parser")
    print("=" * 40)
    print()

    # Load trait descriptions first
    print("Loading trait descriptions...")
    trait_descriptions = load_trait_descriptions()
    print(f"Loaded {len(trait_descriptions)} trait descriptions")
    print()

    # Find all weapon files
    weapon_files = glob.glob(os.path.join(WEAPONS_DIR, '*.md'))

    # Filter out special files
    skip_files = ['index.md', 'bala-honda.md', 'dardo-cerbatana.md',
                  'flecha.md', 'virote.md', 'bomba-alquimica.md']
    weapon_files = [f for f in weapon_files if os.path.basename(f) not in skip_files]

    print(f"Found {len(weapon_files)} weapon files")
    print()

    # Parse all weapons
    weapons = []
    for filepath in sorted(weapon_files):
        try:
            weapon = parse_weapon_file(filepath, trait_descriptions)
            if weapon['name']:  # Only add if has a name
                weapons.append(weapon)
                print(f"  ✓ {weapon['name']}")
        except Exception as e:
            print(f"  ✗ Error parsing {filepath}: {e}")

    print()
    print(f"Parsed {len(weapons)} weapons")

    # Group by category
    categories = {}
    for weapon in weapons:
        cat = weapon.get('category', 'Otros')
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1

    print("\nBy category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    # Save to JSON
    output_data = {
        'weapons': weapons,
        'trait_descriptions': trait_descriptions,
        'total': len(weapons)
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
