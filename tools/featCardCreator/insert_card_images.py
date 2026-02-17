#!/usr/bin/env python3
"""
Insertor de imágenes de cartas en archivos markdown de dotes
Agrega referencias a las imágenes generadas en los archivos de dotes
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime


def backup_file(file_path):
    """Crea una copia de seguridad del archivo"""
    backup_path = file_path.with_suffix('.md.backup')
    shutil.copy2(file_path, backup_path)
    return backup_path


def insert_card_image(feat_file, card_image_rel_path, dry_run=False):
    """Inserta la imagen de carta en el archivo markdown de dote"""
    try:
        with open(feat_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar donde insertar (después del título, antes de la descripción)
        # Formato esperado:
        # ## Nombre de la Dote
        # <div class="feat-traits-header">...</div>
        # [AQUÍ insertamos la imagen]
        # Descripción...

        # Patrón para encontrar la posición de inserción
        pattern = r'(##\s+.+?\n.*?<div class="feat-traits-header".*?</div>\n)(.*?)(\n\*\*|$)'

        # Verificar si ya tiene una imagen de carta
        if '<div class="feat-card">' in content or 'class="feat-card"' in content:
            return 'already_exists'

        # HTML para la imagen de carta
        card_html = f'''
<div class="feat-card">
  <img src="{card_image_rel_path}" alt="Carta de dote">
</div>

'''

        # Insertar después del div de rasgos
        def replacer(match):
            return match.group(1) + card_html + match.group(2) + match.group(3)

        new_content = re.sub(pattern, replacer, content, count=1, flags=re.DOTALL)

        if new_content == content:
            # Patrón alternativo: insertar después del div de rasgos directamente
            pattern2 = r'(<div class="feat-traits-header".*?</div>\n)(\n)?'
            new_content = re.sub(pattern2, r'\1' + card_html, content, count=1, flags=re.DOTALL)

        if new_content == content:
            return 'no_match'

        if not dry_run:
            with open(feat_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

        return 'success'

    except Exception as e:
        print(f"Error procesando {feat_file}: {e}")
        return 'error'


def process_all_feats(feats_json_path, cards_dir, feats_base_dir, dry_run=False, backup=False):
    """Procesa todos los archivos de dotes para insertar imágenes"""
    with open(feats_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    feats = data['feats']
    cards_path = Path(cards_dir)
    base_path = Path(feats_base_dir)

    print(f"🔍 Procesando {len(feats)} dotes...\n")

    if dry_run:
        print("⚠️  MODO DRY-RUN: No se modificarán archivos\n")

    stats = {
        'success': 0,
        'already_exists': 0,
        'no_match': 0,
        'error': 0,
        'not_found': 0
    }

    for i, feat in enumerate(feats, 1):
        if i % 100 == 0:
            print(f"  Procesando {i}/{len(feats)}...")

        feat_id = feat.get('id', '')
        source_file = feat.get('source_file', '')

        if not source_file:
            stats['not_found'] += 1
            continue

        # Verificar que existe la imagen de carta
        card_image = cards_path / f"{feat_id}.png"
        if not card_image.exists():
            stats['not_found'] += 1
            continue

        # Calcular ruta relativa para la imagen
        # La imagen se copiará a /assets/cards/feats/
        card_image_rel = f"/assets/cards/feats/{feat_id}.png"

        # Archivo de dote
        feat_file = Path(source_file)

        if not feat_file.exists():
            stats['not_found'] += 1
            continue

        # Backup si se solicita
        if backup and not dry_run:
            backup_file(feat_file)

        # Insertar imagen
        result = insert_card_image(feat_file, card_image_rel, dry_run)
        stats[result] = stats.get(result, 0) + 1

    print(f"\n📊 Resultados:")
    print(f"  ✅ Insertadas: {stats['success']}")
    print(f"  ℹ️  Ya existían: {stats['already_exists']}")
    print(f"  ⚠️  Sin coincidencia de patrón: {stats['no_match']}")
    print(f"  ❌ Errores: {stats['error']}")
    print(f"  📁 No encontradas: {stats['not_found']}")

    return stats


def copy_cards_to_assets(cards_dir, assets_dir):
    """Copia las cartas generadas al directorio de assets"""
    cards_path = Path(cards_dir)
    assets_path = Path(assets_dir) / 'cards' / 'feats'

    assets_path.mkdir(parents=True, exist_ok=True)

    print(f"\n📦 Copiando cartas a {assets_path}...")

    card_files = list(cards_path.glob('*.png'))

    for i, card_file in enumerate(card_files, 1):
        if i % 100 == 0:
            print(f"  Copiando {i}/{len(card_files)}...")

        dest_file = assets_path / card_file.name
        shutil.copy2(card_file, dest_file)

    print(f"✅ Copiadas {len(card_files)} imágenes")


if __name__ == '__main__':
    import argparse

    print("=" * 60)
    print("Insertor de Imágenes de Cartas de Dotes")
    print("=" * 60)
    print()

    parser = argparse.ArgumentParser(
        description='Inserta imágenes de cartas en archivos markdown de dotes'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Modo de prueba sin modificar archivos'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Crear copias de seguridad antes de modificar'
    )
    parser.add_argument(
        '--skip-copy',
        action='store_true',
        help='No copiar imágenes a assets'
    )

    args = parser.parse_args()

    base_path = Path(__file__).parent
    feats_json = base_path / 'data' / 'feats.json'
    cards_dir = base_path / 'generated_cards'
    feats_base = base_path.parent.parent / 'docs' / '_dotes'
    assets_dir = base_path.parent.parent / 'docs' / 'assets'

    if not feats_json.exists():
        print(f"❌ Error: No se encontró {feats_json}")
        exit(1)

    if not cards_dir.exists() or not list(cards_dir.glob('*.png')):
        print(f"❌ Error: No se encontraron cartas en {cards_dir}")
        print("Ejecuta generate_feat_cards.py primero")
        exit(1)

    # Copiar cartas a assets (si no se omite)
    if not args.skip_copy:
        copy_cards_to_assets(cards_dir, assets_dir)

    # Insertar referencias en markdown
    stats = process_all_feats(
        feats_json,
        cards_dir,
        feats_base,
        dry_run=args.dry_run,
        backup=args.backup
    )

    print("\n" + "=" * 60)
    print("✨ Inserción completada")
    print("=" * 60)
