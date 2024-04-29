import asyncio
import ipaddress
import socket
import subprocess

class NetworkScanner:
    def __init__(self, network):
        self.network = ipaddress.IPv4Network(network)

    async def scan_ips(self, port, timeout=0.35):
        tasks = [self.check_port(str(ip), port, timeout) for ip in self.network.hosts()]
        results = await asyncio.gather(*tasks)
        ip_with_port_open = [ip for ip, is_open in zip(self.network.hosts(), results) if is_open]
        return ip_with_port_open

    async def check_port(self, ip, port, timeout):
        """
        Asynchronously checks if a specified port on a given IP address is open.
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