"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import pygame
import tcod

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers

# Load the background image using pygame instead of tcod
# Note: menu_background.png must be in the same directory or adjust path
background_image = pygame.image.load("menu_background.png")


def engine_base_setup() -> Engine:
    """
    Sets up the engine and player template without generating the world yet.
    Used by both Quick Start and Manual Character Creation.
    """
    map_width = 125
    map_height = 125

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    return engine


def new_game() -> Engine:
    """Return a brand new 'Quick Start' game session as an Engine instance."""
    engine = engine_base_setup()
    player = engine.player

    # Standard "Quick Start" equipment setup
    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    # Generate the world immediately for Quick Start
    engine.game_world.generate_floor()

    if engine.player not in engine.game_map.entities:
        engine.game_map.entities.add(engine.player)

    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, surface: pygame.Surface) -> None:
        """Render the main menu on a background image."""
        # Draw the background image to fill the screen
        surface.blit(pygame.transform.scale(background_image, surface.get_size()), (0, 0))

        # Import UI_FONT for consistent text rendering
        from render_functions import UI_FONT

        # Render Title
        title_text = "TOMBS OF THE ANCIENT KINGS"
        title_surf = UI_FONT.render(title_text, True, color.menu_title)
        title_x = surface.get_width() // 2 - title_surf.get_width() // 2
        title_y = surface.get_height() // 2 - 150
        surface.blit(title_surf, (title_x, title_y))

        menu_options = [
            "[N] Quick Start (Default Player)",
            "[M] Manual Character Creation",
            "[C] Continue last game",
            "[Q] Quit"
        ]

        # Render each menu option with a dark background for readability
        for i, text in enumerate(menu_options):
            option_surf = UI_FONT.render(text, True, color.menu_text)
            option_x = surface.get_width() // 2 - option_surf.get_width() // 2
            option_y = surface.get_height() // 2 - 50 + (i * 40)

            # Draw a semi-transparent black box behind the text
            bg_rect = pygame.Rect(option_x - 10, option_y - 5, option_surf.get_width() + 20, option_surf.get_height() + 10)
            overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (bg_rect.x, bg_rect.y))

            surface.blit(option_surf, (option_x, option_y))

    def ev_keydown(self, event: pygame.event.Event) -> Optional[input_handlers.BaseEventHandler]:
        # Handle menu navigation using Pygame key constants
        if event.key in (pygame.K_q, pygame.K_ESCAPE):
            raise SystemExit()

        elif event.key == pygame.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")

        elif event.key == pygame.K_n:
            # Jump directly into the game with default stats
            return input_handlers.MainGameEventHandler(new_game())

        elif event.key == pygame.K_m:
            # Transition to the modular character creation screen
            return input_handlers.CharacterCreationHandler(engine_base_setup())

        return None