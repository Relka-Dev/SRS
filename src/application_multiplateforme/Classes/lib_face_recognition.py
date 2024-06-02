import face_recognition
import face_recognition_models
import base64
import json


class LibFaceRecognition:
    @staticmethod
    def get_face_encodings(image):
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if len(face_encodings) == 1:
            # Convert the encodings to a list of floats and then to a base64 string
            encodings_json = json.dumps(face_encodings[0].tolist())
            encodings_base64 = base64.b64encode(encodings_json.encode('utf-8')).decode('utf-8')
            return True, encodings_base64
        elif len(face_encodings) < 1:
            return False, "Aucun visage détecté."
        else:
            return False, "Trop de visages détectés, veuillez vous isoler."
