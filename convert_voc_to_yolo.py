import os
import xml.etree.ElementTree as ET

base_annotation_folder = 'C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\annotation'
output_folder = os.path.join(base_annotation_folder, 'yolo_labels')
classes_file = 'classes.txt'

# Création du dossier de sortie
os.makedirs(output_folder, exist_ok=True)

# Chargement des classes
with open(classes_file, 'r', encoding='utf-8') as f:
    class_list = [line.strip().lower() for line in f.readlines()]

def convert_bbox(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[1]) / 2.0 * dw
    y_center = (box[2] + box[3]) / 2.0 * dh
    width = (box[1] - box[0]) * dw
    height = (box[3] - box[2]) * dh
    return (x_center, y_center, width, height)

# Parcours des XML
for subdir in os.listdir(base_annotation_folder):
    sub_path = os.path.join(base_annotation_folder, subdir)
    if not os.path.isdir(sub_path) or subdir == 'yolo_labels':
        continue

    for xml_file in os.listdir(sub_path):
        if not xml_file.endswith('.xml'):
            continue

        xml_path = os.path.join(sub_path, xml_file)

        try:
            tree = ET.parse(xml_path)
        except ET.ParseError:
            print(f" Fichier XML invalide : {xml_file}")
            continue

        root = tree.getroot()
        size_tag = root.find('size')
        if size_tag is None:
            continue

        w = int(size_tag.find('width').text)
        h = int(size_tag.find('height').text)

        yolo_lines = []

        for obj in root.findall('object'):
            class_name = obj.find('name').text.strip().lower()
            if class_name not in class_list:
                print(f" Classe inconnue '{class_name}' ignorée dans {xml_file}")
                continue

            class_id = class_list.index(class_name)
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            xmax = int(bndbox.find('xmax').text)
            ymin = int(bndbox.find('ymin').text)
            ymax = int(bndbox.find('ymax').text)

            bbox = convert_bbox((w, h), (xmin, xmax, ymin, ymax))
            yolo_lines.append(f"{class_id} " + " ".join([str(round(val, 6)) for val in bbox]))

        if yolo_lines:
            output_path = os.path.join(output_folder, os.path.splitext(xml_file)[0] + '.txt')
            with open(output_path, 'w') as f:
                f.write('\n'.join(yolo_lines))
            print(f" {xml_file} converti")
        else:
            print(f" {xml_file} ignoré (aucune annotation YOLO)")
