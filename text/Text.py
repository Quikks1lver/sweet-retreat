import pygame
from enum import Enum
from typing import Tuple, Union

class Text():
    """
    Helpers for rendering text
    """
    
    class Font(Enum):
        Dewangga = "dewangga.otf"

    class Color():
        Neon_Cyan = (8, 247, 254)
        Neon_Green = (57, 255, 20)
        Neon_Magenta = (255, 29, 206)
        Red = (255, 0, 0)
        White = (255, 255, 255)

    @staticmethod
    def render(screen, text: str, font, font_size: int, color: Union[Color, Tuple[int, int, int]], location: Tuple[int, int]) -> int:
        """
        Renders text to the screen, returns width of text
        :param screen:
        :param text: text to be displayed
        :param font: Text.Font enum
        :param font_size: in pixels
        :param color: Text.Color or RGB tuple
        :param location: x, y tuple
        """
        font = pygame.font.Font(f"./text/{font.value}", font_size)
        text = font.render(text, True, color)
        screen.blit(text, location)

        return text.get_width()