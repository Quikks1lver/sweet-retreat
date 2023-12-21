import pygame


def play_sound(filepath: str, volume: float = 1):
    """
    Plays sound from designated file within sounds directory, with optional param for volume level
    """
    sound = pygame.mixer.Sound(f"sounds/{filepath}")
    sound.set_volume(volume)
    sound.play()


def play_background_music(filepath: str):
    """
    Stops any existing background music and plays new one from sounds directory
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load(f"sounds/{filepath}")
    pygame.mixer.music.play(-1)
