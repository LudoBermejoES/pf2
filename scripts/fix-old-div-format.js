const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Find all files with old div format (without markdown="0")
const findOldDivFiles = () => {
  try {
    const result = execSync(
      `grep -rl '<div class="feat-traits-header">' docs/_dotes/ | while read file; do grep -L 'markdown="0"' "$file" 2>/dev/null && echo "$file"; done`,
      { encoding: 'utf-8', shell: 'bash' }
    );
    return result.trim().split('\n').filter(f => f);
  } catch (error) {
    console.error('Error finding files:', error.message);
    return [];
  }
};

// Fix old div format by adding markdown="0"
const fixDivFormat = (filePath) => {
  try {
    let content = fs.readFileSync(filePath, 'utf-8');

    // Replace old format with new format
    const oldPattern = /<div class="feat-traits-header">/g;
    const newFormat = '<div class="feat-traits-header" markdown="0">';

    if (content.match(oldPattern)) {
      content = content.replace(oldPattern, newFormat);
      fs.writeFileSync(filePath, content, 'utf-8');
      return true;
    }

    return false;
  } catch (error) {
    console.error(`Error fixing ${filePath}:`, error.message);
    return false;
  }
};

// Main execution
console.log('🔍 Buscando archivos con formato div antiguo...\n');

const files = findOldDivFiles();
console.log(`📋 Encontrados ${files.length} archivos con formato antiguo:\n`);

let fixedCount = 0;

files.forEach((file, index) => {
  console.log(`${index + 1}. ${file}`);
  if (fixDivFormat(file)) {
    fixedCount++;
  }
});

console.log(`\n✅ Corregidos ${fixedCount} de ${files.length} archivos`);
console.log('✨ Todos los divs ahora tienen markdown="0"');
