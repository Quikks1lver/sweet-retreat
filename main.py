# Adam Fernandes
# May 2021
# My first pygame!

import pygame
from characters.Player import Player

# constants
WIDTH, HEIGHT = 800, 600
PLAYER_X_START, PLAYER_Y_START = 50, 460
PLAYER_X_VELOCITY, PLAYER_Y_VELOCITY = 2, 2

# initialize the pygame & create screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# background and stage
background = pygame.image.load("images/background.png").convert()
background_width, background_height = background.get_rect().size
stage_width = background_width * 2
stage_pos_x = 0
start_scrolling_pos_x = WIDTH / 2

def draw_background() -> None:
    """
    Draws background onto screen, scrolling if necessary
    This was super helpful: https://www.youtube.com/watch?v=US3HSusUBeI
    :return:
    """
    # get relative x position, and subtract background width to ensure background can be seen
    rel_x = stage_pos_x % background_width
    screen.blit(background, (rel_x - background_width, 0))

    # seamlessly blit another background when relative pos is less than display surface width
    if rel_x < WIDTH:
        screen.blit(background, (rel_x, 0))

# init player character
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x, stage_width, WIDTH)

running = True
while running:

    for event in pygame.event.get():
        # break out of game loop if user quits
        if event.type == pygame.QUIT:
            running = False

        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.set_x_velocity(-PLAYER_X_VELOCITY)
            if event.key == pygame.K_RIGHT:
                player.set_x_velocity(PLAYER_X_VELOCITY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.set_x_velocity(0)

    player.move_player()

    # move stage itself when player is in "middle" portion of display
    if not player.x < player.start_scrolling_pos_x and not player.x > player.stage_width - player.start_scrolling_pos_x:
        stage_pos_x += -player.x_velocity

    draw_background()
    player.draw_player(screen)
    pygame.display.update()