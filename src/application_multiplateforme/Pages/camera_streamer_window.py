import io
import requests
import imageio
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen 
from threading import Thread
from kivy.clock import Clock

class CameraStreamerWindow(Screen):
    def on_enter(self):
        super().on_enter()
        self.server_url = 'http://192.168.1.131:4298/video?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiU1JTLVNlcnZlciIsImV4cCI6MTcxNDQ3NjIyMH0.63zb0fjHPFmUtKttnOE3m2uqmQoQVDPm-2YFhZ7BFDY'


        self.video_image = self.ids['video_image']

        self.is_fetching_stream = False

        self.start_fetching_stream()

    def fetch_stream(self):
        """
        Fonction pour récupérer et afficher la vidéo en streaming depuis l'URL donnée.
        """
        try:
            self.is_fetching_stream = True
            response = requests.get(self.server_url, stream=True)
            if response.status_code == 200:
                bytes_stream = bytes()
                for chunk in response.iter_content(chunk_size=1024):
                    bytes_stream += chunk
                    a = bytes_stream.find(b'\xff\xd8')
                    b = bytes_stream.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = bytes_stream[a:b+2]
                        bytes_stream = bytes_stream[b+2:]
                        # Conversion du flux en une image Kivy
                        texture = Texture.create(size=(self.video_image.width, self.video_image.height))
                        texture.blit_buffer(jpg, colorfmt='rgb', bufferfmt='ubyte')
                        # Planifier la mise à jour de l'image dans le thread principal
                        Clock.schedule_once(lambda dt: self.update_video_image(texture))
                        if not self.is_fetching_stream:
                            break
            else:
                print("Error fetching stream - HTTP Status Code:", response.status_code)
        except Exception as e:
            print("Error fetching stream:", e)

    def update_video_image(self, texture):
        """
        Met à jour l'élément d'image avec la texture dans le thread principal.
        """
        def update_image(dt):
            self.video_image.texture = texture
            self.video_image.canvas.ask_update()

        Clock.schedule_once(update_image)

    def start_fetching_stream(self):
        """
        Fonction pour démarrer la récupération de la vidéo en streaming dans un thread séparé.
        """
        if not self.is_fetching_stream:
            self.is_fetching_stream = True
            Thread(target=self.fetch_stream).start()

    def stop_fetching_stream(self):
        """
        Fonction pour arrêter la récupération de la vidéo en streaming.
        """
        self.is_fetching_stream = False


