const fs = require('fs');
const path = require('path');

/**
 * Script para verificar y corregir links rotos en archivos markdown
 * Detecta:
 * - Links a archivos que no existen
 * - Extensiones incorrectas (.md vs sin extensión)
 * - Paths incorrectos
 * - Anchors que no existen en archivos objetivo
 */

class LinkChecker {
  constructor() {
    this.docsPath = path.join(__dirname, '..', 'docs');
    this.brokenLinks = [];
    this.fixedLinks = [];
    this.fileCache = new Map();
    this.headingCache = new Map();
  }

  /**
   * Obtiene todos los archivos markdown en el directorio docs
   */
  getAllMarkdownFiles(dir = this.docsPath) {
    let files = [];
    const entries = fs.readdirSync(dir);

    entries.forEach(entry => {
      const fullPath = path.join(dir, entry);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        files = files.concat(this.getAllMarkdownFiles(fullPath));
      } else if (entry.endsWith('.md')) {
        files.push(fullPath);
      }
    });

    return files;
  }

  /**
   * Extrae todos los headings de un archivo markdown
   */
  getHeadings(filePath) {
    if (this.headingCache.has(filePath)) {
      return this.headingCache.get(filePath);
    }

    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const headings = new Set();

      // Buscar headings en formato markdown: # Heading, ## Heading, etc.
      const headingRegex = /^#+\s+(.+)$/gm;
      let match;

      while ((match = headingRegex.exec(content)) !== null) {
        // Convertir a anchor format: "My Heading" → "my-heading"
        const anchor = match[1]
          .toLowerCase()
          .trim()
          .replace(/[^\w\s-]/g, '')
          .replace(/\s+/g, '-')
          .replace(/-+/g, '-');
        headings.add(anchor);
      }

      this.headingCache.set(filePath, headings);
      return headings;
    } catch (err) {
      console.error(`❌ Error leyendo ${filePath}: ${err.message}`);
      return new Set();
    }
  }

  /**
   * Encuentra el archivo correcto, intentando múltiples variaciones
   */
  findFile(basePath, targetPath) {
    const variations = [
      targetPath,
      targetPath + '.md',
      path.join(targetPath, 'index.md'),
      targetPath.replace(/\.md$/, ''),
    ];

    for (const variant of variations) {
      const fullPath = path.resolve(basePath, variant);
      const relativePath = path.relative(this.docsPath, fullPath);

      // Verificar que el archivo está dentro de docs/
      if (!fullPath.startsWith(this.docsPath)) continue;

      if (fs.existsSync(fullPath) && fs.statSync(fullPath).isFile()) {
        return fullPath;
      }
    }

    return null;
  }

  /**
   * Procesa los links de un archivo
   */
  processFile(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const relativePath = path.relative(this.docsPath, filePath);

      // Regex para encontrar links markdown: [texto](ruta)
      // También captura links HTML: href="ruta"
      const linkRegex = /\[([^\]]+)\]\(([^)]+)\)|href=["']([^"']+)["']/g;
      let match;
      const fileDir = path.dirname(filePath);

      while ((match = linkRegex.exec(content)) !== null) {
        const linkText = match[1] || '';
        const linkTarget = match[2] || match[3];

        // Ignorar links con sintaxis Jekyll {{ ... }}
        if (linkTarget.includes('{{') || linkTarget.includes('}}')) {
          continue;
        }

        // Ignorar links externos (http://, https://, etc.)
        if (linkTarget.startsWith('http') || linkTarget.startsWith('#')) {
          continue;
        }

        // Separar path y anchor
        const [linkPath, anchor] = linkTarget.split('#');

        // Ignorar enlaces vacíos o solo anchors dentro del mismo archivo
        if (!linkPath && anchor) {
          continue;
        }

        // Verificar si el archivo existe
        const resolvedFile = this.findFile(fileDir, linkPath);

        if (!resolvedFile) {
          this.brokenLinks.push({
            file: relativePath,
            link: linkTarget,
            linkText: linkText,
            fullPath: filePath,
            type: 'missing-file'
          });
          console.log(`❌ ${relativePath}: Link a archivo no encontrado: [${linkText}](${linkTarget})`);
        } else if (anchor) {
          // Verificar si el anchor existe en el archivo destino
          const headings = this.getHeadings(resolvedFile);
          const anchorNormalized = anchor.toLowerCase();

          if (!headings.has(anchorNormalized)) {
            this.brokenLinks.push({
              file: relativePath,
              link: linkTarget,
              linkText: linkText,
              fullPath: filePath,
              type: 'missing-anchor'
            });
            console.log(`⚠️  ${relativePath}: Anchor no encontrado: [${linkText}](${linkTarget})`);
          }
        }
      }
    } catch (err) {
      console.error(`❌ Error procesando ${filePath}: ${err.message}`);
    }
  }

  /**
   * Ejecuta la verificación de todos los archivos
   */
  run() {
    console.log(`🔍 Escaneando archivos markdown en ${this.docsPath}...\n`);

    const files = this.getAllMarkdownFiles();
    console.log(`📁 Encontrados ${files.length} archivos markdown\n`);

    files.forEach(file => this.processFile(file));

    console.log(`\n${'='.repeat(70)}\n`);
    console.log(`📊 RESULTADO DE VERIFICACIÓN:\n`);
    console.log(`   Links totales verificados: Múltiples`);
    console.log(`   Links rotos encontrados: ${this.brokenLinks.length}\n`);

    if (this.brokenLinks.length > 0) {
      console.log(`🔗 LINKS ROTOS POR TIPO:\n`);

      const byType = {};
      this.brokenLinks.forEach(link => {
        byType[link.type] = (byType[link.type] || 0) + 1;
      });

      Object.entries(byType).forEach(([type, count]) => {
        console.log(`   ${type}: ${count}`);
      });

      console.log(`\n📋 DETALLES:\n`);
      this.brokenLinks.forEach((link, idx) => {
        console.log(`${idx + 1}. ${link.file}`);
        console.log(`   Link: ${link.link}`);
        console.log(`   Tipo: ${link.type}`);
      });
    } else {
      console.log(`✅ ¡Todos los links están correctos!\n`);
    }

    return this.brokenLinks;
  }
}

// Ejecutar
const checker = new LinkChecker();
const broken = checker.run();

// Exportar para uso como módulo
module.exports = LinkChecker;
