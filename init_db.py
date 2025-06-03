import sqlite3
import csv
import os
from datetime import datetime

# Chemins
db_path = "database/wildlens.db"
csv_path = "backend/app/infos_especes.csv"
images_base_path = "images_nettoyees"

# Créer le dossier s'il n'existe pas
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connexion à la base
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Supprimer les anciennes tables proprement
cursor.execute("PRAGMA foreign_keys = OFF;")
cursor.execute("DROP TABLE IF EXISTS empreintes")
cursor.execute("DROP TABLE IF EXISTS especes")
cursor.execute("PRAGMA foreign_keys = ON;")

#  Créer les nouvelles tables
cursor.execute('''
CREATE TABLE especes (
    classe INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    nom_scientifique TEXT,
    description TEXT,
    famille TEXT,
    taille TEXT,
    habitat TEXT
)
''')

cursor.execute('''
CREATE TABLE empreintes (
    id_empreinte INTEGER PRIMARY KEY AUTOINCREMENT,
    espece_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    localisation TEXT,
    photo_filename TEXT,
    FOREIGN KEY (espece_id) REFERENCES especes(classe)
)
''')

#  Charger les espèces depuis le CSV
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO especes (classe, nom, nom_scientifique, description, famille, taille, habitat)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(row['classe']),
            row['nom'],
            row['nom_scientifique'],
            row['description'],
            row['famille'],
            row['taille'],
            row['habitat']
        ))

#  Insérer les empreintes à partir des dossiers d’images
if os.path.isdir(images_base_path):
    for espece_nom in os.listdir(images_base_path):
        espece_path = os.path.join(images_base_path, espece_nom)
        if not os.path.isdir(espece_path):
            continue

        cursor.execute("SELECT classe FROM especes WHERE nom = ?", (espece_nom,))
        result = cursor.fetchone()

        if result is None:
            print(f" Espèce '{espece_nom}' non trouvée dans la table especes.")
            continue

        espece_id = result[0]

        for filename in os.listdir(espece_path):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                photo_path = os.path.join(espece_path, filename)
                cursor.execute("""
                    INSERT INTO empreintes (espece_id, date, localisation, photo_filename)
                    VALUES (?, ?, ?, ?)
                """, (
                    espece_id,
                    datetime.now().isoformat(),
                    None,
                    photo_path
                ))

print(" Base de données 'wildlens.db' initialisée avec succès.")
conn.commit()
conn.close()
