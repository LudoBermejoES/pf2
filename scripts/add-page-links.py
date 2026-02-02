#!/usr/bin/env python3
"""
Script para añadir enlaces web a las referencias de páginas del libro.
Mantiene el texto original "pág. X" pero añade un enlace a la sección correspondiente.
"""

import os
import re
import glob

# Mapeo de páginas del libro a URLs de la web
# Basado en Player Core (PC1) y GM Core
PAGE_MAP = {
    # Habilidades y acciones generales (PC1 páginas 228-252)
    "228": "/habilidades/descifrar-escritura/",
    "229": "/habilidades/obtener-ingresos/",
    "231": "/habilidades/recordar-conocimiento/",
    "232": "/habilidades/subsistir/",
    "234": "/habilidades/artesania/",
    "239": "/habilidades/engano/",
    "240": "/habilidades/interpretacion/",
    "242": "/habilidades/medicina/",
    "244": "/habilidades/sigilo/",
    "246": "/habilidades/latrocinio/",
    "251": "/dotes/habilidad/",
    "252": "/dotes/habilidad/",

    # Equipo (PC1 páginas 268-297)
    "268": "/equipo/objetos/",
    "274": "/equipo/armas/",
    "276": "/equipo/armas/",
    "281": "/equipo/armas/",
    "284": "/equipo/armas/",
    "288": "/equipo/objetos/",
    "294": "/habilidades/artesania/",

    # Conjuros (PC1 páginas 303-311)
    "303": "/conjuros/introduccion/",
    "304": "/conjuros/",
    "311": "/conjuros/",

    # Familiares y compañeros (PC1 página 212)
    "212": "/clases/companeros/familiares/",

    # Arquetipos multiclase (PC1 página 215)
    "215": "/clases/arquetipos/",

    # Reglas de juego (PC1 páginas 404-447)
    "404": "/reglas/pruebas/",
    "407": "/reglas/dano/",
    "410": "/reglas/puntos-golpe/",
    "411": "/reglas/puntos-golpe/",
    "416": "/reglas/acciones-basicas/huir/",
    "417": "/reglas/acciones-basicas/retrasar/",
    "418": "/reglas/acciones-especialidad/agarrarse-a-un-saliente/",
    "419": "/reglas/acciones-especialidad/",
    "420": "/reglas/movimiento/",
    "421": "/reglas/movimiento/",
    "422": "/reglas/movimiento/",
    "423": "/reglas/movimiento/",
    "426": "/reglas/efectos/",
    "431": "/conjuros/introduccion/",
    "433": "/reglas/percepcion-deteccion/",
    "434": "/reglas/percepcion-deteccion/",
    "435": "/reglas/modo-encuentro/",
    "437": "/reglas/batallas-especiales/",
    "438": "/reglas/modo-exploracion/",
    "440": "/reglas/modo-tiempo-libre/",
    "442": "/apendices/estados/",
    "443": "/apendices/estados/",
    "444": "/apendices/estados/",
    "445": "/apendices/estados/",
    "446": "/apendices/estados/",
    "447": "/apendices/estados/",

    # GM Core páginas
    "219": "/equipo/magia/",
    "220": "/equipo/magia/",
    "223": "/reglas/runas/",
    "225": "/reglas/runas/",
    "226": "/reglas/runas/",
    "238": "/reglas/runas/",
    "257": "/conjuros/conjuros-foco/",
    "258": "/conjuros/conjuros-foco/",
    "269": "/reglas/runas/",
    "295": "/habilidades/artesania/",
}

# Patrón unificado para encontrar todas las referencias a páginas
# Captura: (pág. 123), (página 123), (pag. 123), pág. 123, página 123, pag. 123
UNIFIED_PATTERN = r'(?<!\[ver\]\()(?:páginas?|paginas?|pág\.|pag\.)\s*(\d+)(?:\s*(?:a|y)\s*(\d+))?'

def process_file(filepath, page_map, dry_run=True):
    """Procesa un archivo markdown añadiendo enlaces a las referencias de páginas."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []
    processed_positions = set()

    def replace_func(match):
        start = match.start()

        # Evitar procesar la misma posición dos veces
        if start in processed_positions:
            return match.group(0)
        processed_positions.add(start)

        full_match = match.group(0)
        page_num = match.group(1)
        page_num_end = match.group(2)  # Para rangos como "páginas 442 a 447"

        # Verificar si ya tiene un enlace después
        end = match.end()
        after_text = content[end:end+10] if end+10 < len(content) else content[end:]
        if ' ([ver]' in after_text or after_text.startswith(' ([ver]'):
            return full_match

        # Buscar la página en el mapa
        if page_num in page_map:
            url = page_map[page_num]
            changes.append(f"  {full_match} -> enlace a {url}")
            return f'{full_match} ([ver]({url}))'

        return full_match

    new_content = re.sub(UNIFIED_PATTERN, replace_func, content, flags=re.IGNORECASE)

    if changes and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return changes

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Añadir enlaces a referencias de páginas')
    parser.add_argument('--dry-run', action='store_true', help='Solo mostrar cambios sin aplicarlos')
    parser.add_argument('--file', help='Procesar solo un archivo específico')
    args = parser.parse_args()

    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')

    if args.file:
        files = [args.file]
    else:
        files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)

    total_changes = 0
    files_changed = 0

    for filepath in files:
        changes = process_file(filepath, PAGE_MAP, dry_run=args.dry_run)
        if changes:
            files_changed += 1
            total_changes += len(changes)
            print(f"\n{filepath}:")
            for change in changes:
                print(change)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Total: {total_changes} cambios en {files_changed} archivos")

    if args.dry_run:
        print("\nEjecuta sin --dry-run para aplicar los cambios")

if __name__ == '__main__':
    main()
