import face_recognition
import face_recognition_models
import base64
import json


class LibFaceRecognition:
    @staticmethod
    def get_face_encodings(image):
        """
        Récupère les encodages des visages dans une image donnée. Ne peut fonctionner s'il y a qu'une seule personne dans l'image.

        Args:
        image (numpy.ndarray): L'image dans laquelle chercher les visages.

        Returns:
        tuple: Un tuple contenant un booléen indiquant le succès et soit l'encodage du visage en base64, soit un message d'erreur.
        """
        # Récupération de la position des visages
        face_locations = face_recognition.face_locations(image)
        # Récupération des encodages
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if len(face_encodings) == 1:
            # Convertit l'encodage en une liste de flottants puis en une chaîne base64
            encodings_json = json.dumps(face_encodings[0].tolist())
            encodings_base64 = base64.b64encode(encodings_json.encode('utf-8')).decode('utf-8')
            return True, encodings_base64
        elif len(face_encodings) < 1:
            return False, "Aucun visage détecté."
        else:
            return False, "Trop de visages détectés, veuillez vous isoler."
