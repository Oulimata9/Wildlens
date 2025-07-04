import sqlite3
import pandas as pd
from datetime import datetime
import os
from ultralytics import YOLO

# === PARAMÈTRES ===
CHEMIN_CLASSES = r"C:\cours_b3\mspr-ia\WildLens_MSPR\backend\app\classes.txt"
CHEMIN_IMAGE = r"C:\cours_b3\mspr-ia\WildLens_MSPR\test\ours1.jpeg"
CHEMIN_MODELE = r"C:\cours_b3\mspr-ia\runs\detect\wildlens_v2\weights\best.pt"
CHEMIN_BDD = r"C:\cours_b3\mspr-ia\WildLens_MSPR\database\wildlens.db"
CHEMIN_CSV_INFOS = r"C:\cours_b3\mspr-ia\WildLens_MSPR\backend\app\infos_especes.csv"

# === Chargement YOLO et données ===
model = YOLO(CHEMIN_MODELE)

# Charger les noms des classes (YOLO)
with open(CHEMIN_CLASSES, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

# Charger le CSV des infos espèces
df_infos = pd.read_csv(CHEMIN_CSV_INFOS)
df_infos["nom"] = df_infos["nom"].str.strip().str.lower()

# Dictionnaire YOLO ➝ noms CSV
yolo_to_csv = {
    "beaver": "castor",
    "cat": "chat",
    "dog": "chien",
    "coyote": "coyote",
    "fox": "renard",
    "bear": "ours",
    "lynx": "lynx",
    "wolf": "loup",
    "rabbit": "lapin",
    "puma": "puma",
    "squirrel": "ecureuil",
    "rat": "rat",
    "raccoon": "raton laveur"
}

# === Fonction principale ===
def predict_and_store(image_path):
    results = model.predict(image_path, conf=0.4)
    boxes = results[0].boxes

    if boxes is None or len(boxes.cls) == 0:
        print("Aucune espèce détectée.")
        return

    predicted_class_id = int(boxes.cls[0])
    yolo_name = class_names[predicted_class_id].lower()

    nom_espece = yolo_to_csv.get(yolo_name)
    if not nom_espece:
        print("Classe non reconnue.")
        return

    info = df_infos[df_infos["nom"] == nom_espece]
    if info.empty:
        print(f"Espèce '{nom_espece}' non trouvée dans le CSV.")
        return

    espece = info.iloc[0]
    print(f"Espèce détectée : {nom_espece} ({espece['nom_scientifique']})")

    conn = sqlite3.connect(CHEMIN_BDD)
    cursor = conn.cursor()

    # Vérifier si la table predictions existe, sinon la créer
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id_prediction INTEGER PRIMARY KEY AUTOINCREMENT,
            id_espece INTEGER NOT NULL,
            nom_espece TEXT,
            nom_scientifique TEXT,
            description TEXT,
            date_prediction TEXT,
            image_path TEXT,
            confidence REAL,
            FOREIGN KEY (id_espece) REFERENCES especes(id_espece)
        )
    """)

    # Récupérer id_espece dans la base
    cursor.execute("SELECT id_espece FROM especes WHERE LOWER(TRIM(nom)) = ?", (nom_espece.lower().strip(),))
    row = cursor.fetchone()
    if row:
        id_espece = row[0]
    else:
        print(f"Espèce '{nom_espece}' introuvable dans la base.")
        conn.close()
        return

    # Insertion dans la table predictions
    cursor.execute("""
        INSERT INTO predictions (
            id_espece,
            nom_espece,
            nom_scientifique,
            description,
            date_prediction,
            image_path,
            confidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        id_espece,
        espece["nom"],
        espece["nom_scientifique"],
        espece["description"],
        datetime.now().isoformat(),
        os.path.basename(image_path),
        float(boxes.conf[0])
    ))

    conn.commit()
    conn.close()
    print("Prédiction enregistrée avec succès.")

# === Lancer si fichier exécuté directement ===
if __name__ == "__main__":
    predict_and_store(CHEMIN_IMAGE)

