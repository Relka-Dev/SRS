import requests
import hashlib
import re
import json
import socket

from Classes.camera import Camera

class ServerClient:
    __SERVER_PORT = 4299

    def __init__(self, server_ip : str):
        self.server_ip = server_ip
        self.server_url = "http://{ip}:{port}".format(ip = self.server_ip, port = self.__SERVER_PORT)
        self.initialize_token = None
        self.API_token = None

    def ping_srs_server(self):
        if not self.server_ip:
            return False
        
        response = requests.get(f"{self.server_url}/ping")

        if response.status_code == 200:
            return True
        else:
            return False

    def is_server_set_up(self):
        if not self.server_ip:
            return False
        
        response = requests.get(f"{self.server_url}/is_set_up")

        if response.status_code == 200:
            return True
        else:
            return False
        
    def initialize_login(self, username, password):
        if not self.server_ip:
            return False
        
        endpoint_url = f"{self.server_url}/initialize"
        auth = (username, password)
        
        response = requests.get(endpoint_url, auth=auth)

        if response.status_code == 200:
            self.initialize_token = response.json().get("token")
            return True, "Initialisation réussie"
        elif response.status_code == 403:
            return False, "Identifiants de connexion erronés."
        elif response.status_code == 402:
            return False, "Impossible d'ajouter l'admin quand un autre est déjà présent."
        else:
            print(f"Erreur inattendue: {response.status_code}")
            return False, "Erreur inattendue"
    
    def add_first_admin(self, admin_name: str, clear_password: str):
        if not self.server_ip:
            return False, "ip du serveur manquante"
        
        is_strong, message = ServerClient.check_password_strength(clear_password)

        if not is_strong:
            return False, message

        hashed_password = ServerClient.hash_password(clear_password)
        endpoint_url = f"{self.server_url}/first_admin"
        params = {
            "username": admin_name,
            "password": hashed_password,
            "token": self.initialize_token
        }

        response = requests.post(endpoint_url, params=params)

        if response.status_code == 201:
            return True, "Admin ajouté avec succès."
        else:
            return False, response.json()
        
    def admin_login(self, admin_name : str, clear_password : str):
        if not self.server_ip:
            return False, "IP du serveur manquante"

        hashed_password = ServerClient.hash_password(clear_password)
        endpoint_url = f"{self.server_url}/admin_login"
        auth = (admin_name, hashed_password)

        response = requests.post(endpoint_url, auth=auth)

        if response.status_code == 200:
            self.API_token = response.json().get("token")
            print(self.API_token)
            return True, "Authentification réussie"
        elif response.status_code == 403:
            return False, "Aucun administrateur n'est présent dans le système."
        elif response.status_code == 400:
            return False, "Les identifiants de connexion sont erronés."
        else:
            return False, "Erreur inattendue lors de la tentative de connexion."
        
    def get_person_types(self):
        if not self.server_ip:
            return False
        
        params = {
            "token": self.API_token
        }
        
        endpoint_url = f"{self.server_url}/person_types"
        response = requests.get(endpoint_url, params=params)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response
    
    def add_user(self, username, idPersonType, encodings):
        if not self.server_ip:
            return False, "ip du serveur manquante"

        endpoint_url = f"{self.server_url}/add_user"

        encodings_list = [encoding.tolist() for encoding in encodings]

        data = {
            "username": username,
            "idPersonType": idPersonType,
            "encodings": encodings_list,
        }

        # Encoder les données en JSON
        data_json = json.dumps(data)

        url_with_token = f"{endpoint_url}?token={self.API_token}"

        response = requests.post(url_with_token, data=data_json)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    
    def get_person_types_by_name(self, typeName : str):
        if not self.server_ip:
            return False
        
        params = {
            "token": self.API_token,
            "typeName": typeName
        }
        
        endpoint_url = f"{self.server_url}/person_type_by_name"
        response = requests.get(endpoint_url, params=params)

        if response.status_code == 200:
            return True, response.json()['message']['idPersonType']
        else:
            return False, response
        
    def get_walls(self):
        if not self.server_ip:
            return False
        
        params = {
            "token": self.API_token
        }
        
        endpoint_url = f"{self.server_url}/walls"
        response = requests.get(endpoint_url, params=params)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response
        
    def get_cameras(self):
        if not self.server_ip:
            return False
        
        print(ServerClient.get_netowk_from_ip(self.server_ip))
        
        params = {
            "token": self.API_token,
            "ip": ServerClient.get_netowk_from_ip(self.server_ip),
            "subnetMask": 24
        }
        
        endpoint_url = f"{self.server_url}/cameras"
        response = requests.get(endpoint_url, params=params)

        if response.status_code == 201:

            response_data = response.content.decode('utf-8')
            cameras_data = json.loads(response_data)

            cameras = []
            for camera in cameras_data:

                cameras.append(Camera(camera[0],camera[1],camera[2],camera[3],camera[4],camera[5],camera[6]))

            return True, cameras
        else:
            return False, response

        
    @staticmethod
    def hash_password(password : str):
        password_bytes = password.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(password_bytes)
        hashed_password = hasher.hexdigest()
        return hashed_password
    
    @staticmethod
    def check_password_strength(password):
        
        # Au moins 8 charactères
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères."

        # Au moins une majuscule et une minuscule
        if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
            return False, "Le mot de passe doit contenir au moins une lettre majuscule et une lettre minuscule."

        # Au moins un chiffre
        if not re.search("[0-9]", password):
            return False, "Le mot de passe doit contenir au moins un chiffre."

        # Au moins un charactère spécial.
        if not re.search("[!@#$%^&*()-_=+{};:,<.>]", password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial parmi !@#$%^&*()-_=+{};:,<.>."

        return True, "Le mot de passe est robuste."
    
    @staticmethod
    def get_netowk_from_ip(ip):
        return '.'.join(ip.split('.')[:-1]) + ".0"
    
