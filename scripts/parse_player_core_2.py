#!/usr/bin/env python3
"""
Parser for Pathfinder 2 Player Core 2 text file.
Converts the plain text extraction into organized markdown files.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configuration
SOURCE_FILE = Path("player_core_2/player_core_2.txt")
OUTPUT_DIR = Path("docs/player_core_2")

# Chapter definitions with page ranges (approximate line numbers based on content)
CHAPTERS = {
    "introduccion": {
        "title": "Introducción",
        "title_en": "Introduction",
        "start_marker": "INTRODUCTION",
        "end_marker": "CHAPTER 1:",
        "order": 0
    },
    "ascendencias": {
        "title": "Ascendencias y Trasfondos",
        "title_en": "Ancestries & Backgrounds",
        "start_marker": "CHAPTER 1:",
        "end_marker": "CHAPTER 2:",
        "order": 1
    },
    "clases": {
        "title": "Clases",
        "title_en": "Classes",
        "start_marker": "CHAPTER 2:",
        "end_marker": "CHAPTER 3:",
        "order": 2
    },
    "arquetipos": {
        "title": "Arquetipos",
        "title_en": "Archetypes",
        "start_marker": "CHAPTER 3:",
        "end_marker": "CHAPTER 4:",
        "order": 3
    },
    "dotes": {
        "title": "Dotes",
        "title_en": "Feats",
        "start_marker": "CHAPTER 4:",
        "end_marker": "CHAPTER 5:",
        "order": 4
    },
    "conjuros": {
        "title": "Conjuros",
        "title_en": "Spells",
        "start_marker": "CHAPTER 5:",
        "end_marker": "CHAPTER 6:",
        "order": 5
    },
    "tesoros": {
        "title": "Tesoros",
        "title_en": "Treasure Trove",
        "start_marker": "CHAPTER 6:",
        "end_marker": "GLOSSARY",
        "order": 6
    },
    "glosario": {
        "title": "Glosario e Índice",
        "title_en": "Glossary & Index",
        "start_marker": "GLOSSARY",
        "end_marker": None,
        "order": 7
    }
}

# Ancestry names mapping (English to Spanish)
ANCESTRIES = {
    "catfolk": {"es": "Gatofolk", "en": "Catfolk"},
    "hobgoblin": {"es": "Hobgoblin", "en": "Hobgoblin"},
    "kholo": {"es": "Kholo", "en": "Kholo"},
    "kobold": {"es": "Kobold", "en": "Kobold"},
    "lizardfolk": {"es": "Lagartino", "en": "Lizardfolk"},
    "ratfolk": {"es": "Ratonero", "en": "Ratfolk"},
    "tengu": {"es": "Tengu", "en": "Tengu"},
    "tripkee": {"es": "Tripkee", "en": "Tripkee"}
}

# Versatile heritages
VERSATILE_HERITAGES = {
    "dhampir": {"es": "Dhampir", "en": "Dhampir"},
    "dragonblood": {"es": "Sangre de Dragón", "en": "Dragonblood"},
    "duskwalker": {"es": "Caminante del Crepúsculo", "en": "Duskwalker"}
}

# Class names mapping
CLASSES = {
    "alchemist": {"es": "Alquimista", "en": "Alchemist"},
    "barbarian": {"es": "Bárbaro", "en": "Barbarian"},
    "champion": {"es": "Campeón", "en": "Champion"},
    "investigator": {"es": "Investigador", "en": "Investigator"},
    "monk": {"es": "Monje", "en": "Monk"},
    "oracle": {"es": "Oráculo", "en": "Oracle"},
    "sorcerer": {"es": "Hechicero", "en": "Sorcerer"},
    "swashbuckler": {"es": "Espadachín", "en": "Swashbuckler"}
}

# Navigation sidebar pattern to remove
NAV_SIDEBAR_PATTERN = re.compile(
    r'Introduction\nAncestries &\nBackgrounds.*?Glossary & Index',
    re.DOTALL
)

# Page number pattern
PAGE_NUM_PATTERN = re.compile(r'^Player Core 2\n\d+$', re.MULTILINE)
PAGE_FOOTER_PATTERN = re.compile(r'^(Classes|Ancestries & Backgrounds|Archetypes|Feats|Spells|Treasure Trove) \d+$', re.MULTILINE)


def read_source_file() -> str:
    """Read the source text file."""
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def clean_text(text: str) -> str:
    """Clean up the text by removing navigation sidebars and page numbers."""
    # Remove navigation sidebars
    text = NAV_SIDEBAR_PATTERN.sub('', text)

    # Remove page numbers
    text = PAGE_NUM_PATTERN.sub('', text)
    text = PAGE_FOOTER_PATTERN.sub('', text)

    # Remove repeated "Player Core 2" markers
    text = re.sub(r'\nPlayer Core 2\n', '\n', text)

    # Clean up multiple blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    return text


def find_section_markers(text: str, start_marker: str, end_marker: Optional[str]) -> Tuple[int, int]:
    """Find the start and end positions of a section."""
    start_pos = text.find(start_marker)
    if start_pos == -1:
        return -1, -1

    if end_marker:
        end_pos = text.find(end_marker, start_pos + len(start_marker))
        if end_pos == -1:
            end_pos = len(text)
    else:
        end_pos = len(text)

    return start_pos, end_pos


def extract_ancestry(text: str, ancestry_name: str, next_ancestry: Optional[str] = None) -> str:
    """Extract content for a specific ancestry."""
    # Find the ancestry heading (uppercase)
    pattern = rf'\n{ancestry_name.upper()}\n'
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        # Try alternative pattern
        pattern = rf'^{ancestry_name}$'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)

    if not match:
        return ""

    start_pos = match.start()

    # Find the end (next ancestry or end of section)
    if next_ancestry:
        next_pattern = rf'\n{next_ancestry.upper()}\n'
        next_match = re.search(next_pattern, text[start_pos + 100:], re.IGNORECASE)
        if next_match:
            end_pos = start_pos + 100 + next_match.start()
        else:
            end_pos = len(text)
    else:
        end_pos = len(text)

    return text[start_pos:end_pos].strip()


def extract_class(text: str, class_name: str, next_class: Optional[str] = None) -> str:
    """Extract content for a specific class."""
    # Classes often start with a description like "The alchemist..."
    # Or with "ALCHEMIST" as a heading
    pattern = rf'\b{class_name}\b'

    # Find the main class entry
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    if not matches:
        return ""

    # Usually the first significant mention is the start
    start_pos = matches[0].start()

    # Go back to find the actual start of the section
    section_start = text.rfind('\n\n', 0, start_pos)
    if section_start != -1:
        start_pos = section_start

    # Find end
    if next_class:
        next_pattern = rf'^\s*{next_class}\s*$'
        next_match = re.search(next_pattern, text[start_pos + 1000:], re.IGNORECASE | re.MULTILINE)
        if next_match:
            end_pos = start_pos + 1000 + next_match.start()
        else:
            end_pos = len(text)
    else:
        end_pos = len(text)

    return text[start_pos:end_pos].strip()


def text_to_markdown(text: str, title: str) -> str:
    """Convert plain text to markdown format."""
    lines = text.split('\n')
    md_lines = []

    # Add front matter
    md_lines.append('---')
    md_lines.append(f'title: "{title}"')
    md_lines.append('---')
    md_lines.append('')

    in_list = False
    prev_line_empty = True

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip empty lines but track them
        if not stripped:
            if not prev_line_empty:
                md_lines.append('')
                prev_line_empty = True
            continue

        prev_line_empty = False

        # Detect headers (ALL CAPS lines that are short)
        if stripped.isupper() and len(stripped) < 60 and not stripped.startswith('•'):
            # Check if it's a main section header
            if len(stripped.split()) <= 4:
                md_lines.append(f'\n## {stripped.title()}\n')
                continue

        # Detect feat/ability headers (NAME [action] FEAT X pattern)
        feat_match = re.match(r'^([A-Z][A-Z\s\'-]+)\s*(\[[^\]]+\])?\s*(FEAT \d+)?$', stripped)
        if feat_match:
            feat_name = feat_match.group(1).strip().title()
            action = feat_match.group(2) or ''
            level = feat_match.group(3) or ''
            md_lines.append(f'\n### {feat_name} {action} {level}\n'.strip())
            continue

        # Detect level headers (1ST LEVEL, 5TH LEVEL, etc.)
        if re.match(r'^\d+(ST|ND|RD|TH) LEVEL$', stripped):
            md_lines.append(f'\n## Nivel {stripped.split()[0]}\n')
            continue

        # Detect bullet points
        if stripped.startswith('•'):
            md_lines.append(f'- {stripped[1:].strip()}')
            in_list = True
            continue

        # Detect trait blocks (RARITY, HIT POINTS, etc.)
        if stripped in ['RARITY', 'HIT POINTS', 'SIZE', 'SPEED', 'ATTRIBUTE BOOSTS',
                        'ATTRIBUTE FLAW', 'LANGUAGES', 'TRAITS']:
            md_lines.append(f'\n**{stripped.title()}**')
            continue

        # Regular paragraph
        md_lines.append(stripped)

    return '\n'.join(md_lines)


def create_ancestry_files(text: str, output_dir: Path):
    """Create markdown files for each ancestry."""
    ancestries_dir = output_dir / "01-ascendencias"
    ancestries_dir.mkdir(parents=True, exist_ok=True)

    ancestry_list = list(ANCESTRIES.keys())

    for i, ancestry in enumerate(ancestry_list):
        next_ancestry = ancestry_list[i + 1] if i + 1 < len(ancestry_list) else None
        content = extract_ancestry(text, ancestry, next_ancestry)

        if content:
            ancestry_dir = ancestries_dir / ancestry
            ancestry_dir.mkdir(exist_ok=True)

            # Create main description file
            info = ANCESTRIES[ancestry]
            md_content = text_to_markdown(content, info['en'])

            with open(ancestry_dir / "descripcion.md", 'w', encoding='utf-8') as f:
                f.write(md_content)

            print(f"  Created: {ancestry_dir}/descripcion.md")


def create_heritage_files(text: str, output_dir: Path):
    """Create markdown files for versatile heritages."""
    heritages_dir = output_dir / "01-ascendencias" / "herencias-versatiles"
    heritages_dir.mkdir(parents=True, exist_ok=True)

    heritage_list = list(VERSATILE_HERITAGES.keys())

    for i, heritage in enumerate(heritage_list):
        next_heritage = heritage_list[i + 1] if i + 1 < len(heritage_list) else None

        # Find heritage content
        pattern = rf'{heritage}'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = text.rfind('\n\n', 0, match.start())
            if next_heritage:
                next_match = re.search(next_heritage, text[match.end():], re.IGNORECASE)
                end = match.end() + next_match.start() if next_match else len(text)
            else:
                # Find "Common Backgrounds" as the end
                end_match = re.search(r'COMMON BACKGROUNDS', text[match.end():], re.IGNORECASE)
                end = match.end() + end_match.start() if end_match else len(text)

            content = text[start:end].strip()
            if content:
                info = VERSATILE_HERITAGES[heritage]
                md_content = text_to_markdown(content, info['en'])

                with open(heritages_dir / f"{heritage}.md", 'w', encoding='utf-8') as f:
                    f.write(md_content)

                print(f"  Created: {heritages_dir}/{heritage}.md")


def create_class_files(text: str, output_dir: Path):
    """Create markdown files for each class."""
    classes_dir = output_dir / "02-clases"
    classes_dir.mkdir(parents=True, exist_ok=True)

    class_list = list(CLASSES.keys())

    for i, cls in enumerate(class_list):
        next_cls = class_list[i + 1] if i + 1 < len(class_list) else None

        # Each class has a substantial section
        # Find class by looking for the class name followed by class-specific content
        pattern = rf'(?:^|\n){cls.upper()}\n'
        matches = list(re.finditer(pattern, text, re.IGNORECASE))

        if matches:
            # Use the match that's in the classes chapter
            for match in matches:
                context = text[max(0, match.start()-100):match.start()]
                if 'Classes' in context or match.start() > len(text) * 0.1:
                    start = match.start()
                    break
            else:
                start = matches[0].start()

            # Find end
            if next_cls:
                next_pattern = rf'(?:^|\n){next_cls.upper()}\n'
                next_match = re.search(next_pattern, text[start + 500:], re.IGNORECASE)
                end = start + 500 + next_match.start() if next_match else len(text)
            else:
                # End at FAMILIARS or next chapter
                end_match = re.search(r'(?:^|\n)FAMILIARS\n', text[start + 500:], re.IGNORECASE)
                if not end_match:
                    end_match = re.search(r'CHAPTER 3:', text[start + 500:])
                end = start + 500 + end_match.start() if end_match else len(text)

            content = text[start:end].strip()
            if content and len(content) > 500:  # Classes should have substantial content
                class_dir = classes_dir / cls
                class_dir.mkdir(exist_ok=True)

                info = CLASSES[cls]
                md_content = text_to_markdown(content, info['en'])

                with open(class_dir / "descripcion.md", 'w', encoding='utf-8') as f:
                    f.write(md_content)

                print(f"  Created: {class_dir}/descripcion.md")


def create_backgrounds_file(text: str, output_dir: Path):
    """Create markdown file for backgrounds."""
    backgrounds_dir = output_dir / "01-ascendencias"
    backgrounds_dir.mkdir(parents=True, exist_ok=True)

    # Find Common Backgrounds section
    start_match = re.search(r'COMMON BACKGROUNDS', text, re.IGNORECASE)
    if start_match:
        start = start_match.start()

        # Find end at Rare Backgrounds or Chapter 2
        end_match = re.search(r'CHAPTER 2:', text[start:])
        end = start + end_match.start() if end_match else len(text)

        content = text[start:end].strip()
        if content:
            md_content = text_to_markdown(content, "Trasfondos")

            with open(backgrounds_dir / "trasfondos.md", 'w', encoding='utf-8') as f:
                f.write(md_content)

            print(f"  Created: {backgrounds_dir}/trasfondos.md")


def create_archetypes_file(text: str, output_dir: Path):
    """Create markdown files for archetypes chapter."""
    archetypes_dir = output_dir / "03-arquetipos"
    archetypes_dir.mkdir(parents=True, exist_ok=True)

    # Find archetypes chapter
    start_match = re.search(r'CHAPTER 3:', text)
    end_match = re.search(r'CHAPTER 4:', text)

    if start_match and end_match:
        content = text[start_match.start():end_match.start()].strip()
        md_content = text_to_markdown(content, "Arquetipos")

        with open(archetypes_dir / "introduccion.md", 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"  Created: {archetypes_dir}/introduccion.md")


def create_feats_file(text: str, output_dir: Path):
    """Create markdown files for feats chapter."""
    feats_dir = output_dir / "04-dotes"
    feats_dir.mkdir(parents=True, exist_ok=True)

    # Find feats chapter
    start_match = re.search(r'CHAPTER 4:', text)
    end_match = re.search(r'CHAPTER 5:', text)

    if start_match and end_match:
        content = text[start_match.start():end_match.start()].strip()
        md_content = text_to_markdown(content, "Dotes")

        with open(feats_dir / "dotes.md", 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"  Created: {feats_dir}/dotes.md")


def create_spells_file(text: str, output_dir: Path):
    """Create markdown files for spells chapter."""
    spells_dir = output_dir / "05-conjuros"
    spells_dir.mkdir(parents=True, exist_ok=True)

    # Find spells chapter
    start_match = re.search(r'CHAPTER 5:', text)
    end_match = re.search(r'CHAPTER 6:', text)

    if start_match and end_match:
        content = text[start_match.start():end_match.start()].strip()

        # Split into spell lists, spells, focus spells, rituals
        spell_lists_match = re.search(r'Spell Lists', content, re.IGNORECASE)
        spells_match = re.search(r'(?:^|\n)Spells\n', content, re.IGNORECASE)
        focus_match = re.search(r'Focus Spells', content, re.IGNORECASE)
        rituals_match = re.search(r'Rituals', content, re.IGNORECASE)

        # Create introduction
        if spell_lists_match:
            intro_content = content[:spell_lists_match.start()].strip()
            md_content = text_to_markdown(intro_content, "Introducción a los Conjuros")
            with open(spells_dir / "introduccion.md", 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"  Created: {spells_dir}/introduccion.md")

        # Create full chapter file
        md_content = text_to_markdown(content, "Conjuros")
        with open(spells_dir / "conjuros.md", 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  Created: {spells_dir}/conjuros.md")


def create_treasure_file(text: str, output_dir: Path):
    """Create markdown files for treasure chapter."""
    treasure_dir = output_dir / "06-tesoros"
    treasure_dir.mkdir(parents=True, exist_ok=True)

    # Find treasure chapter
    start_match = re.search(r'CHAPTER 6:', text)
    end_match = re.search(r'(?:GLOSSARY|Glossary & Index)', text)

    if start_match:
        end = end_match.start() if end_match else len(text)
        content = text[start_match.start():end].strip()
        md_content = text_to_markdown(content, "Tesoros")

        with open(treasure_dir / "tesoros.md", 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"  Created: {treasure_dir}/tesoros.md")


def create_glossary_file(text: str, output_dir: Path):
    """Create markdown file for glossary."""
    glossary_dir = output_dir / "07-glosario"
    glossary_dir.mkdir(parents=True, exist_ok=True)

    # Find glossary
    start_match = re.search(r'(?:GLOSSARY|Glossary & Index)', text)

    if start_match:
        content = text[start_match.start():].strip()
        md_content = text_to_markdown(content, "Glosario e Índice")

        with open(glossary_dir / "glosario.md", 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"  Created: {glossary_dir}/glosario.md")


def create_index_files(output_dir: Path):
    """Create index files for each chapter."""
    chapters = [
        ("01-ascendencias", "Ascendencias y Trasfondos", "Nuevas ascendencias del Player Core 2"),
        ("02-clases", "Clases", "Las ocho clases del Player Core 2"),
        ("03-arquetipos", "Arquetipos", "Arquetipos de multiclase y especializaciones"),
        ("04-dotes", "Dotes", "Dotes generales y de habilidad adicionales"),
        ("05-conjuros", "Conjuros", "Nuevos conjuros, conjuros de foco y rituales"),
        ("06-tesoros", "Tesoros", "Armas, armaduras, alquimia y objetos mágicos"),
        ("07-glosario", "Glosario", "Términos y referencias del Player Core 2"),
    ]

    for dirname, title, description in chapters:
        chapter_dir = output_dir / dirname
        if chapter_dir.exists():
            index_content = f"""---
