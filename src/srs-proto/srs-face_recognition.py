import os
import torch
import cv2
import face_recognition
import numpy as np
import argparse
import mysql.connector
import base64
import json
from triangulation import Triangulation

# Configuration des caméras et de la pièce
CAMERA_URLS = [
    "http://192.168.1.115:4298/video",
    "http://192.168.1.121:4298/video",
    "http://192.168.1.118:4298/video",
    "http://192.168.1.114:4298/video"
]
CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés
ROOM_WIDTH = 4  # Largeur de la pièce en mètres
ROOM_HEIGHT = 4  # Hauteur de la pièce en mètres

# Argument parser for headless mode
parser = argparse.ArgumentParser(description="Object Detection and Triangulation")
parser.add_argument('--headless', action='store_true', help='Run in headless mode without GUI')
args = parser.parse_args()

# Charger le modèle YOLOv5 pré-entraîné
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

# Classe pour gérer la base de données
class DatabaseClient:
    def __init__(self):
        self.dbConnexion = mysql.connector.connect(
            host="127.0.0.1",
            user="srs-admin",
            password="fzg5jc29cHbKcSuK",
            database="srs"
        )
        self.cursor = self.dbConnexion.cursor()

    def get_encodings(self):
        try:
            self.cursor.execute("SELECT username, encodings FROM Users")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

# Initialiser la base de données
db_client = DatabaseClient()
users_data = db_client.get_encodings()

# Listes pour stocker les encodages de visages et les noms
known_face_encodings = []
known_face_names = []

# Convertir les encodages de chaînes d'octets en listes de nombres flottants
for user_data in users_data:
    known_face_names.append(user_data[0])
    encoding_base64 = user_data[1]
    encoding_json = base64.b64decode(encoding_base64).decode('utf-8')
    encoding = json.loads(encoding_json)
    if len(encoding) == 128:  # Vérifier la taille de chaque encodage
        known_face_encodings.append(encoding)
    else:
        print(f"Encodage incorrect pour {user_data[0]}: {encoding}")

# Fonction pour faire la reconnaissance faciale
def recognize_faces(image, bbox, tolerance=0.6):
    top, left, bottom, right = int(bbox[1]), int(bbox[0]), int(bbox[3]), int(bbox[2])
    face_image = image[top:bottom, left:right]
    
    # Convertir l'image au format RGB
    face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    
    # Trouver les visages et encodages de visages dans l'image
    face_locations = face_recognition.face_locations(face_image_rgb)
    if not face_locations:
        return "None"
    
    face_encodings = face_recognition.face_encodings(face_image_rgb, face_locations)
    if not face_encodings:
        return "None"
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance)
        name = "Unknown"
        
        if np.any(matches):  # Utiliser np.any() pour vérifier s'il y a au moins une correspondance
            # Trouver les distances
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            # Assurez-vous que best_match_index est dans les limites de matches et matches n'est pas vide
            if matches and best_match_index < len(matches) and matches[best_match_index]:
                name = known_face_names[best_match_index]
        
        return name
    return "None"

# Initialisation des captures vidéo
caps = [cv2.VideoCapture(url) for url in CAMERA_URLS]

# Vérifiez si les captures vidéo sont ouvertes correctement
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"Erreur : Impossible de lire le flux vidéo de la caméra {i + 1}")
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
    frames = []
    ret_values = []
    for cap in caps:
        ret, frame = cap.read()
        ret_values.append(ret)
        frames.append(frame)
    
    # Si une des captures échoue, on sort de la boucle
    if not all(ret_values):
        print("Erreur : Impossible de lire une frame des flux vidéo")
        break

    # Inverser les frames verticalement et horizontalement
    frames = [cv2.flip(cv2.flip(frame, 0), 1) for frame in frames]

    # Traiter les frames pour détecter les personnes et calculer les angles
    processed_frames = []
    all_angles = []
    for frame in frames:
        processed_frame, angles = process_frame(frame, model, CAMERA_FOV)
        processed_frames.append(processed_frame)
        all_angles.append(angles)

    if not args.headless:
        # Afficher les frames dans des fenêtres séparées
        for i, frame in enumerate(processed_frames):
            cv2.imshow(f'Camera {i + 1}', frame)

    # Vérifier si les angles sont disponibles pour toutes les caméras
    if all(len(angles) == 2 for angles in all_angles):
        result, response = Triangulation.get_objects_positions(3.5, *all_angles, tolerence=0.5)

        # Créer une carte vide
        map_frame = np.zeros((map_height, map_width, 3), dtype=np.uint8)
        
        if result:
            if args.headless:
                print("-----")
                for point in response.points:
                    print(point.value)
            else:
                for i, point in enumerate(response.points):
                    # Redimensionner les positions pour correspondre à la carte
                    map_x = int((point.value[0] / ROOM_WIDTH) * map_width)
                    map_y = int((point.value[1] / ROOM_HEIGHT) * map_height)
                    # Limiter les coordonnées à l'intérieur de la carte
                    map_x = np.clip(map_x, 0, map_width - 1)
                    map_y = np.clip(map_y, 0, map_height - 1)
                    # Dessiner un point à la position calculée
                    cv2.circle(map_frame, (map_x, map_y), 5, (0, 0, 255), -1)  # Rouge pour le point bot
                    cv2.putText(map_frame, f"User {i + 1} = X: {point.value[0]:.2f}, Y: {point.value[1]:.2f}", 
                                (10, i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.imshow('Map', map_frame)

    # Appuyer sur 'q' pour quitter les fenêtres
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les captures vidéo et fermer les fenêtres
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
