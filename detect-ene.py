#!/usr/bin/env python3
"""
Detect Spanish Ñ/ñ problems - words that have N/n where they should have Ñ/ñ.
Reports exact location (file, line, column) of potential Ñ issues.
"""

import os
import re
import json
import enchant
from pathlib import Path

# Get Spanish spell checker
spell_checker = enchant.Dict("es_ES")

# Palabras que no son errores (excepciones)
WHITELIST_WORDS = {
    'Bonificador', 'Bonificadores', 'Calistria', 'Inframundo',
    'Multiclase', 'Penalizador', 'Penalizadores', 'Reenfocar',
    'bonificador', 'bonificadores', 'constructo', 'multiclase',
    'ocultistas', 'penalizador', 'penalizadores', 'planario',
    'pág', 'págs',
    # Deidades y lugares
    'Sarenrae', 'Desna', 'Gorum', 'Iomedae', 'Erastil', 'Nethys',
    'Pharasma', 'Calistria', 'Shelyn', 'Cayden', 'Lamashtu', 'Urgathoa',
    'Golarion', 'Avistan', 'Garund', 'Varisia', 'Absalom', 'Brevoy',
}


def is_n_to_ene_error(word, suggestions):
    """
    Check if the word has an N where it should have Ñ.
    Returns the correct suggestion if found, None otherwise.
    """
    word_lower = word.lower()

    for suggestion in suggestions:
        suggestion_lower = suggestion.lower()

        # Check if same length and differs only in n->ñ
        if len(word_lower) == len(suggestion_lower):
            differences = []
            for i, (c1, c2) in enumerate(zip(word_lower, suggestion_lower)):
                if c1 != c2:
                    differences.append((i, c1, c2))

            # Check if all differences are n->ñ
            if differences and all(d[1] == 'n' and d[2] == 'ñ' for d in differences):
                return suggestion

    return None


def extract_markdown_links(line):
    """Extract markdown link positions to avoid checking them"""
    links = []
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    for match in re.finditer(link_pattern, line):
        links.append((match.start(), match.end()))
    return links


def is_position_in_link(pos, links):
    """Check if a position is inside a markdown link"""
    for start, end in links:
        if start <= pos < end:
            return True
    return False


def should_skip_line(line, in_frontmatter=False):
    """Check if line should be skipped"""
    stripped = line.strip()
    if not stripped:
        return True, in_frontmatter
    if stripped.startswith('---'):
        in_frontmatter = not in_frontmatter
        return True, in_frontmatter
    if in_frontmatter:
        return True, in_frontmatter
    if stripped.startswith('```') or stripped.startswith('`'):
        return True, in_frontmatter
    if '<' in line and '>' in line:
        return True, in_frontmatter
    if stripped.startswith('|') or stripped.startswith('#') or stripped.startswith('*'):
        return True, in_frontmatter
    return False, in_frontmatter


def detect_ene_issues(filepath):
    """Detect Ñ issues in a file and return detailed locations"""
    issues = []
    in_frontmatter = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            should_skip, in_frontmatter = should_skip_line(line, in_frontmatter)
            if should_skip:
                continue

            links = extract_markdown_links(line)
            words_pattern = r'\b[\w]+\b'

            for match in re.finditer(words_pattern, line):
                word = match.group()
                start_pos = match.start()

                # Skip if word is in a link or whitelist
                if is_position_in_link(start_pos, links):
                    continue
                if word in WHITELIST_WORDS:
                    continue

                # Only check words containing 'n' or 'N'
                if 'n' not in word.lower():
                    continue

                # Check if word is misspelled
                if not spell_checker.check(word):
                    try:
                        suggestions = spell_checker.suggest(word)
                        if suggestions:
                            correct_word = is_n_to_ene_error(word, suggestions)
                            if correct_word:
                                issues.append({
                                    'file': filepath,
                                    'line': line_num,
                                    'column': start_pos + 1,
                                    'word': word,
                                    'correction': correct_word,
                                    'context': line.strip()
                                })
                    except:
                        pass

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

    return issues


def walk_dir(root_dir):
    """Walk directory and find all markdown files"""
    for root, dirs, files in os.walk(root_dir):
        for filename in sorted(files):
            if filename.endswith('.md'):
                yield os.path.join(root, filename)


# Process all markdown files
root_dir = './docs'
all_issues = []

print("Detectando errores de Ñ/ñ (palabras con N donde debería haber Ñ)...\n")

file_count = 0
for filepath in walk_dir(root_dir):
    issues = detect_ene_issues(filepath)
    if issues:
        file_count += 1
        all_issues.extend(issues)
        print(f"Encontrados {len(issues)} errores en {filepath}")

# Write results to JSON
output_file = 'RESULTS_ENE.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'total_issues': len(all_issues),
        'files_with_issues': file_count,
        'issues': all_issues
    }, f, indent=2, ensure_ascii=False)

print(f"\n✓ Detección completa!")
print(f"✓ Total errores de Ñ encontrados: {len(all_issues)}")
print(f"✓ Archivos con errores: {file_count}")
print(f"✓ Resultados guardados en: {output_file}")

# Print summary by word
if all_issues:
    print("\n--- Resumen por palabra ---")
    word_counts = {}
    for issue in all_issues:
        key = f"{issue['word']} -> {issue['correction']}"
        word_counts[key] = word_counts.get(key, 0) + 1

    for word, count in sorted(word_counts.items(), key=lambda x: -x[1]):
        print(f"  {word}: {count} ocurrencias")
