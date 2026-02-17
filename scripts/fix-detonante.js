const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Find all barbarian files with "Detonante:"
const findDetonanteFiles = () => {
  try {
    const result = execSync(
      `grep -l "Detonante:" docs/_dotes/barbaro/*.md`,
      { encoding: 'utf-8', shell: 'bash' }
    );
    return result.trim().split('\n').filter(f => f);
  } catch (error) {
    if (error.stdout) {
      return error.stdout.trim().split('\n').filter(f => f);
    }
    return [];
  }
};

// Fix "Detonante:" to "Desencadenante:"
const fixDetonante = (filePath) => {
  try {
    let content = fs.readFileSync(filePath, 'utf-8');

    // Replace "Detonante:" with "Desencadenante:"
    // Handle both formats: with and without space after **
    const pattern1 = /\*\*Detonante:\*\*/g;
    const pattern2 = /\*\*Detonante\*\*/g;

    let modified = false;

    if (content.match(pattern1)) {
      content = content.replace(pattern1, '**Desencadenante:**');
      modified = true;
    }

    if (content.match(pattern2)) {
      content = content.replace(pattern2, '**Desencadenante**');
      modified = true;
    }

    if (modified) {
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
console.log('🔍 Buscando dotes de bárbaro con "Detonante:"...\n');

const files = findDetonanteFiles();
console.log(`📋 Encontrados ${files.length} archivos con "Detonante:"\n`);

let fixedCount = 0;

files.forEach((file, index) => {
  const fileName = path.basename(file, '.md');
  console.log(`${index + 1}. ${fileName}`);

  if (fixDetonante(file)) {
    fixedCount++;
    console.log(`   ✓ Corregido: Detonante → Desencadenante`);
  }
});

console.log(`\n✅ Corregidos ${fixedCount} de ${files.length} archivos`);
console.log('✨ Todas las dotes de bárbaro ahora usan "Desencadenante:"');
