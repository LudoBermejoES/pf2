#!/usr/bin/env python3
"""
Generate armor cards as PNG images
Creates Magic-sized cards (63x88mm at 300 DPI = 744x1039px)
"""

import os
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Card dimensions (Magic card size at 300 DPI)
CARD_WIDTH = 744
CARD_HEIGHT = 1039
DPI = 300

# Layout constants
BORDER_WIDTH = 8
SAFE_ZONE = 20
CONTENT_PADDING = 15
LINE_HEIGHT = 24
TRAIT_HEIGHT = 28
SECTION_SPACING = 6

# Font sizes
TITLE_FONT_SIZE = 38
BODY_FONT_SIZE = 20
TRAIT_FONT_SIZE = 15
LABEL_FONT_SIZE = 16
SMALL_FONT_SIZE = 14
TRAIT_DESC_FONT_SIZE = 20

# Colors - armor themed (blue/steel)
COLOR_BG = (250, 250, 255)
COLOR_BORDER = (70, 90, 120)  # Steel blue for armor
COLOR_BORDER_HEAVY = (50, 60, 80)  # Darker for heavy armor
COLOR_BORDER_LIGHT = (100, 130, 160)  # Lighter for light armor
COLOR_TITLE = (30, 40, 60)
COLOR_TEXT = (40, 40, 50)
COLOR_TRAIT_BG = (70, 90, 120)
COLOR_TRAIT_TEXT = (255, 255, 255)
COLOR_SEPARATOR = (180, 190, 200)
COLOR_STAT_BG = (240, 242, 248)
COLOR_LABEL = (60, 80, 110)
COLOR_TRAIT_DESC_BG = (245, 247, 252)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, 'assets', 'fonts')
DATA_FILE = os.path.join(SCRIPT_DIR, 'data', 'armors.json')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'generated_cards')


def get_font(size, bold=False, display=False):
    """Get a font with fallback"""
    if display:
        font_name = 'Cinzel-Bold.ttf' if bold else 'Cinzel-Regular.ttf'
        font_path = os.path.join(FONTS_DIR, 'Cinzel', 'static', font_name)
        if not os.path.exists(font_path):
            font_path = os.path.join(FONTS_DIR, 'Cinzel-Regular.ttf')
    else:
        font_path = os.path.join(FONTS_DIR, 'Oldenburg-Regular.ttf')

    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()


def create_card_base(border_color):
    """Create a blank card with border"""
    card = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(card)

    # Draw border
    draw.rectangle(
        [(SAFE_ZONE, SAFE_ZONE),
         (CARD_WIDTH - SAFE_ZONE, CARD_HEIGHT - SAFE_ZONE)],
        outline=border_color,
        width=BORDER_WIDTH
    )

    return card, draw


def draw_title(draw, title, y):
    """Draw the armor title centered"""
    font = get_font(TITLE_FONT_SIZE, bold=True, display=True)
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]

    # Reduce font size if too wide
    current_size = TITLE_FONT_SIZE
    while text_width > CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 40 and current_size > 20:
        current_size -= 2
        font = get_font(current_size, bold=True, display=True)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]

    x = (CARD_WIDTH - text_width) // 2
    draw.text((x, y), title, fill=COLOR_TITLE, font=font)

    return bbox[3] - bbox[1] + 17  # More margin after title


def draw_separator(draw, y):
    """Draw a horizontal separator line"""
    x1 = SAFE_ZONE + BORDER_WIDTH + 5
    x2 = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5
    draw.line([(x1, y), (x2, y)], fill=COLOR_SEPARATOR, width=1)
    return 8


