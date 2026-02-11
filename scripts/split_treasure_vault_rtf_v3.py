#!/usr/bin/env python3
"""
Split Treasure Vault RTF into chapters using line-based detection
"""

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


def find_chapter_lines(text_content):
    """Find chapter start lines in text"""
    lines = text_content.split('\n')

    # Chapter markers with their approximate line numbers (from grep output)
    # Looking for standalone uppercase lines
    chapters = []
    chapter_markers = [
        ('01_Introduction', 'INTO THE VAULT'),
        ('02_Armor_and_Armaments', 'ARMOR & ARMAMENTS'),
        ('03_Alchemy_Unleashed', 'ALCHEMY UNLEASHED'),
        ('04_Momentary_Magic', 'MOMENTARY MAGIC'),
        ('05_Trappings_of_Power', 'TRAPPINGS OF POWER'),
        ('06_Secrets_of_Crafting', 'SECRETS OF CRAFTING'),
        ('07_Gamemasters_Trove', 'ARCHETYPE ARTIFACTS'),  # First section of GM's Trove
        ('08_Treasure_Tables', 'TREASURE TABLES'),
        ('09_Glossary_and_Index', 'GLOSSARY & INDEX'),
    ]

    for chapter_name, marker in chapter_markers:
        if marker:
            # Find first occurrence of marker as a standalone line or prominent heading
            found = False
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped == marker:
                    chapters.append((chapter_name, i, stripped))
                    print(f"Encontrado capítulo en línea {i}: {stripped}")
                    found = True
                    break

            if not found:
                print(f"WARNING: No se encontró '{marker}'")

    return sorted(chapters, key=lambda x: x[1])


def split_rtf_by_lines(input_file, output_dir, chapter_lines, total_lines):
    """Split RTF based on line proportions"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Read RTF as binary
    with open(input_file, 'rb') as f:
        rtf_bytes = f.read()

    total_size = len(rtf_bytes)

    # Calculate byte positions based on line proportions
    chapter_positions = []
    for name, line_num, marker in chapter_lines:
        proportion = line_num / total_lines
        byte_pos = int(proportion * total_size)
        chapter_positions.append((name, byte_pos, marker))
        print(f"{name}: línea {line_num}/{total_lines} = byte {byte_pos:,}/{total_size:,}")

    # Add frontmatter chapter (everything before first chapter)
    if chapter_positions:
        first_byte = chapter_positions[0][1]
        output_file = output_dir / "00_Frontmatter.rtf"
        with open(output_file, 'wb') as f:
            f.write(rtf_bytes[:first_byte])
        print(f"✓ 00_Frontmatter.rtf ({first_byte:,} bytes)")

    # Split chapters
    for i, (name, byte_pos, marker) in enumerate(chapter_positions):
        if i < len(chapter_positions) - 1:
            next_byte = chapter_positions[i + 1][1]
        else:
            next_byte = total_size

        chapter_bytes = rtf_bytes[byte_pos:next_byte]
        output_file = output_dir / f"{name}.rtf"
        with open(output_file, 'wb') as f:
            f.write(chapter_bytes)
        print(f"✓ {name}.rtf ({len(chapter_bytes):,} bytes)")

    print(f"\n✓ Divididos {len(chapter_positions) + 1} capítulos en {output_dir}")


if __name__ == "__main__":
    input_file = "original/treasure_vault/Treasure Vault (Remastered).rtf"
    output_dir = "original/treasure_vault/chapters_rtf"

    print("Convirtiendo RTF a texto...")
    text_content = convert_rtf_to_text(input_file)
    lines = text_content.split('\n')
    total_lines = len(lines)
    print(f"Total de líneas: {total_lines:,}")

    print("\nBuscando capítulos...")
    chapter_lines = find_chapter_lines(text_content)

    print(f"\nDividiendo RTF...")
    split_rtf_by_lines(input_file, output_dir, chapter_lines, total_lines)
