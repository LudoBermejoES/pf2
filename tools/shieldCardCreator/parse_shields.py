#!/usr/bin/env python3
"""
Parse shield markdown files from the PF2e wiki
Extracts shield data, generates shields.json
"""

import os
import re
import json
import glob

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
SHIELDS_DIR = os.path.join(WIKI_PATH, '_equipo', 'escudos')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'shields.json')


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


def extract_stats(content):
    """Extract shield stats from the stats line"""
    stats = {}

    # Find the stats line - it's the line that starts with **Bon. CA**
    stats_match = re.search(r'\*\*Bon\. CA\*\*[^\n]+', content)
    if not stats_match:
        return stats

    stats_line = stats_match.group(0)

    # Split by ; first, then parse each segment
    segments = stats_line.split(';')

    for segment in segments:
        segment = segment.strip()
        match = re.match(r'\*\*([^*]+)\*\*\s*(.+)', segment)
        if match:
            label = match.group(1).strip()
            value = match.group(2).strip()

            if label == 'Bon. CA':
                stats['ac_bonus'] = value
            elif label == 'Pen. Velocidad':
                stats['speed_penalty'] = value
            elif label == 'Impedimenta':
                stats['bulk'] = value
            elif label == 'Dureza':
                stats['hardness'] = value
            elif label == 'PG':
                stats['hp'] = value

    return stats


def extract_price(content):
    """Extract price from **Precio** line"""
    match = re.search(r'\*\*Precio\*\*\s*([^\n]+)', content)
    if match:
        return match.group(1).strip()
    return None


def extract_description(content):
    """Extract shield description text"""
    # Find content after stats section (after the second ---)
    parts = content.split('---')

    if len(parts) >= 5:  # frontmatter(2) + price(1) + stats(1) + description(1)
        for i, part in enumerate(parts[3:], start=3):
            text = part.strip()
            # Skip "Ver también" sections
            if text.startswith('## Ver también'):
                continue
            # Skip if it's just stats
            if text.startswith('**Bon. CA**'):
                continue
            # Skip empty
            if not text:
                continue
            # This should be the description
            if not text.startswith('#') and not text.startswith('**'):
                # Remove any markdown tables
                lines = text.split('\n')
                clean_lines = []
                for line in lines:
                    if line.strip().startswith('|'):
                        break
                    clean_lines.append(line)

                return '\n'.join(clean_lines).strip()

    return None


def parse_shield_file(filepath):
    """Parse a single shield markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter = extract_frontmatter(content)

    # Extract basic info
    shield = {
        'id': os.path.basename(filepath).replace('.md', ''),
        'name': frontmatter.get('title', ''),
        'source': frontmatter.get('source', 'PC1'),
        'permalink': frontmatter.get('permalink', ''),
    }

    # Extract price
    price = extract_price(content)
    if price:
        shield['price'] = price

    # Extract stats
    stats = extract_stats(content)
    shield.update(stats)

    # Extract description
    description = extract_description(content)
    if description:
        shield['description'] = description

    return shield


def main():
    """Main function to parse all shields"""
    print("PF2e Shields Parser")
    print("=" * 40)
    print()

    # Find all shield files
    shield_files = glob.glob(os.path.join(SHIELDS_DIR, '*.md'))

    # Filter out special files
    skip_files = ['index.md']
    shield_files = [f for f in shield_files if os.path.basename(f) not in skip_files]

    print(f"Found {len(shield_files)} shield files")
    print()

    # Parse all shields
    shields = []
    for filepath in sorted(shield_files):
        try:
            shield = parse_shield_file(filepath)
            if shield['name']:
                shields.append(shield)
                print(f"  + {shield['name']}")
        except Exception as e:
            print(f"  x Error parsing {filepath}: {e}")

    print()
    print(f"Parsed {len(shields)} shields")

    # Save to JSON
    output_data = {
        'shields': shields,
        'total': len(shields)
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n+ Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
