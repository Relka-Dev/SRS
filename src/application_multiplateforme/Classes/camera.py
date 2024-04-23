class Camera:

    def __init__(self, idCamera, ip, idNetwork, jwt, positionX, idWall, macAddress):
        self.idCamera = idCamera
        self._ip = ip
        self.idNetwork = idNetwork
        self.jwt = jwt
        self.positionX = positionX
        self.idWall = idWall
        self.macAddress = macAddress
    
    @property
    def ip(self):
        """Getter pour l'adresse IP"""
        return self._ip

    @ip.setter
    def ip(self, new_ip):
        """Setter pour l'adresse IP"""
        # Vous pouvez ajouter une validation d'adresse IP ici si nécessaire
        self._ip = new_ip