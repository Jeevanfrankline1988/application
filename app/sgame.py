import pygame
import random

# Game settings
WIDTH, HEIGHT = 400, 400
BLOCK_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.snake = [(100, 100)]
        self.direction = (BLOCK_SIZE, 0)  # moving right initially
        self.food = self.spawn_food()
        self.game_over = False

    def spawn_food(self):
        return (
            random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
        )

    def change_direction(self, key):
        if key == "ArrowUp" and self.direction != (0, BLOCK_SIZE):
            self.direction = (0, -BLOCK_SIZE)
        elif key == "ArrowDown" and self.direction != (0, -BLOCK_SIZE):
            self.direction = (0, BLOCK_SIZE)
        elif key == "ArrowLeft" and self.direction != (BLOCK_SIZE, 0):
            self.direction = (-BLOCK_SIZE, 0)
        elif key == "ArrowRight" and self.direction != (-BLOCK_SIZE, 0):
            self.direction = (BLOCK_SIZE, 0)

    def step(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Collisions
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH
            or new_head[1] < 0 or new_head[1] >= HEIGHT
            or new_head in self.snake
        ):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.display.fill(BLACK)

        # Draw food
        pygame.draw.rect(self.display, RED, (*self.food, BLOCK_SIZE, BLOCK_SIZE))

        # Draw snake
        for x, y in self.snake:
            pygame.draw.rect(self.display, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))

        return self.display
