#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Fix YAML frontmatter issues:
 * 1. Unquoted values with colons (title: Something: Something)
 * 2. Unquoted values with exclamation marks (title: !Something!)
 * 3. Already quoted values should be preserved
 */
function fixYamlFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  let inFrontmatter = false;
  let modified = false;
  const output = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Track frontmatter boundaries
    if (line === '---') {
      inFrontmatter = !inFrontmatter;
      output.push(line);
      continue;
    }

    // Only process lines inside frontmatter
    if (!inFrontmatter) {
      output.push(line);
      continue;
    }

    // Match YAML key-value pairs
    const yamlMatch = line.match(/^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.+)$/);

    if (yamlMatch) {
      const indent = yamlMatch[1];
      const key = yamlMatch[2];
      const value = yamlMatch[3].trim();

      // Check if value needs quoting
      const needsQuoting =
        // Not already quoted
        !(value.startsWith('"') && value.endsWith('"')) &&
        !(value.startsWith("'") && value.endsWith("'")) &&
        // Contains special characters that require quoting
        (
          value.includes(':') ||     // Colons
          value.includes('|') ||     // Pipes
          value.startsWith('!') ||   // Exclamation marks at start
          value.includes('#')        // Hash symbols
        );

      if (needsQuoting) {
        // Escape any double quotes inside the value
        const escapedValue = value.replace(/"/g, '\\"');
        output.push(`${indent}${key}: "${escapedValue}"`);
        modified = true;
      } else {
        output.push(line);
      }
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

function processDirectory(dir, pattern = '**/*.md') {
  let fixedCount = 0;
  const files = fs.readdirSync(dir, { withFileTypes: true });

  for (const file of files) {
    const fullPath = path.join(dir, file.name);

    if (file.isDirectory()) {
      fixedCount += processDirectory(fullPath, pattern);
    } else if (file.name.match(/\.(md|html)$/)) {
      try {
        if (fixYamlFrontmatter(fullPath)) {
          console.log(`✓ Fixed: ${path.relative(process.cwd(), fullPath)}`);
          fixedCount++;
        }
      } catch (error) {
        console.error(`✗ Error processing ${fullPath}: ${error.message}`);
      }
    }
  }

  return fixedCount;
}

console.log('🔧 Fixing all YAML frontmatter issues...\n');

const docsDir = path.join(__dirname, '../docs');
const fixedCount = processDirectory(docsDir);

console.log(`\n✅ Fixed ${fixedCount} files with YAML issues`);
