from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.clock import Clock
from Classes.network_scanner import NetworkScanner
from Classes.server_client import ServerClient

class ServerResearchWindow(Screen):     
    SERVER_PORT = 4299

    def on_enter(self):
        Clock.schedule_once(self.run_network_scan)
        

    def retry(self):
        self.ids.retry_button.disabled = True
        self.ids.state_label.text = "Recherche en cours"
        self.ids.state_label.color = (1, 1, 1, 1) 
        self.run_network_scan(None)
 
    def run_network_scan(self, dt):
        self.networkScanner = NetworkScanner()
        Clock.schedule_once(lambda dt: self.async_scan_ips(self.SERVER_PORT), 0)

    def async_scan_ips(self, port):
        ip_serveur = self.networkScanner.scan_ips(port)
        self.app = App.get_running_app()

        if ip_serveur:
            self.app.set_server_ip(ip_serveur)

            serverClient = ServerClient(ip_serveur)

            if serverClient.is_server_set_up():
                self.manager.current = "main"
            else:
                self.manager.current = "initializeLogin"
        else:
            self.ids.state_label.text = "Erreur: Aucun serveur SRS trouvé sur votre réseau."
            self.ids.state_label.color = (1, 0, 0, 1) 
            self.ids.retry_button.disabled = False
        

