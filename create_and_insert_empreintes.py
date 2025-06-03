import sqlite3
import pandas as pd
from datetime import datetime
import os

# Connexion à la base de données
conn = sqlite3.connect("database/wildlens.db")
cursor = conn.cursor()

# Activer les clés étrangères
cursor.execute("PRAGMA foreign_keys = ON;")

# Recréer la table 'empreintes'
cursor.execute("DROP TABLE IF EXISTS empreintes")
cursor.execute("""
CREATE TABLE empreintes (
    id_empreinte INTEGER PRIMARY KEY AUTOINCREMENT,
    espece_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    localisation TEXT,
    photo_filename TEXT,
    FOREIGN KEY (espece_id) REFERENCES especes(id_espece)
)
""")

# Charger le CSV préparé
df = pd.read_csv("empreintes_preparees.csv")

# Connexion pour chercher les ID d'espèces
def get_espece_id(nom_espece):
    cursor.execute("SELECT id_espece FROM especes WHERE nom = ?", (nom_espece,))
    result = cursor.fetchone()
    return result[0] if result else None

# Insérer les empreintes
count = 0
for _, row in df.iterrows():
    espece_id = get_espece_id(row["Espèce"])
    if espece_id is None:
        print(f" Espèce inconnue ignorée : {row['Espèce']}")
        continue
    cursor.execute("""
        INSERT INTO empreintes (espece_id, date, localisation, photo_filename)
        VALUES (?, ?, ?, ?)
    """, (
        espece_id,
        datetime.today().strftime('%Y-%m-%d'),
        "",  # Localisation vide
        os.path.basename(row["Image_nettoyee"])
    ))
    count += 1

conn.commit()
conn.close()
print(f" {count} empreintes insérées proprement.")
