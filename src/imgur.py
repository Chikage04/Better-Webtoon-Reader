import requests
import os
import base64
import time

def main():
    # Remplacez par vos informations d'identification Imgur
    client_id = "dbad42f279f3dc8"
    access_token = "6404b896d778328986b3e1689d2c6480601a5cdd"

    # Titre de l'album
    album_title = "Mon album d'images"

    # Création de l'album
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post("https://api.imgur.com/3/album", headers=headers)

    if response.status_code == 200:
        album_id = response.json()["data"]["id"]
        album_url = f"https://cubari.moe/read/imgur/{album_id}/1/1/"
        print(f"Album créé avec succès: {album_url}")
    else:
        print(f"Erreur lors de la création de l'album: {response.status_code}")
        print(f"Contenu de la réponse: {response.content}")
        album_id = None

    # Téléchargement des images vers l'album
    def upload_image(image_path, album_id):
        print(f"Tentative d'upload de l'image: {image_path}")
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        success = False
        attempt = 0
        while not success:
            print(f"Tentative d'upload de l'image: {image_path} (Tentative #{attempt + 1})")
            response = requests.post(
                "https://api.imgur.com/3/image",
                headers=headers,
                data={
                    "image": image_data,
                    "album": album_id,
                    "type": "base64",
                },
            )
            if response.status_code == 200:
                success = True
                print(f"Image téléchargée avec succès: {image_path}")
            else:
                attempt += 1
                print(f"Erreur lors du téléchargement de l'image: {image_path}")
                print(f"Code d'état de la réponse: {response.status_code}")
                print(f"Contenu de la réponse: {response.content}")
                time.sleep(5)

    # Remplacez 'images_folder' par le chemin d'accès à votre dossier d'images
    images_folder = '10k'

    if album_id:
        for image_path in os.listdir(images_folder):
            full_image_path = os.path.join(images_folder, image_path)
            if os.path.isfile(full_image_path):
                print(f"Upload de l'image : {image_path}")
                upload_image(full_image_path, album_id)
        print(f"Album complet disponible à l'adresse : {album_url}")
    else:
        print("L'album n'a pas pu être créé, donc les images ne seront pas téléchargées.")

if __name__ == "__main__":
    main()
