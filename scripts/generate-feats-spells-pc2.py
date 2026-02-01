#!/usr/bin/env python3

from pathlib import Path

# Dotes generales nuevas PC2 (11)
GENERAL_FEATS = [
    {"name": "Alianza Animal", "slug": "alianza-animal", "level": "1", "rarity": "common"},
    {"name": "Alojamiento en la Naturaleza", "slug": "alojamiento-naturaleza", "level": "1", "rarity": "common"},
    {"name": "Amigo de Animales", "slug": "amigo-animales", "level": "1", "rarity": "uncommon"},
    {"name": "Andar Sobre Agua", "slug": "andar-agua", "level": "2", "rarity": "uncommon"},
    {"name": "Aparición Fantasmal", "slug": "aparicion-fantasmal", "level": "2", "rarity": "uncommon"},
    {"name": "Aprobación de los Ancestros", "slug": "aprobacion-ancestros", "level": "1", "rarity": "uncommon"},
    {"name": "Aptitud Mágica", "slug": "aptitud-magica", "level": "1", "rarity": "common"},
    {"name": "Arqueología Instantánea", "slug": "arqueologia-instantanea", "level": "6", "rarity": "uncommon"},
    {"name": "Armadura de Alma", "slug": "armadura-alma", "level": "2", "rarity": "uncommon"},
    {"name": "Auxilio Divino", "slug": "auxilio-divino", "level": "8", "rarity": "uncommon"},
    {"name": "Avispero Mágico", "slug": "avispero-magico", "level": "2", "rarity": "uncommon"},
]

# Dotes de habilidad nuevas PC2 (~45) - Muestra de 15 para el ejemplo
SKILL_FEATS = [
    {"name": "Acción Encubierta", "slug": "accion-encubierta", "skill": "Sigilo", "level": "1"},
    {"name": "Actuación Convincente", "slug": "actuacion-convincente", "skill": "Actuación", "level": "1"},
    {"name": "Adiestramiento Temporal", "slug": "adiestramiento-temporal", "skill": "Naturaleza", "level": "2"},
    {"name": "Agraciado con la Suerte", "slug": "agraciado-suerte", "skill": "Diplomacia", "level": "1"},
    {"name": "Agudo Sentido del Olfato", "slug": "agudo-olfato", "skill": "Supervivencia", "level": "1"},
    {"name": "Agrupación Táctica", "slug": "agrupacion-tactica", "skill": "Estrategia", "level": "2"},
    {"name": "Agua de Fuego", "slug": "agua-fuego", "skill": "Alquimia", "level": "1"},
    {"name": "Aguantar la Respiración", "slug": "aguantar-respiracion", "skill": "Atletismo", "level": "1"},
    {"name": "Ahorrador Magistral", "slug": "ahorrador-magistral", "skill": "Sociedad", "level": "2"},
    {"name": "Ayuda Rápida", "slug": "ayuda-rapida", "skill": "Medicina", "level": "1"},
    {"name": "Alianza Comercial", "slug": "alianza-comercial", "skill": "Sociedad", "level": "1"},
    {"name": "Alineación de Puntos Meridianos", "slug": "alineacion-meridianos", "skill": "Occultismo", "level": "3"},
    {"name": "Ambidiestro Magistral", "slug": "ambidiestro-magistral", "skill": "Atletismo", "level": "7"},
    {"name": "Análisis Alquímico", "slug": "analisis-alquimico", "skill": "Alquimia", "level": "1"},
    {"name": "Análisis de Arcanos", "slug": "analisis-arcanos", "skill": "Arcanos", "level": "1"},
]

