"""
Classe NetworkScanner

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Scanne un réseau pour détecter les adresses IP avec des ports ouverts en utilisant des méthodes asynchrones.

Attributs :
- network : Réseau IPv4 à scanner.

Méthodes :
- scan_ips : Scanne les adresses IP avec un port spécifié ouvert.
- check_port : Vérifie asynchronement si un port est ouvert sur une adresse IP.
- lookForCameras : Scanne le réseau pour les caméras sur un port spécifié.
- is_network_valid : Vérifie si un réseau est valide et accessible.
"""

import asyncio
import ipaddress
import socket
import subprocess

class NetworkScanner:
    def __init__(self, network):
        """
        Initialise la classe avec un réseau spécifié.

        Args:
            network (str): Le réseau à scanner.
        """
        self.network = ipaddress.IPv4Network(network)

    async def scan_ips(self, port, timeout=0.35):
        """
        Scanne les adresses IP du réseau pour vérifier si un port spécifique est ouvert.

        Args:
            port (int): Le port à vérifier sur chaque adresse IP.
            timeout (float): Le temps d'attente maximum pour une réponse.

        Returns:
            list: Une liste des adresses IP avec le port spécifié ouvert.
        """
        tasks = [self.check_port(str(ip), port, timeout) for ip in self.network.hosts()]
        results = await asyncio.gather(*tasks)
        ip_with_port_open = [ip for ip, is_open in zip(self.network.hosts(), results) if is_open]
        return ip_with_port_open

    async def check_port(self, ip, port, timeout):
        """
        Vérifie asynchronement si un port est ouvert sur une adresse IP donnée.

        Args:
            ip (str): L'adresse IP à vérifier.
            port (int): Le port à vérifier.
            timeout (float): Le temps d'attente maximum pour une réponse.

        Returns:
            bool: Renvoie True si le port est ouvert, sinon False.
        """
        conn = asyncio.open_connection(ip, port)
        try:
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False

    async def lookForCameras(self, port):
        """
        Scanne le réseau pour détecter les caméras sur un port spécifié.

        Args:
            port (int): Le port à vérifier pour les caméras.

        Returns:
            list: Une liste des adresses IP des caméras trouvées.
        """
        return await self.scan_ips(port)
        
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
            timeout = 0.5
            result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), router_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False