#!/usr/bin/env python3
"""
Test markitdown conversion on Treasure Vault RTF chapters
"""

from markitdown import MarkItDown
from pathlib import Path

# Initialize MarkItDown
md = MarkItDown()

# Test with Introduction chapter
input_file = "original/treasure_vault/chapters_rtf/01_Introduction.rtf"
output_file = "original/treasure_vault/test_introduction.md"

print(f"Converting {input_file} to markdown...")

# Convert RTF to markdown
result = md.convert(input_file)

# Save to file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(result.text_content)

print(f"✓ Converted to {output_file}")
print(f"  File size: {len(result.text_content):,} characters")
print(f"\nFirst 500 characters:")
print(result.text_content[:500])
