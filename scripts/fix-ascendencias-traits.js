const fs = require('fs');
const path = require('path');

// Directorios de ascendencias a corregir
const ascendenciasToFix = [
  'elfo', 'enano', 'espadachin', 'gnomo', 'goblin',
  'humano', 'leshy', 'mediano', 'monje', 'orco',
  'hobgoblin', 'hombres-lagarto', 'kholo', 'kobold', 'ratfolk', 'tengu', 'tripkee'
];

function fixFeatFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');

  let modified = false;
  const newLines = [];
  let hasFeatTraitsDiv = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Detectar si el archivo tiene el div de rasgos
    if (line.includes('feat-traits-header')) {
      hasFeatTraitsDiv = true;
    }

    // Buscar línea redundante con **Dote X** seguida de rasgos
    // Patrones: **Dote X** · Rasgo o **Dote X** - Rasgo o solo **Dote X**
    const match = line.match(/^\*\*Dote \d+\*\*(\s+[·\-]\s+.+)?$/);

    if (match && hasFeatTraitsDiv) {
      // Eliminar la línea redundante
      console.log(`  ${path.basename(filePath)}: Eliminada línea redundante: "${line}"`);
      modified = true;
      continue; // Saltar esta línea
    }

    newLines.push(line);
  }

  if (modified) {
    fs.writeFileSync(filePath, newLines.join('\n'), 'utf8');
    return true;
  }

  return false;
}

function processAscendencia(ascendenciaName) {
  const dirPath = path.join(__dirname, '..', 'docs', '_dotes', ascendenciaName);

  if (!fs.existsSync(dirPath)) {
    console.log(`⚠️  Directorio no existe: ${ascendenciaName}`);
    return;
  }

  console.log(`\n📁 Procesando ${ascendenciaName}...`);

  const files = fs.readdirSync(dirPath);
  let fixedCount = 0;

  for (const file of files) {
    if (file === 'dotes_short.md' || !file.endsWith('.md')) {
      continue;
    }

    const filePath = path.join(dirPath, file);
    if (fixFeatFile(filePath)) {
      fixedCount++;
    }
  }

  console.log(`✅ ${ascendenciaName}: ${fixedCount} archivos corregidos`);
}

console.log('🔧 Eliminando líneas redundantes de rasgos en ascendencias...\n');

ascendenciasToFix.forEach(ascendencia => {
  processAscendencia(ascendencia);
});

console.log('\n✨ Corrección completada!');
