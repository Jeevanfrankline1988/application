import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()
SPEED = 10

# Snake setup
snake = [(100, 50), (90, 50), (80, 50)]
direction = "RIGHT"

# Food setup
food = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)

score = 0

def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

def show_score(score):
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Move snake
    x, y = snake[0]
    if direction == "UP":
        y -= CELL_SIZE
    elif direction == "DOWN":
        y += CELL_SIZE
    elif direction == "LEFT":
        x -= CELL_SIZE
    elif direction == "RIGHT":
        x += CELL_SIZE
    new_head = (x, y)

    # Check game over
    if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in snake):
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1
        food = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
    else:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    show_score(score)
    pygame.display.update()
    clock.tick(SPEED)


