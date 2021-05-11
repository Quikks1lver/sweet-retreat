# Adam Fernandes
# May 2021
# My first pygame!

import pygame
import random
from typing import List

import background.Background_Methods as bg_methods
from characters.Player import Player
from characters.Enemy import Enemy

# constants
WIDTH, HEIGHT = 800, 600
ENEMY_HEALTH = 50
ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY = 0.15, 0.1
NUM_ENEMIES = 5
PLAYER_HEALTH = 100
PLAYER_X_START, PLAYER_Y_START = 50, 460
PLAYER_X_VELOCITY, PLAYER_Y_VELOCITY = 0.7, 0.3
Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD = 440, 500
COLLISION_THRESHOLD = 25

# initialize the pygame & create screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# background and stage
background = pygame.image.load("images/background.png").convert()
background_width, background_height = background.get_rect().size
stage_width = background_width * 2
stage_pos_x = 0
start_scrolling_pos_x = WIDTH / 2

# init player and enemy characters
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x,
                stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, PLAYER_HEALTH)
enemies: List[Enemy] = []
for i in range(NUM_ENEMIES):
    enemy_img = "gingerbread-man.png" if i % 2 == 0 else "cupcake.png"
    enemies.append(Enemy(f"images/{enemy_img}", random.randint(-WIDTH, WIDTH), PLAYER_Y_START, start_scrolling_pos_x,
                         stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, ENEMY_HEALTH, ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY))

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

    player.move()
    for e in enemies:
        e.move(player)
        player.is_collision(e, COLLISION_THRESHOLD)

    stage_pos_x += bg_methods.determine_stage_change(player)

    bg_methods.draw_background(screen, background, stage_pos_x, background_width, WIDTH)
    player.draw(screen)

    for e in enemies:
        e.draw(screen)

    pygame.display.update()