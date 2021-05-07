import pygame

# constants
WIDTH, HEIGHT = 800, 600
PLAYER_X_START, PLAYER_Y_START = 50, 460

# initialize the pygame & create screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# background and stage
background = pygame.image.load("images/background.png").convert()
background_width, background_height = background.get_rect().size
stage_width: int = background_width * 2
stage_pos_x = 0
start_scrolling_pos_x = WIDTH / 2

player_image = pygame.image.load("images/ghost.png")
player_x, player_y = PLAYER_X_START, PLAYER_Y_START
player_x_change, player_y_change = 0, 0
player_circle = 64

def player(x: float, y: float):
    """
    draws player on the screen
    """
    screen.blit(player_image, (x, y))

running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            if event.key == pygame.K_RIGHT:
                player_x_change = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    screen.blit(background, (0, 0))

    player_x += player_x_change
    if player_x > stage_width - 64:
        player_x = stage_width - 64
    if player_x < 0:
        player_x = 0

    if player_x < start_scrolling_pos_x:
        player_circle = player_x
    elif player_x > stage_width - start_scrolling_pos_x:
        player_circle = player_x - stage_width + WIDTH
    else:
        player_circle = start_scrolling_pos_x
        stage_pos_x += -player_x_change

    rel_x = stage_pos_x % background_width
    screen.blit(background, (rel_x - background_width, 0))
    if rel_x < WIDTH:
        screen.blit(background, (rel_x, 0))

    # pygame.draw.circle(s, WHITE, (circlePosX, playerPosY - 25), circleRadius, 0)
    player(player_circle, player_y)

    pygame.display.update()

    # WATCH THIS
    # TODO
    # https: // www.youtube.com / watch?v = US3HSusUBeI