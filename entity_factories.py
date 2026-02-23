from __future__ import annotations

import copy
from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
# Ensure you have an abilities component file; adjust this import as needed
from components.abilities import Abilities
from entity import Actor, Item

# --- Player Template ---

player = Actor(
    char="@",
    color=(50, 200, 255),
    name="Player",
    ai_cls=HostileEnemy, # Usually handled by input_handlers, but kept for factory structure
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    abilities=Abilities(), # Matches the new __init__ argument in entity.py
    image_path="resources/tiles/actors/character/humans/char_armor_01.png",
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
    image_path="resources/tiles/actors/character/humans/char_armor_01.png",
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
    image_path="resources/tiles/actors/character/humans/char_armor_01.png",
)

# --- Items ---

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
    image_path="resources/tiles/actors/character/humans/char_armor_01.pngg",
)

lightning_scroll = Item(
    char="?",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    image_path="resources/tiles/actors/character/humans/char_armor_01.png",
)

confusion_scroll = Item(
    char="?",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
    image_path="resources/tiles/actors/character/humans/char_armor_01.png",
)

fireball_scroll = Item(
    char="?",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    image_path="resources/tiles/actors/character/humans/char_armor_01.png",
)

# --- Equipment ---


# Weapon entities
sword = Item(
    char=chr(584),
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Sword(power_bonus=0),
)

club = Item(
    char=chr(292),
    color=(0, 191, 255),
    name="Club",
    equippable=equippable.Club(power_bonus=0),
)

cross_bow = Item(
    char=chr(442),
    color=(0, 191, 255),
    name="Cross Bow",
    equippable=equippable.Crossbow(power_bonus=0),
)

dagger = Item(
    char=chr(486),
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger(power_bonus=0),
)

halberd = Item(
    char=chr(591),
    color=(0, 191, 255),
    name="Halberd",
    equippable=equippable.Club(power_bonus=0),
)

hatchet = Item(
    char=chr(593),
    color=(0, 191, 255),
    name="Hatchet",
    equippable=equippable.Hatchet(power_bonus=0),
)

hunting_bow = Item(
    char=chr(491),
    color=(0, 191, 255),
    name="Hunting Bow",
    equippable=equippable.HuntingBow(power_bonus=0),
)

javelin = Item(
    char=chr(437),
    color=(0, 191, 255),
    name="Javelin",
    equippable=equippable.Javelin(power_bonus=0),
)

long_spear = Item(
    char=chr(437),
    color=(0, 191, 255),
    name="Long Spear",
    equippable=equippable.LongSpear(power_bonus=0),
)

long_sword = Item(
    char=")",
    color=(0, 191, 255),
    name="Long Sword",
    equippable=equippable.LongSword(power_bonus=0),
)

lumber_axe = Item(
    char=chr(537),
    color=(0, 191, 255),
    name="Lumber Axe",
    equippable=equippable.LumberAxe(power_bonus=0),
)

mace = Item(
    char=chr(291),
    color=(0, 191, 255),
    name="Mace",
    equippable=equippable.Mace(power_bonus=0),
)

poleaxe = Item(
    char=chr(447),
    color=(0, 191, 255),
    name="Poleaxe",
    equippable=equippable.PoleAxe(power_bonus=0),
)

quarterstaff = Item(
    char=chr(439),
    color=(0, 191, 255),
    name="Quarterstaff",
    equippable=equippable.Quarterstaff(power_bonus=0),
)

shield = Item(
    char=chr(298),
    color=(0, 191, 255),
    name="Shield",
    equippable=equippable.Shield(power_bonus=0),
)

short_spear = Item(
    char=chr(339),
    color=(0, 191, 255),
    name="Short Spear",
    equippable=equippable.ShortSpear(power_bonus=0),
)

war_axe = Item(
    char=chr(541),
    color=(0, 191, 255),
    name="War Axe",
    equippable=equippable.WarAxe(power_bonus=0),
)

war_bow = Item(
    char=chr(494),
    color=(0, 191, 255),
    name="War Bow",
    equippable=equippable.WarBow(power_bonus=0),
)

warhammer = Item(
    char=chr(540),
    color=(0, 191, 255),
    name="Warhammer",
    equippable=equippable.WarHammer(power_bonus=0),
)

# Armor entities
leather_armor = Item(
    char=chr(241),
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char=chr(242),
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail()
)