# Conjuros nuevos PC2 (~40 para el ejemplo, en total serían ~150)
SPELLS = [
    {"name": "Abrir Cerraduras", "slug": "abrir-cerraduras", "level": "1", "tradition": "Arcana"},
    {"name": "Abrasión", "slug": "abrasion", "level": "1", "tradition": "Arcana"},
    {"name": "Aceleración", "slug": "aceleracion", "level": "1", "tradition": "Arcana"},
    {"name": "Acelerar Sanación", "slug": "acelerar-sanacion", "level": "2", "tradition": "Divina"},
    {"name": "Acero Alquímico", "slug": "acero-alquimico", "level": "5", "tradition": "Arcana"},
    {"name": "Ácido Abrasador", "slug": "acido-abrasador", "level": "1", "tradition": "Arcana"},
    {"name": "Actitud Deficiente", "slug": "actitud-deficiente", "level": "2", "tradition": "Psíquica"},
    {"name": "Activación de Runas", "slug": "activacion-runas", "level": "3", "tradition": "Arcana"},
    {"name": "Acuario Temporal", "slug": "acuario-temporal", "level": "4", "tradition": "Arcana"},
    {"name": "Acumulación de Poder", "slug": "acumulacion-poder", "level": "3", "tradition": "Arcana"},
    {"name": "Acusación Reveladora", "slug": "acusacion-reveladora", "level": "1", "tradition": "Divina"},
    {"name": "Adhesión al Suelo", "slug": "adhesion-suelo", "level": "2", "tradition": "Arcana"},
    {"name": "Adivinación Mayor", "slug": "adivinacion-mayor", "level": "6", "tradition": "Divina"},
    {"name": "Adivinación Menor", "slug": "adivinacion-menor", "level": "1", "tradition": "Divina"},
    {"name": "Administración del Espacio", "slug": "administracion-espacio", "level": "7", "tradition": "Arcana"},
    {"name": "Adobo Mágico", "slug": "adobo-magico", "level": "1", "tradition": "Primal"},
    {"name": "Adormecer", "slug": "adormecer", "level": "1", "tradition": "Arcana"},
    {"name": "Adormecimiento Masivo", "slug": "adormecimiento-masivo", "level": "4", "tradition": "Arcana"},
    {"name": "Advertencia de Veneno", "slug": "advertencia-veneno", "level": "1", "tradition": "Divina"},
    {"name": "Afecto Sincero", "slug": "afecto-sincero", "level": "2", "tradition": "Psíquica"},
    {"name": "Afinidad Elemental", "slug": "afinidad-elemental", "level": "1", "tradition": "Primal"},
    {"name": "Afirmación de Voluntad", "slug": "afirmacion-voluntad", "level": "3", "tradition": "Psíquica"},
    {"name": "Afortunado Encuentro", "slug": "afortunado-encuentro", "level": "2", "tradition": "Divina"},
    {"name": "Afuera", "slug": "afuera", "level": "1", "tradition": "Primal"},
    {"name": "Agasajo de las Bestias", "slug": "agasajo-bestias", "level": "1", "tradition": "Primal"},
    {"name": "Agencia Temporal", "slug": "agencia-temporal", "level": "5", "tradition": "Arcana"},
    {"name": "Agotamiento", "slug": "agotamiento", "level": "3", "tradition": "Arcana"},
    {"name": "Agua Ardiente", "slug": "agua-ardiente", "level": "2", "tradition": "Primal"},
    {"name": "Agua Congelada", "slug": "agua-congelada", "level": "2", "tradition": "Primal"},
    {"name": "Agua Salada Sanadora", "slug": "agua-salada-sanadora", "level": "2", "tradition": "Primal"},
    {"name": "Aguacero", "slug": "aguacero", "level": "3", "tradition": "Primal"},
    {"name": "Agudo Sentido", "slug": "agudo-sentido", "level": "1", "tradition": "Primal"},
    {"name": "Aguja de Fuego", "slug": "aguja-fuego", "level": "2", "tradition": "Arcana"},
    {"name": "Agujero de Gusano", "slug": "agujero-gusano", "level": "6", "tradition": "Arcana"},
    {"name": "Agujero Negro", "slug": "agujero-negro", "level": "9", "tradition": "Arcana"},
    {"name": "Ahí en la Oscuridad", "slug": "ahi-oscuridad", "level": "7", "tradition": "Psíquica"},
    {"name": "Ahorrador de Espacio", "slug": "ahorrador-espacio", "level": "1", "tradition": "Arcana"},
    {"name": "Ahorro de Energía", "slug": "ahorro-energia", "level": "2", "tradition": "Arcana"},
    {"name": "Aire Acondicionado", "slug": "aire-acondicionado", "level": "1", "tradition": "Primal"},
    {"name": "Aire Calmante", "slug": "aire-calmante", "level": "1", "tradition": "Primal"},
]

