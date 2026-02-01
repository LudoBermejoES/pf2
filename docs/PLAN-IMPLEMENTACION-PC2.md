# Plan de Implementación Player Core 2

**Estado**: En Progreso
**Rama**: `pc2`
**Fecha de Inicio**: 2026-02-01
**Estimado de Finalización**: 2026-02-20

---

## Resumen Ejecutivo

Incorporación de contenido de **Pathfinder Player Core 2** en la web existente de PF2. Total estimado: **~520 archivos nuevos** organizados en 4 fases.

### Estadísticas

| Sección | Archivos | Avance |
|---------|----------|--------|
| **Fase 1: Infraestructura** | 2 (layouts + CSS) | ✅ **100%** |
| **Fase 2: Contenido Core** | ~70 (Asc. + Clases) | ⏳ **0%** |
| **Fase 3: Opciones** | ~262 (Arq. + Dotes + Conj.) | ⏳ **0%** |
| **Fase 4: Equipo** | ~205 (Alquimia + Objetos + Trampas) | ⏳ **0%** |
| **TOTAL** | **~540** | **~3.7%** |

---

## Fase 1: Infraestructura ✅

**Estado**: Completada en commit `f84ced5`

### Completado:
- [x] Sistema de badges para source (PC1/PC2/PC1+PC2)
- [x] Actualización de 4 layouts principales
- [x] CSS con estilos para los badges
- [x] Script de retroalimentación para marcar archivos existentes
- [x] 904 archivos marcados como `source: PC1`

### Archivos Modificados:
- `docs/_layouts/page.html`
- `docs/_layouts/spell.html`
- `docs/_layouts/ancestry.html`
- `docs/_layouts/class.html`
- `docs/assets/css/main.css` (+42 líneas)

### Archivos Creados:
- `scripts/add-source-pc1.py`
- `templates/ascendencia-template.md` (plantilla para nuevas ascendencias)

---

## Fase 2: Contenido Core ⏳

**Prioridad**: ALTA
**Archivos Estimados**: ~70
**Contenido**: Ascendencias (8 nuevas) + Clases (9 nuevas) + Arquetipos Multiclase (8)

### 2.1 Ascendencias Nuevas (8)
- [ ] Catfolk (3 archivos: index, herencias, dotes)
- [ ] Hobgoblin (3 archivos)
- [ ] Kholo (3 archivos)
- [ ] Kobold (3 archivos)
- [ ] Lizardfolk (3 archivos)
- [ ] Ratfolk (3 archivos)
- [ ] Tengu (3 archivos)
- [ ] Tripkee (3 archivos)

**Subtotal**: 24 archivos

### 2.2 Herencias Versatiles Nuevas (3)
- [ ] Dhampir
- [ ] Sangre de Dragón
- [ ] Caminante del Ocaso

**Subtotal**: 3 archivos

### 2.3 Clases Nuevas (9)
- [ ] Alquimista (~4 archivos: index, características, dotes, campos investigación)
- [ ] Bárbaro (~4 archivos: index, características, dotes, instintos)
- [ ] Campeón (~5 archivos: index, características, dotes, causas, dominios)
- [ ] Espadachín (~4 archivos: index, características, dotes, estilos)
- [ ] Hechicero (~4 archivos: index, características, dotes, linajes)
- [ ] Investigador (~4 archivos: index, características, dotes, metodologías)
- [ ] Monje (~3 archivos: index, características, dotes)
- [ ] Oráculo (~4 archivos: index, características, dotes, misterios)

**Subtotal**: ~32 archivos

### 2.4 Arquetipos Multiclase Nuevos (8)
- [ ] Alquimista (multiclase)
- [ ] Bárbaro (multiclase)
- [ ] Campeón (multiclase)
- [ ] Espadachín (multiclase)
- [ ] Hechicero (multiclase)
- [ ] Investigador (multiclase)
- [ ] Monje (multiclase)
- [ ] Oráculo (multiclase)

**Subtotal**: 8 archivos

### Fase 2 Total: **67 archivos**

---

## Fase 3: Opciones de Personaje ⏳

**Prioridad**: MEDIA
**Archivos Estimados**: ~262

### 3.1 Arquetipos Otros (31 + 1 index)
**Subtotal**: 36 archivos

### 3.2 Dotes Generales Nuevas (11)
**Subtotal**: 11 archivos

### 3.3 Dotes de Habilidad (~45)
**Subtotal**: ~45 archivos

### 3.4 Conjuros Individuales (~150)
**Subtotal**: ~150 archivos

### 3.5 Conjuros de Foco (4 clases)
**Subtotal**: 4 archivos

### 3.6 Rituales (13)
**Subtotal**: 13 archivos

### Fase 3 Total: **~259 archivos**

---

## Fase 4: Equipo y Tesoros ⏳

**Prioridad**: MEDIA-BAJA
**Archivos Estimados**: ~205

### 4.1 Alquimia (~80 archivos)
- Bombas
- Elixires
- Mutágenos
- Venenos
- Herramientas alquímicas

### 4.2 Objetos Mágicos (~100)
- Permanentes
- Consumibles
- Bastones
- Varitas

### 4.3 Trampas (~25)
- Reglas
- Trampas individuales

### Fase 4 Total: **~205 archivos**

---

## Estrategia de Implementación

### Enfoque Recomendado:

1. **Fase 2 PRIMERO**: Contenido core (ascendencias/clases) requiere decisiones de diseño
2. **Fase 3 EN PARALELO**: Dotes y Arquetipos pueden ser más automatizados
3. **Fase 4 ÚLTIMO**: Equipo es más volumétrico pero menos crítico para jugabilidad

### Recursos Disponibles:

- **Templates**: `templates/ascendencia-template.md` (expandible)
- **Scripts**: `scripts/add-source-pc1.py` (modelo para otros scripts)
- **Datos Fuente**: `original/player_core_2_es/` (PDF y archivos)

### Herramientas Sugeridas:

- Scripts de generación de archivos masivos
- Agentes/Swarms para paralelizar creación
- Validadores de estructura de frontmatter
- Generador de índices automático

---

## Hitos Clave

| Hito | Fecha Estimada | Estado |
|------|----------------|--------|
| ✅ Fase 1: Infraestructura | 2026-02-01 | **COMPLETADA** |
| ⏳ Fase 2: Content Core 50% | 2026-02-05 | Pendiente |
| ⏳ Fase 2: Completa | 2026-02-08 | Pendiente |
| ⏳ Fase 3: En Progreso | 2026-02-08 | Pendiente |
| ⏳ Fase 4: En Progreso | 2026-02-12 | Pendiente |
| ⏳ Verificación Final | 2026-02-15 | Pendiente |

---

## Próximos Pasos Inmediatos

1. **Crear generador de ascendencias**: Script que crea los 8 archivos base para ascendencias
2. **Crear generador de clases**: Script que crea los ~32 archivos base para clases
3. **Actualizar navigation.yml**: Con todas las nuevas entradas
4. **Comenzar Fase 2**: Población de contenido

---

## Notas

- **Rama activa**: `pc2` (no mergear a `main` hasta validación completa)
- **Source branching**: Todos los archivos nuevos tendrán `source: PC2` automáticamente
- **Validación necesaria**: Después de cada fase, verificar links internos y coherencia

---

*Documento actualizado: 2026-02-01*
*Autor: Claude AI*
