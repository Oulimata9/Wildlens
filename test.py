import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("database/wildlens.db")
cursor = conn.cursor()

# Affichage du contenu de la table especes
print(" Table 'especes' :")
cursor.execute("SELECT * FROM especes")
for row in cursor.fetchall():
    print(row)

print("\n Table 'empreintes' :")
cursor.execute("SELECT id_empreinte, espece_id, date, photo_filename FROM empreintes LIMIT 10")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Compter le nombre total d’empreintes
cursor.execute("SELECT COUNT(*) FROM empreintes")
total = cursor.fetchone()[0]
print(f"\n Nombre total d’empreintes : {total}")

conn.close()
