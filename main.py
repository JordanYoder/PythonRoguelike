import traceback

import pygame

import color
import exceptions
import input_handlers
import setup_game


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active engine, save the game."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    # Screen resolution - adjust these to match your monitor's preferred size
    screen_width = 2560
    screen_height = 1440

    pygame.init()

    # 200ms delay before repeating, then repeat every 50ms
    pygame.key.set_repeat(200, 50)

    # Set the window icon and title
    pygame.display.set_caption("Tombs of the Ancient Kings")
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    clock = pygame.time.Clock()

    while True:
        # 1. Render the current state
        try:
            # Clear the screen with black
            screen.fill((0, 0, 0))

            # The handler (Menu or Game) draws itself to the screen
            handler.on_render(screen)

            pygame.display.flip()
        except Exception:
            traceback.print_exc()

        # 2. Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save and Exit
                if isinstance(handler, input_handlers.EventHandler):
                    save_game(handler, "savegame.sav")
                pygame.quit()
                raise SystemExit()

            # Handle mouse motion for hovering over enemies/items
            elif event.type == pygame.MOUSEMOTION:
                if isinstance(handler, input_handlers.EventHandler):
                    # Capture raw pixel coordinates
                    handler.engine.mouse_location = event.pos

            # Hand off all other events (keyboard, etc.) to the current handler
            try:
                handler = handler.handle_events(event)
            except exceptions.Impossible as exc:
                # If an action is impossible, report it to the message log
                if isinstance(handler, input_handlers.EventHandler):
                    handler.engine.message_log.add_message(exc.args[0], color.impossible)
            except Exception:
                traceback.print_exc()
                if isinstance(handler, input_handlers.EventHandler):
                    handler.engine.message_log.add_message(traceback.format_exc(), color.error)

        # Caps the game at 60 FPS
        clock.tick(60)


if __name__ == "__main__":
    main()