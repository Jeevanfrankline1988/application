import pygame

class SnakeGame:
    def __init__(self, width=400, height=400, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.snake = [(width // 2, height // 2)]
        self.direction = (0, -block_size)  # initially up
        self.food = self.spawn_food()
        self.game_over = False

        # Initialize Pygame surface
        pygame.init()
        self.surface = pygame.Surface((self.width, self.height))

    def spawn_food(self):
        import random
        while True:
            x = (random.randint(0, (self.width // self.block_size) - 1) * self.block_size)
            y = (random.randint(0, (self.height // self.block_size) - 1) * self.block_size)
            if (x, y) not in self.snake:
                return (x, y)

    def step(self):
        if self.game_over:
            return

        # Move snake
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check collisions
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def change_direction(self, key):
        # Prevent reversing
        dx, dy = self.direction
        if key == "UP" and dy == 0:
            self.direction = (0, -self.block_size)
        elif key == "DOWN" and dy == 0:
            self.direction = (0, self.block_size)
        elif key == "LEFT" and dx == 0:
            self.direction = (-self.block_size, 0)
        elif key == "RIGHT" and dx == 0:
            self.direction = (self.block_size, 0)

    def draw(self):
        # Clear surface
        self.surface.fill((0, 0, 0))

        # Draw food
        pygame.draw.rect(self.surface, (255, 0, 0),
                         (*self.food, self.block_size, self.block_size))

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.surface, (0, 255, 0),
                             (*segment, self.block_size, self.block_size))

        # Draw game over text
        if self.game_over:
            font = pygame.font.SysFont(None, 50)
            text = font.render("Game Over!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width//2, self.height//2))
            self.surface.blit(text, text_rect)

        return self.surface
