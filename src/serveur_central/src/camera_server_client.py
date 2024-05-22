from network_scanner import NetworkScanner
import requests
from requests.exceptions import RequestException
import asyncio

class CameraServerClient:
    __CLIENT_USERNAME = 'SRS-Server'
    __CLIENT_PASSWORD = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
    __CAMERAS_SERVER_PORT = 4298


    def __init__(self, network : str, subnetMask=24):
        self.network = network
        self.subnetMask = subnetMask
        self.networkScanner = NetworkScanner("{n}/{sub}".format(n = network, sub = subnetMask))

    async def lookForCameras(self):
        self.camerasIPs = await self.networkScanner.scan_ips(self.__CAMERAS_SERVER_PORT)
        return self.camerasIPs
    
    def getCamerasTokens(self, cameraIPs):
        if not cameraIPs:
            return None
    
        tokens_for_ip = {}
        for cameraip in cameraIPs:
            camera_url = f"http://{cameraip}:{self.__CAMERAS_SERVER_PORT}/login"
            response = requests.get(camera_url, auth=(self.__CLIENT_USERNAME, self.__CLIENT_PASSWORD))
    
            if response.status_code == 200:
                tokens_for_ip[cameraip] = response.json().get('token')
            else:
                print(f"Échec de l'obtention du token JWT pour l'ip : {cameraip}:", response.status_code)
    
        return tokens_for_ip
    
    @staticmethod
    def getCameraImage(ip_camera, JWT):
        camera_url = f"http://{ip_camera}:{CameraServerClient.__CAMERAS_SERVER_PORT}/image?token={JWT}"
        try:
            response = requests.get(camera_url)
            if response.status_code == 200:
                return True, response.content
            else:
                return False, f"Échec de la récupération de l'image pour l'ip : {ip_camera}. Statut : {response.status_code}"
        except RequestException as e:
            return False, f"Erreur de connexion avec la caméra à l'ip : {ip_camera}. Détail de l'erreur : {str(e)}"
    
    @staticmethod
    def getCameraVideo(ip_camera, JWT):
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
        camera_url = "http://{ip}:{port}".format(ip = cameraIp, port = CameraServerClient.__CAMERAS_SERVER_PORT)
        auth = (CameraServerClient.__CLIENT_USERNAME, CameraServerClient.__CLIENT_PASSWORD)
        response = requests.get(f"{camera_url}/login", auth=auth)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print("Échec de l'obtention du token JWT pour l'ip : {ip}:".format(ip=cameraIp), response.status_code)

    def getCamerasData(self):
        cameras = []

        
