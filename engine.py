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

        # engine.py
        # engine.py

        # engine.py

        # engine.py

    def render(self, surface: pygame.Surface) -> None:
        """Render the game map, UI, and coordinate-aware tooltips."""
        s_width, s_height = surface.get_size()

        # 1. Draw the game map (this uses self.camera_x/y internally)
        self.game_map.render(surface)

        # 2. TRANSLATE MOUSE PIXELS TO MAP COORDINATES
        raw_x, raw_y = self.mouse_location

        # Calculate which tile index the mouse is over ON THE SCREEN
        screen_tile_x = raw_x // render_functions.TILE_SIZE
        screen_tile_y = raw_y // render_functions.TILE_SIZE

        # Add the CAMERA OFFSET to find the actual tile in the WORLD
        map_x = screen_tile_x + self.camera_x
        map_y = screen_tile_y + self.camera_y

        # --- UI ELEMENTS ---
        side_margin = 20
        bottom_margin = 40
        log_height = 150
        log_y = s_height - log_height - bottom_margin

        # 3. Message Log
        self.message_log.render(surface, side_margin, log_y, 600, log_height)

        # 4. Health Bar
        bar_y = log_y - 40
        render_functions.render_bar(surface, self.player.fighter.hp, self.player.fighter.max_hp, 200,
                                    (side_margin, bar_y))

        # 5. Dungeon Level
        level_y = bar_y - 30
        render_functions.render_dungeon_level(surface, self.game_world.current_floor, (side_margin, level_y))

        # 6. RENDER NAMES AT MOUSE LOCATION
        # We pass the translated map_x and map_y here
        render_functions.render_names_at_mouse_location(
            surface=surface,
            x=side_margin,
            y=10,
            engine=self,
            map_pos=(map_x, map_y)
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