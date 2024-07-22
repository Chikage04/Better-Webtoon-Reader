from PIL import Image
import pytesseract

# Assurez-vous d'avoir le chemin vers le binaire tesseract si ce n'est pas dans le PATH
# pytesseract.pytesseract.tesseract_cmd = r'chemin/vers/tesseract'

def split_image(image, chunk_height):
    """
    Divise l'image en morceaux de hauteur chunk_height.
    """
    width, height = image.size
    chunks = []
    for i in range(0, height, chunk_height):
        box = (0, i, width, min(i + chunk_height, height))
        chunks.append(image.crop(box))
    return chunks

def extract_text_from_image(image_path, chunk_height=1000):
    """
    Extrait le texte d'une image très grande en la divisant en morceaux.
    """
    image = Image.open(image_path)
    chunks = split_image(image, chunk_height)
    
    full_text = []
    for i, chunk in enumerate(chunks):
        print(f"Extraction de texte pour le morceau {i + 1} sur {len(chunks)}...")
        text = pytesseract.image_to_string(chunk, lang='fra')  # 'fra' pour le français, changer selon la langue
        full_text.append(text)
    
    return "\n".join(full_text)

# Remplacez 'chemin/vers/mon_image.png' par le chemin de votre image
image_path = 'a.png'
extracted_text = extract_text_from_image(image_path)
print("Texte extrait :")
print(extracted_text)
