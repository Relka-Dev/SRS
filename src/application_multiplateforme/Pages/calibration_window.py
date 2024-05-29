from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

class CalibrationWindow(Screen):

    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        self.api_call_loop = Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        result, camera_data = self.server_client.get_calibration(44)
        
        if result:
            if len(camera_data) > 0 and isinstance(camera_data[0][1][0], list) and len(camera_data[0][1][0]) > 0:
                self.update_label(self.ids.camera1_label, camera_data[0][1][0][0])
            if len(camera_data) > 1 and isinstance(camera_data[1][1][0], list) and len(camera_data[1][1][0]) > 0:
                self.update_label(self.ids.camera2_label, camera_data[1][1][0][0])
            if len(camera_data) > 2 and isinstance(camera_data[2][1][0], list) and len(camera_data[2][1][0]) > 0:
                self.update_label(self.ids.camera3_label, camera_data[2][1][0][0])
            if len(camera_data) > 3 and isinstance(camera_data[3][1][0], list) and len(camera_data[3][1][0]) > 0:
                self.update_label(self.ids.camera4_label, camera_data[3][1][0][0])
    

    def update_label(self, label, value):
        label.text = str(value)
        if -1 <= value <= 1:
            label.color = (0, 1, 0, 1)
        else:
            label.color = (1, 0, 0, 1)
    
    def on_leave(self):
        self.api_call_loop.cancel()