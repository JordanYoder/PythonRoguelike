from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

from entity import Actor, Item
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before

        self.downstairs_location = (0, 0)

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int,
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside  the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    # In game_map.py

    def render(self, console: Console) -> None:
        """
        Renders the map.

        Uses camera offsets from the engine to slice the map and render
        only the visible portion.
        """
        # 1. Get camera offsets from the engine
        # Ensure you have defined camera_x and camera_y properties in engine.py
        cam_x = self.engine.camera_x
        cam_y = self.engine.camera_y

        # 2. Define the size of the viewport (the map area on screen)
        # Based on your engine.py UI, 80x43 is a safe area
        viewport_width = 80
        viewport_height = 35

        # 3. Slice the map arrays to extract only the tiles visible to the camera
        # We use [cam_x : cam_x + viewport_width] to get the correct slice of the world
        visible_tiles = self.tiles[cam_x: cam_x + viewport_width, cam_y: cam_y + viewport_height]

        console.rgb[0:viewport_width, 0:viewport_height] = np.select(
            condlist=[
                self.visible[cam_x: cam_x + viewport_width, cam_y: cam_y + viewport_height],
                self.explored[cam_x: cam_x + viewport_width, cam_y: cam_y + viewport_height]
            ],
            choicelist=[visible_tiles["light"], visible_tiles["dark"]],
            default=tile_types.SHROUD,
        )

        # 4. Sort entities by render order so corpses stay below actors
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        # 5. Render entities that are in FOV and within the camera viewport
        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                # Subtract camera offsets to translate "World Map" coords to "Screen" coords
                screen_x = entity.x - cam_x
                screen_y = entity.y - cam_y

                # Only print if the entity is physically within the visible screen area
                if 0 <= screen_x < viewport_width and 0 <= screen_y < viewport_height:
                    console.print(
                        x=screen_x,
                        y=screen_y,
                        string=entity.char,
                        fg=entity.color
                    )


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: Engine,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        current_floor: int = 0
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = max_rooms

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.current_floor = current_floor

    def generate_floor(self) -> None:
        from procgen import generate_dungeon

        self.current_floor += 1

        self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine,
        )
