import random

from .Enemy import Enemy

class EnemyFactory():
    """
    A way to easily create pre-set enemies
    """

    def __init__(self, stage_width: int, game_width: int, y_start: int, y_top_threshold: int, y_bottom_threshold: int, start_scrolling_pos_x: int):
        """
        Creates an EnemyFactory object
        """
        self.stage_width = stage_width
        self.game_width = game_width
        self.y_start = y_start
        self.y_top_threshold = y_top_threshold
        self.y_bottom_threshold = y_bottom_threshold
        self.start_scrolling_pos_x = start_scrolling_pos_x

    def create_basic_enemy(self) -> Enemy:
        """
        Returns a random-looking basic enemy
        """
        damage = .3
        health = 50
        x_velocity, y_velocity = 0.4, 0.1
        enemy_img = "gingerbread-man" if random.randint(0, 1) == 0 else "cupcake"
        enemy_start = self.stage_width + 200 if random.randint(0, 1) == 0 else -200
        point_gain_on_hit, point_gain_on_defeat = 1, 11

        return Enemy(f"images/characters/{enemy_img}.png", enemy_start, self.y_start, self.start_scrolling_pos_x,
                     self.stage_width, self.game_width, self.y_top_threshold, self.y_bottom_threshold, health,
                     x_velocity, y_velocity, damage, point_gain_on_hit, point_gain_on_defeat)
    
    def create_ice_cream_monster(self) -> Enemy:
        """
        Returns a fast ice cream enemy
        """
        damage = .1
        health = 40
        x_velocity, y_velocity = 1.2, 0.5
        enemy_start = self.stage_width + 300 if random.randint(0, 1) == 0 else -300
        point_gain_on_hit, point_gain_on_defeat = 1, 25

        return Enemy(f"images/characters/ice-cream.png", enemy_start, self.y_start, self.start_scrolling_pos_x,
                     self.stage_width, self.game_width, self.y_top_threshold, self.y_bottom_threshold, health,
                     x_velocity, y_velocity, damage, point_gain_on_hit, point_gain_on_defeat)
    
    def create_brownie_tank(self) -> Enemy:
        """
        Returns a tanky brownie enemy
        """
        damage = 1
        health = 500
        x_velocity, y_velocity = 0.2, 0.1
        enemy_start = self.stage_width + 100 if random.randint(0, 1) == 0 else -100
        point_gain_on_hit, point_gain_on_defeat = 5, 100

        return Enemy(f"images/characters/brownie.png", enemy_start, self.y_start, self.start_scrolling_pos_x,
                     self.stage_width, self.game_width, self.y_top_threshold, self.y_bottom_threshold, health,
                     x_velocity, y_velocity, damage, point_gain_on_hit, point_gain_on_defeat)

    def create_final_boss(self) -> Enemy:
        """
        Returns the final boss enemy
        """
        damage = 3
        health = 2000
        x_velocity, y_velocity = .7, .1
        enemy_start = self.stage_width + 100 if random.randint(0, 1) == 0 else -100
        point_gain_on_hit, point_gain_on_defeat = 10, 1000
        blitted_health_offset_x, blitted_health_offset_y = 40, 120

        return Enemy(f"images/characters/wedding_cake.png", enemy_start, self.y_start, self.start_scrolling_pos_x,
                     self.stage_width, self.game_width, self.y_top_threshold, self.y_bottom_threshold, health,
                     x_velocity, y_velocity, damage, point_gain_on_hit, point_gain_on_defeat,
                     blitted_health_offset_x, blitted_health_offset_y)