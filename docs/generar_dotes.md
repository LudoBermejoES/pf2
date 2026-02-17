# Plan para Generación de Cartas de Dotes

## Análisis del Sistema Actual

### Estructura Existente

El sistema actual de generación de cartas funciona en 4 fases:

1. **Parseo** (`parse_*.py`): Extrae información de archivos markdown
2. **Generación JSON**: Almacena datos estructurados
3. **Generación de Imágenes** (`generate_*_cards.py`): Crea PNG con PIL
4. **Inserción** (`insert_card_images.py`): Añade imágenes a markdown

### Componentes Clave Identificados

#### 1. Estructura de Directorios
```
tools/
└── featCardCreator/          # Nuevo directorio para dotes
    ├── assets/
    │   ├── fonts/           # Fuentes (Cinzel, Oldenburg)
    │   └── images/          # Iconos si necesarios
    ├── data/
    │   └── feats.json       # Datos extraídos
    ├── generated_cards/     # PNGs generados
    ├── parse_feats.py       # Extractor de dotes
    ├── generate_feat_cards.py  # Generador de imágenes
    └── insert_card_images.py   # Insertor a markdown
```

#### 2. Especificaciones Técnicas Actuales

**Dimensiones (300 DPI print quality):**
- Ancho: 744px (63mm)
- Alto: 1039px (88mm)
- Zona segura: 24px (2mm)
- Radio esquinas: 30px (2.5mm)
- Borde: 8px

**Fuentes:**
- Títulos: Cinzel (44pt) - Display font
- Cuerpo: Oldenburg (24pt) - Body text
- Rasgos: 17pt
- Etiquetas: 20pt

**Colores PF2e:**
- Fondo: `(244, 228, 201)` - Pergamino
- Borde: `(125, 68, 55)` - Rojo PF
- Rasgos fondo: `(93, 48, 48)` - Rojo oscuro
- Rasgos texto: `(218, 165, 32)` - Dorado
- Texto: `(45, 39, 34)` - Oscuro
- Título: `(184, 134, 11)` - Dorado

#### 3. Datos Extraídos de Dotes

De los archivos markdown actuales en `docs/_dotes/`, extraer:

```json
{
  "id": "garras-de-saga",
  "name": "Garras de saga",
  "level": 1,
  "traits": ["Changeling"],
  "heritage": "Changeling",
  "ancestry": null,
  "requirements": null,
  "prerequisites": null,
  "special": "Las garras de saga pueden desarrollarse...",
  "description": "Cuando alcanzaste la mayoría de edad...",
  "benefit": "Obtienes un ataque sin armas de garra..."
}
```

## Plan de Implementación

### Fase 1: Análisis y Preparación (2-3 horas)

#### 1.1. Análisis de Datos de Dotes
- [x] Revisar estructura de archivos en `docs/_dotes/`
- [x] Identificar patrones comunes en markdown
- [x] Documentar variaciones de formato
- [x] Crear lista de todos los campos posibles

**Ubicaciones actualizadas (2024):**
- Dotes de ascendencias: `docs/_dotes/{ascendencia}/` (18 ascendencias)
- Dotes de herencias versátiles: `docs/_dotes/herencias-versatiles/{herencia}/` (2 herencias: aiuvarin, dromaar)
- Dotes de clases: `docs/_dotes/{clase}/` (17 clases)
- Dotes de arquetipos: `docs/_dotes/arquetipo/{arquetipo}/` (43 arquetipos)
  - Multiclase: 8 arquetipos (bardo, brujo, clerigo, druida, explorador, guerrero, mago, picaro)
  - Especialización (PC2): 35 arquetipos (acrobata, arqueologo, arquero, etc.)
- Dotes generales: `docs/_dotes/generales/`
- Dotes de habilidad: `docs/_dotes/habilidad/{habilidad}/`

**Total real:** 1,840 archivos de dotes individuales

**Estado del formato (análisis realizado):**
- 1,806 archivos con formato actual (`<div class="feat-traits-header" markdown="0">`)
- 20 archivos con formato div antiguo (sin `markdown="0"`)
- 256 archivos con línea legacy `**Dote X** · Rasgo` que debería eliminarse
- 14 dotes de bárbaro usan "Detonante:" en lugar de "Desencadenante:"

