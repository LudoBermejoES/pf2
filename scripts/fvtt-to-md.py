#!/usr/bin/env python3
"""
fvtt-to-md.py — Convierte un JSON de actor FoundryVTT PF2e a una hoja de personaje Markdown.

Uso:
    python3 scripts/fvtt-to-md.py <ruta/al/actor.json>
    python3 scripts/fvtt-to-md.py <ruta/al/actor.json> --output docs/_campana/personajes/

El script detecta automáticamente si el JSON es formato FoundryVTT (tiene clave 'items')
o Pathbuilder (tiene clave 'build') y lo procesa de forma adecuada.
"""

import json
import re
import sys
import os
import argparse
from pathlib import Path

# ─── Tablas de traducción ──────────────────────────────────────────────────────

RANK_ES = {
    0: "No entrenado",
    1: "Entrenado",
    2: "Experto",
    3: "Maestro",
    4: "Legendario",
}

RANK_BONUS = {0: 0, 1: 3, 2: 5, 3: 7, 4: 9}  # nivel 1: entrenado = +3

ABILITY_ES = {
    "str": "Fuerza",
    "dex": "Destreza",
    "con": "Constitución",
    "int": "Inteligencia",
    "wis": "Sabiduría",
    "cha": "Carisma",
}

ABILITY_ABBREV_ES = {
    "str": "Fue",
    "dex": "Des",
    "con": "Con",
    "int": "Int",
    "wis": "Sab",
    "cha": "Car",
}

SKILL_ES = {
    "acrobatics": "Acrobacias",
    "arcana": "Arcanos",
    "athletics": "Atletismo",
    "crafting": "Artesanía",
    "deception": "Engaño",
    "diplomacy": "Diplomacia",
    "intimidation": "Intimidación",
    "medicine": "Medicina",
    "nature": "Naturaleza",
    "occultism": "Ocultismo",
    "performance": "Interpretación",
    "religion": "Religión",
    "society": "Sociedad",
    "stealth": "Sigilo",
    "survival": "Supervivencia",
    "thievery": "Trapacería",
}

SKILL_SLUG = {
    "acrobatics": "acrobacias",
    "arcana": "arcanos",
    "athletics": "atletismo",
    "crafting": "artesania",
    "deception": "engano",
    "diplomacy": "diplomacia",
    "intimidation": "intimidacion",
    "medicine": "medicina",
    "nature": "naturaleza",
    "occultism": "ocultismo",
    "performance": "interpretacion",
    "religion": "religion",
    "society": "sociedad",
    "stealth": "sigilo",
    "survival": "supervivencia",
    "thievery": "trapaceria",
}

TRADITION_ES = {
    "arcane": "Arcana",
    "divine": "Divina",
    "occult": "Oculta",
    "primal": "Primaria",
}

PREPARED_ES = {
    "prepared": "preparado",
    "spontaneous": "espontáneo",
    "focus": "concentración",
    "innate": "innato",
}

DAMAGE_TYPE_ES = {
    "piercing": "Perforante",
    "slashing": "Cortante",
    "bludgeoning": "Contundente",
    "fire": "Fuego",
    "cold": "Frío",
    "electricity": "Electricidad",
    "acid": "Ácido",
    "sonic": "Sónico",
    "poison": "Veneno",
    "negative": "Negativo",
    "positive": "Positivo",
    "vitality": "Vitalidad",
    "void": "Vacío",
    "spirit": "Espiritual",
    "mental": "Mental",
    "force": "Fuerza",
    "chaotic": "Caótico",
    "lawful": "Legal",
    "good": "Bueno",
    "evil": "Malvado",
}

WEAPON_CATEGORY_ES = {
    "simple": "Simple",
    "martial": "Marcial",
    "advanced": "Avanzada",
    "unarmed": "Desarmado",
}

ARMOR_CATEGORY_ES = {
    "unarmored": "Sin armadura",
    "light": "Ligera",
    "medium": "Media",
    "heavy": "Pesada",
}

FEAT_CATEGORY_ES = {
    "classfeature": "Aptitud de clase",
    "class": "Dote de clase",
    "ancestry": "Dote de ascendencia",
    "heritage": "Linaje",
    "skill": "Dote de habilidad",
    "general": "Dote general",
    "bonus": "Dote extra",
    "background": "Bagaje",
}

# ─── Funciones auxiliares ──────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Genera un slug válido para URLs a partir de un texto."""
    text = text.lower().strip()
    # Reemplazar caracteres especiales españoles
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ü": "u", "ñ": "n", "à": "a", "è": "e", "ì": "i",
        "ò": "o", "ù": "u",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def ability_modifier(score: int) -> int:
    return (score - 10) // 2


def fmt_mod(mod: int) -> str:
    return f"+{mod}" if mod >= 0 else str(mod)


def get_item_slug(name: str) -> str:
    """Genera slug de URL a partir del nombre de un objeto."""
    return slugify(name)


# ─── Índice del site (permalink lookup) ───────────────────────────────────────

def _extract_frontmatter(path: Path) -> dict:
    """Extrae el frontmatter YAML de un archivo Markdown (solo claves simples)."""
    result = {}
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return result
    if not text.startswith("---"):
        return result
    end = text.find("---", 3)
    if end == -1:
        return result
    for line in text[3:end].splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


