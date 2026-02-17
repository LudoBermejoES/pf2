#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const versatileHeritagesDir = path.join(__dirname, '../docs/_ascendencias/herencias-versatiles');

console.log('📝 Actualizando archivos de herencias versátiles...\n');

const heritageFiles = [
  { file: 'ascendencia-mixta.md', slug: 'ascendencia-mixta', name: 'Ascendencia Mixta' },
  { file: 'caminante-del-ocaso.md', slug: 'caminante-del-ocaso', name: 'Caminante del Ocaso' },
  { file: 'changeling.md', slug: 'changeling', name: 'Changeling' },
  { file: 'dhampir.md', slug: 'dhampir', name: 'Dhampir' },
  { file: 'nefilim.md', slug: 'nefilim', name: 'Nefilim' },
  { file: 'sangre-de-dragon.md', slug: 'sangre-de-dragon', name: 'Sangre de Dragón' }
];

heritageFiles.forEach(heritage => {
  const filePath = path.join(versatileHeritagesDir, heritage.file);

  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  No se encontró: ${heritage.file}`);
    return;
  }

  console.log(`\n🔍 Procesando ${heritage.name}...`);

  // Read file content
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  // Find where feats section starts and ends
  let newLines = [];
  let inFeatsSection = false;
  let foundFeatsSection = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Check for any "Dotes" section
    if (line.match(/^##\s+Dotes/i)) {
      inFeatsSection = true;
      foundFeatsSection = true;
      console.log(`  📍 Encontrada sección de dotes en línea ${i + 1}`);
      continue;
    }

    // Check if we reached another main section (stop removing)
    if (inFeatsSection && line.match(/^##\s+[^#]/) && !line.match(/^##\s+Dotes/i)) {
      inFeatsSection = false;
      // Add the link section before this new section
      newLines.push('## Selecciones relacionadas\n');
      newLines.push(`- [Dotes]({{ '/ascendencias/herencias-versatiles/${heritage.slug}/dotes_short/' | relative_url }})\n`);
      newLines.push('');
    }

    // Add line if not in feats section
    if (!inFeatsSection) {
      newLines.push(line);
    }
  }

  // If we ended while still in feats section, add the link at the end
  if (inFeatsSection || foundFeatsSection) {
    // Remove trailing empty lines
    while (newLines.length > 0 && newLines[newLines.length - 1].trim() === '') {
      newLines.pop();
    }

    newLines.push('');
    newLines.push('## Selecciones relacionadas\n');
    newLines.push(`- [Dotes]({{ '/ascendencias/herencias-versatiles/${heritage.slug}/dotes_short/' | relative_url }})\n`);
  }

  const newContent = newLines.join('\n');

  // Write updated content
  fs.writeFileSync(filePath, newContent, 'utf-8');
  console.log(`  ✓ Actualizado: ${heritage.file}`);
});

console.log('\n✅ Archivos actualizados');
