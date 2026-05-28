import tkinter as tk
from tkinter import ttk, messagebox

from database import Database

db = Database()

# ==========================
# APPLICATION
# ==========================

def run_app():

    root = tk.Tk()

    root.title("Gestion des Contacts")

    root.geometry("950x600")

    # ==========================
    # AJOUT CONTACT
    # ==========================

    def ajouter_contact():

        nom = entry_nom.get()

        email = entry_email.get()

        telephone = entry_tel.get()

        if nom == "" or email == "" or telephone == "":

            messagebox.showwarning(
                "Attention",
                "Tous les champs sont obligatoires"
            )

            return

        success = db.add_contact(
            nom,
            email,
            telephone
        )

        if success:

            messagebox.showinfo(
                "Succès",
                "Contact ajouté"
            )

            afficher_contacts()

            clear_fields()

        else:

            messagebox.showerror(
                "Erreur",
                "Email déjà utilisé"
            )

    # ==========================
    # SUPPRIMER CONTACT
    # ==========================

    def supprimer_contact():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Attention",
                "Sélectionnez un contact"
            )

            return

        values = tree.item(selected)["values"]

        contact_id = values[0]

        # supprimer seulement SQLite
        if contact_id < 1000:

            db.delete_contact_by_id(contact_id)

        afficher_contacts()

    # ==========================
    # AFFICHER CONTACTS
    # ==========================

    def afficher_contacts():

        # vider tableau
        for row in tree.get_children():

            tree.delete(row)

        # SQLite
        contacts_sqlite = db.get_contacts()

        # CSV
        contacts_csv = db.get_csv_contacts()

        displayed_emails = set()

        # SQLITE
        for contact in contacts_sqlite:

            tree.insert(
                "",
                "end",
                values=contact
            )

            displayed_emails.add(contact[2])

        # CSV
        for contact in contacts_csv:

            email = contact[2]

            if email not in displayed_emails:

                tree.insert(
                    "",
                    "end",
                    values=contact
                )

                displayed_emails.add(email)

    # ==========================
    # EXPORT CSV
    # ==========================

    def exporter_csv():

        db.export_csv()

        messagebox.showinfo(
            "Succès",
            "Export CSV terminé"
        )

    # ==========================
    # CLEAR FIELDS
    # ==========================

    def clear_fields():

        entry_nom.delete(0, tk.END)

        entry_email.delete(0, tk.END)

        entry_tel.delete(0, tk.END)

    # ==========================
    # TITLE
    # ==========================

    title = tk.Label(
        root,
        text="📒 Gestion des Contacts",
        font=("Segoe UI", 22, "bold")
    )

    title.pack(pady=15)

    # ==========================
    # TABLE
    # ==========================

    columns = (
        "ID",
        "Nom",
        "Email",
        "Téléphone"
    )

    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=12
    )

    for col in columns:

        tree.heading(col, text=col)

        if col == "ID":

            tree.column(col, width=70)

        else:

            tree.column(col, width=260)

    tree.pack(pady=10)

    # ==========================
    # FORM
    # ==========================

    frame = tk.Frame(root)

    frame.pack(pady=15)

    # NOM
    tk.Label(
        frame,
        text="Nom"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5
    )

    entry_nom = tk.Entry(frame)

    entry_nom.grid(
        row=0,
        column=1,
        pady=5
    )

    # EMAIL
    tk.Label(
        frame,
        text="Email"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=5
    )

    entry_email = tk.Entry(frame)

    entry_email.grid(
        row=1,
        column=1,
        pady=5
    )

    # TELEPHONE
    tk.Label(
        frame,
        text="Téléphone"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=5
    )

    entry_tel = tk.Entry(frame)

    entry_tel.grid(
        row=2,
        column=1,
        pady=5
    )

    # ==========================
    # BUTTONS
    # ==========================

    frame_buttons = tk.Frame(root)

    frame_buttons.pack(pady=20)

    # AJOUTER
    btn_add = tk.Button(
        frame_buttons,
        text="Ajouter",
        bg="#27ae60",
        fg="white",
        width=15,
        command=ajouter_contact
    )

    btn_add.grid(
        row=0,
        column=0,
        padx=10
    )

    # SUPPRIMER
    btn_delete = tk.Button(
        frame_buttons,
        text="Supprimer",
        bg="#e74c3c",
        fg="white",
        width=15,
        command=supprimer_contact
    )

    btn_delete.grid(
        row=0,
        column=1,
        padx=10
    )

    # EXPORT CSV
    btn_export = tk.Button(
        frame_buttons,
        text="Exporter CSV",
        bg="#3498db",
        fg="white",
        width=15,
        command=exporter_csv
    )

    btn_export.grid(
        row=0,
        column=2,
        padx=10
    )

    # ==========================
    # LOAD CONTACTS
    # ==========================

    afficher_contacts()

    # ==========================
    # MAINLOOP
    # ==========================

    root.mainloop()


# ==========================
# RUN
# ==========================

if __name__ == "__main__":

    run_app()