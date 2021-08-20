
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
    TIMED_TEXT_AMOUNT_SEC = 3

    # for adding new enemies to the game
    enemy_addition_cooldown = 0
    ENEMY_ADDITION_COOLDOWN_AMOUNT_MS = 15000 # 15 seconds

    @staticmethod
    def progress(screen, enemies: List[Enemy], enemy_factory: EnemyFactory, num_enemies_defeated: int) -> None:
        """
        Makes the game harder as more enemies are defeated
        """
        Game_State.timed_text_helper.run(screen)

        if num_enemies_defeated == 0: return
        if not Clock_Methods.is_past_this_time(Game_State.enemy_addition_cooldown): return

        if num_enemies_defeated % 25 == 0: Game_State.__add_ice_cream_monster(enemies, enemy_factory)
        if num_enemies_defeated % 50 == 0: Game_State.__add_brownie_tank(enemies, enemy_factory)

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
                                                                    (260, 100), Game_State.TIMED_TEXT_AMOUNT_SEC)

    @staticmethod
    def __add_ice_cream_monster(enemies: List[Enemy], enemy_factory: EnemyFactory) -> None:
        """
        Adds an ice cream monster to the game
        """
        enemies.append(enemy_factory.create_ice_cream_monster())
        Game_State.__set_cooldown()
        Game_State.timed_text_helper.populate_timed_text_parameters("Ice Cream Monster Incoming",
                                                                    Text.Font.Euro_Horror, 30, Colors.Neon_Orange,
                                                                    (210, 100), Game_State.TIMED_TEXT_AMOUNT_SEC)