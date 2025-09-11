from flask import Flask, render_template, Response
import pygame
import io
from PIL import Image
from sgame import SnakeGame

app = Flask(__name__)  # Flask looks in /app/templates
game = SnakeGame()

@app.route("/")
def index():
    return render_template("index.html")  # Loads index.html from /app/templates

@app.route("/frame")
def frame():
    game.step()
    surface = game.draw()
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
    app.run(host="0.0.0.0", port=5000, debug=True)
