#!/usr/bin/env python3
"""
Insert weapon card images into weapon markdown files
Copies generated cards to assets/images/armas/ and adds img tags to weapon files
"""

import os
import re
import shutil
import glob

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'docs')
WEAPONS_DIR = os.path.join(WIKI_PATH, '_equipo', 'armas')
GENERATED_CARDS_DIR = os.path.join(SCRIPT_DIR, 'generated_cards')
TARGET_IMAGES_DIR = os.path.join(WIKI_PATH, 'assets', 'images', 'armas')


def copy_card_images():
    """Copy all generated card images to assets/images/armas/"""
    os.makedirs(TARGET_IMAGES_DIR, exist_ok=True)

    copied = 0
    for category_dir in glob.glob(os.path.join(GENERATED_CARDS_DIR, '*')):
        if os.path.isdir(category_dir):
            for png_file in glob.glob(os.path.join(category_dir, '*.png')):
                filename = os.path.basename(png_file)
                target_path = os.path.join(TARGET_IMAGES_DIR, filename)
                shutil.copy2(png_file, target_path)
                copied += 1

    return copied


def insert_image_tag(filepath):
    """Insert image tag into a weapon markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get the weapon slug from filename
    slug = os.path.basename(filepath).replace('.md', '')
    image_path = f"/assets/images/armas/{slug}.png"

    # Check if image exists
    full_image_path = os.path.join(TARGET_IMAGES_DIR, f"{slug}.png")
    if not os.path.exists(full_image_path):
        return False, "Image not found"

    # Check if image tag already exists
    if 'class="action-card-image"' in content or 'class="weapon-card-image"' in content:
        return False, "Already has image"

    # Find the end of frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, "Invalid frontmatter"

    frontmatter = parts[1]
    body = parts[2]

    # Insert image tag after frontmatter, before the first content
    # The image should go right after the frontmatter
    image_tag = f'\n<img src="{{{{ \'{image_path}\' | relative_url }}}}" class="weapon-card-image" alt="Carta de arma">\n'

    new_content = f"---{frontmatter}---{image_tag}{body}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Image inserted"


def main():
    print("Weapon Card Image Inserter")
    print("=" * 40)
    print()

    # Step 1: Copy images to assets folder
    print("Copying card images to assets/images/armas/...")
    copied = copy_card_images()
    print(f"Copied {copied} images")
    print()

    # Step 2: Insert image tags into weapon files
    print("Inserting image tags into weapon files...")

    # Skip files that shouldn't have cards
    skip_files = ['index.md', 'bala-honda.md', 'dardo-cerbatana.md',
                  'flecha.md', 'virote.md', 'bomba-alquimica.md']

    inserted = 0
    skipped = 0
    errors = []

    for filepath in sorted(glob.glob(os.path.join(WEAPONS_DIR, '*.md'))):
        filename = os.path.basename(filepath)

        if filename in skip_files:
            continue

        success, message = insert_image_tag(filepath)

        if success:
            inserted += 1
            print(f"  + {filename}")
        else:
            skipped += 1
            if message != "Already has image":
                errors.append(f"{filename}: {message}")

    print()
    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")

    if errors:
        print()
        print("Errors:")
        for error in errors:
            print(f"  - {error}")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
