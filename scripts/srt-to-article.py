#!/usr/bin/env python3
"""
srt-to-article.py — Convierte subtítulos SRT a artículos Markdown para _reglas/detalle/

USO:
    python3 scripts/srt-to-article.py <archivo.srt> \
        --subcarpeta combate \
        --slug economia-de-acciones \
        --title "La Economía de Acciones" \
        [--dry-run]

FLUJO:
    1. Lee el archivo .srt y extrae el texto limpio (sin marcas de tiempo ni números).
    2. Deduplica las líneas solapadas típicas del formato SRT.
    3. Guarda el texto limpio en subtitulos/limpios/<slug>.txt para revisión.
    4. Escribe el artículo Markdown en docs/_reglas/detalle/<subcarpeta>/<slug>.md
       con el frontmatter correcto (layout, title, permalink, chapter, category).
    5. Añade la entrada al sidebar en docs/_includes/sidebar.html, en la
       subsección "Detalle: <subcarpeta>" (en mayúsculas con tilde si procede).
    6. Regenera docs/assets/js/search-index.json.

DEPENDENCIAS:
    - python3 estándar (re, pathlib, argparse, subprocess, textwrap)
    - El script generate-search-index.py debe existir en scripts/

NOTA SOBRE EL CONTENIDO:
    El script extrae y limpia el texto, pero NO traduce automáticamente.
    El artículo generado contiene el texto en inglés estructurado.
    Para publicar en español, edita manualmente el .md generado o usa
    la opción --texto-limpio para obtener solo el .txt y redactar tú mismo.
"""

import re
import sys
import argparse
import subprocess
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# Rutas base
# ─────────────────────────────────────────────────────────────
REPO = Path(__file__).parent.parent
DOCS = REPO / "docs"
LIMPIOS_DIR = REPO / "subtitulos" / "limpios"
REGLAS_DETALLE = DOCS / "_reglas" / "detalle"
SIDEBAR = DOCS / "_includes" / "sidebar.html"
SEARCH_SCRIPT = REPO / "scripts" / "generate-search-index.py"

# Mapa de subcarpeta → etiqueta del sidebar (con acentos)
SUBCARPETA_LABEL = {
    "combate":     "Detalle: Combate",
    "magia":       "Detalle: Magia",
    "artesania":   "Detalle: Artesanía",
    "personajes":  "Detalle: Personajes",
    "peligros":    "Detalle: Peligros",
    "equipo":      "Detalle: Equipo",
    "exploracion": "Detalle: Exploración",
    "social":      "Detalle: Social",
}


# ─────────────────────────────────────────────────────────────
# 1. Extraer texto limpio del SRT
# ─────────────────────────────────────────────────────────────
def extract_text(srt_path: Path) -> list[str]:
    """Lee un SRT y devuelve lista de líneas de texto únicas y no vacías."""
    content = srt_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\n+", content.strip())
    seen = set()
    lines_out = []
    for block in blocks:
        text_lines = []
        for line in block.strip().split("\n"):
            s = line.strip()
            if re.match(r"^\d+$", s):
                continue
            if re.match(r"^\d{2}:\d{2}:\d{2}", s):
                continue
            if s and s != " ":
                text_lines.append(s)
        text = " ".join(text_lines)
        if text and text not in seen:
            seen.add(text)
            lines_out.append(text)
    return lines_out


# ─────────────────────────────────────────────────────────────
# 2. Guardar texto limpio
# ─────────────────────────────────────────────────────────────
def save_clean(lines: list[str], slug: str) -> Path:
    LIMPIOS_DIR.mkdir(parents=True, exist_ok=True)
    out = LIMPIOS_DIR / f"{slug}.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ─────────────────────────────────────────────────────────────
# 3. Generar artículo Markdown
# ─────────────────────────────────────────────────────────────
def build_article(title: str, slug: str, subcarpeta: str, lines: list[str]) -> str:
    permalink = f"/reglas/detalle/{subcarpeta}/{slug}/"
    # Agrupa las líneas en párrafos aproximados (cada ~6 líneas)
    body_lines = []
    chunk = []
    for line in lines:
        # Saltar líneas de despedida/agradecimiento del canal
        if any(kw in line.lower() for kw in [
            "subscribe", "patreon", "like button", "thanks for watching",
            "happy gaming", "take care", "leave a comment", "twitter",
            "facebook", "maps of mastery"
        ]):
            continue
        chunk.append(line)
        # Heurística: nueva frase completa (termina en ./?/!) → posible párrafo
        if line.rstrip().endswith((".", "?", "!")):
            body_lines.append(" ".join(chunk))
            chunk = []
    if chunk:
        body_lines.append(" ".join(chunk))

    body = "\n\n".join(body_lines)

    return f"""---
layout: page
title: "{title}"
permalink: {permalink}
chapter: Cómo Jugar
category: reglas
---

{body}
"""


