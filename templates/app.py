# app.py
from flask import Flask, send_file, request
import pygame
import io
from PIL import Image
import random
import threading
import time

app = Flask(__name__)

# ----- Pygame setup -----
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.Surface((WIDTH, HEIGHT))

# Snake game state
snake = [(WIDTH//2, HEIGHT//2)]
direction = (0, -CELL_SIZE)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
lock = threading.Lock()  # To safely update snake in threads

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def update_game():
    global snake, food
    with lock:
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)

        # Check self-collision
        if new_head in snake:
            snake.clear()
            snake.append((WIDTH//2, HEIGHT//2))

        snake.insert(0, new_head)
        # Check food collision
        if abs(new_head[0] - food[0]) < CELL_SIZE and abs(new_head[1] - food[1]) < CELL_SIZE:
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        else:
            snake.pop()  # Remove tail if no food eaten

def draw_game():
    screen.fill(BLACK)
    with lock:
        for x, y in snake:
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

def get_frame_bytes():
    draw_game()
    buf = io.BytesIO()
    arr = pygame.surfarray.array3d(screen)
    arr = arr.swapaxes(0,1)
    im = Image.fromarray(arr).convert("RGB")
    im.save(buf, format='PNG')
    buf.seek(0)
    return buf

# ----- Flask routes -----
@app.route("/frame")
def frame():
    return send_file(get_frame_bytes(), mimetype='image/png')

@app.route("/move", methods=["POST"])
def move():
    global direction
    data = request.get_json()
    dir_map = {
        "UP": (0, -CELL_SIZE),
        "DOWN": (0, CELL_SIZE),
        "LEFT": (-CELL_SIZE, 0),
        "RIGHT": (CELL_SIZE, 0)
    }
    if data["direction"] in dir_map:
        new_dir = dir_map[data["direction"]]
        with lock:
            if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                direction = new_dir
    return {"status": "ok"}

# ----- Background thread -----
def game_loop():
    while True:
        update_game()
        time.sleep(0.1)  # 10 FPS

threading.Thread(target=game_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
