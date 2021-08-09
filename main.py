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
from game_state.Game_State import Game_State
from timing.Clock_Methods import Clock_Methods
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
NUM_ENEMIES_DEFEATED_FOR_VICTORY = 200
PAUSE_START_FLAG = -1
SCREEN = 1

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
enemy_explosion = pygame.image.load("images/enemy_explosion.png")

# background music
pygame.mixer.music.load("sounds/background_music.wav")
pygame.mixer.music.play(-1)

# sounds
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")

# init player and starting enemy characters
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x,
                stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, PLAYER_HEALTH)
player.add_weapon(Arsenal.revolver(player))

enemy_factory = EnemyFactory(stage_width, WIDTH, PLAYER_Y_START, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, start_scrolling_pos_x)
enemies: List[Enemy] = [enemy_factory.create_basic_enemy() for i in range(NUM_ENEMIES)]

# init mystery box
mystery_box = MysteryBox()

# init starting screens
splash_screen = Start_Screen("images/splash_screen.png")
lore_screen = Start_Screen("images/lore_screen.png")
directions_screen = Start_Screen("images/directions_screen.png")

# important flags and variables for main game loop
collision: bool = False
pause: bool = False
running: bool = True
game_has_started = False
died: bool = False
pause_started: bool = False
victory: bool = False
final_score: int = 0
uncounted_time: float = 0
pause_time_start: float = PAUSE_START_FLAG
time_survived: float = 0
num_enemies_defeated: int = 0

# game loop
while running:
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
            if event.key == pygame.K_ESCAPE: pause = not pause
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: player.set_x_velocity(0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN: player.set_y_velocity(0)
    if pygame.key.get_pressed()[pygame.K_SPACE] and player.get_current_weapon().is_full_auto(): player.fire_current_weapon() # full auto

    # check which screen we're on
    if SCREEN < Screens.GAME.value:
        if SCREEN == Screens.SPLASH.value: splash_screen.draw(screen)
        elif SCREEN == Screens.LORE.value: lore_screen.draw(screen)
        elif SCREEN == Screens.DIRECTIONS.value: directions_screen.draw(screen)
        else: pass
        
        # immediately update display and continue if on starting few screens
        pygame.display.update()
        continue

    # log the exact time the player actually begins the game
    if not game_has_started and SCREEN == Screens.GAME.value:
        game_has_started = True
        uncounted_time = Clock_Methods.get_current_time_in_seconds(2)

    # victory screen; play victory music, too
    if num_enemies_defeated > NUM_ENEMIES_DEFEATED_FOR_VICTORY:
        if not victory:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/victory_music.wav")
            pygame.mixer.music.play(-1)
            time_survived = Clock_Methods.get_time_survived(uncounted_time, 2)
            victory = True
        bg_methods.victory(screen, time_survived, WIDTH, HEIGHT)
        pygame.display.update()
        continue

    # game over screen
    if player.health <= 0:
        if not died:
            final_score = num_enemies_defeated
            time_survived = Clock_Methods.get_time_survived(uncounted_time, 2)
            died = True
        bg_methods.game_over(screen, final_score, time_survived, WIDTH, HEIGHT)
        pygame.display.update()
        continue

    # pause game & log how much time is spent in pause screen to uncounted time
    if pause:
        if not pause_started:
            pause_started = True
            pause_time_start = Clock_Methods.get_current_time_in_seconds(2)
        bg_methods.pause(screen, WIDTH, HEIGHT)
        pygame.display.update()
        continue
    else:
        pause_started = False
        if pause_time_start != PAUSE_START_FLAG:
            pause_time_delta = Clock_Methods.get_current_time_in_seconds(2) - pause_time_start
            uncounted_time += pause_time_delta
            pause_time_start = PAUSE_START_FLAG

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

        enemy_pos_x, enemy_pos_y = e.real_x_position, e.y

        collision_type = e.check_for_bullet_collision(player.get_current_weapon().bullet, COLLISION_THRESHOLD)
        if collision_type == Enemy_Collision.HIT:
            player.add_points(e.get_point_gain_on_hit())
        elif collision_type == Enemy_Collision.DEFEATED:
            player.add_points(e.get_point_gain_on_defeat())
            explosion_sound.play()
            screen.blit(enemy_explosion, (enemy_pos_x - 5, enemy_pos_y - 10))
            num_enemies_defeated += 1

    # draw score & ammo metadata
    bg_methods.display_points(screen, player.points)
    bg_methods.display_ammo(screen, player.get_current_weapon())

    # progress game
    Game_State.progress(enemies, enemy_factory, num_enemies_defeated)

    # update display
    pygame.display.update()