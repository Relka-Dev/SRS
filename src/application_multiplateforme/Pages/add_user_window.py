import cv2
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 

class ClickableImage(ButtonBehavior, Image):
    pass

class AddUserWindow(Screen):   
    capture = None  
    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        self.ids.qrcam.play = True

    def camera_button_pressed(self):
        self.ids.qrcam.play = not self.ids.qrcam.play

        if self.ids.qrcam.play:
            self.ids.camera_button.text = "Prendre une photo"
        else:
            self.ids.camera_button.text = "Reprendre une photo"
    
    def get_picture(self):
        image_texture = self.qrcam.texture
        pixels = image_texture.pixels

        # Convertir les pixels en tableau numpy
        pixels_array = np.array(pixels)

        # Remodeler le tableau numpy pour obtenir une image avec les dimensions appropriées
        image = pixels_array.reshape((480, 640, 4)) 

        # Convertir l'image en format BGR (utilisé par OpenCV)
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        return image_bgr
            
