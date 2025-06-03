import sqlite3
import os
from datetime import datetime
from ultralytics import YOLO

# === Paramètres ===
chemin_image = r"C:\cours_b3\mspr-ia\WildLens_MSPR\test\th.jpeg"
chemin_modele = r"C:\cours_b3\mspr-ia\runs\detect\train2\weights\best.pt"
chemin_bdd = r"C:\cours_b3\mspr-ia\WildLens_MSPR\database\wildlens.db"

# === Dictionnaire de correspondance des noms YOLO → noms en base ===
traductions = {
    "dog": "Chien",
    "cat": "Chat",
    "wolf": "Loup",
    "fox": "Renard",
    "bear": "Ours",
    "puma": "Puma",
    "raccoon": "Raton laveur",
    "rabbit": "Lapin",
    "squirrel": "Écureuil",
    "rat": "Rat",
    "coyote": "Coyote",
    "beaver": "Castor",
    "lynx": "Lynx"  # Au cas où tu ajoutes cette classe au modèle
}

# === Étape 1 : Chargement du modèle ===
model = YOLO(chemin_modele)

# === Étape 2 : Prédiction ===
results = model.predict(chemin_image, conf=0.4)

# === Étape 3 : Traitement des résultats ===
for result in results:
    boxes = result.boxes
    names = model.names

    for box in boxes:
        class_id = int(box.cls[0])
        nom_yolo = names[class_id]  # ex : "bear"
        nom_fr = traductions.get(nom_yolo.lower(), nom_yolo)
        confiance = float(box.conf[0])
        print(f"Espèce détectée : {nom_yolo} → {nom_fr} avec confiance {confiance:.2f}")

        # === Étape 4 : Connexion à la base ===
        conn = sqlite3.connect(chemin_bdd)
        cursor = conn.cursor()

        # Recherche de l'espèce dans la base
        cursor.execute("SELECT id_espece FROM especes WHERE LOWER(nom) = ?", (nom_fr.lower(),))
        result_id = cursor.fetchone()

        if result_id:
            espece_id = result_id[0]
            date_obs = datetime.now().isoformat()
            localisation = "Test automatique"
            photo_filename = os.path.basename(chemin_image)

            cursor.execute('''
                INSERT INTO empreintes (espece_id, date, localisation, photo_filename)
                VALUES (?, ?, ?, ?)
            ''', (espece_id, date_obs, localisation, photo_filename))

            conn.commit()
            print(" Insertion en base réussie.")
        else:
            print(f" Espèce '{nom_fr}' non trouvée dans la base.")

        conn.close()
