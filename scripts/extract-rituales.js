#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read the rituales file
const ritualFilePath = path.join(__dirname, '../docs/_conjuros/rituales/rituales.md');
const content = fs.readFileSync(ritualFilePath, 'utf-8');

// Directory for individual ritual files
const ritualsDir = path.join(__dirname, '../docs/_conjuros/rituales');

// Parse rituals from the file
// Each ritual starts with "## Ritual Name [RITUAL X]" and ends with "---" or at the next ritual
const ritualPattern = /## (.+?)\s*\[RITUAL\s+(\d+)\]([\s\S]*?)(?=^---$|^## (?=.+\[RITUAL|$))/gm;

const rituals = [];
let match;

while ((match = ritualPattern.exec(content)) !== null) {
  const name = match[1].trim();
  const rank = parseInt(match[2]);
  const fullContent = match[0];

  // Extract traits
  const traitsMatch = fullContent.match(/\*\*Rasgos:\*\*\s*([^\n]+)/);
  const traits = traitsMatch ? traitsMatch[1].trim() : '';

  // Create slug from name
  const slug = name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

  rituals.push({
    name,
    rank,
    slug,
    traits,
    content: fullContent
  });
}

console.log(`Found ${rituals.length} rituals`);

// Create individual files for each ritual
rituals.forEach(ritual => {
  const filename = `${ritual.slug}.md`;
  const filepath = path.join(ritualsDir, filename);

  const frontmatter = `---
layout: page
permalink: /conjuros/rituales/${ritual.slug}/
title: ${ritual.name}
chapter: Conjuros
category: conjuros
ritual_rank: ${ritual.rank}
---

`;

  const fileContent = frontmatter + ritual.content;

  fs.writeFileSync(filepath, fileContent, 'utf-8');
  console.log(`Created: ${filename}`);
});

// Now update the main rituales.md file with links
const headerContent = content.substring(0, content.indexOf('## Rituales por Rango'));
const tableStart = content.indexOf('| Rango | Ritual |');
const tableEnd = content.indexOf('\n\n## Como Aprender');

const oldTable = content.substring(tableStart, tableEnd);

// Parse old table rows
const oldRows = oldTable.split('\n').slice(2, -1).filter(line => line.trim().startsWith('|'));

// Create new table
let newTable = '| Rango | Ritual | Descripción | Rasgos |\n';
newTable += '|-------|--------|-------------|--------|\n';

// Map of ritual descriptions
const descriptions = {
  'animar-objeto': 'Transforma un objeto en una criatura animada bajo tu control.',
  'asolar': 'Marchita las plantas de una zona grande, reduciendo las cosechas.',
  'circulo-de-ligadura': 'Llama a una criatura extraplanar y negocia un trato con ella.',
  'comunion': 'Contacta con seres poderosos para que respondan a tus preguntas.',
  'consagrar': 'Consagra un lugar a tu dios con efectos beneficiosos para sus adoradores.',
  'controlar-el-clima': 'Altera el clima y los fenómenos meteorológicos de una amplia zona.',
  'crear-muerto-viviente': 'Transforma un cadáver en una criatura no-muerta.',
  'crecimiento-vegetal': 'Enriquece las plantas de una zona, aumentando las cosechas.',
  'deseo': 'Conjuro supremo que altera la realidad para conceder un deseo.',
  'desplazamiento-planario': 'Transporta criaturas a un plano de existencia diferente.',
  'dotar-de-consciencia-a-un-animal': 'Concede inteligencia humanoide a un animal.',
  'expiar': 'Ayuda a una criatura arrepentida a expiar sus transgresiones.',
  'geas': 'Impone una obligación mágica a una criatura voluntaria.',
  'llamada-primigenia': 'Llama a un animal, hada o planta a distancia.',
  'llamar-a-un-espiritu': 'Contacta con el espíritu de un difunto para hacer preguntas.',
  'recuerdos-colectivos': 'Sondea los recuerdos compartidos de la humanidad sobre un tema.',
  'resucitar': 'Devuelve la vida a una criatura muerta hace poco tiempo.',
  'servidor-planario': 'Llama a un servidor divino para que te ayude en una tarea.',
  'trampa-runica': 'Crea una trampa mágica que lanza un conjuro al ser activada.'
};

rituals.forEach(ritual => {
  const slug = ritual.slug;
  const description = descriptions[slug] || 'Poderoso ritual de magia arcana.';
  const link = `[${ritual.name}]({{ '/conjuros/rituales/${slug}/' | relative_url }})`;

  newTable += `| ${ritual.rank} | ${link} | ${description} | ${ritual.traits} |\n`;
});

// Reconstruct the file
const contentAfterTable = content.substring(tableEnd);
const newContent = headerContent +
  '## Rituales por Rango\n\n' +
  newTable +
  contentAfterTable;

fs.writeFileSync(ritualFilePath, newContent, 'utf-8');
console.log('\nUpdated main rituales.md file with links and descriptions');
console.log('Done!');
