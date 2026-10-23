class Root:

  def __init__(self, length=1.0):
    self.length = length  # en cm

  def absorb_water(self, soil_moisture):
    # L'absorption dépend de la longueur des racines et de l'humidité du sol
    return self.length * 0.5 * soil_moisture
