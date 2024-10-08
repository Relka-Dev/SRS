"""
Auteur      : Karel Vilém Svoboda
Affiliation : CFPTi - SRS
Date        : 09.06.2024

Script      : app.py
Description : Serveur central du projet SRS
            : Routes pour l'API
Version     : 1
"""

from flask import Flask, jsonify, request, json, Response
from database_client import DatabaseClient
from jwt_library import JwtLibrary
from camera_server_client import CameraServerClient
from network_scanner import NetworkScanner
import asyncio
import cv2
import numpy as np
import re
import torch
import base64
from PIL import Image
import io

from Classes.network import Network
from Classes.camera import Camera
from space_recognition import SpaceRecognition

class ServeurCentral:
    # Constantes de l'application
    DB_HOST = "127.0.0.1"
    DB_NAME = "srs"
    DB_USER = "srs-admin"
    DB_PASSWORD = "fzg5jc29cHbKcSuK"

    # Identifiants pour la première initialisation
    DEFAULT_USERNAME = "admin"
    DEFAULT_PASSWORD = "super"

    def __init__(self):
        self.app = Flask(__name__)
        self.db_client = None
        self.cameraServerClient = None
        self.spaceRecognition = SpaceRecognition()
        self.initialize_routes()
    
    def initialize_routes(self):
        self.db_client = DatabaseClient(self.DB_HOST, self.DB_NAME, self.DB_USER, self.DB_PASSWORD)

        # Routes ping
        self.app.add_url_rule('/ping', 'ping', self.ping, methods=['GET'])
        self.app.add_url_rule('/is_set_up', 'is_set_up', self.is_set_up, methods=['GET'])
        
        # Routes liées à l'initialisation
        self.app.add_url_rule('/initialize', 'initialize', self.initialize, methods=['GET'])
        self.app.add_url_rule('/first_admin', 'first_admin', self.first_admin, methods=['POST'])
        self.app.add_url_rule('/admin_login', 'admin_login', self.admin_login, methods=['POST'])
        # Routes sécurisés disponibles uniquement pour les administrateurs
        self.app.add_url_rule('/add_network', 'add_network', self.add_network, methods=['POST'])
        self.app.add_url_rule('/cameras_data', 'cameras_data', self.cameras_data, methods=['GET'])
        self.app.add_url_rule('/person_types', 'person_types', self.person_types, methods=['GET'])
        self.app.add_url_rule('/person_type_by_name', 'person_type_by_name', self.person_type_by_name, methods=['GET'])
        self.app.add_url_rule('/add_user', 'add_user', self.add_user, methods=['POST'])
        self.app.add_url_rule('/walls', 'walls', self.walls, methods=['GET'])
        self.app.add_url_rule('/cameras', 'cameras', self.cameras, methods=['GET'])
        self.app.add_url_rule('/update_camera_list', 'update_camera_list', self.update_camera_list, methods=['GET'])
        self.app.add_url_rule('/update_camera', 'update_camera', self.update_camera, methods=['PUT'])
        self.app.add_url_rule('/update_user', 'update_user', self.update_user, methods=['PUT'])
        self.app.add_url_rule('/delete_user', 'delete_user', self.delete_user, methods=['DELETE'])
        self.app.add_url_rule('/get_users', 'get_users', self.get_users, methods=['GET'])
        self.app.add_url_rule('/get_users', 'get_users', self.get_users, methods=['GET'])

        self.app.add_url_rule('/calibration', 'calibration', self.calibration, methods=['GET'])

    
    def ping(self):
        return jsonify({'Ping Success': 'SRS server'}), 200
    
    def is_set_up(self):
        if self.db_client.isAdminTableEmpty():
            return jsonify({'erreur': 'Le serveur n\'est pas configuré'}), 400
        else:
            return jsonify({'message': 'Le serveur est configuré'}), 200

    # Routes liées à l'initialisation
    def initialize(self):
        """
        Route d'initialisation du projet, sert à récupérer le JWT pour l'initialisation
        """
        auth = request.authorization
        # Vérification des crendentials de l'authentification
        if auth and auth.password == self.DEFAULT_PASSWORD and auth.username == self.DEFAULT_USERNAME:
            # Vérification si la table administrateur est libre pour des question de sécurité
            if self.db_client.isAdminTableEmpty():
                return jsonify({'token': JwtLibrary.generateJwtForInitialization(auth.username)}), 200
            else:
                return jsonify({'erreur': 'Impossible d\'ajouter l\'admin quand un autre est déjà présent.'}), 402
        else:
            return jsonify({'erreur': 'Identifiants de connexion manquants ou erronés (utilisez basic auth)'}), 403

    @JwtLibrary.initialization_token_required    
    def first_admin(self):
        """
        Route permettant d'ajouter le premier administrateur, requert le token du premier login
        """
        if self.db_client.isAdminTableEmpty():
            username = request.args.get('username')
            password = request.args.get('password')

            if password and username:
                # Ajout des données dans la bdd
                self.db_client.addAdmin(username, password)
                return jsonify({'message': 'L\'admin a été ajouté'}), 201
            else:
                return jsonify({'erreur': 'Mauvais paramètres, utilisez (username, password) pour le nom d\'utilisateur et le mot de passe respectivement.'}), 400
        else:
            return jsonify({'erreur': 'Impossible d\'ajouter l\'admin quand un autre est déjà présent.'}), 402

    def admin_login(self):
        """
        Permet à l'administrateur de se connecter. Retourne un JWT si tout est ok.
        """
        if self.db_client.isAdminTableEmpty():
            return jsonify({'erreur': 'Aucun administrateur n\'est présent dans le système.'}), 403
        
        auth = request.authorization

        # Vérification des données de connexion
        if self.db_client.adminLogin(auth.username, auth.password):
            return jsonify({'token': JwtLibrary.generateJwtForAPI(auth.username)}), 200
        else:
            return jsonify({'erreur': 'Les identifiants de connexion sont erronés'}), 400
            
        
    # Routes sécurisés disponibles uniquement pour les administrateurs

    @JwtLibrary.API_token_required
    def add_network(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        if not ip or not subnetMask:
            return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\ip du réseau et le masque de sous-réseau respectivement.'}), 400
        
        if not NetworkScanner.is_network_valid("{n}/{sub}".format(n = ip, sub = subnetMask)):
            return jsonify({'erreur': 'Le réseau fournit n\'est pas valide ou n\'est pas accessible'}), 400
        
        if not self.db_client.addNetwork(ip, subnetMask):
            return jsonify({'erreur': 'Le réseau fournit est est déjà dans la base de données'}), 400

    @JwtLibrary.API_token_required
    def cameras_data(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        if not ip or not subnetMask:
            return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\ip du réseau et le masque de sous-réseau respectivement.'}), 400

        self.cameraServerClient = CameraServerClient(ip, subnetMask)

        self.cameraServerClient.lookForCameras()
        tokens_for_ip = self.cameraServerClient.getCamerasTokens()

        self.db_client.addCameras(tokens_for_ip, ip, subnetMask)

        return jsonify({'tokens' : tokens_for_ip})

    
    @JwtLibrary.API_token_required
    def person_types(self):
        return jsonify(self.db_client.getPersonTypes()), 200
    
    @JwtLibrary.API_token_required
    def walls(self):
        try:
            return jsonify(self.db_client.getWalls()), 200
        except Exception as e:
            return jsonify({'erreur' : str(e)}), 500
    
    @JwtLibrary.API_token_required
    def add_user(self):
        try:
            data_json = request.data.decode('utf-8')
            data = json.loads(data_json)

            idPersonType = data.get('idPersonType')
            encodings = data.get('encodings')
            username = data.get('username')

            print(json.dumps(encodings))

            result, response = self.db_client.addUser(idPersonType, json.dumps(encodings), username)

            if result:
                return jsonify({'message' : response}), 200
            else:
                return jsonify({'erreur' : response}), 400
        except Exception as e:
            # Afficher l'erreur précise
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
            # Retourner une réponse avec un code de statut 500 (Erreur interne du serveur)
            return jsonify({'erreur' : str(e)}), 500

    
    @JwtLibrary.API_token_required
    def person_type_by_name(self):
        typeName = request.args.get('typeName')

        result, response = self.db_client.getPersonTypeByName(typeName)

        if result:
            return jsonify({'message' : response}), 200
        else:
            return jsonify({'erreur' : response}), 400
        
    
    @JwtLibrary.API_token_required
    def cameras(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        if not ip or not subnetMask:
            return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\ip du réseau et le masque de sous-réseau respectivement.'}), 400

        if not NetworkScanner.is_network_valid("{n}/{sub}".format(n = ip, sub = subnetMask)):
            return jsonify({'erreur': 'Le réseau donné est inavalide'}), 400
        

        self.cameraServerClient = CameraServerClient(ip, subnetMask)

        networkId = self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask)

        # Vérification si le réseau n'existe pas
        # Recherche automatique de caméras, vérification la présence des caméras et ajout dans la base.
        if(not self.db_client.checkIfNetworkExists(ip)):
            return self.intialise_network_with_cameras(ip, subnetMask)
        
        cameras = self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)
        # Si aucune camera n'est dans le network, recheche de cameras.
        if cameras == None:
            return self.initialize_cameras_in_network(ip, subnetMask)
        
        # Vérification si la durée de vie des JWT des cameras est dépassée
        if self.db_client.areTheCamerasInTheNetworkInNeedOfAnUpdate(networkId):
            for camera in cameras:
                result, camera_data = self.db_client.getByIdCameras(camera[0])

                self.db_client.updateCameraToken(camera_data[0], self.cameraServerClient.getCameraToken(camera[1]))
            
            self.db_client.refreshNetworkTimestamp(networkId)
        
        return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)), 201
    
    @JwtLibrary.API_token_required
    def update_camera_list(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        if not ip or not subnetMask:
            return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\'ip du réseau et le masque de sous-réseau respectivement.'}), 401

        if not NetworkScanner.is_network_valid("{n}/{sub}".format(n=ip, sub=subnetMask)):
            
            return jsonify({'erreur': 'Le réseau donné est invalide'}), 402

        cameraServerClient = CameraServerClient(ip, subnetMask)
        networkId = self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask)

        if not self.db_client.checkIfNetworkExists(ip):
            return self.intialise_network_with_cameras(ip, subnetMask)

        # Utilisation d'un event loop pour exécuter la recherche des caméras de manière asynchrone
        loop = asyncio.new_event_loop()     
        asyncio.set_event_loop(loop)
        cameras_in_network = loop.run_until_complete(cameraServerClient.lookForCameras())
        loop.close()

        # Après la récupération des adresses IP des caméras, obtenir les tokens associés
        tokens_for_ip = cameraServerClient.getCamerasTokens()

        cameras_in_db = self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)

        cameras_to_add = ServeurCentral.get_cameras_that_are_not_in_database(tokens_for_ip, cameras_in_db)

        cameras_to_remove = ServeurCentral.get_cameras_that_are_not_in_network(cameras_in_network, cameras_in_db)

        if cameras_to_add:
            self.db_client.addCamerasToNetwork(cameras_to_add, networkId)
        if cameras_to_remove:
            self.db_client.deleteCamerasFromNetwork(cameras_to_remove, networkId)

        return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)), 201



    @JwtLibrary.API_token_required
    def update_camera(self):
        idCamera = request.args.get('idCamera')
        idNetwork = request.args.get('idNetwork')
        positionX = request.args.get('positionX')
        idWall = request.args.get('idWall')
    
        if not idCamera or not idNetwork or not positionX or not idWall:
            return jsonify({'erreur': 'Paramètres manquants, veuillez fournir idCamera, idNetwork, positionX et idWall'}), 400
    
        result, message = self.db_client.updateCameraByIdCameraAndIdNetwork(idCamera, idNetwork, positionX, idWall)
    
        if result:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'erreur': message}), 500


    @staticmethod
    def get_cameras_that_are_not_in_database(network_cameras, database_cameras):
        """
        Cette fonction prend en entrée deux listes : une liste de caméras de réseau et une liste de caméras de base de données.
        Elle retourne une liste des caméras de réseau qui ne sont pas présentes dans la base de données.

        :param network_cameras: Liste des caméras de réseau. Chaque caméra est représentée par une liste contenant une adresse IP (IPv4Address) et un token.
        :param database_cameras: Liste des caméras de la base de données. Chaque caméra est représentée par une liste contenant une adresse IP (IPv4Address) et un token.
        :return: Liste des caméras de réseau qui ne sont pas dans la base de données. Chaque caméra est représentée par une liste contenant une adresse IP (str) et un token.
        """

        result_camera_list = []

        # Affectation des listes si aucune donnée n'est présente
        if network_cameras is None:
            network_cameras = []
        if database_cameras is None:
            database_cameras = []

        # Extraction des tokens des caméras dans la base de données pour les comparer
        database_camera_tokens = [str(db_camera[1]) for db_camera in database_cameras]

        for network_camera in network_cameras:
            ip_address_str = str(network_camera[0])
            print(f"ip adress network: {ip_address_str}")
            print(f"database data = {database_camera_tokens}")

            if ip_address_str not in database_camera_tokens:
                print("match")
                result_camera_list.append([ip_address_str, network_camera[1]])

        return result_camera_list

    @staticmethod
    def get_cameras_that_are_not_in_network(network_cameras, database_cameras):
        if network_cameras is None:
            network_cameras = []
        if database_cameras is None:
            database_cameras = []
        
        result_camera_list = []
        pattern = r"'(.*?)'"
        network_cameras = re.findall(pattern, str(network_cameras))

        for database_camera in database_cameras:
            if database_camera[1] not in network_cameras:
                result_camera_list.append(database_camera)
        return result_camera_list


    @JwtLibrary.API_token_required
    def update_user(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        try:
            data = request.json
            user_id = data.get('idUser')
            new_username = data.get('username')
            new_idPersonType = data.get('idPersonType')
            new_encodings = data.get('encodings')

            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400

            update_data = {}
            if new_username:
                update_data['username'] = new_username
            if new_idPersonType:
                update_data['idPersonType'] = new_idPersonType
            if new_encodings:
                update_data['encodings'] = json.dumps(new_encodings)

            if not update_data:
                return jsonify({'error': 'No new data provided for update'}), 400

            result, message = self.db_client.updateUser(user_id, update_data)
            if result:
                return jsonify({'message': message}), 200
            else:
                return jsonify({'error': message}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @JwtLibrary.API_token_required
    def get_users(self):
        """
        Retrieve user data from the database.
        """
        try:
            users = self.db_client.getUsers()
            return jsonify(users), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @JwtLibrary.API_token_required
    def delete_user(self):
        try:
            user_id = request.args.get('idUser')
            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400
    
            result, message = self.db_client.deleteUser(user_id)
            if result:
                return jsonify({'message': message}), 200
            else:
                return jsonify({'error': message}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @JwtLibrary.API_token_required
    def calibration(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        idNetwork = self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask)

        if not idNetwork:
            print("id Network manquant")
            return jsonify({'error': 'Network ID is required'}), 400
            

        response = []
        result, response = self.db_client.getCamerasByIdNetwork(idNetwork)
        if not result:
            return jsonify({'error': 'Camera not found'}), 404

        cameras_angles = []
        for data in response:
            camera = Camera(data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, None)
            resultImg, responseImg = CameraServerClient.getCameraImage(camera.ip, camera.jwt)

            if resultImg:
                angles_and_sizes = self.spaceRecognition.get_persons_angles_with_size(responseImg, 62.2)
                cameras_angles.append({
                    'camera_ip': camera.ip,
                    'angles_and_sizes': [{'angle': float(angle), 'size_y': float(size_y)} for angle, size_y in angles_and_sizes]
                })

        return jsonify(cameras_angles), 200
    
    def intialise_network_with_cameras(self, networkip, subnetMask):
        # Recherche automatique des cameras
        loop = asyncio.new_event_loop()     
        asyncio.set_event_loop(loop)
        # cameras_in_network = loop.run_until_complete(self.cameraServerClient.lookForCameras())
        loop.close()
        # Donne la liste des ip des cameras ainsi que leurs tokens
        tokens_for_ip = self.cameraServerClient.getCamerasTokens()
        if(tokens_for_ip == None):
            return jsonify({'erreur' : 'Aucune caméra active n\'est présente sur le réseau'}), 400
        
        self.db_client.addNetwork(networkip, subnetMask)
        self.db_client.addCameras(tokens_for_ip, self.db_client.getNetworkIdByIpAndSubnetMask(networkip, subnetMask))
        return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(networkip, subnetMask)), 201
    
    def initialize_cameras_in_network(self, networkip, subnetMask):
        # Recherche automatique des cameras
        self.cameraServerClient.lookForCameras()
        # Donne la liste des ip des cameras ainsi que leurs tokens
        tokens_for_ip = self.cameraServerClient.getCamerasTokens()
        if(tokens_for_ip == None):
            return jsonify({'erreur' : 'Aucune caméra active n\'est présente sur le réseau'}), 400
        
        self.db_client.addCameras(tokens_for_ip, self.db_client.getNetworkIdByIpAndSubnetMask(networkip, subnetMask))
        return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(networkip, subnetMask)), 201


    def run(self):
        self.app.run(host='0.0.0.0', port=4299)

if __name__ == '__main__':
    my_app = ServeurCentral()
    my_app.run()
