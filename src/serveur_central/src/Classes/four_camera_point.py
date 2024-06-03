from Classes.two_camera_point import TwoCameraPoint

class FourCameraPoint:
    def __init__(self, point_bot: TwoCameraPoint, point_top: TwoCameraPoint, value):
        self._point_bot = point_bot
        self._point_top = point_top
        self._value = value

    @property
    def point_bot(self):
        return self._point_bot

    @property
    def point_top(self):
        return self._point_top
    
    @property
    def value(self):
        return self._value
    
    def compare_points(self, fourCameraPoint):
        #true : same point

        if self.point_bot.angle_gauche == fourCameraPoint.point_bot.angle_gauche or self.point_bot.angle_droit == fourCameraPoint.point_bot.angle_droit:
            return True
        
        if self.point_top.angle_gauche == fourCameraPoint.point_top.angle_gauche or self.point_top.angle_droit == fourCameraPoint.point_top.angle_droit:
            return True
        
        return False