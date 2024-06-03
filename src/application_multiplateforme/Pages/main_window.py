from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image

class MainWindow(Screen):     
    def on_enter(self):
        super().on_enter()
        self.app = App.get_running_app()
        self.server_client = self.app.get_server_client()

    def show_about_popup(self):
        # Layout pour l'image et le texte
        content_layout = BoxLayout(orientation='horizontal')
        
        # Image à gauche
        image = Image(source='Ressources/cfpt.png', size_hint=(0.3, 1), keep_ratio=True, allow_stretch=True)
        content_layout.add_widget(image)
        
        # Texte à droite de l'image
        text_layout = BoxLayout(orientation='vertical')
        text_layout.add_widget(Label(text="Système de Reconnaissance Spatiale\nVersion : 1.0\nDéveloppé par : Karel Vilém Svoboda\nAffiliation : CFPT Informatique\n©2023-2024"))
        
        # Ajout du texte au layout principal
        content_layout.add_widget(text_layout)
        
        # Bouton de fermeture
        close_button = Button(text="Fermer", size_hint=(1, 0.2))
        main_content = BoxLayout(orientation='vertical')
        main_content.add_widget(content_layout)
        main_content.add_widget(close_button)

        # Création de la pop-up
        popup = Popup(title='À propos', content=main_content, size_hint=(0.8, 0.5))
        close_button.bind(on_release=popup.dismiss)
        popup.open()