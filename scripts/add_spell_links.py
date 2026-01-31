#!/usr/bin/env python3
"""
Convert spell names in list files to internal links pointing to individual spell pages.
Handles two formats:
  Format 1 (arcana, etc): - **Spell Name P** - Description
  Format 2 (divina, etc): - **Spell NameP** Description (no space before P, no dash separator)
"""

import re
import os
import unicodedata
from pathlib import Path

def remove_accents(text):
    """Remove accents from text for URL slug."""
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

def spell_to_slug(spell_name):
    """Convert spell name to URL slug format (unaccented, lowercase, hyphens)."""
    # Remove accents first
    spell = remove_accents(spell_name)

    # Convert to lowercase
    slug = spell.lower()

    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)

    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)

    # Remove leading/trailing hyphens
    slug = slug.strip('-')

    return slug

def process_list_file(file_path):
    """Process a spell list file and convert spell names to links."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    updated_lines = []

    for line in lines:
        # Check for Format 1: - **Spell Name P** - Description
        match1 = re.match(r'^- \*\*([^*]+)\*\* - (.*)$', line)
        if match1:
            spell_text = match1.group(1)
            description = match1.group(2)

            # Extract spell name and P/PC indicator
            spell_name = spell_text.strip()
            indicator = ''

            # Check for P or PC at the end (with potential space before)
            if ' P' in spell_name or ', P' in spell_name:
                if spell_name.endswith(' P'):
                    indicator = ' P'
                    spell_name = spell_name[:-2].strip()
                elif ', P' in spell_name:
                    parts = spell_name.rsplit(', P', 1)
                    spell_name = parts[0].strip()
                    indicator = ', P'
            elif ' PC' in spell_name or ', PC' in spell_name:
                if spell_name.endswith(' PC'):
                    indicator = ' PC'
                    spell_name = spell_name[:-3].strip()
                elif ', PC' in spell_name:
                    parts = spell_name.rsplit(', PC', 1)
                    spell_name = parts[0].strip()
                    indicator = ', PC'

            # Create slug and build link
            slug = spell_to_slug(spell_name)
            new_line = f'- **[{spell_name}](/conjuros/{slug}/){indicator}** - {description}'
            updated_lines.append(new_line)
        else:
            # Check for Format 2: - **Spell NameP** Description (no space before P, no dash)
            match2 = re.match(r'^- \*\*([^*]+)\*\* (.*)$', line)
            if match2:
                spell_text = match2.group(1)
                description = match2.group(2)

                # Extract spell name and P/PC indicator (attached directly, no space)
                spell_name = spell_text.strip()
                indicator = ''

                # Check if ends with P or PC (no space before)
                if spell_name.endswith('P'):
                    # Check if it's actually PC
                    if spell_name.endswith('PC'):
                        indicator = 'PC'
                        spell_name = spell_name[:-2].strip()
                    else:
                        indicator = 'P'
                        spell_name = spell_name[:-1].strip()

                # Create slug and build link
                slug = spell_to_slug(spell_name)
                new_line = f'- **[{spell_name}](/conjuros/{slug}/) {indicator}** {description}'
                updated_lines.append(new_line)
            else:
                # Not a spell entry, keep as-is
                updated_lines.append(line)

    updated_content = '\n'.join(updated_lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✓ Processed: {file_path}")

# Process all 4 spell list files
list_files = [
    '/Users/ludo/code/pf2/docs/_conjuros/listas/arcana.md',
    '/Users/ludo/code/pf2/docs/_conjuros/listas/divina.md',
    '/Users/ludo/code/pf2/docs/_conjuros/listas/oculta.md',
    '/Users/ludo/code/pf2/docs/_conjuros/listas/primigenia.md'
]

for file_path in list_files:
    if os.path.exists(file_path):
        process_list_file(file_path)
    else:
        print(f"✗ File not found: {file_path}")

print("\nAll spell list files updated with internal links!")
