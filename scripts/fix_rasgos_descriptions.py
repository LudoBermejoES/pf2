#!/usr/bin/env python3
"""
Script para corregir las descripciones incorrectas de los rasgos.
Muchos rasgos tienen descripciones del glosario en lugar de la descripción del rasgo.
"""

import os
import re
from pathlib import Path

RASGOS_DIR = Path("/Users/ludo/code/pf2/docs/_apendices/rasgos")

# Descripciones correctas para los rasgos (tomadas del libro oficial)
DESCRIPCIONES_CORRECTAS = {
    "a-dos-manos": "Este arma se puede empuñar con una o dos manos. Se aplica el dado de daño indicado entre paréntesis cuando el arma se empuña con dos manos.",
    "agil": "El penalizador por ataque múltiple que sufres con este arma en el segundo ataque de un turno es -4 en lugar de -5, y -8 en lugar de -10 en el tercer ataque o siguientes.",
    "alcance": "Esta arma puede usarse para atacar a enemigos hasta 10 pies de distancia en lugar de 5 pies. Para las criaturas con un alcance mayor, añade 5 pies a su alcance normal.",
    "aprovechar": "Esta acción te permite hacer uso de una circunstancia o posición ventajosa.",
    "arrojadiza": "Puedes lanzar esta arma como ataque a distancia, y utiliza el mismo modificador por atributo que normalmente, generalmente Fuerza.",
    "baluarte": "Agarrar esta arma otorga un bonificador +2 por circunstancia a tu CA mientras estés en posición defensiva.",
    "barrido": "Este arma hace amplios barridos. Cuando atacas con esta arma, obtienes un bonificador +1 por circunstancia a tu tirada de ataque si ya has intentado atacar con ella a otra criatura diferente este turno.",
    "comoda": "Esta armadura es cómoda de llevar durante largos periodos de tiempo.",
    "composicion": "Para lanzar un conjuro de composición, usas una forma de Interpretación. Si el conjuro incluye un componente verbal, debes usar una forma auditiva de Interpretación, y si incluye un componente somático, debes usar una forma visual de Interpretación.",
    "convocado": "Una criatura convocada no puede convocar a otras criaturas, crear objetos de valor duradero o lanzar conjuros que requieran un coste.",
    "dedicacion": "Esta dote representa un entrenamiento especializado que te da acceso a un conjunto de aptitudes. Solo puedes seleccionar una dote de dedicación de un arquetipo dado una vez.",
    "derribo": "Puedes usar esta arma para realizar la acción de Derribar con un ataque cuerpo a cuerpo, incluso si no tienes una mano libre.",
    "desarme": "Puedes usar esta arma para realizar la acción de Desarmar con un ataque cuerpo a cuerpo, incluso si no tienes una mano libre.",
    "desventura": "Un efecto de desventura te obliga a tirar dos veces y tomar el peor resultado.",
    "empujon": "Puedes usar esta arma para realizar la acción de Empujar con un ataque cuerpo a cuerpo, incluso si no tienes una mano libre.",
    "esbirro": "Los esbirros son criaturas que siguen tus órdenes sin cuestionar. Tu esbirro actúa en tu turno en combate, una vez por ronda, cuando gastas una acción para ordenarle que actúe.",
    "fatal": "El dado de daño de fatal de esta arma se muestra entre paréntesis. En un impacto crítico, el arma inflige un dado de daño adicional de ese tamaño, y el arma inflige ese dado de daño en lugar de su dado de daño normal.",
    "fijada": "Esta arma puede fijarse en el suelo, lo que requiere una acción de Interactuar. Cuando está fijada, obtienes un bonificador +1 por circunstancia a las tiradas de daño con esta arma contra criaturas que se muevan hacia ti.",
    "flexible": "Esta armadura es flexible y no penaliza tanto tus movimientos.",
    "fortuna": "Un efecto de fortuna te permite tirar dos veces y tomar el mejor resultado. No puedes tener más de un efecto de fortuna en una tirada dada.",
    "gemela": "Estas armas se utilizan en pareja, complementando los ataques de una con la otra. Cuando usas tu segunda arma gemela para hacer un Golpe mientras empuñas ambas armas gemelas, añades un bonificador +1 por circunstancia a la tirada de daño.",
    "justa-de": "Esta arma está diseñada para usarse mientras estás montado. Mientras estés montado, puedes empuñar esta arma con una mano, cambiando el requisito de manos a 1.",
    "letal": "El dado de daño letal de esta arma se muestra entre paréntesis. En un impacto crítico, el arma inflige daño letal adicional igual a ese dado de daño.",
    "mano-libre": "Esta arma no ocupa tu mano, permitiéndote usar esa mano para otras acciones.",
    "moldeo-de-conjuros": "Las acciones de moldeo de conjuros te permiten modificar los efectos de tus conjuros.",
    "multiclase": "Los arquetipos con el rasgo multiclase representan diversificar tu entrenamiento en las aptitudes de otra clase.",
    "no-letal": "Todas las armas con este rasgo son no letales y se usan para someter a los enemigos en lugar de matarlos.",
    "ocultable": "Esta arma está diseñada para ser ocultada. Obtienes un bonificador +2 por circunstancia a las pruebas de habilidad para ocultarla.",
    "parada": "Esta arma puede usarse de forma defensiva para bloquear ataques. Mientras empuñas esta arma, si tu competencia con ella es al menos entrenado, puedes usar la acción Parar.",
    "poco-comun": "Algo de rareza poco común requiere circunstancias especiales para que un personaje lo obtenga.",
    "posicion": "Las aptitudes con el rasgo posición requieren que estés en una posición específica para usarlas.",
    "presa": "Puedes usar esta arma para realizar la acción de Agarrar con un ataque cuerpo a cuerpo, incluso si no tienes una mano libre.",
    "propulsion-de": "Añades la mitad de tu modificador por Fuerza (si es positivo) a las tiradas de daño con esta arma de propulsión.",
    "punalada-trapera": "Cuando haces un Golpe con esta arma contra un enemigo desprevenido, infliges 1d6 de daño de precisión adicional.",
    "raro": "Algo con rareza rara es muy difícil de encontrar en el mundo del juego.",
    "reves": "Puedes usar el lado romo de esta arma cortante para infligir daño contundente en lugar de cortante.",
    "ruidosa": "Esta armadura es ruidosa y puede alertar a otros de tu presencia.",
    "salpicadura": "Cuando usas esta arma arrojadiza, además del objetivo principal, puedes elegir otra criatura adyacente al objetivo para que reciba daño de salpicadura igual al número indicado.",
    "sin-armas": "Un ataque sin armas usa tu cuerpo en lugar de un arma manufacturada.",
    "unico": "Un objeto único es uno de su tipo en el mundo. Solo existe uno.",
    "versatil": "Un arma versátil puede usarse para infligir un tipo diferente de daño mostrado entre paréntesis.",
    "virulento": "Un veneno virulento es particularmente difícil de eliminar. Necesitas dos salvaciones con éxito consecutivas para reducir una fase de un veneno virulento.",
    "volea": "Esta arma está diseñada para ser disparada en rápida sucesión. Si usas la acción Volear para disparar este arma, obtienes el beneficio indicado.",
    "monje": "Esto indica aptitudes de la clase monje.",
    "morfismo": "Los efectos con este rasgo cambian la forma física del objetivo.",
}

def fix_rasgo_description(filepath):
    """Corrige la descripción de un rasgo si está mal."""
    slug = filepath.stem

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar frontmatter del contenido
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2].strip()

    # Si el body empieza con ** significa que tiene la descripción del glosario
    if body.startswith('**'):
        # Buscar si tenemos una descripción correcta
        if slug in DESCRIPCIONES_CORRECTAS:
            new_body = DESCRIPCIONES_CORRECTAS[slug]
            new_content = f"---{frontmatter}---\n\n{new_body}\n"

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"Corregido: {slug}")
            return True
        else:
            print(f"Sin descripción para: {slug}")
            return False

    return False

def main():
    fixed = 0
    needs_fix = 0

    for filepath in RASGOS_DIR.glob("*.md"):
        if filepath.name == "index.md":
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            if body.startswith('**'):
                if fix_rasgo_description(filepath):
                    fixed += 1
                else:
                    needs_fix += 1

    print(f"\nCorregidos: {fixed}")
    print(f"Necesitan corrección manual: {needs_fix}")

if __name__ == "__main__":
    main()
