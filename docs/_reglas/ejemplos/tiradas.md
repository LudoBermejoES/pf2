---
layout: page
permalink: /reglas/ejemplos/tiradas/
title: "Ejemplo: Tiradas y Grados de Éxito"
chapter: Cómo Jugar
category: reglas
source: PC1
nav_order: 105
---

Este ejemplo demuestra cómo funcionan las tiradas de dados, los modificadores, y especialmente los cuatro grados de éxito en diversas situaciones. Verás cómo éxitos críticos y fallos críticos cambian radicalmente los resultados.

## Los Grados de Éxito

Cada tirada en Pathfinder 2e tiene cuatro posibles resultados:

| Grado | Cómo se obtiene |
|-------|-----------------|
| **Éxito Crítico** | Superas la CD por 10 o más, O sacas 20 natural (sube un grado) |
| **Éxito** | Iguales o superas la CD |
| **Fallo** | No alcanzas la CD |
| **Fallo Crítico** | Fallas por 10 o más, O sacas 1 natural (baja un grado) |

> **Regla clave:** El 20 natural y el 1 natural solo **modifican** el grado, no garantizan éxito/fallo automático.

---

## Ejemplo 1: Escalar un Muro

Valeria ([Atletismo]({{ '/habilidades/atletismo/' | relative_url }}) +9) intenta escalar un muro de piedra.

### Escenario A: Muro Fácil (CD 15)

**Tirada:** 1d20+9 = 12+9 = **21**
- 21 supera CD 15 por 6 → **Éxito**
- Valeria escala el muro sin problemas

**Tirada alternativa:** 1d20+9 = 18+9 = **27**
- 27 supera CD 15 por 12 → **Éxito Crítico**
- Valeria escala el doble de rápido

**Tirada alternativa:** 1d20+9 = 3+9 = **12**
- 12 no alcanza CD 15 → **Fallo**
- Valeria no avanza este turno

**Tirada alternativa:** 1d20+9 = 1+9 = **10** (1 natural)
- 10 no alcanza CD 15 → Sería Fallo
- 1 natural baja un grado → **Fallo Crítico**
- Valeria cae y recibe daño

### Escenario B: Muro Imposible (CD 35)

**Tirada:** 1d20+9 = 20+9 = **29** (20 natural)
- 29 no alcanza CD 35 → Sería Fallo
- 20 natural sube un grado → **Éxito**
- ¡Valeria logra lo aparentemente imposible!

> **Nota:** Si la CD fuera 40, incluso un 20 natural resultaría en fallo (29 falla por 11, sería fallo crítico, sube a fallo).

---

## Ejemplo 2: Lanzar un Conjuro

Zander lanza *rayo de escarcha* (ataque de conjuro +9) contra un gólem de piedra (CA 25).

### Los Cuatro Resultados Posibles

**Fallo Crítico (tirada ≤ 5):**
- Ejemplo: 1d20+9 = 3+9 = **12** (falla por 13)
- El rayo se dispersa inútilmente
- Algunos conjuros tienen efectos negativos en fallo crítico

**Fallo (tirada 6-15):**
- Ejemplo: 1d20+9 = 10+9 = **19** (falla por 6)
- El gólem esquiva o el rayo pasa de largo
- No ocurre daño

**Éxito (tirada 16-25):**
- Ejemplo: 1d20+9 = 17+9 = **26** (supera por 1)
- **Daño:** 2d4+4 = 6+4 = **10 de daño de frío**

**Éxito Crítico (tirada ≥ 26 o 20 natural):**
- Ejemplo: 1d20+9 = 20+9 = **29** o tirada que supere por 10+
- **Daño crítico:** 2d4+4 = 6+4 = 10 → **20 de daño de frío**
- ¡El doble de daño!

---

## Ejemplo 3: Tirada de Salvación

Un dragón usa su aliento de fuego. Todos en el área deben hacer una tirada de salvación de Reflejos CD 22.

### Efectos del Conjuro (Aliento de Dragón)

| Grado | Daño (de 8d6 = 28) |
|-------|---------------------|
| **Éxito Crítico** | 0 daño (evitado completamente) |
| **Éxito** | 14 daño (mitad) |
| **Fallo** | 28 daño (completo) |
| **Fallo Crítico** | 28 daño + efecto adicional |

### Las Tiradas del Grupo

**Theron (Reflejos +11):**
- Tirada: 1d20+11 = 15+11 = **26** (supera por 4)
- Resultado: **Éxito** → 14 de daño
- *Theron rueda esquivando la peor parte*

**Valeria (Reflejos +8):**
- Tirada: 1d20+8 = 20+8 = **28** (20 natural)
- Resultado: Éxito (supera por 6) → **Éxito Crítico** (20 natural)
- → **0 daño**
- *Valeria alza su escudo justo a tiempo*

**Zander (Reflejos +8):**
- Tirada: 1d20+8 = 1+8 = **9** (1 natural)
- Resultado: Fallo (falla por 13) → **Fallo Crítico** (1 natural)
- → 28 de daño + queda **en llamas** (daño persistente)
- *Las llamas envuelven a Zander*

**Mira (Reflejos +6):**
- Tirada: 1d20+6 = 10+6 = **16** (falla por 6)
- Resultado: **Fallo** → 28 de daño
- *Mira recibe el impacto completo*

---

## Ejemplo 4: Tirada de Habilidad con Grados

Theron intenta [Abrir una Cerradura]({{ '/habilidades/latrocinio/' | relative_url }}) con [Latrocinio]({{ '/habilidades/latrocinio/' | relative_url }}) +9. La cerradura tiene CD 20.

