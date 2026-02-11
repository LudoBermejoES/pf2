#!/usr/bin/env python3
"""
Split Treasure Vault RTF into chapters
"""

import re
from pathlib import Path


# Define chapter markers - we'll search for these titles in the RTF
# Using the exact text from the RTF content
chapters = [
    ('00_Frontmatter', None, 'Introduction: Into the Vault'),
    ('01_Introduction', 'Introduction: Into the Vault', 'Armor & Armaments'),
    ('02_Armor_and_Armaments', 'Armor & Armaments', 'Alchemy Unleashed'),
    ('03_Alchemy_Unleashed', 'Alchemy Unleashed', 'Momentary Magic'),
    ('04_Momentary_Magic', 'Momentary Magic', 'Trappings of Power'),
    ('05_Trappings_of_Power', 'Trappings of Power', 'Secrets of Crafting'),
    ('06_Secrets_of_Crafting', 'Secrets of Crafting', "Gamemaster's Trove"),
    ('07_Gamemasters_Trove', "Gamemaster's Trove", 'Treasure Tables'),
    ('08_Treasure_Tables', 'Treasure Tables', 'Glossary & Index'),
    ('09_Glossary_and_Index', 'Glossary & Index', None),
]


def find_text_position(rtf_content, search_text):
    """Find position of text in RTF content"""
    # RTF encodes text with control codes, so we need to search carefully
    # Convert search text to find it in RTF format
    pos = rtf_content.find(search_text)
    return pos


def split_rtf(input_file, output_dir):
    """Split RTF into chapters"""

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Read RTF
    with open(input_file, 'r', encoding='utf-8') as f:
        rtf_content = f.read()

    # Extract RTF header (everything up to first chapter)
    # Find the start of document content after the preamble
    header_end = rtf_content.find('\\pard')
    if header_end == -1:
        print("ERROR: No se encontró el inicio del contenido RTF")
        return

    rtf_header = rtf_content[:header_end]

    # Find all chapter positions
    chapter_positions = {}
    for chapter_name, start_marker, end_marker in chapters:
        if start_marker is None:
            # First chapter starts at beginning of content
            chapter_positions[chapter_name] = (0, start_marker, end_marker)
        else:
            pos = find_text_position(rtf_content, start_marker)
            if pos != -1:
                chapter_positions[chapter_name] = (pos, start_marker, end_marker)
                print(f"Encontrado '{start_marker}' en posición {pos}")
            else:
                print(f"WARNING: No se encontró '{start_marker}' para {chapter_name}")

    # Split chapters
    for chapter_name, start_marker, end_marker in chapters:
        if chapter_name not in chapter_positions:
            continue

        start_pos, _, _ = chapter_positions[chapter_name]

        # Find end position
        if end_marker:
            end_pos = find_text_position(rtf_content, end_marker)
            if end_pos == -1:
                print(f"WARNING: No se encontró el marcador final '{end_marker}' para {chapter_name}")
                end_pos = len(rtf_content) - 10  # End before closing braces
        else:
            # Last chapter - go to end but remove closing braces
            end_pos = rtf_content.rfind('}')
            if end_pos == -1:
                end_pos = len(rtf_content)

        # Extract chapter content
        if start_pos == 0:
            # Frontmatter - include full header
            chapter_content = rtf_content[:end_pos]
        else:
            # Other chapters - create new RTF with header + content
            content_section = rtf_content[start_pos:end_pos]
            chapter_content = rtf_header + content_section

        # Close RTF properly
        if not chapter_content.rstrip().endswith('}'):
            chapter_content += '\n}'

        # Save chapter file
        output_file = output_dir / f"{chapter_name}.rtf"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chapter_content)

        print(f"✓ {chapter_name}.rtf ({len(chapter_content):,} caracteres)")

    print(f"\n✓ Divididos {len(chapter_positions)} capítulos en {output_dir}")


if __name__ == "__main__":
    input_file = "original/treasure_vault/Treasure Vault (Remastered).rtf"
    output_dir = "original/treasure_vault/chapters_rtf"

    split_rtf(input_file, output_dir)
