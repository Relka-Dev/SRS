"""
Détection d'Objets et Triangulation avec plusieurs caméras

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Ce script utilise OpenCV et YOLOv5 pour capturer et traiter les flux vidéo de quatre caméras IP.
Il détecte les personnes dans chaque flux, calcule leurs angles, et utilise ces angles pour trianguler
leurs positions dans une pièce.

Configuration :
- CAMERA_URLS : Liste des URL des caméras IP.
- CAMERA_FOV : Champ de vision des caméras en degrés.
- ROOM_WIDTH : Largeur de la pièce en mètres.
- ROOM_HEIGHT : Hauteur de la pièce en mètres.

Arguments :
- --camera_url1 : URL de la première caméra.
- --camera_url2 : URL de la deuxième caméra.
- --camera_url3 : URL de la troisième caméra.
- --camera_url4 : URL de la quatrième caméra.
- --wall_size : Taille des murs (largeur et hauteur de la pièce).

Dépendances :
- OpenCV
- Torch
- NumPy

Utilisation :
Assurez-vous que les caméras sont accessibles et que les dépendances sont installées.
Exécutez le script avec les URLs des caméras et la taille des murs spécifiées.
"""


import cv2
import torch
import numpy as np
from triangulation import Triangulation
import argparse

parser = argparse.ArgumentParser(description="Object Detection and Triangulation with multiple cameras")
parser.add_argument('--camera_url1', type=str, required=True, help='URL of the first camera')
parser.add_argument('--camera_url2', type=str, required=True, help='URL of the second camera')
parser.add_argument('--camera_url3', type=str, required=True, help='URL of the third camera')
parser.add_argument('--camera_url4', type=str, required=True, help='URL of the fourth camera')
parser.add_argument('--wall_size', type=str, required=True, help='Size of the walls')
args = parser.parse_args()

CAMERA_URLS = [
    args.camera_url1,
    args.camera_url2,
    args.camera_url3,
    args.camera_url4
]

wall_size = float(args.wall_size)

CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés
ROOM_WIDTH = wall_size  # Largeur de la pièce en mètres
ROOM_HEIGHT = wall_size  # Hauteur de la pièce en mètres

# Charger le modèle YOLOv5 pré-entrainé et déplacer le modèle sur le GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

# Initialisation des captures vidéo
cap1 = cv2.VideoCapture(CAMERA_URLS[0])
cap2 = cv2.VideoCapture(CAMERA_URLS[1])
cap3 = cv2.VideoCapture(CAMERA_URLS[2])
cap4 = cv2.VideoCapture(CAMERA_URLS[3])

# Vérifiez si les captures vidéo sont ouvertes correctement
if not cap1.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 1")
    exit()
if not cap2.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 2")
    exit()
# Vérifiez si les captures vidéo sont ouvertes correctement
if not cap3.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 3")
    exit()
if not cap4.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 4")
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
            angles.append(angle)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"Angle: {angle:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, angles

map_width, map_height = 600, 600

while True:
    # Lire les frames des caméras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()
    ret4, frame4 = cap4.read()

    # Si une des captures échoue, on sort de la boucle
    if not ret1 or not ret2 or not ret3 or not ret4:
        print("Erreur : Impossible de lire une frame des flux vidéo")
        break

    # Inverser les frames verticalement et horizontalement
    frame1 = cv2.flip(cv2.flip(frame1, 0), 1)
    frame2 = cv2.flip(cv2.flip(frame2, 0), 1)
    frame3 = cv2.flip(cv2.flip(frame3, 0), 1)
    frame4 = cv2.flip(cv2.flip(frame4, 0), 1)

    # Traiter les frames pour détecter les personnes et calculer les angles
    frame1_processed, angles_cam1 = process_frame(frame1, model, CAMERA_FOV)
    frame2_processed, angles_cam2 = process_frame(frame2, model, CAMERA_FOV)
    frame3_processed, angles_cam3 = process_frame(frame3, model, CAMERA_FOV)
    frame4_processed, angles_cam4 = process_frame(frame4, model, CAMERA_FOV)

    # Afficher les frames dans des fenêtres séparées
    cv2.imshow('Camera 1', frame1_processed)
    cv2.imshow('Camera 2', frame2_processed)
    cv2.imshow('Camera 3', frame3_processed)
    cv2.imshow('Camera 4', frame4_processed)

    if len(angles_cam1) == 1 and len(angles_cam2) == 1 and len(angles_cam3) == 1 and len(angles_cam4) == 1:
        result_bot, response_bot = Triangulation.get_object_position(3.5, angles_cam1[0], angles_cam2[0])
        result_top, response_top = Triangulation.get_object_position(3.5, angles_cam4[0], angles_cam3[0], reverse=True)
        
        # Créer une carte vide
        map_frame = np.zeros((map_height, map_width, 3), dtype=np.uint8)
        
        if result_bot:
            # Redimensionner les positions pour correspondre à la carte
            map_x_bot = int((response_bot[1] / ROOM_WIDTH) * map_width)
            map_y_bot = int((response_bot[0] / ROOM_HEIGHT) * map_height)
            # Limiter les coordonnées à l'intérieur de la carte
            map_x_bot = np.clip(map_x_bot, 0, map_width - 1)
            map_y_bot = np.clip(map_y_bot, 0, map_height - 1)
            # Dessiner un point à la position calculée
            cv2.circle(map_frame, (map_x_bot, map_y_bot), 5, (0, 0, 255), -1)  # Rouge pour le point bot
            cv2.putText(map_frame, f"Bot X: {response_bot[0]:.2f}, Y: {response_bot[1]:.2f}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        if result_top:
            map_x_top = int((response_top[1] / ROOM_WIDTH) * map_width)
            map_y_top = int((response_top[0] / ROOM_HEIGHT) * map_height)
            # Limiter les coordonnées à l'intérieur de la carte
            map_x_top = np.clip(map_x_top, 0, map_width - 1)
            map_y_top = np.clip(map_y_top, 0, map_height - 1)
            # Dessiner un point à la position calculée

            cv2.circle(map_frame, (map_x_top, map_y_top), 5, (255, 0, 0), -1)  # Bleu pour le point top
            cv2.putText(map_frame, f"Top X: {response_top[0]:.2f}, Y: {response_top[1]:.2f}", 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Map', map_frame)

    # Appuyer sur 'q' pour quitter les fenêtres
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les captures vidéo et fermer les fenêtres
cap1.release()
cap2.release()
cv2.destroyAllWindows()
