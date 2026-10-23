


#########################################################################################################

import roots as roots
import leaves as leaves
import stem as stem
import random




class Plant:

  def __init__(self, name="Plante"):
    self.name = name
    self.root = roots.Root()
    self.stem = stem.Stem()
    self.leaves = [leaves.Leaf(size=0.5)]
    self.water = 5.0
    self.energy = 5.0

  def simulate_day(self, day_number, weather):
    print(f"--- Jour {day_number} [Météo : {weather}] ---")

    soil_moisture = 1.0
    sun_multiplier = 1.0

    # 1. Impact de la météo du jour
    if weather == "Pluie":
      water_from_rain = random.uniform(3.0, 6.0)#quantité de pluie random
      self.water += water_from_rain
      soil_moisture = 1.5
      print(f"Il pleut ! La pluie apporte +{water_from_rain:.1f} d'eau.")
    elif weather == "Grand Soleil":
      sun_multiplier = 1.8
      soil_moisture = (0.7)  # Le soleil évapore une partie de l'humidité du sol
          
      
    else:
      print("Temps nuageux. Conditions neutres.")

    # 2. Les racines absorbent l'eau du sol
    water_absorbed = self.root.absorb_water(soil_moisture)
    self.water += water_absorbed
    print(f"Les racines ont absorbé {water_absorbed:.1f} d'eau.")

    # 3. Photosynthèse (influencée par le soleil)
    if self.water >= 1.5:
      total_leaf_surface = sum(leaf.size for leaf in self.leaves)
      energy_produced = total_leaf_surface * 1.2 * sun_multiplier
      self.energy += energy_produced
      self.water -= 1.2  # Consommation d'eau
      
    else:
      print(
          "Sécheresse ! Pas assez d'eau pour que les feuilles fassent la photosynthèse."
      )

    # 4. Croissance si assez d'énergie
    if self.energy >= 5.0:
      self.stem.height += 0.4
      self.root.length += 0.3
      self.energy -= 5.0

      if len(self.leaves) < 6:
        self.leaves.append(leaves.Leaf(size=1.0))
        print("Une nouvelle feuille est apparue !")

      print(
          f"Croissance : Tige = {self.stem.height:.1f} cm | Racines ="
          f" {self.root.length:.1f} cm."
      )
    else:
      print("Énergie insuffisante pour grandir aujourd'hui.")

    # Bilan de la journée
    # print(
    #     f"Bilan -> Eau : {self.water:.1f} | Énergie : {self.energy:.1f}"
    #     f" | Feuilles : {len(self.leaves)}\n"
    # )
   

####################################################################################################



