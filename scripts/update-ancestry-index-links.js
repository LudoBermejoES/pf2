#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ancestriesDir = path.join(__dirname, '../docs/_ascendencias');

console.log('🔗 Actualizando enlaces en archivos index.md de ascendencias...\n');

// Get all ancestry directories
const ancestryDirs = fs.readdirSync(ancestriesDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name);

let updatedCount = 0;

ancestryDirs.forEach(ancestryDir => {
  const indexPath = path.join(ancestriesDir, ancestryDir, 'index.md');

  if (!fs.existsSync(indexPath)) {
    return;
  }

  const content = fs.readFileSync(indexPath, 'utf-8');

  // Replace Liquid-style links to dotes with absolute links to dotes_short
  const updated = content.replace(
    /\{\{\s*'\/ascendencias\/([^\/]+)\/dotes\/'\s*\|\s*relative_url\s*\}\}/g,
    '/ascendencias/$1/dotes_short/'
  );

  if (content !== updated) {
    fs.writeFileSync(indexPath, updated, 'utf-8');
    console.log(`✓ ${ancestryDir}/index.md`);
    updatedCount++;
  }
});

console.log(`\n✅ ${updatedCount} archivos actualizados`);
