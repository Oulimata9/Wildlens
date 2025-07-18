from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.model_wrapper import predict_image
import shutil
import uuid
import os
from app.model_wrapper import predict_image

app = FastAPI()

#  Autoriser les requêtes depuis ton front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifie le vrai domaine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer automatiquement le dossier s’il n’existe pas
os.makedirs("temp_images", exist_ok=True)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Sauvegarde temporaire
    temp_filename = f"temp_images/{uuid.uuid4()}.jpg"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Prédiction via YOLO
    result = predict_image(temp_filename)

    # Suppression de l’image après traitement
    try:
        import os
        os.remove(temp_filename)
    except Exception as e:
        print("Erreur lors de la suppression de l’image :", e)

    return result