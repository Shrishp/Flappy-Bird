import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
BIRD_SIZE = 50  # Size of the bird
GRAVITY = 0.25
JUMP_STRENGTH = -5
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 2

# Colors
WHITE = (255, 255, 255)

# Game Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
background_img = pygame.image.load('background.png').convert()
bird_img = pygame.image.load('bird1.png').convert_alpha()
pipe_img = pygame.image.load('pipe.png').convert()

# Scale images if needed
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, SCREEN_HEIGHT))

# Initialize font
pygame.font.init()
score_font = pygame.font.SysFont('Arial', 30)
game_over_font = pygame.font.SysFont('Arial', 40)

# Bird Properties
bird_x, bird_y = SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2
bird_speed = 0

# Pipe Properties
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(150, 450)

# Score
score = 0
highest_score = 0

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Functions
def reset_game():
    """ Resets the game to the initial state. """
    global bird_y, bird_speed, pipe_x, pipe_height, score, PIPE_SPEED
    bird_y = SCREEN_HEIGHT // 2
    bird_speed = 0
    pipe_x = SCREEN_WIDTH
    pipe_height = random.randint(100, 400)
    score = 0
    PIPE_SPEED = 2

def reset_pipe():
    """ Resets the pipe when it goes off-screen and updates the score. """
    global pipe_x, pipe_height, score, PIPE_SPEED
    pipe_x = SCREEN_WIDTH
    pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
    score += 1
    if score % 5 == 0:
        PIPE_SPEED += 0.25

def draw_bird():
    """ Draws the bird on the screen. """
    screen.blit(bird_img, (bird_x - BIRD_SIZE // 2, bird_y - BIRD_SIZE // 2))

def draw_pipes():
    """ Draws the upper and lower pipes on the screen. """
    # Upper pipe
    screen.blit(pipe_img, (pipe_x, pipe_height - SCREEN_HEIGHT))
    # Lower pipe
    screen.blit(pipe_img, (pipe_x, pipe_height + PIPE_GAP))

def draw_score():
    """ Draws the current score on the screen. """
    score_surface = score_font.render(f'Score: {score}', False, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

def draw_game_over():
    """ Draws the game over screen. """
    global highest_score
    highest_score = max(score, highest_score)
    game_over_surface = game_over_font.render('Game Over', False, (0, 0, 0))
    high_score_surface = score_font.render(f'High Score: {highest_score}', False, (0, 0, 0))
    play_again_surface = score_font.render('Press Space to play again', False, (0, 0, 0))
    screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, 150))
    screen.blit(high_score_surface, (SCREEN_WIDTH // 2 - high_score_surface.get_width() // 2, 250))
    screen.blit(play_again_surface, (SCREEN_WIDTH // 2 - play_again_surface.get_width() // 2, 350))

def check_collision():
    """ Checks for collisions between the bird and the pipes or ground. """
    bird_rect = pygame.Rect(bird_x - BIRD_SIZE // 2, bird_y - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
    bottom_pipe_rect = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP)
    top_pipe_rect = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    if bird_rect.colliderect(bottom_pipe_rect) or bird_rect.colliderect(top_pipe_rect):
        return True
    if bird_y - BIRD_SIZE // 2 < 0 or bird_y + BIRD_SIZE // 2 > SCREEN_HEIGHT:
        return True
    return False

def game_over():
    """ Shows the game over screen and waits for the player to press space to restart. """
    draw_game_over()
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before allowing restart
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_key = False
    reset_game()

def start_screen():
    """ Shows the start screen. """
    screen.blit(background_img, (0, 0))
    welcome_text = game_over_font.render('Flappy Bird', False, (0, 0, 0))
    start_text = score_font.render('Press Space to start', False, (0, 0, 0))
    screen.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, 150))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 250))
    pygame.display.flip()
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_start = False

def game_loop():
    """ The main game loop. """
    global bird_speed, bird_y, pipe_x

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = JUMP_STRENGTH

        bird_speed += GRAVITY
        bird_y += bird_speed

        pipe_x -= PIPE_SPEED
        if pipe_x < -PIPE_WIDTH:
            reset_pipe()

        if check_collision():
            game_over()

        screen.blit(background_img, (0, 0))
        draw_pipes()
        draw_bird()
        draw_score()
        pygame.display.flip()
        clock.tick(30)

# Main execution
start_screen()
game_loop()