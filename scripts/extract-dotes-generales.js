#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const inputFile = '/Users/ludo/code/pf2/docs/_dotes/generales.md';
const outputDir = '/Users/ludo/code/pf2/docs/_dotes/generales';

// Create output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Read the input file
const content = fs.readFileSync(inputFile, 'utf-8');

// Parse the file into feats by splitting on "### " headers (feat names)
const lines = content.split('\n');
let currentLevel = null;
let currentFeat = null;
let currentContent = [];
const feats = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // Detect level headers (## Nivel X)
  if (line.match(/^## Nivel \d+/)) {
    currentLevel = line.match(/^## Nivel (\d+)/)[1];
    continue;
  }

  // Detect feat headers (### Feat Name)
  if (line.match(/^### /)) {
    // Save previous feat if exists
    if (currentFeat) {
      feats.push({
        level: currentLevel,
        name: currentFeat,
        content: currentContent.join('\n').trim()
      });
    }

    // Start new feat
    currentFeat = line.replace(/^### /, '').trim();
    currentContent = [];
  } else if (currentFeat) {
    currentContent.push(line);
  }
}

// Save last feat
if (currentFeat) {
  feats.push({
    level: currentLevel,
    name: currentFeat,
    content: currentContent.join('\n').trim()
  });
}

// Create individual files for each feat
feats.forEach((feat) => {
  // Create slug from name (lowercase, replace spaces and special chars)
  const slug = feat.name
    .toLowerCase()
    .replace(/[↺\s]/g, '-')
    .replace(/--+/g, '-')
    .replace(/^-|-$/g, '')
    .replace(/ó/g, 'o')
    .replace(/á/g, 'a')
    .replace(/é/g, 'e')
    .replace(/í/g, 'i')
    .replace(/ú/g, 'u');

  const fileName = `${slug}.md`;
  const filePath = path.join(outputDir, fileName);

  // Extract traits from content (lines between feat-traits-header divs)
  const traitsMatch = feat.content.match(/<div class="feat-traits-header">([\s\S]*?)<\/div>/);
  let traits = '';
  if (traitsMatch) {
    traits = traitsMatch[1]
      .split('\n')
      .filter(line => line.includes('feat-trait'))
      .map(line => line.replace(/<span class="feat-trait">|<\/span>/g, '').trim())
      .filter(t => t.length > 0)
      .join(', ');
  }

  // Extract prerequisites if any
  const prereqMatch = feat.content.match(/\*\*Prerrequisitos:\*\*\s*(.+?)(?:\n\n|$)/);
  const prerequisites = prereqMatch ? prereqMatch[1].trim() : '';

  // Extract cost if any
  const costMatch = feat.content.match(/\*\*Coste:\*\*\s*(.+?)(?:\n\n|$)/);
  const cost = costMatch ? costMatch[1].trim() : '';

  // Create YAML frontmatter
  const frontmatter = `---
layout: page
permalink: /dotes/generales/${slug}/
title: ${feat.name}
chapter: Dotes
category: dotes
level: ${feat.level}
---`;

  // Create the file content
  const fileContent = `${frontmatter}\n\n${feat.content}`;

  // Write file
  fs.writeFileSync(filePath, fileContent, 'utf-8');
  console.log(`✓ Created: ${fileName}`);
});

console.log(`\nTotal feats extracted: ${feats.length}`);

// Generate index data for table creation
const featsByLevel = {};
feats.forEach((feat) => {
  if (!featsByLevel[feat.level]) {
    featsByLevel[feat.level] = [];
  }

  // Create slug
  const slug = feat.name
    .toLowerCase()
    .replace(/[↺\s]/g, '-')
    .replace(/--+/g, '-')
    .replace(/^-|-$/g, '')
    .replace(/ó/g, 'o')
    .replace(/á/g, 'a')
    .replace(/é/g, 'e')
    .replace(/í/g, 'i')
    .replace(/ú/g, 'u');

  // Extract traits
  const traitsMatch = feat.content.match(/<div class="feat-traits-header">([\s\S]*?)<\/div>/);
  let traits = [];
  if (traitsMatch) {
    traits = traitsMatch[1]
      .split('\n')
      .filter(line => line.includes('feat-trait'))
      .map(line => line.replace(/<span class="feat-trait">|<\/span>/g, '').trim())
      .filter(t => t.length > 0);
  }

  // Extract prerequisites
  const prereqMatch = feat.content.match(/\*\*Prerrequisitos:\*\*\s*(.+?)(?:\n\n|$)/);
  const prerequisites = prereqMatch ? prereqMatch[1].trim() : '';

  // Extract cost
  const costMatch = feat.content.match(/\*\*Coste:\*\*\s*(.+?)(?:\n\n|$)/);
  const cost = costMatch ? costMatch[1].trim() : '';

  // Get first paragraph as description
  const descLines = feat.content.split('\n');
  let description = '';
  for (const line of descLines) {
    if (line.trim() && !line.includes('feat-trait') && !line.includes('<') && !line.includes('**Prerrequi') && !line.includes('**Coste')) {
      description = line.trim();
      break;
    }
  }

  featsByLevel[feat.level].push({
    name: feat.name,
    slug: slug,
    traits: traits,
    prerequisites: prerequisites,
    cost: cost,
    description: description
  });
});

// Output JSON for table generation
console.log('\n--- TABLE DATA ---\n');
console.log(JSON.stringify(featsByLevel, null, 2));
