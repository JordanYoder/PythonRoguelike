from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0, # Flat bonus (like +1 weapons)
        defense_bonus: int = 0,
        damage_dice_num: int = 1,   # Number of dice (e.g., 2 in 2d6)
        damage_dice_sides: int = 4, # Sides of dice (e.g., 6 in 1d6)
    ):
        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.damage_dice_num = damage_dice_num
        self.damage_dice_sides = damage_dice_sides


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)
