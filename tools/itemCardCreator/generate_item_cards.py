#!/usr/bin/env python3
"""
PF2e Item Cards Generator
Generates Magic-sized item cards for Pathfinder 2e
Uses brown/leather theme for items/equipment
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json
import textwrap

# Card specifications (300 DPI for print quality)
# Magic card size: 63mm x 88mm
CARD_WIDTH = 744    # 63mm at 300 DPI
CARD_HEIGHT = 1039  # 88mm at 300 DPI
SAFE_ZONE = 24      # 2mm safe zone
CORNER_RADIUS = 30  # 2.5mm rounded corners
BORDER_WIDTH = 8    # Border thickness

# Colors (RGB) - Brown/leather theme for items
COLOR_BACKGROUND = (248, 241, 230)      # Light cream/parchment
COLOR_BORDER = (101, 67, 33)            # Dark brown (leather)
COLOR_TRAIT_BG = (139, 90, 43)          # Medium brown
COLOR_TRAIT_TEXT = (255, 248, 220)      # Cream/cornsilk
COLOR_TEXT = (45, 39, 34)               # Dark text
COLOR_TITLE = (101, 67, 33)             # Dark brown for title
COLOR_SEPARATOR = (139, 90, 43)         # Medium brown for lines
COLOR_LABEL = (139, 90, 43)             # Medium brown for labels
COLOR_STAT_BG = (235, 222, 200)         # Lighter parchment for stat box

# Layout
TITLE_Y = SAFE_ZONE + 12
LINE_HEIGHT = 24
SECTION_SPACING = 6

# Font sizes
TITLE_FONT_SIZE = 38
BODY_FONT_SIZE = 22
LABEL_FONT_SIZE = 20
SMALL_FONT_SIZE = 18

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, 'assets', 'fonts')
DATA_FILE = os.path.join(SCRIPT_DIR, 'data', 'items.json')
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
    """Draw the item title"""
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

    return bbox[3] - bbox[1] + 17


def draw_separator(draw, y):
    """Draw a horizontal separator line"""
    x1 = SAFE_ZONE + BORDER_WIDTH + 5
    x2 = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5
    draw.line([(x1, y), (x2, y)], fill=COLOR_SEPARATOR, width=1)
    return 8


def draw_stat_box(draw, item_data, y):
    """Draw the stats box with item stats"""
    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10
    padding = 12
    row_height = 30

    # Determine number of rows needed
    has_hands = 'hands' in item_data
    num_rows = 2 if has_hands else 1
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
    def draw_stat(sx, sy, label, value, spacing=12):
        draw.text((sx, sy), label, fill=COLOR_LABEL, font=label_font)
        bbox = draw.textbbox((0, 0), label, font=label_font)
        label_width = bbox[2] - bbox[0]
        draw.text((sx + label_width + spacing, sy), value, fill=COLOR_TEXT, font=value_font)

    # Row 1: Precio | Impedimenta
    price = item_data.get('price', '—')
    bulk = item_data.get('bulk', '—')

    col1_x = x + padding
    col2_x = x + width // 2 + 20

    draw_stat(col1_x, current_y, "Precio:", price, 12)
    draw_stat(col2_x, current_y, "Imp.:", bulk, 12)

    current_y += row_height

    # Row 2 (if hands): Manos
    if has_hands:
        hands = item_data.get('hands', '—')
        draw_stat(col1_x, current_y, "Manos:", hands, 12)

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


def generate_item_card(item_data, output_path):
    """Generate a single item card"""
    # Create base card
    card = create_rounded_rectangle(
        (CARD_WIDTH, CARD_HEIGHT),
        CORNER_RADIUS,
        COLOR_BACKGROUND,
        COLOR_BORDER,
        BORDER_WIDTH
    )

    draw = ImageDraw.Draw(card)

    content_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 8

    current_y = TITLE_Y

    # Draw title
    title_height = draw_title(draw, item_data['name'], current_y, content_width)
    current_y += title_height

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Draw stat box
    stat_height = draw_stat_box(draw, item_data, current_y)
    current_y += stat_height

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Draw description
    description = item_data.get('description', '')
    if description:
        current_y += 4
        # Calculate remaining space
        remaining_space = CARD_HEIGHT - current_y - SAFE_ZONE - 20

        # Adjust font size based on content length
        font_size = BODY_FONT_SIZE
        if len(description) > 300 or remaining_space < 200:
            font_size = BODY_FONT_SIZE - 2
        if len(description) > 500 or remaining_space < 150:
            font_size = BODY_FONT_SIZE - 4
        if len(description) > 700:
            font_size = BODY_FONT_SIZE - 6

        draw_description(draw, description, current_y, content_width, font_size)

    # Convert to RGB and save
    rgb_card = Image.new('RGB', card.size, (255, 255, 255))
    rgb_card.paste(card, mask=card.split()[3] if card.mode == 'RGBA' else None)
    rgb_card.save(output_path, 'PNG', dpi=(300, 300))


def main():
    """Main function to generate all item cards"""
    print("PF2e Item Cards Generator")
    print("=" * 40)
    print()

    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found: {DATA_FILE}")
        print("Please run parse_items.py first!")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data.get('items', [])
    print(f"Found {len(items)} items to generate")
    print(f"Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ 300 DPI (63x88mm Magic)")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_generated = 0
    for item in items:
        item_id = item['id']
        output_file = os.path.join(OUTPUT_DIR, f"{item_id}.png")

        try:
            generate_item_card(item, output_file)
            print(f"  ✓ {item['name']}")
            total_generated += 1
        except Exception as e:
            print(f"  ✗ Error generating {item['name']}: {e}")
            import traceback
            traceback.print_exc()

    print()
    print(f"✓ Generated {total_generated} cards in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
