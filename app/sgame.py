import pygame, random, io
from flask import Flask, Response
from PIL import Image

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
SPEED = 10

snake = [(100, 50), (90, 50), (80, 50)]
direction = "RIGHT"
food = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
score = 0

app = Flask(__name__)

def update_game():
    global snake, direction, food, score
    x, y = snake[0]
    if direction == "UP": y -= CELL_SIZE
    elif direction == "DOWN": y += CELL_SIZE
    elif direction == "LEFT": x -= CELL_SIZE
    elif direction == "RIGHT": x += CELL_SIZE
    new_head = (x, y)

    if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in snake):
        snake[:] = [(100, 50), (90, 50), (80, 50)]
        direction = "RIGHT"
        score = 0
        return

    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
    else:
        snake.pop()

def render_frame():
    global snake, food, score
    screen.fill((0,0,0))
    for pos in snake:
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))
    font = pygame.font.SysFont("Arial", 24)
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), [10,10])

    return surface_to_bytes(screen)

def surface_to_bytes(surface):
    image = pygame.image.tostring(surface, "RGB")
    pil_img = Image.frombytes("RGB", surface.get_size(), image)
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG")
    return buf.getvalue()

@app.route('/frame')
def frame():
    def generate():
        while True:
            update_game()
            img = render_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            clock.tick(SPEED)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
