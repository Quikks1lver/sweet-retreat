import pygame
import random
from typing import List

from characters import Player
from timing.Clock_Methods import Clock_Methods
from weapons.Weapon import Weapon
from weapons.Arsenal import Arsenal

class MysteryBox():
    """
    Represents a mystery box object
    """

    def __init__(self):
        self.x_start, self.y_start = 600, 370

        self.show_box = True
        self.waiting_for_weapon_pickup = False

        self.target_time = 0
        self.TIMER_DELAY = 5000

        self.image = pygame.image.load("images/mystery_box.png")

        self.sparkles_threshold = 0

        self.mystery_weapon: Weapon = None

    def draw(self, screen, player: Player, cost: int, trying_to_buy: bool, trying_to_pick_up_weapon: bool) -> None:
        """
        Draws mystery box and weapons (if available) to screen
        :param screen:
        :param player:
        :param cost:
        :param trying_to_buy: whether player is trying to buy
        :param trying_to_pick_up_weapon: whether player is trying to pick up the weapon
        :return:
        """
        if self.show_box or Clock_Methods.get_current_time() > self.target_time:
            self.__draw_mystery_box(screen, player, cost, trying_to_buy)
        else:
            self.__draw_weapon(screen, player, trying_to_pick_up_weapon, self.mystery_weapon)

    def __draw_mystery_box(self, screen, player: Player, cost: int, trying_to_buy: bool) -> None:
        """
        Draws mystery box box onto the screen
        :param screen:
        :param player:
        :param cost:
        :param trying_to_buy:
        :return:
        """
        self.x_start, self.y_start = 600, 370
        self.sparkles_threshold = player.stage_width - player.start_scrolling_pos_x

        # draw mystery box and description of cost on right side of screen
        if player.x >= self.sparkles_threshold:
            self.x_start, self.y_start = 600, 370

            screen.blit(self.image, (self.x_start, self.y_start))

            font = pygame.font.Font("./fonts/dewangga.otf", 24)
            title = font.render("Press 'B' for Mystery Weapon", True, (255, 255, 255))  # white
            score_title = font.render(f"Cost: {cost} points", True, (255, 255, 255))  # white
            screen.blit(title, (self.x_start - 70, self.y_start - 55))
            screen.blit(score_title, (self.x_start - 10, self.y_start - 30))

            if trying_to_buy and player.points >= cost:
                if self.__is_inbounds(player):
                    self.show_box = False
                    self.target_time = Clock_Methods.get_current_time() + self.TIMER_DELAY

                    self.mystery_weapon = MysteryBox.__choose_mystery_weapon(player)

                    pygame.mixer.Sound("sounds/mystery_box.wav").play()
                    player.remove_points(cost)

        # draw sparkles when approaching mystery box from left
        if player.x > self.sparkles_threshold - 10 and player.x < self.sparkles_threshold:
            sparkles_img = pygame.image.load("images/sparkles.png")
            screen.blit(sparkles_img, (self.x_start, self.y_start))

    def __draw_weapon(self, screen, player: Player, trying_to_pick_up_weapon: bool, weapon: Weapon) -> None:
        """
        Draws a weapon to the screen
        :param screen:
        :param player:
        :param trying_to_pick_up_weapon: whether player is trying to pick up the weapon
        :param weapon: weapon to be drawn to screen
        :return:
        """
        # only display when on right side of screen
        if player.x >= self.sparkles_threshold:
            explosion_image = pygame.image.load("images/explosion.png")
            screen.blit(explosion_image, (self.x_start - 2 * weapon.image_width, self.y_start - 80))

            font = pygame.font.Font("./fonts/dewangga.otf", 24)
            title = font.render(f"Press 'C' for {weapon.name}", True, (0, 255, 0))  # green
            screen.blit(title, (self.x_start - weapon.image_width + 10, self.y_start - 35))
            screen.blit(weapon.image, (self.x_start + 2.5 * weapon.image_width, self.y_start + 30))

            # give player weapon
            if trying_to_pick_up_weapon and self.__is_inbounds(player):
                self.show_box = True
                player.add_mystery_weapon(weapon)

    def __is_inbounds(self, player: Player) -> bool:
        """
        Returns true if player is in bounds of box, false otherwise
        :param player:
        :return:
        """
        return True if player.real_x_position >= self.x_start and player.real_x_position <= (self.x_start + self.image.get_width()) else False

    @staticmethod
    def __choose_mystery_weapon(player: Player) -> Weapon:
        """
        Randomly choose and return a mystery weapon
        :param player:
        :return:
        """
        weapons: List[Weapon] = []
        weapons.append(Arsenal.ray_gun(player))
        weapons.append(Arsenal.revolver(player))
        weapons.append(Arsenal.sniper(player))
        weapons.append(Arsenal.rifle(player))

        return weapons[random.randint(0, len(weapons) - 1)]