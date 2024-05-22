import cv2
import requests
import numpy as np
import time
import os

time.sleep(3)
# Créer des répertoires pour sauvegarder les images récupérées
os.makedirs('./stereoLeft', exist_ok=True)
os.makedirs('./stereoRight', exist_ok=True)

# URLs des serveurs Flask pour récupérer les images de calibration
image_urls = ['http://192.168.1.131:4298/image', 'http://192.168.1.26:4298/image']

# Token JWT
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiU1JTLVNlcnZlciIsImV4cCI6MTcxNTkzMTYzNH0.bnhGSMCLVPuIXbTtuqz1N1WC1T2rfMo56n2m0m18wh8'


# Headers pour l'authentification
params = {'token': token}

def get_calibration_images(urls, params, num_images=10):
    for j in range(num_images):
        images = []
        for i, url in enumerate(urls):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                img_array = np.frombuffer(response.content, np.uint8)
                img = cv2.flip(cv2.imdecode(img_array, cv2.IMREAD_COLOR), 0)
                if img is not None:
                    images.append((i, img))
            else:
                print(f"Failed to get image from {url}. Status code: {response.status_code}")
                continue

        if len(images) == len(urls):
            for i, img in images:
                # Sauvegarder l'image dans le dossier correspondant
                if i == 0:
                    image_path = f'./stereoLeft/imageL{j+1}.jpg'
                else:
                    image_path = f'./stereoRight/imageR{j+1}.jpg'
                cv2.imwrite(image_path, img)
                print(f"Saved image to {image_path}")

        # Attendre une seconde avant la prochaine capture
        time.sleep(1)

# Appel de la fonction pour récupérer et enregistrer les images
get_calibration_images(image_urls, params)
