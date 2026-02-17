#!/usr/bin/env python3
"""
Generador de cartas de dotes de Pathfinder 2e
Crea imágenes PNG de cartas desde datos JSON
"""

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor

# Dimensiones de la carta (300 DPI print quality)
CARD_WIDTH = 744  # 63mm
CARD_HEIGHT = 1039  # 88mm
SAFE_ZONE = 24  # 2mm
CORNER_RADIUS = 30  # 2.5mm
BORDER_WIDTH = 8

# Colores PF2e
COLOR_BACKGROUND = (244, 228, 201)  # Pergamino
COLOR_BORDER = (125, 68, 55)  # Rojo PF
COLOR_TRAIT_BG = (93, 48, 48)  # Rojo oscuro
COLOR_TRAIT_TEXT = (218, 165, 32)  # Dorado
COLOR_TEXT = (45, 39, 34)  # Oscuro
COLOR_TITLE = (184, 134, 11)  # Dorado
COLOR_LABEL = (125, 68, 55)  # Rojo para etiquetas


def load_fonts(base_path):
    """Carga las fuentes necesarias"""
    fonts_path = base_path / 'assets' / 'fonts'

    fonts = {
        'title': ImageFont.truetype(str(fonts_path / 'Cinzel-Regular.ttf'), 44),
        'title_small': ImageFont.truetype(str(fonts_path / 'Cinzel-Regular.ttf'), 36),
        'body': ImageFont.truetype(str(fonts_path / 'Oldenburg-Regular.ttf'), 24),
        'body_small': ImageFont.truetype(str(fonts_path / 'Oldenburg-Regular.ttf'), 20),
        'trait': ImageFont.truetype(str(fonts_path / 'Oldenburg-Regular.ttf'), 17),
        'label': ImageFont.truetype(str(fonts_path / 'Oldenburg-Regular.ttf'), 20),
    }

    return fonts


