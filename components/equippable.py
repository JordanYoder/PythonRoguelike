from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


# In components/equippable.py

class Equippable(BaseComponent):
    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        damage_dice_num: int = 1,
        damage_dice_sides: int = 4,
        scaling_stat: str = "STR",  # Default for swords/melee
    ):
        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.damage_dice_num = damage_dice_num
        self.damage_dice_sides = damage_dice_sides
        self.scaling_stat = scaling_stat


class Sword(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=10,
            scaling_stat="STR",
        )


class Club(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=10,
            scaling_stat="STR",
        )


class Crossbow(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=12,
            scaling_stat="DEX_WIS",
        )


class Dagger(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=6,
            scaling_stat="STR_DEX",
        )


class Halberd(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=12,
            scaling_stat="STR_INT",
        )


class Hatchet(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=6,
            scaling_stat="STR",
        )


class HuntingBow(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=8,
            scaling_stat="DEX",
        )


class Javelin(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=6,
            scaling_stat="STR",
        )


class LongSpear(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=12,
            scaling_stat="STR",
        )


class LongSword(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=12,
            scaling_stat="STR",
        )


class LumberAxe(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=8,
            scaling_stat="STR",
        )


class Mace(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=6,
            scaling_stat="STR",
        )


class PoleAxe(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=12,
            scaling_stat="STR",
        )


class Quarterstaff(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=8,
            scaling_stat="STR",
        )


class Shield(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=6,
            scaling_stat="STR",
        )


class ShortSpear(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=8,
            scaling_stat="STR_DEX",
        )


class WarAxe(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=10,
            scaling_stat="STR",
        )


class WarBow(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=12,
            scaling_stat="STR_DEX",
        )


class WarHammer(Equippable):
    def __init__(self, power_bonus: int = 0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=power_bonus,
            damage_dice_num=1,
            damage_dice_sides=10,
            scaling_stat="STR",
        )


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)