# Mapa de traducción de nombres de armas/armaduras inglés → español
# (para cuando el JSON de FVTT no ha sido traducido por Babele)
WEAPON_NAME_EN_ES = {
    "longbow": "Arco largo",
    "shortbow": "Arco corto",
    "composite longbow": "Arco largo compuesto",
    "composite shortbow": "Arco corto compuesto",
    "dagger": "Daga",
    "shortsword": "Espada corta",
    "longsword": "Espada larga",
    "bastard sword": "Espada bastarda",
    "rapier": "Espada ropera",
    "greatsword": "Espadón",
    "handaxe": "Hacha de mano",
    "battleaxe": "Hacha de batalla",
    "greataxe": "Gran hacha",
    "spear": "Lanza",
    "lance": "Lanza de caballería",
    "greatspear": "Gran lanza",
    "halberd": "Alabarda",
    "glaive": "Guadaña",
    "staff": "Bastón",
    "club": "Cachiporra",
    "mace": "Mazo",
    "warhammer": "Martillo de guerra",
    "flail": "Flagelo",
    "crossbow": "Ballesta",
    "heavy crossbow": "Ballesta pesada",
    "hand crossbow": "Ballesta de mano",
    "sling": "Honda",
    "javelin": "Jabalina",
    "dart": "Dardo",
    "kukri": "Kukri",
    "scimitar": "Cimitarra",
    "falchion": "Alfanje",
    "pick": "Pico ligero",
    "light pick": "Pico ligero",
    "heavy pick": "Gran pico",
    "trident": "Tridente",
    "ranseur": "Roncona",
    "fist": "Puño",
    "claw": "Garra",
    "jaws": "Mandíbulas",
    "tail": "Cola",
    "horn": "Cuerno",
}

ARMOR_NAME_EN_ES = {
    "chain mail": "Cota de Malla",
    "chainmail": "Cota de Malla",
    "chain shirt": "Camisote de Malla",
    "scale mail": "Cota de Escamas",
    "leather armor": "Armadura de Cuero",
    "studded leather": "Armadura de Cuero Tachonado",
    "hide armor": "Armadura de Pieles",
    "breastplate": "Coraza",
    "half plate": "Armadura de Placas y Mallas",
    "full plate": "Armadura Completa",
    "plate armor": "Armadura Completa",
    "splint mail": "Armadura Laminada",
    "explorer's clothing": "Ropa de Explorador",
    "padded armor": "Ropa Acolchada",
    "hide armor": "Armadura de Pieles",
    "hide": "Armadura de Pieles",
}


class SiteIndex:
    """
    Construye y consulta un índice de permalinks del site Jekyll.
    Mapea: título_normalizado → permalink, para conjuros, dotes, armas y armaduras.
    """

    def __init__(self, site_root: Path):
        self.site_root = site_root
        # índices por colección: {normalizado: permalink}
        self.spells = {}
        self.feats = {}
        self.weapons = {}
        self.armors = {}
        self._build()

    def _build(self):
        self._index_dir(self.site_root / "_conjuros" / "spell-individual", self.spells)
        for subdir in (self.site_root / "_dotes").iterdir():
            if subdir.is_dir():
                self._index_dir(subdir, self.feats)
        self._index_dir(self.site_root / "_equipo" / "armas", self.weapons)
        self._index_dir(self.site_root / "_equipo" / "armaduras", self.armors)

    def _index_dir(self, directory: Path, index: dict):
        if not directory.exists():
            return
        for md_file in directory.glob("*.md"):
            fm = _extract_frontmatter(md_file)
            permalink = fm.get("permalink", "")
            title = fm.get("title", "")
            if permalink and title:
                index[_normalize(title)] = permalink

    def lookup_spell(self, name: str, slug: str = "") -> str:
        """Devuelve el permalink del conjuro o '' si no se encuentra."""
        return self._lookup(name, slug, self.spells)

    def lookup_feat(self, name: str, slug: str = "", category: str = "", class_slug: str = "") -> str:
        """Devuelve el permalink de la dote o '' si no se encuentra."""
        return self._lookup(name, slug, self.feats)

    def lookup_weapon(self, name: str, slug: str = "") -> str:
        """Devuelve el permalink del arma o '' si no se encuentra."""
        result = self._lookup(name, slug, self.weapons)
        if result:
            return result
        # Intentar con traducción inglés → español
        es_name = WEAPON_NAME_EN_ES.get(name.lower()) or WEAPON_NAME_EN_ES.get(slug.replace("-", " ").lower())
        if es_name:
            return self._lookup(es_name, "", self.weapons)
        return ""

    def lookup_armor(self, name: str, slug: str = "") -> str:
        """Devuelve el permalink de la armadura o '' si no se encuentra."""
        result = self._lookup(name, slug, self.armors)
        if result:
            return result
        # Intentar con traducción inglés → español
        es_name = ARMOR_NAME_EN_ES.get(name.lower()) or ARMOR_NAME_EN_ES.get(slug.replace("-", " ").lower())
        if es_name:
            return self._lookup(es_name, "", self.armors)
        return ""

    def _lookup(self, name: str, slug: str, index: dict) -> str:
        # 1. Por nombre exacto normalizado
        key = _normalize(name)
        if key in index:
            return index[key]
        # 2. Por slug inglés normalizado (por si el title del site usa el mismo texto)
        if slug:
            key2 = _normalize(slug.replace("-", " "))
            if key2 in index:
                return index[key2]
        # 3. Búsqueda parcial (el nombre del JSON contiene el del site o viceversa)
        for site_title, permalink in index.items():
            if key and (key in site_title or site_title in key):
                return permalink
        return ""


def _normalize(text: str) -> str:
    """Normaliza un string para comparación: minúsculas, sin acentos, sin puntuación."""
    text = text.lower().strip()
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ü": "u", "ñ": "n", "à": "a", "è": "e", "ì": "i",
        "ò": "o", "ù": "u", "'": "", "'": "", "\u2019": "",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Instancia global del índice (se inicializa en main())
