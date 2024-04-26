from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

class UpdateUserWindow(Screen):
    selected_user = None

    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()
        status, users = self.server_client.get_users()
        self.users = users

        success, person_types = self.server_client.get_person_types()
        if success:
            self.update_person_type_spinner([pt[1] for pt in person_types]) 
        else:
            self.update_person_type_spinner(["Failed to retrieve types"])

        user_details = [user.username for user in users] if status else ["Failed to retrieve users"]
        self.update_user_spinner(user_details)


    def update_user_spinner(self, user_details):
        self.ids.user_spinner.values = user_details
        self.ids.user_spinner.text = user_details[0] if user_details else "No users found"
        self.ids.user_spinner.disabled = not user_details
    
    def update_person_type_spinner(self, type_details):
        self.ids.person_type_spinner.values = type_details
        self.ids.person_type_spinner.text = type_details[0] if type_details else "No types found"
        self.ids.person_type_spinner.disabled = not type_details

    
    def user_changed(self, text_user_selected):
        self.selected_user = next((user for user in self.users if user.username == text_user_selected), None)
        enable = bool(self.selected_user)
        self.ids.username_textInput.text = self.selected_user.username if enable else ''
        self.ids.username_textInput.disabled = not enable
        self.ids.take_picture_button.disabled = not enable
        self.ids.update_user_button.disabled = not enable
        self.ids.delete_user_button.disabled = not enable

        if self.selected_user:
            user_type_id = self.selected_user._idPersonType
            type_name = self.get_type_name_by_id(user_type_id)

            self.ids.person_type_spinner.text = type_name if type_name else "Type de personne non trouvé"
            self.ids.person_type_spinner.disabled = False
        else:
            self.ids.person_type_spinner.text = "Sélectionnez un utilisateur"
            self.ids.person_type_spinner.disabled = True


    
    def get_type_name_by_id(self, type_id):
        result, person_types = self.server_client.get_person_types()
        if result:
            for person_type in person_types:
                if person_type[0] == type_id:
                    return person_type[1]
        return None
    
    def delete_user(self, instance):
        self.popup.dismiss()
        if self.selected_user:
            success, message = self.server_client.delete_user(self.selected_user.user_id)
            if success:
                self.ids.status_label.text = "Utilisateur supprimé avec succès."
                self.refresh_user_list()
            else:
                self.ids.status_label.text = "Échec de la suppression : " + message
        else:
            self.ids.status_label.text = "Aucun utilisateur sélectionné."

    def refresh_user_list(self):
        status, users = self.server_client.get_users()
        if status:
            user_details = [user.username for user in users]
        else:
            user_details = ["Failed to retrieve users"]
        self.update_user_spinner(user_details)
        self.users = users 


    def show_delete_confirmation(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        buttons = BoxLayout(size_hint_y=None, height='50dp')

        content.add_widget(Label(text='Êtes-vous sûr de vouloir supprimer cet utilisateur ?'))

        btn_yes = Button(text='Oui', on_release=self.delete_user)
        btn_no = Button(text='Non', on_release=lambda *x: self.popup.dismiss())

        buttons.add_widget(btn_yes)
        buttons.add_widget(btn_no)

        content.add_widget(buttons)
        self.popup = Popup(title='Confirmation de suppression',
                           content=content,
                           size_hint=(None, None), size=('400dp', '200dp'),
                           auto_dismiss=False)
        self.popup.open()

