import pygame

from characters.Player import Player
from text.Text import Text
from weapons.Weapon import Weapon

def draw_ammo_box(screen, player: Player, cost: int, ammo_gain: int, trying_to_buy: bool) -> None:
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
        ammo_box_img = pygame.image.load("images/ammo_box.png")
        screen.blit(ammo_box_img, (x_start, y_start))

        Text.render(screen, "Press 'B' for Ammo", Text.Font.Dewangga, 24, (255, 255, 255), (x_start, y_start - 55))
        Text.render(screen, f"Cost: {cost} points", Text.Font.Dewangga, 24, (255, 255, 255), (x_start, y_start - 30))

        if trying_to_buy and player.points >= cost:
            if player.x >= x_start and player.x <= (x_start + ammo_box_img.get_width()):
                player.get_current_weapon().add_ammo(ammo_gain)
                player.remove_points(cost)

    # draw sparkles when approaching ammo box from right
    if player.x >= player.start_scrolling_pos_x and player.x <= player.start_scrolling_pos_x + 10:
        sparkles_img = pygame.image.load("images/sparkles.png")
        screen.blit(sparkles_img, (x_start, y_start))

def draw_background(screen, background_img, stage_pos_x: int, background_width: int, game_width: int) -> None:
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
    if not player.x < player.start_scrolling_pos_x and not player.x > player.stage_width - player.start_scrolling_pos_x:
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
    Text.render(screen, f"Points: {str(points)}", Text.Font.Dewangga, 40, (255, 255, 255), (20, 20))

def display_ammo(screen, weapon: Weapon) -> None:
    """
    Displays ammo to the screen
    :param screen:
    :param weapon:
    :return:
    """
    ammo_bar = ""
    for i in range(weapon.ammo): ammo_bar += "I"

    weapon_name_width = Text.render(screen, f"{weapon.name} ", Text.Font.Dewangga, 25, (77, 255, 77), (20, 60))
    Text.render(screen, f"ammo: {ammo_bar}", Text.Font.Dewangga, 25, (255, 255, 255), (20 + weapon_name_width, 60))

def game_over(screen, score: int, game_width: int, game_height: int) -> None:
    """
    Displays game over screen
    :param screen:
    :param score:
    :param game_width:
    :param game_height:
    :return:
    """
    pygame.mixer.stop()

    screen.fill([0, 0, 0]) # black

    Text.render(screen, "GAME OVER", Text.Font.Dewangga, 50, (255, 0, 0), (game_width / 2.75, game_height / 2.4))
    Text.render(screen, f"Enemies Defeated: {score}", Text.Font.Dewangga, 35, (255, 0, 0), (game_width / 2.75, game_height / 2.4 + 50))