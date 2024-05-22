import face_recognition
import cv2

# Charger une image de test
image = face_recognition.load_image_file("karel.jpg")  # Remplacez par le chemin vers votre photo

# Détecter les visages
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

print("Number of faces detected:", len(face_locations))
for face_encoding in face_encodings:
    print("Face encoding:", face_encoding)
