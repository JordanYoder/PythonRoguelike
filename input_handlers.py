from __future__ import annotations

from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union

import pygame
import actions
from actions import (
    Action,
    BumpAction,
    PickupAction,
    WaitAction,
)
import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item

# Constants for pixel math
TILE_SIZE = 32

# Map Pygame keys to direction vectors
MOVE_KEYS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_KP8: (0, -1),
    pygame.K_KP2: (0, 1),
    pygame.K_KP4: (-1, 0),
    pygame.K_KP6: (1, 0),
    pygame.K_KP7: (-1, -1),
    pygame.K_KP9: (1, -1),
    pygame.K_KP1: (-1, 1),
    pygame.K_KP3: (1, 1),
    # Vi Keys
    pygame.K_h: (-1, 0),
    pygame.K_j: (0, 1),
    pygame.K_k: (0, -1),
    pygame.K_l: (1, 0),
    pygame.K_y: (-1, -1),
    pygame.K_u: (1, -1),
    pygame.K_b: (-1, 1),
    pygame.K_n: (1, 1),
}

WAIT_KEYS = {pygame.K_PERIOD, pygame.K_KP_PERIOD, pygame.K_KP5}

# Import the font and rendering helpers
from render_functions import UI_FONT

ActionOrHandler = Union[Action, "BaseEventHandler"]


class BaseEventHandler:
    def handle_events(self, event: pygame.event.Event) -> BaseEventHandler:
        if event.type == pygame.QUIT:
            raise SystemExit()

        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        return self

    def dispatch(self, event: pygame.event.Event) -> ActionOrHandler:
        if event.type == pygame.KEYDOWN:
            return self.ev_keydown(event)
        elif event.type == pygame.MOUSEMOTION:
            return self.ev_mousemotion(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self.ev_mousebuttondown(event)
        return self

    def on_render(self, surface: pygame.Surface) -> None:
        raise NotImplementedError()

    def ev_keydown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        return None

    def ev_mousemotion(self, event: pygame.event.Event) -> None:
        pass

    def ev_mousebuttondown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        return None


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: pygame.event.Event) -> BaseEventHandler:
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            if not self.engine.player.is_alive:
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)
        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        if action is None:
            return False
        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False

        self.engine.handle_enemy_turns()
        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event: pygame.event.Event) -> None:
        self.engine.mouse_location = (event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE)

    def on_render(self, surface: pygame.Surface) -> None:
        self.engine.render(surface)


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.key

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            return BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            return WaitAction(player)
        elif key == pygame.K_ESCAPE:
            raise SystemExit()
        elif key == pygame.K_g:
            return PickupAction(player)
        elif key == pygame.K_i:
            return InventoryActivateHandler(self.engine)
        elif key == pygame.K_d:
            return InventoryDropHandler(self.engine)
        elif key == pygame.K_c:
            return CharacterScreenEventHandler(self.engine)
        elif key == pygame.K_SLASH:
            return LookHandler(self.engine)
        return None


class AskUserEventHandler(EventHandler):
    def ev_keydown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        if event.key in {pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT,
                         pygame.K_RALT}:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        return self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
        return MainGameEventHandler(self.engine)


class LevelUpEventHandler(AskUserEventHandler):
    TITLE = "Level Up"

    def on_render(self, surface: pygame.Surface) -> None:
        super().on_render(surface)
        menu_rect = pygame.Rect(100, 100, 450, 250)
        pygame.draw.rect(surface, (0, 0, 0), menu_rect)
        pygame.draw.rect(surface, color.white, menu_rect, 2)

        title_surf = UI_FONT.render(self.TITLE, True, color.menu_title)
        surface.blit(title_surf, (menu_rect.x + 20, menu_rect.y + 20))

        options = [
            f"a) Constitution (+20 HP, from {self.engine.player.fighter.max_hp})",
            f"b) Strength (+1 attack, from {self.engine.player.fighter.power})",
            f"c) Agility (+1 AC, from {self.engine.player.fighter.armor_class})"
        ]

        for i, text in enumerate(options):
            surf = UI_FONT.render(text, True, color.white)
            surface.blit(surf, (menu_rect.x + 20, menu_rect.y + 70 + (i * 30)))

    def ev_keydown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        player = self.engine.player
        if event.key == pygame.K_a:
            player.level.increase_max_hp()
        elif event.key == pygame.K_b:
            player.level.increase_power()
        elif event.key == pygame.K_c:
            player.level.increase_defense()
        else:
            return None
        return super().ev_keydown(event)


