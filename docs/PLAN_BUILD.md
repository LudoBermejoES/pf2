  # Plan de Configuraciones Divertidas para Pathfinder 2e Remaster

Este documento contiene 3 configuraciones divertidas y efectivas para cada clase del Pathfinder 2e Remaster, basadas en investigación de guías populares, foros de la comunidad y recursos especializados.

---

## Plan de Implementación

### Objetivo
Crear archivos `.md` individuales para cada configuración/build y enlazarlos desde las páginas de índice de cada clase.

### Estructura de Archivos Propuesta

```
docs/_clases/
├── barbaro/
│   ├── index.md              # Descripción de la clase + enlaces a builds
│   ├── caracteristicas.md    # (ya existe)
│   ├── dotes.md              # (ya existe)
│   └── builds/
│       ├── furia-del-dragon.md
│       ├── gigante-con-alcance.md
│       └── espiritual-totemico.md
├── campeon/
│   ├── index.md
│   ├── builds/
│       ├── redentor-protector.md
│       ├── liberador-movilidad.md
│       └── paladin-castigador.md
├── guerrero/
│   └── builds/
│       ├── duelista-doble-arma.md
│       ├── escudo-reactivo.md
│       └── arquero-precision.md
... (igual para todas las clases)
└── kingmaker/
    └── builds/
        ├── clerigo-erastil.md
        ├── explorador-tierras-robadas.md
        ├── hechicero-feerico.md
        ├── druida-bosque-verde.md
        ├── duelista-aldori.md
        └── bardo-cronista.md
```

### Formato de Archivo de Build

Cada archivo `.md` de build tendrá:

```yaml
---
layout: page
title: "Nombre de la Build"
permalink: /clases/[clase]/builds/[nombre-build]/
parent: [Clase]
category: builds
source: PC1/PC2
tags: [daño/tanque/apoyo/control]
recommended: false           # true para builds recomendadas (Kingmaker, etc.)
adventure_path: null         # "Kingmaker" si es específica de esa AP
---
```

### Modificaciones a index.md de Clases

Añadir sección "Builds Recomendadas" con enlaces. **IMPORTANTE**: Las builds recomendadas para Sendas de Aventura (como Kingmaker) deben:
1. Aparecer **primero** en la lista
2. Llevar la etiqueta **"⭐ Recomendada para Kingmaker"** (o la AP correspondiente)

```markdown
## Builds Recomendadas

Configuraciones probadas y divertidas para esta clase:

### Para Kingmaker
- ⭐ [Clérigo Arquero de Erastil](builds/clerigo-erastil/) - **Recomendada para Kingmaker** - Sanador y cazador devoto del Viejo Desencadenado

### Builds Generales
- [Redentor Protector](builds/redentor-protector/) - Tanque que protege aliados con reacciones
- [Liberador de Alta Movilidad](builds/liberador-movilidad/) - Combate montado y rescate de aliados
- [Paladín Castigador](builds/paladin-castigador/) - Daño contra enemigos profanos
```

### Orden de Visualización en index.md

Para cada clase que tenga builds de Kingmaker, el orden será:
1. **Builds Recomendadas para Sendas de Aventura** (con ⭐ y etiqueta)
2. **Builds Generales** (las 3 configuraciones estándar)

Clases con builds de Kingmaker:
- **Clérigo**: Clérigo Arquero de Erastil
- **Explorador**: Explorador de las Tierras Robadas
- **Hechicero**: Hechicero del Linaje Feérico
- **Druida**: Druida del Bosque Verde
- **Guerrero/Espadachín**: Duelista Aldori
- **Bardo**: Bardo Cronista del Reino

### Requisitos de Verificación y Enlaces

**IMPORTANTE**: Antes de crear cada archivo de build, se debe verificar y enlazar:

#### 1. Verificación de Dotes (Feats)
- [ ] Verificar que cada dote mencionada **existe** en `docs/_clases/[clase]/dotes.md`
- [ ] Si la dote NO existe, marcarla con ✗ y buscar el nombre correcto
- [ ] Si la dote existe, marcarla con ✓

#### 2. Enlaces Obligatorios
Todos los elementos enlazables deben tener enlaces en formato Liquid:

```markdown
**Dotes de clase:**
- [Momento de Claridad]({{ '/clases/barbaro/dotes/#momento-de-claridad' | relative_url }})
- [Postura del Dragón]({{ '/clases/monje/dotes/#postura-del-dragon' | relative_url }})

**Dotes de habilidad:**
- [Intimidación Aterradora]({{ '/dotes/habilidad/intimidacion-aterradora/' | relative_url }})

**Habilidades:**
- [Atletismo]({{ '/habilidades/atletismo/' | relative_url }})
- [Intimidación]({{ '/habilidades/intimidacion/' | relative_url }})

**Armas:**
- [Espada bastarda]({{ '/equipo/armas/espada-bastarda/' | relative_url }})

**Armaduras:**
- [Placas completas]({{ '/equipo/armaduras/placas-completas/' | relative_url }})

**Conjuros:**
- [Bola de Fuego]({{ '/conjuros/bola-de-fuego/' | relative_url }})

**Ascendencias/Bagajes:**
- [Espadachín de Aldori]({{ '/ascendencias/bagajes/espadachin-de-aldori/' | relative_url }})

**Deidades:**
- [Erastil]({{ '/setting/deidades/erastil/' | relative_url }})
```

#### 3. Checklist por Build
Antes de finalizar cada archivo `.md`:
- [ ] ¿Todas las dotes existen y están verificadas con ✓?
- [ ] ¿Todas las dotes tienen enlace a su página?
- [ ] ¿Todas las habilidades mencionadas tienen enlace?
- [ ] ¿Las armas y armaduras tienen enlace (si existe la página)?
- [ ] ¿Los conjuros clave tienen enlace?
- [ ] ¿El bagaje recomendado tiene enlace?
- [ ] ¿La deidad (si aplica) tiene enlace?

#### 4. Rutas de Verificación
Ubicaciones para verificar existencia de contenido:
- **Dotes de clase**: `docs/_clases/[clase]/dotes.md`
- **Dotes de habilidad**: `docs/_dotes/habilidad/[nombre].md`
- **Habilidades**: `docs/_habilidades/[nombre].md`
- **Armas**: `docs/_equipo/armas/[nombre].md`
- **Armaduras**: `docs/_equipo/armaduras/[nombre].md`
- **Conjuros**: `docs/_conjuros/[nombre].md`
- **Bagajes**: `docs/_ascendencias/bagajes/[nombre].md`

#### 5. Manejo de Enlaces Rotos
Si una página no existe todavía:
- Crear el enlace igualmente (para cuando se cree la página)
- Añadir comentario `<!-- TODO: crear página -->` junto al enlace
- Registrar en la sección de tareas pendientes

---

### Tareas Pendientes

- [ ] Crear carpeta `builds/` en cada directorio de clase
- [ ] Generar archivos `.md` individuales para cada configuración (51 builds totales)
  - [ ] Bárbaro: 3 builds
  - [ ] Campeón: 3 builds
  - [ ] Guerrero: 3 builds
  - [ ] Espadachín: 3 builds
  - [ ] Pícaro: 3 builds
  - [ ] Explorador: 3 builds
  - [ ] Monje: 3 builds
  - [ ] Mago: 3 builds
  - [ ] Hechicero: 3 builds
  - [ ] Clérigo: 3 builds
  - [ ] Druida: 3 builds
  - [ ] Oráculo: 3 builds
  - [ ] Bardo: 3 builds
  - [ ] Alquimista: 3 builds
  - [ ] Taumaturgo: 3 builds
  - [ ] Investigador: 3 builds
  - [ ] Brujo: 3 builds
  - [ ] Kingmaker: 6 builds especiales
- [ ] **Verificar todas las dotes** mencionadas en cada build
- [ ] **Añadir enlaces** a todas las dotes, habilidades, armas, conjuros, etc.
- [ ] Actualizar `index.md` de cada clase con sección de builds y enlaces
- [ ] Actualizar sidebar para mostrar builds como subsección

### Prioridad de Implementación

1. **Fase 1**: Clases PC1 más populares (Guerrero, Mago, Clérigo, Pícaro)
2. **Fase 2**: Resto de clases PC1
3. **Fase 3**: Clases PC2 (Espadachín, Investigador, Oráculo, Brujo, Taumaturgo)
4. **Fase 4**: Builds especiales de Kingmaker

---

## Índice de Clases

