"""
Détection d'Angles de Personnes à partir d'une Vidéo

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Ce script utilise OpenCV et YOLOv5 pour détecter des personnes et calculer leurs angles par rapport au centre de l'image
à partir d'un flux vidéo d'une caméra. Les résultats sont affichés en temps réel sur la vidéo.

Dépendances :
- OpenCV
- Torch

Utilisation :
Assurez-vous que la caméra est accessible via l'URL spécifiée et que les dépendances sont installées.
Exécutez le script en fournissant l'URL du flux vidéo de la caméra.
"""


import cv2
import torch
import argparse

# Configuration
CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés

# Argument parser
parser = argparse.ArgumentParser(description='Script de détection d\'angles de personnes à partir d\'une vidéo.')
parser.add_argument('--camera_url1', type=str, required=True, help='URL du flux vidéo de la caméra')
args = parser.parse_args()

CAMERA_URL = args.camera_url1

# Charger le modèle YOLOv5 pré-entrainé et déplacer le modèle sur le GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(CAMERA_URL)

# Vérifiez si la capture vidéo est ouverte correctement
if not cap.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra")
    exit()

def process_frame(frame, model, fov):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    angles = []
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:  # Détecter les personnes uniquement
            center_x = (x1 + x2) / 2
            angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
            print(angle)
            angles.append(angle)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"Angle: {angle:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, angles

while True:
    # Lire la frame de la caméra
    ret, frame = cap.read()

    # Si la capture échoue, on sort de la boucle
    if not ret:
        print("Erreur : Impossible de lire une frame du flux vidéo")
        break

    # Inverser la frame de haut en bas
    frame = cv2.flip(frame, 0)

    # Traiter la frame pour détecter les personnes et calculer les angles
    frame_processed, angles = process_frame(frame, model, CAMERA_FOV)

    # Afficher la frame avec l'angle détecté
    cv2.imshow('Camera', frame_processed)

    # Appuyer sur 'q' pour quitter les fenêtres
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture vidéo et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
