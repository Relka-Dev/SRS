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
        if len(self.camerasIPs) == 0:
            return None

        tokens = []
        for cameraip in self.camerasIPs:
            camera_url = "http://{ip}:{port}".format(ip = cameraip, port = self.__CAMERAS_SERVER_PORT)
            print(camera_url)
            auth = (self.__CLIENT_USERNAME, self.__CLIENT_PASSWORD)
            response = requests.get(f"{camera_url}/login", auth=auth)

            if response.status_code == 200:
                tokens.append(response.json().get('token'))
            else:
                print("Échec de l'obtention du token JWT pour l'ip : {ip}:".format(ip=cameraip), response.status_code)
            
        return tokens