import os
import csv

# Chemin vers le dossier contenant les sous-dossiers par espèce
base_path = 'C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\Mammiferes'
output_csv = 'empreintes.csv'

# Initialisation de l'ID incrémental
current_id = 0

# Création du fichier CSV
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id_empreinte', 'Espèce', 'Chemin d\'accès'])

    for espece in os.listdir(base_path):
        species_dir = os.path.join(base_path, espece)
        if os.path.isdir(species_dir):
            for img_file in os.listdir(species_dir):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    full_path = os.path.abspath(os.path.join(species_dir, img_file))
                    writer.writerow([current_id, espece, full_path])
                    current_id += 1

print(f'Fichier {output_csv} généré avec succès ({current_id} lignes).')
