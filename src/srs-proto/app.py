import cv2
import torch
import numpy as np
from triangulation import Triangulation

# Configuration
CAMERA_URLS = [
    "http://192.168.1.131:4298/video?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiU1JTLVNlcnZlciIsImV4cCI6MTcxNjQ2MTA2NX0.lIPgSF798aOxdRcOBiEV9SOOSO1y3oDfYxSsIZTqNtU",
    "http://192.168.1.26:4298/video?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiU1JTLVNlcnZlciIsImV4cCI6MTcxNjQ2MTA2NX0.lIPgSF798aOxdRcOBiEV9SOOSO1y3oDfYxSsIZTqNtU"
]

CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés

# Charger le modèle YOLOv5 pré-entrainé
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Initialisation des captures vidéo
cap1 = cv2.VideoCapture(CAMERA_URLS[0])
cap2 = cv2.VideoCapture(CAMERA_URLS[1])

# Vérifiez si les captures vidéo sont ouvertes correctement
if not cap1.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 1")
if not cap2.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 2")

def process_frame(frame, model, fov):
    results = model(frame)
    angles = []
    for det in results.xyxy[0].numpy():
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

    frame1 = cv2.flip(frame1, 0)
    frame2 = cv2.flip(frame2, 0)

    # Traiter les frames pour détecter les personnes et calculer les angles
    frame1_processed, angles_cam1 = process_frame(frame1, model, CAMERA_FOV)
    frame2_processed, angles_cam2 = process_frame(frame2, model, CAMERA_FOV)

    # Afficher les frames dans des fenêtres séparées
    cv2.imshow('Camera 1', frame1_processed)
    cv2.imshow('Camera 2', frame2_processed)

    if len(angles_cam2) == 1 and len(angles_cam1) == 1: 
        result, response = Triangulation.get_object_position(1, angles_cam1[0], angles_cam2[0])
        if result:
            map_frame = np.zeros((map_height, map_width, 3), dtype=np.uint8)
            # Redimensionner les positions pour correspondre à la carte
            map_x = int((response[0] / 10.0) * map_width)  # Ajuster selon l'échelle réelle
            map_y = int((response[1] / 10.0) * map_height)  # Ajuster selon l'échelle réelle
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
