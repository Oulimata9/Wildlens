from ultralytics import YOLO
import pandas as pd
import sqlite3
from datetime import datetime
import os

# Charger le modèle YOLO
model = YOLO("app/best.pt") 

# Afficher les classes connues par le modèle YOLO
print(" Modèle YOLO chargé avec les classes :", model.names)

# Charger le fichier des espèces
df_infos = pd.read_csv("app/infos_especes.csv")

# Nettoyage : on travaille sur la colonne 'nom' maintenant
df_infos["nom"] = df_infos["nom"].astype(str).str.strip().str.lower()

# Charger les classes YOLO (en anglais)
with open("app/classes.txt", "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

# Dictionnaire : classe YOLO (anglais) ➝ nom français
yolo_to_csv_mapping = {
    "beaver": "Castor",
    "cat": "Chat",
    "dog": "Chien",
    "coyote": "Coyote",
    "fox": "Renard",
    "bear": "Ours",
    "lynx": "Lynx",
    "wolf": "Loup",
    "rabbit": "Lapin",
    "puma": "Puma",
    "squirrel": "Ecureuil",
    "rat": "Rat",
    "raccoon": "Raton laveur"
}

def predict_image(image_path: str) -> dict:
    # Faire la prédiction
    results = model(image_path)
    predictions = results[0]

    # Rien détecté
    if len(predictions.boxes.cls) == 0:
        return {
            "nom_espece": "Aucune espèce détectée",
            "description": "L'image n'a pas permis d'identifier une empreinte animale connue."
        }

    # Obtenir l’ID de la classe prédite
    predicted_class_id = int(predictions.boxes.cls[0])

    # Sécurité
    if predicted_class_id < 0 or predicted_class_id >= len(class_names):
        return {
            "nom_espece": "Classe inconnue",
            "description": f"L'ID de classe prédit ({predicted_class_id}) est hors limites."
        }

    # Obtenir le nom YOLO (anglais)
    predicted_class_name = class_names[predicted_class_id]
    print("Classe YOLO prédite :", predicted_class_name)

    # Traduire en français
    nom_csv = yolo_to_csv_mapping.get(predicted_class_name.lower())
    if not nom_csv:
        return {
            "nom_espece": "Espèce inconnue",
            "description": f"Aucune correspondance trouvée pour la classe YOLO '{predicted_class_name}'"
        }

   # Nettoyer et chercher dans le CSV
    # Nettoyer et chercher dans le CSV
    nom_csv_clean = nom_csv.strip().lower()
    infos = df_infos[df_infos["nom"] == nom_csv_clean] 


    if not infos.empty:
        info = infos.iloc[0]

        # 🔹 Enregistrement en BDD AVANT le return
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # dossier backend/app
        DB_PATH = os.path.join(BASE_DIR, "../../database/wildlens.db")
        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()
        # Chercher id_espece correspondant au nom
        cursor.execute("SELECT id_espece FROM especes WHERE nom = ?", (nom_csv,))
        row = cursor.fetchone()

        if row:
            id_espece = row[0]

            cursor.execute("""
                INSERT INTO predictions (id_espece, nom_espece, nom_scientifique, description, date_prediction, image_path, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                id_espece,
                nom_csv,
                info["nom_scientifique"],
                info["description"],
                datetime.now().isoformat(),
                image_path,
                float(predictions.boxes.conf[0])
            ))
            conn.commit()

            # Ajouter ceci pour que le backend retourne le bon résultat !
            confidence = float(predictions.boxes.conf[0])

            return {
                "nom_espece": nom_csv,
                "description": info["description"],
                "nom_scientifique": info["nom_scientifique"],
                "habitat": info["habitat"],
                "taille": info["taille"],
                "famille": info["famille"],
                "confidence": round(confidence * 100, 2)

            }

        else:
            print(f"Erreur : l'espèce '{nom_csv}' n'existe pas dans la table especes.")
        # Si on arrive ici, c’est qu’aucun return n’a été déclenché
        return {
            "nom_espece": "Erreur",
            "description": "Aucune prédiction n’a été possible."
        }
