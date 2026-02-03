#!/usr/bin/env python3
"""
PF2e Spell Cards Generator
Generates Magic-sized spell cards for Pathfinder 2e
Includes spell stats, traits, description and heightened effects
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

# Colors (RGB) - Purple/Arcane theme for spells
COLOR_BACKGROUND = (244, 238, 248)      # Light purple parchment
COLOR_BORDER = (75, 50, 100)            # Deep purple
COLOR_BORDER_CANTRIP = (60, 90, 110)    # Blue-gray for cantrips
COLOR_TRAIT_BG = (93, 48, 48)           # Darker red for traits (same as weapons)
COLOR_TRAIT_TEXT = (218, 165, 32)       # Gold text on traits
COLOR_TEXT = (45, 39, 34)               # Dark text
COLOR_TITLE = (75, 50, 100)             # Purple for title
COLOR_SEPARATOR = (125, 68, 55)         # Red for lines
COLOR_LABEL = (125, 68, 55)             # Red for labels
COLOR_STAT_BG = (235, 228, 242)         # Lighter purple for stat box
COLOR_HEIGHTENED_BG = (250, 245, 230)   # Light gold for heightened section
COLOR_TRADITION_ARCANA = (100, 50, 120) # Purple for arcana
COLOR_TRADITION_DIVINA = (180, 150, 50) # Gold for divine
COLOR_TRADITION_OCULTA = (80, 80, 100)  # Dark blue-gray for occult
COLOR_TRADITION_PRIMIGENIA = (60, 100, 60)  # Green for primal

# Layout
TITLE_Y = SAFE_ZONE + 12
TRAIT_HEIGHT = 28
TRAIT_PADDING = 6
LINE_HEIGHT = 24
SECTION_SPACING = 6

# Font sizes
TITLE_FONT_SIZE = 34
BODY_FONT_SIZE = 20  # +2 for description
TRAIT_FONT_SIZE = 15
LABEL_FONT_SIZE = 16
SMALL_FONT_SIZE = 14
HEIGHTENED_FONT_SIZE = 17
TABLE_FONT_SIZE = 11  # Smaller font for tables

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, 'assets', 'fonts')
DATA_FILE = os.path.join(SCRIPT_DIR, 'data', 'spells.json')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'generated_cards')

# Action icons - image paths
IMAGES_DIR = os.path.join(SCRIPT_DIR, 'assets', 'images')
ACTION_IMAGES = {
    1: os.path.join(IMAGES_DIR, 'Una_accion.png'),
    2: os.path.join(IMAGES_DIR, 'dos_acciones.png'),
    3: os.path.join(IMAGES_DIR, 'tres_acciones.png'),
    0: os.path.join(IMAGES_DIR, 'accion_libre.png'),
    'libre': os.path.join(IMAGES_DIR, 'accion_libre.png'),
    'reaccion': os.path.join(IMAGES_DIR, 'reaccion.png'),
}

# Cache for loaded action images
_action_image_cache = {}

def load_action_image(actions, target_height=20):
    """Load and resize action icon image"""
    global _action_image_cache

    cache_key = (actions, target_height)
    if cache_key in _action_image_cache:
        return _action_image_cache[cache_key]

    if actions not in ACTION_IMAGES:
        return None

    image_path = ACTION_IMAGES[actions]
    if not os.path.exists(image_path):
        return None

    try:
        img = Image.open(image_path).convert('RGBA')
        # Resize proportionally to target height
        ratio = target_height / img.height
        new_width = int(img.width * ratio)
        img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)
        _action_image_cache[cache_key] = img
        return img
    except Exception:
        return None


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


def draw_title_with_level(draw, spell_data, y, max_width):
    """Draw the spell title with level indicator"""
    name = spell_data['name']
    level = spell_data.get('level', '?')
    is_cantrip = spell_data.get('isCantrip', False)

    # Format level text
    if is_cantrip:
        level_text = "TRUCO"
    else:
        level_text = f"RANGO {level}"

    font = get_font(TITLE_FONT_SIZE, bold=True, display=True)
    # Double the size for rank text (LABEL_FONT_SIZE * 2 = 32)
    rank_font = get_font(LABEL_FONT_SIZE * 2, bold=True, display=True)

    # Calculate title width
    bbox = draw.textbbox((0, 0), name, font=font)
    title_width = bbox[2] - bbox[0]

    # Shrink title if needed
    current_size = TITLE_FONT_SIZE
    while title_width > max_width - 80 and current_size > 18:
        current_size -= 2
        font = get_font(current_size, bold=True, display=True)
        bbox = draw.textbbox((0, 0), name, font=font)
        title_width = bbox[2] - bbox[0]

    # Draw title centered
    x = (CARD_WIDTH - title_width) // 2
    draw.text((x, y), name, fill=COLOR_TITLE, font=font)

    title_height = bbox[3] - bbox[1]

    # Draw level below title with more margin
    level_bbox = draw.textbbox((0, 0), level_text, font=rank_font)
    level_width = level_bbox[2] - level_bbox[0]
    level_height = level_bbox[3] - level_bbox[1]
    level_x = (CARD_WIDTH - level_width) // 2
    level_y = y + title_height + 10  # More margin above rank

    draw.text((level_x, level_y), level_text, fill=COLOR_LABEL, font=rank_font)

    return title_height + level_height + 24  # More margin below rank


def draw_separator(draw, y):
    """Draw a horizontal separator line"""
    x1 = SAFE_ZONE + BORDER_WIDTH + 5
    x2 = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5
    draw.line([(x1, y), (x2, y)], fill=COLOR_SEPARATOR, width=1)
    return 6


def draw_traditions(draw, traditions, y):
    """Draw tradition icons/badges"""
    if not traditions:
        return 0

    font = get_font(SMALL_FONT_SIZE, bold=True, display=True)

    tradition_colors = {
        'arcana': COLOR_TRADITION_ARCANA,
        'divina': COLOR_TRADITION_DIVINA,
        'ocultista': COLOR_TRADITION_OCULTA,
        'primigenia': COLOR_TRADITION_PRIMIGENIA,
    }

    # Calculate total width
    total_width = 0
    tradition_boxes = []
    spacing = 4

    for tradition in traditions:
        text = tradition.upper()[:3]  # ARC, DIV, OCU, PRI
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        box_width = text_width + 10
        color = tradition_colors.get(tradition.lower(), COLOR_BORDER)
        tradition_boxes.append((text, box_width, text_width, color, tradition))
        total_width += box_width + spacing

    total_width -= spacing

    # Center the tradition boxes
    x = (CARD_WIDTH - total_width) // 2
    box_height = 22

    for text, box_width, text_width, color, tradition in tradition_boxes:
        draw.rounded_rectangle(
            [(x, y), (x + box_width, y + box_height)],
            radius=3,
            fill=color,
            outline=(255, 255, 255),
            width=1
        )
        text_x = x + (box_width - text_width) // 2
        text_y = y + 2
        draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
        x += box_width + spacing

    return box_height + 4


def draw_traits(draw, traits, y):
    """Draw trait boxes"""
    if not traits:
        return 0

    font = get_font(TRAIT_FONT_SIZE, bold=True, display=True)

    total_width = 0
    trait_boxes = []
    spacing = 4

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


def draw_stat_box(draw, spell_data, y, card_image=None):
    """Draw the stats box with spell info.
    Any field that doesn't fit in half-width automatically becomes full-width with wrapping.
    Never uses ellipsis - text always wraps to multiple lines if needed.
    """
    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10
    padding = 10
    row_height = 24

    # Fonts
    label_font = get_font(LABEL_FONT_SIZE + 2, bold=True, display=True)
    value_font = get_font(SMALL_FONT_SIZE + 2)

    # Collect all stats as (label, value, icon)
    all_stats = []

    # Actions or casting time
    actions = spell_data.get('actions')
    casting_time = spell_data.get('casting_time')
    if casting_time:
        all_stats.append(("Lanzamiento:", casting_time, None))
    elif actions:
        action_icon = load_action_image(actions, target_height=20)
        if action_icon:
            all_stats.append(("Acciones:", None, action_icon))
        else:
            all_stats.append(("Acciones:", str(actions), None))

    if 'range' in spell_data:
        all_stats.append(("Rango:", spell_data['range'], None))
    if 'area' in spell_data:
        all_stats.append(("Área:", spell_data['area'], None))
    if 'duration' in spell_data:
        all_stats.append(("Duración:", spell_data['duration'], None))
    if 'defense' in spell_data:
        all_stats.append(("Defensa:", spell_data['defense'], None))
    if 'targets' in spell_data:
        all_stats.append(("Objetivos:", spell_data['targets'], None))

    if not all_stats:
        return 0

    # Calculate half-width available for values
    half_width = (width // 2) - padding - 15

    # Helper to wrap text to lines
    def wrap_text(text, max_pixel_width):
        if not text:
            return []
        bbox = draw.textbbox((0, 0), text, font=value_font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_pixel_width:
            return [text]
        # Calculate chars per line
        if len(text) > 0:
            char_width = text_width / len(text)
            chars_per_line = max(10, int(max_pixel_width / char_width))
            return textwrap.wrap(text, width=chars_per_line)
        return [text]

    # Classify stats: determine which fit in half-width and which need full-width
    # Process in order, building rows
    rows = []  # Each row is either ('pair', stat1, stat2) or ('full', stat, lines)

    i = 0
    while i < len(all_stats):
        label, value, icon = all_stats[i]

        # Calculate label width
        label_bbox = draw.textbbox((0, 0), label, font=label_font)
        label_width = label_bbox[2] - label_bbox[0]

        # Check if value fits in half-width
        fits_half = False
        if icon:
            fits_half = True  # Icons always fit
        elif value:
            value_bbox = draw.textbbox((0, 0), value, font=value_font)
            value_width = value_bbox[2] - value_bbox[0]
            available_half = half_width - label_width - 10
            fits_half = value_width <= available_half

        if fits_half:
            # Try to pair with next stat if it also fits
            if i + 1 < len(all_stats):
                next_label, next_value, next_icon = all_stats[i + 1]
                next_label_bbox = draw.textbbox((0, 0), next_label, font=label_font)
                next_label_width = next_label_bbox[2] - next_label_bbox[0]

                next_fits = False
                if next_icon:
                    next_fits = True
                elif next_value:
                    next_value_bbox = draw.textbbox((0, 0), next_value, font=value_font)
                    next_value_width = next_value_bbox[2] - next_value_bbox[0]
                    next_available = half_width - next_label_width - 10
                    next_fits = next_value_width <= next_available

                if next_fits:
                    # Pair them
                    rows.append(('pair', all_stats[i], all_stats[i + 1]))
                    i += 2
                    continue

            # Single stat in half-width (no pair available or next doesn't fit)
            rows.append(('pair', all_stats[i], None))
            i += 1
        else:
            # Full-width: wrap text to multiple lines
            full_width_available = width - label_width - padding * 2 - 10
            lines = wrap_text(value, full_width_available)
            rows.append(('full', all_stats[i], lines))
            i += 1

    # Calculate total rows needed
    total_row_count = 0
    for row in rows:
        if row[0] == 'pair':
            total_row_count += 1
        else:  # full
            lines = row[2]
            total_row_count += max(1, len(lines))

    box_height = padding * 2 + (total_row_count * row_height)

    # Draw background box
    draw.rounded_rectangle(
        [(x, y), (x + width, y + box_height)],
        radius=5,
        fill=COLOR_STAT_BG,
        outline=COLOR_BORDER,
        width=1
    )

    current_y = y + padding
    col1_x = x + padding
    col2_x = x + width // 2

    # Draw rows
    for row in rows:
        if row[0] == 'pair':
            stat1 = row[1]
            stat2 = row[2]

            # Draw first stat
            label, value, icon = stat1
            draw.text((col1_x, current_y), label, fill=COLOR_LABEL, font=label_font)
            bbox = draw.textbbox((0, 0), label, font=label_font)
            label_width = bbox[2] - bbox[0]

            if icon and card_image:
                icon_x = int(col1_x + label_width + 6)
                icon_y = int(current_y + 1)
                card_image.paste(icon, (icon_x, icon_y), icon)
            elif value:
                draw.text((col1_x + label_width + 4, current_y + 1), value, fill=COLOR_TEXT, font=value_font)

            # Draw second stat if exists
            if stat2:
                label2, value2, icon2 = stat2
                draw.text((col2_x, current_y), label2, fill=COLOR_LABEL, font=label_font)
                bbox2 = draw.textbbox((0, 0), label2, font=label_font)
                label_width2 = bbox2[2] - bbox2[0]

                if icon2 and card_image:
                    icon_x = int(col2_x + label_width2 + 6)
                    icon_y = int(current_y + 1)
                    card_image.paste(icon2, (icon_x, icon_y), icon2)
                elif value2:
                    draw.text((col2_x + label_width2 + 4, current_y + 1), value2, fill=COLOR_TEXT, font=value_font)

            current_y += row_height

        else:  # full-width
            stat = row[1]
            lines = row[2]
            label, value, icon = stat

            draw.text((col1_x, current_y), label, fill=COLOR_LABEL, font=label_font)
            bbox = draw.textbbox((0, 0), label, font=label_font)
            label_width = bbox[2] - bbox[0]

            # Draw lines
            if lines:
                draw.text((col1_x + label_width + 4, current_y + 1), lines[0], fill=COLOR_TEXT, font=value_font)
                current_y += row_height

                for line in lines[1:]:
                    draw.text((col1_x + label_width + 4, current_y + 1), line, fill=COLOR_TEXT, font=value_font)
                    current_y += row_height
            else:
                current_y += row_height

    return box_height + 4


def parse_markdown_table(text):
    """Parse markdown table and return header and rows.
    Returns (title, headers, rows) or None if not a table.
    """
    lines = text.strip().split('\n')
    title = None
    table_start = 0

    # Check for ### title before table
    for i, line in enumerate(lines):
        if line.startswith('###'):
            title = line.replace('###', '').strip()
            table_start = i + 1
            break

    # Find table lines (lines with |)
    table_lines = []
    for i in range(table_start, len(lines)):
        line = lines[i].strip()
        if line.startswith('|') and line.endswith('|'):
            table_lines.append(line)
        elif table_lines:  # Stop at first non-table line after table started
            break

    if len(table_lines) < 2:
        return None

    # Parse header
    header_line = table_lines[0]
    headers = [h.strip() for h in header_line.split('|')[1:-1]]

    # Skip separator line (|---|---|)
    # Parse data rows
    rows = []
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells:
            rows.append(cells)

    return (title, headers, rows)


def draw_table(draw, title, headers, rows, y, max_width, card_image=None):
    """Draw a markdown table on the card.
    Returns total height used.
    """
    x = SAFE_ZONE + BORDER_WIDTH + 5
    font = get_font(TABLE_FONT_SIZE)
    bold_font = get_font(TABLE_FONT_SIZE, bold=True)
    title_font = get_font(TABLE_FONT_SIZE + 2, bold=True)

    line_height = TABLE_FONT_SIZE + 4
    padding = 3
    total_height = 0

    # Draw title if present
    if title:
        draw.text((x, y), title, fill=COLOR_LABEL, font=title_font)
        total_height += line_height + 2

    current_y = y + total_height

    # Calculate column widths based on content
    num_cols = len(headers)
    available_width = max_width - 10

    # Measure max width needed for each column
    col_widths = []
    for i in range(num_cols):
        max_col_width = 0
        # Check header
        bbox = draw.textbbox((0, 0), headers[i], font=bold_font)
        max_col_width = max(max_col_width, bbox[2] - bbox[0])
        # Check all rows
        for row in rows:
            if i < len(row):
                bbox = draw.textbbox((0, 0), row[i], font=font)
                max_col_width = max(max_col_width, bbox[2] - bbox[0])
        col_widths.append(max_col_width + padding * 2)

    # Scale down if total width exceeds available
    total_cols_width = sum(col_widths)
    if total_cols_width > available_width:
        scale = available_width / total_cols_width
        col_widths = [int(w * scale) for w in col_widths]

    # Draw header row with background
    header_height = line_height + 2
    draw.rectangle(
        [(x, current_y), (x + sum(col_widths), current_y + header_height)],
        fill=COLOR_STAT_BG
    )

    col_x = x
    for i, header in enumerate(headers):
        if i < len(col_widths):
            # Truncate header if too long
            text = header
            bbox = draw.textbbox((0, 0), text, font=bold_font)
            while bbox[2] - bbox[0] > col_widths[i] - padding * 2 and len(text) > 3:
                text = text[:-1]
                bbox = draw.textbbox((0, 0), text, font=bold_font)
            draw.text((col_x + padding, current_y + padding), text, fill=COLOR_LABEL, font=bold_font)
            col_x += col_widths[i]

    current_y += header_height
    total_height += header_height

    # Draw data rows
    for row_idx, row in enumerate(rows):
        row_bg = COLOR_BACKGROUND if row_idx % 2 == 0 else (250, 245, 252)
        draw.rectangle(
            [(x, current_y), (x + sum(col_widths), current_y + line_height)],
            fill=row_bg
        )

        col_x = x
        for i, cell in enumerate(row):
            if i < len(col_widths):
                # Truncate cell if too long
                text = cell
                bbox = draw.textbbox((0, 0), text, font=font)
                while bbox[2] - bbox[0] > col_widths[i] - padding * 2 and len(text) > 3:
                    text = text[:-1]
                    bbox = draw.textbbox((0, 0), text, font=font)
                draw.text((col_x + padding, current_y + 1), text, fill=COLOR_TEXT, font=font)
                col_x += col_widths[i]

        current_y += line_height
        total_height += line_height

    # Draw border around table
    draw.rectangle(
        [(x, y + (line_height + 2 if title else 0)), (x + sum(col_widths), current_y)],
        outline=COLOR_SEPARATOR,
        width=1
    )

    return total_height + 4


def clean_markdown_for_wrap(text):
    """Remove markdown for text wrapping calculation, but keep content."""
    # Remove Jekyll includes for wrapping calculation
    clean = re.sub(r'\{%\s*include\s+accion\.html\s+tipo="[^"]*"\s*%\}', '◆', text)
    # Remove bold markers for length calculation
    clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)
    return clean


def draw_rich_line(draw, line, x, y, font_size, card_image=None):
    """Draw a line with markdown support (bold, action icons).
    Returns the width drawn.
    """
    font = get_font(font_size)
    bold_font = get_font(font_size, bold=True)

    current_x = x

    # Convert Jekyll action includes to markers first
    line = re.sub(r'\{%\s*include\s+accion\.html\s+tipo="1"\s*%\}', '{{ACTION1}}', line)
    line = re.sub(r'\{%\s*include\s+accion\.html\s+tipo="2"\s*%\}', '{{ACTION2}}', line)
    line = re.sub(r'\{%\s*include\s+accion\.html\s+tipo="3"\s*%\}', '{{ACTION3}}', line)
    line = re.sub(r'\{%\s*include\s+accion\.html\s+tipo="libre"\s*%\}', '{{ACTION0}}', line)
    line = re.sub(r'\{%\s*include\s+accion\.html\s+tipo="reaccion"\s*%\}', '{{ACTIONR}}', line)

    # Parse the line into segments: (text, is_bold, is_action)
    segments = []
    pattern = r'(\*\*[^*]+\*\*|\{\{ACTION[0123R]\}\})'
    parts = re.split(pattern, line)

    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            # Bold text
            segments.append((part[2:-2], True, None))
        elif part.startswith('{{ACTION') and part.endswith('}}'):
            # Action icon
            action_type = part[8:-2]
            action_map = {'1': 1, '2': 2, '3': 3, '0': 0, 'R': 'reaccion'}
            segments.append((None, False, action_map.get(action_type, 1)))
        else:
            # Normal text
            segments.append((part, False, None))

    # Draw each segment
    for text, is_bold, action_type in segments:
        if action_type is not None:
            # Draw action icon
            icon = load_action_image(action_type, target_height=int(font_size * 0.9))
            if icon and card_image:
                icon_y = int(y + (font_size - icon.height) // 2)
                card_image.paste(icon, (int(current_x), icon_y), icon)
                current_x += icon.width + 2
            else:
                # Fallback to symbol
                symbol = {'1': '◆', '2': '◆◆', '3': '◆◆◆', '0': '◇', 'reaccion': '↺'}.get(action_type, '◆')
                draw.text((current_x, y), symbol, fill=COLOR_TEXT, font=font)
                bbox = draw.textbbox((0, 0), symbol, font=font)
                current_x += bbox[2] - bbox[0] + 2
        elif text:
            use_font = bold_font if is_bold else font
            draw.text((current_x, y), text, fill=COLOR_TEXT, font=use_font)
            bbox = draw.textbbox((0, 0), text, font=use_font)
            current_x += bbox[2] - bbox[0]

    return current_x - x


def draw_description(draw, text, y, max_width, font_size=None, max_lines=None, card_image=None):
    """Draw wrapped description text with markdown support (bold, action icons, tables)."""
    if not text:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE

    font = get_font(font_size)
    x = SAFE_ZONE + BORDER_WIDTH + 8

    # Check if text contains a markdown table (### heading followed by | lines)
    table_match = re.search(r'(###[^\n]+\n\n?\|[^|]+\|.+?)(?=\*\*Potenciado|\Z)', text, re.DOTALL)

    if table_match:
        # Split text into before-table and table parts
        table_start = table_match.start()
        before_table = text[:table_start].strip()
        table_text = table_match.group(1).strip()

        total_height = 0
        current_y = y

        # Draw text before table
        if before_table:
            height = draw_text_block(draw, before_table, current_y, max_width, font_size, max_lines, card_image)
            total_height += height
            current_y += height

        # Parse and draw the table
        table_data = parse_markdown_table(table_text)
        if table_data:
            title, headers, rows = table_data
            table_height = draw_table(draw, title, headers, rows, current_y, max_width, card_image)
            total_height += table_height

        return total_height
    else:
        # No table, draw as regular text
        return draw_text_block(draw, text, y, max_width, font_size, max_lines, card_image)


def draw_text_block(draw, text, y, max_width, font_size=None, max_lines=None, card_image=None):
    """Draw a block of text with word wrapping and markdown support."""
    if not text:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE

    font = get_font(font_size)
    x = SAFE_ZONE + BORDER_WIDTH + 8

    # Clean text for wrapping calculation
    clean_text = clean_markdown_for_wrap(text)

    # Calculate characters per line using Spanish text sample
    test_text = "Este conjuro es una demostración de magia"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    test_width = bbox[2] - bbox[0]
    chars_per_line = int((max_width / test_width) * len(test_text))

    # Wrap the clean text to get line breaks
    clean_wrapped = textwrap.wrap(clean_text, width=chars_per_line)

    # If max_lines specified, just cut at line boundary (no ellipsis)
    if max_lines and len(clean_wrapped) > max_lines:
        clean_wrapped = clean_wrapped[:max_lines]

    # Now we need to map back to original text with markdown
    # Split original text by words and rebuild lines
    original_words = text.split()

    # Build a mapping from clean words to original words
    lines_with_markdown = []
    word_idx = 0

    for clean_line in clean_wrapped:
        line_words = []
        clean_line_words = clean_line.split()
        for cw in clean_line_words:
            if word_idx < len(original_words):
                line_words.append(original_words[word_idx])
                word_idx += 1
        lines_with_markdown.append(' '.join(line_words))

    total_height = 0
    line_spacing = font_size + 4

    for i, line in enumerate(lines_with_markdown):
        draw_rich_line(draw, line, x, y + (i * line_spacing), font_size, card_image)
        total_height = (i + 1) * line_spacing

    return total_height + 2


def draw_results(draw, results, y, max_width, font_size=None):
    """Draw success/failure results section"""
    if not results:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE  # Same size as description

    labels = [
        ('criticalSuccess', 'Éxito crítico'),
        ('success', 'Éxito'),
        ('failure', 'Fallo'),
        ('criticalFailure', 'Fallo crítico')
    ]

    total_height = 0
    x = SAFE_ZONE + BORDER_WIDTH + 8

    for key, label in labels:
        text = results.get(key)
        if text:
            height = draw_result_item(draw, label, text, y + total_height, max_width, font_size)
            total_height += height

    return total_height


def draw_result_item(draw, label, text, y, max_width, font_size):
    """Draw a single result item (Éxito crítico, Éxito, etc.)"""
    if not text:
        return 0

    label_font = get_font(font_size, bold=True, display=True)
    text_font = get_font(font_size)

    x = SAFE_ZONE + BORDER_WIDTH + 8

    # Draw label in red
    draw.text((x, y), f"{label}:", fill=COLOR_LABEL, font=label_font)
    label_bbox = draw.textbbox((0, 0), f"{label}:", font=label_font)
    label_width = label_bbox[2] - label_bbox[0]

    # Calculate chars per line
    test_text = "Este es un texto de prueba para medir"
    bbox = draw.textbbox((0, 0), test_text, font=text_font)
    test_width = bbox[2] - bbox[0]

    # First line has less space (after label)
    first_line_width = max_width - label_width - 15
    chars_first_line = int((first_line_width / test_width) * len(test_text))
    chars_rest = int((max_width / test_width) * len(test_text))

    # Wrap text
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    is_first = True

    for word in words:
        max_chars = chars_first_line if is_first else chars_rest
        if current_length + len(word) + 1 <= max_chars:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
                is_first = False
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(' '.join(current_line))

    # Draw lines
    line_height = font_size + 3
    total_height = 0
    for i, line in enumerate(lines):
        if i == 0:
            draw.text((x + label_width + 5, y), line, fill=COLOR_TEXT, font=text_font)
        else:
            draw.text((x, y + (i * line_height)), line, fill=COLOR_TEXT, font=text_font)
        total_height = (i + 1) * line_height

    return max(line_height, total_height) + 2


def draw_heightened(draw, heightened_effects, y, max_width, remaining_space):
    """Draw heightened effects section.
    Never uses ellipsis - all text wraps naturally to multiple lines.
    Box adjusts to fit all content.
    """
    if not heightened_effects:
        return 0

    x = SAFE_ZONE + BORDER_WIDTH + 5
    width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 10
    padding = 6

    font = get_font(HEIGHTENED_FONT_SIZE)
    label_font = get_font(HEIGHTENED_FONT_SIZE, bold=True, display=True)

    # Calculate chars per line
    test_text = "Potenciado nivel descripción efecto"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    test_width = bbox[2] - bbox[0]
    chars_per_line = int(((width - padding * 2 - 10) / test_width) * len(test_text))

    line_height = HEIGHTENED_FONT_SIZE + 3
    lines = []

    for effect in heightened_effects:
        level = effect['level']
        desc = effect['effect']

        # Wrap full text without truncation
        prefix = f"({level})"
        wrapped = textwrap.wrap(f"{prefix} {desc}", width=chars_per_line)
        lines.extend(wrapped)

    # Calculate total height needed
    total_height = padding + line_height + len(lines) * line_height + padding

    # If it doesn't fit, we still show as much as possible but WITHOUT ellipsis
    # Just cut at line boundaries
    if total_height > remaining_space - 5:
        available_for_lines = remaining_space - 5 - padding * 2 - line_height
        max_lines = max(1, int(available_for_lines // line_height))
        lines = lines[:max_lines]
        total_height = padding + line_height + len(lines) * line_height + padding

    # Draw background
    draw.rounded_rectangle(
        [(x, y), (x + width, y + total_height)],
        radius=5,
        fill=COLOR_HEIGHTENED_BG,
        outline=COLOR_SEPARATOR,
        width=1
    )

    # Draw title "POTENCIADO"
    current_y = y + padding
    draw.text((x + padding, current_y), "POTENCIADO", fill=COLOR_LABEL, font=label_font)

    # Draw effects below title
    current_y += line_height
    for line in lines:
        draw.text((x + padding, current_y), line, fill=COLOR_TEXT, font=font)
        current_y += line_height

    return total_height + 4


def generate_spell_card(spell_data, output_path):
    """Generate a single spell card"""
    is_cantrip = spell_data.get('isCantrip', False)
    border_color = COLOR_BORDER_CANTRIP if is_cantrip else COLOR_BORDER

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

    # Draw title with level
    title_height = draw_title_with_level(draw, spell_data, current_y, content_width)
    current_y += title_height

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Draw traditions
    traditions = spell_data.get('traditions', [])
    if traditions:
        current_y += draw_traditions(draw, traditions, current_y)
        current_y += 2

    # Draw traits
    traits = spell_data.get('traits', [])
    if traits:
        current_y += draw_traits(draw, traits, current_y)
        current_y += draw_separator(draw, current_y)

    # Draw stat box (pass card image for action icons)
    stat_height = draw_stat_box(draw, spell_data, current_y, card)
    if stat_height > 0:
        current_y += stat_height
        current_y += draw_separator(draw, current_y)

    # Calculate remaining space for description, results, and heightened
    # Maximum Y position to stay within card bounds
    max_y = CARD_HEIGHT - SAFE_ZONE - BORDER_WIDTH - 5

    heightened = spell_data.get('heightened', [])
    results = spell_data.get('results', {})
    description = spell_data.get('description', '')

    # Reserve space for heightened if present
    heightened_reserve = 80 if heightened else 0

    # Calculate available space for description
    available_for_desc = max_y - current_y - heightened_reserve

    # Draw description with strict space limit
    if description and available_for_desc > 50:
        font_size = BODY_FONT_SIZE

        # Reduce font for very long descriptions
        if len(description) > 800:
            font_size = BODY_FONT_SIZE - 4
        elif len(description) > 500:
            font_size = BODY_FONT_SIZE - 2

        line_height = font_size + 4
        max_lines = max(3, int(available_for_desc / line_height) - 1)

        desc_height = draw_description(draw, description, current_y, content_width, font_size, max_lines, card)
        current_y += desc_height

        # Safety check - don't exceed bounds
        if current_y > max_y - heightened_reserve:
            current_y = max_y - heightened_reserve

    # Draw save results only if space remains
    if results and current_y < max_y - heightened_reserve - 60:
        available_for_results = max_y - current_y - heightened_reserve
        results_height = draw_results(draw, results, current_y, content_width, font_size if description else BODY_FONT_SIZE)
        # Limit results height
        if results_height > available_for_results:
            results_height = available_for_results
        current_y += min(results_height, available_for_results)

    # Draw heightened effects with remaining space
    remaining_space = max_y - current_y
    if heightened and remaining_space > 40:
        current_y += draw_separator(draw, current_y)
        remaining_space = max_y - current_y
        draw_heightened(draw, heightened, current_y, content_width, remaining_space)

    # Convert to RGB and save
    rgb_card = Image.new('RGB', card.size, (255, 255, 255))
    rgb_card.paste(card, mask=card.split()[3] if card.mode == 'RGBA' else None)
    rgb_card.save(output_path, 'PNG', dpi=(300, 300))


def main():
    """Main function to generate all spell cards"""
    print("PF2e Spell Cards Generator")
    print("=" * 40)
    print()

    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found: {DATA_FILE}")
        print("Please run parse_spells.py first!")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    spells = data.get('spells', [])
    print(f"Found {len(spells)} spells to generate")
    print(f"Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ 300 DPI (63x88mm Magic)")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group by level for organization
    spells_by_level = {}
    for spell in spells:
        level = spell.get('level', 'unknown')
        if level == 'TRUCO':
            folder = 'cantrips'
        else:
            folder = f'rank-{level}'
        if folder not in spells_by_level:
            spells_by_level[folder] = []
        spells_by_level[folder].append(spell)

    total_generated = 0
    for folder, folder_spells in sorted(spells_by_level.items()):
        folder_dir = os.path.join(OUTPUT_DIR, folder)
        os.makedirs(folder_dir, exist_ok=True)

        print(f"Generating {folder} ({len(folder_spells)} spells)...")
        for spell in folder_spells:
            spell_id = spell['id']
            output_file = os.path.join(folder_dir, f"{spell_id}.png")

            try:
                generate_spell_card(spell, output_file)
                print(f"  ✓ {spell['name']}")
                total_generated += 1
            except Exception as e:
                print(f"  ✗ Error generating {spell['name']}: {e}")
                import traceback
                traceback.print_exc()

        print()

    print(f"✓ Generated {total_generated} cards in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
