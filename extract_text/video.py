import cv2
import pytesseract
import concurrent.futures
from tqdm import tqdm
from difflib import SequenceMatcher

# Configuration du chemin de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Assurez-vous que c'est le bon chemin

# Fonction pour extraire le texte d'une image
def extract_text_from_frame(frame):
    text = pytesseract.image_to_string(frame)
    return text

# Fonction pour comparer le texte entre deux frames
def similar_text(text1, text2, threshold=0.8):
    similarity_ratio = SequenceMatcher(None, text1, text2).quick_ratio()
    return similarity_ratio >= threshold

# Chargement de la vidéo
video_path = 'c.mp4'  # Remplacez par le chemin de votre vidéo

# Ouvrir la vidéo en lecture
video_capture = cv2.VideoCapture(video_path)

# Vérifier si la vidéo est ouverte correctement
if not video_capture.isOpened():
    print(f"Erreur lors de l'ouverture de la vidéo : {video_path}")
    exit()

# Récupérer les propriétés de la vidéo
frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Ajout de messages de débogage
print(f"Informations sur la vidéo :")
print(f" - Nombre de frames : {frame_count}")
print(f" - FPS : {fps}")
print(f" - Résolution : {width} x {height}")

# Utilisation de multithreading pour accélérer le processus
full_text = ""
previous_text = ""
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for _ in tqdm(range(0, frame_count, 3), desc="Extraction du texte"):
        ret, frame = video_capture.read()
        if not ret:
            break
        future = executor.submit(extract_text_from_frame, frame)
        futures.append(future)

    for future in concurrent.futures.as_completed(futures):
        current_text = future.result()
        if current_text and not similar_text(current_text, previous_text):
            full_text += current_text + "\n"
            previous_text = current_text

# Sauvegarder le texte extrait dans un fichier
with open('extracted_text_from_video.txt', 'w', encoding='utf-8') as file:
    file.write(full_text)

# Libérer la capture vidéo
video_capture.release()
cv2.destroyAllWindows()

print("Extraction du texte depuis la vidéo terminée et sauvegardée dans 'extracted_text_from_video.txt'.")
