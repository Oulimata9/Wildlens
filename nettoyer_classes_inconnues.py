import os
import xml.etree.ElementTree as ET

# === Dossiers ===
base_annotation_folder = 'C:\\cours_b3\\mspr-ia\\animalprint\\projet MSPR\\annotation'
classes_file = 'classes.txt'

# Chargement des classes autorisées (en minuscules)
with open(classes_file, 'r', encoding='utf-8') as f:
    classes_autorisees = [line.strip().lower() for line in f.readlines()]

fichiers_modifiés = 0
annotations_supprimées = 0

# === Parcours des sous-dossiers
for sous_dossier in os.listdir(base_annotation_folder):
    chemin_sous_dossier = os.path.join(base_annotation_folder, sous_dossier)
    if not os.path.isdir(chemin_sous_dossier):
        continue

    for fichier in os.listdir(chemin_sous_dossier):
        if not fichier.endswith('.xml'):
            continue

        chemin_xml = os.path.join(chemin_sous_dossier, fichier)
        try:
            tree = ET.parse(chemin_xml)
        except ET.ParseError:
            print(f" Fichier corrompu ignoré : {fichier}")
            continue

        root = tree.getroot()
        objets = root.findall('object')
        modifié = False

        for obj in objets:
            nom_classe = obj.find('name').text.strip().lower()
            if nom_classe not in classes_autorisees:
                root.remove(obj)
                annotations_supprimées += 1
                modifié = True
                print(f" Annotation '{nom_classe}' supprimée dans {fichier}")

        if modifié:
            tree.write(chemin_xml, encoding='utf-8')
            fichiers_modifiés += 1

print(f"\n Nettoyage terminé : {annotations_supprimées} annotation(s) supprimée(s) dans {fichiers_modifiés} fichier(s).")
