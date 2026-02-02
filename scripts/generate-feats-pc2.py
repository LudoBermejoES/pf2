#!/usr/bin/env python3
"""
Genera archivos individuales de dotes de PC2 basándose en el contenido del PDF traducido.
Las dotes se organizan en:
- docs/_dotes/generales/ (dotes generales no de habilidad)
- docs/_dotes/habilidad/ (dotes de habilidad)
"""

import os
import re
from pathlib import Path

def slugify(text):
    """Convierte texto a slug para URLs"""
    text = text.lower()
    text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    text = text.replace('ñ', 'n').replace('ü', 'u')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def create_general_feat(name, level, prerequisites, description, traits):
    """Crea el contenido de una dote general"""
    slug = slugify(name)
    prereq_line = f"**Prerrequisitos:** {prerequisites}\n\n" if prerequisites and prerequisites != "—" else ""

    traits_html = ''.join([f'<span class="feat-trait">{t.upper()}</span>' for t in traits])

    content = f"""---
layout: page
permalink: /dotes/generales/{slug}/
title: {name}
chapter: Dotes
category: dotes
level: {level}
source: PC2
---

<div class="feat-traits-header" markdown="0">{traits_html}</div>

**Dote {level}**

{prereq_line}{description}

---
"""
    return slug, content

def create_skill_feat(name, level, prerequisites, description, traits, skill=None):
    """Crea el contenido de una dote de habilidad"""
    slug = slugify(name)
    prereq_line = f"**Prerrequisitos:** {prerequisites}\n\n" if prerequisites else ""

    traits_html = ''.join([f'<span class="feat-trait">{t.upper()}</span>' for t in traits])

    habilidad_line = f"habilidad: {skill}\n" if skill else ""

    content = f"""---
layout: page
permalink: /dotes/habilidad/{slug}/
title: {name}
chapter: Dotes
category: dotes
{habilidad_line}level: {level}
source: PC2
---

<div class="feat-traits-header" markdown="0">{traits_html}</div>

**Dote {level}**

{prereq_line}{description}

---
"""
    return slug, content

