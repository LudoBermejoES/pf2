#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ancestriesDir = path.join(__dirname, '../docs/_ascendencias');

console.log('📝 Añadiendo sección "Selecciones relacionadas" a archivos index.md...\n');

// List of ancestry directories that need the section
const ancestriesToFix = [
  'catfolk',
  'changeling',
  'kholo',
  'kobold',
  'ratfolk',
  'tengu',
  'tripkee'
];

let addedCount = 0;

ancestriesToFix.forEach(ancestryDir => {
  const indexPath = path.join(ancestriesDir, ancestryDir, 'index.md');

  if (!fs.existsSync(indexPath)) {
    console.log(`⚠️  No se encontró: ${ancestryDir}/index.md`);
    return;
  }

  let content = fs.readFileSync(indexPath, 'utf-8');

  // Check if it already has "Selecciones relacionadas"
  if (content.includes('Selecciones relacionadas')) {
    console.log(`⏭️  Ya tiene la sección: ${ancestryDir}/index.md`);
    return;
  }

  // Add the section at the end
  const relatedSection = `\n## Selecciones relacionadas

- [Dotes](/ascendencias/${ancestryDir}/dotes_short/)
- [Herencias]({{ '/ascendencias/${ancestryDir}/herencias/' | relative_url }})
`;

  // Trim trailing whitespace and add the section
  content = content.trimEnd() + '\n' + relatedSection;

  fs.writeFileSync(indexPath, content, 'utf-8');
  console.log(`✓ ${ancestryDir}/index.md`);
  addedCount++;
});

console.log(`\n✅ ${addedCount} archivos actualizados`);
