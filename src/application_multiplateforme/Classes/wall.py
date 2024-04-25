class Wall:
    def __init__(self, idWall, wallName):
        self._idWall = idWall
        self._wallName = wallName

    @property
    def idWall(self):
        """Getter for the wall ID"""
        return self._idWall

    @idWall.setter
    def idWall(self, value):
        """Setter for the wall ID"""
        self._idWall = value

    @property
    def wallName(self):
        """Getter for the wall name"""
        return self._wallName

    @wallName.setter
    def wallName(self, value):
        """Setter for the wall name"""
        self._wallName = value
