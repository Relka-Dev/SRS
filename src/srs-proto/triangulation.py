import math
from two_camera_point import TwoCameraPoint
from four_camera_point import FourCameraPoint
from unique_point_list import UniquePointList

class Triangulation:

    @staticmethod
    def get_object_position(wall_length, object_angle_from_left, object_angle_from_right, debug=False, reverse=False):
        """
        Calcule la position d'un objet par rapport à une caméra en utilisant la triangulation.
        
        Args:
            wall_length: La longueur du mur sur lequel se trouve la caméra.
            object_angle_from_left: L'angle de l'objet par rapport à la caméra gauche.
            object_angle_from_right: L'angle de l'objet par rapport à la caméra droite.
            debug: Affiche les informations de débogage si True (par défaut False).
            reverse: Inverse les coordonnées de la position si True (par défaut False).
        
        Returns:
            Un tuple contenant un booléen indiquant le succès du calcul et les coordonnées [position_x, position_y] de l'objet,
            ou un message d'erreur si les angles sont invalides.
        """
        # Conversion des angles en radians
        alpha = 90 / 2 - object_angle_from_left
        beta = 90 / 2 + object_angle_from_right

        if beta > 90 or alpha > 90:
            return False, "Impossible de calculer la triangulation pour un angle supérieur à 90°"
        
        if beta < 0 or alpha < 0:
            return False, "Impossible de calculer la triangulation pour un angle inférieur à 90°"
        
        # Calcul de gamma
        gamma = 180 - alpha - beta

        # Calcul de la distance entre la caméra et l'objet
        distance_camera_object = wall_length / math.sin(math.radians(gamma)) * (math.sin(math.radians(beta)))

        # Calcul de la position Y
        position_y = distance_camera_object * math.sin(math.radians(alpha))


        # Calcul de la position X
        position_x = math.sqrt(distance_camera_object**2 - position_y**2)

        if reverse:
            position_x = wall_length - position_x
            position_y = wall_length - position_y

        if debug:
            print("alpha : " + str(alpha))
            print("beta : " + str(beta))
            print("gamma : " + str(gamma))
            print("cam_left -> object : " + str(distance_camera_object))
            print("position x : " + str(position_x))
            print("position y : " + str(position_y))

        print([position_x, position_y])

        return True, [position_x, position_y]

    @staticmethod
    def get_objects_positions(wall_length, objects_angles_from_bot_left, objects_angles_from_bot_right, object_angles_from_top_left, object_angles_from_top_right, tolerence=0.5):
        all_possible_points_bot = []

        for left_object_bot in objects_angles_from_bot_left:
            for right_object_bot in objects_angles_from_bot_right:
                result, pointXY = Triangulation.get_object_position(wall_length, left_object_bot, right_object_bot)
                if result:
                    all_possible_points_bot.append(TwoCameraPoint(left_object_bot, right_object_bot, pointXY))

        all_possible_points_top = []

        for left_object_top in object_angles_from_top_left:
            for right_object_top in object_angles_from_top_right:
                result, pointXY = Triangulation.get_object_position(wall_length, left_object_top, right_object_top, reverse=True)
                if result:
                   all_possible_points_top.append(TwoCameraPoint(left_object_top, right_object_top, pointXY))
        

        unique_point_list = UniquePointList()

        for possible_point_bot in all_possible_points_bot:
            for possible_point_top in all_possible_points_top:
                if(abs(possible_point_bot.value[0] - possible_point_top.value[0] < tolerence) and abs(possible_point_bot.value[1] - possible_point_top.value[1] < tolerence)):
                    unique_point_list.add_point(FourCameraPoint(possible_point_bot, possible_point_top, [(possible_point_bot.value[0] + possible_point_top.value[0]) / 2, (possible_point_bot.value[1] + possible_point_top.value[1]) / 2]))

        return True, unique_point_list