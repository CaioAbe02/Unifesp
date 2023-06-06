from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        return Builder.load_file('main_screen.kv')
