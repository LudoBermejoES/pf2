const fs = require('fs');
const path = require('path');

// Mapeo de correcciones finales - SOLO acentos legítimos
const corrections = {
  'recuperacion': 'recuperación',
  'poblacion': 'población',
  'relojeria': 'relojería',
  'historicas': 'históricas',
  'terrorifico': 'terrorífico',
  'subacuaticas': 'subacuáticas',
  'rapidos': 'rápidos',
  'ilicitos': 'ilícitos',
  'prohibio': 'prohibió',
  'tecnologicas': 'tecnológicas',
  'arqueologo': 'arqueólogo',
  'descubrio': 'descubrió',
  'luciernaga': 'luciérnaga',
  'carnivoros': 'carnívoros',
  'consiguio': 'consiguió',
  'huracan': 'huracán',
  'subterraneos': 'subterráneos',
  'recien': 'recién',
  'licantropos': 'licántropos',
  'vastago': 'vástago',
  'campeon': 'campeón',
  'revolucion': 'revolución',
  'concedio': 'concedió',
  'atencion': 'atención',
  'municion': 'munición',
  'polvora': 'pólvora',
  'muneca': 'muñeca',
  'metalicos': 'metálicos',
  'caidos': 'caídos',
  'comprension': 'comprensión',
  'orientacion': 'orientación',
  'coordinacion': 'coordinación',
  'intuicion': 'intuición',
  'formacion': 'formación',
  'progresion': 'progresión',
  'seleccion': 'selección',
  'cooperacion': 'cooperación',
  'desesperacion': 'desesperación',
  'iluminacion': 'iluminación',
  'permitio': 'permitió',
  'desentranar': 'desentrañar',
  'rendicion': 'rendición',
  'convirtiendose': 'convirtiéndose',
  'sacrilegas': 'sacrílegas',
  'tacticas': 'tácticas',
  'reducirian': 'reducirían',
  'estaras': 'estarás',
  'acuatico': 'acuático',
  'elevacion': 'elevación',
  'bipedos': 'bípedos',
  'cuadrupedos': 'cuadrúpedos',
  'tentaculos': 'tentáculos',
  'costaria': 'costaría',
  'exposicion': 'exposición',
  'suposicion': 'suposición',
  'caparazon': 'caparazón',
  'anadiendo': 'añadiendo',
  'denominacion': 'denominación',
  'deberia': 'debería',
  'gustaria': 'gustaría',
  'ocupaciónes': 'ocupaciones',
  'investigaciónes': 'investigaciones',
  'preocupaciónes': 'preocupaciones',
  'aproximaciónes': 'aproximaciones'
};

console.log(`🔄 Iniciando correcciones finales de acentos...\n`);
console.log(`Palabras a corregir: ${Object.keys(corrections).length}`);
console.log(`${Object.entries(corrections).map(([sin, con]) => `  ${sin} → ${con}`).join('\n')}\n`);

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
        // Crear regex que busque la palabra sin acento (case-insensitive, word boundaries)
        const regex = new RegExp(`\\b${sinAccento}\\b`, 'gi');

        // Reemplazar todas las instancias en el contenido
        content = content.replace(regex, (match, offset, fullText) => {
          // Verificar si estamos dentro de un enlace o URL
          if (isInPermalinkOrLink(fullText, offset)) {
            return match; // No cambiar
          }
          replacements++;

          // Preservar la capitalizacion del match original
          if (match[0] === match[0].toUpperCase()) {
            return conAccento.charAt(0).toUpperCase() + conAccento.slice(1);
          }
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
 * Verifica si una posición en el texto está dentro de un enlace o URL
 * @param {string} text - El texto completo
 * @param {number} offset - Posición del match
 * @returns {boolean} true si está en enlace/URL
 */
function isInPermalinkOrLink(text, offset) {
  // Búsqueda hacia atrás para encontrar si estamos en un enlace markdown [texto](url)
  // Solo verificar si está dentro de los paréntesis de la URL
  const beforeOffset = text.substring(0, offset);
  const afterOffset = text.substring(offset);

  // Contar paréntesis: si hay más ( que ) antes del offset, estamos potencialmente en un enlace
  const lastOpenParen = beforeOffset.lastIndexOf('(');
  const lastCloseParen = beforeOffset.lastIndexOf(')');
  const nextCloseParen = afterOffset.indexOf(')');

  // Si hay un ( sin cerrar antes de este punto, y se cierra después, probablemente estamos en una URL
  if (lastOpenParen > lastCloseParen && nextCloseParen !== -1) {
    // Verificar que este ( sea parte de un patrón markdown [...](...)
    // buscando hacia atrás desde el (
    const beforeParen = text.substring(Math.max(0, lastOpenParen - 50), lastOpenParen);
    if (beforeParen.includes(']')) {
      // Parece ser una URL markdown, no cambiar
      return true;
    }
  }

  return false;
}

// Iniciar procesamiento
processDirectory(docsPath);

console.log(`\n✅ Proceso completado:`);
console.log(`   Archivos modificados: ${archivosModificados}`);
console.log(`   Total de reemplazos: ${totalReemplazos}`);
console.log(`\n⚠️  IMPORTANTE: Verifica los cambios antes de hacer commit`);
console.log(`   Usa: git diff`);
