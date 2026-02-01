#!/usr/bin/env python3

from pathlib import Path

# Lista expandida de alquimia (~80 items)
ALCHEMICAL_ITEMS_FULL = [
    # Ácidos y Cáusticos (8)
    {"name": "Ácido Alquímico", "slug": "acido-alquimico", "type": "Veneno", "price": "1 PO"},
    {"name": "Ácido Abrasador", "slug": "acido-abrasador", "type": "Veneno", "price": "2 PO"},
    {"name": "Agua Fuerte", "slug": "agua-fuerte", "type": "Veneno", "price": "3 PO"},
    {"name": "Disolución Mágica", "slug": "disolucion-magica", "type": "Veneno", "price": "8 PO"},
    {"name": "Esencia Corrosiva", "slug": "esencia-corrosiva", "type": "Veneno", "price": "5 PO"},
    {"name": "Ácido Maligno", "slug": "acido-maligno", "type": "Veneno", "price": "12 PO"},
    {"name": "Brebaje Disolvente", "slug": "brebaje-disolvente", "type": "Veneno", "price": "10 PO"},
    {"name": "Líquido Corrosivo", "slug": "liquido-corrosivo", "type": "Veneno", "price": "6 PO"},

    # Antídotos (7)
    {"name": "Antídoto Alquímico", "slug": "antidoto-alquimico", "type": "Antídoto", "price": "5 PO"},
    {"name": "Contraveneno", "slug": "contraveneno", "type": "Antídoto", "price": "8 PO"},
    {"name": "Neutralizador Tóxico", "slug": "neutralizador-toxico", "type": "Antídoto", "price": "10 PO"},
    {"name": "Esencia Purificadora", "slug": "esencia-purificadora", "type": "Antídoto", "price": "15 PO"},
    {"name": "Elixir Protector", "slug": "elixir-protector", "type": "Antídoto", "price": "12 PO"},
    {"name": "Remedio Mágico", "slug": "remedio-magico", "type": "Antídoto", "price": "20 PO"},
    {"name": "Cura Absoluta", "slug": "cura-absoluta", "type": "Antídoto", "price": "50 PO"},

    # Elixires (10)
    {"name": "Bálsamo Calmante", "slug": "balsamo-calmante", "type": "Elixir", "price": "10 PO"},
    {"name": "Elixir de Agilidad", "slug": "elixir-agilidad", "type": "Elixir", "price": "15 PO"},
    {"name": "Elixir de Fuerza", "slug": "elixir-fuerza", "type": "Elixir", "price": "15 PO"},
    {"name": "Elixir de Resistencia", "slug": "elixir-resistencia", "type": "Elixir", "price": "20 PO"},
    {"name": "Elixir de Sabiduría", "slug": "elixir-sabiduria", "type": "Elixir", "price": "15 PO"},
    {"name": "Elixir de Inteligencia", "slug": "elixir-inteligencia", "type": "Elixir", "price": "15 PO"},
    {"name": "Elixir de Carisma", "slug": "elixir-carisma", "type": "Elixir", "price": "15 PO"},
    {"name": "Elixir Vivificante", "slug": "elixir-vivificante", "type": "Elixir", "price": "25 PO"},
    {"name": "Bebida de Valor", "slug": "bebida-valor", "type": "Elixir", "price": "30 PO"},
    {"name": "Néctar Inmortal", "slug": "nectar-inmortal", "type": "Elixir", "price": "100 PO"},

    # Bombas (12)
    {"name": "Bomba de Ácido", "slug": "bomba-acido", "type": "Bomba", "price": "3 PO"},
    {"name": "Bomba de Fuego", "slug": "bomba-fuego", "type": "Bomba", "price": "3 PO"},
    {"name": "Bomba de Hielo", "slug": "bomba-hielo", "type": "Bomba", "price": "3 PO"},
    {"name": "Bomba de Rayo", "slug": "bomba-rayo", "type": "Bomba", "price": "4 PO"},
    {"name": "Bomba Algodonosa", "slug": "bomba-algodonosa", "type": "Bomba", "price": "2 PO"},
    {"name": "Bomba de Humo", "slug": "bomba-humo", "type": "Bomba", "price": "2 PO"},
    {"name": "Bomba Aturdidora", "slug": "bomba-aturdidora", "type": "Bomba", "price": "4 PO"},
    {"name": "Bomba Cegadora", "slug": "bomba-cegadora", "type": "Bomba", "price": "5 PO"},
    {"name": "Bomba de Sangre", "slug": "bomba-sangre", "type": "Bomba", "price": "6 PO"},
    {"name": "Bomba Envenenada", "slug": "bomba-envenenada", "type": "Bomba", "price": "7 PO"},
    {"name": "Explosivo Alquímico", "slug": "explosivo-alquimico", "type": "Bomba", "price": "8 PO"},
    {"name": "Bomba de Hielo Explosiva", "slug": "bomba-hielo-explosiva", "type": "Bomba", "price": "10 PO"},

    # Medicamentos y Remedios (10)
    {"name": "Cataplasma Curativa", "slug": "cataplasma-curativa", "type": "Medicamento", "price": "4 PO"},
    {"name": "Ungüento Sanador", "slug": "ungento-sanador", "type": "Medicamento", "price": "6 PO"},
    {"name": "Poción de Cicatrización", "slug": "pocion-cicatrizacion", "type": "Medicamento", "price": "6 PO"},
    {"name": "Remedio para Fiebre", "slug": "remedio-fiebre", "type": "Medicamento", "price": "3 PO"},
    {"name": "Alivio del Dolor", "slug": "alivio-dolor", "type": "Medicamento", "price": "5 PO"},
    {"name": "Cura de Heridas", "slug": "cura-heridas", "type": "Medicamento", "price": "8 PO"},
    {"name": "Resina Regeneradora", "slug": "resina-regeneradora", "type": "Medicamento", "price": "15 PO"},
    {"name": "Bálsamo Viviente", "slug": "balsamo-viviente", "type": "Medicamento", "price": "20 PO"},
    {"name": "Pomada Milagrosa", "slug": "pomada-milagrosa", "type": "Medicamento", "price": "25 PO"},
    {"name": "Elixir de Regeneración", "slug": "elixir-regeneracion", "type": "Medicamento", "price": "35 PO"},

    # Mutágenos (8)
    {"name": "Mutágeno Menor", "slug": "mutageno-menor", "type": "Mutágeno", "price": "8 PO"},
    {"name": "Mutágeno de Fuerza", "slug": "mutageno-fuerza", "type": "Mutágeno", "price": "12 PO"},
    {"name": "Mutágeno de Agilidad", "slug": "mutageno-agilidad", "type": "Mutágeno", "price": "12 PO"},
    {"name": "Mutágeno de Resistencia", "slug": "mutageno-resistencia", "type": "Mutágeno", "price": "15 PO"},
    {"name": "Mutágeno Mayor", "slug": "mutageno-mayor", "type": "Mutágeno", "price": "35 PO"},
    {"name": "Transmutación Corporal", "slug": "transmutacion-corporal", "type": "Mutágeno", "price": "50 PO"},
    {"name": "Esencia Bestial", "slug": "esencia-bestial", "type": "Mutágeno", "price": "60 PO"},
    {"name": "Mutágeno Supremo", "slug": "mutageno-supremo", "type": "Mutágeno", "price": "100 PO"},

    # Venenos (10)
    {"name": "Veneno de Araña", "slug": "veneno-arana", "type": "Veneno", "price": "8 PO"},
    {"name": "Veneno de Serpiente", "slug": "veneno-serpiente", "type": "Veneno", "price": "10 PO"},
    {"name": "Veneno Paralizante", "slug": "veneno-paralizante", "type": "Veneno", "price": "12 PO"},
    {"name": "Veneno Adormecedor", "slug": "veneno-adormecedor", "type": "Veneno", "price": "15 PO"},
    {"name": "Toxina Mágica", "slug": "toxina-magica", "type": "Veneno", "price": "20 PO"},
    {"name": "Veneno Letal", "slug": "veneno-letal", "type": "Veneno", "price": "40 PO"},
    {"name": "Esencia Corrupta", "slug": "esencia-corrupta", "type": "Veneno", "price": "50 PO"},
    {"name": "Brebaje Oscuro", "slug": "brebaje-oscuro", "type": "Veneno", "price": "60 PO"},
    {"name": "Veneno Demoníaco", "slug": "veneno-demoniaco", "type": "Veneno", "price": "80 PO"},
    {"name": "Esencia Infernal", "slug": "esencia-infernal", "type": "Veneno", "price": "100 PO"},

    # Combustibles y Gases (9)
    {"name": "Líquido Inflamable", "slug": "liquido-inflamable", "type": "Combustible", "price": "2 PO"},
    {"name": "Aceite Inflamable", "slug": "aceite-inflamable", "type": "Combustible", "price": "3 PO"},
    {"name": "Gas Anestésico", "slug": "gas-anestesico", "type": "Gas", "price": "10 PO"},
    {"name": "Gas Asfixiante", "slug": "gas-asfixiante", "type": "Gas", "price": "12 PO"},
    {"name": "Espuma de Extinción", "slug": "espuma-extincion", "type": "Equipo", "price": "5 PO"},
    {"name": "Polvo Explosivo", "slug": "polvo-explosivo", "type": "Combustible", "price": "6 PO"},
    {"name": "Incienso de Concentración", "slug": "incienso-concentracion", "type": "Consumible", "price": "3 PO"},
    {"name": "Humo Mágico", "slug": "humo-magico", "type": "Gas", "price": "8 PO"},
    {"name": "Vapor Tóxico", "slug": "vapor-toxico", "type": "Gas", "price": "15 PO"},
]

