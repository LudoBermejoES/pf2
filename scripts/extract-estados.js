#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read both estado files
const estadosAEPath = path.join(__dirname, '../docs/_apendices/estados-a-e.md');
const estadosFZPath = path.join(__dirname, '../docs/_apendices/estados-f-z.md');

const estadosAEContent = fs.readFileSync(estadosAEPath, 'utf-8');
const estadosFZContent = fs.readFileSync(estadosFZPath, 'utf-8');

// Combine both files
const allContent = estadosAEContent + '\n' + estadosFZContent;

// Create output directory
const outputDir = path.join(__dirname, '../docs/_apendices/estados');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Extract header content (before "# Lista de estados")
const headerMatch = allContent.match(/^([\s\S]*?)# Lista de estados/);
const headerContent = headerMatch ? headerMatch[1] : '';

// Extract all state definitions using regex
// Matches ## Estado Name and everything until the next ## or EOF
const stateRegex = /## ([^\n]+)\n\n([\s\S]*?)(?=## [^\n]+\n\n|$)/g;
const states = [];
let match;

while ((match = stateRegex.exec(allContent)) !== null) {
  const name = match[1].trim();
  const content = match[2].trim();
  states.push({ name, content });
}

// Filter out non-state entries (like "Valores de estado", "Estados prevalentes", etc.)
const skipPatterns = [
  'Valores de estado',
  'Estados prevalentes',
  'Lista de estados',
  'Grupos de estados',
  'Reglas de muerte',
  'Ganar y perder acciones',
  'Estados redundantes'
];

const filteredStates = states.filter(
  s => !skipPatterns.some(p => s.name.includes(p))
);

console.log(`Found ${filteredStates.length} states to extract`);

// Create slug from state name
function slugify(name) {
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/á/g, 'a')
    .replace(/é/g, 'e')
    .replace(/í/g, 'i')
    .replace(/ó/g, 'o')
    .replace(/ú/g, 'u')
    .replace(/ñ/g, 'n')
    .replace(/\s+/g, '-')
    .replace(/[^\w-]/g, '');
}

// Get first line of content (for table description)
function getFirstLine(content) {
  const lines = content.split('\n');
  return lines[0]?.replace(/^[*_]+|[*_]+$/g, '').substring(0, 100) || '';
}

// Create individual state files
filteredStates.forEach((state, index) => {
  const slug = slugify(state.name);
  const filePath = path.join(outputDir, `${slug}.md`);

  const frontmatter = `---
layout: page
permalink: /apendices/estados/${slug}/
title: ${state.name}
chapter: Apéndices
category: apéndices
nav_order: ${index + 1}
parent: Estados
grand_parent: Apéndices
---

`;

  const fileContent = frontmatter + state.content + '\n';

  fs.writeFileSync(filePath, fileContent, 'utf-8');
  console.log(`✓ Created: ${slug}.md`);
});

// Create states index file (renamed from estados-a-e.md)
const stateTable = filteredStates
  .map(state => {
    const slug = slugify(state.name);
    const description = getFirstLine(state.content);
    return `| [${state.name}](/apendices/estados/${slug}/) | ${description} |`;
  })
  .join('\n');

const indexContent = `---
layout: page
permalink: /apendices/estados/
title: Estados
chapter: Apéndices
category: apéndices
nav_order: 8
---

${headerContent}
---

## Índice de estados

| Estado | Descripción |
|--------|-------------|
${stateTable}
`;

const indexPath = path.join(path.dirname(outputDir), 'estados.md');
fs.writeFileSync(indexPath, indexContent, 'utf-8');
console.log(`✓ Created: estados.md (index)`);

console.log('\nExtraction complete!');
console.log(`Total states extracted: ${filteredStates.length}`);
console.log(`Output directory: ${outputDir}`);
console.log(`Index file: ${indexPath}`);
