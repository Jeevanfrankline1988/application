from flask import Flask, Response
import sgame

app = Flask(__name__)

@app.route("/")
def home():
    return "Snake Game running! Visit /frame to see a snapshot."

@app.route("/frame")
def frame():
    sgame.update_game()
    img_bytes = sgame.render_frame()
    return Response(img_bytes, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

