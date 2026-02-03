# Estudio: Mejores Librerías Node.js para Editar PDFs

## Resumen Ejecutivo

Para **editar PDFs existentes** en Node.js, la mejor opción general es **pdf-lib**. Para casos de uso más avanzados con PDFs encriptados o manipulación de bajo nivel, considera **MuhammaraJS**.

---

## Comparativa de Librerías

| Librería | Editar PDFs existentes | Crear nuevos | Dependencias nativas | Navegador | Licencia | NPM semanal |
|----------|------------------------|--------------|---------------------|-----------|----------|-------------|
| **pdf-lib** | ✅ Excelente | ✅ | ❌ Ninguna | ✅ | MIT | ~1.5M |
| **MuhammaraJS** | ✅ Muy buena | ✅ | ✅ C++ bindings | ❌ | Apache 2 | ~50K |
| **PDFKit** | ⚠️ Limitada | ✅ Excelente | ❌ | ⚠️ | MIT | ~800K |
| **Puppeteer** | ❌ No | ✅ (HTML→PDF) | ✅ Chrome | ❌ | Apache 2 | ~4M |
| **pdfmake** | ❌ No | ✅ | ❌ | ✅ | MIT | ~400K |

---

## 1. pdf-lib (Recomendada para la mayoría)

```bash
npm install pdf-lib
```

### Capacidades
- ✅ Crear y modificar PDFs existentes
- ✅ Añadir, insertar, eliminar páginas
- ✅ Fusionar y dividir PDFs
- ✅ Dibujar texto, imágenes, formas, SVG
- ✅ Crear y rellenar formularios
- ✅ Incrustar fuentes personalizadas
- ✅ Funciona en browser y Node.js
- ✅ Sin dependencias nativas

### Limitaciones
- ❌ **No extrae texto** de páginas (solo de campos de formulario)
- ❌ **No soporta PDFs encriptados** (falla o devuelve páginas en blanco)
- ❌ No soporta HTML/CSS

### Ejemplo básico
```javascript
import { PDFDocument, rgb } from 'pdf-lib';
import fs from 'fs';

// Cargar PDF existente
const existingPdfBytes = fs.readFileSync('documento.pdf');
const pdfDoc = await PDFDocument.load(existingPdfBytes);

// Obtener primera página
const pages = pdfDoc.getPages();
const firstPage = pages[0];

// Añadir texto
firstPage.drawText('Texto añadido', {
  x: 50,
  y: 500,
  size: 30,
  color: rgb(0, 0.53, 0.71),
});

// Guardar
const pdfBytes = await pdfDoc.save();
fs.writeFileSync('documento-modificado.pdf', pdfBytes);
```

---

## 2. MuhammaraJS (Para casos avanzados)

```bash
npm install muhammara
```

### Capacidades
- ✅ Crear y modificar PDFs existentes
- ✅ Soporta JPG, PNG, TIFF (incluyendo transparentes)
- ✅ Fuentes TrueType, OpenType, Type1
- ✅ Fusionar contenido de múltiples PDFs
- ✅ API "Recipe" para manipulación estilo Canvas
- ✅ **Muy rápido** (bindings C++)
- ✅ Manipulación de bajo nivel

### Limitaciones
- ❌ Requiere compilación nativa (node-gyp)
- ❌ No funciona en navegador
- ❌ No compatible con Node < 15

### Ejemplo básico
```javascript
const muhammara = require('muhammara');

// Modificar PDF existente
const pdfWriter = muhammara.createWriterToModify('input.pdf', {
  modifiedFilePath: 'output.pdf'
});

const pageModifier = new muhammara.PDFPageModifier(pdfWriter, 0);
const context = pageModifier.startContext().getContext();

context.writeText('Texto añadido', 50, 500, {
  font: pdfWriter.getFontForFile('arial.ttf'),
  size: 14,
  color: 0x000000
});

pageModifier.endContext().writePage();
pdfWriter.end();
```

---

## 3. PDFKit (Para crear desde cero)

```bash
npm install pdfkit
```

### Cuándo usarla
- Generar PDFs nuevos programáticamente
- Informes, facturas, documentos dinámicos
- Control preciso del layout

### Limitaciones para edición
- No puede modificar contenido existente de forma efectiva
- Orientada a creación, no edición

---

## 4. Puppeteer (HTML → PDF)

```bash
npm install puppeteer
```

### Cuándo usarla
- Convertir páginas web a PDF
- Cuando ya tienes el contenido en HTML/CSS
- Necesitas renderizado exacto de web

### Limitaciones
- No edita PDFs existentes
- Requiere Chrome/Chromium
- Lento (inicia browser cada vez)
- Alto consumo de recursos

---

## Matriz de Decisión

| Necesitas... | Usa |
|--------------|-----|
| Editar PDF existente (añadir texto, imágenes) | **pdf-lib** |
| Rellenar formularios PDF | **pdf-lib** |
| Fusionar/dividir PDFs | **pdf-lib** |
| Editar PDFs encriptados | **MuhammaraJS** (con limitaciones) |
| Manipulación de bajo nivel | **MuhammaraJS** |
| Máxima velocidad | **MuhammaraJS** |
| Crear PDF desde cero | **PDFKit** o **pdfmake** |
| HTML/CSS → PDF | **Puppeteer** |
| Funcionar en navegador | **pdf-lib** |
| Extraer texto | **pdf-parse** (solo lectura) |

---

## Recomendación Final

Empezar con **pdf-lib** porque:

1. Sin dependencias nativas = fácil de desplegar
2. Funciona igual en Node y browser
3. API moderna y bien documentada
4. Cubre el 90% de casos de edición de PDFs
5. Comunidad activa (~1.5M descargas/semana)

Si encuentras limitaciones (PDFs encriptados, necesidad de extracción de texto, rendimiento extremo), entonces considera **MuhammaraJS** como alternativa.

---

## Fuentes

- [pdf-lib en NPM](https://www.npmjs.com/package/pdf-lib)
- [pdf-lib documentación oficial](https://pdf-lib.js.org/)
- [GitHub - pdf-lib](https://github.com/Hopding/pdf-lib)
- [MuhammaraJS en GitHub](https://github.com/julianhille/MuhammaraJS)
- [MuhammaraJS en NPM](https://www.npmjs.com/package/muhammara)
- [Comparativa de librerías PDF - DEV Community](https://dev.to/handdot/generate-a-pdf-in-js-summary-and-comparison-of-libraries-3k0p)
- [Tutorial pdf-lib - Nutrient.io](https://www.nutrient.io/blog/how-to-build-a-nodejs-pdf-editor-with-pdflib/)
- [Node.js PDF Library Comparison - IronPDF](https://ironpdf.com/nodejs/blog/compare-to-other-components/node-pdf-library/)
- [Top JavaScript PDF libraries 2025 - Nutrient.io](https://www.nutrient.io/blog/top-js-pdf-libraries/)
