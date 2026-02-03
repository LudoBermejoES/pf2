# Plan: Generador de Tarjetas de Acciones PF2e

## Resumen del Proyecto

Crear una herramienta Python que genere tarjetas de acciones de Pathfinder 2e en formato PDF, similares al estilo del PDF de referencia `basic_action_cards.pdf`, pero en español y tamaño tarot.

**Basado en:** El proyecto exitoso `/Users/ludo/code/arcadia/deck/` que usa Pillow + ReportLab.

---

## 1. Arquitectura Elegida: **Python (Pillow + ReportLab)**

### Justificación

El proyecto Arcadia ya demostró que esta combinación funciona muy bien:

| Componente | Librería | Uso |
|------------|----------|-----|
| **Generación de imágenes** | Pillow | Crear cada tarjeta como PNG a 300 DPI |
| **Generación de PDF** | ReportLab | Combinar tarjetas en hojas imprimibles |
| **Parseo de datos** | Python estándar | Leer JSON/MD con los datos de acciones |

### Ventajas sobre Node.js

1. **Probado**: Ya funciona en el proyecto Arcadia
2. **Más simple**: Sin necesidad de Puppeteer/Chromium
3. **Más rápido**: Pillow es muy eficiente
4. **Menos dependencias**: Solo 2 paquetes principales
5. **Control total**: Dibujo programático de cada elemento

---

## 2. Análisis del PDF de Referencia

### 2.1 Estructura de las Tarjetas

```
┌─────────────────────────────────────┐
│ TÍTULO                    [ICONO]  │ ← Título + icono de acción
├─────────────────────────────────────┤
│ [TRAIT1] [TRAIT2] [TRAIT3]         │ ← Traits con fondo rojo
├─────────────────────────────────────┤
│ Trigger: ...                        │ ← Solo para reacciones
│ Requirements: ...                   │ ← Si aplica
├─────────────────────────────────────┤
│ Descripción del efecto principal    │
│ ...                                 │
├─────────────────────────────────────┤
│ Critical Success: ...               │ ← Grados de éxito
│ Success: ...                        │
│ Failure: ...                        │
│ Critical Failure: ...               │
└─────────────────────────────────────┘
```

### 2.2 Elementos Visuales

