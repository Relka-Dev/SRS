"""
Auteur      : Karel Vilém Svoboda
Affiliation : CFPTi - SRS
Date        : 28.03.2024

Script      : app.py
Description : Code pour les cameras Wifi du projet SRS
Version     : 0.1
"""

from flask import Flask, jsonify, request, make_response
from functools import wraps
import jwt
import datetime
import cv2
import face_recognition
import multiprocessing
from multiprocessing import Process, Queue


app = Flask(__name__)

# Constantes de l'application Flask
app.config['SECRET_KEY'] = 'dMbgbnTDxK82SE3Bn2XgcMFTqmdLZWn9'
app.config['CLIENT_USERNAME'] = 'SRS-Server'
app.config['CLIENT_PASSWORD'] = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'

class Detection:
    """
    Librairie contenant les fonctions liées à la détection.
    """
    @staticmethod
    def detect_faces_and_profiles(image):
        """
        Permet de détecter les faces et profiles

        Args:
            image: L'image à analyser pour détecter les profils et faces

        Returns:
            faces: Tableau contenant les coordonées et tailles des faces
            profiles: Tableau contenant les coordonées et tailles des profiles
        """
        face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
        profile_cascade = cv2.CascadeClassifier('cascades/haarcascade_profileface.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        profiles = profile_cascade.detectMultiScale(gray, 1.1, 4)
        return faces, profiles
    
    @staticmethod
    def get_face_encodings(image):
        """
        Récupère les données faciales de la personne dans l'image

        Args:
            image: L'image à analyser avec les faces

        Returns:
            face_encodings : Données des visages
        """
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        return face_encodings

def token_required(f):
    """
    Fonction décoratrice permettant de forcer une autre fonction d'être identifié par JWT

    Args:
        f : Fonction à décorer
    
    Returns:
        f : Fonction décorée
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing'}), 403
        # Try catch car jwt.decode retourne une erreur en cas de non correspondance
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)

    return decorated

def detect_worker(image, result_queue):
    """
    Fonction asychrone
    Récupères les données dans l'image (Faces et profiles)

    Args:
        image: image à analyser
        result_queue (Queue): Queue des contenant les résultats des autres instances de la fonction
    """
    faces, profiles = Detection.detect_faces_and_profiles(image)
    faces_encodings = Detection.get_face_encodings(image)
    result_data = (faces, profiles, faces_encodings)
    result_queue.put(result_data)

@app.route('/detect', methods=['GET'])
@token_required
def detect():
    """
    Route permettant d'avoir les information sur les personnes présentes dans la vue de la camera

    Returns:
        Json: Résultat de l'interprétation de l'image
    """
    # CAP_V4L2 permet d'éviter une erreur
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    ret, frame = camera.read()
    camera.release()

    if ret:
        result_queue = Queue()
        process = Process(target=detect_worker, args=(frame, result_queue))
        process.start()
        process.join()

        faces, profiles, faces_encodings = result_queue.get()

    faces_data = []
    for ((x, y, w, h), encoding) in zip(faces, faces_encodings):
        face_data = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h),
            'encoding': encoding.tolist()
        }
        faces_data.append(face_data)
    
    profiles_data = []
    for (x, y, w, h) in profiles:
        profile_info = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h)
        }
        profiles_data.append(profile_info)

    return jsonify({
        'nb_faces': len(faces),
        'faces_data': faces_data,
        'nb_profiles': len(profiles),
        'profiles_data': profiles_data
    })

@app.route('/login')
def login():
    """
    Route permettant à se connecter

    Returns:
        str: JWT généré
    """
    auth = request.authorization

    if auth and auth.password == app.config['CLIENT_PASSWORD'] and auth.username == app.config['CLIENT_USERNAME']:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4298)