from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.abilities import Abilities
from components.equippable import Equippable
from equipment_types import EquipmentType
from render_order import RenderOrder
from entity import Actor, Item


player = Actor(
    char=chr(188),
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hit_dice=10, armor_value=0, base_damage_die=1),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    abilities=Abilities(strength=18, dexterity=18, charisma=18, intelligence=18, wisdom=18, constitution=18),
    render_order=RenderOrder.PLAYER,
)

orc = Actor(
    char=chr(286),
    color=(0, 255, 0),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hit_dice=2, armor_value=0, base_damage_die=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    abilities=Abilities(strength=12, dexterity=10, charisma=10, intelligence=10, wisdom=10, constitution=10 )
)
troll = Actor(
    char=chr(484),
    color=(182, 215, 73),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, armor_value=2, base_damage_die=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    abilities=Abilities(strength=10, dexterity=10, charisma=10, intelligence=10, wisdom=10, constitution=10)
)

confusion_scroll = Item(
    char=chr(928),
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char=chr(928),
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char=chr(740),
    color=(255, 255, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char=chr(928),
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(
    char=")", color=(0, 191, 255), name="Dagger",
    equippable=Equippable(
        equipment_type=EquipmentType.WEAPON,
        damage_dice_num=1,
        damage_dice_sides=4
    ),
)

sword = Item(
    char=chr(584),
    color=(0, 191, 255),
    name="Sword",
    equippable=Equippable(
        equipment_type=EquipmentType.WEAPON,
        damage_dice_num=1,
        damage_dice_sides=6
    ),
)

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
