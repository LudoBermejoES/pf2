const axios = require('axios');
const cheerio = require('cheerio');
const url = require('url');

/**
 * Script para verificar links rotos en una página web remota
 * Extrae todos los links de una página y verifica su estado HTTP
 */

class RemoteLinkChecker {
  constructor(baseUrl, options = {}) {
    this.baseUrl = baseUrl;
    this.timeout = options.timeout || 10000;
    this.maxConcurrent = options.maxConcurrent || 5;
    this.brokenLinks = [];
    this.checkedUrls = new Set();
    this.visitedPages = new Set();
    this.linksByPage = new Map();
    this.statusCodeCounts = {};
  }

  /**
   * Normaliza una URL relativa a absoluta basada en la URL de la página
   */
  resolveUrl(pageUrl, linkHref) {
    try {
      // Si es un link absoluto, devolverlo tal cual
      if (linkHref.startsWith('http')) {
        return linkHref;
      }

      // Si es un anchor (#), ignorarlo
      if (linkHref.startsWith('#')) {
        return null;
      }

      // Si es una URL relativa, resolverla
      return new URL(linkHref, pageUrl).href;
    } catch (err) {
      return null;
    }
  }

  /**
   * Extrae todos los links de una página HTML
   */
  extractLinks(html, pageUrl) {
    const $ = cheerio.load(html);
    const links = new Set();

    // Buscar todos los links en <a href>
    $('a[href]').each((i, elem) => {
      const href = $(elem).attr('href');
      const text = $(elem).text().trim();
      const resolved = this.resolveUrl(pageUrl, href);

      if (resolved) {
        links.add({ url: resolved, text: text || href, source: pageUrl });
      }
    });

    return Array.from(links);
  }

  /**
   * Verifica el status de una URL
   */
  async checkUrl(urlToCheck) {
    // Evitar verificar la misma URL múltiples veces
    if (this.checkedUrls.has(urlToCheck)) {
      return;
    }

    this.checkedUrls.add(urlToCheck);

    try {
      const response = await axios.head(urlToCheck, {
        timeout: this.timeout,
        maxRedirects: 5,
        validateStatus: () => true // Aceptar todos los status codes
      });

      const status = response.status;
      this.statusCodeCounts[status] = (this.statusCodeCounts[status] || 0) + 1;

      // Considerar rotos los status 404, 410, 500, 502, 503, etc.
      if (status >= 400) {
        this.brokenLinks.push({
          url: urlToCheck,
          status: status,
          message: `${status} ${response.statusText || 'Error'}`
        });
        console.log(`❌ ${urlToCheck} - ${status}`);
        return false;
      } else {
        console.log(`✅ ${urlToCheck} - ${status}`);
        return true;
      }
    } catch (err) {
      this.brokenLinks.push({
        url: urlToCheck,
        status: 0,
        message: err.message
      });
      console.log(`❌ ${urlToCheck} - Error: ${err.message}`);
      return false;
    }
  }

  /**
   * Ejecuta verificaciones con concurrencia controlada
   */
  async checkUrlsConcurrent(urlsToCheck) {
    const results = [];

    for (let i = 0; i < urlsToCheck.length; i += this.maxConcurrent) {
      const batch = urlsToCheck.slice(i, i + this.maxConcurrent);
      const batchResults = await Promise.all(
        batch.map(urlItem => this.checkUrl(urlItem.url))
      );
      results.push(...batchResults);

      // Pequeña pausa entre batches
      if (i + this.maxConcurrent < urlsToCheck.length) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }

    return results;
  }

  /**
   * Obtiene y procesa una página remota
   */
  async scrapePage(pageUrl) {
    if (this.visitedPages.has(pageUrl)) {
      return [];
    }

    this.visitedPages.add(pageUrl);

    try {
      console.log(`\n🔍 Escaneando: ${pageUrl}`);
      const response = await axios.get(pageUrl, {
        timeout: this.timeout,
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)'
        }
      });

      const links = this.extractLinks(response.data, pageUrl);
      this.linksByPage.set(pageUrl, links);

      return links;
    } catch (err) {
      console.error(`❌ Error accediendo a ${pageUrl}: ${err.message}`);
      return [];
    }
  }

  /**
   * Ejecuta la verificación completa
   */
  async run(startUrl, options = {}) {
    const maxPages = options.maxPages || 1; // Por defecto solo la página principal
    const internalOnly = options.internalOnly !== false; // Por defecto solo links internos

    console.log(`\n🚀 VERIFICADOR DE LINKS REMOTOS\n`);
    console.log(`📄 URL inicial: ${startUrl}`);
    console.log(`⚙️  Configuración:`);
    console.log(`   - Máximo de páginas: ${maxPages}`);
    console.log(`   - Solo links internos: ${internalOnly}`);
    console.log(`   - Timeout: ${this.timeout}ms`);
    console.log(`   - Concurrencia: ${this.maxConcurrent} simultáneas\n`);

    const urlsToScan = [startUrl];
    let allLinks = [];

    // Escanear páginas (de momento solo la principal)
    for (const pageUrl of urlsToScan) {
      if (this.visitedPages.size >= maxPages) break;

      const links = await this.scrapePage(pageUrl);

      // Filtrar solo links internos si está configurado
      let filteredLinks = links;
      if (internalOnly) {
        const baseDomain = new URL(startUrl).hostname;
        filteredLinks = links.filter(link => {
          const linkDomain = new URL(link.url).hostname;
          return linkDomain === baseDomain;
        });
      }

      allLinks = allLinks.concat(filteredLinks);
    }

    // Eliminar duplicados
    const uniqueLinks = Array.from(
      new Map(allLinks.map(link => [link.url, link])).values()
    );

    console.log(`\n📊 Links encontrados: ${uniqueLinks.length}`);
    console.log(`🔗 Verificando links...\n`);

    // Verificar todos los links con concurrencia
    await this.checkUrlsConcurrent(uniqueLinks);

    // Generar reporte
    this.generateReport();
  }

  /**
   * Genera un reporte de la verificación
   */
  generateReport() {
    console.log(`\n${'='.repeat(70)}\n`);
    console.log(`📋 REPORTE DE VERIFICACIÓN\n`);

    console.log(`✅ URLs verificadas correctamente: ${this.checkedUrls.size - this.brokenLinks.length}`);
    console.log(`❌ Links rotos encontrados: ${this.brokenLinks.length}\n`);

    if (Object.keys(this.statusCodeCounts).length > 0) {
      console.log(`📈 Distribución de status codes:\n`);
      Object.entries(this.statusCodeCounts)
        .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
        .forEach(([code, count]) => {
          const status = parseInt(code) < 400 ? '✅' : '❌';
          console.log(`   ${status} ${code}: ${count} links`);
        });
    }

    if (this.brokenLinks.length > 0) {
      console.log(`\n🔴 LINKS ROTOS:\n`);
      this.brokenLinks.forEach((link, idx) => {
        console.log(`${idx + 1}. ${link.url}`);
        console.log(`   Status: ${link.message}`);
      });
    } else {
      console.log(`\n✨ ¡Todos los links funcionan correctamente!\n`);
    }

    console.log(`\n${'='.repeat(70)}\n`);

    return this.brokenLinks;
  }
}

// Uso del script
const args = process.argv.slice(2);
const baseUrl = args[0] || 'https://ludobermejoES.github.io/pf2/';

const checker = new RemoteLinkChecker(baseUrl, {
  timeout: 10000,
  maxConcurrent: 5
});

checker.run(baseUrl, {
  maxPages: 1,
  internalOnly: true
}).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});

module.exports = RemoteLinkChecker;
