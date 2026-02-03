#!/usr/bin/env python3
"""
Generate shield cards as PNG images
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
SECTION_SPACING = 6

# Font sizes
TITLE_FONT_SIZE = 38
BODY_FONT_SIZE = 20
LABEL_FONT_SIZE = 16
SMALL_FONT_SIZE = 14

# Colors - shield themed (brown/wood tones)
COLOR_BG = (252, 248, 240)              # Warm parchment
COLOR_BORDER = (101, 67, 33)            # Wood brown
COLOR_TITLE = (60, 40, 20)              # Dark brown
COLOR_TEXT = (45, 35, 25)               # Dark text
COLOR_SEPARATOR = (180, 150, 120)       # Light brown
COLOR_STAT_BG = (245, 235, 220)         # Light wood
COLOR_LABEL = (101, 67, 33)             # Wood brown for labels

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, 'assets', 'fonts')
DATA_FILE = os.path.join(SCRIPT_DIR, 'data', 'shields.json')
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


def create_card_base():
    """Create a blank card with border"""
    card = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(card)

    # Draw border
    draw.rectangle(
        [(SAFE_ZONE, SAFE_ZONE),
         (CARD_WIDTH - SAFE_ZONE, CARD_HEIGHT - SAFE_ZONE)],
        outline=COLOR_BORDER,
        width=BORDER_WIDTH
    )

    return card, draw


def draw_title(draw, title, y):
    """Draw the shield title centered"""
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

    return bbox[3] - bbox[1] + 17


def draw_separator(draw, y):
    """Draw a horizontal separator line"""
    x1 = SAFE_ZONE + BORDER_WIDTH + 5
    x2 = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5
    draw.line([(x1, y), (x2, y)], fill=COLOR_SEPARATOR, width=1)
    return 8


def draw_stat_box(draw, shield_data, y):
    """Draw the stats box with shield stats"""
    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10
    padding = 10
    row_height = 26

    # Shields need 2 rows of stats
    num_rows = 2
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

    # Row 1: Precio | Bon. CA | Imp.
    price = shield_data.get('price', '—')
    ac_bonus = shield_data.get('ac_bonus', '—')
    bulk = shield_data.get('bulk', '—')

    col1_x = x + padding
    col2_x = x + width // 3 + 10
    col3_x = x + 2 * width // 3

    draw_stat(col1_x, current_y, "Precio:", price, 8)
    draw_stat(col2_x, current_y, "Bon.CA:", ac_bonus, 8)
    draw_stat(col3_x, current_y, "Imp.:", bulk, 8)

    current_y += row_height

    # Row 2: Dureza | PG (UR)
    hardness = shield_data.get('hardness', '—')
    hp = shield_data.get('hp', '—')
    speed_pen = shield_data.get('speed_penalty', '—')

    draw_stat(col1_x, current_y, "Dureza:", hardness, 8)
    draw_stat(col2_x, current_y, "PG:", hp, 8)
    if speed_pen and speed_pen != '—':
        draw_stat(col3_x, current_y, "Pen.Vel.:", speed_pen, 8)

    return box_height + 6


def draw_description(draw, text, y, max_width, font_size=None):
    """Draw wrapped description text"""
    if not text:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE

    font = get_font(font_size)
    x = SAFE_ZONE + BORDER_WIDTH + 10

    # Calculate available width in pixels
    available_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 20

    # Use a representative test string for Spanish text
    test_text = "Este tipo de armadura es una cota de malla"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    test_width = bbox[2] - bbox[0]
    chars_per_line = int((available_width / test_width) * len(test_text))

    # Wrap text properly
    wrapped = textwrap.wrap(text, width=chars_per_line)

    # Draw each line
    total_height = 0
    line_spacing = LINE_HEIGHT - 2
    for i, line in enumerate(wrapped):
        draw.text((x, y + (i * line_spacing)), line, fill=COLOR_TEXT, font=font)
        total_height = (i + 1) * line_spacing

    return total_height + 4


def generate_shield_card(shield_data, output_path):
    """Generate a single shield card"""
    card, draw = create_card_base()

    # Start drawing content
    current_y = SAFE_ZONE + BORDER_WIDTH + 15

    # Title
    current_y += draw_title(draw, shield_data['name'], current_y)

    # Separator
    current_y += draw_separator(draw, current_y)
    current_y += 2

    # Stats box
    current_y += draw_stat_box(draw, shield_data, current_y)
    current_y += 6

    # Description
    description = shield_data.get('description', '')
    if description:
        content_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 20

        font_size = None
        if len(description) > 300:
            font_size = BODY_FONT_SIZE - 3

        current_y += draw_description(draw, description, current_y, content_width, font_size)

    # Convert to RGB and save
    rgb_card = Image.new('RGB', card.size, (255, 255, 255))
    rgb_card.paste(card, mask=card.split()[3] if card.mode == 'RGBA' else None)
    rgb_card.save(output_path, 'PNG', dpi=(300, 300))


def main():
    print("PF2e Shield Cards Generator")
    print("=" * 40)

    # Load shield data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    shields = data['shields']
    print(f"Found {len(shields)} shields to generate")
    print(f"Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ {DPI} DPI (63x88mm Magic)")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate cards
    for shield in shields:
        output_path = os.path.join(OUTPUT_DIR, f"{shield['id']}.png")
        try:
            generate_shield_card(shield, output_path)
            print(f"  + {shield['name']}")
        except Exception as e:
            print(f"  x Error generating {shield['name']}: {e}")

    print()
    print(f"+ Generated {len(shields)} cards in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
