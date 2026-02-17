# Feat Card Generator

Generador de cartas de dotes de Pathfinder 2e en formato físico imprimible.

## Características

- **Parse automático**: Extrae datos de 1,840+ archivos markdown de dotes
- **Formato profesional**: Cartas de 63x88mm (300 DPI print quality)
- **Diseño PF2e**: Colores y fuentes oficiales del estilo Pathfinder
- **Campos completos**: Prerrequisitos, requisitos, frecuencia, desencadenante, efectos, resultados
- **Inserción automática**: Agrega las cartas a los archivos markdown

## Requisitos

```bash
pip install -r requirements.txt
```

Requisitos:
- Python 3.8+
- Pillow (PIL) >= 10.0.0
- PyYAML >= 6.0

## Uso

### 1. Parsear dotes desde markdown

```bash
cd tools/featCardCreator
python parse_feats.py
```

Esto genera `data/feats.json` con la información estructurada de todas las dotes.

**Salida esperada:**
```
🔍 Buscando archivos de dotes...
📋 Encontrados 1840 archivos markdown
✅ Parseadas 1840 dotes exitosamente
💾 Datos guardados en data/feats.json

📊 Estadísticas por categoría:
  class: 979
  skill: 154
  ancestry: 313
  archetype: 276
  general: 118
```

### 2. Generar imágenes de cartas

```bash
python generate_feat_cards.py
```

Esto crea archivos PNG en `generated_cards/` para cada dote.

**Salida esperada:**
```
📚 Cargando fuentes...
🎴 Generando 1840 cartas...
✅ Generadas 1840 cartas exitosamente
```

### 3. Insertar cartas en markdown

```bash
# Modo dry-run (sin modificar archivos)
python insert_card_images.py --dry-run

# Inserción real con backup
python insert_card_images.py --backup

# Sin copiar a assets (solo modificar markdown)
python insert_card_images.py --skip-copy
```

**Opciones:**
- `--dry-run`: Vista previa sin modificar archivos
- `--backup`: Crear copias `.md.backup` antes de modificar
- `--skip-copy`: No copiar imágenes a `docs/assets/cards/feats/`

## Script Maestro

Ejecuta todo el pipeline:

```bash
#!/bin/bash
# generate_all_feat_cards.sh

echo "🎴 Generando cartas de dotes..."

echo "1️⃣ Parseando dotes..."
python parse_feats.py || exit 1

echo "2️⃣ Generando imágenes..."
python generate_feat_cards.py || exit 1

echo "3️⃣ Copiando a assets..."
python insert_card_images.py --backup

echo "✅ ¡Completado!"
```

## Estructura de Archivos

```
tools/featCardCreator/
├── assets/
│   ├── fonts/
│   │   ├── Cinzel-Regular.ttf       # Títulos
│   │   └── Oldenburg-Regular.ttf    # Cuerpo de texto
│   └── images/                      # Iconos (futuro)
├── data/
│   └── feats.json                   # Datos parseados
├── generated_cards/                 # PNGs generados
│   ├── paso-elfo.png
│   ├── golpe-preciso.png
│   └── ...
├── parse_feats.py                   # Parser de markdown
├── generate_feat_cards.py           # Generador de imágenes
├── insert_card_images.py            # Insertor en markdown
├── requirements.txt                 # Dependencias Python
└── README.md                        # Esta documentación
```

## Diseño de Carta

### Dimensiones (300 DPI)
- **Tamaño**: 744x1039 px (63x88mm)
- **Zona segura**: 24px (2mm)
- **Radio esquinas**: 30px (2.5mm)
- **Borde**: 8px

### Fuentes
- **Título**: Cinzel 44pt (36pt si es largo)
- **Cuerpo**: Oldenburg 24pt (20pt si es largo)
- **Rasgos**: Oldenburg 17pt
- **Etiquetas**: Oldenburg 20pt

### Colores PF2e
- **Fondo**: RGB(244, 228, 201) - Pergamino
- **Borde**: RGB(125, 68, 55) - Rojo PF
- **Rasgos fondo**: RGB(93, 48, 48) - Rojo oscuro
- **Rasgos texto**: RGB(218, 165, 32) - Dorado
- **Texto**: RGB(45, 39, 34) - Oscuro
- **Título**: RGB(184, 134, 11) - Dorado