**Estructura estándar de archivo de dote:**
```markdown
---
layout: page
permalink: /dotes/clase/nombre-dote/
title: Nombre de la Dote
chapter: Dotes
category: dotes
clase: Clase          # o ancestry, heritage, archetype, archetype_type
level: X
---

## Nombre de la Dote {% include accion.html tipo="reaccion" %}

<div class="feat-traits-header" markdown="0">
  <a href="/apendices/rasgos/rasgo1/" class="feat-trait">Rasgo1</a>
  <a href="/apendices/rasgos/rasgo2/" class="feat-trait">Rasgo2</a>
</div>

**Prerrequisitos** Dote Anterior o experto en Habilidad o Carisma +2

**Desencadenante** Condición que activa la dote (para reacciones)

**Requisitos** Condiciones temporales para usar la dote

**Frecuencia** una vez cada 10 minutos

Descripción principal de la dote con mecánicas y efectos...

**Exito critico** Resultado excepcional de la tirada
**Exito** Resultado normal de éxito
**Fallo** Resultado de fallo
**Fallo critico** Resultado crítico de fallo

**Especial** Notas adicionales, reglas especiales, interacciones

---
```

**Campos a extraer:**
- `name`: Título de la dote
- `level`: Nivel requerido (del frontmatter YAML)
- `traits`: Lista de rasgos (de `<div class="feat-traits-header">` con enlaces `<a>`)
- `ancestry/heritage/class`: Ascendencia/herencia/clase (del frontmatter)
- `actionType`: Tipo de acción (de `{% include accion.html tipo="..." %}`)
  - Valores posibles: "1", "2", "3", "libre", "reaccion"
  - Puede aparecer en el título `## Nombre {% include... %}` o en línea separada
- `prerequisites`: Prerrequisitos (puede tener o no dos puntos ":")
  - **Formatos variados:**
    - Nombre de otra dote: "Interpretacion Fascinante", "Riposte Oportuno"
    - Rango de habilidad: "entrenado en Acrobacias", "experto en Atletismo", "maestro en Atletismo"
    - Puntuación de característica: "Carisma +2", "Fuerza +14"
    - Requisito de dados: "golpe preciso 6d6"
    - Múltiples requisitos separados por comas
- `requirements`: Requisitos (condiciones que deben cumplirse al usar la dote)
  - Ejemplos: "Empuñas un broquel", "Estas adyacente a un enemigo", "No estas sobrecargado"
  - Diferencia con prerequisites: requirements son condiciones temporales, prerequisites son permanentes
- `trigger`: Desencadenante o Detonante (para dotes de reacción y algunas acciones libres)
  - **IMPORTANTE**: Algunos archivos usan "Detonante:" (14 dotes de bárbaro) en lugar de "Desencadenante:"
  - Ejemplos: "Eres objetivo de un ataque a distancia", "Caes", "Tu turno comienza"
- `frequency`: Frecuencia (limitaciones de uso temporal)
  - Ejemplos: "una vez cada 10 minutos", "una vez por dia", "una vez por combate"
- `cost`: Coste (recursos que deben gastarse)
  - Ejemplos: "Gastar un conjuro de dañar o de curar", "El Precio del objeto elegido"
  - Solo 2 archivos usan este campo
- `effect`: Efecto (efectos específicos, especialmente en dotes de familiares)
  - 6 archivos usan "**Efecto:**" para describir efectos detallados
- `description`: Descripción principal de la dote
- `benefit`: Beneficio (si está separado de la descripción como sección aparte)
  - Común en dotes de ascendencias y generales antiguas
- `special`: Texto especial (notas adicionales, casos especiales)
- `critical_success/success/failure/critical_failure`: Resultados (para dotes que requieren tiradas)

#### 1.2. Crear Estructura de Directorios
```bash
mkdir -p tools/featCardCreator/{assets/{fonts,images},data,generated_cards}
```

#### 1.3. Copiar Assets Compartidos
```bash
# Copiar fuentes
cp tools/actionsCardCreator/assets/fonts/* tools/featCardCreator/assets/fonts/

# Copiar iconos de acciones si son necesarios
cp tools/actionsCardCreator/assets/icons/* tools/featCardCreator/assets/images/
```

### Fase 2: Script de Parseo (4-6 horas)

#### 2.1. Crear `parse_feats.py`

**Funcionalidades principales:**

{% raw %}
```python
def extract_feat_data(file_path):
    """
    Extrae información de un archivo markdown de dote

    Returns:
        dict: Datos estructurados de la dote
    """
    # 1. Leer frontmatter (YAML)
    # 2. Extraer rasgos de <div class="feat-traits-header">
    # 3. Extraer tipo de acción de **Dote X** · o {% include accion.html %}
    # 4. Extraer secciones especiales:
    #    - **Prerrequisitos:** o **Prerrequisito:**
    #    - **Requisitos:**
    #    - **Desencadenante:**
    #    - **Frecuencia:**
    #    - **Beneficio:**
    #    - **Especial:**
    # 5. Extraer descripción (primer párrafo después de encabezado)
    # 6. Limpiar markdown (eliminar [ver](/...), (pág. X), etc.)
```
{% endraw %}

