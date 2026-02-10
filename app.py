from flask import Flask, render_template, request, redirect, session
import psycopg2, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "alhudha_secret_key"

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Alhudha Haj Dynamic Travel System - RUNNING"

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("admin/login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

# ---------------- ADD TRAVELER ----------------
@app.route("/traveler/add", methods=["GET","POST"])
def add_traveler():
    if request.method == "POST":
        f = request.form
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO travelers (
            traveler_id, surname, given_name, nationality, gender, dob,
            place_of_birth, passport_no, passport_name,
            passport_issue_place, passport_issue_date, passport_expiry_date,
            father_name, mother_name, spouse_name,
            mobile, email, address, aadhaar, pan,
            vaccine_status, admin_notes, created_at
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,
            %s,%s,%s,
            %s,%s,%s,%s,%s,
            %s,%s,%s
        )
        """, (
            f.get("traveler_id"),
            f.get("surname"),
            f.get("given_name"),
            f.get("nationality"),
            f.get("gender"),
            f.get("dob"),
            f.get("place_of_birth"),
            f.get("passport_no"),
            f.get("passport_name"),
            f.get("passport_issue_place"),
            f.get("passport_issue_date"),
            f.get("passport_expiry_date"),
            f.get("father_name"),
            f.get("mother_name"),
            f.get("spouse_name"),
            f.get("mobile"),
            f.get("email"),
            f.get("address"),
            f.get("aadhaar"),
            f.get("pan"),
            f.get("vaccine_status"),
            f.get("admin_notes"),
            datetime.now()
        ))

        conn.commit()
        cur.close()
        conn.close()
        return redirect("/traveler/list")

    return render_template("admin/traveler_form.html")

# ---------------- TRAVELER LIST ----------------
@app.route("/traveler/list")
def traveler_list():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, traveler_id, surname, given_name, passport_no, mobile
        FROM travelers
        ORDER BY id DESC
    """)

    travelers = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("admin/traveler_list.html", travelers=travelers)

# ---------------- EDIT TRAVELER ----------------
@app.route("/traveler/edit/<int:id>", methods=["GET","POST"])
def edit_traveler(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        f = request.form
        cur.execute("""
        UPDATE travelers SET
            surname=%s,
            given_name=%s,
            mobile=%s,
            email=%s,
            address=%s,
            admin_notes=%s
        WHERE id=%s
        """, (
            f.get("surname"),
            f.get("given_name"),
            f.get("mobile"),
            f.get("email"),
            f.get("address"),
            f.get("admin_notes"),
            id
        ))

        conn.commit()
        cur.close()
        conn.close()
        return redirect("/traveler/list")

    cur.execute("SELECT * FROM travelers WHERE id=%s", (id,))
    traveler = cur.fetchone()

    cur.close()
    conn.close()
    return render_template("admin/traveler_edit.html", traveler=traveler)

# ---------------- DELETE TRAVELER ----------------
@app.route("/traveler/delete/<int:id>")
def delete_traveler(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM travelers WHERE id=%s", (id,))
    conn.commit()

    cur.close()
    conn.close()
    return redirect("/traveler/list")

# ---------------- PAYMENT ----------------
@app.route("/payment/<int:traveler_id>", methods=["GET","POST"])
def payment(traveler_id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        f = request.form
        cur.execute("""
        INSERT INTO payments (traveler_id, amount, mode, status, remarks)
        VALUES (%s,%s,%s,%s,%s)
        """, (
            traveler_id,
            f.get("amount"),
            f.get("mode"),
            f.get("status"),
            f.get("remarks")
        ))

        conn.commit()
        cur.close()
        conn.close()
        return redirect("/traveler/list")

    cur.close()
    conn.close()
    return render_template("admin/payment.html", traveler_id=traveler_id)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
