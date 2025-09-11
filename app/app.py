from flask import Flask, render_template, Response, request
import cv2
from sgame import SnakeGame
import threading
import numpy as np

app = Flask(__name__)
game = SnakeGame()
lock = threading.Lock()
last_action = None

def generate_frames():
    global last_action
    while True:
        with lock:
            if last_action:
                game.step(last_action)
                last_action = None

            if game.game_over:
                game.reset()

            frame = game.render_frame()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move', methods=['POST'])
def move():
    global last_action
    data = request.json
    key = data.get('key')
    with lock:
        last_action = key
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
