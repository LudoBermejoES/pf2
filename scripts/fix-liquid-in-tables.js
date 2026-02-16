#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const classesDir = path.join(__dirname, '../docs/_clases');

/**
 * Fix Liquid syntax errors in markdown tables by wrapping table content in {% raw %} tags
 */
function fixLiquidInTables(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const output = [];

  let inTable = false;
  let tableStartIndex = -1;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Check if this is a table header (starts with |)
    if (line.trim().startsWith('|') && line.includes('|') && !inTable) {
      // Check if next line is separator (----)
      if (i + 1 < lines.length && lines[i + 1].match(/^\|[-:\s|]+\|$/)) {
        inTable = true;
        tableStartIndex = i;
        output.push('{% raw %}');
        output.push(line);
        continue;
      }
    }

    // If in table, check if we're leaving it
    if (inTable) {
      if (line.trim() === '' || !line.trim().startsWith('|')) {
        // End of table
        output.push('{% endraw %}');
        output.push(line);
        inTable = false;
        continue;
      }
    }

    output.push(line);
  }

  // If we're still in a table at the end, close it
  if (inTable) {
    output.push('{% endraw %}');
  }

  return output.join('\n');
}

// Process all dotes_short.md files
function processAllDotesFiles() {
  const classes = fs.readdirSync(classesDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  console.log(`🔧 Corrigiendo sintaxis Liquid en ${classes.length} archivos...\n`);

  let fixedCount = 0;

  for (const className of classes) {
    const dotesPath = path.join(classesDir, className, 'dotes_short.md');

    if (fs.existsSync(dotesPath)) {
      const fixed = fixLiquidInTables(dotesPath);
      fs.writeFileSync(dotesPath, fixed, 'utf-8');
      console.log(`✓ ${className}/dotes_short.md`);
      fixedCount++;
    }
  }

  console.log(`\n✅ ${fixedCount} archivos corregidos`);
}

processAllDotesFiles();
