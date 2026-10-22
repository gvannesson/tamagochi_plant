from utils import demander_nombre_entier_positif
from plante import Plante

SANTE_MAX = 12



print("""Bienvenue dans ton Tamagochi Plant
Ton but: Prendre soin de ton amie la plante""")


nom_plante = input('Donne un nom à ta plante ')
petales = demander_nombre_entier_positif('Combien de pétales a ta plante ? ')
feuilles = demander_nombre_entier_positif('Combien de feuilles a ta plante ? ')

plante = Plante(nom_plante, feuilles, petales)
print(plante)