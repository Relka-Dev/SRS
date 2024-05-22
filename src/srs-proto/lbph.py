import cv2
import numpy as np
import os

# Charger votre image et la convertir en niveaux de gris
known_image_path = "karel.jpg"  # Remplacez par le chemin vers votre photo
known_image = cv2.imread(known_image_path)
gray_known_image = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)

# Créer un répertoire pour stocker les images de formation si nécessaire
if not os.path.exists("training_images"):
    os.makedirs("training_images")

# Sauvegarder l'image dans le répertoire de formation
cv2.imwrite("training_images/known_face.jpg", gray_known_image)

# Préparer les données de formation pour le modèle LBPH
faces = []
labels = []

# Charger les images de formation
training_image_path = "training_images/known_face.jpg"
face_image = cv2.imread(training_image_path, cv2.IMREAD_GRAYSCALE)
faces.append(face_image)
labels.append(1)  # Etiquette pour votre visage

# Entraîner le modèle LBPH
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

# Sauvegarder le modèle entraîné
face_recognizer.save("face_recognizer_model.yml")
