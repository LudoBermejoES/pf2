#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const classesDir = path.join(__dirname, '../docs/_clases');

// Find all dotes.md files in class directories
function renameClassDotesFiles() {
  const classes = fs.readdirSync(classesDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  console.log(`📝 Renombrando archivos de dotes en ${classes.length} clases...\n`);

  for (const className of classes) {
    const dotesPath = path.join(classesDir, className, 'dotes.md');
    const dotesShortPath = path.join(classesDir, className, 'dotes_short.md');

    if (fs.existsSync(dotesPath)) {
      // Read the file
      const content = fs.readFileSync(dotesPath, 'utf-8');

      // Update the permalink
      const updatedContent = content.replace(
        /permalink: (\/[^\/]+\/[^\/]+\/)dotes\//,
        'permalink: $1dotes_short/'
      );

      // Write to new file
      fs.writeFileSync(dotesShortPath, updatedContent, 'utf-8');

      // Delete old file
      fs.unlinkSync(dotesPath);

      console.log(`✓ ${className}: dotes.md → dotes_short.md`);
    }
  }
}

// Update links in other files that reference /dotes/
function updateLinksInFiles() {
  console.log('\n📝 Actualizando enlaces...\n');

  const filesToUpdate = [
    'docs/_clases/*/index.md',
    'docs/_clases/*/caracteristicas.md',
    'docs/_clases/*/descripcion.md'
  ];

  let updatedCount = 0;

  function updateFile(filePath) {
    if (!fs.existsSync(filePath)) return;

    const content = fs.readFileSync(filePath, 'utf-8');

    // Update links from /clases/*/dotes/ to /clases/*/dotes_short/
    const updatedContent = content.replace(
      /(\[.*?\]\([^)]*\/clases\/[^\/]+\/)dotes\//g,
      '$1dotes_short/'
    );

    if (content !== updatedContent) {
      fs.writeFileSync(filePath, updatedContent, 'utf-8');
      updatedCount++;
      console.log(`✓ Actualizado: ${path.relative(process.cwd(), filePath)}`);
    }
  }

  // Find and update all class files
  const classes = fs.readdirSync(classesDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  for (const className of classes) {
    const classPath = path.join(classesDir, className);
    const files = fs.readdirSync(classPath)
      .filter(f => f.endsWith('.md'))
      .map(f => path.join(classPath, f));

    files.forEach(updateFile);
  }

  console.log(`\n✓ ${updatedCount} archivos actualizados`);
}

// Main execution
renameClassDotesFiles();
updateLinksInFiles();

console.log('\n✅ Renombrado completado!');