### Clases Marciales
- [Bárbaro](#bárbaro)
- [Campeón](#campeón)
- [Guerrero (Fighter)](#guerrero-fighter)
- [Espadachín (Swashbuckler)](#espadachín-swashbuckler)

### Clases de Habilidad
- [Investigador](#investigador)
- [Pícaro (Rogue)](#pícaro-rogue)
- [Explorador (Ranger)](#explorador-ranger)
- [Monje](#monje)

### Lanzadores Arcanos
- [Mago](#mago)
- [Brujo (Witch)](#brujo-witch)
- [Hechicero (Sorcerer)](#hechicero-sorcerer)

### Lanzadores Divinos
- [Clérigo](#clérigo)
- [Oráculo](#oráculo)

### Lanzadores Primarios
- [Druida](#druida)

### Lanzadores Ocultos
- [Bardo](#bardo)

### Clases Especiales
- [Alquimista](#alquimista)
- [Taumaturgo](#taumaturgo)

---

## Bárbaro

### Configuración 1: Furia del Dragón
**Concepto**: En lo más profundo de tu linaje corre la sangre de un dragón ancestral, un poder que despierta cuando la ira te consume. Al entrar en furia, escamas comienzan a brotar por tu piel, tu aliento se convierte en un torrente de energía elemental devastadora, y con el tiempo, alas majestuosas surgen de tu espalda. Eres la encarnación mortal de la furia dracónica, un guerrero que hace temblar a sus enemigos con el mismo terror que inspiran los grandes wyrms.
- **Instinto**: Dragón (Plata o Blanco recomendado para daño de frío - menos resistido)
- **Atributos**: Prioriza Fuerza (+4), luego Constitución (+3), Destreza y Sabiduría secundarios (+1)
- **Arma**: Espada bastarda o Hacha de guerra
- **Dotes clave**:
  - Nivel 1: Momento de Claridad ✓
  - Nivel 1: Arrogancia Dracónica ✓
  - Nivel 6: Aliento de Ira Dracónica ✓
  - Nivel 12: Alas de Ira Dracónica ✓
  - Nivel 16: Transformación Dracónica ✓
- **Estilo de juego**: Daño de energía que ignora resistencias físicas, culminando en transformación dracónica.

### Configuración 2: Gigante con Alcance
**Concepto**: Llevas en ti el espíritu de los gigantes primordiales, aquellos colosos que moldearon montañas y derrumbaron fortalezas con sus manos desnudas. En combate, tu estatura se vuelve legendaria: empuñas armas del tamaño de un hombre que barren el campo de batalla como guadañas segando trigo. Donde tú estás, ningún enemigo está a salvo, pues tu alcance abarca todo lo que te rodea, convirtiendo cada encuentro en una danza de destrucción titánica.
- **Instinto**: Gigante
- **Atributos**: Prioriza Fuerza (+4), luego Constitución (+3), Destreza secundaria (+1)
- **Arma**: Arma de tamaño Grande (gratis con el instinto) - Guadaña o Martillo de guerra
- **Dotes clave**:
  - Nivel 1: Ataque de Oportunidad ✓ (capacidad de clase con Instinto Gigante)
  - Nivel 6: Estatura de Gigante ✓
  - Nivel 8: Abusón Furioso ✓
  - Nivel 12: Estatura de Titán ✓
  - Nivel 14: Estocada de Gigante ✓
- **Estilo de juego**: Control del campo de batalla con alcance masivo, amenazando un área enorme.

### Configuración 3: Bárbaro Espiritual Totémico
**Concepto**: Un vínculo sagrado te une a los espíritus animales de la naturaleza salvaje. Cuando la furia te posee, no es simple rabia lo que te impulsa, sino el espíritu primordial de tu animal tótem: la tenacidad del oso, la astucia del lobo, o la velocidad del ciervo. Tu piel se endurece como cuero curtido, tus sentidos se agudizan, y por momentos, la línea entre guerrero y bestia se difumina. Eres el puente entre el mundo mortal y el reino de los espíritus salvajes.
- **Instinto**: Animal (Lobo, Oso o Ciervo)
- **Atributos**: Prioriza Fuerza y Constitución (+3 ambos), Destreza (+2), Sabiduría secundaria (+1)
- **Arma**: Depende del animal - Garras (Lobo), Mandíbulas (Oso)
- **Dotes clave**:
  - Nivel 6: Piel Animal ✓
  - Nivel 4: Atleta Rabioso ✓
  - Nivel 8: Vigor Renovado ✓ (antes "Furia Renovada" - nombre incorrecto)
  - Nivel 8: Compartir Ira ✓
- **Estilo de juego**: Más defensivo que otros bárbaros, con transformaciones animales.

---

## Campeón

> **Nota Remaster**: En el Remaster, el Campeón usa el sistema de Santificado/Profano en lugar de alineamientos. Las causas (Paladín, Redentor, Liberador, Desraizador, Déspota, Antipaladín) determinan tu reacción especial y si eres santificado o profano.

### Configuración 1: Redentor Protector
**Concepto**: Crees fervientemente que incluso el alma más oscura puede encontrar la redención. Tu escudo no es solo metal y madera, sino un símbolo de la misericordia divina que extiendes a todos, incluso a tus enemigos. Cuando un aliado está en peligro, tu cuerpo y tu fe se interponen como un muro inquebrantable. Los golpes que deberían destrozar a tus compañeros se desvanecen contra tu determinación sagrada, y aquellos que osan atacar a los que proteges descubren que su fuerza se desvanece ante tu presencia bendita.
- **Causa**: Redentor
- **Atributos**: Prioriza Fuerza y Carisma (+3 ambos), Constitución (+2), Sabiduría secundaria (+1)
- **Arma**: Espada larga + Escudo
- **Armadura**: Placas completas
- **Aliado Divino**: Escudo
- **Dotes clave**:
  - Nivel 1: Corcel Fiel ✓ o Dominio del Campeón ✓
  - Nivel 6: Guardián del Escudo ✓
  - Nivel 6: Expandir Aura ✓
  - Nivel 8: Bloqueo con Escudo Rápido ✓
- **Estilo de juego**: Reacción para reducir daño a aliados y Enfeeble al atacante. Muy difícil de matar.
- **Nota**: Imposición de manos es un conjuro de devoción (capacidad de clase), no una dote.

### Configuración 2: Liberador de Alta Movilidad
**Concepto**: La libertad es tu credo sagrado, y ninguna cadena, trampa o restricción puede mantener cautivos a aquellos bajo tu protección. Cabalgando sobre tu corcel bendecido, llegas como un rayo de esperanza al rescate de los oprimidos. Donde otros campeones permanecen firmes como rocas, tú fluyes como el viento: liberando aliados de garras, tentáculos y magia restrictiva, permitiéndoles escapar y reagruparse mientras cubres su retirada. Eres el caballero errante que rompe cadenas y abre caminos.
- **Causa**: Liberador
- **Atributos**: Prioriza Fuerza (+3), Destreza, Constitución y Carisma equilibrados (+2)
- **Arma**: Lucero del alba + Escudo
- **Aliado Divino**: Corcel (Compañero Animal)
- **Dotes clave**:
  - Nivel 1: Corcel Fiel ✓
  - Nivel 4: Aura de Coraje ✓
  - Nivel 6: Montura Leal ✓
  - Nivel 10: Corcel Imponente ✓
- **Estilo de juego**: Combate montado, liberando aliados de restricciones mientras cabalga al rescate.
- **Nota**: Imposición de manos es un conjuro de devoción (capacidad de clase), no una dote.

### Configuración 3: Paladín Castigador
**Concepto**: Donde otros campeones perdonan, tú castigas. Tu fe es un fuego purificador que no tolera la maldad, y cada ataque contra un inocente es respondido con la ira sagrada de tu deidad. Tu espada brilla con luz divina cuando golpea a los profanos, y aquellos que osan atacar a tus aliados descubren que han despertado una tormenta de represalias. No eres un muro que absorbe golpes, sino un martillo que los devuelve multiplicados. La justicia, en tus manos, es swift y devastadora.
- **Causa**: Paladín
- **Atributos**: Prioriza Fuerza (+4), Constitución y Carisma secundarios (+2)
- **Arma**: Espada de dos manos (Espadón) o Martillo de guerra
- **Aliado Divino**: Hoja
- **Dotes clave**:
  - Nivel 1: Avance Defensivo ✓
  - Nivel 4: Aura de Coraje ✓
  - Nivel 6: Golpe Retributivo a Distancia ✓ (antes "Ataque del Desafío" - no existe)
  - Nivel 10: Armamento Radiante ✓
- **Estilo de juego**: Daño extra contra enemigos profanos, contraataques frecuentes.

---

## Guerrero (Fighter)

### Configuración 1: Duelista de Doble Arma
**Concepto**: Dos hojas centellean en tus manos como las alas de un colibrí mortal. Donde otros guerreros dependen de golpes contundentes, tú has perfeccionado el arte del acero gemelo: una danza letal de estocadas, paradas y contraataques que abruma a tus oponentes con una lluvia incesante de cortes. Tu defensa y tu ofensa son una misma cosa, pues cada parada se convierte en un ataque y cada ataque prepara el siguiente. Los enemigos que se enfrentan a ti descubren demasiado tarde que están luchando contra una tormenta de acero.
- **Atributos**: Prioriza Destreza (+4), Constitución secundaria (+2), Fuerza terciaria (+1)
- **Armas**: Rapier + Espada corta o Espada Aldori + Daga
- **Armadura**: Cuero tachonado o Cota de malla ligera
- **Dotes clave**:
  - Nivel 1: Doble Tajo ✓
  - Nivel 2: Parada Gemela ✓
  - Nivel 4: Distracción Gemela ✓ (antes "Finta Gemela")
  - Nivel 6: Réplica Gemela ✓ (antes "Riposte Gemela")
  - Nivel 16: Defensa Gemela ✓ (antes "Posición de Doble Arma" - nombre y nivel incorrectos)
- **Estilo de juego**: Muchos ataques con penalización reducida, defensa con parada gemela.

### Configuración 2: Guerrero de Escudo Reactivo
**Concepto**: Tu escudo no es solo una defensa, es una promesa: cualquiera que te ataque pagará el precio. Has convertido el arte del bloqueo en una ciencia mortal, donde cada golpe enemigo rebota contra tu escudo solo para encontrarse con tu contraataque devastador. Eres el centro inamovible del campo de batalla, una fortaleza viviente que invita a los enemigos a estrellarse contra ti. Mientras tus aliados danzan alrededor tuyo, tú permaneces firme, absorbiendo el castigo y devolviéndolo con intereses.
- **Atributos**: Prioriza Fuerza (+4), Constitución (+3), Destreza secundaria (+1)
- **Armas**: Espada larga/Hacha de batalla + Escudo pesado
- **Armadura**: Placas completas
- **Dotes clave**:
  - Nivel 1: Escudo Reactivo ✓
  - Nivel 2: Bloqueo Agresivo ✓
  - Nivel 4: Embestida con Escudo ✓ (antes "Golpe de Escudo" - no existe)
  - Nivel 6: Guardián Escudo ✓
  - Nivel 8: Bloqueo con el Escudo Rápido ✓
- **Estilo de juego**: Bloquea, contraataca, nunca muere. Simple pero devastador.

### Configuración 3: Arquero de Precisión
**Concepto**: Donde otros arqueros disparan flechas, tú disparas sentencias de muerte. Tu dominio del arco trasciende la simple puntería: cada flecha vuela con una precisión sobrenatural, encontrando las grietas en la armadura, los puntos vitales desprotegidos, las debilidades que otros ni siquiera ven. La maestría marcial del guerrero aplicada al arco significa que tus flechas impactan con una frecuencia de golpes críticos que otros arqueros solo pueden soñar. A cien pasos de distancia, eres tan letal como cualquier espadachín cuerpo a cuerpo.
- **Atributos**: Prioriza Destreza (+4), Fuerza (+2 para arcos compuestos), Sabiduría secundaria (+1)
- **Arma**: Arco largo compuesto
- **Armadura**: Cuero
- **Dotes clave**:
  - Nivel 1: Disparo de Ayuda ✓
  - Nivel 2: Disparo Doble ✓
  - Nivel 6: Disparo Triple ✓
  - Nivel 8: Posición de Disparo Móvil ✓
  - Nivel 10: Disparo Debilitante ✓
  - Nivel 10: Disparo Múltiple
- **Estilo de juego**: Alto daño a distancia, excelente precisión gracias a la progresión de competencia del guerrero.

---

## Espadachín (Swashbuckler)

### Configuración 1: Pistolero Fanfarrón
**Concepto**: Con una pistola humeante en una mano y una rapier centelleante en la otra, encarnas el espíritu romántico del pirata legendario. Cada disparo es un espectáculo, cada estocada viene acompañada de una sonrisa desafiante. Tu estilo de combate es pura teatralidad mortal: disparas desde la distancia para ganar confianza y aplomo, luego te lanzas al combate cuerpo a cuerpo para rematar con un floreo devastador. Los bardos cantarán sobre tus hazañas, y tú te asegurarás de darles material digno de baladas.
- **Estilo**: Pistolero (Bravado)
- **Atributos**: Prioriza Destreza (+4), Carisma (+3), Constitución secundaria (+1)
- **Armas**: Pistola + Rapier
- **Dotes clave**:
  - Nivel 1: Broquel Elegante ✓ o Cuchilla Voladora ✓
  - Nivel 2: Desenfundado Ostentoso ✓
  - Nivel 4: Remate Desequilibrante ✓
  - Nivel 6: Lanzamiento Giratorio ✓
  - Nivel 8: Remate Aturdidor ✓
- **Estilo de juego**: Dispara, gana Aplomo, acércate para el Remate devastador.
- **Nota**: Espadachín no tiene dotes específicas de pistola; usar arquetipo Pistolero.

### Configuración 2: Duelista Gimnástico
**Concepto**: El campo de batalla es tu escenario y cada superficie es una oportunidad. Mientras otros luchan con los pies plantados en el suelo, tú saltas sobre mesas, te deslizas bajo espadas, rebotás en paredes y conviertes cada combate en una coreografía imposible de acrobacias mortales. Tu espada encuentra su objetivo mientras giras en el aire, y tus enemigos no pueden predecir desde qué ángulo llegará tu próximo ataque. Eres el duelista que hace que el combate parezca un ballet, aunque un ballet donde solo tú sales vivo.
- **Estilo**: Gimnasta
- **Atributos**: Prioriza Destreza (+4), Carisma (+2), Fuerza secundaria (+1)
- **Arma**: Rapier o Sable
- **Dotes clave**:
  - Nivel 1: Caída de Gato ✓ (dote de habilidad)
  - Nivel 1: Caída en Picado ✓
  - Nivel 4: Atleta Extravagante ✓
  - Nivel 6: Voltereta Vejatoria ✓
  - Nivel 8: Rodar Llamativo ✓
- **Estilo de juego**: Volteretas, saltos, tropiezos - el espadachín más móvil.

### Configuración 3: Espadachín Ingenioso (Wit)
**Concepto**: Tu lengua es tan afilada como tu espada, y a menudo más peligrosa. Mientras otros espadachines dependen de la fuerza o la agilidad, tú has dominado el arte de la guerra psicológica. Tus burlas certeras hacen hervir la sangre de tus enemigos, tus comentarios mordaces los distraen en el momento crucial, y cuando pierden la compostura, tu estocada encuentra su marca. Eres el duelista que derrota a sus oponentes mentalmente antes de tocarlos con el acero, el maestro de la provocación convertida en arte mortal.
- **Estilo**: Ingenioso (Wit)
- **Atributos**: Prioriza Carisma (+4), Destreza (+3), Inteligencia secundaria (+1)
- **Arma**: Espada corta o Estoque
- **Dotes clave**:
  - Nivel 1: Fascinación Concentrada ✓
  - Nivel 2: Finta Provocadora ✓
  - Nivel 2: Antagonizar ✓
  - Nivel 4: Disfrutar el Espectáculo ✓
  - Nivel 8: Fanfarronería Vivaz ✓
- **Estilo de juego**: Control social y mental, confunde enemigos, Portavoz del grupo.

---

## Pícaro (Rogue)

### Configuración 1: Ladrón Clásico (Thief)
**Concepto**: Las sombras son tu hogar y la daga tu mejor amiga. Te deslizas invisible entre los enemigos, apareciendo solo cuando tu hoja ya está hundida en un punto vital, para desvanecerte de nuevo antes de que puedan reaccionar. Eres el fantasma del campo de batalla, el susurro de acero que los guerreros temen pero nunca ven venir. Tu agilidad felina te permite entrar y salir del combate a voluntad, convirtiendo cada enfrentamiento en una cacería donde tú eres siempre el depredador, nunca la presa.
- **Método**: Ladrón (Thief)
- **Atributos**: Prioriza Destreza (+4), Inteligencia (+2), Carisma secundario (+1)
- **Armas**: Dagas (arrojadizas también), Espada corta
- **Dotes clave**:
  - Nivel 1: Movilidad ✓
  - Nivel 2: Adepto del Movimiento Furtivo ✓
  - Nivel 4: Golpe Hostigador ✓
  - Nivel 6: Golpe Desequilibrante ✓
  - Nivel 8: Desviar Atención ✓
- **Estilo de juego**: Entra, apuñala, desaparece. El pícaro clásico.

### Configuración 2: Matón Intimidante (Ruffian)
**Concepto**: No necesitas sigilo cuando tienes músculos y una mirada que hiela la sangre. Mientras otros pícaros se esconden en las sombras, tú caminas directamente hacia tus víctimas, y el terror en sus ojos es toda la ventaja que necesitas. Tus golpes no son sutiles puñaladas sino impactos brutales que dejan a tus enemigos tambaleándose, sangrando y rogando misericordia. Eres el matón de los callejones, el cobrador de deudas, el tipo de pícaro que no roba carteras sino que las exige con una sonrisa amenazadora.
- **Método**: Rufián (Ruffian)
- **Atributos**: Prioriza Fuerza (+4), Constitución y Destreza equilibrados (+2)
- **Armas**: Maza, Sap, o armas d8
- **Armadura**: Armadura media
- **Dotes clave**:
  - Nivel 1: Tu Eres el Siguiente ✓ (de Espadachín, vía arquetipo)
  - Nivel 2: Paliza Brutal ✓
  - Nivel 4: Golpe Hostigador ✓
  - Nivel 6: Derribo Doloroso ✓
  - Nivel 8: Desarme Taimado ✓
- **Estilo de juego**: Golpea fuerte, aterroriza, deja inconscientes. Menos sigiloso, más contundente.

### Configuración 3: Cerebro Criminal (Mastermind)
**Concepto**: Tu mente es el arma más letal del arsenal. Con una mirada evalúas a tu oponente: su postura revela su entrenamiento, sus cicatrices cuentan su historia, y cada detalle te susurra exactamente dónde golpear para causar el máximo daño. No atacas a ciegas; calculas, analizas, y cuando finalmente actúas, tu precisión quirúrgica explota cada debilidad que has identificado. Eres el estratega criminal, el pícaro que derrota a sus enemigos con información antes que con acero, aunque el acero siempre sella el trato.
- **Método**: Cerebro (Mastermind)
- **Atributos**: Prioriza Inteligencia (+4), Destreza (+3), Carisma secundario (+1)
- **Armas**: Ballesta de mano, Rapier
- **Dotes clave**:
  - Nivel 1: Analizar Debilidad ✓ (capacidad del Método Cerebro)
  - Nivel 2: Golpe Estratégico ✓
  - Nivel 4: Conocimiento Perturbador ✓ (dote de habilidad)
  - Nivel 6: Predicción Táctica ✓
  - Nivel 8: Ataque de Puntos de Presión ✓
- **Estilo de juego**: Identifica enemigos, comunica debilidades al grupo, ataca puntos vitales.

---

## Explorador (Ranger)

### Configuración 1: Explorador de Ráfaga con Compañero
**Concepto**: Tú y tu compañero animal sois una tormenta de colmillos, garras y acero. Donde otros combatientes atacan solos, vosotros descargáis una avalancha coordinada de golpes que abruma a cualquier enemigo. Tu lobo derriba mientras tú apuñalas; tu leopardo distrae mientras tú rematas. La Ventaja de Ráfaga te permite atacar una y otra vez con penalización reducida, y cuando tu compañero se une a la refriega, los enemigos enfrentan no a un oponente, sino a una manada hambrienta de victoria.
- **Ventaja del Cazador**: Ráfaga (Flurry)
- **Atributos**: Prioriza Destreza (+4), Sabiduría (+2), Constitución secundaria (+1)
- **Armas**: Dos espadas cortas o Hacha de mano + Hacha arrojadiza
- **Compañero Animal**: Lobo (Derribar) o Leopardo (Velocidad)
- **Dotes clave**:
  - Nivel 1: Compañero Animal ✓
  - Nivel 2: Derribo Gemelo ✓
  - Nivel 4: Compañero Animal Maduro ✓
  - Nivel 6: Disparo Instantáneo ✓ (antes "Ataque del Compañero Increíble" - no existe)
  - Nivel 8: Grito del Compañero ✓
- **Estilo de juego**: 4 ataques propios + 2-3 del compañero por turno. Abrumador.

### Configuración 2: Arquero de Precisión
**Concepto**: Un disparo, un enemigo menos. Has rechazado la filosofía de saturar el aire con flechas en favor de la perfección absoluta: cada proyectil que liberas está destinado a encontrar un punto vital. Tu paciencia de cazador te permite estudiar a tu presa, identificar el momento exacto, y entonces tu flecha vuela con la inevitabilidad de la muerte misma. Mientras otros arqueros vacían sus carcajs, tú derribas gigantes con disparos únicos que atraviesan armaduras como si fueran papel.
- **Ventaja del Cazador**: Precisión
- **Atributos**: Prioriza Destreza (+4), Sabiduría (+2), Fuerza secundaria (+1 para arcos compuestos)
- **Arma**: Arco largo compuesto
- **Dotes clave**:
  - Nivel 1: Puntería del Cazador ✓
  - Nivel 2: Disparo a Larga Distancia ✓
  - Nivel 4: Presa Predilecta ✓
  - Nivel 6: Disparo Instantáneo ✓
  - Nivel 8: Doble Presa ✓
- **Estilo de juego**: Menos ataques pero más daño por disparo. Ideal para ballestas también.

### Configuración 3: Explorador de Artimañas (Outwit)
**Concepto**: La caza no es solo violencia; es astucia, paciencia y conocimiento. Has estudiado a los monstruos del mundo no para temerlos, sino para superarlos. Conoces sus costumbres, sus debilidades, sus patrones de comportamiento. En tu terreno predilecto te mueves como un fantasma, y contra tu presa marcada despliegas un arsenal de trucos: te escondes donde no pueden encontrarte, los engañas con señuelos, y cuando finalmente atacas, cada golpe explota una vulnerabilidad que solo tú conocías. Eres el cazador de monstruos definitivo.
- **Ventaja del Cazador**: Artimañas (Outwit)
- **Atributos**: Prioriza Sabiduría y Destreza (+3 ambos), Carisma secundario (+2)
- **Arma**: Arco corto + Espada corta
- **Dotes clave**:
  - Nivel 1: Cazador de Monstruos ✓
  - Nivel 2: Terreno Predilecto ✓
  - Nivel 4: Presa Predilecta ✓
  - Nivel 6: Guardián contra Monstruos ✓
  - Nivel 8: Maestro del Terreno ✓
- **Estilo de juego**: El explorador definitivo. Bonificador a Sigilo, Engaño, Intimidación contra la presa.

---

## Monje

### Configuración 1: Monje de la Grulla (Tanque)
**Concepto**: Como la grulla que permanece inmóvil en el estanque, tú esperas con serenidad absoluta mientras el caos del combate ruge a tu alrededor. Tu postura elevada y elegante te convierte en un objetivo casi imposible de alcanzar: los golpes pasan silbando junto a ti mientras fluyes como agua entre los ataques. Y cuando un enemigo finalmente comete un error, tu contraataque llega con la velocidad y precisión del pico de la grulla. Eres el ojo del huracán, la calma letal en medio de la tormenta de batalla.
- **Postura**: Postura de la Grulla
- **Atributos**: Prioriza Destreza (+4), Sabiduría (+3), Constitución secundaria (+2)
- **Dotes clave**:
  - Nivel 1: Postura de la Grulla ✓
  - Nivel 2: Golpes Aturdidores ✓
  - Nivel 4: Postura Reflexiva ✓
  - Nivel 6: Aleteo de Grulla ✓
  - Nivel 8: Atrapar Proyectil ✓
- **Estilo de juego**: CA altísima, aguanta en primera línea, contraataques elegantes.
- **Nota**: Ráfaga de Golpes es capacidad de clase, no una dote.

### Configuración 2: Monje Dragón (Daño)
**Concepto**: Has canalizado la ferocidad del dragón en cada fibra de tu ser. Tu postura es ancha y poderosa, tus golpes caen como las garras de un wyrm, y de tu boca puede emerger un rugido que hace temblar los huesos de tus enemigos, o incluso un torrente de energía elemental. No buscas la elegancia ni la defensa; buscas la destrucción pura. Cada puñetazo lleva el peso de una montaña, cada patada tiene la furia de una tormenta. Eres el monje que eligió el camino del dragón: absoluta, devastadora potencia.
- **Postura**: Postura del Dragón
- **Atributos**: Prioriza Fuerza (+4), Sabiduría y Constitución secundarios (+2)
- **Dotes clave**:
  - Nivel 1: Postura del Dragón ✓
  - Nivel 2: Rugido del Dragón ✓
  - Nivel 4: Golpe de Empujón ✓
  - Nivel 6: Zarpa de Tigre Fiera ✓
  - Nivel 8: Golpe de un Centímetro ✓
- **Estilo de juego**: Alto daño cuerpo a cuerpo más daño de área ocasional.

### Configuración 3: Monje Místico de Qi
**Concepto**: Has desbloqueado los secretos del qi, la energía vital que fluye a través de todas las cosas. Tus puños no solo golpean carne; pueden conmocionar el espíritu, drenar la fuerza vital, o liberar explosiones de energía pura. Saltas distancias imposibles propulsado por tu voluntad, corres sobre el agua, y caminas sobre el aire mismo. Mientras otros monjes se limitan al reino físico, tú has trascendido esas barreras, convirtiendo cada combate en una demostración de poder sobrenatural que desafía las leyes de la naturaleza.
- **Postura**: Flexible (Postura del Lobo o Postura de la Montaña)
- **Atributos**: Prioriza Sabiduría (+4), Destreza (+3), Constitución secundaria (+2)
- **Dotes clave**:
  - Nivel 1: Hechizos de Qi ✓ (otorga Conmoción Interna u Oleada de Qi)
  - Nivel 4: Salto de Viento ✓
  - Nivel 6: Hechizos de Qi Avanzados ✓ (Explosión de Qi o Reducir la Distancia)
  - Nivel 8: Iniciado de Vientos Salvajes ✓ (Postura de Vientos Salvajes)
  - Nivel 16: Hechizos de Qi Maestros ✓ (Ira de la Medusa o Toque de Muerte)
- **Estilo de juego**: Poderes sobrenaturales, movilidad mágica, versatilidad.
- **Nota**: En el Remaster, los poderes "ki" se llaman "conjuros de qi" (Qi Spells).

---

## Mago

> **Nota Remaster**: El Mago tuvo cambios significativos en el Remaster. Las antiguas escuelas de magia (Evocación, Ilusión, Conjuración, etc.) fueron eliminadas. Ahora hay 7 escuelas arcanas basadas en disciplinas de práctica. Cada escuela proporciona un currículo de conjuros, un espacio de conjuro adicional por rango, y conjuros de foco únicos.

### Configuración 1: Mago de Batalla (Destructor)
**Concepto**: Has dedicado tu vida al estudio de la magia en su forma más devastadora. Mientras otros magos se pierden en teorías abstractas, tú has perfeccionado el arte de convertir energía arcana en destrucción pura. Bolas de fuego que incineran ejércitos, rayos que parten el cielo, ondas de fuerza que pulverizan murallas: este es tu dominio. Eres el arma definitiva del grupo de aventureros, el mago que entra a una habitación llena de enemigos y sale dejando solo cenizas humeantes.
- **Escuela**: Escuela de Magia de Batalla
- **Tesis Arcana**: Moldeo de Conjuros Experimental (más opciones de moldeo)
- **Atributos**: Prioriza Inteligencia (+4), Constitución (+2), Destreza secundaria (+1)
- **Conjuros del currículo**:
  - Trucos: Escudo, Proyectil Telecinético
  - Nivel 1: Respirar Fuego, Descarga de Fuerza, Armadura Mística
  - Nivel 3: Bola de Fuego
  - Nivel 6: Cadena de Relámpagos, Desintegrar
- **Conjuro de escuela inicial**: Rayo de Fuerza
- **Dotes clave**:
  - Nivel 1: Extender Conjuro ✓
  - Nivel 4: Conjuro de Escuela Avanzado ✓ (Absorción de Energía)
  - Nivel 6: Lanzamiento de Conjuros Firme ✓
- **Estilo de juego**: Explosiones masivas, control de multitudes con daño. Los conjuros de fuerza ignoran resistencias.

### Configuración 2: Mago Mentalista (Controlador)
**Concepto**: La mente es el campo de batalla más peligroso, y tú eres su maestro indiscutible. Con un susurro arcano puedes hacer que un guerrero ataque a sus aliados, que un rey firme su propia sentencia de muerte, o que un ejército entero huya aterrorizado de fantasmas que solo ellos pueden ver. Tus ilusiones son tan perfectas que la realidad misma parece cuestionarse, y tus encantamientos convierten a los enemigos más feroces en marionetas dóciles. El combate más limpio es aquel donde el enemigo nunca sabe que está luchando contra ti.
- **Escuela**: Escuela del Mentalismo
- **Tesis Arcana**: Mezcla de Conjuros (más espacios de alto nivel)
- **Atributos**: Prioriza Inteligencia (+4), Sabiduría (+2), Carisma secundario (+1)
- **Conjuros del currículo**:
  - Trucos: Atontar, Fantasía
  - Nivel 1: Colores Mareantes, Dormir, Golpe Seguro
  - Nivel 3: Leer la Mente
  - Nivel 5: Alucinación, Escena Ilusoria
- **Conjuro de escuela inicial**: Empujón Encantador
- **Dotes clave**:
  - Nivel 2: Familiar Potenciado ✓
  - Nivel 4: Conjuro de Escuela Avanzado ✓ (Capa de Invisibilidad)
  - Nivel 6: Ilusión Convincente ✓
- **Estilo de juego**: Controla mentes, crea ilusiones, debilita enemigos. El portavoz arcano del grupo.

### Configuración 3: Mago del Límite (Invocador/Necromante)
**Concepto**: El velo entre los planos es fino para ti, y lo cruzas con la facilidad de quien abre una puerta. Convocas horrores de otras dimensiones para que luchen por ti, arrancas espíritus del más allá para servir tus propósitos, y manipulas el tejido mismo de la realidad para teletransportarte o desterrar a tus enemigos. ¿Por qué arriesgar tu vida en combate cuando puedes enviar un ejército de servidores convocados? Eres el mago que nunca lucha solo, rodeado siempre de criaturas del vacío, fantasmas vinculados y aberraciones de pesadilla.
- **Escuela**: Escuela del Límite
- **Tesis Arcana**: Sintonización de Familiar Mejorada
- **Atributos**: Prioriza Inteligencia (+4), Constitución (+2), Sabiduría secundaria (+1)
- **Conjuros del currículo**:
  - Trucos: Mano Telecinética, Distorsión del Vacío
  - Nivel 1: Zarcillos Macabros, Esbirro Fantasmal, Convocar Muertos Vivientes
  - Nivel 4: Parpadeo, Cambiar de Sitio
  - Nivel 5: Destierro, Invocar Espíritus
- **Conjuro de escuela inicial**: Fortificar Convocación
- **Dotes clave**:
  - Nivel 2: Familiar Potenciado ✓
  - Nivel 4: Conjuro de Escuela Avanzado ✓ (Espiral de Horrores)
  - Nivel 8: Conjuro Rápido ✓
- **Estilo de juego**: Economía de acción masiva, convocaciones y magia dimensional.

---

## Hechicero (Sorcerer)

### Configuración 1: Hechicero Dracónico (Destructor)
**Concepto**: La sangre de los dragones corre por tus venas, y con cada conjuro que lanzas, ese poder ancestral despierta un poco más. Tu aliento se convierte en un torrente de fuego, hielo o relámpago; escamas brillantes brotan de tu piel en momentos de peligro; y la devastación que desatas rivalizaría con la de los grandes wyrms de la antigüedad. A diferencia de los magos que estudian para obtener poder, tú naciste con él. La magia no es una herramienta que uses; es lo que eres, y lo que eres es destrucción encarnada.
- **Linaje**: Dracónico (Plata o Blanco - frío)
- **Tradición**: Arcano
- **Atributos**: Prioriza Carisma (+4), Constitución (+2), Destreza secundaria (+1)
- **Conjuros clave**:
  - Trucos: Rayo de Escarcha
  - Nivel 3: Aliento del Dragón (Conjuro de foco)
  - Nivel 3+: Bola de Fuego, Cono de Frío
- **Dotes clave**:
  - Nivel 1: Sangre Emergente ✓
  - Nivel 1: Ampliar Conjuro ✓
  - Nivel 6: Linaje Avanzado ✓
- **Estilo de juego**: Daño masivo de área, resistencia al tipo de daño elegido, escamas de dragón.

### Configuración 2: Hechicero Angélico (Apoyo)
**Concepto**: Un ancestro celestial dejó su marca en tu linaje, y ahora la luz divina fluye a través de ti tan naturalmente como la sangre. Donde otros sanadores rezan por milagros, tú simplemente extiendes las manos y la energía vital surge en oleadas doradas. Tu presencia reconforta a los aliados heridos y hace retroceder a las criaturas de la oscuridad. Eres el ángel guardián del grupo, el portador de esperanza cuya magia teje luz y vida incluso en las situaciones más desesperadas.
- **Linaje**: Angélico
- **Tradición**: Divino
- **Atributos**: Prioriza Carisma (+4), Sabiduría y Constitución equilibrados (+2)
- **Conjuros clave**:
  - Sanación, Bendición, Restauración
  - Foco: Aureola de Sanación
- **Dotes clave**:
  - Nivel 1: Sangre Emergente ✓
  - Nivel 4: Evolución Divina ✓
  - Nivel 8: Resistencia del Linaje ✓
- **Estilo de juego**: El sanador espontáneo, mejor que el clérigo en situaciones imprevistas.

### Configuración 3: Hechicero Aberrante (Controlador)
**Concepto**: Algo antinatural se retorció en tu árbol genealógico, dejándote conectado a realidades que desafían la cordura. Tu magia no sigue las reglas del mundo normal: tentáculos emergen de portales imposibles, pensamientos alienígenas invaden las mentes de tus enemigos, y tu propio cuerpo puede distorsionarse de formas que harían vomitar a los espectadores. Eres inquietante, perturbador, y absolutamente devastador. Los enemigos que se enfrentan a ti no solo luchan contra un hechicero; luchan contra el horror mismo del vacío entre las estrellas.
- **Linaje**: Aberrante
- **Tradición**: Oculto
- **Atributos**: Prioriza Carisma (+4), Constitución (+2), Inteligencia secundaria (+1)
- **Conjuros clave**:
  - Conjuros de toque con alcance extendido
  - Control mental, confusión
  - Foco: Miembros Tentaculares
- **Dotes clave**:
  - Nivel 1: Extender Conjuro ✓
  - Nivel 4: Evolución Oculta ✓
  - Nivel 8: Explosión de Poder ✓
- **Estilo de juego**: Raro y perturbador, extiende toque a 10 pies, control mental.

---

## Clérigo

> **Nota Remaster**: En el Remaster, "energía positiva" se denomina **vitalidad** y "energía negativa" se denomina **vacío**. Las Fuentes de Sanación y Daño usan esta nueva terminología.

### Configuración 1: Clérigo de Batalla (Warpriest)
**Concepto**: Tu fe no se queda en el templo; la llevas al corazón de la batalla, envuelta en acero y bañada en sangre sagrada. Con el arma favorita de tu deidad en mano y sus oraciones en tus labios, cargas junto a los guerreros, sanando heridas con una mano mientras castigas a los impíos con la otra. Eres el sacerdote que predica con el ejemplo, el puente entre lo divino y lo marcial. Tus aliados saben que mientras estés de pie, ni morirán abandonados ni los enemigos de tu fe quedarán sin castigo.
- **Doctrina**: Sacerdote de Guerra (Warpriest)
- **Deidad**: Gorum (Espadón), Iomedae (Espada larga), o Sarenrae (Cimitarra)
- **Atributos**: Prioriza Sabiduría y Fuerza (+3 ambos), Constitución secundaria (+2)
- **Dominio**: Guerra, Celo, o Confianza
- **Dotes clave**:
  - Nivel 1: Simplicidad Mortal ✓
  - Nivel 2: Armadura del Sacerdote de Guerra ✓
  - Nivel 4: Canalizar Castigo ✓
  - Nivel 6: Arma Divina ✓
- **Estilo de juego**: Tanque que sana, combate cuerpo a cuerpo con magia de apoyo.

### Configuración 2: Clérigo Sanador (Cloistered Cleric)
**Concepto**: La vida es sagrada, y tú eres su guardián más devoto. Tu conexión con lo divino te permite canalizar oleadas de energía curativa que restauran carne desgarrada, purifican venenos y destierran enfermedades con un simple gesto. Donde otros sanadores deben elegir a quién salvar, tú inundas el campo de batalla con energía vital que alcanza a todos tus aliados simultáneamente. Eres el pilar que mantiene de pie al grupo, el milagro ambulante que convierte heridas mortales en cicatrices y derrotas seguras en victorias improbables.
- **Doctrina**: Clérigo Enclaustrado
- **Deidad**: Sarenrae, Farasma, o Shelyn
- **Atributos**: Prioriza Sabiduría (+4), Carisma y Constitución secundarios (+2)
- **Fuente**: Fuente de Sanación
- **Dotes clave**:
  - Nivel 1: Manos Curativas ✓
  - Nivel 2: Curación en Común ✓
  - Nivel 4: Canalización Dirigida ✓
  - Nivel 6: Energía Selectiva ✓
- **Estilo de juego**: Sanaciones de área gratuitas, mantiene al grupo vivo sin esfuerzo.

### Configuración 3: Clérigo de Daño (Harm Font)
**Concepto**: Mientras otros clérigos predican misericordia, tú traes el juicio final. Tu deidad te ha otorgado dominio sobre la energía del vacío, la fuerza que deshace la vida misma. Con cada canalización, ondas de oscuridad corrosiva emanan de ti, marchitando la carne de los vivos y devolviendo a los muertos vivientes al polvo del que surgieron. Eres el segador divino, el heraldo de la muerte sagrada. Los enemigos de tu fe aprenden rápidamente que no todos los clérigos vienen a sanar; algunos vienen a cobrar el precio final.
- **Doctrina**: Sacerdote de Guerra o Enclaustrado
- **Deidad**: Urgathoa, Zon-Kuthon, o Farasma
- **Atributos**: Prioriza Sabiduría (+4), Constitución (+2), Carisma secundario (+1)
- **Fuente**: Fuente de Daño
- **Dotes clave**:
  - Nivel 1: Manos Dañinas ✓
  - Nivel 2: Minar la Vida ✓
  - Nivel 4: Canalizar Castigo ✓
  - Nivel 6: Energía Selectiva ✓
- **Estilo de juego**: Daña a todos los vivos en área, excelente contra hordas.

---

## Druida

### Configuración 1: Druida Salvaje (Forma Salvaje)
**Concepto**: La línea entre druida y bestia es, para ti, una sugerencia que ignoras a voluntad. Tu alma está tan conectada con la naturaleza salvaje que tu cuerpo puede adoptar cualquiera de sus formas: el oso que aplasta, el lobo que desgarra, el dinosaurio que devasta, o incluso el dragón que incinera. En combate, abandonas la fragilidad humana para convertirte en el depredador más letal que la situación requiera. Eres la naturaleza en su forma más pura y terrible, un cambiaformas cuyo repertorio de transformaciones no conoce límites.
- **Orden**: Salvaje (Salvaje)
- **Atributos**: Prioriza Sabiduría (+4), Constitución y Fuerza secundarios (+2)
- **Dotes clave**:
  - Nivel 1: Forma Salvaje ✓
  - Nivel 6: Forma de Insecto ✓
  - Nivel 8: Forma Feroz ✓ (dinosaurios)
  - Nivel 10: Forma Elemental ✓
  - Nivel 12: Forma de Dragón ✓
  - Nivel 16: Forma de Monstruosidad ✓
- **Estilo de juego**: Cambia de forma según la situación, tanque temporal cuando se transforma.

### Configuración 2: Druida de Tormenta (Destructor)
**Concepto**: Los cielos obedecen tu llamado. Cuando alzas las manos, las nubes se congregan, los vientos rugen y los relámpagos caen sobre tus enemigos con la furia de la naturaleza desatada. Eres el heraldo de la tempestad, el druida que ha dominado el poder más espectacular y destructivo del mundo natural. Tus conjuros no son sutiles manipulaciones de la vida; son cataclismos en miniatura, tormentas personales que descargan toda su violencia sobre aquellos que osan desafiar el equilibrio natural que tú proteges.
- **Orden**: Tormenta
- **Atributos**: Prioriza Sabiduría (+4), Destreza (+2), Constitución secundaria (+1)
- **Conjuros clave**:
  - Llamar Relámpago, Control del Clima
  - Oleada de Tempestad (Conjuro de foco de la orden)
- **Dotes clave**:
  - Nivel 1: Nacido de la Tormenta ✓
  - Nivel 6: Castigo de la Tormenta ✓
  - Nivel 8: Llamador del Viento ✓
  - Nivel 10: Conjuro Atronador ✓
  - Nivel 16: Vientos Inspiradores ✓
- **Estilo de juego**: Daño de área eléctrico, control del campo con viento y lluvia.

### Configuración 3: Druida Animal (Compañero)
**Concepto**: No caminas solo por los senderos salvajes; a tu lado marcha un compañero que es más que una mascota, más que un aliado. Tu vínculo con este animal trasciende el entrenamiento ordinario: os comunicáis sin palabras, lucháis como una sola mente en dos cuerpos, y juntos sois más formidables que cualquier aventurero solitario. Mientras tú canalizas la magia de la naturaleza desde la retaguardia, tu compañero—ya sea oso, lobo, o bestia aún más exótica—desgarra a tus enemigos con una ferocidad que ningún animal doméstico podría igualar.
- **Orden**: Animal
- **Atributos**: Prioriza Sabiduría (+3), Constitución y Destreza equilibrados (+2)
- **Compañero**: Oso (tanque), Lobo (flanqueo), o Dinosaurio
- **Dotes clave**:
  - Nivel 1: Compañero Animal ✓
  - Nivel 4: Compañero Animal Maduro ✓
  - Nivel 6: Apoyo Instintivo ✓
  - Nivel 8: Compañero Sensacional ✓
  - Nivel 10: Codo con Codo ✓
  - Nivel 14: Compañero Especializado ✓
- **Estilo de juego**: Tu compañero es tan importante como tú, trabajan en equipo.

---

## Oráculo

### Configuración 1: Oráculo de las Llamas
**Concepto**: El fuego te eligió, o quizás te maldijo, porque la línea entre bendición y condena es borrosa para un oráculo. Las llamas danzan en tus ojos, el calor emana constantemente de tu piel, y cuando canalizas tu poder, te conviertes en un avatar de la conflagración divina. Cada conjuro que lanzas alimenta el ardor en tu interior, llevándote más cerca de la combustión total. Caminas por el filo entre el poder devastador y la autodestrucción, y en ese equilibrio precario encuentras una fuerza que los magos ordinarios jamás comprenderán.
- **Misterio**: Llamas
- **Atributos**: Prioriza Carisma (+4), Constitución (+2), Sabiduría secundaria (+1)
- **Maldición**: Ardor (ganas debilidad al frío pero poderes de fuego)
- **Dotes clave**:
  - Nivel 1: Hechizo Extendido ✓ o Ampliar Hechizo ✓
  - Nivel 6: Revelación Avanzada ✓
  - Nivel 8: Poder Surgente ✓
  - Nivel 10: Juicio del Fuego Celestial ✓
  - Nivel 12: Revelación Mayor ✓
- **Estilo de juego**: Destructor divino, gestiona tu maldición para maximizar daño.
- **Nota**: La "revelación del fuego" es el conjuro de foco inicial del misterio, no una dote.

### Configuración 2: Oráculo de Huesos (Necromante)
**Concepto**: La muerte susurra secretos en tu oído desde que tienes memoria. Tu misterio te conecta con el reino de los difuntos, otorgándote poder sobre los huesos, los espíritus y la energía vital misma. Esqueletos se levantan a tu orden, la fuerza de los vivos fluye hacia ti con un toque, y los muertos te obedecen como a un soberano natural. Tu maldición te acerca cada vez más al umbral de la muerte, pero en esa proximidad encuentras un dominio sobre la no-vida que los necromantes estudian toda su existencia sin alcanzar.
- **Misterio**: Huesos
- **Atributos**: Prioriza Carisma (+4), Constitución (+3), Sabiduría secundaria (+1)
- **Dotes clave**:
  - Nivel 1: Susurros de Debilidad ✓
  - Nivel 6: Revelación Avanzada ✓
  - Nivel 8: Dicotomía Debilitante ✓
  - Nivel 10: Los Muertos Caminan ✓
  - Nivel 12: Revelación Mayor ✓
- **Estilo de juego**: Necromante divino, rodéate de servidores esqueléticos.
- **Nota**: Los conjuros del misterio como "Toque de Muerte" son conjuros de foco, no dotes.

### Configuración 3: Oráculo de la Vida (Sanador)
**Concepto**: La vida fluye a través de ti como un río desbordado, tan poderoso que a veces amenaza con ahogarte. Tu conexión con la fuerza vital es tan intensa que puedes cerrar heridas mortales con un pensamiento, devolver a los moribundos del borde del abismo, y mantener a grupos enteros luchando cuando deberían haber caído hace mucho. Pero este don tiene un precio: cada vez que canalizas tu poder, el dolor de aquellos que sanas resuena en tu propia carne. Eres el mártir sanador, el que sufre para que otros vivan.
- **Misterio**: Vida
- **Atributos**: Prioriza Carisma (+4), Sabiduría y Constitución equilibrados (+2)
- **Dotes clave**:
  - Nivel 1: Advertencia Oracular ✓
  - Nivel 2: Égida Divina ✓
  - Nivel 6: Revelación Avanzada ✓
  - Nivel 8: Poder Surgente ✓
  - Nivel 12: Revelación Mayor ✓
  - Nivel 16: Conducto de Vacío y Vitalidad ✓
- **Estilo de juego**: Sanación masiva pero tu maldición te daña. Gestiona el riesgo.
- **Nota**: "Enlace Vital" es el conjuro de foco inicial del misterio Vida, no una dote.

---

## Bardo

### Configuración 1: Bardo de Inspiración (Maestro Potenciador)
**Concepto**: Tu música no es mero entretenimiento; es magia pura que eleva a los héroes a hazañas legendarias. Cuando entonas tu Himno Valeroso, los brazos cansados encuentran nueva fuerza, las espadas golpean con precisión sobrenatural, y los corazones temerosos se llenan de coraje inquebrantable. Eres el multiplicador de poder del grupo, el catalizador que transforma a buenos aventureros en leyendas vivientes. Mientras tu canto resuene, tus aliados lucharán mejor, golpearán más fuerte y resistirán más de lo que creían posible.
- **Musa**: Maestro
- **Atributos**: Prioriza Carisma (+4), Destreza (+2), Constitución secundaria (+1)
- **Composiciones clave**:
  - Himno Valeroso (+1 ataque y daño)
  - Himno de Reagrupamiento (+1 CA)
  - Endecha de Perdición (-1 a enemigos)
- **Dotes clave**:
  - Nivel 1: Composición Persistente ✓
  - Nivel 4: Himno de Reagrupamiento ✓
  - Nivel 6: Armonizar ✓
  - Nivel 6: Endecha de Perdición ✓
  - Nivel 8: Composición Fortísima ✓
- **Estilo de juego**: Mantén inspiración constantemente, el grupo entero mejora.

### Configuración 2: Bardo de Ocultismo (Debilitador)
**Concepto**: Donde otros bardos inspiran, tú desmoralizas. Tu música es un arma psicológica que se infiltra en las mentes enemigas, sembrando dudas, miedos y confusión. Tu Endecha de Perdición hace que las manos tiemblen y los golpes fallen; tus encantamientos convierten a guerreros feroces en cobardes patéticos. Has estudiado los secretos ocultos de la mente, y ese conocimiento te permite desarmar a tus enemigos antes de que levanten sus armas. Eres el saboteador arcano, el bardo cuya melodía es una maldición disfrazada de canción.
- **Musa**: Enigma
- **Atributos**: Prioriza Carisma (+4), Inteligencia (+2), Sabiduría secundaria (+1)
- **Conjuros clave**:
  - Miedo, Risas Histéricas, Sugestión
  - Endecha de Perdición
- **Dotes clave**:
  - Nivel 1: Saber Bárdico ✓
  - Nivel 2: Estudio del Maestro del Saber ✓
  - Nivel 6: Conocimiento Asegurado ✓
  - Nivel 8: Sabelotodo ✓
  - Nivel 12: Conocimiento del Enigma ✓
- **Estilo de juego**: Controla enemigos, reduce sus tiradas, Portavoz del grupo.
- **Nota**: "Canto Hipnótico" y "Control Mental" son conjuros, no dotes de bardo.

### Configuración 3: Bardo de Combate (Valor)
**Concepto**: Los bardos que se esconden detrás del grupo no entienden el verdadero significado del valor. Tú cantas desde la primera línea, con la espada en una mano y la inspiración en tus labios. Tu ejemplo no es solo musical; es marcial. Cuando cargas contra el enemigo entonando himnos de guerra, tus aliados te siguen con un fervor que ningún discurso desde la retaguardia podría igualar. Eres el bardo que las baladas celebran: el que no solo canta sobre héroes, sino que se convierte en uno de ellos.
- **Musa**: Combatiente
- **Atributos**: Prioriza Carisma y Destreza (+3 ambos), Constitución secundaria (+2)
- **Armas**: Rapier + Escudo o Arco
- **Dotes clave**:
  - Nivel 1: Interpretación Marcial ✓
  - Nivel 2: Canción de Fuerza ✓
  - Nivel 4: Avance Valeroso ✓
  - Nivel 6: Coordinación Defensiva ✓
  - Nivel 8: Valor Reflexivo ✓
  - Nivel 10: Asalto Valeroso ✓
- **Estilo de juego**: Pelea mientras cantas, inspira con el ejemplo.

---

## Alquimista

### Configuración 1: Bombardero
**Concepto**: ¿Por qué conformarse con una espada cuando puedes tener explosiones? Tu laboratorio portátil produce un arsenal interminable de bombas alquímicas: ácido que derrite armaduras, fuego líquido que se adhiere a la carne, hielo instantáneo que congela extremidades. Mientras otros aventureros se acercan a golpear, tú mantienes la distancia y conviertes el campo de batalla en un infierno de destrucción química. Eres el artillero del grupo, el científico loco cuya respuesta a cada problema es, invariablemente, más explosiones.
- **Campo de Investigación**: Bombardero
- **Atributos**: Prioriza Inteligencia (+4), Destreza (+3), Constitución secundaria (+1)
- **Objetos clave**: Bombas Alquímicas de todo tipo
- **Dotes clave**:
  - Nivel 1: Bombardero Rápido ✓
  - Nivel 2: Bomba de Humo ✓
  - Nivel 6: Bomba Debilitante ✓
  - Nivel 8: Bomba Pegajosa ✓
  - Nivel 10: Salpicadura Expandida ✓
  - Nivel 20: Mega Bomba ✓
- **Estilo de juego**: Boom, boom, boom. Daño de área constante.

### Configuración 2: Mutagenista
**Concepto**: La transformación es tu obsesión. Con un trago de tus brebajes mutagénicos, tu cuerpo se retuerce y cambia: músculos se hinchan hasta proporciones monstruosas, garras brotan de tus dedos, tu piel se endurece como cuero. Eres tu propio experimento más peligroso, un científico que usa su propio cuerpo como laboratorio. Cada combate es una oportunidad para probar los límites de la carne alterada químicamente. Eres el Dr. Jekyll que abraza a Mr. Hyde, el alquimista que se convirtió en su propia arma definitiva.
- **Campo de Investigación**: Mutagenista
- **Atributos**: Prioriza Inteligencia y Fuerza (+3 ambos), Constitución secundaria (+2)
- **Objetos clave**: Mutágeno Bestial, Mutágeno de Fuerza
- **Dotes clave**:
  - Nivel 2: Mutágeno Revivificante ✓
  - Nivel 4: Regurgitar Mutágeno ✓
  - Nivel 8: Fisiología Mutante ✓
  - Nivel 14: Inervación Mutante ✓
  - Nivel 16: Mutágeno Persistente ✓
- **Estilo de juego**: El Sr. Hyde alquímico, transformación temporal en bestia.

### Configuración 3: Quirurgo/Sanador
**Concepto**: La magia es para quienes no entienden la ciencia. Tú curas con conocimiento, no con oraciones: elixires que regeneran tejidos, antídotos que neutralizan cualquier veneno, tónicos que restauran la vitalidad perdida. Tu botiquín alquímico contiene la solución para casi cualquier aflicción, y tus manos entrenadas pueden estabilizar heridas que matarían a un hombre en segundos. Eres el médico de campo definitivo, el sanador que no necesita dioses ni magia, solo química pura y conocimiento anatómico impecable.
- **Campo de Investigación**: Quirurgo
- **Atributos**: Prioriza Inteligencia (+4), Sabiduría (+2), Destreza secundaria (+1)
- **Objetos clave**: Elixires de Vida, Antídotos
- **Dotes clave**:
  - Nivel 1: Viales Reconfortantes ✓
  - Nivel 2: Elixires Coagulantes ✓
  - Nivel 4: Bomba Curativa ✓
  - Nivel 4: Elixir Vigorizante ✓
  - Nivel 6: Elixires Fortificados ✓
  - Nivel 12: Extender Elixir ✓
- **Estilo de juego**: Sanador no-mágico, siempre tiene el objeto correcto.

---

## Taumaturgo

### Configuración 1: Taumaturgo de Espejo
**Concepto**: Los espejos son ventanas a verdades ocultas, y tú has aprendido a usarlos como armas. Tu espejo implemento refleja no solo luz sino realidad misma: duplicados ilusorios de ti confunden a tus enemigos, reflejos revelan las debilidades ocultas de los monstruos, y a veces, aquello que el espejo muestra es más real que la realidad que lo rodea. Eres el cazador de monstruos que convierte la percepción en un arma, el taumaturgo que hace que sus enemigos duden de sus propios ojos.
- **Implemento**: Espejo
- **Atributos**: Prioriza Carisma (+4), Constitución y Destreza equilibrados (+2)
- **Arma**: Espada de una mano + implemento
- **Dotes clave**: *(pendiente de documentación en el proyecto)*
- **Estilo de juego**: Crea duplicados, confunde enemigos, nunca saben cuál eres tú.

### Configuración 2: Taumaturgo de Arma
**Concepto**: Para ti, no hay separación entre el cazador y su herramienta. Tu arma no es un simple trozo de acero; es un implemento imbuido con tu voluntad y conocimiento esotérico. Cuando golpeas, no solo cortas carne; explotas debilidades sobrenaturales que has identificado con tu perspicacia de cazador. Eres el taumaturgo más directo: sin trucos elaborados ni implementos secundarios, solo tú, tu espada, y un conocimiento enciclopédico de cómo matar cada monstruo que existe.
- **Implemento**: Arma
- **Atributos**: Prioriza Carisma y Fuerza (+3 ambos), Constitución secundaria (+2)
- **Arma**: Espada bastarda o Martillo de guerra
- **Dotes clave**: *(pendiente de documentación en el proyecto)*
- **Estilo de juego**: Marcial puro con trucos de cazador de monstruos.

### Configuración 3: Taumaturgo de Libro (Conocimiento)
**Concepto**: Mientras otros cazadores aprenden de sus errores, tú aprendes de los errores de toda la historia registrada. Tu tomo implemento contiene siglos de conocimiento sobre criaturas sobrenaturales: sus orígenes, sus debilidades, sus patrones de comportamiento. Con una mirada a tu enemigo y una consulta rápida a tus páginas, sabes exactamente qué lo mata, qué lo asusta, y qué lo hace vulnerable. Eres el taumaturgo erudito, el cazador de monstruos cuya arma más poderosa es la información.
- **Implemento**: Tomo
- **Atributos**: Prioriza Carisma e Inteligencia (+3 ambos), Sabiduría secundaria (+1)
- **Arma**: Ballesta de mano + Tomo
- **Dotes clave**: *(pendiente de documentación en el proyecto)*
- **Estilo de juego**: Identifica debilidades, las explota, informa al grupo.

---

## Otras Clases

### Investigador
**Configuración 1: Detective Forense**
- **Concepto**: Donde otros ven un cadáver, tú ves una historia esperando ser descifrada. Has dedicado tu vida a dominar las ciencias de la investigación: lees escenas del crimen como libros abiertos, identificas venenos por su olor, y reconstruyes los últimos momentos de las víctimas con precisión quirúrgica. Ningún detalle escapa a tu escrutinio, ninguna pista es demasiado pequeña. Eres el detective que resuelve los casos imposibles, el investigador forense que hace hablar a los muertos a través de la evidencia que dejaron atrás.
- **Dotes clave**:
  - Nivel 1: Eliminar Pistas Falsas ✓
  - Nivel 1: Buscador de Trampas ✓
  - Nivel 4: Preparación del Detective ✓
  - Nivel 6: Investigación Exhaustiva ✓
  - Nivel 12: Hacerlos Sudar ✓

**Configuración 2: Espía Social**
- **Concepto**: En los salones de la nobleza y los callejones del submundo, tú eres quien mueve los hilos invisibles. Tu rostro cambia según la ocasión, tu voz adopta cualquier acento, y tus mentiras son tan perfectas que a veces olvidas cuál es la verdad. Extraes secretos de labios sellados, te infiltras en círculos impenetrables, y siempre sabes más de lo que aparentas. Eres el espía maestro, el agente encubierto cuya verdadera identidad es el misterio más grande de todos.
- **Dotes clave**:
  - Nivel 1: Investigador del Submundo ✓
  - Nivel 2: Persona de Interés ✓
  - Nivel 4: Detector de Mentiras ✓
  - Nivel 10: Sólo Una Cosa Más ✓
  - Nivel 18: As del Tramposo ✓

**Configuración 3: Estratega de Combate**
- **Concepto**: El combate no es caos; es un rompecabezas que puedes resolver. Mientras otros se lanzan a la batalla confiando en reflejos y fuerza bruta, tú observas, analizas, y atacas con la precisión de un cirujano. Cada enemigo tiene un patrón, una debilidad, un momento de vulnerabilidad, y tú los encuentras todos. Tus estratagemas convierten enfrentamientos imposibles en victorias calculadas. Eres el combatiente cerebral, el investigador que ha convertido el análisis táctico en un arte mortal.
- **Dotes clave**:
  - Nivel 1: Debilidades Conocidas ✓
  - Nivel 2: Estratagema Certera ✓
  - Nivel 4: Evaluación Estratégica ✓
  - Nivel 8: Estratagema Defensiva ✓
  - Nivel 14: Derivación Estratégica ✓

### Brujo (Witch)
**Configuración 1: Familiar Poderoso**
- **Concepto**: Tu familiar no es una simple mascota mágica; es tu socio, tu confidente, y a menudo la mitad más competente de tu dúo. Mientras otros brujos tratan a sus familiares como herramientas, tú has cultivado un vínculo tan profundo que tu pequeño compañero puede realizar hazañas que rivalizan con aventureros experimentados. Habla con elocuencia, espía en lugares imposibles, entrega conjuros a distancia, e incluso puede salvarte la vida cuando todo sale mal. Juntos sois más que la suma de vuestras partes.
- **Dotes clave**:
  - Nivel 2: Familiar Potenciado ✓
  - Nivel 2: Idioma del Familiar ✓
  - Nivel 8: Familiar Sensacional ✓
  - Nivel 8: Familiar Espiritual ✓
  - Nivel 8: Familiar Hilvanado ✓

**Configuración 2: Maldiciones Persistentes**
- **Concepto**: Tu especialidad no es la destrucción directa, sino la ruina gradual e inevitable. Cada maleficio que lanzas se aferra a tu víctima como una sanguijuela, drenando su fuerza, nublando su juicio, pudriendo su suerte. Tus enemigos no caen de un solo golpe; se desmoronan poco a poco bajo el peso acumulado de tus maldiciones, cada una alimentando a la siguiente. Eres el brujo que hace que la victoria del enemigo se convierta en cenizas en su boca, el tejedor de infortunios cuyas maldiciones persisten mucho después de que has abandonado el campo.
- **Dotes clave**:
  - Nivel 1: Risa Estridente ✓
  - Nivel 2: Lección Básica ✓
  - Nivel 6: Lección Mayor ✓
  - Nivel 10: Lección Superior ✓
  - Nivel 18: Dividir Maleficio ✓

**Configuración 3: Patrón de Noche**
- **Concepto**: Tu patrón mora en las sombras entre las estrellas, y te ha otorgado dominio sobre la oscuridad misma. Las tinieblas son tu aliado: te ocultan, te protegen, y golpean a tus enemigos cuando menos lo esperan. Tu magia teje velos de noche impenetrable, invoca terrores que acechan en lo negro, y hace que la luz misma huya de tu presencia. Eres el brujo de la noche eterna, el favorito de poderes que existen donde la luz no se atreve a brillar.
- **Dotes clave**:
  - Nivel 1: Caldero ✓
  - Nivel 6: Tutela de Brujo ✓
  - Nivel 12: Foco de Maleficios ✓
  - Nivel 14: Presencia del Patrón ✓
  - Nivel 20: Verdad del Patrón ✓

---

## Configuraciones para Kingmaker 2e

> **Nota de Compatibilidad**: La Senda de Aventura Kingmaker 2e es totalmente compatible con las reglas del Remaster de Pathfinder 2e. James Jacobs (director creativo de Paizo) ha confirmado que no se necesita conversión ya que el AP no tiene contenido que entre en conflicto con los cambios del Remaster.

### Sobre las Tierras Robadas

Kingmaker se desarrolla en las Tierras Robadas (Stolen Lands), una región salvaje e inexplorada en los Reinos del Río. Los personajes no solo explorarán mazmorras y derrotarán monstruos, sino que también fundará y administrará un reino. Las configuraciones siguientes están optimizadas para:
- Exploración de territorios salvajes
- Combate contra bandidos, bestias y criaturas feéricas
- Interacción con el Primer Mundo (reino de las hadas)
- Liderazgo y administración de un reino en crecimiento

### Ascendencias y Bagajes Recomendados

**Ascendencias ideales para Kingmaker:**
- **Humano**: Versátil, funciona con cualquier concepto
- **Elfo**: Conexión con los bosques de las Tierras Robadas
- **Gnomo**: Vínculos con el Primer Mundo (muy temático)
- **Mediano**: Excelentes exploradores y diplomáticos
- **Enano**: Resistentes colonos y constructores
- **Goblin**: Supervivientes adaptables del yermo
- **Leshy**: Criaturas del Primer Mundo, perfectos para Kingmaker

**Bagajes recomendados:**
- **Espadachín de Aldori** o **Desterrado Brévico**: Conexión directa con la trama
- **Peregrino**: Para clérigos y personajes devotos
- **Explorador**: Natural para las Tierras Robadas
- **Herbalista** o **Granjero**: Útil para la construcción del reino

---

### Configuración KM1: Clérigo Arquero de Erastil

**Concepto**: Erastil, el Viejo Desencadenado, es la deidad más venerada en las Tierras Robadas. Como su servidor, combinas la devoción sagrada con la maestría del arco largo, el arma favorita de tu dios. Proteges a las comunidades agrícolas, bendices las cosechas, y cazas a los monstruos que amenazan a los colonos. En la construcción de un nuevo reino, eres tanto el protector espiritual como el cazador que alimenta a su pueblo. Tu arco canta oraciones con cada flecha, y Erastil guía tus disparos contra los enemigos de la civilización.

- **Clase**: Clérigo (Sacerdote de Guerra)
- **Deidad**: Erastil
- **Doctrina**: Warpriest
- **Atributos**: Prioriza Sabiduría (+3), Destreza (+3), Constitución secundaria (+2)
- **Dominio**: Familia o Naturaleza
- **Arma**: Arco largo (arma favorita de Erastil)
- **Dotes clave**:
  - Nivel 1: Simplicidad Mortal ✓
  - Nivel 2: Armadura del Sacerdote de Guerra ✓
  - Nivel 4: Canalizar Castigo ✓
  - Arquetipo: Arquetipo de Arquero (opcional)
- **Habilidades importantes**: Supervivencia, Naturaleza, Religión
- **Rol en Kingmaker**: Líder espiritual de la comunidad, cazador de monstruos, sanador del grupo
- **Estilo de juego**: Combina sanación de área con daño a distancia. Excelente para exploración y defensa de asentamientos.

---

### Configuración KM2: Explorador de las Tierras Robadas

**Concepto**: Las Tierras Robadas son un laberinto de bosques traicioneros, pantanos mortíferos y ruinas ocultas. Nadie las conoce mejor que tú. Con tu compañero animal a tu lado—quizás un lobo de las estepas o un gran felino del bosque—rastreas bandidos, localizas recursos valiosos y mapeas territorios que ningún cartógrafo ha documentado. Eres los ojos y oídos del reino en formación, el explorador que convierte lo desconocido en conocido y lo peligroso en seguro.

- **Clase**: Explorador (Ranger)
- **Ventaja del Cazador**: Artimañas (Outwit) o Precisión
- **Atributos**: Prioriza Destreza (+4), Sabiduría (+3), Constitución secundaria (+1)
- **Compañero Animal**: Lobo (Derribar), Leopardo (Velocidad), u Oso (Tanque)
- **Arma**: Arco largo compuesto + Espada corta
- **Dotes clave**:
  - Nivel 1: Compañero Animal ✓
  - Nivel 2: Terreno Predilecto ✓ (Bosque o Pantano)
  - Nivel 4: Cazador de Monstruos ✓
  - Nivel 4: Compañero Animal Maduro ✓
  - Nivel 6: Guardián contra Monstruos ✓
- **Habilidades importantes**: Supervivencia, Naturaleza, Sigilo, Atletismo
- **Rol en Kingmaker**: Explorador principal, guía del grupo, protector de las fronteras
- **Estilo de juego**: Domina la exploración del hexágono, identifica amenazas antes de que lleguen, excelente contra bestias y bandidos.

---

### Configuración KM3: Hechicero del Linaje Feérico

**Concepto**: El Primer Mundo late cerca de las Tierras Robadas, y su magia corre por tus venas. Quizás una ninfa besó a tu ancestro, o un señor feérico dejó su marca en tu linaje. Tu magia es caprichosa, hermosa y peligrosa como las hadas mismas: encantas mentes, tejes ilusiones, y invocas criaturas del reino más allá del velo. En Kingmaker, tu conexión con el Primer Mundo te convierte en diplomático natural con las criaturas feéricas y en una fuente de magia perfectamente sintonizada con la tierra.

- **Clase**: Hechicero (Sorcerer)
- **Linaje**: Feérico (Fey) o Ninfa
- **Tradición**: Primal
- **Atributos**: Prioriza Carisma (+4), Constitución (+2), Sabiduría secundaria (+1)
- **Conjuros clave**:
  - Trucos: Producir Llama, Enredar
  - Nivel 1: Encanto, Colores Mareantes
  - Nivel 2: Invisibilidad, Calmar Emociones
  - Foco: Polvo de Hadas (Conjuro de linaje)
- **Dotes clave**:
  - Nivel 1: Sangre Emergente ✓
  - Nivel 4: Evolución Primal ✓
  - Nivel 6: Linaje Avanzado ✓
- **Habilidades importantes**: Diplomacia, Naturaleza, Engaño, Actuación
- **Rol en Kingmaker**: Diplomático con criaturas feéricas, controlador de multitudes, Portavoz del grupo
- **Estilo de juego**: Control mental e ilusiones. Perfecto para resolver encuentros sin combate y negociar con habitantes del Primer Mundo.

---

### Configuración KM4: Druida del Bosque Verde

**Concepto**: Los bosques de las Tierras Robadas son antiguos, salvajes y llenos de secretos. Tú eres su voz y su defensor. Como druida de la orden Animal o Salvaje, te mueves por la espesura como un fantasma, comunicándote con las bestias, apaciguando a los espíritus de la naturaleza, y desatando la furia del bosque contra quienes lo profanan. En la fundación de un nuevo reino, eres quien asegura que la civilización y la naturaleza coexistan en armonía, no en conflicto.

- **Clase**: Druida
- **Orden**: Animal o Salvaje
- **Atributos**: Prioriza Sabiduría (+4), Constitución (+2), Destreza secundaria (+1)
- **Compañero Animal** (si Orden Animal): Oso o Lobo
- **Conjuros clave**:
  - Enredar, Espinas, Llamar Relámpago
  - Hablar con Animales, Hablar con Plantas
  - Forma Salvaje (si Orden Salvaje)
- **Dotes clave**:
  - Nivel 1: Forma Salvaje ✓ o Compañero Animal ✓
  - Nivel 4: Compañero Animal Maduro ✓
  - Nivel 6: Forma de Insecto ✓ (si Salvaje)
  - Nivel 8: Compañero Sensacional ✓
- **Habilidades importantes**: Naturaleza, Supervivencia, Medicina, Atletismo
- **Rol en Kingmaker**: Conexión con la naturaleza salvaje, sanador del grupo, explorador de territorios vírgenes
- **Estilo de juego**: Versátil entre combate en forma animal y magia de apoyo. Esencial para interactuar con la fauna y flora de las Tierras Robadas.

---

### Configuración KM5: Guerrero Duelista Aldori

**Concepto**: Las espadas Aldori son legendarias en Brevoy, y tú has dedicado tu vida a dominar su estilo único. La elegancia letal del esgrima Aldori te convierte en un duelista sin par, capaz de enfrentarte a cualquier enemigo en combate singular y salir victorioso. En las intrigas políticas de Kingmaker, tu reputación como espadachín te abre puertas, y en combate, tu hoja danza con una gracia que deja a los bandidos y monstruos desarmados—literalmente.

- **Clase**: Guerrero (Fighter) o Espadachín (Swashbuckler)
- **Estilo** (si Espadachín): Fanfarrón o Luchador
- **Atributos**: Prioriza Destreza (+4), Constitución (+2), Carisma secundario (+1)
- **Arma**: Espada Aldori (espada de duelo)
- **Bagaje**: Espadachín de Aldori (otorga entrenamiento con la espada Aldori)
- **Dotes clave (Guerrero)**:
  - Nivel 1: Escudo Reactivo ✓
  - Nivel 2: Duelista Aldori ✓ (Arquetipo de dedicación)
  - Nivel 4: Parada Aldori ✓
  - Nivel 6: Riposte Aldori ✓
- **Dotes clave (Espadachín)**:
  - Nivel 1: Fascinación Concentrada ✓
  - Nivel 2: Duelista Aldori ✓ (Arquetipo)
  - Nivel 4: Remate Desequilibrante ✓
- **Habilidades importantes**: Atletismo, Intimidación, Diplomacia, Sociedad
- **Rol en Kingmaker**: Campeón en duelos, figura pública del reino, combatiente de élite
- **Estilo de juego**: Combate cuerpo a cuerpo elegante con énfasis en desarmar y ripostar. Muy efectivo contra enemigos humanoides.

---

### Configuración KM6: Bardo Cronista del Reino

**Concepto**: Cada reino necesita quien cuente su historia, y tú eres esa voz. Tus canciones inspiran a los colonos, tus relatos inmortalizan las hazañas de los héroes, y tu conocimiento enciclopédico de leyendas e historia te convierte en consejero invaluable. En combate, tu música eleva a tus aliados a proezas legendarias. Fuera de él, eres diplomático, espía, y la memoria viviente del reino que están construyendo.

- **Clase**: Bardo
- **Musa**: Maestro o Enigma
- **Atributos**: Prioriza Carisma (+4), Inteligencia (+2), Constitución secundaria (+1)
- **Composiciones clave**:
  - Himno Valeroso (+1 ataque y daño)
  - Himno de Reagrupamiento (+1 CA)
- **Conjuros clave**:
  - Encanto, Sugestión, Calmar Emociones
  - Leer la Mente, Enviar Mensaje
- **Dotes clave**:
  - Nivel 1: Composición Persistente ✓
  - Nivel 1: Saber Bárdico ✓
  - Nivel 4: Himno de Reagrupamiento ✓
  - Nivel 6: Armonizar ✓
  - Nivel 8: Sabelotodo ✓
- **Habilidades importantes**: Diplomacia, Actuación, Sociedad, Engaño, todos los Saberes
- **Rol en Kingmaker**: Portavoz del grupo, diplomático, consejero real, fuente de conocimiento
- **Estilo de juego**: Potencia a todo el grupo mientras resuelve encuentros sociales. Perfecto para la gestión del reino.

---

### Composición de Grupo Sugerida para Kingmaker

Un grupo equilibrado para Kingmaker debería cubrir:

1. **Exploración**: Explorador o Druida (navegación, supervivencia)
2. **Combate frontal**: Guerrero Aldori, Campeón, o Bárbaro
3. **Sanación**: Clérigo de Erastil o Druida
4. **Magia de apoyo/control**: Hechicero Feérico o Bardo
5. **Habilidades sociales**: Bardo, Espadachín Ingenioso, o cualquier personaje con alto Carisma

**Composición ejemplo de 4 jugadores:**
- Clérigo Arquero de Erastil (sanación + daño a distancia)
- Explorador con Compañero Animal (exploración + daño)
- Hechicero Feérico (control + diplomacia feérica)
- Guerrero Duelista Aldori (combate cuerpo a cuerpo + conexión con la trama)

---

## Fuentes y Referencias

- [RPGBOT - Guías de Clases Remastered](https://rpgbot.net/p2/characters/classes/)
- [Archives of Nethys - Base de Datos Oficial](https://2e.aonprd.com/)
- [Pop Culture Pathfinder - Configuraciones temáticas](https://pathfinderbuilds.com)
- [The Gamer - Guías de Configuraciones](https://www.thegamer.com)
- [Paizo Forums - Discusiones de la Comunidad](https://paizo.com/community)
- [Dexerto - Guías de Clases](https://www.dexerto.com/gaming/)
- [CBR - Mejores Configuraciones para Principiantes](https://www.cbr.com/pathfinder-2e-beginner-builds/)
- [The Whiteroom - Guía de Optimización del Taumaturgo](https://the-whiteroom.github.io/thaumaturge-optimisation-guide)

---

## Notas sobre el Remaster

El **Pathfinder 2e Remaster** (Player Core 1 y 2) introdujo cambios significativos:

1. **Alineamiento eliminado**: Ahora se usa Santificado/Profano y Edictos/Anatemas
2. **Causas del Campeón**: Los términos Paladín, Redentor, etc. son genéricos
3. **Escuelas del Mago**: Completamente reorganizadas - ya no existen Evocación, Ilusión, Conjuración, etc. Ahora hay 7 escuelas basadas en disciplinas de práctica (Magia de Batalla, Mentalismo, Límite, etc.)
4. **Tradiciones mágicas**: Se mantienen Arcana, Divina, Oculta y Primal
5. **Terminología de energía**: "Energía positiva" ahora es **vitalidad** y "energía negativa" ahora es **vacío**
6. **Poderes Ki del Monje**: Ahora se llaman "conjuros de qi"
7. **Clases en PC2**: Espadachín, Investigador, Oráculo, Brujo, Taumaturgo (las demás están en PC1)

Las configuraciones de este documento están diseñadas para funcionar con el contenido Remastered.

---

## Leyenda de Verificación de Dotes

- ✓ = Dote verificada (existe en la documentación)
- ✗ = Dote que NO existe o tiene nombre incorrecto
- Sin marca = Pendiente de verificación

**Clases verificadas:** Bárbaro, Campeón, Guerrero, Espadachín, Pícaro, Explorador, Monje, Mago, Hechicero, Clérigo, Druida, Oráculo, Bardo, Alquimista, Brujo, Investigador

**Clases sin dotes documentadas (PC2):** Taumaturgo - Esta clase es de Player Core 2 y aún no tiene sus dotes en la documentación del proyecto