def generate_feats():
    """Genera todos los archivos de dotes PC2"""
    docs_root = Path("/Users/ludo/code/pf2/docs/_dotes")
    generales_dir = docs_root / "generales"
    habilidad_dir = docs_root / "habilidad"

    # Asegurarse de que existen los directorios
    generales_dir.mkdir(parents=True, exist_ok=True)
    habilidad_dir.mkdir(parents=True, exist_ok=True)

    files_created = 0

    # ============================================
    # DOTES GENERALES (NO DE HABILIDAD) - PC2
    # ============================================

    general_feats = [
        {
            "name": "Reparación improvisada",
            "level": 3,
            "prerequisites": "—",
            "traits": ["General"],
            "description": """Puedes parchear apresuradamente equipo dañado, pero la reparación temporal carece del cuidado completo requerido para reparaciones duraderas. Parcheas un objeto roto poseído por ti o una criatura adyacente voluntaria. Hasta que el objeto reciba daño de nuevo, sigue funcionando como un objeto defectuoso de su tipo. Si es un objeto mágico u otro objeto con activaciones, no puede activarse mientras está parcheado, pero puede usarse para funciones normales (como Golpear con un arma o usar Bloqueo con escudo con un escudo). Esta actividad no restaura Puntos de Golpe, así que el objeto es fácil de destruir. Una vez que el objeto es Reparado normalmente de forma que ya no esté roto, tampoco está ya defectuoso."""
        },
        {
            "name": "Seguidor entusiasta",
            "level": 3,
            "prerequisites": "—",
            "traits": ["General"],
            "description": """Tu aguda observación de tus aliados te ha hecho mejor siguiendo su ejemplo. Cuando usas la actividad Seguir al experto en modo exploración, obtienes un bonificador circunstancial +3 si el aliado que estás siguiendo es experto y un bonificador circunstancial +4 si tu aliado es maestro.

Puedes compartir tus observaciones con otros para ayudar a coordinar mejor al grupo. Si el aliado que estás siguiendo tiene Aliados silenciosos u otra dote de habilidad que permite al grupo tirar una sola prueba de habilidad para una actividad de exploración y usar el modificador más bajo, pueden usar tu modificador en su lugar, incluso si no es el más bajo."""
        },
        {
            "name": "Acelerar el paso",
            "level": 3,
            "prerequisites": "Constitución +2",
            "traits": ["General"],
            "description": """Lideras con el ejemplo y puedes ayudar a otros a empujarse más allá de sus límites normales. Cuando te Apresuras en grupo durante el modo exploración, tu grupo puede Apresurarse durante tanto tiempo como el miembro que podría Apresurarse más tiempo por sí solo."""
        },
        {
            "name": "Salud robusta",
            "level": 3,
            "prerequisites": "—",
            "traits": ["General"],
            "description": """Tu fisiología responde bien a los primeros auxilios. Obtienes un bonificador circunstancial al número de Puntos de Golpe que recuperas igual a tu nivel de un intento exitoso de Tratar tus heridas o usar Medicina de batalla en ti. Después de que tú o un aliado use Medicina de batalla en ti, quedas temporalmente inmune a esa Medicina de batalla durante solo 1 hora, en lugar de 1 día."""
        },
        {
            "name": "Búsqueda exhaustiva",
            "level": 3,
            "prerequisites": "Experto en Percepción",
            "traits": ["General"],
            "description": """Te tomas tu tiempo buscando para asegurarte de encontrar todo. Cuando Buscas, puedes tardar el doble de tiempo. Normalmente esto significa que Buscas a hasta un cuarto de tu Velocidad, hasta un máximo de 45 metros por minuto para revisar todo, o 22 metros por minuto para revisar todo antes de caminar hacia un área. Si lo haces y el DJ tira tu prueba secreta para Buscar para notar algo, obtienes un bonificador circunstancial +2 a esa prueba de Percepción y si tienes éxito, obtienes un éxito crítico en su lugar."""
        },
        {
            "name": "Insensible a la muerte",
            "level": 7,
            "prerequisites": "Tenaz, haber muerto al menos una vez",
            "traits": ["General"],
            "description": """Tu pasado te ha dejado insensible a la llamada de la muerte. La primera vez cada día que recuperas Puntos de Golpe mientras estás muriendo, obtienes un bonificador circunstancial al número de Puntos de Golpe que recuperas igual a tu nivel, y no obtienes la condición herido ni aumentas el valor de esta condición."""
        },
        {
            "name": "Supercatador",
            "level": 7,
            "prerequisites": "Maestro en Percepción",
            "traits": ["General"],
            "description": """Has refinado tu paladar y tienes un sentido del gusto exigente que puede detectar anormalidades en el sabor y textura de comida y bebidas. Cuando comes comida o bebes una bebida, intentas automáticamente identificar los ingredientes, lo que podría alertarte de la presencia de alteraciones o aditivos, como venenos. El DJ tira una prueba secreta de Percepción contra una CD determinada por el nivel del veneno; si la comida o bebida está envenenada, con un éxito, aprendes que la comida o bebida fue envenenada, pero no el veneno específico usado. Si detectas con éxito que la comida o bebida fue envenenada, puedes escupir la comida o bebida a tiempo para no estar expuesto a esa instancia del veneno (a menos que reanudes comiendo o bebiendo la comida o bebida envenenada).

Si lames o pruebas algo mientras Investigas o intentas Recordar conocimiento para identificar algo, y si el sabor proporcionaría información adicional relevante (a discreción del DJ), obtienes un bonificador circunstancial +2 a tu prueba."""
        },
        {
            "name": "Un hogar en cada puerto",
            "level": 11,
            "prerequisites": "Carisma +3",
            "traits": ["Entre descansos", "General"],
            "description": """Tienes reputación en pueblos y aldeas que has visitado, y los residentes siempre están dispuestos a abrirte sus puertas. Cuando estés en un pueblo o aldea, durante el tiempo de inactividad, puedes pasar 8 horas para localizar a un residente dispuesto a proporcionar alojamiento para ti y hasta seis aliados durante hasta 24 horas sin cargo. El nivel de vida dentro del alojamiento adquirido es cómodo, y las comidas se proporcionan sin coste. Después de 24 horas, debes pagar los precios estándar por alojamiento y comidas adicionales o usar esta dote de nuevo para encontrar un nuevo residente dispuesto a hospedarte."""
        },
        {
            "name": "Líder de caravana",
            "level": 11,
            "prerequisites": "Acelerar el paso",
            "traits": ["General"],
            "description": """Sabes cómo sacar el máximo esfuerzo de tus aliados en el camino. Tu grupo puede Apresurarse durante 20 minutos adicionales más allá del tiempo que el miembro que podría Apresurarse más tiempo por sí solo."""
        },
        {
            "name": "Explorador increíble",
            "level": 11,
            "prerequisites": "Maestro en Percepción",
            "traits": ["Exploración", "General"],
            "description": """Cuando exploras, estás particularmente alerta al peligro, otorgando a tus aliados momentos preciosos para prepararse para luchar. Cuando usas la actividad de exploración Explorar, otorgas a tus aliados un bonificador circunstancial +2 a sus tiradas de iniciativa en lugar de un bonificador circunstancial +1."""
        },
        {
            "name": "Percepción verdadera",
            "level": 19,
            "prerequisites": "Legendario en Percepción",
            "traits": ["General", "Revelación"],
            "description": """Tus habilidades perceptivas y capacidad para procesar información sensorial están tan más allá de lo normal que notas discrepancias diminutas en todo tipo de ilusiones y transformaciones físicas. Estás constantemente bajo los efectos de un conjuro de visión verdadera de rango 6, usando tu modificador de Percepción para la prueba de contrarrestar."""
        },
    ]

    # ============================================
    # DOTES DE HABILIDAD - PC2
    # ============================================

    skill_feats = [
        # Variables (múltiples habilidades)
        {
            "name": "Asistencia con armadura",
            "level": 1,
            "prerequisites": "entrenado en Atletismo o Saber bélico",
            "traits": ["General", "Habilidad"],
            "skill": "Variable",
            "description": """Tienes práctica ayudándote a ti mismo y a otros a ponerse equipo pesado. Puedes intentar una prueba de Atletismo o Saber bélico con una CD determinada por el DJ (normalmente CD 15 para armadura común, CD 20 para armadura poco común y CD 25 para armadura rara) para reducir a la mitad el tiempo que tardas en ponerte la armadura. Puedes reducir a la mitad el tiempo de un aliado para ponerse la armadura trabajando con él y teniendo éxito en una prueba de Atletismo o Saber bélico contra la misma CD."""
        },
        {
            "name": "Identificación segura",
            "level": 2,
            "prerequisites": "experto en Arcanos, Naturaleza, Ocultismo o Religión",
            "traits": ["General", "Habilidad"],
            "skill": "Variable",
            "description": """Rara vez identificas incorrectamente un objeto. Cuando usas pruebas de Arcanos, Naturaleza, Ocultismo o Religión para Identificar magia, si sacas un fallo crítico, obtienes un fallo en su lugar. Si identificarías incorrectamente un objeto maldito porque sacaste un éxito pero no un éxito crítico, simplemente no puedes identificarlo en su lugar."""
        },
        {
            "name": "Investigación discreta",
            "level": 2,
            "prerequisites": "experto en Engaño o Diplomacia",
            "traits": ["General", "Habilidad"],
            "skill": "Variable",
            "description": """Eres sutil en tus esfuerzos por aprender las cosas que necesitas saber. Cuando Reúnes información, puedes ocultar el verdadero tema de tu indagación entre otros temas de poco interés para ti sin aumentar la dificultad de la prueba ni tardar más tiempo en Reunir información. Cualquiera que intente Reunir información para determinar si alguien más estaba preguntando sobre el tema en cuestión debe superar tu CD de Engaño o la CD normal para Reunir información sobre tus indagaciones, la que sea más alta, o de lo contrario no se enteran de tus esfuerzos."""
        },
        {
            "name": "Ojos de la ciudad",
            "level": 2,
            "prerequisites": "entrenado en Diplomacia o Sociedad",
            "traits": ["General", "Habilidad"],
            "skill": "Variable",
            "description": """Puedes rastrear objetivos con la ayuda de los locales. Puedes usar Diplomacia o Sociedad, en la que estés entrenado, para Rastrear criaturas en asentamientos. Charlas con los locales para ayudar a seguir el rastro de las criaturas que Rastreas. A discreción del DJ, puede que no haya suficiente gente con quien hablar para seguir el rastro."""
        },
        {
            "name": "Presa escurridiza",
            "level": 2,
            "prerequisites": "entrenado en Acrobacias o Atletismo",
            "traits": ["General", "Habilidad"],
            "skill": "Variable",
            "description": """Puedes escapar de ataduras más fácilmente que otros. Cuando intentas Escapar usando Acrobacias o Atletismo, reduces la penalización por ataques múltiples para intentos repetidos a -4 y -8 si estás entrenado en la habilidad. La penalización se convierte en -3 y -6 si eres maestro en la habilidad apropiada. Si eres legendario en la habilidad, no recibes penalizaciones por múltiples intentos de Escapar en el mismo turno. Independientemente de tu entrenamiento, tus intentos de Escapar todavía tienen el rasgo ataque e incurren en penalización por ataques múltiples con otras acciones."""
        },
        {
            "name": "Consultar a los espíritus",
            "level": 7,
            "prerequisites": "maestro en Naturaleza, Ocultismo o Religión",
            "traits": ["General", "Secreto", "Habilidad"],
            "skill": "Variable",
            "description": """Has aprendido ritos o meditaciones que te permiten percibir espíritus menores e invisibles dentro de un lugar. Elige Naturaleza, Ocultismo o Religión cuando selecciones esta dote. Naturaleza te permite contactar a los espíritus de la naturaleza que forman leshys, que nacen de esencia vital pura en lugar de energía espiritual y pueden responder preguntas sobre características naturales como la ubicación de agua cercana o vida vegetal. Religión revela la presencia de espíritus angélicos, demoníacos u otros al servicio de seres divinos, que proporcionan información sobre fuentes de energía vital poderosa o energía del Vacío; influencias sagradas o profanas; o la presencia de no-muertos. Ocultismo te permite contactar espíritus persistentes, ecos psíquicos de los muertos, y espíritus de más allá de la realidad, que te hablan sobre cosas como auras extrañas, efectos, o la presencia de seres ocultos antinaturales.

Pasa 10 minutos e intenta una prueba para Recordar conocimiento con la habilidad elegida; la CD la determina el DJ (normalmente una CD muy alta para el nivel de la criatura de nivel más alto que podrías encontrar en el área). Si eres legendario en la habilidad elegida, puedes usar esta dote una vez por hora, en lugar de solo una vez al día, pero no puedes usarla de nuevo en ningún área que se superponga con un área anterior.

**Éxito crítico** Los espíritus se revelan ante ti y tienen una actitud servicial hacia ti. Solo tú puedes percibir estos espíritus. Responden a tres preguntas simples sobre el entorno dentro de 30 metros de ti, dependiendo de la habilidad que elegiste y por tanto el tipo de espíritus que contactas. Sus respuestas son casi siempre una sola palabra, y su conocimiento está limitado a su área de interés.

**Éxito** Como con un éxito crítico, pero los espíritus son indiferentes hacia ti y responden solo una pregunta.

**Fallo** No puedes contactar a los espíritus de este lugar.

**Fallo crítico** Contactas a uno o más espíritus malevolentes. Son hostiles hacia ti, aunque puede que no parezcan serlo inmediatamente. Responden hasta tres preguntas pero te dan información que es perjudicial para ti de alguna manera, según determine el DJ.

**Especial** Puedes seleccionar esta dote múltiples veces, eligiendo cada vez una habilidad diferente en la que tengas rango de competencia maestro. Puedes usar esta dote con cada habilidad una vez al día (o una vez por hora, si eres legendario)."""
        },
        {
            "name": "Robo rodante",
            "level": 7,
            "prerequisites": "experto en Acrobacias y Latrocinio",
            "traits": ["General", "Habilidad"],
            "skill": "Acrobacias",
            "description": """Alcanzas un objeto de un oponente mientras pasas junto a un enemigo. Si tienes éxito crítico en tu prueba para Rodar a través del espacio de un enemigo, puedes intentar Robar algo del enemigo como reacción. Obtienes un bonificador circunstancial +1 a tu prueba de Latrocinio para Robar ya que tu volteo hace difícil que tu enemigo siga tu movimiento. Puedes Robar cualquier objeto inmediatamente accesible de Volumen ligero o despreciable en la persona del enemigo, como una poción o bolsa de monedas colgando de un cinturón, pero no nada dentro de un contenedor ni nada que el enemigo esté sosteniendo. El DJ tiene la última palabra sobre lo que puedes Robar."""
        },

        # Acrobacias
        {
            "name": "Intérprete acrobático",
            "level": 1,
            "prerequisites": "entrenado en Acrobacias",
            "traits": ["General", "Habilidad"],
            "skill": "Acrobacias",
            "description": """Eres un acróbata increíble, evocando asombro y cautivando audiencias con tu destreza. Puedes tirar una prueba de Acrobacias en lugar de una de Interpretación cuando usas la acción Interpretar. Si estás entrenado tanto en Acrobacias como en Interpretación, obtienes un bonificador circunstancial +1 a las pruebas de Acrobacias hechas para Interpretar."""
        },
        {
            "name": "Aterrizaje rodante",
            "level": 2,
            "prerequisites": "Caída felina",
            "traits": ["General", "Habilidad"],
            "skill": "Acrobacias",
            "description": """Aterrizas con giros rápidos que te ayudan a mantener tu impulso. Si caes y no recibes daño (normalmente debido a tratar la caída como una distancia más corta), puedes usar tu reacción para entrar inmediatamente en un giro corto cuando aterrizas y Dar un paso. Si eres experto en Acrobacias, puedes usar tu reacción para Dar un paso o Avanzar hasta la mitad de tu Velocidad después de caer sin recibir daño. Si eres maestro en Acrobacias, puedes usar esta reacción para Dar un paso o Avanzar hasta tu Velocidad completa. Si eres legendario en Acrobacias, no provocas reacciones desencadenadas por movimiento cuando Avanzas de esta manera."""
        },
        {
            "name": "Trabajo en equipo rodante",
            "level": 2,
            "prerequisites": "experto en Acrobacias",
            "traits": ["General", "Habilidad"],
            "skill": "Acrobacias",
            "description": """Tu volteo distrae a un enemigo lo suficiente como para crear una ventaja para uno de tus aliados. Cuando Ruedas a través del espacio de un enemigo con éxito, un aliado que esté adyacente a ese enemigo puede Dar un paso como reacción, pero debe permanecer adyacente a ese enemigo."""
        },
        {
            "name": "Maestría en acrobacias aéreas",
            "level": 7,
            "prerequisites": "maestro en Acrobacias",
            "traits": ["General", "Habilidad"],
            "skill": "Acrobacias",
            "description": """Te mueves con gracia en vuelo y puedes realizar acrobacias aéreas asombrosas. Obtienes un bonificador circunstancial +2 a las pruebas de Acrobacias para Maniobrar en vuelo y puedes combinar dos maniobras en una sola acción, como invertir la dirección mientras haces un ascenso o descenso pronunciado o flotar en vientos huracanados. La CD de la prueba de Acrobacias es igual a la CD de la maniobra más difícil +5. Si eres legendario en Acrobacias, puedes combinar tres maniobras en una sola acción; la CD de la prueba de Acrobacias es igual a la CD de la maniobra más difícil +10. Independientemente de la combinación, estas maniobras rara vez te permiten moverte más allá de tu Velocidad de vuelo."""
        },

        # Atletismo
        {
            "name": "Escalador líder",
            "level": 2,
            "prerequisites": "experto en Atletismo",
            "traits": ["General", "Habilidad"],
            "skill": "Atletismo",
            "description": """Cuando escalas, puedes preparar rutas para que otros las sigan, y puedes tirar de tus aliados para evitar el desastre. Cuando tus aliados intentan Escalar una ruta que estableciste usando la actividad de exploración Seguir al experto, si alguno de ellos falla críticamente sus pruebas para Escalar, puedes intentar una prueba de Atletismo contra la misma CD. Si tienes éxito, tu aliado solo falla en lugar de fallar críticamente. Si también fallas críticamente, ambos experimentáis las consecuencias del fallo crítico."""
        },
        {
            "name": "Esprint acuático",
            "level": 7,
            "prerequisites": "maestro en Atletismo",
            "traits": ["General", "Habilidad"],
            "skill": "Atletismo",
            "description": """La experiencia y el entrenamiento te han enseñado que el agua tiene justo la suficiente tensión superficial para que un esprínter maestro atraviese la superficie. Cuando Avanzas en línea recta, si te mueves al menos la mitad de tu Velocidad sobre suelo, puedes mover cualquier cantidad de la distancia restante a través de la superficie de un cuerpo de agua nivelado. Si no terminas tu Avance sobre suelo sólido, caes al agua.

Si eres legendario en Atletismo, mientras empieces sobre suelo sólido, cualquier parte de tu Avance puede cruzar la superficie del agua, incluso si no te mueves en línea recta, aunque sigues cayendo al agua si no terminas tu movimiento sobre suelo sólido."""
        },

        # Artesanía
        {
            "name": "Tasación de artesano",
            "level": 1,
            "prerequisites": "entrenado en Artesanía",
            "traits": ["General", "Habilidad"],
            "skill": "Artesanía",
            "description": """Tu conocimiento de la construcción de objetos te permite discernir también sus efectos mágicos. Puedes usar Artesanía en lugar de una habilidad asociada con una tradición mágica para Identificar magia en objetos mágicos, aunque no en ningún otro tipo de magia."""
        },
        {
            "name": "Improvisar herramienta",
            "level": 1,
            "prerequisites": "entrenado en Artesanía",
            "traits": ["General", "Habilidad"],
            "skill": "Artesanía",
            "description": """Puedes improvisar soluciones cuando no tienes las herramientas adecuadas a mano. Puedes intentar Reparar objetos dañados sin un kit de reparación.

Si tienes las materias primas, puedes Fabricar un set básico de abrojos, vela, brújula, palanca, equipo de pesca, pedernal y acero, martillo, escalera, pitón, cuerda, pértiga de 3 metros, ganzúas de repuesto, herramienta larga o corta, o antorcha como si tuvieras sus fórmulas."""
        },
        {
            "name": "Fabricación de lazos",
            "level": 1,
            "prerequisites": "entrenado en Artesanía",
            "traits": ["General", "Habilidad"],
            "skill": "Artesanía",
            "description": """Puedes usar la actividad Fabricar para crear lazos. Cuando seleccionas esta dote, inmediatamente añades las fórmulas de cuatro lazos comunes de nivel 1 a tu libro de fórmulas."""
        },
        {
            "name": "Fijación rápida",
            "level": 7,
            "prerequisites": "maestro en Artesanía",
            "traits": ["General", "Habilidad"],
            "skill": "Artesanía",
            "description": """Solo tardas 1 minuto en Fijar un talismán. Si eres legendario en Artesanía, puedes Fijar un talismán como una actividad de 3 acciones."""
        },
        {
            "name": "Artesanía distintiva",
            "level": 7,
            "prerequisites": "maestro en Artesanía, Artesanía mágica",
            "traits": ["Poco común", "General", "Habilidad"],
            "skill": "Artesanía",
            "description": """Los objetos mágicos que creas llevan una marca específica de tu trabajo. Cuando Fabricas con éxito un objeto mágico permanente, tira una prueba plana CD 9 cuando el objeto esté completamente terminado. Cualquier beneficio que una criatura obtenga de una peculiaridad de objeto se aplica solo mientras la criatura lleve el objeto (para un objeto llevado) o lo sostenga (para un objeto sostenido). El DJ podría permitir peculiaridades personalizadas similares a las listadas.

**Éxito crítico** Elige una peculiaridad de objeto de la tabla y sus detalles.

**Éxito** El objeto obtiene una peculiaridad de objeto aleatoria con cualquier detalle seleccionado por el DJ."""
        },

        # Engaño
        {
            "name": "Disfraz de respaldo",
            "level": 2,
            "prerequisites": "experto en Engaño",
            "traits": ["General", "Habilidad"],
            "skill": "Engaño",
            "description": """Tienes un disfraz específico que mantienes listo, llevándolo debajo de tu ropa exterior. Puedes cambiarte a este disfraz para Hacerte pasar por otro como una actividad de 3 acciones. Si eres maestro en Engaño, es una actividad de 2 acciones, y si eres legendario en Engaño, es una sola acción. Puedes crear un nuevo disfraz de respaldo gastando la cantidad normal de tiempo que te llevaría Hacerte pasar por otro, pero solo puedes tener un disfraz de respaldo a la vez. Tener un disfraz de respaldo no te permite quitarte la armadura u otra pieza de ropa compleja más rápido, pero una vez que te lo has quitado, el disfraz está disponible. Debido a que tienes el disfraz de respaldo listo, es posible que una búsqueda exhaustiva pueda revelar algunos elementos del disfraz (ver Ocultar un objeto en la habilidad Sigilo)."""
        },
        {
            "name": "Sembrar rumor",
            "level": 2,
            "prerequisites": "experto en Engaño",
            "traits": ["Poco común", "General", "Secreto", "Habilidad"],
            "skill": "Engaño",
            "description": """Difundes rumores, que pueden o no ser verdad, sobre un tema específico. Si el tema de tu rumor no es actualmente el tema de ningún rumor contradictorio, esto toma tanto tiempo como normalmente te tomaría Reunir información (típicamente 2 horas), al final de lo cual el DJ tira una prueba secreta de Engaño contra una CD que establece para ver qué tan bien difundes el rumor.

**Éxito crítico** Tu rumor se difunde como la pólvora. Cualquiera que tenga éxito en una prueba para Reunir información sobre el tema específico aprende tu rumor en preferencia a otros rumores sobre el tema. Tu rumor persiste durante 1 mes. Obtienes un bonificador circunstancial +2 a las pruebas de Engaño, Diplomacia e Intimidación en una situación apropiada cuando invocas tu rumor.

**Éxito** Difundes el rumor con éxito. Cualquiera que tenga éxito en una prueba para Reunir información sobre el tema específico añade tu rumor a la lista de rumores que podrían aprender sobre el tema. Tu rumor persiste durante 1 semana. Obtienes un bonificador circunstancial +1 a las pruebas de Engaño, Diplomacia e Intimidación en una situación apropiada cuando invocas tu rumor.

**Fallo** Tu rumor muere, sin volverse lo suficientemente popular para que otras personas lo aprendan mediante Reunir información.

**Fallo crítico** No puedes difundir un rumor y recibes una penalización circunstancial -4 a las pruebas de Engaño para Sembrar rumores sobre el mismo tema dentro de la misma región durante 1 semana. Además, se difunde un rumor sobre alguien intentando difundir rumores falsos sobre el tema."""
        },
        {
            "name": "Doble sentido",
            "level": 7,
            "prerequisites": "maestro en Engaño",
            "traits": ["General", "Habilidad"],
            "skill": "Engaño",
            "description": """Eres hábil diciendo una cosa y significando algo diferente. Disfrazas tu verdadero significado detrás de otras palabras y frases, confiando en énfasis sutiles y experiencias compartidas para transmitir significados que solo tus aliados entienden. Cualquier aliado que haya viajado a tu lado durante al menos 1 semana completa discierne automáticamente tu significado. Otros observadores deben tener éxito en una prueba de Percepción contra tu CD de Engaño para darse cuenta de que estás pasando un mensaje secreto, y deben obtener un éxito crítico para entender el mensaje en sí."""
        },

        # Diplomacia
        {
            "name": "Agudeza verbal",
            "level": 1,
            "prerequisites": "entrenado en Diplomacia",
            "traits": ["Auditivo", "Concentrar", "Emoción", "General", "Lingüístico", "Mental", "Habilidad"],
            "skill": "Diplomacia",
            "description": """Lanzas una réplica perspicaz a un enemigo, distrayéndolo. Elige un enemigo dentro de 9 metros y tira una prueba de Diplomacia contra la CD de Voluntad del objetivo.

**Éxito crítico** El objetivo está distraído y recibe una penalización de estado -3 a Percepción y salvaciones de Voluntad durante 1 minuto. El objetivo puede terminar el efecto antes con una réplica a tu Agudeza verbal. Esto puede ser una acción simple que tenga el rasgo concentrar o una acción de habilidad apropiada para enmarcar su réplica. El DJ determina qué acciones de habilidad califican, aunque deben tomar al menos 1 acción. Típicamente, la réplica necesita usar una acción de habilidad lingüística basada en Carisma.

**Éxito** Como éxito crítico, pero la penalización es -2.

**Fallo crítico** Tu réplica es atroz. Recibes la misma penalización que un enemigo habría recibido si hubieras tenido éxito. Esto termina después de 1 minuto o si lanzas otra Agudeza verbal y tienes éxito."""
        },
        {
            "name": "Evangelizar",
            "level": 7,
            "prerequisites": "maestro en Diplomacia, seguidor de una religión o filosofía específica",
            "traits": ["General", "Habilidad"],
            "skill": "Diplomacia",
            "description": """Señalas un detalle que apoya incontrovertiblemente tu fe, haciendo que la mente de un oyente dé vueltas. Intenta una prueba de Diplomacia y compara el resultado con la CD de Voluntad de un único objetivo que pueda oírte y entienda tu idioma; ese objetivo es entonces temporalmente inmune a Evangelizar con respecto a tu deidad o filosofía durante 1 día. Una criatura que ya está de acuerdo contigo no se ve afectada, y a discreción del DJ, un objetivo que genuinamente cambia su perspectiva para apoyar tu fe como resultado del argumento tampoco se ve afectado.

**Éxito crítico** El objetivo queda estupefacto 2 durante 1 asalto.

**Éxito** El objetivo queda estupefacto 1 durante 1 asalto.

**Fallo** El objetivo no se ve afectado."""
        },

        # Intimidación
        {
            "name": "Resistencia aterradora",
            "level": 2,
            "prerequisites": "experto en Intimidación",
            "traits": ["General", "Habilidad"],
            "skill": "Intimidación",
            "description": """Los conjuros de aquellos a quienes has Desmoralizado son menos efectivos en ti. Si tienes éxito en Desmoralizar a una criatura, durante las próximas 24 horas obtienes un bonificador circunstancial +1 a las salvaciones contra los conjuros de esa criatura."""
        },

        # Saber
        {
            "name": "Planificador de batalla",
            "level": 2,
            "prerequisites": "experto en Saber bélico",
            "traits": ["General", "Habilidad"],
            "skill": "Saber bélico",
            "description": """Estás constantemente elaborando planes y escenarios de batalla, reuniendo estrategias e inteligencia recopilada para uso posterior. Cuando exploras la posición de un enemigo o recibes un informe detallado de un aliado que exploró la posición del enemigo, si tienes una indicación clara del número, posición e identidades de tus posibles enemigos, puedes pasar 1 minuto para idear un plan de batalla que tenga en cuenta dichos factores potenciales y reduzca el papel que juega la suerte en la ecuación. Tira una prueba de Saber bélico. Mientras la información fuera precisa y siga siendo precisa cuando tires iniciativa contra esos enemigos, puedes usar el resultado de Saber bélico que tiraste previamente para tu tirada de iniciativa; si lo haces, esto es un efecto de fortuna."""
        },

        # Medicina
        {
            "name": "Perspicacia forense",
            "level": 1,
            "prerequisites": "entrenado en Medicina",
            "traits": ["General", "Habilidad"],
            "skill": "Medicina",
            "description": """Entiendes principios de medicina forense, haciéndote mejor examinando un cuerpo para determinar la causa de muerte o lesión. Puedes realizar un examen forense en un cuerpo, como se describe bajo Recordar conocimiento en la habilidad Medicina, en la mitad del tiempo normal (hasta un mínimo de 5 minutos). Si tienes éxito en tu prueba, puedes intentar una prueba inmediata para Recordar conocimiento para seguir algo que encontraste, con un bonificador circunstancial +2. Esta prueba normalmente está relacionada con la causa de la lesión o muerte, como una prueba de Artesanía para identificar un veneno o arma usada o una prueba adicional de Medicina para identificar una enfermedad específica. Si prefieres, puedes en cambio intentar Recordar conocimiento sobre el tipo de criatura cuyo cuerpo examinaste, usando la habilidad apropiada y obteniendo el mismo bonificador circunstancial.

El bonificador circunstancial aumenta a +3 si tienes competencia de maestro en Medicina y +4 si tienes competencia legendaria."""
        },
        {
            "name": "Inoculación",
            "level": 1,
            "prerequisites": "entrenado en Medicina",
            "traits": ["General", "Curación", "Habilidad"],
            "skill": "Medicina",
            "description": """Tienes práctica combatiendo plagas, y tus pacientes son menos propensos a sucumbir a la misma enfermedad de nuevo por un tiempo. Cuando Tratas con éxito una enfermedad en alguien y se recupera completamente de la enfermedad, obtiene un bonificador circunstancial +2 a las salvaciones contra esa misma enfermedad durante 1 semana."""
        },
        {
            "name": "Cirugía arriesgada",
            "level": 1,
            "prerequisites": "entrenado en Medicina",
            "traits": ["General", "Habilidad"],
            "skill": "Medicina",
            "description": """Tu cirugía puede traer a un paciente de vuelta del borde de la muerte, pero podría empujarlo al otro lado. Cuando Tratas heridas, puedes infligir 1d8 de daño cortante a tu paciente justo antes de aplicar los efectos de Tratar heridas. Si lo haces, obtienes un bonificador circunstancial +2 a tu prueba de Medicina para Tratar heridas, y si sacas un éxito, obtienes un éxito crítico en su lugar."""
        },

        # Naturaleza
        {
            "name": "Jinete expreso",
            "level": 1,
            "prerequisites": "entrenado en Naturaleza",
            "traits": ["Exploración", "General", "Habilidad"],
            "skill": "Naturaleza",
            "description": """Puedes animar a tu montura a cubrir terreno rápidamente. Al calcular tu Velocidad de viaje para el día mientras vas montado, puedes intentar una prueba de Naturaleza para Ordenar a un animal para aumentar la Velocidad de viaje de tu montura. La CD la determina el DJ, pero típicamente se basa en el nivel de la montura o la dificultad del entorno, lo que sea más difícil. Con un éxito, aumentas la Velocidad de viaje de tu montura a la mitad. Esto no tiene efecto en el movimiento de tu montura en encuentros. Este beneficio se extiende hasta a otros seis aliados que viajen contigo, siempre que todos esos aliados también vayan montados, o sean cuadrúpedos con una Velocidad de al menos 9 metros."""
        },
        {
            "name": "Influir en la naturaleza",
            "level": 7,
            "prerequisites": "maestro en Naturaleza",
            "traits": ["Entre descansos", "General", "Habilidad"],
            "skill": "Naturaleza",
            "description": """Con paciencia y tiempo, puedes hacer llamadas de pájaros, dejar rastros de caza, y finalmente influir en el comportamiento de cierto tipo de animales en la región para que te favorezcan e incluso te ayuden en los días venideros. El DJ determina la CD de cualquier prueba requerida y la cantidad de tiempo que requiere tu trabajo (normalmente al menos uno o dos días de tiempo de inactividad). Aunque no puedes controlar directamente cómo has influido en la naturaleza, puedes esperar ciertos efectos, como cacerías más fáciles o pájaros que se callan cuando se acerca el peligro. Si eres legendario en Naturaleza, puedes provocar estos mismos ajustes al comportamiento animal en el área gastando solo 10 minutos."""
        },

        # Ocultismo
        {
            "name": "Adoración engañosa",
            "level": 1,
            "prerequisites": "entrenado en Ocultismo",
            "traits": ["General", "Habilidad"],
            "skill": "Ocultismo",
            "description": """Los miembros de tu culto frecuentemente se hacen pasar por adoradores de otras religiones. Puedes usar Ocultismo en lugar de Engaño para Hacerte pasar por un adorador típico de otra fe o para Mentir específicamente para afirmar que eres miembro de la fe que estás suplantando. Todavía necesitas usar la habilidad Engaño para Hacerte pasar por un adorador específico o para realizar otras acciones engañosas, como intentar Mentir sobre cualquier otro asunto."""
        },
        {
            "name": "Magia de raíz",
            "level": 1,
            "prerequisites": "entrenado en Ocultismo",
            "traits": ["General", "Habilidad"],
            "skill": "Ocultismo",
            "description": """Tus talismanes protegen contra la magia vil. Durante tus preparaciones diarias, puedes ensamblar una pequeña bolsa con trozos de hierbas, pelo, aceites sagrados y otros ingredientes rituales, que das a un aliado; el aliado no puedes ser tú mismo. La primera vez ese día que el aliado intente una salvación contra un conjuro o aparición, obtiene un bonificador circunstancial +1 a la tirada. Este bonificador aumenta a +2 si eres experto en Ocultismo o +3 si eres legendario."""
        },
        {
            "name": "Conocimiento perturbador",
            "level": 7,
            "prerequisites": "maestro en Ocultismo",
            "traits": ["Emoción", "Miedo", "General", "Mental", "Habilidad"],
            "skill": "Ocultismo",
            "description": """Pronuncias una letanía de nombres espantosos, profecías y descripciones de reinos más allá de la comprensión mortal, extraídos de tu estudio de tomos y pergaminos prohibidos. Incluso aquellos que no entienden tu idioma se sienten inquietos por estos secretos terribles. Intenta una prueba de Ocultismo y compara el resultado con la CD de Voluntad de un enemigo dentro de 9 metros, o con las CD de Voluntad de cualquier número de enemigos dentro de 9 metros si eres legendario en Ocultismo. Esas criaturas son temporalmente inmunes durante 24 horas.

**Éxito crítico** El objetivo queda confundido durante 1 asalto y asustado 1.

**Éxito** El objetivo queda asustado 1.

**Fallo** El objetivo no se ve afectado.

**Fallo crítico** Te dejas llevar demasiado por tus propias palabras y quedas asustado 1."""
        },

        # Interpretación
        {
            "name": "Interpretación distrayente",
            "level": 2,
            "prerequisites": "experto en Interpretación",
            "traits": ["General", "Habilidad"],
            "skill": "Interpretación",
            "description": """Tus interpretaciones son especialmente distrayentes, permitiendo a tus aliados Escabullirse con facilidad. Creas una Distracción, excepto que tiras una prueba de Interpretación en lugar de Engaño, y los beneficios de las pruebas exitosas se aplican a un aliado de tu elección en lugar de a ti. Los efectos de un éxito duran hasta el final del turno de ese aliado, y pueden terminar antes basándose en las acciones del aliado. No necesitas estar observando a tu aliado ni saber dónde está, pero necesitas saber que está presente para elegirlo."""
        },

        # Religión
        {
            "name": "Símbolo del peregrino",
            "level": 1,
            "prerequisites": "entrenado en Religión, seguidor de una religión específica",
            "traits": ["General", "Habilidad"],
            "skill": "Religión",
            "description": """Llevas un pequeño símbolo de protección de un sitio sagrado para tu fe. Obtienes un símbolo religioso de madera para tu deidad gratis. Mientras este símbolo religioso esté en tu posesión, cuando empates la tirada de iniciativa de un adversario, actúas primero.

Si pierdes este símbolo religioso, debes comprar o Fabricar un reemplazo y sintonizarlo. Tal símbolo normalmente cuesta al menos 1 pp, y la sintonización toma 10 minutos de oración. También puedes sintonizar un símbolo religioso diferente con la misma cantidad de tiempo, pero pierdes el beneficio del símbolo religioso anterior."""
        },
        {
            "name": "Exhortar a los fieles",
            "level": 2,
            "prerequisites": "experto en Religión, seguidor de una religión específica",
            "traits": ["General", "Habilidad"],
            "skill": "Religión",
            "description": """Tu conocimiento de los principios de tu fe te da perspicacia sobre las mejores formas de conseguir que otros de tu fe te ayuden o sigan tus instrucciones. Cuando Solicitas algo de o Coaccionas a miembros de tu propia fe, puedes intentar una prueba de Religión en lugar de Diplomacia o Intimidación, y obtienes un bonificador circunstancial +2 a la prueba. En un intento fallado críticamente de hacer una Solicitud, la actitud del objetivo hacia ti no empeora."""
        },
        {
            "name": "Santificar agua",
            "level": 2,
            "prerequisites": "experto en Religión, debes adorar a una deidad que liste \"sagrada\" o \"profana\" en su santificación",
            "traits": ["General", "Habilidad"],
            "skill": "Religión",
            "description": """Imbuyes agua con la bendición de tu deidad. Elige un recipiente de agua con Volumen ligero poseído por ti o un aliado dentro de tu alcance. Hasta el final de tu próximo turno, se convierte en agua bendita o agua profana. Puedes elegir agua bendita si tu deidad permite santificación sagrada, agua profana si tu deidad permite santificación profana, o cualquiera si tu deidad permite ambas santificaciones. Este es un efecto temporal y no imparte valor monetario ni permite que el agua sea usada para costes de rituales o similares. Si eres maestro en Religión, puedes santificar dos recipientes cuando tomas esta acción, y si eres legendario, puedes santificar tres."""
        },

        # Sociedad
        {
            "name": "Ojo para los números",
            "level": 1,
            "prerequisites": "entrenado en Sociedad",
            "traits": ["General", "Habilidad"],
            "skill": "Sociedad",
            "description": """Has aprendido a estimar rápidamente el número de objetos en un grupo con precisión relativa con solo un vistazo. Aprendes inmediatamente el número de objetos visualmente similares en un grupo que puedes ver, redondeado al primer dígito del número total. Por ejemplo, podrías mirar una caja de viales de poción y saber que contenía unos 30 viales, pero no sabrías que eran exactamente 33 viales, cuántos tipos diferentes de pociones había, o cuántas de cada tipo. Similarmente, podrías mirar una pila de 2.805 monedas y saber que había unas 3.000 monedas en total. Solo puedes usar esta habilidad en objetos que típicamente pueden contarse, así que no puedes usarla en granos de arena o estrellas en el cielo, por ejemplo.

Si cuentas un número específico de objetos poseídos por un enemigo, como el número de monedas o piezas de equipo que lleva, puedes usar esta información la próxima vez que Fintas o Crees una distracción contra ese objetivo dentro de 1 minuto. Si lo haces, obtienes un bonificador circunstancial +1 a tu prueba y puedes usar Sociedad en lugar de Engaño para la prueba.

Puedes usar esta acción durante un intento de Descifrar escritura que sea principalmente numérica o matemática para obtener un bonificador circunstancial +2 a tu prueba."""
        },
        {
            "name": "Captar contenido",
            "level": 1,
            "prerequisites": "entrenado en Sociedad",
            "traits": ["General", "Habilidad"],
            "skill": "Sociedad",
            "description": """Eres experto en escanear rápidamente papeles sueltos y discernir cuidadosamente el contenido de cartas selladas sin dañar el sello. Puedes intentar pruebas de Sociedad para Descifrar escritura en un mensaje que solo se ve parcialmente, al revés o invertido desde tu perspectiva, y obtienes un bonificador circunstancial +1 a la prueba cuando lo haces. También puedes usar esta dote para descifrar cartas selladas, añadiendo el rasgo manipular a tu intento de Descifrar escritura. Esto no evita que los testigos noten tus esfuerzos; podrías necesitar intentar pruebas de Engaño o Sigilo para evitar ser notado. En cualquier uso de esta dote, el destinatario es consciente de tus esfuerzos en un fallo crítico (por ejemplo, podrías ser pillado fisgoneando o podrías alterar los papeles de una forma que su dueño note)."""
        },
        {
            "name": "Aprovechar contactos",
            "level": 2,
            "prerequisites": "experto en Sociedad, y Gracias cortesanas o Callejero",
            "traits": ["Poco común", "General", "Habilidad"],
            "skill": "Sociedad",
            "description": """Conoces a la gente adecuada que puede hacer cosas por ti en ciertos círculos. Una vez por semana, cuando estés en un área que tenga un grupo establecido de nobles influyentes, élites mercantiles, o similares (si tienes Gracias cortesanas), o una red de personajes desagradables como un gremio de ladrones (si tienes Callejero), puedes usar Sociedad para Solicitar un favor o ayuda de esa gente como si fueran amistosos contigo. Tu solicitud debe tener sentido para el tipo de gente que contactas. Por ejemplo, un miembro de la corte real podría conseguirte una invitación adecuada a un baile elegante, mientras que un ladrón local podría señalarte una forma de infiltrarte sigilosamente en esa misma fiesta. Si tienes éxito crítico en esta prueba, tu contacto te da un consejo útil o te deja entrar en un pequeño secreto, otorgándote a ti o a un miembro de tu grupo un bonificador circunstancial +2 a la primera prueba de habilidad que intentéis cuando actuéis sobre el favor. Si fallas críticamente esta prueba, podrías tener que realizar algún servicio para tu contacto para volver a sus buenas gracias, según determine el DJ."""
        },
        {
            "name": "Red clandestina",
            "level": 2,
            "prerequisites": "experto en Sociedad, Callejero",
            "traits": ["Poco común", "General", "Habilidad"],
            "skill": "Sociedad",
            "description": """Estás conectado con grupos que saben lo que está pasando en las calles, y puedes sacarles información rápidamente. Cuando usas Sociedad para Reunir información en un área donde tienes una red (típicamente un asentamiento donde has pasado al menos una semana o pasado un día de tiempo de inactividad para construir una red más rápido), puedes contactar a un miembro de estos grupos para obtener información directamente de ellos. Esto normalmente toma alrededor de una hora, y no llama tanta atención como Reunir información en público podría. La prueba y la información obtenida por lo demás siguen las reglas normales para Reunir información.

Además, si has consultado con éxito la red clandestina, obtienes un bonificador circunstancial +1 a la próxima prueba para Recordar conocimiento que intentes sobre el tema sobre el que estabas Reuniendo información, o un bonificador circunstancial +2 si estás usando Saber del hampa para la prueba. El DJ podría cambiar la habilidad de Saber relacionada con la red dependiendo de tu ubicación o los detalles específicos de la red a la que estás accediendo."""
        },
        {
            "name": "Ojo biográfico",
            "level": 7,
            "prerequisites": "maestro en Sociedad",
            "traits": ["General", "Secreto", "Habilidad"],
            "skill": "Sociedad",
            "description": """Incluso en una breve conversación o interacción social, captas señales sociales y visuales sutiles para aprender mucho sobre el origen e historia de una persona. Podrías notar trozos de verde bajo las uñas de la persona y determinar que es un herbolario, espiar un alfiler que indica su pertenencia a una sociedad secreta, o algo similar. Captas solo detalles que tienen que ver con su rol social, así que podrías aprender el distrito de la ciudad donde vive un vampiro, pero no aprenderías ninguna de sus debilidades, ni necesariamente que es un vampiro.

Pasa 1 minuto en presencia de alguien que no hayas conocido antes, o que no hayas conocido desde que obtuviste Ojo biográfico por primera vez, luego intenta una prueba de Sociedad CD 30. Obtienes un bonificador circunstancial +1 a la prueba si entablaste conversación con la persona durante este tiempo. Si la persona está tratando deliberadamente de ocultar su naturaleza o presentar una identidad falsa, aprendes sobre su biografía falsa en lugar de la verdadera a menos que el resultado de tu prueba de Sociedad exceda su CD de Voluntad.

**Éxito crítico** Aprendes la profesión de la criatura, su especialidad dentro de esa profesión, y un logro o controversia importante de su carrera. También aprendes la nación y asentamiento donde viven, así como el distrito en una ciudad lo suficientemente grande como para tener distritos. Además, aprendes la nación o asentamiento donde pasaron sus años de formación.

**Éxito** Aprendes la profesión de la criatura y su especialidad dentro de esa profesión. Aprendes la nación o asentamiento donde viven normalmente.

**Fallo** Aprendes la profesión de la criatura y la región del mundo de donde proviene, pero nada más.

**Fallo crítico** Aprendes una información errónea sobre la criatura."""
        },

        # Sigilo
        {
            "name": "Sigilo con armadura",
            "level": 2,
            "prerequisites": "experto en Sigilo",
            "traits": ["General", "Habilidad"],
            "skill": "Sigilo",
            "description": """Has aprendido técnicas para ajustar y modificar tu armadura y movimientos para reducir el ruido que haces. Cuando llevas armadura no ruidosa con la que estás entrenado, tu penalización a las pruebas de Sigilo se reduce en 1 (hasta un mínimo de 0). Si eres maestro en Sigilo, reduces la penalización en 2, y si eres legendario, la reduces en 3. Si tu armadura tiene el rasgo ruidosa, en lugar de reducir la penalización a las pruebas de Sigilo, ignoras los efectos del rasgo ruidosa, permitiéndote eliminar la penalización con una puntuación de Fuerza suficiente como es normal."""
        },
        {
            "name": "Marca de sombra",
            "level": 2,
            "prerequisites": "experto en Sigilo",
            "traits": ["General", "Habilidad"],
            "skill": "Sigilo",
            "description": """Has aprendido trucos especiales que te ayudan a seguir a individuos sin que te noten. Cuando intentas una prueba de Sigilo para Evitar ser detectado mientras sigues a un objetivo específico, el objetivo recibe una penalización circunstancial -2 a su CD de Percepción. Si tienes competencia de maestro en Sigilo, la penalización es -3 o -4 si eres legendario. Si inicias un encuentro con el objetivo mientras lo sigues en las sombras, el objetivo recibe esta penalización a su tirada de iniciativa y a su CD de Percepción para determinar si te nota, como es normal para Escabullirse."""
        },

        # Supervivencia
        {
            "name": "Guía ambiental",
            "level": 7,
            "prerequisites": "maestro en Supervivencia",
            "traits": ["General", "Habilidad"],
            "skill": "Supervivencia",
            "description": """Puedes adaptarte rápidamente a los climas y ayudar a otros a hacer lo mismo. Después de una hora en un entorno, tú y hasta cinco aliados podéis tratar los efectos de temperatura natural de un entorno como un paso menos severos (tratar el frío extremo como frío severo o el calor extremo como calor severo, por ejemplo). Esta reducción en severidad es acumulativa con cualquier equipo (como ropa de abrigo) o conjuros (como resistencia ambiental). Si eres legendario en Supervivencia, puedes protegerte a ti mismo y hasta cinco aliados, y tratáis los efectos de temperatura como dos pasos menos severos."""
        },
        {
            "name": "Guía legendario",
            "level": 15,
            "prerequisites": "legendario en Supervivencia",
            "traits": ["General", "Habilidad"],
            "skill": "Supervivencia",
            "description": """Conoces la naturaleza tan bien que puedes ayudar a tu grupo a viajar a través de ella con facilidad. Cuando estás estableciendo el camino para tu grupo a través de terreno salvaje, tu grupo obtiene un bonificador circunstancial +3 metros a su Velocidad para el propósito de calcular la Velocidad de viaje del grupo, la Velocidad de viaje de tu grupo no disminuye en terreno difícil, y el terreno muy difícil reduce a la mitad la Velocidad de viaje de tu grupo en lugar de reducirla a un tercio. Esto no aumenta la Velocidad de tu grupo durante un encuentro ni permite a tu grupo ignorar el terreno difícil durante un encuentro."""
        },

        # Latrocinio
        {
            "name": "Prestidigitación ocultadora",
            "level": 1,
            "prerequisites": "entrenado en Latrocinio",
            "traits": ["General", "Habilidad"],
            "skill": "Latrocinio",
            "description": """En lugar de esconder un objeto donde los inspectores no buscarán, eres hábil manteniendo el objeto en movimiento para que nunca esté donde miran. Cuando Ocultas un objeto de Volumen ligero o menos, puedes usar Latrocinio en lugar de Sigilo para tus pruebas y para la CD de la prueba de Percepción de un buscador activo. Tiras la prueba solo una vez, pero debes continuar usando acciones para Ocultar un objeto durante todo el proceso."""
        },
        {
            "name": "Truco sucio",
            "level": 1,
            "prerequisites": "entrenado en Latrocinio",
            "traits": ["Ataque", "General", "Manipular", "Habilidad"],
            "skill": "Latrocinio",
            "description": """Atas los cordones de las botas de un enemigo, le bajas el sombrero sobre los ojos, le aflojas el cinturón, o de alguna otra forma confundes su movilidad mediante una táctica deshonesta. Intenta una prueba de Latrocinio contra la CD de Reflejos del objetivo.

**Requisitos:** Tienes una mano libre y estás dentro del alcance cuerpo a cuerpo de un oponente.

**Éxito crítico** El objetivo queda torpe 1 hasta que use una acción Interactuar para terminar el impedimento.

**Éxito** Como éxito crítico, pero la condición termina automáticamente después de 1 asalto.

**Fallo crítico** Caes derribado cuando tu intento falla."""
        },
    ]

    # Generar archivos de dotes generales
    for feat in general_feats:
        slug, content = create_general_feat(
            feat["name"],
            feat["level"],
            feat.get("prerequisites", "—"),
            feat["description"],
            feat["traits"]
        )
        filepath = generales_dir / f"{slug}.md"
        if not filepath.exists():
            filepath.write_text(content, encoding='utf-8')
            files_created += 1
            print(f"✅ General: {feat['name']}")

    # Generar archivos de dotes de habilidad
    for feat in skill_feats:
        slug, content = create_skill_feat(
            feat["name"],
            feat["level"],
            feat.get("prerequisites", ""),
            feat["description"],
            feat["traits"],
            feat.get("skill")
        )
        filepath = habilidad_dir / f"{slug}.md"
        if not filepath.exists():
            filepath.write_text(content, encoding='utf-8')
            files_created += 1
            print(f"✅ Habilidad: {feat['name']}")

    print(f"\n📦 Total: {files_created} archivos de dotes PC2 generados")
    print(f"   - {len(general_feats)} dotes generales")
    print(f"   - {len(skill_feats)} dotes de habilidad")

    return files_created

if __name__ == '__main__':
    generate_feats()
