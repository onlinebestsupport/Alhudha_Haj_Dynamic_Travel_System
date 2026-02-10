import psycopg2
from flask import Flask, render_template, request, redirect
import os
def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])
@app.route("/traveler/add", methods=["GET"])
def traveler_add():
    return render_template("traveler_add.html")
@app.route("/traveler/add", methods=["POST"])
def traveler_save():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO travelers (
            surname, given_name, gender, dob, nationality, marital_status,
            passport_no, passport_place_issue, passport_issue_date, passport_expiry_date, passport_original,
            phone, whatsapp, email, address, city, state, country, pincode,
            batch_name, travel_type, mahram_name, relation, medical_notes,
            admin_notes, status
        ) VALUES (
            %(surname)s, %(given_name)s, %(gender)s, %(dob)s, %(nationality)s, %(marital_status)s,
            %(passport_no)s, %(passport_place_issue)s, %(passport_issue_date)s, %(passport_expiry_date)s, %(passport_original)s,
            %(phone)s, %(whatsapp)s, %(email)s, %(address)s, %(city)s, %(state)s, %(country)s, %(pincode)s,
            %(batch_name)s, %(travel_type)s, %(mahram_name)s, %(relation)s, %(medical_notes)s,
            %(admin_notes)s, %(status)s
        )
    """, request.form)

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/dashboard")

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
@app.route("/admin/traveler/add", methods=["GET", "POST"])
def add_traveler():
    if request.method == "POST":
        return "Traveler saved (database coming next) ✅"
    return render_template("admin/traveler_form.html")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
