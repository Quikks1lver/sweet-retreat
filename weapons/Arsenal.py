from .Weapon import Weapon
from characters import Player

class Arsenal():
    """
    A collection of weapons the player character can use
    """

    @staticmethod
    def revolver(player: Player) -> Weapon:
        """
        Returns a revolver weapon (player's starting weapon)
        :param player:
        :return:
        """
        return Weapon("images/revolver.png",  "sounds/weapon.wav", "images/bullet.png", player, 7, 10, 50)

    @staticmethod
    def ray_gun(player: Player) -> Weapon:
        """
        Returns a ray gun weapon
        :param player:
        :return:
        """
        return Weapon("images/revolver.png",  "sounds/weapon.wav", "images/bullet.png", player, 7, 10, 50)