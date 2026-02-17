#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Base paths
const ancestriesDir = path.join(__dirname, '../docs/_ascendencias');
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

// Clean feat name by removing Liquid includes and "Dote X" markers
function cleanFeatName(name) {
  // Remove everything from {% include onwards
  let cleaned = name.replace(/\s*\{%[^%]*%\}/g, '');

  // Remove "· Dote X ·" or "Dote X ·" patterns
  cleaned = cleaned.replace(/\s*·?\s*[Dd]ote\s+\d+\s*·?\s*/g, '');

  // Remove trailing separators
  cleaned = cleaned.replace(/\s*·\s*$/g, '');

  return cleaned.trim();
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
      !trimmed.startsWith('**Beneficio') &&
      !trimmed.startsWith('**Frecuencia') &&
      !trimmed.startsWith('**Coste') &&
      !trimmed.startsWith('**Desencadenante') &&
      !trimmed.startsWith('**Acceso') &&
      !trimmed.startsWith('**Dote ') &&
      !trimmed.match(/^\*\*Dote \d+\*\*/) &&
      !trimmed.match(/^\*[^*]+\*$/) && // Skip italic-only lines
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

// Helper to extract traits from **Dote X** · Trait1, Trait2 line
function extractTraits(headerLine, content) {
  const traits = [];

  // Try to extract from **Dote X** · Traits format
  const traitMatch = headerLine.match(/\*\*Dote \d+\*\*\s*·\s*(.+)/);
  if (traitMatch) {
    const traitsPart = traitMatch[1].trim();
    // Split by comma or · and clean up
    const traitList = traitsPart.split(/[,·]/).map(t => t.trim()).filter(t => t);
    traits.push(...traitList);
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

// Parse an ancestry feats file
function parseAncestryFeats(filePath, ancestryName) {
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

    // Detect level headers (## Nivel X)
    const levelMatch = line.match(/^##\s+Nivel (\d+)/);
    if (levelMatch) {
      currentLevel = levelMatch[1];
      i++;
      continue;
    }

    // Detect feat headers (### Feat Name)
    const featMatch = line.match(/^###\s+(.+)$/);
    if (featMatch) {
      const rawFeatName = featMatch[1].trim();
      const featName = cleanFeatName(rawFeatName); // Clean the name
      i++;

      // Next line should have **Dote X** · Traits
      let headerLine = '';
      let featLevel = currentLevel || '1';

      if (i < lines.length) {
        headerLine = lines[i];
        const levelMatch = headerLine.match(/\*\*Dote (\d+)\*\*/);
        if (levelMatch) {
          featLevel = levelMatch[1];
          i++;
        }
      }

      // Collect feat content until next feat, section, or ---
      const featContent = [headerLine]; // Include the **Dote X** line

      while (i < lines.length) {
        const currentLine = lines[i];

        // Stop at next feat or section
        if (currentLine.match(/^(###|##) /)) {
          break;
        }

        // Stop at --- separator (but include it)
        if (currentLine.trim() === '---') {
          featContent.push(currentLine);
          i++;
          break;
        }

        featContent.push(currentLine);
        i++;
      }

      // Remove trailing empty lines
      while (featContent.length && !featContent[featContent.length - 1].trim()) {
        featContent.pop();
      }

      feats.push({
        name: featName,
        originalName: rawFeatName, // Keep original for reference
        level: featLevel,
        headerLine: headerLine,
        content: featContent.join('\n').trim()
      });

      continue;
    }

    i++;
  }

  return feats;
}

// Create individual feat files
function createFeatFiles(feats, ancestryName, ancestrySlug) {
  const outputDir = path.join(outputBaseDir, ancestrySlug);

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
    const traits = extractTraits(feat.headerLine, feat.content);
    const prerequisites = extractPrerequisites(feat.content);
    const requirements = extractRequirements(feat.content);
    const description = extractDescription(feat.content);

    // Create YAML frontmatter
    const frontmatter = `---
layout: page
permalink: /dotes/${ancestrySlug}/${featSlug}/
title: ${feat.name}
chapter: Dotes
category: dotes
ascendencia: ${ancestryName}
level: ${feat.level}
---`;

    // Reconstruct feat header for content
    const featHeader = `## ${feat.name}`;

    // Add trait badges if traits exist
    let traitBadges = '';
    if (traits.length > 0) {
      traitBadges = '\n<div class="feat-traits-header" markdown="0">';
      traits.forEach(trait => {
        const traitSlug = slug(trait);
        traitBadges += `<a href="/apendices/rasgos/${traitSlug}/" class="feat-trait">${trait}</a>`;
      });
      traitBadges += '</div>\n';
    }

    // Create file content
    const fileContent = `${frontmatter}\n\n${featHeader}\n${traitBadges}\n${feat.content}`;

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

// Generate dotes_short.md with table
function generateDotesShort(ancestryName, ancestrySlug, featsByLevel, originalIntro) {
  let markdown = '';

  // Sort levels numerically
  const levels = Object.keys(featsByLevel).map(Number).sort((a, b) => a - b);

  levels.forEach(level => {
    markdown += `## Nivel ${level}\n\n`;
    markdown += '| Dote | Descripción | Rasgos | Requisitos |\n';
    markdown += '|------|-------------|--------|------------|\n';

    featsByLevel[level].forEach(feat => {
      const name = `[${feat.name}](/dotes/${ancestrySlug}/${feat.slug}/)`;
      const desc = feat.description || '—';
      const traits = feat.traits.join(', ') || '—';
      const reqs = feat.prerequisites || feat.requirements || '—';

      markdown += `| ${name} | ${desc} | ${traits} | ${reqs} |\n`;
    });

    markdown += '\n';
  });

  return markdown;
}

// Create dotes_short.md file
function createDotesShortFile(ancestryPath, ancestryName, ancestrySlug, featsByLevel) {
  const content = fs.readFileSync(ancestryPath, 'utf-8');
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
      frontmatterLines.push(lines[i]); // closing ---
      i++;
    }
  }

  // Update frontmatter permalink to dotes_short
  const updatedFrontmatter = frontmatterLines.map(line => {
    if (line.startsWith('permalink:')) {
      return line.replace('/dotes/', '/dotes_short/');
    }
    return line;
  });

  // Get intro (everything before first ## header or first --- separator after frontmatter)
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
  const frontmatter = updatedFrontmatter.join('\n');
  const intro = introLines.join('\n').trim();
  const table = generateDotesShort(ancestryName, ancestrySlug, featsByLevel, intro);

  const newContent = `${frontmatter}\n\n${intro}\n\n${table}`;

  // Write dotes_short.md file
  const outputPath = ancestryPath.replace('dotes.md', 'dotes_short.md');
  fs.writeFileSync(outputPath, newContent, 'utf-8');

  return outputPath;
}

// Main execution
console.log('📚 Extrayendo dotes de ascendencia...\n');

// Get all ancestry directories
const ancestryDirs = fs.readdirSync(ancestriesDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name);

let totalFeats = 0;
let totalFiles = 0;

ancestryDirs.forEach(ancestryDir => {
  const ancestryPath = path.join(ancestriesDir, ancestryDir, 'dotes.md');

  // Check if feats file exists
  if (!fs.existsSync(ancestryPath)) {
    console.log(`⚠️  No se encontró archivo de dotes para: ${ancestryDir}`);
    return;
  }

  // Parse ancestry name from directory
  const ancestryName = ancestryDir.charAt(0).toUpperCase() + ancestryDir.slice(1);
  const ancestrySlug = slug(ancestryDir);

  console.log(`\n📖 Procesando: ${ancestryName}`);

  // Parse feats
  const feats = parseAncestryFeats(ancestryPath, ancestryName);
  console.log(`   Encontradas ${feats.length} dotes`);

  if (feats.length === 0) {
    return;
  }

  // Create individual files
  console.log('   Creando archivos individuales...');
  const featData = createFeatFiles(feats, ancestryName, ancestrySlug);

  // Organize by level
  const featsByLevel = {};
  featData.forEach(feat => {
    if (!featsByLevel[feat.level]) {
      featsByLevel[feat.level] = [];
    }
    featsByLevel[feat.level].push(feat);
  });

  // Create dotes_short.md with table
  console.log('   Creando dotes_short.md con tabla...');
  const shortPath = createDotesShortFile(ancestryPath, ancestryName, ancestrySlug, featsByLevel);

  console.log(`   ✓ Completado: ${feats.length} dotes procesadas`);
  console.log(`   ✓ Creado: ${path.basename(shortPath)}`);
  totalFeats += feats.length;
  totalFiles++;
});

console.log(`\n✅ Proceso completado!`);
console.log(`   Total de dotes extraídas: ${totalFeats}`);
console.log(`   Total de ascendencias procesadas: ${totalFiles}`);
console.log(`   Archivos individuales creados en: docs/_dotes/[ascendencia]/`);
console.log(`   Archivos dotes_short.md creados en: docs/_ascendencias/[ascendencia]/`);
