const fs = require('fs');
const path = require('path');

// Términos de Pathfinder 2 que NO deben cambiar (sin acentos intencionalmente)
const pathfinder2Terms = new Set([
  'exito',           // éxito - término técnico del juego
  'critico',         // crítico - término técnico
  'fallo',          // término técnico
  'automaticamente', // término técnico
  'tradicion',      // tradición - término técnico (traditions en PF2)
  'comun',          // común - término técnico
  'rango',          // término técnico
  'entrenado',      // término técnico
  'experto',        // término técnico
  'maestro',        // término técnico
  'legendario',     // término técnico
  'DJ',             // Director de Juego
  'prueba',         // término técnico (check)
  'secreta',        // término técnico
  'Arcanos',        // nombre propio
  'Naturaleza',     // nombre propio (skill name)
  'Ocultismo',      // nombre propio (skill name)
  'Religion',       // nombre propio (skill name)
  'conjuro',        // término técnico
  'identificas',    // verbo específico del contexto
  'tirar',          // término específico del juego
  'resultado',      // término técnico
  'peor',           // comparativo técnico
  'incrementa',     // término técnico
  'lanzado',        // término específico (spell cast)
  'familiar',       // término técnico
  'compañero',      // término técnico
  'animal',         // término técnico
  'hechizo',        // término técnico
  'magia',          // término técnico
  'defensa',        // término técnico
  'ataque',         // término técnico
  'iniciativa',     // término técnico
  'velocidad',      // término técnico
  'armadura',       // término técnico
  'arma',           // término técnico
  'escudo',         // término técnico
  'accion',         // acción - término técnico del sistema
  'reaccion',       // reacción - término técnico
  'actividad',      // término técnico
  'rasgo',          // término técnico
  'efecto',         // término técnico
  'mejorado',       // término técnico
  'penalizacion',   // penalización - término técnico
  'bonificacion',   // bonificación - término técnico
  'modificador',    // término técnico
  'dado',           // término técnico
  'pocion',         // poción - término técnico
  'ritual',         // término técnico
  'encantamiento',  // término técnico
  'maldicion',      // maldición - término técnico
  'bendicion',      // bendición - término técnico
  'veneno',         // término técnico
  'enfermedad',     // término técnico
  'condicion',      // condición - término técnico del sistema
  'invulnerable',   // término técnico
  'petrificado',    // término técnico
  'confundido',     // término técnico
  'asustado',       // término técnico
  'debilitado',     // término técnico
  'paralizado',     // término técnico
  'ceguera',        // término técnico
  'sordera',        // término técnico
  'resistencia',    // término técnico
  'inmunidad',      // término técnico
  'vulnerabilidad', // término técnico
  'caracteristica', // característica - término técnico
  'atributo',       // término técnico
  'habilidad',      // término técnico
  'destreza',       // término técnico
  'constitucion',   // constitución - término técnico
  'inteligencia',   // término técnico
  'sabiduria',      // sabiduría - término técnico
  'carisma',        // término técnico
]);

// Palabras que SÍ deberían tener acentos (correcciones legítimas)
const shouldHaveAccents = new Set([
  'tradición',
  'éxito',
  'crítico',
  'información',
  'descripción',
  'número',
  'párrafo',
  'página',
  'línea',
  'técnica',
  'técnico',
  'específico',
  'específicamente',
  'objetivo',
  'objetivo',
  'carácter',
  'característica',
  'constitución',
  'sabiduría',
  'penalización',
  'bonificación',
  'acción',
  'reacción',
  'condición',
  'poción',
  'maldición',
  'bendición',
  'próximo',
  'anterior',
  'último',
  'primero',
  'siguiente',
  'final',
  'inicial',
]);

// Leer el archivo RESULTS_ACCENTS.json
const filePath = path.join(__dirname, '..', 'RESULTS_ACCENTS.json');
const jsonData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
const data = jsonData.issues;

const cambios = [];
const noCambios = [];

