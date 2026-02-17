const fs = require('fs');
const path = require('path');

// Herencias versátiles que necesitan corrección
const herenciasToFix = ['aiuvarin', 'changeling', 'dromaar', 'nefilim'];

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function fixFeatFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');

  let modified = false;
  const newLines = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Buscar línea con **Dote X** · Rasgo(s)
    const match = line.match(/^\*\*Dote \d+\*\*\s+·\s+(.+)$/);

    if (match) {
      // Extraer rasgos (separados por comas)
      const traitsText = match[1];
      const traits = traitsText.split(',').map(t => t.trim());

      // Crear div con enlaces a rasgos
      const traitLinks = traits.map(trait => {
        const slug = slugify(trait);
        return `<a href="/apendices/rasgos/${slug}/" class="feat-trait">${trait}</a>`;
      }).join('');

      const traitDiv = `<div class="feat-traits-header" markdown="0">${traitLinks}</div>`;

      // Reemplazar la línea con el div
      newLines.push(traitDiv);
      modified = true;

      console.log(`  ${path.basename(filePath)}: Reemplazado "${line}" con div de rasgos`);
    } else {
      newLines.push(line);
    }
  }

  if (modified) {
    fs.writeFileSync(filePath, newLines.join('\n'), 'utf8');
    return true;
  }

  return false;
}

function processHerencia(herenciaName) {
  const dirPath = path.join(__dirname, '..', 'docs', '_dotes', herenciaName);

  if (!fs.existsSync(dirPath)) {
    console.log(`⚠️  Directorio no existe: ${herenciaName}`);
    return;
  }

  console.log(`\n📁 Procesando ${herenciaName}...`);

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

  console.log(`✅ ${herenciaName}: ${fixedCount} archivos corregidos`);
}

console.log('🔧 Corrigiendo formato de rasgos en herencias versátiles...\n');

herenciasToFix.forEach(herencia => {
  processHerencia(herencia);
});

console.log('\n✨ Corrección completada!');
