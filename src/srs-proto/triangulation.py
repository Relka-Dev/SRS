import math

class Triangulation:

    @staticmethod
    def get_object_position(wall_length, object_angle_from_left, object_angle_from_right, debug=False, reverse=False):
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

        # Calcul de la position X
        position_y = distance_camera_object * math.sin(math.radians(alpha))


        # Calcul de la position Y
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

        return True, [position_x, position_y]
    

    def find_angle_from_top_left(position, wall_length):
        A = wall_length - position[1] # Distance Y entre la camera et l'objet
        B = position[0] # Distance X entre l'objet et la camera

        C = math.sqrt(A ** 2 + B ** 2) # Distance camera objet

        gamma = math.radians(90) # Angle droit entre A et B
        alpha = math.asin(math.sin(gamma) / C * A) # Angle entre la camera et l'objet
        return math.degrees(alpha)

    def find_angle_from_top_right(position, wall_length):
        A = wall_length - position[1] # Distance Y entre la camera et l'objet
        B = wall_length - position[0] # Distance X entre l'objet et la camera
        C = math.sqrt(A ** 2 + B ** 2) # Distance camera objet

        gamma = math.radians(90) # Angle droit entre A et B
        beta = math.asin(math.sin(gamma) / C * B) # Angle entre la camera et l'objet
        return math.degrees(beta)

    def get_objects_positions(wall_length, objects_angles_from_bot_left, objects_angles_from_bot_right, object_angles_from_top_left, object_angles_from_top_right, tolerence=10**-15):
        all_possible_points = []

        for left_object in objects_angles_from_bot_left:
            for right_object in objects_angles_from_bot_right:
                result, pointXY = Triangulation.get_object_position(wall_length, left_object, right_object)
                if result:
                    all_possible_points.append(pointXY)

        list_true_points_left = []
        list_true_points_right = []

        for possible_point in all_possible_points:
            for top_left_angle in object_angles_from_top_left:
                top_left_angle = 90/2 + top_left_angle
                angle_object_camera = Triangulation.find_angle_from_top_left(possible_point, wall_length)
                print(str(angle_object_camera) + " : "  + str(top_left_angle))
                if abs(angle_object_camera - top_left_angle) < tolerence:
                    list_true_points_left.append(possible_point)

            #for top_right_angle in object_angles_from_top_right:
            #    top_right_angle = 90/2 + top_right_angle
            #    angle_object_camera = Triangulation.find_angle_from_top_right(possible_point, wall_length)
            #    if abs(angle_object_camera - top_right_angle) < tolerence:
            #        list_true_points_right.append(possible_point)

        list_true_points = []

        list_true_points.append(list_true_points_left)

        #for left_object in list_true_points_left:
        #    for right_object in list_true_points_right:
        #        if left_object != right_object:
        #            list_true_points.append(right_object)    
            
        return list_true_points_left
    
    def convert_to_top_position(wall_length, objects_positions):
        #positions_from_top = []
        for position in objects_positions:
            print(position[0])
        #    positions_from_top.append((wall_length - position[0], wall_length - position[1]))
        #    print(position[0])
        #    print(position[1])

        return objects_positions
    
    def get_objects_positions_v2(wall_length, objects_angles_from_bot_left, objects_angles_from_bot_right, objects_angles_from_top_left, objects_angles_from_top_right, tolerence=10**-15):
        all_possible_points_bot = []
        all_possible_points_top = []

        for left_object_bot in objects_angles_from_bot_left:
            for right_object_bot in objects_angles_from_bot_right:
                result, pointXY = Triangulation.get_object_position(wall_length, left_object_bot, right_object_bot)
                if result:
                    all_possible_points_bot.append(pointXY)

        print(all_possible_points_bot)
        for left_object_top in objects_angles_from_top_left:
            for right_object_top in objects_angles_from_top_right:
                result, pointXY = Triangulation.get_object_position(wall_length, left_object_top, right_object_top)
                if result:
                    all_possible_points_top.append(pointXY)
        
        all_possible_points_top = Triangulation.convert_to_top_position(wall_length, all_possible_points_top)

        true_points = []
        for top_point in all_possible_points_top:
            for bot_point in all_possible_points_bot:
                print("Top :" + str(top_point))
                print("Bot :" + str(bot_point))
                if(abs(top_point[0] - bot_point[0]) < tolerence and abs(top_point[1] - bot_point[1]) < tolerence):
                    true_points.append([(top_point[0] + bot_point[0]) / 2, (top_point[1] + bot_point[1]) / 2])

        return true_points
            
                

# Définir la longueur du mur (en unités quelconques, par exemple mètres)
# wall_length = 10.0
# # 
# # Définir les angles des objets par rapport à la caméra de gauche (en degrés)
# objects_angles_from_bot_left = [-20, 15, 10]
# 
# # Définir les angles des objets par rapport à la caméra de droite (en degrés)
# objects_angles_from_bot_right = [-25, 12, 20]
# 
# #objects_angles_from_top_left = [39.587847211318405 - 45, 45.000000000000014 - 45, 62.465562540631474 - 45]
# objects_angles_from_top_left = [28.855030188101914 - 45, 63.94675178320236 - 45, 68.55727721216165 - 45]
# objects_angles_from_top_right = [32.72971691120047 - 45, 19.651290100757024 - 45, 39.587847211318405 - 45]
# 
# 
# # Appeler la fonction get_objects_positions
# positions = Triangulation.get_objects_positions(wall_length, objects_angles_from_bot_left, objects_angles_from_bot_right, objects_angles_from_top_left, objects_angles_from_top_right)

# # Afficher les positions des objets
# print("Positions des objets :")
# for position in positions:
#     print(f"X: {position[0]}, Y: {position[1]}")
##
#result, response = Triangulation.get_object_position(10, 15, 12, True)
#print(response)
#print(Triangulation.find_angle_from_top_left(response, 10))
#print(Triangulation.find_angle_from_top_right(response, 10))