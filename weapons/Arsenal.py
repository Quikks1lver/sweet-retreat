from .Weapon import Weapon
from characters import Player

class Arsenal():
    """
    A collection of weapons the player character can use
    """

    @staticmethod
    def bow_and_arrows(player: Player) -> Weapon:
        """
        Returns a bow and arrow weapon
        """
        return Weapon("Bow", "images/bow.png",  "sounds/bow.wav", "images/arrow.png", player, 4, 20, 50)

    @staticmethod
    def desert_eagle(player: Player) -> Weapon:
        """
        Returns a desert eagle weapon
        """
        return Weapon("D. Eagle", "images/desert_eagle.png",  "sounds/desert_eagle.wav", "images/bullet.png", player, 7, 20, 30)

    @staticmethod
    def ray_gun(player: Player) -> Weapon:
        """
        Returns a ray gun weapon
        """
        return Weapon("Ray Gun", "images/ray_gun.png",  "sounds/ray_gun.wav", "images/ray_gun_bullet.png", player, 2, 50, 25)

    @staticmethod
    def revolver(player: Player) -> Weapon:
        """
        Returns a revolver weapon (player's starting weapon)
        """
        return Weapon("Revolver", "images/revolver.png",  "sounds/revolver.wav", "images/bullet.png", player, 5, 10, 50)

    @staticmethod
    def rifle(player: Player) -> Weapon:
        """
        Returns a rifle weapon
        """
        return Weapon("Rifle", "images/rifle.png", "sounds/rifle.wav", "images/bullet.png", player, 30, 15, 75)
    
    @staticmethod
    def rpg(player: Player) -> Weapon:
        """
        Returns an RPG weapon
        """
        return Weapon("RPG", "images/rpg.png", "sounds/rpg.wav", "images/rpg_bullet.png", player, 4, 75, 10)

    @staticmethod
    def smg(player: Player) -> Weapon:
        """
        Returns a smg weapon
        """
        return Weapon("SMG", "images/smg.png", "sounds/smg.wav", "images/bullet.png", player, 50, 12, 100)

    @staticmethod
    def sniper(player: Player) -> Weapon:
        """
        Returns a sniper rifle weapon
        """
        return Weapon("Sniper", "images/sniper.png", "sounds/sniper.wav", "images/bullet.png", player, 10, 25, 30)