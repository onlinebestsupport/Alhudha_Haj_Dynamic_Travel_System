from flask import Flask
import os

app = Flask(__name__)

# Health check for Railway
@app.route("/health")
def health():
    return "OK", 200

# Home route
@app.route("/")
def home():
    return "Alhudha Haj Dynamic Travel System – RUNNING ✅", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
