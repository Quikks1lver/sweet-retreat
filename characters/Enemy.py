from enum import Enum
import pygame
import math
import random

from color.Colors import Colors
from .Player import Player
from text.Text import Text
from weapons.Bullet import Bullet, Bullet_State

class Enemy_Collision(Enum):
    NO_HIT = 0
    HIT = 1
    DEFEATED = 2

class Enemy(Player):
    """
    Represents an enemy character in the pygame
    """

    def __init__(self, image_path: str, x_start: int, y_start: int, start_scrolling_pos_x: int, stage_width: int,
                 game_width: int, y_top_threshold: int, y_bottom_threshold: int, health: int, x_velocity: float,
                 y_velocity: float, damage: int, point_gain_on_hit: int, point_gain_on_defeat: int,
                 blitted_health_offset_x: int = 20, blitted_health_offset_y: int = 70):
        """
        Initialize an enemy character
        :param image_path: file path of player image
        :param x_start:
        :param y_start:
        :param start_scrolling_pos_x: point at which background scrolls/moves, not the player
        :param stage_width: width of stage (a few times the background image)
        :param game_width: width of game window itself
        :param y_top_threshold: top threshold where character cannot go above
        :param y_bottom_threshold: bottom threshold where character cannot go below
        :param health: hit points of character
        :param x_velocity:
        :param y_velocity:
        :param damage: how much damage the enemy deals
        :param point_gain_on_hit: how many points the player gains by hitting this enemy
        :param point_gain_on_defeat: how many points the player gains by defeating this enemy
        :param blitted_health_offset_x: (optional) offset for where to blit health bar relative to enemy, x
        :param blitted_health_offset_y: (optional) offset for where to blit health bar relative to enemy, y
        """
        super().__init__(image_path, x_start, y_start, start_scrolling_pos_x, stage_width,
                         game_width, y_top_threshold, y_bottom_threshold, health)

        self.max_health = health
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.damage = damage
        self.point_gain_on_hit = point_gain_on_hit
        self.point_gain_on_defeat = point_gain_on_defeat
        self.blitted_health_offset_x = blitted_health_offset_x
        self.blitted_health_offset_y = blitted_health_offset_y

    def draw(self, screen) -> None:
        """
        draws enemy and metadata onto the pygame window, changing orientation if necessary
        """
        # print enemy
        if self.is_left_facing: screen.blit(self.image, (self.real_x_position, self.y))
        else: screen.blit(pygame.transform.flip(self.image, True, False), (self.real_x_position, self.y))

        # print health
        Text.render(screen, str(int(self.health)), Text.Font.Dewangga, 23, Colors.Red, (self.real_x_position + self.blitted_health_offset_x, self.y + self.blitted_health_offset_y))

    def move(self, player: Player) -> None:
        """
        Moves enemy according to current position and player's position
        Also has some random movement to simulate being crazy
        :param player: player object
        :return:
        """
        # inject some randomness
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

        # track player's x position
        if self.x > player.x: self.x -= self.x_velocity
        elif self.x < player.x: self.x += self.x_velocity
        else: pass

        # track player's y position
        if self.y > player.y: self.y -= self.y_velocity
        elif self.y < player.y: self.y += self.y_velocity
        else: pass

        # make sure enemy doesn't go above y thresholds; it can go past x-thresholds, though
        if self.y < self.y_top_threshold: self.y = self.y_top_threshold
        if self.y > self.y_bottom_threshold: self.y = self.y_bottom_threshold

        # refer to Player file for comments on these lines
        if self.x < self.start_scrolling_pos_x:
            self.real_x_position = self.x
        elif self.x > self.stage_width - self.start_scrolling_pos_x:
            self.real_x_position = self.x - self.stage_width + self.game_width
        else:
            self.real_x_position = self.start_scrolling_pos_x

    def has_collision_with_player(self, player: Player, threshold: float) -> bool:
        """
        Determines whether the enemy collides with the player
        :param player: player character
        :param threshold: below or equal to which is considered a collision
        :return:
        """
        return True if math.dist([self.x, self.y], [player.x, player.y]) <= threshold else False

    def check_for_bullet_collision(self, bullet: Bullet, threshold: float) -> Enemy_Collision:
        """
        Checks whether bullet has hit enemy and updates health and bullet status
        :param bullet:
        :param threshold:
        :return: what kind of collision occurred
        """

        if bullet.state == Bullet_State.MOVING and math.dist([self.real_x_position, self.y], [bullet.x, bullet.y]) <= threshold:
            bullet.state = Bullet_State.READY
            self.take_damage(bullet.damage)
            if self.health <= 0:
                self.respawn()
                return Enemy_Collision.DEFEATED
            return Enemy_Collision.HIT
        return Enemy_Collision.NO_HIT

    def respawn(self):
        """
        Respawns the enemy character
        :return:
        """
        self.health = self.max_health
        self.x = self.stage_width + 200 if random.randint (0, 1) == 0 else -200

    def damage_amount(self) -> int:
        """
        Returns how much damage this enemy deals
        """
        return self.damage

    def get_point_gain_on_hit(self) -> int:
        """
        Returns how many points the player gains by hitting this enemy
        """
        return self.point_gain_on_hit

    def get_point_gain_on_defeat(self) -> int:
        """
        Returns how many points the player gains by defeating this enemy
        """
        return self.point_gain_on_defeat

    def __repr__(self):
        return f"{self.health} {self.damage} ||"