// Analizar cada error
data.forEach(error => {
  const word = error.word.toLowerCase();
  const suggestion = error.suggestions[0]; // Primera sugerencia

  // Revisar si es un término de Pathfinder 2
  const isPF2Term = pathfinder2Terms.has(word);

  // Revisar si está en contexto de "No cambios" (términos técnicos del juego)
  const context = error.context.toLowerCase();
  const isGameMechanic = context.includes('conjuro') ||
                         context.includes('hechizo') ||
                         context.includes('accion') ||
                         context.includes('rasgo') ||
                         context.includes('condicion') ||
                         context.includes('efecto');

  if (isPF2Term || isGameMechanic) {
    noCambios.push({
      file: error.file,
      line: error.line,
      word: word,
      reason: isPF2Term ? 'Término técnico de Pathfinder 2' : 'Parte de mecánica del juego',
      context: error.context.substring(0, 150) + '...'
    });
  } else {
    cambios.push({
      file: error.file,
      line: error.line,
      word: word,
      suggestion: suggestion,
      context: error.context.substring(0, 150) + '...'
    });
  }
});

// Agrupar por palabra para análisis
const cambiosPorPalabra = {};
const noCambiosPorPalabra = {};

cambios.forEach(item => {
  if (!cambiosPorPalabra[item.word]) {
    cambiosPorPalabra[item.word] = { count: 0, suggestion: item.suggestion, files: [] };
  }
  cambiosPorPalabra[item.word].count++;
  cambiosPorPalabra[item.word].files.push(item.file);
});

noCambios.forEach(item => {
  if (!noCambiosPorPalabra[item.word]) {
    noCambiosPorPalabra[item.word] = { count: 0, reason: item.reason, files: [] };
  }
  noCambiosPorPalabra[item.word].count++;
  noCambiosPorPalabra[item.word].files.push(item.file);
});

// Crear resumen
const resumen = {
  totalErrores: data.length,
  cambiosIdentificados: cambios.length,
  noCambiosIdentificados: noCambios.length,
  porcentajeQueCambia: ((cambios.length / data.length) * 100).toFixed(2) + '%',
  porcentajeQueNoCambia: ((noCambios.length / data.length) * 100).toFixed(2) + '%',
  palabrasParaCambiar: cambiosPorPalabra,
  palabrasParaNoCAmbiar: noCambiosPorPalabra
};

console.log('\n=== RESUMEN DE ANÁLISIS ===\n');
console.log(`Total de errores encontrados: ${resumen.totalErrores}`);
console.log(`Cambios a hacer: ${resumen.cambiosIdentificados} (${resumen.porcentajeQueCambia})`);
console.log(`No cambios: ${resumen.noCambiosIdentificados} (${resumen.porcentajeQueNoCambia})`);

console.log('\n=== PALABRAS PARA CAMBIAR ===');
Object.entries(cambiosPorPalabra)
  .sort((a, b) => b[1].count - a[1].count)
  .forEach(([word, data]) => {
    console.log(`${word} → ${data.suggestion} (${data.count} ocurrencias)`);
  });

console.log('\n=== PALABRAS QUE NO CAMBIAN ===');
Object.entries(noCambiosPorPalabra)
  .sort((a, b) => b[1].count - a[1].count)
  .forEach(([word, data]) => {
    console.log(`${word} (${data.count} ocurrencias) - ${data.reason}`);
  });

// Guardar archivos
fs.writeFileSync(
  path.join(__dirname, '..', 'CAMBIOS.json'),
  JSON.stringify({ resumen, cambios: Object.entries(cambiosPorPalabra) }, null, 2),
  'utf8'
);

fs.writeFileSync(
  path.join(__dirname, '..', 'NO_CAMBIOS.json'),
  JSON.stringify({ resumen: { total: noCambios.length }, noCambios: Object.entries(noCambiosPorPalabra) }, null, 2),
  'utf8'
);

console.log('\n✅ Archivos generados: CAMBIOS.json y NO_CAMBIOS.json');
