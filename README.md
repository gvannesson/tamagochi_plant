

# Installation du jeu

1. Ouvrir son prompt Anaconda

2. Insérer :

## Principe

1. Tu crées ta plante en choisissant son nom, son nombre de feuilles et de pétales.
2. Ces choix déterminent ses besoins en eau et en engrais, qui restent secrets.
3. Chaque jour, tu lui donnes de l'eau et de l'engrais. La plante en consomme une partie.
4. Des indices (terre sèche, feuilles pâles…) t'aident à deviner si tu en donnes trop ou pas assez.
5. Trop ou pas assez, et la plante perd des points de santé. À 0, elle meurt.

## Lancer le jeu

Prérequis : Python 3, sans bibliothèque externe.

```bash
Chemin d'installation des packages nécessaire pour l'utilisation du modèle APTOS
conda create -n openalea_fresh -c openalea3 -c conda-forge openalea.plantgl openalea.lpy openalea.mtg openalea.caribu openalea.libcaribu pandas matplotlib oawidgets-y

-- Il s'agit des packages nécessaires à l'utilisation du modèle de plante APTOS (Solen)

3. Cloner le jeu à partir du dépôt Github. Dans ton prompt, aller dans le dossier où se situe le jeu cloné

4. Aller dans le module demo : cd demo

5. Lancer le fichier : python main.py

6. LET'S GO 

# Tamagochi Plant

Un petit jeu en console : prends soin d'une plante virtuelle et garde-la en vie le plus longtemps possible.

## Principe

1. Tu crées ta plante en choisissant son nom, son nombre de feuilles et de pétales.
2. Ces choix déterminent ses besoins en eau et en engrais, qui restent secrets.
3. Chaque jour, tu lui donnes de l'eau et de l'engrais. La plante en consomme une partie.
4. Des indices (terre sèche, feuilles pâles…) t'aident à deviner si tu en donnes trop ou pas assez.
5. Trop ou pas assez, et la plante perd des points de santé. À 0, elle meurt.

## Lancer le jeu

Prérequis : Python 3, sans bibliothèque externe.

```bash
python main.py
```

## Organisation du code

| Fichier | Rôle |
|---|---|
| `main.py` | Déroulement de la partie et dialogue avec le joueur |
| `plante.py` | Classe `Plante` : besoins, niveaux d'eau et d'engrais, santé, indices |
| `utils.py` | Saisie sécurisée des nombres |

Les règles du jeu (seuils, santé maximale…) sont des constantes en haut de `plante.py`.

## Contributeurs

- Solen Farra
- Gauthier Vannesson

Projet réalisé dans le cadre d'une formation Data Engineer.
