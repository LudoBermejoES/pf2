#!/usr/bin/env python3
"""
Split Treasure Vault RTF into chapters using page breaks
"""

import re
from pathlib import Path
import subprocess


def convert_rtf_to_text(rtf_file):
    """Convert RTF to plain text using textutil"""
    result = subprocess.run(
        ['textutil', '-convert', 'txt', '-stdout', rtf_file],
        capture_output=True,
        text=True
    )
    return result.stdout


def find_chapter_pages(text_content):
    """Find approximate page breaks in text"""
    # Look for chapter titles with their page numbers from TOC
    chapters_info = [
        ('00_Frontmatter', 0, 'Introduction: Into the Vault'),
        ('01_Introduction', None, 'INTO THE VAULT'),
        ('02_Armor_and_Armaments', None, 'Armor & Armaments'),
        ('03_Alchemy_Unleashed', None, 'Alchemy Unleashed'),
        ('04_Momentary_Magic', None, 'Momentary Magic'),
        ('05_Trappings_of_Power', None, 'Trappings of Power'),
        ('06_Secrets_of_Crafting', None, 'Secrets of Crafting'),
        ('07_Gamemasters_Trove', None, "Gamemaster's Trove"),
        ('08_Treasure_Tables', None, 'Treasure Tables'),
        ('09_Glossary_and_Index', None, 'Glossary & Index'),
    ]

    positions = []
    for name, _, marker in chapters_info:
        if marker:
            # Find the marker in text
            # Look for the section header pattern
            pattern = re.compile(re.escape(marker), re.IGNORECASE)
            match = pattern.search(text_content)
            if match:
                pos = match.start()
                positions.append((name, marker, pos))
                print(f"Encontrado '{marker}' en posición de texto {pos}")
            else:
                print(f"WARNING: No se encontró '{marker}' en el texto")

    return positions


def split_rtf_by_percentage(input_file, output_dir, text_positions):
    """Split RTF based on text position percentages"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Read RTF as binary
    with open(input_file, 'rb') as f:
        rtf_bytes = f.read()

    total_size = len(rtf_bytes)

    # Get text version to calculate percentages
    text_content = convert_rtf_to_text(input_file)
    text_size = len(text_content)

    # Sort positions
    sorted_positions = sorted(text_positions, key=lambda x: x[2])

    # Split RTF based on proportional positions
    prev_name = '00_Frontmatter'
    prev_pos_bytes = 0

    for i, (name, marker, text_pos) in enumerate(sorted_positions):
        # Calculate proportional position in RTF bytes
        proportion = text_pos / text_size
        rtf_pos = int(proportion * total_size)

        # Extract this chapter
        if i > 0:
            # Save previous chapter
            chapter_bytes = rtf_bytes[prev_pos_bytes:rtf_pos]
            output_file = output_dir / f"{prev_name}.rtf"
            with open(output_file, 'wb') as f:
                f.write(chapter_bytes)
            print(f"✓ {prev_name}.rtf ({len(chapter_bytes):,} bytes)")

        prev_name = name
        prev_pos_bytes = rtf_pos

    # Save last chapter
    chapter_bytes = rtf_bytes[prev_pos_bytes:]
    output_file = output_dir / f"{prev_name}.rtf"
    with open(output_file, 'wb') as f:
        f.write(chapter_bytes)
    print(f"✓ {prev_name}.rtf ({len(chapter_bytes):,} bytes)")

    # Save frontmatter
    chapter_bytes = rtf_bytes[:sorted_positions[0][2] if sorted_positions else total_size]
    output_file = output_dir / "00_Frontmatter.rtf"
    with open(output_file, 'wb') as f:
        f.write(chapter_bytes)
    print(f"✓ 00_Frontmatter.rtf ({len(chapter_bytes):,} bytes)")


if __name__ == "__main__":
    input_file = "original/treasure_vault/Treasure Vault (Remastered).rtf"
    output_dir = "original/treasure_vault/chapters_rtf"

    print("Convirtiendo RTF a texto...")
    text_content = convert_rtf_to_text(input_file)

    print("\nBuscando posiciones de capítulos...")
    text_positions = find_chapter_pages(text_content)

    print(f"\nDividiendo RTF en {len(text_positions) + 1} capítulos...")
    split_rtf_by_percentage(input_file, output_dir, text_positions)

    print(f"\n✓ Completado en {output_dir}")
