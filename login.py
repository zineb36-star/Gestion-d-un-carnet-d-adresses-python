import tkinter as tk
from tkinter import messagebox

import main

from database import Database

db = Database()

# ==========================
# LOGIN
# ==========================

def verifier_login():

    username = entry_user.get()

    password = entry_pass.get()

    if db.login(username, password):

        messagebox.showinfo(
            "Succès",
            "Connexion réussie"
        )

        login_window.destroy()

        main.run_app()

    else:

        messagebox.showerror(
            "Erreur",
            "Login incorrect"
        )

# ==========================
# WINDOW
# ==========================

login_window = tk.Tk()

login_window.title("Connexion")

login_window.geometry("350x250")

login_window.config(bg="#1e1e2f")

# ==========================
# TITLE
# ==========================

title = tk.Label(
    login_window,
    text="🔐 Connexion",
    font=("Segoe UI", 18, "bold"),
    bg="#1e1e2f",
    fg="white"
)

title.pack(pady=20)

# ==========================
# USERNAME
# ==========================

tk.Label(
    login_window,
    text="Nom utilisateur",
    bg="#1e1e2f",
    fg="white"
).pack()

entry_user = tk.Entry(login_window)

entry_user.pack(pady=5)

# ==========================
# PASSWORD
# ==========================

tk.Label(
    login_window,
    text="Mot de passe",
    bg="#1e1e2f",
    fg="white"
).pack()

entry_pass = tk.Entry(
    login_window,
    show="*"
)

entry_pass.pack(pady=5)

# ==========================
# BUTTON
# ==========================

btn = tk.Button(
    login_window,
    text="Connexion",
    bg="#27ae60",
    fg="white",
    width=15,
    command=verifier_login
)

btn.pack(pady=20)

# ==========================
# MAINLOOP
# ==========================

login_window.mainloop()