from flask import Flask, request, Response, send_from_directory
import threading, time
import sgame

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/frame")
def frame():
    img_bytes = sgame.render_frame()
    return Response(img_bytes, mimetype="image/jpeg")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    direction = data.get("direction")
    if direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
        # Prevent reversing direction instantly
        if (sgame.direction, direction) not in [
            ("UP","DOWN"), ("DOWN","UP"),
            ("LEFT","RIGHT"), ("RIGHT","LEFT")
        ]:
            sgame.direction = direction
    return {"status": "ok", "direction": sgame.direction}

def game_loop():
    while True:
        sgame.update_game()
        time.sleep(0.1)  # 10 FPS

threading.Thread(target=game_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
