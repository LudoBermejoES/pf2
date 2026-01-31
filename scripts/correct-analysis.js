const fs = require('fs');
const path = require('path');

// ÚNICOS términos de Pathfinder 2 que realmente NO deben cambiar
const pf2CoreTerms = new Set([
  'accion',      // acción - término técnico core del sistema
  'reaccion',    // reacción - término técnico core del sistema
  'exito',       // éxito - término técnico core del sistema (resultado de tirada)
]);

// Mapeo de palabras sin acento a formas correctas
const accentMap = {
  'amplian': 'amplían',
  'otorgandote': 'otorgándote',
  'especificos': 'específicos',
  'basandose': 'basándose',
  'sabiduria': 'sabiduría',
  'distraccion': 'distracción',
  'ensenar': 'enseñar',
  'discrecion': 'discreción',
  'obligandola': 'obligándola',
  'interplanario': 'interplanar',
  'anadir': 'añadir',
  'mayoria': 'mayoría',
  'empunando': 'empuñando',
  'sufrira': 'sufrirá',
  'posicion': 'posición',
  'direccion': 'dirección',
  'intimidacion': 'intimidación',
  'situacion': 'situación',
  'reposicionar': 'reposicionar',
  'ocultista': 'ocultista',
  'reposicionas': 'reposicionas',
  'incorporeas': 'incorporeas',
  'descerebrado': 'descerebrado',
  'erratica': 'errática',
  'inmovilizantes': 'inmovilizantes',
  'rastreais': 'rastreáis',
  'danandolas': 'dañándolas',
  'haciendola': 'haciéndola',
  'exploracion': 'exploración',
  'maldicion': 'maldición',
  'clerigos': 'clérigos',
  'devocion': 'devoción',
  'potenciandolo': 'potenciándolo',
  'concediendote': 'concediéndote',
  'senescales': 'senescales',
  'tendrias': 'tendrías',
  'basandote': 'basándote',
  'cleriga': 'clérига',
  'despues': 'después',
  'tactico': 'táctico',
  'vibracion': 'vibración',
  'alli': 'allí',
  'habitacion': 'habitación',
  'quiza': 'quizá',
  'constitucion': 'constitución',
  'dificil': 'difícil',
  'daninos': 'dañinos',
  'caracteristica': 'característica',
  'demas': 'demás',
  'resiliencia': 'resiliencia',
  'racheado': 'achasado',
  'lentifica': 'lentifica',
  'desencadenante': 'desencadenante',
  'indetectable': 'indetectable',
  'colapse': 'colapso',
  'traera': 'traerá',
  'heroismo': 'heroísmo',
  'danino': 'dañino',
  'danina': 'dañina',
  'cambiaformas': 'cambiaformas',
  'polimorfado': 'polimorfado',
  'combinandolos': 'combinándolos',
  'llegais': 'llegáis',
  'encerrandola': 'encerrándola',
  'obligandole': 'obligándole',
  'reenfocado': 'reenfocado',
  'amontonandose': 'amontonándose',
  'subiendose': 'subiéndose',
  'impondrian': 'impondrían',
  'aferrandose': 'aferrándose',
  'opcion': 'opción',
  'cancion': 'canción',
  'seccion': 'sección',
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
  'sacrilegeas': 'sacrilegas',
  'haciendolos': 'haciéndolos',
  'fortisimma': 'fortísima',
  'preparandoles': 'preparándoles',
  'teurgicos': 'teúrgicos',
  'interaccion': 'interacción',
  'piromanticas': 'piromántcas',
  'asegurate': 'asegúrate',
  'pocion': 'poción',
  'interactuas': 'interactúas',
  'oscurecedor': 'oscurecedor',
  'empunar': 'empuñar',
  'pags': 'págs',
  'empunas': 'empuñas',
  'tendrian': 'tendrían',
  'acabarian': 'acabarían',
  'requeriran': 'requerirán',
  'anaden': 'añaden',
  'obstaculos': 'obstáculos',
  'alquimicas': 'alquímicas',
  'especializacion': 'especialización',
  'flamigera': 'flamígera',
  'constructos': 'constructos',
  'pajaro': 'pájaro',
  'tuneles': 'túneles',
  'dificiles': 'difíciles',
  'caidas': 'caídas',
  'reduccion': 'reducción',
  'interactuan': 'interactúan',
  'empujon': 'empujón',
  'vacio': 'vacío',
  'reposicionan': 'reposicionan',
  'haria': 'haría',
  'dromaar': 'dromaar',
  'artesania': 'artesanía',
  'percepcion': 'percepción',
  'magicos': 'mágicos',
  'tamano': 'tamaño',
  'tradicion': 'tradición',
  'deteccion': 'detección',
  'informacion': 'información',
  'continuacion': 'continuación',
  'algun': 'algún',
  'basicos': 'básicos',
  'escudrinamiento': 'escudriñamiento',
  'prediccion': 'predicción',
  'revelacion': 'revelación',
  'fenomenos': 'fenómenos',
  'interaccionas': 'interaccionas',
  'esperables': 'esperables',
  'maximo': 'máximo',
  'asi': 'así',
  'reenfocas': 'reenofcas',
  'origenes': 'orígenes',
  'clerigo': 'clérigo',
  'pocion': 'poción',
  'maldicion': 'maldición',
};

// Leer NO_CAMBIOS.json
const noCambiosPath = path.join(__dirname, '..', 'NO_CAMBIOS.json');
const noCambiosData = JSON.parse(fs.readFileSync(noCambiosPath, 'utf8'));

const shouldChange = [];
const shouldntChange = [];

// Procesar cada término
noCambiosData.noCambios.forEach(([word, info]) => {
  if (pf2CoreTerms.has(word)) {
    shouldntChange.push({ word, ...info, reason: 'Término técnico core de Pathfinder 2' });
  } else if (accentMap[word]) {
    shouldChange.push({ word, suggestion: accentMap[word], ...info });
  }
});

// Ordenar
shouldChange.sort((a, b) => b.count - a.count);
shouldntChange.sort((a, b) => b.count - a.count);

console.log('\n=== ANÁLISIS CORRECTO ===\n');
console.log(`Total en NO_CAMBIOS original: ${noCambiosData.resumen.total}`);
console.log(`Términos que SÍ DEBEN cambiar: ${shouldChange.length}`);
console.log(`Términos que NO deben cambiar: ${shouldntChange.length}\n`);

console.log('=== PRINCIPALES CAMBIOS NECESARIOS ===');
shouldChange.slice(0, 20).forEach(item => {
  console.log(`${item.word} → ${item.suggestion} (${item.count} ocurrencias)`);
});

console.log('\n=== TÉRMINOS QUE NO CAMBIAN ===');
shouldntChange.forEach(item => {
  console.log(`${item.word} (${item.count} ocurrencias) - ${item.reason}`);
});

// Generar archivo de correcciones necesarias
fs.writeFileSync(
  path.join(__dirname, '..', 'CORRECCIONES_NECESARIAS.json'),
  JSON.stringify({
    resumen: {
      totalEnNoCambios: noCambiosData.resumen.total,
      debenCambiar: shouldChange.length,
      noDebenCambiar: shouldntChange.length,
      porcentajeErrorMisclasificacion: ((shouldChange.length / noCambiosData.resumen.total) * 100).toFixed(2) + '%'
    },
    debenCambiar: shouldChange,
    noDebenCambiar: shouldntChange
  }, null, 2)
);

console.log('\n✅ Archivo generado: CORRECCIONES_NECESARIAS.json');
