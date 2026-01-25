from __future__ import annotations
from components.base_component import BaseComponent


class Abilities(BaseComponent):
    def __init__(
        self,
        strength: int = 10,
        dexterity: int = 10,
        constitution: int = 10,
        intelligence: int = 10,
        wisdom: int = 10,
        charisma: int = 10,
    ):
        self.str = strength
        self.dex = dexterity
        self.con = constitution
        self.int = intelligence
        self.wis = wisdom
        self.cha = charisma

    def get_modifier(self, score: int) -> int:
        """FTD Ability Score to Modifier conversion [cite: 315]"""
        if score >= 18: return 4
        if score >= 16: return 3
        if score >= 14: return 2
        if score >= 12: return 1
        if score >= 10: return 0
        if score >= 8:  return -1
        if score >= 6:  return -2
        if score >= 4:  return -3
        return -4

    @property
    def str_mod(self) -> int:
        return (self.str - 10) // 2

    @property
    def dex_mod(self) -> int:
        return (self.dex - 10) // 2

    @property
    def con_mod(self) -> int: return self.get_modifier(self.con)
    @property
    def int_mod(self) -> int: return self.get_modifier(self.int)
    @property
    def wis_mod(self) -> int: return self.get_modifier(self.wis)
    @property
    def cha_mod(self) -> int: return self.get_modifier(self.cha)