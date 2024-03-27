from flask import Flask, jsonify
import cv2
import face_recognition

app = Flask(__name__)

def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces, image

def get_face_encodings(image):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings

@app.route('/faces', methods=['GET'])
def get_faces():
    image_path = 'capture.jpg' 
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    cv2.imwrite(image_path, frame)
    camera.release()

    faces, image = detect_faces(image_path)
    face_encodings = get_face_encodings(image)

    data = []
    for ((x, y, w, h), encoding) in zip(faces, face_encodings):
        face_data = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h),
            'encoding': encoding.tolist()
        }
        data.append(face_data)

    return jsonify({
        'nb_faces': len(faces),
        'faces_data': data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4298)
