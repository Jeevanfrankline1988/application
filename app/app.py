from flask import Flask, render_template, Response
import pygame
import io
from PIL import Image
from sgame import SnakeGame

app = Flask(__name__)
game = SnakeGame()

@app.route("/")
def index():
    # Serve your HTML page from /app/templates/index.html
    return render_template("index.html")

@app.route("/frame")
def frame():
    # Advance game state
    game.step()

    # Draw Pygame surface
    surface = game.draw()

    # Convert Pygame surface → PNG bytes
    img_str = pygame.image.tostring(surface, "RGB")
    img = Image.frombytes("RGB", surface.get_size(), img_str)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(buf.getvalue(), mimetype="image/png")

@app.route("/keydown/<key>")
def keydown(key):
    game.change_direction(key)
    return "ok"

if __name__ == "__main__":
    # Listen on all interfaces for Kubernetes / SSH tunnel
    app.run(host="0.0.0.0", port=5000, debug=True)
