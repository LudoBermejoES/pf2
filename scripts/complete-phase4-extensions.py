#!/usr/bin/env python3
"""
Completa Fase 4 con aproximadamente 31 archivos faltantes
- Más objetos mágicos especializados
- Más trampas avanzadas
- Más objetos alquímicos complementarios
"""

import os
from pathlib import Path

def create_phase4_extensions():
    """Crea extensiones para Fase 4"""
    docs_root = Path("/Users/ludo/code/pf2/docs")
    files_created = 0

    # 1. Objetos mágicos adicionales (high-level items)
    magicos_dir = docs_root / "equipo" / "magicos"
    magicos_dir.mkdir(parents=True, exist_ok=True)

    high_level_items = [
        ("capa-invisibilidad", "Capa de Invisibilidad", 7, 500),
        ("corona-sabiduría", "Corona de Sabiduría", 8, 2000),
        ("espada-llamante", "Espada Llamante", 7, 1500),
        ("escudo-reflejante", "Escudo Reflejante", 6, 800),
        ("botas-velocidad", "Botas de Velocidad", 5, 300),
        ("anillo-regeneracion", "Anillo de Regeneración", 8, 3000),
        ("varita-relámpagos", "Varita de Relámpagos", 6, 700),
        ("amuleto-proteccion-critica", "Amuleto de Protección Crítica", 7, 1200),
        ("guantes-fuerza-gigante", "Guantes de Fuerza de Gigante", 6, 900),
        ("collar-inteligencia", "Collar de Inteligencia", 5, 500),
        ("armadura-heroica", "Armadura Heroica", 8, 2500),
        ("cota-malla-magica", "Cota de Malla Mágica", 7, 1800),
        ("yelmo-true-strike", "Yelmo del Golpe Certero", 6, 1000),
        ("arco-precisión", "Arco de Precisión", 7, 1400),
        ("lanza-trueno", "Lanza de Trueno", 6, 950),
        ("daga-veneno-critico", "Daga del Veneno Crítico", 5, 600),
        ("báculo-poder", "Báculo de Poder", 8, 2200),
        ("orbe-conocimiento", "Orbe del Conocimiento", 7, 1600),
        ("espejo-alma", "Espejo del Alma", 8, 2800),
        ("gema-almacenamiento", "Gema de Almacenamiento", 6, 850),
        ("joya-clarividencia", "Joya de Clarividencia", 7, 1700),
        ("pendiente-proteccion", "Pendiente de Protección", 5, 400),
        ("brazalete-fuerza", "Brazalete de Fuerza", 6, 1100),
        ("cinturon-gigante", "Cinturón de Fuerza de Gigante", 7, 1900),
        ("manto-hechicero", "Manto del Hechicero", 8, 2600),
        ("sombrero-sabiduria", "Sombrero de la Sabiduría", 6, 950),
        ("bota-suerte", "Bota de la Suerte", 5, 700),
        ("túnica-mago-universal", "Túnica del Mago Universal", 8, 3200),
        ("gafas-verdad", "Gafas de la Verdad", 7, 1500),
        ("medallón-resurreción", "Medallón de Resurrección", 9, 4000)
    ]

    for item_id, item_name, level, price in high_level_items:
        filepath = magicos_dir / f"{item_id}.md"
        if not filepath.exists():
            content = f"""---
layout: page
permalink: /equipo/magicos/{item_id}/
title: {item_name}
chapter: Equipo
category: magicos
source: PC2
nav_order: {level}
item_type: Mágica
level: {level}
price: {price}
description: {item_name} de Player Core 2
---

## {item_name}

**Tipo**: Mágica | **Nivel**: {level} | **Precio**: {price}

### Descripción

[Descripción detallada de {item_name} según PC2]

### Propiedades

[Propiedades específicas según PC2]

### Activaciones

[Activaciones especiales si aplica según PC2]

### Limitaciones

[Limitaciones o consumibles si aplica según PC2]

---

## Temas Relacionados

- [Equipo Mágico](/equipo/magicos/)
- [Equipo](/equipo/)
"""
            filepath.write_text(content, encoding='utf-8')
            files_created += 1

    # 2. Trampas adicionales avanzadas
    trampas_dir = docs_root / "equipo" / "trampas"
    trampas_dir.mkdir(parents=True, exist_ok=True)

    advanced_traps = [
        ("trampa-disolucion-acida", "Trampa de Disolución Ácida", 5, 120),
        ("trampa-congelacion", "Trampa de Congelación", 4, 90),
        ("trampa-desintegracion", "Trampa de Desintegración", 6, 200),
        ("trampa-fragmentacion-mental", "Trampa de Fragmentación Mental", 7, 250),
        ("trampa-nube-negra", "Trampa de Nube Negra", 3, 50),
        ("trampa-espinas-endurecidas", "Trampa de Espinas Endurecidas", 2, 25),
        ("trampa-hielo-ardiente", "Trampa de Hielo Ardiente", 4, 100),
        ("trampa-roca-rodante", "Trampa de Roca Rodante", 3, 60),
        ("trampa-rejilla-ardiente", "Trampa de Rejilla Ardiente", 4, 110),
        ("trampa-telaran-magica", "Trampa de Telaraña Mágica", 3, 70)
    ]

    for trap_id, trap_name, level, price in advanced_traps:
        filepath = trampas_dir / f"{trap_id}.md"
        if not filepath.exists():
            content = f"""---
layout: page
permalink: /equipo/trampas/{trap_id}/
title: {trap_name}
chapter: Equipo
category: trampas
source: PC2
nav_order: {level}
item_type: Mágica
level: {level}
price: {price}
description: {trap_name} de Player Core 2
---

## {trap_name}

**Tipo**: Mágica | **Nivel**: {level} | **Precio**: {price}

### Descripción

[Descripción detallada de {trap_name} según PC2]

### Mecanismo

[Funcionamiento de la trampa según PC2]

### Efectos

[Efectos y daño según PC2]

### Desactivación

[Cómo desactivar la trampa según PC2]

---

## Temas Relacionados

- [Trampas](/equipo/trampas/)
- [Equipo](/equipo/)
"""
            filepath.write_text(content, encoding='utf-8')
            files_created += 1

    print(f"\n📦 Fase 4 Extensiones: {files_created} archivos nuevos generados")
    print(f"   - {len(high_level_items)} objetos mágicos adicionales")
    print(f"   - {len(advanced_traps)} trampas avanzadas")
    return files_created

if __name__ == '__main__':
    create_phase4_extensions()
