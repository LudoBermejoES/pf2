#!/usr/bin/env python3
"""
Remove images from PDF while preserving text and layout.
Requires: pip install pymupdf
"""

import fitz  # PyMuPDF
import sys
from pathlib import Path


def remove_images_from_pdf(input_path: str, output_path: str = None) -> str:
    """
    Remove all images from a PDF file while keeping text and layout.
    """
    input_path = Path(input_path)

    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_no_images.pdf"
    else:
        output_path = Path(output_path)

    doc = fitz.open(input_path)
    images_removed = 0
    total_pages = len(doc)

    for page_num in range(total_pages):
        page = doc[page_num]

        # Get all images on this page
        images = page.get_images(full=True)

        for img in images:
            xref = img[0]  # xref number of the image
            try:
                # Get the rectangle(s) where this image appears
                rects = page.get_image_rects(xref)
                for rect in rects:
                    # Add white redaction over the image area
                    page.add_redact_annot(rect, fill=(1, 1, 1))
                    images_removed += 1
            except Exception as e:
                # Skip problematic images
                pass

        # Apply all redactions on this page
        page.apply_redactions()
        print(f"Page {page_num + 1}/{total_pages} processed")

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

    print(f"\nTotal pages: {total_pages}")
    print(f"Images removed: {images_removed}")
    print(f"Output saved to: {output_path}")

    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_pdf_images.py <input.pdf> [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    remove_images_from_pdf(input_file, output_file)
