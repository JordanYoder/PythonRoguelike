from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

import numpy as np
import pygame
from tcod.map import compute_fov

import exceptions
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = render_functions.MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view."""
        # Extract transparency boolean array from TileType objects
        transparency = np.vectorize(lambda t: t.transparent)(self.game_map.tiles)

        self.game_map.visible[:] = compute_fov(
            transparency,
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, surface: pygame.Surface) -> None:
        """Render the game map, UI, and bars to the Pygame surface."""
        self.game_map.render(surface)

        # UI Positioning (Pixel coordinates)
        self.message_log.render(surface=surface, x=20, y=550, width=600, height=150)

        render_functions.render_bar(
            surface=surface,
            current_val=self.player.fighter.hp,
            max_val=self.player.fighter.max_hp,
            total_width=200,
            location=(20, 520)
        )

        render_functions.render_dungeon_level(
            surface=surface,
            dungeon_level=self.game_world.current_floor,
            location=(20, 500),
        )

        render_functions.render_names_at_mouse_location(
            surface=surface, x=20, y=480, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)

    @property
    def camera_x(self) -> int:
        val = self.player.x - 40
        return max(0, min(val, self.game_map.width - 80))

    @property
    def camera_y(self) -> int:
        val = self.player.y - 17
        return max(0, min(val, self.game_map.height - 35))