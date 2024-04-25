class Camera:
    def __init__(self, idCamera, ip, idNetwork, jwt, positionX, idWall, macAddress):
        self._idCamera = idCamera
        self._ip = ip
        self._idNetwork = idNetwork
        self._jwt = jwt
        self._positionX = positionX
        self._idWall = idWall
        self._macAddress = macAddress

    @property
    def idCamera(self):
        """Getter for the camera ID"""
        return self._idCamera

    @idCamera.setter
    def idCamera(self, value):
        """Setter for the camera ID"""
        self._idCamera = value

    @property
    def ip(self):
        """Getter for the IP address"""
        return self._ip

    @ip.setter
    def ip(self, new_ip):
        """Setter for the IP address"""
        # Add IP validation if necessary
        self._ip = new_ip

    @property
    def idNetwork(self):
        """Getter for the network ID"""
        return self._idNetwork

    @idNetwork.setter
    def idNetwork(self, value):
        """Setter for the network ID"""
        self._idNetwork = value

    @property
    def jwt(self):
        """Getter for the JWT token"""
        return self._jwt

    @jwt.setter
    def jwt(self, new_jwt):
        """Setter for the JWT token"""
        self._jwt = new_jwt

    @property
    def positionX(self):
        """Getter for the X position"""
        return self._positionX

    @positionX.setter
    def positionX(self, value):
        """Setter for the X position"""
        self._positionX = value

    @property
    def idWall(self):
        """Getter for the wall ID"""
        return self._idWall

    @idWall.setter
    def idWall(self, value):
        """Setter for the wall ID"""
        self._idWall = value

    @property
    def macAddress(self):
        """Getter for the MAC address"""
        return self._macAddress

    @macAddress.setter
    def macAddress(self, value):
        """Setter for the MAC address"""
        self._macAddress = value
