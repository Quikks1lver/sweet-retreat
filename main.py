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
ENEMY_HIT = .1
ENEMY_HEALTH = 50
ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY = 0.07, 0.1
NUM_ENEMIES = 5
PLAYER_HEALTH = 100
PLAYER_X_START, PLAYER_Y_START = 50, 460
PLAYER_X_VELOCITY, PLAYER_Y_VELOCITY = 0.5, 0.3
Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD = 440, 530
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
background_collision = pygame.image.load("images/background_collision.png").convert()

# init player and enemy characters
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x,
                stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, PLAYER_HEALTH)
enemies: List[Enemy] = []

# DEBUGGING
# enemies.append(Enemy(f"images/cupcake.png", PLAYER_X_START + 10, PLAYER_Y_START,
#                      start_scrolling_pos_x,
#                      stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, ENEMY_HEALTH, ENEMY_X_VELOCITY,
#                      ENEMY_Y_VELOCITY))

for i in range(NUM_ENEMIES):
    enemy_img = "gingerbread-man.png" if random.randint(0, 1) == 0 else "cupcake.png"
    bounds = [-.5 * stage_width, 0] if random.randint(0, 1) == 0 else [stage_width, 1.5 * stage_width]
    enemies.append(Enemy(f"images/{enemy_img}", PLAYER_X_START + random.randint(bounds[0], bounds[1]), PLAYER_Y_START, start_scrolling_pos_x,
                         stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, ENEMY_HEALTH, ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY))

# game states
def game_over(screen) -> None:
    """
    Displays game over screen
    :return:
    """
    screen.fill([0, 0, 0]) # black
    font = pygame.font.Font("./fonts/dewangga.otf", 50)
    health_status = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(health_status, (WIDTH / 2.75, HEIGHT / 2))

collision = False
running = True
while running:
    collision = False

    # event handlers
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

    # move all characters
    player.move()
    for e in enemies:
        e.move(player)
        if e.has_collision(player, COLLISION_THRESHOLD):
            player.take_damage(ENEMY_HIT)
            collision = True

    # move stage if need be
    stage_pos_x += bg_methods.determine_stage_change(player)

    # draw everyone to screen
    bg_methods.draw_background(screen, background_collision if collision else background, stage_pos_x, background_width, WIDTH)
    player.draw(screen)
    for e in enemies: e.draw(screen, player)

    # game over screen
    if player.health <= 0: game_over(screen)

    # update display
    pygame.display.update()