import random


SEUIL_BAS = 100
SEUIL_HAUT = 300
SEUIL_BAS_ENGRAIS = 200
SEUIL_HAUT_ENGRAIS = 400

SANTE_MAX = 10
NB_TOURS_POUR_AUGMENTER_SANTE = 3

class MaPlante :


    def __init__(self, nom, feuilles):
        self.nom = nom
        self.feuilles = feuilles

        self.azote_tot = 0
        
        self.besoin_eau = self.calcul_besoin_eau()
        self.besoin_engrais = self.calcul_besoin_engrais()
        self.points_sante = SANTE_MAX
        self.niveau_eau = self.besoin_eau
        self.niveau_engrais = self.besoin_engrais
        self.compteur_bons_tours = 0

    def calcul_azote(self):

        from utils import charger_excel
        
        chemin_fichier = ("MTG.xlsx")  
        df = charger_excel(chemin_fichier)
        df_filtre = df[df['label'] == 'FababeanLeaf']


        self.azote_tot = df_filtre['NitrogenDemand'].sum()

        self.besoin_engrais = self.calcul_besoin_engrais()
        self.niveau_engrais = df_filtre['NitrogenContent'].sum()

        return self.azote_tot

    def calcul_besoin_eau(self):
        besoin_eau = random.randint(2,4)*self.feuilles -1
        return besoin_eau
    
    def calcul_besoin_engrais(self):
        besoin_engrais = self.azote_tot
        return besoin_engrais

    def __str__(self):
        return f'{self.nom} est une jolie plante avec {self.feuilles} feuilles'

    def recevoir_eau(self, ajout_eau):
        self.niveau_eau = self.niveau_eau + ajout_eau

    def recevoir_engrais(self, ajout_engrais):
        self.niveau_engrais = self.niveau_engrais+ajout_engrais

        return self.niveau_engrais

    def consommation_eau(self):
        self.niveau_eau = max(0, self.niveau_eau-self.besoin_eau)

    def consommation_engrais(self):
        self.niveau_engrais = max(0, self.niveau_engrais-self.besoin_engrais)

    def classement_niveau_eau(self, niveau):
        if niveau < SEUIL_BAS:
            return "trop_bas"
        elif niveau > SEUIL_HAUT:
            return "trop_haut"
        else:
            return "ok"

    def classement_niveau_engrais(self, niveau):
            if niveau < SEUIL_BAS_ENGRAIS:
                return "trop_bas"
            elif niveau > SEUIL_HAUT_ENGRAIS:
                return "trop_haut"
            else:
                return "ok"

    def donner_indices(self):
        zone_eau = self.classement_niveau_eau(self.niveau_eau)
        zone_engrais = self.classement_niveau_engrais(self.niveau_engrais)

        indices_eau = {
            "trop_bas": "La terre est sèche et les feuilles peuvent jaunir.",
            "ok": "La terre est humide juste comme il faut.",
            "trop_haut": "La terre est détrempée et les feuilles sont flétries.",
        }
        indices_engrais = {
            "trop_bas": "Les feuilles sont pâles et la plante pousse lentement.",
            "ok": "Les feuilles sont d'un beau vert.",
            "trop_haut": "Le bord des feuilles brunit et une croûte blanche couvre la terre.",
        }

        return indices_eau[zone_eau] + "\n" + indices_engrais[zone_engrais]


    def mettre_a_jour_sante(self):
        zone_eau = self.classement_niveau_eau(self.niveau_eau)
        zone_engrais = self.classement_niveau_engrais(self.niveau_engrais)

        if zone_eau == "ok" and zone_engrais == "ok":
            self.compteur_bons_tours += 1
            if self.compteur_bons_tours == NB_TOURS_POUR_AUGMENTER_SANTE:
                self.points_sante += 1
                self.compteur_bons_tours = 0
        else:
            self.compteur_bons_tours = 0
            if zone_eau != "ok":
                self.points_sante -= 1
            if zone_engrais != "ok":
                self.points_sante -= 1

        self.points_sante = max(0, min(self.points_sante, SANTE_MAX))

    def est_vivante(self):
        return self.points_sante > 0

    ##############################################################################

