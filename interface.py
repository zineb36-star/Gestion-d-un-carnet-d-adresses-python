import tkinter as tk
from tkinter import ttk, messagebox

from contact import Contact
from address_book import AddressBook

book = AddressBook()

# ==========================
# FONCTIONS
# ==========================

def ajouter_contact():

    nom = entry_nom.get()
    email = entry_email.get()
    numtele = entry_numtele.get()

    if not nom or not email:

        messagebox.showwarning(
            "Attention",
            "Nom et Email sont obligatoires"
        )

        return

    try:

        contact = Contact(nom, email, numtele)

        book.add_contact(contact)

        afficher_contacts()

        clear_fields()

    except Exception as e:

        messagebox.showerror(
            "Erreur",
            str(e)
        )


def supprimer_contact():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Attention",
            "Sélectionnez un contact"
        )

        return

    values = tree.item(selected)["values"]

    email = values[1]

    book.remove_contact(email)

    afficher_contacts()


def afficher_contacts():

    for row in tree.get_children():

        tree.delete(row)

    contacts = book.load_contacts()

    contacts.sort(key=lambda c: c.nom.lower())

    for c in contacts:

        tree.insert(
            "",
            "end",
            values=(c.nom, c.email, c.numtele)
        )


def clear_fields():

    entry_nom.delete(0, tk.END)

    entry_email.delete(0, tk.END)

    entry_numtele.delete(0, tk.END)

# ==========================
# INTERFACE
# ==========================

root = tk.Tk()

root.title("Carnet d'adresses Pro")

root.geometry("700x500")

style = ttk.Style()

style.theme_use("clam")

# ==========================
# TITRE
# ==========================

title = ttk.Label(
    root,
    text="📒 Carnet d'adresses",
    font=("Segoe UI", 18, "bold")
)

title.pack(pady=10)

# ==========================
# TABLE
# ==========================

frame_table = ttk.Frame(root)

frame_table.pack(pady=10)

columns = ("Nom", "Email", "Téléphone")

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings",
    height=10
)

for col in columns:

    tree.heading(col, text=col)

    tree.column(col, width=200)

tree.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(
    frame_table,
    orient="vertical",
    command=tree.yview
)

scrollbar.pack(side=tk.RIGHT, fill="y")

tree.configure(yscrollcommand=scrollbar.set)

# ==========================
# FORMULAIRE
# ==========================

frame_form = ttk.LabelFrame(
    root,
    text="Ajouter un contact"
)

frame_form.pack(
    pady=10,
    fill="x",
    padx=20
)

ttk.Label(frame_form, text="Nom").grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)

entry_nom = ttk.Entry(frame_form)

entry_nom.grid(row=0, column=1)

ttk.Label(frame_form, text="Email").grid(
    row=1,
    column=0,
    padx=10,
    pady=5
)

entry_email = ttk.Entry(frame_form)

entry_email.grid(row=1, column=1)

ttk.Label(frame_form, text="Téléphone").grid(
    row=2,
    column=0,
    padx=10,
    pady=5
)

entry_numtele = ttk.Entry(frame_form)

entry_numtele.grid(row=2, column=1)

# ==========================
# BOUTONS
# ==========================

frame_buttons = ttk.Frame(root)

frame_buttons.pack(pady=10)

btn_add = ttk.Button(
    frame_buttons,
    text="Ajouter",
    command=ajouter_contact
)

btn_add.grid(row=0, column=0, padx=10)

btn_delete = ttk.Button(
    frame_buttons,
    text="Supprimer",
    command=supprimer_contact
)

btn_delete.grid(row=0, column=1, padx=10)

btn_show = ttk.Button(
    frame_buttons,
    text="Afficher",
    command=afficher_contacts
)

btn_show.grid(row=0, column=2, padx=10)