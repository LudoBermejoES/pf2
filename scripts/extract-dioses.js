#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Read the religion file
const religionPath = path.join(__dirname, '../docs/_introduccion/religion.md');
const content = fs.readFileSync(religionPath, 'utf-8');

// Extract the gods section (from "## Dioses principales" to "## Santificacion")
const godsSectionMatch = content.match(/## Dioses principales\n\n([\s\S]*?)(?=## Santificacion)/);
if (!godsSectionMatch) {
  console.error('Could not find gods section');
  process.exit(1);
}

const godsSection = godsSectionMatch[1];

// Extract each god using regex
const godRegex = /### ([^\n]+)\n\n\*\*([^\*]+)\*\*\n\n([\s\S]*?)(?=(?:^### |\n---\n$))/gm;

const gods = [];
let match;

while ((match = godRegex.exec(godsSection)) !== null) {
  const name = match[1].trim();
  const title = match[2].trim();
  const fullContent = match[3].trim();

  // Extract the description and deity benefits separately
  const descriptionMatch = fullContent.match(/([\s\S]*?)(?=\n- \*\*Areas de interes)/);
  const description = descriptionMatch ? descriptionMatch[1].trim() : '';

  gods.push({
    name,
    title,
    description,
    fullContent
  });
}

console.log(`Found ${gods.length} gods`);

// Create dioses folder if it doesn't exist
const diosesDir = path.join(__dirname, '../docs/_introduccion/dioses');
if (!fs.existsSync(diosesDir)) {
  fs.mkdirSync(diosesDir, { recursive: true });
  console.log(`Created directory: ${diosesDir}`);
}

// Function to create slug from name
function createSlug(name) {
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove accents
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Create individual god files
gods.forEach((god, index) => {
  const slug = createSlug(god.name);
  const filePath = path.join(diosesDir, `${slug}.md`);

  const frontmatter = `---
layout: page
permalink: /introduccion/dioses/${slug}/
title: ${god.name}
subtitle: ${god.title}
chapter: Introducción
category: introduccion
nav_order: ${index + 1}
parent: Religion
grand_parent: Introducción
---

`;

  const fileContent = frontmatter + god.fullContent;

  fs.writeFileSync(filePath, fileContent, 'utf-8');
  console.log(`Created: ${filePath}`);
});

// Generate table markdown for religion.md
let tableMarkdown = '\n## Dioses principales\n\n| Dios | Epíteto | Descripción |\n|-----|---------|-------------|\n';

gods.forEach((god) => {
  const slug = createSlug(god.name);
  const shortDesc = god.description.split('\n')[0].substring(0, 100) + '...';
  tableMarkdown += `| [${god.name}](/introduccion/dioses/${slug}/) | ${god.title} | ${shortDesc.replace(/\|/g, '\\|')} |\n`;
});

// Read the full religion.md file
const religionContent = fs.readFileSync(religionPath, 'utf-8');

// Replace the gods section with the table
const newContent = religionContent
  .replace(
    /## Dioses principales\n\n([\s\S]*?)(?=## Santificacion)/,
    tableMarkdown + '\n## Santificacion'
  );

fs.writeFileSync(religionPath, newContent, 'utf-8');
console.log(`Updated: ${religionPath}`);

console.log(`\n✅ Extraction complete! Created ${gods.length} god files.`);
