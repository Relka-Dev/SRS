from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen 
import threading

from Classes.camera import Camera

class CamerasManagementWindow(Screen):
    walls = []
    cameras = []

    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        self.get_walls_thread = threading.Thread(target=self.get_walls)
        self.get_walls_thread.start()
        self.get_cameras_thread = threading.Thread(target=self.get_cameras)
        self.get_cameras_thread.start()
    
    def get_walls(self):
        result, response = self.server_client.get_walls()

        if result:
            for data in response:
                self.walls.append(data[1])
            Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'values', self.walls))
    
    def get_cameras(self):
        result, response = self.server_client.get_cameras()
        
        cameras_ips = []
        if result:
            for camera in response:
                cameras_ips.append(str(camera.ip))

            if len(cameras_ips) < 1:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', []))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', "Aucune camera trouvée sur votre réseau"))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
            else:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', cameras_ips))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', "Veuillez séléctionner une camera"))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', False))
        
    def camera_changed(self):
        pass
