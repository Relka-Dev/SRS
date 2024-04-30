from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 

class LoginWindow(Screen):    
    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_ip = self.app.get_server_ip()
        self.server_client = self.app.get_server_client()

    def update_boutton(self):
        username = self.ids.username_textInput.text
        password = self.ids.password_textInput.text

        if username == "" or password == "":
            self.ids.submit_button.disabled = True
        else:
            self.ids.submit_button.disabled = False

    def login(self):
        username = self.ids.username_textInput.text
        password = self.ids.password_textInput.text

        if username is None or password is None:
            return False
    
        result, response = self.server_client.admin_login(username, password)
    
        if result:

            self.manager.current = "main"
        else:
            self.ids.status_label.text = response
            self.ids.status_label.color = (1, 0, 0, 1) 