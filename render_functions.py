from __future__ import annotations

from typing import Tuple, TYPE_CHECKING, List
import pygame
import color

if TYPE_CHECKING:
    from engine import Engine
    from game_map import GameMap

# 1. Initialize Font
pygame.font.init()
FONT_SIZE = 20
UI_FONT = pygame.font.SysFont("arial", FONT_SIZE)

TILE_SIZE = 32


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
            self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True
    ) -> None:
        if stack and self.messages and self.messages[-1].plain_text == text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self, surface: pygame.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        """Render the log with a background panel."""
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (15, 15, 15), panel_rect)
        pygame.draw.rect(surface, (100, 100, 100), panel_rect, 1)

        current_draw_y = y + height - 25

        for message in reversed(self.messages):
            msg_surf = UI_FONT.render(message.full_text, True, message.fg)
            surface.blit(msg_surf, (x + 10, current_draw_y))
            current_draw_y -= 22

            if current_draw_y < y + 5:
                break

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    """Returns a string of names at map coordinates (x, y)."""
    # Important: only show names if the tile is in bounds AND currently visible
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities
        if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar(
        surface: pygame.Surface, current_val: int, max_val: int, total_width: int, location: Tuple[int, int]
) -> None:
    x, y = location
    bar_width = int((float(current_val) / max_val) * total_width)

    pygame.draw.rect(surface, color.bar_empty, (x, y, total_width, 20))
    if bar_width > 0:
        pygame.draw.rect(surface, color.bar_filled, (x, y, bar_width, 20))

    health_text = f"HP: {current_val}/{max_val}"
    text_surf = UI_FONT.render(health_text, True, color.bar_text)
    surface.blit(text_surf, (x + 5, y + 1))


def render_dungeon_level(
        surface: pygame.Surface, dungeon_level: int, location: Tuple[int, int]
) -> None:
    level_text = f"Dungeon level: {dungeon_level}"
    text_surf = UI_FONT.render(level_text, True, color.white)
    surface.blit(text_surf, location)


def render_names_at_mouse_location(
        surface: pygame.Surface, x: int, y: int, engine: Engine, map_pos: Tuple[int, int]
) -> None:
    map_x, map_y = map_pos

    names = get_names_at_location(map_x, map_y, engine.game_map)

    if names:
        text_surf = UI_FONT.render(names, True, color.white)
        # Background box for readability
        bg_rect = text_surf.get_rect(topleft=(x, y))
        pygame.draw.rect(surface, (0, 0, 0), bg_rect.inflate(10, 10))
        surface.blit(text_surf, (x, y))