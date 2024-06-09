"""
Script de Surveillance Vidéo Multi-Caméras avec Détection de Personnes utilisant YOLOv5

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Ce script utilise OpenCV et YOLOv5 pour capturer et traiter les flux vidéo de deux caméras IP. 
L'objectif est de détecter les personnes dans chaque flux vidéo et de calculer leurs angles par rapport au centre de chaque image.
Les angles sont ensuite utilisés pour trianguler et afficher les positions d'une personne dans une carte de la pièce.

Configuration :
- CAMERA_FOV : Champ de vision (FOV) des caméras en degrés.
- ROOM_WIDTH : Largeur de la pièce en mètres.
- ROOM_HEIGHT : Hauteur de la pièce en mètres.

Argumentation :
- --camera_url1 : URL du flux vidéo de la première caméra.
- --camera_url2 : URL du flux vidéo de la deuxième caméra.

Fonctionnement :
1. Charge un modèle pré-entrainé YOLOv5 pour la détection de personnes.
2. Initialise les captures vidéo pour chaque caméra via les URLs fournies en arguments.
3. Vérifie si les flux vidéo sont accessibles.
4. Capture et traite les frames de chaque caméra pour détecter les personnes.
5. Calcule les angles des personnes détectées par rapport au centre de chaque image.
6. Triangule les positions des personnes dans la pièce et affiche les résultats sur une carte.
7. Libère les ressources et ferme les fenêtres lorsqu'on appuie sur 'q'.

Dépendances :
- OpenCV
- Torch
- NumPy

Exécution :
Assurez-vous que les caméras IP sont accessibles aux URL spécifiées et que les dépendances sont installées.
Exécutez le script en ligne de commande avec les URLs des flux vidéo des caméras :
    python script.py --camera_url1 <URL_CAMERA_1> --camera_url2 <URL_CAMERA_2>

Notes :
- Ce script est configuré pour fonctionner avec deux caméras IP positionnées de manière à couvrir la pièce.
- La détection de personnes est basée sur le modèle YOLOv5s pré-entrainé.
- Les angles calculés peuvent être utilisés pour estimer la position des personnes dans la pièce.

"""
import cv2
import torch
import argparse
import numpy as np
from triangulation import Triangulation

# Configuration
CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés
ROOM_WIDTH = 3.5  # Largeur de la pièce en mètres
ROOM_HEIGHT = 3.5 # Hauteur de la pièce en mètres

# Argument parser
parser = argparse.ArgumentParser(description='Script de détection d\'angles de personnes à partir de deux vidéos.')
parser.add_argument('--camera_url1', type=str, required=True, help='URL du flux vidéo de la première caméra')
parser.add_argument('--camera_url2', type=str, required=True, help='URL du flux vidéo de la deuxième caméra')
parser.add_argument('--wall_size', type=str, required=True, help='Distance entre les deux cameras')
args = parser.parse_args()

wall_size = float(args.wall_size)

CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés
ROOM_WIDTH = wall_size  # Largeur de la pièce en mètres
ROOM_HEIGHT = wall_size  # Hauteur de la pièce en mètres

CAMERA_URL1 = args.camera_url1
CAMERA_URL2 = args.camera_url2

# Chargement de modèle YOLOv5 pré-entrainé et déplacer le modèle sur le GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

# Initialisation des captures vidéo
cap1 = cv2.VideoCapture(CAMERA_URL1)
cap2 = cv2.VideoCapture(CAMERA_URL2)

# Vérifiez si les captures vidéo sont ouvertes correctement
if not cap1.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 1")
    exit()
if not cap2.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 2")
    exit()

def process_frame(frame, model, fov):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    angles = []
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:
            center_x = (x1 + x2) / 2
            angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
            angles.append(angle)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"Angle: {angle:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, angles

map_width, map_height = 600, 600

while True:
    # Lire les frames des deux caméras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    # Si une des captures échoue, on sort de la boucle
    if not ret1 or not ret2:
        print("Erreur : Impossible de lire une frame des flux vidéo")
        break

    frame1 = cv2.flip(cv2.flip(frame1, 0), 1)
    frame2 = cv2.flip(cv2.flip(frame2, 0), 1)

    # Traiter les frames pour détecter les personnes et calculer les angles
    frame1_processed, angles_cam1 = process_frame(frame1, model, CAMERA_FOV)
    frame2_processed, angles_cam2 = process_frame(frame2, model, CAMERA_FOV)

    # Afficher les frames dans des fenêtres séparées
    cv2.imshow('Camera 1', frame1_processed)
    cv2.imshow('Camera 2', frame2_processed)

    if len(angles_cam2) == 1 and len(angles_cam1) == 1:
        result, response = Triangulation.get_object_position(3.5, angles_cam1[0], angles_cam2[0], True)
        if result:
            map_frame = np.zeros((map_height, map_width, 3), dtype=np.uint8)
            # Redimensionner les positions pour correspondre à la carte
            map_x = int(((ROOM_WIDTH - response[0]) / ROOM_WIDTH) * map_width)
            map_y = int(((ROOM_HEIGHT - response[1]) / ROOM_HEIGHT) * map_height)
            # Limiter les coordonnées à l'intérieur de la carte
            map_x = np.clip(map_x, 0, map_width - 1)
            map_y = np.clip(map_y, 0, map_height - 1)
            # Dessiner un point à la position calculée
            cv2.circle(map_frame, (map_x, map_y), 5, (0, 0, 255), -1)
            cv2.putText(map_frame, f"X: {response[0]:.2f}, Y: {response[1]:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.imshow('Map', map_frame)

    # Appuyer sur 'q' pour quitter les fenêtres
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les captures vidéo et fermer les fenêtres
cap1.release()
cap2.release()
cv2.destroyAllWindows()