_site_index = None  # type: SiteIndex


def get_site_index():
    global _site_index
    if _site_index is None:
        # Intentar localizar el site_root relativo al script
        script_dir = Path(__file__).parent
        site_root = script_dir.parent / "docs"
        if not site_root.exists():
            site_root = Path("docs")
        _site_index = SiteIndex(site_root)
    return _site_index


# ─── Parseo de formato FoundryVTT ──────────────────────────────────────────────

class FVTTCharacter:
    def __init__(self, data: dict):
        self.data = data
        self.name = data.get("name", "Personaje")
        self.system = data.get("system", {})
        self.items = data.get("items", [])
        self._parse()

    def _parse(self):
        sys = self.system
        details = sys.get("details", {})

        self.level = details.get("level", {}).get("value", 1)
        self.gender = details.get("gender", {}).get("value", "")
        self.age = details.get("age", {}).get("value", "")
        self.ethnicity = details.get("ethnicity", {}).get("value", "")
        self.nationality = details.get("nationality", {}).get("value", "")
        self.deity_name = details.get("deity", {}).get("value", "")
        self.hp = sys.get("attributes", {}).get("hp", {}).get("value", 0)
        self.size = sys.get("traits", {}).get("size", {}).get("value", "med")
        self.key_ability = details.get("keyability", {}).get("value", "")

        # Habilidades — en FVTT no hay atributos precalculados, se derivan de boosts
        self.abilities = self._compute_abilities()

        # Habilidades
        self.skills = sys.get("skills", {})

        # Salvaciones (ranks)
        self.saving_throws = sys.get("savingThrows", {})

        # Competencias en armaduras/armas
        self.martial = sys.get("martial", {})

        # Items clasificados por tipo
        self._classify_items()

    def _compute_abilities(self) -> dict:
        """
        Calcula puntuaciones de atributos a partir de los boosts en system.build.attributes.boosts
        y los boosts de ancestría e items. Todos los personajes nuevos empiezan en 10.
        """
        scores = {"str": 10, "dex": 10, "con": 10, "int": 10, "wis": 10, "cha": 10}

        # Flaws de ancestría (si los hay)
        ancestry = next((i for i in self.items if i.get("type") == "ancestry"), None)
        if ancestry:
            flaws = ancestry.get("system", {}).get("flaws", {})
            for flaw_key in flaws.values():
                for stat in flaw_key.get("value", []):
                    if flaw_key.get("selected") and flaw_key["selected"] == stat:
                        scores[stat] = max(8, scores[stat] - 2)
                if flaw_key.get("selected"):
                    scores[flaw_key["selected"]] = max(8, scores[flaw_key["selected"]] - 2)

        # Boosts de ancestría
        if ancestry:
            boosts = ancestry.get("system", {}).get("boosts", {})
            # Puede ser alternateAncestryBoosts
            alt_boosts = ancestry.get("system", {}).get("alternateAncestryBoosts", [])
            if alt_boosts:
                for stat in alt_boosts:
                    scores[stat] = _apply_boost(scores[stat])
            else:
                for b in boosts.values():
                    sel = b.get("selected")
                    if sel:
                        scores[sel] = _apply_boost(scores[sel])

        # Boosts de bagaje
        background = next((i for i in self.items if i.get("type") == "background"), None)
        if background:
            boosts = background.get("system", {}).get("boosts", {})
            for b in boosts.values():
                sel = b.get("selected")
                if sel:
                    scores[sel] = _apply_boost(scores[sel])

        # Boosts de clase (key ability)
        class_item = next((i for i in self.items if i.get("type") == "class"), None)
        if class_item:
            key = class_item.get("system", {}).get("keyAbility", {}).get("selected")
            if key:
                scores[key] = _apply_boost(scores[key])

        # Boosts de nivel 1 (system.build.attributes.boosts)
        build_boosts = self.system.get("build", {}).get("attributes", {}).get("boosts", {})
        level_boosts = build_boosts.get("1", [])
        for stat in level_boosts:
            scores[stat] = _apply_boost(scores[stat])

        return scores

    def _classify_items(self):
        self.ancestry_item = None
        self.heritage_item = None
        self.class_item = None
        self.background_item = None
        self.feats = []
        self.weapons = []
        self.armor = None
        self.spellcasting_entries = []
        self.spells = []
        self.equipment = []
        self.lore_skills = []
        self.money = {}

        for item in self.items:
            t = item.get("type", "")
            if t == "ancestry":
                self.ancestry_item = item
            elif t == "heritage":
                self.heritage_item = item
            elif t == "class":
                self.class_item = item
            elif t == "background":
                self.background_item = item
            elif t == "feat":
                self.feats.append(item)
            elif t == "weapon":
                self.weapons.append(item)
            elif t == "armor":
                self.armor = item
            elif t == "spellcastingEntry":
                self.spellcasting_entries.append(item)
            elif t == "spell":
                self.spells.append(item)
            elif t == "lore":
                self.lore_skills.append(item)
            elif t in ("equipment", "backpack", "consumable", "tool", "kit"):
                self.equipment.append(item)
            elif t == "treasure":
                slug = item.get("system", {}).get("slug", "")
                qty = item.get("system", {}).get("quantity", 0)
                self.money[slug] = qty

    # ── Getters de datos clave ─────────────────────────────────────────────────

    @property
    def ancestry_name(self) -> str:
        return self.ancestry_item.get("name", "") if self.ancestry_item else ""

    @property
    def heritage_name(self) -> str:
        return self.heritage_item.get("name", "") if self.heritage_item else ""

    @property
    def class_name(self) -> str:
        return self.class_item.get("name", "") if self.class_item else ""

    @property
    def background_name(self) -> str:
        return self.background_item.get("name", "") if self.background_item else ""

    @property
    def perception_rank(self) -> int:
        """Rango de percepción desde el item de clase."""
        if self.class_item:
            return self.class_item.get("system", {}).get("perception", 1)
        return 1

    @property
    def speed(self) -> int:
        if self.ancestry_item:
            feet = self.ancestry_item.get("system", {}).get("speed", 25)
            return feet
        return 25

    def ability_score(self, key: str) -> int:
        return self.abilities.get(key, 10)

    def ability_mod(self, key: str) -> int:
        return ability_modifier(self.ability_score(key))

    def skill_rank(self, skill: str) -> int:
        return self.skills.get(skill, {}).get("rank", 0)

    def skill_total(self, skill: str) -> int:
        """Calcula el total de habilidad a nivel 1 (solo rank + ability mod + level si entrenado)."""
        rank = self.skill_rank(skill)
        prof_bonus = RANK_BONUS.get(rank, 0)
        if rank > 0:
            level_bonus = self.level
        else:
            level_bonus = 0
        # La habilidad clave de cada skill
        skill_ability = SKILL_ABILITY.get(skill, "int")
        mod = self.ability_mod(skill_ability)
        return mod + prof_bonus + level_bonus if rank > 0 else mod  # Sin entrenamiento no suma level ni prof en PF2e

    def save_rank(self, save: str) -> int:
        return self.saving_throws.get(save, 0)

    def save_total(self, save: str, ability: str) -> int:
        rank = self.save_rank(save)
        prof_bonus = RANK_BONUS.get(rank, 0)
        level_bonus = self.level if rank > 0 else 0
        return self.ability_mod(ability) + prof_bonus + level_bonus

    def perception_total(self) -> int:
        rank = self.perception_rank
        prof_bonus = RANK_BONUS.get(rank, 0)
        level_bonus = self.level if rank > 0 else 0
        return self.ability_mod("wis") + prof_bonus + level_bonus

    def spell_dc(self, ability: str) -> int:
        """CD de conjuro: 10 + nivel + mod + competencia entrenada (rank 1)."""
        return 10 + self.level + self.ability_mod(ability) + RANK_BONUS.get(1, 3)

    def spell_attack(self, ability: str) -> int:
        return self.level + self.ability_mod(ability) + RANK_BONUS.get(1, 3)

    def class_dc(self) -> int:
        key = self.key_ability or "str"
        return 10 + self.level + self.ability_mod(key) + RANK_BONUS.get(1, 3)

    def ac(self) -> int:
        """CA básica con armadura."""
        if self.armor:
            ac_bonus = self.armor.get("system", {}).get("acBonus", 0)
            dex_cap = self.armor.get("system", {}).get("dexCap", 99)
            dex_applied = min(self.ability_mod("dex"), dex_cap)
            armor_rank = self.martial.get(self.armor.get("system", {}).get("category", "medium"), {}).get("rank", 0)
            prof_bonus = RANK_BONUS.get(armor_rank, 0)
            level_bonus = self.level if armor_rank > 0 else 0
            return 10 + ac_bonus + dex_applied + prof_bonus + level_bonus
        else:
            unarmored_rank = self.martial.get("unarmored", {}).get("rank", 0)
            prof_bonus = RANK_BONUS.get(unarmored_rank, 0)
            level_bonus = self.level if unarmored_rank > 0 else 0
            return 10 + self.ability_mod("dex") + prof_bonus + level_bonus

    def weapon_attack(self, weapon: dict) -> int:
        """Ataque con arma (no incluye runas)."""
        cat = weapon.get("system", {}).get("category", "simple")
        rank_key = cat if cat in ("simple", "martial", "advanced", "unarmed") else "simple"
        rank = self.martial.get(rank_key, {}).get("rank", 0)
        traits = weapon.get("system", {}).get("traits", {}).get("value", [])
        # Finesse usa Destreza si es mayor
        if "finesse" in traits:
            stat_mod = max(self.ability_mod("str"), self.ability_mod("dex"))
        elif weapon.get("system", {}).get("range"):
            stat_mod = self.ability_mod("dex")
        else:
            stat_mod = self.ability_mod("str")
        prof_bonus = RANK_BONUS.get(rank, 0)
        level_bonus = self.level if rank > 0 else 0
        return stat_mod + prof_bonus + level_bonus

    def get_spells_by_entry(self) -> list:
        """Devuelve lista de (entrada, [conjuros]) agrupados por spellcastingEntry."""
        result = []
        for entry in self.spellcasting_entries:
            entry_id = entry.get("_id")
            entry_spells = [s for s in self.spells if s.get("system", {}).get("location", {}).get("value") == entry_id]
            result.append((entry, entry_spells))
        return result

    def get_prepared_spell_names(self, entry: dict, slot: str) -> list:
        """Devuelve los IDs de conjuros preparados en un slot."""
        slots = entry.get("system", {}).get("slots", {})
        slot_data = slots.get(slot, {})
        prepared = slot_data.get("prepared", {})
        if isinstance(prepared, list):
            return []
        return [v.get("id") for v in prepared.values() if isinstance(v, dict) and "id" in v]

    def get_money(self) -> dict:
        """Devuelve dinero como {pp, po, pp, pc}."""
        return {
            "pp": self.money.get("platinum-pieces", 0),
            "po": self.money.get("gold-pieces", 0),
            "pp_plata": self.money.get("silver-pieces", 0),
            "pc": self.money.get("copper-pieces", 0),
        }

    def get_ancestry_hp(self) -> int:
        if self.ancestry_item:
            return self.ancestry_item.get("system", {}).get("hp", 0)
        return 0

    def get_class_hp(self) -> int:
        if self.class_item:
            return self.class_item.get("system", {}).get("hp", 0)
        return 0


