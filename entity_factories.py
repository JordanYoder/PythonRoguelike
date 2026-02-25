from __future__ import annotations

import copy
from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.abilities import Abilities
from entity import Actor, Item

# --- Player Template ---

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,  # Usually handled by input_handlers, but kept for factory structure
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    abilities=Abilities(), # Matches the new __init__ argument in entity.py
    image_path="resources/tiles/entities/humans/human_armor_01.png",
)

# --- Monsters ---

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(level_up_base=0),
    abilities=Abilities(),
    image_path="resources/tiles/entities/humanoids/humanoid_goblin_01.png",
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(level_up_base=0),
    abilities=Abilities(),
    image_path="resources/tiles/entities/humanoids/humanoid_troll.png",
)

# --- Items ---

health_potion = Item(
    char="!",
    color=(255, 0, 0),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
    image_path="resources/tiles/consumables/potions/potion_potion01.png",
)

lightning_scroll = Item(
    char="?",
    color=(255, 51, 51),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    image_path="resources/tiles/consumables/scrolls/consumable_scroll01.png",
)

confusion_scroll = Item(
    char="?",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
    image_path="resources/tiles/consumables/scrolls/consumable_scroll02.png",
)

fireball_scroll = Item(
    char="?",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    image_path="resources/tiles/consumables/scrolls/consumable_scroll02.png",
)

# --- Equipment ---


# Weapon entities
sword = Item(
    char=chr(584),
    color=(0, 192, 192),
    name="Sword",
    image_path="resources/tiles/equippables/swords/swords_sword01.png",
    equippable=equippable.Sword(power_bonus=0),
)

club = Item(
    char=chr(292),
    color=(255, 153, 153),
    name="Club",
    image_path="resources/tiles/equippables/clubs/clubs_club01.png",
    equippable=equippable.Club(power_bonus=0),
)

cross_bow = Item(
    char=chr(442),
    color=(255, 153, 153),
    image_path="resources/tiles/equippables/crossbows/crossbows_crossbow01.png.png",
    equippable=equippable.Crossbow(power_bonus=0),
)

dagger = Item(
    char=chr(486),
    color=(0, 192, 192),
    name="Dagger",
    image_path="resources/tiles/equippables/daggers/daggers_dagger01.png",
    equippable=equippable.Dagger(power_bonus=0),
)

halberd = Item(
    char=chr(591),
    color=(0, 192, 192),
    name="Halberd",
    image_path="resources/tiles/equippables/halberds/halberds_halberd01.png",
    equippable=equippable.Club(power_bonus=0),
)

hatchet = Item(
    char=chr(593),
    color=(128, 128, 128),
    name="Hatchet",
    image_path="resources/tiles/equippables/axes/axes_hatchet.png",
)

hunting_bow = Item(
    char=chr(491),
    color=(255, 153, 153),
    name="Hunting Bow",
    image_path="resources/tiles/equippables/bows/bows_hunterbow.png",
    equippable=equippable.HuntingBow(power_bonus=0),
)

javelin = Item(
    char=chr(437),
    color=(255, 153, 153),
    name="Javelin",
    image_path="resources/tiles/equippables/javelins/javelins_javelin.png",
    equippable=equippable.Javelin(power_bonus=0),
)

long_spear = Item(
    char=chr(437),
    color=(255, 153, 153),
    name="Long Spear",
    image_path="resources/tiles/equippables/spears/spears_longspear.png",
    equippable=equippable.LongSpear(power_bonus=0),
)

long_sword = Item(
    char=")",
    color=(0, 192, 192),
    name="Long Sword",
    image_path="resources/tiles/equippables/swords/swords_longsword01.png",
    equippable=equippable.LongSword(power_bonus=0),
)

lumber_axe = Item(
    char=chr(537),
    color=(0, 192, 192),
    name="Lumber Axe",
    image_path="resources/tiles/equippables/axes/axes_lumberaxe.png",
    equippable=equippable.LumberAxe(power_bonus=0),
)

mace = Item(
    char=chr(291),
    color=(128, 128, 128),
    name="Mace",
    image_path="resources/tiles/equippables/maces/maces_mace01.png",
    equippable=equippable.Mace(power_bonus=0),
)

poleaxe = Item(
    char=chr(447),
    color=(128, 128, 128),
    name="Poleaxe",
    image_path="resources/tiles/equippables/poleaxe/poleaxes_poleaxe01.png.png",
    equippable=equippable.PoleAxe(power_bonus=0),
)

quarterstaff = Item(
    char=chr(439),
    color=(255, 153, 153),
    name="Quarterstaff",
    image_path="resources/tiles/equippables/quarterstaff/quarterstaffs_quarterstaff01.png",
    equippable=equippable.Quarterstaff(power_bonus=0),
)

shield = Item(
    char=chr(298),
    color=(255, 153, 153),
    name="Shield",
    image_path="resources/tiles/equippables/shields/shields_shield01.png",
    equippable=equippable.Shield(power_bonus=0),
)

short_spear = Item(
    char=chr(339),
    color=(128, 128, 128),
    name="Short Spear",
    image_path="resources/tiles/equippables/spears/spears_shortspear.png",
    equippable=equippable.ShortSpear(power_bonus=0),
)

war_axe = Item(
    char=chr(541),
    color=(128, 128, 128),
    name="War Axe",
    image_path="resources/tiles/equippables/axes/axes_waraxe01.png",
    equippable=equippable.WarAxe(power_bonus=0),
)

war_bow = Item(
    char=chr(494),
    color=(255, 153, 153),
    name="War Bow",
    image_path="resources/tiles/equippables/bows/bows_warbow01.png",
    equippable=equippable.WarBow(power_bonus=0),
)

warhammer = Item(
    char=chr(540),
    color=(128, 128, 128),
    name="Warhammer",
    image_path="resources/tiles/equippables/hammers/hammers_warhammer_01.png",
    equippable=equippable.WarHammer(power_bonus=0),
)

# Armor entities
leather_armor = Item(
    char=chr(241),
    color=(255, 153, 153),
    name="Leather Armor",
    image_path="resources/tiles/equippables/armor_chest/armor_chest_leather.png",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char=chr(242),
    color=(0, 192, 192),
    name="Chain Mail",
    image_path="resources/tiles/equippables/armor_chest/armor_chest_chainmail.png",
    equippable=equippable.ChainMail()
)