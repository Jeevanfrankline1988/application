from flask import Flask, jsonify, request, render_template
import random
import threading
import time

app = Flask(__name__)

# ----- Game State -----
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

snake = [[WIDTH//2, HEIGHT//2]]
direction = [0, -CELL_SIZE]  # moving up initially
food = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]

lock = threading.Lock()

def update_game():
    global snake, food
    while True:
        time.sleep(0.1)  # 10 FPS
        with lock:
            # Move snake
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = [(head_x + dx) % WIDTH, (head_y + dy) % HEIGHT]

            # Check self-collision
            if new_head in snake:
                snake[:] = [[WIDTH//2, HEIGHT//2]]  # reset snake
                direction[:] = [0, -CELL_SIZE]

            snake.insert(0, new_head)

            # Check food collision
            if abs(new_head[0] - food[0]) < CELL_SIZE and abs(new_head[1] - food[1]) < CELL_SIZE:
                food[:] = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]
            else:
                snake.pop()  # remove tail

# Start background thread
threading.Thread(target=update_game, daemon=True).start()

# ----- Flask Routes -----
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    with lock:
        return jsonify({"snake": snake, "food": food})

@app.route("/move", methods=["POST"])
def move():
    global direction
    data = request.get_json()
    dir_map = {
        "UP": [0, -CELL_SIZE],
        "DOWN": [0, CELL_SIZE],
        "LEFT": [-CELL_SIZE, 0],
        "RIGHT": [CELL_SIZE, 0]
    }
    if data["direction"] in dir_map:
        new_dir = dir_map[data["direction"]]
        with lock:
            # Prevent reversing
            if new_dir[0] != -direction[0] or new_dir[1] != -direction[1]:
                direction[:] = new_dir
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
