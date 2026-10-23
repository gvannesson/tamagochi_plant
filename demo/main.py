

####################################################################################################""



from utils import demander_nombre_entier_positif
from plante import MaPlante

from aptos import main


from data import df_filtre

print("""Bienvenue dans ton Tamagochi Plant
Ton but: Prendre soin de ton amie la plante""")


nom_plante = input('Donne un nom à ta plante ')
feuilles = len(df_filtre)

plant = MaPlante(nom_plante, feuilles)
print(plant)

nb_tours = 0
while plant.est_vivante():
        plant.calculer_azote()
        ajout_eau = demander_nombre_entier_positif("Avec combien de litres d'eau arroses tu ta plante ? ", 0)
        ajout_engrais = demander_nombre_entier_positif("Combien de kilos d'engrais donnes tu à ta plante ? ", 0)
        plant.recevoir_eau(ajout_eau)
        plant.recevoir_engrais(ajout_engrais)
        plant.consommation_eau()
        plant.consommation_engrais()
        plant.mettre_a_jour_sante()
        nb_tours += 1
        print(plant.donner_indices())
        print(f'ta plante a {plant.points_sante} points de santé')

        main.Run.faba_bean_plant_simulation(default = None, initial_step = 2,final_step = 2)
        print("APTOS est mis à jour")

print(f'ta plante est morte au bout de {nb_tours} jours')