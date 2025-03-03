import os

# Fonction pour lire les deux premières lignes d’un fichier
def lire_deux_premieres_lignes(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()
        titre = lignes[0].strip() if len(lignes) > 0 else None
        auteurs_info = lignes[1].strip() if len(lignes) > 1 else None
        return titre, auteurs_info


def lire_premieres_lignes(fichier):
    """Lit et affiche les 2 premières lignes d'un fichier."""
    try:
        with open(fichier, "r", encoding="utf-8") as file:
            lignes = [file.readline().strip() for _ in range(2)]  # Lire 2 lignes
            print(f"\n📄 Fichier : {fichier}")
            for ligne in lignes:
                print(ligne)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier}' est introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")


def parcourir_dossiers(racine):
    """Parcourt récursivement les dossiers et traite chaque fichier."""
    for dossier, _, fichiers in os.walk(racine):
        for fichier in fichiers:
            chemin_fichier = os.path.join(dossier, fichier)
            lire_premieres_lignes(chemin_fichier)

# Fonction pour lire le titre (1ère ligne) d’un fichier
def lire_premiere_ligne(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return f.readline().strip()  # Lire la première ligne et enlever les espaces inutiles

