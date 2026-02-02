# Plan de Incorporación de Ambientación en Ascendencias

## Resumen Ejecutivo

Este documento detalla el plan para integrar el rico contenido de ambientación extraído de la *Guía de los Presagios Perdidos* dentro de las páginas individuales de cada ascendencia del sitio web de Pathfinder 2.

---

## Análisis del Estado Actual

### Estructura Actual de las Ascendencias

Cada ascendencia tiene una estructura similar en `docs/_ascendencias/[ascendencia]/index.md`:

1. **Frontmatter YAML** (layout, permalink, title, chapter, etc.)
2. **Imagen** (float right)
3. **Introducción general** (1-2 párrafos)
4. **Estadísticas** (tabla)
5. **Podrías...** / **Otros probablemente...**
6. **Descripción física**
7. **Sociedad**
8. **Creencias** (edictos/anatemas)
9. **Nombres** (ejemplos)
10. **Selecciones relacionadas** (enlaces a dotes/herencias)

### Contenido de Ambientación Disponible (golarion-presagios.md)

| Ascendencia | Contenido Disponible |
|-------------|---------------------|
| **Humano** | 13 etnias detalladas (Erutaki, Garundi, Keleshita, Kélido, Mwangi, Nidalés, Shoanti, Taldano, Tian, Ulfen, Varisiano, Vudranos, Azlante) + civilizaciones antiguas |
| **Elfo** | 5 etnias (Aiudeen, Ilverani, Mualijae, Juramentados de la Espira, Vourinoi) + historia (Sovyrian, Guerra del Arrasador, Kyonin) |
| **Enano** | 3 grupos principales (Grondaksen, Ergaksen, Holtaksen) + 5 etnias notables + tradición de dagas de clan + Búsqueda del Cielo |
| **Gnomo** | La Decoloración + 4 tipos (Hijos feéricos, Crueles, Brillantes, Llama entusiasta) + 4 enclaves |
| **Goblin** | 4 etnias (Bosque, Escarcha, Mono, Raspadores) + 4 tribus notables + mitos de origen |
| **Mediano** | 6 etnias (Chelaxianos, Jarics, Mihrinis, Othobans, Song'o, Uhlams) + Red de la Campanilla |
| **Semielfo** | 6 etnias derivadas + concepto de Patria del Alma |
| **Semiorco** | Mitos de origen + contexto social + culturas de aceptación |
| **Hobgoblin** | Nación de Oprak + Legión del Colmillo de Hierro |
| **Leshy** | Origen espiritual + conexión con la naturaleza |
| **Iruxi** | Imperios antiguos + tradiciones astrológicas |

---

## Opciones de Implementación

### Opción A: Sección Nueva "Etnias y Culturas" (RECOMENDADA)

**Descripción:** Añadir una nueva sección después de "Sociedad" o "Nombres" en cada página de ascendencia.

**Ventajas:**
- Mantiene la información de ambientación claramente separada de las reglas
- No altera la estructura existente del contenido de PC1
- Fácil de mantener y actualizar
- Los usuarios pueden encontrar rápidamente la información cultural

**Estructura propuesta:**

```markdown
## Etnias y Culturas de Golarion

[Introducción breve sobre la diversidad de la ascendencia]

### [Nombre de Etnia 1]

[Descripción física, cultural, ubicación]

**Nombres típicos:** [ejemplos]

### [Nombre de Etnia 2]
...

> **Ver también:** [Ambientación completa de Golarion](/ambientacion/golarion-presagios/)
```

---

### Opción B: Páginas Separadas de Ambientación

**Descripción:** Crear un archivo `ambientacion.md` dentro de cada carpeta de ascendencia.

**Estructura:** `docs/_ascendencias/humano/ambientacion.md`

**Ventajas:**
- Separación total entre reglas y ambientación
- Páginas más ligeras
- Permite profundidad sin sobrecargar la página principal

**Desventajas:**
- Más archivos que mantener
- Los usuarios deben navegar a otra página
- Puede parecer contenido fragmentado

---

### Opción C: Acordeones/Colapsables

**Descripción:** Usar elementos HTML colapsables para mostrar/ocultar la información de etnias.

**Ventajas:**
- Todo el contenido en una página
- Los usuarios eligen qué leer
- No sobrecarga visualmente

**Desventajas:**
- Requiere modificar CSS/JS
- Puede no funcionar bien con la búsqueda
- Mayor complejidad técnica

---

## Plan de Implementación Detallado (Opción A)

### Fase 1: Humanos (Mayor contenido)

**Archivo:** `docs/_ascendencias/humano/index.md`

**Cambios:**

1. **Expandir la sección "Grupos étnicos"** existente (líneas 69-84) con el contenido completo de cada etnia:
   - Descripción física detallada
   - Historia y cultura
   - Ubicación en Golarion
   - Nombres típicos (masculinos, femeninos, neutros)

2. **Añadir subsecciones para:**
   - Civilizaciones Antiguas (Azlant, Jistka, Shory)
   - La Diáspora Taldana
   - Subgrupos Mwangi (Zenj, Mauxi, Bekyar, Bonuwat, Caldaru)
   - Los Siete Quahs Shoanti (tabla)
   - Etnias Tian (tabla completa)

3. **Eliminar duplicados** en `descripcion.md` (actualmente idéntico a index.md)

**Ejemplo de estructura expandida:**

```markdown
## Grupos Étnicos Humanos

Una gran variedad de grupos étnicos humanos puebla los continentes de la Región del mar Interior de Golarion...

### Erutaki

Los erutaki son un grupo de pueblos que viven en el extremo norte de Golarion, entre los glaciares de la **Corona del Mundo**. Son personas bajas y compactas, con piel color terracota, a menudo curtida por los vientos helados de su tierra natal, y cabello negro y liso.

Muchos erutaki son seminómadas y siguen migraciones de renos o bueyes almizcleros...

**Nombres típicos:** Aklaq, Oki, Tulimak (masculinos); Aluki, Liak, Noayak (femeninos); Amaruq, Miki, Yuka (neutros).

### Garundi
...
```

---

### Fase 2: Elfos

**Archivo:** `docs/_ascendencias/elfo/index.md`

**Contenido a añadir:**

1. **Nueva sección "Historia Élfica"** después de "Sociedad":
   - Llegada desde Sovyrian
   - Piedra de Sovyrian
   - Conflicto con los alghollthus
   - Gran Caída y exilio
   - Regreso en 2632 ra
   - Guerra contra el Arrasador de Árboles

2. **Nueva sección "Kyonin"**:
   - Nación élfica principal
   - Reina Telandia Edasseril
   - Apertura de fronteras

3. **Nueva sección "Etnias Élficas"**:
   - Aiudeen (Los Retornados)
   - Ilverani (Elfos Nivales) + Oradores del Crepúsculo
   - Mualijae (Elfos de la Jungla) + Alijae, Ekujae, Kallijae
   - Juramentados de la Espira (incluyendo sus máscaras y comportamiento único)
   - Vourinoi (Elfos de los Oasis) + concepto de kala-shei y el Brillo

---

### Fase 3: Enanos

**Archivo:** `docs/_ascendencias/enano/index.md` (necesita crearse si no existe, o expandir herencias.md)

**Contenido a añadir:**

1. **Nueva sección "La Búsqueda del Cielo"**:
   - Origen subterráneo
   - Visión oracular
   - Viaje hacia la superficie
   - Rey Taargick y las Ciudadelas Celestes

2. **Nueva sección "Dagas de Clan"**:
   - Tradición de las piedras preciosas
   - Ceremonia del nacimiento
   - Matrimonio y vainas

3. **Nueva sección "Grupos Étnicos Enanos"**:
   - **Tabla de los tres grupos principales:**
     | Grupo | Ubicación | Características |
     |-------|-----------|-----------------|
     | Grondaksen | Bajo tierra | Tradicionalistas, "día de la forja" |
     | Ergaksen | Superficie | Adaptables |
     | Holtaksen | Montañas | Guerreros, "cintas de la gloria" |

   - Etnias notables: Kulenett, Mbe'ke, Taralu, Pahmet, Paraheen, Vahird

---

### Fase 4: Gnomos

**Archivo:** `docs/_ascendencias/gnomo/index.md`

**Cambios:**

1. **Expandir la sección sobre la Decoloración** (ya existe pero es breve):
   - Añadir información sobre los Decolorados
   - Explicar los síntomas y la progresión

2. **Nueva sección "Tipos de Gnomos"**:
   - Hijos feéricos
   - Gnomos crueles
   - Gnomos brillantes
   - Llama entusiasta

3. **Nueva sección "Enclaves Gnomos"**:
   - Brastlewark (Cheliax)
   - Descubrellano (Katapesh)
   - Irrere (refugio de Decolorados)
   - Wispil (fanáticos de la ópera)

---

### Fase 5: Goblins

**Archivo:** `docs/_ascendencias/goblin/index.md`

**Contenido a añadir:**

1. **Nueva sección "Mitos de Origen"**:
   - Leyenda de los barghest (Hadregash, Venkelvore, Zarongel, Zogmugot)
   - Los cuatro dones

2. **Nueva sección "El Cambio de Percepción"**:
   - Goblins de Katapesh (Yigrig el Triunfador)
   - Goblins en la Cicatriz de Sarkoris

3. **Nueva sección "Etnias Goblin"**:
   - Del bosque
   - De la escarcha (Pelaje Congelado)
   - Mono (Isla Mediogalti)
   - Raspadores

4. **Nueva sección "Tribus Notables"**:
   - Dedos Torcidos (Absalom)
   - Pelaje Congelado (Sociedad Pathfinder)
   - Moradores del Dragón
   - Masticabarro (Magnimar)

---

### Fase 6: Medianos

**Archivo:** `docs/_ascendencias/mediano/index.md`

**Contenido a añadir:**

1. **Nueva sección "La Suerte Mediana"**:
   - Tradición de objetos de la suerte
   - Bayas y botones

2. **Nueva sección "La Red de la Campanilla"**:
   - Organización de liberación de esclavos
   - Operaciones en Cheliax

3. **Nueva sección "Etnias Medianas"**:
   - Chelaxianos ("zafas")
   - Jarics (montañas, "alabandas")
   - Mihrinis ("tironetes")
   - Othobans (desplazados en el tiempo)
   - Song'o (supersticiones sobre cumplidos)
   - Uhlams (trabajadores)

---

### Fase 7: Ascendencias Mixtas

**Archivos:**
- `docs/_ascendencias/humano/herencias.md` (para semielfos/semiorcos)
- O crear `docs/_ascendencias/herencias-versatiles/semielfo.md` y `semiorco.md`

**Contenido:**

1. **Semielfos:**
   - Concepto de "Patria del Alma"
   - 6 etnias semielfas (tabla)

2. **Semiorcos:**
   - Mitos de Farasma y Gorum
   - Prejuicios y autosuficiencia
   - Culturas de aceptación (Shoanti, Ulfen)

---

### Fase 8: Ascendencias PC2

**Archivos:**
- `docs/_ascendencias/hobgoblin/index.md`
- `docs/_ascendencias/leshy/index.md`
- `docs/_ascendencias/lizardfolk/index.md`

**Hobgoblin - Añadir:**
- Historia de la Legión del Colmillo de Hierro
- Detalles sobre Oprak y la diplomacia

**Leshy - Añadir:**
- Profundizar en el origen espiritual
- Categorías de espíritus

**Iruxi - Añadir:**
- Referencias a los imperios antiguos
- Tradiciones astrológicas detalladas

---

## Consideraciones Técnicas

### Enlaces Cruzados

Implementar enlaces bidireccionales:

1. **Desde ascendencias hacia ambientación:**
   ```markdown
   > **Más información:** Ver [Ambientación de Golarion](/ambientacion/golarion-presagios/#etnias-humanas-del-mar-interior)
   ```

2. **Desde ambientación hacia ascendencias:**
   ```markdown
   *Para las reglas de juego de los humanos, ver [Ascendencia Humana](/ascendencias/humano/)*
   ```

### Actualización del Sidebar

Añadir enlace a la sección de ambientación dentro del sidebar de Ascendencias:

```html
<li><a href="{{ '/ambientacion/golarion-presagios/' | relative_url }}">Culturas de Golarion</a></li>
```

### SEO y Búsqueda

Actualizar `search-index.json` para incluir:
- Tags de etnias específicas
- Palabras clave culturales
- Referencias geográficas

---

## Priorización

| Prioridad | Ascendencia | Razón |
|-----------|-------------|-------|
| 1 | Humano | Mayor cantidad de contenido (13 etnias) |
| 2 | Elfo | Contenido rico con historia y 5 etnias |
| 3 | Enano | Tradiciones únicas (dagas de clan) |
| 4 | Gnomo | Profundizar la Decoloración existente |
| 5 | Goblin | 4 etnias + tribus notables |
| 6 | Mediano | 6 etnias + Red de la Campanilla |
| 7 | Semielfos/Semiorcos | Complemento a Humano/Elfo |
| 8 | Hobgoblin/Leshy/Iruxi | Contenido más limitado |

---

## Estimación de Trabajo

| Fase | Archivos | Contenido Nuevo (aprox.) |
|------|----------|-------------------------|
| Humanos | 1-2 | ~8.000 palabras |
| Elfos | 1 | ~3.000 palabras |
| Enanos | 1 | ~2.500 palabras |
| Gnomos | 1 | ~1.500 palabras |
| Goblins | 1 | ~2.000 palabras |
| Medianos | 1 | ~1.500 palabras |
| Mixtas | 2 | ~1.500 palabras |
| PC2 | 3 | ~1.000 palabras |

**Total:** ~21.000 palabras de contenido de ambientación integrado

---

## Ejemplo Completo: Sección Humana Expandida

```markdown
## Grupos Étnicos Humanos

Una gran variedad de grupos étnicos humanos puebla los continentes de la Región del mar Interior de Golarion y de las tierras más allá de la misma. Los personajes humanos pueden ser de cualquier grupo étnico, sea cual sea su lugar de procedencia.

Los personajes de los grupos étnicos humanos de la Región del mar Interior hablan común (también conocido como taldano), y algunos grupos étnicos conceden acceso a un idioma regional poco común.

---

### Erutaki

Los erutaki son un grupo de pueblos que viven en el extremo norte de Golarion, entre los glaciares de la **Corona del Mundo**. Son personas bajas y compactas, con piel color terracota, a menudo curtida por los vientos helados de su tierra natal, y cabello negro y liso.

Muchos erutaki son seminómadas y siguen migraciones de renos o bueyes almizcleros, mientras que otros viven a lo largo de las costas, pescando y cazando ballenas. Al vivir en un entorno tan duro, los erutaki son conscientes en todo momento de los límites del poder humano y se esfuerzan por vivir en armonía con la naturaleza.

**Nombres típicos:** Aklaq, Oki, Tulimak (masculinos); Aluki, Liak, Noayak (femeninos); Amaruq, Miki, Yuka (neutros).

---

### Garundi

Los garundi provienen de la parte norte del continente de Garund. Son de los humanos más altos de Golarion; el garundi promedio destaca por encima de los demás...

[continúa con todas las etnias]
```

---

## Decisiones Pendientes

1. **¿Mantener descripcion.md?** - Actualmente es duplicado de index.md en varias ascendencias
2. **¿Crear index.md para enanos?** - Solo existe herencias.md actualmente
3. **¿Nivel de detalle?** - ¿Incluir toda la información o versión resumida con enlace a golarion-presagios.md?
4. **¿Imágenes?** - ¿Añadir ilustraciones de las diferentes etnias si están disponibles?

---

## Conclusión

La **Opción A** (sección nueva dentro de cada página de ascendencia) es la más recomendable porque:

1. Mantiene todo el contenido relevante en un solo lugar
2. No requiere cambios en la estructura del sitio
3. Los jugadores encuentran la información cultural junto a las reglas
4. Es la opción más fácil de implementar y mantener

La implementación debería seguir el orden de priorización, empezando por los Humanos debido a la cantidad de contenido disponible y su relevancia para la mayoría de jugadores.

---

*Plan creado: 2026-02-02*
*Fuente de ambientación: /docs/_ambientacion/golarion-presagios.md*
