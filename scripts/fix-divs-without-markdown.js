const fs = require('fs');
const { execSync } = require('child_process');

// Get list of files from first argument or find them
const filesToFix = process.argv.slice(2);

if (filesToFix.length === 0) {
  console.log('❌ No files provided');
  console.log('Usage: node fix-divs-without-markdown.js file1.md file2.md ...');
  process.exit(1);
}

// Fix div format
const fixDiv = (filePath) => {
  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;

    // Replace div without markdown="0" with div with markdown="0"
    content = content.replace(
      /<div class="feat-traits-header">/g,
      '<div class="feat-traits-header" markdown="0">'
    );

    if (content !== originalContent) {
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
console.log('🔍 Corrigiendo divs sin markdown="0"...\n');

let fixedCount = 0;

filesToFix.forEach((file, index) => {
  const relativePath = file.replace(/^docs\/_dotes\//, '');
  console.log(`${index + 1}. ${relativePath}`);

  if (fixDiv(file)) {
    fixedCount++;
  }
});

console.log(`\n✅ Corregidos ${fixedCount} de ${filesToFix.length} archivos`);
console.log('✨ Todos los divs ahora tienen markdown="0"');
