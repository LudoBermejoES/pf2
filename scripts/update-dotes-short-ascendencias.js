#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const dotesDir = path.join(__dirname, '../docs/_dotes');
const ascendenciasDir = path.join(__dirname, '../docs/_ascendencias');

console.log('📝 Actualizando dotes_short.md de ascendencias...\n');

const ancestries = [
  'catfolk', 'elfo', 'enano', 'gnomo', 'goblin', 'hobgoblin',
  'hombres-lagarto', 'humano', 'kholo', 'kobold', 'leshy',
  'mediano', 'orco', 'ratfolk', 'tengu', 'tripkee'
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

    // Extract requirements
    if (line.match(/\*\*(Requisitos?|Prerrequisitos?|Requirements?):/i)) {
      const reqMatch = line.match(/\*\*(Requisitos?|Prerrequisitos?|Requirements?):\*\*\s*(.+)/i);
      if (reqMatch) {
        requirements = reqMatch[2].trim();
      }
      continue;
    }

    // Extract description (first non-empty paragraph that's not a special section)
    if (!description && line.trim() && !line.startsWith('**') && !line.startsWith('---') && !line.startsWith('<div') && !line.startsWith('*') && !line.includes('include')) {
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

ancestries.forEach(ancestry => {
  const dotesAncestryDir = path.join(dotesDir, ancestry);
  const ascendenciasAncestryDir = path.join(ascendenciasDir, ancestry);

  if (!fs.existsSync(dotesAncestryDir)) {
    console.log(`⚠️  No se encontró directorio de dotes: ${ancestry}`);
    return;
  }

  if (!fs.existsSync(ascendenciasAncestryDir)) {
    console.log(`⚠️  No se encontró directorio de ascendencia: ${ancestry}`);
    return;
  }

  console.log(`\n🔍 Procesando ${ancestry}...`);

  // Read all feat files
  const files = fs.readdirSync(dotesAncestryDir)
    .filter(f => f.endsWith('.md') && f !== 'dotes_short.md')
    .sort();

  if (files.length === 0) {
    console.log(`  ⚠️  No se encontraron dotes`);
    return;
  }

  // Group feats by level
  const featsByLevel = {};
  files.forEach(file => {
    const filePath = path.join(dotesAncestryDir, file);
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
      tablesContent += `| [${feat.name}](/dotes/${ancestry}/${feat.slug}/) | ${feat.description} | ${feat.traits} | ${feat.requirements} |\n`;
    });

    tablesContent += `\n`;
  });

  // Read existing dotes_short.md to preserve frontmatter
  const dotesShortPath = path.join(ascendenciasAncestryDir, 'dotes_short.md');
  let existingContent = '';
  let frontmatter = {};

  if (fs.existsSync(dotesShortPath)) {
    existingContent = fs.readFileSync(dotesShortPath, 'utf-8');
    const frontmatterMatch = existingContent.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      const frontmatterText = frontmatterMatch[1];
      frontmatterText.split('\n').forEach(line => {
        const match = line.match(/^(\w+):\s*(.+)/);
        if (match) {
          frontmatter[match[1]] = match[2];
        }
      });
    }
  }

  // Generate intro text
  const ancestryName = ancestry.charAt(0).toUpperCase() + ancestry.slice(1);
  const introText = `A 1.er nivel, obtienes una dote de ascendencia y otra adicional cada 4 niveles posteriores (en 5.º, 9.º, 13.º y 17.º nivel). Como ${ancestry}, puedes elegir entre las siguientes dotes de ascendencia.`;

  // Preserve existing frontmatter or create new
  const frontmatterText = Object.keys(frontmatter).length > 0
    ? Object.entries(frontmatter).map(([key, value]) => `${key}: ${value}`).join('\n')
    : `layout: page
permalink: /ascendencias/${ancestry}/dotes_short/
title: "Dotes de Ascendencia: ${ancestryName}"
chapter: Ascendencias
category: ascendencias
ancestry: ${ancestryName}`;

  const dotesShortContent = `---
${frontmatterText}
---

${introText}

---

${tablesContent}`;

  fs.writeFileSync(dotesShortPath, dotesShortContent, 'utf-8');
  console.log(`  ✓ Actualizado dotes_short.md con ${files.length} dotes en ${levels.length} niveles`);
});

console.log('\n✅ Archivos actualizados');
