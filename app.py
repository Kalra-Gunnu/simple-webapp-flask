import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

@app.route('/how are you')
def hello():
    env = os.getenv("APP_ENV", "Unknown")
    return f"<h1>Hello from {env} environment!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
