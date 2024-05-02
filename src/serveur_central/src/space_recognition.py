import cv2
import torch
import numpy as np

class SpaceRecognition:

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    
    def _detect_people(self, image):
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        results = results.pandas().xyxy[0]
        people = results[results['name'] == 'person']
        return people


    def get_people_positions_x(self, imageBase64):
        nparr = np.frombuffer(imageBase64, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        detections = self._detect_people(image)

        people_positions = []

        for index, row in detections.iterrows():
            x_center = (row['xmin'] + row['xmax']) / 2
            width = image.shape[1]
            normalized_x_position = (x_center / width) * 100  # En pourcentage
            people_positions.append(normalized_x_position)

        return people_positions
