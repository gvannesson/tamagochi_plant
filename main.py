from utils import demander_nombre_entier_positif
from plante import Plante


print("""Bienvenue dans ton Tamagochi Plant
Ton but: Prendre soin de ton amie la plante""")


nom_plante = input('Donne un nom à ta plante ')
petales = demander_nombre_entier_positif('Combien de pétales a ta plante ? ')
feuilles = demander_nombre_entier_positif('Combien de feuilles a ta plante ? ')

plante = Plante(nom_plante, feuilles, petales)
print(plante)

nb_tours = 0
while plante.est_vivante():
        ajout_eau = demander_nombre_entier_positif("Avec combien de litres d'eau arroses tu ta plante ? ")
        ajout_engrais = demander_nombre_entier_positif("Combien de kilos d'engrais donnes tu à ta plante ? ")
        plante.recevoir_eau(ajout_eau)
        plante.recevoir_engrais(ajout_engrais)
        plante.consommation_eau()
        plante.consommation_engrais()
        plante.mettre_a_jour_sante()
        nb_tours += 1
        print(plante.donner_indices())
        print(f'ta plante a {plante.points_sante} points de santé')
print(f'ta plante est morte au bout de {nb_tours} jours')