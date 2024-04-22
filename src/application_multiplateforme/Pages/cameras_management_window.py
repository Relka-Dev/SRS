from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 

class CamerasManagementWindow(Screen):
    walls = []

    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        print(self.get_walls())
    
    def get_walls(self):
        result, response = self.server_client.get_walls()

        if result:
            for data in response:
                self.walls.append(data[1])
                self.ids.walls_spinner.values = self.walls
            return True, response
        else:
            return False, response