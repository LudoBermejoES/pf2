---
layout: page
permalink: /clases/explorador/ejemplos/
title: Ejemplos de Juego - Explorador
chapter: Clases
category: clases
nav_order: 3
class_name: Explorador
source: PC1
---

Estos ejemplos muestran cómo se juega un explorador de nivel 1 en los tres modos de juego de Pathfinder 2e. Nuestro personaje de ejemplo es **Raven**, una exploradora humana cazadora de presas, especializada en arco y rastreo.

---

## Ejemplo de Modo Encuentro

### Situación

Raven y sus compañeros cazan a un gnoll que ha estado atacando caravanas. Lo han rastreado hasta su guarida.

### Estadísticas de Raven (Nivel 1)

| Estadística | Valor |
|-------------|-------|
| CA | 17 (armadura de cuero tachonado) |
| PG | 18 |
| Velocidad | 25 pies |
| Arco corto | +7 a impactar, 1d6 perforante, alcance 60 pies |
| Espada corta | +7 a impactar, 1d6+1 perforante |

### Mecánica Clave: Cacería del Explorador

**Cacería del Explorador** {% include accion.html tipo="1" %}: Designa a una criatura como tu presa cazada.

**Beneficios contra tu presa:**
- Ignoras la penalización de terreno difícil cuando rastreas
- Puedes Buscar tu presa mientras te mueves a velocidad completa
- Tu primer ataque cada turno contra tu presa ignora penalizador por alcance

### Asalto 1: Turno de Raven

El gnoll está a 50 pies, parcialmente oculto tras unas rocas.

> **Jugadora:** "Lo marco como mi presa y disparo."

**Acción 1 {% include accion.html tipo="1" %}: Cacería del Explorador**

Raven designa al gnoll como su presa cazada.

> **Regla:** Cacería del Explorador dura hasta que el combate termine o Raven designe una nueva presa.

**Acción 2 {% include accion.html tipo="1" %}: Golpe (Arco Corto)**

- Alcance: 50 pies (dentro del primer incremento de 60 pies)
- Tirada: 1d20+7 = 17+7 = **24** → **Éxito**
- Daño: 1d6 = **5 de daño perforante**

> **DJ:** "Tu flecha atraviesa el hombro del gnoll. Aúlla y carga hacia ti."

**Acción 3 {% include accion.html tipo="1" %}: Golpe (Arco Corto)**

- Penalizador: -5 (segundo ataque)
- Tirada: 1d20+7-5 = 14+2 = **16** → **Éxito** (CA del gnoll es 15)
- Daño: 1d6 = **4 de daño**

> **DJ:** "Otra flecha lo impacta en el muslo. Tropieza pero sigue avanzando."

### Asalto 2: Turno de Raven

El gnoll está ahora a 15 pies, demasiado cerca para el arco.

> **Jugadora:** "Saco mi espada corta y ataco."

**Acción 1 {% include accion.html tipo="1" %}: Interactuar (Enfundar arco)**

**Acción 2 {% include accion.html tipo="1" %}: Interactuar (Desenfundar espada)**

**Acción 3 {% include accion.html tipo="1" %}: Golpe (Espada Corta)**

- Tirada: 1d20+7 = 19+7 = **26** → **Éxito crítico** (19 = crítico contra CA 15)
- Daño crítico: (1d6+1) × 2 = 5 × 2 = **10 de daño**

> **DJ:** "Tu espada se hunde en el pecho del gnoll mientras carga. Cae a tus pies, derrotado."

### Combate Alternativo: Uso del Borde del Cazador

Si Raven tuviera la dote **Borde del Cazador** (nivel 1):

> **Jugadora:** "Uso Borde del Cazador para hacer un segundo ataque sin penalizador contra mi presa."

**Borde del Cazador:** Tu segundo Golpe contra tu presa durante tu turno no sufre penalizador por ataque múltiple.

Esto convertiría al explorador en un daño a distancia devastador.

### Mecánicas Clave del Explorador

| Mecánica | Efecto |
|----------|--------|
| **Cacería del Explorador** | Designa presa, obtén beneficios al rastrear y atacar |
| **Borde del Cazador** | Segundo ataque sin penalizador vs. presa |
| **Versatilidad** | Eficaz tanto a distancia como cuerpo a cuerpo |
| **Rastreo** | Experto en seguir enemigos |

---

## Ejemplo de Modo Exploración

### Situación

El grupo sigue el rastro de una banda de saqueadores a través de un bosque denso.

### Actividad de Exploración: Rastrear

Raven lidera usando **Rastrear**.

> **Jugadora:** "Sigo las huellas de los saqueadores mientras el grupo me sigue."

**Mecánica:**
- Usa Supervivencia para seguir el rastro
- Mueve a la mitad de velocidad mientras rastrea
- Pero con Cacería del Explorador activa, ignora terreno difícil

### Evento: Rastro Perdido

> **DJ:** "El rastro llega a un arroyo. Las huellas desaparecen."

**Acción: Rastrear (Supervivencia CD 18)**

- Tirada: 1d20+7 = 15+7 = **22** → **Éxito**

> **DJ:** "Encuentras marcas en la orilla opuesta, 100 pies río arriba. Cruzaron para despistar."

### Evento: Campamento Abandonado

Siguiendo el rastro, encuentran un campamento reciente.

> **Jugadora:** "Examino el campamento para saber cuántos son y hace cuánto se fueron."

**Acción: Recordar Conocimiento (Supervivencia CD 15)**

