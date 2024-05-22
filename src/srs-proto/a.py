import math

class Triangulation:

    @staticmethod
    def get_object_position(wall_length, object_angle_from_left, object_angle_from_right, debug=False):

        print(object_angle_from_left)
        print(object_angle_from_right)
        # Conversion des angles en radians
        alpha = 90 / 2 + object_angle_from_left
        beta = 90 / 2 + object_angle_from_right

        if beta > 90 or alpha > 90:
            return False, "Impossible de calculer la triangulation pour un angle supérieur à 90°"
        
        if beta < 0 or alpha < 0:
            return False, "Impossible de calculer la triangulation pour un angle inférieur à 90°"
        
        # Calcul de gamma
        gamma = 180 - alpha - beta

        # Calcul de la distance entre la caméra et l'objet
        distance_camera_object = wall_length * math.sin(math.radians(alpha)) / math.sin(math.radians(gamma))

        # Calcul de la position Y
        position_y = distance_camera_object * math.sin(math.radians(beta))

        # Calcul de la position X
        position_x = math.sqrt(distance_camera_object**2 - position_y**2)

        if debug:
            print("alpha : " + str(alpha))
            print("beta : " + str(beta))
            print("gamma : " + str(gamma))
            print("cam_left -> object : " + str(distance_camera_object))
            print("position x : " + str(position_x))
            print("position y : " + str(position_y))

        return True, [position_x, position_y]
    

    @staticmethod
    def get_objects_positions(wall_length, objects_angles_from_left, objects_angles_from_right):
        list_points_from_left = []
        list_points_from_right = []

        for left_angle in objects_angles_from_left:
            for right_angle in objects_angles_from_right:
                result, pointXY = Triangulation.get_object_position(wall_length, left_angle, right_angle)
                if result:
                    list_points_from_left.append(pointXY)

                result, pointXY = Triangulation.get_object_position(wall_length, right_angle, left_angle)
                if result:
                    list_points_from_right.append(pointXY)

        # Utiliser une tolérance pour comparer les points flottants
        tolerance = 0.001
        list_true_points = []

        i = 0
        while i < len(list_points_from_left):
            point_left = list_points_from_left[i]
            found_match = False
            j = 0
            while j < len(list_points_from_right):
                point_right = list_points_from_right[j]
                if (abs(point_left[0] - point_right[0]) < tolerance and
                    abs(point_left[1] - point_right[1]) < tolerance):
                    list_true_points.append(point_left)
                    list_points_from_right.pop(j)
                    list_points_from_left.pop(i)
                    break
                j += 1
            if found_match:
                list_points_from_left.pop(i)
            else:
                i += 1

        return list_true_points

# Définir la longueur du mur (en unités quelconques, par exemple mètres)
wall_length = 5.0

# Définir les angles des objets par rapport à la caméra de gauche (en degrés)
objects_angles_from_left = [9, -30]

# Définir les angles des objets par rapport à la caméra de droite (en degrés)
objects_angles_from_right = [-30, 9]

# Appeler la fonction get_objects_positions
positions = Triangulation.get_objects_positions(wall_length, objects_angles_from_left, objects_angles_from_right)

# Afficher les positions des objets
print("Positions des objets :")
for position in positions:
    print(f"X: {position[0]}, Y: {position[1]}")