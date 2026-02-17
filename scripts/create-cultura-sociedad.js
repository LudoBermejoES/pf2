#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ancestriesDir = path.join(__dirname, '../docs/_ascendencias');

console.log('📚 Creando archivos cultura-sociedad.md para ascendencias...\n');

// List of ancestries to process
const ancestriesToProcess = [
  'catfolk',
  'kholo',
  'kobold',
  'ratfolk',
  'tengu',
  'tripkee'
];

let createdCount = 0;

ancestriesToProcess.forEach(ancestryDir => {
  const indexPath = path.join(ancestriesDir, ancestryDir, 'index.md');
  const culturaPath = path.join(ancestriesDir, ancestryDir, 'cultura-sociedad.md');

  if (!fs.existsSync(indexPath)) {
    console.log(`⚠️  No se encontró: ${ancestryDir}/index.md`);
    return;
  }

  if (fs.existsSync(culturaPath)) {
    console.log(`⏭️  Ya existe: ${ancestryDir}/cultura-sociedad.md`);
    return;
  }

  // Read index.md
  const content = fs.readFileSync(indexPath, 'utf-8');
  const lines = content.split('\n');

  // Extract frontmatter
  let i = 0;
  const frontmatterLines = [];
  if (lines[0] === '---') {
    frontmatterLines.push(lines[0]);
    i = 1;
    while (i < lines.length && lines[i] !== '---') {
      frontmatterLines.push(lines[i]);
      i++;
    }
    if (i < lines.length) {
      frontmatterLines.push(lines[i]);
      i++;
    }
  }

  // Extract ancestry name from frontmatter
  const titleMatch = frontmatterLines.find(l => l.startsWith('title:'));
  const ancestryName = titleMatch ? titleMatch.replace('title:', '').trim() : ancestryDir;

  const sourceMatch = frontmatterLines.find(l => l.startsWith('source:'));
  const source = sourceMatch ? sourceMatch.replace('source:', '').trim() : 'PC2';

  // Find sections to extract
  const sectionsToExtract = [
    'Descripción física',
    'Sociedad',
    'Nombres',
    'Creencias'
  ];

  const extractedSections = [];
  let currentSection = null;
  let sectionContent = [];

  for (let j = i; j < lines.length; j++) {
    const line = lines[j];

    // Check for section headers
    const sectionMatch = line.match(/^##\s+(.+)$/);
    if (sectionMatch) {
      const sectionTitle = sectionMatch[1];

      // Save previous section if it's one we want
      if (currentSection && sectionsToExtract.includes(currentSection)) {
        extractedSections.push({
          title: currentSection,
          content: sectionContent.join('\n').trim()
        });
      }

      // Start new section
      if (sectionsToExtract.includes(sectionTitle)) {
        currentSection = sectionTitle;
        sectionContent = [line];
      } else {
        currentSection = null;
        sectionContent = [];
      }
    } else if (currentSection) {
      sectionContent.push(line);
    }
  }

  // Save last section
  if (currentSection && sectionsToExtract.includes(currentSection)) {
    extractedSections.push({
      title: currentSection,
      content: sectionContent.join('\n').trim()
    });
  }

  // Create cultura-sociedad.md
  const newFrontmatter = `---
layout: page
permalink: /ascendencias/${ancestryDir}/cultura-sociedad/
title: Cultura y Sociedad de ${ancestryName}
chapter: Ascendencias
category: ascendencias
nav_order: 2
ancestry: ${ancestryName}
source: ${source}
---
`;

  const sectionContents = extractedSections.map(s => s.content).join('\n\n---\n\n');

  const newContent = newFrontmatter + '\n' + sectionContents + '\n';

  fs.writeFileSync(culturaPath, newContent, 'utf-8');
  console.log(`✓ Creado: ${ancestryDir}/cultura-sociedad.md`);
  createdCount++;

  // Update index.md to add link
  const updatedIndexContent = content.replace(
    /(- \[Herencias\].*?\n)/,
    '$1- [Cultura y Sociedad]({{ \'/ascendencias/' + ancestryDir + '/cultura-sociedad/\' | relative_url }})\n'
  );

  if (updatedIndexContent !== content) {
    fs.writeFileSync(indexPath, updatedIndexContent, 'utf-8');
    console.log(`  ✓ Actualizado: ${ancestryDir}/index.md`);
  }
});

console.log(`\n✅ ${createdCount} archivos creados`);
