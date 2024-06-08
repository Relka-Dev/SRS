"""
Auteur      : Karel Vilém Svoboda
Affiliation : CFPTi - SRS
Date        : 08.06.2024

Script      : app.py
Description : Code pour les cameras Wifi du projet SRS
Version     : 1.0
"""

from flask import Flask, jsonify, request, make_response, Response
from functools import wraps
import jwt
import datetime
import uuid
import cv2


app = Flask(__name__)

# Constantes de l'application Flask
app.config['SECRET_KEY'] = 'dMbgbnTDxK82SE3Bn2XgcMFTqmdLZWn9'
app.config['CLIENT_USERNAME'] = 'SRS-Server'
app.config['CLIENT_PASSWORD'] = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'

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

@app.route('/ping', methods=['GET'])
@token_required
def ping():
    """
    Retourne l'adresse mac du serveur

    Returns:
        Dictionary: 'Mac Adress' : Mac adress
    """
    return jsonify({'Mac address' : hex(uuid.getnode())}), 200

def gen_frames():
    """
    Capture des images de la caméra en temps réel et les génère en tant que flux de trames JPEG.

    Cette fonction utilise OpenCV pour accéder à la caméra par défaut (index 0) et capture en continu
    les images de la caméra. Chaque image capturée est encodée au format JPEG et envoyée sous forme de
    flux de trames pouvant être utilisé pour le streaming vidéo via un serveur HTTP.

    Le flux de trames est renvoyé dans un format multipart, où chaque trame est précédée par les en-têtes
    HTTP appropriés.

    Yield:
        bytes: Trames d'images encodées en JPEG avec les en-têtes HTTP pour le streaming vidéo.

    Raises:
        RuntimeError: Si la caméra ne peut pas être lue correctement.
    """
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/video')
@token_required
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image')
@token_required
def image():
    """
    Route qui retourne une image capturée de la caméra.
    """
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    camera.release()
    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        return Response(buffer.tobytes(), mimetype='image/jpeg')
    else:
        return jsonify({'message': 'Failed to capture image'}), 500


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