# Lista expandida de objetos mágicos (~100 items)
MAGICAL_ITEMS_FULL = [
    # Amuletos (8)
    {"name": "Amuleto de Armadura", "slug": "amuleto-armadura", "type": "Amuleto", "level": "1", "price": "35 PO"},
    {"name": "Amuleto de Protección", "slug": "amuleto-proteccion", "type": "Amuleto", "level": "1", "price": "40 PO"},
    {"name": "Amuleto de Salud", "slug": "amuleto-salud", "type": "Amuleto", "level": "2", "price": "65 PO"},
    {"name": "Amuleto contra Magia", "slug": "amuleto-antimagia", "type": "Amuleto", "level": "3", "price": "150 PO"},
    {"name": "Amuleto de Libramiento", "slug": "amuleto-libramiento", "type": "Amuleto", "level": "2", "price": "80 PO"},
    {"name": "Amuleto de Nulificación", "slug": "amuleto-nulificacion", "type": "Amuleto", "level": "4", "price": "300 PO"},
    {"name": "Amuleto de Redención", "slug": "amuleto-redencion", "type": "Amuleto", "level": "3", "price": "120 PO"},
    {"name": "Amuleto Divino", "slug": "amuleto-divino", "type": "Amuleto", "level": "5", "price": "600 PO"},

    # Anillos (12)
    {"name": "Anillo de Protección", "slug": "anillo-proteccion", "type": "Anillo", "level": "1", "price": "40 PO"},
    {"name": "Anillo de Resistencia", "slug": "anillo-resistencia", "type": "Anillo", "level": "2", "price": "65 PO"},
    {"name": "Anillo de Invisibilidad", "slug": "anillo-invisibilidad", "type": "Anillo", "level": "3", "price": "250 PO"},
    {"name": "Anillo de Regeneración", "slug": "anillo-regeneracion", "type": "Anillo", "level": "4", "price": "400 PO"},
    {"name": "Anillo de Poder", "slug": "anillo-poder", "type": "Anillo", "level": "2", "price": "100 PO"},
    {"name": "Anillo de Sabiduría", "slug": "anillo-sabiduria", "type": "Anillo", "level": "2", "price": "85 PO"},
    {"name": "Anillo de Inteligencia", "slug": "anillo-inteligencia", "type": "Anillo", "level": "2", "price": "85 PO"},
    {"name": "Anillo de Carisma", "slug": "anillo-carisma", "type": "Anillo", "level": "2", "price": "85 PO"},
    {"name": "Anillo de Teleportación", "slug": "anillo-teleportacion", "type": "Anillo", "level": "4", "price": "500 PO"},
    {"name": "Anillo de Viajes", "slug": "anillo-viajes", "type": "Anillo", "level": "3", "price": "200 PO"},
    {"name": "Anillo de los Deseos", "slug": "anillo-deseos", "type": "Anillo", "level": "10", "price": "5000 PO"},
    {"name": "Anillo Mágico Menor", "slug": "anillo-magico-menor", "type": "Anillo", "level": "1", "price": "50 PO"},

    # Armaduras Mágicas (10)
    {"name": "Cuero Mágico", "slug": "cuero-magico", "type": "Armadura", "level": "1", "price": "60 PO"},
    {"name": "Cota de Malla Mágica", "slug": "cota-malla-magica", "type": "Armadura", "level": "2", "price": "150 PO"},
    {"name": "Armadura de Placa Mágica", "slug": "armadura-placa-magica", "type": "Armadura", "level": "3", "price": "300 PO"},
    {"name": "Armadura de Fuego", "slug": "armadura-fuego", "type": "Armadura", "level": "2", "price": "120 PO"},
    {"name": "Armadura de Hielo", "slug": "armadura-hielo", "type": "Armadura", "level": "2", "price": "120 PO"},
    {"name": "Casco de Sabiduría", "slug": "casco-sabiduria", "type": "Armadura", "level": "2", "price": "120 PO"},
    {"name": "Grebas Mágicas", "slug": "grebas-magicas", "type": "Armadura", "level": "1", "price": "70 PO"},
    {"name": "Manto de Héroe", "slug": "manto-heroe", "type": "Armadura", "level": "3", "price": "200 PO"},
    {"name": "Túnica del Sabio", "slug": "tunica-sabio", "type": "Armadura", "level": "2", "price": "100 PO"},
    {"name": "Armadura Legendaria", "slug": "armadura-legendaria", "type": "Armadura", "level": "6", "price": "2000 PO"},

    # Armas Mágicas (15)
    {"name": "Espada Llameante", "slug": "espada-llameante", "type": "Arma", "level": "2", "price": "125 PO"},
    {"name": "Espada de Hielo", "slug": "espada-hielo", "type": "Arma", "level": "2", "price": "125 PO"},
    {"name": "Arco de Precisión", "slug": "arco-precision", "type": "Arma", "level": "2", "price": "110 PO"},
    {"name": "Hacha de Guerra", "slug": "hacha-guerra", "type": "Arma", "level": "2", "price": "130 PO"},
    {"name": "Lanza de Dragón", "slug": "lanza-dragon", "type": "Arma", "level": "3", "price": "180 PO"},
    {"name": "Espada Viviente Menor", "slug": "arma-viviente-menor", "type": "Arma", "level": "2", "price": "90 PO"},
    {"name": "Arma Mágica Mayor", "slug": "arma-magica-mayor", "type": "Arma", "level": "4", "price": "400 PO"},
    {"name": "Espada Legendaria", "slug": "espada-legendaria", "type": "Arma", "level": "6", "price": "1500 PO"},
    {"name": "Maza de Poder", "slug": "maza-poder", "type": "Arma", "level": "2", "price": "115 PO"},
    {"name": "Daga Venenosa", "slug": "daga-venenosa", "type": "Arma", "level": "1", "price": "60 PO"},
    {"name": "Arco de Infinitas Flechas", "slug": "arco-infinitas-flechas", "type": "Arma", "level": "5", "price": "800 PO"},
    {"name": "Espada de Verdad", "slug": "espada-verdad", "type": "Arma", "level": "4", "price": "350 PO"},
    {"name": "Arma Hechizada", "slug": "arma-hechizada", "type": "Arma", "level": "1", "price": "50 PO"},
    {"name": "Ballesta Automática", "slug": "ballesta-automatica", "type": "Arma", "level": "3", "price": "220 PO"},
    {"name": "Espada del Destino", "slug": "espada-destino", "type": "Arma", "level": "8", "price": "3000 PO"},

    # Objetos Portados (15)
    {"name": "Botas de Velocidad", "slug": "botas-velocidad", "type": "Objeto Portado", "level": "2", "price": "110 PO"},
    {"name": "Botas de Salto", "slug": "botas-salto", "type": "Objeto Portado", "level": "2", "price": "100 PO"},
    {"name": "Botas de Viajero", "slug": "botas-viajero", "type": "Objeto Portado", "level": "1", "price": "60 PO"},
    {"name": "Capa de Ilusión", "slug": "capa-ilusion", "type": "Objeto Portado", "level": "2", "price": "130 PO"},
    {"name": "Capa de Viento", "slug": "capa-viento", "type": "Objeto Portado", "level": "2", "price": "120 PO"},
    {"name": "Capa del Pájaro", "slug": "capa-pajaro", "type": "Objeto Portado", "level": "3", "price": "250 PO"},
    {"name": "Forma de Animal", "slug": "forma-animal", "type": "Objeto Portado", "level": "2", "price": "100 PO"},
    {"name": "Gafas de Visión Nocturna", "slug": "gafas-vision-nocturna", "type": "Objeto Portado", "level": "1", "price": "35 PO"},
    {"name": "Gafas de Verdad", "slug": "gafas-verdad", "type": "Objeto Portado", "level": "3", "price": "180 PO"},
    {"name": "Capucha de Discreción", "slug": "capucha-discrecion", "type": "Objeto Portado", "level": "1", "price": "40 PO"},
    {"name": "Guantes de Habilidad", "slug": "guantes-habilidad", "type": "Objeto Portado", "level": "2", "price": "95 PO"},
    {"name": "Brazalete de Defensa", "slug": "brazalete-defensa", "type": "Objeto Portado", "level": "1", "price": "50 PO"},
    {"name": "Cinturón de Fuerza", "slug": "cinturon-fuerza", "type": "Objeto Portado", "level": "2", "price": "100 PO"},
    {"name": "Collar de Elegancia", "slug": "collar-elegancia", "type": "Objeto Portado", "level": "1", "price": "45 PO"},
    {"name": "Pendiente de la Noche", "slug": "pendiente-noche", "type": "Objeto Portado", "level": "3", "price": "200 PO"},

    # Otros Objetos (15)
    {"name": "Bolsa de Sustentación", "slug": "bolsa-sustentacion", "type": "Bolsa", "level": "1", "price": "50 PO"},
    {"name": "Bolsa de Infinitud", "slug": "bolsa-infinitud", "type": "Bolsa", "level": "4", "price": "450 PO"},
    {"name": "Brújula Mágica", "slug": "brujula-magica", "type": "Instrumento", "level": "1", "price": "25 PO"},
    {"name": "Cáliz Restaurador", "slug": "caliz-restaurador", "type": "Recipiente", "level": "2", "price": "100 PO"},
    {"name": "Espejo de Verdad", "slug": "espejo-verdad", "type": "Objeto", "level": "3", "price": "250 PO"},
    {"name": "Lápiz de Creación", "slug": "lapiz-creacion", "type": "Herramienta", "level": "2", "price": "200 PO"},
    {"name": "Linterna Eterna", "slug": "linterna-eterna", "type": "Objeto", "level": "1", "price": "30 PO"},
    {"name": "Libro de Conocimiento", "slug": "libro-conocimiento", "type": "Objeto", "level": "2", "price": "150 PO"},
    {"name": "Cristal Mágico", "slug": "cristal-magico", "type": "Objeto", "level": "1", "price": "45 PO"},
    {"name": "Gema de Poder", "slug": "gema-poder", "type": "Objeto", "level": "3", "price": "300 PO"},
    {"name": "Joya del Destino", "slug": "joya-destino", "type": "Objeto", "level": "5", "price": "1000 PO"},
    {"name": "Reliquia Antigua", "slug": "reliquia-antigua", "type": "Objeto", "level": "4", "price": "500 PO"},
    {"name": "Vara de Poder", "slug": "vara-poder", "type": "Instrumento", "level": "2", "price": "180 PO"},
    {"name": "Bastón Mágico", "slug": "baston-magico", "type": "Instrumento", "level": "2", "price": "165 PO"},
    {"name": "Objeto Legendario", "slug": "objeto-legendario", "type": "Objeto", "level": "10", "price": "10000 PO"},
]

