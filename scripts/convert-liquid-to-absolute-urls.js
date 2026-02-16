#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const classesDir = path.join(__dirname, '../docs/_clases');

/**
 * Convert Liquid relative_url to absolute paths in tables
 * From: {{ '/dotes/guerrero/ataque/' | relative_url }}
 * To: /dotes/guerrero/ataque/
 */
function convertLiquidToAbsoluteUrls(content) {
  // Replace {{ 'path' | relative_url }} with just /path/
  return content.replace(/\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}/g, '$1');
}

// Process all dotes_short.md files
function processAllDotesFiles() {
  const classes = fs.readdirSync(classesDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  console.log(`🔧 Convirtiendo URLs Liquid a absolutas en ${classes.length} archivos...\n`);

  let fixedCount = 0;

  for (const className of classes) {
    const dotesPath = path.join(classesDir, className, 'dotes_short.md');

    if (fs.existsSync(dotesPath)) {
      const content = fs.readFileSync(dotesPath, 'utf-8');
      const converted = convertLiquidToAbsoluteUrls(content);

      if (content !== converted) {
        fs.writeFileSync(dotesPath, converted, 'utf-8');
        console.log(`✓ ${className}/dotes_short.md`);
        fixedCount++;
      }
    }
  }

  console.log(`\n✅ ${fixedCount} archivos convertidos`);
}

processAllDotesFiles();
