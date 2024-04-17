import socket
import ipaddress
import subprocess
import re
    
class NetworkScanner:
    def __init__(self, network):
        self.network = ipaddress.IPv4Network(network)

    def scan_ips(self, port,  timeout=0.01):
        ip_with_port_open = []
        for ip in self.network.hosts():
            if self.check_port(ip, port, timeout):
                ip_with_port_open.append(str(ip))

        return ip_with_port_open

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
    def is_network_valid(network : str):
        """
        Vérifie si un réseau spécifié est valide.

        La fonction commence par vérifier si le réseau est conforme puis ping le routeur pour vérifier que le réseau est disponible.

        Args:
            network (str): réseau à vérifier.

        Returns:
            bool: Renvoie True si le réseau est valide, sinon False.
        """

        try:
            ipaddress.IPv4Network(network)
        except ValueError:
            return False
        
        # Ajout de 1 au dernier charactère
        ip, mask = network.split('/')

        router_ip = ip[:-1] + '1'

        try:
            # Ping du routeur
            timeout = 0.1
            result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), router_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False