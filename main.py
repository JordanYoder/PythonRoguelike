#!/usr/bin/env python3
import pygame
import traceback
import color
import exceptions
import setup_game
import input_handlers

# Constants for the new pixel-based window
TILE_SIZE = 32
SCREEN_WIDTH_TILES = 80
SCREEN_HEIGHT_TILES = 40
PIXEL_WIDTH = SCREEN_WIDTH_TILES * TILE_SIZE  # 2560 pixels
PIXEL_HEIGHT = SCREEN_HEIGHT_TILES * TILE_SIZE  # 1280 pixels


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    pygame.init()

    # Create the window with Pygame
    screen = pygame.display.set_mode((PIXEL_WIDTH, PIXEL_HEIGHT))
    pygame.display.set_caption("Tombs of the Ancient Kings")

    clock = pygame.time.Clock()

    # Initialize the handler (this still uses setup_game for now)
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    try:
        while True:
            # 1. Clear the screen (Replacing root_console.clear)
            screen.fill((0, 0, 0))

            # 2. Render current state
            # Note: We will need to update on_render in other files to accept 'screen'
            handler.on_render(screen)

            # 3. Update display (Replacing context.present)
            pygame.display.flip()

            # 4. Handle Events (Replacing tcod.event.wait)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()

                # Logic for handling keys and mouse will shift into the handler
                try:
                    handler = handler.handle_events(event)
                except Exception:
                    traceback.print_exc()
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )

            # Limit to 60 FPS
            clock.tick(60)

    except exceptions.QuitWithoutSaving:
        pygame.quit()
        raise
    except SystemExit:
        save_game(handler, "savegame.sav")
        pygame.quit()
        raise
    except BaseException:
        save_game(handler, "savegame.sav")
        pygame.quit()
        raise


if __name__ == "__main__":
    main()
