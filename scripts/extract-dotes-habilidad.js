#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const inputFile = '/Users/ludo/code/pf2/docs/_dotes/habilidad.md';
const outputDir = '/Users/ludo/code/pf2/docs/_dotes/habilidad';

// Create output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Read the input file
const content = fs.readFileSync(inputFile, 'utf-8');
const lines = content.split('\n');

const feats = [];
let currentAbility = null;
let currentLevel = 1;
let i = 0;

// Skip intro and general header
while (i < lines.length && !lines[i].match(/^## Dotes de Habilidad Generales/)) {
  i++;
}

// Parse from "Dotes de Habilidad Generales" onwards
while (i < lines.length) {
  const line = lines[i];

  // Detect ability headers (## Ability Name)
  if (line.match(/^## [A-Z]/i) && !line.includes('Nivel')) {
    currentAbility = line.replace(/^## /, '').trim();
    i++;
    continue;
  }

  // Detect level headers (### Nivel X)
  if (line.match(/^### Nivel \d+/)) {
    currentLevel = parseInt(line.match(/^### Nivel (\d+)/)[1]);
    i++;
    continue;
  }

  // Detect feat headers (#### Feat Name)
  if (line.match(/^#### /)) {
    const featName = line.replace(/^#### /, '').trim();
    const featContent = [];
    i++;

    // Collect all lines until next feat or section
    while (i < lines.length && !lines[i].match(/^(####|###|##) /)) {
      featContent.push(lines[i]);
      i++;
    }

    feats.push({
      name: featName,
      ability: currentAbility,
      level: currentLevel,
      content: featContent.join('\n').trim()
    });
    continue;
  }

  i++;
}

console.log(`Found ${feats.length} feats`);

// Create individual files for each feat
feats.forEach((feat) => {
  // Create slug from name
  const slug = feat.name
    .toLowerCase()
    .replace(/[↺◆]/g, '')
    .replace(/\s+/g, '-')
    .replace(/--+/g, '-')
    .replace(/^-|-$/g, '')
    .replace(/ó/g, 'o')
    .replace(/á/g, 'a')
    .replace(/é/g, 'e')
    .replace(/í/g, 'i')
    .replace(/ú/g, 'u')
    .replace(/ñ/g, 'n');

  const fileName = `${slug}.md`;
  const filePath = path.join(outputDir, fileName);

  // Create YAML frontmatter
  const frontmatter = `---
layout: page
permalink: /dotes/habilidad/${slug}/
title: ${feat.name}
chapter: Dotes
category: dotes
habilidad: ${feat.ability}
level: ${feat.level}
---`;

  // Create the file content
  const fileContent = `${frontmatter}\n\n${feat.content}`;

  // Write file
  fs.writeFileSync(filePath, fileContent, 'utf-8');
  console.log(`✓ Created: ${fileName}`);
});

console.log(`\nTotal feats extracted: ${feats.length}`);

// Generate data for table by grouping feats
const featsByAbility = {};

feats.forEach((feat) => {
  if (!featsByAbility[feat.ability]) {
    featsByAbility[feat.ability] = [];
  }

  // Create slug
  const slug = feat.name
    .toLowerCase()
    .replace(/[↺◆]/g, '')
    .replace(/\s+/g, '-')
    .replace(/--+/g, '-')
    .replace(/^-|-$/g, '')
    .replace(/ó/g, 'o')
    .replace(/á/g, 'a')
    .replace(/é/g, 'e')
    .replace(/í/g, 'i')
    .replace(/ú/g, 'u')
    .replace(/ñ/g, 'n');

  // Extract traits
  const traitsMatch = feat.content.match(/<div class="feat-traits-header"[^>]*>([\s\S]*?)<\/div>/);
  let traits = [];
  if (traitsMatch) {
    traits = traitsMatch[1]
      .split('\n')
      .filter(line => line.includes('feat-trait'))
      .map(line => line.replace(/<span class="feat-trait">|<\/span>/g, '').trim())
      .filter(t => t.length > 0);
  }

  // Extract prerequisites
  const prereqMatch = feat.content.match(/\*\*Prerrequisitos?:\*\*\s*(.+?)(?:\n\n|$)/);
  const prerequisites = prereqMatch ? prereqMatch[1].trim() : '';

  featsByAbility[feat.ability].push({
    name: feat.name,
    slug: slug,
    level: feat.level,
    traits: traits,
    prerequisites: prerequisites
  });
});

// Output JSON for table generation
console.log('\n--- TABLE DATA ---\n');
console.log(JSON.stringify(featsByAbility, null, 2));
