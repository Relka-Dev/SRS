"""
Classe SpaceRecognition

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Cette classe utilise OpenCV et YOLOv5 pour détecter les personnes dans des images et calculer leurs angles par rapport 
au centre de l'image, ainsi que leur taille. Elle permet également de convertir des images encodées en base64 en 
positions normalisées des personnes dans l'image.

Attributs :
- device : Le dispositif (CPU ou GPU) sur lequel exécuter le modèle YOLOv5.
- model : Le modèle pré-entraîné YOLOv5 pour la détection d'objets.

Méthodes :
- _detect_people : Détecte les personnes dans une image donnée.
- get_persons_angles : Calcule les angles des personnes par rapport au centre de l'image.
- get_persons_angles_with_size : Calcule les angles et les tailles des personnes par rapport au centre de l'image.
- get_people_positions_x : Convertit une image encodée en base64 en positions normalisées des personnes dans l'image.

Utilisation :
Cette classe est conçue pour être utilisée dans des systèmes de surveillance et d'analyse vidéo pour détecter et 
suivre les personnes dans un espace donné.
"""

import cv2
import torch
import numpy as np

class SpaceRecognition:

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(self.device)

    
    def _detect_people(self, image):
        """
        Détecte les personnes dans une image donnée.

        Args:
            image (np.ndarray): L'image dans laquelle détecter les personnes.

        Returns:
            pd.DataFrame: Un DataFrame contenant les informations des personnes détectées.
        """
        frame_rgb = cv2.cvtColo
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        results = results.pandas().xyxy[0]
        people = results[results['name'] == 'person']
        return people
    
    def get_persons_angles(self, frame, fov):
        """
        Calcule les angles des personnes par rapport au centre de l'image.

        Args:
            frame (np.ndarray): L'image dans laquelle détecter les personnes.
            fov (float): Le champ de vision de la caméra en degrés.

        Returns:
            tuple: Un booléen indiquant le succès de l'opération et une liste des angles des personnes détectées.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        angles = []
        for det in results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2, conf, cls = det
            if cls == 0:
                center_x = (x1 + x2) / 2
                angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
                angles.append(angle)
        return True, angles
    
    def get_persons_angles_with_size(self, frame, fov):
        """
        Calcule les angles et les tailles des personnes par rapport au centre de l'image.

        Args:
            frame (np.ndarray): L'image dans laquelle détecter les personnes.
            fov (float): Le champ de vision de la caméra en degrés.

        Returns:
            list: Une liste de tuples contenant les angles et les tailles des personnes détectées.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        angles_and_sizes = []
        for det in results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2, conf, cls = det
            if cls == 0:
                center_x = (x1 + x2) / 2
                angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
                size_y = y2 - y1
                angles_and_sizes.append((angle, size_y))
        return angles_and_sizes

    
    def get_people_positions_x(self, imageBase64):
        """
        Convertit une image encodée en base64 en positions normalisées des personnes dans l'image.

        Args:
            imageBase64 (bytes): L'image encodée en base64.

        Returns:
            list: Une liste des positions normalisées des personnes dans l'image.
        """
        nparr = np.frombuffer(imageBase64, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detections = self._detect_people(image)

        people_positions = []

        for index, row in detections.iterrows():
            x_center = (row['xmin'] + row['xmax']) / 2
            width = image.shape[1]
            normalized_x_position = (x_center / width) * 100
            people_positions.append(normalized_x_position)

        return people_positions
