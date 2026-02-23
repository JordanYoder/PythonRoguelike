# tile_types.py
from typing import Tuple, Optional
import pygame


# Simplified tile structure to hold image paths
class TileType:
    def __init__(
        self,
        walkable: bool,
        transparent: bool,
        dark_color: Tuple[int, int, int],
        light_color: Tuple[int, int, int],
        image_path: Optional[str] = None,
    ):
        self.walkable = walkable
        self.transparent = transparent
        self.dark_color = dark_color
        self.light_color = light_color
        self.image_path = image_path
        self._image: Optional[pygame.Surface] = None

    @property
    def image(self) -> Optional[pygame.Surface]:
        """Lazy load the tile image."""
        if self._image is None and self.image_path:
            try:
                self._image = pygame.image.load(self.image_path).convert_alpha()
            except pygame.error:
                return None
        return self._image


def new_tile(
    *,
    walkable: bool,
    transparent: bool,
    dark: Tuple[int, int, int],
    light: Tuple[int, int, int],
    image_path: Optional[str] = None,
) -> TileType:
    return TileType(walkable, transparent, dark, light, image_path)


# Define your tiles with paths to your PNG files
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(25, 25, 25),
    light=(60, 60, 60),
    image_path="resources/tiles/floor/tile_01.png",
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(50, 40, 20),
    light=(130, 110, 50),
    image_path="resources/tiles/wall/wall_01.png",
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(0, 0, 100),    # Deep blue for explored stairs
    light=(0, 0, 255),   # Bright blue for visible stairs
    image_path="",
)