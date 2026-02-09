#!/usr/bin/env python3
"""
PF2e Trait Cards Generator
Generates Magic-sized trait cards for Pathfinder 2e
Includes trait name, type badge, description and subsections
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json
import textwrap
import re

# Card specifications (300 DPI for print quality)
# Magic card size: 63mm x 88mm
CARD_WIDTH = 744    # 63mm at 300 DPI
CARD_HEIGHT = 1039  # 88mm at 300 DPI
SAFE_ZONE = 24      # 2mm safe zone
CORNER_RADIUS = 30  # 2.5mm rounded corners
BORDER_WIDTH = 8    # Border thickness

# Colors (RGB) - Warm parchment theme for traits
COLOR_BACKGROUND = (244, 228, 201)      # Parchment #f4e4c9
COLOR_BORDER = (125, 68, 55)            # PF red #7d4437
COLOR_TRAIT_BG = (93, 48, 48)           # Darker red for trait name box
COLOR_TRAIT_TEXT = (218, 165, 32)       # Gold text on traits
COLOR_TEXT = (45, 39, 34)               # Dark text #2d2722
COLOR_TITLE = (125, 68, 55)             # Red for title
COLOR_SEPARATOR = (125, 68, 55)         # Red for lines
COLOR_LABEL = (125, 68, 55)             # Red for labels
COLOR_TYPE_BG = (235, 220, 195)         # Lighter parchment for type box
COLOR_SUBSECTION_BG = (250, 240, 220)   # Light cream for subsection headers

# Trait type colors - color-coded badges
TRAIT_TYPE_COLORS = {
    'general':      (100, 80, 60),       # Brown
    'acción':       (60, 100, 140),      # Blue
    'accion':       (60, 100, 140),      # Blue (without accent)
    'clase':        (140, 60, 80),       # Crimson
    'ascendencia':  (60, 120, 80),       # Green
    'criatura':     (120, 80, 40),       # Dark amber
    'efecto':       (100, 50, 120),      # Purple
    'magia':        (80, 60, 140),       # Indigo
    'equipo':       (80, 100, 80),       # Olive
    'tradición':    (140, 100, 40),      # Gold
    'tradicion':    (140, 100, 40),      # Gold (without accent)
    'conjuro':      (100, 50, 120),      # Purple (same as magic)
    'alquimia':     (60, 120, 100),      # Teal
    'emocion':      (160, 60, 60),       # Red
    'veneno':       (80, 120, 40),       # Lime green
    'daño':         (160, 40, 40),       # Dark red
    'dote':         (100, 80, 60),       # Brown (same as general)
    'arma':         (80, 80, 100),       # Steel gray
    'elemental':    (40, 100, 140),      # Cerulean
    'material':     (140, 120, 60),      # Mustard
    'frecuencia':   (100, 100, 100),     # Gray
    'alineamiento': (140, 100, 40),      # Gold
    'arquetipo':    (100, 60, 100),      # Plum
    'peligro':      (160, 80, 40),       # Orange
}

# Trait type display names
TRAIT_TYPE_NAMES = {
    'general': 'General',
    'acción': 'Acción',
    'accion': 'Acción',
    'clase': 'Clase',
    'ascendencia': 'Ascendencia',
    'criatura': 'Criatura',
    'efecto': 'Efecto',
    'magia': 'Magia',
    'equipo': 'Equipo',
    'tradición': 'Tradición',
    'tradicion': 'Tradición',
    'conjuro': 'Conjuro',
    'alquimia': 'Alquimia',
    'emocion': 'Emoción',
    'veneno': 'Veneno',
    'daño': 'Daño',
    'dote': 'Dote',
    'arma': 'Arma',
    'elemental': 'Elemental',
    'material': 'Material',
    'frecuencia': 'Frecuencia',
    'alineamiento': 'Alineamiento',
    'arquetipo': 'Arquetipo',
    'peligro': 'Peligro',
}

# Layout
TITLE_Y = SAFE_ZONE + 12
TRAIT_HEIGHT = 32
TRAIT_PADDING = 8
LINE_HEIGHT = 28
SECTION_SPACING = 8

# Font sizes
TITLE_FONT_SIZE = 44
BODY_FONT_SIZE = 24
TYPE_FONT_SIZE = 22
LABEL_FONT_SIZE = 20
SMALL_FONT_SIZE = 14
SUBSECTION_FONT_SIZE = 22

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, '..', 'spellCardCreator', 'assets', 'fonts')
DATA_FILE = os.path.join(SCRIPT_DIR, 'data', 'traits.json')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'generated_cards')


def get_font(size, bold=False, display=False):
    """Load a font with fallback options"""
    if display:
        if bold:
            font_paths = [
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-Bold.ttf'),
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-SemiBold.ttf'),
            ]
        else:
            font_paths = [
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-Regular.ttf'),
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-Medium.ttf'),
            ]
        font_paths.extend([
            os.path.join(FONTS_DIR, 'Cinzel', 'Cinzel-VariableFont_wght.ttf'),
            "/System/Library/Fonts/Times.ttc",
        ])
    else:
        font_paths = [
            os.path.join(FONTS_DIR, 'Oldenburg-Regular.ttf'),
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/System/Library/Fonts/Times.ttc",
        ]

    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except Exception:
            continue

    return ImageFont.load_default()


def create_rounded_rectangle(size, radius, fill_color, border_color=None, border_width=0):
    """Create a rounded rectangle image"""
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    if border_color and border_width > 0:
        draw.rounded_rectangle(
            [(0, 0), (size[0]-1, size[1]-1)],
            radius=radius,
            fill=border_color
        )
        draw.rounded_rectangle(
            [(border_width, border_width),
             (size[0]-1-border_width, size[1]-1-border_width)],
            radius=max(0, radius - border_width),
            fill=fill_color
        )
    else:
        draw.rounded_rectangle(
            [(0, 0), (size[0]-1, size[1]-1)],
            radius=radius,
            fill=fill_color
        )

    return image


def draw_title(draw, name, y, max_width):
    """Draw the trait title"""
    font = get_font(TITLE_FONT_SIZE, bold=True, display=True)

    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]

    # Shrink title if needed
    current_size = TITLE_FONT_SIZE
    while text_width > max_width and current_size > 20:
        current_size -= 2
        font = get_font(current_size, bold=True, display=True)
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]

    # Center title
    x = (CARD_WIDTH - text_width) // 2
    draw.text((x, y), name, fill=COLOR_TITLE, font=font)

    return bbox[3] - bbox[1] + 18


def draw_separator(draw, y):
    """Draw a horizontal separator line"""
    x1 = SAFE_ZONE + BORDER_WIDTH + 5
    x2 = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5
    draw.line([(x1, y), (x2, y)], fill=COLOR_SEPARATOR, width=1)
    return 6


def draw_type_badge(draw, trait_type, y):
    """Draw the trait type badge centered"""
    display_name = TRAIT_TYPE_NAMES.get(trait_type, trait_type.capitalize())
    color = TRAIT_TYPE_COLORS.get(trait_type, (100, 80, 60))

    font = get_font(TYPE_FONT_SIZE, bold=True, display=True)

    text = display_name.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    box_width = text_width + 24
    box_height = text_height + 18
    x = (CARD_WIDTH - box_width) // 2

    # Draw badge background
    draw.rounded_rectangle(
        [(x, y), (x + box_width, y + box_height)],
        radius=5,
        fill=color,
        outline=(255, 255, 255),
        width=1
    )

    # Draw text centered in badge (equal top and bottom)
    text_x = x + (box_width - text_width) // 2
    text_y = y + (box_height - text_height) // 2
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    return box_height + 6


def draw_source_badge(draw, source, y):
    """Draw the source badge (PC1, PC2, etc.) centered"""
    font = get_font(SMALL_FONT_SIZE, bold=True, display=True)

    text = source.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    box_width = text_width + 12
    box_height = text_height + 8
    x = (CARD_WIDTH - box_width) // 2

    draw.rounded_rectangle(
        [(x, y), (x + box_width, y + box_height)],
        radius=3,
        fill=(180, 160, 130),
        outline=(150, 130, 100),
        width=1
    )

    text_x = x + (box_width - text_width) // 2
    text_y = y + (box_height - text_height) // 2 - 1
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    return box_height + 4


def draw_subsection_header(draw, title, y, max_width):
    """Draw a subsection header (e.g., 'Rasgo de conjuro')"""
    font = get_font(SUBSECTION_FONT_SIZE, bold=True, display=True)

    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = SAFE_ZONE + BORDER_WIDTH + 5
    box_width = max_width
    box_height = text_height + 10

    # Draw background bar
    draw.rounded_rectangle(
        [(x, y), (x + box_width, y + box_height)],
        radius=3,
        fill=COLOR_SUBSECTION_BG,
        outline=COLOR_SEPARATOR,
        width=1
    )

    # Draw text left-aligned with padding
    text_x = x + 8
    text_y = y + (box_height - text_height) // 2 - 1
    draw.text((text_x, text_y), title, fill=COLOR_LABEL, font=font)

    return box_height + 4


def draw_wrapped_text(draw, text, y, max_width, font_size=None):
    """Draw wrapped body text"""
    if not text:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE

    font = get_font(font_size)
    x = SAFE_ZONE + BORDER_WIDTH + 8

    # Calculate characters per line
    test_text = "Este rasgo es una demostración de texto"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    test_width = bbox[2] - bbox[0]
    chars_per_line = int((max_width / test_width) * len(test_text))

    # Wrap text
    wrapped = textwrap.wrap(text, width=chars_per_line)

    total_height = 0
    line_spacing = font_size + 4

    for i, line in enumerate(wrapped):
        draw.text((x, y + (i * line_spacing)), line, fill=COLOR_TEXT, font=font)
        total_height = (i + 1) * line_spacing

    return total_height + 2


def generate_trait_card(trait_data, output_path):
    """Generate a single trait card"""
    trait_type = trait_data.get('trait_type', 'general')
    border_color = TRAIT_TYPE_COLORS.get(trait_type, COLOR_BORDER)

    # Create base card
    card = create_rounded_rectangle(
        (CARD_WIDTH, CARD_HEIGHT),
        CORNER_RADIUS,
        COLOR_BACKGROUND,
        border_color,
        BORDER_WIDTH
    )

    draw = ImageDraw.Draw(card)
    content_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 8

    current_y = TITLE_Y

    # Draw trait name as title
    title_height = draw_title(draw, trait_data['name'], current_y, content_width)
    current_y += title_height

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Draw type badge
    current_y += draw_type_badge(draw, trait_type, current_y)

    # Draw source badge
    source = trait_data.get('source', 'PC1')
    current_y += draw_source_badge(draw, source, current_y)

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Maximum Y to stay within bounds
    max_y = CARD_HEIGHT - SAFE_ZONE - BORDER_WIDTH - 5

    # Draw content
    subsections = trait_data.get('subsections', [])

    if subsections:
        # Draw each subsection with its own header
        for subsection in subsections:
            if current_y >= max_y - 60:
                break

            # Draw subsection header
            current_y += draw_subsection_header(
                draw, subsection['title'], current_y, content_width
            )
            current_y += 2

            # Draw subsection description
            desc = subsection.get('description', '')
            if desc and current_y < max_y - 30:
                # Adjust font size based on remaining space
                remaining = max_y - current_y
                font_size = BODY_FONT_SIZE
                if len(desc) > 400 or remaining < 400:
                    font_size = BODY_FONT_SIZE - 2
                if len(desc) > 600 or remaining < 250:
                    font_size = BODY_FONT_SIZE - 4

                desc_height = draw_wrapped_text(
                    draw, desc, current_y, content_width, font_size
                )
                current_y += desc_height + 4
    else:
        # Single description
        description = trait_data.get('description', '')
        if description:
            # Adjust font size based on description length
            font_size = BODY_FONT_SIZE
            if len(description) > 500:
                font_size = BODY_FONT_SIZE - 2
            if len(description) > 800:
                font_size = BODY_FONT_SIZE - 4

            current_y += 4
            draw_wrapped_text(draw, description, current_y, content_width, font_size)

    # Convert to RGB and save
    rgb_card = Image.new('RGB', card.size, (255, 255, 255))
    rgb_card.paste(card, mask=card.split()[3] if card.mode == 'RGBA' else None)
    rgb_card.save(output_path, 'PNG', dpi=(300, 300))


def main():
    """Main function to generate all trait cards"""
    print("PF2e Trait Cards Generator")
    print("=" * 40)
    print()

    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found: {DATA_FILE}")
        print("Please run parse_traits.py first!")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    traits = data.get('traits', [])
    print(f"Found {len(traits)} traits to generate")
    print(f"Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ 300 DPI (63x88mm Magic)")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group by trait_type for organization
    traits_by_type = {}
    for trait in traits:
        trait_type = trait.get('trait_type', 'general')
        if trait_type not in traits_by_type:
            traits_by_type[trait_type] = []
        traits_by_type[trait_type].append(trait)

    total_generated = 0
    for trait_type, type_traits in sorted(traits_by_type.items()):
        folder_dir = os.path.join(OUTPUT_DIR, trait_type)
        os.makedirs(folder_dir, exist_ok=True)

        print(f"Generating {trait_type} ({len(type_traits)} traits)...")
        for trait in type_traits:
            trait_id = trait['id']
            output_file = os.path.join(folder_dir, f"{trait_id}.png")

            try:
                generate_trait_card(trait, output_file)
                print(f"  + {trait['name']}")
                total_generated += 1
            except Exception as e:
                print(f"  x Error generating {trait['name']}: {e}")
                import traceback
                traceback.print_exc()

        print()

    print(f"Generated {total_generated} cards in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
