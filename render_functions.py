from __future__ import annotations

from typing import Tuple, TYPE_CHECKING, List
import pygame
import color

if TYPE_CHECKING:
    from engine import Engine
    from game_map import GameMap

# 1. Initialize Standard Pygame Font
pygame.font.init()

# Using SysFont to grab Arial from the OS
FONT_SIZE = 20
UI_FONT = pygame.font.SysFont("arial", FONT_SIZE)
# You can also make a bold version for titles
TITLE_FONT = pygame.font.SysFont("arial", 32, bold=True)

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
        """Render the log. Coordinates are pixels."""
        # Optional: Draw a dark background for the message log area
        # pygame.draw.rect(surface, (0, 0, 0), (x, y, width * 16, height * 20))

        render_y = y + height  # Start at the top of the log area

        for message in reversed(self.messages):
            # Standard pygame.font.render(text, antialias, color)
            msg_surf = UI_FONT.render(message.full_text, True, message.fg)
            surface.blit(msg_surf, (x, render_y))
            render_y -= 22  # Vertical spacing

            if render_y < y:
                break


def render_bar(
        surface: pygame.Surface, current_val: int, max_val: int, total_width: int, location: Tuple[int, int]
) -> None:
    x, y = location
    bar_width = int((float(current_val) / max_val) * total_width)

    # Draw background bar
    pygame.draw.rect(surface, color.bar_empty, (x, y, total_width, 20))
    # Draw current health bar
    if bar_width > 0:
        pygame.draw.rect(surface, color.bar_filled, (x, y, bar_width, 20))

    # Render health text
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
        surface: pygame.Surface, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    # Get names from game map logic
    entities_at_location = [
        e.name for e in engine.game_map.entities
        if e.x == mouse_x and e.y == mouse_y and engine.game_map.visible[e.x, e.y]
    ]
    names = ", ".join(entities_at_location)

    if names:
        text_surf = UI_FONT.render(names, True, color.white)
        surface.blit(text_surf, (x, y))