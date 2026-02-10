from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

# ------------------
# ROUTES
# ------------------

@app.route("/")
def home():
    return redirect("/admin/login")

@app.route("/health")
def health():
    return "OK", 200

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            return redirect("/admin/dashboard")
        else:
            return "Invalid Login ❌"

    return render_template("admin/login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")

# ------------------
# RAILWAY PORT
# ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