# ─────────────────────────────────────────────────────────────
# 4. Escribir el artículo
# ─────────────────────────────────────────────────────────────
def write_article(subcarpeta: str, slug: str, content: str, dry_run: bool) -> Path:
    dest_dir = REGLAS_DETALLE / subcarpeta
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slug}.md"
    if dry_run:
        print(f"[DRY-RUN] Escribiría: {dest}")
        print("─" * 60)
        print(content[:500] + "…")
        print("─" * 60)
    else:
        dest.write_text(content, encoding="utf-8")
        print(f"✓ Artículo creado: {dest}")
    return dest


# ─────────────────────────────────────────────────────────────
# 5. Actualizar sidebar
# ─────────────────────────────────────────────────────────────
def update_sidebar(subcarpeta: str, slug: str, title: str, dry_run: bool):
    label = SUBCARPETA_LABEL.get(subcarpeta, f"Detalle: {subcarpeta.capitalize()}")
    permalink = f"/reglas/detalle/{subcarpeta}/{slug}/"
    new_li = f'          <li><a href="{{{{ \'{permalink}\' | relative_url }}}}">{title}</a></li>'

    html = SIDEBAR.read_text(encoding="utf-8")

    # Comprobar si ya existe
    if permalink in html:
        print(f"  Sidebar: ya existe entrada para {permalink}, se omite.")
        return

    # Buscar la subsección correcta y añadir la entrada al final de su <ul>
    pattern = re.compile(
        r'(<span class="subsection-label">' + re.escape(label) + r'</span>\s*'
        r'<ul class="subsection-links">)(.*?)(</ul>)',
        re.DOTALL
    )
    match = pattern.search(html)
    if not match:
        print(f"  AVISO: No se encontró la subsección '{label}' en el sidebar.")
        print(f"  Añade manualmente: {new_li}")
        return

    new_ul_content = match.group(2) + "\n" + new_li + "\n        "
    new_html = html[:match.start()] + match.group(1) + new_ul_content + match.group(3) + html[match.end():]

    if dry_run:
        print(f"[DRY-RUN] Añadiría al sidebar en '{label}':\n  {new_li}")
    else:
        SIDEBAR.write_text(new_html, encoding="utf-8")
        print(f"✓ Sidebar actualizado: '{label}' ← {title}")


# ─────────────────────────────────────────────────────────────
# 6. Regenerar índice de búsqueda
# ─────────────────────────────────────────────────────────────
def regenerate_index(dry_run: bool):
    if dry_run:
        print("[DRY-RUN] Se regeneraría el índice de búsqueda.")
        return
    result = subprocess.run(
        [sys.executable, str(SEARCH_SCRIPT)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✓ Índice de búsqueda regenerado.")
        # Mostrar resumen de colecciones
        for line in result.stdout.strip().splitlines():
            if "reglas" in line or "Total" in line:
                print(f"  {line}")
    else:
        print(f"  ERROR al regenerar índice: {result.stderr}")


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Convierte un .srt a artículo Markdown en _reglas/detalle/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("srt", help="Ruta al archivo .srt de entrada")
    parser.add_argument("--subcarpeta", required=True,
                        help="Subcarpeta de destino (combate, magia, personajes, ...)")
    parser.add_argument("--slug", required=True,
                        help="Slug del artículo (ej: economia-de-acciones)")
    parser.add_argument("--title", required=True,
                        help="Título del artículo en español")
    parser.add_argument("--texto-limpio", action="store_true",
                        help="Solo extrae el texto limpio al .txt, sin crear el .md")
    parser.add_argument("--dry-run", action="store_true",
                        help="Muestra lo que haría sin escribir nada")
    args = parser.parse_args()

    srt_path = Path(args.srt)
    if not srt_path.exists():
        print(f"ERROR: No se encuentra el archivo: {srt_path}")
        sys.exit(1)

    print(f"\n── Procesando: {srt_path.name}")

    # 1. Extraer texto
    lines = extract_text(srt_path)
    print(f"  Líneas únicas extraídas: {len(lines)}")

    # 2. Guardar texto limpio
    clean_path = save_clean(lines, args.slug)
    print(f"  Texto limpio guardado en: {clean_path}")

    if args.texto_limpio:
        print("  Modo --texto-limpio: fin del proceso.")
        return

    # 3. Generar contenido del artículo
    content = build_article(args.title, args.slug, args.subcarpeta, lines)

    # 4. Escribir artículo
    write_article(args.subcarpeta, args.slug, content, args.dry_run)

    # 5. Actualizar sidebar
    update_sidebar(args.subcarpeta, args.slug, args.title, args.dry_run)

    # 6. Regenerar índice
    regenerate_index(args.dry_run)

    print()


if __name__ == "__main__":
    main()
