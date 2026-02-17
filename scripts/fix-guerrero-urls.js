#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '../docs/_clases/guerrero/dotes_short.md');

console.log('🔧 Arreglando URLs de guerrero/dotes_short.md...\n');

let content = fs.readFileSync(filePath, 'utf-8');

// Count matches before replacement
const matches = content.match(/\{\{\s*'\/dotes\/guerrero\/[^']+'\s*\|\s*relative_url\s*\}\}/g);
console.log(`Found ${matches ? matches.length : 0} Liquid URLs to convert\n`);

// Replace {{ '/dotes/guerrero/slug/' | relative_url }} with /dotes/guerrero/slug/
content = content.replace(
  /\{\{\s*'(\/dotes\/guerrero\/[^']+)'\s*\|\s*relative_url\s*\}\}/g,
  '$1'
);

fs.writeFileSync(filePath, content, 'utf-8');

console.log('✅ Archivo convertido exitosamente');
