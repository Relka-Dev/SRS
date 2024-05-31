class TwoCameraPoint:
    def __init__(self, angle_gauche, angle_droit, value):
        self._angle_gauche = angle_gauche
        self._angle_droit = angle_droit
        self._value = value

    @property
    def angle_gauche(self):
        return self._angle_gauche

    @property
    def angle_droit(self):
        return self._angle_droit

    @property
    def value(self):
        return self._value