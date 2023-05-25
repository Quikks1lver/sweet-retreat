import pygame
import random
from typing import List

from characters import Player
from color.Colors import Colors
from text.Text import Text
from timing.ClockMethods import ClockMethods
from weapons.Arsenal import Arsenal
from weapons.Weapon import Weapon

class MysteryBox():
    """
    Represents a mystery box object
    """

    def __init__(self):
        self.x_start, self.y_start = 600, 370

        self.show_box = True

        self.target_time = 0
        self.TIMER_DELAY = 5000

        self.image = pygame.image.load("images/stage/mystery_box.png")

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
        if self.show_box or ClockMethods.get_current_time() > self.target_time:
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

            Text.render(screen, "Press 'B' for Mystery Weapon", Text.Font.Dewangga, 24, Colors.Neon_Cyan, (self.x_start - 70, self.y_start - 55))
            Text.render(screen, f"Cost: {cost} points", Text.Font.Dewangga, 24, Colors.Neon_Cyan, (self.x_start - 10, self.y_start - 30))

            if trying_to_buy and player.points >= cost:
                if self.__is_inbounds(player):
                    self.show_box = False
                    self.target_time = ClockMethods.get_current_time() + self.TIMER_DELAY

                    self.mystery_weapon = MysteryBox.__choose_mystery_weapon(player)

                    pygame.mixer.Sound("sounds/special/mystery_box.wav").play()
                    player.remove_points(cost)

        # draw sparkles when approaching mystery box from left
        if player.x > self.sparkles_threshold - 10 and player.x < self.sparkles_threshold:
            sparkles_img = pygame.image.load("images/stage/sparkles.png")
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
            explosion_image = pygame.image.load("images/stage/explosion.png")
            screen.blit(explosion_image, (self.x_start - 2 * weapon.image_width, self.y_start - 80))

            Text.render(screen, f"Press 'C' for {weapon.name}", Text.Font.Dewangga, 24, Colors.Neon_Green, (self.x_start - weapon.image_width + 10, self.y_start - 35))            
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
        weapons.append(Arsenal.bow_and_arrows(player))
        weapons.append(Arsenal.desert_eagle(player))
        weapons.append(Arsenal.ray_gun(player))
        weapons.append(Arsenal.revolver(player))
        weapons.append(Arsenal.rifle(player))
        weapons.append(Arsenal.rpg(player))
        weapons.append(Arsenal.smg(player))
        weapons.append(Arsenal.sniper(player))
        weapons.append(Arsenal.lightsaber(player))

        return weapons[random.randint(0, len(weapons) - 1)]