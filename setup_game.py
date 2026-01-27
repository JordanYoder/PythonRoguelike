"""Handle the loading and initialization of game sessions."""
from __future__ import annotations
from tcod import libtcodpy

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("menu_background.png")[:, :, :3]


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

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "TOMBS OF THE ANCIENT KINGS",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_options = [
            "[N] Quick Start (Default Player)",
            "[M] Manual Character Creation",
            "[C] Continue last game",
            "[Q] Quit"
        ]

        menu_width = 34
        for i, text in enumerate(menu_options):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.Q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()

        elif event.sym == tcod.event.KeySym.C:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")

        elif event.sym == tcod.event.KeySym.N:
            # Jump directly into the game with default stats
            return input_handlers.MainGameEventHandler(new_game())

        elif event.sym == tcod.event.KeySym.M:
            # Transition to the modular character creation screen
            return input_handlers.CharacterCreationHandler(engine_base_setup())

        return None