"""
Classe UniquePointList

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Cette classe représente une liste de points uniques détectés par quatre caméras. Chaque point est représenté par un 
objet FourCameraPoint, et la classe assure que seuls des points uniques sont ajoutés à la liste en comparant les 
nouvelles entrées avec les points existants.

Attributs :
- points : Une liste de points uniques représentés par des objets FourCameraPoint.

Méthodes :
- add_point : Ajoute un nouveau point à la liste s'il n'est pas déjà présent.
- points : Retourne la liste des points uniques.
- __repr__ : Représente la classe sous forme de chaîne de caractères.

Utilisation :
Cette classe est utilisée pour stocker et gérer des points uniques dans des systèmes de surveillance vidéo multi-caméras 
où la triangulation et la détection de points sont nécessaires pour suivre les objets dans un espace tridimensionnel.
"""

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