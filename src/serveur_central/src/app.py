"""
Auteur      : Karel Vilém Svoboda
Affiliation : CFPTi - SRS
Date        : 28.03.2024

Script      : app.py
Description : Serveur central du projet SRS
            : Routes pour l'API
Version     : 0.1
"""

from flask import Flask, jsonify, request
from database_client import DatabaseClient
from jwt_library import JwtLibrary
from camera_server_client import CameraServerClient
from network_scanner import NetworkScanner

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
                return jsonify({'message': JwtLibrary.generateJwtForInitialization(auth.username)}), 200
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
        if not self.db_client.isAdminTableEmpty():
            username = request.args.get('username')
            password = request.args.get('password')
            
            if not username or not password:
                return jsonify({'erreur': 'Mauvais paramètres, utilisez (username, password) pour le nom d\'utilisateur et le mot de passe respectivement.'}), 400
            
            # Vérification des données de connexion
            if self.db_client.adminLogin(username, password):
                return jsonify({'token': JwtLibrary.generateJwtForAPI(username)}), 200
            else:
                return jsonify({'erreur': 'Les identifiants de connexion sont erronés'}), 400
        else:
            return jsonify({'erreur': 'Aucun administrateur n\'est présent dans le système.'}), 403
        
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
        
        return jsonify({'tkt': 'ok'}), 200

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


    def run(self):
        self.app.run(host='0.0.0.0', port=4299)

if __name__ == '__main__':
    my_app = ServeurCentral()
    my_app.run()
