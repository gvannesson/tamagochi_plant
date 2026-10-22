def demander_nombre_entier_positif(entree_utilisateur):
    while True:
        saisie = input(entree_utilisateur)
        try:
            nombre = int(saisie)
            if nombre >= 0:
                return nombre
            else:
                print("Veuillez entrer un nombre entier positif.")
        except ValueError:
            print("Veuillez entrer un nombre entier positif.")   