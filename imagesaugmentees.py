import os

# === PARAMÈTRES ===
augmented_image_folder = 'C:/cours_b3/mspr-ia/WildLens_MSPR/augmented/images'
augmented_label_folder = 'C:/cours_b3/mspr-ia/WildLens_MSPR/augmented/labels'
classes_txt_path = 'C:/cours_b3/mspr-ia/WildLens_MSPR/classes.txt'

# Charger les classes dans une liste indexée par ID
with open(classes_txt_path, 'r', encoding='utf-8') as f:
    id_to_class = [line.strip() for line in f.readlines()]

# Dictionnaire pour compter les images par classe
image_counts_per_class = {class_name: 0 for class_name in id_to_class}

# Parcourir les fichiers d'annotation YOLO
for filename in os.listdir(augmented_label_folder):
    if not filename.endswith('.txt'):
        continue

    filepath = os.path.join(augmented_label_folder, filename)
    class_ids_found = set()

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            try:
                class_id = int(float(parts[0]))  # Gère aussi les formats comme '5.0'
                class_ids_found.add(class_id)
            except Exception as e:
                print(f"[ERREUR] {filename} → {e}")

    for class_id in class_ids_found:
        if 0 <= class_id < len(id_to_class):
            class_name = id_to_class[class_id]
            image_counts_per_class[class_name] += 1
        else:
            print(f"[AVERTISSEMENT] ID de classe hors limites : {class_id} dans {filename}")

# Résultat
print("\nNombre d’images augmentées par espèce :\n")
for species, count in image_counts_per_class.items():
    print(f"{species} : {count}")
