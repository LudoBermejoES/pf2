#!/usr/bin/env python3
"""
Convert Treasure Vault HTML chapters to Markdown using markitdown
"""

from markitdown import MarkItDown
from pathlib import Path

def convert_html_chapters(input_dir, output_dir):
    """Convert all HTML chapters to markdown"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Initialize MarkItDown
    md = MarkItDown()

    # Get all HTML files
    html_files = sorted(input_dir.glob("*.html"))

    for html_file in html_files:
        # Generate output filename
        output_file = output_dir / f"{html_file.stem}.md"

        print(f"Converting {html_file.name}...")

        try:
            # Convert HTML to markdown
            result = md.convert(str(html_file))

            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)

            print(f"✓ {output_file.name} ({len(result.text_content):,} characters)")

        except Exception as e:
            print(f"✗ Error converting {html_file.name}: {e}")

    print(f"\n✓ Conversion complete. Files saved to {output_dir}")


if __name__ == "__main__":
    input_dir = "original/treasure_vault/chapters_html"
    output_dir = "docs/treasure_vault_md"

    convert_html_chapters(input_dir, output_dir)
