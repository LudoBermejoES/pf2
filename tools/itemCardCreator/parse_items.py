#!/usr/bin/env python3
"""
Parse item markdown files from the PF2e wiki
Extracts item data and generates items.json
"""

import os
import re
import json
import glob

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
ITEMS_DIR = os.path.join(WIKI_PATH, '_equipo', 'objetos')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'items.json')


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


def extract_price(content):
    """Extract price from **Precio** line"""
    match = re.search(r'\*\*Precio\*\*\s*([^\n]+)', content)
    if match:
        return match.group(1).strip()
    return None


def extract_stats(content):
    """Extract item stats from the stats line"""
    stats = {}

    # Find the stats line - contains **Impedimenta** and/or **Manos**
    stats_match = re.search(r'\*\*Impedimenta\*\*[^\n]+', content)
    if stats_match:
        stats_line = stats_match.group(0)

        # Extract Impedimenta (Bulk)
        bulk_match = re.search(r'\*\*Impedimenta\*\*\s*([^;*\n]+)', stats_line)
        if bulk_match:
            stats['bulk'] = bulk_match.group(1).strip()

        # Extract Manos (Hands)
        hands_match = re.search(r'\*\*Manos\*\*\s*([^;*\n]+)', stats_line)
        if hands_match:
            stats['hands'] = hands_match.group(1).strip()

    return stats


def extract_description(content):
    """Extract item description text"""
    # Split by --- to find sections
    parts = re.split(r'\n---\s*\n', content)

    if len(parts) >= 4:
        # Get the description part (after frontmatter, price, and stats)
        for i, part in enumerate(parts[3:], start=3):
            text = part.strip()
            # Skip "Ver también" sections
            if text.startswith('## Ver también'):
                continue
            # Skip if it's stats
            if text.startswith('**Impedimenta**') or text.startswith('**Precio**'):
                continue
            # Skip empty
            if not text:
                continue
            # This should be the description
            if not text.startswith('#'):
                # Remove links but keep text
                text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
                return text.strip()

    return None


def parse_item_file(filepath):
    """Parse a single item markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter = extract_frontmatter(content)

    # Extract basic info
    item = {
        'id': os.path.basename(filepath).replace('.md', ''),
        'name': frontmatter.get('title', ''),
        'source': frontmatter.get('source', 'PC1'),
        'permalink': frontmatter.get('permalink', ''),
    }

    # Extract price
    price = extract_price(content)
    if price:
        item['price'] = price

    # Extract stats
    stats = extract_stats(content)
    item.update(stats)

    # Extract description
    description = extract_description(content)
    if description:
        item['description'] = description

    return item


def main():
    """Main function to parse all items"""
    print("PF2e Items Parser")
    print("=" * 40)
    print()

    # Find all item files
    item_files = glob.glob(os.path.join(ITEMS_DIR, '*.md'))

    # Filter out special files
    skip_files = ['index.md']
    item_files = [f for f in item_files if os.path.basename(f) not in skip_files]

    print(f"Found {len(item_files)} item files")
    print()

    # Parse all items
    items = []
    for filepath in sorted(item_files):
        try:
            item = parse_item_file(filepath)
            if item['name']:  # Only add if has a name
                items.append(item)
                print(f"  ✓ {item['name']}")
        except Exception as e:
            print(f"  ✗ Error parsing {filepath}: {e}")

    print()
    print(f"Parsed {len(items)} items")

    # Save to JSON
    output_data = {
        'items': items,
        'total': len(items)
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
