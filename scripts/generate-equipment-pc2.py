#!/usr/bin/env python3

from pathlib import Path

# Alquimia PC2 (~20 muestra de 80)
ALCHEMICAL_ITEMS = [
    {"name": "Ácido Alquímico", "slug": "acido-alquimico", "type": "Veneno", "price": "1 PO"},
    {"name": "Antídoto Alquímico", "slug": "antidoto-alquimico", "type": "Antídoto", "price": "5 PO"},
    {"name": "Bálsamo Calmante", "slug": "balsamo-calmante", "type": "Elixir", "price": "10 PO"},
    {"name": "Bomba de Ácido", "slug": "bomba-acido", "type": "Bomba", "price": "3 PO"},
    {"name": "Bomba de Fuego", "slug": "bomba-fuego", "type": "Bomba", "price": "3 PO"},
    {"name": "Bomba de Hielo", "slug": "bomba-hielo", "type": "Bomba", "price": "3 PO"},
    {"name": "Bomba Algodonosa", "slug": "bomba-algodonosa", "type": "Bomba", "price": "2 PO"},
    {"name": "Cataplasma Curativa", "slug": "cataplasma-curativa", "type": "Medicamento", "price": "4 PO"},
    {"name": "Elixir de Agilidad", "slug": "elixir-agilidad", "type": "Elixir", "price": "15 PO"},
    {"name": "Elixir de Fuerza", "slug": "elixir-fuerza", "type": "Elixir", "price": "15 PO"},
    {"name": "Elixir de Resistencia", "slug": "elixir-resistencia", "type": "Elixir", "price": "20 PO"},
    {"name": "Espuma de Extinción", "slug": "espuma-extincion", "type": "Equipo", "price": "5 PO"},
    {"name": "Explosivo Alquímico", "slug": "explosivo-alquimico", "type": "Bomba", "price": "8 PO"},
    {"name": "Gas Anestésico", "slug": "gas-anestesico", "type": "Gas", "price": "10 PO"},
    {"name": "Incienso de Concentración", "slug": "incienso-concentracion", "type": "Consumible", "price": "3 PO"},
    {"name": "Líquido Inflamable", "slug": "liquido-inflamable", "type": "Combustible", "price": "2 PO"},
    {"name": "Mutágeno Mayor", "slug": "mutageno-mayor", "type": "Mutágeno", "price": "35 PO"},
    {"name": "Mutágeno Menor", "slug": "mutageno-menor", "type": "Mutágeno", "price": "8 PO"},
    {"name": "Poción de Cicatrización", "slug": "pocion-cicatrizacion", "type": "Poción", "price": "6 PO"},
    {"name": "Veneno de Araña", "slug": "veneno-arana", "type": "Veneno", "price": "8 PO"},
]

# Objetos Mágicos PC2 (~20 muestra de 100)
MAGICAL_ITEMS = [
    {"name": "Amuleto de Armadura", "slug": "amuleto-armadura", "type": "Amuleto", "level": "1", "price": "35 PO"},
    {"name": "Anillo de Protección", "slug": "anillo-proteccion", "type": "Anillo", "level": "1", "price": "40 PO"},
    {"name": "Anillo de Resistencia", "slug": "anillo-resistencia", "type": "Anillo", "level": "2", "price": "65 PO"},
    {"name": "Arma Viviente Menor", "slug": "arma-viviente-menor", "type": "Arma", "level": "2", "price": "90 PO"},
    {"name": "Bolsa de Sustentación", "slug": "bolsa-sustentacion", "type": "Bolsa", "level": "1", "price": "50 PO"},
    {"name": "Botas de Velocidad", "slug": "botas-velocidad", "type": "Objeto Portado", "level": "2", "price": "110 PO"},
    {"name": "Brazalete de Defensa", "slug": "brazalete-defensa", "type": "Pulsera", "level": "1", "price": "50 PO"},
    {"name": "Brújula Mágica", "slug": "brujula-magica", "type": "Instrumento", "level": "1", "price": "25 PO"},
    {"name": "Caliz Restaurador", "slug": "caliz-restaurador", "type": "Recipiente", "level": "2", "price": "100 PO"},
    {"name": "Capa de Ilusión", "slug": "capa-ilusion", "type": "Objeto Portado", "level": "2", "price": "130 PO"},
    {"name": "Casco de Sabiduría", "slug": "casco-sabiduria", "type": "Armadura", "level": "2", "price": "120 PO"},
    {"name": "Collar de Elegancia", "slug": "collar-elegancia", "type": "Collar", "level": "1", "price": "45 PO"},
    {"name": "Cuero Mágico", "slug": "cuero-magico", "type": "Armadura", "level": "1", "price": "60 PO"},
    {"name": "Espada Llameante", "slug": "espada-llameante", "type": "Arma", "level": "2", "price": "125 PO"},
    {"name": "Escudo Mágico", "slug": "escudo-magico", "type": "Armadura", "level": "1", "price": "55 PO"},
    {"name": "Espejo de Verdad", "slug": "espejo-verdad", "type": "Objeto", "level": "3", "price": "250 PO"},
    {"name": "Forma de Animal", "slug": "forma-animal", "type": "Objeto Portado", "level": "2", "price": "100 PO"},
    {"name": "Gafas de Visión Nocturna", "slug": "gafas-vision-nocturna", "type": "Objeto Portado", "level": "1", "price": "35 PO"},
    {"name": "Lápiz de Creación", "slug": "lapiz-creacion", "type": "Herramienta", "level": "2", "price": "200 PO"},
    {"name": "Linterna Eterna", "slug": "linterna-eterna", "type": "Objeto", "level": "1", "price": "30 PO"},
]

