#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Base paths
const classesDir = path.join(__dirname, '../docs/_clases');
const outputBaseDir = path.join(__dirname, '../docs/_dotes');

// Helper to create slug
function slug(str) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove accents
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Helper to extract first meaningful paragraph as description
function extractDescription(content) {
  const lines = content.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (
      trimmed &&
      !trimmed.startsWith('<') &&
      !trimmed.startsWith('**Prerrequisitos') &&
      !trimmed.startsWith('**Requisitos') &&
      !trimmed.startsWith('**Frecuencia') &&
      !trimmed.startsWith('**Coste') &&
      !trimmed.startsWith('**Desencadenante') &&
      !trimmed.startsWith('**Acceso') &&
      !trimmed.startsWith('**Dote ') &&
      !trimmed.match(/^\*\*Dote \d+\*\*$/) &&
      !trimmed.match(/^\*[^*]+\*$/) && // Skip italic-only lines (traits like *Guerrero*)
      !trimmed.includes('feat-trait') &&
      !trimmed.includes('---')
    ) {
      // Truncate if too long
      if (trimmed.length > 150) {
        return trimmed.substring(0, 147) + '...';
      }
      return trimmed;
    }
  }
  return '';
}

// Helper to extract traits
function extractTraits(content) {
  const traitsMatch = content.match(/<div class="feat-traits-header"[^>]*>([\s\S]*?)<\/div>/);
  const traits = [];

  if (traitsMatch) {
    const traitLines = traitsMatch[1].split('\n');
    for (const line of traitLines) {
      if (line.includes('feat-trait')) {
        const traitMatch = line.match(/>([^<]+)<\/a>/);
        if (traitMatch) {
          traits.push(traitMatch[1].trim());
        }
      }
    }
  }

  return traits;
}

// Helper to extract prerequisites
function extractPrerequisites(content) {
  const prereqMatch = content.match(/\*\*Prerrequisitos?:\*\*\s*(.+?)(?:\n\n|\n\*\*|$)/s);
  return prereqMatch ? prereqMatch[1].trim().replace(/\n/g, ' ') : '';
}

// Helper to extract requirements
function extractRequirements(content) {
  const reqMatch = content.match(/\*\*Requisitos:\*\*\s*(.+?)(?:\n\n|\n\*\*|$)/s);
  return reqMatch ? reqMatch[1].trim().replace(/\n/g, ' ') : '';
}

