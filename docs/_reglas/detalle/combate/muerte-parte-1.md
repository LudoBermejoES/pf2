---
layout: page
permalink: /reglas/detalle/combate/muerte-parte-1/
title: "Muerte Parte 1: Moribundo y Herido"
chapter: Cómo Jugar
category: reglas
nav_order: 999
source: PC1
---

La muerte en PF2e no es instantánea para los personajes jugadores. Este artículo explica el proceso completo de quedar inconsciente, el estado moribundo y el estado herido.

## Proceso básico al llegar a 0 PG

Cuando un PJ llega a 0 Puntos de Golpe, se producen estos pasos en orden:

1. Quedas **inconsciente** y caes al suelo (tumbado).
2. Tu posición de **iniciativa** se mueve a justo antes del turno actual — lo que garantiza que todos tus aliados tienen al menos un turno para ayudarte antes de tu primera prueba de recuperación.
3. Ganas el estado **moribundo 1** (o más, según las circunstancias).
4. Si el valor de moribundo llega a **moribundo 4**, mueres instantáneamente.
5. Al inicio de cada uno de tus turnos mientras estás moribundo, haces una **prueba de recuperación**.

> Los muertos vivientes y los constructos son la excepción: cuando llegan a 0 PG, quedan destruidos directamente.

## Estado: Inconsciente

Estar inconsciente implica todos estos efectos simultáneamente:

- Caes al suelo (**tumbado**) y sueltas lo que sostienes.
- No puedes realizar ninguna acción.
- Sufres penalizador −4 por estatus a la CA, Percepción y salvaciones de Reflejos.
- Ganas los estados **cegado** y **desprevenido**.

Si recibes curación (aunque sea 1 PG), pierdes el estado inconsciente y puedes actuar con normalidad en tu siguiente turno.

## Estado: Moribundo

### Valor inicial de moribundo

| Situación | Valor de moribundo |
|-----------|-------------------|
| Reducido a 0 PG normalmente | Moribundo 1 |
| Impacto crítico del atacante / fallo crítico en tu tirada | +1 adicional |
| Sufres el estado herido | +valor de herido |
| Daño no letal | No ganas moribundo (solo inconsciente) |

### Pruebas de recuperación

Al inicio de cada turno mientras estás moribundo haces una **prueba plana** (sin modificadores) con CD = 10 + tu valor actual de moribundo.

| Resultado | Efecto |
|-----------|--------|
| Éxito crítico | Moribundo −2 |
| Éxito | Moribundo −1 |
| Fallo | Moribundo +1 |
| Fallo crítico | Moribundo +2 |

### Sufrir daño adicional mientras moribundo

Si recibes más daño mientras estás moribundo, tu valor de moribundo aumenta en 1 (o en 2 si es un impacto crítico del atacante o un fallo crítico tuyo). La cantidad de daño es irrelevante.

### Estabilización

Si tu valor de moribundo llega a **0**, pierdes el estado moribundo y te estabilizas: sigues inconsciente a 0 PG, pero ya no haces pruebas de recuperación. Si recibes daño de nuevo, el proceso vuelve a empezar.

## Estado: Herido

Cada vez que pierdes el estado moribundo (al estabilizarte o ser curado), el estado **herido** aumenta en 1. Si ya lo tenías, aumenta en 1; si no, ganas herido 1.

El estado herido hace que la próxima vez que seas reducido a 0 PG comiences con un valor de moribundo más alto: moribundo = 1 + valor de herido.

**Ejemplo de escalada:**

| Vez | Evento | Estado |
|-----|--------|--------|
| 1.ª | Reducido a 0 PG | Moribundo 1 |
| — | Curado → pierde moribundo | Herido 1 |
| 2.ª | Reducido a 0 PG de nuevo | Moribundo 2 (1 + herido 1) |
| — | Curado → pierde moribundo | Herido 2 |
| 3.ª | Reducido a 0 PG de nuevo | Moribundo 3 (1 + herido 2) |

### Cómo eliminar el estado herido

- Ser curado mediante **Tratar Heridas** (habilidad Medicina), con un resultado de al menos 1 PG. Nota: Medicina de Batalla *no* elimina el estado herido.
- Ser curado hasta el **máximo de PG** y descansar **10 minutos**.

## Resumen visual

```
0 PG → Inconsciente + Moribundo X
         │
         ├── Cada turno: Prueba plana (CD 10 + moribundo)
         │       ├── Éxito → moribundo baja
         │       └── Fallo → moribundo sube
         │
         ├── Moribundo 0 → Estabilizado (inconsciente, sin pruebas)
         ├── Recibe curación → Despierta, pierde moribundo, gana Herido +1
         └── Moribundo 4 → MUERTE
```
