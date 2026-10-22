class Plante:
    def __init__(self, nom, feuilles, petales):
        self.nom = nom
        self.feuilles = feuilles
        self.petales = petales
        self.besoin_eau = self.calcul_besoin_eau()
        self.besoin_engrais = self.calcul_besoin_engrais()
        self.points_sante = 10
        self.niveau_eau = self.besoin_eau
        self.niveau_engrais = self.besoin_engrais
        self.compteur_bons_tours = 0

    def calcul_besoin_eau(self):
        besoin_eau = 3*self.feuilles + 2 * self.petales -1
        return besoin_eau

    def calcul_besoin_engrais(self):
        besoin_engrais = self.feuilles + 2 * self.petales + 3
        return besoin_engrais

    def __str__(self):
        return f'{self.nom} est une jolie plante avec {self.feuilles} feuilles et {self.petales} pétales'

    def recevoir_eau(self, ajout_eau):
        self.niveau_eau = self.niveau_eau + ajout_eau

    def recevoir_engrais(self, ajout_engrais):
        self.niveau_engrais = self.niveau_engrais+ajout_engrais

    def consommation_eau(self):
        self.niveau_eau = max(0, self.niveau_eau-self.besoin_eau)

    def consommation_engrais(self):
        self.niveau_engrais = max(0, self.niveau_engrais-self.besoin_engrais)