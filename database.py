import sqlite3
import csv


class Database:

    def __init__(self):

        self.conn = sqlite3.connect("contacts.db")

        self.cursor = self.conn.cursor()

        self.create_tables()

    # ==========================
    # TABLES
    # ==========================

    def create_tables(self):

        # table contacts
        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS contacts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            telephone TEXT NOT NULL

        )

        """)

        # table admins
        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS admins(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )

        """)

        self.conn.commit()

        self.create_default_admin()

    # ==========================
    # ADMIN PAR DÉFAUT
    # ==========================

    def create_default_admin(self):

        self.cursor.execute(
            "SELECT * FROM admins WHERE username=?",
            ("admin",)
        )

        admin = self.cursor.fetchone()

        if admin is None:

            self.cursor.execute(
                "INSERT INTO admins(username,password) VALUES(?,?)",
                ("admin", "admin123")
            )

            self.conn.commit()

    # ==========================
    # LOGIN
    # ==========================

    def login(self, username, password):

        self.cursor.execute(
            "SELECT * FROM admins WHERE username=? AND password=?",
            (username, password)
        )

        admin = self.cursor.fetchone()

        return admin is not None

    # ==========================
    # AJOUT CONTACT SQLITE
    # ==========================

    def add_contact(self, nom, email, telephone):

        try:

            self.cursor.execute(
                "INSERT INTO contacts(nom,email,telephone) VALUES(?,?,?)",
                (nom, email, telephone)
            )

            self.conn.commit()

            return True

        except:

            return False

    # ==========================
    # CONTACTS SQLITE
    # ==========================

    def get_contacts(self):

        self.cursor.execute(
            "SELECT id, nom, email, telephone FROM contacts"
        )

        return self.cursor.fetchall()

    # ==========================
    # CONTACTS CSV
    # ==========================

    def get_csv_contacts(self):

        contacts = []

        try:

            with open(
                "contacts.csv",
                "r",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                # ignorer header
                next(reader, None)

                current_id = 1000

                for row in reader:

                    # CSV :
                    # Nom,Email,Téléphone

                    if len(row) == 3:

                        nom = row[0]
                        email = row[1]
                        telephone = row[2]

                        contacts.append((
                            current_id,
                            nom,
                            email,
                            telephone
                        ))

                        current_id += 1

        except FileNotFoundError:

            pass

        return contacts

    # ==========================
    # SUPPRIMER CONTACT
    # ==========================

    def delete_contact_by_id(self, contact_id):

        self.cursor.execute(
            "DELETE FROM contacts WHERE id=?",
            (contact_id,)
        )

        self.conn.commit()

    # ==========================
    # EXPORT CSV
    # ==========================

    def export_csv(self):

        contacts_db = self.get_contacts()

        existing_emails = set()

        # ==========================
        # LIRE CSV EXISTANT
        # ==========================

        try:

            with open(
                "contacts.csv",
                "r",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                next(reader, None)

                for row in reader:

                    if len(row) >= 2:

                        existing_emails.add(row[1])

        except FileNotFoundError:

            pass

        # ==========================
        # AJOUT CSV
        # ==========================

        with open(
            "contacts.csv",
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # HEADER
            if file.tell() == 0:

                writer.writerow([
                    "Nom",
                    "Email",
                    "Téléphone"
                ])

            # SQLITE -> CSV
            for contact in contacts_db:

                nom = contact[1]
                email = contact[2]
                telephone = contact[3]

                if email not in existing_emails:

                    writer.writerow([
                        nom,
                        email,
                        telephone
                    ])

                    existing_emails.add(email)

            # TXT -> CSV
            try:

                with open(
                    "contacts.txt",
                    "r",
                    encoding="utf-8"
                ) as txt_file:

                    for ligne in txt_file:

                        ligne = ligne.strip()

                        if ligne:

                            data = ligne.split(";")

                            if len(data) == 3:

                                nom = data[0]
                                email = data[1]
                                telephone = data[2]

                                if email not in existing_emails:

                                    writer.writerow([
                                        nom,
                                        email,
                                        telephone
                                    ])

                                    existing_emails.add(email)

            except FileNotFoundError:

                pass

        print("Export CSV terminé")