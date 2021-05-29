import pygame
from enum import Enum
from typing import Tuple

class Text():
    """
    Helpers for rendering text
    """
    
    class Font(Enum):
        Dewangga = "dewangga.otf"

    @staticmethod
    def render(screen, text: str, font, font_size: int, color: Tuple[int, int, int], location: Tuple[int, int]) -> int:
        """
        Renders text to the screen, returns width of text
        :param screen:
        :param text: text to be displayed
        :param font: Text.Font enum
        :param font_size: in pixels
        :param color: RGB tuple
        :param location: x, y tuple
        """
        font = pygame.font.Font(f"./text/{font.value}", font_size)
        text = font.render(text, True, color)
        screen.blit(text, location)

        return text.get_width()