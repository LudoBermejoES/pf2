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
        // Crear regex que busque la palabra sin acento (case-insensitive, word boundaries)
        const regex = new RegExp(`\\b${sinAccento}\\b`, 'gi');

        // Reemplazar todas las instancias en el contenido
        content = content.replace(regex, (match) => {
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

// Iniciar procesamiento
console.log('🔄 Iniciando correcciones en lote (sin protección de enlaces)...\n');
processDirectory(docsPath);

console.log(`\n✅ Proceso completado:`);
console.log(`   Archivos modificados: ${archivosModificados}`);
console.log(`   Total de reemplazos: ${totalReemplazos}`);
console.log(`\n⚠️  IMPORTANTE: Verifica los cambios antes de hacer commit`);
console.log(`   Usa: git diff`);
