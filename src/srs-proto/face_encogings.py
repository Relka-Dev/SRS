import mysql.connector

class DatabaseClient:
    
    def __init__(self):
        self.dbConnexion = mysql.connector.connect(
            host="127.0.0.1",
            user="srs-admin",
            password="fzg5jc29cHbKcSuK",
            database="srs"
        )
        self.cursor = self.dbConnexion.cursor()

    def getEncodings(self):
        try:
            self.cursor.execute("SELECT username, encodings FROM Users")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

print(DatabaseClient().getEncodings())