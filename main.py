# Adam Fernandes
# May 2021
# My first pygame!

import pygame
import random
from typing import List

import background.Background_Methods as bg_methods
from background.MysteryBox import MysteryBox
from background.Screens import Screens
from background.StartScreen import Start_Screen
from characters.Player import Player
from characters.Enemy import Enemy, Enemy_Collision
from characters.EnemyFactory import EnemyFactory
from weapons.Arsenal import Arsenal

# constants
WIDTH, HEIGHT = 800, 600

NUM_ENEMIES = 5

PLAYER_HEALTH = 100
PLAYER_X_START, PLAYER_Y_START = 50, 460
PLAYER_X_VELOCITY, PLAYER_Y_VELOCITY = 5, 2

AMMO_COST, AMMO_GAIN = 50, 25
MYSTERY_BOX_COST = 100

Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD = 440, 530
COLLISION_THRESHOLD = 25

# initialize the pygame & create screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# game header/caption and icon
pygame.display.set_caption("Sweet Retreat")
pygame.display.set_icon(pygame.image.load("images/cookie.png"))

# background and stage
background = pygame.image.load("images/background.png").convert()
background_width, background_height = background.get_rect().size
stage_width = background_width * 2
stage_pos_x = 0
start_scrolling_pos_x = WIDTH / 2
background_collision = pygame.image.load("images/background_collision.png").convert()

# sounds
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")

# init player and enemy characters
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x,
                stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, PLAYER_HEALTH)
player.add_weapon(Arsenal.revolver(player))

enemy_factory = EnemyFactory(stage_width, WIDTH, PLAYER_Y_START, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, start_scrolling_pos_x)
enemies: List[Enemy] = [enemy_factory.create_basic_enemy() for i in range(NUM_ENEMIES)]
enemies.append(enemy_factory.create_ice_cream_monster())

# init mystery box
mystery_box = MysteryBox()

# init starting screens
splash_screen = Start_Screen("images/splash_screen.png")
lore_screen = Start_Screen("images/lore_screen.png")
directions_screen = Start_Screen("images/directions_screen.png")

# important flags and variables for main game loop
collision = False
running = True
died = False
final_score = 0
enemies_defeated = 0
SCREEN = 1

# game loop
while running:
    current_time = pygame.time.get_ticks()

    collision = False
    trying_to_buy_item = False
    trying_to_pick_up_weapon = False

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if SCREEN < Screens.GAME.value and event.key == pygame.K_RETURN: SCREEN += 1
            if SCREEN < Screens.GAME.value: break
            if event.key == pygame.K_LEFT: player.set_x_velocity(-PLAYER_X_VELOCITY)
            if event.key == pygame.K_RIGHT: player.set_x_velocity(PLAYER_X_VELOCITY)
            if event.key == pygame.K_UP: player.set_y_velocity(-PLAYER_Y_VELOCITY)
            if event.key == pygame.K_DOWN: player.set_y_velocity(PLAYER_Y_VELOCITY)
            if event.key == pygame.K_SPACE: player.fire_current_weapon()
            if event.key == pygame.K_b: trying_to_buy_item = True
            if event.key == pygame.K_c: trying_to_pick_up_weapon = True
            if event.key == pygame.K_v: player.switch_to_next_weapon()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: player.set_x_velocity(0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN: player.set_y_velocity(0)

    # check which screen we're on
    if SCREEN < Screens.GAME.value:
        if SCREEN == Screens.SPLASH.value: splash_screen.draw(screen)
        elif SCREEN == Screens.LORE.value: lore_screen.draw(screen)
        elif SCREEN == Screens.DIRECTIONS.value: directions_screen.draw(screen)
        else: pass
        
        # immediately update display and continue if on starting few screens
        pygame.display.update()
        continue

    # move all characters
    player.move()
    for e in enemies:
        e.move(player)
        if e.has_collision_with_player(player, COLLISION_THRESHOLD):
            player.take_damage(e.damage_amount())
            collision = True

    # move stage if need be
    stage_pos_x += bg_methods.determine_stage_change(player)

    # draw everything to screen; also, check for bullet collisions here
    bg_methods.draw_background(screen, background_collision if collision else background, stage_pos_x, background_width, WIDTH)
    bg_methods.draw_ammo_box(screen, player, AMMO_COST, AMMO_GAIN, trying_to_buy_item)
    mystery_box.draw(screen, player, MYSTERY_BOX_COST, trying_to_buy_item, trying_to_pick_up_weapon)
    player.draw(screen)
    for e in enemies:
        e.draw(screen)

        collision_type = e.check_for_bullet_collision(player.get_current_weapon().bullet, COLLISION_THRESHOLD)
        if collision_type == Enemy_Collision.HIT:
            player.add_points(e.get_point_gain_on_hit())
        elif collision_type == Enemy_Collision.DEFEATED:
            player.add_points(e.get_point_gain_on_defeat())
            explosion_sound.play()
            enemies_defeated += 1

    # draw score & ammo metadata
    bg_methods.display_points(screen, player.points)
    bg_methods.display_ammo(screen, player.get_current_weapon())

    # game over screen
    if player.health <= 0:
        if not died:
            final_score = enemies_defeated
            died = True
        bg_methods.game_over(screen, enemies_defeated, WIDTH, HEIGHT)

    # update display
    pygame.display.update()