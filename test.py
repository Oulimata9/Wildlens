from ultralytics import YOLO

# Charger le modèle
model = YOLO("backend/app/best.pt")  # attention : pas "app/best.pt" si on est déjà dans app/

# Image test : choisis une image qui marchait bien avant (genre un chat ou un ours)
image_path = "C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\test\\castor.jpg"  # copie cette image dans le même dossier

# Lancer la prédiction
results = model.predict(image_path, save=True, conf=0.25)

# Afficher le résultat
for r in results:
    print("Classes détectées :", r.names)
    print("Boxes :", r.boxes)
