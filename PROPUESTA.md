# Propuesta de Reorganización del Sitio PF2e

## Diagnóstico: Problemas Actuales

El sitio tiene **~3.848 artículos** distribuidos en 12 colecciones, lo que lo hace excepcionalmente completo. Sin embargo, la estructura actual arrastra tres problemas de fondo:

### 1. Navegación de un solo nivel: el sidebar monolítico
El sidebar es un bloque HTML enorme (~440 líneas) con condicionales `{% if page.chapter == "X" %}` que se duplican para cada sección. Añadir una entrada nueva implica editar manualmente ese archivo. No escala.

La sección **Cómo Jugar** es la que más sufre esto: tiene contenido en `_reglas/` (acciones, movimiento, daño, estados…) y también en `_reglas/detalle/` (19 artículos de combate, 7 de magia, 7 de personajes…). Visualmente todo aparece como una lista plana sin jerarquía real.

### 2. Dos colecciones que hacen lo mismo
`_reglas/detalle/` y `_videos/` (originalmente `_videos/`) son en realidad artículos de referencia ampliada. Su existencia como colecciones separadas no tiene ventaja técnica: complica la búsqueda, el sidebar y la generación del índice.

### 3. La home no refleja la verdadera utilidad del sitio
La página de inicio muestra 8 cards iguales que repiten la navegación principal. Para alguien que ya conoce el sitio (el uso habitual), no aporta nada. Para alguien nuevo, no orienta sobre qué encontrará en cada sección.

---

## Propuesta

### Parte 1 — Nueva arquitectura de navegación

En lugar de un sidebar diferente por sección, propongo una **navegación de dos niveles** persistente:

```
Barra superior fija (nav principal):
  Personaje | Mundo | Mecánicas | Referencia

Sidebar contextual (según sección):
  Muestra solo el árbol de la sección activa
```

**Agrupación propuesta de las 12 colecciones en 4 bloques:**

#### Bloque "Personaje"
Agrupa todo lo que define a un PJ:
- Introducción
- Ascendencias (+ bagajes + herencias)
- Clases (+ arquetipos + compañeros)
- Habilidades
- Dotes

*Rationale:* Son las secciones que un jugador consulta al crear o avanzar su personaje. Hoy están dispersas en la nav principal pero forman una unidad conceptual.

#### Bloque "Mundo"
Agrupa el lore y la ambientación:
- Ambientación (Golarion, religión, sociedad, regiones)
- Campaña (Kingmaker)

*Rationale:* Estas secciones no afectan mecánicas, son consulta de lore puro.

#### Bloque "Mecánicas"
Agrupa las reglas de juego:
- Cómo Jugar (`_reglas/`) — fusionando el contenido de `detalle/` como subsección
- Equipo (armas, armaduras, objetos mágicos, alquimia)
- Conjuros

*Rationale:* Son las secciones que se consultan durante el juego o la preparación de sesión.

#### Bloque "Referencia"
Agrupa las páginas de consulta rápida:
- Apéndices (glosario, estados, rasgos)
- Búsqueda

*Rationale:* Son páginas a las que se llega desde otras secciones, no se navegan linealmente.

---

### Parte 2 — Sidebar generado por datos

En lugar del sidebar.html monolítico, propongo mover la estructura de navegación a archivos de datos YAML en `_data/`:

```
_data/
  nav_personaje.yml
  nav_mundo.yml
  nav_mecanicas.yml
  nav_referencia.yml
```

Ejemplo de `nav_mecanicas.yml`:
```yaml
- title: Cómo Jugar
  url: /reglas/
  subsections:
    - title: Modos de Juego
      links:
        - { title: Encuentro, url: /reglas/encuentro/ }
        - { title: Exploración, url: /reglas/exploracion/ }
    - title: Acciones
      links:
        - { title: Acciones Básicas, url: /reglas/acciones-basicas/ }
    - title: Combate (Detalle)
      links:
        - { title: Economía de Acciones, url: /reglas/detalle/combate/economia-de-acciones/ }
        - ...
```

El sidebar.html pasa de 440 líneas de HTML hardcoded a un loop de ~20 líneas que itera sobre el YAML de la sección activa. Añadir una entrada nueva = editar un YAML, no el HTML.

---

### Parte 3 — Fusionar `_reglas/detalle/` en `_reglas/`

Los artículos de `detalle/` (combate, magia, personajes, artesanía, peligros) son artículos de reglas normales con más profundidad. No hay razón para que vivan en una subcarpeta conceptualmente separada.

**Propuesta:** mantener la estructura de carpetas pero eliminar el prefijo `detalle/` de las URLs y del sidebar:

```
Actual:    /reglas/detalle/combate/flanqueo/
Propuesto: /reglas/combate/flanqueo/
```

Esto simplifica el sidebar (una sola sección "Combate" en lugar de "Combate" + "Detalle: Combate") y hace las URLs más limpias. Se implementa con redirecciones 301 para no romper enlaces externos.

---

### Parte 4 — Home page orientada al uso real

La home actual tiene 8 cards que duplican la nav. Propuesta de rediseño en dos zonas:

**Zona 1 — Para jugadores (uso frecuente):**
Accesos directos a las consultas más habituales durante el juego:
- Estados de condición (enlace directo al glosario de estados)
- Buscador (prominente, no como botón secundario)
- Acciones básicas de combate

**Zona 2 — Para lectores / nuevos:**
Las 4 rutas narrativas de uso del libro:
- "Crear un personaje" → guía paso a paso (Intro → Ascendencias → Clases → Habilidades)
- "Consultar reglas" → Cómo Jugar
- "Preparar una sesión" → Equipo + Conjuros + Mecánicas
- "Explorar el mundo" → Ambientación

---

### Parte 5 — Breadcrumbs

Dado que la jerarquía llega a 4 niveles (ej: `Mecánicas > Cómo Jugar > Combate > Flanqueo`), añadir breadcrumbs encima del título de cada artículo aportaría mucha orientación sin coste de navegación. Se implementa con Liquid usando `page.url` y `page.chapter`.

---

## Resumen de cambios técnicos

| Cambio | Complejidad | Impacto |
|--------|-------------|---------|
| Mover nav a `_data/*.yml` | Media | Elimina sidebar.html manual; escala solo |
| Fusionar `detalle/` en `_reglas/combate/` etc. | Baja | Sidebar más limpio; URLs más cortas |
| Rediseño home (2 zonas) | Baja | Mejor orientación para nuevos y veteranos |
| Breadcrumbs por nivel | Baja | Orientación en secciones profundas |
| Reagrupar nav principal en 4 bloques | Media | Reduce de 10 a 4 entradas en la nav superior |

## Lo que NO cambiaría

- La estructura de carpetas de las colecciones (está bien organizada)
- El sistema de frontmatter (`chapter`, `category`, `source`)
- Los layouts especializados (`spell.html`, `class.html`, `ancestry.html`)
- El motor de búsqueda (MiniSearch funciona bien)
- Los permalinks de artículos existentes (solo `detalle/` se eliminaría con redirecciones)
