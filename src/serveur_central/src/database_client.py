"""
Auteur      : Karel Vilém Svoboda
Affiliation : CFPTi - SRS
Date        : 16.04.2024

Script      : database_client.py
Description : Client de la base de données
Version     : 0.1
"""

import mysql.connector

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
    
    def addCameras(self, cameras_ips_with_token : dict, networkIP : str, networkSubnetMask : str):
        networkId = self.getNetworkIdByIpAndSubnetMask(networkIP, networkSubnetMask)

        try:
            for camera in cameras_ips_with_token:
                
                if not self.checkIfCameraExists(camera, networkId):               
                    self.cursor.execute("INSERT INTO srs.Cameras (ip, idNetwork, JWT) VALUES(%s, %s, %s);", (camera, networkId, cameras_ips_with_token[camera]))
                    self.dbConnexion.commit()

            return True
        except Exception as e:
            print(f"Erreur lors de l'insertion dans la base de données: {e}")

        print(networkIP)

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
                return False, f"Impossible d'ajouter l'utilisateur : Le type de personne n'existe pas."
            
            if self.checkIfUsername(username):
                return False, f"Impossible d'ajouter l'utilisateur : Un utilisateur avec le même nom existe déjà dans la base"
            
            self.cursor.execute("INSERT INTO srs.Users (idPersonType, encodings, username) VALUES(%s, %s, %s);", (int(idPersonType), encodings, username))
            
            self.dbConnexion.commit()
            return True, "L'utilisateur a été ajouté avec succès."
        except Exception as e:
            print(f"Error: {e}")
            return False, f"Impossible d'ajouter l'utilisateur : {e}"

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






