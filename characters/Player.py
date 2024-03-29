import pygame

from background.SoundHelpers import play_sound
from color.Colors import Colors
from text.Text import Text
from typing import List, Union
from weapons.Weapon import Weapon


class Player:
    """
    Represents a player character in the pygame
    """

    def __init__(
        self,
        image_path: str,
        x_start: int,
        y_start: int,
        start_scrolling_pos_x: int,
        stage_width: int,
        game_width: int,
        y_top_threshold: int,
        y_bottom_threshold: int,
        health: int,
    ):
        """
        Initialize a player character
        :param image_path: file path of player image
        :param x_start:
        :param y_start:
        :param start_scrolling_pos_x: point at which background scrolls/moves, not the player
        :param stage_width: width of stage (a few times the background image)
        :param game_width: width of game window itself
        :param y_top_threshold: top threshold where character cannot go above
        :param y_bottom_threshold: bottom threshold where character cannot go below
        :param health: hit points of character
        """
        self.image = pygame.image.load(image_path)
        self.image_width = self.image.get_width()

        self.x = x_start
        self.y = y_start
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.real_x_position = self.image_width

        self.start_scrolling_pos_x = start_scrolling_pos_x
        self.stage_width = stage_width
        self.game_width = game_width

        self.y_top_threshold = y_top_threshold
        self.y_bottom_threshold = y_bottom_threshold

        self.health = health

        self.is_left_facing = False

        self.weapons: List[Weapon] = []
        self.current_weapon = 0

        self.points = 0

    def draw(self, screen) -> None:
        """
        draws player and metadata onto the pygame window, changing orientation if necessary
        :param screen: pygame display
        :return: None
        """
        # print character
        if self.is_left_facing:
            screen.blit(self.image, (self.real_x_position, self.y))
        else:
            screen.blit(
                pygame.transform.flip(self.image, True, False),
                (self.real_x_position, self.y),
            )

        # print health
        Text.render(
            screen,
            str(int(self.health)) + " HP",
            Text.Font.Euro_Horror,
            15,
            Colors.Red,
            (self.real_x_position + 20, self.y + 70),
        )

        # print weapon
        if len(self.weapons) > 0:
            self.get_current_weapon().draw(screen)

    def set_x_velocity(self, new_velocity: float) -> None:
        """
        Changes x velocity field
        :param new_velocity:
        :return:
        """
        self.x_velocity = new_velocity

        # change player's orientation/direction
        if self.x_velocity == 0:
            return
        else:
            self.is_left_facing = False if self.x_velocity > 0 else True

    def set_y_velocity(self, new_velocity: float) -> None:
        """
        Changes y velocity field
        :param new_velocity:
        :return:
        """
        self.y_velocity = new_velocity

    def move(self) -> None:
        """
        Moves player character according to current position and velocities
        This was super helpful: https://www.youtube.com/watch?v=AX8YU2hLBUg
        :return:
        """
        self.x += self.x_velocity
        self.y += self.y_velocity

        # makes sure player doesn't go beyond stage to the right
        if self.x > self.stage_width - self.image_width:
            self.x = self.stage_width - self.image_width
        # makes sure player doesn't go beyond stage to the left
        if self.x < 0:
            self.x = 0
        # makes sure player doesn't go above top threshold
        if self.y < self.y_top_threshold:
            self.y = self.y_top_threshold
        # makes sure player doesn't go below bottom threshold
        if self.y > self.y_bottom_threshold:
            self.y = self.y_bottom_threshold

        # where x position of player is less than scrolling threshold
        if self.x < self.start_scrolling_pos_x:
            self.real_x_position = self.x
        # where stage no longer scrolls, but the player moves to the end
        elif self.x > self.stage_width - self.start_scrolling_pos_x:
            self.real_x_position = self.x - self.stage_width + self.game_width
        # scroll stage (handled elsewhere), but keep player "still" in the middle area
        else:
            self.real_x_position = self.start_scrolling_pos_x

    def take_damage(self, damage: float) -> None:
        """
        Character hitpoints get removed
        :param damage: number of hitpoints to be removed
        :return:
        """
        self.health -= abs(damage)

    def add_weapon(self, w: Weapon) -> None:
        """
        Adds a weapon to the player's inventory
        :param w:
        :return:
        """
        self.weapons.append(w)

    def add_mystery_weapon(self, weapon: Weapon) -> None:
        """
        Adds a mystery weapon to the player's kit
        :param weapon: weapon to be added
        :return:
        """
        if len(self.weapons) <= 1:
            self.add_weapon(weapon)
            self.switch_to_next_weapon()
        else:
            self.weapons[self.current_weapon] = weapon

    def switch_to_next_weapon(self) -> None:
        """
        Switches to the next weapon in inventory, if available and current weapon isn't being used
        :return:
        """
        if len(self.weapons) == 0:
            self.current_weapon = 0
            return

        old_curr = self.current_weapon
        if not self.get_current_weapon().is_being_used():
            self.current_weapon += 1
            self.current_weapon %= len(self.weapons)

            if old_curr != self.current_weapon and len(self.weapons) > 1:
                old_weapon = self.weapons[old_curr]
                curr_weapon = self.weapons[self.current_weapon]

                # swap in/out sounds
                potential_swap_out_filepath = old_weapon.swap_out_sound_filepath
                potential_swap_in_filepath = curr_weapon.swap_in_sound_filepath
                sound_to_play = (
                    potential_swap_in_filepath
                    if potential_swap_in_filepath is not None
                    else potential_swap_out_filepath
                )
                if sound_to_play is None:
                    sound_to_play = Weapon.GENERIC_WEAPON_SWAP_SOUND_FILEPATH
                play_sound(sound_to_play)

                # play looping sound for weapon active, if exists
                # be sure to stop previous weapon active sound, if existed
                if old_weapon.weapon_active_sound is not None:
                    old_weapon.weapon_active_sound.stop()
                if curr_weapon.weapon_active_sound is not None:
                    curr_weapon.weapon_active_sound.play(-1)

    def get_current_weapon(self) -> Union[Weapon, None]:
        """
        Gets current weapon from weapons list
        :return: Weapon
        """
        if len(self.weapons) == 0:
            return None

        if self.current_weapon >= len(self.weapons):
            self.current_weapon = 0

        return self.weapons[self.current_weapon]

    def remove_current_weapon(self):
        """
        Removes current weapon from player's hands
        """
        old_weapon_index = self.current_weapon
        self.switch_to_next_weapon()
        del self.weapons[old_weapon_index]

    def fire_current_weapon(self) -> None:
        """
        Fires current weapon, if able to
        :return:
        """
        if self.get_current_weapon() == None:
            return
        else:
            self.get_current_weapon().fire()

    def add_points(self, amount: int) -> None:
        """
        Adds amount to points
        :param: amount to add
        :return:
        """
        self.points += amount

    def remove_points(self, amount: int) -> None:
        """
        Removes amount from points
        :param amount:
        :return:
        """
        self.points -= amount
