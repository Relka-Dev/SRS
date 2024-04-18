from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 

class MainWindow(Screen):     
    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()

