#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Base paths
const classesDir = path.join(__dirname, '../docs/_clases');

// Classes with PC1 format that need normalization
const pc1Classes = [
  'bardo', 'brujo', 'clerigo', 'druida',
  'explorador', 'guerrero', 'mago', 'picaro'
];

/**
 * Normalizes PC1 format feats to PC2 format
 * PC1 format:
 *   ### Feat Name {% include accion.html tipo="1" %}
 *   **Dote 1**
 *
 *   *Guerrero*
 *
 *   **Requisitos** ...
 *
 *   Description...
 *
 * PC2 format:
 *   ### Feat Name · {% include accion.html tipo="1" %} · Dote 1
 *
 *   <div class="feat-traits-header" markdown="0"><a href="/apendices/rasgos/guerrero/" class="feat-trait">Guerrero</a></div>
 *
 *   **Requisitos:** ...
 *
 *   Description...
 */
function normalizeClassFeats(filePath, className) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  let i = 0;
  const output = [];

  // Keep frontmatter
  if (lines[0] === '---') {
    output.push(lines[0]);
    i = 1;
    while (i < lines.length && lines[i] !== '---') {
      output.push(lines[i]);
      i++;
    }
    if (i < lines.length) {
      output.push(lines[i]); // closing ---
      i++;
    }
  }

  // Keep intro
  while (i < lines.length && !lines[i].match(/^## /)) {
    output.push(lines[i]);
    i++;
  }

  // Process feats
  while (i < lines.length) {
    const line = lines[i];

    // Level header
    if (line.match(/^## Nivel \d+/)) {
      output.push('');
      output.push(line);
      output.push('');
      output.push('---');
      output.push('');
      i++;
      continue;
    }

    // Feat header - handle multiple formats:
    // Format 1: ### Name · Action · Dote X
    // Format 2: ### Name | Dote X
    // Format 3: ### Name - Dote X
    // Format 4: ### Name · Action
    // Format 5: ### Name Action | Dote X · Action (duplicate action icons)
    const featMatch = line.match(/^### (.+)$/);
    if (featMatch) {
      const headerContent = featMatch[1].trim();

      // Extract action icon (first occurrence only)
      const actionMatch = headerContent.match(/{% include accion\.html.*?%}/);
      const actionIcon = actionMatch ? actionMatch[0] : '';

      // Remove all action icons from name
      let cleanName = headerContent.replace(/{% include accion\.html.*?%}/g, '').trim();

      // Extract Dote X from header if present (using any separator: ·, |, -)
      let doteLine = '';
      const doteInHeaderMatch = cleanName.match(/[·|\-]\s*(Dote\s+\d+)\s*$/);
      if (doteInHeaderMatch) {
        doteLine = `**${doteInHeaderMatch[1]}**`;
        cleanName = cleanName.replace(/[·|\-]\s*Dote\s+\d+\s*$/, '').trim();
      }

      // Also remove any remaining separators at the end
      cleanName = cleanName.replace(/[·|\-]\s*$/, '').trim();

      const featName = cleanName;

      i++;

      // Skip empty lines
      while (i < lines.length && !lines[i].trim()) {
        i++;
      }

      // Initialize traits array
      let traits = [];

      // Check for **Nivel X** | format (Mago/Pícaro style)
      // Example: **Nivel 1** | <div class="feat-traits-header"...
      // This can be on its own line OR combined with traits div
      if (i < lines.length && lines[i].match(/^\*\*Nivel \d+\*\*/)) {
        const levelLine = lines[i];
        const levelMatch = levelLine.match(/^\*\*Nivel (\d+)\*\*/);
        if (levelMatch && !doteLine) {
          doteLine = `**Dote ${levelMatch[1]}**`;
        }

        // Check if traits div is on the same line
        if (levelLine.includes('<div class="feat-traits-header"')) {
          const divMatch = levelLine.match(/<div class="feat-traits-header"[^>]*>([\s\S]*?)<\/div>/);
          if (divMatch) {
            const traitHtml = divMatch[1];
            const traitMatches = traitHtml.matchAll(/>([^<]+)<\/a>/g);
            for (const match of traitMatches) {
              traits.push(match[1].trim());
            }
          }
        }

        i++; // Skip this line

        // Skip empty lines after **Nivel X** line
        while (i < lines.length && !lines[i].trim()) {
          i++;
        }
      }

      // Get **Dote X** line if on separate line
      if (i < lines.length && lines[i].match(/^\*\*Dote \d+\*\*$/)) {
        if (!doteLine) {
          doteLine = lines[i].trim();
        }
        i++;
      }

      // Skip empty lines
      while (i < lines.length && !lines[i].trim()) {
        i++;
      }

      // Get traits (italic line like *Guerrero* or *Guerrero, Floritura*)
      // OR traits from **Nivel X** | <div...> format (already extracted above)

      // If traits weren't already extracted from **Nivel X** line, look for them now
      if (traits.length === 0) {
        if (i < lines.length && lines[i].match(/^\*[^*]+\*$/)) {
          // Standard italic format
          const traitLine = lines[i].trim();
          const traitText = traitLine.replace(/^\*/, '').replace(/\*$/, '');
          traits = traitText.split(',').map(t => t.trim());
          i++;
        } else if (i < lines.length && lines[i].match(/<div class="feat-traits-header"/)) {
          // Already formatted with div (extract traits)
          const divMatch = lines[i].match(/<div class="feat-traits-header"[^>]*>([\s\S]*?)<\/div>/);
          if (divMatch) {
            const traitHtml = divMatch[1];
            const traitMatches = traitHtml.matchAll(/>([^<]+)<\/a>/g);
            for (const match of traitMatches) {
              traits.push(match[1].trim());
            }
          }
          i++;
        }
      }

      // Skip empty lines
      while (i < lines.length && !lines[i].trim()) {
        i++;
      }

      // Collect the rest of the feat content
      const featContent = [];
      while (i < lines.length && !lines[i].match(/^(###|##) /)) {
        featContent.push(lines[i]);
        i++;
      }

      // Remove trailing empty lines
      while (featContent.length && !featContent[featContent.length - 1].trim()) {
        featContent.pop();
      }

      // Build normalized feat
      let normalizedHeader = `### ${featName}`;
      if (actionIcon) {
        normalizedHeader += ` · ${actionIcon}`;
      }
      if (doteLine) {
        normalizedHeader += ` · ${doteLine.replace(/\*\*/g, '')}`;
      }

      output.push(normalizedHeader);
      output.push('');

      // Add traits div
      if (traits.length > 0) {
        const traitLinks = traits.map(trait => {
          const traitSlug = trait.toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '');
          return `<a href="/apendices/rasgos/${traitSlug}/" class="feat-trait">${trait}</a>`;
        }).join('');

        output.push(`<div class="feat-traits-header" markdown="0">${traitLinks}</div>`);
        output.push('');
      }

      // Process feat content - change **Prerequisitos** to **Prerrequisitos:**
      featContent.forEach(line => {
        let processedLine = line;

        // Skip any leading --- lines
        if (processedLine.trim() === '---') {
          return;
        }

        // Normalize prerequisite/requirement headers
        processedLine = processedLine.replace(/^\*\*Prerrequisitos\*\*/, '**Prerrequisitos:**');
        processedLine = processedLine.replace(/^\*\*Requisitos\*\*/, '**Requisitos:**');
        processedLine = processedLine.replace(/^\*\*Frecuencia\*\*/, '**Frecuencia:**');
        processedLine = processedLine.replace(/^\*\*Desencadenante\*\*/, '**Desencadenante:**');
        processedLine = processedLine.replace(/^\*\*Coste\*\*/, '**Coste:**');
        processedLine = processedLine.replace(/^\*\*Acceso\*\*/, '**Acceso:**');

        output.push(processedLine);
      });

      output.push('');
      output.push('---');
      output.push('');

      continue;
    }

    i++;
  }

  // Remove trailing empty lines and dashes
  while (output.length && (!output[output.length - 1].trim() || output[output.length - 1] === '---')) {
    output.pop();
  }

  return output.join('\n');
}

// Main execution
console.log('🔄 Normalizando formato de dotes PC1 a PC2...\n');

pc1Classes.forEach(classDir => {
  const classPath = path.join(classesDir, classDir, 'dotes.md');

  if (!fs.existsSync(classPath)) {
    console.log(`⚠️  No existe: ${classDir}/dotes.md`);
    return;
  }

  console.log(`📝 Procesando: ${classDir}`);

  // Backup original
  const backupPath = classPath + '.backup';
  fs.copyFileSync(classPath, backupPath);

  // Get class name
  const className = classDir.charAt(0).toUpperCase() + classDir.slice(1);

  // Normalize
  const normalized = normalizeClassFeats(classPath, className);

  // Write
  fs.writeFileSync(classPath, normalized, 'utf-8');

  console.log(`   ✓ Normalizado (backup: ${path.basename(backupPath)})`);
});

console.log('\n✅ Normalización completada!');
console.log('   Los archivos originales están respaldados con extensión .backup');
