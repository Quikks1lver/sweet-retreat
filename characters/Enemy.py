import math
import pygame

class Enemy():
    """
    Represents an enemy character in the pygame
    """

    def __init__(self, image_path: str, x_start: int, y_start: int, x_velocity: int, y_velocity: int, stage_width: int, game_width: int, y_top_threshold: int, y_bottom_threshold: int):
        # TODO
        # DOCUMENTATION

        """
        Initialize an enemy character
        """
        self.image = pygame.image.load(image_path)
        self.image_width = self.image.get_width()

        self.x = x_start
        self.y = y_start
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

        self.stage_width = stage_width
        self.game_width = game_width

        self.y_top_threshold = y_top_threshold
        self.y_bottom_threshold = y_bottom_threshold

        self.is_left_facing = False

    def draw(self, screen) -> None:
        if self.is_left_facing: screen.blit(self.image, (self.x, self.y))
        else: screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))

    def move(self, player) -> None:
        if self.x > player.real_x_position: self.x -= self.x_velocity
        elif self.x < player.real_x_position: self.x += self.x_velocity
        else: pass

        if self.y > player.y: self.y -= self.y_velocity
        elif self.y < player.y: self.y += self.y_velocity
        else: pass