
from flask import Flask

app = Flask(__name__)

@app.route("/")
def health():
    return "Game Running", 200

if __name__ == "__main__":
    # Flask keeps the container alive
    app.run(host="0.0.0.0", port=5000)
