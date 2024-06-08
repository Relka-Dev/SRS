"""
Tests Unitaires pour la Classe Triangulation

Auteur : Karel Vilém Svoboda
Affiliation : CFPT Informatique
Version : 1.0
Date : 08.06.2024

Description :
Ce script contient des tests unitaires pour la classe Triangulation en utilisant pytest.
Il vérifie les calculs de positions d'objets basés sur les angles fournis, et la triangulation
des positions avec plusieurs ensembles d'angles provenant de différentes caméras.

Dépendances :
- pytest
- math (isclose)
- Triangulation (Classe à tester)
- UniquePointList (Classe pour stocker les points uniques)

Utilisation :
Assurez-vous que pytest et les modules nécessaires sont installés. Exécutez ce script pour valider
les calculs de la classe Triangulation.
"""

import pytest
from math import isclose
from triangulation import Triangulation
from unique_point_list import UniquePointList

def test_get_object_position_valid_angles():
    result, position = Triangulation.get_object_position(3, 30, -20)
    assert result == True
    assert isclose(position[0], 1.9052229112310002, abs_tol=0.001)
    assert isclose(position[1], 0.5105029404656191, abs_tol=0.001)

def test_get_object_position_equilateral_rectangle():
    result, position = Triangulation.get_object_position(3, 15, 15)
    assert result == True
    assert isclose(position[0], 2.25, abs_tol=0.001)
    assert isclose(position[1], 1.2990381056766578, abs_tol=0.001)

def test_get_object_position_isosceles_rectangle():
    result, position = Triangulation.get_object_position(3, 30, 30, True)
    assert result == True
    assert isclose(position[0], 2.7990381056766584, abs_tol=0.001)
    assert isclose(position[1], 0.75, abs_tol=0.001)

def test_get_object_position_angle_greater_than_90():
    result, message = Triangulation.get_object_position(3, 45, 50)
    assert result == False
    assert message == "Impossible de calculer la triangulation pour un angle supérieur à 90°"

def test_get_object_position_angle_less_than_0():
    result, message = Triangulation.get_object_position(3, -50, -50)
    assert result == False
    assert message == "Impossible de calculer la triangulation pour un angle supérieur à 90°"

def test_get_object_position_boundary_angles():
    result, position = Triangulation.get_object_position(3, 0, 0)
    assert result == True
    assert isclose(position[0], 1.5, abs_tol=0.001)
    assert isclose(position[1], 1.5, abs_tol=0.001)

def test_get_objects_positions():
    wall_length = 3
    objects_angles_from_bot_left = [0, -10]
    objects_angles_from_bot_right = [0, 10]
    objects_angles_from_top_left = [0, -20]
    objects_angles_from_top_right = [0, 20]
    tolerance = 1.5

    result, unique_point_list = Triangulation.get_objects_positions(
        wall_length,
        objects_angles_from_bot_left,
        objects_angles_from_bot_right,
        objects_angles_from_top_left,
        objects_angles_from_top_right,
        tolerance
    )

    assert result == True
    assert isinstance(unique_point_list, UniquePointList)
    assert len(unique_point_list.points) > 0

    # Verify that the points in the unique_point_list are within the tolerance range
    for point in unique_point_list.points:
        bot_point = point.point_bot
        top_point = point.point_top
        assert abs(bot_point.value[0] - top_point.value[0]) < tolerance
        assert abs(bot_point.value[1] - top_point.value[1]) < tolerance

if __name__ == "__main__":
    pytest.main()
