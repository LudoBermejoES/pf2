const fs = require('fs');
const path = require('path');

// Leer correcciones necesarias
const correctionsPath = path.join(__dirname, '..', 'CORRECCIONES_NECESARIAS.json');
const correctionsData = JSON.parse(fs.readFileSync(correctionsPath, 'utf8'));

// Crear mapa de correcciones: palabra sin acento -> palabra con acento
const corrections = {};
correctionsData.debenCambiar.forEach(item => {
  corrections[item.word] = item.suggestion;
});

console.log(`Cargadas ${Object.keys(corrections).length} correcciones\n`);

// Procesar archivos
const docsPath = path.join(__dirname, '..', 'docs');
let totalReemplazos = 0;
let archivosModificados = 0;

function processDirectory(dir) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      processDirectory(fullPath);
    } else if (file.endsWith('.md')) {
      const original = fs.readFileSync(fullPath, 'utf8');
      let content = original;
      let replacements = 0;

      // Procesar cada corrección
      Object.entries(corrections).forEach(([sinAccento, conAccento]) => {
        // Crear regex que busque la palabra sin acento
        // Usar word boundaries para no cambiar dentro de otras palabras
        const regex = new RegExp(`\\b${sinAccento}\\b`, 'g');

        // Reemplazar, pero evitar permalinks y enlaces
        content = content.replace(regex, (match, offset, fullText) => {
          // Verificar si estamos dentro de un permalink o enlace
          if (isInPermalinkOrLink(fullText, offset)) {
            return match; // No cambiar
          }
          replacements++;
          return conAccento;
        });
      });

      if (replacements > 0) {
        fs.writeFileSync(fullPath, content, 'utf8');
        archivosModificados++;
        totalReemplazos += replacements;
        console.log(`✏️  ${fullPath.replace(docsPath, '')}: ${replacements} cambio(s)`);
      }
    }
  });
}

/**
 * Verifica si una posición en el texto está dentro de un permalink o enlace
 * @param {string} text - El texto completo
 * @param {number} offset - Posición del match
 * @returns {boolean} true si está en permalink/enlace
 */
function isInPermalinkOrLink(text, offset) {
  // Búsqueda hacia atrás para encontrar si estamos en un permalink
  const permalinkStart = text.lastIndexOf('permalink:', offset);
  const permalinkEnd = text.indexOf('\n', offset);

  if (permalinkStart !== -1 && permalinkEnd !== -1) {
    // Verificar si el offset está entre permalink: y el final de la línea
    if (offset > permalinkStart && offset < permalinkEnd) {
      // Verificar que sea de verdad un permalink (debe estar después de "permalink:")
      const afterPermalink = text.substring(permalinkStart, offset);
      if (afterPermalink.includes('permalink:')) {
        return true;
      }
    }
  }

  // Búsqueda hacia atrás para encontrar si estamos en un enlace markdown [texto](url)
  // Patrón: [algo](/ruta/)
  const linkStartBracket = text.lastIndexOf('[', offset);
  const linkStartParen = text.indexOf('(', linkStartBracket);
  const linkEndParen = text.indexOf(')', linkStartParen);

  if (linkStartBracket !== -1 && linkStartParen !== -1 && linkEndParen !== -1) {
    // Verificar que el offset esté dentro de los paréntesis (la URL)
    if (offset > linkStartParen && offset < linkEndParen) {
      // Asegurarse de que esto es un patrón markdown válido [...](...)
      const betweenBrackets = text.substring(linkStartBracket, linkStartParen);
      if (betweenBrackets.includes(']')) {
        // Estamos dentro de una URL markdown
        return true;
      }
    }
  }

  // Búsqueda de URLs directas (http://, https://)
  const beforeOffset = text.substring(Math.max(0, offset - 100), offset);

  if ((beforeOffset.includes('http://') || beforeOffset.includes('https://')) &&
      !beforeOffset.includes('\n')) {
    return true;
  }

  return false;
}

// Iniciar procesamiento
console.log('🔄 Iniciando correcciones...\n');
processDirectory(docsPath);

console.log(`\n✅ Proceso completado:`);
console.log(`   Archivos modificados: ${archivosModificados}`);
console.log(`   Total de reemplazos: ${totalReemplazos}`);
console.log(`\n⚠️  IMPORTANTE: Verifica los cambios antes de hacer commit`);
console.log(`   Usa: git diff`);
