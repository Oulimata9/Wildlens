import os
import xml.etree.ElementTree as ET

# === Chemin vers le dossier contenant les sous-dossiers d'annotations
base_annotation_folder = 'C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\annotation'

# === Dictionnaire de traduction : français ➜ anglais
fr_to_en = {
    'chien': 'dog',
    'chat': 'cat',
    'castor': 'beaver',
    'ours': 'bear',
    'renard': 'fox',
    'raton laveur': 'raccoon',
    'rat': 'rat',
    'puma': 'puma',
    'coyote': 'coyote',
    'écureuil': 'squirrel',
    'lapin': 'rabbit',
    'loup': 'wolf',
}

traductions = 0
fichiers_modifiés = 0

# === Parcours de tous les fichiers XML dans les sous-dossiers
for sous_dossier in os.listdir(base_annotation_folder):
    chemin_sous_dossier = os.path.join(base_annotation_folder, sous_dossier)
    if not os.path.isdir(chemin_sous_dossier):
        continue

    for fichier in os.listdir(chemin_sous_dossier):
        if not fichier.endswith('.xml'):
            continue

        chemin_fichier = os.path.join(chemin_sous_dossier, fichier)

        try:
            tree = ET.parse(chemin_fichier)
        except ET.ParseError:
            print(f" Fichier corrompu : {fichier}")
            continue

        root = tree.getroot()
        modifié = False

        for obj in root.findall('object'):
            tag = obj.find('name')
            if tag is not None:
                nom = tag.text.strip().lower()
                if nom in fr_to_en:
                    nouveau_nom = fr_to_en[nom]
                    print(f" {nom} ➜ {nouveau_nom} dans {fichier}")
                    tag.text = nouveau_nom
                    modifié = True
                    traductions += 1

        if modifié:
            tree.write(chemin_fichier, encoding='utf-8')
            fichiers_modifiés += 1

print(f"\n {traductions} annotation(s) traduite(s) dans {fichiers_modifiés} fichier(s) XML.")