# Trampas PC2 (~12 muestra de 25)
TRAPS = [
    {"name": "Aguja Envenenada", "slug": "aguja-envenenada", "type": "Mecánica", "level": "1", "dc": "12"},
    {"name": "Alarma Mágica", "slug": "alarma-magica", "type": "Mágica", "level": "1", "dc": "11"},
    {"name": "Bloqueo Mágico", "slug": "bloqueo-magico", "type": "Mágica", "level": "2", "dc": "15"},
    {"name": "Bola de Fuego", "slug": "bola-fuego", "type": "Mágica", "level": "3", "dc": "20"},
    {"name": "Caída de Rocas", "slug": "caida-rocas", "type": "Mecánica", "level": "2", "dc": "16"},
    {"name": "Chamuscador de Llamas", "slug": "chamuscador-llamas", "type": "Mágica", "level": "1", "dc": "13"},
    {"name": "Cristal Afilado", "slug": "cristal-afilado", "type": "Mecánica", "level": "0", "dc": "10"},
    {"name": "Disruptor Mágico", "slug": "disruptor-magico", "type": "Mágica", "level": "3", "dc": "22"},
    {"name": "Esfera de Rayo", "slug": "esfera-rayo", "type": "Mágica", "level": "4", "dc": "25"},
    {"name": "Espinas Venenosas", "slug": "espinas-venenosas", "type": "Mecánica", "level": "1", "dc": "14"},
    {"name": "Foso Oculto", "slug": "foso-oculto", "type": "Mecánica", "level": "1", "dc": "15"},
    {"name": "Gas Paralizante", "slug": "gas-paralizante", "type": "Mecánica", "level": "2", "dc": "17"},
]

def create_alchemical_item(name, slug, item_type, price):
    """Crea un archivo de objeto alquímico."""
    content = f"""---
layout: page
permalink: /equipo/alquimia/{slug}/
title: {name}
chapter: Equipo
category: alquimia
source: PC2
nav_order: 10
item_type: {item_type}
price: {price}
description: Objeto alquímico {name}
---

## {name}

**Tipo**: {item_type} | **Precio**: {price}

### Descripción

[Descripción del objeto alquímico {name} a completar según PC2]

### Cómo Se Usa

[Instrucciones de uso a documentar según PC2]

### Efectos

[Efectos específicos del objeto alquímico a documentar según PC2]

---

## Temas Relacionados

- [Alquimia](/equipo/alquimia/)
- [Equipo](/equipo/)
- [Objetos Consumibles](/equipo/consumibles/)
"""

    return content

