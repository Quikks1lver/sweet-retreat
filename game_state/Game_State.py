
from sys import maxsize
from typing import List

from characters.Enemy import Enemy
from characters.EnemyFactory import EnemyFactory
from timing.Clock_Methods import Clock_Methods

class Game_State():
    """
    Deals with game progression
    """
    cooldown = 0
    COOLDOWN_AMOUNT = 15000 # 15 seconds

    @staticmethod
    def progress(enemies: List[Enemy], enemy_factory: EnemyFactory, num_enemies_defeated: int) -> None:
        """
        Makes the game harder as more enemies are defeated
        """
        if num_enemies_defeated == 0: return
        if not Clock_Methods.is_past_this_time(Game_State.cooldown): return

        if num_enemies_defeated % 25 == 0: Game_State.__add_ice_cream_monster(enemies, enemy_factory)
        if num_enemies_defeated % 50 == 0: Game_State.__add_brownie_tank(enemies, enemy_factory)
        
    @staticmethod
    def __set_cooldown() -> None:
        """
        Sets a cooldown period after the creation of each new enemy
        """
        Game_State.cooldown = Clock_Methods.get_current_time() + Game_State.COOLDOWN_AMOUNT

    @staticmethod
    def __add_brownie_tank(enemies: List[Enemy], enemy_factory: EnemyFactory) -> None:
        """
        Adds a brownie tank to the game
        """
        enemies.append(enemy_factory.create_brownie_tank())
        Game_State.__set_cooldown()

    @staticmethod
    def __add_ice_cream_monster(enemies: List[Enemy], enemy_factory: EnemyFactory) -> None:
        """
        Adds an ice cream monster to the game
        """
        enemies.append(enemy_factory.create_ice_cream_monster())
        Game_State.__set_cooldown()