"""
Classe ServerResearchWindow

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 09.06.2024

Description :
Cette classe gère la fenêtre de recherche de serveur dans une application Kivy. Elle inclut des méthodes pour
effectuer une analyse du réseau à la recherche d'un serveur spécifique, configurer la connexion au serveur, et
naviguer vers différentes fenêtres en fonction de la configuration du serveur.

Attributs :
- SERVER_PORT : Port utilisé pour la recherche du serveur.
- networkScanner : Instance de la classe NetworkScanner pour effectuer l'analyse du réseau.
- app : Instance de l'application Kivy en cours d'exécution.

Méthodes :
- on_enter : Méthode appelée lorsque l'écran est affiché, démarre l'analyse du réseau.
- retry : Réactive le bouton de réessai et relance l'analyse du réseau.
- run_network_scan : Initialise et planifie l'analyse du réseau.
- async_scan_ips : Exécute l'analyse des IPs en recherchant le serveur et configure la connexion si un serveur est trouvé.

Utilisation :
Cette classe est conçue pour être utilisée dans une application Kivy afin de rechercher et configurer la connexion à un serveur
lors du démarrage ou après une tentative échouée de connexion initiale.
"""

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
        """
        Effectue une analyse asynchrone des IPs sur le réseau pour trouver un serveur SRS.
    
        Args:
            port (int): Le port sur lequel scanner les IPs pour trouver le serveur.
    
        Description:
            Cette méthode utilise la classe NetworkScanner pour analyser les IPs sur le réseau local
            afin de trouver une adresse IP où un serveur SRS est en cours d'exécution sur le port spécifié.
            Si une adresse IP de serveur est trouvée, elle configure l'application avec cette adresse IP
            et crée un client serveur. Ensuite, elle vérifie si le serveur est correctement configuré.
            En fonction du résultat de cette vérification, elle navigue soit vers l'écran de connexion
            soit vers l'écran d'initialisation de connexion. Si aucun serveur n'est trouvé, elle affiche
            un message d'erreur et réactive le bouton de réessai.
    
        Returns:
            None
        """
        ip_serveur = self.networkScanner.scan_ips(port)  # Utilise le scanner de réseau pour trouver l'IP du serveur sur le port spécifié
        self.app = App.get_running_app()  # Récupère l'instance de l'application Kivy en cours d'exécution
    
        if ip_serveur:
            # Si une IP de serveur est trouvée, configure l'application avec cette IP
            self.app.set_server_ip(ip_serveur)
            self.app.set_server_client(ServerClient(ip_serveur))  # Crée un client serveur avec l'IP trouvée
    
            serverClient = ServerClient(ip_serveur)  # Crée une instance de ServerClient
    
            # Vérifie si le serveur est correctement configuré
            if serverClient.is_server_set_up():
                # Si le serveur est configuré, passe à l'écran de connexion
                self.manager.current = "login"
            else:
                # Sinon, passe à l'écran d'initialisation de connexion
                self.manager.current = "initializeLogin"
        else:
            # Si aucune IP de serveur n'est trouvée, affiche un message d'erreur
            self.ids.state_label.text = "Erreur: Aucun serveur SRS trouvé sur votre réseau."
            self.ids.state_label.color = (1, 0, 0, 1)  # Change la couleur du texte en rouge
            self.ids.retry_button.disabled = False  # Active le bouton de réessai
    
        