- **Fondo**: Blanco/crema (#FFFFFF o #F5F0E6)
- **Borde exterior**: Rojo oscuro (#5D0000)
- **Título**: Fuente serif grande, negrita
- **Icono de acción**: PNG en esquina superior derecha
- **Traits**: Fondo rojo (#722F37), texto blanco, mayúsculas
- **Separadores**: Líneas negras horizontales
- **Texto cuerpo**: Sans-serif, 8-10pt equivalente
- **Secciones en negrita**: "Desencadenante:", "Requisitos:", "Éxito crítico:", etc.

### 2.3 Tamaño Tarot

| Especificación | Valor |
|----------------|-------|
| Dimensiones | 70 × 120 mm |
| En pulgadas | 2.756 × 4.724 in |
| A 300 DPI | 827 × 1417 px |
| Bleed (3mm) | 76 × 126 mm → 898 × 1488 px |
| Esquinas | Radio 3.5mm ≈ 41px |
| Tarjetas/A4 | 4 (2×2) |

---

## 3. Estructura del Proyecto

```
tools/actionsCardCreator/
├── PLAN.md                     # Este documento
├── requirements.txt            # Dependencias Python
├── generate_cards.py           # Generador principal de tarjetas
├── create_print_pdf.py         # Combinador en hojas PDF
├── parse_actions.py            # Parser de archivos MD del wiki
├── assets/
│   ├── icons/                  # Iconos de acciones (PNG)
│   │   ├── action-1.png
│   │   ├── action-2.png
│   │   ├── action-3.png
│   │   ├── reaction.png
│   │   └── free.png
│   └── fonts/                  # Fuentes (opcional)
│       ├── title-font.ttf
│       └── body-font.ttf
├── data/
│   └── actions.json            # Datos de acciones procesados
├── generated_cards/            # Salida: PNGs individuales
└── print_output/               # Salida: PDFs para imprimir
```

---

## 4. Especificaciones de Tarjeta

### 4.1 Constantes (basadas en Arcadia)

```python
# Tamaño Tarot a 300 DPI
CARD_WIDTH = 827    # 70mm a 300 DPI
CARD_HEIGHT = 1417  # 120mm a 300 DPI
BLEED = 35          # 3mm bleed
SAFE_ZONE = 47      # 4mm safe zone
CORNER_RADIUS = 41  # 3.5mm rounded corners

# Colores (RGB)
COLOR_BACKGROUND = (255, 255, 255)      # Blanco
COLOR_BORDER = (93, 0, 0)               # Rojo PF2e oscuro #5D0000
COLOR_TRAIT_BG = (114, 47, 55)          # Rojo trait #722F37
COLOR_TRAIT_TEXT = (255, 255, 255)      # Blanco
COLOR_TEXT = (26, 26, 26)               # Negro suave
COLOR_TITLE = (93, 0, 0)                # Rojo PF2e para título
COLOR_SEPARATOR = (26, 26, 26)          # Negro para líneas
```

### 4.2 Layout de la Tarjeta

```
┌───────────────────────────────────────┐
│ SAFE_ZONE (47px)                      │
│  ┌─────────────────────────────────┐  │
│  │ TÍTULO              [ICONO 80px]│  │ ← 80px altura
│  ├─────────────────────────────────┤  │ ← Separador 2px
│  │ [TRAIT] [TRAIT]                 │  │ ← 40px altura
│  ├─────────────────────────────────┤  │ ← Separador 2px
│  │ Desencadenante: ...             │  │ ← Variable
│  │ Requisitos: ...                 │  │ ← Variable
│  ├─────────────────────────────────┤  │
│  │                                 │  │
│  │ Descripción principal           │  │ ← Área principal
│  │ ...                             │  │
│  │                                 │  │
│  ├─────────────────────────────────┤  │
│  │ Éxito crítico: ...              │  │ ← Resultados
│  │ Éxito: ...                      │  │
│  │ Fallo: ...                      │  │
│  │ Fallo crítico: ...              │  │
│  └─────────────────────────────────┘  │
│ SAFE_ZONE (47px)                      │
└───────────────────────────────────────┘
```

---

## 5. Modelo de Datos

### 5.1 Estructura JSON (actions.json)

```json
{
  "actions": [
    {
      "id": "golpe",
      "name": "Golpe",
      "actionType": "1",
      "traits": ["Ataque"],
      "category": "basica",
      "trigger": null,
      "requirements": null,
      "description": "Atacas con un arma que empuñas o con un ataque sin armas...",
      "results": {
        "criticalSuccess": "Como éxito, pero infliges el doble de daño.",
        "success": "Infliges daño según el arma o ataque sin armas.",
        "failure": null,
        "criticalFailure": null
      }
    },
    {
      "id": "prestar-ayuda",
      "name": "Prestar Ayuda",
      "actionType": "reaction",
      "traits": [],
      "category": "basica",
      "trigger": "Un aliado está a punto de usar una acción que requiere una prueba de habilidad o tirada de ataque.",
      "requirements": "El aliado está dispuesto a aceptar tu ayuda y te has preparado para ayudar.",
      "description": "Para usar esta reacción, primero debes prepararte para ayudar usando una ◆ durante tu turno...",
      "results": {
        "criticalSuccess": "Concedes a tu aliado un bonificador de circunstancia de +2...",
        "success": "Concedes a tu aliado un bonificador de circunstancia de +1...",
        "failure": null,
        "criticalFailure": "Tu aliado sufre una penalización de circunstancia de -1..."
      }
    }
  ]
}
```

### 5.2 Tipos de Acción

```python
ACTION_TYPES = {
    "1": {"icon": "action-1.png", "label": "Acción"},
    "2": {"icon": "action-2.png", "label": "Actividad (2 acciones)"},
    "3": {"icon": "action-3.png", "label": "Actividad (3 acciones)"},
    "reaction": {"icon": "reaction.png", "label": "Reacción"},
    "free": {"icon": "free.png", "label": "Acción gratuita"}
}
```

### 5.3 Categorías

```python
CATEGORIES = {
    "basica": "Acción Básica",
    "especialidad": "Acción de Especialidad",
    "habilidad": "Acción de Habilidad"
}
```

---

## 6. Implementación

### 6.1 generate_cards.py (Estructura Principal)

```python
#!/usr/bin/env python3
"""
PF2e Action Cards Generator
Generates tarot-sized action cards for Pathfinder 2e
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json
import textwrap

# Card specifications (300 DPI for print quality)
CARD_WIDTH = 827    # 70mm at 300 DPI
CARD_HEIGHT = 1417  # 120mm at 300 DPI
SAFE_ZONE = 47      # 4mm safe zone
CORNER_RADIUS = 41  # 3.5mm rounded corners

# Colors
COLOR_BACKGROUND = (255, 255, 255)
COLOR_BORDER = (93, 0, 0)
COLOR_TRAIT_BG = (114, 47, 55)
COLOR_TRAIT_TEXT = (255, 255, 255)
COLOR_TEXT = (26, 26, 26)
COLOR_TITLE = (93, 0, 0)

def create_rounded_rectangle(size, radius, fill_color):
    """Create card base with rounded corners"""
    # Similar a Arcadia
    pass

def draw_title(draw, title, icon_path, y_offset):
    """Draw title and action icon"""
    pass

def draw_traits(draw, traits, y_offset):
    """Draw trait boxes with red background"""
    pass

def draw_text_section(draw, label, text, y_offset, bold_label=True):
    """Draw a labeled text section"""
    pass

def draw_wrapped_text(draw, text, x, y, max_width, font, color):
    """Draw text with automatic wrapping"""
    pass

def generate_action_card(action_data, output_path):
    """Generate a single action card"""
    pass

def main():
    """Main function to generate all cards"""
    pass
```

### 6.2 create_print_pdf.py (PDF Layout)

```python
#!/usr/bin/env python3
"""
Print Sheet PDF Generator for PF2e Action Cards
Creates printable A4/Letter sheets with 4 tarot cards per page
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
import os

# Tarot card size
CARD_WIDTH_MM = 70
CARD_HEIGHT_MM = 120

LAYOUTS = {
    'a4_2x2': {
        'pagesize': A4,
        'cards_per_row': 2,
        'cards_per_col': 2,
        'margin_mm': 15
    },
    'letter_2x2': {
        'pagesize': letter,
        'cards_per_row': 2,
        'cards_per_col': 2,
        'margin_mm': 15
    }
}
```

### 6.3 parse_actions.py (Parser del Wiki)

```python
#!/usr/bin/env python3
"""
Parse action markdown files from the PF2e wiki
"""

import os
import re
import json

def parse_action_file(filepath):
    """Parse a single action markdown file"""
    # Extraer: nombre, tipo, traits, descripción, resultados
    pass

def parse_all_actions(wiki_path):
    """Parse all action files and generate actions.json"""
    pass
```

---

## 7. Dependencias

### requirements.txt

```
# Generación de imágenes
Pillow>=10.0.0

# Generación de PDFs
reportlab>=4.0.0
```

### Instalación

```bash
cd tools/actionsCardCreator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 8. Iconos de Acciones

Necesitamos crear o encontrar iconos PNG para cada tipo de acción:

| Tipo | Archivo | Símbolo Original |
|------|---------|------------------|
| 1 acción | action-1.png | ◆ |
| 2 acciones | action-2.png | ◆◆ |
| 3 acciones | action-3.png | ◆◆◆ |
| Reacción | reaction.png | ↺ |
| Gratuita | free.png | ◇ |

**Opción**: Usar los iconos PNG que ya existen en `docs/assets/images/acciones/`:
- `1accion.png`
- `2acciones.png`
- `3acciones.png`
- `reaccion.png`
- `libre.png`

---

## 9. Fuentes de Datos del Wiki

### Acciones Básicas
- Directorio: `docs/_reglas/acciones-basicas/`
- Archivos: `arrastrar.md`, `caminar-a-gatas.md`, `escapar.md`, etc.

### Acciones de Especialidad
- Directorio: `docs/_reglas/acciones-especialidad/`
- Archivos: `agarrarse-a-un-saliente.md`, `alzar-un-escudo.md`, etc.

---

## 10. Comandos de Uso

```bash
# Activar entorno virtual
source venv/bin/activate

# 1. Parsear acciones del wiki → actions.json
python parse_actions.py

# 2. Generar tarjetas PNG
python generate_cards.py

# 3. Crear PDFs para imprimir
python create_print_pdf.py

# O todo junto:
./generate_all.sh
```

---

## 11. Layout de Impresión A4

```
┌────────────────────────────────────────────────────┐
│                    A4 (210 × 297 mm)               │
│                                                    │
│   ┌──────────┐  15mm  ┌──────────┐                │
│   │          │  gap   │          │                │
│   │  Card 1  │        │  Card 2  │                │
│   │ 70×120mm │        │ 70×120mm │                │
│   │          │        │          │                │
│   └──────────┘        └──────────┘                │
│                                                    │
│       15mm gap between rows                        │
│                                                    │
│   ┌──────────┐        ┌──────────┐                │
│   │          │        │          │                │
│   │  Card 3  │        │  Card 4  │                │
│   │ 70×120mm │        │ 70×120mm │                │
│   │          │        │          │                │
│   └──────────┘        └──────────┘                │
│                                                    │
└────────────────────────────────────────────────────┘

Total espacio usado: 155mm × 255mm
Márgenes: ~27mm horizontal, ~21mm vertical
```

---

## 12. Fases de Implementación

### Fase 1: Infraestructura
- [x] Crear estructura de carpetas
- [ ] Crear requirements.txt
- [ ] Copiar iconos de acciones existentes
- [ ] Setup del entorno virtual

### Fase 2: Generador de Tarjetas
- [ ] Implementar `generate_cards.py`
- [ ] Crear tarjeta de prueba manual
- [ ] Ajustar layout y tipografía
- [ ] Manejar textos largos con wrapping

### Fase 3: Parser del Wiki
- [ ] Implementar `parse_actions.py`
- [ ] Generar `actions.json` desde los MD
- [ ] Validar datos extraídos

### Fase 4: Generación Completa
- [ ] Generar todas las acciones básicas
- [ ] Generar acciones de especialidad
- [ ] Revisar y ajustar diseño

### Fase 5: PDF de Impresión
- [ ] Implementar `create_print_pdf.py`
- [ ] Layout A4 con 4 tarjetas
- [ ] Marcas de corte opcionales

---

## 13. Ejemplo Visual Esperado

```
┌─────────────────────────────────────┐
│                                     │
│  Golpe                         ◆   │
│  ═══════════════════════════════   │
│  ┌────────┐                         │
│  │ ATAQUE │                         │
│  └────────┘                         │
│  ───────────────────────────────    │
│                                     │
│  Atacas con un arma que empuñas    │
│  o con un ataque sin armas,        │
│  teniendo como objetivo a una      │
│  criatura dentro de tu alcance     │
│  (para un ataque cuerpo a cuerpo)  │
│  o dentro del alcance (para un     │
│  ataque a distancia).              │
│                                     │
│  ───────────────────────────────    │
│                                     │
│  Éxito crítico: Como éxito, pero   │
│  infliges el doble de daño.        │
│                                     │
│  Éxito: Infliges daño según el     │
│  arma o ataque sin armas.          │
│                                     │
└─────────────────────────────────────┘
```

---

## 14. Referencias

### Proyecto Base
- `/Users/ludo/code/arcadia/deck/` - Generador de cartas Arcadia (Pillow + ReportLab)

### Documentación
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)

### Especificaciones Tarot
- Tamaño estándar: 70 × 120 mm
- Resolución: 300 DPI
- Esquinas redondeadas: 3.5mm

---

## 15. Próximos Pasos

1. **Aprobar este plan**
2. Crear `requirements.txt`
3. Copiar iconos de `docs/assets/images/acciones/`
4. Implementar `generate_cards.py` con una tarjeta de prueba
5. Iterar sobre el diseño visual
6. Implementar parser de archivos MD
7. Generar todas las tarjetas
8. Crear PDF de impresión

---

*Documento actualizado para usar Python (Pillow + ReportLab)*
*Basado en el proyecto exitoso de Arcadia*
