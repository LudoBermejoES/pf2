# Claude Code Configuration

## Reglas generales

- Do what has been asked; nothing more, nothing less.
- NEVER create files unless they're absolutely necessary for achieving your goal.
- ALWAYS prefer editing an existing file to creating a new one.
- NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
- Never save working files, text/mds and tests to the root folder.

## Fecha actual

Today's date is 2026-03-03.

## Estructura del proyecto

Este proyecto es un sitio Jekyll estático con documentación de Pathfinder 2e en español.

- `docs/` — Sitio Jekyll (fuente del site)
  - `_ambientacion/` — Páginas de ambientación
  - `_apendices/` — Apéndices (estados, glosario, rasgos)
  - `_ascendencias/` — Páginas de ascendencias
  - `_clases/` — Páginas de clases
  - `_conjuros/` — Conjuros
  - `_data/` — Datos de navegación YAML
  - `_dotes/` — Dotes
  - `_equipo/` — Equipo
  - `_habilidades/` — Habilidades
  - `_includes/` — Plantillas parciales (sidebar.html es la nav lateral)
  - `_layouts/` — Layouts Jekyll
  - `_reglas/` — Reglas del juego
  - `assets/js/search-index.json` — Índice de búsqueda (regenerar con scripts/generate-search-index.py)
- `original/` — Fuentes originales (no en git)
- `scripts/` — Scripts de utilidad Python
- `tools/` — Herramientas de generación de tarjetas

## Navegación del sitio

**IMPORTANTE**: La barra lateral está hardcodeada en `docs/_includes/sidebar.html`. El archivo `docs/_data/nav_*.yml` no se usa para renderizar la nav lateral — hay que editar sidebar.html directamente para añadir enlaces nuevos.

## Scripts útiles

### Índice de búsqueda

```bash
# Regenerar docs/assets/js/search-index.json (hacer después de añadir páginas)
python scripts/generate-search-index.py
```

### Generadores de contenido (`scripts/`)

| Script | Descripción |
|--------|-------------|
| `generate-search-index.py` | Regenera el JSON de búsqueda del sitio |
| `generate-spells-pc2.py` | Genera páginas de conjuros desde PC2 |
| `generate-feats-pc2.py` | Genera páginas de dotes desde PC2 |
| `generate-ancestries-pc2.py` | Genera páginas de ascendencias desde PC2 |
| `generate-magic-items-pc2.py` | Genera páginas de objetos mágicos desde PC2 |
| `generate-alchemy-pc2.py` | Genera páginas de alquimia desde PC2 |
| `generate_rasgos_index.py` | Regenera el índice de rasgos |
| `eliminar_titulos_h1_duplicados.py` | Limpia H1 duplicados en páginas |
| `actualizar_metadatos.py` | Actualiza frontmatter YAML en masa |

### Generadores de cartas físicas (`tools/`)

Cada `tools/<tipo>CardCreator/` sigue el mismo flujo de 3 pasos:

```bash
# Ejemplo completo con dotes:
cd tools/featCardCreator
python parse_feats.py          # 1. Lee los .md → genera data/feats.json
python generate_feat_cards.py  # 2. Genera PNGs en generated_cards/
python insert_card_images.py   # 3. Inserta referencias de imagen en los .md
```

Los mismos pasos aplican a:

| Directorio | Tipo de carta |
|------------|---------------|
| `featCardCreator/` | Dotes (1840+) |
| `spellCardCreator/` | Conjuros (410+) |
| `weaponsCardCreator/` | Armas |
| `armorCardCreator/` | Armaduras |
| `itemCardCreator/` | Objetos |
| `shieldCardCreator/` | Escudos |
| `actionsCardCreator/` | Acciones |
| `traitCardCreator/` | Rasgos |

Requisitos para cartas: `pip install -r tools/featCardCreator/requirements.txt`
(Pillow + PyYAML)

### Build del sitio

```bash
cd docs && bundle exec jekyll build
cd docs && bundle exec jekyll serve  # Servidor local en localhost:4000
```

## Terminología PF2e en español

La terminología oficial española está en `docs/_apendices/`. Referencia principal:
- Estados: `docs/_apendices/estados.md`
- Glosario: `docs/_apendices/glosario.md`

## Git

- Rama principal: `main`
- Remote: GitHub Pages (se despliega automáticamente)
- `original/` y `subtitulos/` están en .gitignore
