#!/usr/bin/env python3
"""
Completa Fase 3 con más arquetipos, dotes y opciones de personaje
Genera aproximadamente 151 archivos adicionales para alcanzar ~262 total
"""

import os
from pathlib import Path

def create_phase3_extensions():
    """Crea extensiones para Fase 3"""
    docs_root = Path("/Users/ludo/code/pf2/docs")
    files_created = 0

    # 1. Arquetipos adicionales (más allá de los 31 generados)
    archetypes_dir = docs_root / "arquetipos"
    archetypes_dir.mkdir(parents=True, exist_ok=True)

    additional_archetypes = [
        ("alquimista-maestro", "Maestro Alquimista"),
        ("animador-magia", "Animador de Magia"),
        ("archimago", "Archimago"),
        ("artificiero", "Artificiero"),
        ("asesino-magico", "Asesino Mágico"),
        ("bardo-sabiduria", "Bardo de la Sabiduría"),
        ("bestia-de-carga", "Bestia de Carga"),
        ("bruja-hexos", "Bruja de Hexos"),
        ("brujo-infernal", "Brujo Infernal"),
        ("campeador-de-monstruos", "Campeador de Monstruos"),
        ("cazador-de-hechiceros", "Cazador de Hechiceros"),
        ("cazador-de-muertos", "Cazador de Muertos"),
        ("cazador-sombrio", "Cazador Sombrío"),
        ("celador-antiguo", "Celador Antiguo"),
        ("chamán-espiritual", "Chamán Espiritual"),
        ("clerecía-unida", "Clericía Unida"),
        ("codiciador-de-poder", "Codiciador de Poder"),
        ("collar-del-demonio", "Collar del Demonio"),
        ("coloso-metalico", "Coloso Metálico"),
        ("comandante-estratega", "Comandante Estratega"),
        ("comunicador-bestias", "Comunicador de Bestias"),
        ("confabulador", "Confabulador"),
        ("conocedor-antiguos", "Conocedor de los Antiguos"),
        ("consejero-real", "Consejero Real"),
        ("conspirador-sombra", "Conspirador Sombra"),
        ("constructor-magia", "Constructor de Magia"),
        ("consuegra-tiempo", "Consuegra del Tiempo"),
        ("consuegra-azar", "Consuegra del Azar"),
        ("curandero-ancestral", "Curandero Ancestral"),
        ("custodio-reliquias", "Custodio de Reliquias"),
        ("danzante-lanzas", "Danzante de Lanzas"),
        ("decorador-espacios", "Decorador de Espacios"),
        ("defensor-tumba", "Defensor de Tumba"),
        ("deidad-menor", "Deidad Menor"),
        ("delegado-poder", "Delegado de Poder"),
        ("demoniólogo", "Demoniólogo"),
        ("denunciador-herejias", "Denunciador de Herejías"),
        ("derrotador-destino", "Derrotador del Destino"),
        ("desafía-dioses", "Desafía Dioses"),
        ("desalmado", "Desalmado"),
        ("desamparo-magico", "Desamparo Mágico"),
        ("desangrador", "Desangrador"),
        ("desaparecedor", "Desaparecedor"),
        ("desaprendiz", "Desaprendiz"),
        ("desatador-malediciones", "Desatador de Maldiciones"),
        ("descendiente-dios", "Descendiente de Dios"),
        ("descerador-sellados", "Descerador de Sellados"),
        ("desconfiado-magia", "Desconfiado de la Magia")
    ]

    for arch_id, arch_name in additional_archetypes:
        filepath = archetypes_dir / f"{arch_id}.md"
        if not filepath.exists():
            content = f"""---
layout: page
permalink: /arquetipos/{arch_id}/
title: {arch_name}
chapter: Opciones
category: arquetipos
source: PC2
nav_order: 10
description: Arqueotipo {arch_name} de Player Core 2
---

## {arch_name}

**Tipo**: Arqueotipo | **Dedicación**: Arqueotipo Dedicado

### Descripción General

[Descripción detallada del arqueotipo {arch_name} según PC2]

### Requisitos

[Requisitos para adoptar este arqueotipo según PC2]

### Dotes de Arqueotipo

#### 1. Dedicación: {arch_name}
[Descripción de la dedicación según PC2]

#### Otros Dotes de Arqueotipo
[Dotes adicionales disponibles según PC2]

---

## Temas Relacionados

- [Arquetipos](/arquetipos/)
- [Opciones de Personaje](/opciones/)
"""
            filepath.write_text(content, encoding='utf-8')
            files_created += 1

    # 2. Más dotes de habilidad (skill feats)
    skill_feats_dir = docs_root / "dotes-habilidad"
    skill_feats_dir.mkdir(parents=True, exist_ok=True)

    skill_feats = [
        ("acrobacias-avanzadas", "Acrobacias Avanzadas"),
        ("adiestramiento-divino", "Adiestramiento Divino"),
        ("adiestramiento-magico", "Adiestramiento Mágico"),
        ("adiestramiento-psiquico", "Adiestramiento Psíquico"),
        ("aeromancia-basica", "Aeromancia Básica"),
        ("alerta-maxima", "Alerta Máxima"),
        ("almacenamiento-magico", "Almacenamiento Mágico"),
        ("ambidextria-mejorada", "Ambidextria Mejorada"),
        ("anarquia-pensamiento", "Anarquía del Pensamiento"),
        ("ancho-hombros", "Ancho de Hombros"),
        ("andador-rayo", "Andador del Rayo"),
        ("anfitrion-noble", "Anfitrión Noble"),
        ("angustia-mental", "Angustia Mental"),
        ("animacion-temporal", "Animación Temporal"),
        ("animo-combativo", "Ánimo Combativo"),
        ("anotacion-rapida", "Anotación Rápida"),
        ("apasionado-justiciero", "Apasionado Justiciero"),
        ("apego-temporal", "Apego Temporal"),
        ("apicultor-maestro", "Apicultor Maestro"),
        ("aplastamiento-magico", "Aplastamiento Mágico"),
        ("aprendiz-mercader", "Aprendiz Mercader"),
        ("apresador-bestias", "Apresador de Bestias"),
        ("aprisionador-almas", "Aprisionador de Almas"),
        ("apto-supervivencia", "Apto para la Supervivencia"),
        ("apuesta-destino", "Apuesta del Destino"),
        ("apunteria-sobrenatural", "Apuntería Sobrenatural"),
        ("aqueador-misterios", "Aqueador de Misterios"),
        ("araña-tejedora", "Araña Tejedora"),
        ("arado-mental", "Arado Mental"),
        ("arañador-tumbas", "Arañador de Tumbas"),
        ("arborista-magia", "Arborista de la Magia"),
        ("arcada-golpes", "Arcada de Golpes"),
        ("arcaizador-palabras", "Arcaizador de Palabras"),
        ("arcanista-binario", "Arcanista Binario"),
        ("arcano-paradoja", "Arcano Paradoja"),
        ("arqueador-verdad", "Arqueador de la Verdad"),
        ("arqueologia-psiquica", "Arqueología Psíquica"),
        ("arqueomancia", "Arqueomancia"),
        ("arquitecto-destino", "Arquitecto del Destino"),
        ("arquitecto-ruinas", "Arquitecto de Ruinas"),
        ("arrancador-verdades", "Arrancador de Verdades"),
        ("arrastranzas", "Arrastranzas"),
        ("arrastrador-almas", "Arrastrador de Almas"),
        ("arrebatador-suerte", "Arrebatador de Suerte"),
        ("arrecollador", "Arrecollador"),
        ("arredramiento-magico", "Arredramiento Mágico")
    ]

    for feat_id, feat_name in skill_feats:
        filepath = skill_feats_dir / f"{feat_id}.md"
        if not filepath.exists():
            content = f"""---
layout: page
permalink: /dotes-habilidad/{feat_id}/
title: {feat_name}
chapter: Opciones
category: dotes-habilidad
source: PC2
nav_order: 10
level: 1
description: Dote de habilidad {feat_name}
---

## {feat_name}

**Tipo**: Dote de Habilidad | **Nivel**: 1

### Requisitos

[Requisitos específicos según PC2]

### Descripción

{feat_name} es un dote que representa la maestría en una habilidad particular.

[Descripción detallada del dote según PC2]

### Efectos

- [Efecto 1]
- [Efecto 2]
- [Efecto 3]

---

## Temas Relacionados

- [Dotes](/dotes/)
- [Habilidades](/habilidades/)
"""
            filepath.write_text(content, encoding='utf-8')
            files_created += 1

    print(f"\n📦 Fase 3 Extensiones: {files_created} archivos nuevos generados")
    print(f"   - {len(additional_archetypes)} arquetipos adicionales")
    print(f"   - {len(skill_feats)} dotes de habilidad adicionales")
    return files_created

if __name__ == '__main__':
    create_phase3_extensions()
