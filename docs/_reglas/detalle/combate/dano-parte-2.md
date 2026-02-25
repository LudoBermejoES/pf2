---
layout: page
title: "Daño: Precisión, Persistente y Tipos Especiales"
permalink: /reglas/detalle/combate/dano-parte-2/
chapter: Cómo Jugar
category: reglas
---

En la [Parte 1](/reglas/detalle/combate/dano-parte-1/) vimos el proceso básico del daño: tirar, aplicar resistencias, debilidades e inmunidades. Aquí cubrimos los tipos de daño con comportamientos más específicos.

## Daño de Precisión

El daño de precisión es daño adicional que otorgan ciertas habilidades —como el **ataque furtivo** del pícaro— que representan atacar en el punto exacto donde más duele.

La regla clave es que el daño de precisión **aumenta el tipo base del ataque**, no es un tipo de daño independiente.

**Ejemplo:** Un pícaro de nivel 1 realiza un ataque furtivo con una daga. La daga inflige 1d4 de daño perforante, y el ataque furtivo añade 1d6 de daño de precisión. El resultado no es "1d4 perforante + 1d6 precisión": es **1d4 + 1d6 de daño perforante**, todo perforante.

### Por qué importa esto: resistencias

Imagina que ese mismo pícaro ataca a un esqueleto con **resistencia 5 al daño perforante**. Saca 2 en la daga y 6 en el ataque furtivo → total: 8 PG de daño perforante → menos resistencia 5 → **3 PG de daño final**.

Si el daño de precisión fuese un tipo separado, el esqueleto solo absorbería los 2 de la daga pero recibiría los 6 de precisión íntegros. Eso no es correcto: todo el daño es perforante y toda la resistencia se aplica al total.

### Por qué importa esto: debilidades

Del mismo modo, si el objetivo tiene debilidad al daño perforante 5, la debilidad se añade al total combinado una sola vez, no por separado a cada fuente.

### Criaturas con inmunidad a críticos

Algunas criaturas (ciertos constructos y no muertos) son inmunes a los críticos y al daño de precisión. En esos casos, el ataque furtivo no añade daño extra aunque se cumplan los requisitos de posición.

## Daño Persistente

El daño persistente es una **condición** que hace que el daño se repita turno tras turno. Hemorragia por una herida grave, quemaduras, ácido corroendo la piel: todos son ejemplos de daño persistente.

### Cómo funciona

Cuando sufres daño persistente:

1. **Al final de cada uno de tus turnos** sufres la cantidad indicada de ese tipo de daño.
2. Inmediatamente después, realizas una **prueba plana CD 15** (sin modificadores, solo 1d20):
   - **15 o más:** La condición de daño persistente desaparece.
   - **14 o menos:** Continúa. Sufrirás el daño de nuevo al final de tu siguiente turno.

**Ejemplo:** Recibes daño persistente de fuego 5. Al final de tu turno sufres 5 PG de fuego y tiras 1d20. Si sacas 12, el fuego continúa. Si sacas 17, el fuego se extingue.

### Recuperación asistida

No estás a merced solo de la prueba plana. Tú o un aliado podéis gastar **2 acciones** en una **recuperación asistida**: explicas al DJ qué estás haciendo para eliminar el efecto y el DJ determina el resultado:

| Acción | Resultado habitual |
|---|---|
| Apagarte las llamas con las manos | Prueba plana CD 15 inmediata adicional |
| Verter agua de tu cantimplora | CD reducida a 10 |
| Saltar a un río o estanque | El fuego se apaga automáticamente |
| Que un aliado cure la hemorragia | El DJ puede eliminar el daño de hemorragia directamente |

El DJ tiene libertad para adaptar el resultado a la lógica de la situación. Por ejemplo, puede eliminar automáticamente el daño de hemorragia si el personaje recibe curación suficiente.

### Resistencias, debilidades y daño persistente

Las resistencias y debilidades se aplican **por separado** al daño persistente y al daño inicial del ataque. Son dos instancias de daño distintas.

**Ejemplo:** Un martillo de llamas inflige 1d8 de daño contundente + 1d4 de daño persistente de fuego. El objetivo tiene debilidad 5 al daño contundente y debilidad 5 al daño de fuego.

- Golpe inicial: 1d8 contundente + debilidad contundente 5 (se aplica una vez).
- Daño persistente: 1d4 de fuego + debilidad fuego 5 (se aplica al final de cada turno que el persistente esté activo).

### Daño persistente y críticos

Si el ataque que aplica el daño persistente es un **éxito crítico**, el daño persistente también se dobla. El pícaro que lanza un frasco de ácido y obtiene un crítico no aplica 1d6 de daño persistente de ácido, sino **2d6**.

### El DJ puede eliminar el daño persistente

En ciertas situaciones, el DJ puede determinar que el daño persistente no se aplica o desaparece sin prueba. Por ejemplo, si un arma cortante que inflige daño persistente de hemorragia no supera en absoluto la resistencia al daño cortante del objetivo, el DJ puede determinar que la herida no es lo bastante profunda para sangrar.

## Daño de Alineamiento → Remaster

> **Nota importante:** El vídeo del que procede este artículo describe el **daño de alineamiento** (caótico, legal, bueno, malvado) tal como existía en la edición original de PF2e. **En el Remaster (2023) este sistema fue eliminado.** Si juegas con el Remaster, usa la siguiente equivalencia:

| Edición original | Remaster |
|---|---|
| Daño bueno | Daño espiritual con rasgo **Santo** |
| Daño malvado | Daño espiritual con rasgo **Profano** |
| Daño caótico | Eliminado / daño espiritual sin equivalente directo |
| Daño legal | Eliminado / daño espiritual sin equivalente directo |
| Resistencia/debilidad al daño bueno | Resistencia/debilidad a **Santo** |
| Resistencia/debilidad al daño malvado | Resistencia/debilidad a **Profano** |

En el Remaster, el daño "bueno" o "malvado" que infligían conjuros como *Lanza Divina* se convierte en **daño espiritual** con el rasgo Santo o Profano (según la santificación del lanzador). Solo afecta a criaturas con el rasgo opuesto o con debilidad explícita.

El daño "caótico" y "legal" prácticamente desaparecen como tipos de daño. Los efectos que antes los usaban han sido rediseñados.

Ver [Santificación](/reglas/detalle/personajes/santificacion/) para una guía completa del sistema Remaster de Santo/Profano.

## Daño de Vitalidad y de Vacío

Estos dos tipos reemplazan al "daño positivo" y "daño negativo" del sistema original:

- **Daño de Vitalidad:** Solo daña a los no muertos. Sin efecto en criaturas vivas u objetos.
- **Daño de Vacío:** Solo daña a las criaturas vivas. Sin efecto en no muertos u objetos.

Algunos efectos usan *energía* de Vitalidad o Vacío (que puede curar o dañar según la criatura); otros aplican directamente *daño* de Vitalidad o Vacío (solo tienen efecto dañino). Ver [Daño: Fundamentos](/reglas/detalle/combate/dano-parte-1/) para más detalle.
