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
        result, cameras_angles = self.server_client.get_calibration(44)
        
        if result:
            if len(cameras_angles) > 0:
                self.update_label(self.ids.camera1_data_label, list(cameras_angles[0].values())[0])
                self.ids.camera1_name_label.text = list(cameras_angles[0].keys())[0]
            if len(cameras_angles) > 1:
                self.update_label(self.ids.camera2_data_label, list(cameras_angles[1].values())[0])
                self.ids.camera2_name_label.text = list(cameras_angles[1].keys())[0]
            if len(cameras_angles) > 2:
                self.update_label(self.ids.camera3_data_label, list(cameras_angles[2].values())[0])
                self.ids.camera3_name_label.text = list(cameras_angles[2].keys())[0]
            if len(cameras_angles) > 3:
                self.update_label(self.ids.camera4_data_label, list(cameras_angles[3].values())[0])
                self.ids.camera4_name_label.text = list(cameras_angles[3].keys())[0]
    

    def update_label(self, label, values):
        if (len(values) > 0):
            value = values[0]
            label.text = str(value)
            if -1 <= value <= 1:
                label.color = (0, 1, 0, 1)
            else:
                label.color = (1, 0, 0, 1)
    
    def on_leave(self):
        self.api_call_loop.cancel()