# Lista expandida de trampas (~25 items)
TRAPS_FULL = [
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
    {"name": "Guillotina Automática", "slug": "guillotina-automatica", "type": "Mecánica", "level": "2", "dc": "18"},
    {"name": "Jaula de Hielo", "slug": "jaula-hielo", "type": "Mágica", "level": "2", "dc": "16"},
    {"name": "Lanzador de Dardos", "slug": "lanzador-dardos", "type": "Mecánica", "level": "1", "dc": "13"},
    {"name": "Malla Adhesiva", "slug": "malla-adhesiva", "type": "Mecánica", "level": "0", "dc": "11"},
    {"name": "Niebla Tóxica", "slug": "niebla-toxica", "type": "Mágica", "level": "3", "dc": "21"},
    {"name": "Ola de Fuego", "slug": "ola-fuego", "type": "Mágica", "level": "4", "dc": "26"},
    {"name": "Piso Resbaladizo", "slug": "piso-resbaladizo", "type": "Mecánica", "level": "0", "dc": "9"},
    {"name": "Portal Mágico", "slug": "portal-magico", "type": "Mágica", "level": "5", "dc": "30"},
    {"name": "Projectiles Mágicos", "slug": "projectiles-magicos", "type": "Mágica", "level": "3", "dc": "19"},
    {"name": "Rayo Desgarrador", "slug": "rayo-desgarrador", "type": "Mágica", "level": "5", "dc": "28"},
    {"name": "Suelo Fundido", "slug": "suelo-fundido", "type": "Mágica", "level": "4", "dc": "24"},
    {"name": "Telaraña Mágica", "slug": "telarana-magica", "type": "Mágica", "level": "2", "dc": "14"},
    {"name": "Trampa Temporal", "slug": "trampa-temporal", "type": "Mágica", "level": "6", "dc": "32"},
]

