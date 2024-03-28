from flask import Flask, jsonify, request, make_response
from functools import wraps
import jwt
import datetime
import cv2
import face_recognition

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dMbgbnTDxK82SE3Bn2XgcMFTqmdLZWn9'

app.config['CLIENT_USERNAME'] = 'SRS-Server'
app.config['CLIENT_PASSWORD'] = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 403
        
        return f(*args, **kwargs)
        
    return decorated

def detect_faces_and_profiles(image):
    face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    profile_cascade = cv2.CascadeClassifier('cascades/haarcascade_profileface.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    profiles = profile_cascade.detectMultiScale(gray, 1.1, 4)
    return faces, profiles, image

def get_face_encodings(image):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings

@app.route('/detect', methods=['GET'])
@token_required
def detect():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    camera.release()
    
    faces, profiles, image = detect_faces_and_profiles(frame)
    faces_encodings = get_face_encodings(image)

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
    auth = request.authorization

    if auth and auth.password == app.config['CLIENT_PASSWORD'] and auth.username == app.config['CLIENT_USERNAME']:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4298)
