from typing import List

from characters.Enemy import Enemy
from characters.EnemyFactory import EnemyFactory

class Game_State():
    """
    Deals with game progression
    """
    ice_cream_monster_one: bool = False
    ice_cream_monster_two: bool = False
    ice_cream_monster_three: bool = False

    @staticmethod
    def progress(enemies: List[Enemy], enemy_factory: EnemyFactory, enemies_defeated: int):
        """
        Makes the game harder as more enemies are defeated
        """
        if enemies_defeated > 25 and not Game_State.ice_cream_monster_one:
            enemies.append(enemy_factory.create_ice_cream_monster())
            Game_State.ice_cream_monster_one = True
        if enemies_defeated > 50 and not Game_State.ice_cream_monster_two:
            enemies.append(enemy_factory.create_ice_cream_monster())
            Game_State.ice_cream_monster_two = True
        if enemies_defeated > 75 and not Game_State.ice_cream_monster_three:
            enemies.append(enemy_factory.create_ice_cream_monster())
            Game_State.ice_cream_monster_three = True