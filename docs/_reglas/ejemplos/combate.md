---
layout: page
permalink: /reglas/ejemplos/combate/
title: "Ejemplo: Un Combate Completo"
chapter: Cómo Jugar
category: reglas
source: PC1
nav_order: 101
---

Este ejemplo muestra un encuentro de combate completo contra un grupo de bandidos. Verás cómo funcionan la iniciativa, las acciones, los ataques, el daño, los estados y las reacciones.

## La Situación

El grupo de aventureros (Valeria, Theron, Mira y Zander) está viajando por un bosque cuando tres bandidos les tienden una emboscada. Uno de los bandidos es un líder veterano.

### Participantes

**Personajes Jugadores (PJs)**

| PJ | CA | PG | Iniciativa |
|----|----|----|------------|
| Valeria (Guerrera) | 20 | 44 | Percepción +7 |
| Theron (Pícaro) | 19 | 32 | Sigilo +11 (estaba explorando) |
| Mira (Clériga) | 18 | 38 | Percepción +9 |
| Zander (Mago) | 16 | 26 | Percepción +6 |

**Enemigos**

| Enemigo | CA | PG | Iniciativa |
|---------|----|----|------------|
| Líder bandido | 18 | 30 | Percepción +8 |
| Bandido 1 | 16 | 15 | Percepción +4 |
| Bandido 2 | 16 | 15 | Percepción +4 |

---

## Inicio del Encuentro

### Paso 1: Determinar Sorpresa

Theron estaba usando la actividad de exploración **[Evitar ser Detectado]({{ '/reglas/modo-exploracion/' | relative_url }})**, así que tira [Sigilo]({{ '/habilidades/sigilo/' | relative_url }}) para iniciativa. Los bandidos intentaban emboscar, pero Mira tenía **Buscar** activo.

> **Regla:** Si usas Evitar ser Detectado, tiras [Sigilo]({{ '/habilidades/sigilo/' | relative_url }}) en lugar de Percepción para iniciativa. Si superas la CD de Percepción de los enemigos, empiezas **[escondido]({{ '/apendices/estados/' | relative_url }})** de ellos.

**Tirada de Theron (Sigilo):** 1d20+11 = 14+11 = **25** → Supera CD 18 (Percepción del líder), empieza escondido

### Paso 2: Tirar Iniciativa

Todos tiran iniciativa:

| Participante | Tirada | Total |
|--------------|--------|-------|
| Theron | 14+11 | **25** |
| Mira | 16+9 | **25** |
| Líder bandido | 12+8 | **20** |
| Valeria | 11+7 | **18** |
| Zander | 10+6 | **16** |
| Bandido 1 | 8+4 | **12** |
| Bandido 2 | 5+4 | **9** |

> **Regla:** En caso de empate, los PJs van antes que los PNJs. Si dos PJs empatan, deciden entre ellos.

Mira y Theron empatan con 25. Deciden que Theron va primero para aprovechar que está escondido.

**Orden final:** Theron → Mira → Líder → Valeria → Zander → Bandido 1 → Bandido 2

---

## Asalto 1

### Turno de Theron (Pícaro)

Theron está escondido detrás de unos arbustos, a 20 pies del líder bandido.

> **Jugador:** "Quiero acercarme sigilosamente y apuñalar al líder por la espalda."

**Acción 1 {% include accion.html tipo="1" %}: Zancada Sigilosa**

Theron tiene la dote **Zancada Sigilosa**, que le permite moverse a mitad de velocidad sin romper el [sigilo]({{ '/habilidades/sigilo/' | relative_url }}).

- Velocidad: 30 pies → Se mueve 15 pies (mitad de velocidad)
- Sigue **escondido** del líder

**Acción 2 {% include accion.html tipo="1" %}: Golpe**

Como está escondido, el líder está **[desprevenido]({{ '/apendices/estados/' | relative_url }})** contra él (-2 CA).

- CA efectiva del líder: 18 - 2 = **16**
- Tirada de ataque: 1d20+10 = 17+10 = **27**
- 27 supera CD 16 por más de 10 → **¡Éxito Crítico!**

> **Regla:** Un éxito crítico en un Golpe inflige daño doble.

**Daño (crítico):**
- Daño base: 1d6+3 = 4+3 = 7
- Daño furtivo (desprevenido): 2d6 = 8
- Total base: 15 → **Crítico: 30 de daño**

El líder bandido recibe 30 de daño. PG restantes: 30-30 = **0 PG** → ¡Inconsciente!

> **DJ:** "Tu espada corta atraviesa la garganta del líder. Se desploma sin hacer ruido."

**Acción 3 {% include accion.html tipo="1" %}: Esconderse**

