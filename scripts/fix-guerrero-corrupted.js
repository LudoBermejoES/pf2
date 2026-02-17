#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '../docs/_clases/guerrero/dotes_short.md');

console.log('🔧 Arreglando tabla corrupta de guerrero/dotes_short.md...\n');

let content = fs.readFileSync(filePath, 'utf-8');
let lineCount = 0;

// Fix the corrupted pattern: {{ '/path/' | Description | Traits | Requirements |
// Should be: /path/) | Description | Traits | Requirements |
content = content.replace(
  /\|\s*\[([^\]]+)\]\(\{\{\s*'(\/dotes\/guerrero\/[^']+)'\s*\|\s*/g,
  (match, text, url) => {
    lineCount++;
    return `| [${text}](${url}) | `;
  }
);

fs.writeFileSync(filePath, content, 'utf-8');

console.log(`✅ ${lineCount} líneas corregidas`);
