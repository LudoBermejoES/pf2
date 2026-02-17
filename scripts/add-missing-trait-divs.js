const fs = require('fs');
const path = require('path');

// Ascendencias que necesitan agregar divs de rasgos
const ascendenciasToFix = [
  'enano', 'espadachin', 'goblin', 'leshy', 'monje', 'orco',
  'hobgoblin', 'hombres-lagarto', 'kholo', 'kobold', 'ratfolk', 'tengu', 'tripkee'
];

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
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Buscar línea con **Dote X** (con o sin rasgos)
    const match = line.match(/^\*\*Dote \d+\*\*(\s+[-·]\s+(.+))?$/);

    if (match) {
      let traits = [];

      // Caso 1: **Dote X** - Rasgos (rasgos en la misma línea)
      if (match[2]) {
        traits = match[2].split(',').map(t => t.trim());
      }
      // Caso 2: **Dote X** seguido de *Rasgos* en las siguientes líneas (saltando líneas vacías)
      else {
        let nextIdx = i + 1;
        // Saltar líneas vacías
        while (nextIdx < lines.length && lines[nextIdx].trim() === '') {
          nextIdx++;
        }

        if (nextIdx < lines.length) {
          const nextLine = lines[nextIdx];
          const italicMatch = nextLine.match(/^\*([^*]+)\*$/);
          if (italicMatch) {
            traits = italicMatch[1].split(',').map(t => t.trim());
            // Marcar para eliminar la línea de rasgos
            lines[nextIdx] = '__DELETE__';
          }
        }
      }

      if (traits.length > 0) {
        // Crear div con enlaces a rasgos
        const traitLinks = traits.map(trait => {
          const slug = slugify(trait);
          return `<a href="/apendices/rasgos/${slug}/" class="feat-trait">${trait}</a>`;
        }).join('');

        const traitDiv = `<div class="feat-traits-header" markdown="0">${traitLinks}</div>`;

        // Agregar el div y saltar la línea original
        newLines.push(traitDiv);
        modified = true;

        console.log(`  ${path.basename(filePath)}: Agregado div de rasgos: ${traits.join(', ')}`);
      } else {
        // **Dote X** sin rasgos - mantener línea original
        newLines.push(line);
      }
    } else {
      newLines.push(line);
    }

    i++;
  }

  if (modified) {
    // Filtrar líneas marcadas para eliminar
    const finalLines = newLines.filter(line => line !== '__DELETE__');
    fs.writeFileSync(filePath, finalLines.join('\n'), 'utf8');
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

console.log('🔧 Agregando divs de rasgos faltantes en ascendencias...\n');

ascendenciasToFix.forEach(ascendencia => {
  processAscendencia(ascendencia);
});

console.log('\n✨ Corrección completada!');
