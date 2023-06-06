from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder

class MainScreen(MDScreen):
    pass

class MyApp(MDApp):
    def build(self):
        return Builder.load_file('main_screen.kv')

MyApp().run()
