##########################################################################################
from utils import charger_excel



chemin_fichier = ("MTG.xlsx")  # .parent remonte d'un cran

# Importation des données
df = charger_excel(chemin_fichier)
print(df['label'])

df_filtre = df[df['label'] == 'FababeanLeaf']

#résultat
print(df_filtre)


#########################################################################################################""