### Grados de Éxito de Abrir Cerradura

| Grado | Resultado |
|-------|-----------|
| **Éxito Crítico** | Abre en 1 acción sin hacer ruido |
| **Éxito** | Abre después de 2 acciones |
| **Fallo** | No abre, puede reintentar |
| **Fallo Crítico** | Rompe las ganzúas, cerradura atascada |

### La Tirada

**Tirada:** 1d20+9 = 8+9 = **17** (falla por 3)
- Resultado: **Fallo**
- Theron forcejea pero la cerradura no cede
- Puede intentarlo de nuevo

**Segundo intento:** 1d20+9 = 14+9 = **23** (supera por 3)
- Resultado: **Éxito**
- Tras 2 acciones de trabajo, la cerradura cede

---

## Ejemplo 5: Modificadores Apilados

Mira hace una tirada de ataque en una situación complicada.

### Situación

- Mira tiene ataque +8 base
- Está bajo el efecto de *bendición* (+1 de estado)
- Está [asustada]({{ '/apendices/estados/' | relative_url }}) 2 (-2 de estado)
- El enemigo está [flanqueado]({{ '/reglas/cobertura-flanqueo/' | relative_url }}) ([desprevenido]({{ '/apendices/estados/' | relative_url }}), -2 CA)
- Hay [cobertura]({{ '/reglas/cobertura-flanqueo/' | relative_url }}) menor (+1 CA al enemigo)

### Calculando Modificadores

**Bonificadores de Mira:**
- Base: +8
- *Bendición*: +1 (estado)
- Asustada: -2 (estado)
- **Nota:** Solo el mejor/peor bonificador/penalizador de estado se aplica

> **Regla:** Los modificadores del mismo tipo no se apilan. Solo cuentas el mayor bonificador y el mayor penalizador de cada tipo.

Bonificador final: +8 + 1 (estado) - 2 (estado) = **+7** (el estado neto es -1)

**CA del Enemigo:**
- CA base: 18
- Desprevenido: -2 (circunstancia)
- Cobertura menor: +1 (circunstancia)
- CA final: 18 - 2 + 1 = **17** (el circunstancia neto es -1)

**Tirada:** 1d20+7 vs CA 17
- Tirada: 1d20 = 14 → Total: **21**
- 21 supera 17 por 4 → **Éxito**

---

## Ejemplo 6: Recordar Conocimiento

Zander intenta identificar a un monstruo desconocido usando [Arcanos]({{ '/habilidades/arcanos/' | relative_url }}) +8.

### Cómo Funciona

> **Regla:** **[Recordar Conocimiento]({{ '/habilidades/acciones-generales/' | relative_url }})** da información basada en el grado de éxito. La CD depende del nivel y rareza de la criatura.

La criatura es un Sluagh (nivel 4, poco común). CD: 21

### Los Resultados

**Éxito Crítico (≥31 o 20 natural que resulte en éxito):**
- Zander obtiene información detallada
- *"Es un Sluagh, un fae oscuro. Son débiles al hierro frío y temen la luz del sol. Pueden volverse incorpóreos brevemente."*

**Éxito (21-30):**
- Zander obtiene información útil
- *"Es un Sluagh, criatura fae. Probablemente débil al hierro frío."*

**Fallo (11-20):**
- Zander no recuerda información
- *"No recuerdas haber leído sobre esta criatura."*

**Fallo Crítico (≤10 o 1 natural):**
- Zander obtiene información **incorrecta**
- *"Crees que es un tipo de no muerto débil al daño positivo."* (¡Falso!)

### La Tirada Real

**Tirada:** 1d20+8 = 11+8 = **19** (falla por 2)
- Resultado: **Fallo**
- *Zander frunce el ceño, incapaz de identificar a la criatura*

---

## Tabla de Referencia Rápida

### Modificadores por Tipo

| Tipo | Se Apilan | Ejemplos |
|------|-----------|----------|
| **Circunstancia** | No | Cobertura, flanqueo, terreno elevado |
| **Estado** | No | Bendición, asustado, enfermo |
| **Objeto** | No | Armas +1, armadura potenciada |
| **Sin tipo** | Sí | Modificadores de atributo, competencia |

### Grados de Éxito

| Resultado | Condición |
|-----------|-----------|
| Éxito Crítico | Supera CD por 10+ o 20 natural (+1 grado) |
| Éxito | Iguala o supera CD |
| Fallo | No alcanza CD |
| Fallo Crítico | Falla por 10+ o 1 natural (-1 grado) |

### Efectos Comunes por Grado

| Situación | Crítico | Éxito | Fallo | Crítico Fallo |
|-----------|---------|-------|-------|---------------|
| **Ataque** | ×2 daño | Daño normal | Sin daño | Sin daño |
| **Salvación** | Sin efecto | Efecto reducido | Efecto completo | Efecto aumentado |
| **Curar** | ×2 curación | Curación normal | Sin curación | — |
| **Sigilo** | Oculto + bonus | Oculto | Detectado | Detectado + penalización |

---

## Lecciones del Ejemplo

1. **Los críticos cambian todo** — Un 20 natural puede salvar de situaciones imposibles
2. **Los tipos de modificadores importan** — Acumular bonificadores del mismo tipo es inútil
3. **El fallo crítico duele** — Puede causar efectos negativos graves
4. **Conoce los grados** — Saber qué pasa en cada grado te ayuda a decidir si vale la pena arriesgarse
5. **El contexto afecta las CD** — Cobertura, actitudes, y situaciones modifican la dificultad
