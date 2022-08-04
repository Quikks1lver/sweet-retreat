import pygame
from sys import maxsize
from typing import List

from characters.Enemy import Enemy
from characters.EnemyFactory import EnemyFactory
from color.Colors import Colors
from text.Text import Text
from text.TimedText import Timed_Text
from timing.ClockMethods import Clock_Methods

class Game_State():
    """
    Deals with game progression
    """
    
    # for text running on a timer
    timed_text_helper: Timed_Text = Timed_Text()
    NORMAL_ENEMY_TIMED_TEXT_AMOUNT_SEC = 5
    FINAL_BOSS_TIMED_TEXT_AMOUNT_SEC = 10

    # for adding new enemies to the game
    enemy_addition_cooldown = 0
    ENEMY_ADDITION_COOLDOWN_AMOUNT_MS = 15000 # 15 seconds

    @staticmethod
    def progress(screen, enemies: List[Enemy], enemy_factory: EnemyFactory, num_enemies_defeated: int, num_enemies_defeated_for_victory: int) -> None:
        """
        Makes the game harder as more enemies are defeated
        """
        Game_State.timed_text_helper.run(screen)
        
        if len(enemies) == 1: return # final boss

        if len(enemies) != 1 and num_enemies_defeated == num_enemies_defeated_for_victory:
            Game_State.__add_final_boss(enemies, enemy_factory)
            Game_State.__play_final_boss_sound()
            return

        if num_enemies_defeated == 0: return
        if not Clock_Methods.is_past_this_time(Game_State.enemy_addition_cooldown): return

        if num_enemies_defeated % 25 == 0:
            Game_State.__add_ice_cream_monster(enemies, enemy_factory)
            Game_State.__play_incoming_enemy_sound()
        if num_enemies_defeated % 50 == 0:
            Game_State.__add_brownie_tank(enemies, enemy_factory)

    @staticmethod
    def __play_incoming_enemy_sound() -> None:
        """
        Plays sound/alert of an incoming enemy
        """
        incoming_enemy_sound = pygame.mixer.Sound("sounds/enemies/enemy_incoming.wav")
        incoming_enemy_sound.set_volume(1)
        incoming_enemy_sound.play()

    @staticmethod
    def __play_final_boss_sound() -> None:
        """
        Plays sound/alert of the final boss
        """
        incoming_enemy_sound = pygame.mixer.Sound("sounds/enemies/final_boss_incoming.wav")
        incoming_enemy_sound.set_volume(1)
        incoming_enemy_sound.play()

    @staticmethod
    def __set_cooldown() -> None:
        """
        Sets a cooldown period after the creation of each new enemy
        """
        Game_State.enemy_addition_cooldown = Clock_Methods.get_current_time() + Game_State.ENEMY_ADDITION_COOLDOWN_AMOUNT_MS

    @staticmethod
    def __add_brownie_tank(enemies: List[Enemy], enemy_factory: EnemyFactory) -> None:
        """
        Adds a brownie tank to the game
        """
        enemies.append(enemy_factory.create_brownie_tank())
        Game_State.__set_cooldown()
        Game_State.timed_text_helper.populate_timed_text_parameters("Brownie Tank Incoming",
                                                                    Text.Font.Euro_Horror, 30, Colors.Neon_Orange,
                                                                    (260, 100), Game_State.NORMAL_ENEMY_TIMED_TEXT_AMOUNT_SEC)

    @staticmethod
    def __add_final_boss(enemies: List[Enemy], enemy_factory: EnemyFactory) -> None:
        """
        Adds the final boss to the game, wiping all other enemies away
        """
        enemies.clear()
        enemies.append(enemy_factory.create_final_boss())
        Game_State.__set_cooldown()
        Game_State.timed_text_helper.populate_timed_text_parameters("Harrys own Wedding Cake Incoming",
                                                                    Text.Font.Euro_Horror, 40, Colors.Neon_Yellow,
                                                                    (67, 110), Game_State.FINAL_BOSS_TIMED_TEXT_AMOUNT_SEC)

    @staticmethod
    def __add_ice_cream_monster(enemies: List[Enemy], enemy_factory: EnemyFactory) -> None:
        """
        Adds an ice cream monster to the game
        """
        enemies.append(enemy_factory.create_ice_cream_monster())
        Game_State.__set_cooldown()
        Game_State.timed_text_helper.populate_timed_text_parameters("Ice Cream Monster Incoming",
                                                                    Text.Font.Euro_Horror, 30, Colors.Neon_Orange,
                                                                    (210, 100), Game_State.NORMAL_ENEMY_TIMED_TEXT_AMOUNT_SEC)