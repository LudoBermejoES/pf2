#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read files
const basicFile = path.join(__dirname, '../docs/_reglas/acciones-basicas.md');
const specialtyFile = path.join(__dirname, '../docs/_reglas/acciones-especialidad.md');

const basicText = fs.readFileSync(basicFile, 'utf-8');
const specialtyText = fs.readFileSync(specialtyFile, 'utf-8');

// Helper to create slug
const slug = (str) => str
  .toLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/^-+|-+$/g, '');

// Parse actions: split content by ## headers
function extractActions(text) {
  const actions = [];
  const lines = text.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const match = lines[i].match(/^##\s+(.+?)\s+(◆+|↺|◇)\s*$/);
    if (!match) continue;

    const name = match[1].trim();
    const icon = match[2];
    const traits = [];
    const requirements = [];
    let trigger = null;
    const content = [];

    // Collect lines until next ## or ---
    for (i++; i < lines.length; i++) {
      const line = lines[i];

      // Stop conditions
      if (line.startsWith('##') || line === '---') {
        i--; // Back up one since for loop will increment
        break;
      }

      // Parse traits (bold uppercase text like **TRAIT1** **TRAIT2**)
      if (line.match(/^\*\*[A-Z]/)) {
        const boldMatches = line.match(/\*\*([^\*]+)\*\*/g) || [];
        boldMatches.forEach(m => {
          const t = m.replace(/\*\*/g, '').trim();
          if (t && !traits.includes(t)) traits.push(t);
        });
      }

      // Parse Rasgos: line
      if (line.startsWith('**Rasgos:')) {
        const rest = line.replace(/^\*\*Rasgos:\*?\s*/, '').trim();
        const ts = rest.split(',').map(x => x.trim()).filter(x => x);
        ts.forEach(t => {
          if (!traits.includes(t)) traits.push(t);
        });
      }

      // Parse Requisitos
      if (line.startsWith('**Requisitos')) {
        const req = line.replace(/^\*\*Requisitos[:\*]?\s*/, '').trim();
        if (req && !requirements.includes(req)) requirements.push(req);
      }

      // Parse Desencadenante
      if (line.startsWith('**Desencadenante')) {
        trigger = line.replace(/^\*\*Desencadenante[:\*]?\s*/, '').trim();
      }

      // Store content
      content.push(line);
    }

    // Remove leading/trailing empty lines
    while (content.length && !content[0].trim()) content.shift();
    while (content.length && !content[content.length - 1].trim()) content.pop();

    actions.push({
      name,
      icon,
      traits,
      requirements,
      trigger,
      content: content.join('\n')
    });
  }

  return actions;
}

// Extract intro (everything before first ##)
function getIntro(text) {
  const idx = text.search(/^##/m);
  return idx > 0 ? text.substring(0, idx).trim() : '';
}

// Create action files
function createActionFiles(actions, subdir, srcFile) {
  const dir = path.join(__dirname, `../docs/_reglas/${subdir}`);
  fs.mkdirSync(dir, { recursive: true });

  // Re-read original file to get complete action blocks
  const srcContent = fs.readFileSync(srcFile, 'utf-8');
  const srcLines = srcContent.split('\n');

  const slugs = [];

  actions.forEach(action => {
    const s = slug(action.name);
    slugs.push(s);

    // Find full action block in source
    let actionBlock = '';
    let inAction = false;
    for (let i = 0; i < srcLines.length; i++) {
      if (srcLines[i].match(new RegExp(`^##\\s+${action.name.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\$&')}\\s+[◆↺◇]`))) {
        inAction = true;
        actionBlock = srcLines[i] + '\n';
      } else if (inAction) {
        if (srcLines[i].startsWith('##') || srcLines[i] === '---') {
          break;
        }
        actionBlock += srcLines[i] + '\n';
      }
    }

    const fm = `---
layout: page
permalink: /reglas/${subdir}/${s}/
title: ${action.name}
chapter: Como Jugar
category: reglas
---

`;

    const fullContent = fm + actionBlock.trim() + '\n';
    fs.writeFileSync(path.join(dir, `${s}.md`), fullContent, 'utf-8');
    console.log(`✓ ${subdir}/${s}.md`);
  });

  return slugs;
}

// Generate table
function makeTable(actions, slugs, subdir) {
  let result = '| Acción | Tipo | Rasgos | Requisitos |\n';
  result += '|--------|------|--------|------------|\n';

  actions.forEach((action, i) => {
    const link = `[${action.name}]({{ '/reglas/${subdir}/${slugs[i]}/' | relative_url }})`;
    const traits = action.traits.join(', ') || '-';
    const reqs = action.requirements[0] || (action.trigger ? action.trigger : '-');
    result += `| ${link} | ${action.icon} | ${traits} | ${reqs} |\n`;
  });

  return result;
}

// Main
console.log('📚 Extrayendo acciones...\n');

const basicActions = extractActions(basicText);
const specialtyActions = extractActions(specialtyText);

console.log(`Found ${basicActions.length} basic actions`);
console.log(`Found ${specialtyActions.length} specialty actions\n`);

console.log('📝 Creating individual action files:\n');
const basicSlugs = createActionFiles(basicActions, 'acciones-basicas', basicFile);
console.log('');
const specialtySlugs = createActionFiles(specialtyActions, 'acciones-especialidad', specialtyFile);

console.log('\n📄 Updating main files:\n');

// Update basic file
const basicIntro = getIntro(basicText);
const basicTable = makeTable(basicActions, basicSlugs, 'acciones-basicas');
const basicNew = basicIntro + '\n\n## Acciones Básicas\n\n' + basicTable + '\n';
fs.writeFileSync(basicFile, basicNew, 'utf-8');
console.log('✓ acciones-basicas.md (table added)');

// Update specialty file
const specialtyIntro = getIntro(specialtyText);
const specialtyTable = makeTable(specialtyActions, specialtySlugs, 'acciones-especialidad');
const specialtyNew = specialtyIntro + '\n\n## Acciones Básicas de Especialidad\n\n' + specialtyTable + '\n';
fs.writeFileSync(specialtyFile, specialtyNew, 'utf-8');
console.log('✓ acciones-especialidad.md (table added)');

console.log('\n✅ Done!\n');
