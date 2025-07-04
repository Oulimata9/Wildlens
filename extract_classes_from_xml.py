import os
import xml.etree.ElementTree as ET

# Dossier principal contenant tous les sous-dossiers d'annotations ===
base_annotation_folder = 'C:/cours_b3/mspr-ia/WildLens_MSPR/annotation'

classes_set = set()

# Parcours de tous les dossiers
for subdir in os.listdir(base_annotation_folder):
    full_subdir_path = os.path.join(base_annotation_folder, subdir)
    if not os.path.isdir(full_subdir_path):
        continue

    for file in os.listdir(full_subdir_path):
        if not file.endswith('.xml'):
            continue

        xml_path = os.path.join(full_subdir_path, file)
        try:
            tree = ET.parse(xml_path)
        except ET.ParseError:
            continue  

        root = tree.getroot()

        for obj in root.findall('object'):
            class_name = obj.find('name').text.strip().lower()
            classes_set.add(class_name)

# Affiche la liste des classes uniques
print(" Classes détectées dans les fichiers .xml :")
for cls in sorted(classes_set):
    print(f" - {cls}")
