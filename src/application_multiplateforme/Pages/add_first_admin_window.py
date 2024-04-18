from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 

class AddFirstAdminWindow(Screen):
    server_ip = None
    server_client = None

    username = None
    password = None

    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
    
    def update_boutton(self):
        username = self.ids.username_textInput.text
        password = self.ids.password_textInput.text

        if username == "" or password == "":
            self.ids.submit_button.disabled = True
        else:
            self.ids.submit_button.disabled = False
    
    def add_admin(self):
        username = self.ids.username_textInput.text
        password = self.ids.password_textInput.text
        
        result, response = self.server_client.add_first_admin(username, password)

        if result:
            self.manager.current = "login"
        else:
            self.ids.status_label.text = response
            self.ids.status_label.color = (1, 0, 0, 1) 