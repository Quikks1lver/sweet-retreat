import pygame

class Clock_Methods():
    """
    Helps with timing
    """

    @staticmethod
    def is_past_this_time(time: int) -> bool:
        """
        Returns true if current time (milliseconds) is past target, false otherwise
        :param time: target time
        :return:
        """
        return True if Clock_Methods.get_current_time() > time else False

    @staticmethod
    def is_past_this_time_in_seconds(time: int) -> bool:
        """
        Returns true if current time (seconds) is past target, false otherwise
        :param time: target time
        :return:
        """
        return True if Clock_Methods.get_current_time_in_seconds() > time else False

    @staticmethod
    def get_current_time() -> int:
        """
        Returns current time in milliseconds
        :return:
        """
        return pygame.time.get_ticks()

    @staticmethod
    def get_current_time_in_seconds(decimal_place: int = 10) -> float:
        """
        Gets current time in seconds, with desired decimal precision
        :param decimal_place: how many decimal places you want in end result
        :return:
        """
        return round((Clock_Methods.get_current_time() / 1000), decimal_place)
    
    @staticmethod
    def get_time_survived(uncounted_time: float, decimal_place: int) -> float:
        """
        Returns the amount of time the player character has survived
        :param uncounted_time: time that does not factor into the time survived (time in first few screens, pause, etc.)
        :param decimal_place: floating point precision
        :return:
        """
        return round(Clock_Methods.get_current_time_in_seconds(decimal_place) - uncounted_time, decimal_place)