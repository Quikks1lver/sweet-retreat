# Adam Fernandes
# May 2021
# My first pygame!

import pygame
import random
from typing import List

import background.Background_Methods as bg_methods
from background.MysteryBox import MysteryBox
from background.Scenes import Scenes
from background.StartScreen import Start_Screen
from characters.Player import Player
from characters.Enemy import Enemy, Enemy_Collision
from weapons.Arsenal import Arsenal

# constants
WIDTH, HEIGHT = 800, 600

NUM_ENEMIES = 5
ENEMY_HIT = .5
ENEMY_HEALTH = 50
ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY = 0.4, 0.1
ENEMY_HIT_POINTS = 1
ENEMY_DEFEATED_POINTS = 11

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

# background and stage
background = pygame.image.load("images/background.png").convert()
background_width, background_height = background.get_rect().size
stage_width = background_width * 2
stage_pos_x = 0
start_scrolling_pos_x = WIDTH / 2
background_collision = pygame.image.load("images/background_collision.png").convert()

# sounds
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")

# init player and enemy characters, and MysteryBox
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x,
                stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, PLAYER_HEALTH)
player.add_weapon(Arsenal.revolver(player))

enemies: List[Enemy] = []
for i in range(NUM_ENEMIES):
    enemy_img = "gingerbread-man" if random.randint(0, 1) == 0 else "cupcake"
    enemy_start = stage_width + 200 if random.randint(0, 1) == 0 else -200
    enemies.append(Enemy(f"images/{enemy_img}.png", enemy_start, PLAYER_Y_START, start_scrolling_pos_x,
                         stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, ENEMY_HEALTH, ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY))

mystery_box = MysteryBox()

# init starting scenes
splash_screen = Start_Screen("images/splash_screen.png")
lore_screen = Start_Screen("images/lore.png")
directions_screen = Start_Screen("images/directions.png")

# important flags and variables for main game loop
collision = False
running = True
died = False
final_score = 0
enemies_defeated = 0
SCENE = 1

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
            if SCENE < Scenes.GAME.value and event.key == pygame.K_RETURN: SCENE += 1
            if SCENE < Scenes.GAME.value: break
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

    # check which scene we're on
    if SCENE < Scenes.GAME.value:
        if SCENE == Scenes.SPLASH.value: splash_screen.draw(screen)
        elif SCENE == Scenes.LORE.value: lore_screen.draw(screen)
        elif SCENE == Scenes.DIRECTIONS.value: directions_screen.draw(screen)
        else: pass
        
        # immediately update display and continue if on starting few screens
        pygame.display.update()
        continue

    # move all characters
    player.move()
    for e in enemies:
        e.move(player)
        if e.has_collision_with_player(player, COLLISION_THRESHOLD):
            player.take_damage(ENEMY_HIT)
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
            player.add_points(ENEMY_HIT_POINTS)
        elif collision_type == Enemy_Collision.DEFEATED:
            player.add_points(ENEMY_DEFEATED_POINTS)
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