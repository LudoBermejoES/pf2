#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const basicPath = path.join(__dirname, '../docs/_reglas/acciones-basicas.md');
const specialtyPath = path.join(__dirname, '../docs/_reglas/acciones-especialidad.md');

let basicContent = fs.readFileSync(basicPath, 'utf-8');
let specialtyContent = fs.readFileSync(specialtyPath, 'utf-8');

// Extract frontmatter
function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n/);
  return match ? match[1] : '';
}

// Extract intro text (everything before first action)
function extractIntro(content) {
  const actionStart = content.search(/^##\s+\w/m);
  if (actionStart === -1) return content;
  return content.substring(0, actionStart).trim();
}

// Parse individual actions
function parseActions(content) {
  const actions = [];
  // Split by ## headers at line start
  const parts = content.split(/\n(?=^##\s)/m);

  for (const part of parts) {
    if (!part.trim().startsWith('##')) continue;

    const lines = part.split('\n');
    const headerLine = lines[0];

    // Parse: ## Name Icon(s)
    const match = headerLine.match(/^##\s+(.+?)\s+(◆+|↺|◇)(.*)$/);
    if (!match) continue;

    const name = match[1].trim();
    const icon = match[2];
    const traits = [];
    const requirements = [];
    let trigger = null;

    // Parse rest of lines for metadata
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i];

      // Stop at next section or separator
      if (line.startsWith('##') || line === '---') break;

      // Parse traits - multiple patterns
      if (line.match(/^\*\*[A-Z]/)) {
        // **TRAIT** **TRAIT** format
        const matches = line.match(/\*\*([A-Z][A-Z\s]+?)\*\*/g);
        if (matches) {
          matches.forEach(m => {
            const t = m.replace(/\*\*/g, '').trim();
            if (!traits.includes(t)) traits.push(t);
          });
        }

        // **Rasgos:** trait1, trait2 format
        if (line.includes('Rasgos:')) {
          const traitsStr = line.replace(/^\*\*Rasgos:\*\*\s*/, '').trim();
          const ts = traitsStr.split(',').map(x => x.trim()).filter(x => x);
          ts.forEach(t => {
            if (!traits.includes(t)) traits.push(t);
          });
        }
      }

      // Parse requisites
      if (line.match(/^\*\*Requisitos/i)) {
        const req = line.replace(/^\*\*Requisitos[:\*]*/i, '').trim();
        if (req && !requirements.includes(req)) requirements.push(req);
      }

      // Parse trigger
      if (line.match(/^\*\*Desencadenante/i)) {
        trigger = line.replace(/^\*\*Desencadenante[:\*]*/i, '').trim();
      }
    }

    actions.push({ name, icon, traits, requirements, trigger });
  }

  return actions;
}

// Create slug
function slug(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Extract and create files
const basicActions = parseActions(basicContent);
const specialtyActions = parseActions(specialtyContent);

console.log(`✓ Found ${basicActions.length} basic actions`);
console.log(`✓ Found ${specialtyActions.length} specialty actions`);

// Helper: Create action files
function createFiles(actions, subdir) {
  const dir = path.join(__dirname, `../docs/_reglas/${subdir}`);
  fs.mkdirSync(dir, { recursive: true });

  const slugs = [];
  actions.forEach(action => {
    const s = slug(action.name);
    slugs.push(s);

    // Extract from original file
    const origPath = subdir === 'acciones-basicas' ? basicPath : specialtyPath;
    const origContent = fs.readFileSync(origPath, 'utf-8');

    // Find the action content in original file
    const regex = new RegExp(`^## ${action.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s+[◆↺◇]([\\s\\S]*?)(?=^##|^---|$)`, 'm');
    const match = origContent.match(regex);
    let actionContent = match ? match[0] : `## ${action.name} ${action.icon}\n`;

    const fm = `---
layout: page
permalink: /reglas/${subdir}/${s}/
title: ${action.name}
chapter: Como Jugar
category: reglas
---

`;

    fs.writeFileSync(
      path.join(dir, `${s}.md`),
      fm + actionContent.trim() + '\n',
      'utf-8'
    );
    console.log(`  ✓ ${subdir}/${s}.md`);
  });

  return slugs;
}

console.log('\n📝 Creating individual action files:\n');
const basicSlugs = createFiles(basicActions, 'acciones-basicas');
console.log('');
const specialtySlugs = createFiles(specialtyActions, 'acciones-especialidad');

// Helper: Generate table
function makeTable(actions, slugs, subdir) {
  let table = '| Acción | Tipo | Rasgos | Requisitos |\n';
  table += '|--------|------|--------|------------|\n';

  actions.forEach((action, i) => {
    const link = `[${action.name}]({{ '/reglas/${subdir}/${slugs[i]}/' | relative_url }})`;
    const traits = action.traits.length > 0 ? action.traits.join(', ') : '-';
    const req = action.requirements.length > 0 ? action.requirements[0] : (action.trigger || '-');
    table += `| ${link} | ${action.icon} | ${traits} | ${req} |\n`;
  });

  return table;
}

// Update main files
console.log('\n📄 Updating main files with tables:\n');

const basicIntro = extractIntro(basicContent);
const basicTable = makeTable(basicActions, basicSlugs, 'acciones-basicas');
const basicNew = basicIntro + '\n\n## Acciones Básicas\n\n' + basicTable + '\n';
fs.writeFileSync(basicPath, basicNew, 'utf-8');
console.log('  ✓ acciones-basicas.md');

const specialtyIntro = extractIntro(specialtyContent);
const specialtyTable = makeTable(specialtyActions, specialtySlugs, 'acciones-especialidad');
const specialtyNew = specialtyIntro + '\n\n## Acciones Básicas de Especialidad\n\n' + specialtyTable + '\n';
fs.writeFileSync(specialtyPath, specialtyNew, 'utf-8');
console.log('  ✓ acciones-especialidad.md');

console.log('\n✅ Done!\n');
