import pygame
from characters.Player import Player
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

        font = pygame.font.Font("./fonts/dewangga.otf", 24)
        title = font.render("Press 'B' for Ammo", True, (255, 255, 255))  # white
        score_title = font.render(f"Cost: {cost} points", True, (255, 255, 255))  # white
        screen.blit(title, (x_start, y_start - 55))
        screen.blit(score_title, (x_start, y_start - 30))

        if trying_to_buy and player.points >= cost:
            if player.x >= x_start and player.x <= (x_start + ammo_box_img.get_width()):
                player.get_current_weapon().add_ammo(ammo_gain)
                player.remove_points(cost)

    # draw sparkles when approaching ammo box from right
    if player.x >= player.start_scrolling_pos_x and player.x <= player.start_scrolling_pos_x + 10:
        sparkles_img = pygame.image.load("images/sparkles.png")
        screen.blit(sparkles_img, (x_start, y_start))

def draw_mystery_box(screen, player: Player, cost: int, trying_to_buy: bool) -> None:
    """
    Draws ammo box onto the screen
    :param screen:
    :param player: player character
    :param cost:
    :param trying_to_buy: whether player is trying to buy ammo or not
    :return:
    """
    x_start, y_start = 600, 370
    sparkles_threshold = player.stage_width - player.start_scrolling_pos_x

    # draw mystery box and description of cost on right side of screen
    if player.x >= sparkles_threshold:
        x_start, y_start = 600, 370

        mystery_box_img = pygame.image.load("images/mystery_box.png")
        screen.blit(mystery_box_img, (x_start, y_start))

        font = pygame.font.Font("./fonts/dewangga.otf", 24)
        title = font.render("Press 'B' for Mystery Weapon", True, (255, 255, 255))  # white
        score_title = font.render(f"Cost: {cost} points", True, (255, 255, 255))  # white
        screen.blit(title, (x_start - 70, y_start - 55))
        screen.blit(score_title, (x_start - 10, y_start - 30))

        if trying_to_buy and player.points >= cost:
            if player.real_x_position >= x_start and player.real_x_position <= (x_start + mystery_box_img.get_width()):
                # TODO
                player.remove_points(cost)

    # draw sparkles when approaching mystery box from left
    if player.x > sparkles_threshold - 10 and player.x < sparkles_threshold:
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
    font = pygame.font.Font("./fonts/dewangga.otf", 40)
    score_text = font.render(f"Points: {str(points)}", True, (255, 255, 255)) # white
    screen.blit(score_text, (20, 20))

def display_ammo(screen, weapon: Weapon) -> None:
    """
    Displays ammo to the screen
    :param screen:
    :param weapon:
    :return:
    """
    font = pygame.font.Font("./fonts/dewangga.otf", 25)
    ammo_bar = ""
    for i in range(weapon.ammo): ammo_bar += "I"

    weapon_name_text = font.render(f"{weapon.name} ", True, (77, 255, 77))  # neon green
    ammo_text = font.render(f"ammo: {ammo_bar}", True, (255, 255, 255))  # white
    screen.blit(weapon_name_text, (20, 60))
    screen.blit(ammo_text, (20 + weapon_name_text.get_width(), 60))

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
    large_font = pygame.font.Font("./fonts/dewangga.otf", 50)
    small_font = pygame.font.Font("./fonts/dewangga.otf", 35)

    game_over_text = large_font.render("GAME OVER", True, (255, 0, 0)) # red
    score_text = small_font.render(f"Enemies Defeated: {score}", True, (255, 0, 0))  # red

    screen.blit(game_over_text, (game_width / 2.75, game_height / 2.4))
    screen.blit(score_text, (game_width / 2.75, game_height / 2.4 + 50))