#!/usr/bin/env node
/**
 * crawl-pathfinderwiki.js
 *
 * Descarga una página de pathfinderwiki.com y los artículos enlazados desde ella,
 * convirtiendo el contenido a Markdown limpio y guardándolo en data/pathfinderwiki/.
 *
 * Uso:
 *   node crawl-pathfinderwiki.js <artículo> [--depth N]
 *
 * Ejemplos:
 *   node crawl-pathfinderwiki.js Brevoy
 *   node crawl-pathfinderwiki.js Brevoy --depth 2
 */

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');
const cheerio = require('cheerio');
const TurndownService = require('turndown');

// ── Configuración ──────────────────────────────────────────────────────────────
const BASE      = 'https://pathfinderwiki.com';
const API_BASE  = `${BASE}/w/api.php`;
const OUT_DIR   = path.join(__dirname, 'data', 'pathfinderwiki');
const DELAY_MS  = 800;   // pausa entre peticiones para no saturar el servidor
const MAX_LINKS = 40;    // máximo de artículos enlazados a seguir por página

// Categorías de artículos de Pathfinder Wiki que se excluyen (metapáginas)
const SKIP_PREFIXES = [
  'Special:', 'Talk:', 'User:', 'File:', 'Category:', 'Template:',
  'Help:', 'Forum:', 'MediaWiki:', 'Portal:', 'Pathfinder_Wiki:',
  'Facts:', 'Meta:', 'PathfinderWiki:'
];

// Palabras en el título que indican que es una página editorial/autoral, no de lore
const SKIP_KEYWORDS = [
  'Paizo', 'Pathfinder Society Scenario', 'Player Companion',
  'Adventure Path', 'Module', 'sourcebook', 'Hardcover'
];

// ── Utilidades ─────────────────────────────────────────────────────────────────
function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function safeFilename(title) {
  return title.replace(/[^a-zA-Z0-9_\-áéíóúÁÉÍÓÚñÑüÜ]/g, '_').toLowerCase();
}

function shouldSkip(title) {
  if (SKIP_PREFIXES.some(p => title.startsWith(p))) return true;
  if (SKIP_KEYWORDS.some(k => title.includes(k))) return true;
  return false;
}

// ── Descarga de una página via MediaWiki API (parse) ──────────────────────────
async function fetchPage(title) {
  const url = new URL(API_BASE);
  url.searchParams.set('action', 'parse');
  url.searchParams.set('page', title);
  url.searchParams.set('prop', 'text|links|categories|sections');
  url.searchParams.set('format', 'json');
  url.searchParams.set('redirects', '1');

  const res = await fetch(url.toString(), {
    headers: {
      'User-Agent': 'PF2SpanishWiki/1.0 (educational; translation project)',
      'Accept': 'application/json'
    }
  });

  if (!res.ok) {
    throw new Error(`HTTP ${res.status} al obtener "${title}"`);
  }

  const data = await res.json();
  if (data.error) {
    throw new Error(`API error para "${title}": ${data.error.info}`);
  }
  return data.parse;
}

// ── Extrae texto limpio + links de la respuesta parse ─────────────────────────
function extractContent(parsed) {
  const $ = cheerio.load(parsed.text['*']);

  // Eliminar elementos que no aportan contenido real
  $('table.toc, .mw-editsection, .navbox, .catlinks, sup.reference, ' +
    '.reflist, #References, .noprint, .sistersitebox, ' +
    'table.ambox, .stub, .cleanup').remove();

  // Extraer enlaces internos a otros artículos
  const links = (parsed.links || [])
    .map(l => l['*'])
    .filter(t => t && !shouldSkip(t));

  // Convertir HTML restante a Markdown
  const td = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced',
    bulletListMarker: '-'
  });

  // Reescribir hrefs internos para que sean relativos al wiki
  $('a[href]').each((_, el) => {
    const href = $(el).attr('href');
    if (href && href.startsWith('/wiki/')) {
      $(el).attr('href', BASE + href);
    }
  });

  const html = $('body').html() || '';
  const markdown = td.turndown(html);

  return { markdown, links };
}

// ── Procesamiento de una sola página ─────────────────────────────────────────
async function processPage(title, visited) {
  if (visited.has(title)) return null;
  visited.add(title);

  console.log(`  → Descargando: ${title}`);
  let parsed;
  try {
    parsed = await fetchPage(title);
  } catch (err) {
    console.warn(`    ✗ Error: ${err.message}`);
    return null;
  }

  const realTitle = parsed.title;
  const { markdown, links } = extractContent(parsed);

  const filename = safeFilename(realTitle) + '.md';
  const outPath  = path.join(OUT_DIR, filename);

  const fileContent = [
    `# ${realTitle}`,
    '',
    `> Fuente: ${BASE}/wiki/${encodeURIComponent(realTitle.replace(/ /g, '_'))}`,
    `> Descargado: ${new Date().toISOString().slice(0, 10)}`,
    '',
    markdown
  ].join('\n');

  fs.writeFileSync(outPath, fileContent, 'utf8');
  console.log(`    ✓ Guardado: ${filename}`);

  return { title: realTitle, links };
}

// ── Crawl principal ────────────────────────────────────────────────────────────
async function crawl(startTitle, depth) {
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const visited = new Set();
  let queue = [startTitle];

  for (let d = 0; d <= depth; d++) {
    if (queue.length === 0) break;

    console.log(`\n── Profundidad ${d} (${queue.length} páginas) ──`);
    const nextQueue = [];

    for (const title of queue) {
      const result = await processPage(title, visited);
      await sleep(DELAY_MS);

      if (result && d < depth) {
        // Añadir a la siguiente ronda los links aún no visitados
        const newLinks = result.links
          .filter(t => !visited.has(t) && !shouldSkip(t))
          .slice(0, MAX_LINKS);
        nextQueue.push(...newLinks);
      }
    }

    queue = [...new Set(nextQueue)]; // deduplicar
  }

  // Generar índice de lo descargado
  const files = fs.readdirSync(OUT_DIR).filter(f => f.endsWith('.md'));
  const index = [
    '# Índice de artículos descargados de Pathfinder Wiki',
    '',
    `Inicio: **${startTitle}** | Profundidad: ${depth} | Total: ${files.length} artículos`,
    '',
    ...files.map(f => `- [${f.replace('.md', '')}](./${f})`)
  ].join('\n');

  fs.writeFileSync(path.join(OUT_DIR, '_index.md'), index, 'utf8');
  console.log(`\n✅ Listo. ${files.length} artículos en ${OUT_DIR}`);
  console.log(`   Índice: ${path.join(OUT_DIR, '_index.md')}`);
}

// ── CLI ───────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Uso: node crawl-pathfinderwiki.js <Artículo> [--depth N]');
  process.exit(1);
}

const article = args[0];
const depthIdx = args.indexOf('--depth');
const depth = depthIdx !== -1 ? parseInt(args[depthIdx + 1], 10) : 1;

console.log(`\nCrawlando: ${article} (profundidad ${depth})`);
crawl(article, depth).catch(err => {
  console.error('Error fatal:', err);
  process.exit(1);
});
