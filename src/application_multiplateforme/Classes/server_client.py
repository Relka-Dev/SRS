import requests

class ServerClient:
    __SERVER_PORT = 4299

    def __init__(self, server_ip : str):
        self.server_ip = server_ip
        self.server_url = "http://{ip}:{port}".format(ip = self.server_ip, port = self.__SERVER_PORT)

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
        
        print(f"{self.server_url}/is_set_up")
        response = requests.get(f"{self.server_url}/is_set_up")


        if response.status_code == 200:
            return True
        else:
            return False