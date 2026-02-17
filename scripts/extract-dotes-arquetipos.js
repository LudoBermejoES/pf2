#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('📝 Extrayendo dotes de arquetipos...\n');

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function extractFeatsFromArchetype(filePath, archetypeName, archetypeType) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  const feats = [];
  let currentFeat = null;
  let inFeat = false;
  let featContent = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Detectar inicio de dote: ### Nombre de dote · Dote X o ### Nombre de dote - Dote X
    const featMatch = line.match(/^###\s+(.+?)\s+[·\-]\s+Dote\s+(\d+)/);

    if (featMatch) {
      // Guardar dote anterior si existe
      if (currentFeat && featContent.length > 0) {
        currentFeat.content = featContent.join('\n').trim();
        feats.push(currentFeat);
      }

      // Iniciar nueva dote
      const featName = featMatch[1].trim();
      const level = parseInt(featMatch[2]);

      currentFeat = {
        name: featName,
        slug: slugify(featName),
        level: level,
        archetype: archetypeName,
        archetypeSlug: slugify(archetypeName),
        archetypeType: archetypeType
      };

      featContent = [];
      inFeat = true;
      continue;
    }

    // Detectar fin de dote (nueva sección ### o ---)
    if (inFeat && (line.startsWith('### ') || line.startsWith('---'))) {
      if (currentFeat && featContent.length > 0) {
        currentFeat.content = featContent.join('\n').trim();
        feats.push(currentFeat);
      }
      currentFeat = null;
      inFeat = false;
      featContent = [];
    }

    // Acumular contenido de la dote
    if (inFeat) {
      featContent.push(line);
    }
  }

  // Guardar última dote si existe
  if (currentFeat && featContent.length > 0) {
    currentFeat.content = featContent.join('\n').trim();
    feats.push(currentFeat);
  }

  return feats;
}

function createFeatFile(feat, outputDir) {
  const featDir = path.join(outputDir, feat.archetypeSlug);

  if (!fs.existsSync(featDir)) {
    fs.mkdirSync(featDir, { recursive: true });
  }

  const frontmatter = `---
layout: page
permalink: /dotes/arquetipo/${feat.archetypeSlug}/${feat.slug}/
title: ${feat.name}
chapter: Dotes
category: dotes
archetype: ${feat.archetype}
archetype_type: ${feat.archetypeType}
level: ${feat.level}
---

`;

  const fullContent = frontmatter + `## ${feat.name}\n\n` + feat.content + '\n\n---\n';

  const featPath = path.join(featDir, `${feat.slug}.md`);
  fs.writeFileSync(featPath, fullContent, 'utf-8');
}

function processArchetypeDirectory(directory, archetypeType) {
  const dirPath = path.join(__dirname, '..', 'docs', '_clases', 'arquetipos', directory);

  if (!fs.existsSync(dirPath)) {
    console.log(`  ⚠️  Directorio no existe: ${directory}`);
    return;
  }

  const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.md') && f !== 'index.md' && f !== 'introduccion.md' && f !== 'arquetipos-multiclase.md');

  console.log(`\n📁 Procesando ${files.length} arquetipos de ${directory}...\n`);

  const outputDir = path.join(__dirname, '..', 'docs', '_dotes', 'arquetipo');
  let totalFeats = 0;

  files.forEach(file => {
    const filePath = path.join(dirPath, file);
    const archetypeName = file.replace('.md', '').replace(/-/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');

    const feats = extractFeatsFromArchetype(filePath, archetypeName, archetypeType);

    if (feats.length > 0) {
      feats.forEach(feat => {
        createFeatFile(feat, outputDir);
      });

      console.log(`  ✓ ${archetypeName}: ${feats.length} dotes extraídas`);
      totalFeats += feats.length;
    }
  });

  console.log(`\n  Total: ${totalFeats} dotes extraídas de ${directory}`);
}

// Procesar arquetipos PC2
processArchetypeDirectory('pc2', 'other');

// Procesar arquetipos multiclase
processArchetypeDirectory('multiclase', 'multiclass');

console.log('\n✅ Extracción completada');
