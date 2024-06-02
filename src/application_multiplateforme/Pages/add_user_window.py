import cv2
import numpy as np
from PIL import Image as PILImage
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 

from Classes.lib_face_recognition import LibFaceRecognition

class ClickableImage(ButtonBehavior, Image):
    pass

class AddUserWindow(Screen):   
    capture = None  
    personTypes = []
    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        self.ids.qrcam.play = True
        self.get_person_types()
        

    def get_person_types(self):
        result, response = self.server_client.get_person_types()

        if result:
            for data in response:
                self.personTypes.append(data[1])
                self.ids.function_spinner.values = self.personTypes
            return True, response
        else:
            return False, response

    def camera_button_pressed(self):
        self.ids.qrcam.play = not self.ids.qrcam.play

        if self.ids.qrcam.play:
            self.ids.camera_button.text = "Prendre une photo"
        else:
            self.ids.camera_button.text = "Reprendre une photo"
    
    def get_picture(self):
        image_texture = self.ids.qrcam.texture
        pixels = image_texture.pixels
        image = PILImage.frombytes('RGBA', (640, 480), pixels, 'raw')
        pixels_array = np.array(image)
        image_bgr = cv2.cvtColor(pixels_array, cv2.COLOR_RGBA2BGR)

        return image_bgr

            
    def enable_add_button(self):
        username = self.ids.username_textInput.text.strip()
        function_selected = self.ids.function_spinner.text != "Sélectionnez une fonction"
        
        if username and function_selected and not self.ids.qrcam.play:
            self.ids.add_user_button.disabled = False
        else:
            self.ids.add_user_button.disabled = True
    
    def add_user_button_pressed(self):

        result_function, id_function = self.server_client.get_person_types_by_name(self.ids.function_spinner.text)

        result_encodings, face_encodings = LibFaceRecognition.get_face_encodings(self.get_picture())

        username = self.ids.username_textInput.text
        
        if result_function and result_encodings:
            result, response = self.server_client.add_user(username, id_function, face_encodings)
            print(response)




