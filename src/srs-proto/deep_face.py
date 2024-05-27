import cv2
from deepface import DeepFace
import os

# Chemin du dossier contenant les images des visages connus
known_faces_dir = 'faces'

# Charger les images des visages connus et extraire les représentations
known_faces = []
for filename in os.listdir(known_faces_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        img_path = os.path.join(known_faces_dir, filename)
        try:
            faces = DeepFace.extract_faces(img_path, enforce_detection=False)
            for face in faces:
                if 'embedding' in face:
                    known_faces.append({
                        'name': os.path.splitext(filename)[0],
                        'representation': face['embedding']
                    })
        except Exception as e:
            print(f"Erreur lors du traitement de l'image {filename}: {e}")

# Fonction pour identifier un visage
def identify_face(face_img):
    if not known_faces:
        return "Inconnu"
    
    # Extraire la représentation du visage
    try:
        face_repr = DeepFace.represent(face_img, enforce_detection=False)
        if face_repr and 'embedding' in face_repr[0]:
            face_repr = face_repr[0]['embedding']
            # Comparer avec les visages connus
            for known_face in known_faces:
                result = DeepFace.verify(face_img, known_face['representation'], model_name='VGG-Face', enforce_detection=False)
                if result['verified']:
                    print(f"Visage identifié: {known_face['name']}")
                    return known_face['name']
    except Exception as e:
        print(f"Erreur lors de l'identification du visage: {e}")
    
    return "Inconnu"

# Capturer le flux vidéo de la caméra
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    try:
        # Détecter les visages dans le cadre
        faces = DeepFace.extract_faces(frame, enforce_detection=False)
        
        if faces:
            for face in faces:
                if 'face' in face and 'facial_area' in face:
                    face_img = face['face']
                    region = face['facial_area']
                    
                    # Identifier le visage
                    name = identify_face(face_img)
                    
                    # Dessiner un rectangle autour du visage
                    (x, y, w, h) = region['x'], region['y'], region['w'], region['h']
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                else:
                    print("Clés 'face' ou 'facial_area' manquantes dans la détection des visages.")
    except Exception as e:
        print(f"Erreur lors de la détection des visages: {e}")
    
    # Afficher le flux vidéo
    cv2.imshow('Camera', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
