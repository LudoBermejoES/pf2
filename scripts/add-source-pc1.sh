#!/bin/bash

# Script to add source: PC1 to all existing markdown files in docs/
# This retroactively marks all current content as PC1 before adding PC2 content

echo "📝 Añadiendo source: PC1 a archivos existentes..."
echo "=================================================="

count=0
skipped=0

# Find all .md files in docs/ (except root level)
find /Users/ludo/code/pf2/docs -type f -name "*.md" -not -path "/Users/ludo/code/pf2/docs/*.md" | while read file; do
  # Check if file already has a source field
  if grep -q "^source:" "$file"; then
    skipped=$((skipped + 1))
    echo "⏭️  Ya tiene source: $(basename "$file")"
  else
    # Check if it's a Jekyll file with frontmatter
    if grep -q "^---$" "$file"; then
      # Add source: PC1 after the first --- and before the closing ---
      # Using sed to insert after the first ---
      sed -i '' '/^---$/!b;N;s/^---\n/---\nsource: PC1\n/' "$file"
      count=$((count + 1))
      echo "✅ Agregado: $(basename "$file")"
    fi
  fi
done

echo ""
echo "=================================================="
echo "✨ Proceso completado:"
echo "   ✅ Archivos actualizados: $count"
echo "   ⏭️  Archivos ya tenían source: $skipped"
echo "=================================================="
