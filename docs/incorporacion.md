# Plan de Incorporacion: Player Core 2 a la Web de PF2

Este documento detalla el plan completo para integrar el contenido de **Pathfinder Player Core 2** en la estructura existente de documentacion de Pathfinder 2 Player Core.

---

## Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Sistema de Marcado de Fuentes](#sistema-de-marcado-de-fuentes)
3. [Ascendencias](#ascendencias)
4. [Clases](#clases)
5. [Arquetipos](#arquetipos)
6. [Dotes](#dotes)
7. [Conjuros](#conjuros)
8. [Tesoros y Equipo](#tesoros-y-equipo)
9. [Modificaciones en Navegacion](#modificaciones-en-navegacion)
10. [Resumen de Ficheros](#resumen-de-ficheros)
11. [Orden de Implementacion Recomendado](#orden-de-implementacion-recomendado)

---

## Resumen Ejecutivo

### Estadisticas Actuales

| Seccion | Archivos Actuales | Archivos PC2 | Total Estimado |
|---------|-------------------|--------------|----------------|
| Ascendencias | 43 | ~35 | ~78 |
| Clases | 48 | ~30 | ~78 |
| Arquetipos | 9 (multiclase) | ~45 | ~54 |
| Dotes | 131 | ~60 | ~191 |
| Conjuros | 343 | ~150 | ~493 |
| Tesoros/Equipo | 174 | ~200+ | ~374+ |
| **TOTAL** | **748** | **~520** | **~1268** |

### Contenido Nuevo de Player Core 2

- **8 ascendencias nuevas**: Catfolk, Hobgoblin, Kholo, Kobold, Lizardfolk, Ratfolk, Tengu, Tripkee
- **3 herencias versatiles nuevas**: Dhampir, Sangre de Dragon, Caminante del Ocaso
- **9 clases**: Alquimista, Barbaro, Campeon, Espadachin, Hechicero, Investigador, Monje, Oraculo, Familiares
- **39 arquetipos**: 8 multiclase + 31 otros
- **~60 dotes nuevas**: Generales y de habilidad
- **~150 conjuros nuevos**: En las 4 tradiciones + foco + rituales
- **~200+ objetos de tesoro**: Alquimia, armas, armaduras, objetos magicos, trampas

---

## Sistema de Marcado de Fuentes

### Propuesta: Campo `source` en Frontmatter

Para diferenciar el contenido de Player Core 1 y Player Core 2, se propone anadir un campo `source` al frontmatter de cada archivo.

#### Formato del Campo

```yaml
---
layout: page
permalink: /ascendencias/catfolk/
title: Catfolk
chapter: Ascendencias
category: ascendencias
source: PC2  # NUEVO CAMPO
nav_order: 9
---
```

#### Valores Posibles

| Valor | Significado |
|-------|-------------|
| `PC1` | Player Core 1 (contenido existente) |
| `PC2` | Player Core 2 (contenido nuevo) |
| `PC1+PC2` | Contenido presente en ambos libros (si aplica) |

### Implementacion Visual

#### Opcion A: Badge/Etiqueta en el Titulo

Modificar `_layouts/page.html` para mostrar una etiqueta visual:

```html
<h1>{{ page.title }}
  {% if page.source == 'PC2' %}
    <span class="source-badge pc2">PC2</span>
  {% elsif page.source == 'PC1' %}
    <span class="source-badge pc1">PC1</span>
  {% endif %}
</h1>
```

#### Opcion B: Icono en la Navegacion

Modificar `_includes/sidebar.html` para mostrar iconos:

```html
<span class="nav-title">{{ item.title }}
  {% if item.source == 'PC2' %} 📗{% endif %}
</span>
```

#### CSS Propuesto

```css
.source-badge {
  font-size: 0.6em;
  padding: 2px 6px;
  border-radius: 4px;
  vertical-align: middle;
  margin-left: 8px;
}
.source-badge.pc1 {
  background-color: #e3f2fd;
  color: #1565c0;
}
.source-badge.pc2 {
  background-color: #e8f5e9;
  color: #2e7d32;
}
```

### Ficheros a Modificar para el Sistema de Marcado

| Fichero | Cambio |
|---------|--------|
| `_layouts/page.html` | Anadir renderizado de badge de source |
| `_layouts/spell.html` | Anadir renderizado de badge de source |
| `_layouts/ancestry.html` | Anadir renderizado de badge de source |
| `_layouts/class.html` | Anadir renderizado de badge de source |
| `assets/css/main.css` | Anadir estilos para badges |
| `_includes/sidebar.html` | Opcional: iconos en navegacion |

### Tarea de Retroalimentacion

Anadir `source: PC1` a todos los archivos existentes (748 archivos). Esto puede hacerse con un script:

```bash
# Script para anadir source: PC1 a archivos existentes
find docs/_* -name "*.md" -exec sed -i '' 's/^---$/---\nsource: PC1/' {} \;
```

---

## Ascendencias

### Nuevas Ascendencias (8)

Cada ascendencia requiere crear una carpeta con 3-4 archivos.

#### Estructura por Ascendencia

```
_ascendencias/
├── catfolk/
│   ├── index.md          # Descripcion principal
│   ├── descripcion.md    # Descripcion fisica, sociedad, nombres (opcional, puede ir en index)
│   ├── herencias.md      # Herencias de la ascendencia
│   └── dotes.md          # Dotes de ascendencia
├── hobgoblin/
│   ├── index.md
│   ├── herencias.md
│   └── dotes.md
├── kholo/
│   └── [...]
├── kobold/
│   └── [...]
├── lizardfolk/
│   └── [...]
├── ratfolk/
│   └── [...]
├── tengu/
│   └── [...]
└── tripkee/
    └── [...]
```

#### Ficheros a Crear: Ascendencias

| Ascendencia | Archivos a Crear | Source |
|-------------|------------------|--------|
| Catfolk | `catfolk/index.md`, `catfolk/herencias.md`, `catfolk/dotes.md` | PC2 |
| Hobgoblin | `hobgoblin/index.md`, `hobgoblin/herencias.md`, `hobgoblin/dotes.md` | PC2 |
| Kholo | `kholo/index.md`, `kholo/herencias.md`, `kholo/dotes.md` | PC2 |
| Kobold | `kobold/index.md`, `kobold/herencias.md`, `kobold/dotes.md` | PC2 |
| Lizardfolk | `lizardfolk/index.md`, `lizardfolk/herencias.md`, `lizardfolk/dotes.md` | PC2 |
| Ratfolk | `ratfolk/index.md`, `ratfolk/herencias.md`, `ratfolk/dotes.md` | PC2 |
| Tengu | `tengu/index.md`, `tengu/herencias.md`, `tengu/dotes.md` | PC2 |
| Tripkee | `tripkee/index.md`, `tripkee/herencias.md`, `tripkee/dotes.md` | PC2 |

**Total: 24 archivos nuevos**

#### Ejemplo de Frontmatter para Ascendencia

```yaml
---
layout: page
permalink: /ascendencias/catfolk/
title: Catfolk
chapter: Ascendencias
category: ascendencias
source: PC2
nav_order: 9
ancestry: Catfolk
rarity: uncommon
---
```

### Nuevas Herencias Versatiles (3)

Se anaden a la carpeta existente `_ascendencias/herencias-versatiles/`.

#### Ficheros a Crear: Herencias Versatiles

| Herencia | Archivo a Crear | Source |
|----------|-----------------|--------|
| Dhampir | `herencias-versatiles/dhampir.md` | PC2 |
| Sangre de Dragon | `herencias-versatiles/sangre-dragon.md` | PC2 |
| Caminante del Ocaso | `herencias-versatiles/caminante-ocaso.md` | PC2 |

**Total: 3 archivos nuevos**

### Ficheros a Modificar: Ascendencias

| Fichero | Cambio |
|---------|--------|
| `_ascendencias/index.md` | Anadir enlaces a las 8 nuevas ascendencias |
| `_ascendencias/herencias-versatiles/index.md` | Anadir enlaces a las 3 nuevas herencias |
| `_ascendencias/bagajes.md` | Revisar si hay bagajes nuevos de PC2 |

---

## Clases

### Nuevas Clases (9)

Player Core 2 introduce 9 clases completas que no estan en Player Core 1.

#### Estructura por Clase

```
_clases/
├── alquimista/
│   ├── index.md              # Descripcion, estadisticas, competencias
│   ├── caracteristicas.md    # Caracteristicas de clase por nivel
│   └── dotes.md              # Dotes de clase
├── barbaro/
│   ├── index.md
│   ├── caracteristicas.md
│   ├── dotes.md
│   └── instintos.md          # Instintos (subclases)
├── campeon/
│   └── [...]
├── espadachin/
│   └── [...]
├── hechicero/
│   ├── index.md
│   ├── caracteristicas.md
│   ├── dotes.md
│   └── linajes.md            # Linajes de hechicero
├── investigador/
│   └── [...]
├── monje/
│   └── [...]
├── oraculo/
│   ├── index.md
│   ├── caracteristicas.md
│   ├── dotes.md
│   └── misterios.md          # Misterios de oraculo
└── familiares/
    └── descripcion.md        # Reglas de familiares actualizadas
```

#### Ficheros a Crear: Clases

| Clase | Archivos a Crear | Archivos Especiales | Source |
|-------|------------------|---------------------|--------|
| Alquimista | `index.md`, `caracteristicas.md`, `dotes.md` | `campos-investigacion.md` | PC2 |
| Barbaro | `index.md`, `caracteristicas.md`, `dotes.md` | `instintos.md` | PC2 |
| Campeon | `index.md`, `caracteristicas.md`, `dotes.md` | `causas.md`, `dominios.md` | PC2 |
| Espadachin | `index.md`, `caracteristicas.md`, `dotes.md` | `estilos.md` | PC2 |
| Hechicero | `index.md`, `caracteristicas.md`, `dotes.md` | `linajes.md` | PC2 |
| Investigador | `index.md`, `caracteristicas.md`, `dotes.md` | `metodologias.md` | PC2 |
| Monje | `index.md`, `caracteristicas.md`, `dotes.md` | — | PC2 |
| Oraculo | `index.md`, `caracteristicas.md`, `dotes.md` | `misterios.md` | PC2 |

**Total: ~32 archivos nuevos**

#### Ejemplo de Frontmatter para Clase

```yaml
---
layout: page
permalink: /clases/barbaro/
title: Barbaro
chapter: Clases
category: clases
source: PC2
nav_order: 10
class_name: Barbaro
key_ability: Fuerza
hp: 12
---
```

### Nuevos Arquetipos Multiclase (8)

Se anaden a la carpeta existente `_clases/arquetipos/multiclase/`.

#### Ficheros a Crear: Arquetipos Multiclase

| Arquetipo | Archivo a Crear | Source |
|-----------|-----------------|--------|
| Alquimista | `multiclase/alquimista.md` | PC2 |
| Barbaro | `multiclase/barbaro.md` | PC2 |
| Campeon | `multiclase/campeon.md` | PC2 |
| Espadachin | `multiclase/espadachin.md` | PC2 |
| Hechicero | `multiclase/hechicero.md` | PC2 |
| Investigador | `multiclase/investigador.md` | PC2 |
| Monje | `multiclase/monje.md` | PC2 |
| Oraculo | `multiclase/oraculo.md` | PC2 |

**Total: 8 archivos nuevos**

### Ficheros a Modificar: Clases

| Fichero | Cambio |
|---------|--------|
| `_clases/index.md` | Anadir enlaces a las 9 nuevas clases |
| `_clases/arquetipos/index.md` | Actualizar con info de arquetipos PC2 |
| `_clases/arquetipos/multiclase/index.md` | Crear o actualizar con 8 arquetipos nuevos |
| `_clases/companeros/familiares.md` | Actualizar con reglas de PC2 |

---

## Arquetipos

### Nuevos Arquetipos (31 no-multiclase)

Player Core 2 incluye 31 arquetipos que no son de multiclase.

#### Nueva Estructura de Carpetas

```
_clases/arquetipos/
├── index.md                    # Indice general (existente)
├── introduccion.md             # Reglas de arquetipos (existente)
├── multiclase/                 # Existente
│   └── [...]
└── otros/                      # NUEVA CARPETA
    ├── index.md                # Indice de arquetipos no-multiclase
    ├── acrobata.md
    ├── arqueologo.md
    ├── arquero.md
    ├── asesino.md
    ├── baluarte.md
    ├── maestro-bestias.md
    ├── bendecido.md
    ├── cazarrecompensas.md
    ├── caballero.md
    ├── celebridad.md
    ├── dandi.md
    ├── guerrero-dos-armas.md
    ├── duelista.md
    ├── arquero-mistico.md
    ├── maestro-familiares.md
    ├── gladiador.md
    ├── herborista.md
    ├── linguista.md
    ├── mariscal.md
    ├── artista-marcial.md
    ├── demoledor.md
    ├── medico.md
    ├── pirata.md
    ├── envenenador.md
    ├── ritualista.md
    ├── explorador.md
    ├── embaucador-pergaminos.md
    ├── buscavidas.md
    ├── centinela.md
    ├── fabricante-trampas.md
    ├── aficionado-talismanes.md
    ├── vigilante.md
    ├── vikingo.md
    ├── improvisador-armas.md
    └── luchador.md
```

#### Lista Completa de Arquetipos a Crear

| # | Arquetipo | Archivo | Source |
|---|-----------|---------|--------|
| 1 | Acrobata | `otros/acrobata.md` | PC2 |
| 2 | Arqueologo | `otros/arqueologo.md` | PC2 |
| 3 | Arquero | `otros/arquero.md` | PC2 |
| 4 | Asesino | `otros/asesino.md` | PC2 |
| 5 | Baluarte | `otros/baluarte.md` | PC2 |
| 6 | Maestro de Bestias | `otros/maestro-bestias.md` | PC2 |
| 7 | Bendecido | `otros/bendecido.md` | PC2 |
| 8 | Cazarrecompensas | `otros/cazarrecompensas.md` | PC2 |
| 9 | Caballero | `otros/caballero.md` | PC2 |
| 10 | Celebridad | `otros/celebridad.md` | PC2 |
| 11 | Dandi | `otros/dandi.md` | PC2 |
| 12 | Guerrero de Dos Armas | `otros/guerrero-dos-armas.md` | PC2 |
| 13 | Duelista | `otros/duelista.md` | PC2 |
| 14 | Arquero Mistico | `otros/arquero-mistico.md` | PC2 |
| 15 | Maestro de Familiares | `otros/maestro-familiares.md` | PC2 |
| 16 | Gladiador | `otros/gladiador.md` | PC2 |
| 17 | Herborista | `otros/herborista.md` | PC2 |
| 18 | Linguista | `otros/linguista.md` | PC2 |
| 19 | Mariscal | `otros/mariscal.md` | PC2 |
| 20 | Artista Marcial | `otros/artista-marcial.md` | PC2 |
| 21 | Demoledor | `otros/demoledor.md` | PC2 |
| 22 | Medico | `otros/medico.md` | PC2 |
| 23 | Pirata | `otros/pirata.md` | PC2 |
| 24 | Envenenador | `otros/envenenador.md` | PC2 |
| 25 | Ritualista | `otros/ritualista.md` | PC2 |
| 26 | Explorador | `otros/explorador.md` | PC2 |
| 27 | Embaucador de Pergaminos | `otros/embaucador-pergaminos.md` | PC2 |
| 28 | Buscavidas | `otros/buscavidas.md` | PC2 |
| 29 | Centinela | `otros/centinela.md` | PC2 |
| 30 | Fabricante de Trampas | `otros/fabricante-trampas.md` | PC2 |
| 31 | Aficionado a Talismanes | `otros/aficionado-talismanes.md` | PC2 |
| 32 | Vigilante | `otros/vigilante.md` | PC2 |
| 33 | Vikingo | `otros/vikingo.md` | PC2 |
| 34 | Improvisador de Armas | `otros/improvisador-armas.md` | PC2 |
| 35 | Luchador | `otros/luchador.md` | PC2 |

**Total: 36 archivos nuevos (35 arquetipos + 1 index)**

#### Ejemplo de Frontmatter para Arquetipo

```yaml
---
layout: page
permalink: /clases/arquetipos/otros/acrobata/
title: Acrobata
chapter: Clases
category: arquetipos
source: PC2
archetype_type: other
---
```

---

## Dotes

### Nuevas Dotes Generales (11)

Dotes que no requieren entrenamiento en una habilidad especifica.

#### Ficheros a Crear: Dotes Generales

| Dote | Archivo | Nivel | Source |
|------|---------|-------|--------|
| Reparacion Improvisada | `generales/reparacion-improvisada.md` | 3 | PC2 |
| Seguidor Perspicaz | `generales/seguidor-perspicaz.md` | 3 | PC2 |
| Acelerar el Paso | `generales/acelerar-paso.md` | 3 | PC2 |
| Salud Robusta | `generales/salud-robusta.md` | 3 | PC2 |
| Busqueda Exhaustiva | `generales/busqueda-exhaustiva.md` | 3 | PC2 |
| Insensible a la Muerte | `generales/insensible-muerte.md` | 7 | PC2 |
| Supercatador | `generales/supercatador.md` | 7 | PC2 |
| Un Hogar en Cada Puerto | `generales/hogar-cada-puerto.md` | 11 | PC2 |
| Lider de Caravana | `generales/lider-caravana.md` | 11 | PC2 |
| Explorador Increible | `generales/explorador-increible.md` | 11 | PC2 |
| Percepcion Verdadera | `generales/percepcion-verdadera.md` | 19 | PC2 |

**Total: 11 archivos nuevos**

### Nuevas Dotes de Habilidad (~50)

Organizadas por habilidad.

#### Estructura Propuesta

```
_dotes/
├── habilidad/
│   ├── [dotes existentes...]
│   └── [dotes nuevas de PC2...]
```

#### Ficheros a Crear: Dotes de Habilidad

| Habilidad | Dotes Nuevas | Archivos |
|-----------|--------------|----------|
| Variables | 7 | `asistencia-armadura.md`, `identificacion-asegurada.md`, `investigacion-discreta.md`, `ojos-ciudad.md`, `presa-escurridiza.md`, `consultar-espiritus.md`, `robo-acrobatico.md` |
| Acrobacias | 4 | `interprete-acrobatico.md`, `aterrizaje-rodante.md`, `trabajo-equipo-acrobatico.md`, `maestria-aerobatica.md` |
| Atletismo | 2 | `escalador-guia.md`, `carrera-acuatica.md` |
| Artesania | 5 | `tasacion-artesano.md`, `improvisar-herramienta.md`, `fabricacion-trampas.md`, `fijacion-rapida.md`, `artesania-signatura.md` |
| Engano | 3 | `disfraz-respaldo.md`, `sembrar-rumor.md`, `doble-sentido.md` |
| Diplomacia | 2 | `buen-dicho.md`, `evangelizar.md` |
| Intimidacion | 1 | `resistencia-aterradora.md` |
| Saber | 1 | `planificador-batalla.md` |
| Medicina | 3 | `perspicacia-forense.md`, `inoculacion.md`, `cirugia-arriesgada.md` |
| Naturaleza | 2 | `jinete-expres.md`, `influenciar-naturaleza.md` |
| Ocultismo | 3 | `adoracion-enganosa.md`, `magia-raiz.md`, `conocimiento-perturbador.md` |
| Interpretacion | 1 | `interpretacion-distraccion.md` |
| Religion | 3 | `simbolo-peregrino.md`, `exhortar-fieles.md`, `santificar-agua.md` |
| Sociedad | 5 | `ojo-numeros.md`, `leer-contenidos.md`, `aprovechar-conexiones.md`, `red-clandestina.md`, `ojo-biografico.md` |
| Sigilo | 2 | `sigilo-blindado.md`, `marcar-sombra.md` |
| Supervivencia | 1 | `guia-ambiental.md` |

**Total: ~45 archivos nuevos**

### Ficheros a Modificar: Dotes

| Fichero | Cambio |
|---------|--------|
| `_dotes/index.md` | Anadir seccion de dotes de PC2 |
| `_dotes/tabla.md` | Actualizar tabla con dotes nuevas |
| `_dotes/generales/index.md` | Crear si no existe, listar dotes generales PC2 |
| `_dotes/habilidad/index.md` | Crear si no existe, listar dotes habilidad PC2 |

---

## Conjuros

### Nuevos Conjuros (~150)

Player Core 2 incluye numerosos conjuros nuevos organizados alfabeticamente.

#### Estructura de Carpetas

```
_conjuros/
├── spell-individual/           # Existente - anadir conjuros nuevos aqui
│   ├── [conjuros existentes...]
│   └── [conjuros nuevos de PC2...]
├── listas/                     # Actualizar listas existentes
│   ├── arcana.md
│   ├── divina.md
│   ├── oculta.md
│   └── primigenia.md
├── conjuros-foco/              # Anadir nuevos conjuros de foco
│   ├── [clases existentes...]
│   ├── campeon.md              # NUEVO
│   ├── hechicero.md            # NUEVO
│   ├── monje.md                # NUEVO
│   └── oraculo.md              # NUEVO
└── rituales/                   # Anadir nuevos rituales
    └── [rituales nuevos...]
```

#### Conjuros Nuevos Identificados (muestra)

De `original/player_core_2_es/05-hechizos/conjuros/a-c.md`:

| Conjuro | Nivel | Tradiciones | Source |
|---------|-------|-------------|--------|
| Vision Animal | 3 | Primigenia | PC2 |
| Asalto Animado | 2 | Arcana, Oculta | PC2 |
| Suelo Ungido | 3 | Divina | PC2 |
| Maldicion Bestial | 4 | Arcana, Oculta, Primigenia | PC2 |
| Manto de Estrellas | 6 | Oculta, Primigenia | PC2 |
| Furia Cegadora | 6 | Divina, Oculta, Primigenia | PC2 |
| Ampollas | 5 | Arcana, Oculta, Primigenia | PC2 |
| Invectiva Abrasadora | 2 | Oculta | PC2 |
| Megafono | Truco | Arcana, Divina, Oculta | PC2 |
| Plataforma de Carga | 1 | Arcana, Oculta | PC2 |
| Abrigo Camaleonico | 5 | Primigenia | PC2 |
| Impetu Caritativo | 2 | Arcana, Divina, Oculta | PC2 |
| Rociada Gelida | 1 | Arcana, Primigenia | PC2 |
| Drenaje de Croma | 4 | Oculta | PC2 |
| Capa de Colores | 5 | Arcana, Oculta | PC2 |
| Transposicion Colectiva | 6 | Arcana, Oculta | PC2 |
| Coro Concordante | 1 | Divina, Oculta | PC2 |
| Colores Confusos | 8 | Arcana, Oculta | PC2 |
| Contencion | 4 | Arcana, Oculta | PC2 |
| Fango Corrosivo | 5 | Arcana, Primigenia | PC2 |
| Ojos Innumerables | 4 | Arcana, Oculta, Primigenia | PC2 |
| Ola Rompiente | 3 | Arcana, Primigenia | PC2 |
| Maldicion del Tiempo Perdido | 3 | Arcana, Oculta, Primigenia | PC2 |

**Estimado total: ~100-150 conjuros nuevos**

#### Ficheros a Crear: Conjuros

Cada conjuro nuevo necesita su propio archivo en `spell-individual/`:

```yaml
---
layout: spell
permalink: /conjuros/vision-animal/
title: Vision Animal
chapter: Conjuros
spell_level: 3
source: PC2
---
```

#### Conjuros de Foco Nuevos (4 clases)

| Clase | Archivo | Cantidad Estimada |
|-------|---------|-------------------|
| Campeon | `conjuros-foco/campeon.md` | ~8 conjuros |
| Hechicero | `conjuros-foco/hechicero.md` | ~15 conjuros |
| Monje | `conjuros-foco/monje.md` | ~8 conjuros |
| Oraculo | `conjuros-foco/oraculo.md` | ~12 conjuros |

#### Rituales Nuevos (13)

| Ritual | Source |
|--------|--------|
| Vinculo del Corazon | PC2 |
| Engatusar | PC2 |
| Custodios Fantasmales | PC2 |
| Reencarnar | PC2 |
| Descanso Eterno | PC2 |
| Doble Sombrio | PC2 |
| Proyeccion Astral | PC2 |
| Brebaje Fortificante | PC2 |
| Dominio Protector | PC2 |
| Llamada de Reunion | PC2 |
| Circulo de Teletransportacion | PC2 |
| Clon | PC2 |
| Fachada Fantastica | PC2 |

### Ficheros a Modificar: Conjuros

| Fichero | Cambio |
|---------|--------|
| `_conjuros/index.md` | Actualizar con info de PC2 |
| `_conjuros/listas/arcana.md` | Anadir conjuros nuevos |
| `_conjuros/listas/divina.md` | Anadir conjuros nuevos |
| `_conjuros/listas/oculta.md` | Anadir conjuros nuevos |
| `_conjuros/listas/primigenia.md` | Anadir conjuros nuevos |
| `_conjuros/conjuros-de-foco.md` | Actualizar con 4 clases nuevas |

---

## Tesoros y Equipo

### Nueva Seccion: Tesoros

Player Core 2 introduce una seccion completa de tesoro que expande significativamente el equipo.

#### Estructura Propuesta

```
_equipo/
├── [estructura existente...]
├── alquimia/                   # NUEVA CARPETA
│   ├── index.md
│   ├── bombas/
│   │   ├── frasco-acido.md
│   │   ├── fuego-alquimista.md
│   │   └── [...]
│   ├── elixires/
│   │   ├── antidoto.md
│   │   ├── elixir-guepardo.md
│   │   └── [...]
│   ├── mutagenos/
│   │   ├── bestial.md
│   │   ├── cognitivo.md
│   │   └── [...]
│   ├── venenos/
│   │   └── [...]
│   └── herramientas/
│       └── [...]
├── objetos-magicos/            # NUEVA CARPETA
│   ├── index.md
│   ├── permanentes/
│   │   └── [...]
│   ├── consumibles/
│   │   ├── pociones/
│   │   ├── aceites/
│   │   ├── talismanes/
│   │   └── municiones/
│   ├── bastones/
│   │   └── [...]
│   └── varitas/
│       └── [...]
└── trampas/                    # NUEVA CARPETA
    ├── index.md
    ├── reglas.md
    └── [trampas individuales...]
```

### Alquimia

El archivo `original/player_core_2_es/06-tesoro/alquimia.md` contiene ~1700 lineas con:

- **Bombas**: Frasco de acido, Fuego de alquimista, Piedra explosiva, etc.
- **Elixires**: Antidoto, Elixir del guepardo, Elixir de ojo de aguila, etc.
- **Mutagenos**: Bestial, Cognitivo, Corazon de draco, etc.
- **Venenos**: Arsenico, Veneno de ciempies gigante, etc.
- **Herramientas alquimicas**: Tinte forense, Vara luminosa, etc.

**Estimado: ~80-100 objetos alquimicos**

### Objetos Magicos

Los archivos de tesoro contienen miles de lineas de objetos:

- `magia-momentanea.md`: Consumibles magicos
- `objetos-de-poder.md`: Objetos permanentes
- `armaduras-y-armamentos.md`: Armaduras y armas magicas especiales

**Estimado: ~150-200 objetos magicos**

### Trampas

El archivo `trampas.md` contiene reglas completas y ejemplos de trampas.

**Contenido**: Reglas de creacion, uso, y ~20 trampas de ejemplo

### Ficheros a Crear: Tesoros (Resumen)

| Categoria | Archivos Estimados |
|-----------|-------------------|
| Alquimia | ~80 |
| Objetos Magicos Permanentes | ~60 |
| Consumibles | ~40 |
| Bastones y Varitas | ~20 |
| Trampas | ~25 |
| **Total** | **~225** |

---

## Modificaciones en Navegacion

### Archivo `_data/navigation.yml`

#### Cambios en Seccion Ascendencias

```yaml
sidebar:
  ascendencias:
    title: Ascendencias
    items:
      # Existentes (PC1)
      - title: "Elfo"
        url: /ascendencias/elfo/
        source: PC1
      # [...otras existentes...]

      # Nuevas (PC2)
      - title: "---"
      - title: "Catfolk"
        url: /ascendencias/catfolk/
        source: PC2
      - title: "Hobgoblin"
        url: /ascendencias/hobgoblin/
        source: PC2
      - title: "Kholo"
        url: /ascendencias/kholo/
        source: PC2
      - title: "Kobold"
        url: /ascendencias/kobold/
        source: PC2
      - title: "Lizardfolk"
        url: /ascendencias/lizardfolk/
        source: PC2
      - title: "Ratfolk"
        url: /ascendencias/ratfolk/
        source: PC2
      - title: "Tengu"
        url: /ascendencias/tengu/
        source: PC2
      - title: "Tripkee"
        url: /ascendencias/tripkee/
        source: PC2

      # Herencias Versatiles actualizadas
      - title: "Herencias Versatiles"
        url: /ascendencias/herencias-versatiles/
        sub_items:
          - title: "Changeling"
            url: /ascendencias/herencias-versatiles/changeling/
            source: PC1
          - title: "Nefilim"
            url: /ascendencias/herencias-versatiles/nefilim/
            source: PC1
          - title: "Ascendencia Mixta"
            url: /ascendencias/herencias-versatiles/ascendencia-mixta/
            source: PC1
          - title: "Dhampir"
            url: /ascendencias/herencias-versatiles/dhampir/
            source: PC2
          - title: "Sangre de Dragon"
            url: /ascendencias/herencias-versatiles/sangre-dragon/
            source: PC2
          - title: "Caminante del Ocaso"
            url: /ascendencias/herencias-versatiles/caminante-ocaso/
            source: PC2
```

#### Cambios en Seccion Clases

```yaml
  clases:
    title: Clases
    items:
      # Existentes (PC1)
      - title: "Bardo"
        url: /clases/bardo/
        source: PC1
      # [...otras existentes...]

      # Nuevas (PC2)
      - title: "---"
      - title: "Alquimista"
        url: /clases/alquimista/
        source: PC2
      - title: "Barbaro"
        url: /clases/barbaro/
        source: PC2
      - title: "Campeon"
        url: /clases/campeon/
        source: PC2
      - title: "Espadachin"
        url: /clases/espadachin/
        source: PC2
      - title: "Hechicero"
        url: /clases/hechicero/
        source: PC2
      - title: "Investigador"
        url: /clases/investigador/
        source: PC2
      - title: "Monje"
        url: /clases/monje/
        source: PC2
      - title: "Oraculo"
        url: /clases/oraculo/
        source: PC2

      # Arquetipos actualizados
      - title: "Arquetipos"
        url: /clases/arquetipos/
        sub_items:
          - title: "Multiclase"
            url: /clases/arquetipos/multiclase/
          - title: "Otros Arquetipos"
            url: /clases/arquetipos/otros/
            source: PC2
```

#### Nueva Seccion Tesoros

```yaml
  tesoros:
    title: Tesoros
    items:
      - title: "Introduccion"
        url: /equipo/tesoros/
        source: PC2
      - title: "Alquimia"
        url: /equipo/alquimia/
        source: PC2
        sub_items:
          - title: "Bombas"
            url: /equipo/alquimia/bombas/
          - title: "Elixires"
            url: /equipo/alquimia/elixires/
          - title: "Mutagenos"
            url: /equipo/alquimia/mutagenos/
          - title: "Venenos"
            url: /equipo/alquimia/venenos/
      - title: "Objetos Magicos"
        url: /equipo/objetos-magicos/
        source: PC2
      - title: "Trampas"
        url: /equipo/trampas/
        source: PC2
```

---

## Resumen de Ficheros

### Ficheros a CREAR (Total Estimado: ~520)

| Seccion | Cantidad | Ejemplo de Ruta |
|---------|----------|-----------------|
| Ascendencias (8 nuevas) | 24 | `_ascendencias/catfolk/index.md` |
| Herencias Versatiles (3 nuevas) | 3 | `_ascendencias/herencias-versatiles/dhampir.md` |
| Clases (9 nuevas) | ~32 | `_clases/barbaro/index.md` |
| Arquetipos Multiclase (8) | 8 | `_clases/arquetipos/multiclase/barbaro.md` |
| Arquetipos Otros (31+1) | 36 | `_clases/arquetipos/otros/acrobata.md` |
| Dotes Generales | 11 | `_dotes/generales/reparacion-improvisada.md` |
| Dotes Habilidad | ~45 | `_dotes/habilidad/buen-dicho.md` |
| Conjuros Individuales | ~150 | `_conjuros/spell-individual/vision-animal.md` |
| Conjuros Foco | 4 | `_conjuros/conjuros-foco/campeon.md` |
| Rituales | 13 | `_conjuros/rituales/clon.md` |
| Alquimia | ~80 | `_equipo/alquimia/bombas/frasco-acido.md` |
| Objetos Magicos | ~100 | `_equipo/objetos-magicos/permanentes/...` |
| Trampas | ~25 | `_equipo/trampas/trampa-fuego.md` |
| **TOTAL** | **~531** | |

### Ficheros a MODIFICAR (Total: ~20)

| Fichero | Tipo de Cambio |
|---------|----------------|
| `_config.yml` | Posible: Anadir coleccion tesoros |
| `_data/navigation.yml` | Anadir todas las entradas nuevas |
| `_layouts/page.html` | Anadir renderizado de source badge |
| `_layouts/spell.html` | Anadir renderizado de source badge |
| `_layouts/ancestry.html` | Anadir renderizado de source badge |
| `_layouts/class.html` | Anadir renderizado de source badge |
| `assets/css/main.css` | Anadir estilos para badges |
| `_includes/sidebar.html` | Opcional: iconos de source |
| `_ascendencias/index.md` | Anadir 8 ascendencias nuevas |
| `_ascendencias/herencias-versatiles/index.md` | Anadir 3 herencias |
| `_clases/index.md` | Anadir 9 clases nuevas |
| `_clases/arquetipos/index.md` | Actualizar con arquetipos nuevos |
| `_dotes/index.md` | Anadir seccion PC2 |
| `_dotes/tabla.md` | Actualizar tabla |
| `_conjuros/index.md` | Actualizar con info PC2 |
| `_conjuros/listas/*.md` (4) | Anadir conjuros nuevos |
| `_conjuros/conjuros-de-foco.md` | Anadir 4 clases |
| `_equipo/index.md` | Anadir seccion tesoros |

### Script de Retroalimentacion para `source: PC1`

Ejecutar sobre todos los 748 archivos existentes para anadir `source: PC1`.

---

## Orden de Implementacion Recomendado

### Fase 1: Infraestructura (Prioridad Alta)

1. **Sistema de marcado de fuentes**
   - Modificar layouts para mostrar badges
   - Anadir CSS para estilos
   - Script para anadir `source: PC1` a archivos existentes

2. **Actualizacion de navegacion**
   - Modificar `_data/navigation.yml`

### Fase 2: Contenido Core (Prioridad Alta)

3. **Ascendencias nuevas** (27 archivos)
   - 8 ascendencias completas
   - 3 herencias versatiles

4. **Clases nuevas** (~40 archivos)
   - 9 clases completas
   - 8 arquetipos multiclase

### Fase 3: Opciones de Personaje (Prioridad Media)

5. **Arquetipos otros** (36 archivos)
   - 31 arquetipos no-multiclase

6. **Dotes nuevas** (~56 archivos)
   - 11 dotes generales
   - ~45 dotes de habilidad

7. **Conjuros** (~170 archivos)
   - ~150 conjuros individuales
   - 4 conjuros de foco
   - 13 rituales
   - Actualizar listas

### Fase 4: Equipo y Tesoros (Prioridad Media-Baja)

8. **Alquimia** (~80 archivos)
   - Bombas, elixires, mutagenos, venenos

9. **Objetos Magicos** (~100 archivos)
   - Permanentes, consumibles, bastones, varitas

10. **Trampas** (~25 archivos)
    - Reglas y trampas individuales

---

## Notas Finales

### Consideraciones de Formato

1. **Mantener consistencia** con el formato existente de frontmatter
2. **Usar slugs en espanol** para las URLs (ej: `/clases/barbaro/` no `/clases/barbarian/`)
3. **Preservar estructura de tablas** igual que en archivos existentes
4. **Usar mismos iconos de acciones**: `◆`, `◆◆`, `◆◆◆`, `◇`

### Herramientas Sugeridas

1. **Scripts de conversion**: Transformar markdown de PC2 al formato de la web
2. **Validador de links**: Verificar que todos los enlaces internos funcionan
3. **Generador de indices**: Crear paginas index automaticamente

### Estimacion de Esfuerzo

| Fase | Archivos | Esfuerzo Estimado |
|------|----------|-------------------|
| Fase 1 | ~20 modif | 1-2 dias |
| Fase 2 | ~67 nuevos | 3-5 dias |
| Fase 3 | ~262 nuevos | 5-8 dias |
| Fase 4 | ~205 nuevos | 4-6 dias |
| **Total** | **~554** | **13-21 dias** |

---

*Documento generado el 2026-02-01*
*Basado en analisis de estructura existente en `docs/` y contenido de `original/player_core_2_es/`*
