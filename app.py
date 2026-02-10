from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

# ---------- HOME ----------
@app.route("/")
def home():
    return "<h2>Alhudha Haj Dynamic Travel System – RUNNING ✅</h2>"

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

# ---------- ADD TRAVELER FORM ----------
@app.route("/traveler/add", methods=["GET", "POST"])
def add_traveler():
    if request.method == "POST":
        data = request.form

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO travelers (
                traveler_id, surname, given_name, nationality, gender, dob, place_of_birth,
                passport_no, passport_name, passport_issue_place, passport_issue_date, passport_expiry_date,
                father_name, mother_name, spouse_name,
                mobile, email, address,
                aadhaar, pan, vaccine_status, wheelchair_required,
                passport_original_received, passport_received_date,
                passport_returned, passport_returned_date,
                admin_notes, pin
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,
                %s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,
                %s,%s,
                %s,%s
            )
        """, (
            data.get("traveler_id"),
            data.get("surname"),
            data.get("given_name"),
            data.get("nationality"),
            data.get("gender"),
            data.get("dob"),
            data.get("place_of_birth"),
            data.get("passport_no"),
            data.get("passport_name"),
            data.get("passport_issue_place"),
            data.get("passport_issue_date"),
            data.get("passport_expiry_date"),
            data.get("father_name"),
            data.get("mother_name"),
            data.get("spouse_name"),
            data.get("mobile"),
            data.get("email"),
            data.get("address"),
            data.get("aadhaar"),
            data.get("pan"),
            data.get("vaccine_status"),
            bool(data.get("wheelchair_required")),
            bool(data.get("passport_original_received")),
            data.get("passport_received_date"),
            bool(data.get("passport_returned")),
            data.get("passport_returned_date"),
            data.get("admin_notes"),
            data.get("pin")
        ))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("admin/traveler_form.html")

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
