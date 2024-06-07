from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 
import os
import subprocess
from Classes.room import Room

class RoomWindow(Screen):


    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        result, self.cameras = self.server_client.get_cameras()

    def run_angle_camera(self):
        camera_url = f"http://{self.cameras[0].ip}:4298/video?token={self.cameras[0].jwt}"  # Remplacez ceci par l'URL de votre caméra
        self._run_subprocess_script('../srs-proto/single-camera-angle.py', [camera_url])
    
    def run_face_recognition(self):# Remplacez ceci par l'URL de votre caméra
        self._run_subprocess_script('../srs-proto/reconnaissance_faciale.py')

    def run_two_cameras(self):
        camera_url1 = f"http://{self.cameras[0].ip}:4298/video?token={self.cameras[0].jwt}"
        camera_url2 = f"http://{self.cameras[1].ip}:4298/video?token={self.cameras[1].jwt}"
        self._run_subprocess_script('../srs-proto/dual-camera.py', [camera_url1, camera_url2])

    def run_four_cameras(self):
        cameras_urls = []

        for i in range(4):
            cameras_urls.append(f"http://{self.cameras[i+1].ip}:4298/video?token={self.cameras[i+1].jwt}")

        self._run_subprocess_script('../srs-proto/quad-camera.py', cameras_urls)

    def run_spatial_recognition_system(self):
        wall_size = self.ids.size_textInput.text
        room = Room()

        api_link = self.server_client.get_users_link()

        for camera in self.cameras:
            match camera.idWall:
                case 1:
                    room.set_top_left(camera)
                case 2:
                    room.set_top_right(camera)
                case 3:
                    room.set_bottom_left(camera)
                case 4:
                    room.set_bottom_right(camera)

        camera_urls = [
            f"http://{room.get_bottom_left().ip}:4298/video?token={room.get_bottom_left().jwt}",
            f"http://{room.get_bottom_right().ip}:4298/video?token={room.get_bottom_right().jwt}",
            f"http://{room.get_top_right().ip}:4298/video?token={room.get_top_left().jwt}",
            f"http://{room.get_top_left().ip}:4298/video?token={room.get_top_right().jwt}"
        ]
            
        self._run_subprocess_script('../srs-proto/srs-face_recognition.py', camera_urls, wall_size, api_link)

    def _run_subprocess_script(self, script_path, cameras=None, wall_size=None, api_link=None):
        # Construire le chemin absolu pour le script
        abs_script_path = os.path.abspath(script_path)
        
        print(f"Tentative d'exécution du script : {abs_script_path} avec les paramètres : {cameras}")

        file_exists = os.path.exists(abs_script_path)
        
        if file_exists:
            try:
                command = ["python", abs_script_path]
                
                if cameras != None:
                    for i, param in enumerate(cameras):
                        command.extend([f'--camera_url{i+1}', param])
                
                if wall_size != None:
                    command.extend([f'--wall_size', wall_size])
                
                if api_link != None:
                    command.extend([f'--api_link', api_link])

                result = subprocess.run(command, capture_output=True, text=True)
                print(f"Sortie du script : {result.stdout}")
                print(f"Erreurs du script : {result.stderr}")
                

            except Exception as e:
                print(f"Erreur lors de l'exécution du script : {e}")
        else:
            print("Le fichier spécifié n'existe pas.")