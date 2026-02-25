---
layout: page
title: "Críticos y Grados de Éxito"
permalink: /reglas/detalle/combate/criticos-y-grados-de-exito/
chapter: Cómo Jugar
category: reglas
---

En Pathfinder 2ª edición, la mayoría de las acciones dan lugar a uno de **cuatro grados de éxito**: éxito crítico, éxito, fracaso y fracaso crítico. Los dos primeros y el tercero suelen entenderse bien, pero los dos resultados críticos pueden generar confusión, especialmente en lo que respecta al daño de los críticos.

## Determinar el grado de éxito

Cada prueba consiste en tirar 1d20, añadir o restar modificadores y comparar el total con una **Clase de Dificultad (CD)**. En la mayoría de los ataques, la CA del objetivo es la CD de la prueba.

**Ejemplo:** Si un enemigo tiene CA 24, necesitas obtener 24 o más para tener éxito y golpear. Con 23 o menos, fallas. En caso de empate, quien tira los dados gana.

## Los resultados críticos: la diferencia con PF2

Aquí es donde PF2 difiere de otros juegos de rol con d20. **Un resultado es crítico cuando el total modificado supera o cae por debajo de la CD en 10 o más.**

| Resultado | Condición |
|---|---|
| **Éxito crítico** | Total ≥ CD + 10 |
| **Éxito** | Total ≥ CD |
| **Fracaso** | Total < CD |
| **Fracaso crítico** | Total ≤ CD − 10 |

**Ejemplo de éxito crítico:** Atacas a un enemigo con CA 24, sacas 19 en el dado y tienes +15 de bonificador al ataque. Total: 34, que es 10 más que la CD → **éxito crítico**.

**Ejemplo de fracaso crítico:** Un mago sin entrenamiento en Atletismo (modificador +0) intenta una prueba con CD 16. Saca un 4. Total: 4, que es más de 10 por debajo de la CD → **fracaso crítico**.

## El 20 natural y el 1 natural

A diferencia de otros juegos de d20, en PF2 **un 20 natural no es automáticamente un éxito ni un crítico**, y **un 1 natural no es automáticamente un fracaso crítico**. En cambio:

- **20 natural:** Calcula el grado de éxito con normalidad y luego **aumenta el grado en un paso**.
- **1 natural:** Calcula el grado de éxito con normalidad y luego **reduce el grado en un paso**.

La escala de grados, de mejor a peor: éxito crítico → éxito → fracaso → fracaso crítico.

**Ejemplo con 20 natural contra oponente difícil:** Un jugador con +8 de bonificador al ataque ataca a un enemigo con CA 30. Saca 20 natural. 20 + 8 = 28, que sería un fracaso (28 < 30). Pero como es 20 natural, el grado sube un paso: fracaso → **éxito normal**. El personaje golpea e inflige daño regular. En este caso es imposible obtener un crítico.

**Ejemplo con 1 natural contra oponente débil:** Un jugador con +19 de bonificador al ataque ataca a un enemigo con CA 18. Saca 1 natural. 1 + 19 = 20, que sería un éxito (20 ≥ 18). Pero como es 1 natural, el grado baja un paso: éxito → **fracaso normal**. Se pierda la acción.

> Esto solo resulta significativo cuando hay una gran disparidad entre el personaje y la CD. En situaciones normales, un 20 natural casi siempre dará un crítico y un 1 natural casi siempre dará un fracaso crítico.

## Qué ocurre en cada grado de éxito

Cada acción, habilidad o efecto incluye en su descripción qué sucede para cada grado de éxito. **Ejemplo con Equilibrio (Acrobacias):**

- **Éxito crítico:** No te afecta la superficie estrecha y te mueves a velocidad completa.
- **Éxito:** Puedes moverte a velocidad completa, pero tratas la superficie como terreno difícil.
- **Fracaso:** No avanzas y pierdes la acción.
- **Fracaso crítico:** Caes.

Cuando una acción no especifica los cuatro grados, los no descritos siguen siendo posibles, pero no ocurre nada especial. Por ejemplo, **Golpear** solo describe el éxito crítico y el éxito normal:

- **Éxito crítico:** El golpe inflige el doble del daño normal.
- **Éxito:** El golpe inflige el daño esperado.
- **Fracaso / Fracaso crítico:** La acción se pierde sin efecto adicional.

## Daño en críticos: cómo se dobla

Cuando un ataque obtiene un éxito crítico, inflige **el doble del daño normal**. Todo el daño que se aplicaría en un golpe normal se dobla; el daño que solo se aplica en críticos no se dobla.

### Ejemplo 1: Guerrero con espada larga

El arma inflige 1d8 + 3 (modificador de Fuerza). Saca 3 en el d8 → total base: 6. El daño crítico es 6 × 2 = **12**.

> En PF2, los bonificadores estáticos como el modificador de Fuerza también se doblan, a diferencia de otros juegos con d20.

### Ejemplo 2: Pícaro con daga

El ataque inflige 1d4 + 2 (Fuerza) + 1d6 (ataque furtivo). Saca 3 en la daga, 5 en el dado de ataque furtivo → total base: 3 + 2 + 5 = 10.

¿Se dobla el ataque furtivo? Sí, porque también se aplica en un golpe normal. Daño crítico: 10 × 2 = **20**.

### Ejemplo 3: Bárbaro en furia con voulge

El arma inflige 1d8 + 4 (Fuerza) + 2 (furia) + 1d8 (rasgo mortal d8). El rasgo **mortal** inflige daño adicional *solo* en críticos.

Saca 6 en el arma, 4 en el dado de mortal, furia +2. Total: (6 + 4 + 2) × 2 + 4 (mortal, no se dobla) = 24 + 4 = **28**.

> La clave: pregúntate si ese daño se aplicaría en un golpe normal. Si sí, se dobla. Si solo se aplica en críticos (como mortal), no se dobla.

El daño persistente también se dobla en un crítico, salvo que el efecto indique lo contrario (como el conjuro *Flecha Ácida*).

## Críticos en conjuros con tiradas de salvación

Muchos conjuros dañinos no describen los cuatro grados de éxito por separado. En cambio, indican "**tirada de salvación básica de Reflejos**" (o Voluntad, o Fortaleza). La palabra **básica** implica siempre estos cuatro resultados estándar:

| Grado | Daño sufrido |
|---|---|
| Éxito crítico | Ningún daño |
| Éxito | Mitad del daño |
| Fracaso | Daño completo |
| Fracaso crítico | Doble del daño |

**Ejemplo con Bola de Fuego:** Todos los objetivos en el área deben hacer una tirada de salvación básica de Reflejos. Los que obtienen éxito crítico no sufren daño; los que tienen éxito simple reciben 33 PG (la mitad de los 6d6); los que fracasan reciben los 66 PG completos; y los que fracasan críticamente reciben 132 PG (el doble).

Paizo usa esta notación abreviada porque estos mismos cuatro resultados se aplican a la inmensa mayoría de los conjuros dañinos con tirada de salvación, ahorrando espacio en el texto.
