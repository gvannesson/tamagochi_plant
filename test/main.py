import random
from plant import Plant


# --- Simulation sur 7 jours avec météo aléatoire ---
ma_monstera = Plant("Ma monstera")
possibilites_meteo = ["Pluie", "Grand Soleil", "Nuageux"]

#TO DO
#+ Ajouter la possibilité de déplacer la plante à l'intérieur
#+ Ajouter une température et humidité intérieure ?
#+ Ajouter des attaques d'insectes/ravageurs ?


for jour in range(1, 8):
  meteo_du_jour = random.choice(possibilites_meteo)
  ma_monstera.simulate_day(jour, meteo_du_jour)




