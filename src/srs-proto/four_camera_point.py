"""
Classe FourCameraPoint pour la Surveillance Vidéo Multi-Caméras avec Détection de Points

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Cette classe représente un point détecté à partir de quatre caméras, en utilisant deux objets TwoCameraPoint pour
définir les points détectés par les caméras du bas et du haut. La classe permet de comparer deux objets FourCameraPoint
pour déterminer s'ils représentent le même point.

Fonctionnalités :
1. Stocke les points détectés par les caméras du bas et du haut via des objets TwoCameraPoint.
2. Stocke une valeur associée au point.
3. Permet la comparaison de deux objets FourCameraPoint pour vérifier s'ils représentent le même point détecté.

Méthodes :
- compare_points(fourCameraPoint): Compare les angles des points détectés pour déterminer si les points sont les mêmes.

Attributs :
- point_bot : Objet TwoCameraPoint représentant les points détectés par les caméras du bas.
- point_top : Objet TwoCameraPoint représentant les points détectés par les caméras du haut.
- value : Valeur associée au point.

Dépendances :
- Module two_camera_point contenant la classe TwoCameraPoint.

Utilisation :
Cette classe est conçue pour être utilisée dans des systèmes de surveillance vidéo multi-caméras où la triangulation
et la détection de points sont nécessaires pour suivre les objets dans un espace tridimensionnel.
"""

from two_camera_point import TwoCameraPoint

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
        if self.point_bot.angle_gauche == fourCameraPoint.point_bot.angle_gauche or self.point_bot.angle_droit == fourCameraPoint.point_bot.angle_droit:
            return True
        
        if self.point_top.angle_gauche == fourCameraPoint.point_top.angle_gauche or self.point_top.angle_droit == fourCameraPoint.point_top.angle_droit:
            return True
        
        return False