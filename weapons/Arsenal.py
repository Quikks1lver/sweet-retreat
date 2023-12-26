from .Weapon import Weapon
from characters import Player


class Arsenal:
    """
    A collection of weapons the player character can use
    """

    IMG_WEAPONS_FILEPATH = "images/weapons"
    IMG_BULLETS_FILEPATH = "images/bullets"
    SOUND_WEAPONS_FILEPATH = "sounds/weapons"

    @staticmethod
    def __weapon_builder(
        name: str,
        image_filename: str,
        sound_filename: str,
        bullet_filename: str,
        character: Player.Player,
        projectile_x_velocity: float,
        damage: float,
        ammo: int,
        full_auto: bool = False,
        max_bullet_dist: int = None,
        swap_out_sound_filepath: str = None,
        swap_in_sound_filepath: str = None,
        sound_volume: float = 0.2,
        weapon_active_sound_filepath: str = None,
    ) -> Weapon:
        """
        Returns a weapon object, with some metadata for filepaths filled in
        """
        return Weapon(
            name,
            f"{Arsenal.IMG_WEAPONS_FILEPATH}/{image_filename}",
            f"{Arsenal.SOUND_WEAPONS_FILEPATH}/{sound_filename}",
            f"{Arsenal.IMG_BULLETS_FILEPATH}/{bullet_filename}",
            character,
            projectile_x_velocity,
            damage,
            ammo,
            full_auto,
            max_bullet_dist,
            swap_out_sound_filepath=swap_out_sound_filepath,
            swap_in_sound_filepath=swap_in_sound_filepath,
            sound_volume=sound_volume,
            weapon_active_sound_filepath=weapon_active_sound_filepath,
        )

    @staticmethod
    def bow_and_arrows(player: Player) -> Weapon:
        """
        Returns a bow and arrow weapon
        """
        return Arsenal.__weapon_builder(
            "Bow", "bow.png", "bow.wav", "arrow.png", player, 4, 20, 50
        )

    @staticmethod
    def desert_eagle(player: Player) -> Weapon:
        """
        Returns a desert eagle weapon
        """
        return Arsenal.__weapon_builder(
            "D. Eagle",
            "desert_eagle.png",
            "desert_eagle.wav",
            "bullet.png",
            player,
            7,
            20,
            30,
        )

    @staticmethod
    def ray_gun(player: Player) -> Weapon:
        """
        Returns a ray gun weapon
        """
        return Arsenal.__weapon_builder(
            "Ray Gun",
            "ray_gun.png",
            "ray_gun.wav",
            "ray_gun_bullet.png",
            player,
            2,
            50,
            25,
        )

    @staticmethod
    def revolver(player: Player) -> Weapon:
        """
        Returns a revolver weapon (player's starting weapon)
        """
        return Arsenal.__weapon_builder(
            "Revolver", "revolver.png", "revolver.wav", "bullet.png", player, 5, 10, 50
        )

    @staticmethod
    def rifle(player: Player) -> Weapon:
        """
        Returns a rifle weapon
        """
        return Arsenal.__weapon_builder(
            "Rifle", "rifle.png", "rifle.wav", "bullet.png", player, 10, 7, 75, True
        )

    @staticmethod
    def rpg(player: Player) -> Weapon:
        """
        Returns an RPG weapon
        """
        return Arsenal.__weapon_builder(
            "RPG", "rpg.png", "rpg.wav", "rpg_bullet.png", player, 6, 40, 10
        )

    @staticmethod
    def smg(player: Player) -> Weapon:
        """
        Returns a smg weapon
        """
        return Arsenal.__weapon_builder(
            "SMG", "smg.png", "smg.wav", "bullet.png", player, 8, 5, 100, True
        )

    @staticmethod
    def sniper(player: Player) -> Weapon:
        """
        Returns a sniper rifle weapon
        """
        return Arsenal.__weapon_builder(
            "Sniper", "sniper.png", "sniper.wav", "bullet.png", player, 10, 25, 30
        )

    @staticmethod
    def lightsaber(player: Player) -> Weapon:
        """
        Returns a lightsaber weapon
        """
        return Arsenal.__weapon_builder(
            "Lightsaber",
            "lightsaber.png",
            "lightsaber.wav",
            "lightsaber_shine.png",
            player,
            10,
            75,
            35,
            max_bullet_dist=30,
            swap_out_sound_filepath="weapons/lightsaber_swap_out.wav",
            swap_in_sound_filepath="weapons/lightsaber_swap_in.wav",
            sound_volume=0.8,
            weapon_active_sound_filepath="weapons/lightsaber_hum.wav",
        )
