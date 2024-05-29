from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen 
import threading

from Classes.camera import Camera
from Classes.wall import Wall

class CamerasManagementWindow(Screen):
    walls = []
    cameras = []
    selected_camera = None
    selected_wall = None

    TEXT_NO_CAMERA_FOUND = "Aucune camera trouvée sur votre réseau"
    TEXT_CAMERA_FOUND = "Veuillez séléctionner une camera"
    TEXT_LOADING_CAMERA = "Recherche des cameras en cours..."

    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        self.get_walls_thread = threading.Thread(target=self.get_walls)
        self.get_walls_thread.start()
        self.ask_camera_update()
        self.get_cameras_thread = threading.Thread(target=self.get_cameras)
        self.get_cameras_thread.start()
        

    def get_walls(self):
        result, response = self.server_client.get_walls()

        if result:
            self.walls = response
            wall_names = [wall.wallName for wall in self.walls]
            Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'values', wall_names))
        else:
            Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'values', []))
            Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'text', "Aucun mur trouvé"))
            Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'disabled', True))
    
    def get_cameras(self):
        result, response = self.server_client.get_cameras()

        camera_details = []
        if result:
            self.cameras = response
            for camera in response:
                display_text = f"IP: {camera.ip} - Wall: {camera.idWall}"
                camera_details.append(display_text)

            if not camera_details:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', []))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_NO_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
            else:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', camera_details))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', False))
        else:
            Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', []))
            Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_NO_CAMERA_FOUND))
            Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
        
        self.ids.update_cameras_list_button.disabled = False

    def wall_changed(self, wall_name):
        selected_wall = next((wall for wall in self.walls if wall.wallName == wall_name), None)
        if selected_wall:
            self.selected_wall = selected_wall
            print(f"Selected wall: {self.selected_wall.wallName}")
        else:
            self.selected_wall = None
            print("No wall matched the selection or no wall selected.")

    def get_wall_names(self):
        return [wall.wallName for wall in self.walls]


        
    def camera_changed(self, input_text):
        if input_text in [self.TEXT_NO_CAMERA_FOUND, self.TEXT_CAMERA_FOUND, self.TEXT_LOADING_CAMERA]:
          self.change_all_view_input_state(True)
        else:
          self.change_all_view_input_state(False)
          camera_ip = input_text.split(" - ")[0].replace("IP: ", "").strip()

          for camera in self.cameras:
              if camera.ip == camera_ip:
                  self.selected_camera = camera
                  break
               
          if self.selected_camera:

              # Update wall selection based on the selected camera's wall ID
              matching_wall = next((wall for wall in self.walls if wall.idWall == self.selected_camera.idWall), None)
              if matching_wall:
                  self.selected_wall = matching_wall
                  self.ids.walls_spinner.text = matching_wall.wallName
              else:
                  print("No matching wall found for the selected camera.")


    def change_all_view_input_state(self, viewDisabled : bool):
        self.ids.cameras_spinner.disabled = viewDisabled
        self.ids.walls_spinner.disabled = viewDisabled
        self.ids.update_camera_button.disabled = viewDisabled
    

    def update_cameras_list(self):
        self.change_all_view_input_state(True)
        self.ids.update_cameras_list_button.disabled = True
        Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_LOADING_CAMERA))
        self.ask_camera_update_thread = threading.Thread(target=self.ask_camera_update)
        self.ask_camera_update_thread.start()
        
    
    def ask_camera_update(self):
        result, response = self.server_client.update_camera_list()
        camera_details = []
        if result:
            self.cameras = response
            for camera in response:
                display_text = f"IP: {camera.ip} - Wall: {camera.idWall}"
                camera_details.append(display_text)

            if not camera_details:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', []))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_NO_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
            else:
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', camera_details))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', False))
        else:
            Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', []))
            Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_NO_CAMERA_FOUND))
            Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
        
        self.ids.update_cameras_list_button.disabled = False

    def update_camera(self):
        if self.selected_camera and self.selected_wall:
            idCamera = self.selected_camera.idCamera
            idNetwork = self.selected_camera.idNetwork
            idWall = self.selected_wall.idWall

            result, response = self.server_client.update_camera(idCamera, idNetwork, idWall)
            
            if result:
                self.ids.status_label.text = str(response['message'])
                print("Camera updated successfully:", response)
            else:
                self.ids.status_label.text = str(response)
                print("Failed to update camera:", response)
            
            self.ask_camera_update_thread = threading.Thread(target=self.ask_camera_update)
            self.ask_camera_update_thread.start()
        else:
            print("No camera or wall selected. Please select both before updating.")

