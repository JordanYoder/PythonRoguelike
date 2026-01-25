from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
            location=(0, 35)  # Explicitly set the location here
        )

        # Message log starts at y=35 (5 rows from the bottom)
        self.message_log.render(console=console, x=21, y=35, width=40, height=4)

        # Dungeon level on row 39 (the very last visible row)
        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 39),
        )

        # Mouse-over names stay at the top (y=1)
        render_functions.render_names_at_mouse_location(
            console=console, x=1, y=1, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)


    # In engine.py
    @property
    def camera_x(self) -> int:
        # Centered on player, clamped to map edges
        # Assuming viewport width is 80
        return max(0, min(self.player.x - 40, self.game_map.width - 80))

    @property
    def camera_y(self) -> int:
        # Centered on player, clamped to map edges
        # Assuming viewport height is 35 (for your 1440p/40-row setup)
        return max(0, min(self.player.y - 17, self.game_map.height - 35))
