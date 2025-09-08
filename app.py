from flask import Flask
import threading
import pygame
import time

app = Flask(__name__)

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Snake Game 🐍")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        time.sleep(0.05)  # avoid high CPU usage

    pygame.quit()

@app.route("/")
def health():
    return "Game Running", 200

if __name__ == "__main__":
    # Run pygame loop in a background thread
    t = threading.Thread(target=run_game)
    t.daemon = True
    t.start()

    # Keep Flask server alive
    app.run(host="0.0.0.0", port=5000)
