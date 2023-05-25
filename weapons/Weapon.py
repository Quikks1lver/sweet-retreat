import pygame
from characters import Player
from .Bullet import Bullet, BulletState, BulletDirection

class Weapon():
    """
    Represents a ranged or melee weapon
    """

    def __init__(self, name: str, image_path: str, sound_path: str, bullet_image: str, character: Player, projectile_x_velocity: float, damage: float, ammo: int, full_auto: bool = False, max_bullet_dist: int = None):
        """
        Initializes a new weapon
        :param name: name of weapon
        :param image_path:
        :param sound_path: sound when firing
        :param character: character who's using the weapon
        :param projectile_x_velocity: how fast the bullet/projectile travels
        :param damage: damage hit
        :param ammo: how much ammunition the weapon holds
        :param full_auto: (optional) full auto capability
        :param max_bullet_dist: used for melee weapons: how much 'distance' the 'bullet' travels
        """
        self.name = name

        self.character: Player = character
        self.x = 0
        self.y = 0

        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.set_volume(.2)

        self.image = pygame.image.load(image_path)
        self.image_width = self.image.get_width()

        self.ammo = ammo
        self.ammo_string = Weapon.__build_ammo_string(ammo)

        self.bullet = Bullet(bullet_image, projectile_x_velocity, damage, self.character.stage_width, max_bullet_dist)

        self.full_auto = full_auto

        self.is_upgraded = False

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

        if self.bullet.state == BulletState.MOVING: self.bullet.draw(screen)

    def fire(self) -> None:
        """
        Fires weapon
        :return:
        """
        if self.bullet.state == BulletState.READY and self.ammo > 0:
            # sound
            self.sound.play()

            # offsets for where bullet comes out of weapon
            dx = -10 if self.character.is_left_facing else 10
            dy = -5
            self.bullet.reset(self.x + dx, self.y + dy)
            self.bullet.state = BulletState.MOVING
            self.bullet.direction = BulletDirection.LEFT if self.character.is_left_facing else BulletDirection.RIGHT
            self.ammo -= 1

    def add_ammo(self, amount: int) -> None:
        """
        Add ammo to weapon
        :param amount: amount of ammo
        :return:
        """
        self.ammo += amount

    def is_being_used(self) -> bool:
        """
        Returns whether the current weapon is being used (whether a bullet is in motion or not)
        :return: True if bullet is in motion, False otherwise
        """
        return self.bullet.state == BulletState.MOVING

    def is_full_auto(self) -> bool:
        """
        Returns whether the weapon can fire full auto
        :return: True if full auto, False otherwise
        """
        return self.full_auto

    @staticmethod
    def __build_ammo_string(ammo: int) -> str:
        """
        Builds string representation of ammo
        Efficient string concat in python => list comprehension (see resources)
        :return: ammo string
        """
        return "".join("I" for i in range(ammo))

    def get_ammo_string(self) -> str:
        """
        Returns string representation of the ammo
        Helps game performance by memoization
        :return: ammo string
        """
        if len(self.ammo_string) == self.ammo:
            return self.ammo_string
        
        self.ammo_string = Weapon.__build_ammo_string(self.ammo)
        return self.ammo_string