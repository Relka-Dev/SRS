from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from Pages.main_window import MainWindow
from Pages.server_research_window import ServerResearchWindow
from Pages.initialize_login_window import InitializeLoginWindow

# Définition du gestionnaire d'écrans
class WindowManager(ScreenManager):
    pass

# Chargement du fichier KV
kv = Builder.load_file("app.kv")

# Définition de l'application principale
class MyMainApp(App):
    server_ip = None

    def build(self):
        # Retourne l'interface utilisateur chargée à partir du fichier app.kv
        return kv

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip

    def get_server_ip(self):
        return self.server_ip

# Point d'entrée de l'application
if __name__ == "__main__":
    # Instancie et exécute l'application
    MyMainApp().run()
