import hashlib
import os


class Auth:

    def __init__(self):

        self.filename = "users.txt"

        # créer admin par défaut
        if not os.path.exists(self.filename):

            self.create_default_admin()

    # hachage mot de passe
    def hash_password(self, password):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    # créer admin
    def create_default_admin(self):

        username = "admin"

        password = "admin123"

        hashed = self.hash_password(password)

        with open(self.filename, "w") as f:

            f.write(f"{username};{hashed}\n")

    # connexion
    def login(self, username, password):

        hashed = self.hash_password(password)

        with open(self.filename, "r") as f:

            for line in f:

                user, pwd = line.strip().split(";")

                if user == username and pwd == hashed:

                    return True

        return False