import pygame

from text.Text import Text
from timing.Clock_Methods import Clock_Methods

class Splash_Screen():
    """
    Class to display splash screen at game start
    """
    TIMER_DELAY = 500
    TARGET_TIME = Clock_Methods.get_current_time() + TIMER_DELAY

    @staticmethod
    def draw(screen) -> None:
        """
        Draws the splash screen onto the screen
        :param screen:
        """
        splash_screen = pygame.image.load("images/splash_screen.png").convert()
        screen.blit(splash_screen, (0, 0))

        if Clock_Methods.is_past_this_time(Splash_Screen.TARGET_TIME):
            Text.render(screen, "Press 'ENTER' to begin", Text.Font.Dewangga, 30, (255, 255, 255), (275, 20))
            
            if Clock_Methods.is_past_this_time(Splash_Screen.TARGET_TIME + 1750):
                Splash_Screen.TARGET_TIME = Clock_Methods.get_current_time() + Splash_Screen.TIMER_DELAY