title: "{title}"
description: "{description}"
---

# {title}

{description}

"""
            with open(chapter_dir / "index.md", 'w', encoding='utf-8') as f:
                f.write(index_content)

            print(f"  Created: {chapter_dir}/index.md")


def main():
    print("=" * 60)
    print("Pathfinder 2 Player Core 2 - Parser")
    print("=" * 60)
    print(f"Source: {SOURCE_FILE}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    if not SOURCE_FILE.exists():
        print(f"ERROR: Source file not found: {SOURCE_FILE}")
        return

    # Read and clean the source file
    print("Reading source file...")
    raw_text = read_source_file()
    print(f"  Read {len(raw_text):,} characters")

    print("\nCleaning text...")
    text = clean_text(raw_text)
    print(f"  Cleaned to {len(text):,} characters")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Process each section
    print("\nProcessing Ancestries...")
    create_ancestry_files(text, OUTPUT_DIR)

    print("\nProcessing Versatile Heritages...")
    create_heritage_files(text, OUTPUT_DIR)

    print("\nProcessing Backgrounds...")
    create_backgrounds_file(text, OUTPUT_DIR)

    print("\nProcessing Classes...")
    create_class_files(text, OUTPUT_DIR)

    print("\nProcessing Archetypes...")
    create_archetypes_file(text, OUTPUT_DIR)

    print("\nProcessing Feats...")
    create_feats_file(text, OUTPUT_DIR)

    print("\nProcessing Spells...")
    create_spells_file(text, OUTPUT_DIR)

    print("\nProcessing Treasure...")
    create_treasure_file(text, OUTPUT_DIR)

    print("\nProcessing Glossary...")
    create_glossary_file(text, OUTPUT_DIR)

    print("\nCreating index files...")
    create_index_files(OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("Parsing complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
