#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Find all feat files with pipe characters in titles
const dotesDir = path.join(__dirname, '../docs/_dotes');

function fixYamlTitle(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  let modified = false;
  const output = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Check for unquoted title with pipe character
    const titleMatch = line.match(/^title:\s*([^"'].*)(\|.*)/);
    if (titleMatch) {
      const titleValue = titleMatch[1] + titleMatch[2];
      output.push(`title: "${titleValue.trim()}"`);
      modified = true;
    } else {
      output.push(line);
    }
  }

  if (modified) {
    fs.writeFileSync(filePath, output.join('\n'), 'utf-8');
    return true;
  }

  return false;
}

function processDirectory(dir) {
  let fixedCount = 0;

  const files = fs.readdirSync(dir, { withFileTypes: true });

  for (const file of files) {
    const fullPath = path.join(dir, file.name);

    if (file.isDirectory()) {
      fixedCount += processDirectory(fullPath);
    } else if (file.name.endsWith('.md')) {
      if (fixYamlTitle(fullPath)) {
        console.log(`✓ Fixed: ${path.relative(dotesDir, fullPath)}`);
        fixedCount++;
      }
    }
  }

  return fixedCount;
}

console.log('🔧 Fixing YAML titles with pipe characters...\n');

const fixedCount = processDirectory(dotesDir);

console.log(`\n✅ Fixed ${fixedCount} files`);
