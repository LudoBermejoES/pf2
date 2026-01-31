#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read the action files
const basicActionsPath = path.join(__dirname, '../docs/_reglas/acciones-basicas.md');
const specialtyActionsPath = path.join(__dirname, '../docs/_reglas/acciones-especialidad.md');

const basicContent = fs.readFileSync(basicActionsPath, 'utf-8');
const specialtyContent = fs.readFileSync(specialtyActionsPath, 'utf-8');

// More robust action parser
function parseActions(content) {
  const actions = [];
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Match: ## Action Name [Icon]
    const headerMatch = line.match(/^## (.+?)\s+(◆+|↺|◇)(.*)$/);
    if (headerMatch) {
      const name = headerMatch[1].trim();
      const icon = headerMatch[2].trim();

      // Collect traits and requirements
      let traits = [];
      let requirements = [];
      let trigger = null;
      let content = '';
      let j = i + 1;
      let endFound = false;

      while (j < lines.length && !endFound) {
        const currentLine = lines[j];

        // Stop at next action or separator
        if (currentLine.match(/^## /) || currentLine === '---') {
          endFound = true;
          break;
        }

        // Parse traits from markdown bold format
        if (currentLine.match(/^\*\*/)) {
          // Handle: **TRAIT1** **TRAIT2** or **Rasgos:** trait1, trait2
          if (currentLine.includes('Rasgos:')) {
            const traitsStr = currentLine
              .replace(/^\*\*Rasgos:\*\*\s*/, '')
              .split(',')
              .map(t => t.trim())
              .filter(t => t && !t.startsWith('**'));
            traits.push(...traitsStr);
          } else {
            const traitMatches = currentLine.match(/\*\*([^*]+)\*\*/g);
            if (traitMatches) {
              traitMatches.forEach(match => {
                const trait = match.replace(/\*\*/g, '').trim();
                if (trait && !traits.includes(trait)) {
                  traits.push(trait);
                }
              });
            }
          }
        }

        // Parse requirements
        if (currentLine.match(/^\*\*Requisitos/i)) {
          const reqText = currentLine
            .replace(/^\*\*Requisitos[:\*]*/i, '')
            .trim()
            .replace(/^\*\*/, '');
          if (reqText && !requirements.includes(reqText)) {
            requirements.push(reqText);
          }
        }

        // Parse trigger
        if (currentLine.match(/^\*\*Desencadenante/i)) {
          trigger = currentLine
            .replace(/^\*\*Desencadenante[:\*]*/i, '')
            .trim()
            .replace(/^\*\*/, '');
        }

        // Accumulate full content
        if (j > i + 1) {
          // Skip empty lines after header
          if (!(currentLine === '' && content === '')) {
            content += currentLine + '\n';
          }
        }

        j++;
      }

      actions.push({
        name,
        icon,
        traits: [...new Set(traits)], // Remove duplicates
        requirements,
        trigger,
        content
      });

      i = j - 1;
    }
  }

  return actions;
}

// Create slug
function createSlug(name) {
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Parse actions
const basicActions = parseActions(basicContent);
const specialtyActions = parseActions(specialtyContent);

console.log(`Found ${basicActions.length} basic actions`);
console.log(`Found ${specialtyActions.length} specialty actions`);

// Create action files
function createActionFiles(actions, subfolder) {
  const actionDir = path.join(__dirname, `../docs/_reglas/${subfolder}`);

  if (!fs.existsSync(actionDir)) {
    fs.mkdirSync(actionDir, { recursive: true });
  }

  const slugs = [];

  actions.forEach(action => {
    const slug = createSlug(action.name);
    slugs.push(slug);

    const filepath = path.join(actionDir, `${slug}.md`);

    const frontmatter = `---
layout: page
permalink: /reglas/${subfolder}/${slug}/
title: ${action.name}
chapter: Como Jugar
category: reglas
---

`;

    // Build the action content
    let actionContent = `## ${action.name} ${action.icon}\n\n`;

    // Add traits
    if (action.traits.length > 0) {
      actionContent += `**Rasgos:** ${action.traits.join(', ')}\n\n`;
    }

    // Add trigger if it's a reaction
    if (action.trigger) {
      actionContent += `**Desencadenante:** ${action.trigger}\n\n`;
    }

    // Add requirements
    if (action.requirements.length > 0) {
      actionContent += `**Requisitos:** ${action.requirements.join(', ')}\n\n`;
    }

    // Add the rest of the content
    actionContent += action.content.trim();

    const fileContent = frontmatter + actionContent + '\n';
    fs.writeFileSync(filepath, fileContent, 'utf-8');
    console.log(`Created: ${subfolder}/${slug}.md`);
  });

  return slugs;
}

console.log('\n--- Creating Basic Action Files ---');
const basicSlugs = createActionFiles(basicActions, 'acciones-basicas');

console.log('\n--- Creating Specialty Action Files ---');
const specialtySlugs = createActionFiles(specialtyActions, 'acciones-especialidad');

// Generate improved table
function generateTable(actions, slugs, subfolder) {
  let table = '| Acción | Tipo | Rasgos | Requisitos |\n';
  table += '|--------|------|--------|------------|\n';

  actions.forEach((action, index) => {
    const slug = slugs[index];
    const link = `[${action.name}]({{ '/reglas/${subfolder}/${slug}/' | relative_url }})`;
    const traits = action.traits.length > 0 ? action.traits.join(', ') : '-';
    const requirements = action.requirements.length > 0
      ? action.requirements[0]
      : (action.trigger ? action.trigger : '-');

    table += `| ${link} | ${action.icon} | ${traits} | ${requirements} |\n`;
  });

  return table;
}

// Update files with tables
console.log('\n--- Updating acciones-basicas.md ---');
const basicIntro = basicContent.substring(0, basicContent.indexOf('## Averiguar intenciones'));
const basicTable = generateTable(basicActions, basicSlugs, 'acciones-basicas');
const basicUpdated = basicIntro.trim() + '\n\n## Acciones Básicas\n\n' + basicTable + '\n';
fs.writeFileSync(basicActionsPath, basicUpdated, 'utf-8');
console.log('Updated acciones-basicas.md');

console.log('\n--- Updating acciones-especialidad.md ---');
const specialtyIntro = specialtyContent.substring(0, specialtyContent.indexOf('## Agarrarse a un Saliente'));
const specialtyTable = generateTable(specialtyActions, specialtySlugs, 'acciones-especialidad');
const specialtyUpdated = specialtyIntro.trim() + '\n\n## Acciones Básicas de Especialidad\n\n' + specialtyTable + '\n';
fs.writeFileSync(specialtyActionsPath, specialtyUpdated, 'utf-8');
console.log('Updated acciones-especialidad.md');

console.log('\n✅ Done! All actions extracted and tables generated.');
