import sqlite3
import pandas as pd
import os

# === Paramètres ===
CSV_PATH = "empreintes_preparees.csv"
DB_PATH = "database/wildlens.db"

# === Lecture du CSV ===
df = pd.read_csv(CSV_PATH)

# === Connexion à la base de données ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === Nettoyage : suppression des lignes avec espèce manquante ou fichier introuvable ===
df = df.dropna(subset=['Espèce', 'Image_nettoyee'])
df = df[df['Image_nettoyee'].apply(lambda x: os.path.exists(x))]

# === Dictionnaire espèce -> ID depuis la table especes ===
cursor.execute("SELECT id_espece, nom FROM especes")
map_especes = {nom: id_ for id_, nom in cursor.fetchall()}



# === Insertion dans la table empreintes ===
inserts = []
for _, row in df.iterrows():
    espece = row['Espèce']
    if espece not in map_especes:
        print(f"Espèce inconnue ignorée : {espece}")
        continue

    id_espece = map_especes[espece]
    photo_filename = os.path.basename(row['Image_nettoyee'])

    inserts.append((id_espece, "2025-05-26", "", photo_filename))

cursor.executemany('''
INSERT INTO empreintes (espece_id, date, localisation, photo_filename)
VALUES (?, ?, ?, ?)
''', inserts)

conn.commit()
conn.close()
print(f" {len(inserts)} empreintes insérées dans la base de données.")
