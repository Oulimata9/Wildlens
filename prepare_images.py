import os
from PIL import Image

input_base = 'C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\Mammiferes'
output_base = 'C:\\cours_b3\\mspr-ia\\WildLens_MSPR\\images_nettoyees'
target_size = (224, 224)

#  génère le fichier empreintes.csv
os.makedirs(output_base, exist_ok=True)

for espece in os.listdir(input_base):
    espece_path = os.path.join(input_base, espece)
    if os.path.isdir(espece_path):
        output_espece_path = os.path.join(output_base, espece)
        os.makedirs(output_espece_path, exist_ok=True)
        for filename in os.listdir(espece_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                img_path = os.path.join(espece_path, filename)
                try:
                    img = Image.open(img_path).convert('RGB')
                    img = img.resize(target_size)
                    base_name = os.path.splitext(filename)[0]
                    output_path = os.path.join(output_espece_path, base_name + '.jpg')
                    img.save(output_path, format='JPEG')
                except Exception as e:
                    print(f"Erreur avec {img_path} : {e}")
print("Traitement terminé.")
