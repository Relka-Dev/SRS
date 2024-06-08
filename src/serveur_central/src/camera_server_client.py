"""
Classe CameraServerClient

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Cette classe permet de gérer les interactions avec des caméras sur un réseau local. Elle inclut des méthodes pour 
scanner le réseau, récupérer des tokens d'authentification, obtenir des images et vidéos des caméras.

Attributs :
- __CLIENT_USERNAME : Nom d'utilisateur pour l'authentification des caméras.
- __CLIENT_PASSWORD : Mot de passe pour l'authentification des caméras.
- __CAMERAS_SERVER_PORT : Port utilisé par les caméras.

Méthodes :
- lookForCameras : Scanne le réseau pour trouver les caméras.
- getCamerasTokens : Récupère les tokens d'authentification des caméras.
- getCameraImage : Récupère une image d'une caméra spécifiée.
- getCameraVideo : Récupère une vidéo d'une caméra spécifiée.
- getCameraToken : Récupère le token d'authentification d'une caméra.
- getCamerasData : Méthode placeholder pour récupérer les données des caméras.

Utilisation :
Cette classe est conçue pour être utilisée dans des systèmes de surveillance pour gérer et contrôler des caméras IP.
"""

from network_scanner import NetworkScanner
import requests
from requests.exceptions import RequestException
import cv2
import numpy as np
import asyncio

class CameraServerClient:
    __CLIENT_USERNAME = 'SRS-Server'
    __CLIENT_PASSWORD = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
    __CAMERAS_SERVER_PORT = 4298


    def __init__(self, network : str, subnetMask=24):
        """
        Initialise la classe avec le réseau et le masque de sous-réseau spécifiés.

        Args:
            network (str): Le réseau à scanner.
            subnetMask (int): Le masque de sous-réseau.
        """
        self.network = network
        self.subnetMask = subnetMask
        self.networkScanner = NetworkScanner("{n}/{sub}".format(n = network, sub = subnetMask))

    async def lookForCameras(self):
        """
        Scanne le réseau pour trouver les caméras sur le port spécifié.

        Returns:
            list: Une liste des adresses IP des caméras trouvées.
        """
        self.camerasIPs = await self.networkScanner.scan_ips(self.__CAMERAS_SERVER_PORT)
        return self.camerasIPs
    
    def getCamerasTokens(self):
        """
        Récupère les tokens d'authentification des caméras.

        Returns:
            list: Une liste de tuples contenant l'adresse IP de la caméra et son token d'authentification.
        """
        cameraIPs = self.camerasIPs
        if not cameraIPs:
            return None
    
        tokens_for_ip = []
        for cameraip in cameraIPs:
            camera_url = f"http://{cameraip}:{self.__CAMERAS_SERVER_PORT}/login"
            response = requests.get(camera_url, auth=(self.__CLIENT_USERNAME, self.__CLIENT_PASSWORD))
    
            if response.status_code == 200:
                tokens_for_ip.append([cameraip, response.json().get('token')])
            else:
                print(f"Échec de l'obtention du token JWT pour l'ip : {cameraip}:", response.status_code)
    
        return tokens_for_ip
    
    @staticmethod
    def getCameraImage(ip, jwt):
        """
        Récupère une image d'une caméra spécifiée.

        Args:
            ip (str): L'adresse IP de la caméra.
            jwt (str): Le token d'authentification.

        Returns:
            tuple: Un booléen indiquant le succès de l'opération et l'image récupérée.
        """
        url = f"http://{ip}:{CameraServerClient.__CAMERAS_SERVER_PORT}/image"
        params = {'token': jwt}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            image_data = np.frombuffer(response.content, np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            if image is not None:
                return True, image
            else:
                print("Failed to decode image")
                return False, None
        else:
            print(f"Failed to get image from camera: {response.status_code}")
            return False, None
    
    @staticmethod
    def getCameraVideo(ip_camera, JWT):
        """
        Récupère une vidéo d'une caméra spécifiée.

        Args:
            ip_camera (str): L'adresse IP de la caméra.
            JWT (str): Le token d'authentification.

        Returns:
            tuple: Un booléen indiquant le succès de l'opération et le contenu de la vidéo ou un message d'erreur.
        """
        camera_url = f"http://{ip_camera}:{CameraServerClient.__CAMERAS_SERVER_PORT}/video_base64?token={JWT}"
        try:
            response = requests.get(camera_url)
            if response.status_code == 200:
                return True, response.content
            else:
                return False, f"Échec de la récupération de la video pour l'ip : {ip_camera}. Statut : {response.status_code}"
        except RequestException as e:
            return False, f"Erreur de connexion avec la caméra à l'ip : {ip_camera}. Détail de l'erreur : {str(e)}"

    @staticmethod
    def getCameraToken(cameraIp):
        """
        Récupère le token d'authentification d'une caméra.

        Args:
            cameraIp (str): L'adresse IP de la caméra.

        Returns:
            str: Le token d'authentification de la caméra.
        """
        camera_url = "http://{ip}:{port}".format(ip = cameraIp, port = CameraServerClient.__CAMERAS_SERVER_PORT)
        auth = (CameraServerClient.__CLIENT_USERNAME, CameraServerClient.__CLIENT_PASSWORD)
        response = requests.get(f"{camera_url}/login", auth=auth)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print("Échec de l'obtention du token JWT pour l'ip : {ip}:".format(ip=cameraIp), response.status_code)