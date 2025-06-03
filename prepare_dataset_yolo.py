import os
import random
import shutil
from pathlib import Path

# PARAMÈTRES 
original_images = 'C:/cours_b3/mspr-ia/WildLens_MSPR/Mammiferes'
original_labels = 'C:/cours_b3/mspr-ia/WildLens_MSPR/annotation/yolo_labels'
aug_images = 'C:/cours_b3/mspr-ia/WildLens_MSPR/augmented/images'
aug_labels = 'C:/cours_b3/mspr-ia/WildLens_MSPR/augmented/labels'
output_dataset = 'C:/cours_b3/mspr-ia/WildLens_MSPR/dataset'
classes_txt = 'C:/cours_b3/mspr-ia/WildLens_MSPR/classes.txt'
split_ratio = 0.8  # 80% train, 20% val

# CRÉATION DES DOSSIERS 
for split in ['train', 'val']:
    os.makedirs(os.path.join(output_dataset, 'images', split), exist_ok=True)
    os.makedirs(os.path.join(output_dataset, 'labels', split), exist_ok=True)

# FONCTION POUR CHERCHER UNE IMAGE DANS TOUS LES SOUS-DOSSIERS 
def find_image(name, base_folder):
    for root, _, files in os.walk(base_folder):
        for file in files:
            if Path(file).stem == name:
                return os.path.join(root, file)
    return None

# RÉUNIR TOUS LES .txt ANNOTÉS (originaux + augmentés) 
label_files = []

for folder in [original_labels, aug_labels]:
    for f in os.listdir(folder):
        if f.endswith('.txt'):
            label_files.append((os.path.join(folder, f), Path(f).stem))

# SHUFFLE & SPLIT 
random.shuffle(label_files)
split_index = int(len(label_files) * split_ratio)
train_files = label_files[:split_index]
val_files = label_files[split_index:]

# COPIE FONCTION
def copy_pairs(pairs, subset):
    for label_path, base_name in pairs:
        # copier le .txt
        dst_label = os.path.join(output_dataset, 'labels', subset, base_name + '.txt')
        shutil.copy(label_path, dst_label)

        # chercher l'image correspondante (originale ou augmentée)
        img = find_image(base_name, original_images) or find_image(base_name, aug_images)
        if img:
            dst_img = os.path.join(output_dataset, 'images', subset, base_name + Path(img).suffix)
            shutil.copy(img, dst_img)
        else:
            print(f" Image non trouvée pour : {base_name}")

copy_pairs(train_files, 'train')
copy_pairs(val_files, 'val')

# GÉNÉRER LE FICHIER data.yaml
with open(classes_txt, 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f.readlines()]

yaml_path = os.path.join(output_dataset, 'data.yaml')
with open(yaml_path, 'w', encoding='utf-8') as f:
    yaml_path_str = output_dataset.replace('\\', '/')
    f.write(f"path: {yaml_path_str}\n")
    f.write("train: images/train\n")
    f.write("val: images/val\n")
    f.write(f"nc: {len(class_names)}\n")
    f.write("names: " + str(class_names) + "\n")

print(f"\n Dataset YOLO prêt dans : {output_dataset}")
print(f" Fichier data.yaml généré.")
