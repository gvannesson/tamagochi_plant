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
