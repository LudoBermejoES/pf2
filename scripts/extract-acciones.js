#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read the action files
const basicActionsPath = path.join(__dirname, '../docs/_reglas/acciones-basicas.md');
const specialtyActionsPath = path.join(__dirname, '../docs/_reglas/acciones-especialidad.md');

const basicContent = fs.readFileSync(basicActionsPath, 'utf-8');
const specialtyContent = fs.readFileSync(specialtyActionsPath, 'utf-8');

// Helper to parse actions from a file
function parseActions(content, type) {
  const actions = [];

  // Match pattern: ## Action Name [ICON(s)]
  // Everything until the next ## or ---
  const actionPattern = /^## (.+?)\s+(◆+|↺|◇)(.*)$/gm;
  let match;

  const contentLines = content.split('\n');
  let currentAction = null;
  let currentIndex = 0;

  while (currentIndex < contentLines.length) {
    const line = contentLines[currentIndex];

    if (line.match(/^## /)) {
      // Found a new action header
      const headerMatch = line.match(/^## (.+?)\s+(◆+|↺|◇)(.*)$/);
      if (headerMatch) {
        if (currentAction) {
          actions.push(currentAction);
        }

        const name = headerMatch[1].trim();
        const icon = headerMatch[2].trim();

        currentAction = {
          name,
          icon,
          traits: [],
          requirements: [],
          trigger: null,
          description: '',
          fullContent: line + '\n',
          startLine: currentIndex + 1
        };
      }
    } else if (currentAction) {
      // Parse content within action
      if (line.match(/^\*\*CONCENTRAR\*\*|^\*\*MOVIMIENTO\*\*|^\*\*ATAQUE\*\*|^\*\*MANIPULAR\*\*|^\*\*SECRETO\*\*|^\*\*Rasgos:/)) {
        // Parse traits line
        const traitsMatch = line.match(/\*\*(.+?)\*\*\s*\*\*(.+?)\*\*/);
        if (traitsMatch) {
          currentAction.traits.push(traitsMatch[1], traitsMatch[2]);
        } else {
          const singleTraitMatch = line.match(/\*\*(.+?)\*\*/g);
          if (singleTraitMatch) {
            singleTraitMatch.forEach(trait => {
              const cleanTrait = trait.replace(/\*\*/g, '').trim();
              if (cleanTrait && !currentAction.traits.includes(cleanTrait)) {
                currentAction.traits.push(cleanTrait);
              }
            });
          }
        }
      } else if (line.match(/^\*\*Rasgos:/i)) {
        const traitsContent = line.replace(/^\*\*Rasgos:\*\*\s*/, '').split(',').map(t => t.trim());
        currentAction.traits = traitsContent.filter(t => t);
      } else if (line.match(/^\*\*Requisitos/i)) {
        const reqContent = line.replace(/^\*\*Requisitos[:\*]*/i, '').trim();
        if (reqContent) {
          currentAction.requirements.push(reqContent);
        }
      } else if (line.match(/^\*\*Desencadenante/i)) {
        const triggerContent = line.replace(/^\*\*Desencadenante[:\*]*/i, '').trim();
        currentAction.trigger = triggerContent;
      } else if (line === '---') {
        // End of action
        if (currentAction) {
          actions.push(currentAction);
          currentAction = null;
        }
      } else if (currentAction && line.trim() !== '') {
        currentAction.fullContent += line + '\n';
      } else if (currentAction) {
        currentAction.fullContent += line + '\n';
      }
    }

    currentIndex++;
  }

  if (currentAction) {
    actions.push(currentAction);
  }

  return actions;
}

// Create slug from name
function createSlug(name) {
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Extract actions
const basicActions = parseActions(basicContent, 'basic');
const specialtyActions = parseActions(specialtyContent, 'specialty');

console.log(`Found ${basicActions.length} basic actions`);
console.log(`Found ${specialtyActions.length} specialty actions`);

// Function to create individual action file
function createActionFile(action, subfolder) {
  const slug = createSlug(action.name);
  const actionDir = path.join(__dirname, `../docs/_reglas/${subfolder}`);

  if (!fs.existsSync(actionDir)) {
    fs.mkdirSync(actionDir, { recursive: true });
  }

  const filename = `${slug}.md`;
  const filepath = path.join(actionDir, filename);

  const frontmatter = `---
layout: page
permalink: /reglas/${subfolder}/${slug}/
title: ${action.name}
chapter: Como Jugar
category: reglas
---

`;

  // Extract the action content (everything after the header until --- or next action)
  const lines = action.fullContent.split('\n');
  let content = '';
  let started = false;

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].match(/^## /)) {
      started = true;
      content += lines[i] + '\n';
    } else if (started && lines[i] === '---') {
      break;
    } else if (started) {
      content += lines[i] + '\n';
    }
  }

  const fileContent = frontmatter + content.trim() + '\n';

  fs.writeFileSync(filepath, fileContent, 'utf-8');
  console.log(`Created: ${subfolder}/${filename}`);

  return slug;
}

// Create individual action files
console.log('\n--- Creating Basic Action Files ---');
const basicSlugs = basicActions.map(action => createActionFile(action, 'acciones-basicas'));

console.log('\n--- Creating Specialty Action Files ---');
const specialtySlugs = specialtyActions.map(action => createActionFile(action, 'acciones-especialidad'));

// Generate summary table
function generateTable(actions, slugs, type) {
  let table = '| Acción | Tipo | Rasgos | Requisitos |\n';
  table += '|--------|------|--------|------------|\n';

  actions.forEach((action, index) => {
    const slug = slugs[index];
    const link = `[${action.name}]({{ '/reglas/${type}/${slug}/' | relative_url }})`;
    const traits = action.traits.length > 0 ? action.traits.join(', ') : '-';
    const requirements = action.requirements.length > 0 ? action.requirements.join(', ') : '-';

    table += `| ${link} | ${action.icon} | ${traits} | ${requirements} |\n`;
  });

  return table;
}

// Update basic actions file
console.log('\n--- Updating acciones-basicas.md ---');
const basicTable = generateTable(basicActions, basicSlugs, 'acciones-basicas');
const basicIntro = basicContent.substring(0, basicContent.indexOf('## Averiguar intenciones'));

const basicUpdated = basicIntro +
  '## Acciones Básicas\n\n' +
  basicTable + '\n';

fs.writeFileSync(basicActionsPath, basicUpdated, 'utf-8');
console.log('Updated acciones-basicas.md with table');

// Update specialty actions file
console.log('\n--- Updating acciones-especialidad.md ---');
const specialtyTable = generateTable(specialtyActions, specialtySlugs, 'acciones-especialidad');
const specialtyIntro = specialtyContent.substring(0, specialtyContent.indexOf('## Agarrarse a un Saliente'));

const specialtyUpdated = specialtyIntro +
  '## Acciones Básicas de Especialidad\n\n' +
  specialtyTable + '\n';

fs.writeFileSync(specialtyActionsPath, specialtyUpdated, 'utf-8');
console.log('Updated acciones-especialidad.md with table');

console.log('\nDone! All actions extracted and tables generated.');
