from two_camera_point import TwoCameraPoint
from four_camera_point import FourCameraPoint

class UniquePointList:
    def __init__(self):
        self._points = []

    def add_point(self, fourCameraPoint : FourCameraPoint):
        for point in self._points:
            if fourCameraPoint.compare_points(point):
                return False
        
        self._points.append(fourCameraPoint)
        return True
    
    @property
    def points(self):
        return self._points

    def __repr__(self):
        return f"UniquePointList(points={self.points})"