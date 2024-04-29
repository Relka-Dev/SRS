from network_scanner import NetworkScanner
import requests

class CameraServerClient:
    __CLIENT_USERNAME = 'SRS-Server'
    __CLIENT_PASSWORD = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
    __CAMERAS_SERVER_PORT = 4298


    def __init__(self, network : str, subnetMask : str):
        self.network = network
        self.subnetMask = subnetMask
        self.networkScanner = NetworkScanner("{n}/{sub}".format(n = network, sub = subnetMask))

    def lookForCameras(self):
        self.camerasIPs = self.networkScanner.scan_ips(self.__CAMERAS_SERVER_PORT)
        return self.camerasIPs
    
    def getCamerasTokens(self):
        if not self.camerasIPs:  # Plus pythonique pour vérifier si la liste est vide
            return None
    
        tokens_for_ip = {}
        for cameraip in self.camerasIPs:
            camera_url = f"http://{cameraip}:{self.__CAMERAS_SERVER_PORT}/login"
            response = requests.get(camera_url, auth=(self.__CLIENT_USERNAME, self.__CLIENT_PASSWORD))
    
            if response.status_code == 200:
                tokens_for_ip[cameraip] = response.json().get('token')
            else:
                print(f"Échec de l'obtention du token JWT pour l'ip : {cameraip}:", response.status_code)
    
        return tokens_for_ip

    
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

        
