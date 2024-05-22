import pytest
from math import isclose
from triangulation import Triangulation

def test_get_object_position_valid_angles():
    result, position = Triangulation.get_object_position(3, 30, -20)
    assert result == True
    assert isclose(position[0], 0.333, abs_tol=0.001)
    assert isclose(position[1], 1.243, abs_tol=0.001)

def test_get_object_position_equilateral_rectangle():
    result, position = Triangulation.get_object_position(3, 15, 15)
    assert result == True
    assert isclose(position[0], 1.5, abs_tol=0.001)
    assert isclose(position[1], 2.598, abs_tol=0.001)

def test_get_object_position_isosceles_rectangle():
    result, position = Triangulation.get_object_position(3, 30, 30, True)
    assert result == True
    assert isclose(position[0], 1.5, abs_tol=0.001)
    assert isclose(position[1], 5.598, abs_tol=0.001)

def test_get_object_position_angle_greater_than_90():
    result, message = Triangulation.get_object_position(3, 45, 50)
    assert result == False
    assert message == "Impossible de calculer la triangulation pour un angle supérieur à 90°"

def test_get_object_position_angle_less_than_0():
    result, message = Triangulation.get_object_position(3, -50, -50)
    assert result == False
    assert message == "Impossible de calculer la triangulation pour un angle inférieur à 90°"

def test_get_object_position_boundary_angles():
    result, position = Triangulation.get_object_position(3, 0, 0)
    assert result == True
    assert isclose(position[0], 1.5, abs_tol=0.001)
    assert isclose(position[1], 1.5, abs_tol=0.001)

if __name__ == "__main__":
    pytest.main()