// Parse a class feats file
function parseClassFeats(filePath, className) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  const feats = [];
  let currentLevel = null;
  let i = 0;

  // Skip frontmatter
  if (lines[0] === '---') {
    i = 1;
    while (i < lines.length && lines[i] !== '---') {
      i++;
    }
    i++;
  }

  // Parse feats
  while (i < lines.length) {
    const line = lines[i];

    // Detect level headers (## Nivel X or ## Dotes de Nivel X)
    const levelMatch = line.match(/^##\s+(?:Dotes de )?Nivel (\d+)/);
    if (levelMatch) {
      currentLevel = levelMatch[1];
      i++;
      continue;
    }

    // Detect feat headers (### Feat Name · ... · Dote X)
    const featMatch = line.match(/^###\s+(.+?)(?:\s+·\s+.*)?$/);
    if (featMatch) {
      const fullName = featMatch[1].trim();

      // Extract level from header if not set by section
      const featLevelMatch = line.match(/Dote\s+(\d+)/);
      const featLevel = featLevelMatch ? featLevelMatch[1] : currentLevel || '1';

      // Clean feat name (remove action icons and "Dote X")
      const cleanName = fullName
        .replace(/·.*$/, '')
        .replace(/{% include accion\.html.*?%}/g, '')
        .replace(/◆+|↺|◇/g, '')
        .trim();

      // Collect feat content
      const featContent = [];
      i++;

      // Collect lines until next feat or section
      while (i < lines.length && !lines[i].match(/^(###|##) /)) {
        featContent.push(lines[i]);
        i++;
      }

      // Remove leading/trailing empty lines
      while (featContent.length && !featContent[0].trim()) {
        featContent.shift();
      }
      while (featContent.length && !featContent[featContent.length - 1].trim()) {
        featContent.pop();
      }

      feats.push({
        name: cleanName,
        originalName: fullName,
        level: featLevel,
        content: featContent.join('\n').trim()
      });

      continue;
    }

    i++;
  }

  return feats;
}

// Create individual feat files
function createFeatFiles(feats, className, classSlug) {
  const outputDir = path.join(outputBaseDir, classSlug);

  // Create output directory
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const featData = [];

  feats.forEach((feat) => {
    const featSlug = slug(feat.name);
    const fileName = `${featSlug}.md`;
    const filePath = path.join(outputDir, fileName);

    // Extract metadata
    const traits = extractTraits(feat.content);
    const prerequisites = extractPrerequisites(feat.content);
    const requirements = extractRequirements(feat.content);
    const description = extractDescription(feat.content);

    // Create YAML frontmatter
    const frontmatter = `---
layout: page
permalink: /dotes/${classSlug}/${featSlug}/
title: ${feat.name}
chapter: Dotes
category: dotes
clase: ${className}
level: ${feat.level}
---`;

    // Reconstruct feat header for content
    const featHeader = `## ${feat.originalName}`;

    // Create file content
    const fileContent = `${frontmatter}\n\n${featHeader}\n\n${feat.content}`;

    // Write file
    fs.writeFileSync(filePath, fileContent, 'utf-8');

    // Store data for table
    featData.push({
      name: feat.name,
      slug: featSlug,
      level: feat.level,
      traits: traits,
      prerequisites: prerequisites,
      requirements: requirements,
      description: description
    });
  });

  return featData;
}

// Generate table markdown
function generateTable(featsByLevel) {
  let markdown = '';

  // Sort levels numerically
  const levels = Object.keys(featsByLevel).map(Number).sort((a, b) => a - b);

  levels.forEach(level => {
    markdown += `## Nivel ${level}\n\n`;
    markdown += '| Dote | Descripción | Rasgos | Requisitos |\n';
    markdown += '|------|-------------|--------|------------|\n';

    featsByLevel[level].forEach(feat => {
      const name = `[${feat.name}]({{ '/dotes/${feat.classSlug}/${feat.slug}/' | relative_url }})`;
      const desc = feat.description || '—';
      const traits = feat.traits.join(', ') || '—';
      const reqs = feat.prerequisites || feat.requirements || '—';

      markdown += `| ${name} | ${desc} | ${traits} | ${reqs} |\n`;
    });

    markdown += '\n';
  });

  return markdown;
}

// Update main class feats file with table
function updateClassFeatsFile(classPath, className, classSlug, featsByLevel) {
  const content = fs.readFileSync(classPath, 'utf-8');
  const lines = content.split('\n');

  // Extract frontmatter and intro
  let i = 0;
  const frontmatterLines = [];

  // Get frontmatter
  if (lines[0] === '---') {
    frontmatterLines.push(lines[0]);
    i = 1;
    while (i < lines.length && lines[i] !== '---') {
      frontmatterLines.push(lines[i]);
      i++;
    }
    if (i < lines.length) {
      frontmatterLines.push(lines[i]); // closing ---
      i++;
    }
  }

  // Get intro (everything before first ## header, first --- separator, or first ### feat)
  const introLines = [];
  let seenIntroText = false;
  while (i < lines.length) {
    const line = lines[i];

    // Stop at ## level headers
    if (line.match(/^## /)) {
      break;
    }

    // Stop at ### feat headers
    if (line.match(/^### /)) {
      break;
    }

    // Stop at --- separator AFTER we've seen intro text
    if (line.trim() === '---' && seenIntroText) {
      introLines.push(line); // Include the separator
      break;
    }

    // Track if we've seen non-empty intro text
    if (line.trim() && line.trim() !== '---') {
      seenIntroText = true;
    }

    introLines.push(line);
    i++;
  }

  // Generate new content
  const frontmatter = frontmatterLines.join('\n');
  const intro = introLines.join('\n').trim();
  const table = generateTable(featsByLevel);

  const newContent = `${frontmatter}\n\n${intro}\n\n${table}`;

  // Write updated file
  fs.writeFileSync(classPath, newContent, 'utf-8');
}

// Main execution
console.log('📚 Extrayendo dotes de clase...\n');

// Get all class directories
const classDirs = fs.readdirSync(classesDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name)
  .filter(name => name !== 'arquetipos' && name !== 'companeros'); // Skip non-class dirs

let totalFeats = 0;

classDirs.forEach(classDir => {
  const classPath = path.join(classesDir, classDir, 'dotes.md');

  // Check if feats file exists
  if (!fs.existsSync(classPath)) {
    console.log(`⚠️  No se encontró archivo de dotes para: ${classDir}`);
    return;
  }

  // Parse class name from directory
  const className = classDir.charAt(0).toUpperCase() + classDir.slice(1);
  const classSlug = slug(classDir);

  console.log(`\n📖 Procesando: ${className}`);

  // Parse feats
  const feats = parseClassFeats(classPath, className);
  console.log(`   Encontradas ${feats.length} dotes`);

  if (feats.length === 0) {
    return;
  }

  // Create individual files
  console.log('   Creando archivos individuales...');
  const featData = createFeatFiles(feats, className, classSlug);

  // Organize by level
  const featsByLevel = {};
  featData.forEach(feat => {
    if (!featsByLevel[feat.level]) {
      featsByLevel[feat.level] = [];
    }
    featsByLevel[feat.level].push({
      ...feat,
      classSlug: classSlug
    });
  });

  // Update main file with table
  console.log('   Actualizando archivo principal con tabla...');
  updateClassFeatsFile(classPath, className, classSlug, featsByLevel);

  console.log(`   ✓ Completado: ${feats.length} dotes procesadas`);
  totalFeats += feats.length;
});

console.log(`\n✅ Proceso completado!`);
console.log(`   Total de dotes extraídas: ${totalFeats}`);
console.log(`   Archivos creados en: docs/_dotes/[clase]/`);
