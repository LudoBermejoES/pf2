# Propuesta de Reorganización del Sitio PF2e

## Estado: IMPLEMENTADA ✅

La reorganización de navegación en 4 bloques ha sido implementada.

---

## Diseño implementado

### Navegación de 3 niveles

```
Nivel 1 — Barra superior (4 bloques):
  Personaje | Mundo | Mecánicas | Referencia

Nivel 2 — Página de bloque (/personaje/, /mundo/, etc.):
  Sidebar muestra las secciones del bloque como lista de enlaces

Nivel 3 — Página de sección o artículo:
  Sidebar muestra ◀ (volver al bloque) + título de sección + artículos de esa sección
```

### Decisiones de diseño

- **Clic en bloque de la barra superior** → va a la página índice del bloque (ej. `/personaje/`)
- **Sidebar en bloque**: muestra las secciones principales del bloque
- **Sidebar en artículo**: muestra los artículos de esa categoría (zoom a sección)
- **Navegación hacia atrás**: flecha ◀ en la cabecera del sidebar + breadcrumb sobre el título
- **Frontmatter**: nuevo campo `block` solo en páginas índice de bloque — los artículos usan el `chapter` existente
- **Sin tocar**: `chapter`, `category`, `nav_order`, `source` existentes se mantienen intactos

### Agrupación de secciones en bloques

| Bloque | Secciones |
|--------|-----------|
| **Personaje** | Introducción, Ascendencias, Clases, Habilidades, Dotes |
| **Mundo** | Ambientación, Campaña |
| **Mecánicas** | Cómo Jugar, Equipo, Conjuros |
| **Referencia** | Apéndices (Glosario, Estados, Rasgos) |

---

## Archivos modificados / creados

### Nuevos archivos de datos
- `docs/_data/blocks.yml` — definición de los 4 bloques y sus secciones
- `docs/_data/nav_personaje.yml` — limpiado al formato estándar (solo Introducción)

### Sidebar reescrito
- `docs/_includes/sidebar.html` — ahora data-driven (~100 líneas vs 480 anteriores)
  - Lee `_data/blocks.yml` para encontrar el bloque del `page.chapter`
  - Lee el `nav_*.yml` correspondiente para listar los artículos
  - Muestra flecha ◀ que lleva de vuelta al bloque

### Layout actualizado
- `docs/_layouts/default.html`
  - Top nav itera `site.data.blocks` (4 entradas en lugar de 11)
  - Breadcrumb: `Inicio › Personaje › Ascendencias › Elfo`

### Nuevas páginas índice de bloque
- `docs/personaje/index.html` → `/personaje/`
- `docs/mundo/index.html` → `/mundo/`
- `docs/mecanicas/index.html` → `/mecanicas/`
- `docs/referencia/index.html` → `/referencia/`

### CSS añadido
- `docs/assets/css/main.css` — estilos para `.sidebar-back`, `.sidebar-heading-link`, `.block-badge`, `.nav-links a.active`

---

## Lo que NO se cambió

- Estructura de carpetas de las colecciones
- Frontmatter de artículos existentes (`chapter`, `category`, etc.)
- Layouts especializados (`spell.html`, `class.html`, etc.)
- Motor de búsqueda MiniSearch
- Permalinks de todos los artículos existentes
- Los archivos `nav_*.yml` por sección (se reutilizan como fuente de verdad)

---

## Propuestas pendientes (no implementadas)

### Fusionar `_reglas/detalle/` en `_reglas/`
Eliminar el prefijo `detalle/` de las URLs con redirecciones 301. Baja prioridad.

### Rediseño home
Dos zonas: accesos rápidos para jugadores veteranos (estados, buscador) + rutas narrativas para nuevos.

### Apéndices → Referencia
Las páginas de Apéndices tienen `chapter: "Apéndices"` no asignado a ningún bloque en `blocks.yml`.
El sidebar los mapea a Referencia vía fallback. Para limpiarlo del todo: añadir `block: referencia`
al frontmatter de esas páginas en una segunda pasada.