### Layout

```
┌─────────────────────────────────────┐
│ ╔═════════════════════════════════╗ │
│ ║  TÍTULO DE LA DOTE              ║ │
│ ╠═════════════════════════════════╣ │
│ ║ ┌────────┐ ┌────────┐ ┌───────┐║ │
│ ║ │ Rasgo1 │ │ Rasgo2 │ │Nivel 5│║ │
│ ║ └────────┘ └────────┘ └───────┘║ │
│ ║ ─────────────────────────────── ║ │
│ ║ Prerrequisitos: ...             ║ │
│ ║ Frecuencia: ...                 ║ │
│ ║ Requisitos: ...                 ║ │
│ ║ Desencadenante: ...             ║ │
│ ║ ─────────────────────────────── ║ │
│ ║ Descripción de la dote con      ║ │
│ ║ texto envuelto automáticamente  ║ │
│ ║ para que quepa en la carta...   ║ │
│ ║                                 ║ │
│ ║ Beneficio: ...                  ║ │
│ ║ Especial: ...                   ║ │
│ ╚═════════════════════════════════╝ │
└─────────────────────────────────────┘
```

## Datos Extraídos

Cada dote incluye:

- `name`: Título
- `level`: Nivel requerido
- `traits`: Lista de rasgos
- `category`: Tipo (class, ancestry, archetype, skill, general)
- `action_type`: Acción ("1", "2", "3", "libre", "reaccion")
- `prerequisites`: Prerrequisitos
- `requirements`: Requisitos (condiciones temporales)
- `trigger`: Desencadenante
- `frequency`: Frecuencia de uso
- `cost`: Coste en recursos
- `effect`: Efecto específico
- `description`: Descripción principal
- `benefit`: Beneficio (si está separado)
- `special`: Texto especial
- `results`: Éxito crítico, éxito, fallo, fallo crítico

## Ejemplo de JSON

```json
{
  "feats": [
    {
      "id": "paso-elfo",
      "name": "Paso elfo",
      "level": 9,
      "traits": ["Elfo"],
      "category": "ancestry",
      "ancestry": "Elfo",
      "action_type": null,
      "description": "Te mueves en una danza grácil, e incluso tus pasos son amplios.",
      "benefit": "Puedes dar un Paso de 5 pies (1,5 m) dos veces.",
      "source_file": "docs/_dotes/elfo/paso-elfo.md"
    }
  ],
  "total": 1840
}
```

## Inserción en Markdown

Las cartas se insertan después del div de rasgos:

```markdown
## Paso elfo

<div class="feat-traits-header" markdown="0">
  <a href="/apendices/rasgos/elfo/" class="feat-trait">Elfo</a>
</div>

<div class="feat-card">
  <img src="/assets/cards/feats/paso-elfo.png" alt="Carta de dote">
</div>

Te mueves en una danza grácil...
```

## CSS para Jekyll

Agregar a `_sass/_feat-cards.scss`:

```scss
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

@media (max-width: 768px) {
  .feat-card {
    max-width: 100%;
    padding: 0 10px;
  }
}

@media print {
  .feat-card img {
    max-width: 300px;
    page-break-inside: avoid;
  }
}
```

## Optimización de Imágenes

Comprimir PNGs después de generar:

```bash
# Optimizar sin pérdida
optipng -o7 generated_cards/*.png

# O con pérdida mínima (mejor compresión)
pngquant --quality=85-95 generated_cards/*.png
```

## Notas

- **Formato homogéneo**: Todos los archivos siguen el mismo formato tras la homogeneización (commit d988a708)
- **Sin líneas legacy**: Se eliminaron 256 líneas `**Dote X**` redundantes
- **Desencadenante estándar**: Todos usan "Desencadenante:" (14 archivos corregidos de "Detonante:")
- **Divs con markdown="0"**: 20 archivos corregidos

## Referencias

- Sistema actual de cartas: `tools/actionsCardCreator/`
- Documentación: `docs/generar_dotes.md`
- Scripts de homogeneización: `scripts/fix-*.js`

## Autor

Generado por Claude Sonnet 4.5 siguiendo la especificación en `docs/generar_dotes.md`
