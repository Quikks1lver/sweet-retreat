import pygame
from characters import Player

class Weapon():
    """
    Represents a (typically ranged) weapon that either a character uses
    """

    def __init__(self, image_path: str, character: Player, projectile_x_velocity: float, damage: float, ammo: int):
        """
        Initializes a new weapon
        :param image_path:
        :param character: character who's using the weapon
        :param projectile_x_velocity: how fast the bullet/projectile travels
        :param damage: damage hit
        :param ammo: how much ammunition the weapon holds
        """
        self.character = character

        self.image = pygame.image.load(image_path)
        self.image_width = self.image.get_width()

        self.x_velocity = projectile_x_velocity
        self.damage = damage
        self.ammo = ammo

    def draw(self, screen) -> None:
        """
        Draws weapon to the screen
        :param screen: game screen
        :return:
        """
        if self.character.is_left_facing: screen.blit(self.image, (self.character.real_x_position - self.image_width, self.character.y + 15))
        else: screen.blit(pygame.transform.flip(self.image, True, False), (self.character.real_x_position + self.image_width + (self.character.image_width/2), self.character.y + 15))

    def add_ammo(self, amount: int) -> None:
        """
        Add ammo to weapon
        :param amount: amount of ammo
        :return:
        """
        self.ammo += amount