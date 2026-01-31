const fs = require('fs');
const path = require('path');

// ÚNICOS términos que REALMENTE no deben cambiar en Pathfinder 2
// (Son mecánicas específicas del juego o convenciones)
const pf2SpecificTerms = new Set([
  'exito',       // éxito - pero es término técnico
  'accion',      // acción - pero es término técnico
  'reaccion',    // reacción - pero es término técnico
]);

// Leer NO_CAMBIOS.json actual
const noCambiosPath = path.join(__dirname, '..', 'NO_CAMBIOS.json');
const noCambiosData = JSON.parse(fs.readFileSync(noCambiosPath, 'utf8'));

// Mapeo de palabras sin acento a formas correctas
const accentMap = {
  'sabiduria': 'sabiduría',
  'constitucion': 'constitución',
  'caracteristica': 'característica',
  'especializacion': 'especialización',
  'informacion': 'información',
  'deteccion': 'detección',
  'exploracion': 'exploración',
  'ubicacion': 'ubicación',
  'posicion': 'posición',
  'direccion': 'dirección',
  'intimidacion': 'intimidación',
  'discrecion': 'discreción',
  'clerigo': 'clérigo',
  'clerigos': 'clérigos',
  'cleriga': 'clérига',
  'cancion': 'canción',
  'seccion': 'sección',
  'artesania': 'artesanía',
  'percepcion': 'percepción',
  'dificil': 'difícil',
  'dificiles': 'difíciles',
  'tamano': 'tamaño',
  'continuacion': 'continuación',
  'algun': 'algún',
  'devocion': 'devoción',
  'magicos': 'mágicos',
  'especificos': 'específicos',
  'distraccion': 'distracción',
  'ensenar': 'enseñar',
  'basandose': 'basándose',
  'mayoria': 'mayoría',
  'empunando': 'empuñando',
  'sufrira': 'sufrirá',
  'otorgandote': 'otorgándote',
  'daninos': 'dañinos',
  'danina': 'dañina',
  'danino': 'dañino',
  'danandolas': 'dañándolas',
  'haciendola': 'haciéndola',
  'haciendolos': 'haciéndolos',
  'tendrias': 'tendrías',
  'basandote': 'basándote',
  'despues': 'después',
  'alli': 'allí',
  'quiza': 'quizá',
  'habitacion': 'habitación',
  'tactico': 'táctico',
  'vibracion': 'vibración',
  'amplian': 'amplían',
  'basicos': 'básicos',
  'escudrinamiento': 'escudriñamiento',
  'prediccion': 'predicción',
  'revelacion': 'revelación',
  'fenomenos': 'fenómenos',
  'maximo': 'máximo',
  'asi': 'así',
  'origenes': 'orígenes',
  'demas': 'demás',
  'traera': 'traerá',
  'cambiaformas': 'cambiaformas',
  'llegais': 'llegáis',
  'encerrandola': 'encerrándola',
  'obligandole': 'obligándole',
  'amontonandose': 'amontonándose',
  'subiendose': 'subiéndose',
  'impondrian': 'impondrían',
  'aferrandose': 'aferrándose',
  'opcion': 'opción',
  'marcandolos': 'marcándolos',
  'extranas': 'extrañas',
  'ficcion': 'ficción',
  'rebanos': 'rebaños',
  'epicos': 'épicos',
  'decadas': 'décadas',
  'canones': 'cánones',
  'fisicos': 'físicos',
  'deberian': 'deberían',
  'atraccion': 'atracción',
  'adoracion': 'adoración',
  'asegurate': 'asegúrate',
  'interactuas': 'interactúas',
  'empunar': 'empuñar',
  'pags': 'págs',
  'empunas': 'empuñas',
  'tendrian': 'tendrían',
  'acabarian': 'acabarían',
  'requeriran': 'requerirán',
  'anaden': 'añaden',
  'obstaculos': 'obstáculos',
  'alquimicas': 'alquímicas',
  'pajaro': 'pájaro',
  'tuneles': 'túneles',
  'caidas': 'caídas',
  'reduccion': 'reducción',
  'interactuan': 'interactúan',
  'empujon': 'empujón',
  'vacio': 'vacío',
  'haria': 'haría',
  'devo': 'devó',
  'interaccion': 'interacción',
  'teurgicos': 'teúrgicos',
  'flamigera': 'flamígera',
  'maldicion': 'maldición',
  'benedicion': 'bendición',
  'pocion': 'poción',
  'tradicion': 'tradición',
  'rastreais': 'rastreáis',
};

const reallyCambios = [];
const reallyNoCambios = [];

// Procesar cada palabra en NO_CAMBIOS
Object.entries(noCambiosData.noCambios).forEach(([word, info]) => {
  if (pf2SpecificTerms.has(word)) {
    // Estos SÍ deben mantenerse sin cambios
    reallyNoCambios.push({
      word,
      count: info[1].count,
      reason: 'Término técnico de Pathfinder 2 que se mantiene sin acentos',
      files: info[1].files
    });
  } else if (accentMap[word]) {
    // Estos DEBERÍAN cambiar
    reallyCambios.push({
      word,
      suggestion: accentMap[word],
      count: info[1].count,
      files: info[1].files
    });
  } else {
    // Estos son dudosos
    console.log(`⚠️  Dudoso: ${word} (${info[1].count} ocurrencias)`);
  }
});

// Ordenar por cantidad de ocurrencias
reallyCambios.sort((a, b) => b.count - a.count);
reallyNoCambios.sort((a, b) => b.count - a.count);

console.log('\n=== ANÁLISIS REFINADO ===\n');
console.log(`Palabras que REALMENTE no deben cambiar: ${reallyNoCambios.length}`);
console.log(`Palabras que SÍ deben cambiar (estaban mal clasificadas): ${reallyCambios.length}\n`);

console.log('=== PALABRAS A CAMBIAR (ANTES ESTABAN EN NO_CAMBIOS) ===');
reallyCambios.forEach(item => {
  console.log(`${item.word} → ${item.suggestion} (${item.count} ocurrencias)`);
});

console.log('\n=== PALABRAS QUE REALMENTE NO DEBEN CAMBIAR ===');
reallyNoCambios.forEach(item => {
  console.log(`${item.word} (${item.count} ocurrencias) - ${item.reason}`);
});

// Guardar archivos refinados
fs.writeFileSync(
  path.join(__dirname, '..', 'CAMBIOS_REFINADOS.json'),
  JSON.stringify({
    resumen: {
      totalAcambiar: reallyCambios.length,
      detalles: reallyCambios
    }
  }, null, 2)
);

fs.writeFileSync(
  path.join(__dirname, '..', 'NO_CAMBIOS_REFINADOS.json'),
  JSON.stringify({
    resumen: {
      totalNoCambios: reallyNoCambios.length,
      detalles: reallyNoCambios
    }
  }, null, 2)
);

console.log('\n✅ Archivos refinados generados: CAMBIOS_REFINADOS.json y NO_CAMBIOS_REFINADOS.json');
