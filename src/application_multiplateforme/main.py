from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.utils import get_color_from_hex

from Pages.main_window import MainWindow
from Pages.server_research_window import ServerResearchWindow
from Pages.initialize_login_window import InitializeLoginWindow
from Pages.add_first_admin_window import AddFirstAdminWindow
from Pages.login_window import LoginWindow
from Pages.navigation_face_management import NavigationFaceManagementWindow
from Pages.add_user_window import AddUserWindow
from Pages.cameras_management_window import CamerasManagementWindow

from Classes.server_client import ServerClient

# Définition du gestionnaire d'écrans
class WindowManager(ScreenManager):
    pass

# Chargement du fichier KV


# Définition de l'application principale
class MyMainApp(App):
    server_ip = None
    server_client = None

    def build(self):

        kv = Builder.load_file("app.kv")

        self.title = 'Système de Reconnaissance Spaciale'

        return kv

    def set_server_ip(self, server_ip : str):
        self.server_ip = server_ip

    def get_server_ip(self):
        return self.server_ip
    
    def set_server_client(self, server_client : ServerClient):
        self.server_client = server_client

    def get_server_client(self):
        return self.server_client

# Point d'entrée de l'application
if __name__ == "__main__":
    # Instancie et exécute l'application
    MyMainApp().run()
