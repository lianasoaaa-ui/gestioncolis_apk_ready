# GESTION DES COLIS MADAGASCAR - APK VERSION
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(text="APP EN CONSTRUCTION APK"))

class MonApp(App):
    def build(self):
        return Root()

if __name__ == "__main__":
    MonApp().run()
