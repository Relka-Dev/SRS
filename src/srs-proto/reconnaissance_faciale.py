import cv2
import dlib
import os
import numpy as np

class FaceRecognitionSRS:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
        self.known_face_descriptors, self.known_labels = self.load_faces('faces')

    # Fonction pour extraire les descripteurs de visage
    def get_face_descriptor(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if len(faces) == 0:
            return None

        shape = self.predictor(gray, faces[0])
        face_descriptor = self.face_rec_model.compute_face_descriptor(img, shape)
        return np.array(face_descriptor)

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

def main():
    # Initialisation de l'instance de reconnaissance faciale
    recognizer = FaceRecognitionSRS()

    # Capture vidéo en temps réel
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensionnement pour accélérer le traitement
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Obtenir le descripteur de visage pour la frame actuelle
        descriptor = recognizer.get_face_descriptor(small_frame)

        if descriptor is not None:
            match, index = recognizer.compare_faces(descriptor, recognizer.known_face_descriptors)
            if match:
                label = recognizer.known_labels[index]
            else:
                label = 'Inconnu'

            # Affichage de l'étiquette sur la frame
            faces = recognizer.detector(cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY))
            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(frame, (x*2, y*2), ((x+w)*2, (y+h)*2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x*2, y*2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
