from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    try:
        # Read the HTML file we copied into /tmp
        with open("/tmp/index.html", "r") as f:
            html = f.read()
        return render_template_string(html)
    except Exception as e:
        return f"<h1>Error loading index.html</h1><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
