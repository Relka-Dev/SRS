class Camera:
    """
    Classe représentant une caméra dans le système SRS.

    Attributs:
        idCamera (int): Identifiant unique de la caméra.
        ip (str): Adresse IP de la caméra.
        idNetwork (int): Identifiant du réseau auquel la caméra est connectée.
        jwt (str): Token JWT pour l'authentification de la caméra.
        positionX (float): Position X de la caméra sur le mur.
        idWall (int): Identifiant du mur où la caméra est installée.
        macAddress (str): Adresse MAC de la caméra.
        picture (str): Image associée à la caméra.
        persons_positions (list): Liste des positions des personnes détectées par la caméra.
    """

    def __init__(self, idCamera, ip, idNetwork, jwt, positionX, idWall, macAddress, picture, persons_positions):
        self._idCamera = idCamera
        self._ip = ip
        self._idNetwork = idNetwork
        self._jwt = jwt
        self._positionX = positionX
        self._idWall = idWall
        self._macAddress = macAddress
        self._picture = picture
        self._persons_positions = persons_positions

    @property
    def idCamera(self):
        return self._idCamera

    @idCamera.setter
    def idCamera(self, value):
        self._idCamera = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def idNetwork(self):
        return self._idNetwork

    @idNetwork.setter
    def idNetwork(self, value):
        self._idNetwork = value

    @property
    def jwt(self):
        return self._jwt

    @jwt.setter
    def jwt(self, value):
        self._jwt = value

    @property
    def positionX(self):
        return self._positionX

    @positionX.setter
    def positionX(self, value):
        self._positionX = value

    @property
    def idWall(self):
        return self._idWall

    @idWall.setter
    def idWall(self, value):
        self._idWall = value

    @property
    def macAddress(self):
        return self._macAddress

    @macAddress.setter
    def macAddress(self, value):
        self._macAddress = value

    @property
    def picture(self):
        return self._picture

    @picture.setter
    def picture(self, value):
        self._picture = value

    @property
    def persons_positions(self):
        return self._persons_positions

    @persons_positions.setter
    def persons_positions(self, value):
        if isinstance(value, list): 
            self._persons_positions = value
        else:
            raise ValueError("The persons_positions must be a list of positions.")
