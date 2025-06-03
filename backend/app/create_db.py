import sqlite3

# Connexion à la base (elle sera créée si elle n'existe pas)
conn = sqlite3.connect("predictions.db")
cursor = conn.cursor()

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_espece TEXT,
    nom_scientifique TEXT,
    description TEXT,
    date_prediction TEXT,
    image_path TEXT,
    latitude REAL,
    longitude REAL
)
""")

conn.commit()
conn.close()

print("Base de données initialisée.")
