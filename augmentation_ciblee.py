import os
import cv2
import albumentations as A
from tqdm import tqdm

# PARAMÈTRES 
classes_to_augment = ['beaver', 'rabbit', 'coyote', 'fox', 'lynx']
input_image_root = 'C:/cours_b3/mspr-ia/WildLens_MSPR/Mammiferes'
input_label_folder = 'C:/cours_b3/mspr-ia/WildLens_MSPR/annotation/yolo_labels'
output_image_folder = 'C:/cours_b3/mspr-ia/WildLens_MSPR/augmented/images'
output_label_folder = 'C:/cours_b3/mspr-ia/WildLens_MSPR/augmented/labels'
classes_txt_path = 'C:/cours_b3/mspr-ia/WildLens_MSPR/classes.txt'

# CRÉER DOSSIERS SORTIE
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# CHARGER LES CLASSES 
with open(classes_txt_path, 'r', encoding='utf-8') as f:
    class_list = [line.strip() for line in f.readlines()]
    target_class_ids = [class_list.index(cls) for cls in classes_to_augment]

# AUGMENTATIONS 
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.4),
    A.Rotate(limit=15, p=0.5),
    A.MotionBlur(p=0.2),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# CHERCHER UNE IMAGE DANS MAMMIFERES 
def find_image_path(image_name):
    for root, _, files in os.walk(input_image_root):
        for file in files:
            if file.lower() == image_name.lower():
                return os.path.join(root, file)
    return None

# TRAITEMENT
augmented_count = 0
for file in tqdm(os.listdir(input_label_folder)):
    if not file.endswith('.txt'):
        continue

    base_name = os.path.splitext(file)[0]
    label_path = os.path.join(input_label_folder, file)

    image_path = find_image_path(base_name + '.jpg') or find_image_path(base_name + '.png')
    if image_path is None:
        continue

    with open(label_path, 'r') as f:
        lines = f.readlines()

    bboxes = []
    class_labels = []
    for line in lines:
        parts = line.strip().split()
        cls_id = int(parts[0])
        if cls_id in target_class_ids:
            bbox = list(map(float, parts[1:]))
            bboxes.append(bbox)
            class_labels.append(cls_id)

    if not bboxes:
        continue

    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    try:
        for i in range(3):  
            transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            aug_image = transformed['image']
            aug_bboxes = transformed['bboxes']
            aug_labels = transformed['class_labels']

            # Enregistrement
            aug_filename = f"{base_name}_aug{i+1}"
            aug_img_path = os.path.join(output_image_folder, aug_filename + '.jpg')
            aug_label_path = os.path.join(output_label_folder, aug_filename + '.txt')

            cv2.imwrite(aug_img_path, aug_image)
            with open(aug_label_path, 'w') as out_f:
                for cls_id, bbox in zip(aug_labels, aug_bboxes):
                    out_f.write(f"{cls_id} {' '.join([str(round(x, 6)) for x in bbox])}\n")

            augmented_count += 1

    except Exception as e:
        print(f" Erreur sur {file} : {e}")

print(f"\n Data augmentation terminée : {augmented_count} images générées.")
