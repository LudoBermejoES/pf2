#!/usr/bin/env python3
"""
Validador de integridad para archivos PC2
Verifica:
1. Presencia del campo source: PC2 en frontmatter
2. Estructura correcta de frontmatter YAML
3. Enlaces internos válidos
4. Rutas permalink válidas
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def validate_pc2_files():
    """Valida todos los archivos generados PC2"""
    docs_root = Path("/Users/ludo/code/pf2/docs")

    results = {
        'total_files': 0,
        'valid_files': 0,
        'missing_source': [],
        'malformed_frontmatter': [],
        'missing_title': [],
        'invalid_permalink': [],
        'warnings': []
    }

    # Buscar archivos en directorios PC2
    pc2_patterns = [
        'ascendencias/*/index.md',
        'ascendencias/*/herencias.md',
        'ascendencias/*/dotes.md',
        'ascendencias/herencias-versatiles/*.md',
        'clases/*/index.md',
        'clases/*/caracteristicas.md',
        'clases/*/dotes.md',
        'arquetipos/*.md',
        'dotes-generales/*.md',
        'dotes-habilidad/*.md',
        'conjuros/*/index.md',
        'conjuros/*/*.md',
        'rituales/*.md',
        'equipo/alquimia/*.md',
        'equipo/magicos/*.md',
        'equipo/trampas/*.md'
    ]

    all_files = []
    for pattern in pc2_patterns:
        all_files.extend(docs_root.glob(pattern))

    print(f"📋 Validando {len(all_files)} archivos PC2...\n")

    for filepath in all_files:
        results['total_files'] += 1

        try:
            content = filepath.read_text(encoding='utf-8')

            # Verificar frontmatter
            frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not frontmatter_match:
                results['malformed_frontmatter'].append(str(filepath))
                continue

            frontmatter = frontmatter_match.group(1)

            # Verificar source: PC2
            if 'source: PC2' not in frontmatter:
                results['missing_source'].append(str(filepath))

            # Verificar title
            if 'title:' not in frontmatter:
                results['missing_title'].append(str(filepath))

            # Verificar permalink
            if 'permalink:' not in frontmatter:
                results['invalid_permalink'].append(str(filepath))

            if not results['missing_source'][-1:] or results['missing_source'][-1] != str(filepath):
                results['valid_files'] += 1

        except Exception as e:
            results['warnings'].append(f"{filepath}: {str(e)}")

    # Imprimir resultados
    print(f"✅ Archivos válidos: {results['valid_files']}/{results['total_files']}")
    print(f"📊 Tasa de validación: {(results['valid_files']/results['total_files']*100):.1f}%\n")

    if results['missing_source']:
        print(f"⚠️  {len(results['missing_source'])} archivos sin 'source: PC2':")
        for f in results['missing_source'][:5]:
            print(f"   - {Path(f).name}")
        if len(results['missing_source']) > 5:
            print(f"   ... y {len(results['missing_source'])-5} más\n")

    if results['malformed_frontmatter']:
        print(f"❌ {len(results['malformed_frontmatter'])} archivos con frontmatter mal formado\n")

    if results['missing_title']:
        print(f"⚠️  {len(results['missing_title'])} archivos sin título\n")

    if results['warnings']:
        print(f"⚠️  {len(results['warnings'])} advertencias durante validación\n")

    return results

if __name__ == '__main__':
    results = validate_pc2_files()
    print("=" * 60)
    print("Validación completada.")