- Tirada: 1d20+7 = 12+7 = **19** → **Éxito**

> **DJ:** "Seis personas acamparon aquí hace unas 4 horas. Se fueron con prisa, dejaron restos de comida. Llevan caballos."

### Tomar Decisiones Tácticas

> **Jugadora:** "Con caballos nos sacarán ventaja. ¿Puedo encontrar un atajo?"

**Acción: Supervivencia (encontrar ruta alternativa) CD 18**

- Tirada: 1d20+7 = 13+7 = **20** → **Éxito**

> **DJ:** "Hay un paso entre colinas que les cortará el camino. Si corréis, llegaréis antes que ellos al cruce."

### Preparar Emboscada

El grupo se adelanta y prepara una emboscada.

> **Jugadora:** "Me escondo entre los arbustos con el arco listo."

**Actividad de Exploración: Evitar ser Detectado (Sigilo)**

- Tirada de Sigilo: 1d20+6 = 17+6 = **23**
- Este será el CD para que los saqueadores la detecten

> **DJ:** "Cuando los saqueadores llegan, no te ven. Tienes la primera acción."

### Actividades de Exploración para Exploradores

| Actividad | Uso |
|-----------|-----|
| **Rastrear** | Seguir criaturas, encontrar guaridas |
| **Explorar** | Reconocer terreno, encontrar recursos |
| **Evitar Detección** | Moverse sigilosamente, preparar emboscadas |
| **Buscar** | Detectar trampas naturales, predadores |

---

## Ejemplo de Modo Tiempo Libre

### Situación

El grupo pasa una semana en una villa fronteriza. Raven aprovecha para reabastecerse y recoger información.

### Días 1-3: Cazar para la Villa

La villa necesita carne fresca. Raven ofrece sus servicios.

> **Jugadora:** "Cazo en el bosque cercano para alimentar a la villa y ganar algo de dinero."

**Actividad: Ganar Dinero** (Supervivencia, CD 15)

| Día | Tirada | Resultado | Ganancia |
|-----|--------|-----------|----------|
| 1 | 22 | Éxito | 2 pp + 1 ciervo |
| 2 | 19 | Éxito | 2 pp + varios conejos |
| 3 | 25 | Éxito crítico | 4 pp + jabalí grande |

**Ingresos:** 8 pp = **8 pp**

> **DJ:** "Los aldeanos están encantados. El carnicero te ofrece un descuento en suministros."

### Días 4-5: Reunir Información

Raven pregunta sobre los bandidos de la zona.

> **Jugadora:** "Hablo con cazadores y leñadores locales sobre actividad sospechosa en el bosque."

**Actividad: Reunir Información** (Supervivencia o Diplomacia, CD 15)

- Día 4: 1d20+7 = 18 → **Éxito**
  - "Hay una vieja fortaleza abandonada al norte. Se ven luces por la noche."

- Día 5: 1d20+7 = 21 → **Éxito**
  - "Los bandidos tienen un contacto en la villa. Nadie sabe quién es."

### Día 6: Elaborar Flechas

Raven repone su munición.

> **Jugadora:** "Compro materiales y fabrico flechas."

**Actividad: Elaborar** (Artesanía, CD 10 para flechas básicas)

- Coste de materiales: 5 pp por 10 flechas
- Tirada: 1d20+3 = 15 → **Éxito**
- Resultado: 20 flechas por 1 po de materiales

### Día 7: Reconocimiento

Raven explora los alrededores de la fortaleza mencionada.

> **Jugadora:** "Voy sola a explorar la fortaleza, sin acercarme demasiado."

**Actividad: Reconocimiento** (Sigilo + Supervivencia)

**Sigilo (para no ser detectada) CD 15:**
- Tirada: 1d20+6 = 19 → **Éxito**

**Supervivencia (observar desde lejos) CD 15:**
- Tirada: 1d20+7 = 22 → **Éxito**

**Información obtenida:**
- Aproximadamente 15 bandidos
- Guardias en la torre día y noche
- Un camino oculto por el lado este menos vigilado

### Resumen de la Semana

| Actividad | Días | Resultado |
|-----------|------|-----------|
| Cazar | 3 | +8 pp, reputación |
| Reunir información | 2 | Intel sobre bandidos |
| Elaborar flechas | 1 | +20 flechas (-1 po) |
| Reconocimiento | 1 | Mapa de la fortaleza |
| **Total** | 7 | -2 pp neto, información valiosa |

### Actividades de Tiempo Libre para Exploradores

| Actividad | Beneficio |
|-----------|-----------|
| **Cazar** | Ganar dinero, obtener materiales |
| **Reunir Información** | Intel sobre enemigos, terreno, contactos |
| **Elaborar** | Crear flechas, trampas, equipo de supervivencia |
| **Reconocimiento** | Explorar ubicaciones enemigas de forma segura |
| **Entrenar Animal** | Si tienes compañero animal |

---

## Consejos para Jugar un Explorador de Nivel 1

1. **Marca tu presa:** Cacería del Explorador es gratis y dura todo el combate. Úsala siempre
2. **Controla la distancia:** Eres mejor a distancia. Mantén enemigos lejos si puedes
3. **Prepara emboscadas:** Tu Sigilo y rastreo te permiten elegir cuándo y dónde luchar
4. **Versatilidad:** Lleva armas cuerpo a cuerpo de respaldo. Las necesitarás
5. **Fuera de combate brillas:** Rastrear, explorar y sobrevivir son tus puntos fuertes
