# WildLens – Projet MSPR TPRE521

WildLens est une application de détection d’empreintes animales à l’aide de la vision par ordinateur. Le projet met en œuvre un pipeline complet de traitement de données (ETL), basé sur l'annotation d’images, l’entraînement d’un modèle de détection YOLOv8, et l'enregistrement des résultats dans une base SQLite.

---

## Objectif pédagogique

Ce projet a pour but de mettre en œuvre un pipeline ETL dans un cas d’usage appliqué à la détection d’empreintes de mammifères :

- E (Extract) : récupération des images et métadonnées
- T (Transform) : normalisation des données, conversion de formats, encodage
- L (Load) : entraînement d’un modèle YOLOv8 ou insertion en base SQLite

Projet réalisé dans le cadre du MSPR TPRE521 – IA & Données.

---

## Étapes du projet

### 1. Extraction

- Collecte des images dans le dossier `Mammiferes/`
- Extraction des annotations XML via LabelImg
- Génération de `empreintes.csv` et `empreintes_preparees.csv`

### 2. Transformation

- Nettoyage et redimensionnement des images (`prepare_images.py`)
- Conversion des annotations au format YOLOv8 (`convert_voc_to_yolo.py`)
- Data augmentation ciblée (`augmentation_ciblee.py`)
- Encodage des classes (`encode_and_split.py`)
- Séparation du dataset en `train/val/test`

### 3. Chargement

- Option 1 : Entraînement du modèle YOLOv8n (léger, optimisé pour mobile)
- Option 2 : Insertion des empreintes détectées dans une base SQLite (`database/wildlens.db`)

---

## Modèle d’intelligence artificielle

- Modèle : YOLOv8n (nano)
- Framework : `ultralytics`
- Entraînement effectué sur Google Colab (GPU Tesla T4)
- Fichier de poids final : `yolov8n.pt`
- Métriques obtenues :
  - mAP@0.5 : 66.3%
  - mAP@0.5:0.95 : 47.4%

---

## Arborescence du projet (extrait)

WildLens_MSPR/
├── Mammiferes/                 # Dossier d'images d'empreintes  
├── annotation/                # Annotations XML LabelImg  
├── database/                  # Base SQLite + scripts BDD  
├── dataset/                   # Données YOLO transformées  
├── images_nettoyees/          # Images nettoyées  
├── visualisation/             # Résultats, courbes et outputs  
├── yolov8n.pt                 # Modèle YOLOv8 entraîné  
├── init_db.py                 # Création des tables BDD  
├── test                       # images pour tester l'entrainement yolo
├── backend/
│ ├── app/
│ │ ├── main.py                 # Backend FastAPI
│ │ ├── predict_image.py        # Détection et enregistrement
│ │ └── infos_especes.csv       # Données descriptives
├── database/
│ └── wildlens.db                # Base SQLite
├── frontend/
│ ├── index.html                 # Accueil de l'application
│ ├── logo.png                  # logo de l'application
├── README.md                    # Ce fichier  

---

## Scripts Python du pipeline

| Nom du script                    | Rôle |
|----------------------------------|------|
| `prepare_images.py`              | Redimensionne les images à 224x224, convertit en JPEG RGB, sauvegarde dans `images_nettoyees/`. |
| `extract_classes_from_xml.py`    | Extrait les classes présentes dans les annotations XML pour vérifier les espèces. |
| `replace_classes_in_xml.py`      | Traduit les noms de classes des XML du français vers l’anglais pour correspondre à YOLOv8. |
| `nettoyer_classes_inconnues.py`  | Supprime des annotations XML les objets dont la classe n’est pas listée dans `classes.txt`. |
| `generer_empreintes_csv.py`      | Génère un fichier `empreintes.csv` à partir des images dans `Mammiferes/`. |
| `convert_voc_to_yolo.py`         | Convertit les annotations Pascal VOC (XML) en format YOLOv8 (TXT normalisé). |
| `compter_classes_yolo.py`        | Analyse les fichiers .txt YOLO pour compter les annotations par classe et détecter les classes rares. |
| `augmentation_ciblee.py`         | Applique une augmentation (flip, rotation, flou, contraste) sur certaines classes sous-représentées. |
| `prepare_dataset_yolo.py`        | Prépare le dataset final pour YOLOv8 avec séparation train/val et génération du fichier `data.yaml`. |
| `split_train_test.py`            | Sépare les empreintes en deux ensembles (`train.csv` / `test.csv`) avec stratification des classes. |
| `encode_and_split.py`            | Encode les noms d'espèces en identifiants numériques et génère le fichier `empreintes_preparees.csv`. |
| `init_db.py`                     | Crée les tables `especes` et `empreintes` dans `wildlens.db` et les remplit avec les données du projet. |
| `generate_csv_from_db.py`        | Exporte les données de la table `especes` au format `infos_especes.csv` pour l’affichage dans l’application. |

## Dépendances principales

pip install ultralytics opencv-python pillow scikit-learn matplotlib

Autres outils :

- Python ≥ 3.10
- LabelImg pour l’annotation manuelle
- SQLite pour le stockage local

---

## Exécution du pipeline (exemples)

### Entraînement YOLOv8

yolo task=detect mode=train model=yolov8n.pt data=dataset.yaml epochs=50 imgsz=640

### Insertion en base de données

python init_db.py

---

### 1. Cloner le projet

git clone <https://github.com/Oulimata9/Wildlens.git>
cd Wildlens

### 2. Créer un environnement virtuel

python -m venv venv

### 3. Activer l’environnement

Sous Windows :

venv\Scripts\activate

Sous macOS/Linux :

source venv/bin/activate

### 4. Installer les dépendances

pip install -r requirements.txt

## Installation & Environnement

## Lancer l'application

### 1. Démarrer l'API FastAPI

uvicorn app.main:app --reload

### 2. Ouvrir le frontend

Ouvrir `frontend/index.html` dans le navigateur.

## Auteur

Oulimata DIEDHIOU  
Étudiante B3 – Intelligence Artificielle  
Projet réalisé dans le cadre du MSPR TPRE521 (mai 2025)

---

## Licence

Projet académique – Usage pédagogique uniquement.
