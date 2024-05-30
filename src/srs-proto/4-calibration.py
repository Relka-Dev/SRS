import cv2
import torch
import numpy as np

# Configuration
CAMERA_URLS = [
    "http://192.168.1.115:4298/video",
    "http://192.168.1.121:4298/video",
    "http://192.168.1.114:4298/video",
    "http://192.168.1.118:4298/video"
]

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
    return angles

map_width, map_height = 600, 600

while True:
    # Lire les frames des deux caméras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()
    ret4, frame4 = cap4.read()

    # Si une des captures échoue, on sort de la boucle
    if not ret1 or not ret2:
        print("Erreur : Impossible de lire une frame des flux vidéo")
        break

    frame1 = cv2.flip(cv2.flip(frame1, 0), 1)
    frame2 = cv2.flip(cv2.flip(frame2, 0), 1)
    frame3 = cv2.flip(cv2.flip(frame3, 0), 1)
    frame4 = cv2.flip(cv2.flip(frame4, 0), 1)

    # Traiter les frames pour détecter les personnes et calculer les angles
    angles_cam1 = process_frame(frame1, model, CAMERA_FOV)
    angles_cam2 = process_frame(frame2, model, CAMERA_FOV)
    angles_cam3 = process_frame(frame3, model, CAMERA_FOV)
    angles_cam4 = process_frame(frame4, model, CAMERA_FOV)

    if len(angles_cam2) >= 1 and len(angles_cam1) >= 1 and len(angles_cam3) >= 1 and len(angles_cam4) >= 1:
        print('-----------')
        print("Sud Ouest : " + str(angles_cam1))
        print("Sud Est : " + str(angles_cam2))
        print("Nord Ouest : " + str(angles_cam3))
        print("Nord Est : " + str(angles_cam4))
        

    # Appuyer sur 'q' pour quitter les fenêtres
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les captures vidéo et fermer les fenêtres
cap1.release()
cap2.release()
cv2.destroyAllWindows()
