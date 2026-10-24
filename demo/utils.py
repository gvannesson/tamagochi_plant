import pandas as pd


def demander_nombre_entier_positif(entree_utilisateur, minimum):
    while True:
        saisie = input(entree_utilisateur)
        try:
            nombre = int(saisie)
            if nombre >= minimum:
                return nombre
            else:
                print(f"Veuillez entrer un nombre entier supérieur ou égal à {minimum}.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


##################################################################################################


def charger_excel(chemin_fichier, nom_feuille=0):
  """Charge un fichier Excel et retourne un DataFrame Pandas.

  :param chemin_fichier: Chemin vers le fichier .xlsx
  :param nom_feuille: Nom ou index de la feuille (par défaut la première)
  :return: DataFrame contenant les données ou None en cas d'erreur
  """
  try:
    # Lecture du fichier Excel
    df = pd.read_excel(chemin_fichier, sheet_name=nom_feuille)
    return df
  except FileNotFoundError:
    print(f'Erreur : Le fichier {chemin_fichier} est introuvable.')
    return None
  except Exception as e:
    print(f'Une erreur est survenue : {e}')
    return None