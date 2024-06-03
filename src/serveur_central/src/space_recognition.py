import cv2
import torch
import numpy as np

class SpaceRecognition:

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(self.device)

    
    def _detect_people(self, image):
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        results = results.pandas().xyxy[0]
        people = results[results['name'] == 'person']
        return people
    
    def get_persons_angles(self, frame, fov):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        angles = []
        for det in results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2, conf, cls = det
            if cls == 0:
                center_x = (x1 + x2) / 2
                angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
                angles.append(angle)
        return angles
    
    def get_persons_angles_with_size(self, frame, fov):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        angles_and_sizes = []
        for det in results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2, conf, cls = det
            if cls == 0:
                center_x = (x1 + x2) / 2
                angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
                size_y = y2 - y1
                angles_and_sizes.append((angle, size_y))
        return angles_and_sizes

    
    def get_people_positions_x(self, imageBase64):
        nparr = np.frombuffer(imageBase64, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detections = self._detect_people(image)

        people_positions = []

        for index, row in detections.iterrows():
            x_center = (row['xmin'] + row['xmax']) / 2
            width = image.shape[1]
            normalized_x_position = (x_center / width) * 100
            people_positions.append(normalized_x_position)

        return people_positions
