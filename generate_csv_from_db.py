import sqlite3
import pandas as pd

# Connexion à la base existante
conn = sqlite3.connect("database/wildlens.db")
cursor = conn.cursor()

# Lire les données des espèces
cursor.execute("SELECT id_espece, nom, description FROM especes")
rows = cursor.fetchall()

# Créer un DataFrame
df = pd.DataFrame(rows, columns=["classe", "nom", "description"])

# Sauvegarder en CSV
df.to_csv("backend/app/infos_especes.csv", index=False, encoding='utf-8')
print("ichier infos_especes.csv généré depuis la base de données.")
