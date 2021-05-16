import pygame

class Clock_Methods():
    """
    Helps with timing
    """

    @staticmethod
    def is_past_this_time(time: int) -> bool:
        """
        Returns true if current time is past target, false otherwise
        :param time: target time
        :return:
        """
        return True if Clock_Methods.get_current_time() > time else False

    @staticmethod
    def get_current_time() -> int:
        """
        Returns current time
        :return:
        """
        return pygame.time.get_ticks()