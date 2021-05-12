import pygame
from characters.Player import Player

def draw_ammo_box(screen, player: Player, score_cost: int, ammo_gain: int, trying_to_buy: bool) -> None:
    """
    Draws ammo box onto the screen
    :param screen:
    :param player: player character
    :return:
    """
    # draw ammo box and description of cost on left side of screen
    if player.x < player.start_scrolling_pos_x:
        x_start, y_start = 100, 370

        ammo_box_img = pygame.image.load("images/ammo_box.png")
        screen.blit(ammo_box_img, (x_start, y_start))

        font = pygame.font.Font("./fonts/dewangga.otf", 24)
        title = font.render("Press 'B' for Ammo", True, (255, 255, 255))  # white
        score_title = font.render(f"Cost: {score_cost} score", True, (255, 255, 255))  # white
        screen.blit(title, (100, 315))
        screen.blit(score_title, (100, 340))

        if trying_to_buy and player.score >= score_cost:
            if player.x >= x_start and player.x <= (x_start + ammo_box_img.get_width()):
                player.get_current_weapon().add_ammo(ammo_gain)
                player.remove_score(score_cost)

    # draw sparkles when approaching ammo box from right
    if player.x >= player.start_scrolling_pos_x and player.x <= player.start_scrolling_pos_x + 7:
        sparkles_img = pygame.image.load("images/sparkles.png")
        screen.blit(sparkles_img, (100, 370))

def draw_background(screen, background_img, stage_pos_x: int, background_width: int, game_width: int) -> None:
    """
    Draws background onto screen, scrolling if necessary
    This was super helpful: https://www.youtube.com/watch?v=US3HSusUBeI
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

def display_score(screen, score: int) -> None:
    """
    Displays score to the screen
    :param screen:
    :param score:
    :return:
    """
    font = pygame.font.Font("./fonts/dewangga.otf", 40)
    score_text = font.render(f"Score: {str(score)}", True, (255, 255, 255)) # white
    screen.blit(score_text, (20, 20))

def display_ammo(screen, ammo: int) -> None:
    """
    Displays ammo to the screen
    :param screen:
    :param ammo:
    :return:
    """
    font = pygame.font.Font("./fonts/dewangga.otf", 25)
    ammo_bar = ""
    for i in range(ammo): ammo_bar += "I"

    ammo_text = font.render(f"Ammo: {ammo_bar}", True, (255, 255, 255))  # white
    screen.blit(ammo_text, (20, 60))

def game_over(screen, score: int, game_width: int, game_height: int) -> None:
    """
    Displays game over screen
    :param screen:
    :param score:
    :return:
    """
    pygame.mixer.stop()

    screen.fill([0, 0, 0]) # black
    font = pygame.font.Font("./fonts/dewangga.otf", 50)

    game_over_text = font.render("GAME OVER", True, (255, 0, 0)) # red
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))  # red

    screen.blit(game_over_text, (game_width / 2.75, game_height / 2.4))
    screen.blit(score_text, (game_width / 2.75, game_height / 2.4 + 40))