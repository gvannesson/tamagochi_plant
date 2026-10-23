##########################################################################################
from utils import charger_excel

from pathlib import Path
import pandas as pd


# 1. Récupère le dossier où se trouve le script Python actuel
dossier_actuel = Path(__file__).resolve().parent

# 2. Construit le chemin absolu vers ton fichier Excel
# (Ajuste les '..' ou les dossiers selon l'emplacement exact de ton script par rapport à 'tamagochi_plant')
chemin_fichier = (dossier_actuel.parent / "src" / "aptos" / "MTG_00001.xlsx")  # .parent remonte d'un cran

# Importation des données
df = charger_excel(chemin_fichier)
print(df['label'])

df_filtre = df[df['label'] == 'FababeanLeaf']

#résultat
print(df_filtre)


#########################################################################################################""