Theron intenta volver a [esconderse]({{ '/habilidades/sigilo/' | relative_url }}) tras el ataque.

- Tirada de [Sigilo]({{ '/habilidades/sigilo/' | relative_url }}): 1d20+11 = 8+11 = **19**
- CD de Percepción de los bandidos: 14
- Éxito → Theron está **escondido** de los bandidos restantes

---

### Turno de Mira (Clériga)

Mira ve que Theron ya eliminó al líder. Decide prepararse para el combate.

> **Jugadora:** "Lanzo *bendición* para ayudar al grupo y me acerco."

**Acción 1-2 {% include accion.html tipo="2" %}: Lanzar *Bendición***

*Bendición* es un conjuro de 2 acciones con área de emanación de 10 pies.

> **Regla:** Los conjuros usan el número de acciones indicado. *Bendición* afecta a los aliados en el área.

- Mira y todos los aliados a 3 m ganan **+1 de estado a tiradas de ataque**
- Duración: 1 minuto (sustentado)

**Acción 3 {% include accion.html tipo="1" %}: Zancada**

Mira se mueve 20 pies hacia adelante para incluir a Valeria en el área de *bendición*.

---

### Turno del Líder Bandido

El líder está inconsciente y moribundo. Al inicio de su turno:

> **Regla:** Una criatura moribunda debe hacer una **prueba de recuperación** (tirada plana CD 10) al inicio de cada turno.

- Tirada plana: 1d20 = 6 → **Fallo**
- Moribundo 1 → **Moribundo 2**

El líder se desangra lentamente...

---

### Turno de Valeria (Guerrera)

Los bandidos aún no han actuado. Valeria ve a Bandido 1 a 30 pies.

> **Jugadora:** "Cargo contra el bandido más cercano y lo ataco dos veces."

**Acción 1 {% include accion.html tipo="1" %}: Zancada**

- Velocidad: 20 pies (con armadura pesada)
- Se mueve 20 pies, quedando a 10 pies del Bandido 1

**Acción 2 {% include accion.html tipo="1" %}: Zancada**

- Se mueve otros 20 pies, llegando junto al Bandido 1

**Acción 3 {% include accion.html tipo="1" %}: Golpe**

- Tirada de ataque: 1d20+11 = 13+11 = **24**
- Bonificador por *bendición*: +1 → Total: **25**
- CA del bandido: 16 → **Éxito**

**Daño:** 1d8+4 = 6+4 = **10 de daño**

Bandido 1: 15-10 = **5 PG restantes**

> **DJ:** "Tu espada corta el costado del bandido, que gruñe de dolor."

---

### Turno de Zander (Mago)

Zander está a 40 pies de Bandido 2.

> **Jugador:** "Lanzo *rayo de escarcha* contra el otro bandido."

**Acción 1-2 {% include accion.html tipo="2" %}: Lanzar *Rayo de Escarcha***

*Rayo de escarcha* es un ataque de conjuro a distancia.

- Tirada de ataque de conjuro: 1d20+9 = 11+9 = **20**
- Bonificador por *bendición*: +1 → Total: **21**
- CA del bandido: 16 → **Éxito**

**Daño:** 2d4+4 (frío) = 5+4 = **9 de daño**

Bandido 2: 15-9 = **6 PG restantes**

**Acción 3 {% include accion.html tipo="1" %}: Zancada**

Zander se mueve 20 pies hacia atrás para mantener distancia.

---

### Turno de Bandido 1

El bandido está herido y enfrentando a Valeria.

**Acción 1 {% include accion.html tipo="1" %}: Golpe contra Valeria**

- Tirada de ataque: 1d20+8 = 14+8 = **22**
- CA de Valeria: 20 → **Éxito**

**Daño:** 1d6+3 = 4+3 = **7 de daño**

Valeria: 44-7 = **37 PG restantes**

**Acción 2 {% include accion.html tipo="1" %}: Golpe contra Valeria (segundo ataque)**

> **Regla:** Cada ataque después del primero en un turno tiene una **penalización por ataques múltiples (PAM)**: -5 en el segundo, -10 en el tercero.

- Tirada de ataque: 1d20+8-5 = 10+3 = **13**
- CA de Valeria: 20 → **Fallo**

**Acción 3 {% include accion.html tipo="1" %}: Alzar un Escudo**

El bandido alza su escudo.

- CA: 16 → **18** hasta el inicio de su próximo turno

---

### Turno de Bandido 2

El bandido herido por el rayo ve a Zander alejándose.

**Acción 1 {% include accion.html tipo="1" %}: Zancada**

Se mueve 25 pies hacia Zander.

**Acción 2 {% include accion.html tipo="1" %}: Zancada**

Se mueve otros 25 pies, llegando junto a Zander.

