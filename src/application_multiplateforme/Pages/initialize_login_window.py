from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 

class InitializeLoginWindow(Screen):
    server_ip = None

    def on_enter(self):
        self.app = App.get_running_app()
        self.server_ip = self.app.get_server_ip()