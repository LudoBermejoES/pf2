---
layout: page
title: "Daño: Fundamentos (Resistencia, Debilidad e Inmunidad)"
permalink: /reglas/detalle/combate/dano-parte-1/
chapter: Cómo Jugar
category: reglas
---

Durante una aventura los personajes se enfrentarán a todo tipo de peligros. Cuando un ataque o efecto impacta, se aplica daño: los Puntos de Golpe (PG) del objetivo se reducen en la cantidad indicada. Si llegan a 0 PG, la criatura cae inconsciente o muere.

## Los cuatro pasos para calcular el daño

### 1. Tirar el daño

Cuando un ataque tiene éxito, el atacante tira los dados de daño especificados en el arma o habilidad y suma los modificadores pertinentes (generalmente el modificador de Fuerza para ataques cuerpo a cuerpo, o el de Destreza para arcos). En un **éxito crítico**, el daño se dobla antes de aplicar resistencias o debilidades.

### 2. Aplicar resistencias

Una **resistencia** reduce el daño de un tipo específico en la cantidad indicada. Por ejemplo, si un esqueleto tiene resistencia al daño perforante 5 y recibe 12 PG de daño perforante, solo sufre 7 PG.

Si una criatura tiene resistencia a "todo el daño", esa resistencia se aplica a cualquier tipo de daño que reciba, con posibles excepciones listadas en el bloque de estadísticas.

**Las resistencias nunca reducen el daño por debajo de 0.** Si un enemigo tiene resistencia 10 y recibe 8 PG del tipo resistido, sufre 0 PG; no se "cura".

### 3. Aplicar debilidades

Una **debilidad** aumenta el daño de un tipo específico. Si ese tipo de daño está presente en el ataque —aunque sea como parte menor—, se añade el valor de la debilidad al daño total.

**Ejemplo:** Un conjuro inflige 10 PG de daño de fuego a una criatura con debilidad al fuego 5. La criatura sufre 10 + 5 = **15 PG**.

> La debilidad se aplica **una sola vez por ataque**, independientemente de cuántas fuentes de ese tipo de daño haya en el mismo golpe.

### 4. Aplicar inmunidades

Una **inmunidad** hace que la criatura no sufra ningún daño de ese tipo. La inmunidad tiene precedencia sobre resistencias y debilidades: si la criatura es inmune al fuego, no le afecta ningún daño de fuego, aunque también tenga debilidad al fuego (una contradicción que en la práctica no ocurre, pero el principio se aplica).

Las inmunidades pueden ser también a **condiciones** o **efectos** (p. ej., inmunidad al veneno, inmunidad a la condición paralizado).

## Tipos de daño físico

| Tipo | Descripción |
|---|---|
| **Contundente** | Porras, mazas, puños desnudos |
| **Perforante** | Flechas, dagas, picos |
| **Cortante** | Espadas, hachas, garras |

La mayoría de las armas infligen un único tipo. Algunas armas versátiles pueden infligir dos tipos (p. ej., una espada bastarda puede usarse a dos manos para añadir daño perforante además de cortante, a elección del atacante en cada Golpe).

## Tipos de daño de energía

| Tipo | Casos típicos |
|---|---|
| **Ácido** | Conjuros de ácido, babosas gigantes |
| **Frío** | Conjuros de hielo, elementales de agua |
| **Electricidad** | Rayos, conjuros eléctricos |
| **Fuego** | Bolas de fuego, dragones de fuego, antorchas |
| **Sónico** | Rugidos, conjuros de sonido |

## Tipos de daño especial

### Daño de Vitalidad y daño de Vacío

Son los dos grandes tipos de energía vital en PF2e Remaster:

- **Daño de Vitalidad** (en ediciones anteriores: "daño positivo"): solo daña a los no muertos. No tiene efecto sobre criaturas vivas ni objetos. Los conjuros de *curación* emiten energía de Vitalidad y por eso curan a los vivos y dañan a los no muertos.

- **Daño de Vacío** (en ediciones anteriores: "daño negativo"): solo daña a las criaturas vivas. No tiene efecto sobre los no muertos ni sobre objetos. Los conjuros de *daño* emiten energía de Vacío.

> **Nota Remaster:** Los términos "daño positivo" y "daño negativo" ya no se usan en PF2e desde el Remaster. El nombre correcto es **daño de Vitalidad** y **daño de Vacío** respectivamente.

Algunos efectos pueden tanto dañar como curar según el tipo de criatura. Por ejemplo, *curación* lanzada en área emite energía de Vitalidad: cura a los vivos en el área y daña a los no muertos.

La distinción importante es entre **energía** y **daño**:
- Cuando el texto dice simplemente "energía de Vitalidad", puede curar o dañar según la criatura.
- Cuando el texto dice explícitamente "**daño** de Vitalidad", solo tiene efecto dañino (sin curación).

### Daño de Espíritu (espiritual)

En el Remaster, el daño "mental", "bueno" o "malvado" de ediciones anteriores se ha reorganizado. El **daño espiritual** es el tipo que usan muchos efectos divinos. Puede tener el rasgo **Santo** (afecta a criaturas con el rasgo Profano) o **Profano** (afecta a criaturas con el rasgo Santo). Ver [Santificación](/reglas/detalle/personajes/santificacion/) para más detalles.

## Resistencias y debilidades a daño no físico

Funcionan exactamente igual que con daño físico:

**Ejemplo con debilidad:** Un vampiro tiene debilidad al fuego 5. Un mago le lanza *Bola de Fuego* y la criatura falla la salvación, sufriendo 35 PG de daño de fuego. El total final es 35 + 5 = **40 PG**.

**Ejemplo con resistencia:** Un elemental de fuego tiene resistencia al fuego 10. Recibe un impacto de *Flecha de Fuego* que inflige 14 PG de daño de fuego. El daño reducido es 14 − 10 = **4 PG**.

## Resistencias y debilidades en críticos

Las resistencias y debilidades se aplican **después** de doblar el daño crítico. Es decir:

1. Se calcula el daño normal.
2. Se dobla (si es crítico).
3. Se aplica la debilidad (suma) o resistencia (resta).

**Ejemplo:** Golpe crítico con espada larga (1d8+3 daño cortante). Se saca 5 en el dado → total base 8 → doblado: 16 PG. El objetivo tiene debilidad al daño cortante 5 → daño final: **21 PG**.
