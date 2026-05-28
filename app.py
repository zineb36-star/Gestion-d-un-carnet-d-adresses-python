from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import csv
import smtplib
import urllib.parse

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

app.secret_key = "secret123"

# ==========================
# DATABASE
# ==========================

def get_connection():

    conn = sqlite3.connect("contacts.db")

    conn.row_factory = sqlite3.Row

    return conn

# ==========================
# CREATE TABLES
# ==========================

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # CONTACTS

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS contacts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nom TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        telephone TEXT NOT NULL,

        categorie TEXT,

        adresse TEXT,

        fonction TEXT,

        entreprise TEXT

    )

    """)

    # ADMINS

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS admins(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )

    """)

    conn.commit()

    # ADMIN DEFAULT

    cursor.execute(
        "SELECT * FROM admins WHERE username=?",
        ("admin",)
    )

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute(
            "INSERT INTO admins(username,password) VALUES(?,?)",
            ("admin", "admin123")
        )

        conn.commit()

    conn.close()

create_tables()

# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM admins WHERE username=? AND password=?",
            (username, password)
        )

        admin = cursor.fetchone()

        conn.close()

        if admin:

            session["admin"] = username

            return redirect("/")

        else:

            return render_template(
                "login.html",
                error="Login incorrect"
            )

    return render_template("login.html")

# ==========================
# LOGOUT
# ==========================

@app.route("/logout")

def logout():

    session.clear()

    return redirect("/login")

# ==========================
# HOME
# ==========================

@app.route("/")

def index():

    if "admin" not in session:

        return redirect("/login")

    search = request.args.get("search", "")

    conn = get_connection()

    cursor = conn.cursor()

    if search:

        cursor.execute("""

        SELECT * FROM contacts

        WHERE nom LIKE ?
        OR email LIKE ?
        OR telephone LIKE ?
        OR categorie LIKE ?
        OR adresse LIKE ?
        OR fonction LIKE ?
        OR entreprise LIKE ?

        """, (

            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"

        ))

    else:

        cursor.execute(
            "SELECT * FROM contacts"
        )

    contacts = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        contacts=contacts,
        search=search
    )

# ==========================
# ADD CONTACT
# ==========================

@app.route("/add", methods=["GET", "POST"])

def add_contact():

    if "admin" not in session:

        return redirect("/login")

    if request.method == "POST":

        nom = request.form["nom"]

        email = request.form["email"]

        telephone = request.form["telephone"]

        categorie = request.form["categorie"]

        adresse = request.form["adresse"]

        fonction = request.form["fonction"]

        entreprise = request.form["entreprise"]

        conn = get_connection()

        cursor = conn.cursor()

        try:

            cursor.execute("""

            INSERT INTO contacts(

                nom,
                email,
                telephone,
                categorie,
                adresse,
                fonction,
                entreprise

            )

            VALUES(?,?,?,?,?,?,?)

            """, (

                nom,
                email,
                telephone,
                categorie,
                adresse,
                fonction,
                entreprise

            ))

            conn.commit()

        except:

            conn.close()

            return "Erreur : email déjà utilisé"

        conn.close()

        flash("✅ Contact ajouté avec succès")

        return redirect("/")

    return render_template("add.html")
# ==========================
# EDIT CONTACT
# ==========================

@app.route("/edit/<int:id>", methods=["GET", "POST"])

def edit_contact(id):

    if "admin" not in session:

        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor()

    if request.method == "POST":

        nom = request.form["nom"]

        email = request.form["email"]

        telephone = request.form["telephone"]

        categorie = request.form["categorie"]

        adresse = request.form["adresse"]

        fonction = request.form["fonction"]

        entreprise = request.form["entreprise"]

        cursor.execute("""

        UPDATE contacts

        SET

            nom=?,
            email=?,
            telephone=?,
            categorie=?,
            adresse=?,
            fonction=?,
            entreprise=?

        WHERE id=?

        """, (

            nom,
            email,
            telephone,
            categorie,
            adresse,
            fonction,
            entreprise,
            id

        ))

        conn.commit()

        conn.close()

        flash("✅ Contact modifié avec succès")

        return redirect("/")

    cursor.execute(
        "SELECT * FROM contacts WHERE id=?",
        (id,)
    )

    contact = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        contact=contact
    )
