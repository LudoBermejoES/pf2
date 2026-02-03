#!/usr/bin/env python3
"""
PF2e Action Cards Generator
Generates Magic-sized action cards for Pathfinder 2e
Based on the Arcadia deck generator
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

# Colors (RGB) - Based on PF2e web theme
COLOR_BACKGROUND = (244, 228, 201)      # Parchment #f4e4c9
COLOR_BORDER = (125, 68, 55)            # PF red #7d4437
COLOR_TRAIT_BG = (93, 48, 48)           # Darker red for traits
COLOR_TRAIT_TEXT = (218, 165, 32)       # Gold text on traits
COLOR_TEXT = (45, 39, 34)               # Dark text #2d2722
COLOR_TITLE = (184, 134, 11)            # Gold for title #b8860b
COLOR_SEPARATOR = (125, 68, 55)         # Red for lines
COLOR_LABEL = (125, 68, 55)             # Red for labels

# Layout - Large and readable for Magic card size
TITLE_Y = SAFE_ZONE + 12
ICON_SIZE = 60
TRAIT_HEIGHT = 32
TRAIT_PADDING = 8
LINE_HEIGHT = 28
SECTION_SPACING = 8

# Font sizes - Extra large for readability
TITLE_FONT_SIZE = 44
BODY_FONT_SIZE = 24
TRAIT_FONT_SIZE = 17
LABEL_FONT_SIZE = 20

# Action type icon mapping
ACTION_ICONS = {
    '1': 'Una_accion.png',
    '2': 'dos_acciones.png',
    '3': 'tres_acciones.png',
    'reaction': 'reaccion.png',
    'free': 'accion_libre.png'
}

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(SCRIPT_DIR, 'assets', 'icons')
FONTS_DIR = os.path.join(SCRIPT_DIR, 'assets', 'fonts')
DATA_FILE = os.path.join(SCRIPT_DIR, 'data', 'actions.json')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'generated_cards')

def get_font(size, bold=False, display=False):
    """Load a font with fallback options - using Cinzel for display, Oldenburg for body"""

    if display:
        # Display font (titles) - Cinzel with multiple weight options
        if bold:
            font_paths = [
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-Bold.ttf'),
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-SemiBold.ttf'),
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-ExtraBold.ttf'),
            ]
        else:
            font_paths = [
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-Regular.ttf'),
                os.path.join(FONTS_DIR, 'Cinzel', 'static', 'Cinzel-Medium.ttf'),
            ]
        # Add fallbacks
        font_paths.extend([
            os.path.join(FONTS_DIR, 'Cinzel', 'Cinzel-VariableFont_wght.ttf'),
            "/System/Library/Fonts/Times.ttc",
            "/Library/Fonts/Times New Roman.ttf",
        ])
    else:
        # Body font - Oldenburg (only has Regular variant)
        font_paths = [
            os.path.join(FONTS_DIR, 'Oldenburg-Regular.ttf'),
            # Fallbacks for body text
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/Library/Fonts/Georgia.ttf",
            "/System/Library/Fonts/Times.ttc",
        ]

    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except Exception:
            continue

    return ImageFont.load_default()

def clean_text(text, remove_traits=True):
    """Clean markdown references but keep bold/italic markers for later rendering"""
    if not text:
        return ""

    # Remove links like [ver](/reglas/...) or (ver)
    text = re.sub(r'\[ver\]\([^)]+\)', '', text)
    text = re.sub(r'\(ver\)', '', text)

    # Remove page references like (pag. 420) or (pág. 420 ([ver](/...)))
    text = re.sub(r'\(p[aá]g\.?\s*\d+[^)]*\)', '', text)
    text = re.sub(r'\(\s*\[ver\][^)]*\)', '', text)

    # Remove orphan parentheses with just references
    text = re.sub(r'\(\s*\)', '', text)

    # Remove "**Rasgos:** ..." pattern that leaked into description
    if remove_traits:
        # Remove **Rasgos:** followed by trait names (Concentrar, Manipular, etc.)
        text = re.sub(r'\*\*Rasgos:\*\*\s*[A-Za-záéíóúñÁÉÍÓÚÑ,\s]+(?=\*\*|$|\s[A-Z])', '', text)
        # Remove trait markers at start (they're shown separately in trait boxes)
        text = re.sub(r'^\*\*(CONCENTRAR|SECRETO|MOVIMIENTO|ATAQUE|MANIPULAR|AUDITIVO|VISUAL)\*\*\s*', '', text.strip())
        text = re.sub(r'^(CONCENTRAR|SECRETO|MOVIMIENTO|ATAQUE|MANIPULAR|AUDITIVO|VISUAL)\s*', '', text.strip())

    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing punctuation issues
    text = text.strip(' .,')

    return text.strip()

def parse_styled_text(text):
    """Parse text and return list of (text, is_bold, is_italic) tuples"""
    if not text:
        return []

    segments = []
    current_pos = 0

    # Pattern for **bold** and *italic*
    pattern = r'(\*\*([^*]+)\*\*|\*([^*]+)\*)'

    for match in re.finditer(pattern, text):
        # Add text before this match as normal
        if match.start() > current_pos:
            plain_text = text[current_pos:match.start()]
            if plain_text:
                segments.append((plain_text, False, False))

        # Determine if it's bold or italic
        if match.group(2):  # **bold**
            segments.append((match.group(2), True, False))
        elif match.group(3):  # *italic*
            segments.append((match.group(3), False, True))

        current_pos = match.end()

    # Add remaining text
    if current_pos < len(text):
        remaining = text[current_pos:]
        if remaining:
            segments.append((remaining, False, False))

    # If no segments found, return entire text as plain
    if not segments:
        segments.append((text, False, False))

    return segments

def create_rounded_rectangle(size, radius, fill_color, border_color=None, border_width=0):
    """Create a rounded rectangle image"""
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw border first if specified
    if border_color and border_width > 0:
        draw.rounded_rectangle(
            [(0, 0), (size[0]-1, size[1]-1)],
            radius=radius,
            fill=border_color
        )
        # Draw inner fill
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

def draw_action_icon(card, action_type, x, y):
    """Draw the action type icon"""
    icon_file = ACTION_ICONS.get(action_type, ACTION_ICONS['1'])
    icon_path = os.path.join(ICONS_DIR, icon_file)

    if os.path.exists(icon_path):
        try:
            icon = Image.open(icon_path)
            # Resize icon
            icon = icon.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
            # Convert to RGBA if needed
            if icon.mode != 'RGBA':
                icon = icon.convert('RGBA')
            card.paste(icon, (x, y), icon)
        except Exception as e:
            print(f"Warning: Could not load icon {icon_path}: {e}")

def draw_title(draw, title, y, max_width):
    """Draw the action title with Cinzel font"""
    font = get_font(TITLE_FONT_SIZE, bold=True, display=True)

    # Check if title fits, reduce font size if needed
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]

    current_size = TITLE_FONT_SIZE
    while text_width > max_width and current_size > 20:
        current_size -= 2
        font = get_font(current_size, bold=True, display=True)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]

    # Center title
    x = (CARD_WIDTH - text_width) // 2
    draw.text((x, y), title, fill=COLOR_TITLE, font=font)

    return bbox[3] - bbox[1] + 8  # Return height used

def draw_separator(draw, y):
    """Draw a horizontal separator line"""
    x1 = SAFE_ZONE + BORDER_WIDTH + 5
    x2 = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - 5
    draw.line([(x1, y), (x2, y)], fill=COLOR_SEPARATOR, width=1)
    return 5  # Return height used

def draw_traits(draw, traits, y):
    """Draw trait boxes"""
    if not traits:
        return 0

    font = get_font(TRAIT_FONT_SIZE, bold=True, display=True)

    # Calculate total width to center traits
    total_width = 0
    trait_boxes = []
    spacing = 6

    for trait in traits:
        bbox = draw.textbbox((0, 0), trait.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        box_width = text_width + (TRAIT_PADDING * 2)
        trait_boxes.append((trait, box_width, text_width, text_height))
        total_width += box_width + spacing

    total_width -= spacing  # Remove last spacing

    # Start X position to center traits
    x = (CARD_WIDTH - total_width) // 2

    for trait, box_width, text_width, text_height in trait_boxes:
        # Draw trait box
        draw.rounded_rectangle(
            [(x, y), (x + box_width, y + TRAIT_HEIGHT)],
            radius=3,
            fill=COLOR_TRAIT_BG,
            outline=COLOR_TRAIT_TEXT,
            width=1
        )

        # Draw trait text centered in box
        text_x = x + (box_width - text_width) // 2
        text_y = y + (TRAIT_HEIGHT - text_height) // 2 - 2
        draw.text((text_x, text_y), trait.upper(), fill=COLOR_TRAIT_TEXT, font=font)

        x += box_width + spacing

    return TRAIT_HEIGHT + 5

def draw_labeled_text(draw, label, text, y, max_width):
    """Draw a labeled section (Trigger, Requirements, etc.)"""
    if not text:
        return 0

    text = clean_text(text)
    if not text:
        return 0

    label_font = get_font(LABEL_FONT_SIZE + 2, bold=True, display=True)
    text_font = get_font(BODY_FONT_SIZE)

    x = SAFE_ZONE + BORDER_WIDTH + 4

    # Draw label
    draw.text((x, y), f"{label}:", fill=COLOR_LABEL, font=label_font)
    label_bbox = draw.textbbox((0, 0), f"{label}:", font=label_font)
    label_width = label_bbox[2] - label_bbox[0]

    # Calculate chars per line
    test_text = "abcdefghijklmnopqrst"
    bbox = draw.textbbox((0, 0), test_text, font=text_font)
    avg_char_width = (bbox[2] - bbox[0]) / len(test_text)

    # First line has less space (after label)
    first_line_width = max_width - label_width - 10
    chars_first_line = int(first_line_width / avg_char_width)
    chars_rest = int((max_width - 4) / avg_char_width)

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
    total_height = 0
    for i, line in enumerate(lines):
        if i == 0:
            draw.text((x + label_width + 5, y), line, fill=COLOR_TEXT, font=text_font)
        else:
            draw.text((x, y + (i * LINE_HEIGHT)), line, fill=COLOR_TEXT, font=text_font)
        total_height = (i + 1) * LINE_HEIGHT

    return max(LINE_HEIGHT, total_height) + 6  # More spacing after labeled sections

def draw_styled_line(draw, text, x, y, max_width, font_size, color=COLOR_TEXT):
    """Draw a single line with bold/italic styling"""
    segments = parse_styled_text(text)
    current_x = x

    for segment_text, is_bold, is_italic in segments:
        if is_bold:
            font = get_font(font_size, bold=True, display=True)
            segment_color = COLOR_LABEL  # Use label color for bold text
        elif is_italic:
            font = get_font(font_size)  # Oldenburg doesn't have italic, use regular
            segment_color = COLOR_TEXT
        else:
            font = get_font(font_size)
            segment_color = color

        draw.text((current_x, y), segment_text, fill=segment_color, font=font)
        bbox = draw.textbbox((0, 0), segment_text, font=font)
        current_x += bbox[2] - bbox[0]

def draw_wrapped_text(draw, text, y, max_width, font_size=None):
    """Draw wrapped body text with bold/italic support"""
    if not text:
        return 0

    text = clean_text(text)
    if not text:
        return 0

    if font_size is None:
        font_size = BODY_FONT_SIZE

    font = get_font(font_size)
    x = SAFE_ZONE + BORDER_WIDTH + 4

    # Calculate characters per line based on actual font width
    test_text = "abcdefghijklmnopqrst"
    bbox = draw.textbbox((0, 0), test_text, font=font)
    avg_char_width = (bbox[2] - bbox[0]) / len(test_text)
    chars_per_line = int((max_width - 8) / avg_char_width)  # Leave small margin

    # Remove markdown for wrapping calculation
    plain_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    plain_text = re.sub(r'\*([^*]+)\*', r'\1', plain_text)

    # Wrap the plain text
    wrapped = textwrap.wrap(plain_text, width=chars_per_line)

    total_height = 0
    line_spacing = LINE_HEIGHT
    for i, line in enumerate(wrapped):
        draw.text((x, y + (i * line_spacing)), line, fill=COLOR_TEXT, font=font)
        total_height = (i + 1) * line_spacing

    return total_height + 2

def draw_results(draw, results, y, max_width):
    """Draw success/failure results section"""
    if not results:
        return 0

    labels = [
        ('criticalSuccess', 'Éxito crítico'),
        ('success', 'Éxito'),
        ('failure', 'Fallo'),
        ('criticalFailure', 'Fallo crítico')
    ]

    total_height = 0

    for key, label in labels:
        text = results.get(key)
        if text:
            height = draw_result_item(draw, label, text, y + total_height, max_width)
            total_height += height

    return total_height

def draw_result_item(draw, label, text, y, max_width):
    """Draw a single result item"""
    text = clean_text(text, remove_traits=False)
    if not text:
        return 0

    # Same size as other labels (Desencadenante, Requisitos)
    label_font = get_font(LABEL_FONT_SIZE + 2, bold=True, display=True)
    text_font = get_font(BODY_FONT_SIZE - 1)

    x = SAFE_ZONE + BORDER_WIDTH + 4

    # Draw label
    draw.text((x, y), f"{label}:", fill=COLOR_LABEL, font=label_font)
    label_bbox = draw.textbbox((0, 0), f"{label}:", font=label_font)
    label_width = label_bbox[2] - label_bbox[0]

    # Calculate chars per line
    test_text = "abcdefghijklmnopqrst"
    bbox = draw.textbbox((0, 0), test_text, font=text_font)
    avg_char_width = (bbox[2] - bbox[0]) / len(test_text)

    first_line_width = max_width - label_width - 8
    chars_first = int(first_line_width / avg_char_width)
    chars_rest = int((max_width - 4) / avg_char_width)

    # Wrap text manually
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    is_first = True

    for word in words:
        max_chars = chars_first if is_first else chars_rest
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
    line_spacing = LINE_HEIGHT - 2
    total_height = 0
    for i, line in enumerate(lines):
        if i == 0:
            draw.text((x + label_width + 4, y), line, fill=COLOR_TEXT, font=text_font)
        else:
            draw.text((x, y + (i * line_spacing)), line, fill=COLOR_TEXT, font=text_font)
        total_height = (i + 1) * line_spacing

    return max(line_spacing, total_height) + 6  # More spacing between result items

def draw_examples(draw, examples, y, max_width):
    """Draw examples table with full rank names, wrapping text to two lines if needed"""
    if not examples:
        return 0

    # Fonts - same size as body text
    label_font = get_font(LABEL_FONT_SIZE + 2, bold=True, display=True)
    rank_font = get_font(BODY_FONT_SIZE - 2, bold=True, display=True)
    text_font = get_font(BODY_FONT_SIZE - 2)

    x = SAFE_ZONE + BORDER_WIDTH + 4

    # Draw "Ejemplos:" header
    draw.text((x, y), "Ejemplos:", fill=COLOR_LABEL, font=label_font)
    current_y = y + LINE_HEIGHT

    # Draw each example with full rank name
    line_spacing = LINE_HEIGHT - 2  # More spacing between examples
    second_line_spacing = LINE_HEIGHT - 6  # Tighter for continuation lines

    for rank, example in examples.items():
        # Draw rank name in bold
        draw.text((x, current_y), f"{rank}:", fill=COLOR_LABEL, font=rank_font)
        rank_bbox = draw.textbbox((0, 0), f"{rank}:", font=rank_font)
        rank_width = rank_bbox[2] - rank_bbox[0]

        # Draw example text after rank
        example_x = x + rank_width + 6
        available_width = max_width - rank_width - 10

        # Check if text fits in one line
        example_text = example
        bbox = draw.textbbox((0, 0), example_text, font=text_font)
        text_width = bbox[2] - bbox[0]

        if text_width <= available_width:
            # Fits in one line
            draw.text((example_x, current_y), example_text, fill=COLOR_TEXT, font=text_font)
            current_y += line_spacing
        else:
            # Need to wrap to two lines
            words = example_text.split()
            first_line = ""
            second_line = ""

            # Build first line
            for i, word in enumerate(words):
                test_line = first_line + (" " if first_line else "") + word
                bbox = draw.textbbox((0, 0), test_line, font=text_font)
                if bbox[2] - bbox[0] <= available_width:
                    first_line = test_line
                else:
                    # Rest goes to second line
                    second_line = " ".join(words[i:])
                    break

            # Draw first line next to rank
            draw.text((example_x, current_y), first_line, fill=COLOR_TEXT, font=text_font)
            current_y += second_line_spacing

            # Draw second line indented (aligned with first line text)
            if second_line:
                # Check if second line needs truncation
                bbox = draw.textbbox((0, 0), second_line, font=text_font)
                full_line_width = max_width - 10
                if bbox[2] - bbox[0] > full_line_width:
                    while bbox[2] - bbox[0] > full_line_width - 15 and len(second_line) > 5:
                        second_line = second_line[:-4] + "..."
                        bbox = draw.textbbox((0, 0), second_line, font=text_font)
                draw.text((x, current_y), second_line, fill=COLOR_TEXT, font=text_font)
                current_y += line_spacing

    return current_y - y + 2


def generate_action_card(action_data, output_path):
    """Generate a single action card"""
    # Create base card with border
    card = create_rounded_rectangle(
        (CARD_WIDTH, CARD_HEIGHT),
        CORNER_RADIUS,
        COLOR_BACKGROUND,
        COLOR_BORDER,
        BORDER_WIDTH
    )

    draw = ImageDraw.Draw(card)

    # Calculate content area - use more of the available space
    content_width = CARD_WIDTH - (2 * SAFE_ZONE) - (2 * BORDER_WIDTH) - 8

    # Current Y position
    current_y = TITLE_Y

    # Draw action icon at top right, aligned with title
    icon_x = CARD_WIDTH - SAFE_ZONE - BORDER_WIDTH - ICON_SIZE - 8
    icon_y = current_y - 5
    draw_action_icon(card, action_data.get('actionType', '1'), icon_x, icon_y)

    # Calculate max title width (leave space for icon)
    title_max_width = CARD_WIDTH - (2 * SAFE_ZONE) - ICON_SIZE - 30

    # Draw title (centered but respecting icon space)
    title_height = draw_title(draw, action_data['name'], current_y, title_max_width)
    current_y += max(title_height, ICON_SIZE) + 5

    # Draw separator
    current_y += draw_separator(draw, current_y)

    # Draw traits
    traits = action_data.get('traits', [])
    if traits:
        current_y += draw_traits(draw, traits, current_y)
        current_y += draw_separator(draw, current_y)

    # Draw trigger (for reactions)
    trigger = action_data.get('trigger')
    if trigger:
        current_y += draw_labeled_text(draw, "Desencadenante", trigger, current_y, content_width)

    # Draw requirements
    requirements = action_data.get('requirements')
    if requirements:
        current_y += draw_labeled_text(draw, "Requisitos", requirements, current_y, content_width)

    # Add separator if we had trigger or requirements
    if trigger or requirements:
        current_y += 3
        current_y += draw_separator(draw, current_y)

    # Draw main description
    description = action_data.get('description', '')
    if description:
        current_y += 4
        # Adjust font size based on remaining space and text length
        remaining_space = CARD_HEIGHT - current_y - SAFE_ZONE - 15
        clean_desc = clean_text(description)
        desc_length = len(clean_desc)

        font_size = BODY_FONT_SIZE
        # Reduce font for long descriptions or little remaining space
        if desc_length > 400 or remaining_space < 400:
            font_size = BODY_FONT_SIZE - 1
        if desc_length > 600 or remaining_space < 300:
            font_size = BODY_FONT_SIZE - 2
        if desc_length > 800 or remaining_space < 200:
            font_size = BODY_FONT_SIZE - 3

        current_y += draw_wrapped_text(draw, description, current_y, content_width, font_size)

    # Draw results section only if there's space
    results = action_data.get('results', {})
    has_results = any(results.get(k) for k in ['criticalSuccess', 'success', 'failure', 'criticalFailure'])
    remaining_space = CARD_HEIGHT - current_y - SAFE_ZONE

    if has_results and remaining_space > 50:
        current_y += 2
        current_y += draw_separator(draw, current_y)
        current_y += 3
        current_y += draw_results(draw, results, current_y, content_width)

    # Draw examples section if present and there's space
    examples = action_data.get('examples')
    remaining_space = CARD_HEIGHT - current_y - SAFE_ZONE
    if examples and remaining_space > 80:
        current_y += 2
        current_y += draw_separator(draw, current_y)
        current_y += 3
        draw_examples(draw, examples, current_y, content_width)

    # Convert to RGB for saving
    rgb_card = Image.new('RGB', card.size, (255, 255, 255))
    rgb_card.paste(card, mask=card.split()[3] if card.mode == 'RGBA' else None)

    # Save card
    rgb_card.save(output_path, 'PNG', dpi=(300, 300))

def main():
    """Main function to generate all cards"""
    print("PF2e Action Cards Generator")
    print("=" * 40)
    print()

    # Check if data file exists
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found: {DATA_FILE}")
        print("Please run parse_actions.py first!")
        return

    # Load action data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    actions = data.get('actions', [])
    print(f"Found {len(actions)} actions to generate")
    print(f"Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ 300 DPI (63x88mm Magic)")
    print()

    # Category folder mapping
    CATEGORY_FOLDERS = {
        'basica': 'acciones-basicas',
        'especialidad': 'acciones-especialidad',
    }

    # Group actions by category
    actions_by_category = {}
    for action in actions:
        category = action.get('category', 'otras')
        if category not in actions_by_category:
            actions_by_category[category] = []
        actions_by_category[category].append(action)

    # Generate cards organized by category
    total_generated = 0
    for category, category_actions in actions_by_category.items():
        folder_name = CATEGORY_FOLDERS.get(category, category)
        category_dir = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(category_dir, exist_ok=True)

        print(f"Generating {folder_name}...")
        for action in category_actions:
            action_id = action['id']
            output_file = os.path.join(category_dir, f"{action_id}.png")

            try:
                generate_action_card(action, output_file)
                print(f"  ✓ {action['name']}")
                total_generated += 1
            except Exception as e:
                print(f"  ✗ Error generating {action['name']}: {e}")
        print()

    print(f"✓ Generated {total_generated} cards in: {OUTPUT_DIR}")
    print(f"✓ Card size: {CARD_WIDTH}x{CARD_HEIGHT}px @ 300 DPI (63x88mm Magic)")

if __name__ == "__main__":
    main()
