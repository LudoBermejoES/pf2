#!/usr/bin/env python3
"""
Insert card images into item markdown files
Adds the spell-card-image tag to each item file
"""

import os
import re
import glob

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
ITEMS_DIR = os.path.join(WIKI_PATH, '_equipo', 'objetos')
IMAGES_DIR = os.path.join(WIKI_PATH, 'assets', 'images', 'objetos')


def insert_card_image(filepath):
    """Insert card image reference into a markdown file"""
    filename = os.path.basename(filepath)
    item_id = filename.replace('.md', '')

    # Check if image exists
    image_path = os.path.join(IMAGES_DIR, f"{item_id}.png")
    if not os.path.exists(image_path):
        return False, "Image not found"

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if image already inserted
    if 'spell-card-image' in content:
        return False, "Already has image"

    # Find the end of frontmatter (second ---)
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, "Invalid frontmatter"

    # Build new content with image after frontmatter
    image_tag = f'<img src="{{{{ \'/assets/images/objetos/{item_id}.png\' | relative_url }}}}" class="spell-card-image" alt="Carta de objeto">\n\n'

    new_content = f"---{parts[1]}---\n{image_tag}{parts[2].lstrip()}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Image inserted"


def main():
    """Main function to insert images into all item files"""
    print("Insert Item Card Images")
    print("=" * 40)
    print()

    # Find all item files
    item_files = glob.glob(os.path.join(ITEMS_DIR, '*.md'))

    # Filter out special files
    skip_files = ['index.md']
    item_files = [f for f in item_files if os.path.basename(f) not in skip_files]

    print(f"Found {len(item_files)} item files")
    print()

    inserted = 0
    skipped = 0
    errors = 0

    for filepath in sorted(item_files):
        filename = os.path.basename(filepath)
        try:
            success, message = insert_card_image(filepath)
            if success:
                print(f"  ✓ {filename}: {message}")
                inserted += 1
            else:
                print(f"  - {filename}: {message}")
                skipped += 1
        except Exception as e:
            print(f"  ✗ {filename}: Error - {e}")
            errors += 1

    print()
    print(f"✓ Inserted: {inserted}")
    print(f"- Skipped: {skipped}")
    if errors:
        print(f"✗ Errors: {errors}")


if __name__ == "__main__":
    main()
