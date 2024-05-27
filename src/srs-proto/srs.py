import cv2
import torch
import numpy as np
import dlib
import os
from triangulation import Triangulation

# Configuration
CAMERA_URLS = [
    "http://192.168.1.115:4298/video",
    "http://192.168.1.114:4298/video"
]

CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés
ROOM_WIDTH = 4  # Largeur de la pièce en mètres
ROOM_HEIGHT = 4  # Hauteur de la pièce en mètres

# Charger le modèle YOLOv5 pré-entrainé et déplacer le modèle sur le GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)
    print("YOLOv5 model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLOv5 model: {e}")
    exit()

# Initialisation des captures vidéo
cap1 = cv2.VideoCapture(CAMERA_URLS[0])
cap2 = cv2.VideoCapture(CAMERA_URLS[1])

# Vérifiez si les captures vidéo sont ouvertes correctement
if not cap1.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 1")
    exit()
if not cap2.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 2")
    exit()

class FaceRecognitionSRS:
    def __init__(self):
        try:
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
            self.face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
            self.known_face_descriptors, self.known_labels = self.load_faces('faces')
            print("Dlib models loaded successfully.")
        except Exception as e:
            print(f"Error loading Dlib models: {e}")
            exit()

    # Fonction pour extraire les descripteurs de visage
    def get_face_descriptor(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if len(faces) == 0:
            return None

        shape = self.predictor(gray, faces[0])
        if isinstance(shape, dlib.full_object_detection):
            print(f"shape is a valid full_object_detection: {shape}")
        else:
            print(f"shape is NOT a valid full_object_detection: {type(shape)}")
        
        if isinstance(img, np.ndarray):
            print(f"img is a valid ndarray with shape {img.shape}")
        else:
            print(f"img is NOT a valid ndarray: {type(img)}")

        face_descriptor = np.array(self.face_rec_model.compute_face_descriptor(img, shape))
        return face_descriptor

    # Chargement des images et extraction des descripteurs
    def load_faces(self, directory):
        face_descriptors = []
        labels = []
        for filename in os.listdir(directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                path = os.path.join(directory, filename)
                descriptor = self.get_face_descriptor(cv2.imread(path))
                if descriptor is not None:
                    face_descriptors.append(descriptor)
                    labels.append(filename)
        return face_descriptors, labels

    # Comparaison des descripteurs
    def compare_faces(self, descriptor, known_descriptors, threshold=0.6):
        distances = np.linalg.norm(known_descriptors - descriptor, axis=1)
        min_distance = np.min(distances)
        if min_distance < threshold:
            return True, np.argmin(distances)
        else:
            return False, None

face_recognition = FaceRecognitionSRS()

def process_frame(frame, model, fov):
    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame_rgb)
    except Exception as e:
        print(f"Error processing frame with YOLOv5: {e}")
        return frame, []

    angles = []
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:  # Détecter les personnes uniquement
            center_x = (x1 + x2) / 2
            angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
            angles.append(angle)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"Angle: {angle:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Reconnaissance faciale sur les zones détectées
            face_frame = frame[int(y1):int(y2), int(x1):int(x2)]
            print(f"Processing face frame of shape: {face_frame.shape}")
            face_descriptor = face_recognition.get_face_descriptor(face_frame)
            if face_descriptor is not None:
                print(f"Face descriptor calculated: {face_descriptor}")
                matched, idx = face_recognition.compare_faces(face_descriptor, face_recognition.known_face_descriptors)
                if matched:
                    label = face_recognition.known_labels[idx]
                    cv2.putText(frame, label, (int(x1), int(y2) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Unknown", (int(x1), int(y2) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                print("No face descriptor found")
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
        result, response = Triangulation.get_object_position(4, angles_cam1[0], angles_cam2[0])
        if result:
            map_frame = np.zeros((map_height, map_width, 3), dtype=np.uint8)
            # Redimensionner les positions pour correspondre à la carte
            map_x = int((response[1] / ROOM_WIDTH) * map_width)
            map_y = int((response[0] / ROOM_HEIGHT) * map_height)
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
