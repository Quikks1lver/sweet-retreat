import pygame
from characters import Player
from .Bullet import Bullet, Bullet_State, Bullet_Direction

class Weapon():
    """
    Represents a (typically ranged) weapon that either a character uses
    """

    def __init__(self, name: str, image_path: str, sound_path: str, bullet_image: str, character: Player, projectile_x_velocity: float, damage: float, ammo: int):
        """
        Initializes a new weapon
        :param name: name of weapon
        :param image_path:
        :param sound_path: sound when firing
        :param character: character who's using the weapon
        :param projectile_x_velocity: how fast the bullet/projectile travels
        :param damage: damage hit
        :param ammo: how much ammunition the weapon holds
        """
        self.name = name

        self.character: Player = character
        self.x = 0
        self.y = 0

        self.sound = pygame.mixer.Sound(sound_path)

        self.image = pygame.image.load(image_path)
        self.image_width = self.image.get_width()

        self.ammo = ammo

        self.bullet = Bullet(bullet_image, projectile_x_velocity, damage, self.character.stage_width)

    def draw(self, screen) -> None:
        """
        Draws weapon to the screen
        :param screen: game screen
        :return:
        """
        self.x = self.character.real_x_position - self.image_width if self.character.is_left_facing else \
                 self.character.real_x_position + self.image_width + (self.character.image_width / 2)
        self.y = self.character.y + 15

        if self.character.is_left_facing: screen.blit(self.image, (self.x, self.y))
        else: screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))

        if self.bullet.state == Bullet_State.MOVING: self.bullet.draw(screen)

    def fire(self) -> None:
        """
        Fires weapon
        :return:
        """
        if self.bullet.state == Bullet_State.READY and self.ammo > 0:
            # sound
            self.sound.play()

            # offsets for where bullet comes out of weapon
            dx = -10 if self.character.is_left_facing else 10
            dy = -5
            self.bullet.reset(self.x + dx, self.y + dy)
            self.bullet.state = Bullet_State.MOVING
            self.bullet.direction = Bullet_Direction.LEFT if self.character.is_left_facing else Bullet_Direction.RIGHT
            self.ammo -= 1

    def add_ammo(self, amount: int) -> None:
        """
        Add ammo to weapon
        :param amount: amount of ammo
        :return:
        """
        self.ammo += amount