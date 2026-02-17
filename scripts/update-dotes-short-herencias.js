#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const dotesDir = path.join(__dirname, '../docs/_dotes');

console.log('📝 Actualizando dotes_short.md de herencias versátiles...\n');

const heritageFiles = [
  { slug: 'ascendencia-mixta', name: 'Ascendencia Mixta' },
  { slug: 'caminante-del-ocaso', name: 'Caminante del Ocaso' },
  { slug: 'changeling', name: 'Changeling' },
  { slug: 'dhampir', name: 'Dhampir' },
  { slug: 'nefilim', name: 'Nefilim' },
  { slug: 'sangre-de-dragon', name: 'Sangre de Dragón' }
];

function extractFeatInfo(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  let description = '';
  let traits = '';
  let requirements = '';
  let inContent = false;
  let foundHeader = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Skip frontmatter
    if (i === 0 && line === '---') {
      inContent = false;
      continue;
    }
    if (!inContent && line === '---') {
      inContent = true;
      continue;
    }
    if (!inContent) continue;

    // Skip the ## header
    if (line.startsWith('##')) {
      foundHeader = true;
      continue;
    }

    if (!foundHeader) continue;

    // Extract traits from <div class="feat-traits-header">
    if (line.includes('feat-traits-header')) {
      // Extract trait names from the links
      const traitMatches = line.matchAll(/class="feat-trait">([^<]+)<\/a>/g);
      const extractedTraits = [];
      for (const match of traitMatches) {
        extractedTraits.push(match[1]);
      }
      traits = extractedTraits.join(', ');
      continue;
    }

    // Extract traits from **Dote X** · Trait format
    if (line.match(/\*\*Dote \d+\*\* · /)) {
      const traitMatch = line.match(/\*\*Dote \d+\*\* · (.+)/);
      if (traitMatch) {
        traits = traitMatch[1].trim();
      }
      continue;
    }

    // Extract requirements
    if (line.match(/\*\*(Requisitos?|Prerrequisitos?|Requirements?):/i)) {
      const reqMatch = line.match(/\*\*(Requisitos?|Prerrequisitos?|Requirements?):\*\*\s*(.+)/i);
      if (reqMatch) {
        requirements = reqMatch[2].trim();
      }
      continue;
    }

    // Extract description (first non-empty paragraph that's not a special section)
    if (!description && line.trim() && !line.startsWith('**') && !line.startsWith('---') && !line.startsWith('<div')) {
      description = line.trim();
      // Limit to ~60 characters
      if (description.length > 60) {
        description = description.substring(0, 57) + '...';
      }
    }

    // Stop at --- or after getting all info
    if (line.startsWith('---') || (description && traits)) {
      break;
    }
  }

  return { description, traits: traits || '—', requirements: requirements || '—' };
}

heritageFiles.forEach(heritage => {
  const heritageDir = path.join(dotesDir, heritage.slug);

  if (!fs.existsSync(heritageDir)) {
    console.log(`⚠️  No se encontró directorio: ${heritage.slug}`);
    return;
  }

  console.log(`\n🔍 Procesando ${heritage.name}...`);

  // Read all feat files
  const files = fs.readdirSync(heritageDir)
    .filter(f => f.endsWith('.md') && f !== 'dotes_short.md')
    .sort();

  if (files.length === 0) {
    console.log(`  ⚠️  No se encontraron dotes`);
    return;
  }

  // Group feats by level
  const featsByLevel = {};
  files.forEach(file => {
    const filePath = path.join(heritageDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');

    // Extract level from frontmatter
    const levelMatch = content.match(/level:\s*(\d+)/);
    const level = levelMatch ? parseInt(levelMatch[1]) : 1;

    // Extract name from frontmatter
    const nameMatch = content.match(/title:\s*(.+)/);
    const name = nameMatch ? nameMatch[1].trim() : file.replace('.md', '');

    // Extract additional info
    const info = extractFeatInfo(filePath);

    const slug = file.replace('.md', '');

    if (!featsByLevel[level]) {
      featsByLevel[level] = [];
    }

    featsByLevel[level].push({
      name,
      slug,
      level,
      description: info.description,
      traits: info.traits,
      requirements: info.requirements
    });
  });

  // Generate tables by level
  const levels = Object.keys(featsByLevel).map(Number).sort((a, b) => a - b);

  let tablesContent = '';
  levels.forEach(level => {
    tablesContent += `## Nivel ${level}\n\n`;
    tablesContent += `| Dote | Descripción | Rasgos | Requisitos |\n`;
    tablesContent += `|------|-------------|--------|------------|\n`;

    featsByLevel[level].forEach(feat => {
      tablesContent += `| [${feat.name}](/dotes/${heritage.slug}/${feat.slug}/) | ${feat.description} | ${feat.traits} | ${feat.requirements} |\n`;
    });

    tablesContent += `\n`;
  });

  // Generate dotes_short.md with intro text
  const introText = `A 1.er nivel, obtienes una dote de ascendencia y otra adicional cada 4 niveles posteriores (en 5.º, 9.º, 13.º y 17.º nivel). Como ${heritage.name.toLowerCase()}, puedes elegir entre las siguientes dotes de ascendencia.`;

  const dotesShortContent = `---
layout: page
permalink: /ascendencias/herencias-versatiles/${heritage.slug}/dotes_short/
title: "Dotes de Herencia: ${heritage.name}"
chapter: Ascendencias
category: ascendencias
herencia_versatil: ${heritage.name}
---

${introText}

---

${tablesContent}`;

  const dotesShortPath = path.join(heritageDir, 'dotes_short.md');
  fs.writeFileSync(dotesShortPath, dotesShortContent, 'utf-8');
  console.log(`  ✓ Actualizado dotes_short.md con ${files.length} dotes`);
});

console.log('\n✅ Archivos actualizados');
