#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const dotesDir = path.join(__dirname, '../docs/_dotes/arquetipo');
const arquetiposDir = path.join(__dirname, '../docs/_clases/arquetipos');

console.log('📝 Creando dotes_short.md para arquetipos...\n');

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

    if (i === 0 && line === '---') {
      inContent = false;
      continue;
    }
    if (!inContent && line === '---') {
      inContent = true;
      continue;
    }
    if (!inContent) continue;

    if (line.startsWith('##')) {
      foundHeader = true;
      continue;
    }

    if (!foundHeader) continue;

    if (line.includes('feat-traits-header')) {
      const traitMatches = line.matchAll(/class="feat-trait">([^<]+)<\/a>/g);
      const extractedTraits = [];
      for (const match of traitMatches) {
        extractedTraits.push(match[1]);
      }
      traits = extractedTraits.join(', ');
      continue;
    }

    if (line.match(/\*\*(Requisitos?|Prerrequisitos?|Requirements?)/i)) {
      let reqMatch = line.match(/\*\*(Requisitos?|Prerrequisitos?|Requirements?):\*\*\s*(.+)/i);
      if (reqMatch) {
        requirements = reqMatch[2].trim();
      } else {
        reqMatch = line.match(/\*\*(Requisitos?|Prerrequisitos?|Requirements?)\*\*\s+(.+)/i);
        if (reqMatch) {
          requirements = reqMatch[2].trim();
        }
      }
      continue;
    }

    if (!description && line.trim() && !line.startsWith('**') && !line.startsWith('---') && !line.startsWith('<div') && !line.startsWith('*') && !line.includes('include')) {
      description = line.trim();
      if (description.length > 60) {
        description = description.substring(0, 57) + '...';
      }
    }

    if (line.startsWith('---') || (description && traits)) {
      break;
    }
  }

  return { description, traits: traits || '—', requirements: requirements || '—' };
}

function processArchetype(archetypeSlug) {
  const archetypeDotesDir = path.join(dotesDir, archetypeSlug);

  if (!fs.existsSync(archetypeDotesDir)) {
    return null;
  }

  const files = fs.readdirSync(archetypeDotesDir)
    .filter(f => f.endsWith('.md'))
    .sort();

  if (files.length === 0) {
    return null;
  }

  const featsByLevel = {};
  let archetypeName = '';
  let archetypeType = '';

  files.forEach(file => {
    const filePath = path.join(archetypeDotesDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');

    const levelMatch = content.match(/level:\s*(\d+)/);
    const level = levelMatch ? parseInt(levelMatch[1]) : 2;

    const nameMatch = content.match(/title:\s*(.+)/);
    const name = nameMatch ? nameMatch[1].trim() : file.replace('.md', '');

    const archetypeMatch = content.match(/archetype:\s*(.+)/);
    if (archetypeMatch) archetypeName = archetypeMatch[1].trim();

    const typeMatch = content.match(/archetype_type:\s*(.+)/);
    if (typeMatch) archetypeType = typeMatch[1].trim();

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

  const levels = Object.keys(featsByLevel).map(Number).sort((a, b) => a - b);

  let tablesContent = '';
  levels.forEach(level => {
    tablesContent += `## Nivel ${level}\n\n`;
    tablesContent += `| Dote | Descripción | Rasgos | Requisitos |\n`;
    tablesContent += `|------|-------------|--------|------------|\n`;

    featsByLevel[level].forEach(feat => {
      tablesContent += `| [${feat.name}](/dotes/arquetipo/${archetypeSlug}/${feat.slug}/) | ${feat.description} | ${feat.traits} | ${feat.requirements} |\n`;
    });

    tablesContent += `\n`;
  });

  const introText = archetypeType === 'multiclass'
    ? `El arquetipo de ${archetypeName} multiclase te permite obtener algunas de las capacidades de la clase ${archetypeName}. Debes cumplir todos los requisitos antes de seleccionar una dote.`
    : `El arquetipo de ${archetypeName} te otorga acceso a nuevas habilidades y talentos especializados. Debes cumplir todos los requisitos antes de seleccionar una dote.`;

  const dotesShortContent = `---
layout: page
permalink: /clases/arquetipos/${archetypeType === 'multiclass' ? 'multiclase' : 'otros'}/${archetypeSlug}/dotes_short/
title: "Dotes de Arquetipo: ${archetypeName}"
chapter: Clases
category: clases
archetype: ${archetypeName}
archetype_type: ${archetypeType}
---

${introText}

---

${tablesContent}`;

  return { content: dotesShortContent, archetypeName, archetypeType, count: files.length };
}

// Obtener lista de arquetipos
const archetypes = fs.readdirSync(dotesDir).filter(f => {
  const fullPath = path.join(dotesDir, f);
  return fs.statSync(fullPath).isDirectory();
});

console.log(`🔍 Procesando ${archetypes.length} arquetipos...\n`);

let totalCreated = 0;

archetypes.forEach(archetypeSlug => {
  const result = processArchetype(archetypeSlug);

  if (result) {
    // Determinar directorio de destino
    const targetDir = result.archetypeType === 'multiclass'
      ? path.join(arquetiposDir, 'multiclase', archetypeSlug)
      : path.join(arquetiposDir, 'pc2', archetypeSlug);

    // Crear directorio si no existe
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }

    // Escribir archivo dotes_short.md
    const dotesShortPath = path.join(targetDir, 'dotes_short.md');
    fs.writeFileSync(dotesShortPath, result.content, 'utf-8');

    console.log(`  ✓ ${result.archetypeName}: ${result.count} dotes`);
    totalCreated++;
  }
});

console.log(`\n✅ Creadas ${totalCreated} tablas dotes_short.md para arquetipos`);
