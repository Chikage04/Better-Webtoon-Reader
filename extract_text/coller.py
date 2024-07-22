import pyautogui
import pyperclip
import time

# Fonction pour effectuer les actions sur chaque ligne
def effectuer_actions_sur_ligne(texte):
    pyautogui.click()
    
    pyperclip.copy(texte)
    
    pyautogui.hotkey('ctrl', 'v')
    
    pyautogui.press('enter')
    
    time.sleep(0.3)
    

nom_fichier = 'resultats.txt'

with open(nom_fichier, 'r', encoding='utf-8') as f:
    lignes = f.readlines()
    for ligne in lignes:
        texte = ligne.strip()
        effectuer_actions_sur_ligne(texte)
