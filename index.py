import os
import mysql.connector
from functions import *

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="tp_inf561"
)
cursor = conn.cursor()


def insert_institution(name):
    cursor.execute("SELECT id FROM institutions WHERE name = %s", (name,))
    result = cursor.fetchone()
    
    if result is None:
        cursor.execute("INSERT INTO institutions (name) VALUES (%s)", (name,))
        conn.commit()
        return cursor.lastrowid
    return result[0]

# Fonction pour insérer un auteur sans doublon
def insert_auteur(name, institution_id):
    cursor.execute("SELECT id FROM auteurs WHERE name = %s AND institution_id = %s", (name, institution_id))
    result = cursor.fetchone()
    
    if result is None:
        cursor.execute("INSERT INTO auteurs (name, institution_id) VALUES (%s, %s)", (name, institution_id))
        conn.commit()
        return cursor.lastrowid
    return result[0]

# Fonction pour lier un article et un auteur dans la table articles_auteurs
def insert_article_auteur(article_id, auteur_id):
    cursor.execute("SELECT * FROM articles_auteurs WHERE article_id = %s AND auteur_id = %s", (article_id, auteur_id))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO articles_auteurs (article_id, auteur_id) VALUES (%s, %s)", (article_id, auteur_id))
        conn.commit()


# Fonction pour insérer un article sans doublon
def insert_article(title, annee_id):
    # Vérifier si le titre existe déjà
    cursor.execute("SELECT id FROM articles WHERE name = %s", (title,))
    result = cursor.fetchone()

    if result is None:
        # Insérer le nouvel article
        cursor.execute("INSERT INTO articles (name, annee_id) VALUES (%s, %s)", (title, annee_id))
        conn.commit()
        print(f"✅ Ajouté : {title}")
    else:
        print(f"⚠️ Déjà en base : {title}")


# Fonction pour traiter les auteurs d’un article
def traiter_auteurs(article_id, auteurs_info):
    if not auteurs_info:
        return
    
    # Séparer les auteurs
    auteurs = auteurs_info.split("|")
    
    for auteur in auteurs:
        parts = auteur.split(", ")
        if len(parts) < 2:
            continue  # Si la structure est incorrecte, on ignore

        nom_auteur = parts[0]
        institution_nom = ", ".join(parts[1:])  # Tout le reste est l'institution
        
        # Insérer institution et récupérer son ID
        institution_id = insert_institution(institution_nom)
        
        # Insérer auteur et récupérer son ID
        auteur_id = insert_auteur(nom_auteur, institution_id)
        
        # Lier article et auteur
        insert_article_auteur(article_id, auteur_id)

def traiter_dossier(base_path):
    for root, _, files in os.walk(base_path):
        annee = os.path.basename(root).split("_")[-1]
        if not annee.isdigit():
            continue

        # Récupérer l'ID de l'année (ou l'ajouter)
        cursor.execute("SELECT id FROM annees WHERE name = %s", (annee,))
        annee_id = cursor.fetchone()
        if annee_id is None:
            cursor.execute("INSERT INTO annees (name) VALUES (%s)", (annee,))
            conn.commit()
            annee_id = cursor.lastrowid
        else:
            annee_id = annee_id[0]

        # Traiter chaque fichier
        for file in files:
            file_path = os.path.join(root, file)
            titre, auteurs_info = lire_deux_premieres_lignes(file_path)

            if titre:
                # Insérer article et récupérer son ID
                cursor.execute("SELECT id FROM articles WHERE name = %s AND annee_id = %s", (titre, annee_id))
                article_id = cursor.fetchone()
                if article_id is None:
                    cursor.execute("INSERT INTO articles (name, annee_id) VALUES (%s, %s)", (titre, annee_id))
                    conn.commit()
                    article_id = cursor.lastrowid
                else:
                    article_id = article_id[0]

                # Traiter les auteurs
                traiter_auteurs(article_id, auteurs_info)

traiter_dossier("assets")
# lire_premieres_lignes("assets/Articles_2017/article15")

































# Fermer la connexion à la BD
cursor.close()
conn.close()
