from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

class CalibrationWindow(Screen):

    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        self.api_call_loop = Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        result, cameras_angles = self.server_client.get_calibration()
        sizes = []
    
        if result:
            if len(cameras_angles) > 0:
                camera1_data = cameras_angles[0]
                camera1_ip = camera1_data['camera_ip']
                camera1_angles_and_sizes = camera1_data['angles_and_sizes']
                angles1 = [item['angle'] for item in camera1_angles_and_sizes]
                size1 = camera1_angles_and_sizes[0]['size_y'] if camera1_angles_and_sizes else 0
                sizes.append(size1)
                self.update_angle_label(self.ids.camera1_data_label, angles1)
                self.update_size_label(self.ids.camera1_size_label, size1)
                self.ids.camera1_name_label.text = f"Camera : {camera1_ip}"
            if len(cameras_angles) > 1:
                camera2_data = cameras_angles[1]
                camera2_ip = camera2_data['camera_ip']
                camera2_angles_and_sizes = camera2_data['angles_and_sizes']
                angles2 = [item['angle'] for item in camera2_angles_and_sizes]
                size2 = camera2_angles_and_sizes[0]['size_y'] if camera2_angles_and_sizes else 0
                sizes.append(size2)
                self.update_angle_label(self.ids.camera2_data_label, angles2)
                self.update_size_label(self.ids.camera2_size_label, size2)
                self.ids.camera2_name_label.text = f"Camera : {camera2_ip}"
            if len(cameras_angles) > 2:
                camera3_data = cameras_angles[2]
                camera3_ip = camera3_data['camera_ip']
                camera3_angles_and_sizes = camera3_data['angles_and_sizes']
                angles3 = [item['angle'] for item in camera3_angles_and_sizes]
                size3 = camera3_angles_and_sizes[0]['size_y'] if camera3_angles_and_sizes else 0
                sizes.append(size3)
                self.update_angle_label(self.ids.camera3_data_label, angles3)
                self.update_size_label(self.ids.camera3_size_label, size3)
                self.ids.camera3_name_label.text = f"Camera : {camera3_ip}"
            if len(cameras_angles) > 3:
                camera4_data = cameras_angles[3]
                camera4_ip = camera4_data['camera_ip']
                camera4_angles_and_sizes = camera4_data['angles_and_sizes']
                angles4 = [item['angle'] for item in camera4_angles_and_sizes]
                size4 = camera4_angles_and_sizes[0]['size_y'] if camera4_angles_and_sizes else 0
                sizes.append(size4)
                self.update_angle_label(self.ids.camera4_data_label, angles4)
                self.update_size_label(self.ids.camera4_size_label, size4)
                self.ids.camera4_name_label.text = f"Camera : {camera4_ip}"
    
            if sizes:
                average_size = sum(sizes) / len(sizes)
                self.update_average_size_label(self.ids.average_size_label, average_size)
                self.update_label_colors([self.ids.camera1_size_label, self.ids.camera2_size_label, self.ids.camera3_size_label, self.ids.camera4_size_label], sizes, average_size)
    
    def update_angle_label(self, label, values):
        if values:
            value = values[0]
            label.text = str(value)
            if -1 <= value <= 1:
                label.color = (0, 1, 0, 1)
            else:
                label.color = (1, 0, 0, 1)
    
    def update_size_label(self, label, size):
        label.text = f"Size: {size:.2f}"
    
    def update_average_size_label(self, label, average_size):
        label.text = f"Average Size Y: {average_size:.2f}"
    
    def update_label_colors(self, labels, sizes, average_size):
        for label, size in zip(labels, sizes):
            if abs(size - average_size) > 20:
                label.color = (1, 0, 0, 1)
            else:
                label.color = (0, 1, 0, 1)
    
    def on_leave(self):
        self.api_call_loop.cancel()