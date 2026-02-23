from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
import pygame

from entity import Actor, Item
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

TILE_SIZE = 32


class GameMap:
    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

        self.downstairs_location = (0, 0)

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this map's living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        """Iterate over the items currently on the map."""
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(
            self, location_x: int, location_y: int
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
        """Return True if x and y are inside the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, surface: pygame.Surface) -> None:
        """
        Renders the map and entities using Pygame.
        The map is shifted based on the camera position in the engine.
        """
        cam_x, cam_y = self.engine.camera_x, self.engine.camera_y

        # Viewport size in tiles (matches main.py settings)
        view_w, view_h = 80, 35

        # 1. Render Tiles
        for x in range(cam_x, cam_x + view_w):
            for y in range(cam_y, cam_y + view_h):
                if not self.in_bounds(x, y):
                    continue

                tile = self.tiles[x, y]
                screen_x = (x - cam_x) * TILE_SIZE
                screen_y = (y - cam_y) * TILE_SIZE
                rect = (screen_x, screen_y, TILE_SIZE, TILE_SIZE)

                if self.visible[x, y]:
                    # Draw the image if it exists, otherwise use light_color rect
                    if tile.image:
                        surface.blit(tile.image, (screen_x, screen_y))
                    else:
                        pygame.draw.rect(surface, tile.light_color, rect)

                elif self.explored[x, y]:
                    # Draw the image with a dark overlay if it exists
                    if tile.image:
                        surface.blit(tile.image, (screen_x, screen_y))
                        # Create a dimming overlay
                        dim_overlay = pygame.Surface((TILE_SIZE, TILE_SIZE))
                        dim_overlay.fill((0, 0, 0))
                        dim_overlay.set_alpha(180)  # Adjust for darkness preference
                        surface.blit(dim_overlay, (screen_x, screen_y))
                    else:
                        pygame.draw.rect(surface, tile.dark_color, rect)
                else:
                    # Unexplored (Shroud)
                    pygame.draw.rect(surface, (0, 0, 0), rect)

        # 2. Render Entities
        # Sorted so corpses appear below items, and items below actors
        entities_sorted = sorted(self.entities, key=lambda e: e.render_order.value)

        for entity in entities_sorted:
            if self.visible[entity.x, entity.y]:
                screen_x = (entity.x - cam_x) * TILE_SIZE
                screen_y = (entity.y - cam_y) * TILE_SIZE

                if entity.image:
                    # We scale entity images here since they change position frequently
                    scaled_img = pygame.transform.scale(entity.image, (TILE_SIZE, TILE_SIZE))
                    surface.blit(scaled_img, (screen_x, screen_y))
                else:
                    # Use the color defined in the factory
                    pygame.draw.rect(surface, entity.color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))


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