**Acción 3 {% include accion.html tipo="1" %}: Golpe**

- Tirada de ataque: 1d20+8 = 18+8 = **26**
- CA de Zander: 16 → **Éxito crítico** (supera por 10+)

> **Regla:** Un crítico en ataque inflige daño doble.

**Daño (crítico):** 1d6+3 = 5+3 = 8 → **16 de daño**

Zander: 26-16 = **10 PG restantes**

> **DJ:** "El bandido te alcanza con un tajo brutal que casi te derriba."

---

## Asalto 2

### Turno de Theron

Theron ve a Zander en problemas.

> **Jugador:** "Salgo de mi escondite y ataco al bandido que atacó a Zander."

**Acción 1 {% include accion.html tipo="1" %}: Zancada**

Se mueve 30 pies hasta llegar junto a Bandido 2.

> **Nota:** Al moverse, Theron deja de estar escondido.

**Acción 2 {% include accion.html tipo="1" %}: Golpe**

Theron y Zander están flanqueando al bandido.

> **Regla:** Cuando dos aliados están en lados opuestos de un enemigo, lo **[flanquean]({{ '/reglas/cobertura-flanqueo/' | relative_url }})**. El enemigo está **[desprevenido]({{ '/apendices/estados/' | relative_url }})** (-2 CA) contra ellos.

- CA efectiva del bandido: 16-2 = **14**
- Tirada de ataque: 1d20+10 = 12+10 = **22**
- Éxito

**Daño:**
- Base: 1d6+3 = 2+3 = 5
- Furtivo (desprevenido): 2d6 = 7
- **Total: 12 de daño**

Bandido 2: 6-12 = **-6 PG** → ¡Derrotado!

**Acción 3 {% include accion.html tipo="1" %}: Zancada**

Theron corre hacia Bandido 1.

---

### Turno de Mira

> **Jugadora:** "Sustento *bendición* y curo a Zander."

**Acción Gratuita {% include accion.html tipo="libre" %}: Inicio de turno**

El contador de *bendición* baja de 10 asaltos a 9.

**Acción 1 {% include accion.html tipo="1" %}: Sustentar *Bendición***

> **Regla:** Los conjuros sustentados requieren 1 acción por turno para mantenerlos activos.

**Acción 2-3 {% include accion.html tipo="2" %}: Lanzar *Curar* (2 acciones)**

Mira lanza *curar* de rango 2 tocando a Zander.

- Curación: 2d10+16 = 7+16 = **23 PG curados**

Zander: 10+23 = **33 PG** (supera su máximo de 26, queda en 26)

---

### Turno de Valeria

Valeria tiene al Bandido 1 frente a ella. Theron está llegando por el otro lado.

**Acción 1 {% include accion.html tipo="1" %}: Golpe**

- Tirada: 1d20+11+1 (bendición) = 8+12 = **20**
- CA del bandido (con escudo): 18 → **Éxito**

**Daño:** 1d8+4 = 7+4 = **11 de daño**

Bandido 1: 5-11 = **-6 PG** → ¡Derrotado!

> **DJ:** "Tu espada atraviesa la defensa del bandido. Cae al suelo."

---

## Fin del Encuentro

Con ambos bandidos derrotados y el líder moribundo, el combate termina.

> **Regla:** El DJ puede terminar el encuentro cuando no queden amenazas activas.

El grupo decide qué hacer con el líder moribundo (estabilizarlo para interrogarlo o dejarlo morir).

---

## Resumen de Reglas Clave

| Concepto | Regla |
|----------|-------|
| **Iniciativa** | Percepción (o Sigilo/Engaño según actividad de exploración) |
| **3 acciones** | Cada turno tienes 3 acciones para usar como quieras |
| **PAM** | -5 al segundo ataque, -10 al tercero |
| **Éxito crítico** | Superar CD por 10+ o sacar 20 natural |
| **Desprevenido** | -2 CA (por flanqueo, escondido, etc.) |
| **Flanqueo** | Dos aliados en lados opuestos del enemigo |
| **Escudo alzado** | +2 CA hasta tu próximo turno |
| **Sustentado** | Requiere 1 acción por turno para mantenerlo |

---

## Lecciones del Ejemplo

1. **El posicionamiento importa** — Theron eliminó al líder porque estaba escondido y obtuvo un crítico
2. **La PAM desincentiva atacar tres veces** — Usar acciones para moverte, alzar escudo o lanzar conjuros suele ser mejor que un tercer ataque con -10
3. **El trabajo en equipo es crucial** — *Bendición* de Mira ayudó a todo el grupo, el flanqueo de Theron y Zander permitió el daño furtivo
4. **Los críticos son devastadores** — Tanto Theron como Bandido 2 mostraron el poder del daño doble
