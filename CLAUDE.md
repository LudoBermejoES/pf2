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

```bash
# Regenerar el índice de búsqueda
python scripts/generate-search-index.py

# Build del sitio Jekyll (desde docs/)
cd docs && bundle exec jekyll build
```

## Terminología PF2e en español

La terminología oficial española está en `docs/_apendices/`. Referencia principal:
- Estados: `docs/_apendices/estados.md`
- Glosario: `docs/_apendices/glosario.md`

## Git

- Rama principal: `main`
- Remote: GitHub Pages (se despliega automáticamente)
- `original/` y `subtitulos/` están en .gitignore
