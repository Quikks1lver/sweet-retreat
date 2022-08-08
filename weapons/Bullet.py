import pygame
from enum import Enum

class BulletState(Enum):
    READY = 0
    MOVING = 1

class BulletDirection(Enum):
    LEFT = 0
    RIGHT = 1

class Bullet():
    """
    Represents a weapon's bullet
    """

    def __init__(self, image_path, x_velocity, damage: int, stage_width: int):
        """
        Initializes a bullet object
        :param image_path:
        :param x_velocity: how fast bullet travels
        :param damage:
        :param stage_width: width of entire stage
        """
        self.image = pygame.image.load(image_path)
        self.image_width = self.image.get_width()

        self.x = 0
        self.y = 0

        self.x_velocity = x_velocity
        self.damage = damage

        self.direction: BulletDirection = BulletDirection.LEFT
        self.state: BulletState = BulletState.READY

        self.stage_width = stage_width

    def reset(self, x: int, y: int) -> None:
        """
        Reset bullet to inside weapon (ready to fire state)
        :param x: x coord
        :param y: y coord
        :return:
        """
        self.state = BulletState.READY
        self.x, self.y = x, y

    def move(self):
        """
        Move bullet
        :return:
        """
        if self.state == BulletState.MOVING:
            self.x += abs(self.x_velocity) if self.direction == BulletDirection.RIGHT else -abs(self.x_velocity)

        # check out of bounds; bullet travels 1/2 of stage width
        if self.x < 0 or self.x > (self.stage_width/2) - self.image_width: self.state = BulletState.READY

    def draw(self, screen) -> None:
        """
        Draws bullet to the screen
        :param screen:
        :return:
        """
        self.move()

        if self.state == BulletState.MOVING:
            if self.direction == BulletDirection.LEFT: screen.blit(self.image, (self.x, self.y))
            else: screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))