import sqlite3
import pandas as pd
from datetime import datetime
import os

# Connexion à la base
conn = sqlite3.connect("database/wildlens.db")
cursor = conn.cursor()

# Activer les clés étrangères
cursor.execute("PRAGMA foreign_keys = ON;")

# Supprimer uniquement la table 'empreintes' (pas 'especes')
cursor.execute("DROP TABLE IF EXISTS empreintes")

# Recréer la table 'empreintes'
cursor.execute("""
CREATE TABLE empreintes (
    id_empreinte INTEGER PRIMARY KEY AUTOINCREMENT,
    id_espece INTEGER NOT NULL,
    date TEXT NOT NULL,
    photo_filename TEXT,
    FOREIGN KEY (id_espece) REFERENCES especes(id_espece)
)
""")

# Charger les empreintes depuis le CSV
df_empreintes = pd.read_csv("empreintes.csv")

# Fonction pour retrouver l'ID de l'espèce à partir de son nom
def get_espece_id(nom_espece):
    cursor.execute("SELECT id_espece FROM especes WHERE nom = ?", (nom_espece,))
    result = cursor.fetchone()
    return result[0] if result else None

# Insérer les empreintes
count = 0
for _, row in df_empreintes.iterrows():
    espece_id = get_espece_id(row["Espèce"])
    if espece_id is None:
        print(f"Espèce inconnue ignorée : {row['Espèce']}")
        continue

    cursor.execute("""
        INSERT INTO empreintes (id_espece, date, photo_filename)
        VALUES (?, ?, ?)
    """, (
        espece_id,
        datetime.today().strftime('%Y-%m-%d'),
        os.path.basename(row["Chemin d'accès"])
    ))
    count += 1

print(f"\n{count} empreintes insérées avec succès.")

# Création ou mise à jour de la table predictions
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id_prediction INTEGER PRIMARY KEY AUTOINCREMENT,
    id_espece INTEGER NOT NULL,
    date TEXT NOT NULL,
    photo_filename TEXT,
    confidence REAL,
    localisation TEXT,
    FOREIGN KEY (id_espece) REFERENCES especes(id_espece)
)
""")
print("Table predictions créée avec succès.")

# Ajouter la colonne 'nom_espece' si elle n'existe pas
try:
    cursor.execute("ALTER TABLE predictions ADD COLUMN nom_espece TEXT")
    print("Colonne 'nom_espece' ajoutée à la table predictions.")
except sqlite3.OperationalError:
    print("La colonne 'nom_espece' existe déjà dans la table predictions.")

# Vérification finale
cursor.execute("SELECT COUNT(*) FROM empreintes")
nb_total = cursor.fetchone()[0]
print(f"Total actuel dans la table empreintes : {nb_total}")

conn.commit()
conn.close()
