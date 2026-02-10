from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

# ======================
# HEALTH CHECK (Railway)
# ======================
@app.route("/health")
def health():
    return "OK", 200

# ======================
# HOME PAGE
# ======================
@app.route("/")
def home():
    return "Alhudha Haj Dynamic Travel System – RUNNING ✅"

# ======================
# LOGIN PAGE
# ======================
@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            return redirect(url_for("dashboard"))
        else:
            return "Invalid login ❌"

    return render_template("admin/login.html")

# ======================
# DASHBOARD
# ======================
@app.route("/admin/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

# ======================
# REQUIRED FOR RAILWAY
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
