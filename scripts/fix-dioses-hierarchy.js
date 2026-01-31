#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const diosesDir = path.join(__dirname, '../docs/_introduccion/dioses');

// Get all god files except index.md
const files = fs.readdirSync(diosesDir)
  .filter(f => f.endsWith('.md') && f !== 'index.md');

console.log(`Updating ${files.length} god files...`);

files.forEach((file, index) => {
  const filePath = path.join(diosesDir, file);
  let content = fs.readFileSync(filePath, 'utf-8');

  // Replace grand_parent line
  content = content.replace(
    /grand_parent: Apéndices/g,
    'grand_parent: Introducción'
  );

  // Replace parent line to "Dioses"
  content = content.replace(
    /parent: Religion/g,
    'parent: Dioses'
  );

  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`Updated: ${file}`);
});

console.log('\n✅ Hierarchy fix complete!');
