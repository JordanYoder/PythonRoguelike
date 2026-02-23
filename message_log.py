from typing import Iterable, List, Reversible, Tuple
import pygame
import color
from render_functions import UI_FONT


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

    def add_message(self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True) -> None:
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """Render the log using pixel-based text wrapping."""
        self.render_messages(surface, x, y, width, height, self.messages)

    @classmethod
    def render_messages(
            cls, surface: pygame.Surface, x: int, y: int, width: int, height: int, messages: Reversible[Message]
    ) -> None:
        y_offset = height - 20  # Start from the bottom of the log area

        for message in reversed(messages):
            # Simple Pygame text wrapping logic
            words = message.full_text.split(' ')
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if UI_FONT.size(test_line)[0] < width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            for line in reversed(lines):
                if y_offset < 0:
                    return
                msg_surf = UI_FONT.render(line, True, message.fg)
                surface.blit(msg_surf, (x, y + y_offset))
                y_offset -= 20  # Move up for the next line
