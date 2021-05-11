import math
import pygame
from .Player import Player
import random

class Enemy(Player):
    """
    Represents an enemy character in the pygame
    """

    def __init__(self, image_path: str, x_start: int, y_start: int, start_scrolling_pos_x: int, stage_width: int, game_width: int, y_top_threshold: int, y_bottom_threshold: int, health: int, x_velocity: float, y_velocity: float):
        super().__init__(image_path, x_start, y_start, start_scrolling_pos_x, stage_width,
                         game_width, y_top_threshold, y_bottom_threshold, health)

        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def move(self, player: Player) -> None:

        # inject some randomness
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

        if self.x > player.x: self.x -= self.x_velocity
        elif self.x < player.x: self.x += self.x_velocity
        else: pass

        if self.y > player.y: self.y -= self.y_velocity
        elif self.y < player.y: self.y += self.y_velocity
        else: pass

        # make sure enemy doesn't go above x/y thresholds
        if self.x > self.stage_width - self.image_width: self.x = self.stage_width - self.image_width
        if self.x < 0: self.x = 0
        if self.y < self.y_top_threshold: self.y = self.y_top_threshold
        if self.y > self.y_bottom_threshold: self.y = self.y_bottom_threshold

        if self.x < self.start_scrolling_pos_x:
            self.real_x_position = self.x
        elif self.x > self.stage_width - self.start_scrolling_pos_x:
            self.real_x_position = self.x - self.stage_width + self.game_width
        else:
            self.real_x_position = self.start_scrolling_pos_x