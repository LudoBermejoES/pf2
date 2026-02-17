#!/usr/bin/env node
/**
 * Actualiza enlaces que apuntan a los viejos permalinks con includes de Liquid
 *
 * Reemplaza:
 *   /dotes/.../nombre-include-accion-html-tipo-X/
 * Con:
 *   /dotes/.../nombre/
 */

const fs = require('fs');
const path = require('path');

const DOCS_DIR = path.join(__dirname, '..', 'docs');

function findMarkdownFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      findMarkdownFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }

  return files;
}

function fixLinks(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;

    // Patrón para capturar enlaces con include-accion-html-tipo-X
    // Ejemplos:
    // /dotes/arquetipo/acrobata/esquiva-evasiva-include-accion-html-tipo-libre/
    // /dotes/arquetipo/mariscal/a-la-batalla-include-accion-html-tipo-1-o-include-accion-html-tipo-2/
    const pattern = /\/dotes\/(.*?)-include-accion-html-tipo-[^\/]+\//g;

    content = content.replace(pattern, (match, base) => {
      return `/dotes/${base}/`;
    });

    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf-8');
      return { modified: true, path: filePath };
    }

    return { modified: false };

  } catch (error) {
    return { error: error.message, path: filePath };
  }
}

function main() {
  console.log('=' .repeat(60));
  console.log('Actualizador de enlaces a dotes con includes');
  console.log('=' .repeat(60));
  console.log();

  console.log(`Buscando archivos markdown en ${DOCS_DIR}...`);
  const files = findMarkdownFiles(DOCS_DIR);
  console.log(`Encontrados ${files.length} archivos markdown\n`);

  let modified = 0;
  let errors = 0;

  for (const file of files) {
    const result = fixLinks(file);

    if (result.modified) {
      modified++;
      const relativePath = path.relative(DOCS_DIR, result.path);
      console.log(`✓ ${relativePath}`);
    } else if (result.error) {
      errors++;
      console.log(`✗ ${path.relative(DOCS_DIR, result.path)}: ${result.error}`);
    }
  }

  console.log('\n' + '=' .repeat(60));
  console.log(`Archivos modificados: ${modified}`);
  if (errors > 0) {
    console.log(`Errores: ${errors}`);
  }
  console.log('=' .repeat(60));
}

main();
