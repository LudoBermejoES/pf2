---
layout: "page"
title: "Encuentros"
chapter: "Introducción"
category: "introduccion"
nav_order: 0
---
# Encuentros

Habra momentos en los que una simple prueba no bastara para resolver un desafio, como cuando unos monstruos se interpongan en el camino. Los encuentros suelen implicar combate, pero tambien persecuciones o esquivar peligros.

## Estructura del encuentro

Un encuentro es una secuencia de turnos donde cada participante actua siguiendo un orden determinado.

- Se tira **iniciativa** para determinar el orden de actuacion
- El encuentro se desarrolla en **asaltos** (cada uno dura aproximadamente 6 segundos)
- Cada participante actua en su turno segun el orden de iniciativa
- El asalto termina cuando todos han actuado, y comienza uno nuevo

### Iniciativa

Al inicio de un encuentro, todos los participantes tiran iniciativa:

| Situacion | Tirada de Iniciativa |
|-----------|---------------------|
| Combate estandar | Percepcion |
| Emboscada (emboscador) | Sigilo |
| Situacion social | Engano o Diplomacia |
| Otras situaciones | Habilidad relevante |

El Director de Juego (DJ) determina que habilidad es apropiada segun las circunstancias.

## Acciones

En tu turno puedes utilizar hasta **tres acciones**. Las acciones se clasifican segun su coste:

### Acciones simples (1 accion)

| Accion | Descripcion |
|--------|-------------|
| Caminar | Moverte hasta tu Velocidad |
| Golpear | Realizar un ataque cuerpo a cuerpo o a distancia |
| Interactuar | Desenvainar un arma, abrir una puerta, recoger un objeto |
| Ponerse en pie | Levantarte si estas derribado |
| Paso | Moverte 1,5 metros sin provocar reacciones |
| Buscar | Intentar detectar algo oculto |
| Soltar | Soltar un objeto que sostienes |

### Actividades (2+ acciones)

Algunas acciones requieren mas tiempo y consumen multiples acciones:

| Actividad | Coste | Descripcion |
|-----------|-------|-------------|
| Lanzar un conjuro | Variable (1-3) | Segun el conjuro |
| Cargar | 2 acciones | Moverte el doble de tu Velocidad |
| Levantarse y moverse | 2 acciones | Combinacion de acciones |
| Preparar | 2 acciones | Preparar una accion para un desencadenante |

### Acciones gratuitas

Las acciones gratuitas no cuentan para tus tres acciones por turno. Pueden tener requisitos especificos o limitaciones de uso.

### Reacciones

Dispones de **1 reaccion por asalto** que puedes usar incluso fuera de tu turno. Las reacciones tienen un desencadenante especifico que debe ocurrir para poder usarlas.

| Reaccion comun | Desencadenante |
|----------------|----------------|
| Ataque de Oportunidad | Una criatura en tu alcance usa accion de manipular, movimiento o ataque a distancia |
| Escudo alzado | Recibes dano fisico mientras tienes el escudo alzado |

## Ataques y Golpes

### Realizar un ataque

**Golpear** es una accion de ataque que consiste en:

1. Elegir un objetivo dentro del alcance de tu arma
2. Tirar 1d20 + modificador de ataque
3. Comparar con la Clase de Armadura (CA) del objetivo

### Resultados de la tirada de ataque

| Resultado | Efecto |
|-----------|--------|
| Exito critico (supera CA por 10+) | Doble dano |
| Exito (iguala o supera CA) | Dano normal |
| Fallo (por debajo de CA) | Sin efecto |
| Fallo critico (falla por 10+) | Posibles efectos negativos adicionales |

### Penalizador por ataque multiple

Cada ataque adicional en el mismo turno sufre un penalizador acumulativo:

| Ataque en el turno | Penalizador |
|--------------------|-------------|
| Primer ataque | 0 |
| Segundo ataque | -5 |
| Tercer ataque (o mas) | -10 |

