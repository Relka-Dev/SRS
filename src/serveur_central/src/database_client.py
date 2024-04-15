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
        self.isAdminTableEmpty()
    
    def isAdminTableEmpty(self):
        self.cursor.execute("SELECT * FROM Admin")
        results = self.cursor.fetchall()
    
        if len(results) == 0:
            return True
        else:
            return False
        
        self.cursor.close()
        self.dbConnexion.close()