**Patrones a detectar:**
{% raw %}
```python
# Rasgos HTML (formato antiguo)
r'<span class="feat-trait">([^<]+)</span>'

# Rasgos en div con enlaces (formato actual desde 2024)
r'<div class="feat-traits-header".*?>(.*?)</div>'
r'<a href="[^"]*" class="feat-trait">([^<]+)</a>'

# Tipo de acción en Liquid (puede estar en título o línea separada)
# Tipos: "1", "2", "3", "libre", "reaccion"
r'\{% include accion\.html tipo="(.*?)" %\}'

# Tipo de acción en texto (formato antiguo)
r'\*\*Dote (\d+)\*\* · (.+)'

# Secciones especiales - IMPORTANTE: Manejar ambos formatos (con y sin dos puntos)
# Formato 1: Con dos puntos
r'\*\*(Prerrequisitos?|Requisitos|Desencadenante|Detonante|Frecuencia|Coste?|Efecto|Beneficio|Especial):\*\*\s*(.+?)(?=\n\n|\*\*[A-Z]|$)'
# Formato 2: Sin dos puntos (algunos archivos legacy)
r'\*\*(Prerrequisitos?|Requisitos|Desencadenante|Detonante|Frecuencia|Coste?|Efecto|Beneficio|Especial)\*\*\s+(.+?)(?=\n\n|\*\*[A-Z]|$)'

# NOTA: "Detonante" es una variante usada en 14 dotes de bárbaro (debería ser "Desencadenante")

# Resultados de acciones (dotes con tiradas)
r'\*\*(Exito critico|Exito|Fallo critico|Fallo)\*\*\s*(.+?)(?=\n\n|\*\*[A-Z]|$)'
```
{% endraw %}

#### 2.2. Estructura del JSON Generado

```json
{
  "feats": [
    {
      "id": "garras-de-saga",
      "name": "Garras de saga",
      "level": 1,
      "actionType": null,
      "traits": ["Changeling"],
      "category": "herencia_versatil",
      "source": "Changeling",
      "prerequisites": null,
      "requirements": null,
      "trigger": null,
      "frequency": null,
      "description": "Cuando alcanzaste la mayoría de edad, las uñas empezaron a crecerte largas y afiladas.",
      "benefit": "Obtienes un ataque sin armas de garra que inflige 1d4 daño cortante. Tus garras pertenecen al grupo pelea y tienen los rasgos ágil, sutileza y sin armas.",
      "special": "Las garras de saga pueden desarrollarse en cualquier momento de la vida de un changeling. Puedes seleccionar esta dote siempre que puedes obtener una dote de ascendencia, pero no puedes reconvertirla.",
      "results": null
    }
  ]
}
```

#### 2.3. Ejecución del Parser
```bash
cd tools/featCardCreator
python3 parse_feats.py
```

**Salida esperada:**
- `data/feats.json`: JSON con todas las dotes
- Estadísticas de parseo (total dotes, errores, advertencias)

### Fase 3: Generador de Imágenes (6-8 horas)

#### 3.1. Crear `generate_feat_cards.py`

**Diseño de Carta de Dote:**

```
┌─────────────────────────────────────┐
│ ╔═════════════════════════════════╗ │
│ ║  TÍTULO DE LA DOTE       [ICON] ║ │  <- Dorado, Cinzel 44pt
│ ╠═════════════════════════════════╣ │
│ ║ ┌────────┐ ┌────────┐ ┌───────┐║ │  <- Cajas de rasgos
│ ║ │ Rasgo1 │ │ Rasgo2 │ │ Nivel │║ │
│ ║ └────────┘ └────────┘ └───────┘║ │
│ ║ ─────────────────────────────── ║ │
│ ║ Requisitos: ...                 ║ │  <- Oldenburg 20pt
│ ║ ─────────────────────────────── ║ │
│ ║                                 ║ │
│ ║ Descripción de la dote...       ║ │  <- Oldenburg 24pt
│ ║                                 ║ │
│ ║                                 ║ │
│ ║ Beneficio: ...                  ║ │  <- Oldenburg 22pt
│ ║                                 ║ │
│ ║ ─────────────────────────────── ║ │
│ ║ Especial: ...                   ║ │  <- Oldenburg 18pt
│ ╚═════════════════════════════════╝ │
└─────────────────────────────────────┘
```

