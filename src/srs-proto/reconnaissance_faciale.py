"""
Détection d'Objets et Reconnaissance Faciale

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Ce script utilise OpenCV et YOLOv5 pour détecter des personnes et reconnaître les visages en temps réel 
à partir d'une caméra. Les encodages des visages sont récupérés d'une base de données MySQL.

Dépendances :
- OpenCV
- Torch
- face_recognition
- NumPy
- mysql.connector

Utilisation :
Exécutez le script avec les dépendances installées et une caméra connectée.
"""

import os
import torch
import cv2
import face_recognition
import numpy as np
import ast
import mysql.connector
import base64
import json

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

# Charger le modèle YOLOv5 pré-entraîné
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialiser la base de données
db_client = DatabaseClient()

# Récupérer les encodages des utilisateurs
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

def recognize_faces(image, bbox, tolerance=0.6):
    top, left, bottom, right = int(bbox[1]), int(bbox[0]), int(bbox[3]), int(bbox[2])
    face_image = image[top:bottom, left:right]
    
    # Conversion au format RGB
    face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    
    # Recherche de visage dans l'image
    face_locations = face_recognition.face_locations(face_image_rgb)
    if not face_locations:
        return "Personne"
    
    face_encodings = face_recognition.face_encodings(face_image_rgb, face_locations)
    if not face_encodings:
        return "Personne"
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance)
        name = "Visage inconnu"
        
        if np.any(matches):  # Permet de déterminer s'il y a une corresponsance dans la liste
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches and best_match_index < len(matches) and matches[best_match_index]:
                name = known_face_names[best_match_index]
        
        return name
    return "Personne"

# Capturer la vidéo en temps réel
video_capture = cv2.VideoCapture(0)

while True:
    # Capturer une image de la vidéo
    ret, frame = video_capture.read()
    
    if not ret:
        break
    
    results = model(frame)
    
    bboxes = results.xyxy[0].cpu().numpy()
    
    # Filtrer pour ne garder que les personnes (class 0 in COCO dataset)
    person_bboxes = [bbox for bbox in bboxes if int(bbox[5]) == 0]
    
    # Liste des résultats
    results_list = []

    # Pour chaque personne détectée, essayer de reconnaître le visage
    for bbox in person_bboxes:
        name = recognize_faces(frame, bbox, tolerance=0.4)  # Ajuster la tolérance ici si nécessaire
        results_list.append({'Position': bbox[:4], 'Personne détectée': name})
        
        # Dessiner la boîte englobante et le nom sur l'image
        left, top, right, bottom = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({left}, {top}, {right}, {bottom})", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Afficher le résultat
    cv2.imshow('Video', frame)
    
    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture de la vidéo
video_capture.release()
cv2.destroyAllWindows()
