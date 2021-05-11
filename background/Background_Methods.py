import pygame
from characters.Player import Player

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

def game_over(screen, score: int, game_width: int, game_height: int) -> None:
    """
    Displays game over screen
    :param screen:
    :param score:
    :return:
    """
    screen.fill([0, 0, 0]) # black
    font = pygame.font.Font("./fonts/dewangga.otf", 50)

    game_over_text = font.render("GAME OVER", True, (255, 0, 0)) # red
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))  # red

    screen.blit(game_over_text, (game_width / 2.75, game_height / 2.4))
    screen.blit(score_text, (game_width / 2.75, game_height / 2.4 + 40))