import socket
import ipaddress
import socket

from Classes.server_client import ServerClient

class NetworkScanner:
    def __init__(self, network=None):
        if network is None:
            self.network = ipaddress.IPv4Network(self.get_local_network())
        else:
            self.network = ipaddress.IPv4Network(network)

    def scan_ips(self, port,  timeout=0.01):
        """
        Scanne les adresses IP du réseau pour un port spécifié et vérifie la connectivité au serveur SRS.
    
        Args:
        port (int): Le numéro de port à vérifier sur chaque adresse IP.
        timeout (float): Le délai d'attente pour chaque vérification de port, par défaut 0.01 seconde.
    
        Returns:
        str or list: Si aucune adresse IP n'a le port ouvert ou n'est pas connectée au serveur SRS, une liste vide est renvoyée.
                     Sinon, la première adresse IP ayant le port ouvert et connectée au serveur SRS est renvoyée.
        """
        ip_with_port_open = []
        for ip in self.network.hosts():
            if self.check_port(ip, port, timeout):
                if ServerClient(ip).ping_srs_server():
                    ip_with_port_open.append(str(ip))

        if len(ip_with_port_open) == 0:
            return ip_with_port_open
        return ip_with_port_open[0]

    def check_port(self, ip, port, timeout):
        """
        Vérifie si un port spécifié sur une adresse IP donnée est ouvert.

        Args:
            ip (str): L'adresse IP à tester.
            port (int): Le numéro de port à vérifier.
            timeout (float): Le temps maximum en secondes à attendre pour une réponse.

        Returns:
            bool: Renvoie True si le port est ouvert, sinon False.
        """
        try:
            # Vérification de l'ouverture du port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((str(ip), port))
                return True
        except (socket.timeout, socket.error):
            return False
    
    @staticmethod
    def get_local_network():
        """
        Obtient le réseau local de l'hôte.
    
        Returns:
        str: Une chaîne représentant le réseau local en notation CIDR.
        """
        ip = socket.gethostbyname(socket.gethostname())
        # à remplacer, ceci est uniquement pour éviter les bugs si le pc est utilisé avec un autre réseau
        return '192.168.1.0/24'