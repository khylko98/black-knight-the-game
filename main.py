import pygame
import sys
import pygame.display
from random import randint

# Initialize pygame
pygame.init()

# Set up the game window
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("The Black Knight: The Game")

# Load game assets
game_font = pygame.font.Font(None, 50)
background_image = pygame.transform.scale(pygame.image.load(
    "images/background.png"), (screen_width, screen_height))
knight_image = pygame.image.load("images/knight.png")
sword_image = pygame.image.load("images/sword.png")
dragon_image = pygame.image.load("images/dragon.png")

# Initialize game variables
KNIGHT_STEP = 5
SWORD_STEP = 2
DRAGON_STEP = 0.5

knight_width, knight_height = knight_image.get_size()
knight_x, knight_y = screen_width / 2 - \
    knight_width / 2, screen_height - knight_height
knight_is_moving_left, knight_is_moving_right = False, False

sword_width, sword_height = sword_image.get_size()
sword_x, sword_y = 0, 0
sword_was_fired = False

dragon_width, dragon_height = dragon_image.get_size()
dragon_x, dragon_y = randint(0, screen_width - dragon_width), 0
dragon_speed = DRAGON_STEP

game_is_running = True
game_score = 0

while game_is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                knight_is_moving_left = True
            if event.key == pygame.K_RIGHT:
                knight_is_moving_right = True
            if event.key == pygame.K_SPACE:
                sword_was_fired = True
                sword_x = knight_x + knight_width / 2 - sword_width / 2
                sword_y = knight_y - sword_height
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                knight_is_moving_left = False
            if event.key == pygame.K_RIGHT:
                knight_is_moving_right = False

    # Knight movement
    if knight_is_moving_left and knight_x >= KNIGHT_STEP:
        knight_x -= KNIGHT_STEP
    if knight_is_moving_right and knight_x <= screen_width - knight_width - KNIGHT_STEP:
        knight_x += KNIGHT_STEP

    # Dragon movement
    dragon_y += dragon_speed

    # Sword movement and collision
    if sword_was_fired and sword_y + sword_height < 0:
        sword_was_fired = False
    if sword_was_fired:
        sword_y -= SWORD_STEP

    # Update the game screen
    screen.blit(background_image, (0, 0))
    screen.blit(knight_image, (knight_x, knight_y))
    screen.blit(dragon_image, (dragon_x, dragon_y))
    if sword_was_fired:
        screen.blit(sword_image, (sword_x, sword_y))
    game_score_text = game_font.render(
        f"Your score is: {game_score}", True, 'white')
    screen.blit(game_score_text, (20, 20))
    pygame.display.update()

    # Game over conditions
    if dragon_y + dragon_height > knight_y:
        game_is_running = False

    if sword_was_fired and dragon_x < sword_x < dragon_x + dragon_width - sword_width and dragon_y < sword_y < dragon_y + dragon_height - sword_height:
        sword_was_fired = False
        dragon_x, dragon_y = randint(0, screen_width - dragon_width), 0
        dragon_speed += DRAGON_STEP / 2
        game_score += 1

# Game over screen
game_over_text = game_font.render("Game Over", True, 'white')
game_over_rectangle = game_over_text.get_rect()
game_over_rectangle.center = (screen_width / 2, screen_height / 2)
screen.blit(game_over_text, game_over_rectangle)
pygame.display.update()
pygame.time.wait(3_000)

# Clean up
pygame.quit()