def create_magical_item(name, slug, item_type, level, price):
    """Crea un archivo de objeto mágico."""
    content = f"""---
layout: page
permalink: /equipo/magicos/{slug}/
title: {name}
chapter: Equipo
category: objetos-magicos
source: PC2
nav_order: 10
item_type: {item_type}
level: {level}
price: {price}
description: Objeto mágico {name}
---

## {name}

**Tipo**: {item_type} | **Nivel**: {level} | **Precio**: {price}

### Descripción

[Descripción del objeto mágico {name} a completar según PC2]

### Activación

[Cómo activar este objeto mágico a documentar según PC2]

### Poderes

[Poderes específicos del objeto mágico a documentar según PC2]

### Construcción

[Requisitos de construcción a documentar según PC2]

---

## Temas Relacionados

- [Objetos Mágicos](/equipo/magicos/)
- [Equipo](/equipo/)
- [Construcción Mágica](/reglas/construccion-magica/)
"""

    return content

def create_trap(name, slug, trap_type, level, dc):
    """Crea un archivo de trampa."""
    content = f"""---
layout: page
permalink: /equipo/trampas/{slug}/
title: {name}
chapter: Equipo
category: trampas
source: PC2
nav_order: 10
trap_type: {trap_type}
level: {level}
dc: {dc}
description: Trampa {name}
---

## {name}

**Tipo**: {trap_type} | **Nivel**: {level} | **DC**: {dc}

### Descripción

[Descripción de la trampa {name} a completar según PC2]

### Construcción

[Cómo se construye o activa esta trampa a documentar según PC2]

### Defensa

[Cómo los personajes pueden defenderse o desactivar esta trampa a documentar según PC2]

### Efectos

[Efectos cuando la trampa se activa a documentar según PC2]

---

## Temas Relacionados

- [Trampas](/equipo/trampas/)
- [Equipo](/equipo/)
- [Construcción de Trampas](/reglas/construccion-trampas/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    equipo_dir = docs_dir / 'equipo'

    print("⚔️ Generando equipo y tesoros PC2...")
    print("=" * 60)

    stats = {'alquimia': 0, 'magicos': 0, 'trampas': 0, 'errors': 0}

    # Alquimia
    print("🧪 Generando alquimia...")
    alquimia_dir = equipo_dir / 'alquimia'
    alquimia_dir.mkdir(parents=True, exist_ok=True)
    for item in ALCHEMICAL_ITEMS:
        try:
            item_path = alquimia_dir / f"{item['slug']}.md"
            content = create_alchemical_item(item['name'], item['slug'], item['type'], item['price'])
            with open(item_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {item['slug']}.md")
            stats['alquimia'] += 1
        except Exception as e:
            print(f"  ❌ Error en {item['slug']}: {e}")
            stats['errors'] += 1

    # Objetos Mágicos
    print("✨ Generando objetos mágicos...")
    magicos_dir = equipo_dir / 'magicos'
    magicos_dir.mkdir(parents=True, exist_ok=True)
    for item in MAGICAL_ITEMS:
        try:
            item_path = magicos_dir / f"{item['slug']}.md"
            content = create_magical_item(item['name'], item['slug'], item['type'], item['level'], item['price'])
            with open(item_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {item['slug']}.md")
            stats['magicos'] += 1
        except Exception as e:
            print(f"  ❌ Error en {item['slug']}: {e}")
            stats['errors'] += 1

    # Trampas
    print("🪤 Generando trampas...")
    trampas_dir = equipo_dir / 'trampas'
    trampas_dir.mkdir(parents=True, exist_ok=True)
    for trap in TRAPS:
        try:
            trap_path = trampas_dir / f"{trap['slug']}.md"
            content = create_trap(trap['name'], trap['slug'], trap['type'], trap['level'], trap['dc'])
            with open(trap_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {trap['slug']}.md")
            stats['trampas'] += 1
        except Exception as e:
            print(f"  ❌ Error en {trap['slug']}: {e}")
            stats['errors'] += 1

    print("")
    print("=" * 60)
    print(f"✨ Generación completada:")
    print(f"   🧪 Objetos alquímicos: {stats['alquimia']}")
    print(f"   ✨ Objetos mágicos: {stats['magicos']}")
    print(f"   🪤 Trampas: {stats['trampas']}")
    print(f"   ❌ Errores: {stats['errors']}")
    print(f"   📊 Total: {sum([stats['alquimia'], stats['magicos'], stats['trampas']])} archivos")
    print("=" * 60)

if __name__ == '__main__':
    main()
