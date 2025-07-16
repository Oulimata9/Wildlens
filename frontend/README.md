# WildLens Frontend

Interface web minimaliste pour prendre une photo / uploader une empreinte et afficher le résultat de détection

## Technologies utilisées

HTML / CSS

JavaScript (Fetch API)

## Arborescence

frontend/
├── index.html       # Page de capture ou upload
├── result.html      # Affichage des infos de l'espèce détectée
├── style.css        # Style visuel responsive
├── script.js        # Appels API + redirection

## Fonctionnement

L'utilisateur prend une photo (via la caméra) ou choisit un fichier

Le fichier est envoyé via POST à <http://localhost:8000/predict/>

La réponse (espèce identifiée + détails) est affichée sur result.html

## Prérequis

Pas d'installation nécessaire. Il suffit d'ouvrir index.html dans un navigateur moderne.

## Lancement

cd frontend

Ouvrir index.html avec un navigateur

## Exemple d'utilisation

Lancer le backend sur localhost:8000

Ouvrir index.html

Envoyer une photo d'empreinte

Voir le résultat s'afficher : nom, description, habitat, etc.

## Backend attendu

URL cible pour les requêtes : <http://localhost:8000/predict/>
