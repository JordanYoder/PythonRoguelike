from __future__ import annotations

from typing import TYPE_CHECKING

import color
import dice
import random
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hit_dice: int = 0, hp: int = 0, armor_value: int = 0, base_damage_die: int = 1):
        self.hit_dice = hit_dice
        # If hit_dice is provided, roll 1d8 per HD as per FTD [cite: 1091]
        if hit_dice > 0:
            self.max_hp = dice.roll(hit_dice, 8)
        else:
            self.max_hp = hp
        self._hp = self.max_hp
        self.armor_value = armor_value
        self.base_damage_die = base_damage_die

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def power(self) -> int:
        """Calculates the final damage result for an attack."""
        str_mod = self.parent.abilities.str_mod
        weapon = getattr(self.parent.equipment, "weapon", None)

        if weapon and weapon.equippable:
            roll = sum(
                random.randint(1, weapon.equippable.damage_dice_sides)
                for _ in range(weapon.equippable.damage_dice_num)
            )
            return roll + str_mod + weapon.equippable.power_bonus

        # Use the renamed variable here for natural attacks
        return random.randint(1, max(1, self.base_damage_die)) + str_mod

    @property
    def armor_class(self) -> int:
        # 1. Base FTD starts at 10
        base_ac = 10

        # 2. Add the Dexterity Modifier from abilities.py
        dex_mod = self.parent.abilities.dex_mod

        # 3. Get the dynamic bonus from currently equipped gear
        # This calls the Equipment component to see what's in the 'slots'
        equipment_bonus = self.parent.equipment.defense_bonus

        # 4. Add "Natural Armor" (base_defense)
        # This is for monsters who have thick skin but don't wear clothes
        natural_armor = self.armor_value

        return base_ac + dex_mod + equipment_bonus + natural_armor

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    @property
    def min_damage(self) -> int:
        str_mod = self.parent.abilities.str_mod
        weapon = getattr(self.parent.equipment, "weapon", None)

        if weapon and weapon.equippable:
            # Minimum roll is 1 per die
            return weapon.equippable.damage_dice_num + str_mod + weapon.equippable.power_bonus

        # Unarmed min is 1 + str_mod
        return 1 + str_mod

    @property
    def max_damage(self) -> int:
        str_mod = self.parent.abilities.str_mod
        weapon = getattr(self.parent.equipment, "weapon", None)

        if weapon and weapon.equippable:
            # Maximum roll is sides * num_dice
            max_roll = weapon.equippable.damage_dice_num * weapon.equippable.damage_dice_sides
            return max_roll + str_mod + weapon.equippable.power_bonus

        # Unarmed max is base_damage_die + str_mod
        return self.base_damage_die + str_mod

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = chr(894)
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
