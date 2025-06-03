import os
from collections import Counter

# Dossier contenant les .txt YOLO
labels_folder = 'C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\annotation\\yolo_labels'
classes_file = 'classes.txt'

# Charger la liste des classes
with open(classes_file, 'r', encoding='utf-8') as f:
    class_list = [line.strip() for line in f.readlines()]

# Compter les apparitions par class_id
counter = Counter()

for txt_file in os.listdir(labels_folder):
    if not txt_file.endswith('.txt'):
        continue
    with open(os.path.join(labels_folder, txt_file), 'r') as f:
        for line in f:
            class_id = int(line.split()[0])
            counter[class_id] += 1

# Affichage des résultats
print("\n Répartition des annotations YOLO :\n")
for class_id in sorted(counter.keys()):
    print(f"  - {class_list[class_id]} ({class_id}) : {counter[class_id]} annotations")

print("\n Classes sous-représentées (< 20 annotations) :")
for class_id, count in counter.items():
    if count < 20:
        print(f"  - {class_list[class_id]} : {count}")
