from sklearn.model_selection import train_test_split
import pandas as pd

# Chargement du CSV préparé
df = pd.read_csv('C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\empreintes_preparees.csv')

# Split 80/20
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['Classe'], random_state=42)

# Sauvegarde
train_df.to_csv('C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\train.csv', index=False)
test_df.to_csv('C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\test.csv', index=False)

print(f"{len(train_df)} images pour l'entraînement, {len(test_df)} pour le test.")