**Funciones principales:**

```python
def create_feat_card(feat_data):
    """
    Genera una imagen PNG para una dote

    Layout sections:
    1. Título (con icono de acción si aplica)
    2. Rasgos (cajas horizontales)
    3. Nivel (caja destacada)
    4. Requisitos/Prerrequisitos (si existen)
    5. Descripción principal
    6. Beneficio (si está separado)
    7. Especial (si existe)
    """

def draw_feat_title(draw, name, action_type):
    """Dibuja título con fuente Cinzel y opcional icono de acción"""

def draw_trait_boxes(draw, traits, level, y_position):
    """Dibuja cajas de rasgos horizontales + nivel"""

def draw_section_label(draw, label, y_position):
    """Dibuja etiqueta de sección (Requisitos:, Beneficio:, etc.)"""

def draw_formatted_text(draw, text, y_position, max_width):
    """
    Dibuja texto con formato (negritas, cursivas)
    Maneja wrapping y múltiples líneas
    """

def draw_special_section(draw, text, y_position):
    """Dibuja sección especial con fondo ligeramente diferente"""
```

**Colores específicos para dotes:**
```python
# Variaciones por tipo de dote
COLOR_BORDER_ANCESTRY = (125, 68, 55)      # Rojo para ascendencias
COLOR_BORDER_CLASS = (80, 90, 120)         # Azul para clases
COLOR_BORDER_GENERAL = (90, 100, 80)       # Verde para generales
COLOR_BORDER_SKILL = (120, 90, 70)         # Marrón para habilidad

# Distinguir por nivel
def get_border_color_by_level(level):
    if level == 1:
        return COLOR_BORDER
    elif level <= 5:
        return lighten_color(COLOR_BORDER, 0.1)
    elif level <= 10:
        return lighten_color(COLOR_BORDER, 0.2)
    # ...
```

#### 3.2. Manejo de Texto Largo

```python
def calculate_font_size_for_content(text_length, available_height):
    """
    Ajusta tamaño de fuente dinámicamente según contenido
    Para que todo quepa en la carta
    """
    base_size = 24
    if text_length > 500:
        return 20
    elif text_length > 800:
        return 18
    elif text_length > 1000:
        return 16
    return base_size
```

#### 3.3. Generación por Lotes

```python
def generate_all_cards(feats_json):
    """
    Genera todas las cartas
    - Barra de progreso
    - Manejo de errores por dote
    - Reporte de generación
    """
```

### Fase 4: Inserción en Markdown (2-3 horas)

#### 4.1. Crear `insert_card_images.py`

```python
def insert_feat_card_image(feat_file, card_image_path):
    """
    Inserta imagen de carta en archivo markdown de dote

    Ubicación sugerida:
    - Después del ## Título
    - Antes de la descripción

    Formato:
    <div class="feat-card">
      <img src="/assets/cards/feats/{id}.png" alt="{name}">
    </div>
    """
```

#### 4.2. Script de Inserción Masiva

```bash
python3 insert_card_images.py --source generated_cards/ --target ../../docs/_dotes/
```

**Opciones:**
- `--dry-run`: Vista previa sin modificar
- `--backup`: Crear copias de seguridad
- `--filter`: Filtrar por ascendencia/clase/nivel

### Fase 5: Optimización y CSS (2-3 horas)

#### 5.1. Estilos CSS para Cartas

```css
/* docs/_sass/_feat-cards.scss */

.feat-card {
  display: flex;
  justify-content: center;
  margin: 20px auto;
  max-width: 400px;

  img {
    width: 100%;
    height: auto;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

    &:hover {
      transform: scale(1.05);
      transition: transform 0.3s ease;
    }
  }
}

/* Vista móvil */
@media (max-width: 768px) {
  .feat-card {
    max-width: 100%;
    padding: 0 10px;
  }
}

/* Vista impresión */
@media print {
  .feat-card img {
    max-width: 300px;
    page-break-inside: avoid;
  }
}
```

#### 5.2. Optimización de Imágenes

```bash
# Comprimir PNGs sin pérdida de calidad
optipng -o7 generated_cards/*.png

# O usar pngquant para mayor compresión
pngquant --quality=85-95 generated_cards/*.png
```

#### 5.3. Generación de PDFs Imprimibles

