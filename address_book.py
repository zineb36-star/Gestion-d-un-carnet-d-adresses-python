from contact import Contact
import os
class AddressBook:
    def __init__(self):
        self.filename = "contacts.txt"

        # créer fichier s'il n'existe pas
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    # lire depuis fichier
    def load_contacts(self):
        contacts = []
        with open(self.filename, "r") as f:
            for ligne in f:
                if ligne.strip():
                    contacts.append(Contact.from_string(ligne))
                    print(ligne)
        return contacts

    # écrire dans fichier
    def save_contacts(self, contacts):
        with open(self.filename, "w") as f:
            for contact in contacts:
                f.write(str(contact) + "\n")

    # ajouter contact
    def add_contact(self, contact):
        contacts = self.load_contacts()

        # gestion doublon
        for c in contacts:
            if c.email == contact.email:
                print("Contact déjà existant")
                return

        # écrire directement dans fichier
        with open(self.filename, "a") as f:
            f.write(str(contact) + "\n")

        print("Contact ajouté")

    # supprimer contact
    def remove_contact(self, email):
        contacts = self.load_contacts()
        new_contacts = []

        for contact in contacts:
            if contact.email != email:
                new_contacts.append(contact)

        self.save_contacts(new_contacts)
        print("Contact supprimé")

    # afficher contacts
    def display_contacts(self):
        contacts = self.load_contacts()

        if len(contacts) == 0:
            print("Aucun contact")
        else:
            print("\nListe des contacts :")
            for contact in contacts:
                print(contact)