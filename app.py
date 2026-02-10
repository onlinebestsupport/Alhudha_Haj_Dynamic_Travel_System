from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "alhudha_secret_key"


# -------------------------------------------------
# HOME PAGE (Health check for Railway)
# -------------------------------------------------
@app.route("/")
def home():
    return "Alhudha Haj Dynamic Travel System – RUNNING ✅"


# -------------------------------------------------
# LOGIN PAGE
# URL: /login
# FILE: templates/admin/login.html
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # For now, no authentication check
        return redirect(url_for("dashboard"))

    return render_template("admin/login.html")


# -------------------------------------------------
# DASHBOARD
# URL: /dashboard
# FILE: templates/admin/dashboard.html
# -------------------------------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")


# -------------------------------------------------
# ADD TRAVELER FORM (33 fields – UI only)
# URL: /traveler/add
# FILE: templates/admin/traveler_form.html
# -------------------------------------------------
@app.route("/traveler/add", methods=["GET", "POST"])
def add_traveler():
    if request.method == "POST":
        # Database insert will be added later
        # For now just return to dashboard
        return redirect(url_for("dashboard"))

    return render_template("admin/traveler_form.html")


# -------------------------------------------------
# REQUIRED FOR RAILWAY + GUNICORN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
