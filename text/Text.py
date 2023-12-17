import pygame
from color.Colors import Colors
from enum import Enum
from typing import Tuple, Union


class Text:
    """
    (Static) helpers for rendering text
    """

    class Font(Enum):
        Dewangga = "dewangga.otf"
        Euro_Horror = "euro_horror.ttf"

    @staticmethod
    def render(
        screen,
        text: str,
        font,
        font_size: int,
        color: Union[Colors, Tuple[int, int, int]],
        location: Tuple[int, int],
    ) -> int:
        """
        Renders text to the screen, returns width of text
        :param screen:
        :param text: text to be displayed
        :param font: Text.Font enum
        :param font_size: in pixels
        :param color: Colors.Color value or RGB tuple
        :param location: x, y tuple
        """
        font = pygame.font.Font(f"./text/fonts/{font.value}", font_size)
        text = font.render(text, True, color)
        screen.blit(text, location)

        return text.get_width()
