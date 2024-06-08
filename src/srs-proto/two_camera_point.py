"""
Classe TwoCameraPoint

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Cette classe représente un point détecté par deux caméras, spécifié par deux angles et une valeur associée.
Elle est utilisée pour faciliter la triangulation des positions d'objets dans un espace tridimensionnel.

Attributs :
- angle_gauche : Angle par rapport à la caméra gauche.
- angle_droit : Angle par rapport à la caméra droite.
- value : Coordonnées du point détecté.

Méthodes :
- angle_gauche : Retourne l'angle par rapport à la caméra gauche.
- angle_droit : Retourne l'angle par rapport à la caméra droite.
- value : Retourne les coordonnées du point détecté.

Utilisation :
Cette classe est conçue pour être utilisée en conjonction avec la classe FourCameraPoint pour la triangulation 
des positions d'objets détectés par plusieurs caméras.
"""

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