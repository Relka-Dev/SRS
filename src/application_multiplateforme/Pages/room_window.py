from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
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
        if len(self.cameras) < 1:
            self.show_popup("Erreur", "Pas assez de caméras disponibles.")
            return
        camera_url = f"http://{self.cameras[0].ip}:4298/video?token={self.cameras[0].jwt}"  # Remplacez ceci par l'URL de votre caméra
        self._run_subprocess_script('../srs-proto/single-camera-angle.py', [camera_url])
    
    def run_face_recognition(self):
        if len(self.cameras) < 1:
            self.show_popup("Erreur", "Pas assez de caméras disponibles.")
            return
        self._run_subprocess_script('../srs-proto/reconnaissance_faciale.py')

    def run_two_cameras(self):
        if len(self.cameras) < 2:
            self.show_popup("Erreur", "Pas assez de caméras disponibles.")
            return
        wall_size = self.ids.size_textInput.text

        if not self.is_float(wall_size):
            self.show_popup("Erreur", "La taille du mur doit être un nombre flottant.")
            return

        # Vérifiez si les caméras sont en bas à gauche et en bas à droite
        bottom_left_camera = next((camera for camera in self.cameras if camera.idWall == 3), None)
        bottom_right_camera = next((camera for camera in self.cameras if camera.idWall == 4), None)

        if not bottom_left_camera or not bottom_right_camera:
            self.show_popup("Erreur", "Deux caméras sont nécessaires : une en bas à gauche et une en bas à droite.")
            return
        
        camera_url1 = f"http://{bottom_left_camera.ip}:4298/video?token={bottom_left_camera.jwt}"
        camera_url2 = f"http://{bottom_right_camera.ip}:4298/video?token={bottom_right_camera.jwt}"
        self._run_subprocess_script('../srs-proto/dual-camera.py', [camera_url1, camera_url2], wall_size)

    def run_four_cameras(self):
        if len(self.cameras) < 4:
            self.show_popup("Erreur", "Pas assez de caméras disponibles.")
            return
        wall_size = self.ids.size_textInput.text
        if not self.is_float(wall_size):
            self.show_popup("Erreur", "La taille du mur doit être un nombre flottant.")
            return

        room = Room()

        # Assigner les caméras aux murs correspondants
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

        # Vérifiez si toutes les positions murales sont couvertes
        if not room.get_bottom_left() or not room.get_bottom_right() or not room.get_top_left() or not room.get_top_right():
            self.show_popup("Erreur", "Quatre caméras sont nécessaires : une sur chaque mur.")
            return

        cameras_urls = [
            f"http://{room.get_bottom_left().ip}:4298/video?token={room.get_bottom_left().jwt}",
            f"http://{room.get_bottom_right().ip}:4298/video?token={room.get_bottom_right().jwt}",
            f"http://{room.get_top_left().ip}:4298/video?token={room.get_top_left().jwt}",
            f"http://{room.get_top_right().ip}:4298/video?token={room.get_top_right().jwt}"
        ]

        self._run_subprocess_script('../srs-proto/quad-camera.py', cameras_urls, wall_size)

    def run_spatial_recognition_system(self):
        if len(self.cameras) < 4:
            self.show_popup("Erreur", "Pas assez de caméras disponibles.")
            return
        wall_size = self.ids.size_textInput.text
        if not self.is_float(wall_size):
            self.show_popup("Erreur", "La taille du mur doit être un nombre flottant.")
            return

        room = Room()

        api_link = self.server_client.get_users_link()

        # Assigner les caméras aux murs correspondants
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

        # Vérifiez si toutes les positions murales sont couvertes
        if not room.get_bottom_left() or not room.get_bottom_right() or not room.get_top_left() or not room.get_top_right():
            self.show_popup("Erreur", "Quatre caméras sont nécessaires : une sur chaque mur.")
            return

        camera_urls = [
            f"http://{room.get_bottom_left().ip}:4298/video?token={room.get_bottom_left().jwt}",
            f"http://{room.get_bottom_right().ip}:4298/video?token={room.get_bottom_right().jwt}",
            f"http://{room.get_top_left().ip}:4298/video?token={room.get_top_left().jwt}",
            f"http://{room.get_top_right().ip}:4298/video?token={room.get_top_right().jwt}"
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

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
