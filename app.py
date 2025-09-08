from flask import Flask
import threading
import pygame, time

app = Flask(__name__)

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Snake Game 🐍")

    while True:
        # Keep loop alive
        pygame.event.pump()
        time.sleep(0.1)

@app.route("/")
def health():
    return "Game Running", 200

if __name__ == "__main__":
    t = threading.Thread(target=run_game, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)

