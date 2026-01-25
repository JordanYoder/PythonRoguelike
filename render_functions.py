from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod.console import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    x, y = int(x), int(y)

    # Use 'explored' so players can see labels of things in the dark
    if not game_map.in_bounds(x, y) or not game_map.explored[x, y]:
        return ""

    entities_at_location = [
        entity for entity in game_map.entities if entity.x == x and entity.y == y
    ]

    lines = []
    for entity in entities_at_location:
        # Capitalize only the name here
        name_str = entity.name.capitalize()

        if hasattr(entity, "abilities") and entity.abilities:
            a = entity.abilities
            f = entity.fighter
            low = max(1, f.min_damage)
            high = max(1, f.max_damage)
            # These uppercase labels will now be preserved
            stats = (f"STR:{a.str} DEX:{a.dex} CON:{a.con} INT:{a.int} WIS:{a.wis} CHA:{a.cha} "
                     f"AC: {entity.fighter.armor_class} Dmg: {low}-{high})"
                     )
            name_str = f"{name_str} {stats}"

        lines.append(name_str)

    # Return the joined string WITHOUT calling .capitalize() at the end
    return ", ".join(lines)


# In render_functions.py

def render_bar(
    console: Console,
    current_value: int,
    maximum_value: int,
    total_width: int,
    location: Tuple[int, int] = (0, 35) # Add a default location that fits the new screen
) -> None:
    x, y = location # Use the location parameter
    bar_width = int(float(current_value) / maximum_value * total_width)

    # Use the 'y' variable instead of the hardcoded 45
    console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=x, y=y, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=x + 1, y=y, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )


def render_dungeon_level(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")


# In render_functions.py

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    # TRANSLATION: Add camera offsets to convert screen coords to world coords
    world_mouse_x = mouse_x + engine.camera_x
    world_mouse_y = mouse_y + engine.camera_y

    names_at_mouse_location = get_names_at_location(
        x=world_mouse_x, y=world_mouse_y, game_map=engine.game_map
    )

    # Print the result at the specified SCREEN location (x=1, y=1)
    console.print(x=x, y=y, string=names_at_mouse_location)