```python
# create_print_pdf.py
def create_printable_sheet(cards, layout='3x3'):
    """
    Crea hoja A4 con múltiples cartas para imprimir
    - 9 cartas por página (3x3)
    - Marcas de corte
    - Dorso genérico opcional
    """
```

### Fase 6: Testing y Validación (2-3 horas)

#### 6.1. Tests de Parseo
- [ ] Verificar todas las dotes parseadas correctamente
- [ ] Comprobar campos nulos/vacíos
- [ ] Validar rasgos extraídos
- [ ] Revisar niveles correctos

#### 6.2. Tests de Generación
- [ ] Generar muestras de cada tipo
- [ ] Verificar legibilidad
- [ ] Comprobar que todo el texto cabe
- [ ] Validar colores y fuentes

#### 6.3. Tests de Inserción
- [ ] Verificar que no rompe markdown existente
- [ ] Comprobar rutas de imágenes
- [ ] Validar en diferentes navegadores

### Fase 7: Documentación y Automatización (2-3 horas)

#### 7.1. README del Proyecto

```markdown
# Feat Card Generator

## Instalación

pip install -r requirements.txt

## Uso

### 1. Parsear dotes desde markdown
python3 parse_feats.py

### 2. Generar imágenes de cartas
python3 generate_feat_cards.py

### 3. Insertar cartas en markdown
python3 insert_card_images.py

## Configuración

Editar config.json para ajustar:
- Colores
- Tamaños de fuente
- Layout
```

#### 7.2. Script Maestro

```bash
#!/bin/bash
# generate_all_feat_cards.sh

echo "🎴 Generando cartas de dotes..."

echo "1️⃣ Parseando dotes..."
python3 parse_feats.py || exit 1

echo "2️⃣ Generando imágenes..."
python3 generate_feat_cards.py || exit 1

echo "3️⃣ Optimizando PNGs..."
optipng -o5 generated_cards/*.png

echo "4️⃣ Insertando en markdown..."
python3 insert_card_images.py --backup

echo "✅ ¡Completado! Generadas $(ls generated_cards/*.png | wc -l) cartas"
```

#### 7.3. GitHub Actions (Opcional)

```yaml
name: Generate Feat Cards

on:
  push:
    paths:
      - 'docs/_dotes/**/*.md'

jobs:
  generate-cards:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r tools/featCardCreator/requirements.txt
      - name: Generate cards
        run: cd tools/featCardCreator && ./generate_all_feat_cards.sh
      - name: Commit cards
        run: |
          git config user.name "Feat Card Bot"
          git add assets/cards/feats/*.png
          git commit -m "🎴 Update feat cards" || true
          git push
```

## Estimación de Tiempo Total

| Fase | Tiempo | Complejidad |
|------|--------|-------------|
| 1. Análisis y Preparación | 2-3h | Baja |
| 2. Script de Parseo | 4-6h | Media |
| 3. Generador de Imágenes | 6-8h | Alta |
| 4. Inserción en Markdown | 2-3h | Baja |
| 5. Optimización y CSS | 2-3h | Media |
| 6. Testing y Validación | 2-3h | Media |
| 7. Documentación | 2-3h | Baja |
| **TOTAL** | **20-29h** | - |

## Consideraciones Especiales

### 1. Variabilidad de Formato
- Algunas dotes tienen formato inconsistente
- Necesario manejar múltiples patrones
- Validación estricta de parseo

### 2. Dotes Largas
- Algunas dotes tienen mucho texto
- Necesario ajuste dinámico de fuente
- Posible generación de cartas de 2 caras

### 3. Performance
- ~1500 dotes totales estimadas
- Generación paralela recomendada
- Cache de fuentes e imágenes

### 4. Mantenimiento
- Script debe ser robusto a cambios
- Configuración externalizada
- Logs detallados de errores

## Extensiones Futuras

1. **Cartas de Dotes Interactivas** (web)
   - Hover para ver detalles
   - Click para expandir
   - Búsqueda y filtrado

2. **Generador de Mazos**
   - Seleccionar dotes por personaje
   - Exportar PDF listo para imprimir
   - Organizador por nivel

3. **Comparador de Dotes**
   - Vista lado a lado
   - Destacar diferencias
   - Recomendaciones

4. **Integración con Constructor de Personajes**
   - Auto-generar cartas de dotes seleccionadas
   - Actualización automática
   - Export to Foundry VTT

## Referencias

- Sistema actual de cartas: `tools/actionsCardCreator/`
- Cartas de conjuros: `tools/spellCardCreator/`
- Cartas de objetos: `tools/itemCardCreator/`
- Documentación PIL: https://pillow.readthedocs.io/
