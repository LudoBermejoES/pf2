#!/usr/bin/env python3
"""
Script to check for broken links in Jekyll markdown files.
Validates that all internal links point to existing pages.
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

def extract_permalinks(docs_dir):
    """Extract all available permalinks from markdown files."""
    permalinks = set()

    for root, dirs, files in os.walk(docs_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract front matter
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end != -1:
                        frontmatter = content[3:end]

                        # Look for explicit permalink
                        permalink_match = re.search(r'permalink:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
                        if permalink_match:
                            permalink = permalink_match.group(1).strip()
                            permalinks.add(permalink)
                        else:
                            # Try to infer from file structure and collection config
                            rel_path = os.path.relpath(filepath, docs_dir)
                            collection_dir = rel_path.split(os.sep)[0]

                            if collection_dir.startswith('_'):
                                # It's a collection
                                collection_name = collection_dir[1:]  # Remove underscore
                                name = Path(file).stem

                                if name == 'index':
                                    # Index files in subdirs map to parent dir
                                    subdir = rel_path.split(os.sep)[1] if len(rel_path.split(os.sep)) > 2 else ''
                                    if subdir:
                                        permalinks.add(f"/{collection_name}/{subdir}/")
                                else:
                                    # Regular files
                                    parts = rel_path.split(os.sep)
                                    if len(parts) == 3:  # _collection/subdir/file.md
                                        subdir = parts[1]
                                        filename = Path(parts[2]).stem
                                        permalinks.add(f"/{collection_name}/{subdir}/{filename}/")
                                    elif len(parts) == 2:  # _collection/file.md
                                        filename = Path(parts[1]).stem
                                        if filename != 'index':
                                            permalinks.add(f"/{collection_name}/{filename}/")

    return permalinks

def extract_links(content):
    """Extract all markdown links from content."""
    # Match [text](url) pattern
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    links = re.findall(pattern, content)
    return [url for _, url in links]

def check_links(docs_dir, baseurl="/pf2"):
    """Check for broken links in all markdown files."""
    permalinks = extract_permalinks(docs_dir)
    broken_links = defaultdict(list)

    print(f"Found {len(permalinks)} available pages")
    print(f"Base URL: {baseurl}")
    print(f"Available permalinks:\n")
    for p in sorted(permalinks):
        print(f"  {p}")
    print("\n" + "="*60 + "\n")

    for root, dirs, files in os.walk(docs_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                links = extract_links(content)

                for link in links:
                    # Skip external links and anchors
                    if link.startswith('http://') or link.startswith('https://'):
                        continue
                    if link.startswith('#'):
                        continue

                    # Normalize link (remove trailing slash variations)
                    normalized_link = link.rstrip('/')

                    # Check if link exists in permalinks
                    found = False
                    for permalink in permalinks:
                        if permalink.rstrip('/') == normalized_link:
                            found = True
                            break

                    # Check if link is missing baseurl prefix
                    if not found and link.startswith('/'):
                        relative_path = os.path.relpath(filepath, docs_dir)

                        # Suggest the correct link with baseurl
                        correct_link = f"{baseurl}{link}"
                        broken_links[relative_path].append({
                            'broken': link,
                            'suggestion': correct_link,
                            'reason': 'Missing baseurl prefix'
                        })

    return broken_links

def main():
    docs_dir = '/Users/ludo/code/pf2/docs'

    if not os.path.exists(docs_dir):
        print(f"Error: {docs_dir} not found")
        sys.exit(1)

    print("Checking for broken links in Jekyll docs...\n")

    broken_links = check_links(docs_dir)

    if broken_links:
        print("⚠️  BROKEN LINKS FOUND:\n")
        for filepath, links in sorted(broken_links.items()):
            print(f"\n📄 {filepath}")
            for link_info in links:
                if isinstance(link_info, dict):
                    print(f"   ❌ {link_info['broken']}")
                    print(f"      Reason: {link_info['reason']}")
                    print(f"      Suggestion: {link_info['suggestion']}")
                else:
                    # Backwards compatibility with old format
                    print(f"   ❌ {link_info}")

        print(f"\n\nTotal files with broken links: {len(broken_links)}")
        print("\n💡 TIP: Make sure all internal links include the baseurl prefix '/pf2'")
        sys.exit(1)
    else:
        print("✅ All links are valid!")
        sys.exit(0)

if __name__ == '__main__':
    main()
