import os


path = "C:\cours_b3\mspr-ia\WildLens_MSPR\Mammiferes"

# Espèce à conserver (tu peux changer 'cat' par 'chien', 'renard', etc.)
espece_cible = "cat"

# Vérification du dossier
if not os.path.exists(path):
    print(f" Le dossier {path} n'existe pas.")
else:
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)

        if os.path.isfile(full_path):
            # Conserve uniquement les fichiers contenant l'espèce cible
            if espece_cible not in filename.lower():
                os.remove(full_path)
                print(f"Supprimé : {filename}")
            else:
                print(f"Conservé : {filename}")
