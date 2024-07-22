import re

def clean_text(text):
    # Convertir en minuscules et supprimer la ponctuation et les chiffres
    text = text.lower()
    text = re.sub(r'[^\w\s]|[\d]', '', text)
    return text

def find_unique_word_groups(text1, text2):
    # Nettoyer les textes
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    
    # Diviser les textes en mots
    words1 = text1.split()
    words2 = text2.split()
    
    unique_groups = set()

    # Trouver les groupes de mots uniques dans text1
    for i in range(len(words1) - 2):
        group = ' '.join(words1[i:i+3])
        if group not in text2:
            unique_groups.add(group)
    
    # Trouver les groupes de mots uniques dans text2
    for i in range(len(words2) - 2):
        group = ' '.join(words2[i:i+3])
        if group not in text1:
            unique_groups.add(group)
    
    return unique_groups

# Exemple d'utilisation
if __name__ == "__main__":
    # Lire les fichiers texte (modifier les chemins selon vos fichiers)
    with open('1.txt', 'r', encoding='utf-8') as file1:
        text1 = file1.read()
    
    with open('2.txt', 'r', encoding='utf-8') as file2:
        text2 = file2.read()
    
    # Trouver les groupes de mots uniques
    unique_word_groups = find_unique_word_groups(text1, text2)
    
    # Afficher les résultats
    print("Groupes de mots uniques (minimum 3 mots consécutifs) :")
    for group in unique_word_groups:
        print(group)
