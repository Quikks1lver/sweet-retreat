# Adam Fernandes
# May 2021
# My first pygame!

import pygame
from characters.Player import Player
import background.Background_Methods as bg_methods

# constants
WIDTH, HEIGHT = 800, 600
PLAYER_X_START, PLAYER_Y_START = 50, 460
PLAYER_X_VELOCITY, PLAYER_Y_VELOCITY = 1.1, 0.3
PLAYER_Y_TOP_THRESHOLD, PLAYER_Y_BOTTOM_THRESHOLD = 440, 500

# initialize the pygame & create screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# background and stage
background = pygame.image.load("images/background.png").convert()
background_width, background_height = background.get_rect().size
stage_width = background_width * 2
stage_pos_x = 0
start_scrolling_pos_x = WIDTH / 2

# init player character
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x,
                stage_width, WIDTH, PLAYER_Y_TOP_THRESHOLD, PLAYER_Y_BOTTOM_THRESHOLD)

running = True
while running:

    for event in pygame.event.get():
        # break out of game loop if user quits
        if event.type == pygame.QUIT:
            running = False

        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: player.set_x_velocity(-PLAYER_X_VELOCITY)
            if event.key == pygame.K_RIGHT: player.set_x_velocity(PLAYER_X_VELOCITY)
            if event.key == pygame.K_UP: player.set_y_velocity(-PLAYER_Y_VELOCITY)
            if event.key == pygame.K_DOWN: player.set_y_velocity(PLAYER_Y_VELOCITY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: player.set_x_velocity(0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN: player.set_y_velocity(0)

    player.move_player()
    stage_pos_x += bg_methods.determine_stage_change(player)

    bg_methods.draw_background(screen, background, stage_pos_x, background_width, WIDTH)
    player.draw_player(screen)
    pygame.display.update()