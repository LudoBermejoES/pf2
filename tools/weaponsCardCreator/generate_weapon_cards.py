#!/usr/bin/env python3
"""
PF2e Weapon Cards Generator
Generates Magic-sized weapon cards for Pathfinder 2e
Includes weapon stats and trait descriptions
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

# Colors (RGB) - Based on PF2e web theme with weapon accent
COLOR_BACKGROUND = (244, 228, 201)      # Parchment #f4e4c9
COLOR_BORDER = (85, 85, 85)             # Steel gray for weapons
COLOR_BORDER_RANGED = (70, 100, 70)     # Green-gray for ranged
COLOR_TRAIT_BG = (93, 48, 48)           # Darker red for traits
COLOR_TRAIT_TEXT = (218, 165, 32)       # Gold text on traits
COLOR_TEXT = (45, 39, 34)               # Dark text #2d2722
COLOR_TITLE = (85, 85, 85)              # Steel for title
COLOR_SEPARATOR = (125, 68, 55)         # Red for lines
COLOR_LABEL = (125, 68, 55)             # Red for labels
COLOR_STAT_BG = (230, 215, 185)         # Lighter parchment for stat box
COLOR_TRAIT_DESC_BG = (250, 240, 220)   # Very light for trait descriptions

# Layout
TITLE_Y = SAFE_ZONE + 12
TRAIT_HEIGHT = 28
TRAIT_PADDING = 6
LINE_HEIGHT = 24
SECTION_SPACING = 6

# Font sizes
TITLE_FONT_SIZE = 38
BODY_FONT_SIZE = 20
TRAIT_FONT_SIZE = 15
LABEL_FONT_SIZE = 18
SMALL_FONT_SIZE = 16
TRAIT_DESC_FONT_SIZE = 16

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, 'assets', 'fonts')
DATA_FILE = os.path.join(SCRIPT_DIR, 'data', 'weapons.json')
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


def draw_title(draw, title, y, max_width):
    """Draw the weapon title"""
    font = get_font(TITLE_FONT_SIZE, bold=True, display=True)

    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]

    current_size = TITLE_FONT_SIZE
    while text_width > max_width and current_size > 20:
        current_size -= 2
        font = get_font(current_size, bold=True, display=True)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]

    x = (CARD_WIDTH - text_width) // 2
    draw.text((x, y), title, fill=COLOR_TITLE, font=font)

    return bbox[3] - bbox[1] + 6


def draw_separator(draw, y):
    """Draw a horizontal separator line"""
    x1 = SAFE_ZONE + BORDER_WIDTH + 5
    x2 = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5
    draw.line([(x1, y), (x2, y)], fill=COLOR_SEPARATOR, width=1)
    return 4


def draw_traits(draw, traits, y):
    """Draw trait boxes"""
    if not traits:
        return 0

    font = get_font(TRAIT_FONT_SIZE, bold=True, display=True)

    total_width = 0
    trait_boxes = []
    spacing = 5

    for trait in traits:
        bbox = draw.textbbox((0, 0), trait.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        box_width = text_width + (TRAIT_PADDING * 2)
        trait_boxes.append((trait, box_width, text_width, text_height))
        total_width += box_width + spacing

    total_width -= spacing

    # Handle overflow - wrap to multiple lines if needed
    available_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 20
    if total_width > available_width:
        # Draw in multiple rows
        rows = []
        current_row = []
        current_width = 0

        for trait_data in trait_boxes:
            if current_width + trait_data[1] + spacing > available_width and current_row:
                rows.append(current_row)
                current_row = [trait_data]
                current_width = trait_data[1] + spacing
            else:
                current_row.append(trait_data)
                current_width += trait_data[1] + spacing

        if current_row:
            rows.append(current_row)

        total_height = 0
        for row in rows:
            row_width = sum(t[1] for t in row) + (len(row) - 1) * spacing
            x = (CARD_WIDTH - row_width) // 2

            for trait, box_width, text_width, text_height in row:
                draw.rounded_rectangle(
                    [(x, y + total_height), (x + box_width, y + total_height + TRAIT_HEIGHT)],
                    radius=3,
                    fill=COLOR_TRAIT_BG,
                    outline=COLOR_TRAIT_TEXT,
                    width=1
                )
                text_x = x + (box_width - text_width) // 2
                text_y = y + total_height + (TRAIT_HEIGHT - text_height) // 2 - 2
                draw.text((text_x, text_y), trait.upper(), fill=COLOR_TRAIT_TEXT, font=font)
                x += box_width + spacing

            total_height += TRAIT_HEIGHT + 3

        return total_height + 2
    else:
        x = (CARD_WIDTH - total_width) // 2

        for trait, box_width, text_width, text_height in trait_boxes:
            draw.rounded_rectangle(
                [(x, y), (x + box_width, y + TRAIT_HEIGHT)],
                radius=3,
                fill=COLOR_TRAIT_BG,
                outline=COLOR_TRAIT_TEXT,
                width=1
            )
            text_x = x + (box_width - text_width) // 2
            text_y = y + (TRAIT_HEIGHT - text_height) // 2 - 2
            draw.text((text_x, text_y), trait.upper(), fill=COLOR_TRAIT_TEXT, font=font)
            x += box_width + spacing

        return TRAIT_HEIGHT + 4


def draw_stat_box(draw, weapon_data, y):
    """Draw the stats box with weapon stats"""
    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10
    box_height = 70

    # Draw background box
    draw.rounded_rectangle(
        [(x, y), (x + width, y + box_height)],
        radius=5,
        fill=COLOR_STAT_BG,
        outline=COLOR_BORDER,
        width=1
    )

    # Fonts
    label_font = get_font(LABEL_FONT_SIZE, bold=True, display=True)
    value_font = get_font(BODY_FONT_SIZE - 2)

    padding = 8
    current_y = y + padding

    # First row: Price and Damage
    price = weapon_data.get('price', '—')
    damage = weapon_data.get('damage', '—')

    draw.text((x + padding, current_y), "Precio:", fill=COLOR_LABEL, font=label_font)
    draw.text((x + padding + 70, current_y), price, fill=COLOR_TEXT, font=value_font)

    draw.text((x + width // 2, current_y), "Daño:", fill=COLOR_LABEL, font=label_font)
    draw.text((x + width // 2 + 60, current_y), damage, fill=COLOR_TEXT, font=value_font)

    current_y += LINE_HEIGHT

    # Second row: Hands, Bulk, Group
    hands = weapon_data.get('hands', '—')
    bulk = weapon_data.get('bulk', '—')
    group = weapon_data.get('group', '—')

    draw.text((x + padding, current_y), "Manos:", fill=COLOR_LABEL, font=label_font)
    draw.text((x + padding + 65, current_y), hands, fill=COLOR_TEXT, font=value_font)

    draw.text((x + width // 3, current_y), "Imp.:", fill=COLOR_LABEL, font=label_font)
    draw.text((x + width // 3 + 45, current_y), bulk, fill=COLOR_TEXT, font=value_font)

    draw.text((x + 2 * width // 3, current_y), "Grupo:", fill=COLOR_LABEL, font=label_font)
    # Truncate group if too long
    if len(group) > 12:
        group = group[:11] + "."
    draw.text((x + 2 * width // 3 + 60, current_y), group, fill=COLOR_TEXT, font=value_font)

    current_y += LINE_HEIGHT

    # Third row (if ranged): Range and Reload
    if weapon_data.get('isRanged'):
        range_val = weapon_data.get('range', '—')
        reload_val = weapon_data.get('reload', '—')

        draw.text((x + padding, current_y), "Rango:", fill=COLOR_LABEL, font=label_font)
        # Truncate range if too long
        if len(range_val) > 15:
            range_val = range_val.split('(')[0].strip()
        draw.text((x + padding + 65, current_y), range_val, fill=COLOR_TEXT, font=value_font)

        draw.text((x + width // 2, current_y), "Recarga:", fill=COLOR_LABEL, font=label_font)
        draw.text((x + width // 2 + 75, current_y), reload_val, fill=COLOR_TEXT, font=value_font)

        box_height = 95
        # Redraw box with new height
        draw.rounded_rectangle(
            [(x, y), (x + width, y + box_height)],
            radius=5,
            fill=COLOR_STAT_BG,
            outline=COLOR_BORDER,
            width=1
        )
        # Redraw all text (simplified - in production would optimize)

    return box_height + 6


def draw_description(draw, text, y, max_width, font_size=None):
    """Draw wrapped description text"""
    if not text:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE

    font = get_font(font_size)
    x = SAFE_ZONE + BORDER_WIDTH + 8

    # Calculate characters per line
    test_text = "abcdefghijklmnopqrst"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    avg_char_width = (bbox[2] - bbox[0]) / len(test_text)
    chars_per_line = int((max_width - 16) / avg_char_width)

    # Wrap text
    wrapped = textwrap.wrap(text, width=chars_per_line)

    total_height = 0
    line_spacing = LINE_HEIGHT - 2
    for i, line in enumerate(wrapped):
        draw.text((x, y + (i * line_spacing)), line, fill=COLOR_TEXT, font=font)
        total_height = (i + 1) * line_spacing

    return total_height + 4


def draw_trait_descriptions(draw, trait_descriptions, y, max_width):
    """Draw trait descriptions section"""
    if not trait_descriptions:
        return 0

    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10

    # Calculate total height needed
    font = get_font(TRAIT_DESC_FONT_SIZE)
    label_font = get_font(TRAIT_DESC_FONT_SIZE, bold=True, display=True)

    test_text = "abcdefghijklmnopqrst"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    avg_char_width = (bbox[2] - bbox[0]) / len(test_text)
    chars_per_line = int((width - 20) / avg_char_width)

    total_height = 8  # Initial padding
    trait_data = []

    for trait in trait_descriptions:
        name = trait['name']
        desc = trait['description']

        # Truncate long descriptions
        if len(desc) > 150:
            desc = desc[:147] + "..."

        wrapped = textwrap.wrap(desc, width=chars_per_line)
        lines_height = len(wrapped) * (LINE_HEIGHT - 6)
        trait_data.append((name, wrapped, lines_height))
        total_height += LINE_HEIGHT - 4 + lines_height + 4

    total_height += 4  # Final padding

    # Draw background
    draw.rounded_rectangle(
        [(x, y), (x + width, y + total_height)],
        radius=5,
        fill=COLOR_TRAIT_DESC_BG,
        outline=COLOR_SEPARATOR,
        width=1
    )

    # Draw header
    current_y = y + 6
    header_font = get_font(LABEL_FONT_SIZE, bold=True, display=True)
    draw.text((x + 8, current_y), "Rasgos:", fill=COLOR_LABEL, font=header_font)
    current_y += LINE_HEIGHT

    # Draw each trait description
    line_height = LINE_HEIGHT - 6
    for name, wrapped_lines, _ in trait_data:
        # Draw trait name
        draw.text((x + 8, current_y), f"• {name}:", fill=COLOR_LABEL, font=label_font)
        current_y += line_height + 2

        # Draw description lines
        for line in wrapped_lines:
            draw.text((x + 16, current_y), line, fill=COLOR_TEXT, font=font)
            current_y += line_height

        current_y += 2

    return total_height + 4


def generate_weapon_card(weapon_data, output_path):
    """Generate a single weapon card"""
    # Determine border color based on weapon type
    border_color = COLOR_BORDER_RANGED if weapon_data.get('isRanged') else COLOR_BORDER

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

    # Draw title
    title_height = draw_title(draw, weapon_data['name'], current_y, content_width)
    current_y += title_height

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Draw traits
    traits = weapon_data.get('traits', [])
    if traits:
        current_y += draw_traits(draw, traits, current_y)
        current_y += draw_separator(draw, current_y)

    # Draw stat box
    stat_height = draw_stat_box(draw, weapon_data, current_y)
    current_y += stat_height

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Draw description
    description = weapon_data.get('description', '')
    if description:
        current_y += 2
        # Adjust font size based on content
        remaining_space = CARD_HEIGHT - current_y - SAFE_ZONE - 20
        trait_descs = weapon_data.get('trait_descriptions', [])

        # Estimate space needed for trait descriptions
        trait_space = len(trait_descs) * 60 if trait_descs else 0
        desc_space = remaining_space - trait_space

        font_size = BODY_FONT_SIZE
        if len(description) > 200 or desc_space < 150:
            font_size = BODY_FONT_SIZE - 2
        if len(description) > 300 or desc_space < 100:
            font_size = BODY_FONT_SIZE - 3

        current_y += draw_description(draw, description, current_y, content_width, font_size)

    # Draw trait descriptions
    trait_descriptions = weapon_data.get('trait_descriptions', [])
    remaining_space = CARD_HEIGHT - current_y - SAFE_ZONE - 10
    if trait_descriptions and remaining_space > 80:
        current_y += draw_separator(draw, current_y)
        current_y += 2
        draw_trait_descriptions(draw, trait_descriptions, current_y, content_width)

    # Convert to RGB and save
    rgb_card = Image.new('RGB', card.size, (255, 255, 255))
    rgb_card.paste(card, mask=card.split()[3] if card.mode == 'RGBA' else None)
    rgb_card.save(output_path, 'PNG', dpi=(300, 300))


def main():
    """Main function to generate all weapon cards"""
    print("PF2e Weapon Cards Generator")
    print("=" * 40)
    print()

    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found: {DATA_FILE}")
        print("Please run parse_weapons.py first!")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    weapons = data.get('weapons', [])
    print(f"Found {len(weapons)} weapons to generate")
    print(f"Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ 300 DPI (63x88mm Magic)")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group by category for organization
    CATEGORY_FOLDERS = {
        'Arma cuerpo a cuerpo sencilla': 'melee-simple',
        'Arma cuerpo a cuerpo marcial': 'melee-martial',
        'Arma cuerpo a cuerpo avanzada': 'melee-advanced',
        'Arma a distancia sencilla': 'ranged-simple',
        'Arma a distancia marcial': 'ranged-martial',
        'Arma a distancia avanzada': 'ranged-advanced',
        'Ataque sin armas': 'unarmed',
    }

    weapons_by_category = {}
    for weapon in weapons:
        category = weapon.get('category', 'Otros')
        if category not in weapons_by_category:
            weapons_by_category[category] = []
        weapons_by_category[category].append(weapon)

    total_generated = 0
    for category, category_weapons in weapons_by_category.items():
        folder_name = CATEGORY_FOLDERS.get(category, 'otros')
        category_dir = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(category_dir, exist_ok=True)

        print(f"Generating {folder_name} ({len(category_weapons)} weapons)...")
        for weapon in category_weapons:
            weapon_id = weapon['id']
            output_file = os.path.join(category_dir, f"{weapon_id}.png")

            try:
                generate_weapon_card(weapon, output_file)
                print(f"  ✓ {weapon['name']}")
                total_generated += 1
            except Exception as e:
                print(f"  ✗ Error generating {weapon['name']}: {e}")
                import traceback
                traceback.print_exc()

        print()

    print(f"✓ Generated {total_generated} cards in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