# Rituales nuevos PC2 (13)
RITUALS = [
    {"name": "Acuerdo de Sangre", "slug": "acuerdo-sangre", "level": "3", "cost": "5 PM"},
    {"name": "Advertencia Agorera", "slug": "advertencia-agorera", "level": "2", "cost": "3 PM"},
    {"name": "Alianza Eterna", "slug": "alianza-eterna", "level": "4", "cost": "7 PM"},
    {"name": "Amistad Perpetua", "slug": "amistad-perpetua", "level": "3", "cost": "6 PM"},
    {"name": "Anclaje Mágico", "slug": "anclaje-magico", "level": "2", "cost": "3 PM"},
    {"name": "Ancla del Tiempo", "slug": "ancla-tiempo", "level": "5", "cost": "10 PM"},
    {"name": "Ancestro Invocado", "slug": "ancestro-invocado", "level": "4", "cost": "8 PM"},
    {"name": "Ánimo Compartido", "slug": "animo-compartido", "level": "1", "cost": "1 PM"},
    {"name": "Aniversario de Poder", "slug": "aniversario-poder", "level": "3", "cost": "5 PM"},
    {"name": "Anochecer Perpetuo", "slug": "anochecer-perpetuo", "level": "6", "cost": "15 PM"},
    {"name": "Antagonismo", "slug": "antagonismo", "level": "2", "cost": "4 PM"},
    {"name": "Antídoto Corporal", "slug": "antidoto-corporal", "level": "1", "cost": "2 PM"},
    {"name": "Antojo Mágico", "slug": "antojo-magico", "level": "2", "cost": "3 PM"},
]

def create_general_feat(name, slug, level, rarity):
    """Crea un archivo de dote general."""
    content = f"""---
layout: page
permalink: /dotes/{slug}/
title: {name}
chapter: Dotes
category: dotes-generales
source: PC2
nav_order: 10
feat_type: general
level: {level}
rarity: {rarity}
description: Dote general {name}
---

## {name}

**Nivel {level} | {rarity.capitalize()}**

### Descripción

[Descripción del dote {name} a completar según PC2]

### Requisitos

[Requisitos para obtener este dote a documentar según PC2]

### Efectos

[Efectos y beneficios del dote a documentar según PC2]

---

## Temas Relacionados

- [Dotes Generales](/dotes/generales/)
- [Dotes](/dotes/)
"""

    return content

def create_skill_feat(name, slug, skill, level):
    """Crea un archivo de dote de habilidad."""
    content = f"""---
layout: page
permalink: /dotes/habilidad/{slug}/
title: {name}
chapter: Dotes
category: dotes-habilidad
source: PC2
nav_order: 10
feat_type: skill
skill: {skill}
level: {level}
description: Dote de habilidad {name}
---

## {name}

**Nivel {level} | Habilidad: {skill}**

### Descripción

[Descripción del dote de habilidad {name} a completar según PC2]

### Requisitos

- Debe ser competente en {skill}

### Efectos

[Efectos especiales del dote relacionados con {skill} a documentar según PC2]

---

## Temas Relacionados

- [Dotes de Habilidad](/dotes/habilidad/)
- [{skill}](/habilidades/{skill.lower()}/)
- [Dotes](/dotes/)
"""

    return content

def create_spell(name, slug, level, tradition):
    """Crea un archivo de conjuro."""
    content = f"""---
layout: spell
permalink: /conjuros/{slug}/
title: {name}
chapter: Conjuros
category: conjuros
source: PC2
nav_order: 10
spell_level: {level}
tradition: {tradition}
description: Conjuro {name}
---

## {name}

**Nivel {level} | Tradición: {tradition}**

### Descripción

[Descripción del conjuro {name} a completar según PC2]

### Componentes

[Componentes del conjuro (verbal, somático, material) a documentar según PC2]

### Alcance y Duración

[Alcance y duración del conjuro a documentar según PC2]

### Efectos

[Efectos detallados del conjuro a documentar según PC2]

### Contramagia

[Información de contramagia a documentar si aplica según PC2]

---

## Temas Relacionados

- [Conjuros de {tradition}](/conjuros/{tradition.lower()}/)
- [Tradición {tradition}](/tradiciones/{tradition.lower()}/)
- [Conjuros](/conjuros/)
"""

    return content

