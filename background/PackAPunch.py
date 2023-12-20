import pygame
import copy

from characters import Player
from color.Colors import Colors
from text.Text import Text
from text.TimedText import TimedText
from timing.ClockMethods import ClockMethods
from weapons.Weapon import Weapon


class PackAPunch:
    """
    Represents a pack a punch box
    """

    def __init__(self):
        self.x_start, self.y_start = 600, 150

        self.show_box = True

        self.target_time = 0
        self.TIMER_DELAY = 13000

        self.image = pygame.image.load("images/stage/papbox.png")

        self.sparkles_threshold = 0

        self.mystery_weapon: Weapon = None

        self.timed_text = TimedText()

    def draw(
        self,
        screen,
        player: Player,
        cost: int,
        trying_to_buy: bool,
        trying_to_pick_up_weapon: bool,
    ) -> None:
        """
        Draws PaP box and weapons (if available) to screen
        """
        self.timed_text.run(screen)

        if self.show_box or ClockMethods.get_current_time() > self.target_time:
            self.__draw_pap_box(screen, player, cost, trying_to_buy)
        else:
            self.__draw_weapon(
                screen, player, trying_to_pick_up_weapon, self.mystery_weapon
            )

    def __draw_pap_box(
        self, screen, player: Player, cost: int, trying_to_buy: bool
    ) -> None:
        """
        Draws PaP box
        """
        self.sparkles_threshold = player.stage_width - player.start_scrolling_pos_x

        if player.x >= self.sparkles_threshold:
            screen.blit(self.image, (self.x_start, self.y_start))

            Text.render(
                screen,
                "Press B to Upgrade Weapon",
                Text.Font.Euro_Horror,
                18,
                Colors.Neon_Orange,
                (self.x_start - 70, self.y_start - 55),
            )
            Text.render(
                screen,
                f"Costs {cost} points",
                Text.Font.Euro_Horror,
                18,
                Colors.Neon_Orange,
                (self.x_start - 10, self.y_start - 30),
            )

            if (
                trying_to_buy
                and player.get_current_weapon() is not None
                and player.get_current_weapon().is_upgraded
                and self.__is_inbounds(player)
            ):
                self.timed_text.populate_timed_text_parameters(
                    "Cannot upgrade an upgraded weapon",
                    Text.Font.Euro_Horror,
                    20,
                    Colors.Red,
                    (210, 130),
                    3,
                )

                return

            if (
                trying_to_buy
                and player.points >= cost
                and player.get_current_weapon() is not None
                and not player.get_current_weapon().is_being_used()
            ):
                if self.__is_inbounds(player):
                    self.show_box = False
                    self.target_time = (
                        ClockMethods.get_current_time() + self.TIMER_DELAY
                    )

                    self.mystery_weapon = PackAPunch.pack_a_punch(
                        player.get_current_weapon()
                    )

                    pygame.mixer.Sound("sounds/special/pap_box_noise.wav").play()
                    player.remove_points(cost)
                    player.remove_current_weapon()

        # draw sparkles when approaching mystery box from left
        if self.sparkles_threshold - 10 < player.x < self.sparkles_threshold:
            sparkles_img = pygame.image.load("images/stage/sparkles.png")
            screen.blit(sparkles_img, (self.x_start, self.y_start))

    def __draw_weapon(
        self, screen, player: Player, trying_to_pick_up_weapon: bool, weapon: Weapon
    ) -> None:
        """
        Draws a weapon to the screen
        """
        # only display when on right side of screen
        if player.x >= self.sparkles_threshold:
            explosion_image = pygame.image.load("images/stage/pap_effect.png")
            screen.blit(
                explosion_image,
                (self.x_start - 2 * weapon.image_width, self.y_start - 80),
            )

            Text.render(
                screen,
                f"Press C for {weapon.name}",
                Text.Font.Euro_Horror,
                18,
                Colors.Neon_Orange,
                (self.x_start - weapon.image_width + 10, self.y_start - 35),
            )
            screen.blit(
                weapon.image,
                (self.x_start + 2.5 * weapon.image_width, self.y_start + 30),
            )

            # give player weapon
            if trying_to_pick_up_weapon and self.__is_inbounds(player):
                self.show_box = True
                player.add_mystery_weapon(weapon)

    def __is_inbounds(self, player: Player) -> bool:
        """
        Returns true if player is in bounds of box, false otherwise
        """
        return (
            True
            if player.real_x_position >= self.x_start
            and player.real_x_position <= (self.x_start + self.image.get_width())
            and player.y >= self.y_start
            and player.y <= (self.y_start + self.image.get_height())
            else False
        )

    @staticmethod
    def pack_a_punch(weapon: Weapon) -> Weapon:
        """
        Returns an upgraded weapon
        """
        pap_weapon = copy.copy(weapon)

        pap_weapon.is_upgraded = True

        # change weapon color (snippet from SO)
        pap_color = pygame.Color("deeppink")
        for x in range(pap_weapon.image.get_width()):
            for y in range(pap_weapon.image.get_height()):
                pap_color.a = pap_weapon.image.get_at((x, y)).a
                pap_weapon.image.set_at((x, y), pap_color)

        pap_weapon.name = pap_weapon.name + " v2"
        pap_weapon.bullet.damage *= 2
        pap_weapon.ammo = pap_weapon.ammo + 100
        pap_weapon.sound.set_volume(0.2)

        if weapon.bullet.max_bullet_dist is not None:  # melee weapons
            pap_weapon.sound = pygame.mixer.Sound("sounds/weapons/pap_melee.wav")
        else:  # ranged
            pap_weapon.sound = pygame.mixer.Sound("sounds/weapons/pap_gun.wav")
            pap_weapon.bullet.image = pygame.image.load("images/bullets/pap_bullet.png")

        return pap_weapon
