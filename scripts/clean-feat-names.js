#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Helper to create slug
function slug(str) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove accents
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Clean feat name by removing Liquid includes and "Dote X" markers
function cleanFeatName(name) {
  // Remove everything from {% include onwards
  let cleaned = name.replace(/\s*\{%[^%]*%\}/g, '');

  // Remove everything from "include-accion" onwards (for file names)
  cleaned = cleaned.replace(/\s*include-accion.*$/i, '');

  // Remove "· Dote X ·" or "Dote X ·" patterns
  cleaned = cleaned.replace(/\s*·?\s*[Dd]ote\s+\d+\s*·?\s*/g, '');

  // Remove trailing separators
  cleaned = cleaned.replace(/\s*·\s*$/g, '');

  return cleaned.trim();
}

console.log('🧹 Limpiando nombres de dotes con código Liquid...\n');

// Find all files with "include-accion" in the name
const dotesDir = path.join(__dirname, '../docs/_dotes');

function findAffectedFiles(dir) {
  const files = [];

  function scan(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);

      if (entry.isDirectory()) {
        scan(fullPath);
      } else if (entry.isFile() && entry.name.includes('include-accion')) {
        files.push(fullPath);
      }
    }
  }

  scan(dir);
  return files;
}

const affectedFiles = findAffectedFiles(dotesDir);

console.log(`Encontrados ${affectedFiles.length} archivos afectados\n`);

let cleanedCount = 0;
let renamedCount = 0;

affectedFiles.forEach(filePath => {
  const content = fs.readFileSync(filePath, 'utf-8');
  const fileName = path.basename(filePath);
  const dirName = path.dirname(filePath);
  const ancestryName = path.basename(dirName);

  // Extract the clean feat name from the file content
  const titleMatch = content.match(/^title:\s*(.+)$/m);
  if (!titleMatch) {
    console.log(`⚠️  No se pudo encontrar título en: ${fileName}`);
    return;
  }

  const originalTitle = titleMatch[1];
  const cleanTitle = cleanFeatName(originalTitle);
  const cleanSlug = slug(cleanTitle);
  const newFileName = `${cleanSlug}.md`;
  const newFilePath = path.join(dirName, newFileName);

  // Clean the content
  let updatedContent = content;

  // Update title
  updatedContent = updatedContent.replace(
    /^title:\s*.+$/m,
    `title: ${cleanTitle}`
  );

  // Update permalink
  updatedContent = updatedContent.replace(
    /^permalink:\s*\/dotes\/[^\/]+\/[^\/]+\/$/m,
    `permalink: /dotes/${ancestryName}/${cleanSlug}/`
  );

  // Update ## header (preserve everything after the title)
  updatedContent = updatedContent.replace(
    /^##\s+.+?(\{%[^%]*%\})?$/m,
    `## ${cleanTitle}`
  );

  // Write updated content to new file
  fs.writeFileSync(newFilePath, updatedContent, 'utf-8');

  // Delete old file if name changed
  if (filePath !== newFilePath) {
    fs.unlinkSync(filePath);
    console.log(`✓ Renombrado: ${fileName} -> ${newFileName}`);
    renamedCount++;
  } else {
    console.log(`✓ Limpiado: ${newFileName}`);
  }

  cleanedCount++;
});

console.log(`\n✅ Proceso completado!`);
console.log(`   ${cleanedCount} archivos limpiados`);
console.log(`   ${renamedCount} archivos renombrados`);