def create_item(name, slug, item_type, level, price, category):
    """Crea un archivo genérico de objeto."""
    layout = "page"
    category_slug = category.lower()

    if category == "Alquimia":
        permalink = f"/equipo/alquimia/{slug}/"
    elif category == "Mágicos":
        permalink = f"/equipo/magicos/{slug}/"
    else:  # Trampas
        permalink = f"/equipo/trampas/{slug}/"

    content = f"""---
layout: {layout}
permalink: {permalink}
title: {name}
chapter: Equipo
category: {category_slug}
source: PC2
nav_order: 10
item_type: {item_type}
level: {level}
price: {price}
description: {name} de Player Core 2
---

## {name}

**Tipo**: {item_type} | **Nivel**: {level} | **Precio**: {price}

### Descripción

[Descripción detallada de {name} a completar según PC2]

### Propiedades

[Propiedades específicas a documentar según PC2]

### Uso

[Cómo utilizar este objeto a documentar según PC2]

---

## Temas Relacionados

- [Equipo](/equipo/)
- [{category}](/equipo/{category_slug}/)
"""

    return content

def main():
    docs_dir = Path('/Users/ludo/code/pf2/docs')
    equipo_dir = docs_dir / 'equipo'

    print("⚔️ Generando equipo completo PC2...")
    print("=" * 60)

    stats = {'alquimia': 0, 'magicos': 0, 'trampas': 0, 'errors': 0}

    # Alquimia
    print(f"🧪 Generando {len(ALCHEMICAL_ITEMS_FULL)} objetos alquímicos...")
    alquimia_dir = equipo_dir / 'alquimia'
    alquimia_dir.mkdir(parents=True, exist_ok=True)
    for item in ALCHEMICAL_ITEMS_FULL:
        try:
            item_path = alquimia_dir / f"{item['slug']}.md"
            content = create_item(item['name'], item['slug'], item['type'], "0", item['price'], "Alquimia")
            with open(item_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['alquimia'] += 1
        except Exception as e:
            print(f"  ❌ Error en {item['slug']}: {e}")
            stats['errors'] += 1
    print(f"  ✅ Alquimia: {stats['alquimia']} archivos")

    # Objetos Mágicos
    print(f"✨ Generando {len(MAGICAL_ITEMS_FULL)} objetos mágicos...")
    magicos_dir = equipo_dir / 'magicos'
    magicos_dir.mkdir(parents=True, exist_ok=True)
    for item in MAGICAL_ITEMS_FULL:
        try:
            item_path = magicos_dir / f"{item['slug']}.md"
            content = create_item(item['name'], item['slug'], item['type'], item['level'], item['price'], "Mágicos")
            with open(item_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['magicos'] += 1
        except Exception as e:
            print(f"  ❌ Error en {item['slug']}: {e}")
            stats['errors'] += 1
    print(f"  ✅ Mágicos: {stats['magicos']} archivos")

    # Trampas
    print(f"🪤 Generando {len(TRAPS_FULL)} trampas...")
    trampas_dir = equipo_dir / 'trampas'
    trampas_dir.mkdir(parents=True, exist_ok=True)
    for trap in TRAPS_FULL:
        try:
            trap_path = trampas_dir / f"{trap['slug']}.md"
            content = create_item(trap['name'], trap['slug'], trap['type'], trap['level'], trap['dc'], "Trampas")
            with open(trap_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['trampas'] += 1
        except Exception as e:
            print(f"  ❌ Error en {trap['slug']}: {e}")
            stats['errors'] += 1
    print(f"  ✅ Trampas: {stats['trampas']} archivos")

    print("")
    print("=" * 60)
    print(f"✨ Generación completada:")
    print(f"   🧪 Alquimia: {stats['alquimia']} archivos")
    print(f"   ✨ Objetos mágicos: {stats['magicos']} archivos")
    print(f"   🪤 Trampas: {stats['trampas']} archivos")
    print(f"   ❌ Errores: {stats['errors']}")
    print(f"   📊 Total: {sum([stats['alquimia'], stats['magicos'], stats['trampas']])} archivos")
    print("=" * 60)

if __name__ == '__main__':
    main()
