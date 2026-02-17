#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('📝 Restaurando descripciones cortas de dotes_short.md...\n');

// Commit antes de los cambios (donde están las descripciones cortas)
const GOOD_COMMIT = '0ad26aee';

// Función para extraer dotes de un archivo markdown
function extractFeatsFromTable(content) {
  const feats = {};
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Detectar líneas de tabla con dotes
    if (line.startsWith('| [') && !line.includes('Dote |')) {
      // Extraer partes de la tabla
      const parts = line.split('|').map(p => p.trim()).filter(p => p);

      if (parts.length >= 2) {
        // Extraer nombre de la dote del enlace [Nombre](/url/)
        const nameMatch = parts[0].match(/\[([^\]]+)\]/);
        if (nameMatch) {
          const featName = nameMatch[1];
          const description = parts[1] || '';

          feats[featName] = description;
        }
      }
    }
  }

  return feats;
}

// Función para actualizar descripciones en un archivo
function updateDescriptions(filePath, oldDescriptions) {
  if (!fs.existsSync(filePath)) {
    console.log(`  ⚠️  Archivo no existe: ${filePath}`);
    return 0;
  }

  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  let updated = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.startsWith('| [') && !line.includes('Dote |')) {
      const parts = line.split('|').map(p => p.trim()).filter(p => p);

      if (parts.length >= 2) {
        const nameMatch = parts[0].match(/\[([^\]]+)\]/);
        if (nameMatch) {
          const featName = nameMatch[1];

          if (oldDescriptions[featName]) {
            // Reemplazar solo la descripción (columna 2)
            const oldDesc = oldDescriptions[featName];
            const currentDesc = parts[1];

            // Solo actualizar si es diferente
            if (currentDesc !== oldDesc) {
              parts[1] = oldDesc;
              lines[i] = '| ' + parts.join(' | ') + ' |';
              updated++;
            }
          }
        }
      }
    }
  }

  if (updated > 0) {
    fs.writeFileSync(filePath, lines.join('\n'), 'utf-8');
  }

  return updated;
}

// Procesar archivos
function processFiles(directory) {
  try {
    const baseDir = path.join(__dirname, '..', directory);

    if (!fs.existsSync(baseDir)) {
      console.log(`  ⚠️  Directorio no existe: ${baseDir}`);
      return;
    }

    // Obtener subdirectorios
    const subdirs = fs.readdirSync(baseDir).filter(f => {
      const fullPath = path.join(baseDir, f);
      return fs.statSync(fullPath).isDirectory();
    });

    console.log(`\n🔍 Procesando ${subdirs.length} directorios en ${directory}...\n`);

    let totalUpdated = 0;

    subdirs.forEach(subdir => {
      const dotesShortPath = path.join(baseDir, subdir, 'dotes_short.md');
      const gitPath = `${directory}/${subdir}/dotes_short.md`;

      if (!fs.existsSync(dotesShortPath)) {
        return;
      }

      try {
        // Obtener contenido del commit antiguo
        const oldContent = execSync(
          `git show ${GOOD_COMMIT}:"${gitPath}"`,
          { encoding: 'utf-8', cwd: path.join(__dirname, '..') }
        );

        // Extraer descripciones del archivo antiguo
        const oldDescriptions = extractFeatsFromTable(oldContent);

        // Actualizar archivo actual
        const updated = updateDescriptions(dotesShortPath, oldDescriptions);

        if (updated > 0) {
          console.log(`  ✓ ${subdir}: ${updated} descripciones actualizadas`);
          totalUpdated += updated;
        }
      } catch (error) {
        // Archivo no existe en commit antiguo
        // console.log(`  ⚠️  ${subdir}: no existe en commit antiguo`);
      }
    });

    console.log(`\n  Total: ${totalUpdated} descripciones actualizadas`);

  } catch (error) {
    console.error(`  ⚠️  Error procesando ${directory}:`, error.message);
  }
}

// Procesar ascendencias
processFiles('docs/_ascendencias');

// Procesar clases
processFiles('docs/_clases');

console.log('\n✅ Restauración completada');
