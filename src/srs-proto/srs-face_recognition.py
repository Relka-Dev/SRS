import cv2
import torch
import numpy as np
import argparse
import face_recognition
from triangulation import Triangulation
import mysql.connector
import json
import base64
import argparse

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

parser = argparse.ArgumentParser(description="Object Detection and Triangulation with multiple cameras")
parser.add_argument('--camera_url1', type=str, required=True, help='URL of the first camera')
parser.add_argument('--camera_url2', type=str, required=True, help='URL of the second camera')
parser.add_argument('--camera_url3', type=str, required=True, help='URL of the third camera')
parser.add_argument('--camera_url4', type=str, required=True, help='URL of the fourth camera')
parser.add_argument('--headless', action='store_true', help='Run in headless mode without GUI')
args = parser.parse_args()


# Configuration
CAMERA_URLS = [
    args.camera_url1,
    args.camera_url2,
    args.camera_url3,
    args.camera_url4
]

db_client = DatabaseClient()

CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés
ROOM_WIDTH = 4  # Largeur de la pièce en mètres
ROOM_HEIGHT = 4  # Hauteur de la pièce en mètres

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

# Imprimer les noms et encodages récupérés pour vérification
print("Noms récupérés de la base de données:")
print(known_face_names)
print("\nEncodages récupérés de la base de données:")
for i, encoding in enumerate(known_face_encodings):
    print(f"Nom: {known_face_names[i]}")
    print(f"Encodage: {encoding[:5]} ...")

def process_frame(frame, model, fov):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    angles = []
    names = []
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:  # Détecter les personnes uniquement
            center_x = (x1 + x2) / 2
            angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
            angles.append(angle)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            name = recognize_faces(frame, (x1, y1, x2, y2))
            names.append(name)
            cv2.putText(frame, f"Angle: {angle:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, name, (int(x1), int(y2) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, angles, names

def get_name_per_index(name_list):
    name_counter = {}  # Dictionnaire pour compter les occurrences des noms
    updated_name_list = []  # Liste pour stocker les noms mis à jour avec leur compteur
    
    for name in name_list:
        if name != "None" and name != "Unknown":
            if name in name_counter:
                name_counter[name] += 1
            else:
                name_counter[name] = 1

            updated_name_list.append(f"{name}_{name_counter[name]}")

        
    
    # Trouver le nom avec la plus grande correspondance
    if(len(name_counter) > 0):
        return max(name_counter, key=name_counter.get)
    
    return "Personne non reconnue"

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
    frame1_processed, angles_cam1, names_cam1 = process_frame(frame1, model, CAMERA_FOV)
    frame2_processed, angles_cam2, names_cam2 = process_frame(frame2, model, CAMERA_FOV)
    frame3_processed, angles_cam3, names_cam3 = process_frame(frame3, model, CAMERA_FOV)
    frame4_processed, angles_cam4, names_cam4 = process_frame(frame4, model, CAMERA_FOV)

    if not args.headless:
        # Afficher les frames dans des fenêtres séparées
        cv2.imshow('Camera 1', frame1_processed)
        cv2.imshow('Camera 2', frame2_processed)
        cv2.imshow('Camera 3', frame3_processed)
        cv2.imshow('Camera 4', frame4_processed)

    if len(angles_cam1) == len(angles_cam2) == len(angles_cam3) == len(angles_cam4):
        result, response = Triangulation.get_objects_positions(3.5, angles_cam1, angles_cam2, angles_cam3, angles_cam4, tolerence=0.5)

        # Créer une carte vide
        map_frame = np.zeros((map_height, map_width, 3), dtype=np.uint8)
        
        if result:  
            if args.headless:
                print("-----")
                for point in response.points:
                    print(point.value)
            else:
                i = 0
                if len(response.points) == len(angles_cam1) and len(response.points) == len(angles_cam2) and len(response.points) == len(angles_cam3) and len(response.points) == len(angles_cam4):
                    for point in response.points:
                        i += 1
                        # Redimensionner les positions pour correspondre à la carte
                        map_x = int((point.value[0] / ROOM_WIDTH) * map_width)
                        map_y = int((point.value[1] / ROOM_HEIGHT) * map_height)
                        # Limiter les coordonnées à l'intérieur de la carte
                        map_x = np.clip(map_x, 0, map_width - 1)
                        map_y = np.clip(map_y, 0, map_height - 1)
                        # Dessiner un point à la position calculée
                        found_name = get_name_per_index([names_cam1[i-1], names_cam2[i-1], names_cam3[i-1], names_cam4[i-1]])
                        cv2.circle(map_frame, (map_x, map_y), 5, (0, 0, 255), -1)  # Rouge pour le point bot
                        cv2.putText(map_frame, f"{found_name} = X: {point.value[0]:.2f}, Y: {point.value[1]:.2f}", 
                                    (10, i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.imshow('Map', map_frame)

    # Appuyer sur 'q' pour quitter les fenêtres
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Libérer les captures vidéo et fermer les fenêtres
cap1.release()
cap2.release()
cap3.release()
cap4.release()
cv2.destroyAllWindows()
