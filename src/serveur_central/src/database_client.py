"""
Auteur      : Karel Vilém Svoboda
Affiliation : CFPTi - SRS
Date        : 16.04.2024

Script      : database_client.py
Description : Client de la base de données
Version     : 0.1
"""

import mysql.connector
from datetime import datetime, timedelta
from network_scanner import NetworkScanner
from flask import json
import numpy as np

class DatabaseClient:
    
    def __init__(self, host, database, user, password):
        self.dbConnexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.dbConnexion.cursor()
    
    def isAdminTableEmpty(self):
        """
        Permet de savoir si un admin est déjà présent dans la base ou non

        Returns:
            bool : True = Vide / False = Données présentes
        """
        self.cursor.execute("SELECT * FROM Admin")
        results = self.cursor.fetchall()
    
        if len(results) == 0:
            return True
        else:
            return False
    
    def addAdmin(self, name: str, password: str):
        """
        Ajoute un administrateur à la base de données.

        Args:
            name (str): Le nom de l'administrateur à ajouter.
            password (str): Le mot de passe de l'administrateur à ajouter.
        """
        try:
            self.cursor.execute("INSERT INTO srs.Admin (Name, Password) VALUES (%s, %s);", (name, password))
            self.dbConnexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'insertion dans la base de données: {e}")
    
    def adminLogin(self, name: str, password: str):
        """
        Connexion d'un administrateur

        Args:
            name (str) : Le nom de l'administrateur à vérifier.
            password (str) : Le mot de passe de l'administrateur à vérifier.
        
        Returns:
            Si l'utilisateur est un admin alors True, sinon False.
        """
        try:
            self.cursor.execute("SELECT * FROM Admin WHERE Name = %s AND Password = %s", (name, password))
            
            results = self.cursor.fetchall()

            if len(results) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error during login: {e}")
            return False
        
    def checkIfNetworkExists(self, ip: str):
        try:
            self.cursor.execute("SELECT * FROM Network WHERE ip = %s", (ip,))
            results = self.cursor.fetchall()
    
            if len(results) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    
    def addNetwork(self, ip : str, submask : str):
        # Réseau déjà présent
        if self.checkIfNetworkExists(ip):
            return False
        
        try:
            self.cursor.execute("INSERT INTO srs.Network (ip, subnetMask) VALUES (%s, %s);", (ip, submask))
            self.dbConnexion.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'insertion dans la base de données: {e}")
    
    def getNetwork(self, idNetwork):
        try:
            self.cursor.execute("SELECT * FROM Network WHERE idNetwork = %s", (idNetwork,))
            results = self.cursor.fetchone()
    
            if results:
                return results
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def getNetworkIdByIpAndSubnetMask(self, ip : str, submask : str):
        try:
            self.cursor.execute("SELECT idNetwork FROM Network WHERE ip = %s AND subnetMask = %s", (ip, submask,))
            results = self.cursor.fetchone()
    
            if results:
                return results[0]
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def addCameras(self, cameras_ips_with_token : dict, networkId : str):

        try:
            for camera in cameras_ips_with_token:
                
                if not self.checkIfCameraExists(camera, networkId):               
                    self.cursor.execute("INSERT INTO srs.Cameras (ip, idNetwork, JWT) VALUES(%s, %s, %s);", (camera, networkId, cameras_ips_with_token[camera]))
                    self.dbConnexion.commit()

            return True
        except Exception as e:
            print(f"Erreur lors de l'insertion de la camera dans la base de données: {e}")


    def checkIfCameraExists(self, camera_ip: str, network_id : int):
        try:
            self.cursor.execute("SELECT * FROM Cameras WHERE ip = %s AND idNetwork = %s", (camera_ip, network_id))
            results = self.cursor.fetchall()
    
            if len(results) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def getPersonTypes(self):
        try:
            self.cursor.execute("SELECT * FROM PersonTypes")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
    
    def getWalls(self):
        try:
            self.cursor.execute("SELECT * FROM Walls")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
    
    def checkIfIdPersonTypeExist(self, idPersonType):
        try:
            
            self.cursor.execute("SELECT * FROM PersonTypes WHERE idPersonType = %s", (idPersonType,))
            print(idPersonType)
            results = self.cursor.fetchall()
    
            if len(results) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def checkIfUsername(self, username):
        try:
            self.cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            results = self.cursor.fetchall()
    
            if len(results) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    
    def addUser(self, idPersonType, encodings, username):
        try:
            if not self.checkIfIdPersonTypeExist(idPersonType):
                return False, "Le type de personne n'existe pas."
            if self.checkIfUsername(username):
                return False, "Un utilisateur avec le même nom existe déjà."
            
            # Convert encodings list to binary
            # encodings_binary = np.array(encodings, dtype=np.float32).tobytes()
            
            self.cursor.execute("INSERT INTO srs.Users (idPersonType, encodings, username) VALUES (%s, %s, %s);", (int(idPersonType), encodings, username))
            self.dbConnexion.commit()
            return True, "L'utilisateur a été ajouté avec succès."
        except Exception as e:
            return False, str(e)

    def getPersonTypeByName(self, typeName: str):
        try:
            self.cursor.execute("SELECT idPersonType FROM PersonTypes WHERE typeName = %s", (typeName,))
            result = self.cursor.fetchone()

            if result is None:
                return False, "Aucune correspondance trouvée"
            else:
                # Extracting the relevant data from the result
                idPersonType = result[0]

                # Returning a JSON serializable object
                return True, {'idPersonType': idPersonType}
        except Exception as e:
            print(f"Error: {e}")
            return False, str(e)
        
    def getCameras(self):
        try:
            self.cursor.execute("SELECT * FROM Cameras")
            return True, self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

    def updateCameraToken(self, idCamera, token):
        try:
            self.cursor.execute("UPDATE Cameras SET JWT = %s WHERE idCamera = %s", (str(token), idCamera,))
            self.dbConnexion.commit()
            return True, "Token de la caméra mis à jour avec succès."
        except Exception as e:
            print(f"Erreur lors de la mise à jour du token de la caméra  : {e}")
            return False, f"Erreur lors de la mise à jour du token de la caméra  : {e}"

    def refreshNetworkTimestamp(self, idNetwork):
        try:
            print(idNetwork)
            # Utilisez CURRENT_TIMESTAMP directement dans la requête SQL
            self.cursor.execute("UPDATE Network SET lastUpdate = CURRENT_TIMESTAMP WHERE idNetwork = %s", (idNetwork,))
            self.dbConnexion.commit()
            return True, "Dernière mise à jour modifiée avec succès"
        except Exception as e:
            return False, f"Erreur lors de la mise à jour de la dernière modification : {e}"



    def getByIdCameras(self, idCamera):
        try:
            self.cursor.execute("SELECT * FROM Cameras WHERE idCamera = %s", (idCamera,))
            return True, self.cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")

    def getCamerasByNetworkIpAndSubnetMask(self, ip, subnetMask):
        try:
            self.cursor.execute("SELECT * FROM Cameras c JOIN Network n ON c.idNetwork AND n.IdNetwork WHERE n.ip = %s AND n.subnetMask = %s", (ip, subnetMask,))
            results = self.cursor.fetchall()
    
            if results:
                return results
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def getCamerasByIdNetwork(self, id_network):
        try:
            self.cursor.execute("SELECT * FROM Cameras WHERE idNetwork = %s", (id_network,))
            results = self.cursor.fetchall()

            if results:
                return True, results
            else:
                return False, None
        except Exception as e:
            print(f"Error: {e}")
            return False

    
    def addCamerasToNetwork(self, cameras, idNetwork):
        try:
            for camera in cameras:
                ip = str(camera)
                token = str(cameras[camera])
                print(ip)
                self.cursor.execute("INSERT INTO Cameras (ip, idNetwork, JWT) VALUES (%s, %s, %s);", (ip, idNetwork, token))
            self.dbConnexion.commit()
            return True, "Cameras added to network successfully."
        except Exception as e:
            print(f"Error adding cameras to the network: {e}")
            return False, f"Error adding cameras to the network: {e}"

    def deleteCamerasFromNetwork(self, cameras, idNetwork):
        try:
            for camera_id in cameras:
                self.cursor.execute("DELETE FROM Cameras WHERE idCamera = %s AND idNetwork = %s", (str(camera_id[0]), str(idNetwork),))
            self.dbConnexion.commit()
            return True, "Cameras removed from the network successfully."
        except Exception as e:
            print(f"Error removing cameras from the network: {e}")
            return False, f"Error removing cameras from the network: {e}"


    def updateCameraByIdCameraAndIdNetwork(self, idCamera, idNetwork, positionX, idWall):
        try:
            self.cursor.execute("UPDATE srs.Cameras SET positionX = %s, idWall = %s WHERE idCamera = %s AND idNetwork = %s", (positionX, idWall, idCamera, idNetwork,))
            self.dbConnexion.commit()
            return True, "Caméra mise à jour avec succès."
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la caméra : {e}")
            return False, f"Erreur lors de la mise à jour de la caméra : {e}"
        
    

    
    
    def areTheCamerasInTheNetworkInNeedOfAnUpdate(self, idNetwork):
        network = self.getNetwork(idNetwork)

        return DatabaseClient.isOlderThan24Hours(str(network[3]))
    
    def updateUser(self, user_id, update_data):
        update_parts = ", ".join([f"{key} = %s" for key in update_data.keys()])
        values = list(update_data.values())
        values.append(user_id)
        try:
            self.cursor.execute(f"UPDATE Users SET {update_parts} WHERE idUser = %s", values)
            self.dbConnexion.commit()
            return True, "User updated successfully."
        except Exception as e:
            return False, str(e)
    
    def getUsers(self):
        """
        Retrieve all users from the database.
        """
        try:
            self.cursor.execute("SELECT idUser, username, idPersonType, encodings FROM Users")
            results = self.cursor.fetchall()
            users = [
                {
                    'idUser': user[0],
                    'username': user[1],
                    'idPersonType': user[2],
                    'encodings': json.loads(user[3]) if user[3] else None  # Load JSON string from database into Python list
                }
                for user in results
            ]
            return users
        except Exception as e:
            print(f"Error retrieving users: {e}")
            raise
        
    def deleteUser(self, user_id):
        try:
            self.cursor.execute("DELETE FROM Users WHERE idUser = %s", (user_id,))
            self.dbConnexion.commit()
            return True, "User deleted successfully."
        except Exception as e:
            return False, str(e)


    
    @staticmethod
    def isOlderThan24Hours(timestamp_input):
        timestamp = datetime.strptime(timestamp_input, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - timestamp
        return diff > timedelta(hours=24)






