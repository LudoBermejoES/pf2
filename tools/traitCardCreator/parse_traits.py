#!/usr/bin/env python3
"""
Parse trait markdown files from the PF2e wiki and extract trait data
Outputs JSON file with all traits for card generation
"""

import os
import re
import json
import glob

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
TRAITS_DIR = os.path.join(WIKI_PATH, '_apendices', 'rasgos')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'traits.json')


def parse_trait_file(filepath):
    """Parse a single trait markdown file and extract data"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    trait_data = {}

    # Get trait ID from filename
    filename = os.path.basename(filepath)
    trait_data['id'] = filename.replace('.md', '')

    # Parse frontmatter
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return None

    frontmatter = frontmatter_match.group(1)

    # Title
    title_match = re.search(r'title:\s*"?(.+?)"?\s*$', frontmatter, re.MULTILINE)
    if title_match:
        trait_data['name'] = title_match.group(1).strip()
    else:
        return None

    # Trait type
    type_match = re.search(r'trait_type:\s*(.+)', frontmatter)
    if type_match:
        trait_data['trait_type'] = type_match.group(1).strip()
    else:
        trait_data['trait_type'] = 'general'

    # Source
    source_match = re.search(r'source:\s*(.+)', frontmatter)
    if source_match:
        trait_data['source'] = source_match.group(1).strip()
    else:
        trait_data['source'] = 'PC1'

    # Get body content after frontmatter
    body_match = re.search(r'^---\s*\n.*?\n---\s*\n(.+)', content, re.DOTALL)
    if body_match:
        body = body_match.group(1).strip()
    else:
        body = ''

    # Check for subsections (like sutil.md with ## Rasgo de conjuro / ## Rasgo de arma)
    subsections = []
    section_pattern = r'##\s+(.+?)\n\n(.+?)(?=\n##|\Z)'
    section_matches = re.findall(section_pattern, body, re.DOTALL)

    if section_matches:
        for section_title, section_body in section_matches:
            subsections.append({
                'title': section_title.strip(),
                'description': section_body.strip()
            })
        trait_data['subsections'] = subsections
        # Combine all subsection descriptions for a full description
        trait_data['description'] = '\n\n'.join(
            f"{s['title']}: {s['description']}" for s in subsections
        )
    else:
        trait_data['description'] = body
        trait_data['subsections'] = []

    return trait_data


def main():
    """Main function to parse all trait files"""
    print("PF2e Trait Parser")
    print("=" * 40)
    print()

    # Create output directory
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Find all trait files
    trait_files = sorted(glob.glob(os.path.join(TRAITS_DIR, '*.md')))
    print(f"Found {len(trait_files)} trait files")
    print()

    traits = []
    errors = []

    for filepath in trait_files:
        filename = os.path.basename(filepath)
        # Skip index files
        if filename == 'index.md':
            continue
        try:
            trait_data = parse_trait_file(filepath)
            if trait_data and 'name' in trait_data:
                traits.append(trait_data)
                print(f"  + {trait_data['name']} ({trait_data['trait_type']})")
            else:
                errors.append(f"{filename}: Could not parse")
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")

    print()
    print(f"Successfully parsed: {len(traits)} traits")

    if errors:
        print()
        print("Errors:")
        for error in errors:
            print(f"  - {error}")

    # Group by trait_type for summary
    by_type = {}
    for trait in traits:
        trait_type = trait.get('trait_type', 'unknown')
        if trait_type not in by_type:
            by_type[trait_type] = []
        by_type[trait_type].append(trait['name'])

    print()
    print("Traits by type:")
    for trait_type in sorted(by_type.keys()):
        print(f"  {trait_type}: {len(by_type[trait_type])} traits")

    # Save to JSON
    output_data = {
        'traits': traits,
        'total': len(traits)
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print()
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