# ==========================
# DELETE CONTACT
# ==========================

@app.route("/delete/<int:id>")

def delete_contact(id):

    if "admin" not in session:

        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    flash("✅ Contact supprimé avec succès")

    return redirect("/")

# ==========================
# EXPORT CSV
# ==========================

@app.route("/export")

def export_csv():

    if "admin" not in session:

        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT nom,email,telephone,categorie,adresse,fonction,entreprise FROM contacts
    """)

    contacts = cursor.fetchall()

    conn.close()

    with open(
        "contacts.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Nom",
            "Email",
            "Téléphone",
            "Categorie",
            "Adresse",
            "Fonction",
            "Entreprise"
        ])

        writer.writerows(contacts)

    flash("✅ Export CSV réalisé avec succès")

    return redirect("/")

# ==========================
# EMAIL
# ==========================

@app.route("/email/<int:id>", methods=["GET", "POST"])

def email(id):

    if "admin" not in session:

        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM contacts WHERE id=?",
        (id,)
    )

    contact = cursor.fetchone()

    conn.close()

    if request.method == "POST":

        receiver = request.form["receiver"]

        subject = request.form["subject"]

        message_text = request.form["message"]

        sender = "meryem.hachamialaoui@gmail.com"

        try:

            message = MIMEMultipart()

            message["From"] = sender

            message["To"] = receiver

            message["Subject"] = subject

            message.attach(
                MIMEText(message_text, "plain")
            )

            server = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            server.starttls()

            server.login(
                sender,
                "syff ujcz dqkv sjzl"
            )

            server.send_message(message)

            server.quit()

            flash("✅ Email envoyé avec succès")

            return redirect("/")

        except Exception as e:

            flash(f"❌ Erreur : {e}")

            return redirect("/")

    return render_template(
        "email_form.html",
        contact=contact
    )

# ==========================
# WHATSAPP
# ==========================

@app.route("/whatsapp/<int:id>", methods=["GET", "POST"])

def whatsapp(id):

    if "admin" not in session:

        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM contacts WHERE id=?",
        (id,)
    )

    contact = cursor.fetchone()

    conn.close()

    if request.method == "POST":

        phone = request.form["phone"]

        message = request.form["message"]

        # Maroc

        phone = phone.replace("0", "212", 1)

        # ENCODE MESSAGE

        message = urllib.parse.quote(message)

        # URL WHATSAPP

        url = f"https://wa.me/{phone}?text={message}"

        return redirect(url)

    return render_template(
        "whatsapp_form.html",
        contact=contact
    )

# ==========================
# GOOGLE CALENDAR RDV
# ==========================

@app.route("/rdv/<int:id>")

def rdv(id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM contacts WHERE id=?",

        (id,)

    )

    contact = cursor.fetchone()

    conn.close()

    # DATE RDV
    date = "20260115T100000"

    end = "20260115T103000"

    # TITRE
    title = f"Rendez-vous avec {contact['nom']}"

    # DETAILS SANS RETOUR LIGNE
    details = (

        f"Contact: {contact['nom']} - "

        f"Telephone: {contact['telephone']} - "

        f"Email: {contact['email']}"

    )

    # URL GOOGLE CALENDAR
    url = (

        "https://calendar.google.com/calendar/render"

        f"?action=TEMPLATE"

        f"&text={title}"

        f"&dates={date}/{end}"

        f"&details={details}"

    )

    return redirect(url)
# ==========================
# RUN
# ==========================

if __name__ == "__main__":

    app.run(debug=True)