class InventoryEventHandler(AskUserEventHandler):
    TITLE = "<missing title>"

    def on_render(self, surface: pygame.Surface) -> None:
        super().on_render(surface)
        items = self.engine.player.inventory.items

        menu_rect = pygame.Rect(100, 100, 400, 20 + (max(1, len(items)) * 25) + 40)
        pygame.draw.rect(surface, (0, 0, 0), menu_rect)
        pygame.draw.rect(surface, color.white, menu_rect, 1)

        title_surf = UI_FONT.render(self.TITLE, True, color.white)
        surface.blit(title_surf, (menu_rect.x + 10, menu_rect.y + 10))

        if not items:
            surf = UI_FONT.render("(Empty)", True, color.white)
            surface.blit(surf, (menu_rect.x + 10, menu_rect.y + 50))
        else:
            for i, item in enumerate(items):
                char = chr(ord("a") + i)
                equipped = " (E)" if self.engine.player.equipment.item_is_equipped(item) else ""
                surf = UI_FONT.render(f"({char}) {item.name}{equipped}", True, color.white)
                surface.blit(surf, (menu_rect.x + 10, menu_rect.y + 50 + (i * 25)))

    def ev_keydown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        index = event.key - pygame.K_a
        if 0 <= index <= 26:
            try:
                selected_item = self.engine.player.inventory.items[index]
                return self.on_item_selected(selected_item)
            except IndexError:
                return None
        return super().ev_keydown(event)


class InventoryActivateHandler(InventoryEventHandler):
    TITLE = "Select an item to use"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return actions.EquipAction(self.engine.player, item)
        return None


class InventoryDropHandler(InventoryEventHandler):
    TITLE = "Select an item to drop"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        return actions.DropItem(self.engine.player, item)


class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Character Information"

    def on_render(self, surface: pygame.Surface) -> None:
        super().on_render(surface)
        sheet_rect = pygame.Rect(200, 150, 400, 250)
        pygame.draw.rect(surface, (0, 0, 0), sheet_rect)
        pygame.draw.rect(surface, color.white, sheet_rect, 2)
        p = self.engine.player
        stats = [f"Level: {p.level.current_level}", f"XP: {p.level.current_xp}", f"Attack: {p.fighter.power}",
                 f"AC: {p.fighter.armor_class}"]
        title_surf = UI_FONT.render(self.TITLE, True, color.menu_title)
        surface.blit(title_surf, (sheet_rect.x + 20, sheet_rect.y + 20))
        for i, text in enumerate(stats):
            surf = UI_FONT.render(text, True, color.white)
            surface.blit(surf, (sheet_rect.x + 20, sheet_rect.y + 70 + (i * 30)))


class SelectIndexHandler(AskUserEventHandler):
    def ev_mousemotion(self, event: pygame.event.Event) -> None:
        self.engine.mouse_location = (event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE)

    def ev_mousebuttondown(self, event: pygame.event.Event) -> Optional[ActionOrHandler]:
        if event.button == 1:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        return MainGameEventHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)
        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    def __init__(self, engine: Engine, radius: int, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)
        self.radius = radius
        self.callback = callback

    def on_render(self, surface: pygame.Surface) -> None:
        super().on_render(surface)
        x, y = self.engine.mouse_location
        cam_x, cam_y = self.engine.camera_x, self.engine.camera_y
        rect_size = (self.radius * 2 + 1) * TILE_SIZE
        overlay = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 100))
        surface.blit(overlay, ((x - cam_x - self.radius) * TILE_SIZE, (y - cam_y - self.radius) * TILE_SIZE))

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class GameOverEventHandler(EventHandler):
    def on_render(self, surface: pygame.Surface) -> None:
        self.engine.render(surface)
        msg = UI_FONT.render("YOU DIED! Press ESC to Quit", True, color.player_die)
        surface.blit(msg, (surface.get_width() // 2 - msg.get_width() // 2, surface.get_height() // 2))

    def ev_keydown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            raise SystemExit()