# ─── Funciones de apoyo fuera de la clase ─────────────────────────────────────

SKILL_ABILITY = {
    "acrobatics": "dex",
    "arcana": "int",
    "athletics": "str",
    "crafting": "int",
    "deception": "cha",
    "diplomacy": "cha",
    "intimidation": "cha",
    "medicine": "wis",
    "nature": "wis",
    "occultism": "int",
    "performance": "cha",
    "religion": "wis",
    "society": "int",
    "stealth": "dex",
    "survival": "wis",
    "thievery": "dex",
}


def _apply_boost(score: int) -> int:
    """PF2e: boosts incrementan de 2 en 2 hasta 18, de 1 en 1 a partir de ahí."""
    if score < 18:
        return score + 2
    return score + 1


def feet_to_meters(feet: int) -> str:
    """Convierte pies a metros usando la convención PF2e (5ft = 1.5m)."""
    # PF2e usa múltiplos de 5 pies / 1.5 metros
    meters_exact = feet * 0.3
    # Redondear al 0.5 más cercano para mostrar bien
    meters_half = round(meters_exact * 2) / 2
    if meters_half == int(meters_half):
        return f"{int(meters_half)} metros ({feet} pies)"
    # Usar coma decimal (estilo español)
    meters_str = f"{meters_half:.1f}".replace(".", ",")
    return f"{meters_str} metros ({feet} pies)"


