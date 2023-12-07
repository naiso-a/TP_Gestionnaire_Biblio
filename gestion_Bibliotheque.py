import json


class NotificateurDeLivre:
    def __init__(self):
        self.observer = []

    def ajouter_observer(self, observer):
        self.observer.append(observer)

    def notificateur_observer(self, livre):
        for observer in self.observer:
            observer.actualiser(livre)


# modele singleton inspiré par chatgpt
class Bibliothèque:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Bibliothèque, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.livres = []
        self.utilisateurs = []
        self.notificateur = NotificateurDeLivre()

    def ajouter_livre(self, livre):
        self.livres.append(livre)
        self.notificateur.notificateur_observer(livre)

    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs.append(utilisateur)

    def sauvegarde(self):
        # Sauvegarde de l'état de la bibliothèque au format JSON
        data = {"livres": [livre.__dict__ for livre in self.livres],
                "utilisateurs": [user.__dict__ for user in self.utilisateurs]}
        with open("bibliotheque_sauvegarde.json", "w") as file:
            json.dump(data, file)


# Factory inspiré du site https://iscinumpy.gitlab.io/post/factory-classmethods-in-python/
class Livre:
    def __init__(self, titre, auteur, categorie):
        self.titre = titre
        self.auteur = auteur
        self.categorie = categorie

    @classmethod
    def creer_livre(cls, titre, auteur, categorie):
        return cls(titre, auteur, categorie)


class Utilisateur:
    def __init__(self, nom):
        self.nom = nom
        self.banni = False

    def bannir(self):
        self.banni = True
        print(f"{self.nom} a été banni.")

    def emprunter_livre(self, livre):
        print(f"{self.nom} ne peut pas emprunter de livre. Utilisateur non abonné.")


class UtilisateurAbonne(Utilisateur):
    def __init__(self, nom):
        super().__init__(nom)
        self.abonnement_active = False
        self.livres_empruntes = []

    def souscrire_abonnement(self):
        self.abonnement_active = True
        print(f"{self.nom} a souscrit à un abonnement.")

    def emprunter_livre(self, livre):
        if not self.banni and self.abonnement_active:
            self.livres_empruntes.append(livre)
            print(f"{self.nom} a emprunté le livre {livre.titre}")
        else:
            print(f"{self.nom} ne peut pas emprunter de livre.")

    def retourner_livre(self, livre):
        if livre in self.livres_empruntes:
            self.livres_empruntes.remove(livre)
            print(f"{self.nom} a rendu le livre {livre.titre}")
        else:
            print(f"{self.nom} ne peut pas rendre ce livre.")


class Recherche:
    def __init__(self, strategie):
        self.strategie = strategie

    def effectuer_recherche(self, requete, livres):
        return self.strategie.rechercher(requete, livres)


# squelette de la classe StrategieRecherche inspiré par chatgpt
class StrategieRecherche:
    def rechercher(self, requete, livres):
        pass


class RechercheTitreStrategie(StrategieRecherche):
    def rechercher(self, requete, livres):
        return [livre for livre in livres if requete.lower() in livre.titre.lower()]


class RechercheAuteurStrategie(StrategieRecherche):
    def rechercher(self, requete, livres):
        return [livre for livre in livres if requete.lower() in livre.auteur.lower()]


class RechercheCategorieStrategie(StrategieRecherche):
    def rechercher(self, requete, livres):
        return [livre for livre in livres if requete.lower() in livre.categorie.lower()]


if __name__ == "__main__":
    bibliotheque = Bibliothèque()

    livre1 = Livre.creer_livre("Le Seigneur des Anneaux", "J.R.R. Tolkien", "Fantasy")
    livre2 = Livre.creer_livre("Harry Potter", "J.K. Rowling", "Fantasy")
    livre3 = Livre.creer_livre("Les Misérables", "Victor Hugo", "Classique")

    bibliotheque.ajouter_livre(livre1)
    bibliotheque.ajouter_livre(livre2)
    bibliotheque.ajouter_livre(livre3)

    utilisateur1 = UtilisateurAbonne("Martin")
    utilisateur2 = Utilisateur("Louis")

    bibliotheque.ajouter_utilisateur(utilisateur1)
    bibliotheque.ajouter_utilisateur(utilisateur2)

    utilisateur1.souscrire_abonnement()

    utilisateur1.emprunter_livre(livre1)
    utilisateur2.emprunter_livre(livre2)

    recherche_titre = Recherche(RechercheTitreStrategie())
    resultat_recherche_titre = recherche_titre.effectuer_recherche("Seigneur", bibliotheque.livres)
    print("Résultat de la recherche par titre:")
    for livre in resultat_recherche_titre:
        print(f"Titre: {livre.titre}, Auteur: {livre.auteur}, Catégorie: {livre.categorie}")


    recherche_auteur = Recherche(RechercheAuteurStrategie())
    resultat_recherche_auteur = recherche_auteur.effectuer_recherche("Rowling", bibliotheque.livres)
    print("Résultat de la recherche par auteur:")
    for livre in resultat_recherche_auteur:
        print(f"Titre: {livre.titre}, Auteur: {livre.auteur}, Catégorie: {livre.categorie}")


    recherche_categorie = Recherche(RechercheCategorieStrategie())
    resultat_recherche_categorie = recherche_categorie.effectuer_recherche("Fantasy", bibliotheque.livres)
    print("Résultat de la recherche par catégorie:")
    for livre in resultat_recherche_categorie:
        print(f"Titre: {livre.titre}, Auteur: {livre.auteur}, Catégorie: {livre.categorie}")

utilisateur1.retourner_livre(livre1)

bibliotheque.sauvegarde()
