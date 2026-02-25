# components/fighter.py
from __future__ import annotations
from typing import TYPE_CHECKING
from components.base_component import BaseComponent
import color
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        if hasattr(self.parent, "equipment"):
            return self.parent.equipment.defense_bonus
        return 0

    @property
    def power_bonus(self) -> int:
        if hasattr(self.parent, "equipment"):
            return self.parent.equipment.power_bonus
        return 0

    def die(self) -> None:
        if self.parent is self.engine.player:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        # 1. Update the path to the skull and bones
        self.parent.image_path = "resources/tiles/glyphs/death/death_skull_bones.png"

        # 2. Force the color to Bright Red
        self.parent.color = (145, 15, 15)

        # 3. Clear the cache so the engine re-renders the sprite with the new color
        self.parent._image = None

        # 4. Standard death state changes
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
