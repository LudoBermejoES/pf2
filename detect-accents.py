#!/usr/bin/env python3
"""
Detect Spanish accent problems using enchant library.
Reports exact location (file, line, column) of potential accent issues.
No corrections are made, only detection.
"""

import os
import re
import json
import enchant
from pathlib import Path

# Get Spanish spell checker
spell_checker = enchant.Dict("es_ES")

# Palabras que no son errores (excepciones del diccionario)
WHITELIST_WORDS = {
    'Bonificador', 'Bonificadores', 'Calistria', 'Inframundo',
    'Multiclase', 'Penalizador', 'Penalizadores', 'Reenfocar',
    'bonificador', 'bonificadores', 'constructo', 'multiclase',
    'ocultistas', 'penalizador', 'penalizadores', 'planario',
    'basicas', 'etnicos', 'inspiracion'
}

# Load words marked as "not_problem" from existing results
def load_not_problems():
    """Load words already marked as not_problem from RESULTS_ACCENTS.json"""
    not_problems = set()
    results_file = 'RESULTS_ACCENTS.json'

    if os.path.exists(results_file):
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for issue in data.get('issues', []):
                    if issue.get('not_problem'):
                        not_problems.add(issue['word'])
        except Exception as e:
            print(f"Warning: Could not load existing results: {e}")

    return not_problems

# Load existing not_problems set and add whitelist
not_problems_set = load_not_problems()
not_problems_set.update(WHITELIST_WORDS)

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
    # Empty lines are skipped
    if not stripped:
        return True, in_frontmatter
    # Toggle frontmatter state on --- delimiter
    if stripped.startswith('---'):
        in_frontmatter = not in_frontmatter
        return True, in_frontmatter
    # Skip any line while in frontmatter
    if in_frontmatter:
        return True, in_frontmatter
    # Skip code blocks
    if stripped.startswith('```') or stripped.startswith('`'):
        return True, in_frontmatter
    # Skip HTML tags and comments
    if '<' in line and '>' in line:
        return True, in_frontmatter
    # Skip table separators and markdown headers
    if stripped.startswith('|') or stripped.startswith('#') or stripped.startswith('*'):
        return True, in_frontmatter
    return False, in_frontmatter

def detect_accent_issues(filepath):
    """Detect accent issues in a file and return detailed locations"""
    issues = []
    in_frontmatter = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            should_skip, in_frontmatter = should_skip_line(line, in_frontmatter)
            if should_skip:
                continue

            # Get link positions
            links = extract_markdown_links(line)

            # Find all words in the line
            words_pattern = r'\b[\w]+\b'

            for match in re.finditer(words_pattern, line):
                word = match.group()
                start_pos = match.start()
                end_pos = match.end()

                # Skip if word is in a link
                if is_position_in_link(start_pos, links):
                    continue

                # Skip if word is already marked as not_problem or in whitelist
                if word in not_problems_set:
                    continue

                # Check if word is misspelled
                if not spell_checker.check(word):
                    # Get suggestions
                    try:
                        suggestions = spell_checker.suggest(word)
                        if suggestions:
                            issues.append({
                                'file': filepath,
                                'line': line_num,
                                'column': start_pos + 1,
                                'word': word,
                                'suggestions': suggestions[:5],  # Top 5 suggestions
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

print("Detecting accent problems with enchant...\n")

file_count = 0
for filepath in walk_dir(root_dir):
    issues = detect_accent_issues(filepath)
    if issues:
        file_count += 1
        all_issues.extend(issues)
        print(f"Found {len(issues)} issues in {filepath}")

# Write results to JSON
output_file = 'RESULTS_ACCENTS.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'total_issues': len(all_issues),
        'files_with_issues': file_count,
        'issues': all_issues
    }, f, indent=2, ensure_ascii=False)

print(f"\n✓ Detection complete!")
print(f"✓ Total issues found: {len(all_issues)}")
print(f"✓ Files with issues: {file_count}")
print(f"✓ Results saved to: {output_file}")