def draw_rounded_rectangle(draw, box, radius, fill, outline=None, width=1):
    """Dibuja un rectángulo con esquinas redondeadas"""
    x1, y1, x2, y2 = box

    # Dibujar rectángulo principal
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=None)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=None)

    # Dibujar esquinas redondeadas
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)

    # Dibujar borde si se especifica
    if outline and width > 0:
        draw.arc([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=outline, width=width)
        draw.arc([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)


def wrap_text(text, font, max_width, draw):
    """Envuelve el texto para que quepa en el ancho máximo"""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def draw_feat_title(draw, feat_data, fonts, y_pos):
    """Dibuja el título de la dote"""
    name = feat_data['name']
    x_center = CARD_WIDTH // 2

    # Elegir fuente según longitud del título
    if len(name) > 20:
        font = fonts['title_small']
    else:
        font = fonts['title']

    # Dibujar título centrado
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = x_center - text_width // 2
    draw.text((x, y_pos), name, font=font, fill=COLOR_TITLE)

    return y_pos + text_height + 20


def draw_trait_boxes(draw, traits, level, fonts, y_pos):
    """Dibuja las cajas de rasgos y nivel"""
    x_start = SAFE_ZONE + 20
    box_height = 28
    box_padding = 8
    box_margin = 6

    # Agregar nivel como rasgo especial
    all_traits = traits + [f"Nivel {level}"]

    x = x_start

    for trait in all_traits:
        # Calcular ancho de la caja
        bbox = draw.textbbox((0, 0), trait, font=fonts['trait'])
        text_width = bbox[2] - bbox[0]
        box_width = text_width + box_padding * 2

        # Dibujar caja de rasgo
        box = [x, y_pos, x + box_width, y_pos + box_height]
        draw_rounded_rectangle(draw, box, 5, COLOR_TRAIT_BG)

        # Dibujar texto del rasgo
        text_y = y_pos + (box_height - (bbox[3] - bbox[1])) // 2
        draw.text((x + box_padding, text_y), trait, font=fonts['trait'], fill=COLOR_TRAIT_TEXT)

        x += box_width + box_margin

        # Salto de línea si es necesario
        if x + 100 > CARD_WIDTH - SAFE_ZONE:
            y_pos += box_height + box_margin
            x = x_start

    return y_pos + box_height + 20


def draw_labeled_section(draw, label, text, fonts, y_pos, max_width):
    """Dibuja una sección con etiqueta (Prerrequisitos, Requisitos, etc.)"""
    if not text:
        return y_pos

    x_start = SAFE_ZONE + 20

    # Dibujar etiqueta
    label_text = f"{label}:"
    bbox = draw.textbbox((0, 0), label_text, font=fonts['label'])
    draw.text((x_start, y_pos), label_text, font=fonts['label'], fill=COLOR_LABEL)

    y_pos += bbox[3] - bbox[1] + 8

    # Dibujar texto envuelto
    lines = wrap_text(text, fonts['body_small'], max_width, draw)
    for line in lines:
        draw.text((x_start, y_pos), line, font=fonts['body_small'], fill=COLOR_TEXT)
        bbox = draw.textbbox((0, 0), line, font=fonts['body_small'])
        y_pos += bbox[3] - bbox[1] + 4

    return y_pos + 12


def draw_description(draw, text, fonts, y_pos, max_width, available_height):
    """Dibuja la descripción principal"""
    if not text:
        return y_pos

    x_start = SAFE_ZONE + 20

    # Calcular tamaño de fuente dinámicamente
    text_length = len(text)
    if text_length > 500 and available_height < 400:
        font = fonts['body_small']
    else:
        font = fonts['body']

    # Envolver y dibujar texto
    lines = wrap_text(text, font, max_width, draw)

    for line in lines:
        if y_pos > CARD_HEIGHT - SAFE_ZONE - 100:
            # Cortar si nos quedamos sin espacio
            draw.text((x_start, y_pos), "...", font=font, fill=COLOR_TEXT)
            break

        draw.text((x_start, y_pos), line, font=font, fill=COLOR_TEXT)
        bbox = draw.textbbox((0, 0), line, font=font)
        y_pos += bbox[3] - bbox[1] + 6

    return y_pos


def create_feat_card(feat_data, fonts, output_path):
    """Genera una carta de dote"""
    try:
        # Crear imagen
        img = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), COLOR_BACKGROUND)
        draw = ImageDraw.Draw(img)

        # Dibujar borde
        draw_rounded_rectangle(
            draw,
            [BORDER_WIDTH, BORDER_WIDTH, CARD_WIDTH - BORDER_WIDTH, CARD_HEIGHT - BORDER_WIDTH],
            CORNER_RADIUS,
            None,
            COLOR_BORDER,
            BORDER_WIDTH
        )

        y_pos = SAFE_ZONE + BORDER_WIDTH + 20
        max_text_width = CARD_WIDTH - (SAFE_ZONE + 20) * 2

        # 1. Título
        y_pos = draw_feat_title(draw, feat_data, fonts, y_pos)

        # 2. Rasgos y nivel
        traits = feat_data.get('traits', [])
        level = feat_data.get('level', 1)
        y_pos = draw_trait_boxes(draw, traits, level, fonts, y_pos)

        # Línea separadora
        draw.line(
            [SAFE_ZONE + 30, y_pos, CARD_WIDTH - SAFE_ZONE - 30, y_pos],
            fill=COLOR_BORDER,
            width=2
        )
        y_pos += 20

        # 3. Campos especiales
        special_fields = [
            ('Prerrequisitos', feat_data.get('prerequisites')),
            ('Frecuencia', feat_data.get('frequency')),
            ('Requisitos', feat_data.get('requirements')),
            ('Desencadenante', feat_data.get('trigger')),
            ('Coste', feat_data.get('cost')),
        ]

        for label, value in special_fields:
            if value:
                y_pos = draw_labeled_section(draw, label, value, fonts, y_pos, max_text_width)

        # 4. Descripción principal
        available_height = CARD_HEIGHT - y_pos - SAFE_ZONE - 60
        description = feat_data.get('description', '')
        if description:
            y_pos = draw_description(draw, description, fonts, y_pos, max_text_width, available_height)
            y_pos += 16

        # 5. Beneficio (si existe)
        benefit = feat_data.get('benefit')
        if benefit:
            y_pos = draw_labeled_section(draw, 'Beneficio', benefit, fonts, y_pos, max_text_width)

        # 6. Especial (si existe)
        special = feat_data.get('special')
        if special and y_pos < CARD_HEIGHT - SAFE_ZONE - 100:
            y_pos = draw_labeled_section(draw, 'Especial', special, fonts, y_pos, max_text_width)

        # Guardar imagen
        img.save(output_path, 'PNG', dpi=(300, 300))
        return True

    except Exception as e:
        print(f"Error generando carta para {feat_data.get('name', 'unknown')}: {e}")
        return False


def generate_all_cards(feats_json_path, output_dir, fonts):
    """Genera todas las cartas desde el JSON"""
    with open(feats_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    feats = data['feats']
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🎴 Generando {len(feats)} cartas...\n")

    success_count = 0
    error_count = 0

    for i, feat in enumerate(feats, 1):
        if i % 50 == 0:
            print(f"  Generando {i}/{len(feats)}...")

        feat_id = feat.get('id', f'feat-{i}')
        output_file = output_path / f"{feat_id}.png"

        if create_feat_card(feat, fonts, output_file):
            success_count += 1
        else:
            error_count += 1

    print(f"\n✅ Generadas {success_count} cartas exitosamente")
    if error_count > 0:
        print(f"⚠️  {error_count} errores durante la generación")

    return success_count, error_count


if __name__ == '__main__':
    print("=" * 60)
    print("Generador de Cartas de Dotes de Pathfinder 2e")
    print("=" * 60)
    print()

    base_path = Path(__file__).parent

    # Cargar fuentes
    print("📚 Cargando fuentes...")
    fonts = load_fonts(base_path)

    # Generar cartas
    feats_json = base_path / 'data' / 'feats.json'
    output_dir = base_path / 'generated_cards'

    if not feats_json.exists():
        print(f"❌ Error: No se encontró {feats_json}")
        print("Ejecuta parse_feats.py primero para generar el JSON")
        exit(1)

    success, errors = generate_all_cards(feats_json, output_dir, fonts)

    print("\n" + "=" * 60)
    print("✨ Generación completada")
    print("=" * 60)