def draw_traits(draw, traits, y):
    """Draw trait boxes"""
    if not traits:
        return 0

    font = get_font(TRAIT_FONT_SIZE, bold=True, display=True)
    x = SAFE_ZONE + BORDER_WIDTH + 5
    max_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10

    # Calculate total width needed
    trait_widths = []
    for trait in traits:
        bbox = draw.textbbox((0, 0), trait.upper(), font=font)
        trait_widths.append(bbox[2] - bbox[0] + 16)

    total_width = sum(trait_widths) + (len(traits) - 1) * 6

    # If traits fit on one line
    if total_width <= max_width:
        # Center the traits
        x = (CARD_WIDTH - total_width) // 2
        spacing = 6

        for i, trait in enumerate(traits):
            bbox = draw.textbbox((0, 0), trait.upper(), font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            box_width = text_width + 16

            # Draw trait box
            draw.rounded_rectangle(
                [(x, y), (x + box_width, y + TRAIT_HEIGHT)],
                radius=4,
                fill=COLOR_TRAIT_BG
            )

            # Draw text centered
            text_x = x + (box_width - text_width) // 2
            text_y = y + (TRAIT_HEIGHT - text_height) // 2 - 2
            draw.text((text_x, text_y), trait.upper(), fill=COLOR_TRAIT_TEXT, font=font)
            x += box_width + spacing

        return TRAIT_HEIGHT + 4
    else:
        # Multi-line layout
        current_x = SAFE_ZONE + BORDER_WIDTH + 5
        current_y = y
        row_start_x = current_x
        spacing = 6

        for i, trait in enumerate(traits):
            bbox = draw.textbbox((0, 0), trait.upper(), font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            box_width = text_width + 16

            # Check if we need a new line
            if current_x + box_width > CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5:
                current_x = row_start_x
                current_y += TRAIT_HEIGHT + 4

            # Draw trait box
            draw.rounded_rectangle(
                [(current_x, current_y), (current_x + box_width, current_y + TRAIT_HEIGHT)],
                radius=4,
                fill=COLOR_TRAIT_BG
            )

            # Draw text centered
            text_x = current_x + (box_width - text_width) // 2
            text_y = current_y + (TRAIT_HEIGHT - text_height) // 2 - 2
            draw.text((text_x, text_y), trait.upper(), fill=COLOR_TRAIT_TEXT, font=font)
            current_x += box_width + spacing

        return (current_y - y) + TRAIT_HEIGHT + 4


def draw_stat_box(draw, armor_data, y):
    """Draw the stats box with armor stats"""
    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10
    padding = 10
    row_height = 24

    # Armors need 3 rows of stats
    num_rows = 3
    box_height = padding * 2 + (num_rows * row_height)

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

    current_y = y + padding

    # Helper to draw label:value pair
    def draw_stat(sx, sy, label, value, spacing=8):
        draw.text((sx, sy), label, fill=COLOR_LABEL, font=label_font)
        bbox = draw.textbbox((0, 0), label, font=label_font)
        label_width = bbox[2] - bbox[0]
        draw.text((sx + label_width + spacing, sy), value, fill=COLOR_TEXT, font=value_font)

    # Row 1: Precio | Bon. CA | Tope Des.
    price = armor_data.get('price', '—')
    ac_bonus = armor_data.get('ac_bonus', '—')
    dex_cap = armor_data.get('dex_cap', '—')

    col1_x = x + padding
    col2_x = x + width // 3
    col3_x = x + 2 * width // 3

    draw_stat(col1_x, current_y, "Precio:", price, 8)
    draw_stat(col2_x, current_y, "Bon.CA:", ac_bonus, 8)
    draw_stat(col3_x, current_y, "Tope Des.:", dex_cap, 8)

    current_y += row_height

    # Row 2: Pen. pruebas | Pen. Velocidad | Fuerza
    check_pen = armor_data.get('check_penalty', '—')
    speed_pen = armor_data.get('speed_penalty', '—')
    strength = armor_data.get('strength', '—')

    # Simplify speed penalty display
    if speed_pen and '(' in speed_pen:
        speed_pen = speed_pen.split('(')[0].strip()

    draw_stat(col1_x, current_y, "Pen.Pr.:", check_pen, 8)
    draw_stat(col2_x, current_y, "Pen.Vel.:", speed_pen, 8)
    draw_stat(col3_x, current_y, "Fuerza:", strength, 8)

    current_y += row_height

    # Row 3: Impedimenta | Grupo
    bulk = armor_data.get('bulk', '—')
    group = armor_data.get('group', '—')

    draw_stat(col1_x, current_y, "Imp.:", bulk, 8)
    draw_stat(col2_x, current_y, "Grupo:", group, 8)

    return box_height + 6


def draw_description(draw, text, y, max_width, font_size=None):
    """Draw wrapped description text"""
    if not text:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE

    font = get_font(font_size)
    x = SAFE_ZONE + BORDER_WIDTH + 10

    # Calculate available width
    available_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 20

    # Wrap text
    avg_char_width = font_size * 0.5
    chars_per_line = int(available_width / avg_char_width)
    wrapped = textwrap.wrap(text, width=chars_per_line)

    # Draw each line
    total_height = 0
    line_spacing = LINE_HEIGHT - 2
    for i, line in enumerate(wrapped):
        draw.text((x, y + (i * line_spacing)), line, fill=COLOR_TEXT, font=font)
        total_height = (i + 1) * line_spacing

    return total_height + 4


def draw_trait_descriptions(draw, trait_descriptions, y, max_width, remaining_space):
    """Draw trait descriptions section"""
    if not trait_descriptions:
        return 0

    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10
    padding = 10

    font_size = TRAIT_DESC_FONT_SIZE
    font = get_font(font_size)
    name_font = get_font(font_size, bold=True, display=True)

    # Calculate available chars per line
    test_text = "abcdefghijklmnopqrstuvwxyz"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    avg_char_width = (bbox[2] - bbox[0]) / len(test_text)
    chars_per_line = int((width - padding * 2 - 10) / avg_char_width)

    line_height = 22

    # Build trait lines
    trait_lines = []
    for trait in trait_descriptions:
        name = trait['name']
        desc = trait['description']

        # Clean up name
        base_name = name.split()[0] if ' ' in name else name

        # Truncate description
        max_desc_len = 80 if remaining_space > 300 else 50
        if len(desc) > max_desc_len:
            desc = desc[:max_desc_len-3].rsplit(' ', 1)[0] + "..."

        full_text = f"{base_name}: {desc}"
        wrapped = textwrap.wrap(full_text, width=chars_per_line)

        if len(wrapped) > 2:
            wrapped = wrapped[:2]
            if not wrapped[-1].endswith('...'):
                wrapped[-1] = wrapped[-1][:-3] + "..."

        trait_lines.append(wrapped)

    # Calculate total height
    total_lines = sum(len(lines) for lines in trait_lines)
    total_height = padding * 2 + total_lines * line_height + (len(trait_lines) - 1) * 4

    # Check if it fits
    if total_height > remaining_space - 10:
        trait_lines = []
        for trait in trait_descriptions[:3]:
            name = trait['name'].split()[0]
            desc = trait['description'][:40]
            if len(trait['description']) > 40:
                desc = desc.rsplit(' ', 1)[0] + "..."
            trait_lines.append([f"{name}: {desc}"])
        total_height = padding * 2 + len(trait_lines) * line_height

    # Draw background
    draw.rounded_rectangle(
        [(x, y), (x + width, y + total_height)],
        radius=5,
        fill=COLOR_TRAIT_DESC_BG,
        outline=COLOR_SEPARATOR,
        width=1
    )

    # Draw traits
    current_y = y + padding
    for i, wrapped_lines in enumerate(trait_lines):
        for j, line in enumerate(wrapped_lines):
            text_x = x + padding
            if j == 0:
                draw.text((text_x, current_y), "•", fill=COLOR_LABEL, font=name_font)
                text_x += 12

                if ':' in line:
                    name_part, rest = line.split(':', 1)
                    draw.text((text_x, current_y), name_part + ":", fill=COLOR_LABEL, font=name_font)
                    name_bbox = draw.textbbox((0, 0), name_part + ":", font=name_font)
                    name_width = name_bbox[2] - name_bbox[0]
                    draw.text((text_x + name_width + 4, current_y), rest.strip(), fill=COLOR_TEXT, font=font)
                else:
                    draw.text((text_x, current_y), line, fill=COLOR_TEXT, font=font)
            else:
                draw.text((text_x + 12, current_y), line, fill=COLOR_TEXT, font=font)

            current_y += line_height

        current_y += 2

    return total_height + 4


def generate_armor_card(armor_data, output_path):
    """Generate a single armor card"""
    # Determine border color based on armor weight
    weight_class = armor_data.get('weight_class', 'medium')
    if weight_class == 'heavy':
        border_color = COLOR_BORDER_HEAVY
    elif weight_class == 'light':
        border_color = COLOR_BORDER_LIGHT
    else:
        border_color = COLOR_BORDER

    card, draw = create_card_base(border_color)

    # Start drawing content
    current_y = SAFE_ZONE + BORDER_WIDTH + 15

    # Title
    current_y += draw_title(draw, armor_data['name'], current_y)

    # Separator
    current_y += draw_separator(draw, current_y)
    current_y += 2

    # Traits
    traits = armor_data.get('traits', [])
    if traits:
        current_y += draw_traits(draw, traits, current_y)
        current_y += 4

    # Stats box
    current_y += draw_stat_box(draw, armor_data, current_y)
    current_y += 6

    # Description
    description = armor_data.get('description', '')
    if description:
        content_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 20
        desc_space = CARD_HEIGHT - current_y - SAFE_ZONE - 100

        font_size = None
        if len(description) > 300 or desc_space < 100:
            font_size = BODY_FONT_SIZE - 3

        current_y += draw_description(draw, description, current_y, content_width, font_size)

    # Trait descriptions
    trait_descriptions = armor_data.get('trait_descriptions', [])
    remaining_space = CARD_HEIGHT - current_y - SAFE_ZONE - 10
    if trait_descriptions and remaining_space > 60:
        current_y += draw_separator(draw, current_y)
        current_y += 2
        draw_trait_descriptions(draw, trait_descriptions, current_y, 0, remaining_space)

    # Convert to RGB and save
    rgb_card = Image.new('RGB', card.size, (255, 255, 255))
    rgb_card.paste(card, mask=card.split()[3] if card.mode == 'RGBA' else None)
    rgb_card.save(output_path, 'PNG', dpi=(300, 300))


def main():
    print("PF2e Armor Cards Generator")
    print("=" * 40)

    # Load armor data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    armors = data['armors']
    print(f"Found {len(armors)} armors to generate")
    print(f"Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ {DPI} DPI (63x88mm Magic)")
    print()

    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group by weight class
    by_weight = {}
    for armor in armors:
        weight = armor.get('weight_class', 'medium')
        if weight not in by_weight:
            by_weight[weight] = []
        by_weight[weight].append(armor)

    # Generate cards
    for weight, armor_list in sorted(by_weight.items()):
        weight_dir = os.path.join(OUTPUT_DIR, weight)
        os.makedirs(weight_dir, exist_ok=True)

        print(f"Generating {weight} ({len(armor_list)} armors)...")

        for armor in armor_list:
            output_path = os.path.join(weight_dir, f"{armor['id']}.png")
            try:
                generate_armor_card(armor, output_path)
                print(f"  + {armor['name']}")
            except Exception as e:
                print(f"  x Error generating {armor['name']}: {e}")

    print()
    print(f"+ Generated {len(armors)} cards in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
