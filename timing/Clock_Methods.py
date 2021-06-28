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

    @staticmethod
    def get_current_time_in_seconds(decimal_place: int) -> float:
        """
        Gets current time in seconds, with desired decimal precision
        :param decimal_place: how many decimal places you want in end result
        """
        return round((Clock_Methods.get_current_time() / 1000), decimal_place)