# WildLens Backend

API de détection d'empreintes animales avec YOLOv8 + FastAPI

## Fonctionnalité principale

Cette API permet :

de recevoir une image d'empreinte animale (upload)

de détecter l'espèce animale correspondante via un modèle YOLOv8

de renvoyer les informations complètes de l'espèce (nom, description, taille, habitat...)

de sauvegarder la prédiction dans une base de données SQLite

## Stack technique

Python 3.10+

FastAPI

Ultralytics YOLOv8

SQLite (base locale)

## Arborescence principale

├── app/
│   ├── main.py               # Point d'entrée FastAPI
│   ├── model_wrapper.py      # Chargement et prédiction YOLOv8
│   ├── best.pt               # Modèle entraîné YOLOv8
│   ├── infos_especes.csv     # Infos complètes sur chaque espèce
│   ├── classes.txt           # Liste des espèces (classes YOLO)
│
├── temp_images/          # Dossier pour sauvegarde temporaire des images

## Endpoints FastAPI

Méthode : POST
URL : /predict
Description : Upload d'une image. Le serveur l’analyse avec YOLOv8 et renvoie l'espèce détectée avec ses informations (nom, description, habitat, etc.).

## Lancer le backend

cd backend/app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Prérequis

pip install -r requirements.txt

## Modèle YOLOv8

Fichier best.pt à placer dans app/

Entraîné avec Ultralytics YOLOv8
