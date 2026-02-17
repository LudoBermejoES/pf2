#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const dotesDir = path.join(__dirname, '../docs/_dotes');
const clasesDir = path.join(__dirname, '../docs/_clases');

console.log('📝 Actualizando dotes_short.md de clases...\n');

const classes = [
  'alquimista', 'barbaro', 'bardo', 'brujo', 'campeon', 'clerigo',
  'druida', 'espadachin', 'explorador', 'guerrero', 'hechicero',
  'investigador', 'mago', 'monje', 'oraculo', 'picaro'
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

classes.forEach(className => {
  const dotesClassDir = path.join(dotesDir, className);
  const clasesClassDir = path.join(clasesDir, className);

  if (!fs.existsSync(dotesClassDir)) {
    console.log(`⚠️  No se encontró directorio de dotes: ${className}`);
    return;
  }

  if (!fs.existsSync(clasesClassDir)) {
    console.log(`⚠️  No se encontró directorio de clase: ${className}`);
    return;
  }

  console.log(`\n🔍 Procesando ${className}...`);

  // Read all feat files
  const files = fs.readdirSync(dotesClassDir)
    .filter(f => f.endsWith('.md') && f !== 'dotes_short.md')
    .sort();

  if (files.length === 0) {
    console.log(`  ⚠️  No se encontraron dotes`);
    return;
  }

  // Group feats by level
  const featsByLevel = {};
  files.forEach(file => {
    const filePath = path.join(dotesClassDir, file);
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
      tablesContent += `| [${feat.name}](/dotes/${className}/${feat.slug}/) | ${feat.description} | ${feat.traits} | ${feat.requirements} |\n`;
    });

    tablesContent += `\n`;
  });

  // Read existing dotes_short.md to preserve frontmatter
  const dotesShortPath = path.join(clasesClassDir, 'dotes_short.md');
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
  const introText = `En cada nivel en el que obtienes una dote de ${className}, puedes seleccionar una de las siguientes. Debes cumplir todos los requisitos antes de seleccionarla.`;

  // Preserve existing frontmatter or create new
  const frontmatterText = Object.keys(frontmatter).length > 0
    ? Object.entries(frontmatter).map(([key, value]) => `${key}: ${value}`).join('\n')
    : `layout: page
permalink: /clases/${className}/dotes_short/
title: Dotes de ${className.charAt(0).toUpperCase() + className.slice(1)}
chapter: Clases
category: clases
class_name: ${className.charAt(0).toUpperCase() + className.slice(1)}`;

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
