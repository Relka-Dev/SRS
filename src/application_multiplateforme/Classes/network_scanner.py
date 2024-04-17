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
        
        ip_with_port_open = []
        for ip in self.network.hosts():
            if self.check_port(ip, port, timeout):
                if ServerClient(ip).ping_srs_server():
                    ip_with_port_open.append(str(ip))

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
        ip = socket.gethostbyname(socket.gethostname())
        return '.'.join(ip.split('.')[:-1]) + '.0/24'