Este penalizador se reinicia al final de tu turno. Algunas armas con el rasgo agil reducen este penalizador a -4/-8.

## Tiradas de salvacion

Las tiradas de salvacion representan tu capacidad para resistir efectos daninos. Se tiran cuando algo te afecta y debes evitarlo o reducir su impacto.

| Tipo | Atributo | Usos comunes |
|------|----------|--------------|
| Fortaleza | Constitucion | Veneno, enfermedad, efectos fisicos debilitantes |
| Reflejos | Destreza | Esquivar efectos de area (bola de fuego, trampa) |
| Voluntad | Sabiduria | Efectos mentales (hechizar, confusion, miedo) |

### Grados de exito en salvaciones

| Resultado | Efecto tipico |
|-----------|---------------|
| Exito critico | Ningun efecto o efecto muy reducido |
| Exito | Efecto reducido (a menudo la mitad del dano) |
| Fallo | Efecto completo |
| Fallo critico | Efecto aumentado o consecuencias adicionales |

## Dano y Puntos de Golpe

### Puntos de Golpe (PG)

Los Puntos de Golpe representan la salud y vitalidad de una criatura. Cuando recibes dano, se resta de tus PG actuales.

| PG actuales | Estado |
|-------------|--------|
| Maximo | Plena salud |
| Por encima de 0 | Funcional, posiblemente herido |
| 0 | Inconsciente y muriendo |
| Debajo de 0 | No existe; llegas a 0 como minimo |

### Morir y recuperacion

Cuando llegas a 0 PG:

1. Caes **inconsciente**
2. Obtienes el estado **muriendo 1**
3. Al inicio de cada turno, tiras una **prueba plana de recuperacion** (CD 10)

| Resultado de prueba plana | Efecto |
|---------------------------|--------|
| Exito critico | Reduces muriendo en 2 |
| Exito | Reduces muriendo en 1 |
| Fallo | Aumentas muriendo en 1 |
| Fallo critico | Aumentas muriendo en 2 |

Si llegas a **muriendo 4**, tu personaje muere.

### Tipos de dano

El dano puede ser de diversos tipos:

| Categoria | Tipos |
|-----------|-------|
| Fisico | Contundente, cortante, perforante |
| Energia | Acido, frio, electricidad, fuego, sonico |
| Alineamiento | Caotico, maligno, bueno, legal |
| Mental | Dano mental |
| Veneno | Dano de veneno |
| Sagrado/Profano | Dano divino positivo o negativo |

### Resistencias y debilidades

| Concepto | Efecto |
|----------|--------|
| Resistencia X | Reduces el dano de ese tipo en X |
| Debilidad X | Aumentas el dano de ese tipo en X |
| Inmunidad | No recibes dano de ese tipo |

## Estados

Los estados son efectos temporales que modifican las capacidades de una criatura. Algunos estados comunes:

| Estado | Efecto |
|--------|--------|
| Derribado | Estas en el suelo; -2 a tiradas de ataque; +2 a CA contra ataques a distancia, -2 contra cuerpo a cuerpo |
| Agarrado | No puedes moverte; desventaja en CA |
| Asustado X | -X a todas las pruebas y CD |
| Enfermo X | -X a todas las pruebas y CD |
| Ralentizado X | Pierdes X acciones al inicio de tu turno |
| Aturdido X | Pierdes X acciones; no puedes usar reacciones |
| Cegado | No puedes ver; fallas automaticamente pruebas de Percepcion visuales |
| Paralizado | No puedes actuar; CA reducida |
| Inconsciente | No puedes actuar ni percibir; caes derribado |

## Fin del encuentro

Un encuentro termina cuando:

- Todos los enemigos han sido derrotados
- Una parte se rinde o huye
- Se alcanza un objetivo especifico
- El DJ determina que la situacion se ha resuelto

Tras el encuentro, los personajes pueden curar heridas, revisar el botin y prepararse para continuar su aventura.
