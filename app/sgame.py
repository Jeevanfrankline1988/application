import pygame
import numpy as np

class SnakeGame:
    def __init__(self, width=400, height=400, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.reset()

    def reset(self):
        self.snake = [(self.width//2, self.height//2)]
        self.direction = (0, -self.block_size)  # moving up initially
        self.spawn_food()
        self.game_over = False

    def spawn_food(self):
        grid_x = self.width // self.block_size
        grid_y = self.height // self.block_size
        while True:
            x = np.random.randint(0, grid_x) * self.block_size
            y = np.random.randint(0, grid_y) * self.block_size
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def step(self, action):
        # action = "UP", "DOWN", "LEFT", "RIGHT"
        if action == "UP" and self.direction != (0, self.block_size):
            self.direction = (0, -self.block_size)
        elif action == "DOWN" and self.direction != (0, -self.block_size):
            self.direction = (0, self.block_size)
        elif action == "LEFT" and self.direction != (self.block_size, 0):
            self.direction = (-self.block_size, 0)
        elif action == "RIGHT" and self.direction != (-self.block_size, 0):
            self.direction = (self.block_size, 0)

        # Move snake
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.snake.insert(0, new_head)

        # Check collisions
        if (
            new_head in self.snake[1:] or
            not 0 <= new_head[0] < self.width or
            not 0 <= new_head[1] < self.height
        ):
            self.game_over = True

        # Check food
        if new_head == self.food:
            self.spawn_food()
        else:
            self.snake.pop()  # remove tail

    def render_frame(self):
        pygame.init()
        surface = pygame.Surface((self.width, self.height))
        surface.fill((0, 0, 0))  # black background

        # Draw food
        pygame.draw.rect(surface, (255, 0, 0), (*self.food, self.block_size, self.block_size))

        # Draw snake
        for x, y in self.snake:
            pygame.draw.rect(surface, (0, 255, 0), (x, y, self.block_size, self.block_size))

        # Convert to RGB array
        frame = pygame.surfarray.array3d(surface)
        frame = np.rot90(frame, 3)  # rotate to correct orientation
        frame = np.flip(frame, axis=1)
        return frame
