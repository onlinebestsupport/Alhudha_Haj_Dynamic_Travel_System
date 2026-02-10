from flask import Flask, render_template, request, redirect, session
import psycopg2, os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "alhudha_secret_key"

# ---------------- DATABASE ----------------
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

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")
    return render_template("admin/dashboard.html")

# ---------------- ADD TRAVELER ----------------
@app.route("/traveler/add", methods=["GET","POST"])
def add_traveler():
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        f = request.form
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO travelers (
            traveler_id, surname, given_name, nationality, gender, dob,
            place_of_birth, passport_no, passport_name, passport_issue_place,
            passport_issue_date, passport_expiry_date,
            father_name, mother_name, spouse_name,
            mobile, email, address, aadhaar, pan,
            vaccine_status, admin_notes, created_at
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,
            %s,%s,
            %s,%s,%s,
            %s,%s,%s,%s,%s,
            %s,%s,%s
        )
        """, (
            f["traveler_id"], f["surname"], f["given_name"], f["nationality"],
            f["gender"], f["dob"], f["place_of_birth"], f["passport_no"],
            f["passport_name"], f["passport_issue_place"],
            f["passport_issue_date"], f["passport_expiry_date"],
            f["father_name"], f["mother_name"], f["spouse_name"],
            f["mobile"], f["email"], f["address"],
            f["aadhaar"], f["pan"], f["vaccine_status"],
            f["admin_notes"], datetime.now()
        ))

        conn.commit()
        cur.close()
        conn.close()
        return redirect("/traveler/list")

    return render_template("admin/traveler_form.html")

# ---------------- TRAVELER LIST ----------------
@app.route("/traveler/list")
def traveler_list():
    if not session.get("user"):
        return redirect("/login")

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
    if not session.get("user"):
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        f = request.form
        cur.execute("""
        UPDATE travelers SET
            surname=%s, given_name=%s, mobile=%s,
            email=%s, address=%s, admin_notes=%s
        WHERE id=%s
        """, (
            f["surname"], f["given_name"], f["mobile"],
            f["email"], f["address"], f["admin_notes"], id
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
    if not session.get("user"):
        return redirect("/login")

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
    if not session.get("user"):
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        f = request.form
        cur.execute("""
        INSERT INTO payments (traveler_id, amount, mode, status, remarks, created_at)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            traveler_id, f["amount"], f["mode"], f["status"], f["remarks"], datetime.now()
        ))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/traveler/list")

    return render_template("admin/payment.html", traveler_id=traveler_id)

# ---------------- INVOICE ----------------
@app.route("/invoice/<int:traveler_id>")
def invoice(traveler_id):
    if not session.get("user"):
        return redirect("/login")

    # DEMO VALUES (can be dynamic later)
    package_amount = 125000
    gst_percent = 5
    gst_amount = package_amount * gst_percent / 100
    tcs_percent = 5
    tcs_amount = (package_amount + gst_amount) * tcs_percent / 100
    grand_total = round(package_amount + gst_amount + tcs_amount)

    return render_template(
        "admin/invoice.html",
        traveler_name="Traveler",
        traveler_id=traveler_id,
        batch_name="Umrah March 2026",
        invoice_date=date.today(),
        package_amount=package_amount,
        gst_percent=gst_percent,
        gst_amount=gst_amount,
        tcs_percent=tcs_percent,
        tcs_amount=tcs_amount,
        grand_total=grand_total
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
