#!/usr/bin/env python3
"""
Split Treasure Vault HTML into chapters
"""

import re
from pathlib import Path

# Define chapter markers
chapters = [
    ('00_Frontmatter', 'bookmark2', 'bookmark6'),
    ('01_Introduction', 'bookmark6', 'bookmark9'),
    ('02_Armor_and_Armaments', 'bookmark9', 'bookmark87'),
    ('03_Alchemy_Unleashed', 'bookmark87', 'bookmark149'),
    ('04_Momentary_Magic', 'bookmark149', 'bookmark206'),
    ('05_Trappings_of_Power', 'bookmark206', 'bookmark313'),
    ('06_Secrets_of_Crafting', 'bookmark313', 'bookmark377'),
    ('07_Gamemasters_Trove', 'bookmark377', 'bookmark457'),
    ('08_Treasure_Tables', 'bookmark457', 'bookmark464'),
    ('09_Glossary_and_Index', 'bookmark464', None),
]

def split_html(input_file, output_dir):
    """Split HTML into chapters"""

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Read HTML
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract HTML header and footer
    head_match = re.search(r'(.*?</head>)', html, re.DOTALL)
    if not head_match:
        print("ERROR: No se encontró el head del HTML")
        return

    html_head = head_match.group(1)

    # Find all bookmark positions
    bookmark_positions = {}
    for match in re.finditer(r'<a name="(bookmark\d+)"', html):
        bookmark = match.group(1)
        pos = match.start()
        bookmark_positions[bookmark] = pos

    print(f"Encontrados {len(bookmark_positions)} bookmarks")

    # Split chapters
    for chapter_name, start_bookmark, end_bookmark in chapters:
        if start_bookmark not in bookmark_positions:
            print(f"WARNING: No se encontró {start_bookmark} para {chapter_name}")
            continue

        start_pos = bookmark_positions[start_bookmark]

        if end_bookmark and end_bookmark in bookmark_positions:
            end_pos = bookmark_positions[end_bookmark]
        else:
            # Last chapter goes to end
            end_pos = html.find('</body>')
            if end_pos == -1:
                end_pos = len(html)

        chapter_content = html[start_pos:end_pos]

        # Create complete HTML file
        chapter_html = f"""<!DOCTYPE html>
<html>
{html_head}
<body>
{chapter_content}
</body>
</html>"""

        output_file = output_dir / f"{chapter_name}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chapter_html)

        print(f"✓ {chapter_name}.html ({len(chapter_content):,} caracteres)")

    print(f"\n✓ Divididos {len(chapters)} capítulos en {output_dir}")


if __name__ == "__main__":
    input_file = "original/treasure_vault/Treasure Vault (Remastered).html"
    output_dir = "original/treasure_vault/chapters_html"

    split_html(input_file, output_dir)
