import pandas as pd
import os

output_base = 'C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\images_nettoyees'
# On repart du CSV des empreintes
df = pd.read_csv('C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\empreintes.csv')

# Créer un dictionnaire d'encodage
classes = sorted(df['Espèce'].unique())
label_map = {esp: idx for idx, esp in enumerate(classes)}

# Ajouter une colonne "Classe"
df['Classe'] = df['Espèce'].map(label_map)

# Mettre à jour les chemins vers les images nettoyées
df['Image_nettoyee'] = df.apply(
    lambda row: os.path.join(output_base, row['Espèce'], row['ID'] + '.jpg'),
    axis=1
)

# Sauvegarder le nouveau CSV
df.to_csv('C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\empreintes_preparees.csv', index=False)

print("Encodage terminé. Mapping :", label_map)
