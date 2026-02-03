#!/usr/bin/env python3
"""
Print Sheet PDF Generator for PF2e Action Cards
Creates printable A4 sheets with 4 tarot cards per page (2x2 layout)
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
import os

# Magic card size in mm
CARD_WIDTH_MM = 63
CARD_HEIGHT_MM = 88

# Layouts - Magic cards are smaller so we can fit 3x3 on A4
LAYOUTS = {
    'a4_3x3': {
        'pagesize': A4,
        'cards_per_row': 3,
        'cards_per_col': 3,
        'margin_mm': 10,    # Outer margin
        'gap_mm': 5         # Gap between cards
    },
    'a4_2x2': {
        'pagesize': A4,
        'cards_per_row': 2,
        'cards_per_col': 2,
        'margin_mm': 20,    # Outer margin
        'gap_mm': 10        # Gap between cards
    },
    'letter_3x3': {
        'pagesize': letter,
        'cards_per_row': 3,
        'cards_per_col': 3,
        'margin_mm': 10,
        'gap_mm': 5
    }
}

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(SCRIPT_DIR, 'generated_cards')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'print_output')

def create_print_sheet(cards_dir, output_pdf, layout='a4_2x2', category_filter=None):
    """Create printable PDF sheet with multiple cards per page"""

    layout_config = LAYOUTS[layout]
    c = canvas.Canvas(output_pdf, pagesize=layout_config['pagesize'])

    page_width, page_height = layout_config['pagesize']
    cards_per_row = layout_config['cards_per_row']
    cards_per_col = layout_config['cards_per_col']
    margin = layout_config['margin_mm'] * mm
    gap = layout_config['gap_mm'] * mm

    cards_per_page = cards_per_row * cards_per_col

    card_width = CARD_WIDTH_MM * mm
    card_height = CARD_HEIGHT_MM * mm

    # Calculate total width/height needed
    total_cards_width = (cards_per_row * card_width) + ((cards_per_row - 1) * gap)
    total_cards_height = (cards_per_col * card_height) + ((cards_per_col - 1) * gap)

    # Center the cards on the page
    start_x = (page_width - total_cards_width) / 2
    start_y = page_height - margin - card_height  # Start from top

    # Get card files (recursively from subdirectories)
    card_files = []
    if os.path.exists(cards_dir):
        for root, dirs, files in os.walk(cards_dir):
            for filename in sorted(files):
                if filename.endswith('.png'):
                    card_files.append(os.path.join(root, filename))
        # Sort by full path to group by category
        card_files.sort()

    if not card_files:
        print(f"No cards found in {cards_dir}")
        return

    print(f"Found {len(card_files)} cards")

    # Process cards
    page_num = 1
    for idx, card_path in enumerate(card_files):
        if idx > 0 and idx % cards_per_page == 0:
            c.showPage()
            page_num += 1
            print(f"  Page {page_num} started...")

        # Calculate position on current page
        card_idx_on_page = idx % cards_per_page
        row = card_idx_on_page // cards_per_row
        col = card_idx_on_page % cards_per_row

        x = start_x + col * (card_width + gap)
        y = start_y - row * (card_height + gap)

        try:
            c.drawImage(
                card_path,
                x, y,
                width=card_width,
                height=card_height,
                preserveAspectRatio=True
            )
            card_name = os.path.basename(card_path).replace('.png', '')
            print(f"  Added: {card_name}")
        except Exception as e:
            print(f"  Error adding {card_path}: {e}")

    c.save()

    print()
    print(f"✓ Created PDF: {output_pdf}")
    print(f"✓ Layout: {layout} ({cards_per_row}x{cards_per_col} cards per page)")
    print(f"✓ Total pages: {page_num}")
    print(f"✓ Total cards: {len(card_files)}")

def create_cut_marks_sheet(output_pdf, layout='a4_2x2'):
    """Create a sheet with cut marks for reference"""

    layout_config = LAYOUTS[layout]
    c = canvas.Canvas(output_pdf, pagesize=layout_config['pagesize'])

    page_width, page_height = layout_config['pagesize']
    cards_per_row = layout_config['cards_per_row']
    cards_per_col = layout_config['cards_per_col']
    gap = layout_config['gap_mm'] * mm

    card_width = CARD_WIDTH_MM * mm
    card_height = CARD_HEIGHT_MM * mm

    # Calculate positions (same as cards)
    total_cards_width = (cards_per_row * card_width) + ((cards_per_row - 1) * gap)
    total_cards_height = (cards_per_col * card_height) + ((cards_per_col - 1) * gap)

    start_x = (page_width - total_cards_width) / 2
    start_y = page_height - ((page_height - total_cards_height) / 2) - card_height

    mark_length = 10 * mm

    # Draw cut marks for each card position
    for row in range(cards_per_col):
        for col in range(cards_per_row):
            x = start_x + col * (card_width + gap)
            y = start_y - row * (card_height + gap)

            # Top-left corner
            c.line(x - mark_length, y + card_height, x, y + card_height)
            c.line(x, y + card_height, x, y + card_height + mark_length)

            # Top-right corner
            c.line(x + card_width, y + card_height, x + card_width + mark_length, y + card_height)
            c.line(x + card_width, y + card_height, x + card_width, y + card_height + mark_length)

            # Bottom-left corner
            c.line(x - mark_length, y, x, y)
            c.line(x, y - mark_length, x, y)

            # Bottom-right corner
            c.line(x + card_width, y, x + card_width + mark_length, y)
            c.line(x + card_width, y - mark_length, x + card_width, y)

    c.save()
    print(f"✓ Created cut marks sheet: {output_pdf}")

def main():
    """Main function to generate print PDFs"""

    print("PF2e Action Cards - Print PDF Generator")
    print("=" * 45)
    print()

    # Check if cards exist
    if not os.path.exists(CARDS_DIR):
        print(f"Error: Cards directory not found: {CARDS_DIR}")
        print("Please run generate_cards.py first!")
        return

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get category subdirectories
    categories = []
    for item in sorted(os.listdir(CARDS_DIR)):
        item_path = os.path.join(CARDS_DIR, item)
        if os.path.isdir(item_path):
            categories.append(item)

    # Generate PDF for each category
    for category in categories:
        category_dir = os.path.join(CARDS_DIR, category)
        print(f"Creating PDF for {category}...")
        pdf_output = os.path.join(OUTPUT_DIR, f'{category}.pdf')
        create_print_sheet(category_dir, pdf_output, layout='a4_3x3')
        print()

    # Also create a combined PDF with all cards
    print("Creating combined PDF with all cards...")
    all_output = os.path.join(OUTPUT_DIR, 'todas_las_acciones.pdf')
    create_print_sheet(CARDS_DIR, all_output, layout='a4_3x3')

    # Create cut marks reference sheet
    print()
    print("Creating cut marks reference sheet...")
    marks_output = os.path.join(OUTPUT_DIR, 'cut_marks_reference.pdf')
    create_cut_marks_sheet(marks_output, layout='a4_3x3')

    print()
    print("=" * 45)
    print(f"✓ Print PDFs ready in: {OUTPUT_DIR}")
    print()
    print("Printing instructions:")
    print("  1. Print the PDF on cardstock (250-300gsm recommended)")
    print("  2. Use the cut marks reference for precise cutting")
    print("  3. Cut cards with a hobby knife and ruler")
    print("  4. Optional: Round corners with a corner punch (3.5mm)")

if __name__ == "__main__":
    main()
