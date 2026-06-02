# =====================================================
# GESTION DES COLIS MADAGASCAR - VERSION APK STABLE
# =====================================================

from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from datetime import datetime
import json
import os

Window.clearcolor = (1,1,1,1)

# =====================================================
# FICHIERS
# =====================================================

FICHIER_COLIS = "colis.json"
FICHIER_USER = "users.json"

# =====================================================
# VILLES
# =====================================================

villes_madagascar = [
    "Antananarivo", "Toamasina", "Mahajanga",
    "Fianarantsoa", "Toliara", "Antsiranana",
    "Antsirabe", "Morondava", "Sambava",
    "Nosy Be", "Ambanja", "Antsalaka"
]

# =====================================================
# USERS
# =====================================================

def charger_users():
    if os.path.exists(FICHIER_USER):
        try:
            with open(FICHIER_USER, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def sauvegarder_users(data):
    with open(FICHIER_USER, "w") as f:
        json.dump(data, f)

# =====================================================
# LOGIN
# =====================================================

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="CONNEXION", font_size=30, color=(0,0,1,1)))

        self.username = TextInput(hint_text="Nom utilisateur", multiline=False, height=50, size_hint_y=None)
        self.password = TextInput(hint_text="Mot de passe", password=True, multiline=False, height=50, size_hint_y=None)

        btn_login = Button(text="SE CONNECTER", size_hint_y=None, height=60, background_color=(0,1,0,1))
        btn_register = Button(text="CREER COMPTE", size_hint_y=None, height=60, background_color=(0,0.5,1,1))

        btn_login.bind(on_press=self.login)
        btn_register.bind(on_press=self.register)

        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(btn_login)
        layout.add_widget(btn_register)

        self.add_widget(layout)

    def login(self, instance):
        users = charger_users()
        user = self.username.text.strip()
        pwd = self.password.text.strip()

        if user in users and users[user] == pwd:
            self.manager.current = "gestion"
        else:
            Popup(title="Erreur", content=Label(text="Login incorrect"), size_hint=(0.7,0.3)).open()

    def register(self, instance):
        users = charger_users()

        user = self.username.text.strip()
        pwd = self.password.text.strip()

        if not user or not pwd:
            Popup(title="Erreur", content=Label(text="Champs vides"), size_hint=(0.7,0.3)).open()
            return

        if user in users:
            Popup(title="Erreur", content=Label(text="Utilisateur existe"), size_hint=(0.7,0.3)).open()
            return

        users[user] = pwd
        sauvegarder_users(users)

        Popup(title="OK", content=Label(text="Compte créé"), size_hint=(0.7,0.3)).open()

# =====================================================
# GESTION COLIS
# =====================================================

class GestionColis(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.colis_data = self.charger_donnees()

        self.search = TextInput(hint_text="Recherche...", size_hint_y=None, height=50)
        self.search.bind(text=self.rechercher_colis)

        self.add_widget(self.search)

        scroll = ScrollView()
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        scroll.add_widget(self.layout)
        self.add_widget(scroll)

        self.afficher_listes()

    # =====================================================
    # DATA
    # =====================================================

    def charger_donnees(self):
        if os.path.exists(FICHIER_COLIS):
            try:
                with open(FICHIER_COLIS, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def sauvegarder_donnees(self):
        with open(FICHIER_COLIS, "w") as f:
            json.dump(self.colis_data, f)

    # =====================================================
    # ADD SIMPLE TEST COLIS (IMPORTANT POUR TEST APK)
    # =====================================================

    def ajouter_test(self):
        colis = {
            "date": str(datetime.now()),
            "numero": "TEST001",
            "mpandefa": "Jean",
            "mpaka": "Marie",
            "toerana": "Antananarivo",
            "prix": "10000"
        }
        self.colis_data.append(colis)
        self.sauvegarder_donnees()
        self.afficher_listes()

    # =====================================================
    # AFFICHAGE
    # =====================================================

    def afficher_listes(self):
        self.layout.clear_widgets()

        for colis in self.colis_data:

            card = BoxLayout(orientation='vertical', size_hint_y=None, height=200)

            texte = Label(text=str(colis), color=(0,0,0,1))

            btn = Button(text="IMPRIMER (TXT)", size_hint_y=None, height=40)
            btn.bind(on_press=lambda x, c=colis: self.imprimer(c))

            card.add_widget(texte)
            card.add_widget(btn)

            self.layout.add_widget(card)

    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher_colis(self, instance, value):
        self.layout.clear_widgets()

        for colis in self.colis_data:
            if value.lower() in str(colis).lower():
                self.layout.add_widget(Label(text=str(colis)))

    # =====================================================
    # IMPRESSION SAFE ANDROID
    # =====================================================

    def imprimer(self, colis):
        try:
            dossier = os.path.join(os.getcwd(), "impressions")
            if not os.path.exists(dossier):
                os.makedirs(dossier)

            file_path = os.path.join(dossier, f"{colis.get('numero','colis')}.txt")

            with open(file_path, "w", encoding="utf-8") as f:
                for k, v in colis.items():
                    f.write(f"{k} : {v}\n")

            Popup(title="OK", content=Label(text="Fichier créé"), size_hint=(0.7,0.3)).open()

        except Exception as e:
            Popup(title="Erreur", content=Label(text=str(e)), size_hint=(0.7,0.3)).open()

# =====================================================
# SCREEN
# =====================================================

class GestionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GestionColis())

class LoginScreen(Screen):
    pass

# =====================================================
# APP
# =====================================================

class MonApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(GestionScreen(name="gestion"))
        sm.current = "login"
        return sm

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    MonApp().run()