#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const versatileHeritagesDir = path.join(__dirname, '../docs/_ascendencias/herencias-versatiles');
const dotesDir = path.join(__dirname, '../docs/_dotes');

console.log('📚 Extrayendo dotes de herencias versátiles...\n');

// List of versatile heritages to process
const heritageFiles = [
  { file: 'ascendencia-mixta.md', slug: 'ascendencia-mixta', name: 'Ascendencia Mixta' },
  { file: 'caminante-del-ocaso.md', slug: 'caminante-del-ocaso', name: 'Caminante del Ocaso' },
  { file: 'changeling.md', slug: 'changeling', name: 'Changeling' },
  { file: 'dhampir.md', slug: 'dhampir', name: 'Dhampir' },
  { file: 'nefilim.md', slug: 'nefilim', name: 'Nefilim' },
  { file: 'sangre-de-dragon.md', slug: 'sangre-de-dragon', name: 'Sangre de Dragón' }
];

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function cleanFeatName(name) {
  // Remove everything from {% include onwards
  let cleaned = name.replace(/\s*\{%[^%]*%\}/g, '');

  // Remove "· Dote X ·" or "Dote X ·" patterns
  cleaned = cleaned.replace(/\s*·?\s*[Dd]ote\s+\d+\s*·?\s*/g, '');

  // Remove trailing separators
  cleaned = cleaned.replace(/\s*·\s*$/g, '');

  return cleaned.trim();
}

let totalFeatsExtracted = 0;

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

  // Find where feats section starts
  let inFeatsSection = false;
  let currentLevel = null;
  let currentFeat = null;
  let currentFeatContent = [];
  const feats = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Check for any "Dotes" section (## Dotes de... or just after seeing feats)
    if (line.match(/^##\s+Dotes/i)) {
      inFeatsSection = true;

      // Check if the section header has "nivel X" pattern
      const levelInHeader = line.match(/^##\s+Dotes de nivel\s+(\d+)/i);
      if (levelInHeader) {
        currentLevel = parseInt(levelInHeader[1]);
      }
      continue;
    }

    // Stop at next main section after feats (except for other Dotes sections)
    if (inFeatsSection && line.match(/^##\s+[^#]/) && !line.match(/^##\s+Dotes/i)) {
      // Save last feat if exists
      if (currentFeat) {
        feats.push({
          name: currentFeat.name,
          level: currentFeat.level,
          content: currentFeatContent.join('\n').trim()
        });
      }
      break;
    }

    if (!inFeatsSection) continue;

    // Check for level headers (### Nivel X)
    const levelMatch = line.match(/^###\s+Nivel\s+(\d+)/i);
    if (levelMatch) {
      currentLevel = parseInt(levelMatch[1]);
      continue;
    }

    // Check for feat name - either #### or ### format
    const featMatch4 = line.match(/^####\s+(.+)$/);
    const featMatch3 = line.match(/^###\s+(.+)$/);
    const featMatch = featMatch4 || featMatch3;

    if (featMatch) {
      // Save previous feat if exists
      if (currentFeat) {
        feats.push({
          name: currentFeat.name,
          level: currentFeat.level,
          content: currentFeatContent.join('\n').trim()
        });
      }

      // Start new feat
      const rawFeatName = featMatch[1].trim();
      const featName = cleanFeatName(rawFeatName);

      currentFeat = {
        name: featName,
        level: currentLevel || 1
      };
      currentFeatContent = [line];
      continue;
    }

    // Accumulate feat content
    if (currentFeat) {
      currentFeatContent.push(line);
    }
  }

  // Save last feat if exists
  if (currentFeat) {
    feats.push({
      name: currentFeat.name,
      level: currentFeat.level,
      content: currentFeatContent.join('\n').trim()
    });
  }

  if (feats.length === 0) {
    console.log(`  ⚠️  No se encontraron dotes`);
    return;
  }

  console.log(`  📝 Encontradas ${feats.length} dotes`);

  // Create output directory for this heritage
  const heritageOutputDir = path.join(dotesDir, heritage.slug);
  if (!fs.existsSync(heritageOutputDir)) {
    fs.mkdirSync(heritageOutputDir, { recursive: true });
  }

  // Generate individual feat files
  let createdCount = 0;
  feats.forEach(feat => {
    const featSlug = slugify(feat.name);
    const featPath = path.join(heritageOutputDir, `${featSlug}.md`);

    // Clean the feat content - remove the first line (the header)
    let contentLines = feat.content.split('\n');
    // Remove first line if it starts with ### or ####
    if (contentLines[0] && (contentLines[0].startsWith('###') || contentLines[0].startsWith('####'))) {
      contentLines.shift();
    }
    let cleanedContent = contentLines.join('\n').trim();

    // Remove trailing --- if it exists
    if (cleanedContent.endsWith('---')) {
      cleanedContent = cleanedContent.slice(0, -3).trim();
    }

    // Create frontmatter
    const frontmatter = `---
layout: page
permalink: /dotes/${heritage.slug}/${featSlug}/
title: ${feat.name}
chapter: Dotes
category: dotes
herencia_versatil: ${heritage.name}
level: ${feat.level}
---

`;

    // Build the full content with proper formatting
    const fullContent = frontmatter + `## ${feat.name}\n\n` + cleanedContent + '\n\n---\n';

    fs.writeFileSync(featPath, fullContent, 'utf-8');
    createdCount++;
  });

  console.log(`  ✓ Creados ${createdCount} archivos de dotes`);

  // Generate dotes_short.md with table
  const tableRows = feats.map(feat => {
    const featSlug = slugify(feat.name);
    return `| [${feat.name}](/dotes/${heritage.slug}/${featSlug}/) | ${feat.level} |`;
  }).join('\n');

  const dotesShortContent = `---
layout: page
permalink: /ascendencias/herencias-versatiles/${heritage.slug}/dotes_short/
title: Dotes de ${heritage.name}
chapter: Ascendencias
category: ascendencias
herencia_versatil: ${heritage.name}
---

# Dotes de ${heritage.name}

| Dote | Nivel |
|------|-------|
${tableRows}
`;

  const dotesShortPath = path.join(heritageOutputDir, 'dotes_short.md');
  fs.writeFileSync(dotesShortPath, dotesShortContent, 'utf-8');
  console.log(`  ✓ Creado dotes_short.md`);

  totalFeatsExtracted += feats.length;
});

console.log(`\n✅ Total de dotes extraídas: ${totalFeatsExtracted}`);
