import pygame

from color.Colors import Colors
from text.Text import Text
from timing.ClockMethods import ClockMethods


class StartScreen:
    """
    Represents a (starting) game screen
    """

    TIMER_DELAY = 500

    def __init__(self, image_path: str) -> None:
        self.TARGET_TIME = ClockMethods.get_current_time() + StartScreen.TIMER_DELAY
        self.image = pygame.image.load(image_path).convert()

    def draw(self, screen) -> None:
        """
        Draws the screen
        :param screen:
        """
        screen.blit(self.image, (0, 0))

        # text appears/disappears every few seconds, like a blinking light
        if ClockMethods.is_past_this_time(self.TARGET_TIME):
            Text.render(
                screen,
                "Press 'ENTER' to continue",
                Text.Font.Dewangga,
                30,
                Colors.White,
                (250, 20),
            )

            if ClockMethods.is_past_this_time(self.TARGET_TIME + 1750):
                self.TARGET_TIME = (
                    ClockMethods.get_current_time() + StartScreen.TIMER_DELAY
                )