# ─── Generador de Markdown ─────────────────────────────────────────────────────

def generate_markdown(char: FVTTCharacter) -> str:
    lines = []
    idx = get_site_index()

    slug = slugify(char.name)
    ancestry_slug = slugify(char.ancestry_name)
    class_slug = slugify(char.class_name)
    background_slug = slugify(char.background_name)

    # Ruta de clase: buscar en el índice del site, o usar /clases/SLUG/
    # Las clases usan el nombre del item de clase (puede tener subtipos como "Guerrero (Atletismo)")
    # Extraer slug base de la clase (sin el paréntesis)
    class_base_slug = re.sub(r"\s*\(.*\)", "", char.class_name).strip()
    class_base_slug = slugify(class_base_slug)

    # ── Frontmatter ──────────────────────────────────────────────────────────
    lines += [
        "---",
        "layout: page",
        f"permalink: /campana/personajes/{slug}/",
        f"title: {char.name}",
        "chapter: Campaña",
        "category: campana",
        "source: Kingmaker",
        "---",
        "",
        f"# {char.name}",
        "",
    ]

    # Subtítulo breve
    subtitle_parts = []
    if char.class_name:
        subtitle_parts.append(f"**[{char.class_name}](/clases/{class_base_slug}/)** nivel {char.level}")
    if char.deity_name:
        subtitle_parts.append(f"de {char.deity_name}")
    if subtitle_parts:
        lines.append(" ".join(subtitle_parts))
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── Datos básicos ────────────────────────────────────────────────────────
    lines.append("## Datos básicos")
    lines.append("")
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append(f"| **Nombre** | {char.name} |")
    if char.class_name:
        lines.append(f"| **Clase** | [{char.class_name}](/clases/{class_base_slug}/) |")
    lines.append(f"| **Nivel** | {char.level} |")
    if char.ancestry_name:
        lines.append(f"| **Ascendencia** | [{char.ancestry_name}](/ascendencias/{ancestry_slug}/) |")
    if char.heritage_name:
        lines.append(f"| **Linaje** | {char.heritage_name} |")
    if char.background_name:
        lines.append(f"| **Bagaje** | {char.background_name} |")
    if char.deity_name:
        lines.append(f"| **Deidad** | {char.deity_name} |")
    if char.gender:
        lines.append(f"| **Género** | {char.gender} |")
    if char.age:
        lines.append(f"| **Edad** | {char.age} |")
    if char.ethnicity:
        lines.append(f"| **Etnia** | {char.ethnicity} |")
    if char.nationality:
        lines.append(f"| **Nacionalidad** | {char.nationality} |")

    size_map = {"sm": "Pequeño", "med": "Mediano", "lg": "Grande", "huge": "Enorme", "grg": "Gigantesco"}
    lines.append(f"| **Tamaño** | {size_map.get(char.size, 'Mediano')} |")
    speed_feet = char.speed
    lines.append(f"| **Velocidad** | {feet_to_meters(speed_feet)} |")

    # Atributo clave
    if char.key_ability:
        lines.append(f"| **Atributo clave** | {ABILITY_ES.get(char.key_ability, char.key_ability)} |")

    # PG
    anc_hp = char.get_ancestry_hp()
    cls_hp = char.get_class_hp()
    con_mod = char.ability_mod("con")
    total_hp = anc_hp + cls_hp + con_mod
    hp_parts = []
    if anc_hp:
        hp_parts.append(f"{anc_hp} ascendencia")
    if cls_hp:
        hp_parts.append(f"{cls_hp} clase")
    if con_mod != 0:
        hp_parts.append(f"{con_mod:+d} Con")
    lines.append(f"| **Puntos de Golpe** | {total_hp} ({' + '.join(hp_parts)}) |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Atributos ────────────────────────────────────────────────────────────
    lines.append("## Atributos")
    lines.append("")
    lines.append("| Atributo | Puntuación | Modificador |")
    lines.append("|----------|:----------:|:-----------:|")
    for key in ("str", "dex", "con", "int", "wis", "cha"):
        score = char.ability_score(key)
        mod = ability_modifier(score)
        lines.append(f"| **{ABILITY_ES[key]}** | {score} | {fmt_mod(mod)} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Defensas ─────────────────────────────────────────────────────────────
    lines.append("## Defensas")
    lines.append("")
    lines.append("| Defensa | Total | Desglose |")
    lines.append("|---------|:-----:|----------|")

    ca = char.ac()
    if char.armor:
        ac_bonus = char.armor.get("system", {}).get("acBonus", 0)
        dex_cap = char.armor.get("system", {}).get("dexCap", 99)
        dex_applied = min(char.ability_mod("dex"), dex_cap)
        armor_rank = char.martial.get(char.armor.get("system", {}).get("category", "medium"), {}).get("rank", 0)
        prof_bonus = RANK_BONUS.get(armor_rank, 0)
        parts = ["10", f"{ac_bonus} (armadura)"]
        if dex_applied != 0:
            parts.append(f"{dex_applied:+d} (Des)".lstrip("+"))
            parts[-1] = f"{dex_applied} (Des)"
        if prof_bonus:
            parts.append(f"{prof_bonus} (competencia)")
        lines.append(f"| **CA** | **{ca}** | {' + '.join(parts)} |")
    else:
        dex_mod = char.ability_mod("dex")
        unarmored_rank = char.martial.get("unarmored", {}).get("rank", 0)
        prof_bonus = RANK_BONUS.get(unarmored_rank, 0)
        lines.append(f"| **CA** | **{ca}** | 10 + {fmt_mod(dex_mod)} (Des) + {prof_bonus} (competencia) |")

    fort_total = char.save_total("fortitude", "con")
    ref_total = char.save_total("reflex", "dex")
    will_total = char.save_total("will", "wis")
    perc_total = char.perception_total()

    fort_rank = RANK_ES.get(char.save_rank("fortitude"), "Entrenado")
    ref_rank = RANK_ES.get(char.save_rank("reflex"), "Entrenado")
    will_rank = RANK_ES.get(char.save_rank("will"), "Experto")
    perc_rank = RANK_ES.get(char.perception_rank, "Experto")

    con_mod = char.ability_mod("con")
    dex_mod = char.ability_mod("dex")
    wis_mod = char.ability_mod("wis")

    lines.append(f"| **Fortaleza** | {fmt_mod(fort_total)} | {fmt_mod(con_mod)} (Con) + {RANK_BONUS[char.save_rank('fortitude')]} ({fort_rank.lower()}) |")
    lines.append(f"| **Reflejos** | {fmt_mod(ref_total)} | {fmt_mod(dex_mod)} (Des) + {RANK_BONUS[char.save_rank('reflex')]} ({ref_rank.lower()}) |")
    lines.append(f"| **Voluntad** | {fmt_mod(will_total)} | {fmt_mod(wis_mod)} (Sab) + {RANK_BONUS[char.save_rank('will')]} ({will_rank.lower()}) |")
    lines.append(f"| **Percepción** | {fmt_mod(perc_total)} | {fmt_mod(wis_mod)} (Sab) + {RANK_BONUS[char.perception_rank]} ({perc_rank.lower()}) |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Competencias ──────────────────────────────────────────────────────────
    lines.append("## Competencias")
    lines.append("")

    # Armaduras
    lines.append("### Armaduras y armas")
    lines.append("")
    lines.append("| Categoría | Rango |")
    lines.append("|-----------|-------|")
    armor_cats = [
        ("unarmored", "Sin armadura"),
        ("light", "Armadura ligera"),
        ("medium", "Armadura media"),
        ("heavy", "Armadura pesada"),
        ("simple", "Armas simples"),
        ("martial", "Armas marciales"),
        ("advanced", "Armas avanzadas"),
        ("unarmed", "Desarmado"),
    ]
    for key, label in armor_cats:
        rank = char.martial.get(key, {}).get("rank", 0)
        if rank > 0:
            lines.append(f"| {label} | {RANK_ES[rank]} |")

    lines.append("")

    # Habilidades
    lines.append("### Habilidades")
    lines.append("")
    lines.append("| Habilidad | Rango | Modificador total |")
    lines.append("|-----------|-------|:-----------------:|")

    for skill_key, skill_name in SKILL_ES.items():
        rank = char.skill_rank(skill_key)
        if rank > 0:
            total = char.skill_total(skill_key)
            slug_url = SKILL_SLUG.get(skill_key, slugify(skill_name))
            lines.append(f"| [{skill_name}](/habilidades/{slug_url}/) | {RANK_ES[rank]} | {fmt_mod(total)} |")

    # Saberes (lore skills)
    for lore in char.lore_skills:
        lore_name = lore.get("name", "Saber")
        lore_rank = lore.get("system", {}).get("proficient", {}).get("value", 1)
        lore_total = char.level + RANK_BONUS.get(lore_rank, 3) + char.ability_mod("int")
        lines.append(f"| Saber ({lore_name}) | {RANK_ES.get(lore_rank, 'Entrenado')} | {fmt_mod(lore_total)} |")

    # CD de clase
    class_dc = char.class_dc()
    key_abbrev = ABILITY_ABBREV_ES.get(char.key_ability, "Atr")
    key_mod = char.ability_mod(char.key_ability) if char.key_ability else 0
    lines.append("")
    lines.append(f"| CD de clase | **{class_dc}** (10 + {fmt_mod(key_mod)} {key_abbrev} + {RANK_BONUS[1]} entrenado) |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Dotes y aptitudes ─────────────────────────────────────────────────────
    lines.append("## Dotes y aptitudes especiales")
    lines.append("")
    lines.append("### Dotes")
    lines.append("")
    lines.append("| Dote | Tipo | Nivel |")
    lines.append("|------|------|:-----:|")

    # Clasificar dotes: excluir duplicados con mismo slug
    seen_feat_slugs = set()
    for feat in sorted(char.feats, key=lambda f: (f.get("system", {}).get("level", {}).get("value", 1), f.get("name", ""))):
        fname = feat.get("name", "")
        fcat = feat.get("system", {}).get("category", "")
        flevel = feat.get("system", {}).get("level", {}).get("value", 1)
        fslug = feat.get("system", {}).get("slug", "")

        # Evitar duplicados exactos
        dedup_key = (fslug or slugify(fname), fcat)
        if dedup_key in seen_feat_slugs:
            continue
        seen_feat_slugs.add(dedup_key)

        cat_label = FEAT_CATEGORY_ES.get(fcat, fcat)

        # Intentar enlazar dotes (no aptitudes de clase que no tienen página propia)
        if fcat in ("skill", "general", "class", "ancestry"):
            permalink = idx.lookup_feat(fname, fslug)
            if permalink:
                feat_link = f"[{fname}]({permalink})"
            else:
                feat_link = fname
        else:
            feat_link = fname

        lines.append(f"| {feat_link} | {cat_label} | {flevel} |")

    lines.append("")

    # Aptitudes especiales (classfeatures notables)
    class_features = [f for f in char.feats if f.get("system", {}).get("category") == "classfeature"]
    if class_features:
        lines.append("### Aptitudes especiales")
        lines.append("")
        # Deduplicar por slug
        seen_cf = set()
        for cf in class_features:
            slug_cf = cf.get("system", {}).get("slug", "") or slugify(cf.get("name", ""))
            if slug_cf in seen_cf:
                continue
            seen_cf.add(slug_cf)
            fname = cf.get("name", "")
            lines.append(f"- **{fname}**")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Armas ────────────────────────────────────────────────────────────────
    if char.weapons:
        lines.append("## Armas")
        lines.append("")
        lines.append("| Arma | Tipo | Ataque | Daño | Tipo de daño |")
        lines.append("|------|------|:------:|------|:------------:|")

        for weapon in char.weapons:
            wname = weapon.get("name", "")
            wcat = weapon.get("system", {}).get("category", "simple")
            wdice = weapon.get("system", {}).get("damage", {}).get("dice", 1)
            wdie = weapon.get("system", {}).get("damage", {}).get("die", "d4")
            wdtype = weapon.get("system", {}).get("damage", {}).get("damageType", "")
            wslug = weapon.get("system", {}).get("slug", "") or weapon.get("system", {}).get("baseItem", "")
            attack_bonus = char.weapon_attack(weapon)
            cat_label = WEAPON_CATEGORY_ES.get(wcat, wcat)
            dtype_es = DAMAGE_TYPE_ES.get(wdtype, wdtype.capitalize())
            permalink = idx.lookup_weapon(wname, wslug)
            # Si el nombre está en inglés, usar la traducción española si existe
            display_name = WEAPON_NAME_EN_ES.get(wname.lower(), wname)
            if permalink:
                wlink = f"[{display_name}]({permalink})"
            else:
                wlink = display_name
            lines.append(f"| {wlink} | {cat_label} | {fmt_mod(attack_bonus)} | {wdice}{wdie} | {dtype_es} |")

        lines.append("")
        lines.append("---")
        lines.append("")

    # ── Armadura ─────────────────────────────────────────────────────────────
    if char.armor:
        lines.append("## Armadura")
        lines.append("")
        lines.append("| Armadura | Tipo | Bonificador a CA |")
        lines.append("|----------|------|:----------------:|")

        aname = char.armor.get("name", "")
        acat = char.armor.get("system", {}).get("category", "medium")
        ac_bonus = char.armor.get("system", {}).get("acBonus", 0)
        aslug = char.armor.get("system", {}).get("slug", "") or char.armor.get("system", {}).get("baseItem", "")
        acat_es = ARMOR_CATEGORY_ES.get(acat, acat)
        permalink = idx.lookup_armor(aname, aslug)
        display_name = ARMOR_NAME_EN_ES.get(aname.lower(), aname)
        if permalink:
            alink = f"[{display_name}]({permalink})"
        else:
            alink = display_name
        lines.append(f"| {alink} | {acat_es} | +{ac_bonus} |")

        lines.append("")
        lines.append("---")
        lines.append("")

    # ── Conjuros ──────────────────────────────────────────────────────────────
    spell_entries = char.get_spells_by_entry()
    if spell_entries:
        for entry, entry_spells in spell_entries:
            entry_name = entry.get("name", "")
            tradition = entry.get("system", {}).get("tradition", {}).get("value", "")
            ability = entry.get("system", {}).get("ability", {}).get("value", "wis")
            prepared_type = entry.get("system", {}).get("prepared", {}).get("value", "prepared")
            tradition_es = TRADITION_ES.get(tradition, tradition.capitalize())
            prepared_es = PREPARED_ES.get(prepared_type, prepared_type)

            lines.append(f"## Conjuros — {entry_name} ({tradition_es}, {prepared_es})")
            lines.append("")

            spell_dc = char.spell_dc(ability)
            spell_atk = char.spell_attack(ability)
            ability_abbrev = ABILITY_ABBREV_ES.get(ability, "Sab")
            ability_mod_val = char.ability_mod(ability)

            lines.append(f"**CD de conjuro:** {spell_dc} (10 + {ability_mod_val} {ability_abbrev} + {RANK_BONUS[1]} entrenado)  ")
            lines.append(f"**Modificador de ataque de conjuro:** {fmt_mod(spell_atk)}")
            lines.append("")

            # Agrupar conjuros por nivel
            spells_by_level: dict[int, list] = {}
            for spell in entry_spells:
                slevel = spell.get("system", {}).get("level", {}).get("value", 0)
                is_cantrip = "cantrip" in spell.get("system", {}).get("traits", {}).get("value", [])
                key = 0 if is_cantrip else slevel
                spells_by_level.setdefault(key, []).append(spell)

            # Slots disponibles
            slots_data = entry.get("system", {}).get("slots", {})

            def spell_link(spell: dict) -> str:
                sname = spell.get("name", "")
                sslug = spell.get("system", {}).get("slug", "")
                permalink = idx.lookup_spell(sname, sslug)
                if permalink:
                    return f"[{sname}]({permalink})"
                return sname

            # Nivel 0 (trucos)
            if 0 in spells_by_level:
                lines.append("### Trucos (rango 0) — ilimitados")
                lines.append("")
                seen_spells: set[str] = set()
                for spell in spells_by_level[0]:
                    sname = spell.get("name", "")
                    if sname in seen_spells:
                        continue
                    seen_spells.add(sname)
                    lines.append(f"- {spell_link(spell)}")
                lines.append("")

            # Rangos 1+
            for slot_num in range(1, 12):
                slot_key = f"slot{slot_num}"
                slot_info = slots_data.get(slot_key, {})
                max_slots = slot_info.get("max", 0)
                if max_slots == 0:
                    continue

                lines.append(f"### Rango {slot_num} — {max_slots} casillas/día")
                lines.append("")

                if prepared_type == "prepared":
                    # Para clérigos preparados, listar los conjuros preparados
                    prepared_ids = char.get_prepared_spell_names(entry, slot_key)
                    seen_spells = set()
                    for spell_id in prepared_ids:
                        spell = next((s for s in entry_spells if s.get("_id") == spell_id), None)
                        if not spell:
                            spell = next((s for s in char.spells if s.get("_id") == spell_id), None)
                        if spell:
                            sname = spell.get("name", "")
                            if sname in seen_spells:
                                continue
                            seen_spells.add(sname)
                            lines.append(f"- {spell_link(spell)}")
                else:
                    # Espontáneo: listar los del nivel
                    if slot_num in spells_by_level:
                        seen_spells = set()
                        for spell in spells_by_level[slot_num]:
                            sname = spell.get("name", "")
                            if sname in seen_spells:
                                continue
                            seen_spells.add(sname)
                            lines.append(f"- {spell_link(spell)}")
                lines.append("")

        lines.append("---")
        lines.append("")

    # ── Equipo ───────────────────────────────────────────────────────────────
    worn = []
    stowed = []
    for item in char.equipment:
        iname = item.get("name", "")
        qty = item.get("system", {}).get("quantity", 1)
        carry = item.get("system", {}).get("equipped", {}).get("carryType", "stowed")
        display = f"{iname}" if qty == 1 else f"{iname} (×{qty})"
        if carry in ("worn", "held"):
            worn.append(display)
        else:
            stowed.append(display)

    if worn or stowed:
        lines.append("## Equipo")
        lines.append("")
        if worn:
            lines.append("### Llevado encima")
            for item in worn:
                lines.append(f"- {item}")
            lines.append("")
        if stowed:
            lines.append("### En la mochila")
            for item in stowed:
                lines.append(f"- {item}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # ── Dinero ───────────────────────────────────────────────────────────────
    money = char.get_money()
    if any(v > 0 for v in money.values()):
        lines.append("## Dinero")
        lines.append("")
        lines.append("| pc | pp | po | ppl |")
        lines.append("|:--:|:--:|:--:|:---:|")
        lines.append(f"| {money['pc']} | {money['pp_plata']} | {money['po']} | {money['pp']} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # ── Notas de juego ────────────────────────────────────────────────────────
    lines.append("## Notas de juego")
    lines.append("")
    lines.append(f"{char.name} es un(a) **{char.class_name}** de nivel {char.level}.")
    if char.background_name:
        lines.append(f"Su bagaje es **{char.background_name}**.")
    lines.append("")
    lines.append(f"→ [Ejemplos de juego: cómo jugar a {char.name}](/campana/personajes/ejemplos/{slug}/)")
    lines.append("")

    return "\n".join(lines)


# ─── Entrada principal ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convierte un JSON de FoundryVTT PF2e a hoja de personaje Markdown."
    )
    parser.add_argument("input", help="Ruta al archivo JSON del actor")
    parser.add_argument(
        "--output", "-o",
        default="docs/_campana/personajes/",
        help="Directorio de salida (por defecto: docs/_campana/personajes/)"
    )
    parser.add_argument(
        "--stdout", action="store_true",
        help="Imprimir a stdout en lugar de guardar a archivo"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: no se encuentra el archivo {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    # Detectar formato
    if "build" in data and "success" in data:
        print("Formato Pathbuilder detectado. (No implementado aún en este script)", file=sys.stderr)
        sys.exit(1)
    elif "items" in data and "system" in data:
        char = FVTTCharacter(data)
    else:
        print("Formato JSON desconocido.", file=sys.stderr)
        sys.exit(1)

    md_content = generate_markdown(char)

    if args.stdout:
        print(md_content)
        return

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(char.name)
    output_file = output_dir / f"{slug}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Generado: {output_file}")


if __name__ == "__main__":
    main()
