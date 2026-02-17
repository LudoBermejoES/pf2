const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Find all files with legacy "**Dote X**" lines
const findLegacyFiles = () => {
  try {
    const result = execSync(
      `grep -rl "^\\*\\*Dote [0-9]" docs/_dotes/`,
      { encoding: 'utf-8', shell: 'bash' }
    );
    return result.trim().split('\n').filter(f => f);
  } catch (error) {
    // grep returns non-zero if no matches
    if (error.stdout) {
      return error.stdout.trim().split('\n').filter(f => f);
    }
    return [];
  }
};

// Remove legacy feat lines
const removeLegacyLine = (filePath) => {
  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    let modified = false;
    const linesToRemove = new Set();

    // Find lines to remove
    lines.forEach((line, index) => {
      const match = line.match(/^\*\*Dote \d+\*\*(\s+[·\-]\s+.+)?$/);
      if (match) {
        modified = true;
        linesToRemove.add(index);
        // Also remove following empty line if exists
        if (index + 1 < lines.length && lines[index + 1].trim() === '') {
          linesToRemove.add(index + 1);
        }
      }
    });

    if (modified) {
      const filteredLines = lines.filter((line, index) => !linesToRemove.has(index));
      fs.writeFileSync(filePath, filteredLines.join('\n'), 'utf-8');
      return true;
    }

    return false;
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    return false;
  }
};

// Main execution
console.log('🔍 Buscando archivos con líneas legacy "**Dote X**"...\n');

const files = findLegacyFiles();
console.log(`📋 Encontrados ${files.length} archivos con formato legacy\n`);

let fixedCount = 0;
const categories = {};

files.forEach((file) => {
  const category = file.split('/')[2]; // Extract category from path
  categories[category] = (categories[category] || 0) + 1;

  if (removeLegacyLine(file)) {
    fixedCount++;
  }
});

console.log(`\n✅ Corregidos ${fixedCount} de ${files.length} archivos`);
console.log('\n📊 Distribución por categoría:');
Object.entries(categories).sort((a, b) => b[1] - a[1]).forEach(([cat, count]) => {
  console.log(`  ${cat}: ${count} archivos`);
});
console.log('\n✨ Todas las líneas legacy han sido eliminadas');
