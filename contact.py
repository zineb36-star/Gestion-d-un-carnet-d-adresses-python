import re
import os

class Contact:
    def __init__(self, nom, email, numtele ):
        assert isinstance(nom, str) and len(nom)>0, "Nom invalide"
        assert isinstance(email, str) and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email), "Email invalide"
        assert isinstance(numtele, str) and numtele.isdigit() and len(numtele) >= 10, "Téléphone invalide"
        #assert isinstance(numtele, str) and numtele.isdigit() and len(numtele) >= 10
        
        self.nom = nom
        self.email = email
        self.numtele = numtele
        
    def __str__(self):
        return f"{self.nom};{self.email};{self.numtele}"
    @staticmethod
    def from_string(ligne):
        nom, email, numtele = ligne.strip().split(";")
        return Contact(nom, email, numtele)
    
    # print("Ajout contact")