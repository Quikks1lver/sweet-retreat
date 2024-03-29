import pygame

from .SoundHelpers import play_sound
from characters.Player import Player
from color.Colors import Colors
from text.Text import Text
from weapons.Weapon import Weapon


def draw_ammo_box(
    screen, player: Player, cost: int, ammo_gain: int, trying_to_buy: bool
) -> None:
    """
    Draws ammo box onto the screen
    :param screen:
    :param player: player character
    :param cost: how much ammo costs
    :param ammo_gain: how much ammo player will gain from buying
    :param trying_to_buy: whether player is trying to buy ammo or not
    :return:
    """
    x_start, y_start = 100, 370

    # draw ammo box and description of cost on left side of screen
    if player.x < player.start_scrolling_pos_x:
        ammo_box_img = pygame.image.load("images/stage/ammo_box.png")
        screen.blit(ammo_box_img, (x_start, y_start))

        Text.render(
            screen,
            "Press B for Ammo",
            Text.Font.Euro_Horror,
            18,
            Colors.Neon_Cyan,
            (x_start, y_start - 55),
        )
        Text.render(
            screen,
            f"Costs {cost} points",
            Text.Font.Euro_Horror,
            18,
            Colors.Neon_Cyan,
            (x_start, y_start - 30),
        )

        # if player has enough points and is in bounds of box, allow them to buy
        if trying_to_buy and player.points >= cost:
            if (
                player.x >= x_start
                and player.x <= (x_start + ammo_box_img.get_width())
                and player.y >= y_start
                and player.y <= (y_start + ammo_box_img.get_height())
            ):
                player.get_current_weapon().add_ammo(ammo_gain)
                player.remove_points(cost)
                play_sound("background/ammo_box.wav")

    # draw sparkles when approaching ammo box from right
    if (
        player.x >= player.start_scrolling_pos_x
        and player.x <= player.start_scrolling_pos_x + 10
    ):
        sparkles_img = pygame.image.load("images/stage/sparkles.png")
        screen.blit(sparkles_img, (x_start, y_start))


def draw_background(
    screen, background_img, stage_pos_x: int, background_width: int, game_width: int
) -> None:
    """
    Draws background onto screen, scrolling if necessary
    This was super helpful: https://www.youtube.com/watch?v=US3HSusUBeI
    :param screen:
    :param background_img:
    :param stage_pos_x:
    :param background_width:
    :param game_width:
    :return:
    """
    # get relative x position, and subtract background width to ensure background can be seen
    rel_x = stage_pos_x % background_width
    screen.blit(background_img, (rel_x - background_width, 0))

    # seamlessly blit another background when relative pos is less than display surface width
    if rel_x < game_width:
        screen.blit(background_img, (rel_x, 0))


def determine_stage_change(player: Player) -> int:
    """
    Determines what the change in stage position is (for scrolling the background)
    :param player:
    :return:
    """
    # move stage itself when player is in "middle" portion of display
    if (
        not player.x < player.start_scrolling_pos_x
        and not player.x > player.stage_width - player.start_scrolling_pos_x
    ):
        return -player.x_velocity
    else:
        return 0


def display_points(screen, points: int) -> None:
    """
    Displays score to the screen
    :param screen:
    :param points:
    :return:
    """
    Text.render(
        screen,
        f"Points: {str(points)}",
        Text.Font.Dewangga,
        40,
        Colors.Neon_Green,
        (20, 20),
    )


def display_ammo(screen, weapon: Weapon, width: int) -> None:
    """
    Displays ammo to the screen
    :param screen:
    :param weapon:
    :param width: width of screen
    :return:
    """
    cushion = 20
    width_of_i = 7

    if weapon is None:
        return

    weapon_name_color = (
        Colors.Neon_Magenta if weapon.is_upgraded else Colors.Neon_Yellow
    )

    weapon_name_width = Text.render(
        screen,
        f"{weapon.name} ",
        Text.Font.Euro_Horror,
        20,
        weapon_name_color,
        (20, 60),
    )
    threshold = width - cushion - weapon_name_width
    weapon_text = (
        weapon.ammo
        if width_of_i * weapon.ammo >= threshold
        else weapon.get_ammo_string()
    )
    Text.render(
        screen,
        f"{weapon_text}",
        Text.Font.Dewangga,
        25,
        Colors.White,
        (cushion + weapon_name_width, 60),
    )


def game_over(
    screen, score: int, time_survived: float, game_width: int, game_height: int
) -> None:
    """
    Displays game over screen
    :param screen:
    :param score:
    :param time_survived: in seconds
    :param game_width:
    :param game_height:
    :return:
    """
    pygame.mixer.stop()

    screen.fill(Colors.Black)

    Text.render(
        screen,
        "There is no Escape",
        Text.Font.Dewangga,
        50,
        Colors.Red,
        (game_width / 3.5, game_height / 2.4),
    )
    Text.render(
        screen,
        f"Sweets Conquered: {score}",
        Text.Font.Dewangga,
        35,
        Colors.Neon_Magenta,
        (game_width / 3.5, game_height / 2.4 + 50),
    )
    Text.render(
        screen,
        f"Time Elapsed: {time_survived} s",
        Text.Font.Dewangga,
        35,
        Colors.Neon_Magenta,
        (game_width / 3.5, game_height / 2.4 + 85),
    )


def pause(screen, game_width: int, game_height: int) -> None:
    """
    Displays pause screen
    :param screen:
    :param game_width:
    :param game_height:
    :return:
    """
    screen.fill(Colors.Black)

    Text.render(
        screen,
        "PAUSE ||",
        Text.Font.Dewangga,
        50,
        Colors.Neon_Green,
        (game_width / 2.6, game_height / 2.4),
    )


def victory(screen, time_survived: float, game_width: int, game_height: int) -> None:
    """
    Displays victory screen
    :param screen:
    :param time_survived: in seconds
    :param game_width:
    :param game_height:
    :return:
    """
    screen.fill(Colors.Medium_Purple)

    Text.render(
        screen,
        f"Victory! ({time_survived} s)",
        Text.Font.Dewangga,
        50,
        Colors.Neon_Cyan,
        (game_width / 3.5, game_height / 2.4),
    )
    Text.render(
        screen,
        "You have conquered your vices.",
        Text.Font.Dewangga,
        35,
        Colors.Neon_Green,
        (game_width / 3.5, game_height / 2.4 + 50),
    )
    Text.render(
        screen,
        "Welcome to the Oasis . . .",
        Text.Font.Dewangga,
        35,
        Colors.White,
        (game_width / 3.5, game_height / 2.4 + 85),
    )
