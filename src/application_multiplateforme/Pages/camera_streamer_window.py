import base64
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from PIL import Image
import io
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.clock import Clock

class CameraStreamerWindow(Screen):
    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        self.image_one = self.ids['image_one']
        
        Clock.schedule_interval(self.update_images, 5)  

    def update_images(self, dt):
        result, cameras = self.server_client.get_cameras()

        if result:
            num_cameras = len(cameras)
            if num_cameras > 0:
                self.update_camera_image(cameras[0], self.ids.image_one)
            if num_cameras > 1:
                self.update_camera_image(cameras[1], self.ids.image_two)
            if num_cameras > 2:
                self.update_camera_image(cameras[2], self.ids.image_three)
            if num_cameras > 3:
                self.update_camera_image(cameras[3], self.ids.image_four)

    def update_camera_image(self, camera, element):
        result, image_or_error = self.server_client.get_image_by_camera(camera)
        
        if result:
            element.texture = self.generate_texture(image_or_error)
        else:
            print("error retrieving image")

    def generate_texture(self, image_base64):
        image_data = base64.b64decode(image_base64)
        image_stream = io.BytesIO(image_data)
        pil_image = Image.open(image_stream)
        pil_image = pil_image.convert('RGB')
        buf = pil_image.tobytes()
        img_texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        return img_texture