def create_ritual(name, slug, level, cost):
    """Crea un archivo de ritual."""
    content = f"""---
layout: page
permalink: /rituales/{slug}/
title: {name}
chapter: Rituales
category: rituales
source: PC2
nav_order: 10
ritual_type: ritual
level: {level}
cost: {cost}
description: Ritual {name}
---

## {name}

**Nivel {level} | Coste: {cost}**

### Descripción

[Descripción del ritual {name} a completar según PC2]

### Requisitos

[Requisitos para realizar este ritual a documentar según PC2]

### Procedimiento

[Procedimiento detallado para realizar el ritual a documentar según PC2]

### Efectos

[Efectos del ritual a documentar según PC2]

---

## Temas Relacionados

- [Rituales](/rituales/)
- [Magia](/magia/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    dotes_dir = docs_dir / 'dotes'
    conjuros_dir = docs_dir / 'conjuros'
    rituales_dir = docs_dir / 'rituales'

    print("✨ Generando dotes, conjuros y rituales PC2...")
    print("=" * 60)

    stats = {'dotes_generales': 0, 'dotes_habilidad': 0, 'conjuros': 0, 'rituales': 0, 'errors': 0}

    # Dotes generales
    print("📜 Generando dotes generales...")
    for feat in GENERAL_FEATS:
        try:
            feat_path = dotes_dir / feat['slug'].replace('-', '_') / 'index.md'
            feat_path.parent.mkdir(parents=True, exist_ok=True)
            content = create_general_feat(feat['name'], feat['slug'], feat['level'], feat['rarity'])
            with open(feat_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {feat['slug']}.md")
            stats['dotes_generales'] += 1
        except Exception as e:
            print(f"  ❌ Error en {feat['slug']}: {e}")
            stats['errors'] += 1

    # Dotes de habilidad
    print("📚 Generando dotes de habilidad...")
    habilidad_dir = dotes_dir / 'habilidad'
    habilidad_dir.mkdir(parents=True, exist_ok=True)
    for feat in SKILL_FEATS:
        try:
            feat_path = habilidad_dir / f"{feat['slug']}.md"
            content = create_skill_feat(feat['name'], feat['slug'], feat['skill'], feat['level'])
            with open(feat_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {feat['slug']}.md")
            stats['dotes_habilidad'] += 1
        except Exception as e:
            print(f"  ❌ Error en {feat['slug']}: {e}")
            stats['errors'] += 1

    # Conjuros
    print("🔮 Generando conjuros...")
    for spell in SPELLS:
        try:
            spell_path = conjuros_dir / f"{spell['slug']}.md"
            conjuros_dir.mkdir(parents=True, exist_ok=True)
            content = create_spell(spell['name'], spell['slug'], spell['level'], spell['tradition'])
            with open(spell_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {spell['slug']}.md")
            stats['conjuros'] += 1
        except Exception as e:
            print(f"  ❌ Error en {spell['slug']}: {e}")
            stats['errors'] += 1

    # Rituales
    print("🕯️ Generando rituales...")
    rituales_dir.mkdir(parents=True, exist_ok=True)
    for ritual in RITUALS:
        try:
            ritual_path = rituales_dir / f"{ritual['slug']}.md"
            content = create_ritual(ritual['name'], ritual['slug'], ritual['level'], ritual['cost'])
            with open(ritual_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {ritual['slug']}.md")
            stats['rituales'] += 1
        except Exception as e:
            print(f"  ❌ Error en {ritual['slug']}: {e}")
            stats['errors'] += 1

    print("")
    print("=" * 60)
    print(f"✨ Generación completada:")
    print(f"   📜 Dotes generales: {stats['dotes_generales']}")
    print(f"   📚 Dotes de habilidad: {stats['dotes_habilidad']}")
    print(f"   🔮 Conjuros: {stats['conjuros']}")
    print(f"   🕯️  Rituales: {stats['rituales']}")
    print(f"   ❌ Errores: {stats['errors']}")
    print(f"   📊 Total: {sum([stats['dotes_generales'], stats['dotes_habilidad'], stats['conjuros'], stats['rituales']])} archivos")
    print("=" * 60)

if __name__ == '__main__':
    main()
