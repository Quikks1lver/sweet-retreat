import pygame

def play_sound(filepath: str):
    """
    Plays sound from designated file within sounds directory
    """
    sound = pygame.mixer.Sound(f"sounds/{filepath}")
    sound.set_volume(1)
    sound.play()