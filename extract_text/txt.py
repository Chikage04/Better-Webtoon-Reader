import cv2
import pytesseract
import numpy as np
import concurrent.futures
from tqdm import tqdm

# Configuration du chemin de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Assurez-vous que c'est le bon chemin

# Fonction pour diviser l'image en segments
def split_image(image, segment_height):
    segments = []
    img_height = image.shape[0]
    for i in range(0, img_height, segment_height):
        segment = image[i:i + segment_height, :]
        segments.append(segment)
    return segments

# Fonction pour extraire le texte d'un segment d'image
def extract_text_from_segment(segment):
    text = pytesseract.image_to_string(segment)
    return text

# Charger l'image
image_path = 'C:/Users/Lucas/Downloads/Webtoon-Downloader-master (1)/Webtoon-Downloader-master/extract_text/a.png'

# Ajout de messages de débogage
print(f"Chargement de l'image depuis : {image_path}")

image = cv2.imread(image_path, cv2.IMREAD_COLOR)

# Diviser l'image en segments
segment_height = 1000  # Définis la hauteur des segments
segments = split_image(image, segment_height)

# Ajout de messages de débogage
print(f"Nombre de segments à découper : {len(segments)}")

# Fonction pour traiter chaque segment avec extraction de texte
def process_segment(segment):
    try:
        return extract_text_from_segment(segment)
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte : {e}")
        return ""

# Utilisation de multithreading pour accélérer le processus
full_text = ""
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(tqdm(executor.map(process_segment, segments), total=len(segments), desc="Extraction du texte"))

# Concaténer les résultats
full_text = "\n".join(results)

# Sauvegarder le texte extrait dans un fichier
with open('extracted_text.txt', 'w', encoding='utf-8') as file:
    file.write(full_text)

print("Extraction du texte terminée et sauvegardée dans 'extracted_text.txt'.")
