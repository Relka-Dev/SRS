from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen 
import threading

from Classes.camera import Camera

class CamerasManagementWindow(Screen):
    walls = []
    cameras = []

    TEXT_NO_CAMERA_FOUND = "Aucune camera trouvée sur votre réseau"
    TEXT_CAMERA_FOUND = "Veuillez séléctionner une camera"
    TEXT_LOADING_CAMERA = "Recherche des cameras en cours..."

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
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_NO_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
            else:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', cameras_ips))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', False))
        
        self.ids.update_cameras_list_button.disabled = False
        
    def camera_changed(self, input_text):
        self.change_all_view_input_state(not (input_text != self.TEXT_NO_CAMERA_FOUND and input_text != self.TEXT_CAMERA_FOUND and input_text != self.TEXT_LOADING_CAMERA))

    def change_all_view_input_state(self, viewDisabled : bool):
        self.ids.cameras_spinner.disabled = viewDisabled
        self.ids.update_cameras_list_button.disabled = viewDisabled
        self.ids.position_slider.disabled = viewDisabled
        self.ids.walls_spinner.disabled = viewDisabled
        self.ids.update_camera_button.disabled = viewDisabled
    

    def update_cameras_list(self):
        self.change_all_view_input_state(True)
        Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_LOADING_CAMERA))
        self.ask_camera_update_thread = threading.Thread(target=self.ask_camera_update)
        self.ask_camera_update_thread.start()
        
    
    def ask_camera_update(self):
        result, response = self.server_client.update_camera_list()

        print(response)
        
        cameras_ips = []
        if result:
            for camera in response:
                cameras_ips.append(str(camera.ip))

            if len(cameras_ips) < 1:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', []))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_NO_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
            else:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', cameras_ips))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', False))
        
        self.ids.update_cameras_list_button.disabled = False

    def update_camera(self):
        pass