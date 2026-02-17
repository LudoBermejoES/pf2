#!/usr/bin/env node
/**
 * Limpia títulos de dotes que incluyen texto de includes de Liquid
 *
 * Problema: Algunos archivos tienen en el frontmatter:
 *   title: ¡A la batalla! · {% include accion.html tipo="1" %}
 *   permalink: /dotes/.../a-la-batalla-include-accion-html-tipo-1/
 *
 * Debe ser:
 *   title: ¡A la batalla!
 *   permalink: /dotes/.../a-la-batalla/
 *
 * El include debe quedar solo en el título ## del documento
 */

const fs = require('fs');
const path = require('path');

const DOTES_DIR = path.join(__dirname, '..', 'docs', '_dotes');

// Buscar archivos con "-include-accion-html-tipo-" en el nombre
function findProblematicFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      findProblematicFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      if (entry.name.includes('-include-accion-html-tipo-')) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

function fixFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');

    let modified = false;
    let newTitle = null;
    let newPermalink = null;

    // Procesar líneas del frontmatter
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Limpiar title
      if (line.startsWith('title:')) {
        const match = line.match(/^title:\s*(.+?)\s*·\s*\{%\s*include\s+accion\.html.*$/);
        if (match) {
          newTitle = match[1].trim();
          lines[i] = `title: ${newTitle}`;
          modified = true;
        }
      }

      // Limpiar permalink
      if (line.startsWith('permalink:')) {
        const match = line.match(/^(permalink:\s*.*?)-include-accion-html-tipo-[^\/]+\/$/);
        if (match) {
          newPermalink = match[1] + '/';
          lines[i] = newPermalink;
          modified = true;
        }
      }
    }

    if (modified) {
      // Escribir archivo modificado
      fs.writeFileSync(filePath, lines.join('\n'), 'utf-8');

      // Calcular nuevo nombre de archivo
      const dirName = path.dirname(filePath);
      const fileName = path.basename(filePath);

      // Remover "-include-accion-html-tipo-X" del nombre del archivo
      const newFileName = fileName.replace(/-include-accion-html-tipo-[^.]+\.md$/, '.md');

      if (newFileName !== fileName) {
        const newFilePath = path.join(dirName, newFileName);

        // Renombrar archivo
        fs.renameSync(filePath, newFilePath);

        return {
          success: true,
          oldPath: filePath,
          newPath: newFilePath,
          title: newTitle
        };
      }

      return {
        success: true,
        oldPath: filePath,
        newPath: filePath,
        title: newTitle
      };
    }

    return { success: false, reason: 'no changes needed' };

  } catch (error) {
    return { success: false, error: error.message };
  }
}

function main() {
  console.log('=' .repeat(60));
  console.log('Limpiador de includes de Liquid en títulos de dotes');
  console.log('=' .repeat(60));
  console.log();

  console.log(`Buscando archivos problemáticos en ${DOTES_DIR}...`);
  const files = findProblematicFiles(DOTES_DIR);

  console.log(`Encontrados ${files.length} archivos con problema\n`);

  if (files.length === 0) {
    console.log('No hay archivos para corregir');
    return;
  }

  let fixed = 0;
  let renamed = 0;
  let errors = 0;

  for (const file of files) {
    const result = fixFile(file);

    if (result.success) {
      fixed++;
      const wasRenamed = result.oldPath !== result.newPath;
      if (wasRenamed) {
        renamed++;
        console.log(`✓ ${path.basename(result.oldPath)}`);
        console.log(`  → ${path.basename(result.newPath)}`);
        console.log(`  Título: ${result.title}\n`);
      } else {
        console.log(`✓ ${path.basename(result.oldPath)}`);
        console.log(`  Título: ${result.title}\n`);
      }
    } else if (result.error) {
      errors++;
      console.log(`✗ ${path.basename(file)}: ${result.error}\n`);
    }
  }

  console.log('=' .repeat(60));
  console.log(`Archivos corregidos: ${fixed}`);
  console.log(`Archivos renombrados: ${renamed}`);
  if (errors > 0) {
    console.log(`Errores: ${errors}`);
  }
  console.log('=' .repeat(60));
}

main();
